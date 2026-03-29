import json
from pathlib import Path
from html import escape
import sys

from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from pydantic import ValidationError
from fastapi.staticfiles import StaticFiles
import uvicorn


def _ensure_core_on_path() -> None:
    core_root = Path(__file__).resolve().parents[2] / "uDOS-core"
    core_root_str = str(core_root)
    if core_root.exists() and core_root_str not in sys.path:
        sys.path.insert(0, core_root_str)


_ensure_core_on_path()

from udos_core.dev_config import get_path, load_dev_config
from udos_core.local_state import ensure_install_id, load_local_state, update_local_state

from .assist import route_assist
from .budget import BudgetPolicy
from .mcp_registry import MCPRegistry
from .beacon import BeaconNode
from .grid_runtime import load_grid_contract, load_grid_seed, resolve_place, validate_place
from .orchestration import OrchestrationRegistry
from .port_manager import configured_runtime_bind_status, resolve_bind_plan, runtime_bind_status_from_plan
from .render_preview import (
    export_render,
    list_render_exports,
    list_render_presets,
    render_export_detail,
    render_contract,
    render_preview,
)
from .runtime_config import get_runtime_config, runtime_config_metadata, runtime_config_snapshot
from .secret_store import get_secret_store
from .ok.provider_registry import ProviderRegistry
from .ok.routing_engine import OKProviderRoutingEngine
from .ok.mcp_policy import mcp_split_policy
from .google_mvp import (
    get_google_mvp_extraction_checklist,
    get_google_mvp_generated_output_example,
    get_google_mvp_lane_bundle,
    get_google_mvp_prompt_template,
)
from .uhome_policy_contract import (
    get_uhome_network_policy_contract,
    get_uhome_network_policy_schema,
    uhome_network_policy_validation_error,
    validate_uhome_network_policy,
)
from .uhome_bridge import (
    automation_jobs as fetch_uhome_automation_jobs,
    automation_results as fetch_uhome_automation_results,
    automation_status as fetch_uhome_automation_status,
    bridge_status as fetch_uhome_bridge_status,
    cancel_automation_job as cancel_uhome_automation_job,
    dispatch_workflow_automation_job,
    get_uhome_server_url,
    process_next_automation_job as process_next_uhome_automation_job,
    reconcile_latest_workflow_result,
    retry_automation_job as retry_uhome_automation_job,
)
from .workflow_state import get_workflow_store
from .demo import build_demo_links
from .broker import (
    dispatch_request as dispatch_broker_request,
    list_services as list_broker_services,
    resolve_request as resolve_broker_request,
)

app = FastAPI(title="uDOS Surface Compatibility Host")

load_dev_config()
ensure_install_id()

budget = BudgetPolicy()
registry = MCPRegistry()
beacon = BeaconNode()
orchestration = OrchestrationRegistry()
static_root = Path(__file__).resolve().parents[1] / "static"
rendered_root = get_path("UDOS_RENDER_ROOT")
surface_ui_dist_root = Path(__file__).resolve().parents[1] / "apps" / "surface-ui" / "dist"
runtime_bind_status = configured_runtime_bind_status()
ok_provider_registry = ProviderRegistry()
ok_routing_engine = OKProviderRoutingEngine(ok_provider_registry)


def _family_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _ubuntu_host_surface_contract_path() -> Path:
    return _family_root() / "uDOS-ubuntu" / "contracts" / "udos-commandd" / "wizard-host-surface.v1.json"


def _ubuntu_host_surface_contract() -> dict[str, object]:
    path = _ubuntu_host_surface_contract_path()
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {
        "version": "v1",
        "owner": "uDOS-ubuntu",
        "consumer": "uDOS-wizard",
        "base_path": "/host",
        "operations": [],
    }


