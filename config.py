from pathlib import Path
from pydantic import BaseModel
from nonebot import get_plugin_config


class ConfigModel(BaseModel):
        marshoai_token: str = ""
config: ConfigModel = get_plugin_config(ConfigModel)
