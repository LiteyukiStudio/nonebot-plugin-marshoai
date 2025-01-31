import os

from zhDateTime import DateTime  # type: ignore

from nonebot_plugin_marshoai.plugin import PluginMetadata, String, on_function_call

# from .web import *
# 定义插件元数据
__marsho_meta__ = PluginMetadata(
    name="基本功能",
    author="MarshoAI",
    description="这个插件提供基本的功能，比如获取当前时间和日期。",
)


weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]


@on_function_call(description="获取当前时间，日期和星期")
async def get_current_time() -> str:
    """获取当前的时间和日期"""
    current_time = DateTime.now()

    time_prompt = "现在的时间是 {}，{}，{}。".format(
        current_time.strftime("%Y.%m.%d %H:%M:%S"),
        weekdays[current_time.weekday()],
        current_time.chinesize.date_hanzify("农历{干支年}{生肖}年 {月份}月{数序日}"),
    )
    return time_prompt
