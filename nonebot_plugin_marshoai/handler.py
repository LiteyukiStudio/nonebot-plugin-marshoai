from typing import Optional, Union

from azure.ai.inference.models import (
    AssistantMessage,
    ImageContentItem,
    ImageUrl,
    TextContentItem,
    ToolMessage,
    UserMessage,
)
from nonebot.adapters import Event
from nonebot.log import logger
from nonebot.matcher import Matcher, current_event, current_matcher
from nonebot_plugin_alconna.uniseg import UniMessage, UniMsg
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

from .config import config
from .constants import SUPPORT_IMAGE_MODELS
from .models import MarshoContext
from .util import (
    get_backup_context,
    get_image_b64,
    get_nickname_by_user_id,
    get_prompt,
    make_chat_openai,
)


class MarshoHandler:
    def __init__(
        self,
        client: AsyncOpenAI,
        context: MarshoContext,
    ):
        self.client = client
        self.context = context
        self.event: Event = current_event.get()
        self.matcher: Matcher = current_matcher.get()
        self.message_id: str = UniMessage.get_message_id(self.event)
        self.target = UniMessage.get_target(self.event)

    async def process_user_input(
        self, user_input: UniMsg, model_name: str
    ) -> Union[str, list]:
        """
        处理用户输入
        """
        is_support_image_model = (
            model_name.lower()
            in SUPPORT_IMAGE_MODELS + config.marshoai_additional_image_models
        )
        usermsg = [] if is_support_image_model else ""
        user_nickname = await get_nickname_by_user_id(self.event.get_user_id())
        if user_nickname:
            nickname_prompt = f"此消息的说话者为: {user_nickname}"
        else:
            nickname_prompt = ""
        for i in user_input:  # type: ignore
            if i.type == "text":
                if is_support_image_model:
                    usermsg += [TextContentItem(text=i.data["text"] + nickname_prompt).as_dict()]  # type: ignore
                else:
                    usermsg += str(i.data["text"] + nickname_prompt)  # type: ignore
            elif i.type == "image":
                if is_support_image_model:
                    usermsg.append(  # type: ignore
                        ImageContentItem(
                            image_url=ImageUrl(  # type: ignore
                                url=str(await get_image_b64(i.data["url"]))  # type: ignore
                            )  # type: ignore
                        ).as_dict()  # type: ignore
                    )  # type: ignore
                    logger.info(f"输入图片 {i.data['url']}")
                elif config.marshoai_enable_support_image_tip:
                    await UniMessage(
                        "*此模型不支持图片处理或管理员未启用此模型的图片支持。图片将被忽略。"
                    ).send()
        return usermsg  # type: ignore

    async def handle_single_chat(
        self,
        user_message: Union[str, list],
        model_name: str,
        tools: list,
        with_context: bool = True,
    ) -> ChatCompletion:
        """
        处理单条聊天
        """
        backup_context = await get_backup_context(self.target.id, self.target.private)
        if backup_context:
            self.context.set_context(
                backup_context, self.target.id, self.target.private
            )  # 加载历史记录
            logger.info(f"已恢复会话 {self.target.id} 的上下文备份~")
        context_msg = (
            get_prompt(model_name)
            + (self.context.build(self.target.id, self.target.private))
            if with_context
            else ""
        )
        response = await make_chat_openai(
            client=self.client,
            msg=context_msg + [UserMessage(content=user_message).as_dict()],  # type: ignore
            model_name=model_name,
            tools=tools,
        )
        return response
