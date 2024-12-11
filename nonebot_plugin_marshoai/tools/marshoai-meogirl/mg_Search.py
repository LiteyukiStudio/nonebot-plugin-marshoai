from nonebot.log import logger

import re
import httpx
import urllib.parse
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}

async def get_async_data (url):
    async with httpx.AsyncClient(timeout = None) as client:
        return await client.get(url, headers = headers)

async def search(msg : str, num : int):
    logger.info(f"搜索 : \"{msg}\"")
    result = ""

    url = "https://mzh.moegirl.org.cn/index.php?search=" + urllib.parse.quote_plus(msg)
    response = await get_async_data(url)
    logger.success(f"连接\"{url}\"完成, 状态码 : {response.status_code}")

    # 正常搜索
    if response.status_code == 200:
        """
            萌娘百科搜索页面结构
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

        # 检测ul.mw-search-results, 是否有结果
        ul_tag = soup.find("ul", class_ = "mw-search-results")
        if ul_tag:
            li_tags = ul_tag.find_all("li")
            for li_tag in li_tags:

                div_heading = li_tag.find("div", class_ = "mw-search-result-heading")
                if div_heading:
                    a_tag = div_heading.find("a")
                    result += a_tag["title"] + "\n"
                    logger.info(f"搜索到 : \"{a_tag["title"]}\"")

                div_result = li_tag.find("div", class_="searchresult")
                if div_result:
                    content = str(div_result).replace("<div class=\"searchresult\">", "").replace("</div>", "")
                    content = content.replace("<span class=\"searchmatch\">", "").replace("</span>", "")
                    result += content + "\n"

                num -= 1
                if num == 0:
                    break
            return result

        # 无ul.mw-search-results, 无结果
        else:
            logger.info("无结果")
            return "无结果"

    # 重定向
    elif response.status_code == 302:
        logger.info(f"\"{msg}\"已被重定向至\"{response.headers.get("location")}\"")
        # 读取重定向结果
        response = await get_async_data(response.headers.get("location"))
        soup = BeautifulSoup(response.text, "html.parser")
        logger.success("重定向成功")
        num = 0

        """
            萌娘百科重定向介绍页面结构
            div#mw-content-text
            └── div.mw-parser-output    # 介绍页面
                └── ....
                └── p ?                 # 可能存在的空p
                └── p                   # 人物介绍
                └── ...
        """

        result += msg + "\n"
        img = soup.find("img", class_="infobox-image")
        if img:
            logger.info(f"照片{img["src"]}")
            result += f"![ {msg} ]( {img["src"]} ) \n"

        div = soup.find("div", class_="mw-parser-output")
        if div:
            p_tags = div.find_all("p")
            for p_tag in p_tags:
                p = str(p_tag)
                p = re.sub(r"<script.*?</script>|<style.*?</style>", "", p, flags=re.DOTALL)
                p = re.sub(r"<.*?>", "", p, flags = re.DOTALL)
                p = re.sub(r"\[.*?]", "", p, flags = re.DOTALL)
                if p != "":
                    result += str(p)

                    num += 1
                    if num >= 5:
                        break
        return result

    # 状态码非200或302
    else:
        logger.error(f"网络错误, 状态码 : {response.status_code}")
        return f"网络错误, 状态码 : {response.status_code}"
