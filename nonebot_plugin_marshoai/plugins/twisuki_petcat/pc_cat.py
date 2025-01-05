# 主交互
import functools
from datetime import datetime
from typing import List

from nonebot.log import logger

from . import pc_info, pc_token
from .pc_info import SKILL_LIST, TYPE_LIST, value_output
from .pc_token import dict_to_token, token_to_dict

"""特判标准
1. 默认, 未初始化: name = Default0
2. 错误: name = ERROR!
3. 死亡: skill = [False] * 8
"""


# 私用列表
DEFAULT_DICT = {
    "name": "Default0",
    "age": 0,
    "type": 0,
    "health": 0,
    "saturation": 0,
    "energy": 0,
    "skill": [False] * 8,
    "date": 0,
}
DEFAULT_TOKEN = "6IyszC6tjoYAAAAAAAAC"


# 交互前数据更新
def cat_update(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args:
            token = args[0]

            data = token_to_dict(token)

            # 检查
            if data["name"] == "Default0":
                return "猫猫尚未初始化, 请初始化猫猫"

            if data["name"] == "ERROR!":
                return (
                    "token出错"
                    f'token应为Base64字符串, 当前token : "{token}"'
                    f"当前token长度应为20, 当前长度 : {len(token)}"
                )

            if data["skill"] == [False] * 8:
                return (
                    "很不幸, 猫猫已死亡"
                    f'名字 : {data["name"]}'
                    f'年龄 : {data["age"]}'
                )

            date = data["date"]
            now = (datetime(2025, 1, 1) - datetime.now()).days

            # 喂食状态更新
            if now - date > 5:
                data["saturation"] = max(data["saturation"] - 64, 0)
                data["health"] = max(data["health"] - 32, 0)
                data["energy"] = max(data["energy"] - 32, 0)
            elif now - date > 2:
                data["saturation"] = max(data["saturation"] - 16, 0)
                data["health"] = max(data["health"] - 8, 0)
                data["energy"] = max(data["energy"] - 16, 0)

            # 机能状态更新
            if data["saturation"] / 1.27 < 20:
                data["health"] = max(data["health"] - 8, 0)
            elif data["saturation"] / 1.27 > 80:
                data["health"] = min(data["health"] + 8, 127)

            # 生长检查
            if now % 7 == 0:
                # 死亡
                if data["health"] / 1.27 < 20:
                    data["health"] = 0

                    death = DEFAULT_DICT
                    death["name"] = data["name"]
                    data = death

                # 生长
                if data["health"] / 1.27 > 60 and data["saturation"] / 1.27 > 40:
                    data["age"] = min(data["age"] + 1, 15)

            token = dict_to_token(data)
            new_args = (token,) + args[1:]
            return func(*new_args, **kwargs)

    return wrapper


# 创建对象
def cat_new(type: str = "猫1") -> str:
    data = DEFAULT_DICT

    if type not in TYPE_LIST:
        return (
            f'未知的"{type}"种类, 请重新选择.'
            f"\n可选种类 : {pc_info.print_type_list()}"
        )

    data["type"] = TYPE_LIST.index(type)
    token = dict_to_token(data)
    return (
        f'猫猫已创建, 种类为 : "{type}"; \ntoken : "{token}",'
        f"\n请妥善保存token, 这是猫猫的唯一标识符!"
        f"\n新的猫猫还没有起名字, 请对猫猫进行初始化, 起一个长度小于等于8位的名字(仅限大小写字母+数字+特殊符号), 并选取一个技能."
        f"\n技能列表 : {pc_info.print_skill_list()}"
    )


# 初始化对象
def cat_init(token: str, name: str, skill: str) -> str:
    data = token_to_dict(token)
    if data["name"] != "Default0":
        logger.info("初始化失败!")
        return "该猫猫已进行交互, 无法进行初始化!"

    if skill not in SKILL_LIST:
        return (
            f'未知的"{skill}"技能, 请重新选择.'
            f"技能列表 : {pc_info.print_skill_list()}"
        )

    data["name"] = name
    data["skill"][SKILL_LIST.index(skill)] = True
    data["health"] = 127
    data["saturation"] = 127
    data["energy"] = 127
    token = dict_to_token(data)
    return (
        f'初始化完成, 名字 : "{data["name"]}", 种类 : "{data["type"]}", 技能 : "{skill}"'
        f'\n新token : "{token}"'
        f"\n请妥善保存token, 这是猫猫的唯一标识符!"
    )


# 查看信息
@cat_update
def cat_show(token: str) -> str:
    result = pc_info.print_info(token)
    data = token_to_dict(token)

    if data["health"] / 1.27 < 20:
        return result + "\n猫猫健康状况非常差! 甚至濒临死亡!! 请立即前往医院救治!!"

    if data["health"] / 1.27 < 60:
        result += "\n猫猫健康状况较差, 请投喂食物或陪猫猫玩耍"
    if data["saturation"] / 1.27 < 40:
        result += "\n猫猫很饿, 请投喂食物"
    if data["energy"] / 1.27 < 20:
        result += "\n猫猫很累, 请抱猫睡觉, 不要投喂食物或陪它玩耍"
    return result


# 陪猫猫玩耍
@cat_update
def cat_play(token: str) -> str:
    data = token_to_dict(token)
    if data["health"] / 1.27 < 20:
        return "猫猫健康状况非常差! 甚至濒临死亡!! 请立即前往医院救治!!"

    if data["saturation"] / 1.27 < 40:
        return "猫猫很饿, 拒接玩耍请求."

    if data["energy"] / 1.27 < 20:
        return "猫猫很累, 拒接玩耍请求"

    data["health"] = min(data["health"] + 16, 127)
    data["saturation"] = max(data["saturation"] - 16, 0)
    data["energy"] = max(data["energy"] - 8, 0)

    token = dict_to_token(data)
    return (
        f'你陪猫猫玩耍了一个小时, 猫猫的生命值上涨到了{value_output(data["health"])}'
        f'\n新token : "{token}"'
        "\n请妥善保存token, 这是猫猫的唯一标识符!"
    )


# 喂食
@cat_update
def cat_feed(token: str) -> str:
    data = token_to_dict(token)
    if data["health"] / 1.27 < 20:
        return "猫猫健康状况非常差! 甚至濒临死亡!! 请立即前往医院救治!!"

    if data["saturation"] / 1.27 > 80:
        return "猫猫并不饿, 不需要喂食"

    if data["energy"] / 1.27 < 40:
        return "猫猫很累, 请抱猫睡觉, 不要投喂食物或陪它玩耍"

    data["saturation"] = min(data["saturation"] + 32, 127)
    data["date"] = (datetime(2025, 1, 1) - datetime.now()).days

    token = dict_to_token(data)
    return (
        f'你投喂了2单位标准猫粮, 猫猫的饱食度提升到了{value_output(data["saturation"])}'
        f'\n新token : "{token}"'
        "\n请妥善保存token, 这是猫猫的唯一标识符!"
    )


# 睡觉
@cat_update
def cat_sleep(token: str) -> str:
    data = token_to_dict(token)
    if data["health"] / 1.27 < 20:
        return "猫猫健康状况非常差! 甚至濒临死亡!! 请立即前往医院救治!!"

    if data["saturation"] / 1.27 < 40:
        return "猫猫很饿, 请喂食."

    if data["energy"] / 1.27 > 80:
        return "猫猫很精神, 不需要睡觉"

    data["health"] = min(data["health"] + 8, 127)
    data["energy"] = min(data["energy"] + 16, 0)

    token = dict_to_token(data)
    return (
        f'你抱猫休息了一阵子, 猫猫的活力值提升到了{value_output(data["energy"])}'
        f'\n新token : "{token}"'
        "\n请妥善保存token, 这是猫猫的唯一标识符!"
    )


"""饼
    1. 商店系统
    2. 技能系统
    3. 提高复杂性和难度
"""
