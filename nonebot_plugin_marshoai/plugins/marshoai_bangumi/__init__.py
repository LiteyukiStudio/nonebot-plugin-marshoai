import traceback

import httpx

from nonebot_plugin_marshoai.plugin import PluginMetadata, function_call

__marsho_meta__ = PluginMetadata(
    name="Bangumi 番剧信息",
    description="Bangumi 番剧信息",
    usage="Bangumi 番剧信息",
    author="Liteyuki",
    homepage="",
)


async def fetch_calendar():
    url = "https://api.bgm.tv/calendar"
    headers = {
        "User-Agent": "LiteyukiStudio/nonebot-plugin-marshoai (https://github.com/LiteyukiStudio/nonebot-plugin-marshoai)"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        # print(response.text)
        return response.json()


@function_call
async def get_bangumi_news() -> str:
    """获取今天的新番（动漫）列表，在调用之前，你需要知道今天星期几。

    Returns:
        _type_: _description_
    """
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


@function_call
def test_sync() -> str:
    return "sync"
