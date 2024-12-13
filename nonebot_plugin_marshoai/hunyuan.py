import contextlib
import json
import traceback
from typing import Optional

from arclet.alconna import Alconna, AllParam, Args
from nonebot import get_driver, logger, on_command
from nonebot.adapters import Event, Message
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot_plugin_alconna import MsgTarget, on_alconna
from nonebot_plugin_alconna.uniseg import UniMessage, UniMsg

from .config import config
from .constants import *
from .metadata import metadata
from .models import MarshoContext
from .util_hunyuan import *

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
