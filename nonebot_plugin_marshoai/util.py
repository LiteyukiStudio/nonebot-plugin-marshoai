import base64
import json
import mimetypes
import os
import uuid
from typing import Any, Optional

import httpx
import nonebot_plugin_localstore as store

# from zhDateTime import DateTime
from azure.ai.inference.aio import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage
from nonebot import get_driver
from nonebot.log import logger
from nonebot_plugin_alconna import Image as ImageMsg
from nonebot_plugin_alconna import Text as TextMsg
from nonebot_plugin_alconna import UniMessage

from .config import config
from .constants import *
from .deal_latex import ConvertLatex

nickname_json = None  # 记录昵称
praises_json = None  # 记录夸赞名单
loaded_target_list = []  # 记录已恢复备份的上下文的列表

# noinspection LongLine
chromium_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


async def get_image_raw_and_type(
    url: str, timeout: int = 10
) -> Optional[tuple[bytes, str]]:
    """
    获取图片的二进制数据

    参数:
        url: str 图片链接
        timeout: int 超时时间 秒

    return:
        tuple[bytes, str]: 图片二进制数据, 图片MIME格式

    """

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=chromium_headers, timeout=timeout)
        if response.status_code == 200:
            # 获取图片数据
            content_type = response.headers.get("Content-Type")
            if not content_type:
                content_type = mimetypes.guess_type(url)[0]
            # image_format = content_type.split("/")[1] if content_type else "jpeg"
            return response.content, str(content_type)
        else:
            return None


async def get_image_b64(url: str, timeout: int = 10) -> Optional[str]:
    """
    获取图片的base64编码

    参数:
        url: 图片链接
        timeout: 超时时间 秒

    return: 图片base64编码
    """

    if data_type := await get_image_raw_and_type(url, timeout):
        # image_format = content_type.split("/")[1] if content_type else "jpeg"
        base64_image = base64.b64encode(data_type[0]).decode("utf-8")
        data_url = "data:{};base64,{}".format(data_type[1], base64_image)
        return data_url
    else:
        return None


async def make_chat(
    client: ChatCompletionsClient,
    msg: list,
    model_name: str,
    tools: Optional[list] = None,
):
    """调用ai获取回复

    参数:
        client: 用于与AI模型进行通信
        msg: 消息内容
        model_name: 指定AI模型名"""
    return await client.complete(
        messages=msg,
        model=model_name,
        tools=tools,
        temperature=config.marshoai_temperature,
        max_tokens=config.marshoai_max_tokens,
        top_p=config.marshoai_top_p,
    )


def get_praises():
    global praises_json
    if praises_json is None:
        praises_file = store.get_plugin_data_file(
            "praises.json"
        )  # 夸赞名单文件使用localstore存储
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
        return await load_context_from_json(
            f"back_up_context_{target_uid}", "contexts/backup"
        )
    return []


"""
以下函数依照 Mulan PSL v2 协议授权

函数: parse_markdown, get_uuid_back2codeblock

版权所有 © 2024 金羿ELS
Copyright (R) 2024 Eilles(EillesWan@outlook.com)

Licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:
         http://license.coscl.org.cn/MulanPSL2
THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""

if config.marshoai_enable_richtext_parse:

    latex_convert = ConvertLatex()  # 开启一个转换实例

    @get_driver().on_bot_connect
    async def load_latex_convert():
        await latex_convert.load_channel(None)

    async def get_uuid_back2codeblock(
        msg: str, code_blank_uuid_map: list[tuple[str, str]]
    ):

        for torep, rep in code_blank_uuid_map:
            msg = msg.replace(torep, rep)

        return msg

    async def parse_richtext(msg: str) -> UniMessage:
        """
        人工智能给出的回答一般不会包含 HTML 嵌入其中，但是包含图片或者 LaTeX 公式、代码块，都很正常。
        这个函数会把这些都以图片形式嵌入消息体。
        """

        if not IMG_LATEX_PATTERN.search(msg):  # 没有图片和LaTeX标签
            return UniMessage(msg)

        result_msg = UniMessage()  # type: ignore
        code_blank_uuid_map = [
            (uuid.uuid4().hex, cbp.group()) for cbp in CODE_BLOCK_PATTERN.finditer(msg)
        ]

        last_tag_index = 0

        # 代码块渲染麻烦，先不处理
        for rep, torep in code_blank_uuid_map:
            msg = msg.replace(torep, rep)

        # for to_rep in CODE_SINGLE_PATTERN.finditer(msg):
        #     code_blank_uuid_map.append((rep := uuid.uuid4().hex, to_rep.group()))
        #     msg = msg.replace(to_rep.group(), rep)

        # print("#####################\n", msg, "\n\n")

        # 插入图片
        for each_find_tag in IMG_LATEX_PATTERN.finditer(msg):

            tag_found = await get_uuid_back2codeblock(
                each_find_tag.group(), code_blank_uuid_map
            )
            result_msg.append(
                TextMsg(
                    await get_uuid_back2codeblock(
                        msg[last_tag_index : msg.find(tag_found)], code_blank_uuid_map
                    )
                )
            )

            last_tag_index = msg.find(tag_found) + len(tag_found)

            if each_find_tag.group(1):

                # 图形一定要优先考虑
                # 别忘了有些图形的地址就是 LaTeX，所以要优先判断

                image_description = tag_found[2 : tag_found.find("]")]
                image_url = tag_found[tag_found.find("(") + 1 : -1]

                if image_ := await get_image_raw_and_type(image_url):

                    result_msg.append(
                        ImageMsg(
                            raw=image_[0],
                            mimetype=image_[1],
                            name=image_description + ".png",
                        )
                    )
                    result_msg.append(TextMsg("（{}）".format(image_description)))

                else:
                    result_msg.append(TextMsg(tag_found))
            elif each_find_tag.group(2):

                latex_exp = await get_uuid_back2codeblock(
                    each_find_tag.group()
                    .replace("$", "")
                    .replace("\\(", "")
                    .replace("\\)", "")
                    .replace("\\[", "")
                    .replace("\\]", ""),
                    code_blank_uuid_map,
                )
                latex_generate_ok, latex_generate_result = (
                    await latex_convert.generate_png(
                        latex_exp,
                        dpi=300,
                        foreground_colour=config.marshoai_main_colour,
                    )
                )

                if latex_generate_ok:
                    result_msg.append(
                        ImageMsg(
                            raw=latex_generate_result,  # type: ignore
                            mimetype="image/png",
                            name="latex.png",
                        )
                    )
                else:
                    result_msg.append(TextMsg(latex_exp + "（公式解析失败）"))
                    if isinstance(latex_generate_result, str):
                        result_msg.append(TextMsg(latex_generate_result))
                    else:
                        result_msg.append(
                            ImageMsg(
                                raw=latex_generate_result,
                                mimetype="image/png",
                                name="latex_error.png",
                            )
                        )
            else:
                result_msg.append(TextMsg(tag_found + "（未知内容解析失败）"))

        result_msg.append(
            TextMsg(
                await get_uuid_back2codeblock(msg[last_tag_index:], code_blank_uuid_map)
            )
        )

        return result_msg


"""
Mulan PSL v2 协议授权部分结束
"""
