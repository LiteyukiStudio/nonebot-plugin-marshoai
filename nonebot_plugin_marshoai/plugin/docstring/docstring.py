# -*- coding: utf-8 -*-
"""
Copyright (C) 2020-2024 LiteyukiStudio. All Rights Reserved 

@Time    : 2024/8/28 下午1:46
@Author  : snowykami
@Email   : snowykami@outlook.com
@File    : docstring.py
@Software: PyCharm
"""
from typing import Optional

from pydantic import BaseModel


class Attr(BaseModel):
    name: str
    type: str = ""
    desc: str = ""


class Args(BaseModel):
    name: str
    type: str = ""
    desc: str = ""


class Return(BaseModel):
    desc: str = ""


class Exception_(BaseModel):
    name: str
    desc: str = ""


class Raise(BaseModel):
    exceptions: list[Exception_] = []


class Example(BaseModel):
    desc: str = ""
    input: str = ""
    output: str = ""


class Docstring(BaseModel):
    raw: str = ""
    desc: str = ""
    args: list[Args] = []
    attrs: list[Attr] = []
    return_: Optional[Return] = None
    raise_: list[Exception_] = []
    example: Optional[str] = None

    front_matter: Optional[dict[str, str]] = None

    is_module: bool = False

    def add_desc(self, desc: str):
        if self.desc == "":
            self.desc = desc
        else:
            self.desc += "\n" + desc

    def add_arg(self, name: str, type_: str = "", desc: str = ""):
        self.args.append(Args(name=name, type=type_, desc=desc))

    def add_attrs(self, name: str, type_: str = "", desc: str = ""):
        self.attrs.append(Attr(name=name, type=type_, desc=desc))

    def add_return(self, desc: str = ""):
        self.return_ = Return(desc=desc)

    def add_raise(self, name: str, desc: str = ""):
        self.raise_.append(Exception_(name=name, desc=desc))

    def add_example(self, desc: str = ""):
        if self.example is None:
            self.example = desc
        else:
            self.example += "\n" + desc

    def add_front_matter(self, key: str, value: str):
        if self.front_matter is None:
            self.front_matter = {}
        self.front_matter[key] = value

    def reduction(self, style: str = "google") -> str:
        """
        通过解析结果还原docstring
        Args:
            style: docstring风格
        Returns:

        """
        ret = ""
        if style == "google":
            ret += self.desc + "\n"
            if self.args:
                ret += "Args:\n"
                for arg in self.args:
                    ret += f"    {arg.name}: {arg.type}\n        {arg.desc}\n"
            if self.attrs:
                ret += "Attributes:\n"
                for attr in self.attrs:
                    ret += f"    {attr.name}: {attr.type}\n        {attr.desc}\n"
            if self.return_:
                ret += "Returns:\n"
                ret += f"    {self.return_.desc}\n"

            if self.raise_:
                ret += "Raises:\n"
                for exception in self.raise_:
                    ret += f"    {exception.name}\n        {exception.desc}\n"

            if self.example:
                ret += "Examples:\n"
                ret += f"    {self.example}\n"
        return ret

    def __str__(self):
        return self.desc
