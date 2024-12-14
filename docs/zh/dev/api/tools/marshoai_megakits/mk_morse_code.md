---
title: mk_morse_code
---
# **模块** `nonebot_plugin_marshoai.tools.marshoai_megakits.mk_morse_code`

---
### ***async func*** `morse_encrypt(msg: str)`


<details>
<summary> <b>源代码</b> 或 <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_megakits/mk_morse_code.py#L62' target='_blank'>在GitHub上查看</a></summary>

```python
async def morse_encrypt(msg: str):
    result = ''
    msg = msg.upper()
    for char in msg:
        if char in MorseEncode:
            result += MorseEncode[char]
        else:
            result += '..--..'
        result += ' '
    return result
```
</details>

---
### ***async func*** `morse_decrypt(msg: str)`


<details>
<summary> <b>源代码</b> 或 <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_megakits/mk_morse_code.py#L76' target='_blank'>在GitHub上查看</a></summary>

```python
async def morse_decrypt(msg: str):
    result = ''
    msg_arr = msg.split()
    for char in msg_arr:
        if char in MorseDecode:
            result += MorseDecode[char]
        else:
            result += '?'
    return result
```
</details>

