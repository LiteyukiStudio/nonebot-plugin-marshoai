# 主交互

from datetime import datetime

from nonebot_plugin_marshoai.plugin import String, on_function_call

from .pc_token import ERROR_DICT, dict_to_token, token_to_dict


@on_function_call(description="创建一个新的猫对象（养一只新猫）").params(
    name=String(description="猫的名字")
)
async def create_cat(name: str) -> str:
    cat_data = {
        "name": name,
        "age": ERROR_DICT["age"],
        "type": ERROR_DICT["type"],
        "health": ERROR_DICT["health"],
        "saturation": ERROR_DICT["saturation"],
        "energy": ERROR_DICT["energy"],
        "skill": ERROR_DICT["skill"],
        "date": (datetime(2025, 1, 1) - datetime.now()).days,
    }
    token = dict_to_token(cat_data)
    return f"猫对象创建成功，Token: {token}"


@on_function_call(description="查询猫对象信息").params(
    token=String(description="猫对象的Token（是一串类似base64的字符串）")
)
async def query_cat(token: str) -> str:
    cat_data = token_to_dict(token)
    return f"猫的名字: {cat_data['name']}, 年龄: {cat_data['age']}, 种类: {cat_data['type']}, 生命值: {cat_data['health']}, 饱食度: {cat_data['saturation']}, 活力值: {cat_data['energy']}, 技能: {cat_data['skill']}, 日期: {cat_data['date']}"
