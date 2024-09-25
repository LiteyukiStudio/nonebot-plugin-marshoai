from .util import *
class MarshoContext:
    def __init__(self):
        self.contents = []

    def append(self, content):
        self.contents.append(content)

    def reset(self):
        self.contents.clear()

    def build(self):
        spell = get_default_spell()
        return [spell] + self.contents
