"""此模块用于获取function call中函数定义信息以及注册函数
"""

import inspect

import litedoc
from nonebot import logger

from nonebot_plugin_marshoai.plugin.utils import is_coroutine_callable

from .models import FunctionCall, FunctionCallArgument
from .typing import (
    ASYNC_FUNCTION_CALL_FUNC,
    FUNCTION_CALL_FUNC,
    SYNC_FUNCTION_CALL_FUNC,
)

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
    description = func.__doc__
    # TODO: 获取函数参数信息
    parameters = {}  # type: ignore
    # 使用inspect解析函数的传参及类型
    sig = inspect.signature(func)
    for name, param in sig.parameters.items():
        logger.debug(name, param)
