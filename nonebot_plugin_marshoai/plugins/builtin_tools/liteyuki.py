from httpx import AsyncClient

from nonebot_plugin_marshoai.plugin import on_function_call


@on_function_call(description="获取分布式轻雪机器人节点情况")
async def get_liteyuki_info() -> str:
    """获取分布式轻雪机器人节点情况

    Returns:
        str: 节点情况
    """
    register = 0
    online = 0
    async with AsyncClient() as client:
        response = await client.get("https://api.liteyuki.icu/count")
        register = response.json().get("register")

        response = await client.get("https://api.liteyuki.icu/online")
        online = response.json().get("online")

    return f"注册节点数: {register}\n在线节点数: {online}"
