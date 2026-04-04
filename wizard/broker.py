from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import error, request

from udos_core.dev_config import get_str


def _utc_now_iso_z() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _family_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


@dataclass(frozen=True)
class ServiceRecord:
    service_id: str
    owner: str
    surface: str
    capabilities: tuple[str, ...]
    routes: tuple[dict[str, Any], ...]
    transport: str
    offline_safe: bool
    dispatch_mode: str
    source: str
    notes: str = ""


INTENT_TO_CAPABILITY: tuple[tuple[tuple[str, ...], str], ...] = (
    (("format", "cleanup", "transform"), "ok.transformation"),
    (("research", "summarize", "analyse", "analyze"), "ok.research"),
    (("ingest", "capture", "link"), "ok.ingest"),
    (("library", "browse", "binder"), "library.browse"),
    (("search",), "library.search"),
    (("beacon", "network", "wifi"), "beacon.status"),
    (("preview", "publish", "render"), "surface.preview"),
    (("schema", "validate", "contract"), "core.validate"),
)

def _local_surface_records() -> list[ServiceRecord]:
    contract_paths = (
        _family_root() / "uDOS-wizard" / "contracts" / "surface-render-surface.v1.json",
        _family_root() / "uDOS-wizard" / "contracts" / "wizard-broker-contract.json",
    )
    records: list[ServiceRecord] = []
    for path in contract_paths:
        if not path.exists():
            continue
        payload = _read_json(path)
        records.append(
            ServiceRecord(
                service_id=str(payload.get("service_id") or payload.get("owner") or "uDOS-wizard"),
                owner=str(payload.get("owner") or "uDOS-wizard"),
                surface=str(payload.get("surface") or "unknown"),
                capabilities=tuple(str(capability) for capability in payload.get("capabilities", [])),
                routes=tuple(payload.get("routes", [])),
                transport=str(payload.get("transport") or "https"),
                offline_safe=bool(payload.get("offline_safe", True)),
                dispatch_mode=str(payload.get("dispatch_mode") or "direct"),
                source=str(path),
                notes=str(payload.get("purpose") or ""),
            )
        )
    return records


def _core_contract_records() -> list[ServiceRecord]:
    path = _family_root() / "uDOS-core" / "contracts" / "runtime-services.json"
    if not path.exists():
        return []
    payload = _read_json(path)
    records: list[ServiceRecord] = []
    for service in payload.get("services", []):
        key = str(service.get("key") or "")
        if not key or "uDOS-wizard" not in service.get("consumers", []):
            continue
        capability = key.replace("runtime.", "core.", 1)
        records.append(
            ServiceRecord(
                service_id="uDOS-core",
                owner=str(service.get("owner") or "uDOS-core"),
                surface="contracts",
                capabilities=(capability,),
                routes=tuple(),
                transport=str(service.get("route") or "local-kernel"),
                offline_safe=True,
                dispatch_mode="direct",
                source=str(path),
                notes=str(service.get("notes") or ""),
            )
        )
    records.append(
        ServiceRecord(
            service_id="uDOS-core",
            owner="uDOS-core",
            surface="contracts",
            capabilities=("core.validate", "core.schema.lookup"),
            routes=tuple(),
            transport="local-kernel",
            offline_safe=True,
            dispatch_mode="direct",
            source="core-overlay",
            notes="Core owns schemas, validation, and offline-safe contracts.",
        )
    )
    return records


