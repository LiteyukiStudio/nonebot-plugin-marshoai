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
:::warning
GitHub Models API comes with significant limitations and is therefore not recommended for use. For better alternatives, it's suggested to adjust the configuration `MARSHOAI_AZURE_ENDPOINT` to use other service providers' models instead.
:::
## 🎉 Usage

End `marsho` in order to get direction for use(If you configured the custom command, please use the configured one).

#### 👉 Double click avatar

When nonebot linked to OneBot v11 adapter, can recieve double click and response to it. More detail in the `MARSHOAI_POKE_SUFFIX` option.

## 🛠️ ~~MarshoTools~~ (Deprecated)

MarshoTools is a feature added in `v0.5.0`, support loading external function library to provide Function Call for Marsho. 

## 🧩 Marsho Plugin
Marsho Plugin is a feature added in `v1.0.0`, replacing the old MarshoTools feature. [Documentation](https://marsho.liteyuki.icu/dev/extension)

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
| MARSHOAI_DEVMODE  | `bool` | `true` | Turn on Development Mode or not |

#### Marsho usage

| Option                | Type       | Default     | Description          |
| --------------------- | ---------- | ----------- | ----------------- |
| MARSHOAI_DEFAULT_NAME | `str`      | `marsho`    | Command to call Marsho |
| MARSHOAI_ALIASES      | `set[str]` | `list["小棉"]` | Other name(Alias) to call Marsho |
| MARSHOAI_AT           | `bool`     | `false`     | Call by @ or not |
| MARSHOAI_MAIN_COLOUR   |  `str`    | `FFAAAA`    | Theme color, used by some tools and features    |

#### AI call

| Option                           | Type    | Default                                 | Description                                                                                           |
| -------------------------------- | ------- | --------------------------------------- | --------------------------------------------------------------------------------------------- |
| MARSHOAI_TOKEN                   | `str`   |                                         | The token needed to call AI API |
| MARSHOAI_DEFAULT_MODEL           | `str`   | `gpt-4o-mini`                           | The default model of Marsho                                                                        |
| MARSHOAI_PROMPT                  | `str`   | Catgirl Marsho's character prompt                    | Marsho's basic system prompt **※Some models(o1 and so on) don't support it**                                                       |
| MARSHOAI_ADDITIONAL_PROMPT       | `str`   |                                         | Marsho's external system prompt                                                                              |
| MARSHOAI_ENFORCE_NICKNAME        | `bool`  | `true`                                  | Enforce user to set nickname or not                                                               |
| MARSHOAI_POKE_SUFFIX             | `str`   | `揉了揉你的猫耳`                               | When double click Marsho who connected to OneBot adapter, the chat content. When it's empty string, double click function is off. Such as, the default content is `*[昵称]揉了揉你的猫耳。` |
| MARSHOAI_AZURE_ENDPOINT          | `str`   | `https://models.inference.ai.azure.com` | OpenAI standard API                                                                            |
| MARSHOAI_TEMPERATURE             | `float` | `null`                                  | temperature parameter                                                                         |
| MARSHOAI_TOP_P                   | `float` | `null`                                  | Nucleus Sampling parameter                                                                       |
| MARSHOAI_MAX_TOKENS              | `int`   | `null`                                  | Max token number                                                                                |
| MARSHOAI_ADDITIONAL_IMAGE_MODELS | `list`  | `[]`                                    | External image-support model list, such as `hunyuan-vision`                                                 |
| MARSHOAI_NICKNAME_LIMIT          | `int`   | `16`                                    | Limit for nickname length |
| MARSHOAI_FIX_TOOLCALLS           | `bool`  | `true`                                  | Fix tool calls or not |

#### Feature Switches

| Option                            | Type   | Default | Description                        |
| --------------------------------- | ------ | ------ | -------------------------- |
| MARSHOAI_ENABLE_SUPPORT_IMAGE_TIP | `bool` | `true` | When on, if user send request with photo and model don't support that, remind the user |
| MARSHOAI_ENABLE_NICKNAME_TIP      | `bool` | `true` | When on, if user haven't set username, remind user to set       |
| MARSHOAI_ENABLE_PRAISES           | `bool` | `true` | Turn on Praise list or not           |
| MARSHOAI_ENABLE_TOOLS             | `bool` | `false` | Turn on Marsho Tools or not           |
| MARSHOAI_ENABLE_PLUGINS             | `bool` | `true` | Turn on Marsho Plugins or not           
| MARSHOAI_PLUGIN_DIRS             | `list[str]` | `[]` |  List of plugins directory        |
| MARSHOAI_LOAD_BUILTIN_TOOLS       | `bool` | `true` | Loading the built-in toolkit or not |
| MARSHOAI_TOOLSET_DIR              | `list` | `[]`   | List of external toolset directory  |
| MARSHOAI_DISABLED_TOOLKITS        | `list` | `[]`   |  List of disabled toolkits' name     |
| MARSHOAI_ENABLE_RICHTEXT_PARSE    | `bool` | `true` | Turn on auto parse rich text feature(including image, LaTeX equation)  |
| MARSHOAI_SINGLE_LATEX_PARSE       | `bool` | `false`| Render single-line equation or not    |
