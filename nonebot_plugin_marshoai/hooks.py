# Marsho 的钩子函数
import os
from pathlib import Path

import nonebot_plugin_localstore as store
from nonebot import logger

from .config import config
from .instances import *
from .plugin import load_plugin, load_plugins
from .util import get_backup_context, save_context_to_json


@driver.on_startup
async def _preload_tools():
    """启动钩子加载工具"""
    tools_dir = store.get_plugin_data_dir() / "tools"
    os.makedirs(tools_dir, exist_ok=True)
    if config.marshoai_enable_tools:
        if config.marshoai_load_builtin_tools:
            tools.load_tools(Path(__file__).parent / "tools")
        tools.load_tools(store.get_plugin_data_dir() / "tools")
        for tool_dir in config.marshoai_toolset_dir:
            tools.load_tools(tool_dir)
        logger.info(
            "如果启用小棉工具后使用的模型出现报错，请尝试将 MARSHOAI_ENABLE_TOOLS 设为 false。"
        )
        logger.opt(colors=True).warning(
            "<y>小棉工具已被弃用，可能会在未来版本中移除。</y>"
        )


@driver.on_startup
async def _():
    """启动钩子加载插件"""
    if config.marshoai_enable_plugins:
        marshoai_plugin_dirs = config.marshoai_plugin_dirs  # 外部插件目录列表
        """加载内置插件"""
        for p in os.listdir(Path(__file__).parent / "plugins"):
            load_plugin(f"{__package__}.plugins.{p}")

        """加载指定目录插件"""
        load_plugins(*marshoai_plugin_dirs)

        """加载sys.path下的包, 包括从pip安装的包"""
        for package_name in config.marshoai_plugins:
            load_plugin(package_name)
        logger.info(
            "如果启用小棉插件后使用的模型出现报错，请尝试将 MARSHOAI_ENABLE_PLUGINS 设为 false。"
        )


@driver.on_shutdown
async def auto_backup_context():
    for target_info in target_list:
        target_id, target_private = target_info
        contexts_data = context.build(target_id, target_private)
        if target_private:
            target_uid = "private_" + target_id
        else:
            target_uid = "group_" + target_id
        await save_context_to_json(
            f"back_up_context_{target_uid}", contexts_data, "contexts/backup"
        )
        logger.info(f"已保存会话 {target_id} 的上下文备份，将在下次对话时恢复~")
