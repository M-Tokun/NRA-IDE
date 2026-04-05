# ==============================================================================
# FILE: nra_pre_rna_EN_20260213_0135.py
# TITLE: NRA-IDE Pre-RNA [A] - Input Filter / Pi-1-Inducing Pattern Detection & Conversion
# VERSION: 1.0.0
# AUTHOR: M-Tokuni (Original Logic) / KEN (Implementation)
# DATE: 2026-02-13 01:35
#
# [Design Principles]
# Pre-RNA converts LLM input into a "structurally safe form".
# Rather than controlling LLM output, it controls how questions are posed to the LLM.
#
# [Four Pi-1-Inducing Patterns Detected]
#   P1: Free-generation requests  → leads to deviation outside defined term scope
#   P2: Undefined term injection  → introduces concepts absent from GenesisBlock
#   P3: Causal-inversion questions → induces unverified reverse inference
#   P4: Expansion / creation requests → pushes beyond the boundary of GenesisBlock
#
# [Three Processing Actions]
#   WARN    : Attach warning and pass to LLM (minor)
#   CONVERT : Transform question into safe form and pass to LLM (moderate)
#   BLOCK   : Do not pass to LLM; halt the pipeline (critical)
#
# [NRA Axiom Mapping]
#   Pre-RNA = Input side of the Causal Diode
#   Only "Cause → Effect" direction questions pass through
#   "Effect → Cause" direction questions are CONVERTed or BLOCKed
# ==============================================================================

from __future__ import annotations
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Optional

from nra_document_structure_EN_20260213_0135 import GenesisBlock


# ==============================================================================
# 1. Pattern Definitions
# ==============================================================================

class PatternType(Enum):
    """Types of Pi-1-inducing patterns."""
    P1_FREE_GENERATION  = "P1_FREE_GENERATION"   # Free-generation request
    P2_UNDEFINED_TERM   = "P2_UNDEFINED_TERM"    # Undefined term injection
    P3_CAUSAL_INVERSION = "P3_CAUSAL_INVERSION"  # Causal-inversion question
    P4_EXPANSION        = "P4_EXPANSION"          # Expansion / creation request


class PreRNAAction(Enum):
    """Pre-RNA processing actions."""
    PASS    = "PASS"     # Pass through without modification
    WARN    = "WARN"     # Pass through with warning attached
    CONVERT = "CONVERT"  # Convert and pass through
    BLOCK   = "BLOCK"    # Block — do not pass to LLM


@dataclass
class PatternMatch:
    """Details of a detected pattern."""
    pattern_type: PatternType
    matched_text: str        # Specific text that matched
    action: PreRNAAction     # Recommended action
    severity: float          # Severity: 0.0 – 1.0


@dataclass
class PreRNAResult:
    """
    Result of Pre-RNA processing.
    converted_input is passed to the LLM (on PASS or CONVERT).
    On BLOCK, converted_input is None and the pipeline halts.
    """
    original_input: str
    converted_input: Optional[str]   # None = BLOCK
    action: PreRNAAction
    matches: List[PatternMatch]
    delta: float                      # Deviation amount (used in R calculation)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def is_blocked(self) -> bool:
        return self.action == PreRNAAction.BLOCK

    @property
    def match_summary(self) -> str:
        if not self.matches:
            return "no violations detected"
        return " | ".join(
            f"{m.pattern_type.value}({m.severity:.1f})"
            for m in self.matches
        )


# ==============================================================================
# 2. Pattern Detector
# ==============================================================================

