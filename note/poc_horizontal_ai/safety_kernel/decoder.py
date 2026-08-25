"""Strict, exception-contained decoder for untrusted action proposals."""

from __future__ import annotations

import json
import unicodedata
from dataclasses import dataclass
from typing import Any

from .proposal import (
    ActionProposal,
    ActionType,
    ChangeKind,
    EffectClass,
    ExecutionEnvironment,
)


_FIELDS = {
    "schema_version",
    "action_type",
    "change_kind",
    "resource_path",
    "patch",
    "state_version",
    "base_sha256",
    "idempotency_key",
    "environment",
    "effect_class",
}


@dataclass(frozen=True, slots=True)
class ProposalDecodeResult:
    proposal: ActionProposal | None
    reason_codes: tuple[str, ...]
    input_digest_material: bytes


class _DuplicateKey(ValueError):
    pass


def _object_without_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKey(key)
        result[key] = value
    return result


def decode_action_proposal(
    raw: str | bytes,
    *,
    max_input_bytes: int = 128 * 1024,
    max_patch_bytes: int = 64 * 1024,
) -> ProposalDecodeResult:
    """Decode one bounded, strict UTF-8 JSON action proposal.

    ``max_input_bytes`` limits the complete encoded request and
    ``max_patch_bytes`` independently limits the patch field. Duplicate or
    unknown fields, non-NFC text, invalid enum values, and size violations are
    returned as reason codes with no proposal. ``raw_bytes`` preserves the
    observable input for audit even when decoding fails.
    """
    reasons: list[str] = []
    if isinstance(raw, str):
        try:
            raw_bytes = raw.encode("utf-8", errors="strict")
        except UnicodeEncodeError:
            return ProposalDecodeResult(None, ("INPUT_NOT_UTF8",), b"")
        text = raw
    elif isinstance(raw, bytes):
        raw_bytes = raw
        try:
            text = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError:
            return ProposalDecodeResult(None, ("INPUT_NOT_UTF8",), raw_bytes)
    else:
        return ProposalDecodeResult(None, ("INPUT_NOT_TEXT_OR_BYTES",), b"")

    if len(raw_bytes) > max_input_bytes:
        return ProposalDecodeResult(None, ("INPUT_TOO_LARGE",), raw_bytes)
    if unicodedata.normalize("NFC", text) != text:
        return ProposalDecodeResult(None, ("INPUT_NOT_NFC",), raw_bytes)

    try:
        data = json.loads(text, object_pairs_hook=_object_without_duplicates)
    except _DuplicateKey:
        return ProposalDecodeResult(None, ("DUPLICATE_FIELD",), raw_bytes)
    except (json.JSONDecodeError, RecursionError):
        return ProposalDecodeResult(None, ("INVALID_JSON",), raw_bytes)

    if not isinstance(data, dict):
        return ProposalDecodeResult(None, ("ROOT_MUST_BE_OBJECT",), raw_bytes)
    unknown = set(data) - _FIELDS
    missing = _FIELDS - set(data)
    if unknown:
        reasons.append("UNKNOWN_FIELDS")
    if missing:
        reasons.append("MISSING_FIELDS")
    if reasons:
        return ProposalDecodeResult(None, tuple(reasons), raw_bytes)

    string_fields = (
        "schema_version",
        "action_type",
        "change_kind",
        "resource_path",
        "patch",
        "idempotency_key",
        "environment",
        "effect_class",
    )
    if any(not isinstance(data[field], str) for field in string_fields):
        reasons.append("INVALID_FIELD_TYPE")
    if not isinstance(data["state_version"], int) or isinstance(
        data["state_version"], bool
    ):
        reasons.append("INVALID_STATE_VERSION_TYPE")
    if data["base_sha256"] is not None and not isinstance(
        data["base_sha256"], str
    ):
        reasons.append("INVALID_BASE_HASH_TYPE")
    if reasons:
        return ProposalDecodeResult(None, tuple(reasons), raw_bytes)

    if len(data["resource_path"]) > 4096:
        reasons.append("RESOURCE_PATH_TOO_LONG")
    if len(data["idempotency_key"]) > 128:
        reasons.append("IDEMPOTENCY_KEY_TOO_LONG")
    if len(data["patch"].encode("utf-8")) > max_patch_bytes:
        reasons.append("PATCH_TOO_LARGE")
    if any(
        unicodedata.normalize("NFC", data[field]) != data[field]
        for field in string_fields
    ):
        reasons.append("FIELD_NOT_NFC")

    try:
        action_type = ActionType(data["action_type"])
        change_kind = ChangeKind(data["change_kind"])
        environment = ExecutionEnvironment(data["environment"])
        effect_class = EffectClass(data["effect_class"])
    except ValueError:
        reasons.append("UNKNOWN_ENUM_VALUE")
        return ProposalDecodeResult(None, tuple(reasons), raw_bytes)
    if reasons:
        return ProposalDecodeResult(None, tuple(reasons), raw_bytes)

    return ProposalDecodeResult(
        ActionProposal(
            schema_version=data["schema_version"],
            action_type=action_type,
            change_kind=change_kind,
            resource_path=data["resource_path"],
            patch=data["patch"],
            state_version=data["state_version"],
            base_sha256=data["base_sha256"],
            idempotency_key=data["idempotency_key"],
            environment=environment,
            effect_class=effect_class,
        ),
        (),
        raw_bytes,
    )
