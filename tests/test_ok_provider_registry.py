from __future__ import annotations

import unittest

from wizard.ok.provider_registry import ProviderRegistry


class OKProviderRegistryTests(unittest.TestCase):
    def test_registry_loads_default_provider_manifests(self) -> None:
        registry = ProviderRegistry()
        provider_ids = set(registry.provider_ids())

        self.assertIn("wizard.anthropic", provider_ids)
        self.assertIn("wizard.openai", provider_ids)
        self.assertIn("wizard.openrouter", provider_ids)
        self.assertIn("wizard.mistral", provider_ids)
        self.assertIn("wizard.gemini", provider_ids)

    def test_capability_filter_returns_matching_providers(self) -> None:
        registry = ProviderRegistry()
        providers = registry.list_providers(capability="multimodal")
        provider_ids = {item["provider_id"] for item in providers}

        self.assertIn("wizard.openai", provider_ids)
        self.assertIn("wizard.gemini", provider_ids)

    def test_unknown_provider_returns_none(self) -> None:
        registry = ProviderRegistry()
        self.assertIsNone(registry.get_provider("wizard.unknown"))


if __name__ == "__main__":
    unittest.main()
