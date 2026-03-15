from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from wizard.runtime_config import get_runtime_config, runtime_config_metadata


def test_runtime_config_uses_secret_store_for_secret_like_keys(tmp_path: Path) -> None:
    with patch.dict(
        "os.environ",
        {
            "UDOS_HOME": str(tmp_path / ".udos"),
            "WIZARD_STATE_ROOT": str(tmp_path / "state" / "wizard"),
        },
        clear=False,
    ):
        from wizard.secret_store import get_secret_store

        store = get_secret_store(root=tmp_path / "state" / "wizard")
        store.set_secret("OPENAI_API_KEY", "secret-value")

        assert get_runtime_config("OPENAI_API_KEY") == "secret-value"
        metadata = runtime_config_metadata("OPENAI_API_KEY")
        assert metadata["source"] == "secret-store"
        assert metadata["present"] is True


def test_runtime_config_prefers_env_over_secret_store(tmp_path: Path) -> None:
    with patch.dict(
        "os.environ",
        {
            "UDOS_HOME": str(tmp_path / ".udos"),
            "WIZARD_STATE_ROOT": str(tmp_path / "state" / "wizard"),
            "OPENAI_API_KEY": "env-value",
        },
        clear=False,
    ):
        from wizard.secret_store import get_secret_store

        store = get_secret_store(root=tmp_path / "state" / "wizard")
        store.set_secret("OPENAI_API_KEY", "secret-value")

        assert get_runtime_config("OPENAI_API_KEY") == "env-value"
        metadata = runtime_config_metadata("OPENAI_API_KEY")
        assert metadata["source"] == "process-env"
