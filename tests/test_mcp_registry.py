from __future__ import annotations

import unittest

from wizard.mcp_registry import MCPRegistry


class MCPRegistryTests(unittest.TestCase):
    def test_register_and_list_tools(self) -> None:
        registry = MCPRegistry()
        registry.register("demo-tool", "Demo tool")
        result = registry.list_tools()
        self.assertEqual(result["count"], 1)
        self.assertIn("demo-tool", result["tools"])


if __name__ == "__main__":
    unittest.main()
