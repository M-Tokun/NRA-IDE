# BioDynamic_IDE_Engine_v2_20260406_1947.py
# title: NRA-IDE Hybrid Engine v2 - Complete Implementation
# Author: M-Tokuni / NRA-IDE Project https://github.com/M-Tokun/NRA-IDE
# Generated: 2026-04-06 19:47 JST
#Directory　note/
# 設計原則:
#   - IDE基点は常に保持・根本は譲らない
#   - 古典計算は補助（摂動）であり上書き禁止
#   - 2次残差ゲートにより数学構造自体がフィルターとして機能
#   - selfをJIT静的引数に渡さない（再コンパイル爆発の回避）

import numpy as np
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Callable, Optional, Tuple, List


# ─────────────────────────────────────────────
# 設定クラス
# ─────────────────────────────────────────────

@dataclass
class HybridConfig:
    """
    全パラメータの一元管理。
    ハードコード値はここにのみ存在する。
    """
    num_nodes: int

    # 時間積分
    dt: float = 0.05
    velocity_damping: float = 0.9

    # IDE大局流
    ide_damping: float = 0.5
    ide_nonlinear_amp: float = 0.2

    # ホットスポット検出（第一段：古典を呼ぶ門番）
    hotspot_threshold: float = 1.5

    # ソフト結合（チャタリング防止）
    softness_beta: float = 5.0

    # 残差ゲート（第二段：古典の発言強度調整）
    residual_knee: float = 1.0          # 典型残差の中央値付近に設定する
    resonance_coupling: float = 1.0
    resonance_epsilon: float = 0.01     # coupling_weight < epsilon は無視

    # 再現性
    random_seed: Optional[int] = 42

    # 履歴
    save_history: bool = True
    history_length: int = 1000


# ─────────────────────────────────────────────
# ゲート関数（純粋関数として独立）
# ─────────────────────────────────────────────

def quadratic_residual_gate(
    correction: np.ndarray,
    knee: float
) -> np.ndarray:
    """
    2次残差ゲート（核心式）

        G(r) = r * |r| / (k + |r|)

    |r| << k → G ≈ 0   小ゆらぎは自然消滅
    |r| >> k → G ≈ r   大逸脱は飽和応答で強調
    εカットオフ不要。数学構造自体がフィルター。
    """
    abs_r = np.abs(correction)
    ratio = abs_r / (knee + abs_r)       # 0〜1に正規化（発散防止）
    return correction * ratio


def soft_coupling_weights(
    state: np.ndarray,
    threshold: float,
    beta: float
) -> np.ndarray:
    """
    ソフト閾値結合重み

        w(x) = 0.5 * (1 + tanh(β(|x| - x_c)))

    バイナリマスクの代替。チャタリング防止。
    JAX自動微分との親和性確保（連続・微分可能）。
    """
    return 0.5 * (1.0 + np.tanh(beta * (np.abs(state) - threshold)))


# ─────────────────────────────────────────────
# メインエンジン
# ─────────────────────────────────────────────

