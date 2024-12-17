import os

from zhDateTime import DateTime

from nonebot_plugin_marshoai.plugin import String, on_function_call


@on_function_call(description="获取当前时间，日期和星期")
async def get_current_time() -> str:
    """获取当前的时间和日期"""
    current_time = DateTime.now().strftime("%Y.%m.%d %H:%M:%S")
    current_weekday = DateTime.now().weekday()

    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    current_weekday_name = weekdays[current_weekday]

    current_lunar_date = DateTime.now().to_lunar().date_hanzify()[5:]
    time_prompt = f"现在的时间是 {current_time}，{current_weekday_name}，农历 {current_lunar_date}。"
    return time_prompt