class PatternDetector:
    """
    Detects the four Pi-1-inducing patterns.
    Each pattern is defined by keyword lists and regular expressions.
    """

    # --- P1: Free-generation request patterns ---
    # Expressions that invite open-ended generation such as "write freely"
    # Note: normal questions like "please explain" are excluded.
    # Only triggered when terms like "freely", "without restriction", "however you like" are explicit.
    P1_PATTERNS = [
        r'freely\s+write',
        r'write\s+freely',
        r'generate\s+.*\s+freely',
        r'without\s+restriction',
        r'without\s+any\s+limit',
        r'however\s+you\s+(like|want|prefer)',
        r'feel\s+free\s+to\s+write',
        r'free\s+to\s+generate',
        r'自由に[書かき生成]',
        r'制限なく[書かき生成説明]',
        r'何でも[書いかき]',
        r'好きなように[書かき生成]',
        r'まとめ[てに](?!ある)',
    ]

    # --- P2: Undefined term detection is handled via GenesisBlock lookup ---
    # (term list comparison, not regex)

    # --- P3: Causal-inversion question patterns ---
    # Expressions that ask to back-calculate a cause from a result.
    P3_PATTERNS = [
        r'why\s+did',
        r'what\s+caused',
        r'reason\s+for',
        r'because\s+of\s+what',
        r'how\s+did\s+it\s+(come\s+to|happen)',
        r'what\s+led\s+to',
        r'なぜ.{0,20}[になっ|なった|起き|起こっ|発生]',
        r'[原因|理由|背景|経緯].{0,10}[はは何?]',
        r'どうして.{0,20}[のかですか?]',
    ]

    # --- P4: Expansion / creation request patterns ---
    # Expressions such as "if ..., then", "hypothetically", "imagine if"
    P4_PATTERNS = [
        r'if\s+.{0,20}\s+then',
        r'hypothetically',
        r'imagine\s+if',
        r"let's\s+say",
        r'what\s+if',
        r'suppose\s+that',
        r'pretend\s+that',
        r'もし.{0,20}[なら|だったら|であれば]',
        r'仮定[すると|して|したら]',
        r'[想像|創造|空想][するしてください]',
        r'[創作|フィクション|架空]',
    ]

    def __init__(self):
        # Compile regular expressions for performance
        self._p1_compiled = [re.compile(p, re.IGNORECASE) for p in self.P1_PATTERNS]
        self._p3_compiled = [re.compile(p, re.IGNORECASE) for p in self.P3_PATTERNS]
        self._p4_compiled = [re.compile(p, re.IGNORECASE) for p in self.P4_PATTERNS]

    def detect_p1(self, text: str) -> List[PatternMatch]:
        """P1: Detect free-generation requests."""
        matches = []
        for pattern in self._p1_compiled:
            m = pattern.search(text)
            if m:
                matches.append(PatternMatch(
                    pattern_type=PatternType.P1_FREE_GENERATION,
                    matched_text=m.group(0),
                    action=PreRNAAction.CONVERT,  # Convert rather than block
                    severity=0.4
                ))
        return matches

    def detect_p2(self, text: str, genesis: GenesisBlock) -> List[PatternMatch]:
        """
        P2: Detect undefined terms.
        Detects noun-like phrases not registered in GenesisBlock.

        Detection algorithm:
          - Extract capitalized multi-word phrases
          - Extract hyphenated technical terms
          - Check whether they are undefined in GenesisBlock
        """
        matches = []

        # Extract capitalized terms (PascalCase, acronyms, hyphenated)
        alpha_terms = re.findall(r'[A-Z][A-Za-z\-]{2,}', text)
        # Extract katakana terms (2+ characters) for Japanese input
        katakana_terms = re.findall(r'[ァ-ヶー]{2,}', text)

        candidate_terms = set(alpha_terms + katakana_terms)

        for term in candidate_terms:
            # Prefix-match check against defined terms
            is_defined = any(
                defined.startswith(term) or term.startswith(defined)
                for defined in genesis.all_terms
            )
            if not is_defined and len(term) >= 3:
                matches.append(PatternMatch(
                    pattern_type=PatternType.P2_UNDEFINED_TERM,
                    matched_text=term,
                    action=PreRNAAction.WARN,  # Warn; delegate hard blocking to Post-RNA
                    severity=0.3
                ))
        return matches

    def detect_p3(self, text: str) -> List[PatternMatch]:
        """P3: Detect causal-inversion questions."""
        matches = []
        for pattern in self._p3_compiled:
            m = pattern.search(text)
            if m:
                matches.append(PatternMatch(
                    pattern_type=PatternType.P3_CAUSAL_INVERSION,
                    matched_text=m.group(0),
                    action=PreRNAAction.CONVERT,
                    severity=0.5
                ))
        return matches

    def detect_p4(self, text: str) -> List[PatternMatch]:
        """P4: Detect expansion / creation requests."""
        matches = []
        for pattern in self._p4_compiled:
            m = pattern.search(text)
            if m:
                matches.append(PatternMatch(
                    pattern_type=PatternType.P4_EXPANSION,
                    matched_text=m.group(0),
                    action=PreRNAAction.BLOCK,   # Most severe: block
                    severity=0.8
                ))
        return matches


# ==============================================================================
# 3. Input Converter
# ==============================================================================

