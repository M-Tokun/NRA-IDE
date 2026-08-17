"""Persistent one-time request and nonce ledger owned by the trusted side."""

from __future__ import annotations

import hashlib
import hmac
import json
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


_SHA256 = re.compile(r"[0-9a-f]{64}")


@dataclass(frozen=True, slots=True)
class NonceConsumeResult:
    accepted: bool
    sequence: int | None
    reason_codes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ExecutionAttemptPrepareResult:
    accepted: bool
    attempt_id: str | None
    reason_codes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ExecutionAttemptEventResult:
    accepted: bool
    sequence: int | None
    reason_codes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ExecutionReconciliationResult:
    accepted: bool
    outcome: str | None
    sequence: int | None
    reason_codes: tuple[str, ...]


class PersistentNonceStore:
    def __init__(self, database_path: Path, integrity_key: bytes) -> None:
        if not database_path.parent.exists():
            raise ValueError("nonce database parent must already exist")
        _validate_key(integrity_key)
        self.database_path = database_path
        self._integrity_key = integrity_key
        self._connection = sqlite3.connect(database_path, timeout=5.0)
        self._connection.execute("PRAGMA synchronous=FULL")
        self._connection.execute("PRAGMA journal_mode=DELETE")
        self._initialize()
        integrity_reasons = self.verify()
        if integrity_reasons:
            self.close()
            raise ValueError(",".join(integrity_reasons))

    def __enter__(self) -> "PersistentNonceStore":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        self._connection.close()

    def consume(
        self,
        *,
        request_id: str,
        nonce: str,
        issued_at: datetime,
        request_digest: str,
        consumed_at: datetime,
    ) -> NonceConsumeResult:
        if (
            not request_id
            or len(request_id) > 128
            or len(nonce) < 16
            or len(nonce) > 128
            or issued_at.tzinfo is None
            or consumed_at.tzinfo is None
            or consumed_at < issued_at
            or not _SHA256.fullmatch(request_digest)
        ):
            return NonceConsumeResult(False, None, ("NONCE_INPUT_INVALID",))
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            integrity_reasons = self.verify()
            if integrity_reasons:
                self._connection.rollback()
                return NonceConsumeResult(False, None, integrity_reasons)
            row = self._connection.execute(
                "SELECT sequence, row_mac FROM consumed_nonce ORDER BY sequence DESC LIMIT 1"
            ).fetchone()
            sequence = 1 if row is None else int(row[0]) + 1
            previous_mac = None if row is None else str(row[1])
            fields = {
                "consumed_at": _format_time(consumed_at),
                "issued_at": _format_time(issued_at),
                "nonce": nonce,
                "previous_mac": previous_mac,
                "request_digest": request_digest,
                "request_id": request_id,
                "sequence": sequence,
            }
            row_mac = _mac(self._integrity_key, fields)
            self._connection.execute(
                """
                INSERT INTO consumed_nonce(
                    sequence, request_id, nonce, issued_at, consumed_at,
                    request_digest, previous_mac, row_mac
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    sequence,
                    request_id,
                    nonce,
                    fields["issued_at"],
                    fields["consumed_at"],
                    request_digest,
                    previous_mac,
                    row_mac,
                ),
            )
            self._connection.commit()
            return NonceConsumeResult(True, sequence, ())
        except sqlite3.IntegrityError:
            self._connection.rollback()
            return NonceConsumeResult(
                False,
                None,
                ("NONCE_OR_REQUEST_REPLAY",),
            )
        except sqlite3.DatabaseError:
            self._connection.rollback()
            return NonceConsumeResult(False, None, ("NONCE_STORE_FAILURE",))

    def consume_and_prepare_execution(
        self,
        *,
        request_id: str,
        nonce: str,
        issued_at: datetime,
        request_digest: str,
        consumed_at: datetime,
        intent_id: str,
        target_id: str,
        action_digest: str,
        postcondition_subject: str,
        postcondition_field: str,
        required_postcondition_value: str,
        authorizer_principal_ids: tuple[str, ...],
    ) -> ExecutionAttemptPrepareResult:
        if (
            not _identifier(request_id, 128)
            or not 16 <= len(nonce) <= 128
            or issued_at.tzinfo is None
            or consumed_at.tzinfo is None
            or consumed_at < issued_at
            or not _SHA256.fullmatch(request_digest)
            or not _identifier(intent_id, 128)
            or not _identifier(target_id, 128)
            or not _SHA256.fullmatch(action_digest)
            or not _identifier(postcondition_subject, 1024)
            or not _identifier(postcondition_field, 128)
            or not isinstance(required_postcondition_value, str)
            or not 0 < len(required_postcondition_value) <= 4096
            or not _principal_ids(authorizer_principal_ids, minimum=2)
        ):
            return ExecutionAttemptPrepareResult(
                False,
                None,
                ("EXECUTION_ATTEMPT_INPUT_INVALID",),
            )
        attempt_id = hashlib.sha256(
            json.dumps(
                {
                    "action_digest": action_digest,
                    "request_digest": request_digest,
                    "request_id": request_id,
                },
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            integrity_reasons = self.verify()
            if integrity_reasons:
                self._connection.rollback()
                return ExecutionAttemptPrepareResult(
                    False,
                    None,
                    integrity_reasons,
                )
            replay = self._connection.execute(
                "SELECT 1 FROM consumed_nonce "
                "WHERE request_id = ? OR nonce = ? LIMIT 1",
                (request_id, nonce),
            ).fetchone()
            if replay is not None:
                self._connection.rollback()
                return ExecutionAttemptPrepareResult(
                    False,
                    None,
                    ("NONCE_OR_REQUEST_REPLAY",),
                )
            if self.unresolved_execution_attempt_ids():
                self._connection.rollback()
                return ExecutionAttemptPrepareResult(
                    False,
                    None,
                    ("EXECUTION_OUTCOME_RECONCILIATION_REQUIRED",),
                )
            row = self._connection.execute(
                "SELECT sequence, row_mac FROM consumed_nonce "
                "ORDER BY sequence DESC LIMIT 1"
            ).fetchone()
            sequence = 1 if row is None else int(row[0]) + 1
            previous_mac = None if row is None else str(row[1])
            nonce_fields = {
                "consumed_at": _format_time(consumed_at),
                "issued_at": _format_time(issued_at),
                "nonce": nonce,
                "previous_mac": previous_mac,
                "request_digest": request_digest,
                "request_id": request_id,
                "sequence": sequence,
            }
            row_mac = _mac(self._integrity_key, nonce_fields)
            self._connection.execute(
                """
                INSERT INTO consumed_nonce(
                    sequence, request_id, nonce, issued_at, consumed_at,
                    request_digest, previous_mac, row_mac
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    sequence,
                    request_id,
                    nonce,
                    nonce_fields["issued_at"],
                    nonce_fields["consumed_at"],
                    request_digest,
                    previous_mac,
                    row_mac,
                ),
            )
            attempt_fields = {
                "action_digest": action_digest,
                "attempt_id": attempt_id,
                "intent_id": intent_id,
                "prepared_at": _format_time(consumed_at),
                "record_type": "execution-attempt/1.0",
                "request_id": request_id,
                "target_id": target_id,
            }
            self._connection.execute(
                """
                INSERT INTO execution_attempt(
                    attempt_id, request_id, intent_id, target_id,
                    action_digest, prepared_at, prepare_mac
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    attempt_id,
                    request_id,
                    intent_id,
                    target_id,
                    action_digest,
                    attempt_fields["prepared_at"],
                    _mac(self._integrity_key, attempt_fields),
                ),
            )
            principal_ids_json = _canonical_json(list(authorizer_principal_ids))
            binding_fields = {
                "attempt_id": attempt_id,
                "authorization_payload_digest": request_digest,
                "authorizer_principal_ids_json": principal_ids_json,
                "postcondition_field": postcondition_field,
                "postcondition_subject": postcondition_subject,
                "record_type": "execution-postcondition-binding/1.0",
                "required_postcondition_sha256": hashlib.sha256(
                    required_postcondition_value.encode("utf-8")
                ).hexdigest(),
            }
            self._connection.execute(
                """
                INSERT INTO execution_postcondition_binding(
                    attempt_id, authorization_payload_digest,
                    authorizer_principal_ids_json, postcondition_subject,
                    postcondition_field, required_postcondition_sha256,
                    binding_mac
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    attempt_id,
                    request_digest,
                    principal_ids_json,
                    postcondition_subject,
                    postcondition_field,
                    binding_fields["required_postcondition_sha256"],
                    _mac(self._integrity_key, binding_fields),
                ),
            )
            self._connection.commit()
            return ExecutionAttemptPrepareResult(True, attempt_id, ())
        except sqlite3.IntegrityError:
            self._connection.rollback()
            return ExecutionAttemptPrepareResult(
                False,
                None,
                ("NONCE_OR_REQUEST_REPLAY",),
            )
        except sqlite3.DatabaseError:
            self._connection.rollback()
            return ExecutionAttemptPrepareResult(
                False,
                None,
                ("NONCE_STORE_FAILURE",),
            )

    def record_execution_event(
        self,
        *,
        attempt_id: str,
        state: str,
        observed_at: datetime,
        result_digest: str | None = None,
    ) -> ExecutionAttemptEventResult:
        if (
            not _SHA256.fullmatch(attempt_id)
            or state
            not in {"STARTED", "EXECUTOR_RETURNED", "OUTCOME_UNKNOWN"}
            or observed_at.tzinfo is None
            or (state == "EXECUTOR_RETURNED") != (result_digest is not None)
            or (
                result_digest is not None
                and not _SHA256.fullmatch(result_digest)
            )
        ):
            return ExecutionAttemptEventResult(
                False,
                None,
                ("EXECUTION_EVENT_INPUT_INVALID",),
            )
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            integrity_reasons = self.verify()
            if integrity_reasons:
                self._connection.rollback()
                return ExecutionAttemptEventResult(
                    False,
                    None,
                    integrity_reasons,
                )
            attempt = self._connection.execute(
                "SELECT 1 FROM execution_attempt WHERE attempt_id = ?",
                (attempt_id,),
            ).fetchone()
            if attempt is None:
                self._connection.rollback()
                return ExecutionAttemptEventResult(
                    False,
                    None,
                    ("EXECUTION_ATTEMPT_UNKNOWN",),
                )
            latest = self._connection.execute(
                "SELECT state FROM execution_attempt_event "
                "WHERE attempt_id = ? ORDER BY sequence DESC LIMIT 1",
                (attempt_id,),
            ).fetchone()
            previous_state = None if latest is None else str(latest[0])
            allowed = (
                (previous_state is None and state == "STARTED")
                or (
                    previous_state == "STARTED"
                    and state in {"EXECUTOR_RETURNED", "OUTCOME_UNKNOWN"}
                )
            )
            if not allowed:
                self._connection.rollback()
                return ExecutionAttemptEventResult(
                    False,
                    None,
                    ("EXECUTION_STATE_TRANSITION_INVALID",),
                )
            row = self._connection.execute(
                "SELECT sequence, event_mac FROM execution_attempt_event "
                "ORDER BY sequence DESC LIMIT 1"
            ).fetchone()
            sequence = 1 if row is None else int(row[0]) + 1
            previous_mac = None if row is None else str(row[1])
            fields = {
                "attempt_id": attempt_id,
                "observed_at": _format_time(observed_at),
                "previous_event_mac": previous_mac,
                "record_type": "execution-attempt-event/1.0",
                "result_digest": result_digest,
                "sequence": sequence,
                "state": state,
            }
            event_mac = _mac(self._integrity_key, fields)
            self._connection.execute(
                """
                INSERT INTO execution_attempt_event(
                    sequence, attempt_id, state, observed_at,
                    result_digest, previous_event_mac, event_mac
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    sequence,
                    attempt_id,
                    state,
                    fields["observed_at"],
                    result_digest,
                    previous_mac,
                    event_mac,
                ),
            )
            self._connection.commit()
            return ExecutionAttemptEventResult(True, sequence, ())
        except sqlite3.DatabaseError:
            self._connection.rollback()
            return ExecutionAttemptEventResult(
                False,
                None,
                ("NONCE_STORE_FAILURE",),
            )

    def unresolved_execution_attempt_ids(self) -> tuple[str, ...]:
        rows = self._connection.execute(
            "SELECT attempt_id FROM execution_attempt ORDER BY attempt_id"
        ).fetchall()
        unresolved = []
        for (attempt_id,) in rows:
            latest = self._connection.execute(
                "SELECT outcome FROM execution_reconciliation "
                "WHERE attempt_id = ? ORDER BY sequence DESC LIMIT 1",
                (attempt_id,),
            ).fetchone()
            # Only a future independently verified resolution may release this
            # attempt. Executor return alone is a report, not observed reality.
            if latest is None or latest[0] != "VERIFIED_RESOLVED":
                unresolved.append(str(attempt_id))
        return tuple(unresolved)

    def record_execution_reconciliation(
        self,
        *,
        attempt_id: str,
        evidence_kind: str,
        evidence_digest: str,
        observer_principal_ids: tuple[str, ...],
        reconciled_at: datetime,
        observation_attempt_id: str | None = None,
        observation_intent_id: str | None = None,
        observation_target_id: str | None = None,
        observation_subject: str | None = None,
        observation_field: str | None = None,
        observed_value: str | None = None,
    ) -> ExecutionReconciliationResult:
        if (
            not _SHA256.fullmatch(attempt_id)
            or evidence_kind not in {"QUORUM", "CONFLICT", "INSUFFICIENT"}
            or not _SHA256.fullmatch(evidence_digest)
            or reconciled_at.tzinfo is None
            or not _principal_ids(
                observer_principal_ids,
                minimum=2 if evidence_kind != "INSUFFICIENT" else 0,
            )
        ):
            return ExecutionReconciliationResult(False, None, None, ("EXECUTION_RECONCILIATION_INPUT_INVALID",))
        observation_fields = (observation_attempt_id, observation_intent_id, observation_target_id, observation_subject, observation_field, observed_value)
        if evidence_kind == "QUORUM" and any(not isinstance(value, str) or not value for value in observation_fields):
            return ExecutionReconciliationResult(False, None, None, ("EXECUTION_RECONCILIATION_INPUT_INVALID",))
        if evidence_kind != "QUORUM" and any(value is not None for value in observation_fields):
            return ExecutionReconciliationResult(False, None, None, ("EXECUTION_RECONCILIATION_INPUT_INVALID",))
        if evidence_kind == "QUORUM" and observation_attempt_id != attempt_id:
            return ExecutionReconciliationResult(False, None, None, ("EXECUTION_RECONCILIATION_ATTEMPT_MISMATCH",))
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            integrity_reasons = self.verify()
            if integrity_reasons:
                self._connection.rollback()
                return ExecutionReconciliationResult(False, None, None, integrity_reasons)
            attempt = self._connection.execute("SELECT intent_id, target_id FROM execution_attempt WHERE attempt_id = ?", (attempt_id,)).fetchone()
            binding = self._connection.execute("SELECT postcondition_subject, postcondition_field, required_postcondition_sha256 FROM execution_postcondition_binding WHERE attempt_id = ?", (attempt_id,)).fetchone()
            latest_event = self._connection.execute("SELECT state FROM execution_attempt_event WHERE attempt_id = ? ORDER BY sequence DESC LIMIT 1", (attempt_id,)).fetchone()
            if attempt is None or binding is None:
                self._connection.rollback()
                return ExecutionReconciliationResult(False, None, None, ("EXECUTION_ATTEMPT_UNKNOWN",))
            if latest_event is None or latest_event[0] != "EXECUTOR_RETURNED":
                self._connection.rollback()
                return ExecutionReconciliationResult(False, None, None, ("EXECUTION_RECONCILIATION_NOT_READY",))
            latest = self._connection.execute("SELECT outcome FROM execution_reconciliation WHERE attempt_id = ? ORDER BY sequence DESC LIMIT 1", (attempt_id,)).fetchone()
            if latest is not None and latest[0] in {"VERIFIED_RESOLVED", "CONFLICT"}:
                self._connection.rollback()
                return ExecutionReconciliationResult(False, None, None, ("EXECUTION_RECONCILIATION_TERMINAL",))
            observed_value_sha256 = None
            if evidence_kind == "INSUFFICIENT":
                outcome = "EVIDENCE_INSUFFICIENT"
            elif evidence_kind == "CONFLICT":
                outcome = "CONFLICT"
            else:
                assert observed_value is not None
                observed_value_sha256 = hashlib.sha256(observed_value.encode("utf-8")).hexdigest()
                matches = (
                    observation_intent_id == attempt[0]
                    and observation_target_id == attempt[1]
                    and observation_subject == binding[0]
                    and observation_field == binding[1]
                    and observed_value_sha256 == binding[2]
                )
                outcome = "VERIFIED_RESOLVED" if matches else "CONFLICT"
            row = self._connection.execute("SELECT sequence, reconciliation_mac FROM execution_reconciliation ORDER BY sequence DESC LIMIT 1").fetchone()
            sequence = 1 if row is None else int(row[0]) + 1
            previous_mac = None if row is None else str(row[1])
            principal_ids_json = _canonical_json(list(observer_principal_ids))
            fields = {
                "attempt_id": attempt_id,
                "evidence_digest": evidence_digest,
                "observed_value_sha256": observed_value_sha256,
                "observer_principal_ids_json": principal_ids_json,
                "outcome": outcome,
                "previous_reconciliation_mac": previous_mac,
                "reconciled_at": _format_time(reconciled_at),
                "record_type": "execution-reconciliation/1.0",
                "sequence": sequence,
            }
            reconciliation_mac = _mac(self._integrity_key, fields)
            self._connection.execute("INSERT INTO execution_reconciliation(sequence, attempt_id, outcome, reconciled_at, evidence_digest, observed_value_sha256, observer_principal_ids_json, previous_reconciliation_mac, reconciliation_mac) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (sequence, attempt_id, outcome, fields["reconciled_at"], evidence_digest, observed_value_sha256, principal_ids_json, previous_mac, reconciliation_mac))
            self._connection.commit()
            return ExecutionReconciliationResult(True, outcome, sequence, ())
        except sqlite3.DatabaseError:
            self._connection.rollback()
            return ExecutionReconciliationResult(False, None, None, ("NONCE_STORE_FAILURE",))

    def verify(self) -> tuple[str, ...]:
        previous_mac = None
        try:
            rows = self._connection.execute(
                """
                SELECT sequence, request_id, nonce, issued_at, consumed_at,
                       request_digest, previous_mac, row_mac
                FROM consumed_nonce ORDER BY sequence
                """
            ).fetchall()
        except sqlite3.DatabaseError:
            return ("NONCE_STORE_FAILURE",)
        for expected_sequence, row in enumerate(rows, 1):
            (
                sequence,
                request_id,
                nonce,
                issued_at,
                consumed_at,
                request_digest,
                stored_previous,
                row_mac,
            ) = row
            if sequence != expected_sequence or stored_previous != previous_mac:
                return ("NONCE_CHAIN_INVALID",)
            fields = {
                "consumed_at": consumed_at,
                "issued_at": issued_at,
                "nonce": nonce,
                "previous_mac": stored_previous,
                "request_digest": request_digest,
                "request_id": request_id,
                "sequence": sequence,
            }
            if not hmac.compare_digest(row_mac, _mac(self._integrity_key, fields)):
                return ("NONCE_CHAIN_INVALID",)
            previous_mac = row_mac
        journal_reasons = self._verify_execution_journal()
        if journal_reasons:
            return journal_reasons
        return self._verify_execution_reconciliation()

    def _verify_execution_reconciliation(self) -> tuple[str, ...]:
        try:
            attempts = {row[0] for row in self._connection.execute("SELECT attempt_id FROM execution_attempt").fetchall()}
            bindings = self._connection.execute("SELECT attempt_id, authorization_payload_digest, authorizer_principal_ids_json, postcondition_subject, postcondition_field, required_postcondition_sha256, binding_mac FROM execution_postcondition_binding").fetchall()
            reconciliations = self._connection.execute("SELECT sequence, attempt_id, outcome, reconciled_at, evidence_digest, observed_value_sha256, observer_principal_ids_json, previous_reconciliation_mac, reconciliation_mac FROM execution_reconciliation ORDER BY sequence").fetchall()
        except sqlite3.DatabaseError:
            return ("EXECUTION_RECONCILIATION_JOURNAL_FAILURE",)
        bound_attempts = set()
        for attempt_id, authorization_digest, principals_json, subject, field, required_sha256, binding_mac in bindings:
            fields = {"attempt_id": attempt_id, "authorization_payload_digest": authorization_digest, "authorizer_principal_ids_json": principals_json, "postcondition_field": field, "postcondition_subject": subject, "record_type": "execution-postcondition-binding/1.0", "required_postcondition_sha256": required_sha256}
            try:
                principals = tuple(json.loads(principals_json))
            except (TypeError, ValueError, json.JSONDecodeError):
                return ("EXECUTION_RECONCILIATION_JOURNAL_INVALID",)
            if (attempt_id not in attempts or not _SHA256.fullmatch(authorization_digest) or not _principal_ids(principals, minimum=2) or not _identifier(subject, 1024) or not _identifier(field, 128) or not _SHA256.fullmatch(required_sha256) or not hmac.compare_digest(binding_mac, _mac(self._integrity_key, fields))):
                return ("EXECUTION_RECONCILIATION_JOURNAL_INVALID",)
            bound_attempts.add(attempt_id)
        previous_mac = None
        latest_outcomes: dict[str, str] = {}
        for expected_sequence, row in enumerate(reconciliations, 1):
            sequence, attempt_id, outcome, reconciled_at, evidence_digest, observed_value_sha256, principals_json, stored_previous, reconciliation_mac = row
            try:
                principals = tuple(json.loads(principals_json))
            except (TypeError, ValueError, json.JSONDecodeError):
                return ("EXECUTION_RECONCILIATION_JOURNAL_INVALID",)
            prior = latest_outcomes.get(attempt_id)
            fields = {"attempt_id": attempt_id, "evidence_digest": evidence_digest, "observed_value_sha256": observed_value_sha256, "observer_principal_ids_json": principals_json, "outcome": outcome, "previous_reconciliation_mac": stored_previous, "reconciled_at": reconciled_at, "record_type": "execution-reconciliation/1.0", "sequence": sequence}
            if (sequence != expected_sequence or attempt_id not in bound_attempts or outcome not in {"VERIFIED_RESOLVED", "CONFLICT", "EVIDENCE_INSUFFICIENT"} or prior in {"VERIFIED_RESOLVED", "CONFLICT"} or not _SHA256.fullmatch(evidence_digest) or (outcome == "VERIFIED_RESOLVED" and not _SHA256.fullmatch(observed_value_sha256 or "")) or not _principal_ids(principals, minimum=(0 if outcome == "EVIDENCE_INSUFFICIENT" else 2)) or stored_previous != previous_mac or not hmac.compare_digest(reconciliation_mac, _mac(self._integrity_key, fields))):
                return ("EXECUTION_RECONCILIATION_JOURNAL_INVALID",)
            latest_outcomes[attempt_id] = outcome
            previous_mac = reconciliation_mac
        return ()

    def _verify_execution_journal(self) -> tuple[str, ...]:
        try:
            attempts = self._connection.execute(
                "SELECT attempt_id, request_id, intent_id, target_id, "
                "action_digest, prepared_at, prepare_mac "
                "FROM execution_attempt ORDER BY attempt_id"
            ).fetchall()
            events = self._connection.execute(
                "SELECT sequence, attempt_id, state, observed_at, "
                "result_digest, previous_event_mac, event_mac "
                "FROM execution_attempt_event ORDER BY sequence"
            ).fetchall()
        except sqlite3.DatabaseError:
            return ("EXECUTION_JOURNAL_FAILURE",)
        attempt_ids = set()
        for row in attempts:
            (
                attempt_id,
                request_id,
                intent_id,
                target_id,
                action_digest,
                prepared_at,
                prepare_mac,
            ) = row
            fields = {
                "action_digest": action_digest,
                "attempt_id": attempt_id,
                "intent_id": intent_id,
                "prepared_at": prepared_at,
                "record_type": "execution-attempt/1.0",
                "request_id": request_id,
                "target_id": target_id,
            }
            if (
                not _SHA256.fullmatch(attempt_id)
                or not _identifier(request_id, 128)
                or not _identifier(intent_id, 128)
                or not _identifier(target_id, 128)
                or not _SHA256.fullmatch(action_digest)
                or not hmac.compare_digest(
                    prepare_mac,
                    _mac(self._integrity_key, fields),
                )
            ):
                return ("EXECUTION_JOURNAL_INVALID",)
            attempt_ids.add(attempt_id)
        previous_mac = None
        states: dict[str, str] = {}
        for expected_sequence, row in enumerate(events, 1):
            (
                sequence,
                attempt_id,
                state,
                observed_at,
                result_digest,
                stored_previous,
                event_mac,
            ) = row
            prior_state = states.get(attempt_id)
            allowed = (
                (prior_state is None and state == "STARTED")
                or (
                    prior_state == "STARTED"
                    and state in {"EXECUTOR_RETURNED", "OUTCOME_UNKNOWN"}
                )
            )
            fields = {
                "attempt_id": attempt_id,
                "observed_at": observed_at,
                "previous_event_mac": stored_previous,
                "record_type": "execution-attempt-event/1.0",
                "result_digest": result_digest,
                "sequence": sequence,
                "state": state,
            }
            if (
                sequence != expected_sequence
                or attempt_id not in attempt_ids
                or stored_previous != previous_mac
                or not allowed
                or (state == "EXECUTOR_RETURNED") != (result_digest is not None)
                or (
                    result_digest is not None
                    and not _SHA256.fullmatch(result_digest)
                )
                or not hmac.compare_digest(
                    event_mac,
                    _mac(self._integrity_key, fields),
                )
            ):
                return ("EXECUTION_JOURNAL_INVALID",)
            states[attempt_id] = state
            previous_mac = event_mac
        return ()

    def _initialize(self) -> None:
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS consumed_nonce (
                sequence INTEGER PRIMARY KEY,
                request_id TEXT NOT NULL UNIQUE,
                nonce TEXT NOT NULL UNIQUE,
                issued_at TEXT NOT NULL,
                consumed_at TEXT NOT NULL,
                request_digest TEXT NOT NULL,
                previous_mac TEXT,
                row_mac TEXT NOT NULL
            );
            CREATE TRIGGER IF NOT EXISTS consumed_nonce_no_update
            BEFORE UPDATE ON consumed_nonce
            BEGIN SELECT RAISE(ABORT, 'append-only nonce ledger'); END;
            CREATE TRIGGER IF NOT EXISTS consumed_nonce_no_delete
            BEFORE DELETE ON consumed_nonce
            BEGIN SELECT RAISE(ABORT, 'append-only nonce ledger'); END;
            CREATE TABLE IF NOT EXISTS execution_attempt (
                attempt_id TEXT PRIMARY KEY,
                request_id TEXT NOT NULL UNIQUE,
                intent_id TEXT NOT NULL,
                target_id TEXT NOT NULL,
                action_digest TEXT NOT NULL,
                prepared_at TEXT NOT NULL,
                prepare_mac TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS execution_attempt_event (
                sequence INTEGER PRIMARY KEY,
                attempt_id TEXT NOT NULL,
                state TEXT NOT NULL,
                observed_at TEXT NOT NULL,
                result_digest TEXT,
                previous_event_mac TEXT,
                event_mac TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS execution_postcondition_binding (
                attempt_id TEXT PRIMARY KEY,
                authorization_payload_digest TEXT NOT NULL,
                authorizer_principal_ids_json TEXT NOT NULL,
                postcondition_subject TEXT NOT NULL,
                postcondition_field TEXT NOT NULL,
                required_postcondition_sha256 TEXT NOT NULL,
                binding_mac TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS execution_reconciliation (
                sequence INTEGER PRIMARY KEY,
                attempt_id TEXT NOT NULL,
                outcome TEXT NOT NULL,
                reconciled_at TEXT NOT NULL,
                evidence_digest TEXT NOT NULL,
                observed_value_sha256 TEXT,
                observer_principal_ids_json TEXT NOT NULL,
                previous_reconciliation_mac TEXT,
                reconciliation_mac TEXT NOT NULL
            );
            CREATE TRIGGER IF NOT EXISTS execution_attempt_no_update
            BEFORE UPDATE ON execution_attempt
            BEGIN SELECT RAISE(ABORT, 'append-only execution attempt'); END;
            CREATE TRIGGER IF NOT EXISTS execution_attempt_no_delete
            BEFORE DELETE ON execution_attempt
            BEGIN SELECT RAISE(ABORT, 'append-only execution attempt'); END;
            CREATE TRIGGER IF NOT EXISTS execution_attempt_event_no_update
            BEFORE UPDATE ON execution_attempt_event
            BEGIN SELECT RAISE(ABORT, 'append-only execution event'); END;
            CREATE TRIGGER IF NOT EXISTS execution_attempt_event_no_delete
            BEFORE DELETE ON execution_attempt_event
            BEGIN SELECT RAISE(ABORT, 'append-only execution event'); END;
            CREATE TRIGGER IF NOT EXISTS execution_postcondition_binding_no_update
            BEFORE UPDATE ON execution_postcondition_binding
            BEGIN SELECT RAISE(ABORT, 'append-only postcondition binding'); END;
            CREATE TRIGGER IF NOT EXISTS execution_postcondition_binding_no_delete
            BEFORE DELETE ON execution_postcondition_binding
            BEGIN SELECT RAISE(ABORT, 'append-only postcondition binding'); END;
            CREATE TRIGGER IF NOT EXISTS execution_reconciliation_no_update
            BEFORE UPDATE ON execution_reconciliation
            BEGIN SELECT RAISE(ABORT, 'append-only reconciliation'); END;
            CREATE TRIGGER IF NOT EXISTS execution_reconciliation_no_delete
            BEFORE DELETE ON execution_reconciliation
            BEGIN SELECT RAISE(ABORT, 'append-only reconciliation'); END;
            """
        )
        self._connection.commit()


def _validate_key(key: bytes) -> None:
    if not isinstance(key, bytes) or len(key) < 32:
        raise ValueError("integrity_key must contain at least 32 bytes")


def _format_time(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat()


def _identifier(value: object, maximum: int) -> bool:
    return (
        isinstance(value, str)
        and 0 < len(value) <= maximum
        and not any(character.isspace() for character in value)
    )


def _principal_ids(value: object, *, minimum: int) -> bool:
    return isinstance(value, tuple) and len(value) >= minimum and value == tuple(sorted(set(value))) and all(_identifier(item, 128) for item in value)


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))


def _mac(key: bytes, fields: dict[str, object]) -> str:
    material = json.dumps(
        fields,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hmac.new(key, material, hashlib.sha256).hexdigest()
