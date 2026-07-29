# ============================================================
# nra_ide_demo14_powergrid_26-0321.py
# NRA-IDE Demo #14 — Power Grid Transition
# 電力系統 遷移点解析
#
# Author: M-Tokuni / NRA-IDE Project
# https://github.com/M-Tokun/NRA-IDE
#
# 依存: nra_ide_core_base_2026-03-21.py（同ディレクトリに置く）
#
# 単体実行:
#   python nra_ide_demo14_powergrid_2026-03-21.py
#
# このファイルが扱うもの:
#   - 電力系統の周波数偏差 δf を Cause-Side として観測
#   - R = δf / τ で構造的接近比を計算
#   - 二重ゆらぎ（micro + macro + spike）の物理モデル
#   - 発電機脱落・需要急増イベントの構造的影響
#   - RUPTURE_BOUNDARY は同一履歴内で解除せず、後続は新評価履歴として開始
# ============================================================

import math
import random
import importlib.util
import sys
from pathlib import Path
from typing import List

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_CORE_PATH = Path(__file__).with_name("nra_ide_core_base_2026-03-21.py")
_CORE_SPEC = importlib.util.spec_from_file_location("nra_ide_core_base", _CORE_PATH)
if _CORE_SPEC is None or _CORE_SPEC.loader is None:
    raise ImportError(f"Cannot load NRA-IDE core base from {_CORE_PATH}")
_CORE = importlib.util.module_from_spec(_CORE_SPEC)
_CORE_SPEC.loader.exec_module(_CORE)

FSMState = _CORE.FSMState
NRAChannel = _CORE.NRAChannel
NRASystemState = _CORE.NRASystemState


# ============================================================
# 電力グリッド NRA エンジン
# ============================================================

class PowerGridNRA:
    """
    Demo #14 物理エンジン

    電力系統の周波数偏差を Cause-Side として観測し、
    R = δf / τ から構造的遷移点への接近を計算する。

    設計原則:
      - τ は系統慣性エネルギーに基づく設計値（スライダーで調整可）
      - δ = |f_current - 50.0Hz|
      - residual_debt: スパイク後も消えない構造的負債
      - RUPTURE_BOUNDARY 後は start_new_evaluation() で独立した新履歴を開始

    Parameters
    ----------
    tau : 吸収厚み τ（デフォルト 0.50）
    """

    F_NOM       = 50.0   # 定格周波数 [Hz]
    K_RECOVERY  = 0.12   # スプリング復元係数

    # FSM 遷移閾値
    TH_CAVEAT      = 0.40
    TH_RUPTURE_BOUNDARY = 1.00

    def __init__(self, tau: float = 0.50):
        self.channel = NRAChannel(
            name="freq",
            tau=tau,
            baseline=self.F_NOM,
            value=self.F_NOM,
        )
        self.freq          = self.F_NOM
        self.residual_debt = 0.0
        self.fsm           = FSMState.PERMIT
        self.elapsed       = 0.0

        # イベント状態（Cause-Side のみ）
        self._trip_decay:  float = 0.0
        self._surge_decay: float = 0.0
        self._recover:     bool  = False

        # 出力ログ
        self.history: List[dict] = []
        self.archived_histories: List[dict] = []

    # ── プロパティ ──

    @property
    def tau(self) -> float:
        return self.channel.tau

    @tau.setter
    def tau(self, v: float):
        self.channel.tau = v

    @property
    def R(self) -> float:
        return self.channel.R

    # ── メインステップ ──

    def step(self, dt: float = 0.016) -> NRASystemState:
        """
        物理を1ステップ進める。

        Parameters
        ----------
        dt : タイムステップ [秒]

        Returns
        -------
        NRASystemState : 現在の構造状態スナップショット
        """
        self.elapsed += dt

        # 二重ゆらぎ生成（Cause-Side 物理ノイズ）
        micro = (random.random() - 0.5) * 0.006 \
              + math.sin(self.elapsed * 3.7) * 0.008
        macro = math.sin(self.elapsed * 0.30) * 0.040 \
              + math.sin(self.elapsed * 0.17) * 0.025

        # イベントδ減衰
        event_delta = 0.0
        if self._trip_decay > 0:
            self._trip_decay = max(0.0, self._trip_decay - dt * 0.4)
            event_delta += self._trip_decay * 0.8
        if self._surge_decay > 0:
            self._surge_decay = max(0.0, self._surge_decay - dt * 0.25)
            event_delta += self._surge_decay * 0.5

        # 復旧力（人間操作で有効化）
        recover_force = 0.35 * dt if self._recover else 0.0

        # δ合成
        raw_delta = micro + macro + event_delta
        delta = max(0.0,
            abs(raw_delta) - recover_force
        ) * math.copysign(1.0, raw_delta + 1e-9)

        # 周波数更新
        self.freq = max(47.0, min(53.0, self.F_NOM - delta * 4.0))

        # R 計算（Cause-Side）
        self.channel.compute_R(self.freq)

        # 残留負債更新
        if self.R > self.TH_CAVEAT:
            self.residual_debt += (
                self.R - self.R * self.K_RECOVERY
            ) * dt * 0.08
        else:
            self.residual_debt = max(0.0, self.residual_debt - dt * 0.03)
        self.residual_debt = min(self.residual_debt, 2.0)

        # FSM 遷移
        self._update_fsm()

        # ログ記録
        self.history.append({
            "t":    round(self.elapsed, 3),
            "freq": round(self.freq, 4),
            "delta": round(self.channel.delta, 5),
            "R":    round(self.R, 5),
            "debt": round(self.residual_debt, 5),
            "fsm":  self.fsm.value,
        })

        return NRASystemState(
            fsm=self.fsm,
            R_total=self.R,
            residual_debt=self.residual_debt,
            elapsed=self.elapsed,
        )

    def _update_fsm(self):
        """FSM 遷移ロジック（組み合わせ回路相当）"""
        if self.fsm == FSMState.RUPTURE_BOUNDARY:
            return
        if self._recover and self.R < 0.8:
            self.fsm = FSMState.CRITICAL
            return

        if self.R >= self.TH_RUPTURE_BOUNDARY or self.residual_debt > 0.8:
            self.fsm = FSMState.RUPTURE_BOUNDARY
        elif self.R >= self.TH_CAVEAT:
            self.fsm = FSMState.CAVEAT
        else:
            self.fsm = FSMState.PERMIT

    # ── イベントトリガー（Cause-Side 入力）──

    def trigger_trip(self, magnitude: float = 1.2):
        """
        発電機脱落イベント。
        周波数偏差 δ を急増させる（Cause-Side）。
        RUPTURE_BOUNDARY 中は受け付けない。
        """
        if self.fsm == FSMState.RUPTURE_BOUNDARY:
            return
        self._trip_decay = magnitude + random.random() * 0.8

    def trigger_surge(self, magnitude: float = 0.9):
        """
        需要急増イベント。
        """
        if self.fsm == FSMState.RUPTURE_BOUNDARY:
            return
        self._surge_decay = magnitude + random.random() * 0.6

    def start_new_evaluation(self):
        """
        系統再検査後、独立した新しい評価履歴を開始する。
        旧RUPTURE_BOUNDARYを解除せず、新しいCause-Side履歴を生成する。
        """
        tau = self.tau
        archives = list(self.archived_histories)
        archives.append(
            {
                "final_state": self.fsm.value,
                "final_R": self.R,
                "history": list(self.history),
            }
        )
        self.__init__(tau)
        self.archived_histories = archives

    def reset(self):
        """独立した新評価履歴を開始する後方互換入口。"""
        self.start_new_evaluation()


