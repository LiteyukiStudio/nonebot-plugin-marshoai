from nonebot import on_type
from nonebot.adapters.onebot.v11 import PokeNotifyEvent  # type: ignore
from nonebot.rule import to_me

poke_notify = on_type((PokeNotifyEvent,), rule=to_me())
