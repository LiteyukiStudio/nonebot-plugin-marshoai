from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    MessageEvent,
    PrivateMessageEvent,
)
from nonebot.exception import FinishedException
from nonebot.permission import SUPERUSER

from nonebot_plugin_marshoai.plugin import String, on_function_call


@on_function_call(description="获取当前会话信息，比如群聊或用户的身份信息").permission(
    SUPERUSER
)
async def get_session_info(bot: Bot, event: MessageEvent) -> str:
    """获取当前会话信息，比如群聊或用户的身份信息

    Args:
        bot (Bot): Bot对象

    Returns:
        str: 会话信息
    """
    if isinstance(event, PrivateMessageEvent):
        return f"当前会话为私聊，用户ID: {event.user_id}"
    elif isinstance(event, GroupMessageEvent):
        return f"当前会话为群聊，群组ID: {event.group_id}, 用户ID: {event.user_id}"
    else:
        return "未知会话类型"


@on_function_call(description="发送消息到指定用户").params(
    user=String(description="用户ID"), message=String(description="消息内容")
).permission(SUPERUSER)
async def send_message(user: str, message: str, bot: Bot) -> str:
    """发送消息到指定用户，实验性功能，仅限onebotv11适配器

    Args:
        user (str): 用户ID
        message (str): 消息内容

    Returns:
        str: 发送结果
    """
    try:
        await bot.send_private_msg(user_id=int(user), message=message)
        return "发送成功"
    except FinishedException as e:
        return "发送完成"
    except Exception as e:
        return "发送失败: " + str(e)


@on_function_call(description="发送消息到指定群组").params(
    group=String(description="群组ID"), message=String(description="消息内容")
).permission(SUPERUSER)
async def send_group_message(group: str, message: str, bot: Bot) -> str:
    """发送消息到指定群组，实验性功能，仅限onebotv11适配器

    Args:
        group (str): 群组ID
        message (str): 消息内容

    Returns:
        str: 发送结果
    """
    try:
        await bot.send_group_msg(group_id=int(group), message=message)
        return "发送成功"
    except FinishedException as e:
        return "发送完成"
    except Exception as e:
        return "发送失败: " + str(e)
