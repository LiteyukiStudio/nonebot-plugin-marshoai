# Marsho 的类实例以及全局变量
from nonebot import get_driver
from openai import AsyncOpenAI

from .config import config
from .models import MarshoContext, MarshoTools

driver = get_driver()

command_start = driver.config.command_start
model_name = config.marshoai_default_model
context = MarshoContext()
tools = MarshoTools()
token = config.marshoai_token
endpoint = config.marshoai_azure_endpoint
# client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(token))
client = AsyncOpenAI(base_url=endpoint, api_key=token)
target_list: list[list] = []  # 记录需保存历史上下文的列表
