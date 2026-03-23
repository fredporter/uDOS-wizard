from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

from .port_manager import build_base_url, resolve_bind_plan


DEFAULT_WIZARD_HOST = "127.0.0.1"
DEFAULT_WIZARD_PORT = 8787
DEFAULT_UHOME_HOST = "127.0.0.1"
DEFAULT_UHOME_PORT = 8000


def workspace_root() -> Path:
    return Path(__file__).resolve().parents[2]


def wizard_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def uhome_repo_root() -> Path:
    return workspace_root() / "uHOME-server"


def configured_uhome_base_url(default_host: str, default_port: int) -> str:
    override = str(os.environ.get("UHOME_SERVER_URL") or "").strip().rstrip("/")
    if override:
        return override
    return f"http://{default_host}:{default_port}"


def build_demo_links(wizard_base_url: str, uhome_base_url: str) -> dict[str, str]:
    return {
        "launch": f"{wizard_base_url}/app/launch",
        "workflow": f"{wizard_base_url}/app/workflow",
        "automation": f"{wizard_base_url}/app/automation",
        "publishing": f"{wizard_base_url}/app/publishing",
        "thin_gui": f"{wizard_base_url}/app/thin-gui",
        "config": f"{wizard_base_url}/app/config",
        "legacy_gui": f"{wizard_base_url}/gui",
        "thin": f"{wizard_base_url}/thin",
        "wizard_demo_links": f"{wizard_base_url}/demo",
        "uhome_thin_automation": f"{uhome_base_url}/api/runtime/thin/automation",
    }


def _print_demo_links(wizard_base_url: str, uhome_base_url: str) -> None:
    print("uDOS demo stack")
    for label, url in build_demo_links(wizard_base_url, uhome_base_url).items():
        print(f"{label}: {url}")


def _spawn_uhome(host: str, port: int) -> subprocess.Popen[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(uhome_repo_root() / "src")
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "uhome_server.app:app", "--host", host, "--port", str(port)],
        cwd=str(uhome_repo_root()),
        env=env,
        text=True,
    )


def _spawn_wizard(host: str, port: int, uhome_url: str) -> subprocess.Popen[str]:
    env = os.environ.copy()
    env["UDOS_WIZARD_HOST"] = host
    env["UDOS_WIZARD_PORT"] = str(port)
    env["UHOME_SERVER_URL"] = uhome_url
    return subprocess.Popen(
        [sys.executable, "-m", "wizard.main"],
        cwd=str(wizard_repo_root()),
        env=env,
        text=True,
    )


def main(argv: list[str] | None = None) -> int:
    cli_args = list(argv) if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(prog="udos-wizard-demo", description="Run the local Wizard + uHOME demo stack.")
    parser.add_argument("--wizard-host", default=DEFAULT_WIZARD_HOST)
    parser.add_argument("--wizard-port", type=int, default=DEFAULT_WIZARD_PORT)
    parser.add_argument("--uhome-host", default=DEFAULT_UHOME_HOST)
    parser.add_argument("--uhome-port", type=int, default=DEFAULT_UHOME_PORT)
    parser.add_argument("--no-uhome", action="store_true", help="Launch Wizard only.")
    args = parser.parse_args(cli_args)

    port_was_explicit = any(
        arg == "--wizard-port" or arg.startswith("--wizard-port=") for arg in cli_args
    )
    if port_was_explicit:
        bind_plan = resolve_bind_plan(host=args.wizard_host, port=args.wizard_port)
    else:
        bind_plan = resolve_bind_plan(host=args.wizard_host)
    wizard_base_url = build_base_url(bind_plan.host, bind_plan.port)
    uhome_base_url = configured_uhome_base_url(args.uhome_host, args.uhome_port)

    processes: list[subprocess.Popen[str]] = []
    try:
        if not args.no_uhome:
            processes.append(_spawn_uhome(args.uhome_host, args.uhome_port))
            time.sleep(1.0)
        processes.append(_spawn_wizard(bind_plan.host, bind_plan.port, uhome_base_url))
        time.sleep(1.0)
        if bind_plan.auto_shifted:
            print(
                f"uDOS demo stack: port {bind_plan.requested_port} unavailable; "
                f"using {bind_plan.port} for Wizard."
            )
        _print_demo_links(wizard_base_url, uhome_base_url)

        while True:
            for process in processes:
                code = process.poll()
                if code is not None:
                    return code
            time.sleep(0.5)
    except KeyboardInterrupt:
        return 0
    finally:
        for process in reversed(processes):
            if process.poll() is None:
                process.send_signal(signal.SIGTERM)
        for process in reversed(processes):
            if process.poll() is None:
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    process.kill()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
