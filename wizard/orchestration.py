from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
import sys


def _ensure_core_on_path() -> None:
    core_root = Path(__file__).resolve().parents[2] / "uDOS-core"
    core_root_str = str(core_root)
    if core_root.exists() and core_root_str not in sys.path:
        sys.path.insert(0, core_root_str)


_ensure_core_on_path()


def _ensure_deerflow_on_path() -> None:
    deerflow_root = (
        Path(__file__).resolve().parents[2]
        / "uDOS-plugin-deerflow"
        / "src/python/udos_plugin_deerflow"
    )
    deerflow_root_str = str(deerflow_root)
    if deerflow_root.exists() and deerflow_root_str not in sys.path:
        sys.path.insert(0, deerflow_root_str)


_ensure_deerflow_on_path()

from udos_core.dev_config import get_path
from udos_core.local_state import ensure_install_id


def _runtime_service_source() -> Path:
    return Path(__file__).resolve().parents[2] / "uDOS-core" / "contracts" / "runtime-services.json"


def _orchestration_contract_source() -> Path:
    return Path(__file__).resolve().parents[1] / "contracts" / "orchestration-contract.json"


def _execution_backends_contract_source() -> Path:
    return Path(__file__).resolve().parents[1] / "contracts" / "execution-backends-contract.json"


def _load_runtime_services() -> dict:
    return json.loads(_runtime_service_source().read_text(encoding="utf-8"))


def _load_orchestration_contract() -> dict:
    return json.loads(_orchestration_contract_source().read_text(encoding="utf-8"))


def _load_execution_backends_contract() -> dict:
    return json.loads(_execution_backends_contract_source().read_text(encoding="utf-8"))


def _known_execution_backends() -> set[str]:
    return {backend["backend_id"] for backend in _load_execution_backends_contract()["backends"]}


def _validate_execution_backend(execution_backend: str) -> None:
    if execution_backend not in _known_execution_backends():
        raise ValueError(f"unknown execution backend: {execution_backend}")


def _validate_execution_mode(execution_mode: str) -> None:
    if execution_mode not in {"preview", "controlled"}:
        raise ValueError(f"unknown execution mode: {execution_mode}")


def _validate_compile_manifest(manifest: dict) -> None:
    if not isinstance(manifest, dict):
        raise ValueError("compile manifest must be an object")

    binder_data = manifest.get("binder")
    compile_data = manifest.get("compile")
    views = manifest.get("views")

    if manifest.get("version") != 1:
        raise ValueError("compile manifest version must be 1")
    if not isinstance(binder_data, dict) or not binder_data.get("id"):
        raise ValueError("compile manifest binder.id is required")
    if not isinstance(compile_data, dict) or not compile_data.get("id"):
        raise ValueError("compile manifest compile.id is required")
    if not compile_data.get("target"):
        raise ValueError("compile manifest compile.target is required")
    if compile_data.get("provider") != "wizard":
        raise ValueError("compile manifest compile.provider must be wizard")
    if not isinstance(views, list) or len(views) == 0:
        raise ValueError("compile manifest views must contain at least one entry")
    for index, view in enumerate(views):
        if not isinstance(view, dict) or not view.get("id"):
            raise ValueError(f"compile manifest views[{index}].id is required")
        if not view.get("kind"):
            raise ValueError(f"compile manifest views[{index}].kind is required")


def _deerflow_compile_run(manifest: dict, execution_mode: str) -> dict:
    try:
        from adapter import compile_manifest_to_workflow, run_adapter
    except ImportError as exc:
        raise ValueError("deerflow adapter is not available") from exc

    workflow = compile_manifest_to_workflow(manifest)
    payload = run_adapter(
        workflow,
        upstream_pin="v2.5-controlled" if execution_mode == "controlled" else "v2.5-preview",
        dry_run=execution_mode == "preview",
    )
    return {
        "workflow_preview": workflow,
        "graph_preview": payload["graph"],
        "result_preview": payload["result"],
        "pin_status": payload["pin_status"],
    }


def _native_compile_result(manifest: dict) -> dict:
    binder_data = manifest.get("binder", {})
    compile_data = manifest.get("compile", {})
    views = manifest.get("views", [])
    generated_at = datetime.now(timezone.utc).isoformat()

    artifacts = [
        {
            "kind": "workspace-surface",
            "path": f"workspace://{binder_data.get('id', 'binder')}/{view.get('id', 'view')}",
            "view_id": view.get("id", "view"),
            "view_kind": view.get("kind", "surface"),
        }
        for view in views
    ]

    return {
        "executionId": f"native:{binder_data.get('id', 'binder')}:{compile_data.get('id', 'compile')}",
        "workflowId": f"native-compile-{compile_data.get('id', 'compile')}",
        "status": "completed",
        "startedAt": generated_at,
        "finishedAt": generated_at,
        "summary": {
            "completed": len(views),
            "failed": 0,
            "artifactsProduced": len(artifacts),
            "message": "Native compile completed in Wizard.",
        },
        "artifacts": artifacts,
    }


