from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require
require("nonebot_plugin_alconna")
require("nonebot_plugin_localstore")
from .azure import *
from nonebot import get_driver, logger
from .config import ConfigModel, config
import nonebot_plugin_localstore as store
usage = """MarshoAI Alpha by Asankilp
用法：
  marsho <聊天内容> : 与 Marsho 进行对话。当模型为 GPT-4o(-mini) 等时，可以带上图片进行对话。
  reset : 重置当前会话的上下文。 ※需要加上命令前缀使用(默认为'/')。
超级用户命令(均需要加上命令前缀使用):
  changemodel <模型名> : 切换全局 AI 模型。
  contexts : 返回当前会话的上下文列表。 ※当上下文包含图片时，不要使用此命令。
  praises : 返回夸赞名单的提示词。
  usermsg <消息> : 往当前会话添加用户消息(UserMessage)。
  assistantmsg <消息> : 往当前会话添加助手消息(AssistantMessage)。
  savecontext <文件名> : 保存当前会话的上下文至插件数据目录下的contexts/<文件名>.json里。
  loadcontext <文件名> : 从插件数据目录下的contexts/<文件名>.json里读取上下文并覆盖到当前会话。
注意事项：
  - 当 Marsho 回复消息为None或以content_filter开头的错误信息时，表示该消息被内容过滤器过滤，请调整你的聊天内容确保其合规。
  - 当回复以RateLimitReached开头的错误信息时，该 AI 模型的次数配额已用尽，请联系Bot管理员。
※本AI的回答"按原样"提供，不提供任何担保。AI也会犯错，请仔细甄别回答的准确性。"""
__author__ = "Asankilp"
__plugin_meta__ = PluginMetadata(
    name="Marsho AI插件",
    description="接入Azure服务的AI聊天插件",
    usage=usage,
    type="application",
    config=ConfigModel,
    homepage="https://github.com/LiteyukiStudio/nonebot-plugin-marshoai",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={"License":"MIT","Author":"Asankilp"}
)
driver = get_driver()


@driver.on_startup
async def _():
    logger.info("MarshoAI 已经加载~🐾")
    logger.info(f"Marsho 的插件数据存储于 : {str(store.get_plugin_data_dir())} 哦~🐾")
    if config.marshoai_token == "":
        logger.warning("token 未配置。可能无法进行聊天。")
    else:
        logger.info("token 已配置~！🐾")

