import contextlib
import traceback
from typing import Optional

import openai
from arclet.alconna import Alconna, AllParam, Args
from azure.ai.inference.models import (
    AssistantMessage,
    CompletionsFinishReason,
    ImageContentItem,
    ImageUrl,
    TextContentItem,
    ToolMessage,
    UserMessage,
)
from nonebot import logger, on_command, on_message
from nonebot.adapters import Bot, Event, Message
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.rule import Rule, to_me
from nonebot.typing import T_State
from nonebot_plugin_alconna import MsgTarget, UniMessage, UniMsg, on_alconna

from .hooks import *
from .instances import *
from .metadata import metadata
from .plugin.func_call.caller import get_function_calls
from .plugin.func_call.models import SessionContext
from .util import *


async def at_enable():
    return config.marshoai_at


changemodel_cmd = on_command(
    "changemodel", permission=SUPERUSER, priority=10, block=True
)
resetmem_cmd = on_command("reset", priority=10, block=True)
# setprompt_cmd = on_command("prompt",permission=SUPERUSER)
praises_cmd = on_command("praises", permission=SUPERUSER, priority=10, block=True)
add_usermsg_cmd = on_command("usermsg", permission=SUPERUSER, priority=10, block=True)
add_assistantmsg_cmd = on_command(
    "assistantmsg", permission=SUPERUSER, priority=10, block=True
)
contexts_cmd = on_command("contexts", permission=SUPERUSER, priority=10, block=True)
save_context_cmd = on_command(
    "savecontext", permission=SUPERUSER, priority=10, block=True
)
load_context_cmd = on_command(
    "loadcontext", permission=SUPERUSER, priority=10, block=True
)
marsho_cmd = on_alconna(
    Alconna(
        config.marshoai_default_name,
        Args["text?", AllParam],
    ),
    aliases=tuple(config.marshoai_aliases),
    priority=10,
    block=True,
)
marsho_help_cmd = on_alconna(
    Alconna(
        config.marshoai_default_name + ".help",
    ),
    priority=10,
    block=True,
)
marsho_status_cmd = on_alconna(
    Alconna(
        config.marshoai_default_name + ".status",
    ),
    priority=10,
    block=True,
)

marsho_at = on_message(rule=to_me() & at_enable, priority=11)
nickname_cmd = on_alconna(
    Alconna(
        "nickname",
        Args["name?", str],
    ),
    priority=10,
    block=True,
)
refresh_data_cmd = on_command(
    "refresh_data", permission=SUPERUSER, priority=10, block=True
)


@add_usermsg_cmd.handle()
async def add_usermsg(target: MsgTarget, arg: Message = CommandArg()):
    if msg := arg.extract_plain_text():
        context.append(UserMessage(content=msg).as_dict(), target.id, target.private)
        await add_usermsg_cmd.finish("已添加用户消息")


@add_assistantmsg_cmd.handle()
async def add_assistantmsg(target: MsgTarget, arg: Message = CommandArg()):
    if msg := arg.extract_plain_text():
        context.append(
            AssistantMessage(content=msg).as_dict(), target.id, target.private
        )
        await add_assistantmsg_cmd.finish("已添加助手消息")


@praises_cmd.handle()
async def praises():
    # await UniMessage(await tools.call("marshoai-weather.get_weather", {"location":"杭州"})).send()
    await praises_cmd.finish(build_praises())


@contexts_cmd.handle()
async def contexts(target: MsgTarget):
    backup_context = await get_backup_context(target.id, target.private)
    if backup_context:
        context.set_context(backup_context, target.id, target.private)  # 加载历史记录
    await contexts_cmd.finish(str(context.build(target.id, target.private)))


@save_context_cmd.handle()
async def save_context(target: MsgTarget, arg: Message = CommandArg()):
    contexts_data = context.build(target.id, target.private)
    if not context:
        await save_context_cmd.finish("暂无上下文可以保存")
    if msg := arg.extract_plain_text():
        await save_context_to_json(msg, contexts_data, "contexts")
        await save_context_cmd.finish("已保存上下文")


@load_context_cmd.handle()
async def load_context(target: MsgTarget, arg: Message = CommandArg()):
    if msg := arg.extract_plain_text():
        await get_backup_context(
            target.id, target.private
        )  # 为了将当前会话添加到"已恢复过备份"的列表而添加，防止上下文被覆盖（好奇怪QwQ
        context.set_context(
            await load_context_from_json(msg, "contexts"), target.id, target.private
        )
        await load_context_cmd.finish("已加载并覆盖上下文")


@resetmem_cmd.handle()
async def resetmem(target: MsgTarget):
    if [target.id, target.private] not in target_list:
        target_list.append([target.id, target.private])
    backup_context = await get_backup_context(target.id, target.private)
    if backup_context:
        context.set_context(backup_context, target.id, target.private)
    context.reset(target.id, target.private)
    await resetmem_cmd.finish("上下文已重置")


