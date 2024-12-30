from pydantic import BaseModel
from nonebot import get_plugin_config, logger

class ConfigModel(BaseModel):
    marshoai_plugin_memory_scheduler: bool = True
    
plugin_config: ConfigModel = get_plugin_config(ConfigModel)