def _register_mcp_tools() -> None:
    registry.register(
        "wizard.resolve",
        "Resolve a family request to the correct service without taking execution authority.",
        input_schema={
            "type": "object",
            "properties": {
                "intent": {"type": "string"},
                "capability": {"type": "string"},
                "offline_only": {"type": "boolean"},
                "approval_required": {"type": "boolean"},
                "payload_ref": {"type": "string"}
            },
            "required": ["intent"],
            "additionalProperties": False
        },
        annotations={
            "owner": "uDOS-wizard",
            "surface": "broker",
            "route": "/wizard/resolve",
        },
        handler=lambda payload: resolve_broker_request(
            intent=str(payload.get("intent") or ""),
            capability=str(payload.get("capability") or ""),
            offline_only=bool(payload.get("offline_only", False)),
            approval_required=bool(payload.get("approval_required", False)),
            payload_ref=str(payload.get("payload_ref") or ""),
        ),
    )
    registry.register(
        "ok.route",
        "Route an OK request through Wizard budget and provider policy.",
        input_schema={
            "type": "object",
            "properties": {
                "task": {"type": "string"},
                "task_class": {"type": "string"},
                "allowed_budget_groups": {"type": "array", "items": {"type": "string"}},
                "approval_granted": {"type": "boolean"},
                "offline_sufficient": {"type": "boolean"},
                "cache_hit": {"type": "boolean"},
                "complexity": {"type": "string"},
            },
            "required": ["task"],
            "additionalProperties": True,
        },
        annotations={
            "owner": "uDOS-wizard",
            "surface": "managed-mcp",
            "route": "/ok/route",
        },
        handler=ok_routing_engine.route,
    )
    registry.register(
        "ok.providers.list",
        "List Wizard OK providers and budget groups.",
        input_schema={
            "type": "object",
            "properties": {
                "capability": {"type": "string"},
                "enabled_only": {"type": "boolean"},
            },
            "additionalProperties": False,
        },
        annotations={
            "owner": "uDOS-wizard",
            "surface": "managed-mcp",
            "route": "/ok/providers",
        },
        handler=lambda payload: {
            "count": len(
                ok_provider_registry.list_providers(
                    capability=str(payload.get("capability") or ""),
                    enabled_only=bool(payload.get("enabled_only", True)),
                )
            ),
            "providers": ok_provider_registry.list_providers(
                capability=str(payload.get("capability") or ""),
                enabled_only=bool(payload.get("enabled_only", True)),
            ),
            "budget_groups": ok_provider_registry.budget_groups(),
        },
    )
    registry.register(
        "ok.google_mvp.bundle",
        "Inspect Wizard's Google MVP lane bundle for Empire prompt and extraction governance.",
        input_schema={
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
        annotations={
            "owner": "uDOS-wizard",
            "surface": "managed-mcp",
            "route": "/ok/lanes/google-mvp-a",
        },
        handler=lambda payload: get_google_mvp_lane_bundle(),
    )


_register_mcp_tools()

if static_root.exists():
    app.mount("/ui-assets", StaticFiles(directory=str(static_root)), name="ui-assets")
rendered_root.mkdir(parents=True, exist_ok=True)
app.mount("/rendered", StaticFiles(directory=str(rendered_root)), name="rendered")
if surface_ui_dist_root.exists() and (surface_ui_dist_root / "assets").exists():
    app.mount("/app-assets", StaticFiles(directory=str(surface_ui_dist_root / "assets")), name="app-assets")

@app.get("/")
def root():
    return {"service": "wizard", "status": "ok", "role": "broker-and-surface-host"}


@app.get("/wizard/services")
def wizard_services():
    services = list_broker_services()
    return {
        "version": "v1",
        "broker": "wizard",
        "count": len(services),
        "services": services,
    }


@app.post("/wizard/resolve")
def wizard_resolve(payload: dict = Body(...)):
    return resolve_broker_request(
        intent=str(payload.get("intent") or ""),
        capability=str(payload.get("capability") or ""),
        offline_only=bool(payload.get("offline_only", False)),
        approval_required=bool(payload.get("approval_required", False)),
        payload_ref=str(payload.get("payload_ref") or ""),
    )


@app.post("/wizard/dispatch")
def wizard_dispatch(payload: dict = Body(...)):
    broker_payload = payload.get("payload")
    if broker_payload is not None and not isinstance(broker_payload, dict):
        raise HTTPException(status_code=400, detail="payload must be an object when provided")
    return dispatch_broker_request(
        intent=str(payload.get("intent") or ""),
        capability=str(payload.get("capability") or ""),
        payload=broker_payload,
        offline_only=bool(payload.get("offline_only", False)),
        approval_required=bool(payload.get("approval_required", False)),
        payload_ref=str(payload.get("payload_ref") or ""),
    )

@app.get("/assist")
def assist(task: str = "demo", mode: str = "auto"):
    return route_assist(task, mode)

@app.get("/budget")
def get_budget():
    return budget.get()

@app.get("/mcp/tools")
def list_tools():
    return registry.list_tools()


@app.post("/mcp/tools/{tool_name}/invoke")
def invoke_tool(tool_name: str, payload: dict = Body(default_factory=dict)):
    try:
        invocation = registry.invoke(tool_name, payload)
    except KeyError as exc:
        return JSONResponse(status_code=404, content={"status": "error", "detail": str(exc)})
    except ValueError as exc:
        return JSONResponse(status_code=400, content={"status": "error", "detail": str(exc)})

    return {
        "status": "ok",
        "invocation": invocation,
    }


@app.post("/mcp")
def mcp_rpc(payload: dict = Body(...)):
    method = str(payload.get("method") or "")
    request_id = payload.get("id")
    params = payload.get("params") or {}

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "serverInfo": {"name": "uDOS Wizard MCP", "version": "v2.2"},
                "capabilities": {"tools": {"listChanged": False}},
            },
        }

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": registry.list_tools(),
        }

    if method == "tools/call":
        tool_name = str(params.get("name") or "")
        arguments = params.get("arguments") or {}
        try:
            invocation = registry.invoke(tool_name, arguments)
        except (KeyError, ValueError) as exc:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32000, "message": str(exc)},
            }
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": invocation,
        }

    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": -32601, "message": f"method not found: {method}"},
    }


