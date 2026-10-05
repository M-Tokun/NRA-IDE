#!/usr/bin/env python
"""Load the full contract for Cline TaskStart/TaskResume."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cline_adapter

def main():
    return cline_adapter.run_task_start()

if __name__ == '__main__':
    sys.exit(main())
