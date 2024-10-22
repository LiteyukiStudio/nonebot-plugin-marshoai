from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require
require("nonebot_plugin_alconna")
require("nonebot_plugin_localstore")
from .azure import *
from nonebot import get_driver, logger
from .config import ConfigModel, config
from .constants import USAGE
import nonebot_plugin_localstore as store

__author__ = "Asankilp"
__plugin_meta__ = PluginMetadata(
    name="Marsho AI插件",
    description="接入Azure服务的AI聊天插件",
    usage=USAGE,
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
    logger.info("マルショは、高性能ですから!")
