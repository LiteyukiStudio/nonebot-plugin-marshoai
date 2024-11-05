from nonebot.plugin import PluginMetadata, inherit_supported_adapters
from .config import ConfigModel, config
from .constants import USAGE

metadata = PluginMetadata(
    name="Marsho AI插件",
    description="接入Azure服务的AI聊天插件",
    usage=USAGE,
    type="application",
    config=ConfigModel,
    homepage="https://github.com/LiteyukiStudio/nonebot-plugin-marshoai",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={"License": "MIT", "Author": "Asankilp"},
)
