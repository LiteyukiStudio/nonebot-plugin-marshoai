import aiofiles  # type: ignore
from nonebot.permission import SUPERUSER

from nonebot_plugin_marshoai.plugin import String, on_function_call


@on_function_call(description="获取设备上本地文件内容").params(
    fp=String(description="文件路径")
).permission(SUPERUSER)
async def read_file(fp: str) -> str:
    """获取设备上本地文件内容

    Args:
        fp (str): 文件路径

    Returns:
        str: 文件内容
    """
    try:
        async with aiofiles.open(fp, "r", encoding="utf-8") as f:
            return await f.read()
    except Exception as e:
        return "读取出错: " + str(e)
