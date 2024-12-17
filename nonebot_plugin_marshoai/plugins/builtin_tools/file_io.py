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


@on_function_call(description="写入内容到设备上本地文件").params(
    fp=String(description="文件路径"), content=String(description="写入内容")
).permission(SUPERUSER)
async def write_file(fp: str, content: str) -> str:
    """写入内容到设备上本地文件

    Args:
        fp (str): 文件路径
        content (str): 写入内容

    Returns:
        str: 写入结果
    """
    try:
        async with aiofiles.open(fp, "w", encoding="utf-8") as f:
            await f.write(content)
        return "写入成功"
    except Exception as e:
        return "写入出错: " + str(e)
