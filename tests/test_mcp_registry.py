from __future__ import annotations

import unittest

from wizard.mcp_registry import MCPRegistry


class MCPRegistryTests(unittest.TestCase):
    def test_register_and_list_tools(self) -> None:
        registry = MCPRegistry()
        registry.register("demo-tool", "Demo tool")
        result = registry.list_tools()
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["tools"][0]["name"], "demo-tool")

    def test_invoke_registered_tool(self) -> None:
        registry = MCPRegistry()
        registry.register(
            "demo-tool",
            "Demo tool",
            handler=lambda payload: {"echo": payload.get("value", "")},
        )

        result = registry.invoke("demo-tool", {"value": "ok"})

        self.assertEqual(result["tool"]["name"], "demo-tool")
        self.assertEqual(result["result"]["echo"], "ok")


if __name__ == "__main__":
    unittest.main()
