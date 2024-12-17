# NyaCode

import base64
import random

NyaCodeCharset = ["喵", "呜", "?", "~"]
NyaCodeSpecialCharset = ["唔", "!", "...", ".."]
NyaCodeEncode = {}

for i in range(64):
    triplet = ""
    for j in range(3):
        index = (i // (4**j)) % 4
        triplet += NyaCodeCharset[index]

    if i < 26:
        char = chr(65 + i)  # 大写字母 A-Z
    elif i < 52:
        char = chr(97 + (i - 26))  # 小写字母 a-z
    elif i < 62:
        char = chr(48 + (i - 52))  # 数字 0-9
    elif i == 62:
        char = chr(43)  # 特殊字符 +
    else:
        char = chr(47)  # 特殊字符 /
    NyaCodeEncode[char] = triplet
NyaCodeDecode = {value: key for key, value in NyaCodeEncode.items()}


async def nya_encrypt(msg: str):
    result = ""
    b64str = base64.b64encode(msg.encode()).decode().replace("=", "")

    nyastr = ""
    for b64char in b64str:
        nyastr += NyaCodeEncode[b64char]

    for char in nyastr:
        if char == "呜" and random.random() < 0.5:
            result += "!"
        if random.random() < 0.25:
            result += random.choice(NyaCodeSpecialCharset) + char
        else:
            result += char
    return result


async def nya_decrypt(msg: str):
    msg = msg.replace("唔", "").replace("!", "").replace(".", "")
    nyastr = []

    i = 0
    if len(msg) % 3 != 0:
        return "这句话不是正确的猫语"

    while i < len(msg):
        nyachar = msg[i : i + 3]
        try:
            if all(char in NyaCodeCharset for char in nyachar):
                nyastr.append(nyachar)
            i += 3
        except Exception:
            return "这句话不是正确的猫语"

    b64str = ""
    for nyachar in nyastr:
        b64str += NyaCodeDecode[nyachar]
    b64str += "=" * (4 - len(b64str) % 4)

    try:
        result = base64.b64decode(b64str.encode()).decode()
    except Exception:
        return "翻译失败"
    return result
