from __future__ import annotations

import socket
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


def _ensure_core_on_path() -> None:
    core_root = Path(__file__).resolve().parents[2] / "uDOS-core"
    core_root_str = str(core_root)
    if core_root.exists() and core_root_str not in sys.path:
        sys.path.insert(0, core_root_str)


_ensure_core_on_path()

from udos_core.dev_config import get_bool, get_int, get_str


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8787
PORT_SEARCH_LIMIT = 25


@dataclass(frozen=True)
class PortOccupant:
    pid: int
    process: str
    port: int


@dataclass(frozen=True)
class BindPlan:
    host: str
    port: int
    requested_port: int
    port_source: str
    auto_shifted: bool
    occupant: PortOccupant | None = None


@dataclass(frozen=True)
class RuntimeBindStatus:
    host: str
    port: int
    base_url: str
    gui_url: str
    thin_url: str
    requested_port: int
    port_source: str
    auto_shifted: bool
    occupant: PortOccupant | None
    actual_binding_known: bool


def _env_flag(name: str, default: bool = False) -> bool:
    return get_bool(name, default)


def configured_host() -> str:
    return get_str("UDOS_WIZARD_HOST", DEFAULT_HOST).strip() or DEFAULT_HOST


def configured_port() -> tuple[int, str]:
    raw = get_str("UDOS_WIZARD_PORT", "")
    if not raw.strip():
        return DEFAULT_PORT, "default"
    return get_int("UDOS_WIZARD_PORT", DEFAULT_PORT), "env"


def detect_port_occupant(port: int) -> PortOccupant | None:
    try:
        result = subprocess.run(
            ["lsof", "-nP", f"-iTCP:{port}", "-sTCP:LISTEN"],
            capture_output=True,
            text=True,
            check=False,
            timeout=2,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        return None

    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if len(lines) < 2:
        return None

    parts = lines[1].split()
    if len(parts) < 2:
        return None

    try:
        pid = int(parts[1])
    except ValueError:
        return None

    return PortOccupant(pid=pid, process=parts[0], port=port)


def is_port_available(host: str, port: int) -> bool:
    family = socket.AF_INET6 if ":" in host else socket.AF_INET
    with socket.socket(family, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, port))
        except OSError:
            return False
    return True


def find_available_port(host: str, start_port: int, limit: int = PORT_SEARCH_LIMIT) -> int | None:
    for candidate in range(start_port + 1, start_port + limit + 1):
        if is_port_available(host, candidate):
            return candidate
    return None


def resolve_bind_plan(host: str | None = None, port: int | None = None) -> BindPlan:
    resolved_host = host or configured_host()
    if port is None:
        requested_port, port_source = configured_port()
    else:
        requested_port, port_source = port, "argument"

    if is_port_available(resolved_host, requested_port):
        return BindPlan(
            host=resolved_host,
            port=requested_port,
            requested_port=requested_port,
            port_source=port_source,
            auto_shifted=False,
            occupant=None,
        )

    occupant = detect_port_occupant(requested_port)
    auto_shift_allowed = (
        port_source == "default" and _env_flag("UDOS_WIZARD_PORT_AUTO_SHIFT", default=True)
    )
    if auto_shift_allowed:
        candidate = find_available_port(resolved_host, requested_port)
        if candidate is not None:
            return BindPlan(
                host=resolved_host,
                port=candidate,
                requested_port=requested_port,
                port_source=port_source,
                auto_shifted=True,
                occupant=occupant,
            )

    raise RuntimeError(format_bind_failure(resolved_host, requested_port, port_source, occupant))


def format_bind_failure(
    host: str,
    port: int,
    port_source: str,
    occupant: PortOccupant | None,
) -> str:
    base = f"Wizard could not bind {host}:{port} (source={port_source})."
    if occupant is None:
        return (
            f"{base} The port is already in use. Set UDOS_WIZARD_PORT to a free port "
            "or stop the existing listener."
        )
    return (
        f"{base} Occupied by {occupant.process} (PID {occupant.pid}). "
        "Stop that process or set UDOS_WIZARD_PORT to a free port."
    )


def build_base_url(host: str, port: int) -> str:
    display_host = "127.0.0.1" if host in {"0.0.0.0", "::", ""} else host
    return f"http://{display_host}:{port}"


def runtime_bind_status_from_plan(bind_plan: BindPlan, actual_binding_known: bool = True) -> RuntimeBindStatus:
    base_url = build_base_url(bind_plan.host, bind_plan.port)
    return RuntimeBindStatus(
        host=bind_plan.host,
        port=bind_plan.port,
        base_url=base_url,
        gui_url=f"{base_url}/gui",
        thin_url=f"{base_url}/thin",
        requested_port=bind_plan.requested_port,
        port_source=bind_plan.port_source,
        auto_shifted=bind_plan.auto_shifted,
        occupant=bind_plan.occupant,
        actual_binding_known=actual_binding_known,
    )


def configured_runtime_bind_status() -> RuntimeBindStatus:
    host = configured_host()
    port, source = configured_port()
    base_url = build_base_url(host, port)
    return RuntimeBindStatus(
        host=host,
        port=port,
        base_url=base_url,
        gui_url=f"{base_url}/gui",
        thin_url=f"{base_url}/thin",
        requested_port=port,
        port_source=source,
        auto_shifted=False,
        occupant=detect_port_occupant(port),
        actual_binding_known=False,
    )
