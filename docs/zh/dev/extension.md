---
order: 2
---

# 扩展开发

## 说明

扩展分为两类，一类为插件，一类为工具。

- 插件
- 工具(由于开发的不便利性，已经停止维护，未来可能会放弃支持，如有需求请看README中的内容，我们不推荐再使用此功能)

## 插件

为什么要有插件呢，插件可以编写function call供AI调用，语言大模型本身不具备一些信息获取能力，可以使用该功能进行扩展。

可以借助这个功能实现获取天气、获取股票信息、获取新闻等等，然后将这些信息传递给AI，AI可以根据这些信息进行正确的整合与回答。

插件很简单，一个Python文件，一个Python包都可以是插件，插件组成也很简单：

- 元数据：包含插件的信息，如名称、版本、作者等
- function call：供AI调用的函数


:::tip
如果你编写过NoneBot插件，那么你会发现插件的编写方式和NoneBot插件的编写方式几乎一样。
:::

## 编写第一个插件

我们编写一个用于查询天气的插件，首先创建`weather.py`文件，然后编写如下内容：

```python
from nonebot_plugin_marshoai.plugin import PluginMetadata, on_function_call, String

__marsho_meta__ = PluginMetadata(
    name="天气查询",
    author="MarshoAI",
    description="一个简单的查询天气的插件"
)

@on_function_call(description="可以用于查询天气").params(
    location=String(description="地点")
)
async def weather(location: str) -> str:
    # 这里可以调用天气API查询天气，这里只是一个简单的示例
    return f"{location}的天气是晴天, 温度是25°C"
```

然后将`weather.py`文件放到`$LOCAL_STORE/plugins`目录下，重启机器人实例即可。

接下来AI会根据你的发送的提示词和`description`来决定调用函数，如`查询北京的天气`，`告诉我东京明天会下雨吗`，AI会调用`weather`函数并传递`location`参数为`北京`。

## 插件元数据

元数据是一个名为`__marsho_meta__`的全局变量，它是一个`PluginMetadata`对象，至于包含什么熟悉可以查看`PluginMetadata`类的定义或IDE提示，这里不再赘述。

## 函数调用参数

`on_function_call`装饰器用于标记一个函数为function call，`description`参数用于描述这个函数的作用，`params`方法用于定义函数的参数，`String`、`Integer`等是OpenAI API接受的参数的类型，`description`是参数的描述。这些都是给AI看的，AI会根据这些信息来调用函数。

```python
@on_function_call(description="可以用于算命").params(
    name=String(description="姓名"),
    age=Integer(description="年龄")
)
def fortune_telling(name: str, age: int) -> str:
    return f"{name}，你的年龄是{age}岁"
```

## 权限及规则

插件的调用权限和规则与NoneBot插件一样，使用Caller的permission和rule函数来设置。

```python
@on_function_call(description="在设备上执行命令").params(
    command=String(description="命令内容")
).permission(SUPERUSER).rule(RegexRule("查询(.*)的天气"))
def execute_command(command: str) -> str:
    return eval(command)
```

## 依赖注入

function call支持NoneBot2原生的会话上下文依赖注入，例如Bot、Event等

```python
@on_function_call(description="获取个人信息")
async def get_user_info(e: Event) -> str:
    return f"用户ID: {e.user_id}"

@on_function_call(description="获取机器人信息")
async def get_bot_info(b: Bot) -> str:
    return f"机器人ID: {b.self_id}"
```

## 其他

- function call支持同步和异步函数
- 本文是一个引导，要查看具体功能请查阅[插件 API 文档](./api/plugin/index)