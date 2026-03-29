from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


def _ensure_core_on_path() -> None:
    core_root = Path(__file__).resolve().parents[2] / "uDOS-core"
    core_root_str = str(core_root)
    if core_root.exists() and core_root_str not in sys.path:
        sys.path.insert(0, core_root_str)


_ensure_core_on_path()

from udos_core.dev_config import get_path


DEFAULT_WORKFLOW_ID = "surface-default"
DEFAULT_STEP_ID = "step-1"


def _utc_now_iso_z() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _workflow_state_path() -> Path:
    return get_path("WIZARD_STATE_ROOT") / "workflow-state.json"


def _workflow_actions_path() -> Path:
    return get_path("WIZARD_STATE_ROOT") / "workflow-actions.json"


def _workflow_reconciled_jobs_path() -> Path:
    return get_path("WIZARD_STATE_ROOT") / "workflow-reconciled-jobs.json"


def _read_json_dict(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return dict(default)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return dict(default)
    return payload if isinstance(payload, dict) else dict(default)


def _read_json_list(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    if not isinstance(payload, list):
        return []
    return [item for item in payload if isinstance(item, dict)]


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def default_workflow_state() -> dict[str, Any]:
    now = _utc_now_iso_z()
    return {
        "contract_version": "v2.0.4",
        "workflow_id": DEFAULT_WORKFLOW_ID,
        "step_id": DEFAULT_STEP_ID,
        "status": "draft",
        "awaiting_user_action": True,
        "last_transition_at": now,
        "origin_surface": "surface",
    }


def _apply_action_defaults(action: str, state: dict[str, Any]) -> dict[str, Any]:
    mapping = {
        "advance": {"status": "running", "awaiting_user_action": False},
        "resume": {"status": "running", "awaiting_user_action": False},
        "approve": {"status": "running", "awaiting_user_action": False},
        "pause": {"status": "paused", "awaiting_user_action": True},
        "reject": {"status": "blocked", "awaiting_user_action": True},
        "request-assist": {"status": "blocked", "awaiting_user_action": True},
        "replan": {"status": "paused", "awaiting_user_action": True},
    }
    next_values = dict(mapping.get(action, {}))
    if action == "advance":
        current_step = str(state.get("step_id") or DEFAULT_STEP_ID)
        if current_step.startswith("step-"):
            try:
                next_values["step_id"] = f"step-{int(current_step.split('-', 1)[1]) + 1}"
            except ValueError:
                next_values["step_id"] = current_step
    return next_values


class WorkflowStateStore:
    def __init__(
        self,
        state_path: Path | None = None,
        actions_path: Path | None = None,
        reconciled_jobs_path: Path | None = None,
    ) -> None:
        self._state_path = state_path or _workflow_state_path()
        self._actions_path = actions_path or _workflow_actions_path()
        self._reconciled_jobs_path = reconciled_jobs_path or _workflow_reconciled_jobs_path()

    def get_state(self) -> dict[str, Any]:
        return _read_json_dict(self._state_path, default_workflow_state())

    def update_state(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = self.get_state()
        state.update({key: value for key, value in payload.items() if value is not None})
        state["contract_version"] = "v2.0.4"
        state["last_transition_at"] = _utc_now_iso_z()
        _write_json(self._state_path, state)
        return state

    def list_actions(self) -> dict[str, Any]:
        items = _read_json_list(self._actions_path)
        return {"contract_version": "v2.0.4", "count": len(items), "items": items}

    def _reconciled_job_ids(self) -> list[str]:
        items = _read_json_list(self._reconciled_jobs_path)
        return [str(item.get("job_id")) for item in items if item.get("job_id")]

    def _mark_reconciled_job(self, job_id: str) -> None:
        items = _read_json_list(self._reconciled_jobs_path)
        if any(item.get("job_id") == job_id for item in items):
            return
        items.append({"job_id": job_id, "reconciled_at": _utc_now_iso_z()})
        _write_json(self._reconciled_jobs_path, items)

    def record_action(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = self.get_state()
        action = {
            "contract_version": "v2.0.4",
            "workflow_id": payload.get("workflow_id") or state["workflow_id"],
            "action": payload.get("action") or "advance",
            "requested_by": payload.get("requested_by") or "surface-ui",
            "requested_at": payload.get("requested_at") or _utc_now_iso_z(),
            "policy_flags": payload.get("policy_flags") or {},
            "origin_surface": payload.get("origin_surface") or "surface",
        }
        items = _read_json_list(self._actions_path)
        items.append(action)
        _write_json(self._actions_path, items)

        next_state = dict(state)
        next_state.update(_apply_action_defaults(action["action"], state))
        overrides = payload.get("state_overrides") or {}
        if isinstance(overrides, dict):
            next_state.update(overrides)
        next_state["workflow_id"] = action["workflow_id"]
        next_state["origin_surface"] = action["origin_surface"]
        updated_state = self.update_state(next_state)
        return {"action": action, "state": updated_state}

    def build_automation_job(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = self.get_state()
        capability = payload.get("requested_capability") or "local-task"
        workflow_id = payload.get("workflow_id") or state["workflow_id"]
        step_id = payload.get("step_id") or state["step_id"]
        job_id = payload.get("job_id") or f"job:{workflow_id}:{step_id}:{capability}"
        return {
            "contract_version": "v2.0.4",
            "job_id": job_id,
            "requested_capability": capability,
            "payload_ref": payload.get("payload_ref") or f"workflow://{workflow_id}/{step_id}",
            "origin_surface": payload.get("origin_surface") or "uDOS-wizard",
            "policy_flags": {
                **(payload.get("policy_flags") or {}),
                "workflow_id": workflow_id,
                "step_id": step_id,
            },
            "queued_at": payload.get("queued_at") or _utc_now_iso_z(),
        }

    def reconcile_automation_result(self, payload: dict[str, Any]) -> dict[str, Any]:
        status = str(payload.get("status") or "completed")
        job_id = str(payload.get("job_id") or "job:unknown")
        if job_id in self._reconciled_job_ids():
            state = self.get_state()
            return {
                "contract_version": "v2.0.4",
                "status": "noop",
                "reason": "already-reconciled",
                "result": {
                    "job_id": job_id,
                    "status": status,
                    "suggested_workflow_action": payload.get("suggested_workflow_action") or "advance",
                },
                "state": state,
            }
        suggested_action = str(payload.get("suggested_workflow_action") or "advance")
        action_result = self.record_action(
            {
                "workflow_id": payload.get("workflow_id") or self.get_state()["workflow_id"],
                "action": suggested_action,
                "requested_by": payload.get("requested_by") or "uHOME-server",
                "policy_flags": {"automation_job_id": job_id, "automation_status": status},
                "origin_surface": payload.get("origin_surface") or "uHOME-server",
            }
        )
        state = dict(action_result["state"])
        if status == "failed":
            state = self.update_state(
                {
                    **state,
                    "status": "blocked",
                    "awaiting_user_action": True,
                    "origin_surface": payload.get("origin_surface") or "uHOME-server",
                }
            )
        self._mark_reconciled_job(job_id)
        return {
            "contract_version": "v2.0.4",
            "status": "applied",
            "result": {
                "job_id": job_id,
                "status": status,
                "output_refs": payload.get("output_refs") or [],
                "event_refs": payload.get("event_refs") or [],
                "completed_at": payload.get("completed_at") or _utc_now_iso_z(),
                "suggested_workflow_action": suggested_action,
            },
            "state": state,
            "recorded_action": action_result["action"],
        }


def get_workflow_store() -> WorkflowStateStore:
    return WorkflowStateStore()
