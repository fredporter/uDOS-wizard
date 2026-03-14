from __future__ import annotations

class BeaconNode:
    def announce(self) -> dict:
        return {"beacon": "announce", "status": "ok"}

    def connect(self, target: str) -> dict:
        return {"beacon": "connect", "target": target, "status": "ok"}

    def redirect(self, target: str) -> dict:
        return {"beacon": "redirect", "target": target, "status": "ok"}
