# FILE: chain_tension_nra_ide_2026-03-19_0113_EN.py
# TITLE: Chain Tension Management — NRA-IDE Fluctuation-Utilising Auto-Adjustment Sample
# Author: M-Tokuni / NRA-IDE Project
# Generated: 2026-03-19 01:13 JST
#
# Design principles:
#   Fluctuation is not noise to be removed — it is a structural signal to be tracked
#   dR/dt (rate of change of R) and fluctuation patterns are used as control signals
#   R >= 1.0 → Fail-Closed (return adjustment authority to human operator)
#   Auto-adjustment operates only while R < 1.0
#
# Polygon effect (chordal action):
#   Chain engagement with a sprocket generates periodic tension fluctuations.
#   Changes in the shape of this fluctuation pattern are precursors to faults.
# -------------------------------------------------------

import math
import time
from dataclasses import dataclass, field
from typing import List

# -------------------------------------------------------
# Constants
# -------------------------------------------------------

T_OPTIMAL   = 800.0    # N : design optimal tension
T_MIN       = 620.0    # N : lower tolerance limit (elongation / derailment risk)
T_MAX       = 1000.0   # N : upper tolerance limit (breakage / sprocket damage)

R_WARN      = 0.75     # WARNING threshold
R_FAIL      = 1.0      # Fail-Closed threshold

# Polygon effect parameters
SPROCKET_TEETH  = 17          # number of sprocket teeth
POLYGON_AMP     = 35.0        # N : normal fluctuation amplitude
POLYGON_PERIOD  = 1.0 / 5.0   # s : fundamental period (5 Hz assumed)

# Auto-adjustment parameters
ADJ_GAIN_FINE   = 0.15   # fine-adjustment gain (R < 0.75)
ADJ_GAIN_AHEAD  = 0.35   # predictive-adjustment gain (R >= 0.75)
ADJ_MAX_STEP    = 25.0   # N/step : maximum adjustment per step
ADJ_HISTORY     = 8      # number of history samples used for dR/dt

# -------------------------------------------------------
# Data structures
# -------------------------------------------------------

@dataclass
class ChainState:
    """Chain condition snapshot"""
    timestamp:  float
    t_raw:      float    # raw tension (with fluctuation)
    t_smooth:   float    # smoothed tension
    delta:      float    # accumulated deviation δ
    tau:        float    # absorption margin τ
    R:          float    # approach ratio R = δ/τ
    drdt:       float    # rate of change dR/dt
    polygon_amp: float   # detected fluctuation amplitude
    status:     str      # SAFE / WARNING / FAIL_CLOSED
    adj_output: float    # auto-adjustment output [N]
    adj_reason: str      # reason for adjustment

@dataclass
class RingBuffer:
    """Fixed-length history buffer"""
    capacity: int
    data: List[float] = field(default_factory=list)

    def push(self, v: float):
        self.data.append(v)
        if len(self.data) > self.capacity:
            self.data.pop(0)

    def mean(self) -> float:
        return sum(self.data) / len(self.data) if self.data else 0.0

    def amplitude(self) -> float:
        if len(self.data) < 2:
            return 0.0
        return max(self.data) - min(self.data)

# -------------------------------------------------------
# NRA-IDE core computation
# -------------------------------------------------------

def calc_ide(t_smooth: float) -> tuple:
    """
    Approach ratio R = δ / τ
    τ = total margin from optimal to the structural limit in the current direction
    """
    delta = abs(t_smooth - T_OPTIMAL)
    tau   = (T_MAX - T_OPTIMAL) if t_smooth >= T_OPTIMAL \
            else (T_OPTIMAL - T_MIN)
    tau   = max(tau, 0.01)
    R     = delta / tau
    return delta, tau, R

# -------------------------------------------------------
# Fluctuation generation (polygon effect simulation)
# -------------------------------------------------------

def polygon_fluctuation(t: float, amp: float) -> float:
    """
    Periodic fluctuation from sprocket engagement (chordal action).
    Fundamental wave + harmonics to approximate real chain fluctuation.
    """
    freq = 1.0 / POLYGON_PERIOD
    v  = amp * math.sin(2 * math.pi * freq * t)
    v += amp * 0.3 * math.sin(2 * math.pi * freq * 2 * t + 0.4)
    v += amp * 0.1 * math.sin(2 * math.pi * freq * 3 * t + 0.9)
    return v

# -------------------------------------------------------
# Auto-adjustment (fluctuation-utilising)
# -------------------------------------------------------

