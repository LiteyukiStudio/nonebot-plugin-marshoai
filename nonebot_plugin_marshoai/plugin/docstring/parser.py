"""
Google docstring parser for Python.
"""

from typing import Optional

from .docstring import Docstring

placeholder = {
    "%20": " ",
    "%3A": ":",
}


def reduction(s: str) -> str:
    """还原特殊字符"""
    for k, v in placeholder.items():
        s = s.replace(k, v)
    return s


pre_handle_ph = {
    "://": "%3A//",
}


def pre_handle(s: str) -> str:
    """特殊字符保护"""
    for k, v in pre_handle_ph.items():
        s = s.replace(k, v)
    return s


class Parser: ...


class GoogleDocstringParser(Parser):
    _tokens = {
        "Args": "args",
        "Arguments": "args",
        "参数": "args",
        "Return": "return",
        "Returns": "return",
        "返回": "return",
        "Attribute": "attribute",
        "Attributes": "attribute",
        "属性": "attribute",
        "Raises": "raises",
        "Raise": "raises",
        "引发": "raises",
        "Example": "example",
        "Examples": "example",
        "示例": "example",
        "Yields": "yields",
        "Yield": "yields",
        "产出": "yields",
        "Requires": "requires",
        "Require": "requires",
        "需要": "requires",
        "FrontMatter": "front_matter",
        "前言": "front_matter",
    }

    def __init__(self, docstring: str, indent: int = 4, **kwargs):
        self.lines = pre_handle(docstring).splitlines()
        self.indent = indent
        self.lineno = 0  # Current line number
        self.char = 0  # Current character position

        self.is_module = kwargs.get("is_module", False)
        """是否为模块的docstring，是则不在说明处添加说明字样"""
        self.docstring = Docstring(raw=docstring, **kwargs)

    def read_line(self, move: bool = True) -> str:
        """
        每次读取一行
        Args:
            move: 是否移动指针
        Returns:
        """
        if self.lineno >= len(self.lines):
            return ""
        line = self.lines[self.lineno]
        if move:
            self.lineno += 1
        return line

    def match_token(self) -> Optional[str]:
        """
        解析下一行的token
        Returns:

        """
        for token in self._tokens:
            line = self.read_line(move=False)
            if line.strip().startswith(token):
                self.lineno += 1
                return self._tokens[token]
        return None

    def parse_args(self):
        """
        依次解析后面的参数行，直到缩进小于等于当前行的缩进
        """
        while line := self.match_next_line():
            if ":" in line:
                name, desc = line.split(":", 1)
                self.docstring.add_arg(reduction(name.strip()), reduction(desc.strip()))
            else:
                self.docstring.add_arg(reduction(line.strip()))

    def parse_return(self):
        """
        解析返回值行
        """
        if line := self.match_next_line():
            self.docstring.add_return(reduction(line.strip()))

    def parse_raises(self):
        """
        解析异常行
        """
        while line := self.match_next_line():
            if ":" in line:
                name, desc = line.split(":", 1)
                self.docstring.add_raise(
                    reduction(name.strip()), reduction(desc.strip())
                )
            else:
                self.docstring.add_raise(reduction(line.strip()))

    def parse_example(self):
        """
        解析示例行
        """
        while line := self.match_next_line():
            self.docstring.add_example(
                reduction(line if line.startswith("    ") else line.strip())
            )

    def parse_attrs(self):
        """
        解析属性行
        """
        while line := self.match_next_line():
            if ":" in line:
                name, desc = line.split(":", 1)
                self.docstring.add_attrs(
                    reduction(name.strip()), reduction(desc.strip())
                )
            else:
                self.docstring.add_attrs(reduction(line.strip()))

    def match_next_line(self) -> Optional[str]:
        """
        在一个子解析器中，解析下一行，直到缩进小于等于当前行的缩进
        Returns:
        """
        line = self.read_line(move=False)
        if line.startswith(" " * self.indent):
            self.lineno += 1
            return line[self.indent :]
        else:
            return None

    def parse(self) -> Docstring:
        """
        逐行解析，直到遇到token，解析token对应的内容，

        最开始未解析到的内容全部加入desc

        Returns:
            Docstring
        """
        add_desc = True
        add_front_matter = False
        while self.lineno < len(self.lines):
            token = self.match_token()

            if token is None and add_desc:
                if self.is_module and self.lines[self.lineno].strip() == "---":
                    add_front_matter = not add_front_matter
                    self.lineno += 1
                    continue
                if add_front_matter and ":" in self.lines[self.lineno]:
                    key, value = map(str.strip, self.lines[self.lineno].split(":", 1))
                    self.docstring.add_front_matter(key, value)
                else:
                    self.docstring.add_desc(reduction(self.lines[self.lineno].strip()))
            if token is not None:
                add_desc = False

            match token:
                case "args":
                    self.parse_args()
                case "return":
                    self.parse_return()
                case "attribute":
                    self.parse_attrs()
                case "raises":
                    self.parse_raises()
                case "example":
                    self.parse_example()
                case _:
                    self.lineno += 1

        return self.docstring


class NumpyDocstringParser(Parser): ...


class ReStructuredParser(Parser): ...


def parse(
    docstring: str, parser: str = "google", indent: int = 4, **kwargs
) -> Docstring:
    if parser == "google":
        return GoogleDocstringParser(docstring, indent, **kwargs).parse()
    else:
        raise ValueError(f"Unknown parser: {parser}")
