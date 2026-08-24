"""AGENTS.md 読了ガードの共通ロジック。

Claude Code / Codex CLI / Gemini CLI の各hookスクリプトから読み込まれる。
AGENTS.md §11「重要文書・Skillの読込保証」第2層（機械的ゲート）の実装。

マーカーファイルは、AIツールごとのセッション/タスクIDをファイル名として
`.agent_state/agents_md_read/<tool>/<id>` に作成する。ツールを分けるのは、
異なるハーネスのID空間が衝突しないようにするため。
"""
import os

# 呼び出し元プロセスのcwdに依存しないよう、リポジトリルートをこのファイル
# 自身の場所（skills/agents-md-guard/_common.py）から逆算する。
# hookは通常プロジェクトルートを起点に呼ばれるが、直前のBash等でcdした
# 状態が残っていると、cwd基準の相対パスは容易にズレるため。
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _repo_path(*parts: str) -> str:
    return os.path.join(_REPO_ROOT, *parts)


MARKER_ROOT = _repo_path(".agent_state", "agents_md_read")

# 読取系コマンドでAGENTS.mdを開いたと推定できるコマンド動詞。
# Codexなど専用Readツールを持たない（シェル経由でファイルを読む）ハーネス向けの
# ヒューリスティック検知に使う。完全ではなく、あくまでベストエフォート。
_READ_VERBS = (
    "cat", "type", "head", "tail", "sed", "rg", "grep",
    "get-content", "gc", "more", "less", "bat",
)


def marker_dir(tool: str) -> str:
    return os.path.join(MARKER_ROOT, tool)


def marker_path(tool: str, task_id: str) -> str:
    return os.path.join(marker_dir(tool), task_id)


def is_marked(tool: str, task_id: str) -> bool:
    if not task_id:
        return False
    return os.path.isfile(marker_path(tool, task_id))


def write_marker(tool: str, task_id: str) -> None:
    if not task_id:
        return
    d = marker_dir(tool)
    os.makedirs(d, exist_ok=True)
    with open(marker_path(tool, task_id), "w", encoding="utf-8") as f:
        f.write("read\n")


def path_targets_agents_md(path_value: str) -> bool:
    """file_path/absolute_path が、リポジトリルートのAGENTS.mdを指しているか。

    サブディレクトリ・worktree内の別AGENTS.md（例: .kilo/worktrees/*/AGENTS.md）
    には一致しない。
    """
    if not path_value:
        return False
    normalized = path_value.replace("\\", "/").lower()
    return normalized.endswith("/nra-ide/agents.md")


def command_reads_agents_md(command_value: str) -> bool:
    """シェルコマンド文字列が、AGENTS.mdを読取系コマンドで開いていそうか。

    専用のReadツールを持たないハーネス（Codex等）向けのヒューリスティック。
    確実な検知ではない点に留意（コマンド文字列の解析であり、実行結果は見ない）。
    """
    if not command_value or "agents.md" not in command_value.lower():
        return False
    lowered = command_value.lower()
    return any(verb in lowered for verb in _READ_VERBS)


REASON_MESSAGE = (
    "AGENTS.mdをまだ読んでいません。先にリポジトリルートの AGENTS.md を"
    "読んでから再試行してください（AGENTS.md 第1章・第11章参照）。"
)

MISSING_REASON_MESSAGE = (
    "AGENTS.md が見つからないか、完全に読み込めません。推論で読んだことに"
    "して続行せず、ここで停止し、利用者に報告してください"
    "（ブートストラップ手順 ステップ4）。"
)

AGENTS_MD_PATH = _repo_path("AGENTS.md")


def agents_md_status() -> str:
    """AGENTS.md が読める状態かを判定する。'ok' / 'missing' / 'unreadable' を返す。

    'missing' はファイルが存在しない場合、'unreadable' は存在するが開けない・
    空である場合。guard側はこの2つを「まだ読んでいない」（is_markedがFalse）
    とは区別して扱う。
    """
    if not os.path.isfile(AGENTS_MD_PATH):
        return "missing"
    try:
        with open(AGENTS_MD_PATH, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return "unreadable"
    if not content.strip():
        return "unreadable"
    return "ok"
