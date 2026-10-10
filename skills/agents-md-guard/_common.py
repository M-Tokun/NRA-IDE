"""AGENTS.md 全文出力記録・更新検知ガードの共通ロジック。

Claude Code / Codex CLI / Gemini CLI / Cline の各hookスクリプトから読み込まれる。
AGENTS.md §11第2層のうち、AGENTS.md全文の出力記録と更新検知を実装する。
他の重要文書・Skillの実績検証、モデルの理解、ホストの配送完了、操作承認は扱わない。

マーカーファイルは、AIツールごとのセッション/タスクIDをファイル名として
`.agent_state/agents_md_read/<tool>/<id>` に作成する。ツールを分けるのは、
異なるハーネスのID空間が衝突しないようにするため。
"""
import hashlib
import json
import os
import re
import shlex
import sys

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MARKER_ROOT = os.path.join(_REPO_ROOT, '.agent_state', 'agents_md_read')
AGENTS_MD_PATH = os.path.join(_REPO_ROOT, 'AGENTS.md')
REASON_MESSAGE = ('このセッションで現在のAGENTS.md全文の読込を確認できません。'
                  '操作を停止し、セッション再開または再読込で開始時hookを実行してください。')
MISSING_REASON_MESSAGE = ('AGENTS.mdが存在しないか完全に読み込めません。'
                          '操作を停止し、利用者に報告してください。')
INVALID_PAYLOAD_MESSAGE = ('hook入力を検証できません。未確認状態を許可せず、操作を停止します。')
READ_ONLY_TOOLS = frozenset({'Read', 'Glob', 'Grep', 'LS', 'WebFetch', 'WebSearch',
    'read_file', 'read_many_files', 'list_directory', 'glob', 'search_file_content',
    'google_web_search', 'web_fetch'})
# AGENTS.md §7: history rewrite and forced sending are not run on the AI route.
SHELL_COMMAND_TOOLS = frozenset({'Bash', 'PowerShell', 'exec_command', 'shell_command',
    'shell', 'run_shell_command', 'cline_tool:execute_command'})
SHELL_DENY_MESSAGE = ('{}は実行しません（AGENTS.md §7）。履歴改変・強制送信・フック回避・'
                      'リモート参照の削除は通常経路で行わず、対象と影響を提示して'
                      '利用者管理の手順へ返してください。')
SHELL_INVALID_MESSAGE = 'シェルコマンドを文字列として確認できません。操作を停止します。'
_SEGMENT_SPLIT = re.compile(r'&&|\|\||[;&|\r\n]')
_WRAPPER_SHELLS = frozenset({'pwsh', 'powershell', 'bash', 'sh', 'zsh', 'cmd'})
_WRAPPER_FLAGS = frozenset({'-c', '-lc', '-ic', '-command', '/c', '/k'})
_LEADING_WORDS = frozenset({'call', 'command', 'exec', 'sudo', 'time', 'nohup', 'env'})
_ENV_ASSIGNMENT = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*=')


def valid_session_id(value):
    # A session identifier must never be interpreted as a filesystem path.
    return isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9_-]{1,200}', value) is not None


def normalized_path(value):
    return os.path.normcase(os.path.realpath(os.path.abspath(value)))


