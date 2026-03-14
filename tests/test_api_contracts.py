from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from wizard.main import app


class APIContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_root_reports_wizard_service(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"service": "wizard", "status": "ok"})

    def test_beacon_announce_route_returns_ok(self) -> None:
        response = self.client.get("/beacon/announce")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["beacon"], "announce")
        self.assertEqual(payload["status"], "ok")

    def test_assist_route_reflects_offline_provider(self) -> None:
        response = self.client.get("/assist", params={"task": "demo", "mode": "offline"})
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["task"], "demo")
        self.assertEqual(payload["provider"], "local-fallback")
        self.assertEqual(payload["executor"], "local-shell")

    def test_orchestration_status_exposes_v2_0_2_runtime_consumption(self) -> None:
        response = self.client.get("/orchestration/status")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["version"], "v2.0.2")
        self.assertEqual(payload["foundation_version"], "v2.0.1")
        self.assertTrue(payload["runtime_service_source"].endswith("uDOS-core/contracts/runtime-services.json"))
        services = {service["service"] for service in payload["services"]}
        self.assertIn("assist", services)
        runtime_services = {service["key"] for service in payload["runtime_services"]}
        self.assertIn("runtime.capability-registry", runtime_services)

    def test_orchestration_dispatch_accepts_surface(self) -> None:
        response = self.client.get(
            "/orchestration/dispatch",
            params={"task": "remote-control", "mode": "auto", "surface": "remote-control"},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["task"], "remote-control")
        self.assertEqual(payload["surface"], "remote-control")
        self.assertEqual(payload["provider"], "wizard-provider")
        self.assertEqual(payload["dispatch_version"], "v2.0.2")
        self.assertEqual(payload["request"]["surface"], "remote-control")
        self.assertEqual(payload["route_contract"]["owner"], "uDOS-wizard")


if __name__ == "__main__":
    unittest.main()
