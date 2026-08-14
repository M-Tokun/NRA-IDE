"""Create-only witness stores and quorum checks for signed anchor receipts."""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Mapping, Sequence

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from .signed_boundary import verify_signed_anchor_receipt


@dataclass(frozen=True, slots=True)
class WitnessRecord:
    witness_id: str
    audit_head_digest: str
    signed_receipt_sha256: str
    record_path: Path


@dataclass(frozen=True, slots=True)
class WitnessQuorumAssessment:
    satisfied: bool
    matching_witness_ids: tuple[str, ...]
    reason_codes: tuple[str, ...]


class CreateOnlyWitnessStore:
    def __init__(self, root: Path, witness_id: str) -> None:
        if not root.is_dir() or root.is_symlink():
            raise ValueError("witness root must be an existing non-symlink directory")
        if not witness_id or len(witness_id) > 128:
            raise ValueError("invalid witness_id")
        self.root = root.resolve()
        self.witness_id = witness_id

    def record(
        self,
        signed_receipt_json: str,
        *,
        trusted_public_keys: Mapping[str, Ed25519PublicKey],
        signature_max_age: timedelta,
    ) -> WitnessRecord:
        verified = verify_signed_anchor_receipt(
            signed_receipt_json,
            trusted_public_keys=trusted_public_keys,
            signature_max_age=signature_max_age,
        )
        if verified.receipt is None:
            raise ValueError(",".join(verified.reason_codes))
        digest = hashlib.sha256(signed_receipt_json.encode("utf-8")).hexdigest()
        path = self.root / f"{verified.receipt.audit_head_digest}.signed.json"
        try:
            with path.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(signed_receipt_json)
                stream.flush()
                os.fsync(stream.fileno())
        except FileExistsError:
            existing = path.read_text(encoding="utf-8")
            if existing != signed_receipt_json:
                raise ValueError("witness head already has different receipt")
        return WitnessRecord(
            self.witness_id,
            verified.receipt.audit_head_digest,
            digest,
            path,
        )

    def read_digest(self, audit_head_digest: str) -> str | None:
        path = self.root / f"{audit_head_digest}.signed.json"
        if not path.is_file() or path.is_symlink():
            return None
        return hashlib.sha256(path.read_bytes()).hexdigest()


def assess_witness_quorum(
    records: Sequence[WitnessRecord],
    *,
    audit_head_digest: str,
    signed_receipt_sha256: str,
    minimum_witnesses: int,
) -> WitnessQuorumAssessment:
    if minimum_witnesses < 2:
        return WitnessQuorumAssessment(
            False,
            (),
            ("WITNESS_QUORUM_CONFIGURATION_INVALID",),
        )
    matching = tuple(
        sorted(
            {
                record.witness_id
                for record in records
                if record.audit_head_digest == audit_head_digest
                and record.signed_receipt_sha256 == signed_receipt_sha256
                and record.record_path.is_file()
                and not record.record_path.is_symlink()
                and hashlib.sha256(record.record_path.read_bytes()).hexdigest()
                == signed_receipt_sha256
            }
        )
    )
    if len(matching) < minimum_witnesses:
        return WitnessQuorumAssessment(
            False,
            matching,
            ("WITNESS_QUORUM_NOT_REACHED",),
        )
    return WitnessQuorumAssessment(True, matching, ())
