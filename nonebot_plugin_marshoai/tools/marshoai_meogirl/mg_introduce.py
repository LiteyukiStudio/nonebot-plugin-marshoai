import re
import urllib.parse

import httpx
from bs4 import BeautifulSoup  # type: ignore
from nonebot.log import logger

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}


async def get_async_data(url):
    async with httpx.AsyncClient(timeout=None) as client:
        return await client.get(url, headers=headers)


async def introduce(msg: str):
    logger.info(f'介绍 : "{msg}" ...')
    result = ""

    url = "https://mzh.moegirl.org.cn/" + urllib.parse.quote_plus(msg)
    response = await get_async_data(url)
    logger.success(f'连接"{url}"完成, 状态码 : {response.status_code}')

    soup = BeautifulSoup(response.text, "html.parser")

    # 正常页
    if response.status_code == 200:
        """
        萌娘百科页面结构
        div#mw-content-text
        └── div#404search           # 空白页面出现
        └── div.mw-parser-output    # 正常页面
            └── div, p, table ...   # 大量的解释项
        """
        result += msg + "\n"

        img = soup.find("img", class_="infobox-image")
        if img:
            result += f"![ {msg} ]( {img['src']} ) \n"

        div = soup.find("div", class_="mw-parser-output")
        if div:
            p_tags = div.find_all("p")
            num = 0
            for p_tag in p_tags:
                p = str(p_tag)
                p = re.sub(
                    r"<script.*?</script>|<style.*?</style>", "", p, flags=re.DOTALL
                )
                p = re.sub(r"<.*?>", "", p, flags=re.DOTALL)
                p = re.sub(r"\[.*?]", "", p, flags=re.DOTALL)

                if p != "":
                    result += str(p)

                    num += 1
                    if num >= 20:
                        break
        return result

    # 空白页
    elif response.status_code == 404:
        logger.info(f'未找到"{msg}", 进行搜索')

        from . import mg_search

        context = await mg_search.search(msg, 1)
        keyword = re.search(r".*?\n", context, flags=re.DOTALL).group()[:-1]  # type: ignore

        logger.success(f'搜索完成, 打开"{keyword}"')
        return await introduce(keyword)

    # 搜索失败
    elif response.status_code == 301:
        return f"未找到{msg}"

    else:
        logger.error(f"网络错误, 状态码 : {response.status_code}")
        return f"网络错误, 状态码 : {response.status_code}"
