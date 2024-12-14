---
title: mg_search
---
# **Module** `nonebot_plugin_marshoai.tools.marshoai_meogirl.mg_search`

---
### ***async func*** `get_async_data(url)`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_meogirl/mg_search.py#L12' target='_blank'>View on GitHub</a></summary>

```python
async def get_async_data(url):
    async with httpx.AsyncClient(timeout=None) as client:
        return await client.get(url, headers=headers)
```
</details>

---
### ***async func*** `search(msg: str, num: int)`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_meogirl/mg_search.py#L17' target='_blank'>View on GitHub</a></summary>

```python
async def search(msg: str, num: int):
    logger.info(f'搜索 : "{msg}" ...')
    result = ''
    url = 'https://mzh.moegirl.org.cn/index.php?search=' + urllib.parse.quote_plus(msg)
    response = await get_async_data(url)
    logger.success(f'连接"{url}"完成, 状态码 : {response.status_code}')
    if response.status_code == 200:
        '\n        萌娘百科搜索页面结构\n        div.searchresults\n        └── p ...\n        └── ul.mw-search-results                        # 若无, 证明无搜索结果\n            └── li                                      # 一个搜索结果\n                └── div.mw-search-result-heading > a    # 标题\n                └── div.mw-searchresult                 # 内容\n                └── div.mw-search-result-data\n            └── li ...\n            └── li ...\n        '
        soup = BeautifulSoup(response.text, 'html.parser')
        ul_tag = soup.find('ul', class_='mw-search-results')
        if ul_tag:
            li_tags = ul_tag.find_all('li')
            for li_tag in li_tags:
                div_heading = li_tag.find('div', class_='mw-search-result-heading')
                if div_heading:
                    a_tag = div_heading.find('a')
                    result += a_tag['title'] + '\n'
                    logger.info(f'搜索到 : "{a_tag['title']}"')
                div_result = li_tag.find('div', class_='searchresult')
                if div_result:
                    content = str(div_result).replace('<div class="searchresult">', '').replace('</div>', '')
                    content = content.replace('<span class="searchmatch">', '').replace('</span>', '')
                    result += content + '\n'
                num -= 1
                if num == 0:
                    break
            return result
        else:
            logger.info('无结果')
            return '无结果'
    elif response.status_code == 302:
        logger.info(f'"{msg}"已被重定向至"{response.headers.get('location')}"')
        from . import mg_introduce
        return await mg_introduce.introduce(msg)
    else:
        logger.error(f'网络错误, 状态码 : {response.status_code}')
        return f'网络错误, 状态码 : {response.status_code}'
```
</details>

### var `soup`

- **Description**: 

- **Default**: `BeautifulSoup(response.text, 'html.parser')`

