"""此模块用于获取function call中函数定义信息以及注册函数
"""

import inspect
from typing import Any, Callable, Coroutine, TypeAlias

from nonebot import logger

from .models import FunctionCall, FunctionCallArgument
from .typing import (
    ASYNC_FUNCTION_CALL_FUNC,
    FUNCTION_CALL_FUNC,
    SYNC_FUNCTION_CALL_FUNC,
)
from .utils import is_coroutine_callable

_loaded_functions: dict[str, FUNCTION_CALL_FUNC] = {}


def async_wrapper(func: SYNC_FUNCTION_CALL_FUNC) -> ASYNC_FUNCTION_CALL_FUNC:
    """将同步函数包装为异步函数，但是不会真正异步执行，仅用于统一调用及函数签名

    Args:
        func: 同步函数

    Returns:
        ASYNC_FUNCTION_CALL: 异步函数
    """

    async def wrapper(*args, **kwargs) -> str:
        return func(*args, **kwargs)

    return wrapper


def function_call(*funcs: FUNCTION_CALL_FUNC) -> None:
    """返回一个装饰器，装饰一个函数, 使其注册为一个可被AI调用的function call函数

    Args:
        func: 函数对象，要有完整的 Google Style Docstring

    Returns:
        str: 函数定义信息
    """
    for func in funcs:
        function_call = get_function_info(func)
        # TODO: 注册函数


def get_function_info(func: FUNCTION_CALL_FUNC):
    """获取函数信息

    Args:
        func: 函数对象

    Returns:
        FunctionCall: 函数信息对象模型
    """
    name = func.__name__
    description = func.__doc__
    logger.info(f"注册函数: {name} {description}")
    # TODO: 获取函数参数信息
