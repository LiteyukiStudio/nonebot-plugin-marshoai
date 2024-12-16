import time

from httpx import AsyncClient
from newspaper import Article
from nonebot import logger

from nonebot_plugin_marshoai.plugin.func_call.caller import on_function_call
from nonebot_plugin_marshoai.plugin.func_call.params import String

headers = {
    "User-Agent": "Firefox/90.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
}


@on_function_call(
    description="使用网页链接(url)获取网页内容摘要,可以让AI上网查询资料"
).params(
    url=String(description="网页链接"),
    typ=String(description="获取类型，摘要还是内容", enum=["摘要", "内容"]),
)
async def get_web_content(url: str, typ: str) -> str:
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
            t1 = time.time()
            article = Article(url)
            article.set_html(response.text)
            article.parse()
            t2 = time.time()
            logger.debug(f"获取网页内容耗时: {t2 - t1}")
            if typ == "摘要":
                return f"标题: {article.title}\n作者: {article.authors}\n发布日期: {article.publish_date}"
            elif typ == "内容":
                return f"标题: {article.title}\n作者: {article.authors}\n发布日期: {article.publish_date}\n摘要: {article.summary}\n正文: {article.text}"
        except Exception as e:
            logger.error(f"marsho builtin: 获取网页内容失败: {e}")
            return "获取网页内容失败：" + str(e)

        return "未能获取到有效的网页内容"
