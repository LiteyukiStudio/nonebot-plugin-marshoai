from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot_plugin_alconna import on_alconna, MsgTarget
from nonebot_plugin_alconna.uniseg import UniMessage, UniMsg
from arclet.alconna import Alconna, Args, AllParam
from .util import *
import traceback
from azure.ai.inference.aio import ChatCompletionsClient
from azure.ai.inference.models import UserMessage, AssistantMessage, TextContentItem, ImageContentItem, ImageUrl, CompletionsFinishReason
from azure.core.credentials import AzureKeyCredential
from .__init__ import __plugin_meta__
from .config import config
from .models import MarshoContext
changemodel_cmd = on_command("changemodel",permission=SUPERUSER)
resetmem_cmd = on_command("reset")
#setprompt_cmd = on_command("prompt",permission=SUPERUSER)
praises_cmd = on_command("praises",permission=SUPERUSER)
add_usermsg_cmd = on_command("usermsg",permission=SUPERUSER)
add_assistantmsg_cmd = on_command("assistantmsg",permission=SUPERUSER)
contexts_cmd = on_command("contexts",permission=SUPERUSER)
save_context_cmd = on_command("savecontext",permission=SUPERUSER)
load_context_cmd = on_command("loadcontext",permission=SUPERUSER)
marsho_cmd = on_alconna(
        Alconna(
            "marsho",
            Args["text?",AllParam],
        )
    )
model_name = config.marshoai_default_model
context = MarshoContext()

@add_usermsg_cmd.handle()
async def add_usermsg(target: MsgTarget, arg: Message = CommandArg()):
    if msg := arg.extract_plain_text():
        context.append(UserMessage(content=msg).as_dict(), target.id, target.private)
        await add_usermsg_cmd.finish("已添加用户消息")

@add_assistantmsg_cmd.handle()
async def add_assistantmsg(target: MsgTarget, arg: Message = CommandArg()):
    if msg := arg.extract_plain_text():
        context.append(AssistantMessage(content=msg).as_dict(), target.id, target.private)
        await add_assistantmsg_cmd.finish("已添加助手消息")

@praises_cmd.handle()
async def praises():
    await UniMessage(build_praises()).send()

@contexts_cmd.handle()
async def contexts(target: MsgTarget):
    await UniMessage(str(context.build(target.id, target.private)[1:])).send()

@save_context_cmd.handle()
async def save_context(target: MsgTarget, arg: Message = CommandArg()):
    contexts = context.build(target.id, target.private)[1:]
    if msg := arg.extract_plain_text():
        await save_context_to_json(msg, contexts)
        await save_context_cmd.finish("已保存上下文")

@load_context_cmd.handle()
async def load_context(target: MsgTarget, arg: Message = CommandArg()):
    if msg := arg.extract_plain_text():
        context.set_context(await load_context_from_json(msg), target.id, target.private)
        await load_context_cmd.finish("已加载并覆盖上下文")

@resetmem_cmd.handle()
async def resetmem(target: MsgTarget):
    context.reset(target.id, target.private)
    await resetmem_cmd.finish("上下文已重置")
    
@changemodel_cmd.handle()
async def changemodel(arg : Message = CommandArg()):
    global model_name
    if model := arg.extract_plain_text():
        model_name = model
        await changemodel_cmd.finish("已切换")

@marsho_cmd.handle()
async def marsho(
        target: MsgTarget,
        message: UniMsg,
        text = None
    ):
        token = config.marshoai_token
        endpoint = config.marshoai_azure_endpoint
        #msg = await UniMessage.generate(message=message)
        client = ChatCompletionsClient(
              endpoint=endpoint,
              credential=AzureKeyCredential(token),
            )
        if not text:
            await UniMessage(
                __plugin_meta__.usage+"\n当前使用的模型："+model_name).send()
            return
       # await UniMessage(str(text)).send()
        try:
            is_support_image_model = model_name.lower() in config.marshoai_support_image_models
            usermsg = [] if is_support_image_model else ""
            marsho_string_removed = False
            for i in message:
                if i.type == "image":
                    if is_support_image_model:
                        imgurl = i.data["url"]
                        picmsg = ImageContentItem(
                            image_url=ImageUrl(url=str(await get_image_b64(imgurl)))
                        )
                        usermsg.append(picmsg)
                    else:
                        await UniMessage("*此模型不支持图片处理。").send()
                elif i.type == "text":
                    if not marsho_string_removed:
                        # 去掉最前面的"marsho "字符串
                        clean_text = i.data["text"].lstrip("marsho ")
                        marsho_string_removed = True  # 标记文本已处理
                    else:
                        clean_text = i.data["text"]
                    if is_support_image_model:
                        usermsg.append(TextContentItem(text=clean_text))
                    else:
                        usermsg += str(clean_text)
            response = await client.complete(
                        messages=context.build(target.id, target.private)+[UserMessage(content=usermsg)],
                        model=model_name,
                        temperature=config.marshoai_temperature,
                        max_tokens=config.marshoai_max_tokens,
                        top_p=config.marshoai_top_p
                  )
            #await UniMessage(str(response)).send()
            choice = response.choices[0]
            if choice["finish_reason"] == CompletionsFinishReason.STOPPED: # 当对话成功时，将dict的上下文添加到上下文类中
                context.append(UserMessage(content=usermsg).as_dict(), target.id, target.private)
                context.append(choice.message.as_dict(), target.id, target.private)
            elif choice["finish_reason"] == CompletionsFinishReason.CONTENT_FILTERED:
                await UniMessage("*已被内容过滤器过滤。*").send()
            #await UniMessage(str(choice)).send()
            await UniMessage(str(choice.message.content)).send(reply_to=True)
            #requests_limit = response.headers.get('x-ratelimit-limit-requests')
             #request_id = response.headers.get('x-request-id')
             #remaining_requests = response.headers.get('x-ratelimit-remaining-requests')
             #remaining_tokens = response.headers.get('x-ratelimit-remaining-tokens')
             #await UniMessage(f"""  剩余token：{remaining_tokens}"""
               #      ).send()
        except Exception as e:
            await UniMessage(str(e)+suggest_solution(str(e))).send()
           # await UniMessage(str(e.reason)).send()
            traceback.print_exc()
            return
