from __future__ import annotations

from udos_core.dev_config import load_dev_config

from .secret_store import get_secret_store

DEFAULT_RUNTIME_KEYS = (
    "UDOS_WIZARD_HOST",
    "UDOS_WIZARD_PORT",
    "UDOS_WIZARD_PORT_AUTO_SHIFT",
    "UHOME_SERVER_URL",
    "UDOS_STATE_ROOT",
    "WIZARD_STATE_ROOT",
    "UDOS_RENDER_ROOT",
    "OPENAI_API_KEY",
)


def _looks_secret_like(key: str) -> bool:
    upper = key.strip().upper()
    return upper.endswith(("_API_KEY", "_TOKEN", "_SECRET", "_PASSWORD"))


def get_runtime_config(key: str, default: str = "") -> str:
    config = load_dev_config()
    value = config.get_str(key, "")
    if value:
        return value
    if _looks_secret_like(key):
        secret_value = get_secret_store().get_secret(key)
        if secret_value:
            return secret_value
    return default


def runtime_config_metadata(key: str) -> dict[str, object]:
    config = load_dev_config()
    process_value = str(config.environ.get(key, "")).strip()
    if process_value:
        return {"key": key, "source": "process-env", "is_secret": _looks_secret_like(key), "present": True}

    repo_value = str(config.repo_env.get(key, "")).strip()
    if repo_value:
        return {"key": key, "source": "repo-env", "is_secret": _looks_secret_like(key), "present": True}

    home_value = str(config.home_env.get(key, "")).strip()
    if home_value:
        return {"key": key, "source": "home-env", "is_secret": _looks_secret_like(key), "present": True}

    secret_value = None
    if _looks_secret_like(key):
        secret_value = get_secret_store().get_secret(key)
    if secret_value:
        return {"key": key, "source": "secret-store", "is_secret": True, "present": True}

    state_value = config._state_value(key)
    if state_value:
        return {"key": key, "source": "local-state", "is_secret": _looks_secret_like(key), "present": True}

    return {"key": key, "source": "default", "is_secret": _looks_secret_like(key), "present": False}


def runtime_config_snapshot(keys: tuple[str, ...] = DEFAULT_RUNTIME_KEYS) -> dict[str, object]:
    entries: list[dict[str, object]] = []
    for key in keys:
        metadata = runtime_config_metadata(key)
        entry = dict(metadata)
        if metadata["present"] and not metadata["is_secret"]:
            entry["value"] = get_runtime_config(key, "")
        else:
            entry["value"] = None
        entries.append(entry)
    return {"keys": list(keys), "entries": entries, "count": len(entries)}
