import random

from nonebot_plugin_marshoai.plugin import Integer, PluginMetadata, on_function_call

__marsho_meta__ = PluginMetadata(
    name="随机数生成器", author="MarshoAI", description="生成指定数量的随机数"
)


@on_function_call(description="生成随机数").params(
    count=Integer(description="随机数的数量")
)
async def generate_random_numbers(count: int) -> str:
    random_numbers = [random.randint(1, 100) for _ in range(count)]
    return f"生成的随机数为: {', '.join(map(str, random_numbers))}"


# 该插件由MarshoAI自举编写


@on_function_call(description="重载测试")
def test_reload():
    return 1
