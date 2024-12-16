from nonebot_plugin_marshoai.plugin import (
    Integer,
    Parameter,
    PluginMetadata,
    String,
    on_function_call,
)

from . import mw_introduce, mw_search

__marsho_meta__ = PluginMetadata(
    name="萌娘百科调用插件",
    author="Twisuki",
    description="用于扒取萌娘百科上的信息, 补充MarshoAI在ACG方面知识的不足",
)


@on_function_call(description="在萌娘百科上搜索/查找某对象").params(
    msg=String(description="搜索对象"),
    num=Integer(description="搜索条数(默认3, 可留空)"),
)
async def search(msg: str, num: int = 3) -> str:
    """萌百搜索"""
    return await mw_search.search(msg, num)


@on_function_call(description="在萌娘百科上介绍/展示某对象").params(
    msg=String(description="介绍对象"),
)
async def introduce(msg: str) -> str:
    """萌百介绍"""
    return await mw_introduce.introduce(msg)
