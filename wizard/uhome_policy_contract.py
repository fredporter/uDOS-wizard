from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field, ValidationError


ContractsRoot = Path(__file__).resolve().parents[1] / "contracts"


PROFILE_RULES: dict[str, dict[str, Any]] = {
    "beacon": {
        "network_scope": "public",
        "visibility": {"visible"},
        "auth_mode": {"open"},
    },
    "crypt": {
        "network_scope": "private",
        "visibility": {"visible"},
        "auth_mode": {"password-protected"},
    },
    "tomb": {
        "network_scope": "private",
        "visibility": {"hidden"},
        "auth_mode": {"discovery-based"},
    },
    "home": {
        "network_scope": "household",
        "visibility": {"visible", "hidden"},
        "auth_mode": {"password-protected"},
    },
}


class UHomeNetworkPolicyPayload(BaseModel):
    contract_version: Literal["v2.0.4"]
    profile_id: Literal["beacon", "crypt", "tomb", "home"]
    network_scope: Literal["public", "private", "household"]
    visibility: Literal["visible", "hidden"]
    auth_mode: Literal["open", "password-protected", "discovery-based"]
    vault_access: Literal["local-only"]
    internet_sharing: Literal["disabled"]
    runtime_owner: Literal["uHOME-server"]
    policy_owner: Literal["uDOS-wizard"]
    consumer_repos: list[Literal["uHOME-server", "uHOME-empire", "sonic-screwdriver"]] = Field(min_length=1)
    secret_refs: list[str] = Field(default_factory=list)
    notes: str | None = None


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return payload


def get_uhome_network_policy_contract() -> dict[str, Any]:
    return _read_json(ContractsRoot / "uhome-network-policy-contract.json")


def get_uhome_network_policy_schema() -> dict[str, Any]:
    return _read_json(ContractsRoot / "uhome-network-policy.schema.json")


def validate_uhome_network_policy(payload: dict[str, Any]) -> dict[str, Any]:
    model = UHomeNetworkPolicyPayload.model_validate(payload)
    rules = PROFILE_RULES[model.profile_id]
    issues: list[str] = []

    if model.network_scope != rules["network_scope"]:
        issues.append(
            f"profile {model.profile_id} requires network_scope={rules['network_scope']}"
        )
    if model.visibility not in rules["visibility"]:
        issues.append(
            f"profile {model.profile_id} requires visibility in {sorted(rules['visibility'])}"
        )
    if model.auth_mode not in rules["auth_mode"]:
        issues.append(
            f"profile {model.profile_id} requires auth_mode in {sorted(rules['auth_mode'])}"
        )

    if issues:
        raise ValueError("; ".join(issues))

    return model.model_dump()


def uhome_network_policy_validation_error(exc: ValidationError | ValueError) -> dict[str, Any]:
    if isinstance(exc, ValidationError):
        return {
            "ok": False,
            "error": "uhome-network-policy-validation-failed",
            "issues": exc.errors(),
        }
    return {
        "ok": False,
        "error": "uhome-network-policy-validation-failed",
        "issues": [{"message": str(exc)}],
    }
