import importlib
import json
import os
import sys

# import importlib.util
import traceback

from nonebot import logger

from .config import config
from .util import *


class MarshoContext:
    """
    Marsho 的上下文类
    """

    def __init__(self):
        self.contents = {"private": {}, "non-private": {}}

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
        if target_id in target_dict:
            target_dict[target_id].clear()

    def reset_all(self):
        """
        重置所有上下文
        """
        self.contents["private"].clear()
        self.contents["non-private"].clear()

    def build(self, target_id: str, is_private: bool) -> list:
        """
        构建返回的上下文，不包括系统消息
        """
        target_dict = self._get_target_dict(is_private)
        if target_id not in target_dict:
            target_dict[target_id] = []
        return target_dict[target_id]


class MarshoTools:
    """
    Marsho 的工具类
    """

    def __init__(self):
        self.tools_list = []
        self.imported_packages = {}

    def load_tools(self, tools_dir):
        """
        从指定路径加载工具包
        """
        if not os.path.exists(tools_dir):
            logger.error(f"工具集目录 {tools_dir} 不存在。")
            return

        for package_name in os.listdir(tools_dir):
            package_path = os.path.join(tools_dir, package_name)

            #  logger.info(f"尝试加载工具包 {package_name}")
            if package_name in config.marshoai_disabled_toolkits:
                logger.info(f"工具包 {package_name} 已被禁用。")
                continue
            if os.path.isdir(package_path) and os.path.exists(
                os.path.join(package_path, "__init__.py")
            ):
                json_path = os.path.join(package_path, "tools.json")
                if os.path.exists(json_path):
                    try:
                        with open(json_path, "r", encoding="utf-8") as json_file:
                            data = json.load(json_file)
                            for i in data:

                                self.tools_list.append(i)

                            spec = importlib.util.spec_from_file_location(
                                package_name, os.path.join(package_path, "__init__.py")
                            )
                            package = importlib.util.module_from_spec(spec)
                            self.imported_packages[package_name] = package
                            sys.modules[package_name] = package
                            spec.loader.exec_module(package)

                            logger.success(f"成功加载工具包 {package_name}")
                    except json.JSONDecodeError as e:
                        logger.error(f"解码 JSON {json_path} 时发生错误: {e}")
                    except Exception as e:
                        logger.error(f"加载工具包时发生错误: {e}")
                        traceback.print_exc()
                else:
                    logger.warning(
                        f"在工具包 {package_path} 下找不到tools.json，跳过加载。"
                    )
            else:
                logger.warning(f"{package_path} 不是有效的工具包路径，跳过加载。")

    async def call(self, full_function_name: str, args: dict):
        """
        调用指定的函数
        """
        # 分割包名和函数名
        parts = full_function_name.split("__")
        if len(parts) == 2:
            package_name = parts[0]
            function_name = parts[1]
        else:
            logger.error("函数名无效")
        if package_name in self.imported_packages:
            package = self.imported_packages[package_name]
            try:
                function = getattr(package, function_name)
                return await function(**args)
            except Exception as e:
                errinfo = f"调用函数 '{function_name}'时发生错误:{e}"
                logger.error(errinfo)
                return errinfo
        else:
            logger.error(f"工具包 '{package_name}' 未导入")

    def has_function(self, full_function_name: str) -> bool:
        """
        检查是否存在指定的函数
        """
        try:
            for t in self.tools_list:
                if t["function"]["name"].replace(
                    "-", "_"
                ) == full_function_name.replace("-", "_"):
                    return True
            return False
        except Exception as e:
            logger.error(f"检查函数 '{full_function_name}' 时发生错误:{e}")
            return False

    def get_tools_list(self):
        if not self.tools_list or not config.marshoai_enable_tools:
            return None
        return self.tools_list
