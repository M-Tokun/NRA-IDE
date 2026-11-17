"""Exact checks for the explanatory margin-balance extension, not a deployed evaluator.

Synthetic data only. Run with python -B and optionally --output <new JSON path>.
Expected exception classifications below are data returned by a test helper;
VALID_DOMAIN is a helper label, not a canonical NRA state.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
BASELINES = {
    "theory/AXIOMS.md": "7911CA41DDC56A5974BD4CD895882EAFCC9A0673B0981B1683C3C68EFD01C916",
    "theory/axioms.json": "812F6663B922F9B4003520F52D5AB279682CB6344D84FD75000C6733683F3DD3",
    "FORMULA.md": "893AA320AF1737E41E1CDC0A38BFE5B0463DD4862B91C4D876BD14A77182B226",
    "dictionary/NRA-IDE_Dictionary_JP.md": "96ED06658D3DAC7062D24C357FDFF9201EDF42D0B1B1CA0C1237B2358B1AB8C3",
    "dictionary/NRA-IDE_Dictionary_EN.md": "D3DC166AABEDEAAE25A77A04A64F32417815341813322337F3C54CDE6A875C24",
    "dictionary/ids.json": "84006DB27B1FE94D8D7FE14FBD92C6D148B205AB85BCA55EEF343F6F98CD0FAD",
    "local_reports/承認待ち一覧.md": "250F7E9F274ED5024D7677A07A11FBFF5E2D21174A2CCE11BF902C763C90A781",
    "nra-core/foundations/開放系_境界接近比の増分分解_論文草案_2026-11-16.md": "E665A2BFC735ED06C5BBDC29DB2FBFBD5F4D4968D8DFD46AEF7BEF41AD3A136D",
    "nra-core/foundations/open_system_R_decomposition_check_20261116.py": "698B68088AF256237EFE2A8BFACD4ED380E8860C5B40B916E8F9C1E959D290CC",
    "note/06_対話セッション記録/現実の開放系を記述する「泥臭い応用式」の骨格計算不可能性と「不明」を内包する構造動力学.MD": "5EEC8483EDE4295BA98CA1D9C689F5DB4373A3C1DE11C10A7A077172060B2D38",
    "note/06_対話セッション記録/NRA-IDE_開いた動的構造式.MD": "82D030E148E6702BC6FD19214C8D2FA8D5515CA372977DD065A263F3C789A6D5",
    "note/06_対話セッション記録/NRA-IDE_開いた動的構造式と泥臭い応用式の対照精査および正典v2.5整合報告.md": "4B5AF63D77CB35DD9A091D4F2CF23FECD9AEC164E6EAD8213327D987CB2B7137",
    "note/06_対話セッション記録/NRA-IDE_開いた動的構造式と泥臭い応用式の対照精査および正典v2.5整合報告_精査報告_2026-11-16.md": "9C9EB0EDA23083204F4F16196D05A08912E43C714246A04A42AB82928BD37E3E",
}


def margin(theta, delta, tau):
    return theta * tau - delta


def resolved_margin_change(theta, q0, p0, q1, p1, t0, t1, old_total_after):
    """No decomposition when a required component is unavailable; never fill with zero."""
    if any(value is None for value in (q0, p0, q1, p1, t0, t1, old_total_after)):
        return None
    deg = old_total_after - t0
    comp = t1 - old_total_after
    return -(q1 - q0) - (p1 - p0) + theta * deg + theta * comp


def domain(delta, tau, *, metadata_known=True, channel_missing=False):
    """Test-only input guard. It neither runs actuators nor replaces the reference evaluator."""
    if not metadata_known:
        return "CONFESSION"
    for value in (delta, tau):
        if value is not None:
            if isinstance(value, bool) or not isinstance(value, (int, float, F)):
                return "CONFESSION"
            if isinstance(value, float) and not math.isfinite(value):
                return "CONFESSION"
            if value < 0:
                return "CONFESSION"
    if delta is None or tau is None:
        return "NOT_OBSERVABLE" if channel_missing else "CONFESSION"
    if tau == 0:
        return "OUT_OF_DESCRIPTION_DOMAIN"
    return "VALID_DOMAIN"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    counts = {}

    def check(group, condition):
        if not condition:
            raise AssertionError(group)
        counts[group] = counts.get(group, 0) + 1

    # Independent endpoint evaluation versus an incremental balance; includes theta=0,
    # zero delta, increasing/decreasing delta, and increasing/decreasing thickness.
    ds = (F(0), F(1, 2), F(1), F(3), F(7))
    ts = (F(1, 2), F(1), F(2), F(5))
    thresholds = (F(0), F(1, 2), F(7, 10), F(9, 10), F(1))
    for d0, d1, t0, t1, theta in product(ds, ds, ts, ts, thresholds):
        m0, m1 = margin(theta, d0, t0), margin(theta, d1, t1)
        dd, dt = d1 - d0, t1 - t0
        check("total_balance", m1 == m0 - (dd - theta * dt))
        check("boundary_equivalence", (d1 / t1 >= theta) == (m1 <= 0))
        check("one_event_equivalence", (d1 / t1 >= theta) == (dd - theta * dt >= m0))
        check("ratio_reconstruction_identity", d1 / t1 == theta - m1 / t1)
        check("margin_order", margin(F(1), d1, t1) - m1 == (1 - theta) * t1)

    # Resolved component examples have nondecreasing residual p and nonincreasing
    # old-composition thickness. A composition change is supplied as separate data.
    for q0, q1, p0, dp, t0, deg, comp, theta in product(
        (F(0), F(1), F(3)), (F(0), F(1), F(3)), (F(0), F(1)),
        (F(0), F(1, 2)), (F(2), F(5)), (F(0), F(-1, 2)),
        (F(-1, 4), F(0), F(1)), thresholds,
    ):
        t1, p1 = t0 + deg + comp, p0 + dp
        dq = q1 - q0
        direct = margin(theta, q1 + p1, t1) - margin(theta, q0 + p0, t0)
        expanded = resolved_margin_change(theta, q0, p0, q1, p1, t0, t1, t0 + deg)
        check("four_contributions", direct == expanded)
        # Previously published R decomposition is checked independently alongside it.
        r0 = (q0 + p0) / t0
        r_terms = dq / t1 + dp / t1 - r0 * deg / t1 - r0 * comp / t1
        check("previous_ratio_decomposition", (q1 + p1) / t1 - r0 == r_terms)
        check("residual_fixed_snapshot", margin(theta, p1, t1) == margin(theta, q1 + p1, t1) + q1)

    # Table printed in the document. lambda for the original element is held at
    # 1/4 after step 2; step 3 adds an independently measured thickness of 4.
    theta = F(7, 10)
    states = [(F(2), F(1), F(9)), (F(7, 2), F(3, 2), F(8)),
              (F(15, 4), F(3, 2), F(15, 2)), (F(15, 4), F(3, 2), F(23, 2)),
              (F(0), F(3, 2), F(23, 2))]
    expected = (F(33, 10), F(3, 5), F(0), F(14, 5), F(131, 20))
    trajectory = []
    cumulative = F(0)
    for i, ((q, p, tau), expected_m) in enumerate(zip(states, expected)):
        delta = q + p
        m = margin(theta, delta, tau)
        check("document_table", m == expected_m)
        row = {"n": i, "q": str(q), "p": str(p), "tau": str(tau),
               "delta": str(delta), "R": str(delta / tau), "margin_0.7": str(m)}
        if i:
            q0, p0, t0 = states[i - 1]
            effective_change = (q + p - q0 - p0) - theta * (tau - t0)
            cumulative += effective_change
            row["margin_change"] = str(m - expected[i - 1])
            check("history_telescope", m == expected[0] - cumulative)
        trajectory.append(row)

    # Exact boundary: strictly below, equal, and strictly above; no rounding used.
    boundary_cases = []
    for dd, expected_side in ((F(1, 5), -1), (F(1, 4), 0), (F(3, 10), 1)):
        d1, t1 = F(5) + dd, F(8) - F(1, 2)
        m1 = margin(theta, d1, t1)
        side = (d1 / t1 > theta) - (d1 / t1 < theta)
        check("boundary_neighbours", side == expected_side)
        boundary_cases.append({"delta_increment": str(dd), "tau_increment": "-1/2",
                               "R": str(d1 / t1), "margin": str(m1), "side": side})

    # Domain exceptions are expected outcomes, not failing executions.
    invalid_cases = [(F(1), F(0), "OUT_OF_DESCRIPTION_DOMAIN"),
                     (F(-1), F(1), "CONFESSION"), (F(1), F(-1), "CONFESSION"),
                     (float("nan"), F(1), "CONFESSION"),
                     (F(1), float("inf"), "CONFESSION"),
                     (F(1), float("-inf"), "CONFESSION"),
                     (True, F(1), "CONFESSION"), (None, F(1), "CONFESSION")]
    for delta, tau, expected_status in invalid_cases:
        check("domain_guards", domain(delta, tau) == expected_status)
    check("domain_guards", domain(None, F(1), channel_missing=True) == "NOT_OBSERVABLE")
    check("domain_guards", domain(F(1), F(2), metadata_known=False) == "CONFESSION")
    check("domain_guards", domain(F(0), F(1)) == "VALID_DOMAIN")
    check("domain_guards", domain(F(1), F(1, 10**100)) == "VALID_DOMAIN")

    # More detail cannot be reconstructed from fewer observed variables.
    check("identifiability", margin(theta, F(4), F(8)) == F(8, 5))
    check("identifiability", F(3) + F(1) == F(1) + F(3))
    check("identifiability", margin(theta, F(1), F(8)) != margin(theta, F(3), F(8)))
    check("component_unavailable_not_zero",
          resolved_margin_change(theta, F(0), F(2), F(0), F(2), F(8), F(5), None) is None)
    check("component_unavailable_not_zero", margin(theta, F(2), F(5)) - margin(theta, F(2), F(8)) == F(-21, 10))
    # A min-composition removal can strengthen the total and needs a new declaration.
    check("serial_removal_scope", min((F(2), F(8))) < min((F(8),)))
    # Positive instantaneous slack never clears an already existing irreversible latch.
    prior_latch = True
    later_r = F(2, 10)
    retained_latch = prior_latch or later_r >= F(9, 10)
    check("latch_preserved", margin(theta, F(2), F(10)) > 0 and retained_latch)
    # Equal observed endpoints alone do not exclude an unobserved excursion.
    full_history = (F(0), F(9, 10), F(0))
    endpoint_history = (full_history[0], full_history[-1])
    check("missing_history", any(r >= F(9, 10) for r in full_history)
          and not any(r >= F(9, 10) for r in endpoint_history)
          and endpoint_history[0] == endpoint_history[1])

    manifest = []
    for relative, expected_hash in BASELINES.items():
        digest = sha256((ROOT / relative).read_bytes()).hexdigest().upper()
        check("source_preservation", digest == expected_hash)
        manifest.append({"path": relative, "sha256": digest, "unchanged": True})
    result = {"kind": "exact_algebra_checks_on_synthetic_data", "all_passed": True,
              "checks_by_group": counts, "total_checks": sum(counts.values()),
              "trajectory": trajectory, "boundary_neighbours": boundary_cases,
              "source_manifest": manifest,
              "artifact_hashes": {
                  "checker": sha256(Path(__file__).read_bytes()).hexdigest(),
                  "document": sha256((ROOT / "nra-core/foundations/境界余白の収支による説明用拡張式_2026-11-17.md").read_bytes()).hexdigest(),
              },
              "physical_validation": "not_performed", "canonical_adoption": "not_claimed"}
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = args.output.resolve()
        output.relative_to(ROOT)  # Restrict writes to this repository.
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(text)  # Create only; never replace a previous result.
    print(text, end="")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
