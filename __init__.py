from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require
require("nonebot_plugin_htmlrender")
require("nonebot_plugin_alconna")
from .azure import *
from nonebot import get_driver
#from .config import ConfigModel
usage = """MarshoAI Alpha by Asankilp
用法：
  marsho <聊天内容>
与 Marsho 进行对话。当模型为gpt时，可以带上图片进行对话。
  changemodel <模型名>
切换 AI 模型。仅超级用户可用。
  reset
重置上下文。仅超级用户可用。
注意事项：
当 Marsho 回复消息为None或以content_filter开头的错误信息时，表示该消息被内容过滤器过滤，请调整你的聊天内容确保其合规。
当回复以RateLimitReached开头的错误信息时，该 AI 模型的次数配额已用尽，请联系Bot管理员。
※本AI的回答"按原样"提供，不提供任何担保。AI也会犯错，请仔细甄别回答的准确性。"""
__author__ = "Asankilp"
__plugin_meta__ = PluginMetadata(
    name="Marsho AI插件",
    description="接入Azure服务的AI聊天插件",
    usage=usage,
    type="application",
    homepage="https://github.com/LiteyukiStudio/nonebot-plugin-marshoai",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={"License":"MIT","Author":"Asankilp"}
)
driver = get_driver()


@driver.on_startup
async def _():
    pass

