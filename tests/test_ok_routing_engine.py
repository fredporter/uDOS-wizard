from __future__ import annotations

import unittest

from wizard.ok.provider_registry import ProviderRegistry
from wizard.ok.routing_engine import OKProviderRoutingEngine


class OKRoutingEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = OKProviderRoutingEngine(ProviderRegistry())

    def test_offline_sufficient_routes_local(self) -> None:
        decision = self.engine.route({"task": "summarize notes", "offline_sufficient": True})
        self.assertEqual(decision["status"], "local")
        self.assertEqual(decision["provider_id"], "core.offline")

    def test_cache_hit_routes_from_cache(self) -> None:
        decision = self.engine.route({"task_class": "analysis", "cache_hit": True})
        self.assertEqual(decision["status"], "cache-hit")
        self.assertEqual(decision["provider_id"], "wizard.cache")

    def test_summary_prefers_low_cost_provider(self) -> None:
        decision = self.engine.route(
            {
                "task_class": "summarize",
                "allowed_budget_groups": ["tier0_free", "tier1_economy"],
            }
        )
        self.assertEqual(decision["status"], "routed")
        self.assertEqual(decision["provider_id"], "wizard.mistral")

    def test_code_routes_to_openrouter(self) -> None:
        decision = self.engine.route({"task_class": "code"})
        self.assertEqual(decision["status"], "routed")
        self.assertEqual(decision["provider_id"], "wizard.openrouter")

    def test_budget_block_can_defer(self) -> None:
        decision = self.engine.route(
            {
                "task_class": "code",
                "allowed_budget_groups": ["tier0_free"],
            }
        )
        self.assertEqual(decision["status"], "deferred")
        self.assertTrue(decision["deferred"])
        self.assertEqual(decision["reason"], "no-eligible-provider")


if __name__ == "__main__":
    unittest.main()
