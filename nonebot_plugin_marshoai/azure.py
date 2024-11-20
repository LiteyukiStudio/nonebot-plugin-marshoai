import contextlib
import traceback
from typing import Optional

from arclet.alconna import Alconna, Args, AllParam
from azure.ai.inference.models import (
    UserMessage,
    AssistantMessage,
    TextContentItem,
    ImageContentItem,
    ImageUrl,
    CompletionsFinishReason,
)
from azure.core.credentials import AzureKeyCredential
from nonebot import on_command, logger
from nonebot.adapters import Message, Event
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot_plugin_alconna import on_alconna, MsgTarget
from nonebot_plugin_alconna.uniseg import UniMessage, UniMsg
from nonebot import get_driver

from .constants import *
from .metadata import metadata
from .models import MarshoContext
from .util import *

driver = get_driver()

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
refresh_data_cmd = on_command("refresh_data", permission=SUPERUSER)

model_name = config.marshoai_default_model
context = MarshoContext()
token = config.marshoai_token
endpoint = config.marshoai_azure_endpoint
client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(token))
target_list = []  # 记录需保存历史上下文的列表


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
        await get_backup_context(target.id, target.private) # 为了将当前会话添加到"已恢复过备份"的列表而添加，防止上下文被覆盖（好奇怪QwQ
        context.set_context(
            await load_context_from_json(msg, "contexts"), target.id, target.private
        )
        await load_context_cmd.finish("已加载并覆盖上下文")


@resetmem_cmd.handle()
async def resetmem(target: MsgTarget):
    if [target.id, target.private] not in target_list:                                          target_list.append([target.id, target.private])
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
        await set_nickname(user_id, name)
        await nickname_cmd.finish("已设置昵称为：" + name)


@refresh_data_cmd.handle()
async def refresh_data():
    await refresh_nickname_json()
    await refresh_praises_json()
    await refresh_data_cmd.finish("已刷新数据")


@marsho_cmd.handle()
async def marsho(target: MsgTarget, event: Event, text: Optional[UniMsg] = None):
    global target_list
    if not text:
        # 发送说明
        await UniMessage(metadata.usage + "\n当前使用的模型：" + model_name).send()
        await marsho_cmd.finish(INTRODUCTION)
    try:
        user_id = event.get_user_id()
        nicknames = await get_nicknames()
        user_nickname = nicknames.get(user_id, "")
        if user_nickname != "":
            nickname_prompt = f"\n*此消息的说话者:{user_nickname}*"
        else:
            nickname_prompt = ""
            #用户名无法获取，暂时注释
            #user_nickname = event.sender.nickname  # 未设置昵称时获取用户名
            #nickname_prompt = f"\n*此消息的说话者:{user_nickname}"
            if config.marshoai_enable_nickname_tip:
                await UniMessage(
                    "*你未设置自己的昵称。推荐使用'nickname [昵称]'命令设置昵称来获得个性化(可能）回答。"
                ).send()

        is_support_image_model = model_name.lower() in SUPPORT_IMAGE_MODELS + config.marshoai_additional_image_models
        is_reasoning_model = model_name.lower() in REASONING_MODELS
        usermsg = [] if is_support_image_model else ""
        for i in text:
            if i.type == "text":
                if is_support_image_model:
                    usermsg += [TextContentItem(text=i.data["text"] + nickname_prompt)]
                else:
                    usermsg += str(i.data["text"] + nickname_prompt)
            elif i.type == "image":
                if is_support_image_model:
                    usermsg.append(
                        ImageContentItem(
                            image_url=ImageUrl(url=str(await get_image_b64(i.data["url"])))
                        )
                    )
                elif config.marshoai_enable_support_image_tip:
                    await UniMessage("*此模型不支持图片处理。").send()
        backup_context = await get_backup_context(target.id, target.private)
        if backup_context:
            context.set_context(backup_context, target.id, target.private)  # 加载历史记录
            logger.info(f"已恢复会话 {target.id} 的上下文备份~")
        context_msg = context.build(target.id, target.private)
        if not is_reasoning_model:
            context_msg = [get_prompt()] + context_msg
            # o1等推理模型不支持系统提示词, 故不添加
        response = await make_chat(
            client=client,
            model_name=model_name,
            msg=context_msg + [UserMessage(content=usermsg)],
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
            if [target.id, target.private] not in target_list:
                target_list.append([target.id, target.private])
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
    async def poke(event: Event):

        user_id = event.get_user_id()
        nicknames = await get_nicknames()
        user_nickname = nicknames.get(user_id, "")
        try:
            if config.marshoai_poke_suffix != "":
                response = await make_chat(
                    client=client,
                    model_name=model_name,
                    msg=[
                        get_prompt(),
                        UserMessage(
                            content=f"*{user_nickname}{config.marshoai_poke_suffix}"
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


@driver.on_shutdown
async def auto_backup_context():
    for target_info in target_list:
        target_id, target_private = target_info
        contexts_data = context.build(target_id, target_private)
        if target_private:
            target_uid = "private_" + target_id
        else:
            target_uid = "group_" + target_id
        await save_context_to_json(f"back_up_context_{target_uid}", contexts_data, "contexts/backup")
        logger.info(f"已保存会话 {target_id} 的上下文备份，将在下次对话时恢复~")