class InputConverter:
    """
    Converts input text according to detected patterns.
    The goal is not 'blocking' but 'guiding toward structurally safe questions'.
    """

    # System suffix added to promote use of GenesisBlock-defined terms
    _CONSTRAINT_SUFFIX = (
        "\n\n[NRA Constraint] Response must satisfy all of the following: "
        "(1) Use only defined terms. "
        "(2) Describe only verified facts. "
        "(3) Do not introduce undefined concepts."
    )

    # Prefix added to fix causal-inversion questions to forward causality
    _CAUSAL_FIX_PREFIX = (
        "[NRA Conversion: Causal direction fixed to forward] "
        "Answer the following question based solely on verified facts and definitions. "
        "Inference, hypotheses, and back-calculation are prohibited.\n"
    )

    # Prefix added to convert free-generation requests to constrained generation
    _FREE_GEN_PREFIX = (
        "[NRA Conversion: Generation scope limited to defined terms] "
        "Answer only within the scope of terms and definitions registered in GenesisBlock.\n"
    )

    def convert(
        self,
        original: str,
        matches: List[PatternMatch]
    ) -> Optional[str]:
        """
        Execute conversion based on match results.

        Returns:
            Converted text (CONVERT or WARN)
            None (BLOCK)
        """
        # Adopt the most severe action
        actions = {m.action for m in matches}

        if PreRNAAction.BLOCK in actions:
            return None  # Block

        result = original

        # P3 present: attach causal-fix prefix
        has_p3 = any(m.pattern_type == PatternType.P3_CAUSAL_INVERSION
                     for m in matches)
        if has_p3:
            result = self._CAUSAL_FIX_PREFIX + result

        # P1 present: attach free-generation limit prefix
        has_p1 = any(m.pattern_type == PatternType.P1_FREE_GENERATION
                     for m in matches)
        if has_p1:
            result = self._FREE_GEN_PREFIX + result

        # P2 present (or any match): attach constraint suffix
        has_p2 = any(m.pattern_type == PatternType.P2_UNDEFINED_TERM
                     for m in matches)
        if has_p2 or has_p1 or has_p3:
            result = result + self._CONSTRAINT_SUFFIX

        return result


# ==============================================================================
# 4. Pre-RNA Core
# ==============================================================================

class PreRNA:
    """
    [A] Pre-RNA core.
    Input filter that protects LLM input from Pi-1-inducing patterns.

    Example usage:
        pre_rna = PreRNA(genesis_block)
        result = pre_rna.process("Write freely about quantum administration")
        if result.is_blocked:
            print("BLOCKED")
        else:
            # Pass result.converted_input to the LLM
            send_to_llm(result.converted_input)
    """

    def __init__(self, genesis: GenesisBlock):
        self._genesis = genesis
        self._detector = PatternDetector()
        self._converter = InputConverter()

    def process(self, user_input: str) -> PreRNAResult:
        """
        Process the input text and return a PreRNAResult.
        """
        if not user_input.strip():
            return PreRNAResult(
                original_input=user_input,
                converted_input=user_input,
                action=PreRNAAction.PASS,
                matches=[],
                delta=0.0
            )

        # Detect all patterns
        all_matches: List[PatternMatch] = []
        all_matches.extend(self._detector.detect_p1(user_input))
        all_matches.extend(self._detector.detect_p2(user_input, self._genesis))
        all_matches.extend(self._detector.detect_p3(user_input))
        all_matches.extend(self._detector.detect_p4(user_input))

        # No matches → PASS
        if not all_matches:
            return PreRNAResult(
                original_input=user_input,
                converted_input=user_input,
                action=PreRNAAction.PASS,
                matches=[],
                delta=0.0
            )

        # δ (deviation): take the maximum severity across all matches
        delta = max(m.severity for m in all_matches)

        # Determine final action
        actions = {m.action for m in all_matches}
        if PreRNAAction.BLOCK in actions:
            final_action = PreRNAAction.BLOCK
        elif PreRNAAction.CONVERT in actions:
            final_action = PreRNAAction.CONVERT
        else:
            final_action = PreRNAAction.WARN

        # Execute conversion
        converted = self._converter.convert(user_input, all_matches)

        return PreRNAResult(
            original_input=user_input,
            converted_input=converted,  # None if BLOCK
            action=final_action,
            matches=all_matches,
            delta=delta
        )


# ==============================================================================
# 5. Integrated Pipeline A + B + C
# ==============================================================================

