import urllib.parse

import httpx
from bs4 import BeautifulSoup
from nonebot.log import logger


async def get_async_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            return await client.get(url=url, headers=headers)
    except httpx.TimeoutException:
        return "萌娘百科服务器日常宕机 ..."


async def search(msg: str, num: int) -> str:
    logger.info(f'开始搜索"{msg}"...')
    result = ""

    url = "https://mzh.moegirl.org.cn/index.php?search=" + urllib.parse.quote_plus(msg)
    response = await get_async_data(url)
    logger.success(f'连接"{url}"完成, 状态码 : {response.status_code}')

    # 正常搜索
    if response.status_code == 200:
        """萌娘百科搜索页面结构
        div.searchresults
        └── p ...
        └── ul.mw-search-results                        # 若无, 证明无搜索结果
            └── li                                      # 一个搜索结果
                └── div.mw-search-result-heading > a    # 标题
                └── div.mw-searchresult                 # 内容
                └── div.mw-search-result-data
            └── li ...
            └── li ...
        """
        soup = BeautifulSoup(response.text, "html.parser")
        print(soup)

        # 检测ul.mw-search-results, 是否有结果
        if ul := soup.find("ul", class_="mw-search-results"):
            li__ = ul.find_all("li")
            for li in li__:
                if heading := li.find("div", class_="mw-search-result-heading"):
                    title = heading.find("a")["title"]
                    result += title + "\n"
                    logger.info(f'搜索到 : "{title}"')

                if result := li.find("div", class_="searchresult"):
                    content = (
                        str(result)
                        .replace('<div class="searchresult">', "")
                        .replace("</div>", "")
                        .replace('<span class="searchmatch">', "")
                        .replace("</span>", "")
                    )
                    result += content + "\n"

                num -= 1
                if num == 0:
                    break
            return result

        # 无ul.mw-search-results, 无结果
        else:
            logger.info("无搜索结果")
            return "无搜索结果"

    # 重定向
    elif response.status_code == 302:
        logger.info(f'"{msg}"已被重定向至 "{response.headers.get("location")}"')
        # 读取重定向结果
        from . import mw_introduce

        return await mw_introduce.introduce(msg)

    else:
        logger.error(f"网络错误, 状态码 : {response.status_code}")
        return f"网络错误, 状态码 : {response.status_code}"


import asyncio

print(asyncio.run(search("Tsumiki", 3)))
