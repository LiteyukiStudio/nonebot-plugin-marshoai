# 🛠️小棉工具
小棉工具(MarshoTools)是一个简单的模块加载器，允许从插件数据目录下的`tools`目录内加载数个工具包与其中定义的函数，以供 AI 模型调用。
有关 Function Call 的更多信息，请参阅[OpenAI 官方文档](https://platform.openai.com/docs/guides/function-calling)。

## ✍️ 编写工具
### 📁 目录结构
插件数据目录下的`tools`目录被称作**工具集**，其中可包含数个**工具包**，工具包与 Python 的**包**结构类似，需要在其中包含`__init__.py`文件与`tools.json`定义文件，这些文件将被用于存放以及定义编写的函数。

一个工具包的目录结构类似于：
```
tools/ # 工具集目录
└── marshoai-example/ # 工具包目录，以包名命名
    └── __init__.py # 工具模块
    └── tools.json # 函数定义文件
```
在这个目录树中：
- **工具包目录**是以`marshoai-xxxxx`命名的目录，目录名即为工具包的包名。编写工具时，应尽量采取此命名标准。
- **工具模块**可包含数个可调用的**异步**函数，可以接受入参，也可以不接受。它们的返回值数据类型应为 AI 模型受支持的类型，一般情况下`str`被大部分模型所支持。
- **函数定义文件**是让 AI 模型知道如何调用这些函数的关键。
### 编写函数
来编写一个简单的函数吧，例如一个获取天气的函数和一个获取时间的函数：
###### **\_\_init\_\_.py**
```python
from datetime import datetime

async def get_weather(location: str):
    return f"{location}的温度是114514℃。" #模拟天气返回信息

async def get_current_time():
    current_time = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
    time_prompt = f"现在的时间是{current_time}。"
    return time_prompt
```
在这个示例代码中，定义了`get_weather`和`get_current_time`两个函数，其中一个接受`str`类型的地点入参。要让 AI 模型知道这两个函数的存在以及调用的条件和方法，需要编写**函数定义文件**。
###### **tools.json**
```json
[
    {
        "type": "function",
        "function": {
            "name": "marshoai-example__get_weather", # 函数调用名称
            "description": "查询指定地点的天气。", # 对该函数的描述，需要清楚描述该函数的用途
            "parameters": {   # 定义函数的入参
                "type": "object",
                "properties": {
                    "location": { # 此处'location'即为__init__.py定义的入参名
                        "type": "string", # 该入参的数据类型
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。" # 对该入参的描述，需要清楚描述该入参应传入什么样子的内容
                    }
                }
            },
            "required": [ # 定义该函数的必需入参
                "location"
            ]
        }
    },
    {
        "type": "function",
        "function": {
            "name": "marshoai-example__get_current_time",
            "description": "获取现在的时间。",
            "parameters": {} # 该函数不需要入参，故此处为空
        }
    }
]
```
在这个文件中定义了两个已经编写好的函数，该定义文件将被输入到 AI 模型中，来让 AI 模型知道这些函数的存在与调用方法。
**函数调用名称**的命名方式比较特别。以获取天气的函数为例，它的函数调用名称`marshoai-example__get_weather`包含三个信息：
- 前面的**marshoai-example**即为该函数所在工具包的**包名**。
- 后面的**get_weather**是这个函数在代码里的名称。
- 中间的两个下划线是用于分割这两个信息的分隔符。

使用这种命名方式，是为了兼容更多的 OpenAI 标准格式 API。因此，在给工具包和函数取名时，不要使用带有两个下划线的名称。
### 测试函数
在编写完工具后，启动 Bot，Nonebot 的日志应当会输出工具包的加载信息。
以下是测试示例：
```
> marsho 深圳天气怎么样
深圳的天气显示温度是114514°C，真是不可思议呢！这一定是个误报吧~(≧▽≦) 希望你那里有个好天气哦！
> marsho 分别告诉我下北泽，杭州，苏州的天气
下北泽、杭州和苏州的天气都显示温度为114514°C呢！这么奇怪的温度，一定是个误报吧~(≧▽≦)

如果要查看真实的天气情况，建议查看专业天气预报哦~
> marsho 现在几点了
现在的时间是2024年11月23日，21点05分哦~(*^ω^) 你准备做些什么呢？
```