@app.get("/ok/providers")
def list_ok_providers(capability: str = "", enabled_only: bool = True):
    providers = ok_provider_registry.list_providers(
        capability=capability,
        enabled_only=enabled_only,
    )
    return {
        "count": len(providers),
        "providers": providers,
        "budget_groups": ok_provider_registry.budget_groups(),
    }


@app.get("/ok/providers/{provider_id}")
def get_ok_provider(provider_id: str):
    provider = ok_provider_registry.get_provider(provider_id)
    if provider is None:
        return {"status": "error", "detail": f"unknown provider: {provider_id}"}
    return provider


@app.post("/ok/route")
def route_ok_request(payload: dict = Body(...)):
    decision = ok_routing_engine.route(payload)
    return {
        "request": payload,
        "decision": decision,
    }


@app.get("/ok/mcp-policy")
def get_ok_mcp_policy():
    return mcp_split_policy()


@app.get("/ok/lanes/google-mvp-a")
def get_ok_google_mvp_lane():
    return get_google_mvp_lane_bundle()


@app.get("/ok/lanes/google-mvp-a/prompt-template")
def get_ok_google_mvp_prompt_template():
    return get_google_mvp_prompt_template()


@app.get("/ok/lanes/google-mvp-a/extraction-checklist")
def get_ok_google_mvp_extraction_checklist():
    return get_google_mvp_extraction_checklist()


@app.get("/ok/lanes/google-mvp-a/generated-output-example")
def get_ok_google_mvp_generated_output_example():
    return get_google_mvp_generated_output_example()

@app.get("/orchestration/status")
def orchestration_status():
    return orchestration.status()

@app.get("/orchestration/dispatch")
def orchestration_dispatch(
    task: str = "demo", mode: str = "auto", surface: str = "assist", execution_backend: str = "native"
):
    try:
        return orchestration.route(task=task, mode=mode, surface=surface, execution_backend=execution_backend)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@app.get("/orchestration/workflow-plan")
def orchestration_workflow_plan(objective: str = "shared-remote-flow", mode: str = "auto"):
    return orchestration.workflow_plan(objective=objective, mode=mode)


