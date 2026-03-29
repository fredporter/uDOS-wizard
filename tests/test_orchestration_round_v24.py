from __future__ import annotations

import tempfile
import unittest

from wizard.orchestration import OrchestrationRegistry


class OrchestrationV24Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.registry = OrchestrationRegistry(result_store_path=f"{self.tempdir.name}/results.json")
        self.manifest = {
            "version": 1,
            "binder": {
                "id": "footloose-adelaide-launch",
                "type": "campaign",
                "title": "Footloose Adelaide Launch",
            },
            "compile": {
                "id": "compile-footloose-dashboard",
                "target": "dashboard",
                "provider": "wizard",
                "status": "draft",
                "template": "campaign-dashboard",
            },
            "views": [
                {"id": "summary", "kind": "card-grid", "fields": ["title", "status"]},
                {"id": "route_map", "kind": "map", "fields": ["lat", "lng"]},
            ],
        }

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_compile_dispatch_returns_deerflow_preview_payloads(self) -> None:
        payload = self.registry.compile_dispatch(
            self.manifest,
            execution_backend="deerflow",
            execution_mode="preview",
        )
        self.assertEqual(payload["execution_backend"], "deerflow")
        self.assertIn("workflow_preview", payload)
        self.assertIn("graph_preview", payload)
        self.assertIn("result_preview", payload)
        self.assertIn("pin_status", payload)
        self.assertEqual(payload["workflow_preview"]["workflowId"], "compile-footloose-adelaide-launch-compile-footloose-dashboard")
        self.assertEqual(payload["result_preview"]["status"], "dry-run")
        self.assertEqual(payload["status"], "dry-run")

    def test_native_compile_dispatch_records_completed_result_and_publish_queue(self) -> None:
        payload = self.registry.compile_dispatch(self.manifest, execution_backend="native")
        self.assertEqual(payload["status"], "completed")
        result_list = self.registry.list_results(prefix="compile:")
        self.assertEqual(result_list["count"], 1)
        publish_queue = self.registry.publish_queue()
        self.assertEqual(publish_queue["count"], 1)
        self.assertEqual(publish_queue["queue"][0]["status"], "scheduled")

    def test_deerflow_controlled_execution_records_completed_artifacts(self) -> None:
        payload = self.registry.compile_dispatch(
            self.manifest,
            execution_backend="deerflow",
            execution_mode="controlled",
        )
        self.assertEqual(payload["status"], "completed")
        self.assertEqual(payload["execution_mode"], "controlled")
        self.assertEqual(payload["result_preview"]["summary"]["artifactsProduced"], 2)
        publish_queue = self.registry.publish_queue()
        self.assertEqual(publish_queue["queue"][0]["execution_mode"], "controlled")

    def test_compile_dispatch_rejects_view_without_kind(self) -> None:
        broken_manifest = {
            **self.manifest,
            "views": [{"id": "summary"}],
        }
        with self.assertRaisesRegex(ValueError, "compile manifest views\\[0\\]\\.kind is required"):
            self.registry.compile_dispatch(broken_manifest, execution_backend="native")


if __name__ == "__main__":
    unittest.main()
