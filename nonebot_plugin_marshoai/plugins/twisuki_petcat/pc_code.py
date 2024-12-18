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
from datetime import datetime
from typing import List

# 公用列表
TYPE_LIST = ["猫1", "猫2", "猫3", "猫4", "猫5", "猫6", "猫7", "猫8"]
SKILL_LIST = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"]


# 二进制 - 十进制转换
async def bin_to_dec(bin_data: List[bool]) -> int:
    result = 0
    for index, bit in enumerate(bin_data):
        if bit:
            result ^= 1 << index
    return result


# 十进制 - 二进制转换
async def dec_to_bin(num: int) -> List[bool]:
    if num == 0:
        return [False]

    result = []
    while num > 0:
        result.append(bool(num % 2))
        num //= 2

    return result[::-1]


# 20位Base64字符串转换为120位Bit数据
async def b64_to_bit(str_data: str) -> list[bool]:
    str_data = str_data.replace("=", "")
    byte_data = base64.b64decode(str_data.encode())
    bool_array = []
    for byte in byte_data:
        for i in range(8):
            bool_array.append(bool(byte & (1 << i)))

    return bool_array


# 120位Bit数据转换为20位Base64字符
async def bit_to_b64(bit_data: List[bool]) -> str:
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


# 112位Bit数据解密
async def bit_to_dict(bit_data: List[bool]) -> dict:
    one_count = 0
    for i in range(112):
        if bit_data[i]:
            one_count += 1
    if one_count % 2 != 0:
        raise

    name_length_bit = bit_data[0:3]
    name_bit = bit_data[3:67]
    age_bit = bit_data[67:71]
    ctype_bit = bit_data[71:74]
    health_bit = bit_data[74:81]
    satiety_bit = bit_data[81:88]
    energy_bit = bit_data[88:95]
    skill_bit = bit_data[95:103]
    time_y_bit = bit_data[103:104]
    time_r_bit = bit_data[104:106]
    time_u_bit = bit_data[106:111]

    # 名字
    name_length = await bin_to_dec(name_length_bit)
    name_byte = bytearray()
    for i in range(0, 8 * name_length, 8):
        byte_value = 0
        for j in range(8):
            if name_bit[i + j]:
                byte_value |= 1 << j
        name_byte.append(byte_value)
    name = name_byte.decode("ASCII")

    # 通用
    age = await bin_to_dec(age_bit)
    ctype = await bin_to_dec(ctype_bit)
    health = await bin_to_dec(health_bit)
    satiety = await bin_to_dec(satiety_bit)
    energy = await bin_to_dec(energy_bit)

    # 技能
    skill = []
    for i in range(0, 8):
        if skill_bit[i]:
            skill.append(SKILL_LIST[i])

    # 时间
    now = datetime.now()
    year = now.year
    time_y = year
    # 奇偶年不同, 证明超一年
    if (year % 2 != 0) != time_y_bit:
        time_y -= 1

    # 季度 - u(2d) - 月/日
    reason = await bin_to_dec(time_r_bit)
    ult = await bin_to_dec(time_u_bit)
    delta_day = 2 * ult

    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    reason_to_months = {1: (1, 4), 2: (4, 7), 3: (7, 10), 4: (10, 13)}

    start_month, end_month = reason_to_months[reason]
    cumulative_days = 0
    current_month = start_month

    while cumulative_days + month_days[current_month - 1] <= delta_day:
        cumulative_days += month_days[current_month - 1]
        current_month += 1

    current_month -= 1
    day = delta_day - (cumulative_days - month_days[current_month - 1])

    data = {
        "name": name,
        "age": age,
        "type": TYPE_LIST[ctype],
        "health": health,
        "satiety": satiety,
        "energy": energy,
        "skill": skill,
        "date": [time_y, current_month, day],
    }

    return data


# 112位Bit数据编码
async def dict_to_bit(data: dict) -> List[bool]:
    bit_data = [False * 112]

    # 名字
    name = data["name"]
    name_length = len(name)
    name_length_bit = await dec_to_bin(name_length)
    name_byte = name.encode("ASCII")
    name_bit = []
    for byte in name_byte:
        for i in range(8):
            name_bit.append(bool(byte & (1 << i)))

    # 通用
    age = data["age"]
    ctype = [i for i in range(0, 8) if TYPE_LIST[i] == data["type"]][0]
    health = data["health"]
    satiety = data["satiety"]
    energy = data["energy"]

    # 技能
    skill: List[bool] = []
    for i in range(0, 8):
        skill[i] = bool(SKILL_LIST[i] in data["skill"])

    # 时间
    now = datetime.now()
    year = now.year
    time_y = year % 2

    # 月/日 - 季度 - u(2d)
    month = now.month
    day = now.day
    reason_start_months = [1, 4, 7, 10]
    reason_index = (month - 1) // 3
    reason_start_month = reason_start_months[reason_index]
    reason_start_date = datetime(year, reason_start_month, 1)
    days_since_reason_start = (now - reason_start_date).days + 1
    ult = days_since_reason_start // 2

    time_r = await dec_to_bin(reason_index)
    time_u = await dec_to_bin(ult)

    bit_data[0:3] = [*name_length_bit]
    bit_data[3:67] = [*name_bit]
    bit_data[67:71] = [*await dec_to_bin(age)]
    bit_data[71:74] = [*await dec_to_bin(ctype)]
    bit_data[74:81] = [*await dec_to_bin(health)]
    bit_data[81:88] = [*await dec_to_bin(satiety)]
    bit_data[88:95] = [*await dec_to_bin(energy)]
    bit_data[95:103] = [*skill]
    bit_data[103:104] = [bool(time_y)]
    bit_data[104:106] = [*time_r]
    bit_data[106:111] = [*time_u]

    one_count = 0
    for i in range(111):
        if bit_data[i]:
            one_count += 1
    bit_data[111:112] = [not (one_count % 2)]

    return [bool(*bit_data)]


# 总编码
async def pc_encode(data: dict) -> str:
    # 对象编码
    bit_112 = await dict_to_bit(data)
    # 汉明码编码
    if len(bit_112) != 112:
        raise
    bit_120 = await hamming_encode(bit_112)
    # 转换为20B644字符串
    if len(bit_120) != 120:
        raise
    sp = await bit_to_b64(bit_112)
    return sp


# 总解码
async def pc_decode(sp: str) -> dict:
    # 转换为120位Bit数据
    if len(sp) != 20:
        raise
    bit_120 = await b64_to_bit(sp)
    # 汉明码解码
    if len(bit_120) != 120:
        raise
    bit_112 = await hamming_decode(bit_120)
    # 对象解码
    if len(bit_112) != 112:
        raise
    data = await bit_to_dict(bit_112)
    return data
