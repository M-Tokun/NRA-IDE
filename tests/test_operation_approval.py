from __future__ import annotations
import copy
import hashlib
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills' / 'operation-approval'))
import manifest as approval
import git_manifest as git

class OperationApprovalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT / 'tests')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'AGENTS.md').write_text('# Contract\n', encoding='utf-8')
        self.file = self.root / 'target.txt'
        self.file.write_text('before', encoding='utf-8')
        self.used = set()
        self.consume = mock.Mock(side_effect=self._consume)
        self.verifier = mock.Mock(side_effect=lambda receipt: copy.deepcopy(self.claims) if receipt == b'test-only-authenticated-receipt' else None)
        self.request = self.file_request()
        self.claims = self.receipt(self.request)
    def tearDown(self):
        self.tmp.cleanup()
    def _consume(self, approval_id, sha):
        if approval_id in self.used:
            return False
        self.used.add(approval_id)
        return True
    def file_request(self):
        return {'schema_version': 1, 'request_id': 'request-1', 'session_id': 'session-1',
                'repo_realpath': os.path.normcase(os.path.realpath(self.root)),
                'agents_sha256': approval.snapshot_file(self.root / 'AGENTS.md')['sha256'],
                'operation': 'file_change', 'impact': 'Overwrite target.txt',
                'plan_sha256': hashlib.sha256(b'write after to target.txt').hexdigest(),
                'created_at': 900, 'expires_at': 1200,
                'targets': [approval.snapshot_file(self.file)], 'git': None}
    def git_snapshot(self):
        return {'remote': 'origin', 'push_urls': ['https://example.invalid/repo.git'],
                'local_ref': 'refs/heads/main', 'remote_ref': 'refs/heads/main',
                'refspec': 'refs/heads/main:refs/heads/main',
                'head_oid': 'c'*40, 'source_oid': 'c'*40, 'remote_oid': 'a'*40,
                'fetched_at': 990, 'incoming': [], 'outgoing': ['b'*40, 'c'*40],
                'scope_commits': ['b'*40, 'c'*40], 'fast_forward': True,
                'flags': {flag: False for flag in git.FLAGS}, 'extra_ref_updates': []}
    def git_request(self):
        value = self.file_request()
        value.update(operation='git_push', targets=[], git=self.git_snapshot())
        return value
    def receipt(self, request):
        return {'approval_id': 'approval-1', 'request_id': request['request_id'],
                'session_id': request['session_id'], 'manifest_sha256': approval.manifest_hash(request),
                'issued_at': 995, 'expires_at': 1100}
    def check(self, current=..., now=1000):
        return approval.check_request(self.request, self.request if current is ... else current,
                                     b'test-only-authenticated-receipt', now=now,
                                     verify_receipt=self.verifier, consume_once=self.consume)
    def test_exact_state_and_authenticated_receipt_pass_once(self):
        self.assertTrue(self.check().valid)
        result = self.check()
        self.assertFalse(result.valid)
        self.assertEqual(result.reason, 'RECEIPT_ALREADY_USED_OR_UNAVAILABLE')
    def test_self_report_without_backend_is_rejected(self):
        for receipt in ({'approved': True}, self.claims, True, 'はい', 'read\n'):
            with self.subTest(receipt=receipt):
                result = approval.check_request(self.request, self.request, receipt, now=1000)
                self.assertEqual(result.reason, 'TRUSTED_APPROVAL_BACKEND_REQUIRED')
    def test_signature_rejection_does_not_consume(self):
        result = approval.check_request(self.request, self.request, {'approved': True}, now=1000,
                                        verify_receipt=self.verifier, consume_once=self.consume)
        self.assertEqual(result.reason, 'UNVERIFIED_RECEIPT')
        self.consume.assert_not_called()
    def test_missing_consumption_backend_rejected(self):
        result = approval.check_request(self.request, self.request, b'test-only-authenticated-receipt', now=1000, verify_receipt=self.verifier)
        self.assertFalse(result.valid)
    def test_receipt_binding_changes_rejected(self):
        for field, value in (('manifest_sha256', '0'*64), ('request_id', 'other'), ('session_id', 'other')):
            with self.subTest(field=field):
                self.claims = self.receipt(self.request)
                self.claims[field] = value
                self.assertEqual(self.check().reason, 'RECEIPT_BINDING_MISMATCH')
        self.consume.assert_not_called()
    def test_receipt_and_request_expiration_boundaries(self):
        self.assertFalse(self.check(now=1100).valid)
        self.assertFalse(self.check(now=1200).valid)
        self.assertFalse(self.check(now=899).valid)
        for field, value in (('issued_at', 1001), ('issued_at', 899), ('expires_at', 1201), ('expires_at', 995)):
            with self.subTest(field=field, value=value):
                self.claims = self.receipt(self.request); self.claims[field] = value
                self.assertFalse(self.check().valid)
        self.consume.assert_not_called()
    def test_backend_failures_and_non_boolean_success_rejected(self):
        for callback in ('verify_receipt', 'consume_once'):
            kwargs = {'verify_receipt': self.verifier, 'consume_once': self.consume}
            kwargs[callback] = mock.Mock(side_effect=OSError('simulated failure'))
            result = approval.check_request(self.request, self.request, b'test-only-authenticated-receipt', now=1000, **kwargs)
            self.assertEqual(result.reason, 'APPROVAL_BACKEND_FAILURE')
        result = approval.check_request(self.request, self.request, b'test-only-authenticated-receipt', now=1000,
                                        verify_receipt=self.verifier, consume_once=lambda *_: 1)
        self.assertFalse(result.valid)
    def test_actual_file_content_change_detected(self):
        self.file.write_text('after', encoding='utf-8')
        result = self.check(approval.observe_files(self.request, now=1000))
        self.assertEqual(result.reason, 'MANIFEST_CHANGED')
        self.consume.assert_not_called()
    def test_actual_contract_change_detected(self):
        (self.root / 'AGENTS.md').write_text('# Changed\n', encoding='utf-8')
        self.assertEqual(self.check(approval.observe_files(self.request, now=1000)).reason, 'MANIFEST_CHANGED')
    def test_actual_file_disappearance_detected(self):
        self.file.unlink()
        self.assertFalse(self.check(approval.observe_files(self.request, now=1000)).valid)
    def test_absent_target_creation_detected(self):
        new_file = self.root / 'new.txt'
        self.request['targets'] = [approval.snapshot_file(new_file)]
        self.claims = self.receipt(self.request)
        new_file.write_text('unexpected', encoding='utf-8')
        self.assertFalse(self.check(approval.observe_files(self.request, now=1000)).valid)
    def test_resolved_path_change_detected(self):
        old_realpath = os.path.realpath
        alternate = os.path.normcase(os.path.abspath(self.root / 'other.txt'))
        def resolve(path):
            return alternate if os.path.normcase(os.path.abspath(path)) == self.request['targets'][0]['path'] else old_realpath(path)
        with mock.patch.object(approval.os.path, 'realpath', side_effect=resolve):
            current = approval.observe_files(self.request, now=1000)
        self.assertFalse(self.check(current).valid)
        self.consume.assert_not_called()
    def test_scope_and_plan_change_detected(self):
        for field, value in (('targets', [*self.request['targets'], approval.snapshot_file(self.root/'extra.txt')]),
                             ('plan_sha256', 'f'*64), ('impact', 'Different operation')):
            current = copy.deepcopy(self.request); current[field] = value
            self.assertFalse(self.check(current).valid)
        self.consume.assert_not_called()
    def test_duplicate_targets_and_directories_rejected(self):
        bad = copy.deepcopy(self.request); bad['targets'] *= 2
        self.assertFalse(self.check(bad).valid)
        with self.assertRaises(git.ManifestError): approval.snapshot_file(self.root)
    def test_manifest_types_and_unknown_fields_rejected(self):
        for field, value in (('schema_version', True), ('created_at', float('nan')), ('expires_at', float('inf')),
                             ('created_at', True), ('targets', {}), ('agents_sha256', 'bad'),
                             ('repo_realpath', 'relative'), ('operation', 'install')):
            bad = copy.deepcopy(self.request); bad[field] = value
            self.assertFalse(self.check(bad).valid)
        for bad in ([], None, {'approved': True}): self.assertFalse(self.check(bad).valid)
        bad = copy.deepcopy(self.request); bad['approved'] = True
        self.assertFalse(self.check(bad).valid)
    def test_canonical_hash_independent_of_object_key_order(self):
        reverse = dict(reversed(list(self.request.items())))
        self.assertEqual(approval.manifest_hash(reverse), approval.manifest_hash(self.request))
        self.assertTrue(self.check(reverse).valid)
    def test_git_exact_observed_snapshot_passes(self):
        self.request = self.git_request(); self.claims = self.receipt(self.request)
        self.assertTrue(self.check().valid)
    def test_git_head_destination_ref_and_commit_changes_rejected(self):
        self.request = self.git_request(); self.claims = self.receipt(self.request)
        for field, value in (('head_oid', 'd'*40), ('remote_oid', 'd'*40), ('remote', 'other'),
                             ('push_urls', ['https://example.invalid/other.git']), ('remote_ref', 'refs/heads/other'),
                             ('outgoing', ['d'*40, 'c'*40]), ('scope_commits', ['d'*40, 'c'*40])):
            with self.subTest(field=field):
                current = copy.deepcopy(self.request); current['git'][field] = value
                self.assertFalse(self.check(current).valid)
        self.consume.assert_not_called()
    def test_git_multiple_destinations_and_extra_refs_rejected(self):
        for field, value in (('push_urls', []), ('push_urls', ['https://example.invalid/a', 'https://example.invalid/b']),
                             ('extra_ref_updates', ['refs/tags/v1']), ('refspec', '+refs/heads/main:refs/heads/main'),
                             ('remote_ref', 'refs/tags/v1'), ('remote_oid', None)):
            snapshot = self.git_snapshot(); snapshot[field] = value
            with self.assertRaises(git.ManifestError): git.validate_git_snapshot(snapshot, now=1000)
    def test_git_unsafe_flags_and_nonfastforward_rejected(self):
        for flag in git.FLAGS:
            for value in (True, 0, None):
                snapshot = self.git_snapshot(); snapshot['flags'][flag] = value
                with self.assertRaises(git.ManifestError): git.validate_git_snapshot(snapshot, now=1000)
        snapshot = self.git_snapshot(); snapshot['fast_forward'] = False
        with self.assertRaises(git.ManifestError): git.validate_git_snapshot(snapshot, now=1000)
    def test_git_incoming_outside_scope_and_duplicate_commits_rejected(self):
        for field, value in (('incoming', ['d'*40]), ('scope_commits', ['c'*40]),
                             ('outgoing', ['b'*40, 'b'*40, 'c'*40]), ('outgoing', []),
                             ('outgoing', ['c'*40, 'b'*40]), ('source_oid', 'd'*40)):
            snapshot = self.git_snapshot(); snapshot[field] = value
            with self.assertRaises(git.ManifestError): git.validate_git_snapshot(snapshot, now=1000)
    def test_fresh_fetch_age_and_future_clock_rejected(self):
        for fetched in (699, 1001, float('nan'), True, 10**1000):
            snapshot = self.git_snapshot(); snapshot['fetched_at'] = fetched
            with self.assertRaises(git.ManifestError): git.validate_git_snapshot(snapshot, now=1000)
        snapshot = self.git_snapshot(); snapshot['fetched_at'] = 700
        self.assertEqual(git.validate_git_snapshot(snapshot, now=1000), snapshot)
    def test_url_secrets_and_errors_not_echoed(self):
        for url in ('https://token-secret@example.invalid/repo', 'https://example.invalid/repo?token=secret',
                    'ssh://git:secret@example.invalid/repo', 'ssh://example.invalid:bad/repo', 'https://[bad/repo', '-option:/repo'):
            with self.subTest(url=url):
                with self.assertRaises(git.ManifestError) as caught: git.safe_push_url(url)
                self.assertEqual(str(caught.exception), 'UNSAFE_PUSH_URL')
        for url in ('https://example.invalid/repo', 'ssh://git@example.invalid/repo', 'git@example.invalid:org/repo.git', 'file:///repo.git'):
            self.assertEqual(git.safe_push_url(url), url)
    def test_same_content_replacement_identity_is_bound(self):
        current = copy.deepcopy(self.request)
        current['targets'][0]['identity']['inode'] += 1
        self.assertEqual(self.check(current).reason, 'MANIFEST_CHANGED')
        self.consume.assert_not_called()
    def test_backend_error_cannot_expose_secret(self):
        for callback in ('verify_receipt', 'consume_once'):
            kwargs = {'verify_receipt': self.verifier, 'consume_once': self.consume}
            kwargs[callback] = mock.Mock(side_effect=git.ManifestError('token-secret'))
            result = approval.check_request(self.request, self.request, b'test-only-authenticated-receipt', now=1000, **kwargs)
            self.assertEqual(result.reason, 'APPROVAL_BACKEND_FAILURE')
    def test_read_race_rejected(self):
        original = os.lstat
        calls = 0
        def changed(path):
            nonlocal calls
            info = original(path)
            calls += 1
            if calls == 2:
                replacement = mock.Mock(wraps=info)
                for key in ('st_dev', 'st_ino', 'st_size', 'st_mtime_ns', 'st_ctime_ns'):
                    setattr(replacement, key, getattr(info, key))
                replacement.st_ino += 1
                return replacement
            return info
        with mock.patch.object(approval.os, 'lstat', side_effect=changed):
            with self.assertRaises(git.ManifestError) as caught:
                approval.snapshot_file(self.file)
        self.assertEqual(str(caught.exception), 'TARGET_CHANGED_DURING_READ')
    def test_git_cannot_use_file_observer(self):
        with self.assertRaises(git.ManifestError): approval.observe_files(self.git_request(), now=1000)

if __name__ == '__main__': unittest.main()
