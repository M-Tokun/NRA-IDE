"""
二重指数崩壊トレンド検知モジュール（プロトタイプ／NRA-IDE向け）

note/02_AI・ガバナンス検討/マルチエージェント相互汚染と人工データ汚染の数理的定式化と解法_20260819.md
第1章の r_t = r_0^(2^t) モデルに対する、実運用向けの検知器。

前バージョン（チャット上で提示された実装）に対して、レビューで確認した2つの問題を修正している。

【修正①：パラメータ較正】
 前バージョンは λ・μ・ν の重みが τ のスケールに対して過大で、健全な初期状態（世代0）
 でも R が 1.0 を超えて即座に RUPTURE_BOUNDARY へ飽和した（実測 R≈15）。
 本バージョンは、後述の Δℓ（対数二乗トレンド）に基づく蓄積則を採用し、
 デフォルト重みで PERMIT → BOUNDARY_WARNING → HANDOFF_REQUIRED → RUPTURE_BOUNDARY が
 4〜5世代かけて段階的に進行するよう較正してある（__main__ のシミュレーションで検証済み）。

【修正②：スナップショット判定からトレンド判定への変更】
 前バージョンの s_t = log2(log2(1/kappa)) は現在の kappa の値だけから計算される
 スナップショット量であり、p_0 に依存する較正定数を差し引いていないため、
 「もともと歪んだ比率のまま安定している系」と「今まさに崩壊が進行中の系」を
 区別できなかった（p_0=0.1 の健全な初期状態が、それだけで警告閾値に抵触する）。

 本バージョンは theory/AXIOMS.md §4.7 の二重ゆらぎ式（Secondary Formula）に倣い、
 連続する観測間の変化量 Δδ・Δτ に基づいてトレンドを判定する。
 蓄積ズレ δ は「観測が悪化した分」だけを加算し、吸収厚み τ は同じ悪化分だけを
 消耗する（τ の非自然回復原則、AXIOMS.md §7）。κ が一定（崩壊していない）系では
 δ・τ とも変化せず、R は低い水準に留まる。

数理的根拠：r_t = r_0^(2^t) のとき、厳密に
    ln(-ln(r_t)) = t * ln2 + ln(-ln(r_0))
が成り立つ（等比的に2倍で効く「対数の対数」表現）。したがって
    Δ[ln(-ln(r_t))] = ln(2)  （世代ごとに一定）
であり、この差分量は p_0 に依存する較正定数を含まない。これを κ（Cause-Side一致率、
p_t の直接代理量）に適用し、ℓ_t = ln(-ln(κ_t)) の差分 Δℓ_t を崩壊トレンドの
一次観測量として δ・τ の更新に用いる。

正典上の位置づけ：ここで用いる δ・τ の算定規則は、いずれも `theory/AXIOMS.md` §15.1が
要求する「領域固有の派生式」であり、律環公理・IDE一次式・二次式そのものではない。
R = δ/τ の算出と境界順序（PERMIT/BOUNDARY_WARNING/HANDOFF_REQUIRED/
IRREVERSIBLE_TRANSITION/RUPTURE_BOUNDARY）の判定だけが正典の権威区分に従う。
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional


# ---------------------------------------------------------------------------
# 設定
# ---------------------------------------------------------------------------

@dataclass
class CollapseConfig:
    """検知パラメータ（領域固有の派生式のパラメータであり、正典の定数ではない）"""

    # Δℓ（対数二乗トレンド）1単位あたりの δ 加算量
    w_delta: float = 0.3
    # Δℓ 1単位あたりの τ 消耗量（AXIOMS.md §7：非自然回復原則）
    w_tau: float = 0.1

    delta_base: float = 0.02   # 基礎蓄積ズレ（対話回数・ノイズ等、崩壊トレンドと無関係の分）
    tau0: float = 1.0          # 初期吸収厚み

    # 境界閾値（現場ごとに変更してよい値。ただし順序 0<=warn<handoff<irrev<1.0 は必須）
    R_warn: float = 0.25
    R_handoff: float = 0.55
    R_irrev: float = 0.80

    # R_rupture はこのクラスの外で 1.0 に固定する（AXIOMS.md §15.3：現場ごとに変更してはならない項目）

    eps: float = 1e-12

    def __post_init__(self):
        if not (0 <= self.R_warn < self.R_handoff < self.R_irrev < 1.0):
            raise ValueError(
                "正典の境界順序 0<=R_warn<R_handoff<R_irrev<1.0 を満たしていません"
            )


R_RUPTURE = 1.0  # 正典固定値。CollapseConfig のフィールドにはしない。


# ---------------------------------------------------------------------------
# 観測・結果
# ---------------------------------------------------------------------------

@dataclass
class Observation:
    """1回の観測ウィンドウ（世代である必要はなく、任意のサンプリング間隔でよい）"""

    kappa: float                     # Cause-Side 一致率（p_t の直接代理量）[0,1]
    alpha: Optional[float] = None    # 自己整合性一致率（診断用途のみ。δには反映しない）
    label: Optional[str] = None      # 観測ラベル（世代番号・時刻など、表示用）
    source: str = "unspecified"      # 出所（監査用、AXIOMS.md §15.1 の要求に対応）


@dataclass
class DetectorResult:
    kappa: float
    alpha: Optional[float]
    label: Optional[str]

    d_ell: float                     # 今回の Δℓ（トレンド量）
    delta: float
    tau: float
    R: Optional[float]               # τ<=0 のときは None（OUT_OF_DESCRIPTION_DOMAIN）

    remaining_ratio_margin: Optional[float]      # M_R = 1 - R
    remaining_absorption_margin: Optional[float] # M_tau = tau - delta

    double_fluctuation: str          # "ACTIVE" | "NOT_ACTIVE" | "NOT_OBSERVABLE"
    state: str                       # 正規状態名 or CONFESSION / OUT_OF_DESCRIPTION_DOMAIN

    alpha_kappa_gap: Optional[float] # 診断専用。δには含めない。


# ---------------------------------------------------------------------------
# 検知器
# ---------------------------------------------------------------------------

class TrendCollapseDetector:
    """観測列から Δℓ トレンドを計算し、δ/τ/R を更新する検知器"""

    def __init__(self, config: Optional[CollapseConfig] = None):
        self.cfg = config or CollapseConfig()
        self.delta = self.cfg.delta_base
        self.tau = self.cfg.tau0
        self._prev_ell: Optional[float] = None
        self._prev_delta: Optional[float] = None
        self._prev_tau: Optional[float] = None
        self.history: List[DetectorResult] = []

    @staticmethod
    def _log_log(kappa: float, eps: float) -> Optional[float]:
        """ell = ln(-ln(kappa))。kappa >= 0.5 では崩壊トレンドの定義域外として None を返す。"""
        if kappa >= 0.5:
            return None
        k = max(kappa, eps)
        inner = -math.log(k)  # > 0 (because k < 0.5 < 1)
        if inner <= 0:
            return None
        return math.log(inner)

    def update(self, obs: Observation) -> DetectorResult:
        cfg = self.cfg

        # --- 入力妥当性検証（CONFESSION 経路） ---
        if obs.kappa is None or not (0.0 <= obs.kappa <= 1.0) or math.isnan(obs.kappa):
            result = DetectorResult(
                kappa=obs.kappa, alpha=obs.alpha, label=obs.label,
                d_ell=0.0, delta=self.delta, tau=self.tau, R=None,
                remaining_ratio_margin=None, remaining_absorption_margin=None,
                double_fluctuation="NOT_OBSERVABLE", state="CONFESSION",
                alpha_kappa_gap=None,
            )
            self.history.append(result)
            return result

        # --- Δℓ トレンドの計算 ---
        ell = self._log_log(obs.kappa, cfg.eps)
        if ell is None:
            d_ell = 0.0  # kappa>=0.5: 健全域。崩壊トレンドは観測されていない扱い。
        elif self._prev_ell is None:
            d_ell = 0.0  # 初回観測はトレンドを持たない（基準点）
        else:
            d_ell = max(0.0, ell - self._prev_ell)

        # --- delta 蓄積・tau 消耗（AXIOMS.md §7：非自然回復原則） ---
        self.delta = self.delta + cfg.w_delta * d_ell
        self.tau = self.tau - cfg.w_tau * d_ell

        # --- tau<=0 は OUT_OF_DESCRIPTION_DOMAIN（AXIOMS.md §6）。R を定義しない。 ---
        if self.tau <= 0:
            result = DetectorResult(
                kappa=obs.kappa, alpha=obs.alpha, label=obs.label,
                d_ell=d_ell, delta=self.delta, tau=self.tau, R=None,
                remaining_ratio_margin=None, remaining_absorption_margin=None,
                double_fluctuation="NOT_OBSERVABLE", state="OUT_OF_DESCRIPTION_DOMAIN",
                alpha_kappa_gap=None,
            )
            self.history.append(result)
            self._prev_ell = ell if ell is not None else self._prev_ell
            return result

        R = self.delta / self.tau
        state = self._decide_state(R)

        # --- 二重ゆらぎ検出（AXIOMS.md §4.7：離散差分規則） ---
        if self._prev_delta is None or self._prev_tau is None:
            fluctuation = "NOT_OBSERVABLE"  # 初回は差分が取れない
        else:
            d_delta = self.delta - self._prev_delta
            d_tau = self.tau - self._prev_tau
            fluctuation = "ACTIVE" if (d_delta > 0 and d_tau < 0) else "NOT_ACTIVE"

        gap = None
        if obs.alpha is not None:
            gap = max(0.0, obs.alpha - obs.kappa)

        result = DetectorResult(
            kappa=obs.kappa, alpha=obs.alpha, label=obs.label,
            d_ell=d_ell, delta=self.delta, tau=self.tau, R=R,
            remaining_ratio_margin=1.0 - R,
            remaining_absorption_margin=self.tau - self.delta,
            double_fluctuation=fluctuation, state=state,
            alpha_kappa_gap=gap,
        )

        self._prev_ell = ell if ell is not None else self._prev_ell
        self._prev_delta = self.delta
        self._prev_tau = self.tau
        self.history.append(result)
        return result

    def _decide_state(self, R: float) -> str:
        cfg = self.cfg
        if R >= R_RUPTURE:
            return "RUPTURE_BOUNDARY"
        if R >= cfg.R_irrev:
            return "IRREVERSIBLE_TRANSITION"
        if R >= cfg.R_handoff:
            return "HANDOFF_REQUIRED"
        if R >= cfg.R_warn:
            return "BOUNDARY_WARNING"
        return "PERMIT"

    def print_table(self) -> None:
        header = f"{'label':>6} | {'kappa':>12} | {'d_ell':>6} | {'delta':>7} | {'tau':>7} | {'R':>8} | {'fluct':>12} | state"
        print(header)
        print("-" * len(header))
        for r in self.history:
            R_str = f"{r.R:.4f}" if r.R is not None else "undef"
            print(
                f"{str(r.label):>6} | {r.kappa:>12.4e} | {r.d_ell:>6.4f} | "
                f"{r.delta:>7.4f} | {r.tau:>7.4f} | {R_str:>8} | {r.double_fluctuation:>12} | {r.state}"
            )


# ---------------------------------------------------------------------------
# デモ／検証
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== シナリオA：論文の 1:9 崩壊系列（実際に崩壊が進行中） ===\n")
    kappas_collapsing = [0.10, 0.0121951, 0.00015239, 2.3231e-8, 5.397e-16, 1e-20]
    det_a = TrendCollapseDetector(CollapseConfig())
    for i, k in enumerate(kappas_collapsing):
        det_a.update(Observation(kappa=k, alpha=min(0.999, k + 0.7), label=f"gen{i}"))
    det_a.print_table()

    print("\n=== シナリオB：p0=0.1 のまま安定している系（崩壊していない） ===")
    print("（修正②の検証：レビューで指摘した誤検知が解消されているか）\n")
    det_b = TrendCollapseDetector(CollapseConfig())
    for i in range(6):
        det_b.update(Observation(kappa=0.10, alpha=0.80, label=f"t{i}"))
    det_b.print_table()

    final_state_b = det_b.history[-1].state
    assert final_state_b == "PERMIT", (
        f"回帰検知: 安定系が誤って {final_state_b} と判定されました。"
        "スナップショット判定への先祖返りの可能性があります。"
    )
    print(f"\n[検証OK] κ=0.10 のまま6回観測しても state={final_state_b} のまま "
          f"（誤警報なし。R={det_b.history[-1].R:.4f}）")
