import hashlib
import json
import sqlite3
import stat
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from note.poc_horizontal_ai.safety_kernel import (
    AppendOnlyHistoryLedger,
    HistoryEventKind,
    ObservationRequest,
    create_audit_bundle,
    encode_observation_request,
)
from note.poc_horizontal_ai.trusted_runtime import (
    AnchorReceipt,
    AuditAnchorStore,
    PersistentNonceStore,
    authenticate_payload,
    derive_subkey,
    process_observation_request,
    verify_authenticated_observation,
    verify_authenticated_payload,
    verify_anchor_receipt,
)


class AuthenticationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.key = b"A" * 32
        self.now = datetime.now(timezone.utc)

    def test_payload_authentication_detects_tampering(self) -> None:
        authenticated = authenticate_payload(
            '{"value":1}',
            key_id="observer-key-v1",
            secret_key=self.key,
            issued_at=self.now,
        )
        valid = verify_authenticated_payload(
            authenticated,
            trusted_keys={"observer-key-v1": self.key},
            max_age=timedelta(seconds=5),
            now=self.now,
        )
        self.assertEqual(valid.payload_json, '{"value":1}')
        tampered = json.loads(authenticated)
        tampered["payload_json"] = '{"value":2}'
        invalid = verify_authenticated_payload(
            json.dumps(tampered),
            trusted_keys={"observer-key-v1": self.key},
            max_age=timedelta(seconds=5),
            now=self.now,
        )
        self.assertIsNone(invalid.payload_json)
        self.assertIn("AUTH_PAYLOAD_DIGEST_MISMATCH", invalid.reason_codes)
        self.assertIn("AUTH_MAC_MISMATCH", invalid.reason_codes)


