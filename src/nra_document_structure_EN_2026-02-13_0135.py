# ==============================================================================
# FILE: nra_document_structure_EN_20260213_0135.py
# TITLE: NRA-IDE Document Structure Engine
# VERSION: 1.0.0
# AUTHOR: M-Tokuni (Original Logic) / KEN (Implementation)
# DATE: 2026-02-13 01:35
#
# [Design Principles]
# This engine applies the NRA-IDE axioms to "structured document generation
# and validation". Applicable to: design specs, technical documents, research
# papers, reports, proposals, protocols (all domains).
#
# [NRA Axiom Mapping]
#   GenesisBlock  → Causal Diode (definition lock / reverse-inference prohibition)
#   SectionNode   → Gear Mechanism (prior section confirmed → next section unlocked)
#   Validator     → R = δ/τ  (quantitative deviation judgment)
#   FAIL-CLOSED   → Discard deviating sections (no passage while ambiguous)
#
# [Usage]
#   1. Set DomainConfig (MEDICAL / TECHNICAL / LEGAL / etc.)
#   2. Register definitions in GenesisBlock (these become the "axioms")
#   3. Add SectionNodes to build the document
#   4. Call DocumentEngine.build() to produce a validated document
# ==============================================================================

from __future__ import annotations
import math
import re
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple
from datetime import datetime


# ==============================================================================
# 1. Domain Configuration (Domain Tuning)
# ==============================================================================

class DomainType(Enum):
    """
    Supported domain types.
    Each domain uses different τ (constraint thickness) and R_op (Fail-Closed
    threshold) values.
    """
    TECHNICAL   = auto()  # Technical specifications / design documents
    MEDICAL     = auto()  # Medical protocols / clinical reports
    ACADEMIC    = auto()  # Research papers / technical whitepapers
    LEGAL       = auto()  # Laws / regulations / contracts
    GENERAL     = auto()  # General purpose (default)


@dataclass(frozen=True)
class DomainConfig:
    """
    Per-domain parameter definition.
    frozen=True → immutable after creation (functions as a Causal Diode).

    tau:              Constraint thickness. Higher = stricter deviation tolerance.
    r_op:             Fail-Closed trigger threshold (R = δ/τ; discard if exceeded).
    allow_forward_ref: Whether forward references (to not-yet-defined sections) are
                       permitted.
    """
    domain: DomainType
    tau: float               # Constraint thickness (0.0 – 1.0)
    r_op: float              # Fail-Closed threshold (typically 0.6 – 1.0)
    allow_forward_ref: bool  # Forward-reference permission flag

    def __post_init__(self):
        # Guard against invalid values (prevent structurally invalid configuration)
        if not (0.0 < self.tau <= 1.0):
            raise ValueError(f"tau must be in (0, 1]. Got: {self.tau}")
        if not (0.0 < self.r_op <= 1.0):
            raise ValueError(f"r_op must be in (0, 1]. Got: {self.r_op}")


# Domain presets (Domain Tuning table)
DOMAIN_PRESETS: Dict[DomainType, DomainConfig] = {
    DomainType.TECHNICAL: DomainConfig(
        domain=DomainType.TECHNICAL,
        tau=0.50,               # Moderate strictness
        r_op=0.80,              # Detect technical deviations strictly
        allow_forward_ref=True  # Forward references are common in specs
    ),
    DomainType.MEDICAL: DomainConfig(
        domain=DomainType.MEDICAL,
        tau=0.60,               # NRA-IDE standard threshold (life-safety level)
        r_op=0.60,              # Near-zero tolerance: Fail-Closed triggers quickly
        allow_forward_ref=False # Undefined references are prohibited in medical use
    ),
    DomainType.ACADEMIC: DomainConfig(
        domain=DomainType.ACADEMIC,
        tau=0.55,
        r_op=0.75,
        allow_forward_ref=True  # Forward references to prior work are allowed
    ),
    DomainType.LEGAL: DomainConfig(
        domain=DomainType.LEGAL,
        tau=0.70,               # Strictest: legal ambiguity has zero tolerance
        r_op=0.55,
        allow_forward_ref=False
    ),
    DomainType.GENERAL: DomainConfig(
        domain=DomainType.GENERAL,
        tau=0.41,               # Balanced setting
        r_op=0.65,
        allow_forward_ref=True
    ),
}


# ==============================================================================
# 2. Genesis Block (Document axioms = immutable definition registry)
# ==============================================================================

