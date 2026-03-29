from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


def _utc_now_iso_z() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class ServiceRecord:
    service_id: str
    owner: str
    surface: str
    capabilities: tuple[str, ...]
    transport: str
    offline_safe: bool
    dispatch_mode: str
    notes: str = ""


SERVICE_REGISTRY: tuple[ServiceRecord, ...] = (
    ServiceRecord(
        service_id="uDOS-ubuntu",
        owner="uDOS-ubuntu",
        surface="okd",
        capabilities=("ok.transformation", "ok.research", "ok.ingest"),
        transport="https",
        offline_safe=False,
        dispatch_mode="direct",
        notes="Ubuntu owns OK execution and provider-backed fallback.",
    ),
    ServiceRecord(
        service_id="uDOS-ubuntu",
        owner="uDOS-ubuntu",
        surface="library",
        capabilities=("library.browse", "library.search", "binder.view"),
        transport="https",
        offline_safe=True,
        dispatch_mode="direct",
        notes="Ubuntu serves the local library and binder views.",
    ),
    ServiceRecord(
        service_id="uDOS-ubuntu",
        owner="uDOS-ubuntu",
        surface="network.beacon",
        capabilities=("beacon.status", "network.status"),
        transport="https",
        offline_safe=True,
        dispatch_mode="direct",
        notes="Ubuntu owns beacon and network state.",
    ),
    ServiceRecord(
        service_id="uDOS-surface",
        owner="uDOS-surface",
        surface="render",
        capabilities=("surface.preview", "surface.publish"),
        transport="https",
        offline_safe=True,
        dispatch_mode="direct",
        notes="Surface owns browser presentation and preview.",
    ),
    ServiceRecord(
        service_id="uDOS-core",
        owner="uDOS-core",
        surface="contracts",
        capabilities=("core.validate", "core.schema.lookup"),
        transport="local",
        offline_safe=True,
        dispatch_mode="direct",
        notes="Core owns schemas, validation, and offline-safe contracts.",
    ),
)


INTENT_TO_CAPABILITY: tuple[tuple[tuple[str, ...], str], ...] = (
    (("format", "cleanup", "transform"), "ok.transformation"),
    (("research", "summarize", "analyse", "analyze"), "ok.research"),
    (("ingest", "capture", "link"), "ok.ingest"),
    (("library", "browse", "binder"), "library.browse"),
    (("beacon", "network", "wifi"), "beacon.status"),
    (("preview", "publish", "render"), "surface.preview"),
    (("schema", "validate", "contract"), "core.validate"),
)


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
            "notes": service.notes,
        }
        for service in SERVICE_REGISTRY
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
        for service in SERVICE_REGISTRY
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
        "notes": service.notes,
    }