class PersistentNonceStoreTests(unittest.TestCase):
    def test_replay_is_rejected_across_store_reopen(self) -> None:
        key = b"N" * 32
        now = datetime.now(timezone.utc)
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "nonce.sqlite3"
            with PersistentNonceStore(database, key) as store:
                first = store.consume(
                    request_id="request-1",
                    nonce="0123456789abcdef",
                    issued_at=now,
                    request_digest="a" * 64,
                    consumed_at=now,
                )
                self.assertTrue(first.accepted)
                self.assertEqual(store.verify(), ())
            with PersistentNonceStore(database, key) as reopened:
                replay = reopened.consume(
                    request_id="request-1",
                    nonce="0123456789abcdef",
                    issued_at=now,
                    request_digest="a" * 64,
                    consumed_at=now,
                )
                self.assertFalse(replay.accepted)
                self.assertEqual(
                    replay.reason_codes,
                    ("NONCE_OR_REQUEST_REPLAY",),
                )

    def test_nonce_rows_reject_update_and_delete(self) -> None:
        key = b"N" * 32
        now = datetime.now(timezone.utc)
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "nonce.sqlite3"
            with PersistentNonceStore(database, key) as store:
                store.consume(
                    request_id="request-1",
                    nonce="0123456789abcdef",
                    issued_at=now,
                    request_digest="a" * 64,
                    consumed_at=now,
                )
            connection = sqlite3.connect(database)
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    "UPDATE consumed_nonce SET nonce = ? WHERE sequence = 1",
                    ("fedcba9876543210",),
                )
            connection.rollback()
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute("DELETE FROM consumed_nonce WHERE sequence = 1")
            connection.close()

    def test_corrupt_nonce_chain_cannot_be_reopened(self) -> None:
        key = b"N" * 32
        now = datetime.now(timezone.utc)
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "nonce.sqlite3"
            with PersistentNonceStore(database, key) as store:
                store.consume(
                    request_id="request-1",
                    nonce="0123456789abcdef",
                    issued_at=now,
                    request_digest="a" * 64,
                    consumed_at=now,
                )
            connection = sqlite3.connect(database)
            connection.execute("DROP TRIGGER consumed_nonce_no_update")
            connection.execute(
                "UPDATE consumed_nonce SET request_digest = ? WHERE sequence = 1",
                ("b" * 64,),
            )
            connection.commit()
            connection.close()

            with self.assertRaisesRegex(ValueError, "NONCE_CHAIN_INVALID"):
                PersistentNonceStore(database, key)

    def test_revoke_all_capabilities_persists_across_reopen(self) -> None:
        key = b"N" * 32
        now = datetime.now(timezone.utc)
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "nonce.sqlite3"
            with PersistentNonceStore(database, key) as store:
                self.assertEqual(store.current_revocation_generation(), 0)
                first = store.revoke_all_capabilities(
                    reason="incident-drill",
                    revoked_at=now,
                )
                self.assertTrue(first.accepted)
                self.assertEqual(first.generation, 1)
                self.assertEqual(store.current_revocation_generation(), 1)
                # Revocation is irreversible: a second call appends another
                # row rather than resetting or being rejected as a no-op.
                second = store.revoke_all_capabilities(
                    reason="second-incident",
                    revoked_at=now,
                )
                self.assertTrue(second.accepted)
                self.assertEqual(second.generation, 2)
            with PersistentNonceStore(database, key) as reopened:
                self.assertEqual(reopened.current_revocation_generation(), 2)

    def test_capability_revocation_rows_reject_update_and_delete(self) -> None:
        key = b"N" * 32
        now = datetime.now(timezone.utc)
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "nonce.sqlite3"
            with PersistentNonceStore(database, key) as store:
                store.revoke_all_capabilities(reason="incident-drill", revoked_at=now)
            connection = sqlite3.connect(database)
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    "UPDATE capability_revocation SET reason = ? WHERE sequence = 1",
                    ("tampered",),
                )
            connection.rollback()
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    "DELETE FROM capability_revocation WHERE sequence = 1"
                )
            connection.close()

    def test_corrupt_capability_revocation_chain_cannot_be_reopened(self) -> None:
        key = b"N" * 32
        now = datetime.now(timezone.utc)
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "nonce.sqlite3"
            with PersistentNonceStore(database, key) as store:
                store.revoke_all_capabilities(reason="incident-drill", revoked_at=now)
            connection = sqlite3.connect(database)
            connection.execute("DROP TRIGGER capability_revocation_no_update")
            connection.execute(
                "UPDATE capability_revocation SET reason = ? WHERE sequence = 1",
                ("tampered-reason",),
            )
            connection.commit()
            connection.close()

            with self.assertRaisesRegex(
                ValueError, "CAPABILITY_REVOCATION_CHAIN_INVALID"
            ):
                PersistentNonceStore(database, key)

    def test_consume_fails_closed_when_logging_is_impossible(self) -> None:
        # Fault injection (T4-3: "logging halted"): a write that cannot
        # reach durable storage (disk full, permission denied) must be
        # reported as rejected, never silently treated as consumed.
        key = b"N" * 32
        now = datetime.now(timezone.utc)
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "nonce.sqlite3"
            PersistentNonceStore(database, key).close()
            database.chmod(stat.S_IREAD)
            try:
                with PersistentNonceStore(database, key) as store:
                    result = store.consume(
                        request_id="request-1",
                        nonce="0123456789abcdef",
                        issued_at=now,
                        request_digest="a" * 64,
                        consumed_at=now,
                    )
                    self.assertFalse(result.accepted)
                    self.assertEqual(
                        result.reason_codes, ("NONCE_STORE_FAILURE",)
                    )
            finally:
                database.chmod(stat.S_IWRITE | stat.S_IREAD)

    def test_revoke_all_capabilities_fails_closed_when_logging_is_impossible(
        self,
    ) -> None:
        # Same fault as above, applied to the safety-critical revocation
        # path specifically: a caller must never be told a revocation
        # succeeded when it was not actually durably recorded.
        key = b"N" * 32
        now = datetime.now(timezone.utc)
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "nonce.sqlite3"
            PersistentNonceStore(database, key).close()
            database.chmod(stat.S_IREAD)
            try:
                with PersistentNonceStore(database, key) as store:
                    result = store.revoke_all_capabilities(
                        reason="incident-drill", revoked_at=now
                    )
                    self.assertFalse(result.accepted)
                    self.assertEqual(
                        result.reason_codes, ("CAPABILITY_REVOCATION_FAILURE",)
                    )
                    self.assertEqual(store.current_revocation_generation(), 0)
            finally:
                database.chmod(stat.S_IWRITE | stat.S_IREAD)


