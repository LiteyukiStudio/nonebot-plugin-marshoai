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


# 120位Bit数据转换为20位Base64字符
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


# 112位Bit数据汉明码加密为120位
async def hamming_encode(bit_data: List[bool]) -> list[bool]:
    m = len(bit_data)
    r = 7
    n = m + r
    hamming_code = [False] * n

    # 将数据位插入 hamming_code，并留出冗余位的位置
    j = 0  # 数据位索引
    for i in range(1, n + 1):
        if (i & (i - 1)) == 0:
            hamming_code[i - 1] = False
        else:
            hamming_code[i - 1] = bool(bit_data[j])
            j += 1

    # 计算并插入冗余位
    for i in range(r):
        idx = 2**i
        value = False
        for j in range(1, n + 1):
            if j & idx:  # 如果 j 位置包含 idx
                if hamming_code[j - 1] is not False:  # 仅计算实际数据位
                    value ^= bool(hamming_code[j - 1])
        hamming_code[idx - 1] = value  # 插入计算得到的冗余位

    return hamming_code


# 120位汉明码Bit数据解码为112位
async def hamming_decode(bit_data: List[bool]) -> List[bool]:
    n = len(bit_data)
    r = 7

    # 检查冗余位并找到错误位置
    error_position = 0
    for i in range(r):
        idx = 2**i
        value = 0
        for j in range(1, n + 1):
            if j & idx:  # 如果 j 位置包含 idx
                value ^= bool(bit_data[j - 1])
        if value != 0:
            error_position += idx

    # 纠正位
    if error_position > 0:
        bit_data[error_position - 1] = not bit_data[error_position - 1]

    # 提取原始数据位
    original_data: List[bool] = []
    for i in range(1, n + 1):
        if (i & (i - 1)) != 0:
            original_data.append(bit_data[i - 1])

    return original_data


# 120位Bit数据解密
async def bit_to_dict(bit_data: List[bool]) -> dict:
    if len(bit_data) != 120:
        raise

    # name_length_bit = bit_data[0:3]
    # name_bit = bit_data[3:67]
    # age_bit = bit_data[67:71]
    # type_bit = bit_data[71:74]
    # height_bit = bit_data[74:81]
    # satiety_bit = bit_data[81:88]
    # energy_bit = bit_data[88:95]
    # skill_bit = bit_data[95:103]
    # time_bit = bit_data[103:111]

    return dict()
