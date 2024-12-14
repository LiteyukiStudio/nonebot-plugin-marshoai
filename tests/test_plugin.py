def example_function(num: int, text: str, is_a: bool) -> str:
    """这是一个示例描述

    Args:
        num (int): 描述整数
        text (str): 文本类型
        is_a (bool): 布尔类型

    Returns:
        str: 消息
    """
    return "-"


class TestPlugin:
    def test_get_function_info(self):
        from nonebot_plugin_marshoai.plugin import get_function_info

        func_info = get_function_info(example_function)
        print(func_info)
