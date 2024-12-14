---
title: index
collapsed: true
---
# **模块** `nonebot_plugin_marshoai.tools.marshoai_basic`

---
### ***async func*** `get_weather(location: str)`


<details>
<summary> <b>源代码</b> 或 <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_basic/__init__.py#L6' target='_blank'>在GitHub上查看</a></summary>

```python
async def get_weather(location: str):
    return f'{location}的温度是114514℃。'
```
</details>

---
### ***async func*** `get_current_env()`


<details>
<summary> <b>源代码</b> 或 <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_basic/__init__.py#L10' target='_blank'>在GitHub上查看</a></summary>

```python
async def get_current_env():
    ver = os.popen('uname -a').read()
    return str(ver)
```
</details>

---
### ***async func*** `get_current_time()`


<details>
<summary> <b>源代码</b> 或 <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_basic/__init__.py#L15' target='_blank'>在GitHub上查看</a></summary>

```python
async def get_current_time():
    current_time = DateTime.now().strftime('%Y.%m.%d %H:%M:%S')
    current_weekday = DateTime.now().weekday()
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    current_weekday_name = weekdays[current_weekday]
    current_lunar_date = DateTime.now().to_lunar().date_hanzify()[5:]
    time_prompt = f'现在的时间是{current_time}，{current_weekday_name}，农历{current_lunar_date}。'
    return time_prompt
```
</details>

