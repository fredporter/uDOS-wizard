from __future__ import annotations

import unittest
from unittest.mock import patch

from wizard.port_manager import (
    BindPlan,
    PortOccupant,
    build_base_url,
    configured_runtime_bind_status,
    format_bind_failure,
    resolve_bind_plan,
    runtime_bind_status_from_plan,
)


class PortManagerTests(unittest.TestCase):
    @patch("wizard.port_manager.is_port_available", return_value=True)
    def test_resolve_bind_plan_uses_default_port_when_free(self, _available) -> None:
        with patch.dict("os.environ", {}, clear=False):
            plan = resolve_bind_plan()

        self.assertEqual(
            plan,
            BindPlan(
                host="127.0.0.1",
                port=8787,
                requested_port=8787,
                port_source="default",
                auto_shifted=False,
                occupant=None,
            ),
        )

    @patch("wizard.port_manager.find_available_port", return_value=8788)
    @patch(
        "wizard.port_manager.detect_port_occupant",
        return_value=PortOccupant(pid=1234, process="Python", port=8787),
    )
    @patch("wizard.port_manager.is_port_available", side_effect=[False])
    def test_resolve_bind_plan_auto_shifts_default_port(
        self,
        _available,
        _occupant,
        _finder,
    ) -> None:
        with patch.dict("os.environ", {}, clear=False):
            plan = resolve_bind_plan()

        self.assertEqual(plan.port, 8788)
        self.assertTrue(plan.auto_shifted)
        self.assertEqual(plan.requested_port, 8787)
        self.assertEqual(plan.occupant.pid, 1234)

    @patch(
        "wizard.port_manager.detect_port_occupant",
        return_value=PortOccupant(pid=777, process="Python", port=9000),
    )
    @patch("wizard.port_manager.is_port_available", side_effect=[False])
    def test_resolve_bind_plan_fails_for_explicit_env_port(self, _available, _occupant) -> None:
        with patch.dict("os.environ", {"UDOS_WIZARD_PORT": "9000"}, clear=False):
            with self.assertRaises(RuntimeError) as ctx:
                resolve_bind_plan()

        self.assertIn("9000", str(ctx.exception))
        self.assertIn("PID 777", str(ctx.exception))

    def test_format_bind_failure_reports_occupant(self) -> None:
        message = format_bind_failure(
            "127.0.0.1",
            8787,
            "default",
            PortOccupant(pid=88, process="Python", port=8787),
        )
        self.assertIn("Python", message)
        self.assertIn("PID 88", message)

    def test_build_base_url_normalizes_wildcard_host(self) -> None:
        self.assertEqual(build_base_url("0.0.0.0", 8787), "http://127.0.0.1:8787")

    def test_runtime_bind_status_from_plan_exposes_gui_and_thin_urls(self) -> None:
        status = runtime_bind_status_from_plan(
            BindPlan(
                host="127.0.0.1",
                port=8788,
                requested_port=8787,
                port_source="default",
                auto_shifted=True,
                occupant=PortOccupant(pid=10, process="Python", port=8787),
            )
        )
        self.assertEqual(status.base_url, "http://127.0.0.1:8788")
        self.assertEqual(status.gui_url, "http://127.0.0.1:8788/gui")
        self.assertEqual(status.thin_url, "http://127.0.0.1:8788/thin")
        self.assertTrue(status.actual_binding_known)

    @patch(
        "wizard.port_manager.detect_port_occupant",
        return_value=PortOccupant(pid=99, process="Python", port=8787),
    )
    def test_configured_runtime_bind_status_reports_unknown_actual_binding(self, _occupant) -> None:
        with patch.dict("os.environ", {}, clear=False):
            status = configured_runtime_bind_status()

        self.assertEqual(status.port, 8787)
        self.assertFalse(status.actual_binding_known)
        self.assertEqual(status.gui_url, "http://127.0.0.1:8787/gui")


if __name__ == "__main__":
    unittest.main()
