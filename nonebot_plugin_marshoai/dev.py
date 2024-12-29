import os
from pathlib import Path

from nonebot import get_driver, logger, require
from nonebot.adapters import Bot, Event
from nonebot.matcher import Matcher
from nonebot.typing import T_State

from nonebot_plugin_marshoai.plugin.load import reload_plugin

from .azure import context
from .config import config
from .plugin.func_call.models import SessionContext

require("nonebot_plugin_alconna")

from nonebot.permission import SUPERUSER
from nonebot_plugin_alconna import (
    Alconna,
    Args,
    MultiVar,
    Subcommand,
    UniMessage,
    on_alconna,
)

from .observer import *
from .plugin import get_plugin, get_plugins
from .plugin.func_call.caller import get_function_calls

driver = get_driver()

function_call = on_alconna(
    command=Alconna(
        f"{config.marshoai_default_name}.funccall",
        Subcommand(
            "call",
            Args["function_name", str]["kwargs", MultiVar(str), []],
            alias={"c"},
        ),
        Subcommand(
            "list",
            alias={"l"},
        ),
        Subcommand("info", Args["function_name", str], alias={"i"}),
    ),
    aliases={"mfc"},
    permission=SUPERUSER,
)


@function_call.assign("list")
async def list_functions():
    reply = "共有如下可调用函数:\n"
    for function in get_function_calls().values():
        reply += f"- {function.short_info}\n"
    await UniMessage(reply).send()


@function_call.assign("info")
async def function_info(function_name: str):
    function = get_function_calls().get(function_name)
    if function is None:
        await UniMessage(f"未找到函数 {function_name}").send()
        return
    await UniMessage(str(function)).send()


@function_call.assign("call")
async def call_function(
    function_name: str,
    kwargs: list[str],
    event: Event,
    bot: Bot,
    matcher: Matcher,
    state: T_State,
):
    function = get_function_calls().get(function_name)
    if function is None:
        for f in get_function_calls().values():
            if f.short_name == function_name:
                function = f
                break
        else:
            await UniMessage(f"未找到函数 {function_name}").send()
            return
    await UniMessage(
        str(
            await function.with_ctx(
                SessionContext(event=event, bot=bot, matcher=matcher, state=state)
            ).call(**{i.split("=", 1)[0]: i.split("=", 1)[1] for i in kwargs})
        )
    ).send()


@on_file_system_event(
    (str(Path(__file__).parent / "plugins"), *config.marshoai_plugin_dirs),
    recursive=True,
)
def on_plugin_file_change(event):
    if event.src_path.endswith(".py"):
        logger.info(f"文件变动: {event.src_path}")
        # 层层向上查找到插件目录
        dir_list: list[str] = event.src_path.split("/")  # type: ignore
        dir_list[-1] = dir_list[-1].split(".", 1)[0]
        dir_list.reverse()
        for plugin_name in dir_list:
            if plugin := get_plugin(plugin_name):
                if plugin.module_path.endswith("__init__.py"):
                    # 包插件
                    if os.path.dirname(plugin.module_path).replace(
                        "\\", "/"
                    ) in event.src_path.replace("\\", "/"):
                        logger.debug(f"找到变动插件: {plugin.name}，正在重新加载")
                        reload_plugin(plugin)
                        context.reset_all()
                        break
                else:
                    # 单文件插件
                    if plugin.module_path == event.src_path:
                        logger.debug(f"找到变动插件: {plugin.name}，正在重新加载")
                        reload_plugin(plugin)
                        context.reset_all()
                        break
        else:
            logger.debug("未找到变动插件")
            return
