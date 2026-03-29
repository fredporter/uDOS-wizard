from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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
            transport="local-kernel",
            offline_safe=True,
            dispatch_mode="direct",
            source="core-overlay",
            notes="Core owns schemas, validation, and offline-safe contracts.",
        )
    )
    return records


def _ubuntu_contract_records() -> list[ServiceRecord]:
    family_root = _family_root()
    host_surface_path = family_root / "uDOS-ubuntu" / "contracts" / "udos-commandd" / "wizard-host-surface.v1.json"
    minimum_ops_path = family_root / "uDOS-ubuntu" / "contracts" / "udos-commandd" / "minimum-operations.v1.json"
    explicit_surface_paths = (
        family_root / "uDOS-ubuntu" / "contracts" / "udos-commandd" / "okd-surface.v1.json",
        family_root / "uDOS-ubuntu" / "contracts" / "udos-commandd" / "library-surface.v1.json",
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
                    service_id="uDOS-ubuntu",
                    owner=str(payload.get("owner") or "uDOS-ubuntu"),
                    surface="host",
                    capabilities=host_capabilities,
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
                service_id=str(payload.get("service_id") or "uDOS-ubuntu"),
                owner=str(payload.get("owner") or "uDOS-ubuntu"),
                surface=str(payload.get("surface") or "unknown"),
                capabilities=tuple(str(capability) for capability in payload.get("capabilities", [])),
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
                service_id="uDOS-ubuntu",
                owner="uDOS-ubuntu",
                surface=surface,
                capabilities=tuple(sorted(entry["capabilities"])),
                transport=str(entry["transport"]),
                offline_safe=bool(entry["offline_safe"]),
                dispatch_mode="direct",
                source=str(minimum_ops_path) if minimum_ops_path.exists() else "ubuntu-overlay",
                notes=str(entry["notes"]),
            )
        )
    return records


def _all_service_records() -> list[ServiceRecord]:
    return _core_contract_records() + _ubuntu_contract_records() + _local_surface_records()


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
            "source": service.source,
            "notes": service.notes,
        }
        for service in _all_service_records()
    ]


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
