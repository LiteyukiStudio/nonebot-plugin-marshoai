from typing import Any, Callable, Coroutine, TypeAlias

SYNC_FUNCTION_CALL_FUNC: TypeAlias = Callable[..., str]
ASYNC_FUNCTION_CALL_FUNC: TypeAlias = Callable[..., Coroutine[str, Any, str]]
FUNCTION_CALL_FUNC: TypeAlias = SYNC_FUNCTION_CALL_FUNC | ASYNC_FUNCTION_CALL_FUNC
