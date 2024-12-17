from httpx import AsyncClient
from newspaper import Article  # type: ignore
from nonebot import logger

from nonebot_plugin_marshoai.plugin.func_call.caller import on_function_call
from nonebot_plugin_marshoai.plugin.func_call.params import String

from .utils import make_html_summary

headers = {
    "User-Agent": "Firefox/90.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
}


@on_function_call(
    description="使用网页链接(url)获取网页内容摘要,可以让AI上网查询资料"
).params(
    url=String(description="网页链接"),
)
async def get_web_content(url: str) -> str:
    """使用网页链接获取网页内容摘要
    为什么要获取摘要，不然token超限了

    Args:
        url (str): _description_

    Returns:
        str: _description_
    """
    async with AsyncClient(headers=headers) as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                article = Article(url)
                article.download(input_html=response.text)
                article.parse()
                if article.text:
                    return article.text
                elif article.html:
                    return await make_html_summary(article.html)
                else:
                    return "未能获取到有效的网页内容"
            else:
                return "获取网页内容失败" + str(response.status_code)

        except Exception as e:
            logger.error(f"marsho builtin: 获取网页内容失败: {e}")
            return "获取网页内容失败：" + str(e)

        return "未能获取到有效的网页内容"
