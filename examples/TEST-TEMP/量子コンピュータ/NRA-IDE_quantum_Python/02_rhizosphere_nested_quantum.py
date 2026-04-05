# FILE: 02_rhizosphere_nested_quantum.py
# TITLE: 複数層ネスト根圏シミュレーション（RhizosphereLayerクラス）
# Author: M-Tokuni / Comment: KEN
# Date: 2026-03-28
# 概要：各層が独立にR_quantumを計算し、子層の位相跳躍が親層にフィードバック。
#       数百層も children リストを再帰的に追加するだけで対応可能。

import numpy as np
from qutip import basis, sigmaz, sigmax, mesolve, expect
import matplotlib.pyplot as plt
from typing import Dict, List


# ─────────────────────────────────────────────
# 根圏1層を表すクラス
# is_quantum_layer=True の層だけ qutip で量子計算する
# 残りは古典ゆらぎ（乱数）で軽量に扱う
# ─────────────────────────────────────────────
class RhizosphereLayer:
    def __init__(
        self,
        layer_id: str,
        is_quantum_layer: bool = False,
        tau_base: float = 1.0,
        lambda_q: float = 0.8,
        alpha_u: float = 0.3,
        alpha_l: float = 0.3,
        alpha_q: float = 0.2,
        R_op: float = 1.2
    ):
        self.layer_id        = layer_id
        self.is_quantum_layer = is_quantum_layer
        self.tau_base        = tau_base
        self.lambda_q        = lambda_q
        self.alpha_u         = alpha_u
        self.alpha_l         = alpha_l
        self.alpha_q         = alpha_q
        self.R_op            = R_op
        self.eps             = 1e-9

        # 各層が持つ動的状態（律環 DynamicState 相当）
        self.delta1_upper    = 0.1
        self.delta1_lower    = 0.05
        self.delta2_coherence = 0.3
        self.ema_upper       = 0.0
        self.ema_lower       = 0.0
        self.ema_q           = 0.0
        self.R_quantum       = 0.0
        self.phi             = 0       # 位相跳躍カウンタ
        self.status          = "initial"

        # 量子状態（quantum_layer のみ使用。基底状態 |0⟩ で初期化）
        self.psi = basis(2, 0) if is_quantum_layer else None

        # 子層リスト（ここに追加するだけで階層が深くなる）
        self.children: List['RhizosphereLayer'] = []

        # 履歴（可視化用）
        self.history: List[Dict] = []

    # ─────────────────────────────────────────
    # 2重ゆらぎ計算：EMA → 動的τ → R_quantum → 状態判定
    # ─────────────────────────────────────────
    def compute_quantum_dual_fluctuation(self, delta2_input: float = None) -> Dict:
        d2 = delta2_input if delta2_input is not None else self.delta2_coherence

        # EMA 更新
        self.ema_upper = self.alpha_u * self.delta1_upper + (1 - self.alpha_u) * self.ema_upper
        self.ema_lower = self.alpha_l * self.delta1_lower + (1 - self.alpha_l) * self.ema_lower
        self.ema_q     = self.alpha_q * d2 + (1 - self.alpha_q) * self.ema_q

        # 動的τ（非対称）
        tau_upper = self.tau_base * (1 + 0.5 * self.ema_upper)
        tau_lower = self.tau_base * max(0.5, 1 - 0.3 * self.ema_lower)
        tau_q     = self.tau_base * (1 + 0.4 * self.ema_q)

        # 干渉項・R 計算
        interference  = d2 ** 2
        r_upper       = self.delta1_upper / tau_upper
        r_lower       = self.delta1_lower / tau_lower
        r_q           = (d2 + self.lambda_q * interference) / tau_q
        self.R_quantum = max(r_upper, r_lower, r_q)

        # 状態判定
        if self.R_quantum < 1.0 - self.eps:
            self.status = "coherence_accumulating"
            phi_next    = None
            delta_next  = {"delta1_upper": self.delta1_upper + 0.01, "delta2": self.delta2_coherence}
        elif self.R_quantum >= 1.0:
            self.status = "phase_jump_generated"
            self.phi   += 1
            phi_next    = self.phi
            delta_next  = {"delta1_upper": 0.0, "delta2": 0.0}
            print(f"【位相跳躍発生！ layer={self.layer_id} phi={phi_next}】 → 親層へエネルギー転移")
        else:
            self.status = "transition_band"
            phi_next    = None
            delta_next  = {"delta1_upper": max(0, self.delta1_upper - tau_upper), "delta2": self.delta2_coherence}

        self.delta1_upper     = delta_next["delta1_upper"]
        self.delta2_coherence = delta_next["delta2"]
        return {"R_quantum": self.R_quantum, "status": self.status, "phi": phi_next}

    # ─────────────────────────────────────────
    # 1ステップ処理（自層 → 子層 → 子層の跳躍を親層にフィードバック）
    # ─────────────────────────────────────────
    def simulate_step(self, dt: float = 0.1, step: int = 0):
        # 量子層：qutip で時間発展してδ2を更新
        if self.is_quantum_layer and self.psi is not None:
            H0 = 2 * np.pi * sigmax()
            def H_t(t, args):
                return H0 + args.get('delta1', 0.0) * np.sin(2 * np.pi * t) * sigmaz()
            result = mesolve(H_t, self.psi, [0, dt], [], e_ops=[expect(sigmaz())],
                             args={'delta1': self.delta1_upper})
            coherence             = abs(result.states[-1].overlap(basis(2, 0))) ** 2
            self.delta2_coherence = coherence + 0.05 * np.random.randn()
            self.psi              = result.states[-1]
        else:
            # 古典層：乱数で土壌・肥料・微生物拮抗を簡易模擬
            self.delta1_upper     += 0.02 * np.random.randn()
            self.delta1_lower     += 0.01 * np.random.randn()
            self.delta2_coherence += 0.03 * np.random.randn()

        # 自層の2重ゆらぎ計算
        state = self.compute_quantum_dual_fluctuation()

        # 子層を再帰処理し、跳躍数を集計
        child_jumps = 0
        for child in self.children:
            child.simulate_step(dt, step)
            if child.status == "phase_jump_generated":
                child_jumps += 1
                # 子層の跳躍エネルギーを親層のδ1に加算（環の閉じ）
                self.delta1_upper += 0.15

        # 履歴に記録
        self.history.append({
            "step":        step,
            "layer_id":    self.layer_id,
            "R_quantum":   self.R_quantum,
            "status":      self.status,
            "phi":         self.phi,
            "coherence":   self.delta2_coherence,
            "child_jumps": child_jumps
        })


