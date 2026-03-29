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
        self._temp_dir = tempfile.TemporaryDirectory()
        temp_root = Path(self._temp_dir.name)
        self._env_patch = patch.dict(
            "os.environ",
            {
                "UDOS_STATE_ROOT": str(temp_root / "state"),
                "WIZARD_STATE_ROOT": str(temp_root / "state" / "wizard"),
                "UDOS_RENDER_ROOT": str(temp_root / "state" / "rendered"),
                "WIZARD_RESULT_STORE_PATH": str(temp_root / "state" / "wizard" / "orchestration-results.json"),
            },
            clear=False,
        )
        self._env_patch.start()
        self.client = TestClient(app)

    def tearDown(self) -> None:
        self._env_patch.stop()
        self._temp_dir.cleanup()

    def test_root_reports_wizard_service(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"service": "wizard", "status": "ok", "role": "broker-and-surface-host"},
        )

    def test_wizard_services_exposes_broker_registry(self) -> None:
        response = self.client.get("/wizard/services")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["broker"], "wizard")
        self.assertGreaterEqual(payload["count"], 3)
        capabilities = {
            capability
            for service in payload["services"]
            for capability in service["capabilities"]
        }
        self.assertIn("ok.transformation", capabilities)
        self.assertIn("surface.preview", capabilities)

    def test_wizard_resolve_delegates_doc_format_to_ubuntu_okd(self) -> None:
        response = self.client.post(
            "/wizard/resolve",
            json={"intent": "format this doc", "payload_ref": "client://capture/1"},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "delegated")
        self.assertEqual(payload["destination_service"], "uDOS-ubuntu")
        self.assertEqual(payload["destination_surface"], "okd")
        self.assertEqual(payload["capability"], "ok.transformation")

    def test_wizard_resolve_returns_help_when_constraints_eliminate_handlers(self) -> None:
        response = self.client.post(
            "/wizard/resolve",
            json={"intent": "format this doc", "offline_only": True},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "help")
        self.assertEqual(payload["capability"], "ok.transformation")

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
        self.assertIn("UDOS_SURFACE_PORT", keys)
        self.assertIn("UDOS_WIZARD_PORT", keys)
        self.assertIn("OPENAI_API_KEY", keys)

    def test_host_contract_route_reports_ubuntu_owned_surface(self) -> None:
        response = self.client.get("/host/contract")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["owner"], "uDOS-ubuntu")
        self.assertEqual(payload["consumer"], "uDOS-wizard")
        self.assertEqual(payload["base_path"], "/host")
        self.assertEqual(payload["proxy_mode"], "wizard-compatibility-bridge")

    def test_host_runtime_summary_route_wraps_config_summary(self) -> None:
        response = self.client.get("/host/runtime-summary")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["owner"], "uDOS-ubuntu")
        self.assertEqual(payload["bridge"], "uDOS-wizard")
        self.assertIn("summary", payload)
        self.assertIn("entries", payload["summary"])

    def test_host_local_state_routes_wrap_local_state_bridge(self) -> None:
        response = self.client.get("/host/local-state")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["owner"], "uDOS-ubuntu")
        self.assertEqual(payload["bridge"], "uDOS-wizard")
        self.assertIn("state", payload)

        updated = self.client.post("/host/local-state", json={"preferences": {"viewport": "publishing"}})
        self.assertEqual(updated.status_code, 200)
        updated_payload = updated.json()
        self.assertEqual(updated_payload["owner"], "uDOS-ubuntu")
        self.assertEqual(updated_payload["state"]["preferences"]["viewport"], "publishing")

    def test_host_secrets_routes_wrap_secret_bridge(self) -> None:
        created = self.client.post("/host/secrets", json={"key": "TEST_HOST_SECRET", "value": "abc"})
        self.assertEqual(created.status_code, 200)
        created_payload = created.json()
        self.assertEqual(created_payload["owner"], "uDOS-ubuntu")
        self.assertEqual(created_payload["key"], "TEST_HOST_SECRET")

        listed = self.client.get("/host/secrets")
        self.assertEqual(listed.status_code, 200)
        listed_payload = listed.json()
        self.assertEqual(listed_payload["owner"], "uDOS-ubuntu")
        keys = {item["key"] for item in listed_payload["keys"]}
        self.assertIn("TEST_HOST_SECRET", keys)

    def test_host_budget_status_route_wraps_budget_bridge(self) -> None:
        response = self.client.get("/host/budget-status")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["owner"], "uDOS-ubuntu")
        self.assertEqual(payload["bridge"], "uDOS-wizard")
        self.assertIn("budget", payload)
        self.assertEqual(payload["budget"]["daily_limit"], 100)

    def test_host_providers_route_wraps_provider_bridge(self) -> None:
        response = self.client.get("/host/providers")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["owner"], "uDOS-ubuntu")
        self.assertEqual(payload["bridge"], "uDOS-wizard")
        self.assertGreaterEqual(payload["count"], 5)
        provider_ids = {item["provider_id"] for item in payload["providers"]}
        self.assertIn("wizard.openai", provider_ids)

    def test_host_orchestration_status_route_wraps_runtime_bridge(self) -> None:
        response = self.client.get("/host/orchestration-status")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["owner"], "uDOS-ubuntu")
        self.assertEqual(payload["bridge"], "uDOS-wizard")
        self.assertIn("orchestration", payload)
        self.assertIn("runtime_services", payload["orchestration"])

    def test_ok_provider_registry_routes_expose_provider_manifests(self) -> None:
        response = self.client.get("/ok/providers")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertGreaterEqual(payload["count"], 5)
        provider_ids = {item["provider_id"] for item in payload["providers"]}
        self.assertIn("wizard.openai", provider_ids)
        self.assertIn("wizard.anthropic", provider_ids)

        detail = self.client.get("/ok/providers/wizard.openai")
        self.assertEqual(detail.status_code, 200)
        detail_payload = detail.json()
        self.assertEqual(detail_payload["provider_id"], "wizard.openai")

    def test_ok_route_returns_budget_aware_decision(self) -> None:
        response = self.client.post(
            "/ok/route",
            json={
                "task": "summarize this changelog",
                "task_class": "summarize",
                "allowed_budget_groups": ["tier0_free", "tier1_economy"],
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("decision", payload)
        self.assertEqual(payload["decision"]["status"], "routed")
        self.assertIn("provider_id", payload["decision"])

    def test_ok_mcp_policy_route_exposes_core_wizard_dev_split(self) -> None:
        response = self.client.get("/ok/mcp-policy")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "ok")
        self.assertIn("core", payload["ownership"])
        self.assertIn("wizard", payload["ownership"])
        self.assertIn("dev", payload["ownership"])

    def test_ok_google_mvp_routes_expose_lane_prompt_and_extraction_contracts(self) -> None:
        lane = self.client.get("/ok/lanes/google-mvp-a")
        self.assertEqual(lane.status_code, 200)
        lane_payload = lane.json()
        self.assertEqual(lane_payload["lane_id"], "google-mvp-a")
        self.assertEqual(lane_payload["provider_entry"]["provider_family"], "wizard.gemini")
        self.assertEqual(
            lane_payload["repo_targets"]["uDOS-empire"],
            "Firestore mirror + Cloud Run binder supervision",
        )

        prompt = self.client.get("/ok/lanes/google-mvp-a/prompt-template")
        self.assertEqual(prompt.status_code, 200)
        prompt_payload = prompt.json()
        self.assertEqual(prompt_payload["provider_hint"], "wizard.gemini")
        self.assertIn("route list", prompt_payload["expected_outputs"])

        extraction = self.client.get("/ok/lanes/google-mvp-a/extraction-checklist")
        self.assertEqual(extraction.status_code, 200)
        extraction_payload = extraction.json()
        self.assertIn("route list", extraction_payload["required_artifacts"])
        self.assertIn("prototype", extraction_payload["promotion_path"])

        generated = self.client.get("/ok/lanes/google-mvp-a/generated-output-example")
        self.assertEqual(generated.status_code, 200)
        generated_payload = generated.json()
        self.assertEqual(generated_payload["service"]["name"], "google-mvp-binder-trigger")
        self.assertEqual(generated_payload["service"]["remote_role"], "firestore-mirror")
        self.assertEqual(generated_payload["routes"][0]["path"], "/binder/google-mvp/mirror")

    def test_mcp_tools_route_lists_live_tools(self) -> None:
        response = self.client.get("/mcp/tools")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertGreaterEqual(payload["count"], 3)
        tool_names = {tool["name"] for tool in payload["tools"]}
        self.assertIn("ok.route", tool_names)
        self.assertIn("ok.providers.list", tool_names)
        self.assertIn("ok.google_mvp.bundle", tool_names)

    def test_mcp_invoke_route_executes_ok_route_tool(self) -> None:
        response = self.client.post(
            "/mcp/tools/ok.route/invoke",
            json={
                "task": "summarize this changelog",
                "task_class": "summarize",
                "allowed_budget_groups": ["tier0_free", "tier1_economy"],
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["invocation"]["tool"]["name"], "ok.route")
        self.assertEqual(payload["invocation"]["result"]["status"], "routed")

    def test_mcp_rpc_tools_call_executes_ok_route_tool(self) -> None:
        response = self.client.post(
            "/mcp",
            json={
                "jsonrpc": "2.0",
                "id": "req-1",
                "method": "tools/call",
                "params": {
                    "name": "ok.route",
                    "arguments": {
                        "task": "summarize this changelog",
                        "task_class": "summarize",
                        "allowed_budget_groups": ["tier0_free", "tier1_economy"],
                    },
                },
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["jsonrpc"], "2.0")
        self.assertEqual(payload["id"], "req-1")
        self.assertEqual(payload["result"]["tool"]["name"], "ok.route")
        self.assertEqual(payload["result"]["result"]["status"], "routed")

    def test_mcp_rpc_initialize_reports_server_info_and_tools_capability(self) -> None:
        response = self.client.post(
            "/mcp",
            json={
                "jsonrpc": "2.0",
                "id": "req-init",
                "method": "initialize",
                "params": {},
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["jsonrpc"], "2.0")
        self.assertEqual(payload["id"], "req-init")
        self.assertEqual(payload["result"]["serverInfo"]["name"], "uDOS Wizard MCP")
        self.assertIn("tools", payload["result"]["capabilities"])

    def test_mcp_rpc_tools_list_reports_live_tools(self) -> None:
        response = self.client.post(
            "/mcp",
            json={
                "jsonrpc": "2.0",
                "id": "req-list",
                "method": "tools/list",
                "params": {},
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["jsonrpc"], "2.0")
        self.assertEqual(payload["id"], "req-list")
        self.assertGreaterEqual(payload["result"]["count"], 3)
        tool_names = {tool["name"] for tool in payload["result"]["tools"]}
        self.assertIn("ok.route", tool_names)
        self.assertIn("ok.providers.list", tool_names)
        self.assertIn("ok.google_mvp.bundle", tool_names)

    def test_mcp_invoke_route_executes_google_mvp_bundle_tool(self) -> None:
        response = self.client.post("/mcp/tools/ok.google_mvp.bundle/invoke", json={})
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["invocation"]["tool"]["name"], "ok.google_mvp.bundle")
        self.assertEqual(payload["invocation"]["result"]["lane_id"], "google-mvp-a")

    def test_uhome_network_policy_contract_and_schema_routes_expose_expected_keys(self) -> None:
        contract = self.client.get("/contracts/uhome/network-policy")
        self.assertEqual(contract.status_code, 200)
        contract_payload = contract.json()
        self.assertEqual(contract_payload["owner"], "uDOS-wizard")
        self.assertEqual(contract_payload["version"], "v2.0.4")
        self.assertIn("beacon", contract_payload["profiles"])
        self.assertEqual(
            contract_payload["routes"]["validate"]["path"],
            "/contracts/uhome/network-policy/validate",
        )

        schema = self.client.get("/contracts/uhome/network-policy/schema")
        self.assertEqual(schema.status_code, 200)
        schema_payload = schema.json()
        self.assertEqual(schema_payload["title"], "WizardToUHomeNetworkPolicy")
        self.assertIn("profile_id", schema_payload["properties"])

    def test_uhome_network_policy_validate_route_accepts_valid_payload_and_rejects_invalid_payload(self) -> None:
        valid = self.client.post(
            "/contracts/uhome/network-policy/validate",
            json={
                "contract_version": "v2.0.4",
                "profile_id": "beacon",
                "network_scope": "public",
                "visibility": "visible",
                "auth_mode": "open",
                "vault_access": "local-only",
                "internet_sharing": "disabled",
                "runtime_owner": "uHOME-server",
                "policy_owner": "uDOS-wizard",
                "consumer_repos": ["uHOME-server", "uDOS-empire"],
                "secret_refs": ["secret://wizard/network/beacon"],
            },
        )
        self.assertEqual(valid.status_code, 200)
        valid_payload = valid.json()
        self.assertTrue(valid_payload["ok"])
        self.assertEqual(valid_payload["profile_id"], "beacon")

        invalid = self.client.post(
            "/contracts/uhome/network-policy/validate",
            json={
                "contract_version": "v2.0.4",
                "profile_id": "tomb",
                "network_scope": "private",
                "visibility": "visible",
                "auth_mode": "password-protected",
                "vault_access": "local-only",
                "internet_sharing": "disabled",
                "runtime_owner": "uHOME-server",
                "policy_owner": "uDOS-wizard",
                "consumer_repos": ["uHOME-server"],
                "secret_refs": [],
            },
        )
        self.assertEqual(invalid.status_code, 400)
        invalid_payload = invalid.json()
        self.assertEqual(invalid_payload["error"], "uhome-network-policy-validation-failed")

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
                self.assertEqual(state.json()["workflow_id"], "surface-default")

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
        self.assertTrue(
            payload["execution_backends_contract_source"].endswith(
                "uDOS-wizard/contracts/execution-backends-contract.json"
            )
        )
        self.assertEqual(payload["orchestration_contract_version"], "v2.0.2")
        self.assertTrue(payload["result_store_path"].endswith("wizard/orchestration-results.json"))
        self.assertEqual(payload["result_store_mode"], "file-json")
        services = {service["service"] for service in payload["services"]}
        self.assertIn("assist", services)
        runtime_services = {service["key"] for service in payload["runtime_services"]}
        self.assertIn("runtime.capability-registry", runtime_services)
        backends = {backend["backend_id"] for backend in payload["execution_backends"]}
        self.assertIn("native", backends)
        self.assertIn("deerflow", backends)

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
        self.assertEqual(payload["execution_backend"], "native")
        self.assertEqual(payload["dispatch_version"], "v2.0.2")
        self.assertEqual(payload["request"]["surface"], "remote-control")
        self.assertEqual(payload["route_contract"]["owner"], "uDOS-wizard")
        self.assertEqual(payload["callback_contract"]["route"], "/orchestration/callback")

    def test_orchestration_dispatch_accepts_deerflow_backend(self) -> None:
        response = self.client.get(
            "/orchestration/dispatch",
            params={
                "task": "long-horizon-plan",
                "mode": "auto",
                "surface": "assist",
                "execution_backend": "deerflow",
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["execution_backend"], "deerflow")
        self.assertEqual(payload["executor"], "deerflow-adapter")
        self.assertTrue(payload["dispatch_id"].endswith(":deerflow"))

    def test_orchestration_dispatch_rejects_unknown_backend(self) -> None:
        response = self.client.get(
            "/orchestration/dispatch",
            params={"task": "demo", "mode": "auto", "surface": "assist", "execution_backend": "unknown"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "unknown execution backend: unknown")

    def test_compile_dispatch_queues_manifest_with_selected_backend(self) -> None:
        response = self.client.post(
            "/compile/dispatch",
            json={
                "execution_backend": "deerflow",
                "execution_mode": "preview",
                "manifest": {
                    "version": 1,
                    "binder": {"id": "footloose-adelaide-launch", "type": "campaign", "title": "Footloose Adelaide Launch"},
                    "compile": {
                        "id": "compile-footloose-dashboard",
                        "target": "dashboard",
                        "template": "campaign-dashboard",
                        "provider": "wizard",
                        "status": "draft",
                    },
                    "views": [{"id": "summary", "kind": "card-grid"}],
                },
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["dispatch_version"], "v2.4")
        self.assertEqual(payload["binder_id"], "footloose-adelaide-launch")
        self.assertEqual(payload["compile_id"], "compile-footloose-dashboard")
        self.assertEqual(payload["execution_backend"], "deerflow")
        self.assertEqual(payload["execution_mode"], "preview")
        self.assertEqual(payload["executor"], "deerflow-adapter")
        self.assertEqual(payload["status"], "dry-run")

    def test_compile_dispatch_runs_controlled_deerflow_execution(self) -> None:
        response = self.client.post(
            "/compile/dispatch",
            json={
                "execution_backend": "deerflow",
                "execution_mode": "controlled",
                "manifest": {
                    "version": 1,
                    "binder": {"id": "footloose-adelaide-launch", "type": "campaign", "title": "Footloose Adelaide Launch"},
                    "compile": {
                        "id": "compile-footloose-dashboard",
                        "target": "dashboard",
                        "template": "campaign-dashboard",
                        "provider": "wizard",
                        "status": "draft",
                    },
                    "views": [{"id": "summary", "kind": "card-grid"}],
                },
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["execution_mode"], "controlled")
        self.assertEqual(payload["status"], "completed")
        self.assertEqual(payload["result_preview"]["summary"]["artifactsProduced"], 1)

    def test_compile_dispatch_rejects_invalid_manifest(self) -> None:
        response = self.client.post(
            "/compile/dispatch",
            json={
                "execution_backend": "native",
                "manifest": {
                    "version": 1,
                    "binder": {"id": "missing-compile", "type": "campaign", "title": "Broken"},
                    "compile": {"target": "dashboard", "provider": "wizard", "status": "draft"},
                    "views": [{"id": "summary", "kind": "card-grid"}],
                },
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "compile manifest compile.id is required")

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
