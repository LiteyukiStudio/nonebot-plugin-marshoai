# 主交互
from typing import List

from nonebot.log import logger
from pc_info import SKILL_LIST, TYPE_LIST
from pc_token import dict_to_token, token_to_dict

from . import pc_info

# 私用列表
DEFAULT_DICT = {
    "name": "Default0",
    "age": 0,
    "type": 0,
    "health": 0,
    "saturation": 0,
    "energy": 0,
    "skill": [False, False, False, False, False, False, False, False],
    "date": 0,
}
DEFAULT_TOKEN = "6IyszC6tjoYAAAAAAAAC"


# 创建对象
def cat_new(type: str = "猫1") -> str:
    data = DEFAULT_DICT

    if type not in TYPE_LIST:
        return f'未知的"{type}"种类, 请重新选择, 可选种类 : {pc_info.print_type_list()}'

    data["type"] = TYPE_LIST.index(type)
    token = dict_to_token(data)
    return f'猫猫已创建, 种类为 : "{type}"; \ntoken : "{token}", 请妥善保存token, 这是猫猫的唯一标识符! \n新的猫猫还没有起名字, 请对猫猫进行初始化, 起一个长度小于等于8位的名字(仅限大小写字母+数字+特殊符号), 并选取一个技能. \n技能列表 : {pc_info.print_skill_list()}'


# 初始化对象
def cat_init(token: str, name: str, skill: str) -> str:
    data = token_to_dict(token)
    if data["name"] != "Default0":
        logger.info("初始化失败!")
        return "该猫猫已进行交互, 无法进行初始化!"

    if skill not in SKILL_LIST:
        return (
            f'未知的"{skill}"技能, 请重新选择, 技能列表 : {pc_info.print_skill_list()}'
        )

    data["name"] = name
    data["skill"][SKILL_LIST.index(skill)] = True
    token = dict_to_token(data)
    return f'初始化完成, 名字 : "{data["name"]}", 种类 : "{data["type"]}", 技能 : "{skill}" \ntoken : "{token}", 请妥善保存token, 这是猫猫的唯一标识符!'
