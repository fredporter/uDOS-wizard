from __future__ import annotations

class MCPRegistry:
    def __init__(self) -> None:
        self.tools: dict[str, dict] = {}

    def register(self, name: str, description: str) -> dict:
        self.tools[name] = {"description": description}
        return {"name": name, "description": description}

    def list_tools(self) -> dict:
        return {"count": len(self.tools), "tools": self.tools}