@dataclass
class DefinitionEntry:
    """
    A single definition entry.
    term:       The term being defined.
    definition: The definition content (string).
    is_axiom:   If True, this entry is axiomatic: it cannot be changed or
                overwritten anywhere in the document.
    """
    term: str
    definition: str
    is_axiom: bool = False
    registered_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self):
        if not self.term.strip():
            raise ValueError("Definition term cannot be empty.")
        if not self.definition.strip():
            raise ValueError(f"Definition for '{self.term}' cannot be empty.")


class GenesisBlock:
    """
    Manages the document's definition registry.
    Acts as the "Causal Diode" in NRA-IDE.

    - Once registered, axiom entries (is_axiom=True) cannot be changed.
    - References to undefined terms are detected as violations.
    - Injecting contradictory definitions after sealing raises an error.
    """

    def __init__(self, domain_config: DomainConfig):
        self._config = domain_config
        self._definitions: Dict[str, DefinitionEntry] = {}
        self._sealed = False  # When True, no further additions are allowed

    def add(self, term: str, definition: str, is_axiom: bool = False) -> None:
        """Add a definition. Raises RuntimeError if GenesisBlock is sealed."""
        if self._sealed:
            raise RuntimeError(
                f"GenesisBlock is sealed. Cannot add '{term}' after sealing."
            )
        if term in self._definitions:
            existing = self._definitions[term]
            if existing.is_axiom:
                # Overwriting an axiom is structurally prohibited (Causal Diode)
                raise ValueError(
                    f"CAUSAL DIODE VIOLATION: Axiom '{term}' cannot be redefined."
                )
        self._definitions[term] = DefinitionEntry(
            term=term,
            definition=definition,
            is_axiom=is_axiom
        )

    def seal(self) -> None:
        """
        Seal the GenesisBlock.
        After sealing, no additions or modifications are allowed.
        Must be called before document generation begins.
        """
        self._sealed = True

    def resolve(self, term: str) -> Optional[DefinitionEntry]:
        """Look up a term's definition. Returns None if undefined."""
        return self._definitions.get(term)

    def is_defined(self, term: str) -> bool:
        return term in self._definitions

    @property
    def all_terms(self) -> List[str]:
        return list(self._definitions.keys())

    @property
    def sealed(self) -> bool:
        return self._sealed


# ==============================================================================
# 3. Section Node (Structural unit of a document)
# ==============================================================================

class SectionStatus(Enum):
    PENDING   = "PENDING"    # Not yet validated
    PASSED    = "PASSED"     # Validation passed
    FAILED    = "FAILED"     # FAIL-CLOSED (discarded)
    CAVEAT    = "CAVEAT"     # Passed with warning (Zone B)


@dataclass
class ValidationResult:
    """
    Validation result for a section.
    Stores the R = δ/τ calculation result and the reasons for any violations.
    """
    section_id: str
    delta: float           # Deviation amount (magnitude of structural drift)
    tau: float             # Constraint thickness (domain setting)
    r_ratio: float         # R = δ/τ
    status: SectionStatus
    violations: List[str]  # List of detected violations
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def zone(self) -> str:
        """Zone classification based on Three-Zone Structure."""
        if self.r_ratio < 0.40:
            return "A (PERMIT)"
        elif self.r_ratio < 1.00:
            return "B (PERMIT_WITH_CAVEAT)"
        else:
            return "C (FAIL-CLOSED)"


@dataclass
class SectionNode:
    """
    Represents a single section in the document.
    Gear Mechanism: this section is not evaluated until its dependency section
    is PASSED or CAVEAT.

    section_id:  Section identifier (e.g., "1.1", "2.3.1")
    title:       Section title
    content:     Section body text
    references:  List of definitions / terms this section references
    depends_on:  section_id of the preceding section (Gear dependency)
    """
    section_id: str
    title: str
    content: str
    references: List[str] = field(default_factory=list)
    depends_on: Optional[str] = None
    status: SectionStatus = SectionStatus.PENDING
    validation_result: Optional[ValidationResult] = None

    def __post_init__(self):
        if not self.section_id.strip():
            raise ValueError("section_id cannot be empty.")
        if not self.title.strip():
            raise ValueError(f"Section '{self.section_id}': title cannot be empty.")
        if not self.content.strip():
            raise ValueError(f"Section '{self.section_id}': content cannot be empty.")


# ==============================================================================
# 4. Structure Validator (R = δ/τ validation engine)
# ==============================================================================

