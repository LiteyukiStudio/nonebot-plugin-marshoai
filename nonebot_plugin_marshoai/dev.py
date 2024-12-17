from nonebot import require
from nonebot.adapters import Bot, Event
from nonebot.matcher import Matcher
from nonebot.typing import T_State

from nonebot_plugin_marshoai.plugin.func_call.models import SessionContext

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

from .plugin.func_call.caller import get_function_calls

function_call = on_alconna(
    command=Alconna(
        "marsho-function-call",
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
        await UniMessage(f"未找到函数 {function_name}").send()
        return
    await UniMessage(
        str(
            await function.with_ctx(
                SessionContext(event=event, bot=bot, matcher=matcher, state=state)
            ).call(**{i.split("=", 1)[0]: i.split("=", 1)[1] for i in kwargs})
        )
    ).send()
