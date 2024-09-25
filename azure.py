from nonebot.typing import T_State
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import ArgPlainText, CommandArg
from nonebot.permission import SUPERUSER
from typing import Optional
#from .acgnapis import *
from nonebot_plugin_alconna import on_alconna
from nonebot_plugin_alconna.uniseg import UniMessage, Target, MsgTarget, UniMsg, Image
from arclet.alconna import Alconna, Args, AllParam, Arparma
from .util import *
import traceback
from azure.ai.inference.aio import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, TextContentItem, ImageContentItem, ImageUrl
from azure.core.credentials import AzureKeyCredential
from .__init__ import __plugin_meta__
from PIL import Image
from .config import config
from .models import MarshoContext
changemdl = on_command("changemodel",permission=SUPERUSER)
resetmem = on_command("reset",permission=SUPERUSER)
setprompt_cmd = on_command("prompt",permission=SUPERUSER)
nekocmd = on_alconna(
        Alconna(
            "marsho",
            Args["text?",AllParam],
        ),
        aliases={"neko"}
    )
model_name = "gpt-4o-mini"
context = MarshoContext()
context_limit = 15
context_count = 0

@setprompt_cmd.handle() #用不了了
async def setprompt(arg: Message = CommandArg()):
    global spell, context
    if prompt := arg.extract_plain_text():
        spell = SystemMessage(content=prompt)
        await setprompt_cmd.finish("已设置提示词")
    else:
        spell = SystemMessage(content="")
        context = []
        await setprompt_cmd.finish("已清除提示词")


@resetmem.handle()
async def reset():
    global context_count
    context.reset()
    context_count = 0
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
        global context_limit, context_count
        token = config.marshoai_token
        endpoint = "https://models.inference.ai.azure.com"
        #msg = await UniMessage.generate(message=message)
        client = ChatCompletionsClient(
              endpoint=endpoint,
              credential=AzureKeyCredential(token),
            )
        if not text:
            await UniMessage(
                """MarshoAI Alpha? by Asankilp
用法：
  marsho <聊天内容>
与 Marsho 进行对话。当模型为gpt时，可以带上图片进行对话。
  changemodel
切换 AI 模型。仅超级用户可用。
  reset
重置上下文。仅超级用户可用。
注意事项：
当 Marsho 回复消息为None或以content_filter开头的错误信息时，表示该消息被内容过滤器过滤，请调整你的聊天内容确保其合规。
当回复以RateLimitReached开头的错误信息时，该 AI 模型的次数配额已用尽，请联系Bot管理员。
※本AI的回答"按原样"提供，不提供担保，不代表开发者任何立场。AI也会犯错，请仔细甄别回答的准确性。
当前使用的模型："""+model_name).send()
            return
        if context_count >= context_limit:
            await UniMessage("上下文数量达到阈值。已自动重置上下文。").send()
            context.reset()
            context_count = 0
       # await UniMessage(str(text)).send()
        try:
            usermsg = [TextContentItem(text=str(text).replace("[image]",""))]
            if model_name == "gpt-4o" or model_name == "gpt-4o-mini":
                for i in message:
                     if i.type == "image":
                        imgurl = i.data["url"]
                        print(imgurl)
                        await download_file(str(imgurl))
                        picmsg = ImageContentItem(image_url=ImageUrl.load(
                                image_file="./azureaipic.png",
                                image_format=Image.open("azureaipic.png").format
                                )
                            )
                        usermsg.append(picmsg)
                #await UniMessage(str(context+[UserMessage(content=usermsg)])).send()
            else:
                usermsg = str(text)
                #await UniMessage('非gpt').send()
            response = await client.complete(
                        messages=context.build()+[UserMessage(content=usermsg)],
                        model=model_name   
                  )
            #await UniMessage(str(response)).send()
            choice = response.choices[0]
            if choice["finish_reason"] == "stop":
                context.append(UserMessage(content=usermsg))
                context.append(choice.message)
                context_count += 1
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
            traceback.print_exc()
            return
