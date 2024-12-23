from nonebot_plugin_marshoai.plugin import PluginMetadata, String, on_function_call

metadata = PluginMetadata(
    name="天气查询", author="MarshoAI", description="一个简单的查询天气的插件"
)


@on_function_call(description="可以用于查询天气").params(
    location=String(description="地点")
)
async def weather(location: str) -> str:
    # 这里可以调用天气API查询天气，这里只是一个简单的示例
    return f"{location}的天气是晴天, 温度是25°C"