# ─────────────────────────────────────────────
# 根圏ツリー構築（3層ネスト例）
# 数百層に拡張したい場合：children.append() をループで追加するだけ
# ─────────────────────────────────────────────
def build_rhizosphere_tree() -> RhizosphereLayer:
    root            = RhizosphereLayer("Soil_Macro",              is_quantum_layer=False, tau_base=1.2)
    microbe_cluster = RhizosphereLayer("Microbe_Cluster_47",      is_quantum_layer=False, tau_base=0.9)
    quantum_electron = RhizosphereLayer("Quantum_Electron_Transfer", is_quantum_layer=True,  tau_base=0.7)

    microbe_cluster.children.append(quantum_electron)
    root.children.append(microbe_cluster)

    # 数百層への拡張例（コメントアウト）：
    # for i in range(100):
    #     root.children.append(RhizosphereLayer(f"Microbe_Sub_{i}", is_quantum_layer=False))

    return root


# ─────────────────────────────────────────────
# 全層の履歴をフラットに収集するヘルパー
# ─────────────────────────────────────────────
def collect_history(layer: RhizosphereLayer) -> list:
    result = list(layer.history)
    for child in layer.children:
        result.extend(collect_history(child))
    return result


# ─────────────────────────────────────────────
# 実行・可視化
# ─────────────────────────────────────────────
if __name__ == "__main__":
    np.random.seed(42)
    root_layer = build_rhizosphere_tree()

    print("=== 律環公理 複数層ネスト根圏シミュレーション開始 ===")
    for step in range(30):
        root_layer.simulate_step(dt=0.1, step=step)

    all_history = collect_history(root_layer)

    # ログ表示（最初の50行）
    for h in all_history[:50]:
        print(f"step {h['step']:2d} | layer={h['layer_id']:25s} | "
              f"R={h['R_quantum']:.3f} | {h['status'][:14]} | phi={h['phi']}")

    # グラフ：3層の R_quantum 時系列比較
    plt.figure(figsize=(12, 6))
    for lid in ["Soil_Macro", "Microbe_Cluster_47", "Quantum_Electron_Transfer"]:
        lh    = [h for h in all_history if h["layer_id"] == lid]
        steps = [h["step"]      for h in lh]
        Rs    = [h["R_quantum"] for h in lh]
        plt.plot(steps, Rs, label=f'{lid}', marker='o', markersize=3)

    plt.axhline(1.0, color='r', linestyle='--', label='位相跳躍閾値')
    plt.xlabel('時間ステップ（根圏ストレス蓄積）')
    plt.ylabel('R_quantum（構造安定度）')
    plt.title('律環公理 2重ゆらぎ量子拡張 × 複数層ネスト根圏シミュレーション')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
