"""此模块用于获取function call中函数定义信息以及注册函数
"""

from typing import TypeVar

from nonebot import logger

from ..docstring.parser import parse
from ..typing import (
    ASYNC_FUNCTION_CALL_FUNC,
    FUNCTION_CALL_FUNC,
    SYNC_FUNCTION_CALL_FUNC,
)
from .params import *

F = TypeVar("F", bound=FUNCTION_CALL_FUNC)

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


def function_call(func: F) -> F:
    """返回一个装饰器，装饰一个函数, 使其注册为一个可被AI调用的function call函数

    Args:
        func: 函数对象，要有完整的 Google Style Docstring

    Returns:
        str: 函数定义信息
    """
    # TODO
    # pre check docstring
    if not func.__doc__:
        logger.error(f"函数 {func.__name__} 没有文档字串，不被加载")
        return func
    else:
        # 解析函数文档字串
        result = parse(docstring=func.__doc__)
        logger.debug(result.reduction())
    return func


def caller(
    description: str | None = None,
    parameters: dict[str, P] | None = None,
):
    """返回一个装饰器，装饰一个函数, 使其注册为一个可被AI调用的function call函数

    Args:
        description: 函数描述
        parameters: 函数参数

    Returns:
        str: 函数定义信息
    """

    def decorator(func: FUNCTION_CALL_FUNC) -> FUNCTION_CALL_FUNC:
        # TODO
        # pre check docstring
        if not func.__doc__:
            logger.error(f"函数 {func.__name__} 没有文档字串，不被加载")
            return func
        else:
            # 解析函数文档字串
            result = parse(docstring=func.__doc__)
            logger.debug(result.reduction())
        return func

    return decorator


# TODO 草案
# @caller(
#     description="这个函数用来给你算命",
#     parameters={
#         "birthday": String(description="生日"),
#         "gender": String(enum=["男", "女"], description="性别"),
#         "name": String(description="姓名"),
#     },
# )
# async def tell_fortune(birthday: str, name: str, gender: str) -> str:
#     """这个函数用来给你算命

#     Args:
#         birthday: 生日
#         name: 姓名

#     Returns:
#         str: 算命结果
#     """
#     return f"{name}，你的生日是{birthday}，你的运势是大吉大利"


@caller(
    description="这个函数用来给你算命",
).parameters(
    birthday=String(description="生日"),
    name=String(enum=["男", "女"], description="性别"),
    gender=String(description="姓名"),
)
async def tell_fortune(birthday: str, name: str, gender: str) -> str:
    """这个函数用来给你算命

    Args:
        birthday: 生日
        name: 姓名

    Returns:
        str: 算命结果
    """
    return f"{name}，你的生日是{birthday}，你的运势是大吉大利"
