from __future__ import annotations

from pathlib import Path

from wizard.secret_store import LocalSecretStore


def test_secret_store_round_trip_creates_key_and_payload(tmp_path: Path) -> None:
    store = LocalSecretStore(root=tmp_path)

    store.set_secret("api-token", "secret-value")

    assert store.get_secret("api-token") == "secret-value"
    assert (tmp_path / "secret-store.key").exists()
    assert (tmp_path / "secrets.enc").exists()


def test_secret_store_returns_none_when_payload_is_corrupt(tmp_path: Path) -> None:
    store = LocalSecretStore(root=tmp_path)
    store.set_secret("api-token", "secret-value")
    (tmp_path / "secrets.enc").write_bytes(b"broken")

    assert store.get_secret("api-token") is None


def test_secret_store_recovers_by_overwriting_corrupt_payload(tmp_path: Path) -> None:
    store = LocalSecretStore(root=tmp_path)
    store.set_secret("api-token", "secret-value")
    (tmp_path / "secrets.enc").write_bytes(b"broken")

    store.set_secret("next-token", "next-value")

    assert store.get_secret("next-token") == "next-value"
