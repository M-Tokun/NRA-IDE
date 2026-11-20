#!/usr/bin/env python
"""Cline PreToolUse の連結：AGENTS.md 読込ガード → 作業ルート外ガードの順に実行する。

Cline はイベントごとに hook を1本しか持てないため、ここで2本を順に呼ぶ。
どちらかが cancel を返せばそこで止める。出力が不正・失敗なら止める（fail-closed）。
"""
import json
import os
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
STEPS = (os.path.join(_ROOT, 'skills', 'agents-md-guard', 'cline_guard.py'),
         os.path.join(_HERE, 'cline_outside.py'))
BLOCK = {'cancel': True, 'contextModification': '',
         'errorMessage': 'Cline hook chain failed; operation blocked.'}


def main():
    raw = sys.stdin.buffer.read()
    result = BLOCK
    for script in STEPS:
        try:
            proc = subprocess.run([sys.executable, '-B', script], input=raw,
                                  capture_output=True, timeout=20)
            result = json.loads(proc.stdout.decode('utf-8'))
            if proc.returncode != 0 or not isinstance(result, dict) or not isinstance(result.get('cancel'), bool):
                raise ValueError('invalid guard result')
        except Exception:
            result = BLOCK
        if result['cancel']:
            break
    print(json.dumps(result, ensure_ascii=True), flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
