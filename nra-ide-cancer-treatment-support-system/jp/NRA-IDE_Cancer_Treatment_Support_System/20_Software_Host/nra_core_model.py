# ═══════════════════════════════════════════════════════════════════════
# File: nra_core_model.py
# Phase: 20 (Reference Model)
# Date: 2026-07-28
#
# 目的: 10_BioCalibrator_TypeA.v の演算を Q8.8 のビット単位で再現する参照実装。
#
#   - FPGA 非接続時のシミュレーション判定
#   - 安全マップ（判定境界）の描画
#
#   の双方が本モジュールだけを判定根拠とする。ホスト側に独自の近似式を
#   持たせてはならない（モデルの二重化の禁止 / PHASE_2 §4）。
#
# 判定式 (PHASE_2 Rev 2.0, 全項 kPa):
#   sigma_el = (E + B) * (D - d)/D
#   sigma_v  = 12 * eta * v * D / (1000 * d^2)
#   sigma_el + sigma_v > dP  =>  BLOCKED
# ═══════════════════════════════════════════════════════════════════════

from typing import Dict, Optional, Tuple

# ── 来歴表記（生成物に転記される） ─────────────────────────────────
#
# 本テンプレートは配布物である。生成されたレポートはリポジトリから切り離され、
# 単独で流通する。したがって成果物自身が、どのモデルで・検証済みか否かを
# 名乗らなければならない。
#
# 【フォークする者への指示】
#   * 物理式を改変した場合、MODEL_VERSION を必ず変更すること。
#     変更しなければ、改変版が本テンプレートの検証状態を騙ることになる。
#   * 実験検証を経ていない状態で VALIDATION_STATUS を書き換えてはならない。
#   * LICENSE_JP.txt は、特約事項を「すべての複製または重要な部分」に
#     記載することを求めている。COPYRIGHT / LICENSE_NOTE を削除してはならない。
#
MODEL_NAME = "NRA-IDE Type A Jamming"
MODEL_VERSION = "PHASE_2 Rev 2.0"
VALIDATION_STATUS = "未検証（マイクロ流路試験プロトコル 未実施）"
TEMPLATE_NAME = "NRA-IDE Cancer Treatment Support System"
TEMPLATE_URL = "https://github.com/M-Tokun/NRA-IDE"
COPYRIGHT = "Copyright (c) 2026 M-Tokuni / MIT License with Medical Disclaimer"
LICENSE_NOTE = "詳細は LICENSE_JP.txt の特約事項1〜3を参照のこと。"

# ── Phase 4 §2 エラーコード ────────────────────────────────────────────
ERR_NONE = 0x00
ERR_GEOM = 0x01         # D < d           すり抜け
ERR_RANGE = 0x02        # 範囲外入力
ERR_VISC0 = 0x03        # eta = 0         律環公理違反
ERR_OVF = 0x04          # 演算オーバーフロー
ERR_COMM = 0x05         # 通信異常（ホストのみ）
ERR_UNSUPPORTED = 0x06  # 未実装の癌腫タイプ（ホストのみ）

# エラーコード名。レポート・可視化とも本辞書のみを参照し、独自に持たない。
ERR_NAME = {
    ERR_NONE:        "ERR_NONE",
    ERR_GEOM:        "ERR_GEOMETRIC",
    ERR_RANGE:       "ERR_RANGE",
    ERR_VISC0:       "ERR_ZERO_VISC",
    ERR_OVF:         "ERR_OVERFLOW",
    ERR_COMM:        "ERR_COMM",
    ERR_UNSUPPORTED: "ERR_UNSUPPORTED",
}

# ── Phase 4 §1 入力範囲 (Q8.8) ─────────────────────────────────────────
RANGES_Q88 = {
    'cell_stiffness': (0x0019, 0x0A00),   # E    0.1  - 10.0  kPa
    'cell_viscosity': (0x0002, 0x0100),   # eta  0.01 -  1.0  Pa*s
    'cell_diameter':  (0x0500, 0x1E00),   # D    5.0  - 30.0  um
    'pore_size':      (0x0500, 0x0F00),   # d    5.0  - 15.0  um
    'flow_dp':        (0x0000, 0x0500),   # dP   0.0  -  5.0  kPa
    'drug_boost':     (0x0000, 0x0A00),   # B    0.0  - 10.0  kPa
}

# 変形速度の既定値。現行の 14 バイトプロトコルは v を搬送しないため、
# 測定値が無い場合は Phase 4 の標準値を用いる（レポートに明記のこと）。
DEFAULT_DEFORM_VELOCITY = 200.0