def _host_contract_records() -> list[ServiceRecord]:
    family_root = _family_root()
    host_surface_path = family_root / "uDOS-host" / "contracts" / "udos-commandd" / "wizard-host-surface.v1.json"
    minimum_ops_path = family_root / "uDOS-host" / "contracts" / "udos-commandd" / "minimum-operations.v1.json"
    explicit_surface_paths = (
        family_root / "uDOS-host" / "contracts" / "udos-commandd" / "okd-surface.v1.json",
        family_root / "uDOS-host" / "contracts" / "udos-commandd" / "library-surface.v1.json",
    )
    records: list[ServiceRecord] = []

    if host_surface_path.exists():
        payload = _read_json(host_surface_path)
        host_capabilities = tuple(
            operation["operation_id"] for operation in payload.get("operations", []) if operation.get("operation_id")
        )
        if host_capabilities:
            records.append(
                ServiceRecord(
                    service_id="uDOS-host",
                    owner=str(payload.get("owner") or "uDOS-host"),
                    surface="host",
                    capabilities=host_capabilities,
                    routes=tuple(payload.get("operations", [])),
                    transport="local-http",
                    offline_safe=True,
                    dispatch_mode="direct",
                    source=str(host_surface_path),
                    notes=str(payload.get("purpose") or ""),
                )
            )

    explicit_surfaces: set[str] = set()
    for path in explicit_surface_paths:
        if not path.exists():
            continue
        payload = _read_json(path)
        explicit_surfaces.add(str(payload.get("surface") or ""))
        records.append(
            ServiceRecord(
                service_id=str(payload.get("service_id") or "uDOS-host"),
                owner=str(payload.get("owner") or "uDOS-host"),
                surface=str(payload.get("surface") or "unknown"),
                capabilities=tuple(str(capability) for capability in payload.get("capabilities", [])),
                routes=tuple(payload.get("routes", [])),
                transport=str(payload.get("transport") or "local-http"),
                offline_safe=bool(payload.get("offline_safe", False)),
                dispatch_mode=str(payload.get("dispatch_mode") or "direct"),
                source=str(path),
                notes=str(payload.get("purpose") or ""),
            )
        )

    minimum_operations = []
    if minimum_ops_path.exists():
        minimum_operations = _read_json(minimum_ops_path).get("minimum_operations", [])

    grouped: dict[str, dict[str, Any]] = {}
    for operation in minimum_operations:
        operation_id = str(operation.get("operation_id") or "")
        if not operation_id:
            continue
        if operation_id.startswith("vault."):
            if "library" in explicit_surfaces:
                continue
            key = "library"
            capability = (
                "library.search"
                if operation_id == "vault.search"
                else "binder.view" if operation_id == "vault.open" else "library.browse"
            )
        elif operation_id.startswith("network.beacon"):
            key = "network.beacon"
            capability = "beacon.status"
        elif operation_id.startswith("network."):
            key = "network"
            capability = operation_id
        elif operation_id.startswith("budget."):
            key = "budget"
            capability = operation_id
        elif operation_id.startswith("jobs."):
            key = "jobs"
            capability = operation_id
        elif operation_id.startswith("sync."):
            key = "sync"
            capability = operation_id
        elif operation_id.startswith("publish.local."):
            key = "publish.local"
            capability = "surface.publish"
        else:
            continue
        entry = grouped.setdefault(
            key,
            {
                "capabilities": set(),
                "transport": "local-http",
                "offline_safe": True,
                "notes": "Discovered from Ubuntu minimum operations.",
            },
        )
        entry["capabilities"].add(capability)

    for surface, entry in grouped.items():
        records.append(
            ServiceRecord(
                service_id="uDOS-host",
                owner="uDOS-host",
                surface=surface,
                capabilities=tuple(sorted(entry["capabilities"])),
                routes=tuple(),
                transport=str(entry["transport"]),
                offline_safe=bool(entry["offline_safe"]),
                dispatch_mode="direct",
                source=str(minimum_ops_path) if minimum_ops_path.exists() else "ubuntu-overlay",
                notes=str(entry["notes"]),
            )
        )
    return records


def _all_service_records() -> list[ServiceRecord]:
    return _core_contract_records() + _host_contract_records() + _local_surface_records()


def list_services() -> list[dict[str, Any]]:
    return [
        {
            "service_id": service.service_id,
            "owner": service.owner,
            "surface": service.surface,
            "capabilities": list(service.capabilities),
            "transport": service.transport,
            "offline_safe": service.offline_safe,
            "dispatch_mode": service.dispatch_mode,
            "routes": list(service.routes),
            "source": service.source,
            "notes": service.notes,
        }
        for service in _all_service_records()
    ]


def _service_base_url(service_id: str) -> str:
    if service_id in {"uDOS-host", "uDOS-ubuntu"}:
        host = get_str("UDOS_HOST_BASE_URL", "").strip()
        legacy = get_str("UDOS_UBUNTU_BASE_URL", "http://127.0.0.1:8991").rstrip("/")
        return (host or legacy).rstrip("/")
    if service_id in {"uDOS-surface", "uDOS-wizard"}:
        return get_str("UDOS_SURFACE_BASE_URL", "http://127.0.0.1:8787").rstrip("/")
    return ""


def _select_route(service: ServiceRecord, capability: str, payload: dict[str, Any] | None) -> dict[str, Any] | None:
    matches = [route for route in service.routes if route.get("capability") == capability]
    if not matches:
        return None
    preferred_method = "POST" if payload else "GET"
    generic_paths = {"/ok/run", "/wizard/resolve", "/wizard/dispatch"}

    def _route_score(route: dict[str, Any]) -> tuple[int, int, int, int]:
        method = str(route.get("method") or "").upper()
        path = str(route.get("path") or route.get("route") or "")
        method_match = 1 if method == preferred_method else 0
        path_specificity = len(path.replace("{", "").replace("}", ""))
        direct_path = 0 if path in generic_paths else 1
        concrete_path = 0 if "{" in path else 1
        return (method_match, direct_path, concrete_path, path_specificity)

    return max(matches, key=_route_score)


