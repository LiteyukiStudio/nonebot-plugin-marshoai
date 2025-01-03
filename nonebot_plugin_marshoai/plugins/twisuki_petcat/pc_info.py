# 插件使用复杂, 这里用作输出提示信息.
# 如: 帮助, 每次操作后对猫猫状态的描述\打印特殊列表
# 公用列表数据转到这里存储


# 公用列表
TYPE_LIST = ["猫1", "猫2", "猫3", "猫4", "猫5", "猫6", "猫7", "猫8"]
SKILL_LIST = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"]

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


# 提示词打印
# 打印种类列表
def print_type_list():
    result = ""
    for type in TYPE_LIST:
        result += f'"{type}", '
    result = result[:-2]
    return f"({result})"


# 打印技能列表
def print_skill_list():
    result = ""
    for skill in SKILL_LIST:
        result += f'"{skill}", '
    result = result[:-2]
    return f"({result})"
