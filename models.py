from .util import *
class MarshoContext:
    """
    Marsho 的上下文类
    """
    def __init__(self):
        self.contents = []
        self.count = 0

    def append(self, content):
        """
        往上下文中添加消息
        Args:
            content: 消息
        """
        self.contents.append(content)

    def reset(self):
        """
        重置上下文
        """
        self.contents.clear()

    def addcount(self, num = 1):
        self.count += num

    def resetcount(self):
        self.count = 0

    def build(self):
        """
        构建返回的上下文，其中包括系统消息
        """
        spell = get_prompt()
        return [spell] + self.contents