# ============================================================
# CLI 実行
# ============================================================

def main():
    print("=" * 65)
    print("NRA-IDE Demo #14 — Power Grid Transition (Python Core)")
    print("電力系統 遷移点解析")
    print("=" * 65)
    print(f"F_nom = {PowerGridNRA.F_NOM} Hz  |  τ = 0.50  |  RUPTURE_BOUNDARY 閾値 R ≥ 1.00")
    print()

    grid = PowerGridNRA(tau=0.50)

    events = {
        80:  ("trigger_trip",    "⚡ 発電機脱落"),
        200: ("trigger_surge",   "📈 需要急増"),
        350: ("start_new_evaluation", "🔄 系統再検査後の新評価開始"),
    }
    prev_fsm = grid.fsm

    for i in range(500):
        # イベント発火
        if i in events:
            method, label = events[i]
            getattr(grid, method)()
            print(f"  [{grid.elapsed:6.2f}s] *** {label} ***")

        state = grid.step(dt=0.05)

        # FSM 遷移を表示
        if state.fsm != prev_fsm:
            print(
                f"  [{state.elapsed:6.2f}s]  遷移: {prev_fsm.value:12s}"
                f" → {state.fsm.value:12s}  R={state.R_total:.4f}"
            )
            prev_fsm = state.fsm

        # 定期表示
        if i % 50 == 0:
            print(
                f"  t={state.elapsed:6.2f}s |"
                f" f={grid.freq:7.3f}Hz |"
                f" R={state.R_total:.4f} |"
                f" debt={state.residual_debt:.4f} |"
                f" {state.fsm.value}"
            )

    print()
    print("=== 構造設計のポイント ===")
    print("  residual_debt: スパイク後も消えない構造的負債")
    print("  RUPTURE_BOUNDARY : 同一履歴では解除せず、start_new_evaluation()で新履歴を開始")
    print("  波形が正常に見えても debt が残れば構造は回復していない")


if __name__ == "__main__":
    main()