class StructureValidator:
    """
    Validates each section against the GenesisBlock definitions and
    quantifies structural deviation.

    Deviation δ (delta) accumulation rules:
      1. Reference to an undefined term           → δ += 0.40 (critical violation)
      2. Forward reference (when prohibited)      → δ += 0.30
      3. Content is empty or extremely short      → δ += 0.20
      4. Invalid section_id format                → δ += 0.10
    """

    def __init__(self, genesis: GenesisBlock, config: DomainConfig):
        self._genesis = genesis
        self._config = config

    def validate(
        self,
        section: SectionNode,
        completed_sections: List[str]
    ) -> ValidationResult:
        """
        Validate a section and return a ValidationResult.

        completed_sections: list of section IDs that have already passed
                            (used for Gear Mechanism dependency check)
        """
        delta = 0.0
        violations: List[str] = []

        # --- [Check 1] Gear Mechanism: dependency completion check ---
        if section.depends_on is not None:
            if section.depends_on not in completed_sections:
                delta += 0.50
                violations.append(
                    f"GEAR_VIOLATION: depends_on '{section.depends_on}' "
                    f"is not yet completed."
                )

        # --- [Check 2] Reference term definition check ---
        for ref_term in section.references:
            if not self._genesis.is_defined(ref_term):
                if not self._config.allow_forward_ref:
                    # Critical violation in domains that prohibit forward references
                    delta += 0.40
                    violations.append(
                        f"UNDEFINED_REF: '{ref_term}' is not defined in GenesisBlock."
                    )
                else:
                    # Minor warning in domains that allow forward references
                    delta += 0.10
                    violations.append(
                        f"FORWARD_REF_WARNING: '{ref_term}' referenced before definition."
                    )

        # --- [Check 3] Content density check ---
        # Sections with very little content are flagged for insufficient density
        content_length = len(section.content.strip())
        if content_length < 20:
            delta += 0.20
            violations.append(
                f"LOW_DENSITY: content too short ({content_length} chars)."
            )
        elif content_length < 50:
            delta += 0.10
            violations.append(
                f"THIN_CONTENT: content may be insufficient ({content_length} chars)."
            )

        # --- [Check 4] section_id format check ---
        # Expected format: numeric with dots (e.g., "1", "2.1", "3.1.2")
        if not re.match(r'^\d+(\.\d+)*$', section.section_id):
            delta += 0.10
            violations.append(
                f"FORMAT_VIOLATION: section_id '{section.section_id}' "
                f"should be numeric (e.g., '1.1', '2.3.1')."
            )

        # --- [Step 5] R = δ/τ calculation ---
        tau = self._config.tau
        r_ratio = delta / tau if tau > 0 else float('inf')

        # --- [Step 6] Three-Zone judgment ---
        if r_ratio >= 1.0 or (len(violations) > 0 and r_ratio >= self._config.r_op):
            status = SectionStatus.FAILED
        elif r_ratio >= 0.40:
            status = SectionStatus.CAVEAT
        else:
            status = SectionStatus.PASSED

        return ValidationResult(
            section_id=section.section_id,
            delta=delta,
            tau=tau,
            r_ratio=r_ratio,
            status=status,
            violations=violations
        )


# ==============================================================================
# 5. Document Engine (Integrated generation engine)
# ==============================================================================

