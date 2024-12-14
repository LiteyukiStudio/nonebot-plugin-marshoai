from types import ModuleType
from typing import Any

from pydantic import BaseModel

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
    """点分割模块路径 例如a.b.c"""
    metadata: PluginMetadata | None = None
    """元"""

    class Config:
        arbitrary_types_allowed = True

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: Any) -> bool:
        return self.name == other.name


class FunctionCallArgument(BaseModel):
    """
    插件函数参数对象

    Attributes:
    ----------
    name: str
        参数名称
    type: str
        参数类型 string integer等
    description: str
        参数描述
    """

    type_: str
    """参数类型描述 string integer等"""
    description: str
    """参数描述"""
    default: Any = None
    """默认值"""

    def data(self) -> dict[str, Any]:
        return {"type": self.type_, "description": self.description}


class FunctionCall(BaseModel):
    """
    插件函数对象

    Attributes:
    ----------
    name: str
        函数名称
    func: "FUNCTION_CALL"
        函数对象
    """

    name: str
    """函数名称 module.func"""
    description: str
    """函数描述 这个函数用于获取天气信息"""
    arguments: dict[str, FunctionCallArgument]
    """函数参数信息"""
    function: FUNCTION_CALL_FUNC
    """函数对象"""

    class Config:
        arbitrary_types_allowed = True

    def __hash__(self) -> int:
        return hash(self.name)

    def data(self) -> dict[str, Any]:
        """生成函数描述信息

        Returns:
            dict[str, Any]: 函数描述信息 字典
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {k: v.data() for k, v in self.arguments.items()},
                },
                "required": [k for k, v in self.arguments.items() if v.default is None],
            },
        }
