import json
from typing import Optional, Union

from azure.ai.inference.models import (
    CompletionsFinishReason,
    ImageContentItem,
    ImageUrl,
    TextContentItem,
    ToolMessage,
    UserMessage,
)
from nonebot.adapters import Bot, Event
from nonebot.log import logger
from nonebot.matcher import (
    Matcher,
    current_bot,
    current_event,
    current_handler,
    current_matcher,
)
from nonebot.typing import T_State
from nonebot_plugin_alconna.uniseg import UniMessage, UniMsg
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

from .config import config
from .constants import SUPPORT_IMAGE_MODELS
from .instances import target_list, tools
from .models import MarshoContext
from .plugin.func_call.caller import get_function_calls
from .plugin.func_call.models import SessionContext
from .util import (
    extract_content_and_think,
    get_backup_context,
    get_image_b64,
    get_nickname_by_user_id,
    get_prompt,
    make_chat_openai,
    parse_richtext,
)


class MarshoHandler:
    def __init__(
        self,
        client: AsyncOpenAI,
        context: MarshoContext,
    ):
        self.client = client
        self.context = context
        self.bot: Bot = current_bot.get()
        self.event: Event = current_event.get()
        self.state: T_State = current_handler.get().state
        self.matcher: Matcher = current_matcher.get()
        self.message_id: str = UniMessage.get_message_id(self.event)
        self.target = UniMessage.get_target(self.event)

    async def process_user_input(
        self, user_input: UniMsg, model_name: str
    ) -> Union[str, list]:
        """
        处理用户输入为可输入 API 的格式，并添加昵称提示
        """
        is_support_image_model = (
            model_name.lower()
            in SUPPORT_IMAGE_MODELS + config.marshoai_additional_image_models
        )
        usermsg = [] if is_support_image_model else ""
        user_nickname = await get_nickname_by_user_id(self.event.get_user_id())
        if user_nickname:
            nickname_prompt = f"此消息的说话者为: {user_nickname}"
        else:
            nickname_prompt = ""
        for i in user_input:  # type: ignore
            if i.type == "text":
                if is_support_image_model:
                    usermsg += [TextContentItem(text=i.data["text"] + nickname_prompt).as_dict()]  # type: ignore
                else:
                    usermsg += str(i.data["text"] + nickname_prompt)  # type: ignore
            elif i.type == "image":
                if is_support_image_model:
                    usermsg.append(  # type: ignore
                        ImageContentItem(
                            image_url=ImageUrl(  # type: ignore
                                url=str(await get_image_b64(i.data["url"]))  # type: ignore
                            )  # type: ignore
                        ).as_dict()  # type: ignore
                    )  # type: ignore
                    logger.info(f"输入图片 {i.data['url']}")
                elif config.marshoai_enable_support_image_tip:
                    await UniMessage(
                        "*此模型不支持图片处理或管理员未启用此模型的图片支持。图片将被忽略。"
                    ).send()
        return usermsg  # type: ignore

    async def handle_single_chat(
        self,
        user_message: Union[str, list],
        model_name: str,
        tools: list,
        with_context: bool = True,
    ) -> ChatCompletion:
        """
        处理单条聊天
        """

        context_msg = (
            get_prompt(model_name)
            + (self.context.build(self.target.id, self.target.private))
            if with_context
            else ""
        )
        response = await make_chat_openai(
            client=self.client,
            msg=context_msg + [UserMessage(content=user_message).as_dict()],  # type: ignore
            model_name=model_name,
            tools=tools,
        )
        return response

    async def handle_function_call(
        self,
        completion: ChatCompletion,
    ):
        # function call
        # 需要获取额外信息，调用函数工具
        tool_msg = []
        choice = completion.choices[0]
        while choice.message.tool_calls is not None:
            # await UniMessage(str(response)).send()
            tool_calls = choice.message.tool_calls
            # try:
            #     if tool_calls[0]["function"]["name"].startswith("$"):
            #         choice.message.tool_calls[0][
            #             "type"
            #         ] = "builtin_function"  # 兼容 moonshot AI 内置函数的临时方案
            # except:
            #     pass
            tool_msg.append(choice.message)
            for tool_call in tool_calls:
                try:
                    function_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    function_args = json.loads(
                        tool_call.function.arguments.replace("'", '"')
                    )
                # 删除args的placeholder参数
                if "placeholder" in function_args:
                    del function_args["placeholder"]
                logger.info(
                    f"调用函数 {tool_call.function.name.replace('-', '.')}\n参数:"
                    + "\n".join([f"{k}={v}" for k, v in function_args.items()])
                )
                await UniMessage(
                    f"调用函数 {tool_call.function.name.replace('-', '.')}\n参数:"
                    + "\n".join([f"{k}={v}" for k, v in function_args.items()])
                ).send()
                # TODO 临时追加插件函数，若工具中没有则调用插件函数
                if tools.has_function(tool_call.function.name):
                    logger.debug(f"调用工具函数 {tool_call.function.name}")
                    func_return = await tools.call(
                        tool_call.function.name, function_args
                    )  # 获取返回值
                else:
                    if caller := get_function_calls().get(tool_call.function.name):
                        logger.debug(f"调用插件函数 {caller.full_name}")
                        # 权限检查，规则检查 TODO
                        # 实现依赖注入，检查函数参数及参数注解类型，对Event类型的参数进行注入
                        func_return = await caller.with_ctx(
                            SessionContext(
                                bot=self.bot,
                                event=self.event,
                                state=self.state,
                                matcher=self.matcher,
                            )
                        ).call(**function_args)
                    else:
                        logger.error(
                            f"未找到函数 {tool_call.function.name.replace('-', '.')}"
                        )
                        func_return = (
                            f"未找到函数 {tool_call.function.name.replace('-', '.')}"
                        )
                tool_msg.append(
                    ToolMessage(tool_call_id=tool_call.id, content=func_return).as_dict()  # type: ignore
                )
                #  tool_msg[0]["tool_calls"][0]["type"] = "builtin_function"
                # await UniMessage(str(tool_msg)).send()
            request_msg = context_msg + [UserMessage(content=usermsg).as_dict()] + tool_msg  # type: ignore
            response = await make_chat_openai(
                client=client,
                model_name=model_name,
                msg=request_msg,  # type: ignore
                tools=(
                    tools_lists if tools_lists else None
                ),  # TODO 临时追加函数，后期优化
            )
            choice = response.choices[0]
            # 当tool_calls非空时，将finish_reason设置为TOOL_CALLS
            if choice.message.tool_calls is not None:
                choice.finish_reason = CompletionsFinishReason.TOOL_CALLS
        if choice.finish_reason == CompletionsFinishReason.STOPPED:

            # 对话成功 添加上下文
            context.append(
                UserMessage(content=usermsg).as_dict(), self.target.id, self.target.private  # type: ignore
            )
            # context.append(tool_msg, self.target.id, self.target.private)
            choice_msg_dict = choice.message.to_dict()
            if "reasoning_content" in choice_msg_dict:
                del choice_msg_dict["reasoning_content"]
            context.append(choice_msg_dict, self.target.id, self.target.private)

            # 发送消息
            if config.marshoai_enable_richtext_parse:
                await (await parse_richtext(str(choice.message.content))).send(
                    reply_to=True
                )
            else:
                await UniMessage(str(choice.message.content)).send(reply_to=True)
        else:
            await marsho_cmd.finish(f"意外的完成原因:{choice.finish_reason}")

    async def handle_common_chat(
        self,
        user_message: Union[str, list],
        model_name: str,
        tools: list,
        with_context: bool = True,
        stream: bool = False,
    ) -> ChatCompletion:
        """
        处理一般聊天
        """
        global target_list
        if stream:
            raise NotImplementedError
        response = await self.handle_single_chat(
            user_message=user_message,
            model_name=model_name,
            tools=tools,
            with_context=with_context,
        )
        choice = response.choices[0]
        # Sprint(choice)
        # 当tool_calls非空时，将finish_reason设置为TOOL_CALLS
        if choice.message.tool_calls is not None and config.marshoai_fix_toolcalls:
            choice.finish_reason = "tool_calls"
        logger.info(f"完成原因：{choice.finish_reason}")
        if choice.finish_reason == CompletionsFinishReason.STOPPED:

            ##### DeepSeek-R1 兼容部分 #####
            choice_msg_content, choice_msg_thinking, choice_msg_after = (
                extract_content_and_think(choice.message)
            )
            if choice_msg_thinking and config.marshoai_send_thinking:
                await UniMessage("思维链：\n" + choice_msg_thinking).send()
            ##### 兼容部分结束 #####

            if [self.target.id, self.target.private] not in target_list:
                target_list.append([self.target.id, self.target.private])

            # 对话成功发送消息
            if config.marshoai_enable_richtext_parse:
                await (await parse_richtext(str(choice_msg_content))).send(
                    reply_to=True
                )
            else:
                await UniMessage(str(choice_msg_content)).send(reply_to=True)
            return (UserMessage(context=user_message), choice_msg_after)
        elif choice.finish_reason == CompletionsFinishReason.CONTENT_FILTERED:

            # 对话失败，消息过滤

            await UniMessage("*已被内容过滤器过滤。请调整聊天内容后重试。").send(
                reply_to=True
            )
            return None
        elif choice.finish_reason == CompletionsFinishReason.TOOL_CALLS:
            pass
        else:
            await UniMessage(f"意外的完成原因:{choice.finish_reason}").send()
            return None
