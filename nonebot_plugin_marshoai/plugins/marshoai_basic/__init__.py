import os

from zhDateTime import DateTime


async def get_weather(location: str):
    return f"{location}的温度是114514℃。"


async def get_current_env():
    ver = os.popen("uname -a").read()
    return str(ver)


async def get_current_time():
    current_time = DateTime.now().strftime("%Y.%m.%d %H:%M:%S")
    current_weekday = DateTime.now().weekday()

    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    current_weekday_name = weekdays[current_weekday]

    current_lunar_date = DateTime.now().to_lunar().date_hanzify()[5:]
    time_prompt = f"现在的时间是{current_time}，{current_weekday_name}，农历{current_lunar_date}。"
    return time_prompt
