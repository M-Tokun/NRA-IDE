"""Current threshold gate backed by the shared canonical adapter.

The old four-level state machine is preserved only in the legacy archive.
"""
from pathlib import Path
import sys

# Resolve the repository root so direct script execution also shares one model.
root = str(Path(__file__).resolve().parents[2])
if root not in sys.path:
    sys.path.insert(0, root)
from gate._canonical_threshold import ThresholdGuardian, SafetyAction, SafetyStatus

__all__ = ['ThresholdGuardian', 'SafetyAction', 'SafetyStatus']

if __name__ == '__main__':
    print(ThresholdGuardian().evaluate(0.1, 1.0, timestamp='DEMO_T0').as_dict())
