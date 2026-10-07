#!/usr/bin/env python
"""Codex実操作前の起動検証。実効Sandbox設定・隔離能力とは区別する。

別CLIやプロセスを起動しない。再検証の利用者確認は対話側が行う。
この記録は権限証明ではなく、対応hook経路の補助である。
"""
import contextlib
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
STATE_ROOT = ROOT / '.agent_state' / 'sandbox_status' / 'codex'
TOKEN = 'NRA_SANDBOX_START_OK'
WINDOWS_PROBE = "Write-Output 'NRA_SANDBOX_START_OK'; Get-Location"
POSIX_PROBE = "printf '%s\\n' 'NRA_SANDBOX_START_OK'; pwd"
PROBE = WINDOWS_PROBE if os.name == 'nt' else POSIX_PROBE
SHELL_TOOLS = {'Bash', 'exec_command', 'shell_command', 'shell'}
ACTION_TOOLS = SHELL_TOOLS | {'apply_patch', 'Edit', 'Write'}
RETRY_QUESTION = '再度、起動検証しますか？'
FAILURES = ('setup refresh had errors', 'runtime read/execute validation failed',
            'Failed to create unified exec process', 'windows sandbox failed:')


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True).encode()).hexdigest()


def valid_id(value):
    return isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9_-]{1,200}', value) is not None


def validate(payload):
    if not isinstance(payload, dict) or not valid_id(payload.get('session_id')):
        raise ValueError('invalid_session')
    if payload.get('hook_event_name') not in {'SessionStart', 'PreToolUse', 'PostToolUse'}:
        raise ValueError('unsupported_event')
    if not isinstance(payload.get('cwd'), str) or not os.path.isabs(payload['cwd']):
        raise ValueError('invalid_cwd')
    if payload['hook_event_name'] != 'SessionStart':
        if not isinstance(payload.get('tool_name'), str) or not isinstance(payload.get('tool_input'), dict):
            raise ValueError('invalid_tool')


def command(payload):
    args = payload.get('tool_input', {})
    value = args.get('command', args.get('cmd'))
    return value if isinstance(value, str) else ''


def is_probe(payload):
    # Markerを含む任意スクリプトは認めず、無害な最小コマンドだけを照合する。
    value = command(payload).strip().replace('\r\n', '\n')
    return payload.get('tool_name') in SHELL_TOOLS and value in {
        PROBE, PROBE.replace('; ', '\n')}


def context_key(payload):
    args = payload.get('tool_input', {})
    directory = args.get('workdir', payload['cwd'])
    if not isinstance(directory, str) or not os.path.isabs(directory):
        raise ValueError('invalid_workdir')
    # 承認モードの変更は証跡を失効させるが、Sandboxの有効/無効には変換しない。
    return digest({'cwd': os.path.normcase(os.path.realpath(directory)),
        'session_id': payload['session_id'], 'transcript': payload.get('transcript_path'),
        'permission_mode': payload.get('permission_mode'),
        'sandbox_permissions': args.get('sandbox_permissions', 'use_default')})


def fresh(payload, reason='not_checked'):
    return {'schema': 1, 'session_id': payload['session_id'],
        'context': context_key(payload), 'result': 'unknown', 'reason': reason,
        'checked_at': None, 'sandbox_setting': 'unknown', 'isolation': 'unverified'}


