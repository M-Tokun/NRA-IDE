# regen_nra_llm_pipeline.py
# FILE: regen_nra_llm_pipeline.py 2026-02-15
# Comments must stay terse.
# FIX: NRAFullPipeline stores genesis at init; run() uses stored genesis by default.
# FIX: Vault raw output capped at vault_raw_max_chars (default 500) to prevent secret leakage.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Any

from regen_nra_pre_rna import PreRNAGate, PolicyAction
from regen_nra_longrun_guard import LongRunGuard, GuardConfig
from regen_nra_document_structure_v32 import (
    CrystallizationEngine, CrystallizationConfig,
    GenesisBlock,
)


@dataclass(frozen=True)
class PipelineConfig:
    crystallization:   CrystallizationConfig = field(default_factory=CrystallizationConfig)
    guard:             GuardConfig            = field(default_factory=GuardConfig)
    fail_closed_return: str                   = ""
    vault_raw_max_chars: int                  = 500   # FIX: cap raw storage


@dataclass(frozen=True)
class PipelineResult:
    text:     str
    ok:       bool
    score:    float
    reasons:  List[str]         = field(default_factory=list)
    vault_id: Optional[str]     = None


class Vault:
    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, Any]] = {}
        self._seq = 0

    def put(self, payload: Dict[str, Any]) -> str:
        self._seq += 1
        vid = f"vault-{self._seq:06d}"
        self._store[vid] = payload
        return vid


class NRAFullPipeline:
    def __init__(
        self,
        llm_fn:    Callable[[str], str],
        config:    Optional[PipelineConfig]         = None,
        pre_gate:  Optional[PreRNAGate]             = None,
        guard:     Optional[LongRunGuard]           = None,
        engine:    Optional[CrystallizationEngine]  = None,
        vault:     Optional[Vault]                  = None,
        genesis:   Optional[GenesisBlock]           = None,   # FIX: stored at init
    ) -> None:
        self.llm_fn  = llm_fn
        self.cfg     = config or PipelineConfig()
        self.pre_gate = pre_gate or PreRNAGate()
        self.guard    = guard    or LongRunGuard(self.cfg.guard)
        self.engine   = engine   or CrystallizationEngine(self.cfg.crystallization)
        self.vault    = vault    or Vault()
        self.genesis  = genesis  # FIX: held for all run() calls

    def _prompt(self, user_text: str, genesis: Optional[GenesisBlock]) -> str:
        rules = [
            "Output headings: ## Crystal and ## Trace.",
            f"Crystal: <= {self.cfg.crystallization.max_crystal_sentences} sentences.",
            "Trace: include 'decision' and 'kept_invariants'.",
        ]
        if genesis and genesis.allowed_terms:
            rules.append("Prefer allowed terms: " + ", ".join(genesis.allowed_terms[:8]))
        return "\n".join(rules) + "\n\nUSER:\n" + user_text

    def _safe_raw(self, raw: str) -> str:
        """FIX: truncate raw for vault to prevent secret storage."""
        cap = self.cfg.vault_raw_max_chars
        return raw[:cap] + ("…[truncated]" if len(raw) > cap else "")

    def run(
        self,
        user_text: str,
        genesis:   Optional[GenesisBlock] = None,
    ) -> PipelineResult:
        # FIX: caller-supplied genesis overrides stored; stored genesis is the default
        effective_genesis = genesis or self.genesis

        pre = self.pre_gate.run(user_text)
        if pre.action == PolicyAction.BLOCK:
            return PipelineResult(
                self.cfg.fail_closed_return, False, 0.0, [f"pre:{pre.reason}"]
            )

        raw    = self.llm_fn(self._prompt(pre.text, effective_genesis))
        events = self.guard.check(raw)
        if self.guard.advise(events).startswith("Return empty"):
            vid = self.vault.put({
                "stage":  "guard",
                "events": [e.__dict__ for e in events],
                "raw":    self._safe_raw(raw),   # FIX: capped
            })
            return PipelineResult(
                self.cfg.fail_closed_return, False, 0.0, ["guard:fail"], vault_id=vid
            )

        out = self.engine.parse_plaintext(raw)
        vr  = self.engine.score(out, effective_genesis)

        if not vr.ok:
            vid = self.vault.put({
                "stage":   "validate",
                "score":   vr.score,
                "reasons": vr.reasons,
                "raw":     self._safe_raw(raw),   # FIX: capped
            })
            return PipelineResult(
                self.cfg.fail_closed_return, False, vr.score, vr.reasons, vault_id=vid
            )

        return PipelineResult(raw, True, vr.score, vr.reasons)
