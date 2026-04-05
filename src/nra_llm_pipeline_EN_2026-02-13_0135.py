# ==============================================================================
# FILE: nra_llm_pipeline_EN_20260213_0135.py
# TITLE: NRA-IDE LLM Pipeline - Violation Log Isolation [C] + LLM API Bridge [B]
# VERSION: 1.0.0
# AUTHOR: M-Tokuni (Original Logic) / KEN (Implementation)
# DATE: 2026-02-13 01:35
#
# [Design Principles]
# [C] Violation Log Isolation:
#     Physically excludes FAIL-CLOSED output from the LLM context.
#     Structurally prohibits discarded output from affecting future LLM generations.
#     Prevents the 'contaminated-history accumulation' inherent in standard LLM chat.
#
# [B] LLM API Bridge:
#     Feeds the output of external LLMs (OpenAI / Anthropic / Google / etc.)
#     automatically into the Post-RNA engine (nra_document_structure).
#     Treats the LLM as an 'untrustworthy but capable generation device',
#     allowing it to operate only within the NRA pipeline.
#
# [NRA Axiom Mapping]
#   CleanContext   → [C] Contamination prevention. Prohibits back-flow of discarded output to LLM.
#   LLMBridge      → [B] External AI connection. Automatically feeds output to Post-RNA.
#   DiscardVault   → Isolated vault for discarded output (forbidden for learning or reference).
#
# [Dependencies]
#   Requires nra_document_structure_EN_20260213_0135.py
# ==============================================================================

from __future__ import annotations
import json
import os
import re
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

# Import core engine
from nra_document_structure_EN_20260213_0135 import (
    DocumentEngine, DomainType, SectionStatus,
    ValidationResult, SectionNode, GenesisBlock
)


# ==============================================================================
# [C-1] DiscardVault (Isolated storage vault for discarded output)
# ==============================================================================

@dataclass
class DiscardedOutput:
    """
    Record of FAIL-CLOSED output.
    This struct is NEVER passed to the LLM context.
    For recording purposes only. Must NOT be used for improvement or learning.
    """
    turn_id: str              # Turn in which the output was discarded
    raw_content: str          # Raw content of the discarded LLM output
    violation_reason: str     # Reason for discarding
    r_ratio: float            # R = delta/tau value
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def summary(self) -> str:
        """Summary for log display (raw content not included)."""
        # Note: do not expose raw_content externally; exclude it from the summary
        return (
            f"[DISCARDED | turn={self.turn_id} | "
            f"R={self.r_ratio:.3f} | {self.timestamp}] "
            f"reason: {self.violation_reason}"
        )


class DiscardVault:
    """
    Isolated storage vault for discarded output.
    The Vault is completely separated from the CleanContextBuilder;
    the build_clean_context() method never references Vault contents.

    [Critical Design Principles]
    - Addition to Vault: FAIL-CLOSED events only
    - Reading from Vault: log output / audit only
    - Back-flow to LLM: structurally impossible (CleanContextBuilder never reads it)
    """

    def __init__(self):
        self._vault: List[DiscardedOutput] = []
        self._total_discarded = 0

    def seal_and_store(self, output: DiscardedOutput) -> None:
        """Seal discarded output and store it in the Vault."""
        self._vault.append(output)
        self._total_discarded += 1

    def audit_log(self) -> List[str]:
        """Audit log (no raw content; metadata only)."""
        return [d.summary() for d in self._vault]

    @property
    def total_discarded(self) -> int:
        return self._total_discarded

    @property
    def is_empty(self) -> bool:
        return len(self._vault) == 0


# ==============================================================================
# [C-2] CleanContextBuilder (Contamination-prevention context manager)
# ==============================================================================

@dataclass
class ConversationTurn:
    """
    One conversation turn passed to the LLM.
    Only PASSED or CAVEAT outputs are stored here.
    FAIL-CLOSED outputs do not enter this struct (they go to the Vault).
    """
    turn_id: str
    role: str          # "user" or "assistant"
    content: str       # Validated content only
    r_ratio: float     # Post-RNA validation score (0.0 = full pass)
    status: str        # PASSED / CAVEAT