class Store:
    def __init__(self, root=STATE_ROOT):
        self.root = Path(root)

    @contextlib.contextmanager
    def locked(self, session):
        # mkdirより先に、存在する親のsymlink/junctionも検査する。
        if self.root.resolve() != self.root.absolute():
            raise ValueError('state_directory_redirected')
        self.root.mkdir(parents=True, exist_ok=True)
        if self.root.resolve() != self.root.absolute():
            raise ValueError('state_directory_redirected')
        lock_path = self.root / (session + '.lock')
        if lock_path.is_symlink():
            raise ValueError('state_lock_redirected')
        with lock_path.open('a+b') as handle:
            handle.seek(0, 2)
            if handle.tell() == 0:
                handle.write(b'0')
                handle.flush()
            handle.seek(0)
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            try:
                yield
            finally:
                handle.seek(0)
                if os.name == 'nt':
                    msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def read(self, session):
        path = self.root / (session + '.json')
        if path.is_symlink():
            raise ValueError('state_record_redirected')
        if not path.exists():
            return None
        if path.stat().st_size > 65536:
            raise ValueError('state_record_too_large')
        record = json.loads(path.read_text(encoding='utf-8'))
        if (not isinstance(record, dict) or record.get('schema') != 1 or
                record.get('session_id') != session or record.get('result') not in
                {'success', 'failure', 'unknown'}):
            raise ValueError('invalid_state_record')
        return record

    def write(self, record):
        target = self.root / (record['session_id'] + '.json')
        if target.is_symlink():
            raise ValueError('state_record_redirected')
        audit = self.root / (record['session_id'] + '.jsonl')
        if audit.is_symlink():
            raise ValueError('state_audit_redirected')
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='\n',
                    dir=self.root, prefix='.status-', suffix='.tmp', delete=False) as handle:
                temporary = Path(handle.name)
                json.dump(record, handle, ensure_ascii=True, sort_keys=True)
                handle.write('\n')
            with audit.open('a', encoding='utf-8', newline='\n') as handle:
                json.dump({'observed_at': now(), **record}, handle, ensure_ascii=True, sort_keys=True)
                handle.write('\n')
            os.replace(temporary, target)
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()


def response_parts(response):
    """既知の構造化応答と、モデル向けの完了済みShell応答だけを解釈する。"""
    if isinstance(response, dict):
        output = response.get('output', response.get('stdout', ''))
        code = response.get('exit_code')
        if isinstance(output, str) and type(code) is int:
            return output, code
        return '', None
    if isinstance(response, str):
        try:
            decoded = json.loads(response)
        except (ValueError, TypeError):
            decoded = None
        if isinstance(decoded, dict):
            return response_parts(decoded)
        # headersをstdout本文から取り出さず、既知の完了形式のみを扱う。
        match = re.fullmatch(r'Chunk ID: [^\n]+\nWall time: [^\n]+\n'
            r'Process exited with code (-?\d+)\nFinal output:\n([\s\S]*)', response)
        if match:
            return match.group(2), int(match.group(1))
    return '', None


def failed_to_start(response):
    if isinstance(response, dict):
        output, code = response_parts(response)
        error = response.get('error', '')
        text = error if isinstance(error, str) else ''
        if code is not None and code != 0:
            text += output
    elif isinstance(response, str) and response.startswith(('exec_command failed:',
            'CreateProcess', 'windows sandbox failed:')):
        text = response
    else:
        return False
    return any(item in text for item in FAILURES)


def result_of_probe(payload):
    response = payload.get('tool_response')
    output, code = response_parts(response)
    if failed_to_start(response):
        return 'failure', 'sandbox_start_error'
    if code is not None and code != 0:
        return 'failure', 'probe_nonzero_exit'
    lines = [line.strip() for line in output.splitlines()]
    directory = payload['tool_input'].get('workdir', payload['cwd'])
    location_seen = any(os.path.normcase(line) == os.path.normcase(directory) for line in lines)
    if code == 0 and TOKEN in lines and location_seen:
        return 'success', 'probe_completed'
    return 'unknown', 'probe_result_unverified'


def feedback(event, text, deny=False):
    specific = {'hookEventName': event, 'additionalContext': text}
    if deny:
        specific.update(permissionDecision='deny', permissionDecisionReason=text)
    return {'systemMessage': text, 'hookSpecificOutput': specific}


def summary(record):
    names = {'success': '成功', 'failure': '失敗', 'unknown': '不明'}
    return ('Shell起動検証: ' + names[record['result']] +
        '。Sandbox実効設定: 不明。隔離制限: 未検証。理由: ' + record['reason'] +
        '。確認日時: ' + (record['checked_at'] or '未実施'))


