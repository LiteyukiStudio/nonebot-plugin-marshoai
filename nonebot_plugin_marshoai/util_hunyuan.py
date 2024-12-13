import json
import types

from tencentcloud.common import credential  # type: ignore
from tencentcloud.common.exception.tencent_cloud_sdk_exception import (  # type: ignore
    TencentCloudSDKException,
)
from tencentcloud.common.profile.client_profile import ClientProfile  # type: ignore
from tencentcloud.common.profile.http_profile import HttpProfile  # type: ignore
from tencentcloud.hunyuan.v20230901 import hunyuan_client  # type: ignore
from tencentcloud.hunyuan.v20230901 import models  # type: ignore

from .config import config


def generate_image(prompt: str):
    cred = credential.Credential(
        config.marshoai_tencent_secretid, config.marshoai_tencent_secretkey
    )
    # 实例化一个http选项，可选的，没有特殊需求可以跳过
    httpProfile = HttpProfile()
    httpProfile.endpoint = "hunyuan.tencentcloudapi.com"

    # 实例化一个client选项，可选的，没有特殊需求可以跳过
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = hunyuan_client.HunyuanClient(cred, "ap-guangzhou", clientProfile)

    req = models.TextToImageLiteRequest()
    params = {"Prompt": prompt, "RspImgType": "url", "Resolution": "1080:1920"}
    req.from_json_string(json.dumps(params))

    # 返回的resp是一个TextToImageLiteResponse的实例，与请求对象对应
    resp = client.TextToImageLite(req)
    # 输出json格式的字符串回包
    return resp.to_json_string()
