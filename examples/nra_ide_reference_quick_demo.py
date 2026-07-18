"""Run canonical NRA-IDE states through the normative reference implementation.

This file is an executable example, not a separate canonical evaluator.
The thresholds are explicit demonstration values, not inferred domain defaults.
Do not use this demo for medical, autonomous-control, or other operational decisions.
"""

from __future__ import annotations

import importlib.util
import pathlib
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "nra-core" / "foundations" / "NRA-IDE_Architecture_public.py"
SPEC = importlib.util.spec_from_file_location("nra_ide_reference_quick_demo", SOURCE)
NRA = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(NRA)

THRESHOLDS = {
    "r_warn": 0.4,
    "r_handoff": 0.6,
    "r_irrev": 0.8,
}

SCENARIOS = (
    ("below warning", 0.1, 1.0, "PERMIT"),
    ("warning boundary", 0.4, 1.0, "BOUNDARY_WARNING"),
    ("human handoff", 0.6, 1.0, "HANDOFF_REQUIRED"),
    ("irreversible onset", 0.8, 1.0, "IRREVERSIBLE_TRANSITION"),
    ("complete rupture", 1.0, 1.0, "RUPTURE_BOUNDARY"),
    ("invalid structural input", "invalid", 1.0, "CONFESSION"),
    ("undefined ratio domain", 0.1, 0.0, "OUT_OF_DESCRIPTION_DOMAIN"),
)


def display_value(value: Any) -> str:
    return "NOT_AVAILABLE" if value is None else str(value)


def main() -> int:
    print("NRA-IDE normative reference quick demo")
    print("Thresholds are explicit demonstration values:", THRESHOLDS)
    print()

    passed = 0
    for name, delta, tau, expected in SCENARIOS:
        result = NRA.nra_ide_core_evaluation(delta, tau, **THRESHOLDS)
        actual = result["status"]
        outcome = "PASS" if actual == expected else "FAIL"
        passed += actual == expected
        print(
            f"{outcome:4} | {name:24} | delta={delta!r:9} | tau={tau!r:4} | "
            f"R={display_value(result['R']):13} | status={actual} | expected={expected}"
        )

    print()
    print(f"Scenarios passed: {passed}/{len(SCENARIOS)}")
    if passed == len(SCENARIOS):
        print("Quick demo result: OK")
        return 0
    print("Quick demo result: FAILED")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
