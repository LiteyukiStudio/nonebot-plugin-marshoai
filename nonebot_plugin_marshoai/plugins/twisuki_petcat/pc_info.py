# 插件使用复杂, 这里用作输出提示信息.
# 如: 帮助, 每次操作后对猫猫状态的描述\打印特殊列表
# 公用列表数据转到这里存储


from nonebot.log import logger

from .pc_token import dict_to_token, token_to_dict

# 公用列表
TYPE_LIST = ["猫1", "猫2", "猫3", "猫4", "猫5", "猫6", "猫7", "猫8"]
SKILL_LIST = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"]


# 提示词打印
# 打印种类列表
def print_type_list() -> str:
    result = ""
    for type in TYPE_LIST:
        result += f'"{type}", '
    result = result[:-2]
    return f"({result})"


# 打印技能列表
def print_skill_list() -> str:
    result = ""
    for skill in SKILL_LIST:
        result += f'"{skill}", '
    result = result[:-2]
    return f"({result})"


# 127位值 - 100%快速转换
def value_output(num: int) -> str:
    value = int(num / 1.27)
    return str(value)


# 打印状态
def print_info(token: str) -> str:
    data = token_to_dict(token)
    return (
        "状态信息: "
        f'\n\t名字 : {data["name"]}'
        f'\n\t种类 : {TYPE_LIST[data["type"]]}'
        f'\n\t生命值 : {value_output(data["health"])}'
        f'\n\t饱食度 : {value_output(data["saturation"])}'
        f"\n\t活力值 : {value_output(data['energy'])}"
        f"\n\t技能 : {print_skill(token)}"
        f"\n新token : {token}"
        f"\ntoken已更新, 请妥善保存token, 这是猫猫的唯一标识符!"
    )


# 打印已有技能
def print_skill(token: str) -> str:
    result = ""
    data = token_to_dict(token)
    for index in range(0, len(SKILL_LIST) - 1):
        if data["skill"][index]:
            result += f"{SKILL_LIST[index]}, "
    logger.info(data["skill"])
    return result[:-2]


# 帮助
# 创建猫猫
def help_cat_new() -> str:
    return (
        "新建一只猫猫, 首先选择猫猫的种类, 获取初始化token;"
        "然后用这个token, 选择名字和一个技能进行初始化;"
        "初始化结束才表示猫猫正式创建成功."
        "\ntoken为猫的唯一标识符, 每次交互都需要传入token"
        f"\n种类可选 : {print_type_list()}"
        f"\n技能可选 : {print_skill_list()}"
    )
