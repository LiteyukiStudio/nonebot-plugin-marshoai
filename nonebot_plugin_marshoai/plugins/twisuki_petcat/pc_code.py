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


import base64
from datetime import datetime
from typing import List

# 公用列表
TYPE_LIST = ["猫1", "猫2", "猫3", "猫4", "猫5", "猫6", "猫7", "猫8"]
SKILL_LIST = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"]


# bool数组/int数据转换
async def bool_to_int(bool_array: List[bool]) -> int:
    result = 0
    for index, bit in enumerate(bool_array[::-1]):
        if bit:
            result |= 1 << index
    return result


async def int_to_bool(integer: int) -> List[bool]:
    bit_length = integer.bit_length()
    bool_array = [False] * bit_length
    for i in range(bit_length):
        if integer & (1 << i):
            bool_array[bit_length - 1 - i] = True
    return bool_array


# 数据解码
async def token_to_dict(token: str) -> dict:
    return {}


import asyncio

print(asyncio.run(bool_to_int([True, True, False, True, False, True, False])))
print(asyncio.run(int_to_bool(106)))
