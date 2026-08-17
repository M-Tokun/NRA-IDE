"""Adapter tests: FileChangePolicy connected to the trusted-runtime hook.

These tests exercise ``FileChangeInvariantAdapter`` directly against a
temporary repository with real files, plus the ``FileChangeContext``
validation and the signed-authorization encode/decode round trip. The
runtime-side wiring (the hook calling the callable and rejecting before the
executor) is covered by the existing execution-gate tests in
``test_latch_witness.py``; this file focuses on the file-change domain
connection itself.
"""

import hashlib
import tempfile
import unittest
from pathlib import Path

from note.poc_horizontal_ai.safety_kernel import FileChangePolicy
from note.poc_horizontal_ai.safety_kernel.proposal import ExecutionEnvironment
from note.poc_horizontal_ai.trusted_runtime.execution_gate import (
    BoundaryExecutionIntent,
    FileChangeContext,
    _decode_file_change,
    _encode_file_change,
)
from note.poc_horizontal_ai.trusted_runtime.file_change_invariant_adapter import (
    FileChangeInvariantAdapter,
)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def modify_diff(path: str, old_line: str, new_line: str) -> bytes:
    return (
        f"--- a/{path}\n"
        f"+++ b/{path}\n"
        "@@ -1,1 +1,1 @@\n"
        f"-{old_line}\n"
        f"+{new_line}\n"
    ).encode("utf-8")


def create_diff(path: str, line: str) -> bytes:
    return (
        "--- /dev/null\n"
        f"+++ b/{path}\n"
        "@@ -0,0 +1,1 @@\n"
        f"+{line}\n"
    ).encode("utf-8")


def make_intent(
    *,
    resource_path: str,
    change_kind: str,
    action_type: str,
    action: bytes,
    expected_base_sha256: str | None,
    state_version: int = 0,
    intent_id: str = "intent-change-001",
) -> BoundaryExecutionIntent:
    context = FileChangeContext(
        resource_path=resource_path,
        change_kind=change_kind,
        action_type=action_type,
        expected_base_sha256=expected_base_sha256,
        state_version=state_version,
    )
    return BoundaryExecutionIntent(
        intent_id=intent_id,
        subject_id="subject-file-change-tests",
        action_type=action_type,
        target_id=f"file:{resource_path}",
        action_digest=hashlib.sha256(action).hexdigest(),
        policy_version="policy-v1",
        postcondition_subject=resource_path,
        postcondition_field="sha256",
        required_postcondition_value=("6" * 64),
        file_change=context,
    )


