from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_alconna")
require("nonebot_plugin_localstore")
from .azure import *
from nonebot import get_driver, logger
from .config import config
from .metadata import metadata
import nonebot_plugin_localstore as store

__author__ = "Asankilp"
__plugin_meta__ = metadata
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
