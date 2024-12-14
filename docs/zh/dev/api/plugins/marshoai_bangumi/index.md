---
title: index
collapsed: true
---
# **模块** `nonebot_plugin_marshoai.plugins.marshoai_bangumi`

---
### ***async func*** `fetch_calendar()`


<details>
<summary> <b>源代码</b> 或 <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugins/marshoai_bangumi/__init__.py#L16' target='_blank'>在GitHub上查看</a></summary>

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
`@function_call`
### ***async func*** `get_bangumi_news() -> str`

**说明**: 获取今天的新番（动漫）列表，在调用之前，你需要知道今天星期几。


**返回**: _type_: _description_


<details>
<summary> <b>源代码</b> 或 <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugins/marshoai_bangumi/__init__.py#L28' target='_blank'>在GitHub上查看</a></summary>

```python
@function_call
async def get_bangumi_news() -> str:
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

---
`@function_call`
### ***func*** `test_sync() -> str`


<details>
<summary> <b>源代码</b> 或 <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugins/marshoai_bangumi/__init__.py#L53' target='_blank'>在GitHub上查看</a></summary>

```python
@function_call
def test_sync() -> str:
    return 'sync'
```
</details>

