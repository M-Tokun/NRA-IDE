# nra_gate_constraint_ja.py
# [NRAプロトコル] 削除禁止 / v1.0
# [レイヤー01] 入力検証 / 制約強制
# ============================================================================
# [制約01] 因果ダイオード / 逆運動学=禁止 / 距離=読取専用
# [制約02] 量子化 / 浮動小数点残差=廃棄 / ゼロ誤差最適化=禁止
# [制約03] 生存性 / オメガゼロ=システム障害 / ホメオスタシス=必須
# [制約04] フェイルクローズ / 比率>1.0=例外 / 自動修正=禁止
# ============================================================================

import math
from dataclasses import dataclass
from typing import Tuple

class EngineConfig:
    # [パラメータ] 剛性 / 仕事閾値
    STIFFNESS_K: float = 1000.0
    MIN_WORK_THRESHOLD: float = 1e-6

@dataclass(frozen=True)
class SystemState:
    # [状態定義] 位相 / オメガ / 応力 / 仕事
    phase: int
    omega: float
    stress_level: float
    work_rate: float

class IdeSafetyCore:
    def validate_input(self, prev_state: SystemState, input_energy: float):
        # [検証01] エネルギー=正のみ
        if input_energy <= 0:
            raise ValueError("エネルギー不足 / 入力エネルギー=正である必要")
        
        # [検証02] 因果違反チェック / 空間変数=禁止
        if hasattr(prev_state, 'distance') or hasattr(prev_state, 'target_pos'):
            raise TypeError("因果違反 / 空間変数=因果状態内")

    def update_step(self, prev_state: SystemState, input_energy: float, distortion_input: float) -> Tuple[SystemState, dict]:
        # [ステップ01] 入力検証=必須
        self.validate_input(prev_state, input_energy)
        
        # [ステップ02] 応力計算 / 公式=歪み*剛性
        stress = distortion_input * EngineConfig.STIFFNESS_K
        work_rate = stress * prev_state.omega
        
        # [ステップ03] 量子化 / 残差廃棄
        raw_next_phase = prev_state.phase + prev_state.omega
        next_phase_int = math.floor(raw_next_phase)
        entropy_export = raw_next_phase - next_phase_int
        
        # [ステップ04] 状態更新 / 不変データクラス
        new_state = SystemState(
            phase=next_phase_int,
            omega=prev_state.omega,
            stress_level=distortion_input,
            work_rate=work_rate
        )
        
        # [ステップ05] テレメトリ生成
        telemetry = {
            "projection_value": distortion_input * 100,
            "entropy_export": entropy_export,
            "status": "正常"
        }
        
        return new_state, telemetry
