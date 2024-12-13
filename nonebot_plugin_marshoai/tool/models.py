from types import ModuleType
from typing import Any
from pydantic import BaseModel


class Plugin(BaseModel):
    """
    存储插件信息
    
    Attributes:
    ----------
    name: str
        包名称 例如marsho_test
    module: ModuleType
        插件模块对象
    module_name: str
        点分割模块路径 例如a.b.c
    metadata: "PluginMeta" | None
        元
    """
    name: str
    """包名称 例如marsho_test"""
    module: ModuleType
    """插件模块对象"""
    module_name: str
    """点分割模块路径 例如a.b.c"""
    metadata: "PluginMetadata" | None = None
    """元"""

class PluginMetadata(BaseModel):
    """
    Marsho 插件 对象元数据
    Attributes:
    ----------

    name: str
        友好名称: 例如Marsho Test
    description: str
        插件描述
    usage: str
        插件使用方法
    type: str
        插件类型
    author: str
        插件作者
    homepage: str
        插件主页
    extra: dict[str, Any]
        额外信息，自定义键值对
    """
    name: str
    description: str = ""
    usage: str = ""
    author: str = ""
    homepage: str = ""
    extra: dict[str, Any] = {}