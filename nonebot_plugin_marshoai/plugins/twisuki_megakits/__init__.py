from nonebot_plugin_marshoai.plugin import (
    Integer,
    Parameter,
    PluginMetadata,
    String,
    on_function_call,
)

from . import mk_morse_code, mk_nya_code

__marsho_meta__ = PluginMetadata(
    name="MegaKits插件",
    description="一个功能混杂的多文件插件",
    author="Twisuki",
)


@on_function_call(description="摩尔斯电码加密").params(
    msg=String(description="被加密语句")
)
async def morse_encrypt(msg: str) -> str:
    """摩尔斯电码加密"""
    return str(await mk_morse_code.morse_encrypt(msg))


@on_function_call(description="摩尔斯电码解密").params(
    msg=String(description="被解密语句")
)
async def morse_decrypt(msg: str) -> str:
    """摩尔斯电码解密"""
    return str(await mk_morse_code.morse_decrypt(msg))


@on_function_call(description="转换为猫语").params(msg=String(description="被转换语句"))
async def nya_encrypt(msg: str) -> str:
    """转换为猫语"""
    return str(await mk_nya_code.nya_encrypt(msg))


@on_function_call(description="将猫语翻译回人类语言").params(
    msg=String(description="被翻译语句")
)
async def nya_decrypt(msg: str) -> str:
    """将猫语翻译回人类语言"""
    return str(await mk_nya_code.nya_decrypt(msg))
