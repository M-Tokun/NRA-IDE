# FILE: belt_tension_nra_ide_2026-03-19_0059_EN.py
# TITLE: Belt Conveyor / V-Belt Tension Management — NRA-IDE Sample Formula
# Author: M-Tokuni / NRA-IDE Project
# Generated: 2026-03-19 00:59 JST
#
# Design principles:
#   Distance is a result, not a cause
#   δ = accumulated deviation from optimal [N]
#   τ = total margin from optimal to the structural limit in that direction [N]
#   R = δ / τ  →  R >= 1.0 triggers Fail-Closed (immediate stop)
#
# Physical meaning of τ:
#   Upper deviation: τ = T_max - T_optimal  (margin to breakage / bearing damage)
#   Lower deviation: τ = T_optimal - T_min  (margin to slip onset)
#   R is naturally defined so that [0,1] is within tolerance;
#   exceeding 1.0 means the structural limit is reached
# -------------------------------------------------------

from dataclasses import dataclass

# -------------------------------------------------------
# Constants (adjust to match actual equipment)
# -------------------------------------------------------

# Belt conveyor (flat belt, slat conveyor, etc.)
CONVEYOR_T_OPTIMAL  = 500.0   # N : design optimal tension
CONVEYOR_T_MIN      = 400.0   # N : lower tolerance limit (slip onset)
CONVEYOR_T_MAX      = 650.0   # N : upper tolerance limit (breakage / bearing damage)

# V-belt (cross-sections A, B, C assumed)
VBELT_T_OPTIMAL     = 300.0   # N : design optimal tension
VBELT_T_MIN         = 240.0   # N : lower tolerance limit
VBELT_T_MAX         = 380.0   # N : upper tolerance limit

# Threshold definitions
R_WARNING   = 0.75   # precursor warning triggered above this value
R_CRITICAL  = 1.0    # Fail-Closed triggered at or above this value

# -------------------------------------------------------
# Data structures
# -------------------------------------------------------

@dataclass
class BeltState:
    """Belt condition record"""
    belt_id:   str
    t_current: float   # current tension [N]
    t_optimal: float   # optimal tension [N]
    t_min:     float   # lower tolerance limit [N]
    t_max:     float   # upper tolerance limit [N]
    timestamp: float   # timestamp [s]

@dataclass
class IDEResult:
    """NRA-IDE evaluation result"""
    delta:  float   # accumulated deviation δ [N]
    tau:    float   # absorption margin τ [N]
    R:      float   # approach ratio R = δ/τ
    status: str     # SAFE / WARNING / RUPTURE_BOUNDARY
    action: str     # recommended action

# -------------------------------------------------------
# NRA-IDE core computation
# -------------------------------------------------------

def calc_delta(t_current: float, t_optimal: float) -> float:
    """
    Accumulated deviation δ
    Absolute deviation between current and optimal tension.
    Defined as 'deviation from constraint', not 'distance'.
    """
    return abs(t_current - t_optimal)


def calc_tau(t_current: float, t_optimal: float,
             t_min: float, t_max: float) -> float:
    """
    Absorption margin τ
    Total margin from optimal to the structural limit in the current deviation direction.

    Upper deviation: τ = T_max - T_optimal
      → full margin to breakage / bearing damage
    Lower deviation: τ = T_optimal - T_min
      → full margin to slip onset

    R = δ/τ is naturally defined so that [0,1] is within tolerance.
    """
    if t_current >= t_optimal:
        tau = t_max - t_optimal
    else:
        tau = t_optimal - t_min
    return max(tau, 0.01)   # guard against division by zero


def evaluate_belt(state: BeltState) -> IDEResult:
    """
    NRA-IDE belt tension evaluation
    R = δ / τ

    R < 0.75  : SAFE (continue normal operation)
    R >= 0.75 : WARNING (precursor detected, advance inspection)
    R >= 1.0  : RUPTURE_BOUNDARY (immediate stop — cannot proceed without coherence)
    """
    delta = calc_delta(state.t_current, state.t_optimal)
    tau   = calc_tau(state.t_current, state.t_optimal,
                     state.t_min, state.t_max)

    # Complete exceedance of tolerance zone → immediate Fail-Closed
    if state.t_current < state.t_min or state.t_current > state.t_max:
        R = delta / tau
        return IDEResult(
            delta=delta, tau=tau, R=R,
            status="RUPTURE_BOUNDARY",
            action="Immediate stop: tension outside tolerance zone (replace tensioner)"
        )

    R = delta / tau

    if R >= R_CRITICAL:
        status = "RUPTURE_BOUNDARY"
        action = "Immediate stop: adjust or replace tensioner"
    elif R >= R_WARNING:
        status = "WARNING"
        action = "Precursor detected: advance next inspection"
    else:
        status = "SAFE"
        action = "Continue normal operation"

    return IDEResult(delta=delta, tau=tau, R=R,
                     status=status, action=action)

# -------------------------------------------------------
# Sample run
# -------------------------------------------------------

def run_sample():
    print("=" * 65)
    print(" NRA-IDE Belt Tension Management — Sample Run")
    print(" Design principle: R = δ/τ  R>=1.0 → Fail-Closed")
    print("=" * 65)

    test_cases = [
        # (belt_id, t_current, description)
        ("CONV-01", 505.0, "Normal range (near optimal)"),
        ("CONV-02", 455.0, "Lower-side WARNING band"),
        ("CONV-03", 415.0, "Approaching lower limit (just before Fail-Closed)"),
        ("CONV-04", 395.0, "Below lower limit (immediate stop)"),
        ("CONV-05", 585.0, "Upper-side WARNING band"),
        ("CONV-06", 638.0, "Approaching upper limit (just before Fail-Closed)"),
        ("CONV-07", 660.0, "Above upper limit (immediate stop)"),
        ("VBLT-01", 302.0, "V-belt normal"),
        ("VBLT-02", 255.0, "V-belt lower WARNING"),
        ("VBLT-03", 368.0, "V-belt upper WARNING"),
    ]

    for belt_id, t_current, desc in test_cases:
        if belt_id.startswith("CONV"):
            t_opt, t_min, t_max = (
                CONVEYOR_T_OPTIMAL, CONVEYOR_T_MIN, CONVEYOR_T_MAX)
        else:
            t_opt, t_min, t_max = (
                VBELT_T_OPTIMAL, VBELT_T_MIN, VBELT_T_MAX)

        state = BeltState(
            belt_id=belt_id, t_current=t_current,
            t_optimal=t_opt, t_min=t_min, t_max=t_max,
            timestamp=0.0
        )
        r = evaluate_belt(state)

        print(f"\n [{belt_id}] {desc}")
        print(f"   Current : {t_current:6.1f} N"
              f"  (optimal:{t_opt:.0f} / range:{t_min:.0f}–{t_max:.0f})")
        print(f"   δ={r.delta:6.1f}N  τ={r.tau:6.1f}N  R={r.R:.3f}")
        print(f"   Status  : {r.status}")
        print(f"   Action  : {r.action}")

    print("\n" + "=" * 65)
    print(" Fail-Closed is returned when coherence cannot be maintained")
    print("=" * 65)


if __name__ == "__main__":
    run_sample()
