from __future__ import annotations

from typing import Any


GOOGLE_MVP_LANE_ID = "google-mvp-a"
GOOGLE_MVP_NAME = "Google MVP A: Firestore mirror + Cloud Run binder + gameplay world export"


def get_google_mvp_lane_bundle() -> dict[str, Any]:
    return {
        "lane_id": GOOGLE_MVP_LANE_ID,
        "name": GOOGLE_MVP_NAME,
        "wizard_owner": "uDOS-wizard",
        "status": "active-definition",
        "provider_entry": {
            "owner": "uDOS-wizard",
            "provider_family": "wizard.gemini",
            "purpose": "prompt generation and extraction governance for Empire's Google lane",
        },
        "repo_targets": {
            "uDOS-empire": "Firestore mirror + Cloud Run binder supervision",
            "uDOS-gameplay": "multiplayer crypt-placement world",
            "uDOS-ubuntu": "always-on local mirror/cache host",
        },
        "non_negotiables": [
            "uDOS-core remains canonical truth",
            "Firestore is mirror storage only",
            "Google-backed services are optional and supervised",
            "generated output must be extracted into repo-owned artifacts",
        ],
        "prompt_template": get_google_mvp_prompt_template(),
        "extraction_checklist": get_google_mvp_extraction_checklist(),
        "generated_output_example": get_google_mvp_generated_output_example(),
    }


def get_google_mvp_prompt_template() -> dict[str, Any]:
    return {
        "lane_id": GOOGLE_MVP_LANE_ID,
        "provider_hint": "wizard.gemini",
        "task_class": "analysis",
        "complexity": "L4",
        "allowed_budget_groups": ["tier2_premium"],
        "prompt_sections": [
            "Build an optional supervised service for uDOS-empire.",
            "Use Firestore only as mirror storage for approved binder or vault artifacts.",
            "Expose a bounded Cloud Run binder-trigger route for approved mirror writes.",
            "Use Firebase Auth only for controlled collaborator or shared-room access when required.",
            "Do not treat Firestore, Firebase Auth, or Cloud Run as canonical uDOS truth.",
            "Produce explicit extraction artifacts for routes, schema, environment variables, auth model, and budget profile.",
            "Keep the service disposable and compatible with Ubuntu local-cache fallback.",
        ],
        "expected_outputs": [
            "route list",
            "Firestore collections and fields",
            "environment variable list",
            "auth model summary",
            "budget profile",
            "mirror eligibility rules",
        ],
    }


def get_google_mvp_extraction_checklist() -> dict[str, Any]:
    return {
        "lane_id": GOOGLE_MVP_LANE_ID,
        "required_artifacts": [
            "architecture summary",
            "route list",
            "environment variable list",
            "auth model summary",
            "Firestore collection and field summary",
            "dependency inventory",
            "deployment target summary",
            "mirror-eligibility rules",
            "uDOS mapping notes",
        ],
        "required_decisions": [
            "what stays generated",
            "what becomes native uDOS code",
            "what is mirrored into markdown or examples",
            "what remains rebuildable from local artifacts",
            "what can be replaced by self-hosted paths later",
        ],
        "promotion_path": [
            "prototype",
            "validated experiment",
            "extracted contract",
            "native module or approved optional connector",
        ],
    }


def get_google_mvp_generated_output_example() -> dict[str, Any]:
    return {
        "lane_id": GOOGLE_MVP_LANE_ID,
        "status": "extracted-example",
        "provider_family": "wizard.gemini",
        "service": {
            "name": "google-mvp-binder-trigger",
            "deployment_target": "cloud-run",
            "remote_role": "firestore-mirror",
        },
        "routes": [
            {
                "path": "/binder/google-mvp/mirror",
                "method": "POST",
                "purpose": "Receive approval-gated binder-trigger payloads for mirror writes",
            },
            {
                "path": "/binder/google-mvp/status/{record_key}",
                "method": "GET",
                "purpose": "Inspect remote mirror status for an extracted artifact",
            },
        ],
        "firestore_schema": {
            "collections": [
                {
                    "name": "binder_artifacts",
                    "fields": [
                        "record_key",
                        "artifact_ref",
                        "artifact_type",
                        "workflow_id",
                        "approval_state",
                        "mirrored_at",
                    ],
                }
            ]
        },
        "environment_variables": [
            "GOOGLE_CLOUD_PROJECT",
            "FIRESTORE_DATABASE",
            "BINDER_TRIGGER_SECRET",
            "GOOGLE_MVP_BUDGET_PROFILE",
        ],
        "auth_model": {
            "inbound": "shared-secret or service-auth",
            "shared_room": "firebase-auth optional",
        },
        "budget_profile": {
            "default": "sandbox",
            "idle_shutdown": "enabled",
            "mirror_write_scope": "approved artifacts only",
        },
        "mirror_eligibility_rules": [
            "artifact must be approved_for_mirror",
            "source_of_truth must remain vault",
            "record must be extractable into repo-owned docs or examples",
        ],
        "udos_mapping_notes": [
            "Empire owns service supervision and policy",
            "Ubuntu owns local cache and degraded-mode fallback",
            "Wizard owns prompt generation and extraction governance",
        ],
    }
