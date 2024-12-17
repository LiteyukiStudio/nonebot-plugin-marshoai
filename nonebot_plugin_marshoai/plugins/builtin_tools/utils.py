import asyncio
from concurrent.futures import ThreadPoolExecutor

from newspaper import Article  # type: ignore
from sumy.nlp.tokenizers import Tokenizer  # type: ignore
from sumy.parsers.plaintext import PlaintextParser  # type: ignore
from sumy.summarizers.lsa import LsaSummarizer  # type: ignore

executor = ThreadPoolExecutor()


async def make_html_summary(
    html_content: str, language: str = "english", length: int = 3
) -> str:
    """使用html内容生成摘要

    Args:
        html_content (str): html内容
        language (str, optional): 语言. Defaults to "english".
        length (int, optional): 摘要长度. Defaults to 3.

    Returns:
        str: 摘要
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        executor, _make_summary, html_content, language, length
    )


def _make_summary(html_content: str, language: str, length: int) -> str:
    parser = PlaintextParser.from_string(html_content, Tokenizer(language))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, length)
    return " ".join([str(sentence) for sentence in summary])