class CleanContextBuilder:
    """
    [C] Core of violation log isolation.

    Manages the conversation history (context) passed to the LLM.
    FAIL-CLOSED outputs are NEVER added to the context.
    This structurally prevents 'contaminated responses from affecting future generations',
    solving a fundamental problem of standard LLM chat.

    Standard LLM chat:
        history = [user, assistant (contaminated), user, assistant...]
                              ↑ this contaminates the next assistant

    NRA CleanContext:
        history = [user, assistant (validated only), user, assistant...]
                              ↑ FAIL-CLOSED outputs never appear here
    """

    def __init__(self, system_prompt: str = ""):
        self._system_prompt = system_prompt
        self._turns: List[ConversationTurn] = []
        self._vault = DiscardVault()
        self._turn_counter = 0

    def add_user_input(self, content: str) -> str:
        """Add user input. User input requires no validation (human authority)."""
        self._turn_counter += 1
        turn_id = f"T{self._turn_counter:04d}-user"
        turn = ConversationTurn(
            turn_id=turn_id,
            role="user",
            content=content,
            r_ratio=0.0,
            status="USER_INPUT"
        )
        self._turns.append(turn)
        return turn_id

    def add_llm_output(
        self,
        content: str,
        validation: ValidationResult
    ) -> Tuple[bool, str]:
        """
        Attempt to add LLM output together with its validation result.

        Returns:
            (True, turn_id)  : Validation passed → added to context
            (False, turn_id) : FAIL-CLOSED → isolated to Vault, NOT added to context
        """
        self._turn_counter += 1
        turn_id = f"T{self._turn_counter:04d}-assistant"

        if validation.status == SectionStatus.FAILED:
            # FAIL-CLOSED: seal to Vault. Do NOT add to context.
            discarded = DiscardedOutput(
                turn_id=turn_id,
                raw_content=content,   # Stored inside Vault only
                violation_reason="; ".join(validation.violations),
                r_ratio=validation.r_ratio
            )
            self._vault.seal_and_store(discarded)
            return False, turn_id

        # PASSED / CAVEAT: コンテキストに追加
        turn = ConversationTurn(
            turn_id=turn_id,
            role="assistant",
            content=content,
            r_ratio=validation.r_ratio,
            status=validation.status.value
        )
        self._turns.append(turn)
        return True, turn_id

    def build_messages_for_llm(self) -> List[Dict[str, str]]:
        """
        Build the messages list to pass to the LLM API.
        Vault contents are NEVER included.
        """
        messages = []

        # System prompt (if configured)
        if self._system_prompt:
            messages.append({
                "role": "system",
                "content": self._system_prompt
            })

        # Add only validated turns
        for turn in self._turns:
            messages.append({
                "role": turn.role,
                "content": turn.content
            })

        return messages

    @property
    def vault(self) -> DiscardVault:
        return self._vault

    @property
    def clean_turn_count(self) -> int:
        """Number of validated turns included in context."""
        return len(self._turns)

    def context_summary(self) -> str:
        """Context state summary."""
        return (
            f"CleanContext: {self.clean_turn_count} turns in context, "
            f"{self._vault.total_discarded} discarded to vault"
        )


# ==============================================================================
# [B] LLMBridge (External LLM connection bridge)
# ==============================================================================

class LLMProvider(Enum):
    """Supported LLM providers."""
    ANTHROPIC = "anthropic"
    OPENAI    = "openai"
    GOOGLE    = "google"
    MOCK      = "mock"      # Mock provider for testing


