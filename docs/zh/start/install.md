---
title: 安装
---

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-marshoai

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-marshoai

</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-marshoai

</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-marshoai

</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-marshoai

</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_marshoai"]

</details>

## 🤖 获取 token(GitHub Models)

- 新建一个[personal access token](https://github.com/settings/tokens/new)，**不需要给予任何权限**。
- 将新建的 token 复制，添加到`.env`文件中的`marshoai_token`配置项中。

## 🎉 使用

发送`marsho`指令可以获取使用说明(若在配置中自定义了指令前缀请使用自定义的指令前缀)。

#### 👉 戳一戳

当 nonebot 连接到支持的 OneBot v11 实现端时，可以接收头像双击戳一戳消息并进行响应。详见`MARSHOAI_POKE_SUFFIX`配置项。

## 🛠️ ~~小棉工具~~（已弃用）

小棉工具(MarshoTools)是`v0.5.0`版本的新增功能，支持加载外部函数库来为 Marsho 提供 Function Call 功能。

## 🧩 小棉插件

小棉插件是`v1.0.0`的新增功能，替代旧的小棉工具功能。[使用文档](https://marsho.liteyuki.icu/dev/extension)

## 👍 夸赞名单

夸赞名单存储于插件数据目录下的`praises.json`里（该目录路径会在 Bot 启动时输出到日志），当配置项为`true`
时发起一次聊天后自动生成，包含人物名字与人物优点两个基本数据。
存储于其中的人物会被 Marsho “认识”和“喜欢”。
其结构类似于：

```json
{
  "like": [
    {
      "name": "Asankilp",
      "advantages": "赋予了Marsho猫娘人格，使用vim与vscode为Marsho写了许多代码，使Marsho更加可爱"
    },
    {
      "name": "神羽(snowykami)",
      "advantages": "人脉很广，经常找小伙伴们开银趴，很会写后端代码"
    },
    ...
  ]
}
```

## ⚙️ 可配置项

在 nonebot2 项目的`.env`文件中添加下表中的配置

#### 插件行为

| 配置项                      | 类型     | 默认值     | 说明               |
| ------------------------ | ------ | ------- | ---------------- |
| MARSHOAI_USE_YAML_CONFIG | `bool` | `false` | 是否使用 YAML 配置文件格式 |
| MARSHOAI_DEVMODE    | `bool` | `false` | 是否启用开发者模式  |

#### Marsho 使用方式

| 配置项                   | 类型         | 默认值         | 说明                |
| --------------------- | ---------- | ----------- | ----------------- |
| MARSHOAI_DEFAULT_NAME | `str`      | `marsho`    | 调用 Marsho 默认的命令前缀 |
| MARSHOAI_ALIASES      | `set[str]` | `set{"小棉"}` | 调用 Marsho 的命令别名   |
| MARSHOAI_AT           | `bool`     | `false`     | 决定是否使用at触发   |
| MARSHOAI_MAIN_COLOUR  | `str`      | `FFAAAA`      | 主题色，部分工具和功能可用   |

#### AI 调用

| 配置项                              | 类型      | 默认值                                     | 说明                                                                                            |
| -------------------------------- | ------- | --------------------------------------- | --------------------------------------------------------------------------------------------- |
| MARSHOAI_TOKEN                   | `str`   |                                         | 调用 AI API 所需的 token                                                                           |
| MARSHOAI_DEFAULT_MODEL           | `str`   | `gpt-4o-mini`                           | Marsho 默认调用的模型                                                                                |
| MARSHOAI_PROMPT                  | `str`   | 猫娘 Marsho 人设提示词                         | Marsho 的基本系统提示词 **※部分模型(o1等)不支持系统提示词。**                                                       |
| MARSHOAI_ADDITIONAL_PROMPT       | `str`   |                                         | Marsho 的扩展系统提示词                                                                               |
| MARSHOAI_POKE_SUFFIX             | `str`   | `揉了揉你的猫耳`                               | 对 Marsho 所连接的 OneBot 用户进行双击戳一戳时，构建的聊天内容。此配置项为空字符串时，戳一戳响应功能会被禁用。例如，默认值构建的聊天内容将为`*[昵称]揉了揉你的猫耳。` |
| MARSHOAI_AZURE_ENDPOINT          | `str`   | `https://models.inference.ai.azure.com` | OpenAI 标准格式 API 端点                                                                            |
| MARSHOAI_TEMPERATURE             | `float` | `null`                                  | 推理生成多样性（温度）参数                                                                                 |
| MARSHOAI_TOP_P                   | `float` | `null`                                  | 推理核采样参数                                                                                       |
| MARSHOAI_MAX_TOKENS              | `int`   | `null`                                  | 最大生成 token 数                                                                                  |
| MARSHOAI_ADDITIONAL_IMAGE_MODELS | `list`  | `[]`                                    | 额外添加的支持图片的模型列表，例如`hunyuan-vision`                                                             |

#### 功能开关

| 配置项                               | 类型     | 默认值    | 说明                         |
| --------------------------------- | ------ | ------ | -------------------------- |
| MARSHOAI_ENABLE_SUPPORT_IMAGE_TIP | `bool` | `true` | 启用后用户发送带图请求时若模型不支持图片，则提示用户 |
| MARSHOAI_ENABLE_NICKNAME_TIP      | `bool` | `true` | 启用后用户未设置昵称时提示用户设置          |
| MARSHOAI_ENABLE_PRAISES           | `bool` | `true` | 是否启用夸赞名单功能                 |
| MARSHOAI_ENABLE_TOOLS             | `bool` | `false` | 是否启用小棉工具                   |
| MARSHOAI_ENABLE_PLUGINS             | `bool` | `true` | 是否启用小棉插件    |
| MARSHOAI_PLUGINS                | `list[str]` | `[]`   | 要从`sys.path`加载的插件的名称，例如从pypi安装的包      |
| MARSHOAI_PLUGIN_DIRS             | `list[str]` | `[]` |  插件目录路径列表       |
| MARSHOAI_LOAD_BUILTIN_TOOLS       | `bool` | `true` | 是否加载内置工具包                  |
| MARSHOAI_TOOLSET_DIR              | `list` | `[]`   |   外部工具集路径列表            |
| MARSHOAI_DISABLED_TOOLKITS        | `list` | `[]`   |  禁用的工具包包名列表           |
| MARSHOAI_ENABLE_RICHTEXT_PARSE    | `bool` | `true` |   是否启用自动解析消息（若包含图片链接则发送图片、若包含LaTeX公式则发送公式图）           |
| MARSHOAI_SINGLE_LATEX_PARSE    | `bool` | `false` |   单行公式是否渲染（当消息富文本解析启用时可用）（如果单行也渲……只能说不好看）           |

#### 开发及调试选项

| 配置项                      | 类型     | 默认值     | 说明               |
| ------------------------ | ------ | ------- | ---------------- |
| MARSHOAI_DEVMODE    | `bool` | `false` | 是否启用开发者模式  |