class OrchestrationRegistry:
    def __init__(self, result_store_path: Path | None = None) -> None:
        if result_store_path is None:
            self._result_store_path = get_path("WIZARD_RESULT_STORE_PATH")
        else:
            self._result_store_path = Path(result_store_path)
        ensure_install_id()
        self._results = self._load_results()

    def _load_results(self) -> dict[str, dict]:
        if not self._result_store_path.exists():
            return {}
        return json.loads(self._result_store_path.read_text(encoding="utf-8"))

    def _persist_results(self) -> None:
        self._result_store_path.parent.mkdir(parents=True, exist_ok=True)
        self._result_store_path.write_text(
            json.dumps(self._results, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def list_results(self, prefix: str = "") -> dict:
        results = []
        for dispatch_id, payload in sorted(self._results.items()):
            if prefix and not dispatch_id.startswith(prefix):
                continue
            results.append(payload)
        return {"count": len(results), "results": results}

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
            "execution_backends_contract_source": str(_execution_backends_contract_source()),
            "orchestration_contract_version": contract["version"],
            "execution_backends": _load_execution_backends_contract()["backends"],
            "result_store_path": str(self._result_store_path),
            "result_store_mode": "file-json",
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

    def route(
        self, task: str, mode: str = "auto", surface: str = "assist", execution_backend: str = "native"
    ) -> dict:
        return route_task(task=task, mode=mode, surface=surface, execution_backend=execution_backend)

    def compile_dispatch(
        self,
        manifest: dict,
        execution_backend: str = "native",
        execution_mode: str = "preview",
    ) -> dict:
        _validate_execution_backend(execution_backend)
        _validate_execution_mode(execution_mode)
        _validate_compile_manifest(manifest)
        contract = _load_orchestration_contract()
        compile_data = manifest.get("compile", {})
        binder_data = manifest.get("binder", {})

        compile_id = str(compile_data.get("id", "compile-unknown"))
        binder_id = str(binder_data.get("id", "binder-unknown"))
        target = str(compile_data.get("target", "workspace"))
        template = str(compile_data.get("template", "") or "")

        preview = {}
        if execution_backend == "deerflow":
            executor = "deerflow-adapter"
            transport = "job-queue"
            preview = _deerflow_compile_run(manifest, execution_mode=execution_mode)
            execution_result = preview["result_preview"]
            status = execution_result["status"]
        else:
            executor = "compile-runner"
            transport = "https"
            execution_result = _native_compile_result(manifest)
            status = execution_result["status"]
            execution_mode = "controlled"

        payload = {
            "dispatch_version": contract["compile_dispatch_contract"]["dispatch_version"],
            "dispatch_id": f"compile:{binder_id}:{compile_id}:{execution_backend}",
            "binder_id": binder_id,
            "compile_id": compile_id,
            "target": target,
            "template": template,
            "provider": "wizard",
            "execution_backend": execution_backend,
            "execution_mode": execution_mode,
            "executor": executor,
            "transport": transport,
            "status": status,
            "manifest": manifest,
            "execution_result": execution_result,
            **preview,
        }
        self.record_result(
            dispatch_id=payload["dispatch_id"],
            status=status,
            result={
                "binder_id": binder_id,
                "compile_id": compile_id,
                "execution_backend": execution_backend,
                "execution_mode": execution_mode,
                "target": target,
                "template": template,
                "execution_result": execution_result,
                "manifest": manifest,
                **preview,
            },
        )
        return payload

    def publish_queue(self) -> dict:
        queue = []
        for dispatch_id, payload in sorted(self._results.items()):
            result = payload.get("result", {})
            if not dispatch_id.startswith("compile:"):
                continue
            binder_id = result.get("binder_id", "binder-unknown")
            compile_id = result.get("compile_id", "compile-unknown")
            execution_backend = result.get("execution_backend", "native")
            compile_status = payload.get("status", "queued")
            queue.append(
                {
                    "publish_id": f"publish:{binder_id}:{compile_id}",
                    "binder_id": binder_id,
                    "compile_id": compile_id,
                    "execution_backend": execution_backend,
                    "execution_mode": result.get("execution_mode", "preview"),
                    "status": "scheduled" if compile_status == "completed" else "awaiting-compile",
                    "channel": "empire-social",
                    "dispatch_id": dispatch_id,
                }
            )
        return {"count": len(queue), "queue": queue}

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
        self._persist_results()
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


def route_task(task: str, mode: str = "auto", surface: str = "assist", execution_backend: str = "native") -> dict:
    _validate_execution_backend(execution_backend)
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
            "execution_backend": "native",
            "executor": "local-shell",
            "transport": "subprocess",
            "status": "queued",
            "route_contract": {"owner": "uDOS-wizard", "surface": surface, "mode": mode},
            "callback_contract": callback_contract,
            **request,
        }

    if execution_backend == "deerflow":
        return {
            "dispatch_version": contract["dispatch_contract"]["dispatch_version"],
            "request": request,
            "dispatch_id": f"dispatch:{surface}:{task}:{mode}:deerflow",
            "provider": "wizard-provider",
            "execution_backend": "deerflow",
            "executor": "deerflow-adapter",
            "transport": "job-queue",
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
            "execution_backend": "native",
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
        "execution_backend": "native",
        "executor": "provider-router",
        "transport": "https",
        "status": "queued",
        "route_contract": {"owner": "uDOS-wizard", "surface": surface, "mode": mode},
        "callback_contract": callback_contract,
        **request,
    }