def _dispatch_http_json(service: ServiceRecord, route: dict[str, Any], payload: dict[str, Any] | None) -> dict[str, Any]:
    base_url = _service_base_url(service.service_id)
    if not base_url:
        raise ValueError(f"no base URL configured for service {service.service_id}")
    path = str(route.get("path") or route.get("route") or "")
    if not path or "{" in path:
        raise ValueError(f"route path is not directly dispatchable: {path}")
    method = str(route.get("method") or "GET").upper()
    data = None
    headers: dict[str, str] = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = request.Request(f"{base_url}{path}", data=data, headers=headers, method=method)
    with request.urlopen(req, timeout=3) as response:
        raw = response.read().decode("utf-8")
    return json.loads(raw) if raw else {}


def infer_capability(intent: str) -> str:
    normalized = intent.strip().lower()
    if not normalized:
        return "help.general"
    if "." in normalized:
        return normalized
    for keywords, capability in INTENT_TO_CAPABILITY:
        if any(keyword in normalized for keyword in keywords):
            return capability
    return "help.general"


def resolve_request(
    intent: str,
    capability: str = "",
    offline_only: bool = False,
    approval_required: bool = False,
    payload_ref: str = "",
) -> dict[str, Any]:
    resolved_capability = capability.strip() or infer_capability(intent)
    candidates = [
        service
        for service in _all_service_records()
        if resolved_capability in service.capabilities
        and (not offline_only or service.offline_safe)
    ]
    request_id = f"req_{abs(hash((intent, resolved_capability, payload_ref))) % 10_000_000:07d}"

    if not candidates:
        return {
            "request_id": request_id,
            "broker": "wizard",
            "status": "help",
            "intent": intent,
            "capability": resolved_capability,
            "message": "No registered family service can satisfy this request with the current constraints.",
            "next_action": "Refine the intent, remove constraints, or add a matching service capability.",
            "candidates": [],
        }

    if len(candidates) > 1:
        return {
            "request_id": request_id,
            "broker": "wizard",
            "status": "multiple_candidates",
            "intent": intent,
            "capability": resolved_capability,
            "candidates": [
                {
                    "service_id": service.service_id,
                    "surface": service.surface,
                    "dispatch_mode": service.dispatch_mode,
                    "offline_safe": service.offline_safe,
                    "source": service.source,
                }
                for service in candidates
            ],
        }

    service = candidates[0]
    return {
        "request_id": request_id,
        "broker": "wizard",
        "status": "delegated",
        "intent": intent,
        "capability": resolved_capability,
        "destination_service": service.service_id,
        "destination_surface": service.surface,
        "dispatch_mode": service.dispatch_mode,
        "constraints": {
            "offline_only": offline_only,
            "approval_required": approval_required,
        },
        "payload_ref": payload_ref or f"wizard://capture/{request_id}",
        "status_callback": f"/wizard/delegations/{request_id}",
        "created_at": _utc_now_iso_z(),
        "source": service.source,
        "notes": service.notes,
    }


def dispatch_request(
    intent: str,
    capability: str = "",
    payload: dict[str, Any] | None = None,
    offline_only: bool = False,
    approval_required: bool = False,
    payload_ref: str = "",
) -> dict[str, Any]:
    resolution = resolve_request(
        intent=intent,
        capability=capability,
        offline_only=offline_only,
        approval_required=approval_required,
        payload_ref=payload_ref,
    )
    if resolution["status"] != "delegated":
        return resolution

    candidates = [
        service
        for service in _all_service_records()
        if service.service_id == resolution["destination_service"]
        and service.surface == resolution["destination_surface"]
    ]
    if not candidates:
        return {
            **resolution,
            "status": "unsupported",
            "message": "Resolved destination service is not currently dispatchable.",
        }

    service = candidates[0]
    if service.transport not in {"local-http", "https"}:
        return {
            **resolution,
            "status": "unsupported",
            "message": "Broker dispatch currently supports only local HTTP-style targets.",
        }

    route = _select_route(service, resolution["capability"], payload)
    if route is None:
        return {
            **resolution,
            "status": "unsupported",
            "message": "No dispatchable route is published for this capability.",
        }

    try:
        result = _dispatch_http_json(service, route, payload)
    except (error.URLError, ValueError, json.JSONDecodeError) as exc:
        return {
            **resolution,
            "status": "blocked_by_policy",
            "message": str(exc),
            "route": route,
        }

    return {
        **resolution,
        "status": "dispatched",
        "route": route,
        "result": result,
    }
