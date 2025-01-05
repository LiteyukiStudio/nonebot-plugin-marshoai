# 由于无法直接存储数据, 使用一个字符串记录全部信息
# 这里作为引用进行编码/解码, 以及公用数据

"""猫对象属性存储编码Token
名字: 3位长度 + 8位ASCII字符 - 67b
年龄: 0 ~ 15 - 4b
种类: 8种 - 3b
生命值: 0 ~ 127 - 7b
饱食度: 0 ~ 127 - 7b
活力值: 0 ~ 127 - 7b
技能: 8种任选 - 8b
时间: 0 ~ 131017d > 2025-1-1 - 17b

总计120b有效数据
总计120b数据, 15字节, 每3字节(utf-8一个字符)转换为4个Base64字符
总计20个Base64字符的字符串
"""

"""定义变量
存储字符串: Token: str
对象数据: data: dict
名字: name: str
年龄: age: int
种类: type: int   # 代表TYPE_LIST中的序号
生命值: health: int    # 0 - 127, 显示时转换为100%
饱食度: saturation: int    # 0 - 127, 显示时转换为100%
活力值: energy: int    # 0 - 127, 显示时转换为100%
技能: skill: List[bool]   # 8元素bool数组
时间: date: int   # 到2025-1-1按日的时间戳
"""

import base64
from datetime import datetime
from typing import List

from nonebot.log import logger

# 私用列表
ERROR_DICT = {
    "name": "ERROR!",
    "age": 0,
    "type": 0,
    "health": 0,
    "saturation": 0,
    "energy": 0,
    "skill": [False, False, False, False, False, False, False, False],
    "date": 0,
}
ERROR_TOKEN = "yKpKSepEIAAAAAAAAAAA"


# bool数组/int数据转换
def bool_to_int(bool_array: List[bool]) -> int:
    result = 0
    for index, bit in enumerate(bool_array[::-1]):
        if bit:
            result |= 1 << index
    return result


def int_to_bool(integer: int, length: int = 0) -> List[bool]:
    bit_length = integer.bit_length()
    bool_array = [False] * bit_length
    for i in range(bit_length):
        if integer & (1 << i):
            bool_array[bit_length - 1 - i] = True
    if len(bool_array) >= length:
        return bool_array
    else:
        return [*([False] * (length - len(bool_array))), *bool_array]


# bool数组/byte数据转换
def bool_to_byte(bool_array: List[bool]) -> bytes:
    byte_data = bytearray()
    for i in range(0, len(bool_array), 8):
        byte = 0
        for j in range(8):
            if i + j < len(bool_array) and bool_array[i + j]:
                byte |= 1 << (7 - j)
        byte_data.append(byte)
    return bytes(byte_data)


def byte_to_bool(byte_data: bytes, length: int = 0) -> List[bool]:
    bool_array = []
    for byte in byte_data:
        for bit in format(byte, "08b"):
            bool_array.append(bit == "1")
    if len(bool_array) >= length:
        return bool_array
    else:
        return [*([False] * (length - len(bool_array))), *bool_array]


# 数据解码
def token_to_dict(token: str) -> dict:
    logger.info(f"开始解码...\n{token}")

    data = {
        "name": "Default0",
        "age": 0,
        "type": 0,
        "health": 0,
        "saturation": 0,
        "energy": 0,
        "skill": [False] * 8,
        "date": 0,
    }

    # 转换token
    try:
        token_byte = base64.b64decode(token.encode())
        code = byte_to_bool(token_byte)
    except ValueError:
        logger.error("token b64解码错误!")
        return ERROR_DICT

    # 拆分code
    name_length = bool_to_int(code[0:3]) + 1
    name_code = code[3:67]
    age = bool_to_int(code[67:71])
    type = bool_to_int(code[71:74])
    health = bool_to_int(code[74:81])
    saturation = bool_to_int(code[81:88])
    energy = bool_to_int(code[88:95])
    skill = code[95:103]
    date = bool_to_int(code[103:120])

    # 解析code
    name: str = ""
    try:
        for i in range(name_length):
            character_code = bool_to_byte(name_code[8 * i : 8 * i + 8])
            name += character_code.decode("ASCII")
    except UnicodeDecodeError:
        logger.error("token ASCII解析错误!")
        return ERROR_DICT

    data["name"] = name
    data["age"] = age
    data["type"] = type
    data["health"] = health
    data["saturation"] = saturation
    data["energy"] = energy
    data["skill"] = skill
    data["date"] = date

    logger.success(f"解码完成, 数据为\n{data}")
    return data


# 数据编码
def dict_to_token(data: dict) -> str:
    logger.info(f"开始编码...\n{data}")

    code = [False] * 120

    # 拆分data
    name_length = len(data["name"])
    if name_length > 8:
        logger.error("name过长")
        return ERROR_TOKEN

    name = data["name"]
    age = data["age"]
    type = data["type"]
    health = data["health"]
    saturation = data["saturation"]
    energy = data["energy"]
    skill = data["skill"]
    date = data["date"]

    # 填入code
    code[0:3] = int_to_bool(name_length - 1, 3)
    name_code = [False] * 64
    try:
        for i in range(name_length):
            character_code = byte_to_bool(name[i].encode("ASCII"), 8)
            name_code[8 * i : 8 * i + 8] = character_code
    except UnicodeEncodeError:
        # "name": "ERROR!"
        logger.error("name内含有非法字符!")
        return ERROR_TOKEN

    code[3:67] = name_code
    code[67:71] = int_to_bool(age, 4)
    code[71:74] = int_to_bool(type, 3)
    code[74:81] = int_to_bool(health, 7)
    code[81:88] = int_to_bool(saturation, 7)
    code[88:95] = int_to_bool(energy, 7)
    code[95:103] = skill
    code[103:120] = int_to_bool(date, 17)

    # 转换token
    token_byte = bool_to_byte(code)
    token = base64.b64encode(token_byte).decode()

    logger.success(f"编码完成, token为\n{token}")
    return token
