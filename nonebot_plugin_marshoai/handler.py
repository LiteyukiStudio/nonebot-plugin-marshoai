import json
from typing import Optional, Tuple, Union

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
    current_matcher,
)
from nonebot_plugin_alconna.uniseg import UniMessage, UniMsg
from openai import AsyncOpenAI, AsyncStream
from openai.types.chat import ChatCompletion, ChatCompletionChunk, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice

from .config import config
from .constants import SUPPORT_IMAGE_MODELS
from .instances import target_list
from .models import MarshoContext
from .plugin.func_call.caller import get_function_calls
from .plugin.func_call.models import SessionContext
from .util import (
    extract_content_and_think,
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
        # self.state: T_State = current_handler.get().state
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
            nickname_prompt = f"\n此消息的说话者为: {user_nickname}"
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
        tools_list: list | None,
        tool_message: Optional[list] = None,
        stream: bool = False,
    ) -> Union[ChatCompletion, AsyncStream[ChatCompletionChunk]]:
        """
        处理单条聊天
        """

        context_msg = await get_prompt(model_name) + (
            self.context.build(self.target.id, self.target.private)
        )
        response = await make_chat_openai(
            client=self.client,
            msg=context_msg + [UserMessage(content=user_message).as_dict()] + (tool_message if tool_message else []),  # type: ignore
            model_name=model_name,
            tools=tools_list if tools_list else None,
            stream=stream,
        )
        return response

    async def handle_function_call(
        self,
        completion: Union[ChatCompletion, AsyncStream[ChatCompletionChunk]],
        user_message: Union[str, list],
        model_name: str,
        tools_list: list,
    ):
        # function call
        # 需要获取额外信息，调用函数工具
        tool_msg = []
        if isinstance(completion, ChatCompletion):
            choice = completion.choices[0]
        else:
            raise ValueError("Unexpected completion type")
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
        for tool_call in tool_calls:  # type: ignore
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
            if caller := get_function_calls().get(tool_call.function.name):
                logger.debug(f"调用插件函数 {caller.full_name}")
                # 权限检查，规则检查 TODO
                # 实现依赖注入，检查函数参数及参数注解类型，对Event类型的参数进行注入
                func_return = await caller.with_ctx(
                    SessionContext(
                        bot=self.bot,
                        event=self.event,
                        matcher=self.matcher,
                        state=None,
                    )
                ).call(**function_args)
            else:
                logger.error(f"未找到函数 {tool_call.function.name.replace('-', '.')}")
                func_return = f"未找到函数 {tool_call.function.name.replace('-', '.')}"
            tool_msg.append(
                ToolMessage(tool_call_id=tool_call.id, content=func_return).as_dict()  # type: ignore
            )
            #  tool_msg[0]["tool_calls"][0]["type"] = "builtin_function"
            # await UniMessage(str(tool_msg)).send()
        return await self.handle_common_chat(
            user_message=user_message,
            model_name=model_name,
            tools_list=tools_list,
            tool_message=tool_msg,
        )

    async def handle_common_chat(
        self,
        user_message: Union[str, list],
        model_name: str,
        tools_list: list,
        stream: bool = False,
        tool_message: Optional[list] = None,
    ) -> Optional[Tuple[UserMessage, ChatCompletionMessage]]:
        """
        处理一般聊天
        """
        global target_list
        if stream:
            response = await self.handle_stream_request(
                user_message=user_message,
                model_name=model_name,
                tools_list=tools_list,
                tools_message=tool_message,
            )
        else:
            response = await self.handle_single_chat(  # type: ignore
                user_message=user_message,
                model_name=model_name,
                tools_list=tools_list,
                tool_message=tool_message,
            )
        choice = response.choices[0]  # type: ignore
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
            return UserMessage(content=user_message), choice_msg_after
        elif choice.finish_reason == CompletionsFinishReason.CONTENT_FILTERED:

            # 对话失败，消息过滤

            await UniMessage("*已被内容过滤器过滤。请调整聊天内容后重试。").send(
                reply_to=True
            )
            return None
        elif choice.finish_reason == CompletionsFinishReason.TOOL_CALLS:
            return await self.handle_function_call(
                response, user_message, model_name, tools_list
            )
        else:
            await UniMessage(f"意外的完成原因:{choice.finish_reason}").send()
            return None

    async def handle_stream_request(
        self,
        user_message: Union[str, list],
        model_name: str,
        tools_list: list,
        tools_message: Optional[list] = None,
    ) -> Union[ChatCompletion, None]:
        """
        处理流式请求
        """
        response = await self.handle_single_chat(
            user_message=user_message,
            model_name=model_name,
            tools_list=None,  # TODO:让流式调用支持工具调用
            tool_message=tools_message,
            stream=True,
        )

        if isinstance(response, AsyncStream):
            reasoning_contents = ""
            answer_contents = ""
            last_chunk = None
            is_first_token_appeared = False
            is_answering = False
            async for chunk in response:
                last_chunk = chunk
                # print(chunk)
                if not is_first_token_appeared:
                    logger.debug(f"{chunk.id}: 第一个 token 已出现")
                    is_first_token_appeared = True
                if not chunk.choices:
                    logger.info("Usage:", chunk.usage)
                else:
                    delta = chunk.choices[0].delta
                    if (
                        hasattr(delta, "reasoning_content")
                        and delta.reasoning_content is not None
                    ):
                        reasoning_contents += delta.reasoning_content
                    else:
                        if not is_answering:
                            logger.debug(
                                f"{chunk.id}: 思维链已输出完毕或无 reasoning_content 字段输出"
                            )
                            is_answering = True
                        if delta.content is not None:
                            answer_contents += delta.content
            # print(last_chunk)
            # 创建新的 ChatCompletion 对象
            if last_chunk and last_chunk.choices:
                message = ChatCompletionMessage(
                    content=answer_contents,
                    role="assistant",
                    tool_calls=last_chunk.choices[0].delta.tool_calls,  # type: ignore
                )
                if reasoning_contents != "":
                    setattr(message, "reasoning_content", reasoning_contents)
                choice = Choice(
                    finish_reason=last_chunk.choices[0].finish_reason,  # type: ignore
                    index=last_chunk.choices[0].index,
                    message=message,
                )
                return ChatCompletion(
                    id=last_chunk.id,
                    choices=[choice],
                    created=last_chunk.created,
                    model=last_chunk.model,
                    system_fingerprint=last_chunk.system_fingerprint,
                    object="chat.completion",
                    usage=last_chunk.usage,
                )
        return None
