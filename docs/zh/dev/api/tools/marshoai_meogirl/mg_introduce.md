---
title: mg_introduce
---
# **模块** `nonebot_plugin_marshoai.tools.marshoai_meogirl.mg_introduce`

---
### ***async func*** `get_async_data(url)`


<details>
<summary> <b>源代码</b> 或 <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_meogirl/mg_introduce.py#L13' target='_blank'>在GitHub上查看</a></summary>

```python
async def get_async_data(url):
    async with httpx.AsyncClient(timeout=None) as client:
        return await client.get(url, headers=headers)
```
</details>

---
### ***async func*** `introduce(msg: str)`


<details>
<summary> <b>源代码</b> 或 <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_meogirl/mg_introduce.py#L18' target='_blank'>在GitHub上查看</a></summary>

```python
async def introduce(msg: str):
    logger.info(f'介绍 : "{msg}" ...')
    result = ''
    url = 'https://mzh.moegirl.org.cn/' + urllib.parse.quote_plus(msg)
    response = await get_async_data(url)
    logger.success(f'连接"{url}"完成, 状态码 : {response.status_code}')
    soup = BeautifulSoup(response.text, 'html.parser')
    if response.status_code == 200:
        '\n        萌娘百科页面结构\n        div#mw-content-text\n        └── div#404search           # 空白页面出现\n        └── div.mw-parser-output    # 正常页面\n            └── div, p, table ...   # 大量的解释项\n        '
        result += msg + '\n'
        img = soup.find('img', class_='infobox-image')
        if img:
            result += f'![ {msg} ]( {img['src']} ) \n'
        div = soup.find('div', class_='mw-parser-output')
        if div:
            p_tags = div.find_all('p')
            num = 0
            for p_tag in p_tags:
                p = str(p_tag)
                p = re.sub('<script.*?</script>|<style.*?</style>', '', p, flags=re.DOTALL)
                p = re.sub('<.*?>', '', p, flags=re.DOTALL)
                p = re.sub('\\[.*?]', '', p, flags=re.DOTALL)
                if p != '':
                    result += str(p)
                    num += 1
                    if num >= 20:
                        break
        return result
    elif response.status_code == 404:
        logger.info(f'未找到"{msg}", 进行搜索')
        from . import mg_search
        context = await mg_search.search(msg, 1)
        keyword = re.search('.*?\\n', context, flags=re.DOTALL).group()[:-1]
        logger.success(f'搜索完成, 打开"{keyword}"')
        return await introduce(keyword)
    elif response.status_code == 301:
        return f'未找到{msg}'
    else:
        logger.error(f'网络错误, 状态码 : {response.status_code}')
        return f'网络错误, 状态码 : {response.status_code}'
```
</details>

### var `keyword`

- **说明**: type: ignore

- **默认值**: `re.search('.*?\\n', context, flags=re.DOTALL).group()[:-1]`

