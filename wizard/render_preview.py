from __future__ import annotations

import sys
from pathlib import Path


def _ensure_core_on_path() -> None:
    core_root = Path(__file__).resolve().parents[2] / "uDOS-core"
    core_root_str = str(core_root)
    if core_root.exists() and core_root_str not in sys.path:
        sys.path.insert(0, core_root_str)


_ensure_core_on_path()

from udos_core.render import RenderEngine  # noqa: E402


engine = RenderEngine()


def render_contract() -> dict:
    return engine.contract()


def list_render_presets() -> dict:
    return {
        "prose_presets": engine.prose_presets(),
        "theme_adapters": engine.theme_adapters(),
        "gameplay_skins": engine.gameplay_skins(),
    }


def render_preview(markdown_text: str, metadata: dict | None = None, target: str = "gui-preview") -> dict:
    return engine.preview(markdown_text=markdown_text, metadata=metadata, target=target)


def export_render(markdown_text: str, metadata: dict | None = None, target: str = "web-prose") -> dict:
    return engine.export(markdown_text=markdown_text, metadata=metadata, target=target)


def list_render_exports() -> dict:
    return {"exports": engine.list_exports()}


def render_export_detail(target: str, slug: str) -> dict:
    return engine.export_detail(target=target, slug=slug)
