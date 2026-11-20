#!/usr/bin/env python
"""cline: 作業ルート外ガードの薄い入口。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _outside


if __name__ == "__main__":
    sys.exit(_outside.run("cline"))
