from nonebot.adapters.onebot.v11 import MessageEvent

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
async def get_user_info(e: MessageEvent, c: Caller) -> str:
    return f"用户ID: {e.user_id} 用户昵称: {e.sender.nickname} FC调用参数:{c._parameters} 消息内容: {e.raw_message}"
