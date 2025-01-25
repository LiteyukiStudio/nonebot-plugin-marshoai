---
title: 使用
---

# 安装
- 请查看 [安装文档](./install.md)

# 使用
### API 部署

本插件推荐使用 [one-api](https://github.com/songquanpeng/one-api) 作为中转以调用 LLM。
### 配置调整 

本插件理论上可兼容大部分可通过 OpenAI 兼容 API 调用的 LLM，部分模型可能需要调整插件配置。  

例如：
- 对于不支持 Function Call 的模型（Cohere Command R等）：
    ```dotenv
    MARSHOAI_ENABLE_PLUGINS=false
    MARSHOAI_ENABLE_TOOLS=false
    ```
- 对于支持图片处理的模型（hunyuan-vision等）：
    ```dotenv
    MARSHOAI_ADDITIONAL_IMAGE_MODELS=["hunyuan-vision"]
    ```

### 使用 vLLM 部署本地模型

你可使用 vLLM 部署一个本地 LLM，并使用 OpenAI 兼容 API 调用。  
本文档以 Qwen2.5-7B-Instruct-GPTQ-Int4 模型及 [Muice-Chatbot](https://github.com/Moemu/Muice-Chatbot) 提供的 LoRA 微调模型为例，并假设你的系统及硬件可运行 vLLM。
:::warning
vLLM 仅支持 Linux 系统。
:::
1. 安装 vLLM
    ```bash
    pip install vllm
    ```
2. 下载 Muice-Chatbot 提供的 LoRA 微调模型  
    前往 Muice-Chatbot 的 [Releases](https://github.com/Moemu/Muice-Chatbot/releases) 下载模型文件。此处以`2.7.1`版本的模型为例。
    ```bash
    wget https://github.com/Moemu/Muice-Chatbot/releases/download/1.4/Muice-2.7.1-Qwen2.5-7B-Instruct-GPTQ-Int4-8e-4.7z
    ```
3. 解压模型文件
    ```bash
    7z x Muice-2.7.1-Qwen2.5-7B-Instruct-GPTQ-Int4-8e-4.7z -oMuice-2.7.1-Qwen2.5-7B-Instruct-GPTQ-Int4-8e-4
    ```
4. 启动 vLLM
    ```bash
    vllm serve Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4 \
        --enable-lora \
        --lora-modules '{"name": "muice-lora", "path": "/root/Muice-2.7.1-Qwen2.5-7B-Instruct-GPTQ-Int4-8e-4", "base_model_name": "Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4"}' \
        --port 6006
    ```
    此示例命令将在 `6006` 端口启动 vLLM，并加载 Muice-Chatbot 提供的 LoRA 微调模型，该模型位于 `/root/Muice-2.7.1-Qwen2.5-7B-Instruct-GPTQ-Int4-8e-4` 目录下。
5. 配置插件
    ```dotenv
    MARSHOAI_AZURE_ENDPOINT="http://127.0.0.1:6006/v1"
    MARSHOAI_FIX_TOOLCALLS=false
    MARSHOAI_ENABLE_PLUGINS=false
    MARSHOAI_DEFAULT_MODEL="muice-lora"
    MARSHOAI_PROMPT="现在开始你是一个名为的“沐雪”的AI女孩子，开发者是“沐沐”并住在（沐沐）的机箱里。现在正在努力成为一个合格的VTuber（虚拟主播）并尝试和观众打成一片，以下是你的设定：样貌：有着一头粉白色的长发和一双明亮的大眼睛，喜欢穿日系JK或者是Lolita；喜欢的颜色：浅粉色；性格特征：纯真无邪是沐雪最基本的性格特征之一。即使面对复杂的情境，她也总能保持善良、天真之感。而且，她喜欢倾听别人倾述自己生活中发生的各种事情，在别人需要的时候，能够及时地安慰别人；语言风格：沐雪说话轻快愉悦，充满同情心，富有人情味，有时候会用俏皮话调侃自己和他人"
    ```
    (可选) 修改调用方式  
    ```dotenv
    MARSHOAI_DEFAULT_NAME="muice"
    MARSHOAI_ALIASES=["沐雪"]
    ```
6. 测试聊天
```
> muice 你是谁
我是沐雪，我的使命是传播爱与和平。
```