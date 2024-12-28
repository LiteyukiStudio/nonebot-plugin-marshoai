import inspect
from typing import Any

from nonebot import logger
from nonebot.adapters import Bot, Event
from nonebot.matcher import Matcher
from nonebot.permission import Permission
from nonebot.rule import Rule
from nonebot.typing import T_State

from ..models import Plugin
from ..typing import ASYNC_FUNCTION_CALL_FUNC, F
from .models import SessionContext, SessionContextDepends
from .utils import async_wrap, is_coroutine_callable

_caller_data: dict[str, "Caller"] = {}


class Caller:
    def __init__(self, name: str = "", description: str | None = None):
        self._name: str = name
        """函数名称"""
        self._description = description
        """函数描述"""
        self._plugin: Plugin | None = None
        """所属插件对象，装饰时声明"""
        self.func: ASYNC_FUNCTION_CALL_FUNC | None = None
        """函数对象"""
        self.module_name: str = ""
        """模块名，仅为父级模块名，不一定是插件顶级模块名"""
        self._parameters: dict[str, Any] = {}
        """声明参数"""

        self.di: SessionContextDepends = SessionContextDepends()
        """依赖注入的参数信息"""

        self.default: dict[str, Any] = {}
        """默认值"""

        self.ctx: SessionContext | None = None

        self._permission: Permission | None = None
        self._rule: Rule | None = None

    def params(self, **kwargs: Any) -> "Caller":
        self._parameters.update(kwargs)
        return self

    def permission(self, permission: Permission) -> "Caller":
        self._permission = self._permission or permission
        return self

    async def pre_check(self) -> tuple[bool, str]:
        if self.ctx is None:
            return False, "上下文为空"
        if self.ctx.bot is None or self.ctx.event is None:
            return False, "Context is None"
        if self._permission and not await self._permission(
            self.ctx.bot, self.ctx.event
        ):
            return False, "告诉用户 Permission Denied 权限不足"

        if self.ctx.state is None:
            return False, "State is None"
        if self._rule and not await self._rule(
            self.ctx.bot, self.ctx.event, self.ctx.state
        ):
            return False, "告诉用户 Rule Denied 规则不匹配"

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
        if not self._name:
            self._name = func.__name__

        # 检查函数签名，确定依赖注入参数
        sig = inspect.signature(func)
        for name, param in sig.parameters.items():
            if issubclass(param.annotation, Event) or isinstance(
                param.annotation, Event
            ):
                self.di.event = name

            if issubclass(param.annotation, Caller) or isinstance(
                param.annotation, Caller
            ):
                self.di.caller = name

            if issubclass(param.annotation, Bot) or isinstance(param.annotation, Bot):
                self.di.bot = name

            if issubclass(param.annotation, Matcher) or isinstance(
                param.annotation, Matcher
            ):
                self.di.matcher = name

            if param.annotation == T_State:
                self.di.state = name

        # 检查默认值情况
        for name, param in sig.parameters.items():
            if param.default is not inspect.Parameter.empty:
                self.default[name] = param.default

        if is_coroutine_callable(func):
            self.func = func  # type: ignore
        else:
            self.func = async_wrap(func)  # type: ignore

        if module := inspect.getmodule(func):
            module_name = module.__name__.split(".")[-1]
        else:
            module_name = ""

        self.module_name = module_name
        _caller_data[self.full_name] = self
        logger.opt(colors=True).debug(
            f"<y>加载函数 {self.full_name}: {self._description}</y>"
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
                "name": self.aifc_name,
                "description": self._description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        **{
                            key: value.data() for key, value in self._parameters.items()
                        },
                        "placeholder": {
                            "type": "string",
                            "description": "占位符，用于显示在对话框中",  # 为保证兼容性而设置的无用参数
                        },
                    },
                },
                "required": [
                    key
                    for key, value in self._parameters.items()
                    if value.default is None
                ],
            },
        }

    def set_ctx(self, ctx: SessionContext) -> None:
        """设置依赖注入上下文

        Args:
            ctx (SessionContext): 依赖注入上下文
        """
        ctx.caller = self
        self.ctx = ctx
        for type_name, arg_name in self.di.model_dump().items():

            if arg_name:
                self.default[arg_name] = ctx.__getattribute__(type_name)

    def with_ctx(self, ctx: SessionContext) -> "Caller":
        """设置依赖注入上下文

        Args:
            ctx (SessionContext): 依赖注入上下文

        Returns:
            Caller: Caller对象
        """
        self.set_ctx(ctx)
        return self

    def __str__(self) -> str:
        return f"{self._name}({self._description})\n" + "\n".join(
            f"  - {key}: {value}" for key, value in self._parameters.items()
        )

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

        # 检查形参是否有默认值或传入，若没有则用default中的默认值填充
        for name, value in self.default.items():
            if name not in kwargs:
                kwargs[name] = value

        return await self.func(*args, **kwargs)

    @property
    def short_name(self) -> str:
        """函数本名"""
        return self._name.split(".")[-1]

    @property
    def aifc_name(self) -> str:
        """AI调用名，没有点"""
        return self.full_name.replace(".", "-")

    @property
    def full_name(self) -> str:
        """完整名"""
        return self.module_name + "." + self._name

    @property
    def short_info(self) -> str:
        return f"{self.full_name}({self._description})"


def on_function_call(name: str = "", description: str | None = None) -> Caller:
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
