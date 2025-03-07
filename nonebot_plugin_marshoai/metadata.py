from nonebot.plugin import PluginMetadata, inherit_supported_adapters

from .config import ConfigModel
from .constants import USAGE

metadata = PluginMetadata(
    name="Marsho AI 插件",
    description="接入 Azure API 或其他 API 的 AI 聊天插件，支持图片处理，外部函数调用，兼容包括 DeepSeek-R1， QwQ-32B 在内的多个模型",
    usage=USAGE,
    type="application",
    config=ConfigModel,
    homepage="https://github.com/LiteyukiStudio/nonebot-plugin-marshoai",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={"License": "MIT, Mulan PSL v2", "Author": "Asankilp, LiteyukiStudio"},
)
