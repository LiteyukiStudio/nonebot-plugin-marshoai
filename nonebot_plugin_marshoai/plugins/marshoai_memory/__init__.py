import json
from pathlib import Path

from azure.ai.inference.models import UserMessage
from nonebot import get_driver, logger, require
from nonebot_plugin_localstore import get_plugin_data_file

require("nonebot_plugin_apscheduler")
require("nonebot_plugin_marshoai")
from nonebot_plugin_apscheduler import scheduler

from nonebot_plugin_marshoai.instances import client
from nonebot_plugin_marshoai.plugin import PluginMetadata, on_function_call
from nonebot_plugin_marshoai.plugin.func_call.params import String

from .command import *
from .config import plugin_config

__marsho_meta__ = PluginMetadata(
    name="记忆保存",
    author="MarshoAI",
    description="这个插件可以帮助AI记住一些事情",
)

memory_path = get_plugin_data_file("memory.json")
if not Path(memory_path).exists():
    with open(memory_path, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=4)
# print(memory_path)
driver = get_driver()


@on_function_call(
    description="当你发现与你对话的用户的一些信息值得你记忆，或者用户让你记忆等时，调用此函数存储记忆内容"
).params(
    memory=String(description="你想记住的内容，概括并保留关键内容"),
    user_id=String(description="你想记住的人的id"),
)
async def write_memory(memory: str, user_id: str):

    with open(memory_path, "r", encoding="utf-8") as f:
        memory_data = json.load(f)

    memorys = memory_data.get(user_id, [])
    memorys.append(memory)
    memory_data[user_id] = memorys

    with open(memory_path, "w", encoding="utf-8") as f:
        json.dump(memory_data, f, ensure_ascii=False, indent=4)

    return "记忆已经保存啦~"


@on_function_call(
    description="你需要回忆有关用户的一些知识时，调用此函数读取记忆内容，当用户问问题的时候也尽量调用此函数参考"
).params(user_id=String(description="你想读取记忆的人的id"))
async def read_memory(user_id: str):
    with open(memory_path, "r", encoding="utf-8") as f:
        memory_data = json.load(f)
    memorys = memory_data.get(user_id, [])
    if not memorys:
        return "好像对ta还没有任何记忆呢~"

    return "这些是有关ta的记忆：" + "\n".join(memorys)


async def organize_memories():
    with open(memory_path, "r", encoding="utf-8") as f:
        memory_data = json.load(f)
    for i in memory_data:
        memory_data_ = "\n".join(memory_data[i])
        msg = f"这是一些大模型记忆信息，请你保留重要内容，尽量减少无用的记忆后重新输出记忆内容，浓缩为一行：\n{memory_data_}"
        res = await client.complete(UserMessage(content=msg))
        try:
            memory = res.choices[0].message.content  # type: ignore
            memory_data[i] = memory
        except AttributeError:
            logger.error(f"整理关于{i}的记忆时出错：{res}")

    with open(memory_path, "w", encoding="utf-8") as f:
        json.dump(memory_data, f, ensure_ascii=False, indent=4)


if plugin_config.marshoai_plugin_memory_scheduler:

    @driver.on_startup
    async def _():
        logger.info("小棉定时记忆整理已启动！")
        scheduler.add_job(
            organize_memories,
            "cron",
            hour="0",
            minute="0",
            second="0",
            day="*",
            id="organize_memories",
        )
