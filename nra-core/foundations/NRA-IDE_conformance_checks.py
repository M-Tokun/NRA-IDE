"""NRA-IDE解説文書の検証済みリファレンス実装（このファイル自体を実行/importすること）。

再実装しないこと。このファイルの目的は、AIや人間が
nra-core/foundations/NRA-IDE_律環公理とIDEのPython解説_2026-08-06.md 15章の主張を
「読んでから書き直す」ことによる劣化を防ぐことである。

使い方：
  python NRA-IDE_conformance_checks.py
  → 同じディレクトリの conformance_vectors.json を読み込み、全ケースを検証して終了コードを返す。

このファイルの関数・クラスを、名前だけを見て別実装に置き換えてはならない。
このファイルをそのまま import して呼び出すこと。
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Optional, Union


# ============================================================
# 3〜5章で定義したコアモデル（15.5節と同一。変更しないこと）
# ============================================================
@dataclass(frozen=True)
class CauseSideObservation:
    delta: float
    tau: float
    source: str
    timestamp: str

    def is_finite(self) -> bool:
        return (
            isinstance(self.delta, (int, float))
            and isinstance(self.tau, (int, float))
            and math.isfinite(self.delta)
            and math.isfinite(self.tau)
        )


class OutOfDescriptionDomain:
    def __init__(self, observation: CauseSideObservation):
        self.observation = observation


class Confession:
    def __init__(self, reason: str, observation: CauseSideObservation):
        self.reason = reason
        self.observation = observation


def compute_boundary_ratio(
    observation: CauseSideObservation,
) -> Union[float, OutOfDescriptionDomain, Confession]:
    if not observation.source or not observation.timestamp:
        return Confession("出所または時点が不明。類推で補ってはならない。", observation)

    if not observation.is_finite():
        return Confession("delta または tau が非有限。", observation)

    if observation.delta < 0.0 or observation.tau < 0.0:
        return Confession("delta は非負、tau は非負でなければならない。", observation)

    if observation.tau == 0.0:
        return OutOfDescriptionDomain(observation)

    return observation.delta / observation.tau


@dataclass(frozen=True)
class Thresholds:
    r_warn: float
    r_handoff: float
    r_irrev: float

    def __post_init__(self) -> None:
        if not (0.0 <= self.r_warn < self.r_handoff < self.r_irrev < 1.0):
            raise ValueError("0 <= R_warn < R_handoff < R_irrev < 1.0 を満たさない。")


@dataclass
class StructuralState:
    target: str
    irreversible_latched: bool = False


def classify_boundary_state(
    ratio: float,
    thresholds: Thresholds,
    state: StructuralState,
) -> str:
    if ratio >= 1.0:
        state.irreversible_latched = True
        return "RUPTURE_BOUNDARY"

    if state.irreversible_latched or ratio >= thresholds.r_irrev:
        state.irreversible_latched = True
        return "IRREVERSIBLE_TRANSITION"

    if ratio >= thresholds.r_handoff:
        return "HANDOFF_REQUIRED"

    if ratio >= thresholds.r_warn:
        return "BOUNDARY_WARNING"

    return "PERMIT"


# ============================================================
# JSON非有限値表記（"NaN" / "Infinity" / "-Infinity"）の変換
# conformance_vectors.json の non_finite_notation に対応。
# ============================================================
_NON_FINITE = {"NaN": float("nan"), "Infinity": float("inf"), "-Infinity": float("-inf")}


def _decode_value(value: Any) -> Any:
    if isinstance(value, str) and value in _NON_FINITE:
        return _NON_FINITE[value]
    return value


# ============================================================
# JSON駆動の検証本体。ここだけがJSONの構造を知っている。
# ============================================================
def verify_against_json(json_path: Path) -> bool:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    vectors = data["test_vectors"]
    th = vectors["thresholds"]
    all_ok = True

    def report(label: str, ok: bool, detail: str = "") -> None:
        nonlocal all_ok
        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] {label} {detail}")
        if not ok:
            all_ok = False

    # --- 有効ケース ---
    for case in vectors["valid_cases"]:
        thresholds = Thresholds(r_warn=th["r_warn"], r_handoff=th["r_handoff"], r_irrev=th["r_irrev"])
        state = StructuralState(target=f"valid_case_delta_{case['delta']}")
        observation = CauseSideObservation(
            delta=_decode_value(case["delta"]),
            tau=_decode_value(case["tau"]),
            source="conformance_test",
            timestamp="t",
        )
        ratio = compute_boundary_ratio(observation)
        ok = isinstance(ratio, float) and math.isclose(ratio, case["expected_R"], rel_tol=1e-9)
        actual_state = classify_boundary_state(ratio, thresholds, state) if isinstance(ratio, float) else None
        ok = ok and actual_state == case["expected_state"]
        report(f"valid_case delta={case['delta']}", ok, f"got_state={actual_state}")

    # --- 不可逆ラッチの永続性（1つのStructuralStateを使い回す） ---
    seq = vectors["latch_persistence_sequence"]
    thresholds = Thresholds(r_warn=th["r_warn"], r_handoff=th["r_handoff"], r_irrev=th["r_irrev"])
    latch_state = StructuralState(target="latch_persistence_sequence")
    for step in seq["steps"]:
        observation = CauseSideObservation(
            delta=_decode_value(step["delta"]), tau=_decode_value(step["tau"]),
            source="conformance_test", timestamp=f"step{step['step']}",
        )
        ratio = compute_boundary_ratio(observation)
        actual_state = classify_boundary_state(ratio, thresholds, latch_state)
        ok = actual_state == step["expected_state"]
        report(f"latch_step {step['step']} delta={step['delta']}", ok, f"R={ratio} got={actual_state}")

    # --- 計算不能な例 ---
    for case in vectors["impossible_cases"]:
        name = case["case"]

        if name == "threshold_order_violation":
            try:
                Thresholds(**case["thresholds"])
                report(name, False, "ValueErrorが発生しなかった")
            except ValueError:
                report(name, True)
            continue

        if name == "fabricated_parameter":
            try:
                CauseSideObservation(
                    delta=1.0, tau=10.0, source="s", timestamp="t",
                    **{case["attempted_kwarg"]: case["attempted_kwarg_value"]},
                )
                report(name, False, "TypeErrorが発生しなかった")
            except TypeError:
                report(name, True)
            continue

        observation = CauseSideObservation(
            delta=_decode_value(case["delta"]),
            tau=_decode_value(case["tau"]),
            source=case.get("source", "conformance_test"),
            timestamp="t",
        )
        result = compute_boundary_ratio(observation)
        actual_type = type(result).__name__ if not isinstance(result, float) else "float"
        ok = actual_type == case["expected_result_type"]
        report(name, ok, f"got={actual_type} expected={case['expected_result_type']}")

    return all_ok


if __name__ == "__main__":
    json_path = Path(__file__).with_name("NRA-IDE_律環公理とIDEのPython解説_conformance_vectors.json")
    success = verify_against_json(json_path)
    print()
    print("RESULT:", "ALL PASS" if success else "SOME FAILED")
    sys.exit(0 if success else 1)
