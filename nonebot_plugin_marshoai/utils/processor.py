from nonebot.log import logger
from openai import AsyncStream
from openai.types.chat import ChatCompletion, ChatCompletionChunk, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice


async def process_chat_stream(
    stream: AsyncStream[ChatCompletionChunk],
) -> ChatCompletion:
    reasoning_contents = ""
    answer_contents = ""
    last_chunk = None
    is_first_token_appeared = False
    is_answering = False
    async for chunk in stream:
        last_chunk = chunk
        # print(chunk)
        if not is_first_token_appeared:
            logger.info(f"{chunk.id}: 第一个 token 已出现")
            is_first_token_appeared = True
        if not chunk.choices:
            logger.info("Usage:", chunk.usage)
        else:
            delta = chunk.choices[0].delta
            if (
                hasattr(delta, "reasoning_content")
                and delta.reasoning_content is not None
            ):
                reasoning_contents += delta.reasoning_content
            else:
                if not is_answering:
                    logger.info(
                        f"{chunk.id}: 思维链已输出完毕或无 reasoning_content 字段输出"
                    )
                    is_answering = True
                if delta.content is not None:
                    answer_contents += delta.content
    # print(last_chunk)
    # 创建新的 ChatCompletion 对象
    if last_chunk and last_chunk.choices:
        message = ChatCompletionMessage(
            content=answer_contents,
            role="assistant",
            tool_calls=last_chunk.choices[0].delta.tool_calls,  # type: ignore
        )
        if reasoning_contents != "":
            setattr(message, "reasoning_content", reasoning_contents)
        choice = Choice(
            finish_reason=last_chunk.choices[0].finish_reason,  # type: ignore
            index=last_chunk.choices[0].index,
            message=message,
        )
        return ChatCompletion(
            id=last_chunk.id,
            choices=[choice],
            created=last_chunk.created,
            model=last_chunk.model,
            system_fingerprint=last_chunk.system_fingerprint,
            object="chat.completion",
            usage=last_chunk.usage,
        )
    else:
        return ChatCompletion(
            id="",
            choices=[],
            created=0,
            model="",
            system_fingerprint="",
            object="chat.completion",
            usage=None,
        )


async def process_completion_to_details(completion: ChatCompletion) -> str:
    usage_text = ""
    usage = completion.usage
    if usage is None:
        usage_text = "无"
    else:
        usage_text = str(usage)

    details_text = f"""=========消息详情=========
    模型: {completion.model}
    消息 ID: {completion.id}
    用量信息: {usage_text}"""
    # print(details_text)
    return details_text
