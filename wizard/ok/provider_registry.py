from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ProviderRegistry:
    """Loads and queries Wizard OK provider manifests."""

    def __init__(self, manifest_root: Path | None = None) -> None:
        self._manifest_root = manifest_root or Path(__file__).resolve().parent / "providers"
        self._providers: dict[str, dict[str, Any]] = {}
        self.refresh()

    def refresh(self) -> None:
        providers: dict[str, dict[str, Any]] = {}
        for manifest_path in sorted(self._manifest_root.glob("*.json")):
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))
            provider_id = str(payload.get("provider_id") or "").strip()
            if not provider_id:
                continue
            payload["manifest_path"] = str(manifest_path)
            providers[provider_id] = payload
        self._providers = providers

    def list_providers(self, capability: str | None = None, enabled_only: bool = True) -> list[dict[str, Any]]:
        required_capability = (capability or "").strip()
        items: list[dict[str, Any]] = []
        for provider in self._providers.values():
            if enabled_only and not bool(provider.get("enabled", True)):
                continue
            capabilities = provider.get("capabilities") or []
            if required_capability and required_capability not in capabilities:
                continue
            items.append(dict(provider))
        return items

    def get_provider(self, provider_id: str) -> dict[str, Any] | None:
        payload = self._providers.get(provider_id)
        return dict(payload) if payload is not None else None

    def provider_ids(self) -> list[str]:
        return sorted(self._providers)

    def budget_groups(self) -> list[str]:
        groups = {str(item.get("budget_group") or "").strip() for item in self._providers.values()}
        groups.discard("")
        return sorted(groups)