def calc_adjustment(R: float, drdt: float,
                    poly_amp: float, t_smooth: float) -> tuple:
    """
    Use dR/dt and fluctuation pattern changes as control signals.

    R < 0.5               : no adjustment needed
    0.5 ≤ R < R_WARN     : fine adjustment (follow fluctuation direction)
    R_WARN ≤ R < R_FAIL  : predictive adjustment (computed from arrival prediction)
    R >= R_FAIL           : Fail-Closed (return authority to human operator)
    """
    if R >= R_FAIL:
        return 0.0, "FAIL_CLOSED: returning adjustment authority to human operator"

    # Abnormal fluctuation amplitude detection (>1.5× normal amplitude = precursor)
    amp_ratio = poly_amp / POLYGON_AMP if POLYGON_AMP > 0 else 1.0
    amp_warn  = amp_ratio > 1.5

    # Direction toward optimal
    direction = 1.0 if t_smooth < T_OPTIMAL else -1.0

    if R < 0.5 and not amp_warn:
        return 0.0, "Normal: no adjustment needed"

    elif R < R_WARN:
        # Fine adjustment: proportional to deviation; extra correction on amplitude anomaly
        gain  = ADJ_GAIN_FINE * (1.0 + 0.5 if amp_warn else 1.0)
        adj   = direction * min(abs(t_smooth - T_OPTIMAL) * gain,
                                ADJ_MAX_STEP * 0.5)
        reason = f"Fine adjustment (R={R:.3f}" + \
                 (" · amplitude anomaly detected" if amp_warn else "") + ")"
        return adj, reason

    else:
        # Predictive adjustment: use dR/dt to estimate arrival time, apply lead control
        if drdt > 0.001:
            # R rising: predict arrival time and apply necessary adjustment in advance
            eta = (R_FAIL - R) / drdt   # estimated time to Fail-Closed [s]
            urgency = max(0.0, 1.0 - eta * 0.5)  # urgency factor
            gain    = ADJ_GAIN_AHEAD * (1.0 + urgency)
        else:
            gain = ADJ_GAIN_AHEAD

        adj    = direction * min(abs(t_smooth - T_OPTIMAL) * gain,
                                 ADJ_MAX_STEP)
        reason = f"Predictive adjustment (R={R:.3f} dR/dt={drdt:+.4f})"
        return adj, reason

# -------------------------------------------------------
# Simulation run
# -------------------------------------------------------

def run_simulation():
    print("=" * 68)
    print(" NRA-IDE Chain Tension Management — Fluctuation-Utilising Auto-Adjustment Simulation")
    print(f" T_OPT={T_OPTIMAL}N  T_MIN={T_MIN}N  T_MAX={T_MAX}N")
    print("=" * 68)

    T_SIM    = 8.0     # total simulation time [s]
    DT       = 0.05    # time step [s]
    steps    = int(T_SIM / DT)

    # Initial tension intentionally set low to observe R rising and auto-adjustment
    t_current = 700.0

    # Buffers
    smooth_buf = RingBuffer(capacity=10)
    R_buf      = RingBuffer(capacity=ADJ_HISTORY)
    raw_buf    = RingBuffer(capacity=20)
    history: List[ChainState] = []

    print(f"\n{'t[s]':>5} {'T_raw':>7} {'T_smt':>7} "
          f"{'δ':>6} {'τ':>6} {'R':>7} "
          f"{'dR/dt':>8} {'Status':>12} {'Adj[N]':>8}")
    print("-" * 90)

    for i in range(steps):
        t = i * DT

        # Add polygon effect fluctuation
        fluct = polygon_fluctuation(t, POLYGON_AMP)
        t_raw = t_current + fluct

        # Smoothing (moving average)
        smooth_buf.push(t_raw)
        raw_buf.push(t_raw)
        t_smooth = smooth_buf.mean()

        # NRA-IDE core computation
        delta, tau, R = calc_ide(t_smooth)

        # Compute dR/dt
        R_buf.push(R)
        if len(R_buf.data) >= 2:
            drdt = (R_buf.data[-1] - R_buf.data[-2]) / DT
        else:
            drdt = 0.0

        # Detect fluctuation amplitude
        poly_amp = raw_buf.amplitude()

        # Status determination
        if R >= R_FAIL:
            status = "FAIL_CLOSED"
        elif R >= R_WARN:
            status = "WARNING"
        else:
            status = "SAFE"

        # Compute auto-adjustment
        adj, reason = calc_adjustment(R, drdt, poly_amp, t_smooth)

        # Apply adjustment (not applied in Fail-Closed)
        if status != "FAIL_CLOSED":
            t_current += adj
            t_current = max(min(t_current, T_MAX + 50), T_MIN - 50)

        # Record
        state = ChainState(
            timestamp=t, t_raw=t_raw, t_smooth=t_smooth,
            delta=delta, tau=tau, R=R, drdt=drdt,
            polygon_amp=poly_amp, status=status,
            adj_output=adj, adj_reason=reason
        )
        history.append(state)

        # Display every 5 steps
        if i % 5 == 0:
            st_sym = {'SAFE':'✓','WARNING':'▲','FAIL_CLOSED':'✕'}[status]
            print(f"{t:5.2f} {t_raw:7.1f} {t_smooth:7.1f} "
                  f"{delta:6.1f} {tau:6.1f} {R:7.4f} "
                  f"{drdt:+8.4f} {st_sym+status:>13} {adj:+8.1f}")

    print("\n" + "=" * 68)
    # Summary
    safe_n = sum(1 for s in history if s.status == "SAFE")
    warn_n = sum(1 for s in history if s.status == "WARNING")
    fail_n = sum(1 for s in history if s.status == "FAIL_CLOSED")
    total  = len(history)
    print(f" SAFE       : {safe_n:3d} steps ({safe_n/total*100:.1f}%)")
    print(f" WARNING    : {warn_n:3d} steps ({warn_n/total*100:.1f}%)")
    print(f" FAIL_CLOSED: {fail_n:3d} steps ({fail_n/total*100:.1f}%)")
    adj_total = sum(abs(s.adj_output) for s in history)
    print(f" Total adj  : {adj_total:.1f} N")
    print("=" * 68)
    print(" Design principle: auto-adjustment operates only while R<1.0.")
    print(" At R>=1.0, authority is returned to the human operator.")
    print("=" * 68)


if __name__ == "__main__":
    run_simulation()
