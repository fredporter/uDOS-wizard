from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any
from urllib import error, request


def _ensure_core_on_path() -> None:
    core_root = Path(__file__).resolve().parents[2] / "uDOS-core"
    core_root_str = str(core_root)
    if core_root.exists() and core_root_str not in sys.path:
        sys.path.insert(0, core_root_str)


_ensure_core_on_path()

from udos_core.dev_config import get_str

from .workflow_state import get_workflow_store


DEFAULT_UHOME_SERVER_URL = "http://127.0.0.1:8000"


def get_uhome_server_url() -> str:
    return get_str("UHOME_SERVER_URL", DEFAULT_UHOME_SERVER_URL).rstrip("/")


def _fetch_json(method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    base_url = get_uhome_server_url()
    url = f"{base_url}{path}"
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = request.Request(url, data=data, headers=headers, method=method)
    with request.urlopen(req, timeout=2) as response:
        raw = response.read().decode("utf-8")
    return json.loads(raw) if raw else {}


def bridge_status() -> dict[str, Any]:
    base_url = get_uhome_server_url()
    try:
        automation = _fetch_json("GET", "/api/runtime/automation/status")
        return {"configured_url": base_url, "connected": True, "automation": automation}
    except (error.URLError, ValueError, json.JSONDecodeError) as exc:
        return {"configured_url": base_url, "connected": False, "error": str(exc)}


def automation_status() -> dict[str, Any]:
    return _fetch_json("GET", "/api/runtime/automation/status")


def automation_jobs() -> dict[str, Any]:
    return _fetch_json("GET", "/api/runtime/automation/jobs")


def automation_results() -> dict[str, Any]:
    return _fetch_json("GET", "/api/runtime/automation/results")


def dispatch_workflow_automation_job(payload: dict[str, Any]) -> dict[str, Any]:
    job_payload = get_workflow_store().build_automation_job(payload)
    accepted = _fetch_json("POST", "/api/runtime/automation/jobs", job_payload)
    return {
        "bridge": {"configured_url": get_uhome_server_url(), "path": "/api/runtime/automation/jobs"},
        "job": job_payload,
        "accepted": accepted,
    }


def process_next_automation_job(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    processed = _fetch_json("POST", "/api/runtime/automation/process-next", payload or {})
    return {
        "bridge": {"configured_url": get_uhome_server_url(), "path": "/api/runtime/automation/process-next"},
        "processed": processed,
    }


def cancel_automation_job(job_id: str) -> dict[str, Any]:
    cancelled = _fetch_json("POST", f"/api/runtime/automation/jobs/{job_id}/cancel")
    return {
        "bridge": {"configured_url": get_uhome_server_url(), "path": f"/api/runtime/automation/jobs/{job_id}/cancel"},
        "cancelled": cancelled,
    }


def retry_automation_job(job_id: str) -> dict[str, Any]:
    retried = _fetch_json("POST", f"/api/runtime/automation/results/{job_id}/retry")
    return {
        "bridge": {"configured_url": get_uhome_server_url(), "path": f"/api/runtime/automation/results/{job_id}/retry"},
        "retried": retried,
    }


def reconcile_latest_workflow_result(workflow_id: str | None = None) -> dict[str, Any]:
    store = get_workflow_store()
    active_state = store.get_state()
    target_workflow_id = workflow_id or active_state["workflow_id"]
    payload = automation_results()
    items = payload.get("items", []) if isinstance(payload, dict) else []
    for item in reversed(items):
        if item.get("workflow_id") and item.get("workflow_id") != target_workflow_id:
            continue
        if item.get("status") not in {"completed", "failed"}:
            continue
        enriched = dict(item)
        enriched["workflow_id"] = enriched.get("workflow_id") or target_workflow_id
        return store.reconcile_automation_result(enriched)
    return {
        "contract_version": "v2.0.4",
        "status": "noop",
        "reason": "no-reconcilable-result",
        "state": active_state,
    }
