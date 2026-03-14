from __future__ import annotations

import json
from pathlib import Path


def _runtime_service_source() -> Path:
    return Path(__file__).resolve().parents[2] / "uDOS-core" / "contracts" / "runtime-services.json"


def _load_runtime_services() -> dict:
    return json.loads(_runtime_service_source().read_text(encoding="utf-8"))


class OrchestrationRegistry:
    def status(self) -> dict:
        manifest = _load_runtime_services()
        runtime_services = []
        for service in manifest["services"]:
            if "uDOS-wizard" not in service.get("consumers", []):
                continue
            runtime_services.append(
                {
                    "key": service["key"],
                    "owner": service["owner"],
                    "route": service["route"],
                    "stability": service["stability"],
                    "consumer": "uDOS-wizard",
                    "usage": _usage_for_service(service["key"]),
                }
            )
        return {
            "version": manifest["version"],
            "foundation_version": manifest["extends"],
            "runtime_service_source": str(_runtime_service_source()),
            "runtime_services": runtime_services,
            "services": [
                {
                    "service": "assist",
                    "executor": "provider-router",
                    "transport": "https",
                },
                {
                    "service": "publish",
                    "executor": "publish-runner",
                    "transport": "job-queue",
                },
                {
                    "service": "local-tools",
                    "executor": "local-shell",
                    "transport": "subprocess",
                },
            ],
            "providers": ["wizard-provider", "local-fallback"],
            "mcp_bridge": "starter",
        }

    def route(self, task: str, mode: str = "auto", surface: str = "assist") -> dict:
        return route_task(task=task, mode=mode, surface=surface)


def _usage_for_service(key: str) -> str:
    if key == "runtime.capability-registry":
        return "provider and assist routing metadata"
    if key == "runtime.release-lanes":
        return "promotion-aware orchestration reporting"
    return "shared platform contract consumption"


def route_task(task: str, mode: str = "auto", surface: str = "assist") -> dict:
    request = {"task": task, "mode": mode, "surface": surface}

    if mode == "offline":
        return {
            "dispatch_version": "v2.0.2",
            "request": request,
            "dispatch_id": f"dispatch:{surface}:{task}:{mode}",
            "provider": "local-fallback",
            "executor": "local-shell",
            "transport": "subprocess",
            "status": "queued",
            "route_contract": {"owner": "uDOS-wizard", "surface": surface, "mode": mode},
            **request,
        }

    if surface == "publish":
        return {
            "dispatch_version": "v2.0.2",
            "request": request,
            "dispatch_id": f"dispatch:{surface}:{task}:{mode}",
            "provider": "wizard-provider",
            "executor": "publish-runner",
            "transport": "job-queue",
            "status": "queued",
            "route_contract": {"owner": "uDOS-wizard", "surface": surface, "mode": mode},
            **request,
        }

    return {
        "dispatch_version": "v2.0.2",
        "request": request,
        "dispatch_id": f"dispatch:{surface}:{task}:{mode}",
        "provider": "wizard-provider",
        "executor": "provider-router",
        "transport": "https",
        "status": "queued",
        "route_contract": {"owner": "uDOS-wizard", "surface": surface, "mode": mode},
        **request,
    }
