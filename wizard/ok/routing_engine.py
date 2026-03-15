from __future__ import annotations

from typing import Any

from .provider_registry import ProviderRegistry


CAPABILITY_BY_CLASS = {
    "summarize": "summarization",
    "draft": "drafting",
    "classify": "classification",
    "analysis": "reasoning",
    "research": "reasoning",
    "code": "code_generation",
    "multimodal": "multimodal",
    "transformation": "transformation",
}

DEFAULT_PRIORITY_BY_COMPLEXITY = {
    "L0": ["wizard.mistral", "wizard.openrouter", "wizard.openai"],
    "L1": ["wizard.mistral", "wizard.openrouter", "wizard.openai"],
    "L2": ["wizard.openrouter", "wizard.openai", "wizard.anthropic"],
    "L3": ["wizard.openai", "wizard.anthropic", "wizard.gemini"],
    "L4": ["wizard.anthropic", "wizard.gemini", "wizard.openai"],
}


class OKProviderRoutingEngine:
    """Budget-aware provider selection for managed Wizard OK requests."""

    def __init__(self, registry: ProviderRegistry | None = None) -> None:
        self.registry = registry or ProviderRegistry()

    def classify_request(self, payload: dict[str, Any]) -> str:
        explicit = str(payload.get("task_class") or "").strip().lower()
        if explicit:
            return explicit

        task = str(payload.get("task") or "").strip().lower()
        if "summar" in task:
            return "summarize"
        if "classif" in task:
            return "classify"
        if "draft" in task or "write" in task:
            return "draft"
        if "code" in task or "refactor" in task:
            return "code"
        if "research" in task:
            return "research"
        if "image" in task or "audio" in task or "video" in task:
            return "multimodal"
        return "analysis"

    def complexity_level(self, payload: dict[str, Any], task_class: str) -> str:
        explicit = str(payload.get("complexity") or "").strip().upper()
        if explicit in {"L0", "L1", "L2", "L3", "L4"}:
            return explicit

        if task_class in {"summarize", "classify"}:
            return "L1"
        if task_class in {"draft", "code", "transformation"}:
            return "L2"
        if task_class in {"research", "multimodal"}:
            return "L3"
        return "L3"

    def route(self, payload: dict[str, Any]) -> dict[str, Any]:
        task_class = self.classify_request(payload)
        complexity = self.complexity_level(payload, task_class)

        if bool(payload.get("offline_sufficient", False)):
            return {
                "status": "local",
                "route": "core.offline",
                "provider_id": "core.offline",
                "task_class": task_class,
                "complexity": complexity,
                "reason": "offline_sufficient",
                "deferred": False,
            }

        if bool(payload.get("cache_hit", False)):
            return {
                "status": "cache-hit",
                "route": "wizard.cache",
                "provider_id": "wizard.cache",
                "task_class": task_class,
                "complexity": complexity,
                "reason": "cache_hit",
                "deferred": False,
            }

        required_capability = CAPABILITY_BY_CLASS.get(task_class, "reasoning")
        allowed_budget_groups = set(payload.get("allowed_budget_groups") or [])
        priority = DEFAULT_PRIORITY_BY_COMPLEXITY.get(complexity, DEFAULT_PRIORITY_BY_COMPLEXITY["L3"])

        attempted: list[dict[str, str]] = []
        for provider_id in priority:
            provider = self.registry.get_provider(provider_id)
            if provider is None:
                attempted.append({"provider_id": provider_id, "reason": "missing_manifest"})
                continue
            if not bool(provider.get("enabled", True)):
                attempted.append({"provider_id": provider_id, "reason": "disabled"})
                continue

            capabilities = provider.get("capabilities") or []
            if required_capability not in capabilities:
                attempted.append({"provider_id": provider_id, "reason": "missing_capability"})
                continue

            budget_group = str(provider.get("budget_group") or "")
            if allowed_budget_groups and budget_group not in allowed_budget_groups:
                attempted.append({"provider_id": provider_id, "reason": "budget_blocked"})
                continue

            if bool(provider.get("approval_required", False)) and not bool(payload.get("approval_granted", False)):
                return {
                    "status": "deferred",
                    "task_class": task_class,
                    "complexity": complexity,
                    "required_capability": required_capability,
                    "provider_id": provider_id,
                    "reason": "approval_required",
                    "deferred": True,
                    "schedule_class": "approval_required",
                    "attempted": attempted,
                }

            models = provider.get("models") or []
            return {
                "status": "routed",
                "task_class": task_class,
                "complexity": complexity,
                "required_capability": required_capability,
                "provider_id": provider_id,
                "model": models[0] if models else "n/a",
                "budget_group": budget_group,
                "retry_policy": provider.get("retry_policy", "cooldown_window"),
                "cache_policy": provider.get("cache_policy", "enabled"),
                "deferred": False,
                "attempted": attempted,
            }

        return {
            "status": "deferred",
            "task_class": task_class,
            "complexity": complexity,
            "required_capability": required_capability,
            "reason": "no-eligible-provider",
            "deferred": True,
            "schedule_class": str(payload.get("schedule_class") or "next_window"),
            "attempted": attempted,
        }
