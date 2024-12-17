from nonebot_plugin_marshoai.plugin import get_plugins, on_function_call


@on_function_call(description="获取已加载的插件列表")
def get_marsho_plugins() -> str:
    """获取已加载的插件列表

    Returns:
        str: 插件列表
    """

    reply = "加载的插件列表"
    for p in get_plugins().values():
        if p.metadata:
            reply += f"名称: {p.metadata.name}，描述: {p.metadata.description}\n"
        else:
            reply += f"名称: {p.name}，描述: 暂无\n"
    return reply
