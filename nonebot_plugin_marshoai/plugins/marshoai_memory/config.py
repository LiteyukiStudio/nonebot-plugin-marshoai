from nonebot import get_plugin_config, logger
from pydantic import BaseModel


class ConfigModel(BaseModel):
    marshoai_plugin_memory_scheduler: bool = True


plugin_config: ConfigModel = get_plugin_config(ConfigModel)
