import asyncio
from typing import Any, Optional

from mcp.types import TextContent
from nonebot import logger

from .config import get_mcp_server_config
from .server import Server, Tool

_servers: list[Server] = list()


async def initialize_servers() -> None:
    """
    初始化全部 MCP 实例
    """
    server_config = get_mcp_server_config()
    _servers.extend(
        [Server(name, srv_config) for name, srv_config in server_config.items()]
    )
    for server in _servers:
        logger.info(f"正在初始化 MCP 服务器: {server.name}...")
        try:
            await server.initialize()
        except Exception as e:
            logger.error(f"初始化 MCP 服务器实例时出现问题: {e}")
            await cleanup_servers()
            raise


async def handle_mcp_tool(
    tool: str, arguments: Optional[dict[str, Any]] = None
) -> Optional[str | list]:
    """
    处理 MCP Tool 调用
    """
    logger.info(f"执行 MCP 工具: {tool} (参数: {arguments})")

    for server in _servers:
        server_tools = await server.list_tools()
        if not any(server_tool.name == tool for server_tool in server_tools):
            continue

        try:
            result = await server.execute_tool(tool, arguments)

            if isinstance(result, dict) and "progress" in result:
                progress = result["progress"]
                total = result["total"]
                percentage = (progress / total) * 100
                logger.info(
                    f"工具 {tool} 执行进度: {progress}/{total} ({percentage:.1f}%)"
                )
            if isinstance(result, list):
                content_string: str = ""
                # Assuming result is a dict with ContentBlock keys or values
                # Adjust as needed based on actual structure
                for content in result:
                    if isinstance(content, TextContent):
                        content_string += content.text
                return content_string
            return f"Tool execution result: {result}"
        except Exception as e:
            error_msg = f"Error executing tool: {str(e)}"
            logger.error(error_msg)
            return error_msg

    return None  # Not found.


async def cleanup_servers() -> None:
    """
    清理 MCP 实例
    """
    cleanup_tasks = [asyncio.create_task(server.cleanup()) for server in _servers]
    if cleanup_tasks:
        try:
            await asyncio.gather(*cleanup_tasks, return_exceptions=True)
        except Exception as e:
            logger.warning(f"清理 MCP 实例时出现错误: {e}")


async def transform_json(tool: Tool) -> dict[str, Any]:
    """
    将 MCP Tool 转换为 OpenAI 所需的 parameters 格式，并删除多余字段
    """
    func_desc = {
        "name": tool.name,
        "description": tool.description,
        "parameters": {},
        "required": [],
    }

    if tool.input_schema:
        parameters = {
            "type": tool.input_schema.get("type", "object"),
            "properties": tool.input_schema.get("properties", {}),
            "required": tool.input_schema.get("required", []),
        }
        func_desc["parameters"] = parameters

    output = {"type": "function", "function": func_desc}

    return output


async def get_mcp_list() -> list[dict[str, dict]]:
    """
    获得适用于 OpenAI Tool Call 输入格式的 MCP 工具列表
    """
    all_tools: list[dict[str, dict]] = []

    for server in _servers:
        tools = await server.list_tools()
        all_tools.extend([await transform_json(tool) for tool in tools])

    return all_tools


async def is_mcp_tool(tool_name: str) -> bool:
    """
    检查工具是否为 MCP 工具
    """
    mcp_list = await get_mcp_list()
    for tool in mcp_list:
        if tool["function"]["name"] == tool_name:
            return True
    return False
