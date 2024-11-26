# 🛠️MarshoTools
Marsho is a simple module loader. It allows to load kits and its function from `tools` in plugin directory, for AI to use.
More information for Function Call, please refr to [OpenAI Offical Documentation](https://platform.openai.com/docs/guides/function-calling)

## ✍️ Writing Tools
### 📁 Directory Structure
`tools` in plugin directory is called **Toolset**. It contains many **Toolkit**, Toolkit is similar with **Packages** in Python in structure. It need `__init__.py` file and `tools.json` definition file in it. They are used to store and define functions.

A directory structure of Toolkit:
```
tools/ # Toolset Directory
└── marshoai-example/ # Toolkit Directory, Named as Packages' name
    └── __init__.py # Tool Module
    └── tools.json # Function Definition File
```
In this directory tree:
- **Toolset Directory** is named as `marshoai-xxxxx`, its name is the name of Toolset. Please follow this naming standard.
- ***Tool Module* could contain many callable **Asynchronous** function, it could have parameters or be parameterless and the return value should be supported by AI model. Generally speaking, the `str` type is accepted to most model.
- **Function Definition File** is for AI model to know how to call these function.
### Function Writing
Let's write a function for getting the weather and one for getting time.
###### **\_\_init\_\_.py**
```python
from datetime import datetime

async def get_weather(location: str):
    return f"The temperature of {location} is 114514℃。" #To simulate the return value of weather.

async def get_current_time():
    current_time = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
    time_prompt = f"Now is {current_time}。"
    return time_prompt
```
In this example, we define two functions, `get_weather` and `get_current_time`. The former accepts a `str` typed parameter. Let AI to know the existence of these funxtions, you shuold write **Function Definition File**
###### **tools.json**
```json
[
    {
        "type": "function",
        "function": {
            "name": "marshoai-example__get_weather", # Function Call Name
            "description": "Get the weather of a specified locatin.", # Description, it need to descripte the usage of this Functin
            "parameters": {   # Define the parameters
                "type": "object",
                "properties": {
                    "location": { # 'location' is the name that _init__.py had defined.
                        "type": "string", # the Type of patameters
                        "description": "City or district. Such as Beijing, Hangzhou, Yuhang District" # Description，it need to descripte the type or example of Actual Parameter
                    }
                }
            },
            "required": [ # Define the Required Parameters
                "location"
            ]
        }
    },
    {
        "type": "function",
        "function": {
            "name": "marshoai-example__get_current_time",
            "description": "Get time",
            "parameters": {} # No parameter requried, so it is blanked
        }
    }
]
```
In this file, we defined tow function. This Function Definition File will be typed into AI model, for letting AI to know when and how to call these function.
**Function Call Name** is specific required. Using weather-getting as an example, this Function Call Name, `marshoai-example__get_weather`, contain these information.
- **marshoai-example** is the name of its Toolkit.
- **get_weather** is the name of function.
- Two **underscores** are used as a separator.

Using this Naming Standard, it could be compatible with more APIs in the standard format of OpenAI. So don't use two underscores as the name of Toolkit or Function.
### Function Testing
After developing the Tools, start the Bot. There loading information of Toolkit in Nonebot Logs.
This is the test example:
```
> marsho What's the weather like in Shenzhen?
Meow! The temperature in Shenzhen is currently an astonishing 114514°C! That's super hot! Make sure to keep cool and stay hydrated! 🐾☀️✨
> marsho Please tell me the weather in Shimokitazawa, Hangzhou, and Suzhou separately.
Meow! Here's the weather for each place:

- Shimokitazawa: The temperature is 114514°C.
- Hangzhou: The temperature is also 114514°C.
- Suzhou: The temperature is again 114514°C.

That's super hot everywhere! Please stay cool and take care! 🐾☀️✨
> marsho What time is it now?
Meow! The current time is 1:15 PM on November 26, 2024. 🐾✨
```
