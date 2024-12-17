import traceback

import httpx
from zhDateTime import DateTime

from nonebot_plugin_marshoai.plugin import PluginMetadata, on_function_call
from nonebot_plugin_marshoai.plugin.func_call.params import String

# 定义插件元数据
__marsho_meta__ = PluginMetadata(
    name="Bangumi日历",
    author="MarshoAI",
    description="这个插件可以帮助你获取Bangumi的日历信息~",
)


@on_function_call(description="获取Bangumi日历信息")
async def get_bangumi_news() -> str:
    async def fetch_calendar():
        url = "https://api.bgm.tv/calendar"
        headers = {
            "User-Agent": "LiteyukiStudio/nonebot-plugin-marshoai (https://github.com/LiteyukiStudio/nonebot-plugin-marshoai)"
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            # print(response.text)
            return response.json()

    try:
        result = await fetch_calendar()
        info = ""
        current_weekday = DateTime.now().weekday()
        weekdays = [
            "星期一",
            "星期二",
            "星期三",
            "星期四",
            "星期五",
            "星期六",
            "星期日",
        ]
        current_weekday_name = weekdays[current_weekday]
        info += f"今天{current_weekday_name}。\n"
        for i in result:
            weekday = i["weekday"]["cn"]
            # print(weekday)
            info += f"{weekday}:"
            items = i["items"]
            for item in items:
                name = item["name_cn"]
                info += f"《{name}》"
            info += ""
        return info
    except Exception as e:
        traceback.print_exc()
        return ""
