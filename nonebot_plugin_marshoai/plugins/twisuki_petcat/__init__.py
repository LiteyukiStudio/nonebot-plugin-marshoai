from nonebot_plugin_marshoai.plugin import (
    Integer,
    Parameter,
    PluginMetadata,
    String,
    on_function_call,
)

from . import pc_cat, pc_info, pc_shop, pc_token

__marsho_meta__ = PluginMetadata(
    name="养猫插件",
    description="在Marsho这里赛博养猫",
    author="Twisuki",
)


# 交互
@on_function_call(description="传入猫猫种类, 新建一只猫猫").params(
    type=String(description='猫猫种类, 默认"猫1", 可留空')
)
async def cat_new(type: str) -> str:
    return pc_cat.cat_new(type)


@on_function_call(
    description="传入token(一串长20的b64字符串), 新名字, 选用技能, 进行猫猫的初始化"
).params(
    token=String(description="token(一串长20的b64字符串)"),
    name=String(description="新名字"),
    skill=String(description="技能"),
)
async def cat_init(token: str, name: str, skill: str) -> str:
    return pc_cat.cat_init(token, name, skill)


@on_function_call(description="传入token, 查看猫猫信息").params(
    token=String(description="token(一串长20的b64字符串)"),
)
async def cat_show(token: str) -> str:
    return pc_cat.cat_show(token)


# 帮助
@on_function_call(description="帮助文档/如何创建一只猫猫").params()
async def help_cat_new() -> str:
    return pc_info.help_cat_new()


@on_function_call(description="可选种类").params()
async def help_cat_type() -> str:
    return pc_info.print_type_list()


@on_function_call(description="可选技能").params()
async def help_cat_skill() -> str:
    return pc_info.print_skill_list()


# 商店
