import inspect
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable

from ..typing import F


def copy_signature(func: F) -> Callable[[Callable[..., Any]], F]:
    """复制函数签名和文档字符串的装饰器"""

    def decorator(wrapper: Callable[..., Any]) -> F:
        @wraps(func)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            return wrapper(*args, **kwargs)

        return wrapped  # type: ignore

    return decorator


def async_wrap(func: F) -> F:
    """装饰器，将同步函数包装为异步函数

    Args:
        func (F): 函数对象

    Returns:
        F: 包装后的函数对象
    """

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return wrapper  # type: ignore


def is_coroutine_callable(call: Callable[..., Any]) -> bool:
    """
    判断是否为async def 函数
    请注意：是否为 async def 函数与该函数是否能被await调用是两个不同的概念，具体取决于函数返回值是否为awaitable对象
    Args:
        call: 可调用对象
    Returns:
        bool: 是否为async def函数
    """
    if inspect.isroutine(call):
        return inspect.iscoroutinefunction(call)
    if inspect.isclass(call):
        return False
    func_ = getattr(call, "__call__", None)
    return inspect.iscoroutinefunction(func_)