class AuthenticatedObserverGatewayTests(unittest.TestCase):
    def test_gateway_authenticates_and_persistently_rejects_replay(self) -> None:
        key = b"G" * 32
        now = datetime.now(timezone.utc)
        request = ObservationRequest(
            "observation-1",
            "0123456789abcdef0123456789abcdef",
            "AGENTS.md",
            21,
            now - timedelta(seconds=1),
        )
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "nonce.sqlite3"
            with PersistentNonceStore(database, key) as store:
                authenticated = process_observation_request(
                    encode_observation_request(request),
                    repository_root=Path.cwd(),
                    observer_id="trusted-observer-v1",
                    nonce_store=store,
                    key_id="observer-key-v1",
                    secret_key=key,
                    request_max_age=timedelta(seconds=5),
                    now=now,
                )
            verified = verify_authenticated_observation(
                authenticated,
                request=request,
                repository_root=Path.cwd(),
                expected_observer_id="trusted-observer-v1",
                trusted_keys={"observer-key-v1": key},
                authentication_max_age=timedelta(seconds=5),
                observation_max_age=timedelta(seconds=5),
                now=datetime.now(timezone.utc),
            )
            self.assertEqual(verified.reason_codes, ())
            self.assertIsNotNone(verified.evidence)
            with PersistentNonceStore(database, key) as reopened:
                with self.assertRaises(ValueError):
                    process_observation_request(
                        encode_observation_request(request),
                        repository_root=Path.cwd(),
                        observer_id="trusted-observer-v1",
                        nonce_store=reopened,
                        key_id="observer-key-v1",
                        secret_key=key,
                        request_max_age=timedelta(seconds=5),
                        now=now,
                    )

    def test_gateway_service_uses_key_file_without_echoing_key(self) -> None:
        key = b"S" * 32
        request = ObservationRequest(
            "observation-service-1",
            "fedcba9876543210fedcba9876543210",
            "AGENTS.md",
            22,
            datetime.now(timezone.utc),
        )
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            key_file = temporary / "observer.key"
            key_file.write_bytes(key)
            key_file.chmod(0o600)
            database = temporary / "nonce.sqlite3"
            command = [
                sys.executable,
                "-m",
                "note.poc_horizontal_ai.trusted_runtime.observer_gateway_service",
                "--repository-root",
                str(Path.cwd()),
                "--observer-id",
                "trusted-observer-v1",
                "--nonce-database",
                str(database),
                "--key-id",
                "observer-key-v1",
                "--key-file",
                str(key_file),
            ]
            first = subprocess.run(
                command,
                input=encode_observation_request(request),
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertNotIn(key.decode("ascii"), first.stdout)
            second = subprocess.run(
                command,
                input=encode_observation_request(request),
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(second.returncode, 2)


class AuditAnchorStoreTests(unittest.TestCase):
    def bundle(self) -> tuple[str, str]:
        ledger = AppendOnlyHistoryLedger()
        ledger.append(
            event_id="event-1",
            kind=HistoryEventKind.OBSERVATION,
            target_id="repo-1",
            source_id="observer-v1",
            occurred_at="2026-08-13T00:00:00+00:00",
            payload={"state": "observed"},
        )
        return (
            create_audit_bundle(
                ledger.events,
                exported_at=datetime.now(timezone.utc),
            ),
            ledger.events[-1].digest,
        )

    def test_bundle_head_is_anchored_once_with_authenticated_receipt(self) -> None:
        key = b"R" * 32
        bundle, head_digest = self.bundle()
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "anchor.sqlite3"
            with AuditAnchorStore(database, key) as store:
                receipt = store.append(
                    anchor_id="anchor-1",
                    audit_head_digest=head_digest,
                    event_count=1,
                    bundle_sha256=hashlib.sha256(bundle.encode("utf-8")).hexdigest(),
                    anchored_at=datetime.now(timezone.utc),
                )
                self.assertEqual(receipt.sequence, 1)
                self.assertEqual(store.verify(), ())
                self.assertTrue(verify_anchor_receipt(receipt, key))
                with self.assertRaises(ValueError):
                    store.append(
                        anchor_id="anchor-2",
                        audit_head_digest=head_digest,
                        event_count=1,
                        bundle_sha256=hashlib.sha256(
                            bundle.encode("utf-8")
                        ).hexdigest(),
                        anchored_at=datetime.now(timezone.utc),
                    )

    def test_corrupt_anchor_chain_cannot_be_reopened(self) -> None:
        key = b"R" * 32
        bundle, head_digest = self.bundle()
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "anchor.sqlite3"
            with AuditAnchorStore(database, key) as store:
                store.append(
                    anchor_id="anchor-1",
                    audit_head_digest=head_digest,
                    event_count=1,
                    bundle_sha256=hashlib.sha256(bundle.encode("utf-8")).hexdigest(),
                    anchored_at=datetime.now(timezone.utc),
                )
            connection = sqlite3.connect(database)
            connection.execute("DROP TRIGGER audit_anchor_no_update")
            connection.execute(
                "UPDATE audit_anchor SET bundle_sha256 = ? WHERE sequence = 1",
                ("f" * 64,),
            )
            connection.commit()
            connection.close()

            with self.assertRaisesRegex(ValueError, "ANCHOR_CHAIN_INVALID"):
                AuditAnchorStore(database, key)

    def test_anchor_service_verifies_bundle_and_returns_receipt(self) -> None:
        master_key = b"M" * 32
        bundle, _ = self.bundle()
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            key_file = temporary / "anchor.key"
            key_file.write_bytes(master_key)
            key_file.chmod(0o600)
            database = temporary / "anchor.sqlite3"
            command = [
                sys.executable,
                "-m",
                "note.poc_horizontal_ai.trusted_runtime.anchor_service",
                "--anchor-database",
                str(database),
                "--anchor-id",
                "anchor-service-1",
                "--key-file",
                str(key_file),
            ]
            completed = subprocess.run(
                command,
                input=bundle,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            data = json.loads(completed.stdout)
            data.pop("schema_version")
            receipt = AnchorReceipt(**data)
            self.assertTrue(
                verify_anchor_receipt(
                    receipt,
                    derive_subkey(master_key, "audit-anchor-v1"),
                )
            )


if __name__ == "__main__":
    unittest.main()
