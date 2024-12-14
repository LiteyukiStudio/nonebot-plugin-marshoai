from enum import Enum
from typing import Any, TypeVar

from pydantic import BaseModel, Field

from ..typing import FUNCTION_CALL_FUNC

P = TypeVar("P", bound="Parameter")
"""参数类型泛型"""


class ParamTypes:
    STRING = "string"
    INTEGER = "integer"
    ARRAY = "array"
    OBJECT = "object"
    BOOLEAN = "boolean"
    NUMBER = "number"


class Parameter(BaseModel):
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
    properties: dict[str, Any] = {}
    """参数定义属性，例如最大值最小值等"""
    required: bool = False
    """是否必须"""

    def data(self) -> dict[str, Any]:
        return {
            "type": self.type_,
            "description": self.description,
            **{k: v for k, v in self.properties.items() if v is not None},
        }


class String(Parameter):
    type_: str = ParamTypes.STRING
    properties: dict[str, Any] = Field(default_factory=dict)
    enum: list[str] | None = None


class Integer(Parameter):
    type_: str = ParamTypes.INTEGER
    properties: dict[str, Any] = Field(
        default_factory=lambda: {"minimum": 0, "maximum": 100}
    )

    minimum: int | None = None
    maximum: int | None = None


class Array(Parameter):
    type_: str = ParamTypes.ARRAY
    properties: dict[str, Any] = Field(
        default_factory=lambda: {"items": {"type": "string"}}
    )
    items: str = Field("string", description="数组元素类型")


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
    arguments: dict[str, Parameter]
    """函数参数信息"""
    function: FUNCTION_CALL_FUNC
    """函数对象"""
    kwargs: dict[str, Any] = {}
    """扩展参数"""

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
                **self.kwargs,
            },
        }
