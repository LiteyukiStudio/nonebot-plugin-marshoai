from nonebot.typing import T_State
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import ArgPlainText, CommandArg
from nonebot.permission import SUPERUSER
from typing import Optional
#from .acgnapis import *
from nonebot_plugin_alconna import on_alconna
from nonebot_plugin_alconna.uniseg import UniMessage, Target, MsgTarget, UniMsg, Image
from arclet.alconna import Alconna, Args, AllParam
from .util import *
import traceback
from azure.ai.inference.aio import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage, TextContentItem, ImageContentItem, ImageUrl, CompletionsFinishReason
from azure.core.credentials import AzureKeyCredential
from .__init__ import __plugin_meta__
from PIL import Image
from .config import config
from .models import MarshoContext
changemdl = on_command("changemodel",permission=SUPERUSER)
resetmem = on_command("reset",permission=SUPERUSER)
setprompt_cmd = on_command("prompt",permission=SUPERUSER)
praises_cmd = on_command("praises",permission=SUPERUSER)
add_usermsg_cmd = on_command("usermsg",permission=SUPERUSER)
add_assistantmsg_cmd = on_command("assistantmsg",permission=SUPERUSER)
contexts_cmd = on_command("contexts",permission=SUPERUSER)
nekocmd = on_alconna(
        Alconna(
            "marsho",
            Args["text?",AllParam],
        ),
        aliases={"neko"}
    )
model_name = config.marshoai_default_model
context = MarshoContext()
context_limit = 15



@add_usermsg_cmd.handle()
async def add_usermsg(arg: Message = CommandArg()):
    if msg := arg.extract_plain_text():
        context.append(UserMessage(content=msg))
        await UniMessage("已添加用户消息").send()

@add_assistantmsg_cmd.handle()
async def add_assistantmsg(arg: Message = CommandArg()):
    if msg := arg.extract_plain_text():
        context.append(AssistantMessage(content=msg))
        await UniMessage("已添加助手消息").send()

@praises_cmd.handle()
async def getpraises():
    await UniMessage(build_praises()).send()

@contexts_cmd.handle()
async def contexts():
    await UniMessage(str(context.build()[1:])).send()

# @setprompt_cmd.handle() #用不了了
# async def setprompt(arg: Message = CommandArg()):
#     global spell, context
#     if prompt := arg.extract_plain_text():
#         spell = SystemMessage(content=prompt)
#         await setprompt_cmd.finish("已设置提示词")
#     else:
#         spell = SystemMessage(content="")
#         context = []
#         await setprompt_cmd.finish("已清除提示词")


@resetmem.handle()
async def reset():
    context.reset()
    context.resetcount()
    await resetmem.finish("上下文已重置")
    
@changemdl.got("model",prompt="请输入模型名")
async def changemodel(model : str = ArgPlainText()):
    global model_name
    model_name = model
    await changemdl.finish("已切换")
@nekocmd.handle()
async def neko(
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
        if context.count >= context_limit:
            await UniMessage("上下文数量达到阈值。已自动重置上下文。").send()
            context.reset()
            context.resetcount()
       # await UniMessage(str(text)).send()
        try:
            is_support_image_model = model_name.lower() in config.marshoai_support_image_models
            usermsg = [] if is_support_image_model else ""
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
                    if is_support_image_model:
                        usermsg.append(TextContentItem(text=i.data["text"]))
                    else:
                        usermsg += str(i.data["text"])
            response = await client.complete(
                        messages=context.build()+[UserMessage(content=usermsg)],
                        model=model_name   
                  )
            #await UniMessage(str(response)).send()
            choice = response.choices[0]
            if choice["finish_reason"] == CompletionsFinishReason.STOPPED:
                context.append(UserMessage(content=usermsg))
                context.append(choice.message)
                context.addcount()
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
            await UniMessage(str(e)).send()
           # await UniMessage(str(e.reason)).send()
            traceback.print_exc()
            return
