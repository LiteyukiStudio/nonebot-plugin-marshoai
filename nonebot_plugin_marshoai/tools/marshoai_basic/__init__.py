import os

from zhDateTime import DateTime

weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
time_prompt = "现在的时间是{date_time}，{weekday_name}，农历{lunar_date}。"


async def get_weather(location: str):
    return f"{location}的温度是114514℃。"


async def get_current_env():
    ver = os.popen("uname -a").read()
    return str(ver)


async def get_current_time():
    current_time = DateTime.now()

    return time_prompt.format(
        date_time=current_time.strftime("%Y年%m月%d日 %H:%M:%S"),
        weekday_name=weekdays[current_time.weekday()],
        lunar_date=current_time.to_lunar().date_hanzify(
            "{干支年}{生肖}年{月份}月{日期}日"
        ),
    )
