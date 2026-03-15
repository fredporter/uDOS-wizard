from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import os
from unittest.mock import patch

from fastapi.testclient import TestClient

from wizard.main import app
from wizard.orchestration import OrchestrationRegistry


class APIContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_root_reports_wizard_service(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"service": "wizard", "status": "ok"})

    def test_port_status_route_reports_runtime_bind_snapshot(self) -> None:
        response = self.client.get("/port/status")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("base_url", payload)
        self.assertIn("gui_url", payload)
        self.assertIn("thin_url", payload)
        self.assertIn("actual_binding_known", payload)

    def test_runtime_config_summary_route_reports_expected_keys(self) -> None:
        response = self.client.get("/config/runtime-summary")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("entries", payload)
        keys = {entry["key"] for entry in payload["entries"]}
        self.assertIn("UDOS_WIZARD_PORT", keys)
        self.assertIn("OPENAI_API_KEY", keys)

    def test_grid_contract_route_exposes_grid_owned_contract(self) -> None:
        response = self.client.get("/grid/contracts/grid-place")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["owner"], "uDOS-grid")
        self.assertIn("place_id", payload["required_fields"])

    def test_grid_seed_route_exposes_seed_registry(self) -> None:
        response = self.client.get("/grid/seeds/places")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["owner"], "uDOS-grid")
        self.assertEqual(payload["consumer"], "uDOS-wizard")
        self.assertGreaterEqual(payload["count"], 1)

    def test_grid_resolve_and_validate_place_routes(self) -> None:
        resolved = self.client.get("/grid/resolve", params={"place_ref": "EARTH:SUR:L300-AJ11"})
        self.assertEqual(resolved.status_code, 200)
        resolved_payload = resolved.json()
        self.assertTrue(resolved_payload["ok"])
        self.assertEqual(resolved_payload["resolved"]["place_id"], "EARTH:SUR:L300-AJ11")

        validated = self.client.post(
            "/grid/validate-place",
            json={
                "place_ref": "EARTH:SUB:L301-AJ11-Z-3",
                "required_space": "SUB",
                "artifact_id": "binder.crypt.south",
            },
        )
        self.assertEqual(validated.status_code, 200)
        validated_payload = validated.json()
        self.assertTrue(validated_payload["ok"])
        self.assertTrue(validated_payload["checks"]["space_match"])
        self.assertTrue(validated_payload["checks"]["artifact_match"])

    def test_gui_shell_route_serves_html(self) -> None:
        response = self.client.get("/gui")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])

    def test_thin_shell_route_serves_html(self) -> None:
        response = self.client.get("/thin")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])

    def test_demo_links_routes_expose_lane_urls(self) -> None:
        response = self.client.get("/demo/links")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["service"], "wizard-demo")
        self.assertIn("workflow", payload["links"])
        self.assertTrue(payload["links"]["workflow"].endswith("/app/workflow"))
        self.assertTrue(payload["links"]["automation"].endswith("/app/automation"))
        self.assertTrue(payload["links"]["publishing"].endswith("/app/publishing"))

        html_response = self.client.get("/demo")
        self.assertEqual(html_response.status_code, 200)
        self.assertIn("text/html", html_response.headers["content-type"])
        self.assertIn("uDOS Demo Links", html_response.text)
        self.assertIn("/app/workflow", html_response.text)

    def test_svelte_app_route_serves_html_or_missing_build_payload(self) -> None:
        response = self.client.get("/app")
        self.assertEqual(response.status_code, 200)
        content_type = response.headers["content-type"]
        self.assertTrue("text/html" in content_type or "application/json" in content_type)

    def test_svelte_app_spa_route_serves_html_or_missing_build_payload(self) -> None:
        response = self.client.get("/app/presets")
        self.assertEqual(response.status_code, 200)
        content_type = response.headers["content-type"]
        self.assertTrue("text/html" in content_type or "application/json" in content_type)

    def test_beacon_announce_route_returns_ok(self) -> None:
        response = self.client.get("/beacon/announce")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["beacon"], "announce")
        self.assertEqual(payload["status"], "ok")

    def test_workflow_state_and_actions_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.dict(
                "os.environ",
                {
                    "UDOS_STATE_ROOT": str(Path(temp_dir) / "state"),
                    "WIZARD_STATE_ROOT": str(Path(temp_dir) / "state" / "wizard"),
                },
                clear=False,
            ):
                state = self.client.get("/workflow/state")
                self.assertEqual(state.status_code, 200)
                self.assertEqual(state.json()["workflow_id"], "wizard-default")

                action = self.client.post(
                    "/workflow/actions",
                    json={
                        "workflow_id": "mission-alpha",
                        "action": "advance",
                        "requested_by": "test-user",
                        "policy_flags": {"requires_online": True},
                    },
                )
                self.assertEqual(action.status_code, 200)
                action_payload = action.json()
                self.assertEqual(action_payload["action"]["action"], "advance")
                self.assertEqual(action_payload["state"]["workflow_id"], "mission-alpha")
                self.assertEqual(action_payload["state"]["status"], "running")

                actions = self.client.get("/workflow/actions")
                self.assertEqual(actions.status_code, 200)
                self.assertEqual(actions.json()["count"], 1)

                updated = self.client.post(
                    "/workflow/state",
                    json={"status": "paused", "awaiting_user_action": True},
                )
                self.assertEqual(updated.status_code, 200)
                self.assertEqual(updated.json()["status"], "paused")

    def test_workflow_handoff_and_reconcile_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.dict(
                "os.environ",
                {
                    "UDOS_STATE_ROOT": str(Path(temp_dir) / "state"),
                    "WIZARD_STATE_ROOT": str(Path(temp_dir) / "state" / "wizard"),
                },
                clear=False,
            ):
                self.client.post(
                    "/workflow/state",
                    json={
                        "workflow_id": "mission-beta",
                        "step_id": "step-4",
                        "status": "running",
                        "awaiting_user_action": False,
                    },
                )

                handoff = self.client.post(
                    "/workflow/handoff/automation-job",
                    json={
                        "requested_capability": "render-export",
                        "payload_ref": "workflow://mission-beta/step-4",
                        "policy_flags": {"requires_online": False},
                    },
                )
                self.assertEqual(handoff.status_code, 200)
                handoff_payload = handoff.json()
                self.assertEqual(handoff_payload["requested_capability"], "render-export")
                self.assertEqual(handoff_payload["policy_flags"]["workflow_id"], "mission-beta")
                self.assertEqual(handoff_payload["policy_flags"]["step_id"], "step-4")

                reconciled = self.client.post(
                    "/workflow/reconcile/automation-result",
                    json={
                        "job_id": handoff_payload["job_id"],
                        "status": "completed",
                        "suggested_workflow_action": "advance",
                        "workflow_id": "mission-beta",
                        "output_refs": ["memory://rendered/web-prose/mission-beta/index.html"],
                    },
                )
                self.assertEqual(reconciled.status_code, 200)
                reconcile_payload = reconciled.json()
                self.assertEqual(reconcile_payload["state"]["workflow_id"], "mission-beta")
                self.assertEqual(reconcile_payload["state"]["status"], "running")
                self.assertEqual(reconcile_payload["state"]["step_id"], "step-5")

    def test_workflow_reconcile_latest_uhome_result_applies_once(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.dict(
                "os.environ",
                {
                    "UDOS_STATE_ROOT": str(Path(temp_dir) / "state"),
                    "WIZARD_STATE_ROOT": str(Path(temp_dir) / "state" / "wizard"),
                },
                clear=False,
            ):
                self.client.post(
                    "/workflow/state",
                    json={
                        "workflow_id": "mission-gamma",
                        "step_id": "step-2",
                        "status": "running",
                        "awaiting_user_action": False,
                    },
                )
                with patch("wizard.main.reconcile_latest_workflow_result") as mock_reconcile:
                    mock_reconcile.return_value = {
                        "contract_version": "v2.0.4",
                        "status": "applied",
                        "state": {"workflow_id": "mission-gamma", "step_id": "step-3", "status": "running"},
                    }
                    response = self.client.post(
                        "/workflow/reconcile/uhome-latest",
                        json={"workflow_id": "mission-gamma"},
                    )
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.json()["status"], "applied")

    def test_uhome_bridge_proxy_and_dispatch_routes(self) -> None:
        with patch("wizard.main.fetch_uhome_bridge_status") as mock_bridge_status:
            mock_bridge_status.return_value = {
                "configured_url": "http://127.0.0.1:8000",
                "connected": True,
                "automation": {"queued_jobs": 1},
            }
            response = self.client.get("/uhome/bridge/status")
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json()["connected"])

        with patch("wizard.main.fetch_uhome_automation_status") as mock_status:
            mock_status.return_value = {"owner": "uHOME-server", "queued_jobs": 2, "recorded_results": 1}
            response = self.client.get("/uhome/automation/status")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["queued_jobs"], 2)

        with patch("wizard.main.fetch_uhome_automation_results") as mock_results:
            mock_results.return_value = {"items": [{"job_id": "job:test", "status": "completed"}]}
            response = self.client.get("/uhome/automation/results")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["items"][0]["job_id"], "job:test")

        with patch("wizard.main.cancel_uhome_automation_job") as mock_cancel:
            mock_cancel.return_value = {"cancelled": {"status": "cancelled", "job_id": "job:test"}}
            response = self.client.post("/uhome/automation/jobs/job:test/cancel")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["cancelled"]["status"], "cancelled")

        with patch("wizard.main.retry_uhome_automation_job") as mock_retry:
            mock_retry.return_value = {"retried": {"status": "queued", "retried_from": "job:test"}}
            response = self.client.post("/uhome/automation/results/job:test/retry")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["retried"]["status"], "queued")

        with patch("wizard.main.process_next_uhome_automation_job") as mock_process:
            mock_process.return_value = {
                "bridge": {"configured_url": "http://127.0.0.1:8000"},
                "processed": {"status": "processed", "job": {"job_id": "job:test"}},
            }
            response = self.client.post("/uhome/automation/process-next", json={"status": "completed"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["processed"]["status"], "processed")

        with patch("wizard.main.dispatch_workflow_automation_job") as mock_dispatch:
            mock_dispatch.return_value = {
                "bridge": {"configured_url": "http://127.0.0.1:8000"},
                "job": {"job_id": "job:test"},
                "accepted": {"job_id": "job:test"},
            }
            response = self.client.post(
                "/workflow/handoff/automation-job/dispatch",
                json={"requested_capability": "render-export"},
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["accepted"]["job_id"], "job:test")

    def test_render_contract_route_exposes_core_owned_render_contract(self) -> None:
        response = self.client.get("/render/contract")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["version"], "v2.0.3")
        self.assertEqual(payload["owner"], "uDOS-core")
        targets = {entry["id"] for entry in payload["targets"]}
        self.assertIn("gui-preview", targets)
        self.assertIn("email-html", targets)

    def test_render_presets_route_lists_prose_and_skin_maps(self) -> None:
        response = self.client.get("/render/presets")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        preset_ids = {entry["id"] for entry in payload["prose_presets"]}
        self.assertIn("prose-default", preset_ids)
        skin_ids = {entry["skin_id"] for entry in payload["gameplay_skins"]}
        self.assertIn("expedition-journal", skin_ids)

    def test_render_preview_route_returns_semantic_html_and_theme_refs(self) -> None:
        response = self.client.post(
            "/render/preview",
            json={
                "target": "web-prose",
                "markdown": "---\ntitle: Demo\ntheme_adapter: public-sunset-prose\n---\n# Heading\n\nBody copy.\n",
                "metadata": {"prose_preset": "prose-reference"},
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["title"], "Demo")
        self.assertEqual(payload["theme_adapter"], "public-sunset-prose")
        self.assertEqual(payload["prose_preset"], "prose-reference")
        self.assertIn("<h1>Heading</h1>", payload["html"])

    def test_render_export_route_writes_manifest_and_output(self) -> None:
        response = self.client.post(
            "/render/export",
            json={
                "target": "web-prose",
                "markdown": "---\ntitle: Exported Page\n---\n# Exported Page\n\nSaved body.\n",
                "metadata": {"prose_preset": "prose-default"},
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["manifest"]["target"], "web-prose")
        self.assertTrue(payload["manifest"]["output_path"].endswith("index.html"))

    def test_render_exports_route_lists_saved_outputs(self) -> None:
        response = self.client.get("/render/exports")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("exports", payload)
        self.assertIsInstance(payload["exports"], list)

    def test_render_export_detail_route_returns_manifest_lookup(self) -> None:
        self.client.post(
            "/render/export",
            json={
                "target": "web-prose",
                "markdown": "---\ntitle: Detail Page\n---\n# Detail Page\n\nSaved body.\n",
                "metadata": {"prose_preset": "prose-default"},
            },
        )
        response = self.client.get("/render/exports/web-prose/detail-page")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["found"])
        self.assertEqual(payload["manifest"]["slug"], "detail-page")

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
        self.assertTrue(payload["orchestration_contract_source"].endswith("uDOS-wizard/contracts/orchestration-contract.json"))
        self.assertEqual(payload["orchestration_contract_version"], "v2.0.2")
        self.assertTrue(payload["result_store_path"].endswith(".udos/state/wizard/orchestration-results.json"))
        self.assertEqual(payload["result_store_mode"], "file-json")
        services = {service["service"] for service in payload["services"]}
        self.assertIn("assist", services)
        runtime_services = {service["key"] for service in payload["runtime_services"]}
        self.assertIn("runtime.capability-registry", runtime_services)

    def test_orchestration_status_respects_overridden_result_store_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["WIZARD_RESULT_STORE_PATH"] = str(Path(temp_dir) / "results.json")
            try:
                payload = OrchestrationRegistry().status()
            finally:
                os.environ.pop("WIZARD_RESULT_STORE_PATH", None)
            self.assertEqual(payload["result_store_path"], str((Path(temp_dir) / "results.json").resolve()))

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
        self.assertEqual(payload["callback_contract"]["route"], "/orchestration/callback")

    def test_orchestration_workflow_plan_returns_shared_steps(self) -> None:
        response = self.client.get(
            "/orchestration/workflow-plan",
            params={"objective": "shared-remote-flow", "mode": "auto"},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["plan_version"], "v2.0.2")
        self.assertEqual(payload["step_count"], 2)
        self.assertTrue(payload["contract_source"].endswith("uDOS-wizard/contracts/orchestration-contract.json"))
        surfaces = {step["surface"] for step in payload["steps"]}
        self.assertIn("remote-control", surfaces)
        self.assertIn("sync", surfaces)

    def test_orchestration_callback_and_result_round_trip(self) -> None:
        dispatch = self.client.get(
            "/orchestration/dispatch",
            params={"task": "remote-control", "mode": "auto", "surface": "remote-control"},
        ).json()
        dispatch_id = dispatch["dispatch_id"]

        callback = self.client.post(
            "/orchestration/callback",
            json={
                "dispatch_id": dispatch_id,
                "status": "completed",
                "result": {"summary": "ok"},
            },
        )
        self.assertEqual(callback.status_code, 200)
        callback_payload = callback.json()
        self.assertEqual(callback_payload["dispatch_id"], dispatch_id)
        self.assertEqual(callback_payload["status"], "completed")
        self.assertEqual(callback_payload["callback_version"], "v2.0.2")

        result = self.client.get(f"/orchestration/result/{dispatch_id}")
        self.assertEqual(result.status_code, 200)
        result_payload = result.json()
        self.assertEqual(result_payload["dispatch_id"], dispatch_id)
        self.assertEqual(result_payload["status"], "completed")
        self.assertEqual(result_payload["result"]["summary"], "ok")

    def test_orchestration_result_store_persists_across_registry_instances(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store_path = Path(temp_dir) / "orchestration-results.json"
            writer = OrchestrationRegistry(result_store_path=store_path)
            payload = writer.record_result(
                dispatch_id="dispatch:remote-control:auto",
                status="completed",
                result={"summary": "persisted"},
            )
            self.assertEqual(payload["result"]["summary"], "persisted")

            reader = OrchestrationRegistry(result_store_path=store_path)
            restored = reader.get_result("dispatch:remote-control:auto")
            self.assertEqual(restored["status"], "completed")
            self.assertEqual(restored["result"]["summary"], "persisted")

    def test_local_state_routes_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.dict(
                "os.environ",
                {
                    "UDOS_STATE_ROOT": str(Path(temp_dir) / "state"),
                    "WIZARD_STATE_ROOT": str(Path(temp_dir) / "state" / "wizard"),
                },
                clear=False,
            ):
                response = self.client.get("/config/local-state")
                self.assertEqual(response.status_code, 200)
                payload = response.json()
                self.assertTrue(payload["install_id"].startswith("udos-"))

                updated = self.client.post(
                    "/config/local-state",
                    json={"user": {"name": "fred", "role": "admin"}, "preferences": {"viewport": "120x40"}},
                )
                self.assertEqual(updated.status_code, 200)
                body = updated.json()
                self.assertEqual(body["user"]["name"], "fred")
                self.assertEqual(body["preferences"]["viewport"], "120x40")

    def test_secret_routes_round_trip_and_runtime_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.dict(
                "os.environ",
                {
                    "UDOS_STATE_ROOT": str(Path(temp_dir) / "state"),
                    "WIZARD_STATE_ROOT": str(Path(temp_dir) / "state" / "wizard"),
                },
                clear=False,
            ):
                created = self.client.post(
                    "/config/secrets",
                    json={"key": "OPENAI_API_KEY", "value": "super-secret"},
                )
                self.assertEqual(created.status_code, 200)
                self.assertEqual(created.json()["status"], "ok")

                listed = self.client.get("/config/secrets")
                self.assertEqual(listed.status_code, 200)
                self.assertEqual(listed.json()["count"], 1)
                self.assertEqual(listed.json()["keys"][0]["key"], "OPENAI_API_KEY")

                presence = self.client.get("/config/secrets/OPENAI_API_KEY")
                self.assertEqual(presence.status_code, 200)
                self.assertTrue(presence.json()["present"])

                runtime = self.client.get("/config/runtime", params={"key": "OPENAI_API_KEY"})
                self.assertEqual(runtime.status_code, 200)
                runtime_payload = runtime.json()
                self.assertTrue(runtime_payload["present"])
                self.assertTrue(runtime_payload["is_secret"])
                self.assertEqual(runtime_payload["source"], "secret-store")
                self.assertIsNone(runtime_payload["value"])


if __name__ == "__main__":
    unittest.main()
