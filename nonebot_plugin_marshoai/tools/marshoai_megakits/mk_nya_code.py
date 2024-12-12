import base64
import random

# NyaCode
NyaCodeCharset = ["喵", "呜", "?", "~"]
NyaCodeSpecialCharset = ["唔", "!", "...", ".."]
NyaCodeEncode = {}
for i in range(64):
    triplet = "".join(NyaCodeCharset[(i // (4**j)) % 4] for j in range(3))
    NyaCodeEncode[
        chr(
            65 + i
            if i < 26
            else (
                97 + (i - 26)
                if i < 52
                else 48 + (i - 52) if i < 62 else (43 if i == 62 else 47)
            )
        )
    ] = triplet
NyaCodeDecode = {value: key for key, value in NyaCodeEncode.items()}


# NyaCode Encrypt
async def nya_encode(msg: str):
    msg_b64str = base64.b64encode(msg.encode()).decode().replace("=", "")
    msg_nyastr = "".join(NyaCodeEncode[base64_char] for base64_char in msg_b64str)
    result = ""
    for char in msg_nyastr:
        if char == "呜" and random.random() < 0.5:
            result += "!"

        if random.random() < 0.25:
            result += random.choice(NyaCodeSpecialCharset) + char
        else:
            result += char
    return result


# NyaCode Decrypt
async def nya_decode(msg: str):
    msg = msg.replace("唔", "").replace("!", "").replace(".", "")
    msg_nyastr = []
    i = 0
    if len(msg) % 3 != 0:
        return "这句话不是正确的猫语"
    while i < len(msg):
        nyachar = msg[i : i + 3]
        try:
            if all(char in NyaCodeCharset for char in nyachar):
                msg_nyastr.append(nyachar)
            i += 3
        except Exception:
            return "这句话不是正确的猫语"
    msg_b64str = "".join(NyaCodeDecode[nya_char] for nya_char in msg_nyastr)
    msg_b64str += "=" * (4 - len(msg_b64str) % 4)
    try:
        result = base64.b64decode(msg_b64str.encode()).decode()
    except Exception:
        return "翻译失败"
    return result
