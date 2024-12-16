from nonebot.plugin import PluginMetadata, inherit_supported_adapters

from .config import ConfigModel
from .constants import USAGE

metadata = PluginMetadata(
    name="Marsho AI插件",
    description="接入Azure服务或其他API的AI猫娘聊天插件，支持图片处理，外部函数调用，兼容多个AI模型，可解析AI回复的富文本信息",
    usage=USAGE,
    type="application",
    config=ConfigModel,
    homepage="https://github.com/LiteyukiStudio/nonebot-plugin-marshoai",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={"License": "MIT, Mulan PSL v2", "Author": "Asankilp, LiteyukiStudio"},
)
