from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


_PLACE_REF_RE = re.compile(r"^(?:[A-Z0-9:_-]+:)?[A-Z]{3}:L\d{3}-[A-Z]{2}\d{2}(?:-Z-?\d+)?$")
_SHORT_PLACE_RE = re.compile(r"^L\d{3}-[A-Z]{2}\d{2}(?:-Z-?\d+)?$")


def _grid_root() -> Path:
    return Path(__file__).resolve().parents[2] / "uDOS-grid"


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_grid_contract(name: str) -> dict[str, Any]:
    filename = {
        "grid-place": "place-record.contract.json",
        "grid-layer": "layer-record.contract.json",
        "grid-artifact": "artifact-record.contract.json",
    }.get(name)
    if not filename:
        raise ValueError(f"unknown grid contract: {name}")
    return _load_json(_grid_root() / "contracts" / filename)


def load_grid_seed(name: str) -> list[dict[str, Any]]:
    filename = {
        "layers": "basic-layer-registry.json",
        "places": "basic-place-registry.json",
        "artifacts": "basic-artifact-registry.json",
    }.get(name)
    if not filename:
        raise ValueError(f"unknown grid seed: {name}")
    payload = _load_json(_grid_root() / "seed" / filename)
    if not isinstance(payload, list):
        raise ValueError(f"expected list payload for grid seed: {name}")
    return payload


def resolve_place(place_ref: str) -> dict[str, Any]:
    cleaned = str(place_ref or "").strip()
    if not cleaned:
        return {"ok": False, "detail": "place_ref is required"}

    if not (_PLACE_REF_RE.match(cleaned) or _SHORT_PLACE_RE.match(cleaned)):
        return {"ok": False, "detail": "invalid place_ref format", "place_ref": cleaned}

    places = load_grid_seed("places")
    for record in places:
        place_id = str(record.get("place_id") or "")
        if place_id == cleaned or place_id.endswith(f":{cleaned}"):
            return {"ok": True, "place_ref": cleaned, "resolved": record}

    return {"ok": False, "detail": "place not found in starter grid seed", "place_ref": cleaned}


def validate_place(payload: dict[str, Any]) -> dict[str, Any]:
    place_ref = str(payload.get("place_ref") or "").strip()
    resolved = resolve_place(place_ref)
    if not resolved.get("ok"):
        return resolved

    record = resolved["resolved"]
    required_space = str(payload.get("required_space") or "").strip()
    artifact_id = str(payload.get("artifact_id") or "").strip()

    checks: dict[str, Any] = {
        "place_resolved": True,
        "space_match": True,
        "artifact_match": True,
    }

    if required_space:
        checks["space_match"] = str(record.get("space") or "") == required_space

    matched_artifact = None
    if artifact_id:
        artifacts = load_grid_seed("artifacts")
        for item in artifacts:
            if str(item.get("artifact_id") or "") != artifact_id:
                continue
            for item_place in item.get("places", []):
                if str(item_place) == place_ref or str(item_place) == str(record.get("place_id") or ""):
                    matched_artifact = item
                    break
            if matched_artifact is not None:
                break
        checks["artifact_match"] = matched_artifact is not None

    return {
        "ok": all(bool(value) for value in checks.values()),
        "place_ref": place_ref,
        "resolved": record,
        "checks": checks,
        "artifact": matched_artifact,
        "owner": "uDOS-grid",
        "consumer": "uDOS-wizard",
    }
