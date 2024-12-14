---
title: hunyuan
---
# **模块** `nonebot_plugin_marshoai.hunyuan`

---
`@genimage_cmd.handle()`
### ***async func*** `genimage(event: Event, prompt = None)`


<details>
<summary> <b>源代码</b> 或 <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/hunyuan.py#L29' target='_blank'>在GitHub上查看</a></summary>

```python
@genimage_cmd.handle()
async def genimage(event: Event, prompt=None):
    if not prompt:
        await genimage_cmd.finish('无提示词')
    try:
        result = generate_image(prompt)
        url = json.loads(result)['ResultImage']
        await UniMessage.image(url=url).send()
    except Exception as e:
        traceback.print_exc()
```
</details>