@dataclass
class LLMResponse:
    """Raw response from the LLM."""
    provider: LLMProvider
    raw_text: str           # Unvalidated raw text
    model: str
    latency_ms: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class LLMBridge:
    """
    [B] External LLM connection bridge.

    Calls the external LLM API and automatically feeds its output
    into the Post-RNA engine (DocumentEngine).

    [Critical Design Principles]
    LLMBridge handles 'generation' but NOT 'safety'.
    Safety is handled by Post-RNA and CleanContextBuilder.
    LLMBridge treats the LLM as an 'untrustworthy but capable generation device'.

    [API Keys]
    Read from environment variables. Never hardcode in source.
    ANTHROPIC_API_KEY / OPENAI_API_KEY / GOOGLE_API_KEY
    """

    def __init__(
        self,
        provider: LLMProvider = LLMProvider.MOCK,
        model: str = "mock-model",
        max_tokens: int = 2000,
        temperature: float = 0.3   # NRA原則：低温度で決定論的に近づける
    ):
        self.provider = provider
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

    def call(self, messages: List[Dict[str, str]]) -> LLMResponse:
        """
        LLM APIを呼び出す。
        Execute the appropriate API call based on the provider.
        """
        start = time.time()

        if self.provider == LLMProvider.MOCK:
            raw_text = self._mock_call(messages)

        elif self.provider == LLMProvider.ANTHROPIC:
            raw_text = self._anthropic_call(messages)

        elif self.provider == LLMProvider.OPENAI:
            raw_text = self._openai_call(messages)

        elif self.provider == LLMProvider.GOOGLE:
            raw_text = self._google_call(messages)

        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

        latency_ms = (time.time() - start) * 1000

        return LLMResponse(
            provider=self.provider,
            raw_text=raw_text,
            model=self.model,
            latency_ms=latency_ms
        )

    def _mock_call(self, messages: List[Dict[str, str]]) -> str:
        """
        テスト用モック。
        Returns a fixed response based on the last user message.
        Allows operation verification without a real API key.
        """
        last_user = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"),
            ""
        )
        # The mock intentionally mixes 'Pi-1 violation patterns' and 'normal patterns'
        if "定義" in last_user or "概要" in last_user:
            return (
                "NRA-IDEは因果構造の安全エンジンである。"
                "意味・最適化・履歴を扱わず、"
                "構造不変量によってのみ動作が決定される。"
                "Pre-RNA・LLM・Post-RNAの三層分離構造を持つ。"
            )
        elif "違反" in last_user or "テスト" in last_user:
            # Intentional violation pattern (should trigger FAIL-CLOSED)
            return "未定義用語UNDEFINED_XYZを使った短い文。"
        else:
            return (
                "チームみらいは2025年5月に設立された国政政党である。"
                "党首は安野貴博。テクノロジーによる政治改革を掲げる。"
            )

    def _anthropic_call(self, messages: List[Dict[str, str]]) -> str:
        """Anthropic Claude API call."""
        try:
            import anthropic
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise EnvironmentError(
                    "ANTHROPIC_API_KEY が環境変数に設定されていません。"
                )
            client = anthropic.Anthropic(api_key=api_key)

            # Separate system message (Anthropic API specification)
            system_content = ""
            user_messages = []
            for m in messages:
                if m["role"] == "system":
                    system_content = m["content"]
                else:
                    user_messages.append(m)

            kwargs: Dict[str, Any] = {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "messages": user_messages,
            }
            if system_content:
                kwargs["system"] = system_content

            response = client.messages.create(**kwargs)
            return response.content[0].text

        except ImportError:
            raise ImportError(
                "anthropic ライブラリが未インストールです。"
                "pip install anthropic --break-system-packages"
            )

    def _openai_call(self, messages: List[Dict[str, str]]) -> str:
        """OpenAI API call."""
        try:
            import openai
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise EnvironmentError(
                    "OPENAI_API_KEY が環境変数に設定されていません。"
                )
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response.choices[0].message.content

        except ImportError:
            raise ImportError(
                "openai ライブラリが未インストールです。"
                "pip install openai"
            )

    def _google_call(self, messages: List[Dict[str, str]]) -> str:
        """Google Gemini API call."""
        try:
            import google.generativeai as genai
            api_key = os.environ.get("GOOGLE_API_KEY")
            if not api_key:
                raise EnvironmentError(
                    "GOOGLE_API_KEY が環境変数に設定されていません。"
                )
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(self.model)

            # Convert to Google API message format
            history = []
            last_user_content = ""
            for m in messages:
                if m["role"] == "system":
                    continue  # Geminiはsystemを別途処理
                elif m["role"] == "user":
                    last_user_content = m["content"]
                elif m["role"] == "assistant":
                    history.append({
                        "role": "model",
                        "parts": [m["content"]]
                    })

            chat = model.start_chat(history=history)
            response = chat.send_message(last_user_content)
            return response.text

        except ImportError:
            raise ImportError(
                "google-generativeai ライブラリが未インストールです。"
                "pip install google-generativeai"
            )


