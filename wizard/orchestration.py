from __future__ import annotations


class OrchestrationRegistry:
    def status(self) -> dict:
        return {
            "version": "v2.0.1",
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


def route_task(task: str, mode: str = "auto", surface: str = "assist") -> dict:
    if mode == "offline":
        return {
            "task": task,
            "mode": mode,
            "surface": surface,
            "provider": "local-fallback",
            "executor": "local-shell",
            "transport": "subprocess",
            "status": "queued",
        }

    if surface == "publish":
        return {
            "task": task,
            "mode": mode,
            "surface": surface,
            "provider": "wizard-provider",
            "executor": "publish-runner",
            "transport": "job-queue",
            "status": "queued",
        }

    return {
        "task": task,
        "mode": mode,
        "surface": surface,
        "provider": "wizard-provider",
        "executor": "provider-router",
        "transport": "https",
        "status": "queued",
    }
