from .util import *

class MarshoContext:
    """
    Marsho 的上下文类
    """
    def __init__(self):
        self.contents = {
            "private": {},
            "non-private": {}
        }

    def _get_target_dict(self, is_private):
        return self.contents["private"] if is_private else self.contents["non-private"]

    def append(self, content, target_id: str, is_private: bool):
        """
        往上下文中添加消息
        """
        target_dict = self._get_target_dict(is_private)
        if target_id not in target_dict:
            target_dict[target_id] = []
        target_dict[target_id].append(content)

    def set_context(self, contexts, target_id: str, is_private: bool):
        """
        设置上下文
        """
        target_dict = self._get_target_dict(is_private)
        target_dict[target_id] = contexts

    def reset(self, target_id: str, is_private: bool):
        """
        重置上下文
        """
        target_dict = self._get_target_dict(is_private)
        target_dict[target_id].clear()

    def build(self, target_id: str, is_private: bool) -> list:
        """
        构建返回的上下文，其中包括系统消息
        """
        spell = get_prompt()
        target_dict = self._get_target_dict(is_private)
        if target_id not in target_dict:
            target_dict[target_id] = []
        return [spell] + target_dict[target_id]