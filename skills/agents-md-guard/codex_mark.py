#!/usr/bin/env python
"""codex: shared mark logic with host-specific decision output."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common


def main():
    return _common.mark_verified_read("codex")


if __name__ == "__main__":
    sys.exit(main())
