from nonebot_plugin_marshoai.plugin import (
    Integer,
    Parameter,
    PluginMetadata,
    String,
    on_function_call,
)

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
    """使用姓名，年龄，性别进行算命

    Args:
        age (int): _description_
        name (str): _description_
        gender (str): _description_

    Returns:
        str: _description_
    """

    # 进行一系列算命操作...

    return f"{name}，你的年龄是{age}，你的性别很好"


@on_function_call(description="获取一个地点未来一段时间的天气").params(
    location=String(description="地点名称，可以是城市名、地区名等"),
    days=Integer(description="天数", minimum=1, maximum=30),
    unit=String(enum=["摄氏度", "华氏度"], description="温度单位"),
)
async def get_weather(location: str, days: int, unit: str) -> str:
    """获取一个地点未来一段时间的天气

    Args:
        location (str): 地点名称，可以是城市名、地区名等
        days (int): 天数
        unit (str): 温度单位

    Returns:
        str: 天气信息
    """

    # 进行一系列获取天气操作...

    return f"{location}未来{days}天的天气信息..."
