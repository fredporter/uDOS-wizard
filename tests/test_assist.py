from __future__ import annotations

import unittest

from wizard.assist import route_assist


class AssistTests(unittest.TestCase):
    def test_offline_mode_uses_local_fallback(self) -> None:
        result = route_assist("demo", "offline")
        self.assertEqual(result["provider"], "local-fallback")
        self.assertEqual(result["status"], "queued")

    def test_default_mode_uses_wizard_provider(self) -> None:
        result = route_assist("demo")
        self.assertEqual(result["provider"], "wizard-provider")


if __name__ == "__main__":
    unittest.main()
