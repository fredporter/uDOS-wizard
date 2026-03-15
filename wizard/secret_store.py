from __future__ import annotations

import json
import os
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken

from udos_core.dev_config import wizard_state_root


class SecretStoreError(Exception):
    pass


class LocalSecretStore:
    def __init__(self, root: Path | None = None) -> None:
        self.root = Path(root).expanduser().resolve() if root else wizard_state_root()
        self.payload_path = self.root / "secrets.enc"
        self.key_path = self.root / "secret-store.key"

    def _ensure_root(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)

    def _fernet(self) -> Fernet:
        self._ensure_root()
        if not self.key_path.exists():
            self.key_path.write_bytes(Fernet.generate_key())
            try:
                os.chmod(self.key_path, 0o600)
            except OSError:
                pass
        return Fernet(self.key_path.read_bytes().strip())

    def _read_payload(self) -> dict[str, str]:
        if not self.payload_path.exists():
            return {}
        try:
            encrypted = self.payload_path.read_bytes()
            if not encrypted:
                return {}
            payload = json.loads(self._fernet().decrypt(encrypted).decode("utf-8"))
        except (InvalidToken, OSError, ValueError, json.JSONDecodeError) as exc:
            raise SecretStoreError("unable to decrypt local secret store") from exc
        if not isinstance(payload, dict):
            raise SecretStoreError("invalid local secret store payload")
        return {str(key): str(value) for key, value in payload.items() if value}

    def _write_payload(self, payload: dict[str, str]) -> None:
        self._ensure_root()
        encrypted = self._fernet().encrypt(
            json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
        )
        self.payload_path.write_bytes(encrypted)

    def get_secret(self, key: str) -> str | None:
        try:
            payload = self._read_payload()
        except SecretStoreError:
            return None
        value = str(payload.get(key) or "").strip()
        return value or None

    def set_secret(self, key: str, value: str) -> None:
        try:
            payload = self._read_payload()
        except SecretStoreError:
            payload = {}
        payload[key] = value
        self._write_payload(payload)

    def list_secret_keys(self) -> list[str]:
        try:
            payload = self._read_payload()
        except SecretStoreError:
            return []
        return sorted(payload.keys())


_store: LocalSecretStore | None = None


def get_secret_store(root: Path | None = None) -> LocalSecretStore:
    global _store
    if root is not None:
        return LocalSecretStore(root=root)
    resolved_root = wizard_state_root()
    if _store is None or _store.root != resolved_root:
        _store = LocalSecretStore(root=resolved_root)
    return _store


def get_secret(key: str) -> str | None:
    return get_secret_store().get_secret(key)


def set_secret(key: str, value: str) -> None:
    get_secret_store().set_secret(key, value)
