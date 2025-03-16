import contextlib
import traceback
from typing import Optional

from arclet.alconna import Alconna, AllParam, Args
from azure.ai.inference.models import (
    AssistantMessage,
    CompletionsFinishReason,
    UserMessage,
)
from nonebot import logger, on_command, on_message
from nonebot.adapters import Bot, Event, Message
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot_plugin_alconna import MsgTarget, UniMessage, UniMsg, on_alconna

from .config import config
from .constants import INTRODUCTION, SUPPORT_IMAGE_MODELS
from .handler import MarshoHandler
from .hooks import *
from .instances import client, context, model_name, target_list, tools
from .metadata import metadata
from .plugin.func_call.caller import get_function_calls
from .util import *


async def at_enable():
    return config.marshoai_at


changemodel_cmd = on_command(
    "changemodel", permission=SUPERUSER, priority=96, block=True
)
# setprompt_cmd = on_command("prompt",permission=SUPERUSER)
praises_cmd = on_command("praises", permission=SUPERUSER, priority=96, block=True)
add_usermsg_cmd = on_command("usermsg", permission=SUPERUSER, priority=96, block=True)
add_assistantmsg_cmd = on_command(
    "assistantmsg", permission=SUPERUSER, priority=96, block=True
)
contexts_cmd = on_command("contexts", permission=SUPERUSER, priority=96, block=True)
save_context_cmd = on_command(
    "savecontext", permission=SUPERUSER, priority=96, block=True
)
load_context_cmd = on_command(
    "loadcontext", permission=SUPERUSER, priority=96, block=True
)
marsho_cmd = on_alconna(
    Alconna(
        config.marshoai_default_name,
        Args["text?", AllParam],
    ),
    aliases=tuple(config.marshoai_aliases),
    priority=96,
    block=True,
)
resetmem_cmd = on_alconna(
    Alconna(
        config.marshoai_default_name + ".reset",
    ),
    priority=96,
    block=True,
)
marsho_help_cmd = on_alconna(
    Alconna(
        config.marshoai_default_name + ".help",
    ),
    priority=96,
    block=True,
)
marsho_status_cmd = on_alconna(
    Alconna(
        config.marshoai_default_name + ".status",
    ),
    priority=96,
    block=True,
)

marsho_at = on_message(rule=to_me() & at_enable, priority=97)
nickname_cmd = on_alconna(
    Alconna(
        "nickname",
        Args["name?", str],
    ),
    priority=96,
    block=True,
)
refresh_data_cmd = on_command(
    "refresh_data", permission=SUPERUSER, priority=96, block=True
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
        backup_context = await get_backup_context(target.id, target.private)
        if backup_context:
            context.set_context(
                backup_context, target.id, target.private
            )  # 加载历史记录
            logger.info(f"已恢复会话 {target.id} 的上下文备份~")
    handler = MarshoHandler(client, context)
    try:
        user_nickname = await get_nickname_by_user_id(event.get_user_id())
        if not user_nickname:
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

        usermsg = await handler.process_user_input(text, model_name)

        tools_lists = tools.tools_list + list(
            map(lambda v: v.data(), get_function_calls().values())
        )
        logger.info(f"正在获取回答，模型：{model_name}")
        # logger.info(f"上下文：{context_msg}")
        response = await handler.handle_common_chat(
            usermsg, model_name, tools_lists, config.marshoai_stream
        )
        # await UniMessage(str(response)).send()
        if response is not None:
            context_user, context_assistant = response
            context.append(context_user.as_dict(), target.id, target.private)
            context.append(context_assistant.to_dict(), target.id, target.private)
        else:
            return
    except Exception as e:
        await UniMessage(str(e) + suggest_solution(str(e))).send()
        traceback.print_exc()
        return


with contextlib.suppress(ImportError):  # 优化先不做（）
    import nonebot.adapters.onebot.v11  # type: ignore

    from .marsho_onebot import poke_notify

    @poke_notify.handle()
    async def poke(event: Event):

        user_nickname = await get_nickname_by_user_id(event.get_user_id())
        try:
            if config.marshoai_poke_suffix != "":
                logger.info(f"收到戳一戳，用户昵称：{user_nickname}")
                response = await make_chat_openai(
                    client=client,
                    model_name=model_name,
                    msg=await get_prompt(model_name)
                    + [
                        UserMessage(
                            content=f"*{user_nickname}{config.marshoai_poke_suffix}"
                        ),
                    ],
                )
                choice = response.choices[0]  # type: ignore
                if choice.finish_reason == CompletionsFinishReason.STOPPED:
                    content = extract_content_and_think(choice.message)[0]
                    await UniMessage(" " + str(content)).send(at_sender=True)
        except Exception as e:
            await UniMessage(str(e) + suggest_solution(str(e))).send()
            traceback.print_exc()
            return
