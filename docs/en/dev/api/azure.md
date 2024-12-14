---
title: azure
---
# **Module** `nonebot_plugin_marshoai.azure`

---
### ***async func*** `at_enable()`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/azure.py#L32' target='_blank'>View on GitHub</a></summary>

```python
async def at_enable():
    return config.marshoai_at
```
</details>

### var `target_list`

- **Description**: 记录需保存历史上下文的列表

- **Default**: `[]`

---
`@add_usermsg_cmd.handle()`
### ***async func*** `add_usermsg(target: MsgTarget, arg: Message = CommandArg())`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/azure.py#L113' target='_blank'>View on GitHub</a></summary>

```python
@add_usermsg_cmd.handle()
async def add_usermsg(target: MsgTarget, arg: Message=CommandArg()):
    if (msg := arg.extract_plain_text()):
        context.append(UserMessage(content=msg).as_dict(), target.id, target.private)
        await add_usermsg_cmd.finish('已添加用户消息')
```
</details>

---
`@add_assistantmsg_cmd.handle()`
### ***async func*** `add_assistantmsg(target: MsgTarget, arg: Message = CommandArg())`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/azure.py#L120' target='_blank'>View on GitHub</a></summary>

```python
@add_assistantmsg_cmd.handle()
async def add_assistantmsg(target: MsgTarget, arg: Message=CommandArg()):
    if (msg := arg.extract_plain_text()):
        context.append(AssistantMessage(content=msg).as_dict(), target.id, target.private)
        await add_assistantmsg_cmd.finish('已添加助手消息')
```
</details>

---
`@praises_cmd.handle()`
### ***async func*** `praises()`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/azure.py#L129' target='_blank'>View on GitHub</a></summary>

```python
@praises_cmd.handle()
async def praises():
    await praises_cmd.finish(build_praises())
```
</details>

---
`@contexts_cmd.handle()`
### ***async func*** `contexts(target: MsgTarget)`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/azure.py#L135' target='_blank'>View on GitHub</a></summary>

```python
@contexts_cmd.handle()
async def contexts(target: MsgTarget):
    backup_context = await get_backup_context(target.id, target.private)
    if backup_context:
        context.set_context(backup_context, target.id, target.private)
    await contexts_cmd.finish(str(context.build(target.id, target.private)))
```
</details>

---
`@save_context_cmd.handle()`
### ***async func*** `save_context(target: MsgTarget, arg: Message = CommandArg())`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/azure.py#L143' target='_blank'>View on GitHub</a></summary>

```python
@save_context_cmd.handle()
async def save_context(target: MsgTarget, arg: Message=CommandArg()):
    contexts_data = context.build(target.id, target.private)
    if not context:
        await save_context_cmd.finish('暂无上下文可以保存')
    if (msg := arg.extract_plain_text()):
        await save_context_to_json(msg, contexts_data, 'contexts')
        await save_context_cmd.finish('已保存上下文')
```
</details>

---
`@load_context_cmd.handle()`
### ***async func*** `load_context(target: MsgTarget, arg: Message = CommandArg())`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/azure.py#L153' target='_blank'>View on GitHub</a></summary>

```python
@load_context_cmd.handle()
async def load_context(target: MsgTarget, arg: Message=CommandArg()):
    if (msg := arg.extract_plain_text()):
        await get_backup_context(target.id, target.private)
        context.set_context(await load_context_from_json(msg, 'contexts'), target.id, target.private)
        await load_context_cmd.finish('已加载并覆盖上下文')
```
</details>

---
`@resetmem_cmd.handle()`
### ***async func*** `resetmem(target: MsgTarget)`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/azure.py#L165' target='_blank'>View on GitHub</a></summary>

```python
@resetmem_cmd.handle()
async def resetmem(target: MsgTarget):
    if [target.id, target.private] not in target_list:
        target_list.append([target.id, target.private])
    context.reset(target.id, target.private)
    await resetmem_cmd.finish('上下文已重置')
```
</details>

---
`@changemodel_cmd.handle()`
### ***async func*** `changemodel(arg: Message = CommandArg())`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/azure.py#L173' target='_blank'>View on GitHub</a></summary>

