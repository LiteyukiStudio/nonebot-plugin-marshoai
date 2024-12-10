from nonebot.log import logger

import re
import httpx
from bs4 import BeautifulSoup

async def search(msg : str, num : int):
    logger.info(f"搜索 : \"{msg}\"")
    result = ""

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    }
    url = "https://mzh.moegirl.org.cn/index.php?search=" + msg
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers = headers)
        logger.info(response.headers.get('Location'))
        logger.info(f"连接萌娘百科中, 状态码 : {response.status_code}")

        """
            萌娘百科搜索页面结构
            div.searchresults                               # 若无, 证明页面已重定向
            └── p ...
            └── ul.mw-search-results                        # 若无, 证明无搜索结果
                └── li                                      # 一个搜索结果
                    └── div.mw-search-result-heading > a    # 标题
                    └── div.mw-searchresult                 # 内容
                    └── div.mw-search-result-data
                └── li ...
                └── li ...
        """
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # 检测div.searchresults, 是否已重定向
            if soup.find('div', class_='searchresults'):
                # 检测ul.mw-search-results, 是否有结果
                if soup.find('ul', class_='mw-search-results'):
                    ul_tag = soup.select('ul.mw-search-results')[0]
                    li_tags = ul_tag.select('li')
                    for li_tag in li_tags:

                        div_heading = li_tag.select('div.mw-search-result-heading')[0]
                        if div_heading:
                            a_tag = div_heading.select('a')[0]
                            result += a_tag['title'] + "\n"
                            logger.info(f"搜索到 : \"{a_tag['title']}\"")

                        div_result = li_tag.find('div', class_='searchresult')
                        if div_result:
                            content = str(div_result).replace('<div class=\"searchresult\">', '').replace('</div>', '')
                            content = content.replace('<span class=\"searchmatch\">', '').replace('</span>', '')
                            result += content + "\n\n"

                        num -= 1
                        if num == 0:
                            break
                    return result

                # 无ul.mw-search-results, 无结果
                else:
                    logger.info("无结果")
                    return "无结果"

            # 无div.searchresults, 重定向
            else:
                logger.info(f"\"{msg}\"已被重定向")
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
                if soup.find('div', class_='mw-parser-output'):
                    div = soup.find('div', class_='mw-parser-output')
                    p_tags = div.select('p')
                    for p_tag in p_tags:
                        p = str(p_tag)
                        p = re.sub(r'<.*?>', '', p)
                        if p != '':
                            result += str(p) + "/n"

                            num += 1
                            if num >= 5:
                                break
                    return result

        # 状态码非200
        else:
            logger.error(f"网络错误, 状态码 : {response.status_code}")
            return f"网络错误, 状态码 : {response.status_code}"
