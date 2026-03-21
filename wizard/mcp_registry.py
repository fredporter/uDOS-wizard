from __future__ import annotations

from collections.abc import Callable
from copy import deepcopy
from typing import Any


ToolHandler = Callable[[dict[str, Any]], dict[str, Any]]


class MCPRegistry:
    def __init__(self) -> None:
        self.tools: dict[str, dict[str, Any]] = {}

    def register(
        self,
        name: str,
        description: str,
        *,
        input_schema: dict[str, Any] | None = None,
        annotations: dict[str, Any] | None = None,
        handler: ToolHandler | None = None,
    ) -> dict[str, Any]:
        tool = {
            "name": name,
            "description": description,
            "input_schema": deepcopy(input_schema or {"type": "object", "properties": {}, "additionalProperties": True}),
            "annotations": deepcopy(annotations or {}),
            "handler": handler,
        }
        self.tools[name] = tool
        return self._public_tool(tool)

    def list_tools(self) -> dict[str, Any]:
        public_tools = [self._public_tool(tool) for _, tool in sorted(self.tools.items())]
        return {"count": len(public_tools), "tools": public_tools}

    def invoke(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        tool = self.tools.get(name)
        if tool is None:
            raise KeyError(f"unknown MCP tool: {name}")

        handler = tool.get("handler")
        if handler is None:
            raise ValueError(f"MCP tool has no handler: {name}")

        payload = dict(arguments or {})
        result = handler(payload)
        return {
            "tool": self._public_tool(tool),
            "arguments": payload,
            "result": result,
        }

    def _public_tool(self, tool: dict[str, Any]) -> dict[str, Any]:
        return {
            "name": tool["name"],
            "description": tool["description"],
            "input_schema": deepcopy(tool["input_schema"]),
            "annotations": deepcopy(tool["annotations"]),
        }
