---
title: index
collapsed: true
---
# **Module** `nonebot_plugin_marshoai.tools.marshoai_meogirl`

---
### ***async func*** `meogirl()`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_meogirl/__init__.py#L5' target='_blank'>View on GitHub</a></summary>

```python
async def meogirl():
    return mg_info.meogirl()
```
</details>

---
### ***async func*** `search(msg: str, num: int = 3)`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_meogirl/__init__.py#L10' target='_blank'>View on GitHub</a></summary>

```python
async def search(msg: str, num: int=3):
    return str(await mg_search.search(msg, num))
```
</details>

---
### ***async func*** `introduce(msg: str)`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_meogirl/__init__.py#L15' target='_blank'>View on GitHub</a></summary>

```python
async def introduce(msg: str):
    return str(await mg_introduce.introduce(msg))
```
</details>

