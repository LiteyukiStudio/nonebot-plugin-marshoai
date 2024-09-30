from .util import *
class MarshoContext:
    def __init__(self):
        self.contents = []
        self.count = 0

    def append(self, content):
        self.contents.append(content)

    def reset(self):
        self.contents.clear()

    def addcount(self, num = 1):
        self.count += num

    def resetcount(self):
        self.count = 0

    def build(self):
        spell = get_prompt()
        return [spell] + self.contents