@dataclass
class DocumentOutput:
    """Final output of the generated document."""
    title: str
    domain: DomainType
    sections: List[SectionNode]          # Only sections that passed
    discarded: List[SectionNode]         # Sections discarded by FAIL-CLOSED
    discard_log: List[ValidationResult]  # Discard log (must NOT be used for learning)
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_text(self, include_meta: bool = False) -> str:
        """
        Output the validated document as plain text.
        If include_meta=True, validation scores are appended to each section.
        """
        lines = [
            f"# {self.title}",
            f"Domain: {self.domain.name}",
            f"Generated: {self.generated_at}",
            f"Sections passed: {len(self.sections)} / "
            f"Discarded: {len(self.discarded)}",
            "=" * 60,
            ""
        ]
        for sec in self.sections:
            lines.append(f"## [{sec.section_id}] {sec.title}")
            if include_meta and sec.validation_result:
                vr = sec.validation_result
                lines.append(
                    f"  [R={vr.r_ratio:.3f} | Zone:{vr.zone} | "
                    f"Status:{vr.status.value}]"
                )
            lines.append(sec.content)
            lines.append("")

        if self.discarded:
            lines.append("=" * 60)
            lines.append("## [DISCARD LOG] FAIL-CLOSED Sections")
            lines.append(
                "NOTE: This log is for structural verification only. "
                "Must NOT be used for improvement or learning."
            )
            for vr in self.discard_log:
                lines.append(f"  - [{vr.section_id}] R={vr.r_ratio:.3f} | "
                              f"Violations: {'; '.join(vr.violations)}")

        return "\n".join(lines)

    def integrity_score(self) -> float:
        """
        Overall structural integrity score (0.0 – 1.0).
        Calculated as pass_rate × complement of average R score (1 - avg_r).
        """
        total = len(self.sections) + len(self.discarded)
        if total == 0:
            return 0.0
        pass_rate = len(self.sections) / total
        if not self.sections:
            return 0.0
        avg_r = sum(
            s.validation_result.r_ratio
            for s in self.sections
            if s.validation_result
        ) / len(self.sections)
        # Lower R means closer to constraint center → higher coherence
        coherence = max(0.0, 1.0 - avg_r)
        return round(pass_rate * coherence, 4)


class DocumentEngine:
    """
    Integrated document generation engine.
    Manages the pipeline:
    GenesisBlock → SectionNode → Validator → DocumentOutput.

    Example usage:
        engine = DocumentEngine("Technical Spec", DomainType.TECHNICAL)
        engine.genesis.add("NRA-IDE", "Causal structure safety engine.", is_axiom=True)
        engine.genesis.seal()
        engine.add_section("1", "Overview",
                           "This document describes the NRA-IDE specification.",
                           references=["NRA-IDE"])
        output = engine.build()
        print(output.to_text())
    """

    def __init__(self, title: str, domain: DomainType = DomainType.GENERAL):
        self.title = title
        self._config = DOMAIN_PRESETS[domain]
        self.genesis = GenesisBlock(self._config)
        self._sections: List[SectionNode] = []
        self._validator = StructureValidator(self.genesis, self._config)

    def add_section(
        self,
        section_id: str,
        title: str,
        content: str,
        references: Optional[List[str]] = None,
        depends_on: Optional[str] = None
    ) -> None:
        """Add a section. GenesisBlock need not be sealed yet (checked at build time)."""
        node = SectionNode(
            section_id=section_id,
            title=title,
            content=content,
            references=references or [],
            depends_on=depends_on
        )
        self._sections.append(node)

    def build(self) -> DocumentOutput:
        """
        Generate the document.
        1. Auto-seal GenesisBlock if not already sealed.
        2. Validate each section in order.
        3. Accept PASSED/CAVEAT sections only; send FAILED to Discard Log.
        """
        if not self.genesis.sealed:
            self.genesis.seal()

        passed_sections: List[SectionNode] = []
        discarded_sections: List[SectionNode] = []
        discard_log: List[ValidationResult] = []
        completed_ids: List[str] = []

        for section in self._sections:
            result = self._validator.validate(section, completed_ids)
            section.validation_result = result
            section.status = result.status

            if result.status in (SectionStatus.PASSED, SectionStatus.CAVEAT):
                passed_sections.append(section)
                completed_ids.append(section.section_id)
            else:
                # FAIL-CLOSED: discard
                discarded_sections.append(section)
                discard_log.append(result)

        return DocumentOutput(
            title=self.title,
            domain=self._config.domain,
            sections=passed_sections,
            discarded=discarded_sections,
            discard_log=discard_log
        )


