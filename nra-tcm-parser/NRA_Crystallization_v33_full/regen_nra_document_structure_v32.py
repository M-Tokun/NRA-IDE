# regen_nra_document_structure_v32.py
# FILE: regen_nra_document_structure_v32.py 2026-02-15
# Comments must stay terse.
# FIX: Japanese split-regex (。／．) and 不変 check corrected from garbled encoding.
# ADD: CrystallizationConfig.from_dict() to load from JSON contracts.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import re


@dataclass(frozen=True)
class Section:
    title:      str
    body:       str
    references: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class GenesisBlock:
    allowed_terms: List[str]       = field(default_factory=list)
    axioms:        Dict[str, str]  = field(default_factory=dict)


@dataclass(frozen=True)
class NRAOutput:
    sections: List[Section]
    meta:     Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ValidationResult:
    ok:      bool
    score:   float
    reasons: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class CrystallizationConfig:
    max_crystal_sentences: int   = 2
    min_score:             float = 0.60
    w_axiom_refs:          float = 0.20
    w_length:              float = 0.20
    w_structure:           float = 0.60

    @classmethod
    def from_dict(cls, d: Dict) -> "CrystallizationConfig":
        """Load from JSON contracts.output block."""
        return cls(
            max_crystal_sentences=d.get("crystal_max_sentences", 2),
            min_score=d.get("crystal_min_score", 0.60),
        )


class StructureValidator:
    def __init__(self, config: Optional[CrystallizationConfig] = None) -> None:
        self.config = config or CrystallizationConfig()
        # FIX: Japanese sentence-end chars 。and ． were garbled; corrected to proper UTF-8
        self._sent_split = re.compile(r"[。．.!?]\s*", re.UNICODE)

    def validate(self, out: NRAOutput) -> ValidationResult:
        reasons: List[str] = []
        sec = {s.title.lower(): s for s in out.sections}

        if "crystal" not in sec:
            return ValidationResult(False, 0.0, ["missing: crystal"])
        if "trace" not in sec:
            return ValidationResult(False, 0.0, ["missing: trace"])

        crystal = sec["crystal"].body.strip()
        if not crystal:
            return ValidationResult(False, 0.0, ["empty: crystal"])

        sentences = [x for x in self._sent_split.split(crystal) if x.strip()]
        if len(sentences) > self.config.max_crystal_sentences:
            reasons.append("crystal: too many sentences")

        trace = sec["trace"].body.lower()
        if "decision" not in trace:
            reasons.append("trace: missing decision")
        # FIX: 不変 was garbled; corrected to proper UTF-8
        if (
            "kept_invariants" not in trace
            and "invariant" not in trace
            and "不変" not in trace
        ):
            reasons.append("trace: missing kept_invariants")

        score = 1.0 - min(0.8, 0.2 * len(reasons))
        score = max(0.0, score)
        return ValidationResult(score >= self.config.min_score, score, reasons)


class CrystallizationEngine:
    def __init__(self, config: Optional[CrystallizationConfig] = None) -> None:
        self.config    = config or CrystallizationConfig()
        self.validator = StructureValidator(self.config)

    def score(self, out: NRAOutput, genesis: Optional[GenesisBlock] = None) -> ValidationResult:
        base = self.validator.validate(out)
        if not genesis:
            # FIX: genesis=None now forces score floor to 0 (cannot earn axiom bonus)
            # Caller must provide GenesisBlock for full scoring.
            return ValidationResult(False, 0.0, list(base.reasons) + ["genesis: missing"])

        ax_keys = {k.lower() for k in genesis.axioms.keys()}
        refs: List[str] = []
        for s in out.sections:
            refs.extend([r.lower() for r in (s.references or [])])
        hit = sum(1 for r in refs if r in ax_keys)

        crystal = next(
            (s.body for s in out.sections if s.title.lower() == "crystal"), ""
        ).strip()
        n_chars = len(crystal)

        ax_bonus  = min(1.0, hit / 3.0) * self.config.w_axiom_refs
        len_bonus = 0.0
        if 1 <= n_chars <= 140:
            len_bonus = 1.0 * self.config.w_length
        elif 141 <= n_chars <= 240:
            len_bonus = 0.5 * self.config.w_length

        score = base.score * self.config.w_structure + ax_bonus + len_bonus
        score = max(0.0, min(1.0, score))

        ok = base.ok and score >= self.config.min_score
        reasons = list(base.reasons)
        if hit == 0:
            reasons.append("refs: no axiom hit")
        return ValidationResult(ok, score, reasons)

    @staticmethod
    def parse_plaintext(text: str) -> NRAOutput:
        sections: List[Section] = []
        title = "crystal"   # default: pre-heading content assigned to crystal
        buf:   List[str] = []
        for line in (text or "").splitlines():
            m = re.match(r"^\s*##+\s*(.+?)\s*$", line)
            if m:
                if buf:
                    sections.append(Section(title, "\n".join(buf).strip()))
                title = m.group(1).strip().lower()
                buf   = []
            else:
                buf.append(line)
        if buf:
            sections.append(Section(title, "\n".join(buf).strip()))
        return NRAOutput(sections=sections)