class FileChangeInvariantAdapterTests(unittest.TestCase):
    def make_adapter(self) -> tuple[Path, FileChangeInvariantAdapter]:
        repository = Path(tempfile.mkdtemp(prefix="t1-adapter-"))
        source = repository / "src"
        source.mkdir()
        (source / "app.py").write_text('print("old")\n', encoding="utf-8")
        (repository / "tests").mkdir()
        adapter = FileChangeInvariantAdapter(
            repository_root=repository,
            policy=FileChangePolicy(repository_root=repository),
            observer_id="adapter-test-observer",
        )
        return repository, adapter

    def test_adapter_requires_file_change_context(self) -> None:
        _, adapter = self.make_adapter()
        action = modify_diff("src/app.py", 'print("old")', 'print("new")')
        generic = BoundaryExecutionIntent(
            intent_id="intent-generic-01",
            subject_id="subject-generic",
            action_type="generic:action",
            target_id="repo-1",
            action_digest=hashlib.sha256(action).hexdigest(),
            policy_version="policy-v1",
            postcondition_subject="deployment.json",
            postcondition_field="deployment_state",
            required_postcondition_value="ready",
        )
        self.assertEqual(
            adapter(generic, action),
            ("FILE_CHANGE_CONTEXT_REQUIRED",),
        )

    def test_adapter_allows_valid_modify(self) -> None:
        repository, adapter = self.make_adapter()
        target = repository / "src" / "app.py"
        action = modify_diff("src/app.py", 'print("old")', 'print("new")')
        intent = make_intent(
            resource_path="src/app.py",
            change_kind="MODIFY",
            action_type="PROPOSE_PATCH",
            action=action,
            expected_base_sha256=file_sha256(target),
        )
        self.assertEqual(adapter(intent, action), ())

    def test_adapter_rejects_base_hash_mismatch(self) -> None:
        repository, adapter = self.make_adapter()
        target = repository / "src" / "app.py"
        action = modify_diff("src/app.py", 'print("old")', 'print("new")')
        # The authorizer committed a stale base hash; the file has moved on.
        stale_hash = hashlib.sha256(b"different-content").hexdigest()
        intent = make_intent(
            resource_path="src/app.py",
            change_kind="MODIFY",
            action_type="PROPOSE_PATCH",
            action=action,
            expected_base_sha256=stale_hash,
            state_version=1,
        )
        self.assertEqual(adapter(intent, action), ("BASE_HASH_MISMATCH",))

    def test_adapter_rejects_modify_target_missing(self) -> None:
        repository, adapter = self.make_adapter()
        (repository / "src" / "app.py").unlink()
        action = modify_diff("src/app.py", 'print("old")', 'print("new")')
        intent = make_intent(
            resource_path="src/app.py",
            change_kind="MODIFY",
            action_type="PROPOSE_PATCH",
            action=action,
            expected_base_sha256="1" * 64,
        )
        self.assertIn("MODIFY_TARGET_MISSING", adapter(intent, action))

    def test_adapter_allows_valid_create(self) -> None:
        _, adapter = self.make_adapter()
        action = create_diff("tests/test_new.py", 'print("new")')
        intent = make_intent(
            resource_path="tests/test_new.py",
            change_kind="CREATE",
            action_type="PROPOSE_TEST_FILE",
            action=action,
            expected_base_sha256=None,
        )
        self.assertEqual(adapter(intent, action), ())

    def test_adapter_rejects_create_target_exists(self) -> None:
        repository, adapter = self.make_adapter()
        (repository / "tests" / "test_new.py").write_text(
            "already here\n", encoding="utf-8"
        )
        action = create_diff("tests/test_new.py", 'print("new")')
        intent = make_intent(
            resource_path="tests/test_new.py",
            change_kind="CREATE",
            action_type="PROPOSE_TEST_FILE",
            action=action,
            expected_base_sha256=None,
        )
        self.assertIn("CREATE_TARGET_EXISTS", adapter(intent, action))


    def test_adapter_rejects_patch_header_path_mismatch(self) -> None:
        repository, adapter = self.make_adapter()
        # The authorizer bound the intent to one file, the action to another.
        action = modify_diff("src/other.py", "old", "new")
        intent = make_intent(
            resource_path="src/app.py",
            change_kind="MODIFY",
            action_type="PROPOSE_PATCH",
            action=action,
            expected_base_sha256=file_sha256(repository / "src" / "app.py"),
        )
        self.assertIn("PATCH_HEADER_PATH_MISMATCH", adapter(intent, action))

    def test_adapter_rejects_symlink_target(self) -> None:
        repository, adapter = self.make_adapter()
        target = repository / "src" / "app.py"
        action = modify_diff("src/app.py", 'print("old")', 'print("new")')
        intent = make_intent(
            resource_path="src/app.py",
            change_kind="MODIFY",
            action_type="PROPOSE_PATCH",
            action=action,
            expected_base_sha256=file_sha256(target),
        )
        link = repository / "src" / "link.py"
        try:
            link.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation is not permitted on this host")
        target.unlink()
        link.replace(target)
        self.assertIn("SYMLINK_TARGET_FORBIDDEN", adapter(intent, action))

    def test_adapter_rejects_dependency_change(self) -> None:
        repository, adapter = self.make_adapter()
        forbidden = repository / "requirements.txt"
        forbidden.write_text("numpy\n", encoding="utf-8")
        action = modify_diff("requirements.txt", "numpy", "numpy>=2.0")
        intent = make_intent(
            resource_path="requirements.txt",
            change_kind="MODIFY",
            action_type="PROPOSE_PATCH",
            action=action,
            expected_base_sha256=file_sha256(forbidden),
        )
        self.assertIn("DEPENDENCY_CHANGE_FORBIDDEN", adapter(intent, action))

    def test_adapter_rejects_disallowed_file_type(self) -> None:
        repository, adapter = self.make_adapter()
        target = repository / "src" / "app.exe"
        target.write_bytes(b"old-binary")
        action = modify_diff("src/app.exe", "old-binary", "new-binary")
        intent = make_intent(
            resource_path="src/app.exe",
            change_kind="MODIFY",
            action_type="PROPOSE_PATCH",
            action=action,
            expected_base_sha256=file_sha256(target),
        )
        self.assertIn("FILE_TYPE_NOT_ALLOWED", adapter(intent, action))

    def test_adapter_rejects_case_variant_secret_path(self) -> None:
        # Adversarial testing (design doc 17, week 3: case differences):
        # confirm the casefold-based forbidden-path match is not bypassed
        # by an uppercase or mixed-case variant of a protected name.
        repository, adapter = self.make_adapter()
        secret = repository / ".ENV"
        secret.write_text("TOKEN=x\n", encoding="utf-8")
        action = modify_diff(".ENV", "TOKEN=x", "TOKEN=y")
        intent = make_intent(
            resource_path=".ENV",
            change_kind="MODIFY",
            action_type="PROPOSE_PATCH",
            action=action,
            expected_base_sha256=file_sha256(secret),
        )
        self.assertIn("SECRET_OR_CONTROL_PATH", adapter(intent, action))

    def test_adapter_rejects_non_nfc_resource_path(self) -> None:
        # Adversarial testing (design doc 17, week 3: Unicode look-alikes):
        # a decomposed-form path (combining accent) must not silently pass
        # just because the strict JSON decoder was never in this path.
        repository, adapter = self.make_adapter()
        decomposed_name = "café.py"  # NFC would be "café.py"
        target = repository / "src" / decomposed_name
        target.write_text('print("old")\n', encoding="utf-8")
        resource_path = f"src/{decomposed_name}"
        action = modify_diff(resource_path, 'print("old")', 'print("new")')
        intent = make_intent(
            resource_path=resource_path,
            change_kind="MODIFY",
            action_type="PROPOSE_PATCH",
            action=action,
            expected_base_sha256=file_sha256(target),
        )
        self.assertIn("FIELD_NOT_NFC", adapter(intent, action))

    def test_adapter_rejects_oversized_patch(self) -> None:
        # Adversarial testing (design doc 17, week 3: huge patch).
        repository, adapter = self.make_adapter()
        target = repository / "src" / "app.py"
        huge_line = "x" * (65 * 1024)
        action = modify_diff("src/app.py", 'print("old")', huge_line)
        intent = make_intent(
            resource_path="src/app.py",
            change_kind="MODIFY",
            action_type="PROPOSE_PATCH",
            action=action,
            expected_base_sha256=file_sha256(target),
        )
        self.assertIn("PATCH_TOO_LARGE", adapter(intent, action))

    def test_adapter_rejects_binary_diff_marker(self) -> None:
        # Adversarial testing (design doc 17, week 3: binary contamination):
        # a git-style "Binary files differ" marker is not a unified diff
        # and must not be treated as an approved single-file text patch.
        repository, adapter = self.make_adapter()
        target = repository / "src" / "app.py"
        action = b"Binary files a/src/app.py and b/src/app.py differ\n"
        intent = make_intent(
            resource_path="src/app.py",
            change_kind="MODIFY",
            action_type="PROPOSE_PATCH",
            action=action,
            expected_base_sha256=file_sha256(target),
        )
        self.assertIn(
            "SINGLE_FILE_UNIFIED_DIFF_REQUIRED", adapter(intent, action)
        )

    def test_adapter_rejects_secret_path(self) -> None:
        repository, adapter = self.make_adapter()
        secret = repository / ".env"
        secret.write_text("TOKEN=x\n", encoding="utf-8")
        action = modify_diff(".env", "TOKEN=x", "TOKEN=y")
        intent = make_intent(
            resource_path=".env",
            change_kind="MODIFY",
            action_type="PROPOSE_PATCH",
            action=action,
            expected_base_sha256=file_sha256(secret),
        )
        self.assertIn("SECRET_OR_CONTROL_PATH", adapter(intent, action))

    def test_adapter_rejects_scope_escape(self) -> None:
        _, adapter = self.make_adapter()
        action = modify_diff("src/app.py", "old", "new")
        intent = make_intent(
            resource_path="../outside.py",
            change_kind="MODIFY",
            action_type="PROPOSE_PATCH",
            action=action,
            expected_base_sha256=("1" * 64),
        )
        self.assertEqual(
            adapter(intent, action),
            ("EXECUTION_FILE_CHANGE_CONTEXT_INVALID",),
        )

    def test_adapter_rejects_non_utf8_action(self) -> None:
        repository, adapter = self.make_adapter()
        target = repository / "src" / "app.py"
        action = b"\xff\xfe\xfd"
        intent = make_intent(
            resource_path="src/app.py",
            change_kind="MODIFY",
            action_type="PROPOSE_PATCH",
            action=action,
            expected_base_sha256=file_sha256(target),
        )
        self.assertEqual(adapter(intent, action), ("ACTION_NOT_UTF8",))


    def test_adapter_rejects_invalid_idempotency_key(self) -> None:
        repository, adapter = self.make_adapter()
        target = repository / "src" / "app.py"
        action = modify_diff("src/app.py", 'print("old")', 'print("new")')
        intent = make_intent(
            resource_path="src/app.py",
            change_kind="MODIFY",
            action_type="PROPOSE_PATCH",
            action=action,
            expected_base_sha256=file_sha256(target),
            intent_id="ab",  # violates the idempotency-key pattern
        )
        self.assertIn("INVALID_IDEMPOTENCY_KEY", adapter(intent, action))

    def test_adapter_rejects_destructive_patch(self) -> None:
        repository, adapter = self.make_adapter()
        target = repository / "src" / "app.py"
        action = (
            "--- a/src/app.py\n"
            "+++ /dev/null\n"
            "@@ -1,1 +0,0 @@\n"
            '-print("old")\n'
        ).encode("utf-8")
        intent = make_intent(
            resource_path="src/app.py",
            change_kind="MODIFY",
            action_type="PROPOSE_PATCH",
            action=action,
            expected_base_sha256=file_sha256(target),
        )
        self.assertIn("DESTRUCTIVE_PATCH_FORBIDDEN", adapter(intent, action))

    def test_adapter_forbids_live_environment(self) -> None:
        repository = Path(tempfile.mkdtemp(prefix="t1-live-"))
        with self.assertRaises(ValueError):
            FileChangeInvariantAdapter(
                repository_root=repository,
                policy=FileChangePolicy(repository_root=repository),
                observer_id="adapter-observer",
                environment=ExecutionEnvironment.LIVE,
            )

    def test_file_change_context_validation(self) -> None:
        with self.assertRaises(ValueError):
            FileChangeContext(
                "src/app.py", "MODIFY", "PROPOSE_PATCH", None, 0
            ).validate()  # MODIFY without a base hash
        with self.assertRaises(ValueError):
            FileChangeContext(
                "src/app.py", "CREATE", "PROPOSE_PATCH", "1" * 64, 0
            ).validate()  # CREATE with a base hash
        with self.assertRaises(ValueError):
            FileChangeContext(
                "src/app.py", "DELETE", "PROPOSE_PATCH", "1" * 64, 0
            ).validate()
        for bad_path in ("/etc/passwd", "../out.py", "a\\b.py", "a:b.py"):
            with self.assertRaises(ValueError):
                FileChangeContext(
                    bad_path, "MODIFY", "PROPOSE_PATCH", "1" * 64, 0
                ).validate()
        # Whitespace is legal in file names; a space must not be rejected.
        spaced = FileChangeContext(
            "docs/my note.md", "MODIFY", "PROPOSE_PATCH", "1" * 64, 0
        )
        spaced.validate()
        good = FileChangeContext(
            "docs/note.md", "MODIFY", "PROPOSE_PATCH", "a" * 64, 3
        )
        good.validate()
        self.assertEqual(good.state_version, 3)

    def test_file_change_encode_decode_round_trip(self) -> None:
        context = FileChangeContext(
            "src/app.py", "MODIFY", "PROPOSE_PATCH", ("b" * 64), 7
        )
        encoded = _encode_file_change(context)
        self.assertIsInstance(encoded, dict)
        decoded = _decode_file_change(encoded)
        self.assertEqual(decoded, context)
        self.assertIsNone(_encode_file_change(None))
        self.assertIsNone(_decode_file_change(None))
        malformed = dict(encoded)
        malformed["extra"] = "x"
        with self.assertRaises(ValueError):
            _decode_file_change(malformed)


if __name__ == "__main__":
    unittest.main()
