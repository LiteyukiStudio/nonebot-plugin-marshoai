---
title: index
collapsed: true
---
# **Module** `nonebot_plugin_marshoai.tools.marshoai_bangumi`

---
### ***async func*** `fetch_calendar()`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_bangumi/__init__.py#L6' target='_blank'>View on GitHub</a></summary>

```python
async def fetch_calendar():
    url = 'https://api.bgm.tv/calendar'
    headers = {'User-Agent': 'LiteyukiStudio/nonebot-plugin-marshoai (https://github.com/LiteyukiStudio/nonebot-plugin-marshoai)'}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()
```
</details>

---
### ***async func*** `get_bangumi_news()`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_bangumi/__init__.py#L17' target='_blank'>View on GitHub</a></summary>

```python
async def get_bangumi_news():
    result = await fetch_calendar()
    info = ''
    try:
        for i in result:
            weekday = i['weekday']['cn']
            info += f'{weekday}:'
            items = i['items']
            for item in items:
                name = item['name_cn']
                info += f'《{name}》'
            info += '\n'
        return info
    except Exception as e:
        traceback.print_exc()
        return ''
```
</details>