@app.post("/compile/dispatch")
def compile_dispatch(payload: dict = Body(...)):
    try:
        return orchestration.compile_dispatch(
            manifest=payload.get("manifest", {}),
            execution_backend=payload.get("execution_backend", "native"),
            execution_mode=payload.get("execution_mode", "preview"),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/compile/results")
def compile_results():
    return orchestration.list_results(prefix="compile:")


@app.get("/publish/queue")
def publish_queue():
    return orchestration.publish_queue()


@app.post("/orchestration/callback")
def orchestration_callback(payload: dict = Body(...)):
    return orchestration.record_result(
        dispatch_id=payload.get("dispatch_id", "dispatch:unknown"),
        status=payload.get("status", "completed"),
        result=payload.get("result", {}),
    )


@app.get("/orchestration/result/{dispatch_id}")
def orchestration_result(dispatch_id: str):
    return orchestration.get_result(dispatch_id)


@app.get("/contracts/uhome/network-policy")
def get_uhome_network_policy_contract_route():
    return get_uhome_network_policy_contract()


@app.get("/contracts/uhome/network-policy/schema")
def get_uhome_network_policy_schema_route():
    return get_uhome_network_policy_schema()


@app.post("/contracts/uhome/network-policy/validate")
def post_uhome_network_policy_validate(payload: dict = Body(...)):
    try:
        validated = validate_uhome_network_policy(payload)
    except (ValueError, ValidationError) as exc:
        return JSONResponse(content=uhome_network_policy_validation_error(exc), status_code=400)
    return {
        "ok": True,
        "contract_version": validated["contract_version"],
        "profile_id": validated["profile_id"],
        "runtime_owner": validated["runtime_owner"],
        "policy_owner": validated["policy_owner"],
        "validated_policy": validated,
    }


@app.get("/workflow/state")
def get_workflow_state():
    return get_workflow_store().get_state()


@app.post("/workflow/state")
def post_workflow_state(payload: dict = Body(...)):
    return get_workflow_store().update_state(payload)


@app.get("/workflow/actions")
def get_workflow_actions():
    return get_workflow_store().list_actions()


@app.post("/workflow/actions")
def post_workflow_action(payload: dict = Body(...)):
    return get_workflow_store().record_action(payload)


@app.post("/workflow/handoff/automation-job")
def post_workflow_handoff_automation_job(payload: dict = Body(...)):
    return get_workflow_store().build_automation_job(payload)


@app.post("/workflow/reconcile/automation-result")
def post_workflow_reconcile_automation_result(payload: dict = Body(...)):
    return get_workflow_store().reconcile_automation_result(payload)


@app.post("/workflow/handoff/automation-job/dispatch")
def post_workflow_handoff_automation_dispatch(payload: dict = Body(...)):
    return dispatch_workflow_automation_job(payload)


@app.get("/uhome/bridge/status")
def get_uhome_bridge_status():
    return fetch_uhome_bridge_status()


@app.get("/uhome/automation/status")
def get_uhome_automation_status():
    return fetch_uhome_automation_status()


@app.get("/uhome/automation/jobs")
def get_uhome_automation_jobs():
    return fetch_uhome_automation_jobs()


@app.post("/uhome/automation/jobs/{job_id}/cancel")
def post_uhome_automation_cancel(job_id: str):
    return cancel_uhome_automation_job(job_id)


@app.get("/uhome/automation/results")
def get_uhome_automation_results():
    return fetch_uhome_automation_results()


@app.post("/uhome/automation/results/{job_id}/retry")
def post_uhome_automation_retry(job_id: str):
    return retry_uhome_automation_job(job_id)


@app.post("/uhome/automation/process-next")
def post_uhome_automation_process_next(payload: dict = Body(default={})):
    return process_next_uhome_automation_job(payload)


@app.post("/workflow/reconcile/uhome-latest")
def post_workflow_reconcile_uhome_latest(payload: dict = Body(...)):
    return reconcile_latest_workflow_result(payload.get("workflow_id"))


@app.get("/grid/contracts/{name}")
def get_grid_contract(name: str):
    try:
        return load_grid_contract(name)
    except ValueError as exc:
        return {"status": "error", "detail": str(exc)}


@app.get("/grid/seeds/{name}")
def get_grid_seed(name: str):
    try:
        items = load_grid_seed(name)
    except ValueError as exc:
        return {"status": "error", "detail": str(exc)}
    return {"owner": "uDOS-grid", "consumer": "uDOS-wizard", "seed": name, "count": len(items), "items": items}


@app.get("/grid/resolve")
def get_grid_resolve(place_ref: str):
    return resolve_place(place_ref)


@app.post("/grid/validate-place")
def post_grid_validate_place(payload: dict = Body(...)):
    return validate_place(payload)

@app.get("/beacon/announce")
def beacon_announce():
    return beacon.announce()


@app.get("/gui")
def gui_shell():
    return FileResponse(static_root / "surface-gui.html")


@app.get("/thin")
def thin_shell():
    return FileResponse(static_root / "thin-gui.html")


@app.get("/demo/links")
def get_demo_links():
    return {
        "service": "wizard-demo",
        "status": "ok",
        "wizard_base_url": runtime_bind_status.base_url,
        "uhome_base_url": get_uhome_server_url(),
        "links": build_demo_links(runtime_bind_status.base_url, get_uhome_server_url()),
    }


@app.get("/demo")
def demo_shell():
    payload = get_demo_links()
    links_markup = "\n".join(
        (
            "<li>"
            f"<strong>{escape(label.replace('_', ' '))}</strong>"
            f"<br><a href=\"{escape(url)}\">{escape(url)}</a>"
            "</li>"
        )
        for label, url in payload["links"].items()
    )
    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>uDOS Demo Links</title>
    <style>
      :root {{
        color-scheme: light;
        --ink: #172033;
        --muted: #5f6474;
        --line: #d8dce6;
        --paper: #f7f3eb;
        --card: #fffdfa;
        --accent: #c96f2d;
      }}
      body {{
        margin: 0;
        font-family: Georgia, "Iowan Old Style", serif;
        background: linear-gradient(180deg, #f3efe7 0%, var(--paper) 100%);
        color: var(--ink);
      }}
      main {{
        max-width: 900px;
        margin: 0 auto;
        padding: 40px 20px 60px;
      }}
      h1 {{
        margin-bottom: 8px;
      }}
      p {{
        color: var(--muted);
        line-height: 1.5;
      }}
      code {{
        background: #f0eadf;
        padding: 2px 6px;
        border-radius: 6px;
      }}
      ul {{
        list-style: none;
        padding: 0;
        display: grid;
        gap: 12px;
      }}
      li {{
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 14px 16px;
      }}
      a {{
        color: var(--accent);
        text-decoration: none;
      }}
      a:hover {{
        text-decoration: underline;
      }}
    </style>
  </head>
  <body>
    <main>
      <h1>uDOS Demo Links</h1>
      <p>Use <code>.venv/bin/udos-surface-demo</code>, <code>.venv/bin/udos-wizard-demo</code>, or <code>.venv/bin/python -m wizard.demo</code> to launch the local Surface compatibility stack, then open any lane from this page.</p>
      <p>Wizard base: <a href="{escape(payload["wizard_base_url"])}">{escape(payload["wizard_base_url"])}</a><br>uHOME base: <a href="{escape(payload["uhome_base_url"])}">{escape(payload["uhome_base_url"])}</a></p>
      <ul>
        {links_markup}
      </ul>
    </main>
  </body>
</html>"""
    return HTMLResponse(html)


@app.get("/app")
def svelte_app_shell():
    if not surface_ui_dist_root.exists():
        return {
            "service": "surface-ui",
            "status": "missing-build",
            "hint": "Run npm run build in apps/surface-ui to enable /app",
        }
    return FileResponse(surface_ui_dist_root / "index.html")


@app.get("/app/{path:path}")
def svelte_app_spa(path: str):
    if not surface_ui_dist_root.exists():
        return {
            "service": "surface-ui",
            "status": "missing-build",
            "hint": "Run npm run build in apps/surface-ui to enable /app",
            "path": path,
        }
    return FileResponse(surface_ui_dist_root / "index.html")


@app.get("/render/contract")
def get_render_contract():
    return render_contract()


@app.get("/render/presets")
def get_render_presets():
    return list_render_presets()


@app.post("/render/preview")
def post_render_preview(payload: dict = Body(...)):
    return render_preview(
        markdown_text=payload.get("markdown", ""),
        metadata=payload.get("metadata", {}),
        target=payload.get("target", "gui-preview"),
    )


@app.post("/render/export")
def post_render_export(payload: dict = Body(...)):
    return export_render(
        markdown_text=payload.get("markdown", ""),
        metadata=payload.get("metadata", {}),
        target=payload.get("target", "web-prose"),
    )


@app.get("/render/exports")
def get_render_exports():
    return list_render_exports()


@app.get("/render/exports/{target}/{slug}")
def get_render_exports_detail(target: str, slug: str):
    return render_export_detail(target=target, slug=slug)


@app.get("/port/status")
def get_port_status():
    payload = runtime_bind_status.__dict__.copy()
    occupant = payload.get("occupant")
    if occupant is not None:
        payload["occupant"] = occupant.__dict__
    return payload


@app.get("/config/runtime")
def get_config_runtime(key: str):
    metadata = runtime_config_metadata(key)
    payload = dict(metadata)
    if metadata["present"] and not metadata["is_secret"]:
        payload["value"] = get_runtime_config(key, "")
    else:
        payload["value"] = None
    return payload


@app.get("/config/runtime-summary")
def get_config_runtime_summary():
    return runtime_config_snapshot()


@app.get("/config/local-state")
def get_config_local_state():
    ensure_install_id()
    return load_local_state()


@app.post("/config/local-state")
def post_config_local_state(payload: dict = Body(...)):
    return update_local_state(payload)


@app.get("/config/secrets")
def get_config_secrets():
    store = get_secret_store()
    keys = store.list_secret_keys()
    return {
        "keys": [{"key": key, "present": True} for key in keys],
        "count": len(keys),
    }


@app.get("/config/secrets/{key}")
def get_config_secret_presence(key: str):
    value = get_secret_store().get_secret(key)
    return {"key": key, "present": bool(value)}


@app.post("/config/secrets")
def post_config_secret(payload: dict = Body(...)):
    key = str(payload.get("key") or "").strip()
    value = str(payload.get("value") or "")
    if not key:
        return {"status": "error", "detail": "key is required"}
    get_secret_store().set_secret(key, value)
    return {"status": "ok", "key": key, "present": True}


@app.get("/host/contract")
def get_host_contract():
    payload = dict(_ubuntu_host_surface_contract())
    payload["proxy_mode"] = "wizard-compatibility-bridge"
    return payload


@app.get("/host/runtime-summary")
def get_host_runtime_summary():
    return {
        "owner": "uDOS-ubuntu",
        "bridge": "uDOS-wizard",
        "status": "compatibility-bridge",
        "deprecated_source_route": "/config/runtime-summary",
        "summary": runtime_config_snapshot(),
    }


@app.get("/host/local-state")
def get_host_local_state():
    ensure_install_id()
    return {
        "owner": "uDOS-ubuntu",
        "bridge": "uDOS-wizard",
        "status": "compatibility-bridge",
        "deprecated_source_route": "/config/local-state",
        "state": load_local_state(),
    }


@app.post("/host/local-state")
def post_host_local_state(payload: dict = Body(...)):
    return {
        "owner": "uDOS-ubuntu",
        "bridge": "uDOS-wizard",
        "status": "compatibility-bridge",
        "deprecated_source_route": "/config/local-state",
        "state": update_local_state(payload),
    }


@app.get("/host/secrets")
def get_host_secrets():
    store = get_secret_store()
    keys = store.list_secret_keys()
    return {
        "owner": "uDOS-ubuntu",
        "bridge": "uDOS-wizard",
        "status": "compatibility-bridge",
        "deprecated_source_route": "/config/secrets",
        "keys": [{"key": key, "present": True} for key in keys],
        "count": len(keys),
    }


@app.post("/host/secrets")
def post_host_secret(payload: dict = Body(...)):
    key = str(payload.get("key") or "").strip()
    value = str(payload.get("value") or "")
    if not key:
        return {"status": "error", "detail": "key is required"}
    get_secret_store().set_secret(key, value)
    return {
        "owner": "uDOS-ubuntu",
        "bridge": "uDOS-wizard",
        "status": "compatibility-bridge",
        "deprecated_source_route": "/config/secrets",
        "key": key,
        "present": True,
    }


@app.get("/host/budget-status")
def get_host_budget_status():
    return {
        "owner": "uDOS-ubuntu",
        "bridge": "uDOS-wizard",
        "status": "compatibility-bridge",
        "deprecated_source_route": "/budget",
        "budget": budget.get(),
    }


@app.get("/host/providers")
def get_host_providers():
    providers = ok_provider_registry.list_providers(enabled_only=False)
    return {
        "owner": "uDOS-ubuntu",
        "bridge": "uDOS-wizard",
        "status": "compatibility-bridge",
        "deprecated_source_route": "/ok/providers",
        "providers": providers,
        "count": len(providers),
        "budget_groups": ok_provider_registry.budget_groups(),
    }


@app.get("/host/orchestration-status")
def get_host_orchestration_status():
    return {
        "owner": "uDOS-ubuntu",
        "bridge": "uDOS-wizard",
        "status": "compatibility-bridge",
        "deprecated_source_route": "/orchestration/status",
        "orchestration": orchestration.status(),
    }

def run():
    bind_plan = resolve_bind_plan()
    global runtime_bind_status
    runtime_bind_status = runtime_bind_status_from_plan(bind_plan, actual_binding_known=True)
    if bind_plan.auto_shifted:
        occupant = ""
        if bind_plan.occupant is not None:
            occupant = f" Occupied by {bind_plan.occupant.process} (PID {bind_plan.occupant.pid})."
        print(
            f"uDOS-wizard: port {bind_plan.requested_port} unavailable; using {bind_plan.port} instead.{occupant}"
        )
    print(f"uDOS-wizard: gui {runtime_bind_status.gui_url}")
    print(f"uDOS-wizard: thin {runtime_bind_status.thin_url}")
    uvicorn.run(app, host=bind_plan.host, port=bind_plan.port)


if __name__ == "__main__":
    run()
