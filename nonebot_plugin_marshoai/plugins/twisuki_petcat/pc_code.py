# 由于无法直接存储数据, 使用一个字符串记录全部信息
# 这里作为引用进行编码/解码, 以及公用数据

"""猫对象属性存储编码
    名字: 3位长度 + 8位ASCII字符 - 67b
    年龄: 0 ~ 15 - 4b
    种类: 8种 - 3b
    生命值: 0 ~ 127 - 7b
    饱食度: 0 ~ 127 - 7b
    活力值: 0 ~ 127 - 7b
    技能: 8种任选 - 8b
    时间: 奇/偶年 + 季度 + 32单位(2天) - 8b
    偶校验: 1b

    总计112b有效数据, 补充7位汉明码 + 高位补0
    总计120b数据, 15字节, 每3字节(utf-8一个字符)转换为4个Base64字符
    总计20个Base64字符的字符串
"""

import base64
from typing import List


# 20位Base64字符串转换为120位Bit数据
async def b64_to_bit(str_data: str) -> list[bool]:
    str_data = str_data.replace("=", "")
    if len(str_data) != 20:
        raise

    byte_data = base64.b64decode(str_data.encode())
    bool_array = []
    for byte in byte_data:
        for i in range(8):
            bool_array.append(bool(byte & (1 << i)))

    return bool_array


# 120为Bit数据转换为20位Base64字符
async def bit_to_b64(bit_data: List[bool]) -> str:
    if len(bit_data) != 120:
        raise

    byte_date = bytearray()
    for i in range(0, len(bit_data), 8):
        byte_value = 0
        for j in range(8):
            if bit_data[i + j]:
                byte_value |= 1 << j
        byte_date.append(byte_value)

    return base64.b64encode(byte_date).decode()


# import asyncio
# # print(asyncio.run(b64_to_bit("1234567890asfdHyUNcr")))
# print(asyncio.run(bit_to_b64([True, True, True, False, True, False, True, True, True, False, True, True, False, True, True, False, False, False, False, True, True, True, True, True, True, True, True, False, False, True, True, True, False, True, True, True, False, True, False, True, False, False, True, True, True, True, True, True, True, True, True, False, True, True, True, True, False, True, True, False, False, False, True, False, False, False, True, True, False, True, False, True, True, False, True, True, True, True, True, False, True, False, False, False, True, False, True, True, False, True, False, False, True, True, True, True, False, False, False, False, True, False, True, False, True, True, True, False, True, False, True, True, True, True, False, True, False, True, False, False]
# )))
