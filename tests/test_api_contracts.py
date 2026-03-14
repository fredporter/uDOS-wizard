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


if __name__ == "__main__":
    unittest.main()
