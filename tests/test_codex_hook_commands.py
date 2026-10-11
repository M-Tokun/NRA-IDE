"""Codex hookの起動コマンドが、起動するシェルに依存しないことの回帰テスト。

Codexのhookは失敗してもツール呼び出しを止めない。外側のシェルがPowerShellだと
`$root` が展開されて起動に失敗し、ガードが黙って無効になるため、`$` を含めない。
実行テストは無効なsession_idを渡し、記録を作らずに起動と応答だけを確認する。
"""
from __future__ import annotations
import json, os, pathlib, shutil, subprocess, tempfile, unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HOOKS = json.loads((ROOT / ".codex" / "hooks.json").read_text(encoding="utf-8"))["hooks"]
ENTRIES = [(event, hook) for event, groups in HOOKS.items()
           for group in groups for hook in group["hooks"]]
BAD_SESSION = "../not-a-session"
# 起動確認用の観測probe。実行すると .agent_state/hooks/pre_tool_use.jsonl に
# 実クライアントの配送証拠と区別できない記録が残るため、実行テストの対象外にする。
OBSERVATION_PROBE = "check.py"


def payload(event):
    value = {"session_id": BAD_SESSION, "hook_event_name": event,
             "cwd": str(ROOT), "tool_name": "Bash", "tool_input": {"command": "git status"}}
    return json.dumps(value)


class CodexHookCommandTests(unittest.TestCase):
    def test_every_hook_has_a_windows_command(self):
        self.assertTrue(ENTRIES)
        for event, hook in ENTRIES:
            with self.subTest(event=event, script=hook["command"][-40:]):
                self.assertIn("commandWindows", hook)

    def test_windows_command_does_not_depend_on_the_launching_shell(self):
        for event, hook in ENTRIES:
            command = hook["commandWindows"]
            with self.subTest(event=event, command=command[:60]):
                self.assertNotIn("$", command)      # PowerShell expands it before Python starts
                self.assertNotIn("`", command)
                self.assertFalse(command.lower().startswith("pwsh"))
                self.assertTrue(command.startswith("python -B -c "))

    def test_windows_command_names_the_same_script_as_the_posix_command(self):
        for event, hook in ENTRIES:
            script = [part.strip() for part in hook["command"].replace('"', " ").split("/")
                      if part.strip().endswith(".py")][-1]
            with self.subTest(event=event, script=script):
                self.assertIn("'" + script + "'", hook["commandWindows"])

    @unittest.skipUnless(os.name == "nt", "commandWindows is used only on Windows")
    def test_runs_from_cmd_and_powershell_in_root_and_subdirectory(self):
        shells = ["cmd"] + (["powershell"] if shutil.which("pwsh") else [])
        directories = [ROOT, ROOT / "skills" / "agents-md-guard"]
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as tmp:
            for event, hook in ENTRIES:
                if "'" + OBSERVATION_PROBE + "'" in hook["commandWindows"]:
                    continue
                file = pathlib.Path(tmp) / (event + ".json")
                file.write_text(payload(event), encoding="utf-8")
                for shell in shells:
                    for directory in directories:
                        with self.subTest(event=event, shell=shell, cwd=directory.name,
                                          script=hook["commandWindows"][-55:]):
                            if shell == "cmd":
                                result = subprocess.run(hook["commandWindows"], shell=True,
                                    cwd=directory, input=payload(event).encode(),
                                    capture_output=True, timeout=30)
                            else:
                                script = "Get-Content -Raw '" + str(file) + "' | " + hook["commandWindows"]
                                result = subprocess.run(["pwsh", "-NoProfile", "-Command", script],
                                    cwd=directory, capture_output=True, timeout=30)
                            self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", "replace"))
                            output = json.loads(result.stdout.decode("utf-8"))
                            self.assertIsInstance(output, dict)
                            self.assertTrue(output)  # 起動して、異常入力に応答した


if __name__ == "__main__":
    unittest.main()