@changemodel_cmd.handle()
async def changemodel(arg: Message = CommandArg()):
    global model_name
    if model := arg.extract_plain_text():
        model_name = model
        await changemodel_cmd.finish("已切换")


@nickname_cmd.handle()
async def nickname(event: Event, name=None):
    nicknames = await get_nicknames()
    user_id = event.get_user_id()
    if not name:
        if user_id not in nicknames:
            await nickname_cmd.finish("你未设置昵称")
        await nickname_cmd.finish("你的昵称为：" + str(nicknames[user_id]))
    if name == "reset":
        await set_nickname(user_id, "")
        await nickname_cmd.finish("已重置昵称")
    else:
        if len(name) > config.marshoai_nickname_limit:
            await nickname_cmd.finish(
                "昵称超出长度限制：" + str(config.marshoai_nickname_limit)
            )
        await set_nickname(user_id, name)
        await nickname_cmd.finish("已设置昵称为：" + name)


@refresh_data_cmd.handle()
async def refresh_data():
    await refresh_nickname_json()
    await refresh_praises_json()
    await refresh_data_cmd.finish("已刷新数据")


@marsho_help_cmd.handle()
async def marsho_help():
    await marsho_help_cmd.finish(metadata.usage)


@marsho_status_cmd.handle()
async def marsho_status(bot: Bot):
    await marsho_status_cmd.finish(
        f"当前适配器：{bot.adapter.get_name()}\n"
        f"当前使用的模型：{model_name}\n"
        # f"当前会话数量：{len(target_list)}\n"
        # f"当前上下文数量：{len(context.contexts)}"
        f"当前支持图片的模型：{str(SUPPORT_IMAGE_MODELS + config.marshoai_additional_image_models)}"
    )


