from nonebot import on_command
from nonebot.adapters import Message, Event
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot_plugin_alconna import on_alconna, MsgTarget
from nonebot_plugin_alconna.uniseg import UniMessage, UniMsg
from arclet.alconna import Alconna, Args, AllParam
from .util import *
import traceback
import contextlib
from azure.ai.inference.aio import ChatCompletionsClient
from azure.ai.inference.models import (
    UserMessage,
    AssistantMessage,
    ContentItem,
    TextContentItem,
    ImageContentItem,
    ImageUrl,
    CompletionsFinishReason,
)
from azure.core.credentials import AzureKeyCredential
from typing import Any, Optional

from .metadata import metadata
from .config import config
from .models import MarshoContext
from .constants import *

changemodel_cmd = on_command("changemodel", permission=SUPERUSER)
resetmem_cmd = on_command("reset")
# setprompt_cmd = on_command("prompt",permission=SUPERUSER)
praises_cmd = on_command("praises", permission=SUPERUSER)
add_usermsg_cmd = on_command("usermsg", permission=SUPERUSER)
add_assistantmsg_cmd = on_command("assistantmsg", permission=SUPERUSER)
contexts_cmd = on_command("contexts", permission=SUPERUSER)
save_context_cmd = on_command("savecontext", permission=SUPERUSER)
load_context_cmd = on_command("loadcontext", permission=SUPERUSER)
marsho_cmd = on_alconna(
    Alconna(
        config.marshoai_default_name,
        Args["text?", AllParam],
    ),
    aliases=config.marshoai_aliases,
)
nickname_cmd = on_alconna(
    Alconna(
        "nickname",
        Args["name?", str],
    )
)
model_name = config.marshoai_default_model
context = MarshoContext()
token = config.marshoai_token
endpoint = config.marshoai_azure_endpoint
client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(token))


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
    await praises_cmd.finish(build_praises())


@contexts_cmd.handle()
async def contexts(target: MsgTarget):
    await contexts_cmd.finish(str(context.build(target.id, target.private)[1:]))


@save_context_cmd.handle()
async def save_context(target: MsgTarget, arg: Message = CommandArg()):
    contexts = context.build(target.id, target.private)[1:]
    if msg := arg.extract_plain_text():
        await save_context_to_json(msg, contexts)
        await save_context_cmd.finish("已保存上下文")


@load_context_cmd.handle()
async def load_context(target: MsgTarget, arg: Message = CommandArg()):
    if msg := arg.extract_plain_text():
        context.set_context(
            await load_context_from_json(msg), target.id, target.private
        )
        await load_context_cmd.finish("已加载并覆盖上下文")


@resetmem_cmd.handle()
async def resetmem(target: MsgTarget):
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
        await nickname_cmd.finish("你的昵称为：" + str(nicknames[user_id]))
    if name == "reset":
        await set_nickname(user_id, "")
        await nickname_cmd.finish("已重置昵称")
    else:
        await set_nickname(user_id, name)
        await nickname_cmd.finish("已设置昵称为：" + name)


@marsho_cmd.handle()
async def marsho(target: MsgTarget, event: Event, text: Optional[UniMsg] = None):
    if not text:
        await UniMessage(metadata.usage + "\n当前使用的模型：" + model_name).send()
        await marsho_cmd.finish(INTRODUCTION)
        return

    try:

        user_id = event.get_user_id()
        nicknames = await get_nicknames()
        nickname = nicknames.get(user_id, "")
        if nickname != "":
            nickname_prompt = f"\n*此消息的说话者:{nickname}*"
        else:
            nickname_prompt = ""
            if config.marshoai_enable_nickname_tip:
                await UniMessage(
                    "*你未设置自己的昵称。推荐使用'nickname [昵称]'命令设置昵称来获得个性化(可能）回答。"
                ).send()

        usermsg: list[ContentItem] = []
        for i in text:
            if i.type == "text":
                usermsg += [TextContentItem(text=i.data["text"] + nickname_prompt)]
            elif i.type == "image" and model_name.lower() in SUPPORT_IMAGE_MODELS:
                usermsg.append(
                    ImageContentItem(
                        image_url=ImageUrl(url=str(await get_image_b64(i.data["url"])))
                    )
                )

        response = await make_chat(
            client=client,
            model_name=model_name,
            msg=context.build(target.id, target.private)
            + [UserMessage(content=usermsg)],
        )
        # await UniMessage(str(response)).send()
        choice = response.choices[0]
        if (
            choice["finish_reason"] == CompletionsFinishReason.STOPPED
        ):  # 当对话成功时，将dict的上下文添加到上下文类中
            context.append(
                UserMessage(content=usermsg).as_dict(), target.id, target.private
            )
            context.append(choice.message.as_dict(), target.id, target.private)
        elif choice["finish_reason"] == CompletionsFinishReason.CONTENT_FILTERED:
            await UniMessage("*已被内容过滤器过滤。请调整聊天内容后重试。").send(
                reply_to=True
            )
            return
        await UniMessage(str(choice.message.content)).send(reply_to=True)
    except Exception as e:
        await UniMessage(str(e) + suggest_solution(str(e))).send()
        traceback.print_exc()
        return


with contextlib.suppress(ImportError):  # 优化先不做（）
    import nonebot.adapters.onebot.v11  # type: ignore
    from .azure_onebot import poke_notify

    @poke_notify.handle()
    async def poke(event: Event, target: MsgTarget):

        user_id = event.get_user_id()
        nicknames = await get_nicknames()
        nickname = nicknames.get(user_id, "")
        try:
            if config.marshoai_poke_suffix != "":
                response = await make_chat(
                    client=client,
                    model_name=model_name,
                    msg=[
                        get_prompt(),
                        UserMessage(
                            content=f"*{nickname}{config.marshoai_poke_suffix}"
                        ),
                    ],
                )
                choice = response.choices[0]
                if choice["finish_reason"] == CompletionsFinishReason.STOPPED:
                    await UniMessage(" " + str(choice.message.content)).send(
                        at_sender=True
                    )
        except Exception as e:
            await UniMessage(str(e) + suggest_solution(str(e))).send()
            traceback.print_exc()
            return
