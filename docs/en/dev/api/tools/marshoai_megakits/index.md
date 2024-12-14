---
title: index
collapsed: true
---
# **Module** `nonebot_plugin_marshoai.tools.marshoai_megakits`

---
### ***async func*** `twisuki()`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_megakits/__init__.py#L5' target='_blank'>View on GitHub</a></summary>

```python
async def twisuki():
    return str(await mk_info.twisuki())
```
</details>

---
### ***async func*** `megakits()`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_megakits/__init__.py#L10' target='_blank'>View on GitHub</a></summary>

```python
async def megakits():
    return str(await mk_info.megakits())
```
</details>

---
### ***async func*** `random_turntable(upper: int, lower: int = 0)`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_megakits/__init__.py#L15' target='_blank'>View on GitHub</a></summary>

```python
async def random_turntable(upper: int, lower: int=0):
    return str(await mk_common.random_turntable(upper, lower))
```
</details>

---
### ***async func*** `number_calc(a: str, b: str, op: str)`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_megakits/__init__.py#L20' target='_blank'>View on GitHub</a></summary>

```python
async def number_calc(a: str, b: str, op: str):
    return str(await mk_common.number_calc(a, b, op))
```
</details>

---
### ***async func*** `morse_encrypt(msg: str)`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_megakits/__init__.py#L25' target='_blank'>View on GitHub</a></summary>

```python
async def morse_encrypt(msg: str):
    return str(await mk_morse_code.morse_encrypt(msg))
```
</details>

---
### ***async func*** `morse_decrypt(msg: str)`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_megakits/__init__.py#L30' target='_blank'>View on GitHub</a></summary>

```python
async def morse_decrypt(msg: str):
    return str(await mk_morse_code.morse_decrypt(msg))
```
</details>

---
### ***async func*** `nya_encode(msg: str)`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_megakits/__init__.py#L35' target='_blank'>View on GitHub</a></summary>

```python
async def nya_encode(msg: str):
    return str(await mk_nya_code.nya_encode(msg))
```
</details>

---
### ***async func*** `nya_decode(msg: str)`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_megakits/__init__.py#L40' target='_blank'>View on GitHub</a></summary>

```python
async def nya_decode(msg: str):
    return str(await mk_nya_code.nya_decode(msg))
```
</details>