@marsho_at.handle()
@marsho_cmd.handle()
async def marsho(
    target: MsgTarget,
    event: Event,
    bot: Bot,
    state: T_State,
    matcher: Matcher,
    text: Optional[UniMsg] = None,
):

    global target_list
    if event.get_message().extract_plain_text() and (
        not text
        and event.get_message().extract_plain_text() != config.marshoai_default_name
    ):
        text = event.get_message()  # type: ignore
    if not text:
        # 发送说明
        # await UniMessage(metadata.usage + "\n当前使用的模型：" + model_name).send()
        await marsho_cmd.finish(INTRODUCTION)
    try:
        user_id = event.get_user_id()
        nicknames = await get_nicknames()
        user_nickname = nicknames.get(user_id, "")
        if user_nickname != "":
            nickname_prompt = (
                f"\n*此消息的说话者id为:{user_id}，名字为:{user_nickname}*"
            )
        else:
            nickname_prompt = ""
            # 用户名无法获取，暂时注释
            # user_nickname = event.sender.nickname  # 未设置昵称时获取用户名
            # nickname_prompt = f"\n*此消息的说话者:{user_nickname}"
            if config.marshoai_enforce_nickname:
                await UniMessage(
                    "※你未设置自己的昵称。你**必须**使用「nickname [昵称]」命令设置昵称后才能进行对话。"
                ).send()
                return
            if config.marshoai_enable_nickname_tip:
                await UniMessage(
                    "※你未设置自己的昵称。推荐使用「nickname [昵称]」命令设置昵称来获得个性化(可能）回答。"
                ).send()

        is_support_image_model = (
            model_name.lower()
            in SUPPORT_IMAGE_MODELS + config.marshoai_additional_image_models
        )
        is_reasoning_model = model_name.lower() in NO_SYSPROMPT_MODELS
        usermsg = [] if is_support_image_model else ""
        for i in text:  # type: ignore
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
                elif config.marshoai_enable_support_image_tip:
                    await UniMessage(
                        "*此模型不支持图片处理或管理员未启用此模型的图片支持。图片将被忽略。"
                    ).send()
        backup_context = await get_backup_context(target.id, target.private)
        if backup_context:
            context.set_context(
                backup_context, target.id, target.private
            )  # 加载历史记录
            logger.info(f"已恢复会话 {target.id} 的上下文备份~")
        context_msg = context.build(target.id, target.private)
        if not is_reasoning_model:
            context_msg = [get_prompt()] + context_msg
            # o1等推理模型不支持系统提示词, 故不添加
        tools_lists = tools.tools_list + list(
            map(lambda v: v.data(), get_function_calls().values())
        )
        logger.info(f"正在获取回答，模型：{model_name}")
        response = await make_chat_openai(
            client=client,
            model_name=model_name,
            msg=context_msg + [UserMessage(content=usermsg).as_dict()],  # type: ignore
            tools=tools_lists if tools_lists else None,  # TODO 临时追加函数，后期优化
        )
        # await UniMessage(str(response)).send()
        choice = response.choices[0]
        # Sprint(choice)
        # 当tool_calls非空时，将finish_reason设置为TOOL_CALLS
        if choice.message.tool_calls != None and config.marshoai_fix_toolcalls:
            choice.finish_reason = CompletionsFinishReason.TOOL_CALLS
        logger.info(f"完成原因：{choice.finish_reason}")
        if choice.finish_reason == CompletionsFinishReason.STOPPED:
            # 当对话成功时，将dict的上下文添加到上下文类中
            context.append(
                UserMessage(content=usermsg).as_dict(), target.id, target.private  # type: ignore
            )

            ##### DeepSeek-R1 兼容部分 #####
            choice_msg_content, choice_msg_thinking, choice_msg_after = (
                extract_content_and_think(choice.message)
            )
            if choice_msg_thinking and config.marshoai_send_thinking:
                await UniMessage("思维链：\n" + choice_msg_thinking).send()
            ##### 兼容部分结束 #####

            context.append(choice_msg_after.to_dict(), target.id, target.private)
            if [target.id, target.private] not in target_list:
                target_list.append([target.id, target.private])

            # 对话成功发送消息
            if config.marshoai_enable_richtext_parse:
                await (await parse_richtext(str(choice_msg_content))).send(
                    reply_to=True
                )
            else:
                await UniMessage(str(choice_msg_content)).send(reply_to=True)
        elif choice.finish_reason == CompletionsFinishReason.CONTENT_FILTERED:

            # 对话失败，消息过滤

            await UniMessage("*已被内容过滤器过滤。请调整聊天内容后重试。").send(
                reply_to=True
            )
            return
        elif choice.finish_reason == CompletionsFinishReason.TOOL_CALLS:
            # function call
            # 需要获取额外信息，调用函数工具
            tool_msg = []
            while choice.message.tool_calls != None:
                # await UniMessage(str(response)).send()
                tool_calls = choice.message.tool_calls
                try:
                    if tool_calls[0]["function"]["name"].startswith("$"):
                        choice.message.tool_calls[0][
                            "type"
                        ] = "builtin_function"  # 兼容 moonshot AI 内置函数的临时方案
                except:
                    pass
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
                                    bot=bot,
                                    event=event,
                                    state=state,
                                    matcher=matcher,
                                )
                            ).call(**function_args)
                        else:
                            logger.error(
                                f"未找到函数 {tool_call.function.name.replace('-', '.')}"
                            )
                            func_return = f"未找到函数 {tool_call.function.name.replace('-', '.')}"
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
                if choice.message.tool_calls != None:
                    choice.finish_reason = CompletionsFinishReason.TOOL_CALLS
            if choice.finish_reason == CompletionsFinishReason.STOPPED:

                # 对话成功 添加上下文
                context.append(
                    UserMessage(content=usermsg).as_dict(), target.id, target.private  # type: ignore
                )
                # context.append(tool_msg, target.id, target.private)
                choice_msg_dict = choice.message.to_dict()
                if "reasoning_content" in choice_msg_dict:
                    del choice_msg_dict["reasoning_content"]
                context.append(choice_msg_dict, target.id, target.private)

                # 发送消息
                if config.marshoai_enable_richtext_parse:
                    await (await parse_richtext(str(choice.message.content))).send(
                        reply_to=True
                    )
                else:
                    await UniMessage(str(choice.message.content)).send(reply_to=True)
            else:
                await marsho_cmd.finish(f"意外的完成原因:{choice.finish_reason}")
        else:
            await marsho_cmd.finish(f"意外的完成原因:{choice.finish_reason}")
    except Exception as e:
        await UniMessage(str(e) + suggest_solution(str(e))).send()
        traceback.print_exc()
        return


with contextlib.suppress(ImportError):  # 优化先不做（）
    import nonebot.adapters.onebot.v11  # type: ignore

    from .marsho_onebot import poke_notify

    @poke_notify.handle()
    async def poke(event: Event):

        user_id = event.get_user_id()
        nicknames = await get_nicknames()
        user_nickname = nicknames.get(user_id, "")
        try:
            if config.marshoai_poke_suffix != "":
                logger.info(f"收到戳一戳，用户昵称：{user_nickname}，用户ID：{user_id}")
                response = await make_chat_openai(
                    client=client,
                    model_name=model_name,
                    msg=[
                        (
                            get_prompt()
                            if model_name.lower() not in NO_SYSPROMPT_MODELS
                            else None
                        ),
                        UserMessage(
                            content=f"*{user_nickname}{config.marshoai_poke_suffix}"
                        ),
                    ],
                )
                choice = response.choices[0]
                if choice.finish_reason == CompletionsFinishReason.STOPPED:
                    content = extract_content_and_think(choice.message)[0]
                    await UniMessage(" " + str(content)).send(at_sender=True)
        except Exception as e:
            await UniMessage(str(e) + suggest_solution(str(e))).send()
            traceback.print_exc()
            return
