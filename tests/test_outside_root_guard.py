"""作業ルート外ガード（skills/outside-root-guard）のテスト。"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARD = os.path.join(ROOT, 'skills', 'outside-root-guard')
OUTSIDE = 'Z:\\nra_outside_test\\file.txt' if os.name == 'nt' else '/nra_outside_test/file.txt'
INSIDE = os.path.join(ROOT, 'AGENTS.md')


def run(host, payload, env=None):
    raw = payload if isinstance(payload, str) else json.dumps(payload)
    proc = subprocess.run([sys.executable, '-B', os.path.join(GUARD, f'{host}_outside.py')],
                          input=raw.encode('utf-8'), capture_output=True, env=env, timeout=30)
    assert proc.returncode == 0, proc.stderr
    out = proc.stdout.decode('utf-8').strip()
    return json.loads(out) if out else None


def tool(name, **args):
    return {'session_id': 's1', 'cwd': ROOT, 'tool_name': name, 'tool_input': args}


def decision(result):
    return result['hookSpecificOutput']['permissionDecision'] if result else None


class FileTools(unittest.TestCase):
    def test_inside_read_passes(self):
        self.assertIsNone(run('claude', tool('Read', file_path=INSIDE)))

    def test_relative_inside_passes(self):
        self.assertIsNone(run('claude', tool('Grep', pattern='x', path='skills')))

    def test_outside_read_asks_with_warning(self):
        result = run('claude', tool('Read', file_path=OUTSIDE))
        self.assertEqual(decision(result), 'ask')
        reason = result['hookSpecificOutput']['permissionDecisionReason']
        self.assertTrue(reason.startswith('CAUTION!!アウトルート_OK!!!!! リポジトリルート外の「読み取り」をしてよいですか？'))
        self.assertIn('警告:', reason)

    def test_outside_write_codex_denies(self):
        self.assertEqual(decision(run('codex', tool('Write', file_path=OUTSIDE, content='x'))), 'deny')

    def test_outside_gemini_denies(self):
        self.assertEqual(run('gemini', tool('read_file', absolute_path=OUTSIDE))['decision'], 'deny')

    def test_gemini_inside_is_empty_object(self):
        self.assertEqual(run('gemini', tool('read_file', absolute_path=INSIDE)), {})

    def test_codex_outside_workdir_denies(self):
        self.assertEqual(decision(run('codex', tool('exec_command', cmd='ls', workdir=os.path.dirname(OUTSIDE)))), 'deny')

    def test_patch_outside_denies(self):
        patch = '*** Begin Patch\n*** Update File: ' + OUTSIDE + '\n@@\n-a\n+b\n*** End Patch\n'
        self.assertEqual(decision(run('codex', tool('apply_patch', input=patch))), 'deny')

    def test_memory_dir_allowed(self):
        home = tempfile.mkdtemp()
        env = dict(os.environ, USERPROFILE=home, HOME=home)
        memo = os.path.join(home, '.claude', 'projects', 'p1', 'memory', 'a.md')
        self.assertIsNone(run('claude', tool('Write', file_path=memo, content='x'), env))


class Shell(unittest.TestCase):
    def test_parent_escape_asks(self):
        self.assertEqual(decision(run('claude', tool('Bash', command='cat ../../outside.txt'))), 'ask')

    def test_cd_outside_asks(self):
        cmd = 'cd /c/Users && ls' if os.name == 'nt' else 'cd /home && ls'
        if os.name != 'nt':
            self.skipTest('git-bash 形式は Windows だけ')
        self.assertEqual(decision(run('claude', tool('Bash', command=cmd))), 'ask')

    def test_home_reference_asks(self):
        self.assertEqual(decision(run('claude', tool('Bash', command='ls ~/.codex'))), 'ask')

    def test_git_range_and_devnull_pass(self):
        self.assertIsNone(run('claude', tool('Bash', command='git log HEAD~1..HEAD 2>/dev/null')))

    def test_inside_absolute_passes(self):
        cmd = f'cd "{ROOT}" && git status'
        self.assertIsNone(run('claude', tool('Bash', command=cmd)))

    def test_url_passes(self):
        self.assertIsNone(run('claude', tool('Bash', command='git ls-remote https://github.com/a/b')))


class Protected(unittest.TestCase):
    def test_write_default_allow_denied(self):
        target = os.path.join(GUARD, 'allow_default.txt')
        self.assertEqual(decision(run('claude', tool('Edit', file_path=target, old_string='a', new_string='b'))), 'deny')

    def test_git_add_and_read_of_allow_file_pass(self):
        for cmd in ('git add -- skills/outside-root-guard/allow_default.txt 2>/dev/null',
                    'cat skills/outside-root-guard/allow_default.txt',
                    'git diff --cached --name-only && git status --short | grep -v allow_default.txt'):
            with self.subTest(cmd=cmd):
                self.assertIsNone(run('claude', tool('Bash', command=cmd)))

    def test_shell_writes_to_allow_file_denied(self):
        for cmd in ('echo x > skills/outside-root-guard/allow_default.txt',
                    'echo x | tee -a .agent_state/outside_root_allow.txt',
                    "sed -i 's/a/b/' skills/outside-root-guard/allow_default.txt",
                    'Add-Content .agent_state/outside_root_allow.txt Z:/x',
                    'rm .agent_state/outside_root_allow.txt'):
            with self.subTest(cmd=cmd):
                self.assertEqual(decision(run('claude', tool('Bash', command=cmd))), 'deny')

    def test_shell_append_local_allow_denied(self):
        cmd = 'echo Z:/x >> .agent_state/outside_root_allow.txt'
        self.assertEqual(decision(run('claude', tool('Bash', command=cmd))), 'deny')


class Failure(unittest.TestCase):
    def test_invalid_json_claude_asks_others_deny(self):
        self.assertEqual(decision(run('claude', '{not json')), 'ask')
        self.assertEqual(decision(run('codex', '{not json')), 'deny')
        self.assertEqual(run('gemini', '{not json')['decision'], 'deny')
        self.assertTrue(run('cline', '{not json')['cancel'])


class Cline(unittest.TestCase):
    def payload(self, name, **params):
        return {'taskId': 't1', 'preToolUse': {'toolName': name, 'parameters': params}}

    def test_inside_read_not_cancelled(self):
        self.assertFalse(run('cline', self.payload('read_file', path='AGENTS.md'))['cancel'])

    def test_outside_read_cancelled(self):
        result = run('cline', self.payload('read_file', path=OUTSIDE))
        self.assertTrue(result['cancel'])
        self.assertIn('警告:', result['errorMessage'])

    def test_outside_command_cancelled(self):
        self.assertTrue(run('cline', self.payload('execute_command', command='cat ../../x'))['cancel'])


if __name__ == '__main__':
    unittest.main()
