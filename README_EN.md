<!--suppress LongLine -->
<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://raw.githubusercontent.com/LiteyukiStudio/nonebot-plugin-marshoai/refs/heads/main/resources/marsho-new.svg" width="800" height="430" alt="NoneBotPluginLogo"></a>
  <br>
</div>

<div align="center">

# nonebot-plugin-marshoai

_✨ A chat bot plugin which use OpenAI standard API ✨_

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/LiteyukiStudio/nonebot-plugin-marshoai.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-marshoai">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-marshoai.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

## 📖 Indroduction

A plugin made by call OpenAI standard API(Such as GitHub Models API) 

Plugin internally installed the catgirl character of Marsho, is able to have a cute conversation!

*Who don't like a cute catgirl with fast answer speed？*  

**Support for adapters other than OneBot and non-Github Models APIs is not fully verified.**

[Melobot implementation](https://github.com/LiteyukiStudio/marshoai-melo)

## 🐱 Character setting

#### Basic information

- Name : Marsho
- Birthday : September 6th

#### Hobbies

- 🌞 Melt in sunshine
- 🤱 Coquetry~ who don't like that~
- 🍫 Eating snacks! Meat is yummy!
- 🐾 Play! I like play with friends!

## 💿 Install

<details open>
<summary>Install with nb-cli</summary>
  
Open shell under the root directory of nonebot2, input the command below.

    nb plugin install nonebot-plugin-marshoai

</details>

<details>
<summary>Install with pack manager</summary>
  
Open shell under the plugin directory of nonebot2, input corresponding command according to your pack manager.

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

Open the `pyproject.toml` file under nonebot2's root directory, Add to`[tool.nonebot]`.

    plugins = ["nonebot_plugin_marshoai"]

</details>

## 🤖 Get token(GitHub Models)

- Create new [personal access token](https://github.com/settings/tokens/new)，**Don't need any permissions**.
- Copy the new token, add to the `.env` file's `marshoai_token` option.

## 🎉 Usage

End `marsho` in order to get direction for use(If you configured the custom command, please use the configured one).

#### 👉 Double click avatar

When nonebot linked to OneBot v11 adapter, can recieve double click and response to it. More detail in the `MARSHOAI_POKE_SUFFIX` option.

## 🛠️ MarshoTools

MarshoTools is a feature added in `v0.5.0`, support loading external function library to provide Function Call for Marsho. [Documentation](./README_TOOLS_EN.md)  

## 👍 Praise list

Praise list stored in the `praises.json` in plugin directory（This directory will putput to log when Bot start), it'll automatically generate when option is `true`, include character name and advantage two basic data.

The character stored in it would be “know” and “like” by Marsho.

It's structure is similar to:

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

## ⚙️ Configurable options

Add options in the `.env` file from the diagram below in nonebot2 project.

#### plugin behaviour

| Option                   | Type   | Default | Description         |
| ------------------------ | ------ | ------- | ---------------- |
| MARSHOAI_USE_YAML_CONFIG | `bool` | `false` | Use YAML config format |

#### Marsho usage

| Option                | Type       | Default     | Description          |
| --------------------- | ---------- | ----------- | ----------------- |
| MARSHOAI_DEFAULT_NAME | `str`      | `marsho`    | Command to call Marsho |
| MARSHOAI_ALIASES      | `set[str]` | `set{"Marsho"}` | Other name(Alias) to call Marsho |
| MARSHOAI_AT           | `bool`     | `false`     | Call by @ or not |

#### AI call

| Option                           | Type    | Default                                 | Description                                                                                           |
| -------------------------------- | ------- | --------------------------------------- | --------------------------------------------------------------------------------------------- |
| MARSHOAI_TOKEN                   | `str`   |                                         | The token needed to call AI API |
| MARSHOAI_DEFAULT_MODEL           | `str`   | `gpt-4o-mini`                           | The default model of Marsho                                                                        |
| MARSHOAI_PROMPT                  | `str`   | Catgirl Marsho's character prompt                    | Marsho's basic system prompt **※Some models(o1 and so on) don't support it**                                                       |
| MARSHOAI_ADDITIONAL_PROMPT       | `str`   |                                         | Marsho's external system prompt                                                                              |
| MARSHOAI_POKE_SUFFIX             | `str`   | `揉了揉你的猫耳`                               | When double click Marsho who connected to OneBot adapter, the chat content. When it's empty string, double click function is off. Such as, the default content is `*[昵称]揉了揉你的猫耳。` |
| MARSHOAI_AZURE_ENDPOINT          | `str`   | `https://models.inference.ai.azure.com` | OpenAI standard API                                                                            |
| MARSHOAI_TEMPERATURE             | `float` | `null`                                  | temperature parameter                                                                         |
| MARSHOAI_TOP_P                   | `float` | `null`                                  | Nucleus Sampling parameter                                                                       |
| MARSHOAI_MAX_TOKENS              | `int`   | `null`                                  | Max token number                                                                                |
| MARSHOAI_ADDITIONAL_IMAGE_MODELS | `list`  | `[]`                                    | External image-support model list, such as `hunyuan-vision`                                                 |

#### Feature Switches

| Option                            | Type   | Default | Description                        |
| --------------------------------- | ------ | ------ | -------------------------- |
| MARSHOAI_ENABLE_SUPPORT_IMAGE_TIP | `bool` | `true` | When on, if user send request with photo and model don't support that, remind the user |
| MARSHOAI_ENABLE_NICKNAME_TIP      | `bool` | `true` | When on, if user haven't set username, remind user to set       |
| MARSHOAI_ENABLE_PRAISES           | `bool` | `true` | Turn on Praise list or not           |
| MARSHOAI_ENABLE_TOOLS             | `bool` | `true` | Turn on Marsho Tools or not           |
| MARSHOAI_LOAD_BUILTIN_TOOLS       | `bool` | `true` | Loading the built-in tool pack or not |


## ❤ Thanks&Copyright

"Marsho" logo contributed by [@Asankilp](https://github.com/Asankilp),
licensed under [CC BY-NC-SA 4.0](http://creativecommons.org/licenses/by-nc-sa/4.0/) lisense.

"nonebot-plugin-marshoai" is licensed under [MIT](./LICENSE) license.

## 🕊️ TODO

- [x] [Melobot](https://github.com/Meloland/melobot) implementation
- [x] Congize chat initiator(know who are chatting with Marsho) (Initially implement)
- [ ] Optimize API (Not only GitHub Models）
- [ ] Persistent storage context by database
