from pathlib import Path

from nonebot import require

require("nonebot_plugin_localstore")
import json

from nonebot_plugin_localstore import get_data_file

memory_path = get_data_file("marshoai", "memory.json")
if not Path(memory_path).exists():
    with open(memory_path, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=4)
print(memory_path)


async def write_memory(memory: str, user_id: str):

    with open(memory_path, "r", encoding="utf-8") as f:
        memory_data = json.load(f)

    memorys = memory_data.get(user_id, [])
    memorys.append(memory)
    memory_data[user_id] = memorys

    with open(memory_path, "w", encoding="utf-8") as f:
        json.dump(memory_data, f, ensure_ascii=False, indent=4)

    return "记忆已经保存啦~"


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
        ...
        # TODO 用大模型对记忆进行整理
