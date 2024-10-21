from nonebot import on_type, message
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import PokeNotifyEvent
poke_notify = on_type(
        (PokeNotifyEvent,),
        rule=to_me()
    )