# ==============================================================================
# 6. Demo (operation check & usage examples)
# ==============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("NRA Document Structure Engine v1.0 - Demo")
    print("=" * 60)

    # --- Example 1: Technical specification (TECHNICAL domain) ---
    print("\n[Example 1] Technical Specification / TECHNICAL Domain\n")

    engine = DocumentEngine("NRA-IDE Technical Specification v1.0", DomainType.TECHNICAL)

    # Register definitions in GenesisBlock (fixed as axioms)
    engine.genesis.add("NRA-IDE",
                       "Causal structure safety engine. Handles no semantics or optimization.",
                       is_axiom=True)
    engine.genesis.add("Causal Diode",
                       "Mechanism that structurally prohibits reverse inference (Pi-1).",
                       is_axiom=True)
    engine.genesis.add("Fail-Closed",
                       "Safety mechanism that blocks output when R >= R_op.",
                       is_axiom=True)
    engine.genesis.add("R",   "R = delta/tau. Ratio of deviation to constraint thickness.")
    engine.genesis.add("delta", "Fluctuation amount representing structural deviation of input.")
    engine.genesis.add("tau",   "Constraint thickness. Domain-specific threshold parameter.")
    engine.genesis.seal()

    # Add sections
    engine.add_section(
        "1", "Overview",
        "This document describes the structural specification of NRA-IDE. "
        "Semantics, optimization, and history are not handled.",
        references=["NRA-IDE"]
    )
    engine.add_section(
        "2", "Core Components",
        "NRA-IDE has a three-layer separation structure: Pre-NRA / LLM / Post-NRA.",
        references=["NRA-IDE"],
        depends_on="1"
    )
    engine.add_section(
        "2.1", "Causal Diode",
        "The Causal Diode structurally prohibits reverse inference (Pi-1). "
        "Only forward causality is allowed; back-calculation from effect to cause is forbidden.",
        references=["Causal Diode", "NRA-IDE"],
        depends_on="2"
    )
    engine.add_section(
        "2.2", "Fail-Closed Mechanism",
        "R = delta/tau is computed. If R >= R_op, output is blocked immediately. "
        "Blocking is not an error; it is the maintenance of structural correctness.",
        references=["Fail-Closed", "R", "delta", "tau"],
        depends_on="2"
    )
    # Intentional violation: undefined reference
    engine.add_section(
        "3", "Undefined Reference Test",
        "This section references a non-existent term 'UNDEFINED_TERM'.",
        references=["UNDEFINED_TERM"],
        depends_on="2.2"
    )
    # Gear violation: dependency on a non-existent section
    engine.add_section(
        "4", "Gear Violation Test",
        "This section depends on section '99' which does not exist.",
        references=["NRA-IDE"],
        depends_on="99"
    )
    engine.add_section(
        "5", "Conclusion",
        "NRA-IDE is a causal structure safety engine. "
        "Sections that deviate from defined axioms are structurally excluded by Fail-Closed.",
        references=["NRA-IDE", "Fail-Closed"],
        depends_on="2.2"
    )

    # Generate document
    output = engine.build()

    # Display results
    print(output.to_text(include_meta=True))
    print(f"\nDocument Integrity Score: {output.integrity_score():.4f}")

    # --- Example 2: Medical protocol (MEDICAL domain) ---
    print("\n" + "=" * 60)
    print("[Example 2] Medical Protocol / MEDICAL Domain\n")

    med_engine = DocumentEngine("ICU Vital Signs Monitoring Protocol", DomainType.MEDICAL)
    med_engine.genesis.add(
        "Threshold_0.6",
        "NRA standard safety threshold. Immediate alert when R >= 0.6.",
        is_axiom=True
    )
    med_engine.genesis.add(
        "VitalSigns",
        "Five parameters: blood pressure, heart rate, body temperature, SpO2, respiratory rate."
    )
    med_engine.genesis.add(
        "Alert",
        "Signal notifying medical staff upon anomaly detection."
    )

    med_engine.add_section(
        "1", "Purpose",
        "This protocol defines the procedure for continuously monitoring ICU patients' "
        "VitalSigns and triggering an Alert when Threshold_0.6 is exceeded.",
        references=["VitalSigns", "Threshold_0.6", "Alert"]
    )
    med_engine.add_section(
        "2", "Monitoring Parameters",
        "All five VitalSigns parameters are monitored. "
        "Each parameter is automatically measured at one-minute intervals.",
        references=["VitalSigns"],
        depends_on="1"
    )
    # Attempt to reference an undefined term in a forward-ref-prohibited domain
    med_engine.add_section(
        "3", "Prohibited Reference Test",
        "This section uses an undefined term 'UNDEFINED_MEDICAL_TERM'.",
        references=["UNDEFINED_MEDICAL_TERM"],
        depends_on="2"
    )
    med_engine.add_section(
        "3.1", "Alert Trigger Conditions",
        "When R = delta/tau reaches R >= 0.6, an Alert is triggered immediately. "
        "The AI does not make the final triggering decision; authority rests with the attending physician.",
        references=["Alert", "Threshold_0.6"],
        depends_on="2"
    )

    med_output = med_engine.build()
    print(med_output.to_text(include_meta=True))
    print(f"\nDocument Integrity Score: {med_output.integrity_score():.4f}")

    print("\n--- Demo complete ---")