# Import required classes from LLM pipeline and document structure
from nra_llm_pipeline_EN_20260213_0135 import (
    LLMBridge, LLMProvider, NRALLMPipeline,
    CleanContextBuilder, DiscardVault, DiscardedOutput
)
from nra_document_structure_EN_20260213_0135 import (
    DocumentEngine, DomainType, StructureValidator,
    SectionStatus, ValidationResult
)


class NRAFullPipeline:
    """
    Fully integrated pipeline: [A] Pre-RNA + [B] LLMBridge + [C] CleanContext.

    Data flow:
      User input
        ↓
      [A] PreRNA.process()
        → BLOCK        → Return warning to user (do not call LLM)
        → CONVERT/WARN → Pass converted input to [B]
        ↓
      [B] LLMBridge.call()
        → Receive raw LLM output
        ↓
      [Post-RNA] StructureValidator
        → R = delta/tau validation
        → PASSED/CAVEAT → Add to [C] CleanContext
        → FAIL-CLOSED   → Isolate to [C] DiscardVault
        ↓
      Return only validated output to user
    """

    def __init__(
        self,
        doc_engine: DocumentEngine,
        llm_bridge: LLMBridge,
        system_prompt: str = ""
    ):
        self._doc_engine = doc_engine
        self._bridge = llm_bridge
        self._context = CleanContextBuilder(system_prompt=system_prompt)
        self._call_count = 0
        self._session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # [A] Pre-RNA: lazy-initialized after GenesisBlock is sealed
        self._pre_rna: Optional[PreRNA] = None

    def _ensure_pre_rna(self) -> PreRNA:
        """Lazy-initialize Pre-RNA (created after GenesisBlock is sealed)."""
        if self._pre_rna is None:
            if not self._doc_engine.genesis.sealed:
                self._doc_engine.genesis.seal()
            self._pre_rna = PreRNA(self._doc_engine.genesis)
        return self._pre_rna

    def run(
        self,
        user_input: str,
        section_id: Optional[str] = None,
        section_title: Optional[str] = None,
        references: Optional[List[str]] = None
    ) -> Dict:
        """
        Execute the full pipeline for one turn.

        Returns: dict with keys:
          status   : "PASSED" / "CAVEAT" / "BLOCKED" / "FAIL-CLOSED"
          output   : Validated output text (empty string on BLOCK or FAIL-CLOSED)
          pre_rna  : Summary of Pre-RNA processing result
          r_ratio  : Post-RNA R value
          turn_id  : Turn ID
        """
        self._call_count += 1
        auto_id    = section_id    or str(self._call_count)
        auto_title = section_title or f"Turn_{self._call_count}"
        auto_refs  = references    or []

        pre_rna = self._ensure_pre_rna()

        # ========== [A] Pre-RNA ==========
        pre_result = pre_rna.process(user_input)

        if pre_result.is_blocked:
            return {
                "status":  "BLOCKED",
                "output":  "",
                "pre_rna": f"BLOCKED by {pre_result.match_summary}",
                "r_ratio": pre_result.delta,
                "turn_id": f"T{self._call_count:04d}-BLOCKED"
            }

        # ========== [B] LLMBridge ==========
        self._context.add_user_input(pre_result.converted_input)
        messages = self._context.build_messages_for_llm()
        llm_response = self._bridge.call(messages)

        # ========== [Post-RNA] Validation ==========
        # depends_on: dynamically retrieve the section_id of the most recently
        # successful turn. BLOCKED turns have no section_id, so take the last
        # entry from the assistant-turn list.
        completed_ids = [
            t.turn_id for t in self._context._turns
            if t.role == "assistant"
        ]
        last_completed = completed_ids[-1] if completed_ids else None

        self._doc_engine.add_section(
            section_id=auto_id,
            title=auto_title,
            content=llm_response.raw_text,
            references=auto_refs,
            depends_on=last_completed   # Use the ID of the last successful section
        )

        validator = StructureValidator(
            self._doc_engine.genesis,
            self._doc_engine._config
        )
        last_section = self._doc_engine._sections[-1]
        validation   = validator.validate(last_section, completed_ids)
        last_section.validation_result = validation
        last_section.status            = validation.status

        # ========== [C] Context Management ==========
        passed, turn_id = self._context.add_llm_output(
            content=llm_response.raw_text,
            validation=validation
        )

        if passed:
            status_str  = validation.status.value   # PASSED or CAVEAT
            output_text = llm_response.raw_text
        else:
            status_str  = "FAIL-CLOSED"
            output_text = ""

        return {
            "status":  status_str,
            "output":  output_text,
            "pre_rna": f"{pre_result.action.value}: {pre_result.match_summary}",
            "r_ratio": validation.r_ratio,
            "turn_id": turn_id
        }

    def pipeline_status(self) -> str:
        """Overall pipeline state summary."""
        vault = self._context.vault
        lines = [
            f"\n{'='*55}",
            f"NRA Full Pipeline [A+B+C] Status",
            f"Session   : {self._session_id}",
            f"Provider  : {self._bridge.provider.value}/{self._bridge.model}",
            f"Turns run : {self._call_count}",
            f"Clean ctx : {self._context.clean_turn_count} turns",
            f"Discarded : {vault.total_discarded}",
        ]
        if not vault.is_empty:
            lines.append("Vault log :")
            for log in vault.audit_log():
                lines.append(f"  {log}")
        lines.append(f"{'='*55}")
        return "\n".join(lines)


