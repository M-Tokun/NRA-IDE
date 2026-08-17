"""Create-only witness checkpoints for irreversible latch heads."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from .irreversible_latch_store import (
    IrreversibleLatchHead,
    PersistentIrreversibleLatchStore,
)


@dataclass(frozen=True, slots=True)
class LatchHeadCheckpoint:
    sequence: int
    previous_mac: str | None
    row_mac: str
    checkpointed_at: str
    checkpoint_mac: str


class CreateOnlyLatchCheckpointStore:
    def __init__(self, root: Path, integrity_key: bytes) -> None:
        if not root.is_dir() or root.is_symlink():
            raise ValueError("latch checkpoint root must be an existing directory")
        _validate_key(integrity_key)
        self.root = root.resolve()
        self._integrity_key = integrity_key

    def latest(self) -> LatchHeadCheckpoint | None:
        checkpoints: list[LatchHeadCheckpoint] = []
        for path in self.root.glob("latch-head-*.json"):
            if not path.is_file() or path.is_symlink():
                raise ValueError("LATCH_CHECKPOINT_INVALID")
            checkpoint = self._decode(path.read_text(encoding="utf-8"))
            expected_name = f"latch-head-{checkpoint.sequence:020d}.json"
            if path.name != expected_name:
                raise ValueError("LATCH_CHECKPOINT_INVALID")
            checkpoints.append(checkpoint)
        if not checkpoints:
            return None
        checkpoints.sort(key=lambda checkpoint: checkpoint.sequence)
        if any(
            current.sequence <= previous.sequence
            for previous, current in zip(checkpoints, checkpoints[1:])
        ):
            raise ValueError("LATCH_CHECKPOINT_SEQUENCE_INVALID")
        return checkpoints[-1]

    def record(
        self,
        head: IrreversibleLatchHead,
        *,
        checkpointed_at: datetime,
    ) -> LatchHeadCheckpoint:
        if checkpointed_at.tzinfo is None:
            raise ValueError("checkpointed_at must be timezone-aware")
        fields = {
            "checkpointed_at": checkpointed_at.astimezone(timezone.utc).isoformat(),
            "previous_mac": head.previous_mac,
            "row_mac": head.row_mac,
            "sequence": head.sequence,
        }
        checkpoint = LatchHeadCheckpoint(
            head.sequence,
            head.previous_mac,
            head.row_mac,
            fields["checkpointed_at"],
            _mac(self._integrity_key, fields),
        )
        path = self.root / f"latch-head-{head.sequence:020d}.json"
        encoded = _canonical_json(asdict(checkpoint))
        try:
            with path.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(encoded)
                stream.flush()
                os.fsync(stream.fileno())
        except FileExistsError:
            existing = self._decode(path.read_text(encoding="utf-8"))
            if not _same_head(existing, checkpoint):
                raise ValueError("LATCH_CHECKPOINT_CONFLICT")
            return existing
        return checkpoint

    def _decode(self, encoded: str) -> LatchHeadCheckpoint:
        try:
            data = json.loads(encoded, object_pairs_hook=_pairs_hook)
            if not isinstance(data, dict) or set(data) != {
                "checkpoint_mac",
                "checkpointed_at",
                "previous_mac",
                "row_mac",
                "sequence",
            }:
                raise ValueError
            checkpoint = LatchHeadCheckpoint(**data)
            if (
                not isinstance(checkpoint.sequence, int)
                or isinstance(checkpoint.sequence, bool)
                or checkpoint.sequence <= 0
                or not _digest(checkpoint.row_mac)
                or (
                    checkpoint.previous_mac is not None
                    and not _digest(checkpoint.previous_mac)
                )
                or not isinstance(checkpoint.checkpointed_at, str)
                or not _digest(checkpoint.checkpoint_mac)
            ):
                raise ValueError
            parsed_time = datetime.fromisoformat(checkpoint.checkpointed_at)
            if parsed_time.tzinfo is None:
                raise ValueError
            fields = {
                "checkpointed_at": checkpoint.checkpointed_at,
                "previous_mac": checkpoint.previous_mac,
                "row_mac": checkpoint.row_mac,
                "sequence": checkpoint.sequence,
            }
            if not hmac.compare_digest(
                checkpoint.checkpoint_mac,
                _mac(self._integrity_key, fields),
            ):
                raise ValueError
            return checkpoint
        except (TypeError, ValueError, json.JSONDecodeError) as error:
            raise ValueError("LATCH_CHECKPOINT_INVALID") from error


def synchronize_latch_checkpoints(
    latch_store: PersistentIrreversibleLatchStore,
    checkpoint_stores: Sequence[CreateOnlyLatchCheckpointStore],
    *,
    checkpointed_at: datetime,
    minimum_witnesses: int = 2,
) -> None:
    if minimum_witnesses < 2 or len(checkpoint_stores) < minimum_witnesses:
        raise ValueError("LATCH_CHECKPOINT_QUORUM_CONFIG_INVALID")
    local_head = latch_store.head()
    latest_by_store = tuple(store.latest() for store in checkpoint_stores)
    if local_head is None:
        if any(checkpoint is not None for checkpoint in latest_by_store):
            raise ValueError("IRREVERSIBLE_LATCH_ROLLBACK")
        return

    matching = 0
    for store, checkpoint in zip(checkpoint_stores, latest_by_store):
        if checkpoint is not None:
            if checkpoint.sequence > local_head.sequence:
                raise ValueError("IRREVERSIBLE_LATCH_ROLLBACK")
            local_at_checkpoint = latch_store.head_at(checkpoint.sequence)
            if (
                local_at_checkpoint is None
                or checkpoint.row_mac != local_at_checkpoint.row_mac
                or checkpoint.previous_mac != local_at_checkpoint.previous_mac
            ):
                raise ValueError("LATCH_CHECKPOINT_CONFLICT")
        if checkpoint is None or checkpoint.sequence < local_head.sequence:
            checkpoint = store.record(
                local_head,
                checkpointed_at=checkpointed_at,
            )
        if _checkpoint_matches_head(checkpoint, local_head):
            matching += 1
    if matching < minimum_witnesses:
        raise ValueError("LATCH_CHECKPOINT_QUORUM_NOT_REACHED")


def _checkpoint_matches_head(
    checkpoint: LatchHeadCheckpoint,
    head: IrreversibleLatchHead,
) -> bool:
    return (
        checkpoint.sequence == head.sequence
        and checkpoint.previous_mac == head.previous_mac
        and checkpoint.row_mac == head.row_mac
    )


def _same_head(
    left: LatchHeadCheckpoint,
    right: LatchHeadCheckpoint,
) -> bool:
    return (
        left.sequence == right.sequence
        and left.previous_mac == right.previous_mac
        and left.row_mac == right.row_mac
    )


def _pairs_hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate field")
        result[key] = value
    return result


def _validate_key(key: bytes) -> None:
    if not isinstance(key, bytes) or len(key) < 32:
        raise ValueError("checkpoint integrity key must contain at least 32 bytes")


def _digest(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _canonical_json(data: dict[str, object]) -> str:
    return json.dumps(
        data,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _mac(key: bytes, fields: dict[str, object]) -> str:
    return hmac.new(
        key,
        _canonical_json(fields).encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
