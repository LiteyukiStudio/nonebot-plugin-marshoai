import traceback

import httpx


async def fetch_calendar():
    url = "https://api.bgm.tv/calendar"
    headers = {
        "User-Agent": "LiteyukiStudio/nonebot-plugin-marshoai (https://github.com/LiteyukiStudio/nonebot-plugin-marshoai)"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        # print(response.text)
        return response.json()


async def get_bangumi_news():
    result = await fetch_calendar()
    info = ""
    try:
        for i in result:
            weekday = i["weekday"]["cn"]
            # print(weekday)
            info += f"{weekday}:"
            items = i["items"]
            for item in items:
                name = item["name_cn"]
                info += f"《{name}》"
            info += "\n"
        return info
    except Exception as e:
        traceback.print_exc()
        return ""
