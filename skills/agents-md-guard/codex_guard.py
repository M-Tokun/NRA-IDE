#!/usr/bin/env python
"""codex: shared guard logic with host-specific decision output."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common


def main():
    return _common.run_guard("codex")


if __name__ == "__main__":
    sys.exit(main())
