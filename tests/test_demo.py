from __future__ import annotations

import unittest
from unittest.mock import patch

from wizard.port_manager import BindPlan


class _Process:
    def __init__(self, return_code: int = 0) -> None:
        self._return_code = return_code

    def poll(self):
        return self._return_code

    def send_signal(self, _signal):
        return None

    def wait(self, timeout=None):
        return self._return_code


class DemoLauncherTests(unittest.TestCase):
    def test_configured_uhome_base_url_uses_env_override(self) -> None:
        from wizard.demo import configured_uhome_base_url

        with patch.dict("os.environ", {"UHOME_SERVER_URL": "http://127.0.0.1:8001"}, clear=False):
            self.assertEqual(
                configured_uhome_base_url("127.0.0.1", 8000),
                "http://127.0.0.1:8001",
            )

    @patch("wizard.demo.time.sleep", return_value=None)
    @patch("wizard.demo._print_demo_links")
    @patch("wizard.demo._spawn_wizard", return_value=_Process())
    @patch("wizard.demo.resolve_bind_plan")
    def test_demo_uses_default_bind_resolution_when_port_not_explicit(
        self,
        resolve_bind_plan,
        _spawn_wizard,
        _print_demo_links,
        _sleep,
    ) -> None:
        from wizard.demo import main

        resolve_bind_plan.return_value = BindPlan(
            host="127.0.0.1",
            port=8788,
            requested_port=8787,
            port_source="default",
            auto_shifted=True,
            occupant=None,
        )

        result = main(["--no-uhome"])

        self.assertEqual(result, 0)
        resolve_bind_plan.assert_called_once_with(host="127.0.0.1")

    @patch("wizard.demo.time.sleep", return_value=None)
    @patch("wizard.demo._print_demo_links")
    @patch("wizard.demo._spawn_wizard", return_value=_Process())
    @patch("wizard.demo.resolve_bind_plan")
    def test_demo_respects_explicit_port_override(
        self,
        resolve_bind_plan,
        _spawn_wizard,
        _print_demo_links,
        _sleep,
    ) -> None:
        from wizard.demo import main

        resolve_bind_plan.return_value = BindPlan(
            host="127.0.0.1",
            port=9900,
            requested_port=9900,
            port_source="argument",
            auto_shifted=False,
            occupant=None,
        )

        result = main(["--no-uhome", "--wizard-port", "9900"])

        self.assertEqual(result, 0)
        resolve_bind_plan.assert_called_once_with(host="127.0.0.1", port=9900)


if __name__ == "__main__":
    unittest.main()
