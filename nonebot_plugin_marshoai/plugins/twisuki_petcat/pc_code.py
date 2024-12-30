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

# 公用列表
TYPE_LIST = ["猫1", "猫2", "猫3", "猫4", "猫5", "猫6", "猫7", "猫8"]
SKILL_LIST = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"]


# bool数组/int数据转换
def bool_to_int(bool_array: List[bool]) -> int:
    result = 0
    for index, bit in enumerate(bool_array[::-1]):
        if bit:
            result |= 1 << index
    return result


def int_to_bool(integer: int) -> List[bool]:
    bit_length = integer.bit_length()
    bool_array = [False] * bit_length
    for i in range(bit_length):
        if integer & (1 << i):
            bool_array[bit_length - 1 - i] = True
    return bool_array


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


def byte_to_bool(byte_data: bytes) -> List[bool]:
    bool_array = []
    for byte in byte_data:
        for bit in format(byte, "08b"):
            bool_array.append(bit == "1")
    return bool_array


# 数据解码
def token_to_dict(token: str) -> dict:
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
    code = base64.b64decode(token.encode())

    return {}


# t = "1234567890QWERTyuiop"
# print(len(t))
# b = base64.b64decode(t.encode())
# print(b)
# li = byte_to_bool(b)
# print(li)
# print(len(li))
# nb = bool_to_byte(li)
# print(nb)
