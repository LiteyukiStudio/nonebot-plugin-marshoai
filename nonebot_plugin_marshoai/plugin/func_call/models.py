from typing import TYPE_CHECKING, Any

from nonebot.adapters import Bot, Event
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from pydantic import BaseModel

if TYPE_CHECKING:
    from .caller import Caller


class SessionContext(BaseModel):
    """依赖注入会话上下文

    Args:
        BaseModel (_type_): _description_
    """

    bot: Bot
    event: Event
    matcher: Matcher
    state: T_State
    caller: Any = None

    class Config:
        arbitrary_types_allowed = True


class SessionContextDepends(BaseModel):
    bot: str | None = None
    event: str | None = None
    matcher: str | None = None
    state: str | None = None
    caller: str | None = None
