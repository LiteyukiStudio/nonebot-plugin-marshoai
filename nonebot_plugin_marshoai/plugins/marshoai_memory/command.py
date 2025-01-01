import json

from arclet.alconna import Alconna, Args, Subcommand
from nonebot import logger
from nonebot.adapters import Bot, Event
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from nonebot_plugin_alconna import on_alconna
from nonebot_plugin_localstore import get_plugin_data_file

from nonebot_plugin_marshoai.config import config

marsho_memory_cmd = on_alconna(
    Alconna(
        f"{config.marshoai_default_name}.memory",
        Subcommand("view", alias={"v"}),
        Subcommand("reset", alias={"r"}),
    ),
    priority=10,
    block=True,
)

memory_path = get_plugin_data_file("memory.json")


@marsho_memory_cmd.assign("view")
async def view_memory(matcher: Matcher, state: T_State, event: Event):
    user_id = str(event.get_user_id())
    with open(memory_path, "r", encoding="utf-8") as f:
        memory_data = json.load(f)
    memorys = memory_data.get(user_id, [])
    if not memorys:
        await matcher.finish("好像对ta还没有任何记忆呢~")
    await matcher.finish("这些是有关ta的记忆：" + "\n".join(memorys))


@marsho_memory_cmd.assign("reset")
async def reset_memory(matcher: Matcher, state: T_State, event: Event):
    user_id = str(event.get_user_id())
    with open(memory_path, "r", encoding="utf-8") as f:
        memory_data = json.load(f)
    if user_id in memory_data:
        del memory_data[user_id]
        with open(memory_path, "w", encoding="utf-8") as f:
            json.dump(memory_data, f, ensure_ascii=False, indent=4)
        await matcher.finish("记忆已重置~")
    await matcher.finish("没有找到该用户的记忆~")
