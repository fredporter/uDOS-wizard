from __future__ import annotations

def route_assist(task: str, mode: str = "auto") -> dict:
    provider = "local-fallback" if mode == "offline" else "wizard-provider"
    return {
        "task": task,
        "mode": mode,
        "provider": provider,
        "status": "queued"
    }
