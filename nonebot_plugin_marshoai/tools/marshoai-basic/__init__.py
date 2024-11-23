import os
from datetime import datetime
from zhDateTime import DateTime
async def get_weather(location: str):
    return f"{location}的温度是114514℃。"
    
async def get_current_env():
    ver = os.popen("uname -a").read()
    return str(ver)

async def get_current_time():
    current_time = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
    current_lunar_date = (DateTime.now().to_lunar().date_hanzify()[5:])
    time_prompt = f"现在的时间是{current_time}，农历{current_lunar_date}。"
    return time_prompt