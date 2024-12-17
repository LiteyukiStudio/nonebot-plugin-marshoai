from types import ModuleType
from typing import Any

from pydantic import BaseModel, Field

from .typing import ASYNC_FUNCTION_CALL_FUNC, FUNCTION_CALL_FUNC


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
    """点分或/割模块路径 例如a.b.c"""
    module_path: str | None
    """实际路径，单文件为.py的路径，包为__init__.py路径"""
    metadata: PluginMetadata | None = None
    """元"""

    class Config:
        arbitrary_types_allowed = True

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: Any) -> bool:
        return self.name == other.name

    def __str__(self) -> str:
        return f"Plugin({self.name}({self.module_path}))"
