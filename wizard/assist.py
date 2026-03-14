from __future__ import annotations
from .orchestration import route_task

def route_assist(task: str, mode: str = "auto") -> dict:
    return route_task(task=task, mode=mode, surface="assist")
