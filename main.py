"""该入口文件仅在nb run无法正常工作时使用
"""

import nonebot
from nonebot import get_driver
from nonebot.adapters.onebot.v11 import Adapter
from nonebot.plugin import load_plugin

nonebot.init()
load_plugin("nonebot_plugin_marshoai")

driver = get_driver()
driver.register_adapter(Adapter)

if __name__ == "__main__":
    nonebot.run()

# 这是猫娘写的代码

# 这是猫娘写的代码
