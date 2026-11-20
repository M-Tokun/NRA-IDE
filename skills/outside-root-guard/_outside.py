"""作業ルート外のパスに触れる操作を、hook で機械的に止める共通ロジック（AGENTS.md §2・§6・§11第2層）。

Claude Code / Codex CLI / Gemini CLI / Cline の各 PreToolUse hook から読み込まれる。
AI が「警告:」を書き忘れても、ルート外のパスに触れた時点で必ず止め、警告を画面に出す。

判定:
- ルート内・許可リスト内のパスだけ → 何も出さず通常の権限確認へ（自動許可はしない）
- ルート外のパスを含む → Claude は ask（利用者の確認待ち）、他のホストは deny（許可リストへの追加は利用者が行う）
- 許可リストのファイルを AI が書き換えようとする → 全ホストで deny
- 判定中の例外 → Claude は ask、他のホストは deny

限界: シェルコマンドは文字列から典型的なパス表記だけを拾う。変数で組み立てたパスや、
スクリプトの中で開くファイルは見えない。AGENTS.md §2 の文章規則と二重で使う。
"""
import fnmatch
import json
import os
import re
import sys
from datetime import datetime, timezone

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(_HERE))
DEFAULT_ALLOW = os.path.join(_HERE, 'allow_default.txt')
LOCAL_ALLOW = os.path.join(REPO_ROOT, '.agent_state', 'outside_root_allow.txt')
LOG_PATH = os.path.join(REPO_ROOT, '.agent_state', 'hooks', 'outside_root.jsonl')

PATH_KEYS = ('file_path', 'path', 'absolute_path', 'notebook_path', 'dir_path',
             'directory', 'cwd', 'workdir', 'target_file')
LIST_KEYS = ('paths',)
PATTERN_KEYS = ('pattern',)  # Glob の pattern が絶対パスのときだけ見る
SHELL_TOOLS = frozenset({'Bash', 'PowerShell', 'exec_command', 'shell_command', 'shell',
                         'run_shell_command', 'cline_tool:execute_command'})
WRITE_TOOLS = frozenset({'Write', 'Edit', 'MultiEdit', 'NotebookEdit', 'write_file', 'replace',
                         'apply_patch', 'cline_tool:write_to_file', 'cline_tool:replace_in_file'})

_STOP = r'[^\s"\'`|;&<>()]'
_DRIVE = re.compile(r'(?<![\w])([A-Za-z]:[\\/]' + _STOP + r'*)')
_GITBASH = re.compile(r'(?<![\w.:/~-])(/[A-Za-z]/' + _STOP + r'*)')
_TMP = re.compile(r'(?<![\w.:/~-])(/tmp(?:/' + _STOP + r'*)?)(?=[\s"\'`|;&<>()]|$)')
_ENV_NAMES = r'(?:HOME|USERPROFILE|APPDATA|LOCALAPPDATA|TEMP|TMP|PROGRAMDATA|PROGRAMFILES|SYSTEMROOT|WINDIR)'
_HOMEISH = re.compile(r'(?<![\w$%])((?:~|\$' + _ENV_NAMES + r'\b|\$\{' + _ENV_NAMES + r'\}|%'
                      + _ENV_NAMES + r'%|\$env:' + _ENV_NAMES + r'\b)(?:[\\/]' + _STOP + r'*)?)',
                      re.IGNORECASE)
_DOTDOT = re.compile(r'(?<![\w.])(\.\.(?:[\\/]' + _STOP + r'*)?)')
_CD = re.compile(r'(?:^|[;&|\n(]|&&)\s*(?:cd|pushd|Set-Location|sl)\s+("[^"]*"|\'[^\']*\'|' + _STOP + r'+)',
                 re.IGNORECASE)
_PATCH = re.compile(r'^\*\*\* (?:(?:Add|Update|Delete) File|Move to): (.+?)\s*$', re.MULTILINE)
_IGNORED = frozenset({'/dev/null', 'nul', 'nul:'})
# 許可リストを守る判定：書込みの操作だけを見る
_REDIRECT = re.compile(r'(?:^|[^\d&>])>>?\s*("[^"]+"|\'[^\']+\'|[^\s|;&<>]+)')
_SEGMENTS = re.compile(r'&&|\|\||[;\n|]')
_WRITE_CMD = re.compile(r'(?:^|\s|\()(?:tee|sed\s+(?:-\S+\s+)*-i\S*|cp|mv|rm|del|erase|truncate|'
                        r'Set-Content|Add-Content|Out-File|Copy-Item|Move-Item|Remove-Item|'
                        r'New-Item|Clear-Content)(?=\s|$)', re.IGNORECASE)
