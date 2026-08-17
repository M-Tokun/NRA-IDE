"""Hard Boolean invariants for the bounded file-change shadow PoC."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from .evidence import AuthoritativeEvidence
from .proposal import (
    ActionProposal,
    ActionType,
    ChangeKind,
    EffectClass,
    ExecutionEnvironment,
)


_SHA256 = re.compile(r"[0-9a-f]{64}")
_IDEMPOTENCY_KEY = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{7,127}")


@dataclass(frozen=True, slots=True)
class FileChangePolicy:
    repository_root: Path
    max_patch_bytes: int = 64 * 1024
    allowed_suffixes: tuple[str, ...] = (
        ".md",
        ".py",
        ".json",
        ".toml",
        ".txt",
        ".yaml",
        ".yml",
    )
    # Grade-gating mechanism (design doc 7.2 / audit T3c): which effect
    # classes this deployment currently admits. The default preserves the
    # PoC's existing E1-only behavior exactly; broadening it is a deployment
    # decision, never automatic. E4_CRITICAL cannot be enabled through this
    # field at all (see violations()) because this PoC has no verified
    # fallback control or independent safety system to back it.
    enabled_effect_classes: frozenset[EffectClass] = frozenset(
        {EffectClass.E1_REVERSIBLE}
    )

    def __post_init__(self) -> None:
        if self.max_patch_bytes <= 0:
            raise ValueError("max_patch_bytes must be positive")
        if not self.allowed_suffixes:
            raise ValueError("allowed_suffixes must not be empty")
        if not isinstance(self.enabled_effect_classes, frozenset) or not all(
            isinstance(effect_class, EffectClass)
            for effect_class in self.enabled_effect_classes
        ):
            raise ValueError(
                "enabled_effect_classes must be a frozenset of EffectClass"
            )
        if EffectClass.E4_CRITICAL in self.enabled_effect_classes:
            raise ValueError(
                "E4_CRITICAL cannot be enabled: no verified fallback "
                "control or independent safety system exists in this PoC"
            )

    @property
    def resolved_root(self) -> Path:
        return self.repository_root.resolve()

    def resolve_target(self, resource_path: str) -> Path:
        return (self.resolved_root / PurePosixPath(resource_path)).resolve()

    def violations(
        self,
        proposal: ActionProposal,
        evidence: AuthoritativeEvidence,
    ) -> tuple[str, ...]:
        violations: list[str] = []
        if proposal.schema_version != "1.0":
            violations.append("UNSUPPORTED_SCHEMA_VERSION")
        if not isinstance(proposal.action_type, ActionType):
            violations.append("UNKNOWN_ACTION_TYPE")
        if not isinstance(proposal.change_kind, ChangeKind):
            violations.append("UNKNOWN_CHANGE_KIND")
        if not isinstance(proposal.environment, ExecutionEnvironment):
            violations.append("UNKNOWN_ENVIRONMENT")
        elif proposal.environment is ExecutionEnvironment.LIVE:
            violations.append("LIVE_ENVIRONMENT_FORBIDDEN")
        if not isinstance(proposal.effect_class, EffectClass):
            violations.append("UNKNOWN_EFFECT_CLASS")
        elif proposal.effect_class is EffectClass.E4_CRITICAL:
            # Defense in depth: __post_init__ already refuses to construct a
            # policy that enables E4; this repeats the refusal here so a
            # future bypass of the constructor guard still cannot permit it.
            violations.append("EFFECT_CLASS_NOT_ALLOWED")
        elif proposal.effect_class not in self.enabled_effect_classes:
            violations.append("EFFECT_CLASS_NOT_ALLOWED")
        if proposal.state_version < 0:
            violations.append("NEGATIVE_STATE_VERSION")
        if not _IDEMPOTENCY_KEY.fullmatch(proposal.idempotency_key):
            violations.append("INVALID_IDEMPOTENCY_KEY")

        patch_size = len(proposal.patch.encode("utf-8"))
        if patch_size == 0:
            violations.append("EMPTY_PATCH")
        if patch_size > self.max_patch_bytes:
            violations.append("PATCH_TOO_LARGE")

        patch_lines = proposal.patch.splitlines()
        old_headers = tuple(line for line in patch_lines if line.startswith("--- "))
        new_headers = tuple(line for line in patch_lines if line.startswith("+++ "))
        if len(old_headers) != 1 or len(new_headers) != 1:
            violations.append("SINGLE_FILE_UNIFIED_DIFF_REQUIRED")
        elif proposal.change_kind is ChangeKind.MODIFY:
            if old_headers != (f"--- a/{proposal.resource_path}",) or new_headers != (
                f"+++ b/{proposal.resource_path}",
            ):
                violations.append("PATCH_HEADER_PATH_MISMATCH")
        elif proposal.change_kind is ChangeKind.CREATE:
            if old_headers != ("--- /dev/null",) or new_headers != (
                f"+++ b/{proposal.resource_path}",
            ):
                violations.append("CREATE_PATCH_HEADER_MISMATCH")

        destructive_markers = (
            "deleted file mode ",
            "rename from ",
            "rename to ",
            "+++ /dev/null",
        )
        if any(
            line.startswith(destructive_markers)
            for line in patch_lines
        ):
            violations.append("DESTRUCTIVE_PATCH_FORBIDDEN")

        path = PurePosixPath(proposal.resource_path)
        path_text = proposal.resource_path
        if (
            not path_text
            or path.is_absolute()
            or path_text.startswith(("/", "\\"))
            or "\\" in path_text
            or ":" in path_text
            or any(part in {"", ".", ".."} for part in path.parts)
        ):
            violations.append("INVALID_RESOURCE_PATH")
        else:
            target = self.resolve_target(path_text)
            try:
                inside_root = os.path.commonpath(
                    (str(self.resolved_root), str(target))
                ) == str(self.resolved_root)
            except ValueError:
                inside_root = False
            if not inside_root:
                violations.append("SCOPE_ESCAPE")
            if evidence.resolved_path.resolve() != target:
                violations.append("RESOLVED_PATH_MISMATCH")

            folded_parts = {part.casefold() for part in path.parts}
            forbidden_parts = {
                ".env",
                ".git",
                ".ssh",
                "credentials",
                "secrets",
            }
            if folded_parts & forbidden_parts:
                violations.append("SECRET_OR_CONTROL_PATH")

            forbidden_names = {
                "requirements.txt",
                "pyproject.toml",
                "poetry.lock",
                "package-lock.json",
                "pnpm-lock.yaml",
                "yarn.lock",
            }
            if path.name.casefold() in forbidden_names:
                violations.append("DEPENDENCY_CHANGE_FORBIDDEN")
            if path.suffix.casefold() not in self.allowed_suffixes:
                violations.append("FILE_TYPE_NOT_ALLOWED")

            if proposal.action_type is ActionType.PROPOSE_TEST_FILE:
                is_test_path = "tests" in folded_parts or path.name.casefold().startswith(
                    "test_"
                )
                if not is_test_path:
                    violations.append("TEST_FILE_PATH_REQUIRED")

        if evidence.resource_path != proposal.resource_path:
            violations.append("EVIDENCE_RESOURCE_MISMATCH")
        if evidence.target_is_symlink:
            violations.append("SYMLINK_TARGET_FORBIDDEN")

        if proposal.change_kind is ChangeKind.MODIFY:
            if not evidence.target_exists:
                violations.append("MODIFY_TARGET_MISSING")
            if proposal.base_sha256 is None or not _SHA256.fullmatch(
                proposal.base_sha256
            ):
                violations.append("INVALID_BASE_HASH")
            elif proposal.base_sha256 != evidence.current_sha256:
                violations.append("BASE_HASH_MISMATCH")
        elif proposal.change_kind is ChangeKind.CREATE:
            if evidence.target_exists:
                violations.append("CREATE_TARGET_EXISTS")
            if proposal.base_sha256 is not None:
                violations.append("CREATE_MUST_NOT_HAVE_BASE_HASH")

        if (
            proposal.action_type is ActionType.PROPOSE_PATCH
            and proposal.change_kind is not ChangeKind.MODIFY
        ):
            violations.append("PATCH_ACTION_REQUIRES_MODIFY")
        if (
            proposal.action_type is ActionType.PROPOSE_TEST_FILE
            and proposal.change_kind is not ChangeKind.CREATE
        ):
            violations.append("TEST_ACTION_REQUIRES_CREATE")

        return tuple(dict.fromkeys(violations))
