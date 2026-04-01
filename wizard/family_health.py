"""Delegate family health probes to uDOS-ubuntu scripts (read-only / check lanes)."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any


def _wizard_package_root() -> Path:
    return Path(__file__).resolve().parent


def family_root() -> Path:
    """Parent of uDOS-wizard checkout (sibling uDOS-ubuntu, uDOS-core, …)."""
    return _wizard_package_root().parent.parent


def ubuntu_repo() -> Path:
    override = os.environ.get("UDOS_UBUNTU_ROOT", "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return (family_root() / "uDOS-ubuntu").resolve()


def _run_bash_script(script: Path, *, cwd: Path, timeout: int) -> dict[str, Any]:
    if not script.is_file():
        return {"skipped": True, "reason": f"missing script: {script.name}"}
    try:
        cp = subprocess.run(
            ["bash", str(script)],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        out: dict[str, Any] = {
            "script": str(script),
            "returncode": cp.returncode,
            "stdout": cp.stdout,
            "stderr": cp.stderr,
        }
        if cp.returncode == 0 and cp.stdout.strip():
            try:
                out["parsed"] = json.loads(cp.stdout.strip())
            except json.JSONDecodeError:
                out["parsed"] = None
        return out
    except subprocess.TimeoutExpired as exc:
        return {
            "script": str(script),
            "returncode": -1,
            "stdout": exc.stdout or "",
            "stderr": (exc.stderr or "") + "\n[timeout]",
            "timed_out": True,
        }
    except FileNotFoundError:
        return {"script": str(script), "skipped": True, "reason": "bash not found"}


def collect_family_health(*, include_ubuntu_checks: bool) -> dict[str, Any]:
    ub = ubuntu_repo()
    disk_script = ub / "scripts" / "report-udos-disk-library.sh"
    checks_script = ub / "scripts" / "run-ubuntu-checks.sh"

    payload: dict[str, Any] = {
        "version": "v1",
        "role": "wizard.family_health",
        "ubuntu_repo": str(ub),
        "ubuntu_repo_present": ub.is_dir(),
        "disk_library": _run_bash_script(disk_script, cwd=ub, timeout=120),
    }

    if include_ubuntu_checks:
        payload["ubuntu_checks"] = _run_bash_script(checks_script, cwd=ub, timeout=600)
    else:
        payload["ubuntu_checks"] = {
            "skipped": True,
            "reason": "pass include_ubuntu_checks=true to run run-ubuntu-checks.sh (slow)",
        }

    return payload
