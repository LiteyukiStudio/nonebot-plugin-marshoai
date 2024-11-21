import contextlib
import traceback
import json
from typing import Optional

from arclet.alconna import Alconna, Args, AllParam                                      
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
from .util_hunyuan import *
from .config import config
genimage_cmd = on_alconna(
    Alconna(
        "genimage",
        Args["prompt?", str],
        )
    )

@genimage_cmd.handle()
async def genimage(event: Event, prompt=None):
    if not prompt:
       await genimage_cmd.finish("无提示词")
    try:
        result = generate_image(prompt)
        url = json.loads(result)["ResultImage"]
        await UniMessage.image(url=url).send()
    except Exception as e:
       # await genimage_cmd.finish(str(e))
        traceback.print_exc()
