from typing import Generic

from ..typing import FUNCTION_CALL_FUNC
from .params import P
from .register import F


class Caller(Generic[P]):
    def __init__(self, name: str | None = None, description: str | None = None):
        self._name = name
        self._description = description
        self._parameters: dict[str, P] = {}
        self.func: FUNCTION_CALL_FUNC | None = None

    def params(self, **kwargs: P) -> "Caller":
        """设置多个函数参数
        Args:
            **kwargs: 参数字典
        Returns:
            Caller: Caller对象
        """
        self._parameters.update(kwargs)
        return self

    def param(self, name: str, param: P) -> "Caller":
        """设置一个函数参数

        Args:
            name (str): 参数名
            param (P): 参数对象

        Returns:
            Caller: Caller对象
        """
        self._parameters[name] = param
        return self

    def name(self, name: str) -> "Caller":
        """设置函数名称

        Args:
            name (str): 函数名称

        Returns:
            Caller: Caller对象
        """
        self._name = name
        return self

    def description(self, description: str) -> "Caller":
        """设置函数描述

        Args:
            description (str): 函数描述

        Returns:
            Caller: Caller对象
        """
        self._description = description
        return self

    def __call__(self, func: F) -> F:
        self.func = func
        return func


def on_function_call(name: str | None = None, description: str | None = None) -> Caller:
    """返回一个Caller类，可用于装饰一个函数，使其注册为一个可被AI调用的function call函数

    Args:
        description: 函数描述，若为None则从函数的docstring中获取

    Returns:
        Caller: Caller对象
    """
    return Caller(name=name, description=description)
