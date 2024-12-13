#!/usr/bin/env python3

import os
import re
import sys


def is_valid_filename(filename: str) -> bool:
    """文件名完整相对路径

    Args:
        filename (str): _description_

    Returns:
        bool: _description_
    """
    # 检查文件名是否仅包含小写字母，数字，下划线
    if not re.match(r"^[a-z0-9_]+\.py$", filename):
        return False
    else:
        return True


def main():
    invalid_files = []
    for root, _, files in os.walk("nonebot_plugin_marshoai"):
        for file in files:
            if file.endswith(".py"):
                if not is_valid_filename(file):
                    invalid_files.append(os.path.join(root, file))

    if invalid_files:
        print("以下文件名不符合命名规则:")
        for file in invalid_files:
            print(file)
        sys.exit(1)


if __name__ == "__main__":
    main()
