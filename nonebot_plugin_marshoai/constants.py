__version__ = "0.3.4.1"
USAGE: str = f"""MarshoAI-NoneBot Beta v{__version__} by Asankilp
用法：
  marsho <聊天内容> : 与 Marsho 进行对话。当模型为 GPT-4o(-mini) 等时，可以带上图片进行对话。
  nickname [昵称] : 为自己设定昵称，设置昵称后，Marsho 会根据你的昵称进行回答。使用'nickname reset'命令可清除自己设定的昵称。
  reset : 重置当前会话的上下文。 ※需要加上命令前缀使用(默认为'/')。
超级用户命令(均需要加上命令前缀使用):
  changemodel <模型名> : 切换全局 AI 模型。
  contexts : 返回当前会话的上下文列表。 ※当上下文包含图片时，不要使用此命令。
  praises : 返回夸赞名单的提示词。
  usermsg <消息> : 往当前会话添加用户消息(UserMessage)。
  assistantmsg <消息> : 往当前会话添加助手消息(AssistantMessage)。
  savecontext <文件名> : 保存当前会话的上下文至插件数据目录下的contexts/<文件名>.json里。
  loadcontext <文件名> : 从插件数据目录下的contexts/<文件名>.json里读取上下文并覆盖到当前会话。
※本AI的回答"按原样"提供，不提供任何担保。AI也会犯错，请仔细甄别回答的准确性。"""

SUPPORT_IMAGE_MODELS: list = ["gpt-4o","gpt-4o-mini","llama-3.2-90b-vision-instruct","llama-3.2-11b-vision-instruct"]
REASONING_MODELS: list = ["o1-preview","o1-mini"]
INTRODUCTION: str =  """你好喵~我是一只可爱的猫娘AI，名叫小棉~🐾！
我的代码在这里哦~↓↓↓
https://github.com/LiteyukiStudio/nonebot-plugin-marshoai

也可以关注一下还在成长中的 Melobot 酱喵~↓↓↓
https://github.com/Meloland/melobot
我与 Melobot 酱贴贴的代码在这里喵~↓↓↓
https://github.com/LiteyukiStudio/marshoai-melo"""