```python
@changemodel_cmd.handle()
async def changemodel(arg: Message=CommandArg()):
    global model_name
    if (model := arg.extract_plain_text()):
        model_name = model
        await changemodel_cmd.finish('已切换')
```
</details>

---
`@nickname_cmd.handle()`
### ***async func*** `nickname(event: Event, name = None)`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/azure.py#L181' target='_blank'>View on GitHub</a></summary>

```python
@nickname_cmd.handle()
async def nickname(event: Event, name=None):
    nicknames = await get_nicknames()
    user_id = event.get_user_id()
    if not name:
        if user_id not in nicknames:
            await nickname_cmd.finish('你未设置昵称')
        await nickname_cmd.finish('你的昵称为：' + str(nicknames[user_id]))
    if name == 'reset':
        await set_nickname(user_id, '')
        await nickname_cmd.finish('已重置昵称')
    else:
        await set_nickname(user_id, name)
        await nickname_cmd.finish('已设置昵称为：' + name)
```
</details>

---
`@refresh_data_cmd.handle()`
### ***async func*** `refresh_data()`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/azure.py#L197' target='_blank'>View on GitHub</a></summary>

```python
@refresh_data_cmd.handle()
async def refresh_data():
    await refresh_nickname_json()
    await refresh_praises_json()
    await refresh_data_cmd.finish('已刷新数据')
```
</details>

---
`@marsho_at.handle()`
`@marsho_cmd.handle()`
### ***async func*** `marsho(target: MsgTarget, event: Event, text: Optional[UniMsg] = None)`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/azure.py#L205' target='_blank'>View on GitHub</a></summary>