# 確認の一言に出す操作の呼び方
KIND_WORDS = {'読取': '読み取り', '書込': '書き込み', 'シェル': 'シェルでの読み書き', '作業場所': '作業場所の移動'}


def _norm(path):
    return os.path.normcase(os.path.realpath(os.path.abspath(path)))


def _expand(token, cwd):
    """シェル表記・環境変数・git-bash 形式を絶対パスに直す。直せなければ None。"""
    text = token.strip().strip('"\'')
    if not text or text.lower() in _IGNORED:
        return None
    text = re.sub(r'\$env:(\w+)', r'%\1%', text, flags=re.IGNORECASE)
    text = re.sub(r'\$\{(\w+)\}', r'$\1', text)
    if text.startswith('~'):
        text = os.path.expanduser('~') + text[1:]
    if re.match(r'^%HOME%', text, re.IGNORECASE) and 'HOME' not in os.environ:
        text = os.path.expanduser('~') + text[6:]
    text = os.path.expandvars(text)
    if re.search(r'%\w+%|\$\w+', text):
        return token  # 展開できない変数：確認できないパスとして扱う
    m = re.match(r'^/([A-Za-z])(/.*)?$', text)
    if m and os.name == 'nt':
        text = m.group(1).upper() + ':' + (m.group(2) or '/')
    if text == '/tmp' or text.startswith('/tmp/'):
        import tempfile
        text = os.path.join(tempfile.gettempdir(), text[5:])
    if not os.path.isabs(text):
        text = os.path.join(cwd, text)
    return _norm(text)


def _inside(path, base):
    try:
        return os.path.commonpath([path, base]) == base
    except ValueError:
        return False  # 別ドライブ


def load_allow():
    entries = []
    for src in (DEFAULT_ALLOW, LOCAL_ALLOW):
        try:
            with open(src, encoding='utf-8') as handle:
                for line in handle:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        entries.append(_norm(os.path.expanduser(os.path.expandvars(line))))
        except OSError:
            pass
    return entries


def is_allowed(path, allow):
    if _inside(path, _norm(REPO_ROOT)):
        return True
    for entry in allow:
        if any(ch in entry for ch in '*?['):
            if fnmatch.fnmatch(path, entry) or fnmatch.fnmatch(path, os.path.join(entry, '*')):
                return True
        elif _inside(path, entry):
            return True
    return False


def shell_paths(command, cwd):
    found = []
    for rx in (_DRIVE, _GITBASH, _TMP, _HOMEISH, _DOTDOT):
        found += [m.group(1) for m in rx.finditer(command)]
    found += [m.group(1) for m in _CD.finditer(command) if m.group(1) not in ('-', '..')]
    return [p for p in (_expand(t, cwd) for t in found) if p]


def collect(payload, tool):
    """(パス, 操作の種類) の一覧を返す。"""
    name = payload.get('tool_name')
    args = payload.get('parameters' if tool == 'cline' else 'tool_input') or {}
    if not isinstance(args, dict):
        raise ValueError('tool arguments must be an object')
    cwd = payload.get('cwd') if isinstance(payload.get('cwd'), str) else REPO_ROOT
    kind = '書込' if name in WRITE_TOOLS else '読取'
    out = []
    for key in PATH_KEYS:
        value = args.get(key)
        if isinstance(value, str) and value:
            out.append((_expand(value, cwd), '作業場所' if key in ('cwd', 'workdir') else kind))
    for key in LIST_KEYS:
        value = args.get(key)
        if isinstance(value, list):
            out += [(_expand(v, cwd), kind) for v in value if isinstance(v, str)]
    for key in PATTERN_KEYS:
        value = args.get(key)
        if isinstance(value, str) and (os.path.isabs(value) or _DRIVE.match(value)):
            out.append((_expand(value, cwd), kind))
    if name in SHELL_TOOLS:
        command = args.get('command', args.get('cmd'))
        if isinstance(command, list):
            command = ' '.join(str(c) for c in command)
        if isinstance(command, str):
            base = args.get('workdir') if isinstance(args.get('workdir'), str) else cwd
            out += [(p, 'シェル') for p in shell_paths(command, base)]
    for value in args.values():
        if isinstance(value, str) and '*** ' in value:
            out += [(_expand(m.group(1), cwd), '書込') for m in _PATCH.finditer(value)]
    return [(p, k) for p, k in out if p]


