from __future__ import annotations


def mcp_split_policy() -> dict:
    """Canonical MCP split for v2 ownership boundaries."""

    return {
        "status": "ok",
        "version": "v2",
        "ownership": {
            "core": {
                "owns": [
                    "typed tool request/response schemas",
                    "local policy validation",
                    "deterministic execution gating",
                    "offline-safe local MCP client use",
                ],
                "must_not_own": [
                    "managed external MCP bridge/server lifecycle",
                    "network routing control plane",
                    "live network scheduling",
                ],
            },
            "wizard": {
                "owns": [
                    "managed MCP bridge/server lifecycle",
                    "registry and auth binding",
                    "budget-aware MCP routing",
                    "deferred queue execution",
                    "retry and cooldown behavior",
                    "scheduled MCP runs",
                    "managed MCP audit",
                ],
                "must_not_own": [
                    "canonical local runtime command authority",
                ],
            },
            "dev": {
                "owns": [
                    "mock MCP servers",
                    "schema fixtures",
                    "registration test rigs",
                    "failure and rate-limit simulations",
                    "promotion harnesses",
                ],
                "must_not_own": [
                    "release runtime behavior",
                ],
            },
        },
        "rule": "local offline-safe deterministic tools may be invoked by Core; managed networked scheduled or budgeted tools are Wizard-owned",
    }
