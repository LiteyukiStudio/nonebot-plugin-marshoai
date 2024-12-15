import inspect
from typing import Any

from nonebot import logger
from nonebot.adapters import Bot, Event
from nonebot.permission import Permission
from nonebot.rule import Rule
from nonebot.typing import T_State

from ..typing import ASYNC_FUNCTION_CALL_FUNC, F
from .utils import async_wrap, is_coroutine_callable

_caller_data: dict[str, "Caller"] = {}


class Caller:
    def __init__(self, name: str | None = None, description: str | None = None):
        self._name = name
        self._description = description
        self.func: ASYNC_FUNCTION_CALL_FUNC | None = None
        self._parameters: dict[str, Any] = {}
        """依赖注入的参数"""
        self.bot: Bot | None = None
        self.event: Event | None = None
        self.state: T_State | None = None

        self._permission: Permission | None = None
        self._rule: Rule | None = None

    def params(self, **kwargs: Any) -> "Caller":
        self._parameters.update(kwargs)
        return self

    def permission(self, permission: Permission) -> "Caller":
        self._permission = self._permission or permission
        return self

    async def pre_check(self) -> tuple[bool, str]:
        if self.bot is None or self.event is None:
            return False, "Context is None"
        if self._permission and not await self._permission(self.bot, self.event):
            return False, "Permission Denied 权限不足"

        if self.state is None:
            return False, "State is None"
        if self._rule and not await self._rule(self.bot, self.event, self.state):
            return False, "Rule Denied 规则不匹配"

        return True, ""

    def rule(self, rule: Rule) -> "Caller":
        self._rule = self._rule and rule
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
        self._description = description
        return self

    def __call__(self, func: F) -> F:
        """装饰函数，注册为一个可被AI调用的function call函数

        Args:
            func (F): 函数对象

        Returns:
            F: 函数对象
        """
        global _caller_data
        if self._name is None:
            if module := inspect.getmodule(func):
                module_name = module.__name__.split(".")[-1]
            else:
                module_name = ""
            self._name = f"{module_name}-{func.__name__}"
        _caller_data[self._name] = self

        if is_coroutine_callable(func):
            self.func = func  # type: ignore
        else:
            self.func = async_wrap(func)  # type: ignore

        if module := inspect.getmodule(func):
            module_name = module.__name__ + "."
        else:
            module_name = ""
        logger.opt(colors=True).info(
            f"<y>加载函数 {module_name}{func.__name__}: {self._description}</y>"
        )

        return func

    def data(self) -> dict[str, Any]:
        """返回函数的json数据

        Returns:
            dict[str, Any]: 函数的json数据
        """
        return {
            "type": "function",
            "function": {
                "name": self._name,
                "description": self._description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        key: value.data() for key, value in self._parameters.items()
                    },
                },
                "required": [
                    key
                    for key, value in self._parameters.items()
                    if value.default is None
                ],
            },
        }

    def set_event(self, event: Event):
        self.event = event

    def set_bot(self, bot: Bot):
        self.bot = bot

    async def call(self, *args: Any, **kwargs: Any) -> Any:
        """调用函数

        Returns:
            Any: 函数返回值
        """
        y, r = await self.pre_check()
        if not y:
            logger.debug(f"Function {self._name} pre_check failed: {r}")
            return r

        if self.func is None:
            raise ValueError("未注册函数对象")
        sig = inspect.signature(self.func)
        for name, param in sig.parameters.items():
            if issubclass(param.annotation, Event) or isinstance(
                param.annotation, Event
            ):
                kwargs[name] = self.event

            if issubclass(param.annotation, Caller) or isinstance(
                param.annotation, Caller
            ):
                kwargs[name] = self

            if issubclass(param.annotation, Bot) or isinstance(param.annotation, Bot):
                kwargs[name] = self.bot

            if param.annotation == T_State:
                kwargs[name] = self.state

        # 检查形参是否有默认值或传入，若没有则用parameters中的默认值填充
        for name, param in sig.parameters.items():
            if name not in kwargs:
                kwargs[name] = self._parameters.get(name, param.default)

        return await self.func(*args, **kwargs)


def on_function_call(name: str | None = None, description: str | None = None) -> Caller:
    """返回一个Caller类，可用于装饰一个函数，使其注册为一个可被AI调用的function call函数

    Args:
        description: 函数描述，若为None则从函数的docstring中获取

    Returns:
        Caller: Caller对象
    """
    caller = Caller(name=name, description=description)
    return caller


def get_function_calls() -> dict[str, Caller]:
    """获取所有已注册的function call函数

    Returns:
        dict[str, Caller]: 所有已注册的function call函数
    """
    return _caller_data