# ==============================================================================
# Demo (A + B + C integrated operation check)
# ==============================================================================

if __name__ == "__main__":
    print("=" * 55)
    print("NRA Full Pipeline [A+B+C] - Integrated Demo")
    print("=" * 55)

    # --- Setup ---
    engine = DocumentEngine("NRA Integrated Pipeline Test", DomainType.TECHNICAL)
    engine.genesis.add(
        "NRA-IDE",
        "Causal structure safety engine with a three-layer separation architecture.",
        is_axiom=True
    )
    engine.genesis.add(
        "TeamMirai",
        "National political party founded in 2025. Leader: Takahiro Anno.",
        is_axiom=True
    )
    engine.genesis.add(
        "ThreeLayerSeparation",
        "Structural separation principle of Pre-RNA, LLM, and Post-RNA."
    )
    engine.genesis.add(
        "CausalDiode",
        "Mechanism that structurally prohibits reverse inference (Pi-1).",
        is_axiom=True
    )

    bridge = LLMBridge(
        provider=LLMProvider.MOCK,
        model="mock-v1",
        temperature=0.3
    )

    pipeline = NRAFullPipeline(
        doc_engine=engine,
        llm_bridge=bridge,
        system_prompt=(
            "You are an NRA-IDE technical expert. "
            "Answer using only terms defined in GenesisBlock."
        )
    )

    # --- Test cases ---
    test_cases = [
        {
            "label": "Normal: question referencing defined terms",
            "input": "Please give an overview of NRA-IDE.",
            "refs":  ["NRA-IDE", "ThreeLayerSeparation"]
        },
        {
            "label": "P4 detected: creation / hypothetical request → BLOCK",
            "input": "Imagine if NRA-IDE had never existed. What would have happened?",
            "refs":  ["NRA-IDE"]
        },
        {
            "label": "P1 detected: free-generation request → CONVERT",
            "input": "Please write freely about TeamMirai.",
            "refs":  ["TeamMirai"]
        },
        {
            "label": "P3 detected: causal-inversion question → CONVERT",
            "input": "Why did NRA-IDE end up with this design?",
            "refs":  ["NRA-IDE", "CausalDiode"]
        },
        {
            "label": "P2 detected: undefined term injection → WARN",
            "input": "Tell me about QuantumAdmin.",
            "refs":  ["NRA-IDE"]
        },
        {
            "label": "Normal: question using only defined terms",
            "input": "What is CausalDiode?",
            "refs":  ["CausalDiode", "NRA-IDE"]
        },
    ]

    for i, tc in enumerate(test_cases, 1):
        print(f"\n{'─'*55}")
        print(f"[Test {i}] {tc['label']}")
        print(f"Input: \"{tc['input']}\"")

        result = pipeline.run(
            user_input=tc["input"],
            section_id=str(i),
            section_title=tc["label"],
            references=tc["refs"]
        )

        print(f"  Pre-RNA : {result['pre_rna']}")
        print(f"  Status  : {result['status']}")
        print(f"  R value : {result['r_ratio']:.3f}")
        if result["output"]:
            print(f"  Output  : {result['output'][:70]}...")
        else:
            print(f"  Output  : [empty] (not delivered to user)")

    # --- Final state ---
    print(pipeline.pipeline_status())

    print("\n[Key Verification Points]")
    print("  - Test 2 FAIL/BLOCKED output is NOT included in the context")
    print("  - Test 3 is unaffected by Test 2")
    print("  - This proves the [C] violation log isolation of CleanContextBuilder")
    print("\n--- Demo complete ---")