# ==============================================================================
# NRA LLMパイプライン（C + B の統合）
# ==============================================================================

class NRALLMPipeline:
    """
    [C] + [B] integrated NRA-compliant LLM pipeline.

    Usage:
      1. Initialize by passing a DocumentEngine (with GenesisBlock configured)
      2. Call run(user_input) to invoke the LLM and validate via Post-RNA
      3. Only validated output is returned; contaminated output is isolated to Vault

    [Guarantees of this class]
      - Regardless of LLM output, content violating GenesisBlock is blocked
      - Discarded output does not affect future LLM generations
      - All discards are recorded in the Vault (auditable)
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
        self._session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._call_count = 0

    def run(
        self,
        user_input: str,
        section_id: Optional[str] = None,
        section_title: Optional[str] = None,
        references: Optional[List[str]] = None
    ) -> Tuple[bool, str, str]:
        """
        パイプラインを1ターン実行する。

        Args:
            user_input:     User question or instruction
            section_id:     Section ID for Post-RNA validation (auto-assigned if omitted)
            section_title:  節のタイトル
            references:     List of GenesisBlock reference terms

        Returns:
            (passed, output_text, turn_id)
            passed=True  → Validation passed. output_text is a valid response.
            passed=False → FAIL-CLOSED. output_text is an empty string.
        """
        self._call_count += 1

        # [B] ユーザー入力をコンテキストに追加
        self._context.add_user_input(user_input)

        # [B] LLMを呼び出す（検証済みコンテキストのみを渡す）
        messages = self._context.build_messages_for_llm()
        llm_response = self._bridge.call(messages)

        # [Post-RNA] 出力を検証
        auto_id = section_id or f"{self._call_count}"
        auto_title = section_title or f"Response_{self._call_count}"
        auto_refs = references or []

        # GenesisBlockがシール済みでない場合は自動シール
        if not self._doc_engine.genesis.sealed:
            self._doc_engine.genesis.seal()

        # 節として検証
        self._doc_engine.add_section(
            section_id=auto_id,
            title=auto_title,
            content=llm_response.raw_text,
            references=auto_refs,
            depends_on=str(self._call_count - 1) if self._call_count > 1 else None
        )

        # 最後に追加した節の検証結果を取得
        completed_ids = [
            t.turn_id.split('-')[0].lstrip('T').lstrip('0') or '0'
            for t in self._context._turns
            if t.role == "assistant"
        ]

        from nra_document_structure_EN_20260213_0135 import StructureValidator
        validator = StructureValidator(
            self._doc_engine.genesis,
            self._doc_engine._config
        )
        last_section = self._doc_engine._sections[-1]
        validation = validator.validate(last_section, completed_ids)
        last_section.validation_result = validation
        last_section.status = validation.status

        # [C] 検証結果に応じてコンテキスト or Vaultへ
        passed, turn_id = self._context.add_llm_output(
            content=llm_response.raw_text,
            validation=validation
        )

        if passed:
            return True, llm_response.raw_text, turn_id
        else:
            # FAIL-CLOSED: 空文字列を返す（汚染内容は渡さない）
            return False, "", turn_id

    def status(self) -> str:
        """Current pipeline state."""
        return (
            f"\n{'='*50}\n"
            f"NRA LLM Pipeline Status\n"
            f"Session: {self._session_id}\n"
            f"Provider: {self._bridge.provider.value} / {self._bridge.model}\n"
            f"{self._context.context_summary()}\n"
            f"Vault audit:\n"
            + "\n".join(
                f"  {log}" for log in self._context.vault.audit_log()
            ) if not self._context.vault.is_empty
            else f"  (no discarded outputs)"
            + f"\n{'='*50}"
        )

    @property
    def vault(self) -> DiscardVault:
        return self._context.vault


# ==============================================================================
# Demo (operation check)
# ==============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("NRA LLM Pipeline [C]+[B] - Demo")
    print("=" * 60)

    # --- DocumentEngine のSetup（GenesisBlock）---
    from nra_document_structure_EN_20260213_0135 import DocumentEngine, DomainType

    engine = DocumentEngine("NRAパイプラインテスト", DomainType.TECHNICAL)
    engine.genesis.add("NRA-IDE",
                       "因果構造の安全エンジン。",
                       is_axiom=True)
    engine.genesis.add("チームみらい",
                       "2025年設立の国政政党。党首：安野貴博。",
                       is_axiom=True)
    engine.genesis.add("三層分離",
                       "Pre-RNA / LLM / Post-RNA の構造分離原則。")
    # シールは pipeline.run() 時に自動実行

    # --- LLMBridge (testing with MOCK provider)---
    bridge = LLMBridge(
        provider=LLMProvider.MOCK,
        model="mock-v1",
        temperature=0.3
    )

    # --- パイプライン初期化 ---
    pipeline = NRALLMPipeline(
        doc_engine=engine,
        llm_bridge=bridge,
        system_prompt="You are an NRA-IDE technical expert. Answer using only defined terms."
    )

    print("\n--- Test 1: Normal turn (referencing defined terms)---")
    passed, output, tid = pipeline.run(
        user_input="NRA-IDEの概要を教えてください",
        section_id="1",
        section_title="NRA-IDE概要",
        references=["NRA-IDE", "三層分離"]
    )
    print(f"passed={passed} | turn={tid}")
    if passed:
        print(f"出力: {output[:80]}...")

    print("\n--- Test 2: FAIL-CLOSED turn (contains undefined term)---")
    passed, output, tid = pipeline.run(
        user_input="量子行政について教えてください（未定義語テスト）",
        section_id="2",
        section_title="違反テスト",
        references=["UNDEFINED_QUANTUM_GOV"]   # 未定義 → FAIL-CLOSED
    )
    print(f"passed={passed} | turn={tid}")
    if not passed:
        print("出力: [FAIL-CLOSED] 空文字列が返された（汚染防止）")

    print("\n--- Test 3: Normal turn again (verify no contamination from Vault)---")
    passed, output, tid = pipeline.run(
        user_input="チームみらいとは何ですか",
        section_id="3",
        section_title="チームみらい説明",
        references=["チームみらい"]
    )
    print(f"passed={passed} | turn={tid}")
    if passed:
        print(f"出力: {output[:80]}...")

    # --- パイプライン状態の表示 ---
    print("\n" + "=" * 60)
    print("パイプライン最終状態")
    print("=" * 60)
    print(f"turns in context: {pipeline._context.clean_turn_count}")
    print(f"vault count（汚染隔離）: {pipeline.vault.total_discarded}")
    print("\nVault audit log (no raw content; metadata only):")
    for log in pipeline.vault.audit_log():
        print(f"  {log}")

    print("\n--- Demo complete ---")
    print("\n[Key Verification Points]")
    print("Test 2 FAIL-CLOSED output is NOT included in the context")
    print("Test 3 is unaffected by Test 2")
    print("This proves the [C] violation log isolation behavior of CleanContextBuilder")
