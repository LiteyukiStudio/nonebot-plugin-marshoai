"""此模块用于获取function call中函数定义信息以及注册函数
"""

import inspect
from typing import Any, Callable, Coroutine, TypeAlias

import nonebot

from .utils import is_coroutine_callable

SYNC_FUNCTION_CALL: TypeAlias = Callable[..., str]
ASYNC_FUNCTION_CALL: TypeAlias = Callable[..., Coroutine[str, Any, str]]
FUNCTION_CALL: TypeAlias = SYNC_FUNCTION_CALL | ASYNC_FUNCTION_CALL

_loaded_functions: dict[str, FUNCTION_CALL] = {}


def async_wrapper(func: SYNC_FUNCTION_CALL) -> ASYNC_FUNCTION_CALL:
    """将同步函数包装为异步函数，但是不会真正异步执行，仅用于统一调用及函数签名

    Args:
        func: 同步函数

    Returns:
        ASYNC_FUNCTION_CALL: 异步函数
    """

    async def wrapper(*args, **kwargs) -> str:
        return func(*args, **kwargs)

    return wrapper


def function_call(*funcs: FUNCTION_CALL):
    """返回一个装饰器，装饰一个函数, 使其注册为一个可被AI调用的function call函数

    Args:
        func: 函数对象，要有完整的 Google Style Docstring

    Returns:
        str: 函数定义信息
    """
    for func in funcs:
        if module := inspect.getmodule(func):
            module_name = module.__name__ + "."
        else:
            module_name = ""
        name = func.__name__
        if not is_coroutine_callable(func):
            func = async_wrapper(func)  # type: ignore

        _loaded_functions[name] = func
        nonebot.logger.opt(colors=True).info(
            f"加载 function call: <c>{module_name}{name}</c>"
        )