# ── Phase 6 §3 定数ROM（10_BioCalibrator_TypeA.v と同一定義） ──────────
# 添字 idx = Q8.8値[12:6]（物理量を 0.25um 刻みに量子化, X = idx/4 [um]）
ROM_RECIP = [0 if n < 20 else 262144 // n for n in range(128)]        # 1/D       Q0.16
ROM_KVISC = [0 if n < 20 else 3221225 // (n * n) for n in range(128)]  # 0.012/d^2 Q0.24


def to_q88(value: float) -> int:
    """Q8.8 への量子化（クランプ＋切り捨て）。全ファイルはこの関数のみを使うこと。"""
    return int(max(0.0, min(255.99, value)) * 256)


def normalize_type(cancer_type: str) -> str:
    """'Type A' / 'TypeA' / 'type_a' などの表記ゆれを吸収する"""
    return (cancer_type or '').replace(' ', '').replace('_', '').lower()


def fixed_terms(eta_q: int, D_q: int, d_q: int, v_q: int) -> Tuple[int, int]:
    """
    患者ごとに固定される項を求める。E（ヤング率）には依存しない。
      strain  : (D-d)/D            Q0.8
      sigma_v : 粘性抵抗応力 [kPa]  Q8.8
    """
    dx = D_q - d_q
    strain = (dx * ROM_RECIP[D_q >> 6]) >> 16
    q1 = ((eta_q * v_q) * ROM_KVISC[d_q >> 6]) >> 24
    sigma_v = (q1 * D_q) >> 16
    return strain, sigma_v


def check_inputs(q: Dict[str, int]) -> int:
    """PHASE_4 §2.1 の判定順序: 0x03 -> 0x02 -> 0x01"""
    if q['cell_viscosity'] == 0:
        return ERR_VISC0
    for key, (lo, hi) in RANGES_Q88.items():
        if not (lo <= q[key] <= hi):
            return ERR_RANGE
    if q['cell_diameter'] < q['pore_size']:
        return ERR_GEOM
    return ERR_NONE


def evaluate(params: Dict[str, float], cancer_type: str = "Type A") -> Dict:
    """
    FPGA 演算コアと同一の判定を返す。
    戻り値は fpga_interface.send_query と同じ形式。
    """
    if normalize_type(cancer_type) != 'typea':
        # Type B は RTL が未完成であり、モデルも未検証（PHASE_2 §3）
        return {'is_jammed': False, 'error_code': ERR_UNSUPPORTED}

    q = {k: to_q88(params.get(k, 0.0)) for k in RANGES_Q88}
    v_q = to_q88(params.get('deform_velocity', DEFAULT_DEFORM_VELOCITY))

    err = check_inputs(q)
    if err != ERR_NONE:
        # Fail-Closed: 異常時は転移リスク側（PASSABLE）へ倒す
        return {'is_jammed': False, 'error_code': err}

    strain, sigma_v = fixed_terms(
        q['cell_viscosity'], q['cell_diameter'], q['pore_size'], v_q)

    el_mul = (q['cell_stiffness'] + q['drug_boost']) * strain
    if el_mul >> 24:                      # el_mul[32:24] != 0
        return {'is_jammed': False, 'error_code': ERR_OVF}

    sigma_total = ((el_mul >> 8) & 0xFFFF) + sigma_v
    if sigma_total >> 16:
        return {'is_jammed': False, 'error_code': ERR_OVF}

    return {'is_jammed': sigma_total > q['flow_dp'], 'error_code': ERR_NONE}


def required_boost(params: Dict[str, float]) -> Optional[float]:
    """
    現在の dP に対し BLOCKED を成立させる最小 Boost [kPa]。
    既に BLOCKED なら 0.0、判定不能なら None。
    """
    q = {k: to_q88(params.get(k, 0.0)) for k in RANGES_Q88}
    v_q = to_q88(params.get('deform_velocity', DEFAULT_DEFORM_VELOCITY))

    q_probe = dict(q, drug_boost=0)
    if check_inputs(q_probe) != ERR_NONE:
        return None

    strain, sigma_v = fixed_terms(
        q['cell_viscosity'], q['cell_diameter'], q['pore_size'], v_q)
    if strain == 0:
        return None

    lo, hi = RANGES_Q88['drug_boost']
    for b_q in range(lo, hi + 1):
        if (((q['cell_stiffness'] + b_q) * strain) >> 8) + sigma_v > q['flow_dp']:
            return b_q / 256.0
    return None


if __name__ == "__main__":
    sample = {'cell_stiffness': 1.5, 'cell_viscosity': 0.05, 'cell_diameter': 12.0,
              'pore_size': 8.0, 'flow_dp': 0.6, 'drug_boost': 0.0}
    print("evaluate      :", evaluate(sample))
    print("required_boost:", required_boost(sample), "kPa")