class BioDynamic_IDE_Engine:
    """
    NRA-IDE 生命動態維持型ハイブリッドシミュレータ v2

    設計の三原則:
        1. IDE基点は常に全域で動作し続ける（根本を譲らない）
        2. 古典計算は有意ノードのみに呼ばれ、ズレだけを返す（上書き禁止）
        3. 2次残差ゲートが補正強度を自動決定する（人工的カットオフ不要）
    """

    def __init__(self, config: HybridConfig):
        self.config = config

        if config.random_seed is not None:
            np.random.seed(config.random_seed)

        self.state    = np.random.normal(0.0, 1.0, config.num_nodes)
        self.velocity = np.zeros(config.num_nodes)

        # 履歴
        self._state_history:    List[np.ndarray] = []
        self._hotspot_history:  List[int]         = []

        # 差し替え可能な関数（デフォルト注入済み）
        self._ide_flow_func:      Callable[[np.ndarray], np.ndarray] = self._default_ide_flow
        self._local_exact_solver: Callable[[np.ndarray], np.ndarray] = self._default_local_exact

    # ── デフォルト関数 ──────────────────────────

    def _default_ide_flow(self, state: np.ndarray) -> np.ndarray:
        """
        大局的IDE流（システムの「呼吸」）
        非線形減衰 + 正弦波相互作用
        """
        c = self.config
        return -c.ide_damping * state + c.ide_nonlinear_amp * np.sin(state * np.pi)

    def _default_local_exact(self, sub_state: np.ndarray) -> np.ndarray:
        """
        局所厳密解（デフォルト）
        実用時はここに PySCF・Qiskit 等の本物のソルバを注入する。
        """
        return np.tanh(sub_state * 1.5)

    # ── 外部注入 API ────────────────────────────

    def set_ide_flow(self, func: Callable[[np.ndarray], np.ndarray]) -> None:
        """IDE大局流を独自実装に差し替える"""
        self._ide_flow_func = func

    def set_local_exact_solver(self, func: Callable[[np.ndarray], np.ndarray]) -> None:
        """
        局所厳密解を本物のソルバに差し替える。
        入力: 有意ノードの部分状態ベクトル（サイズ可変）
        出力: 同サイズの厳密解ベクトル
        ※ 全ノードではなく有意ノードのみが渡される点に注意。
        """
        self._local_exact_solver = func

    # ── コアステップ ────────────────────────────

    def step(self) -> Tuple[np.ndarray, int]:
        """
        1ステップ実行。時間的連続性を完全に保証する。

        処理順:
            1. IDE大局流（根本・全域・常時）
            2. ソフト結合重みによる有意ノード特定
            3. 有意ノードのみに局所厳密解を呼ぶ
            4. 2次残差ゲートで補正強度を自動決定
            5. 加速度合成（IDE + 補助）
            6. velocity経由の連続更新（直接上書き禁止）
            7. 粘性減衰（発散防止）
        """
        cfg = self.config

        # 1. IDE大局流（根本）
        global_flow = self._ide_flow_func(self.state)

        # 2. ソフト結合重み（全ノード、チャタリングなし）
        weights = soft_coupling_weights(
            self.state,
            threshold=cfg.hotspot_threshold,
            beta=cfg.softness_beta
        )

        # 3. 有意ノード特定（epsilon未満は計算コスト不要）
        significant_mask    = weights > cfg.resonance_epsilon
        significant_indices = np.where(significant_mask)[0]
        hotspot_count       = int(significant_mask.sum())

        # 4. 局所厳密補正（有意ノードのみ・ズレを返すだけ）
        resonance_force = np.zeros_like(self.state)

        if hotspot_count > 0:
            local_sub       = self.state[significant_indices]
            exact           = self._local_exact_solver(local_sub)
            raw_correction  = exact - local_sub                  # 上書きせず差分のみ

            # 2次残差ゲート：小ゆらぎ消滅・大逸脱強調
            gated = quadratic_residual_gate(raw_correction, knee=cfg.residual_knee)

            # 補正力として合成（上書き禁止）
            resonance_force[significant_indices] = (
                gated
                * weights[significant_indices]
                * cfg.resonance_coupling
            )

        # 5. 加速度合成
        acceleration = global_flow + resonance_force

        # 6. Verlet風連続更新
        self.velocity += acceleration * cfg.dt
        self.state    += self.velocity  * cfg.dt

        # 7. 粘性減衰
        self.velocity *= cfg.velocity_damping

        # 履歴記録
        if cfg.save_history:
            self._state_history.append(self.state.copy())
            self._hotspot_history.append(hotspot_count)
            if len(self._state_history) > cfg.history_length:
                self._state_history.pop(0)

        return self.state.copy(), hotspot_count

    # ── 一括実行 ────────────────────────────────

    def run(self, steps: int, verbose: bool = True) -> dict:
        """複数ステップ一括実行"""
        hotspot_counts = []

        for i in range(steps):
            _, count = self.step()
            hotspot_counts.append(count)

            if verbose and (i + 1) % max(1, steps // 10) == 0:
                print(
                    f"Step {i+1:6d}/{steps}"
                    f" | Hotspots: {count:4d}"
                    f" | State norm: {np.linalg.norm(self.state):.4f}"
                )

        hc = np.array(hotspot_counts)
        return {
            "final_state": self.state.copy(),
            "hotspot_stats": {
                "total_steps_with_hotspot": int((hc > 0).sum()),
                "hotspot_rate_pct":         float((hc > 0).mean() * 100),
                "max_hotspots":             int(hc.max()) if len(hc) else 0,
                "avg_hotspots":             float(hc.mean()),
            },
            "state_history":    np.array(self._state_history)   if self.config.save_history else None,
            "hotspot_history":  np.array(self._hotspot_history)  if self.config.save_history else None,
        }

    # ── チェックポイント ─────────────────────────

    def save_checkpoint(self, filepath: str) -> None:
        data = {
            "state":    self.state.tolist(),
            "velocity": self.velocity.tolist(),
            "history":  [a.tolist() for a in self._state_history],
            "config":   asdict(self.config),
        }
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Checkpoint saved: {filepath}")

    @classmethod
    def load_checkpoint(
        cls,
        filepath: str,
        override_config: Optional[HybridConfig] = None
    ) -> "BioDynamic_IDE_Engine":
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)

        config = override_config or HybridConfig(**data["config"])
        engine = cls(config)
        engine.state    = np.array(data["state"])
        engine.velocity = np.array(data["velocity"])
        engine._state_history = [np.array(a) for a in data.get("history", [])]
        print(f"✅ Checkpoint loaded: {filepath}")
        return engine


# ─────────────────────────────────────────────
# 使用例
# ─────────────────────────────────────────────

if __name__ == "__main__":

    config = HybridConfig(
        num_nodes         = 10_000,
        dt                = 0.05,
        hotspot_threshold = 1.5,
        residual_knee     = 0.8,    # IDEのみで100ステップ走らせて残差中央値を確認してから設定
        softness_beta     = 5.0,
        random_seed       = 42,
        save_history      = True,
    )

    engine = BioDynamic_IDE_Engine(config)

    # 本物の局所ソルバがあればここで注入
    # engine.set_local_exact_solver(my_quantum_local_solver)

    result = engine.run(steps=2000, verbose=True)

    print("\n=== Simulation Complete ===")
    print(f"Final state norm    : {np.linalg.norm(result['final_state']):.4f}")
    print(f"Hotspot rate        : {result['hotspot_stats']['hotspot_rate_pct']:.2f}%")
    print(f"Max hotspots/step   : {result['hotspot_stats']['max_hotspots']}")

    engine.save_checkpoint("checkpoints/hybrid_v2_2000steps.json")

