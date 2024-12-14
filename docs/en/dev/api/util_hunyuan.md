---
title: util_hunyuan
---
# **Module** `nonebot_plugin_marshoai.util_hunyuan`

---
### ***func*** `generate_image(prompt: str)`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/util_hunyuan.py#L16' target='_blank'>View on GitHub</a></summary>

```python
def generate_image(prompt: str):
    cred = credential.Credential(config.marshoai_tencent_secretid, config.marshoai_tencent_secretkey)
    httpProfile = HttpProfile()
    httpProfile.endpoint = 'hunyuan.tencentcloudapi.com'
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = hunyuan_client.HunyuanClient(cred, 'ap-guangzhou', clientProfile)
    req = models.TextToImageLiteRequest()
    params = {'Prompt': prompt, 'RspImgType': 'url', 'Resolution': '1080:1920'}
    req.from_json_string(json.dumps(params))
    resp = client.TextToImageLite(req)
    return resp.to_json_string()
```
</details>

