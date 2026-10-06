# Current NRA-IDE boundary configuration

Definitions follow [AXIOMS.md](../theory/AXIOMS.md) and [axioms.json](../theory/axioms.json), checked at v2.4. The [reference implementation](../nra-core/foundations/NRA-IDE_Architecture_public.py) supplies classification; [the gate adapter](../gate/_canonical_threshold.py) retains target history across calls.

`R = delta / tau` requires finite delta >= 0 and finite tau > 0. Negative inputs are not repaired with abs(); tau=0 is OUT_OF_DESCRIPTION_DOMAIN. The three predeclared domain thresholds satisfy `0 <= R_warn < R_handoff < R_irrev < 1`. Old universal 0.40/0.99 cutoffs and Zone A/B/C are not the current model.

| Canonical status | Condition | Operational action |
|---|---|---|
| PERMIT | 0 <= R < R_warn | CONTINUE |
| BOUNDARY_WARNING | R_warn <= R < R_handoff | LOG_WARN |
| HANDOFF_REQUIRED | R_handoff <= R < R_irrev | FAIL_CLOSED |
| IRREVERSIBLE_TRANSITION | R_irrev <= R < 1, or retained irreversible latch | FAIL_CLOSED |
| RUPTURE_BOUNDARY | R >= 1, or retained target rupture | FAIL_CLOSED |
| CONFESSION | Invalid or unknown input, declaration or thresholds | FAIL_CLOSED |
| OUT_OF_DESCRIPTION_DOMAIN | tau = 0 for otherwise valid supplied structure | FAIL_CLOSED |

FAIL_CLOSED is an operational effect, not an eighth canonical state or complete silence. Handoff transfers execution authority only. Observation, logging and communication are independent dimensions. After target rupture, POST_RUPTURE_FIXED testimony continues through surviving channels, even if a later ratio falls or an input exception occurs. The target remains ruptured while an invalid sample is separately reported as CONFESSION.

The default JSON has null declaration/threshold fields and therefore returns CONFESSION. A domain operator must supply the target, unit, source, delta/tau construction rules, applicable domain and threshold basis before evaluation. Observation timestamp is required per call. The gate validates structure, not the truth of physical measurements or governing equations.

ide_presets.json contains only SOFTWARE_DEMO with illustrative 0.4/0.6/0.8 thresholds. It is unvalidated and has no clinical or physical safety authority. Old DOMAIN_A/B/C, no_history and JSON action labels are preserved in [legacy/v1](legacy/v1/structural_zones.md), not automatically converted.

Remaining margins are distinct: `remaining_ratio_margin = 1 - R` and `remaining_absorption_margin = tau - delta`. Irreversible/rupture state cannot be released by output changes, configuration copies or a lower R. The caller must preserve evaluation history across process restarts; constructing a new instance does not establish recovery.
