# ============================================================
# nra_ide_core_base_26-0321.py
# NRA-IDE 共通基盤定義
# Author: M-Tokuni / NRA-IDE Project
# https://github.com/M-Tokun/NRA-IDE
#
# このファイルは Demo #14 / Demo #15 の両方が import する。
# 単体で実行しても動作確認ができる。
# ============================================================

import math
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# ============================================================
# FSM状態定義
# ============================================================

class FSMState(Enum):
    """
    NRA-IDE ゲートFSM状態
    WARMUP → PERMIT → CAVEAT → CRITICAL → RUPTURE_BOUNDARY

    RUPTURE_BOUNDARY は同一履歴内で解除しない。
    後続処理は、独立した新対象・新Cause-Side履歴として開始する。
    """
    WARMUP      = "WARMUP"       # τ未確立（経過なし・新患相当）
    PERMIT      = "PERMIT"       # R < 0.35〜0.40 　安定
    CAVEAT      = "CAVEAT"       # 0.35〜0.40 ≤ R < 0.60  警告
    CRITICAL    = "CRITICAL"     # 0.60 ≤ R < 1.00  臨界接近
    RUPTURE_BOUNDARY = "RUPTURE_BOUNDARY"  # R_target ≥ 1.00 → 破断後固定証言


# ============================================================
# 単一チャンネル R 計算ユニット
# ============================================================

@dataclass
class NRAChannel:
    """
    単一チャンネルの δ / τ / R 計算ユニット

    R = δ / τ  (Cause-Side のみ)

    Π⁻¹禁止: Effect-Side（結果値）からτへの逆流は構造的に禁止。
    τは設計時固定の規則に従い設定する。値のみ観測経過で確立する。

    Parameters
    ----------
    name     : チャンネル名（例: "hr", "freq"）
    tau      : 吸収厚み（設計時固定）。0 の場合はウォームアップ中。
    baseline : 自己ベースライン（観測開始時に確立）
    """
    name:     str
    tau:      float
    baseline: float
    value:    float = 0.0
    delta:    float = 0.0
    R:        float = 0.0

    def compute_R(self, current_value: float) -> float:
        """
        現在値を受け取り R を計算して返す。
        τ = 0（ウォームアップ中）の場合は R = 0 を返す。
        """
        self.value = current_value
        self.delta = abs(current_value - self.baseline)
        if self.tau <= 0.0:
            self.R = 0.0
        else:
            self.R = self.delta / self.tau
        return self.R


# ============================================================
# システム状態スナップショット
# ============================================================

@dataclass
class NRASystemState:
    """
    step() が返す1ステップ分の構造状態スナップショット。
    ログ・表示・上位レイヤーへの受け渡しに使う。
    このオブジェクトはτを変更できない（Effect-Side保護）。
    """
    fsm:           FSMState = FSMState.WARMUP
    R_total:       float    = 0.0
    residual_debt: float    = 0.0
    warmup_pct:    float    = 0.0
    elapsed:       float    = 0.0


# ============================================================
# 動作確認
# ============================================================

if __name__ == "__main__":
    print("NRA-IDE Core Base — 動作確認")
    print()

    # NRAChannel 単体テスト
    ch = NRAChannel(name="hr", tau=18.0, baseline=72.0, value=72.0)
    print("=== NRAChannel ===")
    for v in [72, 80, 90, 100, 110]:
        r = ch.compute_R(v)
        zone = ("FAIL" if r >= 1.0 else "CAVEAT" if r >= 0.4 else "PERMIT")
        print(f"  HR={v:3d}  δ={ch.delta:5.1f}  R={r:.4f}  [{zone}]")

    print()

    # FSMState 遷移確認
    print("=== FSMState ===")
    for s in FSMState:
        print(f"  {s.value}")
