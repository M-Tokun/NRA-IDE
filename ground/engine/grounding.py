# ground/engine/grounding.py
# FILE: ground/engine/grounding.py 26-0628-1913
# NRA-IDE Inverse Grounding Engine Rev.2
# 前版：26-0628-1855 → 型分離・3パターン実装・ハード制約化

# ©M-Tokuni 2026

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

BOTTOM = None  # ⊥：未観測・未定義・補完禁止


@dataclass
class GroundedVariable:
    """
    接地済み変数。
    e_i ∈ {0,1}：接地フラグ
    x_i ∈ X_i ∪ {⊥}：物理値
    観測台帳（メタデータ）を必須付帯。
    """
    name: str
    e: int                      # 接地フラグ（0 or 1）
    x: Any                      # 物理値（BOTTOM=⊥）
    # 観測台帳（必須付帯メタデータ）
    acquired_at: str = ""       # 取得時刻
    location: str = ""          # 場所
    unit: str = ""              # 単位
    instrument: str = ""        # 機器
    calibration: str = ""       # 校正状態
    error_margin: float = 0.0   # 測定誤差
    source: str = ""            # 出所

    def __post_init__(self):
        if self.e not in (0, 1):
            raise ValueError(f"接地フラグ e は 0 か 1 のみ有効: {self.name}")
        if self.e == 1 and self.x is BOTTOM:
            raise ValueError(f"e=1 なのに x=⊥ は不整合: {self.name}")
        if self.e == 0:
            self.x = BOTTOM  # e=0 → x は必ず ⊥


class GroundingEngine:
    """
    逆行接地エンジン。
    Pattern A：全必須変数有効 → 逆算実行
    Pattern B：必須変数欠損  → FAIL-CLOSED発火
    Pattern C：非必須変数欠損 → 欠損明示で継続
    """

    def __init__(
        self,
        m_required: set[str],
        c_phys_validator: Any = None,
    ):
        """
        m_required       : 必須変数集合 M_required
        c_phys_validator : 物理制約チェック関数（ドメイン別・未実装は None）
        """
        self.m_required = m_required
        self.c_phys_validator = c_phys_validator

    def classify(
        self, variables: dict[str, GroundedVariable]
    ) -> str:
        """
        3パターン分類。
        Returns: "A" | "B" | "C"
        """
        for name in self.m_required:
            v = variables.get(name)
            if v is None or v.x is BOTTOM:
                return "B"  # Pattern B：必須変数欠損

        missing_optional = [
            name for name, v in variables.items()
            if name not in self.m_required and v.x is BOTTOM
        ]
        if missing_optional:
            return "C"  # Pattern C：非必須変数欠損

        return "A"  # Pattern A：全変数有効

    def execute(
        self, variables: dict[str, GroundedVariable], R: Any
    ) -> dict:
        """
        逆行計算実行。パターン判定 → 分岐処理。
        補完推論は全パターンで禁止。
        """
        pattern = self.classify(variables)

        if pattern == "B":
            missing = [
                name for name in self.m_required
                if variables.get(name) is None
                or variables[name].x is BOTTOM
            ]
            raise RuntimeError(
                f"FAIL-CLOSED [Pattern B]: "
                f"必須変数欠損 {missing}。"
                f"補完禁止・実行権限停止。"
            )

        if pattern == "C":
            missing_optional = [
                name for name, v in variables.items()
                if name not in self.m_required and v.x is BOTTOM
            ]
            # 欠損明示で継続（補完しない）
            result = self._inverse_compute(variables, R)
            result["pattern"] = "C"
            result["missing_optional"] = missing_optional
            result["warning"] = (
                f"非必須変数 {missing_optional} が欠損。"
                f"不確定範囲として返却。補完なし。"
            )
            return result

        # Pattern A：全変数有効
        result = self._inverse_compute(variables, R)
        result["pattern"] = "A"
        return result

    def _inverse_compute(
        self, variables: dict[str, GroundedVariable], R: Any
    ) -> dict:
        """
        実際の逆算処理。
        C_phys バリデーション後に実行。
        ドメイン別実装はサブクラスでオーバーライド。
        """
        # 物理制約チェック（ハード制約）
        if self.c_phys_validator is not None:
            valid, reason = self.c_phys_validator(variables)
            if not valid:
                raise RuntimeError(
                    f"FAIL-CLOSED [C_phys violation]: {reason}"
                )

        # ドメイン別逆算（未実装）
        raise NotImplementedError(
            "ドメイン別 inverse_compute 未実装。"
            "サブクラスで _inverse_compute をオーバーライドすること。"
        )


# ─────────────────────────────────────────
# テストケース（3パターン確認用）
# ─────────────────────────────────────────

def _run_tests():
    from datetime import datetime

    # 必須変数：temperature, pressure
    engine = GroundingEngine(m_required={"temperature", "pressure"})

    # ── Pattern A：全変数有効 ──────────────────
    vars_a = {
        "temperature": GroundedVariable(
            name="temperature", e=1, x=25.3,
            unit="℃", source="sensor_01",
            acquired_at="2026-06-28T10:00:00+09:00"
        ),
        "pressure": GroundedVariable(
            name="pressure", e=1, x=1013.25,
            unit="hPa", source="sensor_02",
            acquired_at="2026-06-28T10:00:00+09:00"
        ),
        "humidity": GroundedVariable(
            name="humidity", e=1, x=65.0,
            unit="%", source="sensor_03",
            acquired_at="2026-06-28T10:00:00+09:00"
        ),
    }
    try:
        engine.execute(vars_a, R={"observation": "test"})
    except NotImplementedError as e:
        print(f"[Pattern A] 変数確定 → NotImplementedError（正常）: {e}")

    # ── Pattern B：必須変数欠損 ──────────────────
    vars_b = {
        "temperature": GroundedVariable(
            name="temperature", e=1, x=25.3,
            unit="℃", source="sensor_01",
            acquired_at="2026-06-28T10:00:00+09:00"
        ),
        "pressure": GroundedVariable(
            name="pressure", e=0, x=BOTTOM,  # 欠損
            unit="hPa", source=""
        ),
    }
    try:
        engine.execute(vars_b, R={})
    except RuntimeError as e:
        print(f"[Pattern B] FAIL-CLOSED発火（正常）: {e}")

    # ── Pattern C：非必須変数欠損 ──────────────────
    vars_c = {
        "temperature": GroundedVariable(
            name="temperature", e=1, x=25.3,
            unit="℃", source="sensor_01",
            acquired_at="2026-06-28T10:00:00+09:00"
        ),
        "pressure": GroundedVariable(
            name="pressure", e=1, x=1013.25,
            unit="hPa", source="sensor_02",
            acquired_at="2026-06-28T10:00:00+09:00"
        ),
        "humidity": GroundedVariable(
            name="humidity", e=0, x=BOTTOM,  # 非必須欠損
            unit="%", source=""
        ),
    }
    try:
        engine.execute(vars_c, R={})
    except NotImplementedError as e:
        print(f"[Pattern C] 欠損明示継続 → NotImplementedError（正常）: {e}")


if __name__ == "__main__":
    _run_tests()
