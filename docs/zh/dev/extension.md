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
).permission(SUPERUSER)
def execute_command(command: str) -> str:
    return eval(command)
```

## 依赖注入

function call支持NoneBot2原生的会话上下文依赖注入

- Event 及其子类实例
- Bot   及其子类实例
- Matcher   及其子类实例
- T_State

```python
@on_function_call(description="获取个人信息")
async def get_user_info(e: Event) -> str:
    return f"用户ID: {e.user_id}"

@on_function_call(description="获取机器人信息")
async def get_bot_info(b: Bot) -> str:
    return f"机器人ID: {b.self_id}"
```

## 兼容性

插件可以编写NoneBot或者轻雪插件的内容，可作为NoneBot插件或者轻雪插件单独发布

不过，所编写功能仅会在对应的实例上加载对应的功能，如果通过marshoai加载混合插件，那么插件中NoneBot的功能将会依附于marshoai插件，
若通过NoneBot加载包含marshoai功能的NoneBot插件，那么marshoai功能将会依附于NoneBot插件。

**我们建议**：若插件中包含了NoneBot功能，仍然使用marshoai进行加载，这样更符合逻辑。若你想发布为NoneBot插件，请注意`require("nonebot_plugin_marshoai")`，这是老生常谈了。

:::tip
本质上都是动态导入和注册声明加载，运行时把这些东西塞到一起
:::

## 插件热重载

插件热重载是一个实验性功能，可以在不重启机器人的情况下更新插件

:::warning
框架无法完全消除之前插件带来的副作用，当开发测试中效果不符合预期时请重启机器人实例

为了更好地让热重载功能正常工作，尽可能使用函数式的编程风格，以减少副作用的影响
:::

将`MARSHOAI_DEVMODE`环境变量设置为`true`，然后在配置的插件目录`MARSHOAI_PLUGIN_DIRS`下开发插件，当插件发生变化时，机器人会自动变动的插件。

## AIGC 自举

:::warning
该功能为实验性功能，请注意甄别AI的行为，不要让AI执行危险的操作。
:::
function call为AI赋能，实现了文件io操作，AI可以调用function call来读取文档然后给自己编写代码，实现自举。

## 其他

- function call支持同步和异步函数
- 本文是一个引导，要查看具体功能请查阅[插件 API 文档](./api/plugin/index)
