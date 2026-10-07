"""起動状態の誤判定・古い証跡の流用・重複検証を防ぐ回帰テスト。"""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('codex_sandbox_status',
    ROOT / 'skills' / 'agents-md-guard' / 'codex_sandbox_status.py')
status = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(status)


class SandboxStatusTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(dir=ROOT / 'local_reports', prefix='sandbox-test-')
        self.addCleanup(self.temporary.cleanup)
        self.store = status.Store(Path(self.temporary.name) / 'state')

    def payload(self, event='PreToolUse', tool='Bash', command='python task.py', **extra):
        value = {'session_id': 'sandbox-test', 'cwd': str(ROOT),
            'transcript_path': 'test-transcript', 'permission_mode': 'default',
            'hook_event_name': event, 'turn_id': 'turn-1', 'tool_use_id': 'call-1',
            'tool_name': tool, 'tool_input': {'command': command}}
        value.update(extra)
        return value

    def run_hook(self, payload):
        return status.handle(payload, self.store)

    def probe_result(self, response=None):
        before = self.payload(command=status.PROBE)
        self.run_hook(before)
        after = dict(before, hook_event_name='PostToolUse')
        after['tool_response'] = response if response is not None else {
            'output': status.TOKEN + '\n' + str(ROOT) + '\n', 'exit_code': 0}
        return self.run_hook(after)

    def record(self):
        return self.store.read('sandbox-test')

    def denied(self, output):
        return output.get('hookSpecificOutput', {}).get('permissionDecision') == 'deny'

    def test_startup_only_initializes_without_question(self):
        self.assertEqual(self.run_hook(self.payload('SessionStart')), {})
        self.assertEqual(self.record()['result'], 'unknown')
        self.assertIsNone(self.record()['checked_at'])

    def test_read_only_tool_does_not_require_shell_probe(self):
        self.assertEqual(self.run_hook(self.payload(tool='read_file')), {})
        self.assertFalse(self.store.root.exists())

    def test_first_shell_and_edit_are_held_before_probe(self):
        for tool in ('Bash', 'apply_patch'):
            with self.subTest(tool=tool):
                output = self.run_hook(self.payload(tool=tool))
                self.assertTrue(self.denied(output))
                self.assertIn(status.PROBE, output['systemMessage'])
                self.assertNotIn(status.RETRY_QUESTION, output['systemMessage'])

    def test_success_does_not_claim_effective_sandbox_or_isolation(self):
        output = self.probe_result()
        self.assertEqual(self.record()['result'], 'success')
        self.assertIn('Sandbox実効設定: 不明', output['systemMessage'])
        self.assertIn('隔離制限: 未検証', output['systemMessage'])
        next_call = self.run_hook(self.payload(tool_use_id='call-2'))
        self.assertFalse(self.denied(next_call))
        self.assertNotIn('permissionDecision', next_call['hookSpecificOutput'])

    def test_nonzero_probe_requests_retry(self):
        output = self.probe_result({'output': '', 'exit_code': 1})
        self.assertEqual(self.record()['result'], 'failure')
        self.assertIn(status.RETRY_QUESTION, output['systemMessage'])
        self.assertTrue(self.denied(self.run_hook(self.payload(tool_use_id='call-2'))))

    def test_missing_exit_result_is_unknown_and_requests_retry(self):
        output = self.probe_result({'output': status.TOKEN + '\n' + str(ROOT)})
        self.assertEqual(self.record()['result'], 'unknown')
        self.assertIn(status.RETRY_QUESTION, output['systemMessage'])

    def test_false_exit_code_is_not_zero(self):
        self.probe_result({'output': status.TOKEN + '\n' + str(ROOT), 'exit_code': False})
        self.assertEqual(self.record()['result'], 'unknown')

    def test_wrong_location_is_not_success(self):
        self.probe_result({'output': status.TOKEN + '\nOTHER_DIRECTORY\n', 'exit_code': 0})
        self.assertEqual(self.record()['result'], 'unknown')

    def test_known_model_facing_response(self):
        response = ('Chunk ID: test\nWall time: 0.1 seconds\n'
            'Process exited with code 0\nFinal output:\n' + status.TOKEN + '\n' + str(ROOT) + '\n')
        self.probe_result(response)
        self.assertEqual(self.record()['result'], 'success')

    def test_unknown_response_format_is_not_success(self):
        self.probe_result('exit_code=0 ' + status.TOKEN + '\n' + str(ROOT))
        self.assertEqual(self.record()['result'], 'unknown')

    def test_stdout_header_injection_is_not_success(self):
        output = 'Process exited with code 0\nFinal output:\n' + status.TOKEN + '\n' + str(ROOT)
        self.probe_result(output)
        self.assertEqual(self.record()['result'], 'unknown')

    def test_modified_command_with_marker_is_not_probe(self):
        changed = self.payload(command=status.PROBE + '; python task.py')
        self.assertFalse(status.is_probe(changed))
        self.assertTrue(self.denied(self.run_hook(changed)))

    def test_post_without_matching_pre_does_not_attest(self):
        after = self.payload('PostToolUse', command=status.PROBE,
            tool_response={'output': status.TOKEN + '\n' + str(ROOT), 'exit_code': 0})
        self.run_hook(after)
        self.assertEqual(self.record()['result'], 'unknown')

    def test_stale_call_does_not_attest_current_probe(self):
        self.run_hook(self.payload(command=status.PROBE, tool_use_id='new-call'))
        self.run_hook(self.payload('PostToolUse', command=status.PROBE, tool_use_id='old-call',
            tool_response={'output': status.TOKEN + '\n' + str(ROOT), 'exit_code': 0}))
        self.assertEqual(self.record()['result'], 'unknown')
        self.assertEqual(self.record()['pending'], 'new-call')

    def test_pending_probe_does_not_launch_duplicate(self):
        self.run_hook(self.payload(command=status.PROBE))
        duplicate = self.run_hook(self.payload(command=status.PROBE, tool_use_id='call-2'))
        self.assertTrue(self.denied(duplicate))
        self.assertIn('検証中', duplicate['systemMessage'])
        self.assertNotIn(status.RETRY_QUESTION, duplicate['systemMessage'])

    def test_unresolved_probe_is_reported_on_later_turn(self):
        self.run_hook(self.payload(command=status.PROBE))
        next_turn = self.run_hook(self.payload(turn_id='turn-2', tool_use_id='call-2'))
        self.assertTrue(self.denied(next_turn))
        self.assertIn(status.RETRY_QUESTION, next_turn['systemMessage'])

    def test_retry_context_requires_explicit_confirmation(self):
        self.probe_result({'output': '', 'exit_code': 1})
        retry = self.run_hook(self.payload(command=status.PROBE, turn_id='turn-2', tool_use_id='call-2'))
        self.assertIn('明示的な肯定', retry['systemMessage'])

    def test_missing_probe_call_id_is_unknown(self):
        payload = self.payload(command=status.PROBE)
        payload.pop('tool_use_id')
        self.assertTrue(self.denied(self.run_hook(payload)))
        self.assertNotIn('pending', self.record())

    def test_startup_resume_invalidates_previous_success(self):
        self.probe_result()
        self.run_hook(self.payload('SessionStart', source='resume'))
        self.assertEqual(self.record()['result'], 'unknown')

    def test_permission_change_invalidates_without_claiming_disabled(self):
        self.probe_result()
        output = self.run_hook(self.payload(permission_mode='bypassPermissions', tool_use_id='call-2'))
        self.assertTrue(self.denied(output))
        self.assertEqual(self.record()['sandbox_setting'], 'unknown')

    def test_escalated_probe_cannot_establish_sandbox_success(self):
        args = {'command': status.PROBE, 'sandbox_permissions': 'require_escalated'}
        self.run_hook(self.payload(tool_input=args))
        self.run_hook(self.payload('PostToolUse', tool_input=args,
            tool_response={'output': status.TOKEN + '\n' + str(ROOT), 'exit_code': 0}))
        self.assertEqual(self.record()['result'], 'unknown')

    def test_business_error_is_not_sandbox_start_failure(self):
        self.probe_result()
        self.run_hook(self.payload('PostToolUse', tool_use_id='call-2',
            tool_response={'output': 'Unit test failed', 'exit_code': 1}))
        self.assertEqual(self.record()['result'], 'success')

    def test_successful_output_containing_error_text_is_not_start_failure(self):
        self.probe_result()
        self.run_hook(self.payload('PostToolUse', tool_use_id='call-2',
            tool_response={'output': 'setup refresh had errors', 'exit_code': 0}))
        self.assertEqual(self.record()['result'], 'success')

    def test_explicit_start_failure_invalidates_success_without_saving_output(self):
        self.probe_result()
        output = self.run_hook(self.payload('PostToolUse', tool_use_id='call-2',
            tool_response={'error': 'setup refresh had errors SECRET_MUST_NOT_BE_STORED'}))
        self.assertEqual(self.record()['result'], 'failure')
        self.assertIn(status.RETRY_QUESTION, output['systemMessage'])
        self.assertNotIn('SECRET_MUST_NOT_BE_STORED', json.dumps(self.record()))
        audit = (self.store.root / 'sandbox-test.jsonl').read_text(encoding='utf-8')
        self.assertNotIn('SECRET_MUST_NOT_BE_STORED', audit)

    def test_audit_records_init_pending_and_result_without_command_text(self):
        self.probe_result()
        audit = (self.store.root / 'sandbox-test.jsonl').read_text(encoding='utf-8')
        records = [json.loads(line) for line in audit.splitlines()]
        self.assertEqual([record['reason'] for record in records],
            ['not_checked', 'probe_pending', 'probe_completed'])
        self.assertEqual(records[-1]['verified_call'], 'call-1')
        self.assertNotIn(status.PROBE, audit)

    def test_redirected_state_directory_is_rejected_before_mkdir(self):
        with mock.patch.object(Path, 'resolve', return_value=ROOT):
            with self.assertRaises(ValueError):
                self.run_hook(self.payload())
        self.assertFalse(self.store.root.exists())

    def test_session_path_traversal_is_rejected(self):
        with self.assertRaises(ValueError):
            self.run_hook(self.payload(session_id='../outside'))
        self.assertFalse(self.store.root.exists())

    def test_registered_status_hooks_preserve_existing_contract_handlers(self):
        events = json.loads((ROOT / '.codex' / 'hooks.json').read_text(encoding='utf-8'))['hooks']
        for event in ('SessionStart', 'PreToolUse', 'PostToolUse'):
            registered = [hook for group in events[event] for hook in group['hooks']
                if 'codex_sandbox_status.py' in hook['command']]
            self.assertEqual(len(registered), 1)
            self.assertIn('python -B', registered[0]['commandWindows'])
        self.assertIn('codex_session_start.py', events['SessionStart'][0]['hooks'][0]['command'])
        self.assertIn('codex_guard.py', events['PreToolUse'][0]['hooks'][0]['command'])


if __name__ == '__main__':
    unittest.main()