def protected_write(payload, tool, pairs):
    """許可リストのファイルを AI が書き換える操作か。"""
    protected = {_norm(DEFAULT_ALLOW), _norm(LOCAL_ALLOW)}
    if any(p in protected for p, k in pairs if k == '書込'):
        return True
    args = payload.get('parameters' if tool == 'cline' else 'tool_input') or {}
    command = args.get('command', args.get('cmd')) if isinstance(args, dict) else None
    if isinstance(command, list):
        command = ' '.join(str(c) for c in command)
    if not isinstance(command, str):
        return False
    names = [os.path.basename(p).lower() for p in (DEFAULT_ALLOW, LOCAL_ALLOW)]
    # リダイレクトの宛先が許可リストなら書込み（2>/dev/null などの宛先は見ない）
    for m in _REDIRECT.finditer(command):
        if os.path.basename(m.group(1).strip('"\'')).lower() in names:
            return True
    # 書込み系コマンドと許可リストの名前が同じ区切りの中にあれば書込み。git add・cat などは通す
    for segment in _SEGMENTS.split(command):
        low = segment.lower()
        if any(n in low for n in names) and _WRITE_CMD.search(segment):
            return True
    return False


def decide(payload, tool):
    """(判定, 理由)。判定は None（通す）/ 'ask' / 'deny'。"""
    pairs = collect(payload, tool)
    if protected_write(payload, tool, pairs):
        return 'deny', ('許可リスト（outside-root-guard）は利用者が編集するファイルです。'
                        'AI は書き換えません（AGENTS.md §11）。')
    allow = load_allow()
    outside = []
    for path, kind in pairs:
        if not os.path.isabs(path) or not is_allowed(path, allow):
            if (path, kind) not in outside:
                outside.append((path, kind))
    if not outside:
        return None, None
    kinds = '・'.join(dict.fromkeys(KIND_WORDS.get(k, k) for _, k in outside))
    head = f'CAUTION!!アウトルート_OK!!!!! リポジトリルート外の「{kinds}」をしてよいですか？ '
    shown = '／'.join(f'警告: {p}: 作業ルート外の{k}' for p, k in outside[:3])
    more = f'（ほか{len(outside) - 3}件）' if len(outside) > 3 else ''
    if tool == 'claude':
        return 'ask', f'{head}{shown}{more}。許可する場合だけ承認してください（AGENTS.md §2・§6）。'
    return 'deny', (f'{head}{shown}{more}。操作を止めました。必要なら、利用者が '
                    f'.agent_state/outside_root_allow.txt にパスを追加してから再実行します（AGENTS.md §2・§6）。')


def emit(tool, decision, reason):
    if tool == 'cline':
        output = {'cancel': decision is not None, 'contextModification': '',
                  'errorMessage': reason or ''}
    elif tool == 'gemini':
        output = {'decision': 'deny', 'reason': reason} if decision else {}
    elif decision:
        output = {'hookSpecificOutput': {'hookEventName': 'PreToolUse',
                  'permissionDecision': decision, 'permissionDecisionReason': reason}}
    else:
        return  # 通常の権限確認へ。自動許可はしない
    print(json.dumps(output, ensure_ascii=True), flush=True)


def log(tool, payload, decision, reason):
    if decision is None:
        return
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        record = {'time_utc': datetime.now(timezone.utc).isoformat(), 'host': tool,
                  'tool_name': payload.get('tool_name') if isinstance(payload, dict) else None,
                  'decision': decision, 'reason': reason}
        with open(LOG_PATH, 'a', encoding='utf-8', newline='\n') as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + '\n')
    except OSError:
        pass  # 記録の失敗を判定に変えない


def run(tool):
    payload = {}
    try:
        raw = sys.stdin.buffer.read() if hasattr(sys.stdin, 'buffer') else sys.stdin.read()
        payload = json.loads(raw.decode('utf-8') if isinstance(raw, bytes) else raw)
        if not isinstance(payload, dict):
            raise ValueError('payload must be an object')
        if tool == 'cline':
            sys.path.insert(0, os.path.join(REPO_ROOT, 'skills', 'agents-md-guard'))
            from cline_adapter import normalize_payload
            payload = normalize_payload(payload)
        decision, reason = decide(payload, tool)
    except Exception:
        decision = 'ask' if tool == 'claude' else 'deny'
        reason = 'ルート外ガードが入力を確認できません。安全のため止めました。'
    log(tool, payload, decision, reason)
    emit(tool, decision, reason)
    return 0