def handle(payload, store=None):
    validate(payload)
    store = store or Store()
    event = payload['hook_event_name']
    if event != 'SessionStart' and payload['tool_name'] not in ACTION_TOOLS:
        return {}  # 会話、Web、参照専用ツールには追加の検証を要求しない。
    with store.locked(payload['session_id']):
        if event == 'SessionStart':
            store.write(fresh(payload))
            return {}  # 開始時は初期化だけ。検証・質問は実操作前まで行わない。
        record = store.read(payload['session_id'])
        if record is None or record.get('context') != context_key(payload):
            record = fresh(payload, 'not_checked' if record is None else 'context_changed')
            store.write(record)
        args = payload['tool_input']
        if args.get('sandbox_permissions') == 'require_escalated':
            return feedback(event, 'Sandbox外の操作は起動成功の証跡にしない。'
                '通常のホスト承認を維持し、結果をSandbox内の実行と区別して報告する。')
        if event == 'PreToolUse':
            if is_probe(payload):
                if not valid_id(payload.get('tool_use_id')):
                    return feedback(event, 'Shell起動検証: 不明。呼出しIDを確認できません。' + RETRY_QUESTION, True)
                if record.get('pending'):
                    if record.get('pending_turn') == payload.get('turn_id'):
                        return feedback(event, 'Shell起動検証: 不明（検証中）。'
                            '既存の実行完了を待ち、同時に再検証しない。', True)
                    record = fresh(payload, 'previous_probe_unresolved')
                retry = record['reason'] not in {'not_checked', 'context_changed'}
                record.update(result='unknown', reason='probe_pending', checked_at=None,
                    pending=payload['tool_use_id'], pending_turn=payload.get('turn_id'))
                store.write(record)
                text = '同じ実行経路の最小起動検証を実行し、出力と終了結果を照合する。'
                if retry:
                    text += '再検証は「' + RETRY_QUESTION + '」への利用者の明示的な肯定がある場合だけ行う。'
                return feedback(event, text)
            # Bootstrapの読取と単純な所在地診断は既存の契約ガードへ戻す。
            bootstrap = "Get-Content -LiteralPath '" + str(ROOT / 'AGENTS.md') + "' -Raw"
            if payload['tool_name'] in SHELL_TOOLS and command(payload).strip() in {'Get-Location', bootstrap}:
                return {}
            if record['result'] == 'success':
                return feedback(event, summary(record) + '。これは現在の業務操作の成功を保証しない。')
            if record.get('pending') and record.get('pending_turn') == payload.get('turn_id'):
                return feedback(event, 'Shell起動検証: 不明（検証中）。完了を待つ。', True)
            text = summary(record)
            if record['reason'] in {'not_checked', 'context_changed'}:
                text += '。本作業の前に、同じShell経路で次の無害な検証を単独実行する: ' + PROBE
            else:
                text += '。本作業を保留し、利用者に「' + RETRY_QUESTION + '」と確認する。'
            return feedback(event, text, True)
        if is_probe(payload):
            if record.get('pending') != payload.get('tool_use_id') or not record.get('pending'):
                return feedback(event, 'Shell起動検証: 不明。今回の検証と対応しない応答は採用しない。')
            outcome, reason = result_of_probe(payload)
            record = fresh(payload, reason)
            record.update(result=outcome, checked_at=now(), verified_call=payload['tool_use_id'])
            store.write(record)
            text = summary(record)
            if outcome != 'success':
                text += '。本作業を保留し、利用者に「' + RETRY_QUESTION + '」と確認する。'
            return feedback(event, text)
        if failed_to_start(payload.get('tool_response')):
            record = fresh(payload, 'sandbox_start_error')
            record.update(result='failure', checked_at=now())
            store.write(record)
            return feedback(event, summary(record) + '。本作業を保留し、利用者に「' + RETRY_QUESTION + '」と確認する。')
        return {}  # 業務コマンドの非0終了をSandbox起動失敗と混同しない。


def main():
    payload = None
    try:
        payload = json.load(sys.stdin)
        output = handle(payload)
    except Exception:
        event = payload.get('hook_event_name') if isinstance(payload, dict) else None
        text = 'Shell起動検証: 不明。hook入力または状態記録を確認できません。' + RETRY_QUESTION
        if event == 'SessionStart':
            output = {'systemMessage': 'Sandbox確認状態の初期化: 不明。実操作前に再確認する。'}
        elif event in {'PreToolUse', 'PostToolUse'}:
            output = feedback(event, text, event == 'PreToolUse')
        else:
            print('Sandbox確認hook入力: 不明。実操作前に確認する。', file=sys.stderr)
            return 2
    print(json.dumps(output, ensure_ascii=True), flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
