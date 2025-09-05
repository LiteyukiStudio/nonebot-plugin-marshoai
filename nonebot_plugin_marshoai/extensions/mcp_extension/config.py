import json
import shutil
from pathlib import Path
from typing import Any, Literal

from nonebot import logger
from pydantic import BaseModel, Field, ValidationError, model_validator
from typing_extensions import Self

mcp_config_file_path = Path("config/marshoai/mcp.json").resolve()


class mcpConfig(BaseModel):
    command: str = Field(default="")
    """执行指令"""
    args: list[str] = Field(default_factory=list)
    """命令参数"""
    env: dict[str, Any] = Field(default_factory=dict)
    """环境配置"""
    headers: dict[str, Any] = Field(default_factory=dict)
    """HTTP请求头(用于 `sse` 和 `streamable_http` 传输方式)"""
    type: Literal["stdio", "sse", "streamable_http"] = Field(default="stdio")
    """传输方式: `stdio`, `sse`, `streamable_http`"""
    url: str = Field(default="")
    """服务器 URL (用于 `sse` 和 `streamable_http` 传输方式)"""

    @model_validator(mode="after")
    def validate_config(self) -> Self:
        srv_type = self.type
        command = self.command
        url = self.url

        if srv_type == "stdio":
            if not command:
                raise ValueError("当 type 为 'stdio' 时，command 字段必须存在")
            # 检查 command 是否为可执行的命令
            elif not shutil.which(command):
                raise ValueError(f"命令 '{command}' 不存在或不可执行。")

        elif srv_type in ["sse", "streamable_http"] and not url:
            raise ValueError(f"当 type 为 '{srv_type}' 时，url 字段必须存在")

        return self


def get_mcp_server_config() -> dict[str, mcpConfig]:
    """
    从 MCP 配置文件 `config/mcp.json` 中获取 MCP Server 配置
    """
    if not mcp_config_file_path.exists():
        return {}

    try:
        with open(mcp_config_file_path, "r", encoding="utf-8") as f:
            configs = json.load(f) or {}
    except (json.JSONDecodeError, IOError, OSError) as e:
        raise RuntimeError(f"读取 MCP 配置文件时发生错误: {e}")

    if not isinstance(configs, dict):
        raise TypeError("非预期的 MCP 配置文件格式")

    mcp_servers = configs.get("mcpServers", {})
    if not isinstance(mcp_servers, dict):
        raise TypeError("非预期的 MCP 配置文件格式")

    mcp_config: dict[str, mcpConfig] = {}
    for name, srv_config in mcp_servers.items():
        try:
            mcp_config[name] = mcpConfig(**srv_config)
        except (ValidationError, TypeError) as e:
            logger.warning(f"无效的MCP服务器配置 '{name}': {e}")
            continue

    return mcp_config
