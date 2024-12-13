# -*- coding: utf-8 -*-
"""
Copyright (C) 2020-2024 LiteyukiStudio. All Rights Reserved
本模块为工具加载模块
"""
import os
import traceback
from importlib import import_module
from pathlib import Path
from typing import Optional

from nonebot import logger

from .models import Plugin, PluginMetadata
from .utils import path_to_module_name

_plugins: dict[str, Plugin] = {}

__all__ = [
    "load_plugin",
    "load_plugins",
    "_plugins",
]


def load_plugin(module_path: str | Path) -> Optional[Plugin]:
    """加载单个插件，可以是本地插件或是通过 `pip` 安装的插件。
    该函数产生的副作用在于将插件加载到 `_plugins` 中。

    Args:
        module_path: 插件名称 `path.to.your.plugin`
        或插件路径 `pathlib.Path(path/to/your/plugin)`
    Returns:
        Optional[Plugin]: 插件对象
    """
    module_path = (
        path_to_module_name(Path(module_path))
        if isinstance(module_path, Path)
        else module_path
    )
    try:
        module = import_module(module_path)  # 导入模块对象
        plugin = Plugin(
            name=module.__name__,
            module=module,
            module_name=module_path,
        )

        plugin.metadata = getattr(module, "__marsho_meta__", None)

        _plugins[plugin.name] = plugin

        logger.opt(colors=True).success(
            f'Succeeded to load liteyuki plugin "{plugin.name}"'
        )
        return _plugins[module.__name__]

    except Exception as e:
        logger.opt(colors=True).success(
            f'Failed to load liteyuki plugin "<r>{module_path}</r>"'
        )
        traceback.print_exc()
        return None


def load_plugins(*plugin_dirs: str) -> set[Plugin]:
    """导入文件夹下多个插件

    参数:
        plugin_dir: 文件夹路径
        ignore_warning: 是否忽略警告，通常是目录不存在或目录为空
    返回:
        set[Plugin]: 插件集合
    """
    plugins = set()
    for plugin_dir in plugin_dirs:
        for f in os.listdir(plugin_dir):
            path = Path(os.path.join(plugin_dir, f))

            module_name = None

            if os.path.isfile(path) and f.endswith(".py"):
                """单文件加载"""
                module_name = f"{path_to_module_name(Path(plugin_dir))}.{f[:-3]}"

            elif os.path.isdir(path) and os.path.exists(
                os.path.join(path, "__init__.py")
            ):
                """包加载"""
                module_name = path_to_module_name(path)

            if module_name and (plugin := load_plugin(module_name)):
                plugins.add(plugin)
    return plugins
