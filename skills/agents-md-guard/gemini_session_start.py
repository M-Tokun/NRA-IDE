#!/usr/bin/env python
"""gemini SessionStart: emit the full contract before recording its hash."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common


def main():
    return _common.run_session_start("gemini")


if __name__ == "__main__":
    sys.exit(main())
