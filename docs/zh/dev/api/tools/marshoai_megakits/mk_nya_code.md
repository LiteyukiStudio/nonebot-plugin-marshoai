---
title: mk_nya_code
---
# **模块** `nonebot_plugin_marshoai.tools.marshoai_megakits.mk_nya_code`

---
### ***async func*** `nya_encode(msg: str)`


<details>
<summary> <b>源代码</b> 或 <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_megakits/mk_nya_code.py#L25' target='_blank'>在GitHub上查看</a></summary>

```python
async def nya_encode(msg: str):
    msg_b64str = base64.b64encode(msg.encode()).decode().replace('=', '')
    msg_nyastr = ''.join((NyaCodeEncode[base64_char] for base64_char in msg_b64str))
    result = ''
    for char in msg_nyastr:
        if char == '呜' and random.random() < 0.5:
            result += '!'
        if random.random() < 0.25:
            result += random.choice(NyaCodeSpecialCharset) + char
        else:
            result += char
    return result
```
</details>

---
### ***async func*** `nya_decode(msg: str)`


<details>
<summary> <b>源代码</b> 或 <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_megakits/mk_nya_code.py#L41' target='_blank'>在GitHub上查看</a></summary>

```python
async def nya_decode(msg: str):
    msg = msg.replace('唔', '').replace('!', '').replace('.', '')
    msg_nyastr = []
    i = 0
    if len(msg) % 3 != 0:
        return '这句话不是正确的猫语'
    while i < len(msg):
        nyachar = msg[i:i + 3]
        try:
            if all((char in NyaCodeCharset for char in nyachar)):
                msg_nyastr.append(nyachar)
            i += 3
        except Exception:
            return '这句话不是正确的猫语'
    msg_b64str = ''.join((NyaCodeDecode[nya_char] for nya_char in msg_nyastr))
    msg_b64str += '=' * (4 - len(msg_b64str) % 4)
    try:
        result = base64.b64decode(msg_b64str.encode()).decode()
    except Exception:
        return '翻译失败'
    return result
```
</details>