```python
@marsho_at.handle()
@marsho_cmd.handle()
async def marsho(target: MsgTarget, event: Event, text: Optional[UniMsg]=None):
    global target_list
    if event.get_message().extract_plain_text() and (not text and event.get_message().extract_plain_text() != config.marshoai_default_name):
        text = event.get_message()
    if not text:
        await UniMessage(metadata.usage + '\n当前使用的模型：' + model_name).send()
        await marsho_cmd.finish(INTRODUCTION)
    try:
        user_id = event.get_user_id()
        nicknames = await get_nicknames()
        user_nickname = nicknames.get(user_id, '')
        if user_nickname != '':
            nickname_prompt = f'\n*此消息的说话者:{user_nickname}*'
        else:
            nickname_prompt = ''
            if config.marshoai_enable_nickname_tip:
                await UniMessage("*你未设置自己的昵称。推荐使用'nickname [昵称]'命令设置昵称来获得个性化(可能）回答。").send()
        is_support_image_model = model_name.lower() in SUPPORT_IMAGE_MODELS + config.marshoai_additional_image_models
        is_reasoning_model = model_name.lower() in REASONING_MODELS
        usermsg = [] if is_support_image_model else ''
        for i in text:
            if i.type == 'text':
                if is_support_image_model:
                    usermsg += [TextContentItem(text=i.data['text'] + nickname_prompt)]
                else:
                    usermsg += str(i.data['text'] + nickname_prompt)
            elif i.type == 'image':
                if is_support_image_model:
                    usermsg.append(ImageContentItem(image_url=ImageUrl(url=str(await get_image_b64(i.data['url'])))))
                elif config.marshoai_enable_support_image_tip:
                    await UniMessage('*此模型不支持图片处理。').send()
        backup_context = await get_backup_context(target.id, target.private)
        if backup_context:
            context.set_context(backup_context, target.id, target.private)
            logger.info(f'已恢复会话 {target.id} 的上下文备份~')
        context_msg = context.build(target.id, target.private)
        if not is_reasoning_model:
            context_msg = [get_prompt()] + context_msg
        response = await make_chat(client=client, model_name=model_name, msg=context_msg + [UserMessage(content=usermsg)], tools=tools.get_tools_list())
        choice = response.choices[0]
        if choice['finish_reason'] == CompletionsFinishReason.STOPPED:
            context.append(UserMessage(content=usermsg).as_dict(), target.id, target.private)
            context.append(choice.message.as_dict(), target.id, target.private)
            if [target.id, target.private] not in target_list:
                target_list.append([target.id, target.private])
            if config.marshoai_enable_richtext_parse:
                await (await parse_richtext(str(choice.message.content))).send(reply_to=True)
            else:
                await UniMessage(str(choice.message.content)).send(reply_to=True)
        elif choice['finish_reason'] == CompletionsFinishReason.CONTENT_FILTERED:
            await UniMessage('*已被内容过滤器过滤。请调整聊天内容后重试。').send(reply_to=True)
            return
        elif choice['finish_reason'] == CompletionsFinishReason.TOOL_CALLS:
            tool_msg = []
            while choice.message.tool_calls != None:
                tool_msg.append(AssistantMessage(tool_calls=response.choices[0].message.tool_calls))
                for tool_call in choice.message.tool_calls:
                    if isinstance(tool_call, ChatCompletionsToolCall):
                        function_args = json.loads(tool_call.function.arguments.replace("'", '"'))
                        logger.info(f'调用函数 {tool_call.function.name} ,参数为 {function_args}')
                        await UniMessage(f'调用函数 {tool_call.function.name} ,参数为 {function_args}').send()
                        func_return = await tools.call(tool_call.function.name, function_args)
                        tool_msg.append(ToolMessage(tool_call_id=tool_call.id, content=func_return))
                response = await make_chat(client=client, model_name=model_name, msg=context_msg + [UserMessage(content=usermsg)] + tool_msg, tools=tools.get_tools_list())
                choice = response.choices[0]
            if choice['finish_reason'] == CompletionsFinishReason.STOPPED:
                context.append(UserMessage(content=usermsg).as_dict(), target.id, target.private)
                context.append(choice.message.as_dict(), target.id, target.private)
                if config.marshoai_enable_richtext_parse:
                    await (await parse_richtext(str(choice.message.content))).send(reply_to=True)
                else:
                    await UniMessage(str(choice.message.content)).send(reply_to=True)
            else:
                await marsho_cmd.finish(f'意外的完成原因:{choice['finish_reason']}')
        else:
            await marsho_cmd.finish(f'意外的完成原因:{choice['finish_reason']}')
    except Exception as e:
        await UniMessage(str(e) + suggest_solution(str(e))).send()
        traceback.print_exc()
        return
```
</details>

---
`@driver.on_shutdown`
### ***async func*** `auto_backup_context()`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/azure.py#L392' target='_blank'>View on GitHub</a></summary>

```python
@driver.on_shutdown
async def auto_backup_context():
    for target_info in target_list:
        target_id, target_private = target_info
        contexts_data = context.build(target_id, target_private)
        if target_private:
            target_uid = 'private_' + target_id
        else:
            target_uid = 'group_' + target_id
        await save_context_to_json(f'back_up_context_{target_uid}', contexts_data, 'contexts/backup')
        logger.info(f'已保存会话 {target_id} 的上下文备份，将在下次对话时恢复~')
```
</details>

---
`@poke_notify.handle()`
### ***async func*** `poke(event: Event)`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/azure.py#L363' target='_blank'>View on GitHub</a></summary>

```python
@poke_notify.handle()
async def poke(event: Event):
    user_id = event.get_user_id()
    nicknames = await get_nicknames()
    user_nickname = nicknames.get(user_id, '')
    try:
        if config.marshoai_poke_suffix != '':
            response = await make_chat(client=client, model_name=model_name, msg=[get_prompt(), UserMessage(content=f'*{user_nickname}{config.marshoai_poke_suffix}')])
            choice = response.choices[0]
            if choice['finish_reason'] == CompletionsFinishReason.STOPPED:
                await UniMessage(' ' + str(choice.message.content)).send(at_sender=True)
    except Exception as e:
        await UniMessage(str(e) + suggest_solution(str(e))).send()
        traceback.print_exc()
        return
```
</details>

### var `text`

- **Description**: type: ignore

- **Default**: `event.get_message()`