def content_hash(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def marker_dir(tool):
    if tool not in {'claude', 'codex', 'gemini', 'cline'}:
        raise ValueError('Invalid tool identifier')
    return os.path.join(MARKER_ROOT, tool)


def marker_path(tool, task_id):
    if not valid_session_id(task_id):
        raise ValueError('Invalid session identifier')
    return os.path.join(marker_dir(tool), task_id)


def read_agents_md():
    with open(AGENTS_MD_PATH, encoding='utf-8') as handle:
        content = handle.read()
    if not content.strip():
        raise ValueError('AGENTS.md is empty')
    return content


def agents_md_status():
    try:
        read_agents_md()
    except FileNotFoundError:
        return 'missing'
    except (OSError, UnicodeError, ValueError):
        return 'unreadable'
    return 'ok'


def marker_record(tool, task_id, content):
    return {'schema': 2, 'tool': tool, 'session_id': task_id,
            'agents_path': normalized_path(AGENTS_MD_PATH),
            'agents_sha256': content_hash(content)}


def is_marked(tool, task_id):
    try:
        path = marker_path(tool, task_id)
        if os.path.islink(path):
            return False
        with open(path, encoding='utf-8') as handle:
            record = json.load(handle)
        return isinstance(record, dict) and record == marker_record(tool, task_id, read_agents_md())
    except (ValueError, TypeError, OSError, UnicodeError):
        return False


def write_marker(tool, task_id, content=None):
    path = marker_path(tool, task_id)
    if os.path.islink(path):
        raise ValueError('Refusing a symlink marker')
    if content is None:
        content = read_agents_md()
    os.makedirs(marker_dir(tool), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as handle:
        json.dump(marker_record(tool, task_id, content), handle)
        handle.write('\n')


def invalidate_marker(tool, task_id):
    path = marker_path(tool, task_id)
    if os.path.islink(path):
        raise ValueError('Refusing a symlink marker')
    if os.path.isfile(path):
        # Invalidate an earlier start before attempting to emit new context.
        with open(path, 'w', encoding='utf-8') as handle:
            handle.write('{}\n')


def path_targets_agents_md(value):
    if not isinstance(value, str) or not value or '\x00' in value:
        return False
    return normalized_path(value) == normalized_path(AGENTS_MD_PATH)


def command_reads_agents_md(value):
    # Kept for old adapters. A command string cannot prove a full successful read.
    return False


def load_payload(stream, tool):
    payload = json.load(stream)
    if not isinstance(payload, dict):
        raise ValueError('Hook payload must be an object')
    if tool == 'cline':
        from cline_adapter import normalize_payload
        payload = normalize_payload(payload)
    key = 'taskId' if tool == 'cline' else 'session_id'
    if not valid_session_id(payload.get(key)):
        raise ValueError('Missing or invalid session identifier')
    for key in ('tool_name', 'hook_event_name'):
        if key in payload and not isinstance(payload[key], str):
            raise ValueError('Invalid hook field')
    for key in ('tool_input', 'parameters'):
        if key in payload and not isinstance(payload[key], dict):
            raise ValueError('Tool arguments must be an object')
    return payload


def reads_only_current_contract(payload, tool):
    # Bootstrap permits only one complete contract read, never search/mixed reads.
    if payload.get('tool_name') not in {'Read', 'read_file', 'read_many_files'}:
        return False
    args = payload.get('parameters' if tool == 'cline' else 'tool_input', {})
    if len(args) != 1 or not set(args).issubset({'path', 'file_path', 'absolute_path', 'paths'}):
        return False
    key, value = next(iter(args.items()))
    if key == 'paths':
        if not isinstance(value, list) or len(value) != 1:
            return False
        value = value[0]
    if not isinstance(value, str) or not value or '\x00' in value:
        return False
    if not os.path.isabs(value):
        base = os.path.dirname(AGENTS_MD_PATH) if tool == 'cline' else payload.get('cwd', os.path.dirname(AGENTS_MD_PATH))
        if not isinstance(base, str) or not os.path.isabs(base):
            return False
        value = os.path.join(base, value)
    return path_targets_agents_md(value)


def _unquote(text):
    text = text.strip()
    if len(text) >= 2 and text[0] in '\'"' and text[-1] == text[0]:
        return text[1:-1]
    return text


def _command_words(segment):
    # Quoted arguments stay single words, so message text is not read as options.
    try:
        # A stray quote at a word edge comes from splitting inside a quoted script.
        words = [word if len(word) >= 2 and word[0] in '\'"' and word[-1] == word[0]
                 else word.strip('\'"') for word in shlex.split(segment, posix=False)]
    except ValueError:
        # An unbalanced quote comes from splitting inside a quoted script; drop the strays.
        words = [word.strip('\'"') for word in re.findall(r'\S+', segment)]
    return [word for word in words if word]


def _program_name(word):
    name = _unquote(word).replace('\\', '/').rsplit('/', 1)[-1].lower()
    return name[:-4] if name.endswith('.exe') else name


def _git_label(args):
    index = 0
    while index < len(args):
        arg = _unquote(args[index])
        low = arg.lower()
        if arg == '-c':
            value = _unquote(args[index + 1]).lower() if index + 1 < len(args) else ''
            if value.startswith('core.hookspath='):
                return 'git -c core.hooksPath'
            index += 2
        elif arg == '-C' or low in {'--git-dir', '--work-tree', '--namespace',
                                    '--super-prefix', '--config-env'}:
            if low == '--config-env' and index + 1 < len(args) and \
                    _unquote(args[index + 1]).lower().startswith('core.hookspath='):
                return 'git --config-env core.hooksPath'
            index += 2
        elif low.startswith('--config-env=') and 'core.hookspath' in low:
            return 'git --config-env core.hooksPath'
        elif arg.startswith('-'):
            index += 1
        else:
            break
    if index >= len(args):
        return None
    sub = _unquote(args[index]).lower()
    raw = args[index + 1:]
    rest = [_unquote(word) for word in raw]
    low_rest = [word.lower() for word in rest]
    # Quoted words (commit messages) are skipped; only bare options count.
    if any(word.lower().startswith('--no-verify') for word in raw):
        return 'git --no-verify'
    if sub in {'filter-repo', 'filter-branch'}:
        return 'git ' + sub
    if sub == 'reflog' and next((w for w in low_rest if not w.startswith('-')), '') == 'expire':
        return 'git reflog expire'
    if sub == 'gc' and any(word.startswith('--prune') for word in low_rest):
        return 'git gc --prune'
    if sub == 'config' and any(word == 'core.hookspath' or word.startswith('core.hookspath=')
                               for word in low_rest):
        return 'git config core.hooksPath'
    if sub == 'push':
        for word, low in zip(rest, low_rest):
            if low.startswith('--force'):
                return 'git push --force'
            if low == '--delete' or re.fullmatch(r'-[a-z]*d[a-z]*', low):
                return 'git push --delete'
            if re.fullmatch(r'-[a-z]*f[a-z]*', low):
                return 'git push --force'
            if word.startswith('+') or word.startswith(':'):
                return 'git push +refspec/:ref'
    return None


def dangerous_git_command(command, depth=0):
    """Return a label if the command string runs a denied git operation, else None.

    A pattern guard against mistakes. It reads only the command text, so scripts,
    aliases, variables and `python -c` bodies are not visible to it.
    """
    for segment in _SEGMENT_SPLIT.split(command):
        words = _command_words(segment)
        index = 0
        while index < len(words) and (_unquote(words[index]).lower() in _LEADING_WORDS
                                      or _ENV_ASSIGNMENT.match(words[index])):
            index += 1
        if index >= len(words):
            continue
        program = _program_name(words[index])
        label = None
        if program == 'git':
            label = _git_label(words[index + 1:])
        elif program == 'git-filter-repo':
            label = 'git filter-repo'
        elif program in _WRAPPER_SHELLS and depth < 3:
            for position in range(index + 1, len(words)):
                if _unquote(words[position]).lower() in _WRAPPER_FLAGS:
                    label = dangerous_git_command(
                        _unquote(' '.join(words[position + 1:])), depth + 1)
                    break
        if label:
            return label
    return None


def shell_deny_reason(payload, tool):
    if payload.get('tool_name') not in SHELL_COMMAND_TOOLS:
        return None
    args = payload.get('parameters' if tool == 'cline' else 'tool_input', {})
    if 'command' not in args and 'cmd' not in args:
        return None  # No command text was sent, so there is nothing to inspect.
    command = args.get('command', args.get('cmd'))
    if not isinstance(command, str):
        return SHELL_INVALID_MESSAGE
    label = dangerous_git_command(command)
    return SHELL_DENY_MESSAGE.format(label) if label else None


def guard_reason(payload, tool):
    if agents_md_status() != 'ok':
        return MISSING_REASON_MESSAGE
    key = 'taskId' if tool == 'cline' else 'session_id'
    if is_marked(tool, payload[key]) or reads_only_current_contract(payload, tool):
        return shell_deny_reason(payload, tool)
    return REASON_MESSAGE


def emit_guard_result(tool, reason):
    if tool == 'cline':
        output = {'cancel': reason is not None}
        if reason:
            output['errorMessage'] = reason
    elif tool == 'gemini':
        # An empty object leaves normal host permissions intact; never auto-approve.
        output = {'decision': 'deny', 'reason': reason} if reason else {}
    elif reason:
        output = {'hookSpecificOutput': {'hookEventName': 'PreToolUse',
            'permissionDecision': 'deny', 'permissionDecisionReason': reason}}
    else:
        # Claude and Codex fall through to the host's ordinary permission checks.
        return
    print(json.dumps(output, ensure_ascii=True), flush=True)


def run_guard(tool):
    try:
        payload = load_payload(sys.stdin, tool)
        reason = guard_reason(payload, tool)
    except Exception:
        reason = INVALID_PAYLOAD_MESSAGE
    emit_guard_result(tool, reason)
    return 0


def run_session_start(tool):
    emitted = False
    try:
        payload = load_payload(sys.stdin, tool)
        invalidate_marker(tool, payload['session_id'])
        content = read_agents_md()
        context = 'AGENTS.md loaded\n\n' + content
        # Refuse to record content that would exceed the output channel's limit.
        limit = 12000 if tool == 'codex' else 10000
        if len(context) > limit:
            raise ValueError('Contract exceeds context limit')
        print(json.dumps({'systemMessage': 'AGENTS.md loaded',
            'hookSpecificOutput': {'hookEventName': 'SessionStart',
                                   'additionalContext': context}}, ensure_ascii=True), flush=True)
        emitted = True
        write_marker(tool, payload['session_id'], content)
        return 0
    except Exception as exc:
        if emitted:
            # One JSON object per hook. A missing marker still blocks mutations.
            print('SessionStart marker recording failed', file=sys.stderr)
            return 2
        reason = MISSING_REASON_MESSAGE if isinstance(exc, (OSError, UnicodeError)) else INVALID_PAYLOAD_MESSAGE
        try:
            print(json.dumps({'continue': False, 'stopReason': reason,
                              'systemMessage': reason}, ensure_ascii=True), flush=True)
        except (OSError, UnicodeError):
            return 2
        # Gemini cannot block startup; its BeforeTool rejects missing markers.
        return 0


def mark_verified_read(tool):
    # Legacy PostToolUse/AfterTool adapters. New configs use SessionStart.
    # Unsupported response formats cannot establish a read.
    try:
        payload = load_payload(sys.stdin, tool)
        args = payload.get('parameters' if tool == 'cline' else 'tool_input', {})
        path = args.get('file_path') or args.get('absolute_path') or args.get('path')
        if not path_targets_agents_md(path):
            return 0
        if any(key in args for key in ('offset', 'limit', 'start_line', 'end_line')):
            return 0
        response = payload.get('tool_response')
        if not isinstance(response, dict) or response.get('error') or response.get('is_error'):
            return 0
        text = response.get('content') or response.get('llmContent')
        if isinstance(response.get('file'), dict):
            text = response['file'].get('content')
        content = read_agents_md()
        if not isinstance(text, str) or text != content:
            return 0
        key = 'taskId' if tool == 'cline' else 'session_id'
        write_marker(tool, payload[key], content)
    except (ValueError, TypeError, OSError, UnicodeError, KeyError):
        pass  # No marker; the next mutation remains blocked.
    return 0
