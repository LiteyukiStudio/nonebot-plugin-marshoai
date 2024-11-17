import base64
import mimetypes
import os
import json
from typing import Any
import httpx
import nonebot_plugin_localstore as store
from datetime import datetime

from nonebot.log import logger
from zhDateTime import DateTime  # type: ignore
from azure.ai.inference.aio import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage
from .config import config

nickname_json = None  # 记录昵称
praises_json = None  # 记录夸赞名单
loaded_target_list = []  # 记录已恢复备份的上下文的列表


async def get_image_b64(url):
    # noinspection LongLine
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            # 获取图片数据
            image_data = response.content
            content_type = response.headers.get("Content-Type")
            if not content_type:
                content_type = mimetypes.guess_type(url)[0]
            # image_format = content_type.split("/")[1] if content_type else "jpeg"
            base64_image = base64.b64encode(image_data).decode("utf-8")
            data_url = f"data:{content_type};base64,{base64_image}"
            return data_url
        else:
            return None


async def make_chat(client: ChatCompletionsClient, msg: list, model_name: str):
    """调用ai获取回复

    参数:
        client: 用于与AI模型进行通信
        msg: 消息内容
        model_name: 指定AI模型名"""
    return await client.complete(
        messages=msg,
        model=model_name,
        temperature=config.marshoai_temperature,
        max_tokens=config.marshoai_max_tokens,
        top_p=config.marshoai_top_p,
    )


def get_praises():
    global praises_json
    if praises_json is None:
        praises_file = store.get_plugin_data_file("praises.json")  # 夸赞名单文件使用localstore存储
        if not os.path.exists(praises_file):
            init_data = {
                "like": [
                    {
                        "name": "Asankilp",
                        "advantages": "赋予了Marsho猫娘人格，使用vim与vscode为Marsho写了许多代码，使Marsho更加可爱",
                    }
                ]
            }
            with open(praises_file, "w", encoding="utf-8") as f:
                json.dump(init_data, f, ensure_ascii=False, indent=4)
        with open(praises_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        praises_json = data
    return praises_json


async def refresh_praises_json():
    global praises_json
    praises_file = store.get_plugin_data_file("praises.json")
    if not os.path.exists(praises_file):
        init_data = {
            "like": [
                {
                    "name": "Asankilp",
                    "advantages": "赋予了Marsho猫娘人格，使用vim与vscode为Marsho写了许多代码，使Marsho更加可爱",
                }
            ]
        }
        with open(praises_file, "w", encoding="utf-8") as f:
            json.dump(init_data, f, ensure_ascii=False, indent=4)
    with open(praises_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    praises_json = data


def build_praises():
    praises = get_praises()
    result = ["你喜欢以下几个人物，他们有各自的优点："]
    for item in praises["like"]:
        result.append(f"名字：{item['name']}，优点：{item['advantages']}")
    return "\n".join(result)


async def save_context_to_json(name: str, context: Any, path: str):
    context_dir = store.get_plugin_data_dir() / path
    os.makedirs(context_dir, exist_ok=True)
    file_path = os.path.join(context_dir, f"{name}.json")
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(context, json_file, ensure_ascii=False, indent=4)


async def load_context_from_json(name: str, path: str) -> list:
    """从指定路径加载历史记录"""
    context_dir = store.get_plugin_data_dir() / path
    os.makedirs(context_dir, exist_ok=True)
    file_path = os.path.join(context_dir, f"{name}.json")
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return []


async def set_nickname(user_id: str, name: str):
    global nickname_json
    filename = store.get_plugin_data_file("nickname.json")
    if not os.path.exists(filename):
        data = {}
    else:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    data[user_id] = name
    if name == "" and user_id in data:
        del data[user_id]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    nickname_json = data


# noinspection PyBroadException
async def get_nicknames():
    """获取nickname_json, 优先来源于全局变量"""
    global nickname_json
    if nickname_json is None:
        filename = store.get_plugin_data_file("nickname.json")
        try:
            with open(filename, "r", encoding="utf-8") as f:
                nickname_json = json.load(f)
        except Exception:
            nickname_json = {}
    return nickname_json


async def refresh_nickname_json():
    """强制刷新nickname_json, 刷新全局变量"""
    global nickname_json
    filename = store.get_plugin_data_file("nickname.json")
    # noinspection PyBroadException
    try:
        with open(filename, "r", encoding="utf-8") as f:
            nickname_json = json.load(f)
    except Exception:
        logger.error("Error loading nickname.json")


def get_prompt():
    """获取系统提示词"""
    prompts = ""
    prompts += config.marshoai_additional_prompt
    if config.marshoai_enable_praises:
        praises_prompt = build_praises()
        prompts += praises_prompt
    if config.marshoai_enable_time_prompt:
        current_time = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        current_lunar_date = (
            DateTime.now().to_lunar().date_hanzify()[5:]
        )  # 库更新之前使用切片
        time_prompt = f"现在的时间是{current_time}，农历{current_lunar_date}。"
        prompts += time_prompt
    marsho_prompt = config.marshoai_prompt
    spell = SystemMessage(content=marsho_prompt + prompts).as_dict()
    return spell


def suggest_solution(errinfo: str) -> str:
    # noinspection LongLine
    suggestions = {
        "content_filter": "消息已被内容过滤器过滤。请调整聊天内容后重试。",
        "RateLimitReached": "模型达到调用速率限制。请稍等一段时间或联系Bot管理员。",
        "tokens_limit_reached": "请求token达到上限。请重置上下文。",
        "content_length_limit": "请求体过大。请重置上下文。",
        "unauthorized": "访问token无效。请联系Bot管理员。",
        "invalid type: parameter messages.content is of type array but should be of type string.": "聊天请求体包含此模型不支持的数据类型。请重置上下文。",
        "At most 1 image(s) may be provided in one request.": "此模型只能在上下文中包含1张图片。如果此前的聊天已经发送过图片，请重置上下文。",
    }

    for key, suggestion in suggestions.items():
        if key in errinfo:
            return f"\n{suggestion}"

    return ""


async def get_backup_context(target_id: str, target_private: bool) -> list:
    """获取历史上下文"""
    global loaded_target_list
    if target_private:
        target_uid = f"private_{target_id}"
    else:
        target_uid = f"group_{target_id}"
    if target_uid not in loaded_target_list:
        loaded_target_list.append(target_uid)
        return await load_context_from_json(f"back_up_context_{target_uid}", "contexts/backup")
    return []
