from __future__ import annotations

import json
from pathlib import Path


def _runtime_service_source() -> Path:
    return Path(__file__).resolve().parents[2] / "uDOS-core" / "contracts" / "runtime-services.json"


def _orchestration_contract_source() -> Path:
    return Path(__file__).resolve().parents[1] / "contracts" / "orchestration-contract.json"


def _load_runtime_services() -> dict:
    return json.loads(_runtime_service_source().read_text(encoding="utf-8"))


def _load_orchestration_contract() -> dict:
    return json.loads(_orchestration_contract_source().read_text(encoding="utf-8"))


class OrchestrationRegistry:
    def __init__(self) -> None:
        self._results: dict[str, dict] = {}

    def status(self) -> dict:
        manifest = _load_runtime_services()
        contract = _load_orchestration_contract()
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
            "orchestration_contract_source": str(_orchestration_contract_source()),
            "orchestration_contract_version": contract["version"],
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

    def workflow_plan(self, objective: str, mode: str = "auto") -> dict:
        contract = _load_orchestration_contract()
        steps = [
            route_task(task="remote-control", mode=mode, surface="remote-control"),
            route_task(task="google-workspace-mirror", mode=mode, surface="sync"),
        ]
        return {
            "plan_version": contract["workflow_plan_contract"]["plan_version"],
            "objective": objective,
            "mode": mode,
            "owner": "uDOS-wizard",
            "contract_source": str(_orchestration_contract_source()),
            "steps": steps,
            "step_count": len(steps),
        }

    def record_result(self, dispatch_id: str, status: str = "completed", result: dict | None = None) -> dict:
        contract = _load_orchestration_contract()
        payload = {
            "dispatch_id": dispatch_id,
            "status": status,
            "result": result or {},
            "callback_version": contract["callback_contract"]["callback_version"],
            "result_route": contract["routes"]["result"]["path_template"].replace("{dispatch_id}", dispatch_id),
        }
        self._results[dispatch_id] = payload
        return payload

    def get_result(self, dispatch_id: str) -> dict:
        payload = self._results.get(dispatch_id)
        if payload is None:
            return {
                "dispatch_id": dispatch_id,
                "status": "missing",
                "result": {},
                "callback_version": _load_orchestration_contract()["callback_contract"]["callback_version"],
                "result_route": _load_orchestration_contract()["routes"]["result"]["path_template"].replace(
                    "{dispatch_id}", dispatch_id
                ),
            }
        return payload


def _usage_for_service(key: str) -> str:
    if key == "runtime.capability-registry":
        return "provider and assist routing metadata"
    if key == "runtime.release-lanes":
        return "promotion-aware orchestration reporting"
    return "shared platform contract consumption"


def route_task(task: str, mode: str = "auto", surface: str = "assist") -> dict:
    contract = _load_orchestration_contract()
    request = {"task": task, "mode": mode, "surface": surface}
    callback_contract = {
        "owner": "uDOS-wizard",
        "method": contract["routes"]["callback"]["method"],
        "route": contract["routes"]["callback"]["path"],
        "result_route_template": contract["routes"]["result"]["path_template"],
    }

    if mode == "offline":
        return {
            "dispatch_version": contract["dispatch_contract"]["dispatch_version"],
            "request": request,
            "dispatch_id": f"dispatch:{surface}:{task}:{mode}",
            "provider": "local-fallback",
            "executor": "local-shell",
            "transport": "subprocess",
            "status": "queued",
            "route_contract": {"owner": "uDOS-wizard", "surface": surface, "mode": mode},
            "callback_contract": callback_contract,
            **request,
        }

    if surface == "publish":
        return {
            "dispatch_version": contract["dispatch_contract"]["dispatch_version"],
            "request": request,
            "dispatch_id": f"dispatch:{surface}:{task}:{mode}",
            "provider": "wizard-provider",
            "executor": "publish-runner",
            "transport": "job-queue",
            "status": "queued",
            "route_contract": {"owner": "uDOS-wizard", "surface": surface, "mode": mode},
            "callback_contract": callback_contract,
            **request,
        }

    return {
        "dispatch_version": contract["dispatch_contract"]["dispatch_version"],
        "request": request,
        "dispatch_id": f"dispatch:{surface}:{task}:{mode}",
        "provider": "wizard-provider",
        "executor": "provider-router",
        "transport": "https",
        "status": "queued",
        "route_contract": {"owner": "uDOS-wizard", "surface": surface, "mode": mode},
        "callback_contract": callback_contract,
        **request,
    }
