import os
import platform

import psutil
from nonebot.adapters import Bot, Event

# from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.permission import SUPERUSER

from nonebot_plugin_marshoai.plugin import (
    Integer,
    Parameter,
    PluginMetadata,
    String,
    on_function_call,
)
from nonebot_plugin_marshoai.plugin.func_call.caller import Caller

__marsho_meta__ = PluginMetadata(
    name="SnowyKami 测试插件",
    description="A test plugin for SnowyKami",
    usage="SnowyKami Test Plugin",
)


@on_function_call(description="使用姓名，年龄，性别进行算命").params(
    age=Integer(description="年龄"),
    name=String(description="姓名"),
    gender=String(enum=["男", "女"], description="性别"),
)
async def fortune_telling(age: int, name: str, gender: str) -> str:
    """使用姓名，年龄，性别进行算命"""

    # 进行一系列算命操作...

    return f"{name}，你的年龄是{age}，你的性别很好"


@on_function_call(description="获取一个地点未来一段时间的天气").params(
    location=String(description="地点名称，可以是城市名、地区名等"),
    days=Integer(description="天数", minimum=1, maximum=30),
    unit=String(enum=["摄氏度", "华氏度"], description="温度单位", default="摄氏度"),
)
async def get_weather(location: str, days: int, unit: str) -> str:
    """获取一个地点未来一段时间的天气"""

    # 进行一系列获取天气操作...

    return f"{location}未来{days}天的天气很好，全都是晴天，温度是34"


@on_function_call(description="获取设备物理地理位置")
def get_location() -> str:
    """获取设备物理地理位置"""

    # 进行一系列获取地理位置操作...

    return "日本 东京都 世田谷区"


@on_function_call(description="获取聊天者个人信息及发送的消息和function call调用参数")
async def get_user_info(e: Event, c: Caller) -> str:
    return (
        f"用户ID: {e.user_id} "
        "用户昵称: {e.sender.nickname} "
        "FC调用参数:{c._parameters} "
        "消息内容: {e.raw_message}"
    )


@on_function_call(description="获取设备信息")
def get_device_info() -> str:
    """获取机器人所运行的设备信息"""

    # 进行一系列获取设备信息操作...

    data = {
        "cpu 性能": f"{psutil.cpu_percent()}% {psutil.cpu_freq().current:.2f}MHz {psutil.cpu_count()}线程 {psutil.cpu_count(logical=False)}物理核",
        "memory 内存": f"{psutil.virtual_memory().percent}% {psutil.virtual_memory().available / 1024 / 1024 / 1024:.2f}/{psutil.virtual_memory().total / 1024 / 1024 / 1024:.2f}GB",
        "swap 交换分区": f"{psutil.swap_memory().percent}% {psutil.swap_memory().used / 1024 / 1024 / 1024:.2f}/{psutil.swap_memory().total / 1024 / 1024 / 1024:.2f}GB",
        "cpu 信息": f"{psutil.cpu_stats()}",
        "system 系统": f"system: {platform.system()}, version: {platform.version()}, arch: {platform.architecture()}, machine: {platform.machine()}",
    }
    return str(data)


@on_function_call(description="在设备上运行Python代码,需要超级用户权限").params(
    code=String(description="Python代码内容")
).permission(SUPERUSER)
async def run_python_code(code: str, b: Bot, e: Event) -> str:
    """运行Python代码"""
    try:
        r = eval(code)
    except Exception as e:
        return "运行出错: " + str(e)
    return "运行成功: " + str(r)


@on_function_call(
    description="在设备上运行shell命令, Run command on this device"
).params(command=String(description="shell命令内容")).permission(SUPERUSER)
async def run_shell_command(command: str, b: Bot, e: Event) -> str:
    """运行shell命令"""
    try:
        r = os.popen(command).read()
    except Exception as e:
        return "运行出错: " + str(e)
    return "运行成功: " + str(r)
