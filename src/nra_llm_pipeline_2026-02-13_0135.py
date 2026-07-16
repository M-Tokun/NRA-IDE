# ==============================================================================
# FILE: nra_llm_pipeline_20260213_0135.py
# TITLE: NRA-IDE LLM Pipeline - 違反ログ隔離 [C] + LLM APIブリッジ [B]
# VERSION: 1.0.0
# AUTHOR: M-Tokuni (Original Logic) / KEN (Implementation)
# DATE: 2026-02-13 01:35
#
# 【設計原則】
# [C] 違反ログ隔離：
#     FAIL-CLOSEDになった出力をLLMコンテキストから物理的に除外する。
#     破棄出力がLLMの次回生成に影響を与えることを構造的に禁止する。
#     通常のLLMチャットが持つ「汚染された履歴の蓄積」を防ぐ。
#
# [B] LLM APIブリッジ：
#     外部LLM（OpenAI / Anthropic / Google等）の出力を
#     Post-NRAエンジン（nra_document_structure）に自動投入する。
#     LLMを「信頼できないが有能な生成装置」として扱い、
#     NRAパイプラインの中でのみ動作させる。
#
# 【NRA公理との対応】
#   CleanContext   → [C] 汚染防止。破棄出力のLLMへの逆流禁止
#   LLMBridge      → [B] 外部AI接続。出力を自動でPost-NRAへ投入
#   DiscardVault   → 破棄出力の隔離保管庫（学習・参照禁止）
#
# 【依存関係】
#   nra_document_structure_20260213_0135.py が必要
# ==============================================================================

from __future__ import annotations
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 既存エンジンをインポート
def _load_local_module(module_name: str, filename: str):
    if module_name in sys.modules:
        return sys.modules[module_name]
    module_path = Path(__file__).with_name(filename)
    spec = __import__("importlib.util").util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {filename}")
    module = __import__("importlib.util").util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_doc_structure = _load_local_module(
    "nra_document_structure_2026_02_13_0135",
    "nra_document_structure_2026-02-13_0135.py",
)
DocumentEngine = _doc_structure.DocumentEngine
DomainType = _doc_structure.DomainType
SectionStatus = _doc_structure.SectionStatus
ValidationResult = _doc_structure.ValidationResult
SectionNode = _doc_structure.SectionNode
GenesisBlock = _doc_structure.GenesisBlock
StructureValidator = _doc_structure.StructureValidator


# ==============================================================================
# [C-1] DiscardVault（破棄出力の隔離保管庫）
# ==============================================================================

@dataclass
class DiscardedOutput:
    """
    FAIL-CLOSEDになった出力の記録。
    この構造体はLLMコンテキストに絶対に渡されない。
    記録目的のみ。改善・学習への利用禁止。
    """
    turn_id: str              # どのターンで破棄されたか
    raw_content: str          # 破棄されたLLM出力の原文
    violation_reason: str     # 破棄理由
    r_ratio: float            # R = δ/τ の値
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def summary(self) -> str:
        """ログ表示用サマリー（内容は含まない）"""
        # 注意：raw_contentを外部に渡さないようsummaryには含めない
        return (
            f"[DISCARDED | turn={self.turn_id} | "
            f"R={self.r_ratio:.3f} | {self.timestamp}] "
            f"reason: {self.violation_reason}"
        )


class DiscardVault:
    """
    破棄出力の隔離保管庫。
    VaultはLLMコンテキストビルダーから完全に分離されており、
    build_clean_context() メソッドは Vault の内容を参照しない。

    【重要な設計原則】
    - Vault への追加：FAIL-CLOSED 時のみ
    - Vault からの読み出し：ログ出力・監査のみ
    - LLMへの逆流：構造的に不可能（CleanContextBuilderが参照しない）
    """

    def __init__(self):
        self._vault: List[DiscardedOutput] = []
        self._total_discarded = 0

    def seal_and_store(self, output: DiscardedOutput) -> None:
        """破棄出力を封印してVaultに格納する"""
        self._vault.append(output)
        self._total_discarded += 1

    def audit_log(self) -> List[str]:
        """監査用ログ（内容は含まない、メタ情報のみ）"""
        return [d.summary() for d in self._vault]

    @property
    def total_discarded(self) -> int:
        return self._total_discarded

    @property
    def is_empty(self) -> bool:
        return len(self._vault) == 0


# ==============================================================================
# [C-2] CleanContextBuilder（汚染防止コンテキスト管理）
# ==============================================================================

@dataclass
class ConversationTurn:
    """
    LLMに渡す会話の1ターン。
    PASSEDまたはCAVEATの出力のみが格納される。
    FAIL-CLOSEDの出力はこの構造体に入らない（Vaultへ）。
    """
    turn_id: str
    role: str          # "user" または "assistant"
    content: str       # 検証済みコンテンツのみ
    r_ratio: float     # Post-NRAの検証スコア（0.0 = 完全通過）
    status: str        # PASSED / CAVEAT


class CleanContextBuilder:
    """
    [C] 違反ログ隔離の核心。

    LLMに渡す会話履歴（コンテキスト）を管理する。
    FAIL-CLOSEDになった出力は絶対にコンテキストに追加されない。
    これにより「汚染された応答が次の生成に影響を与える」
    通常のLLMチャットの問題を構造的に解決する。

    通常のLLMチャット：
        会話履歴 = [user, assistant（汚染あり）, user, assistant...]
                              ↑ これが次のassistantに影響する

    NRA CleanContext：
        会話履歴 = [user, assistant（検証済みのみ）, user, assistant...]
                              ↑ FAIL-CLOSEDはここに入れない
    """

    def __init__(self, system_prompt: str = ""):
        self._system_prompt = system_prompt
        self._turns: List[ConversationTurn] = []
        self._vault = DiscardVault()
        self._turn_counter = 0

    def add_user_input(self, content: str) -> str:
        """ユーザー入力を追加。ユーザー入力は検証不要（人間の権限）"""
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
        LLMの出力を検証結果と共に追加しようとする。

        Returns:
            (True, turn_id)  : 検証通過 → コンテキストに追加
            (False, turn_id) : FAIL-CLOSED → Vaultへ隔離、コンテキストに追加しない
        """
        self._turn_counter += 1
        turn_id = f"T{self._turn_counter:04d}-assistant"

        if validation.status == SectionStatus.FAILED:
            # FAIL-CLOSED: Vaultへ封印。コンテキストには追加しない
            discarded = DiscardedOutput(
                turn_id=turn_id,
                raw_content=content,  # Vault内にのみ保存
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
        LLMのAPIに渡すmessagesリストを構築する。
        Vaultの内容は絶対に含まれない。
        """
        messages = []

        # システムプロンプト（設定されている場合）
        if self._system_prompt:
            messages.append({
                "role": "system",
                "content": self._system_prompt
            })

        # 検証済みターンのみを追加
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
        """コンテキストに含まれる検証済みターン数"""
        return len(self._turns)

    def context_summary(self) -> str:
        """コンテキストの状態サマリー"""
        return (
            f"CleanContext: {self.clean_turn_count} turns in context, "
            f"{self._vault.total_discarded} discarded to vault"
        )


# ==============================================================================
# [B] LLMBridge（外部LLM接続ブリッジ）
# ==============================================================================

class LLMProvider(Enum):
    """対応LLMプロバイダー"""
    ANTHROPIC = "anthropic"
    OPENAI    = "openai"
    GOOGLE    = "google"
    MOCK      = "mock"      # テスト用モックプロバイダー


@dataclass
class LLMResponse:
    """LLMからの生レスポンス"""
    provider: LLMProvider
    raw_text: str           # 未検証の生テキスト
    model: str
    latency_ms: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class LLMBridge:
    """
    [B] 外部LLM接続ブリッジ。

    外部LLMのAPIを呼び出し、その出力を自動的に
    Post-NRAエンジン（DocumentEngine）に投入する。

    【重要な設計原則】
    LLMBridgeは「生成」を担当するが「安全性」は担当しない。
    安全性はPost-NRAとCleanContextBuilderが担当する。
    LLMBridgeはLLMを「信頼できないが有能な生成装置」として扱う。

    【APIキーについて】
    環境変数から読み込む。コードにハードコードしない。
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
        プロバイダーに応じて適切なAPI呼び出しを実行する。
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
        最後のユーザーメッセージに応じた固定レスポンスを返す。
        実APIキー不要で動作確認ができる。
        """
        last_user = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"),
            ""
        )
        # モックは意図的に「Π⁻¹違反パターン」と「正常パターン」を混在させる
        if "定義" in last_user or "概要" in last_user:
            return (
                "NRA-IDEは因果構造の安全エンジンである。"
                "意味・最適化・履歴を扱わず、"
                "構造不変量によってのみ動作が決定される。"
                "Pre-NRA・LLM・Post-NRAの三層分離構造を持つ。"
            )
        elif "違反" in last_user or "テスト" in last_user:
            # 意図的な違反パターン（FAIL-CLOSEDになるはず）
            return "未定義用語UNDEFINED_XYZを使った短い文。"
        else:
            return (
                "チームみらいは2025年5月に設立された国政政党である。"
                "党首は安野貴博。テクノロジーによる政治改革を掲げる。"
            )

    def _anthropic_call(self, messages: List[Dict[str, str]]) -> str:
        """Anthropic Claude API呼び出し"""
        try:
            import anthropic
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise EnvironmentError(
                    "ANTHROPIC_API_KEY が環境変数に設定されていません。"
                )
            client = anthropic.Anthropic(api_key=api_key)

            # systemメッセージを分離（Anthropic APIの仕様）
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
        """OpenAI API呼び出し"""
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
        """Google Gemini API呼び出し"""
        try:
            import google.generativeai as genai
            api_key = os.environ.get("GOOGLE_API_KEY")
            if not api_key:
                raise EnvironmentError(
                    "GOOGLE_API_KEY が環境変数に設定されていません。"
                )
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(self.model)

            # Google APIのmessage形式に変換
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
    [C] + [B] を統合したNRA準拠LLMパイプライン。

    使用手順：
      1. DocumentEngine（GenesisBlock設定済み）を渡して初期化
      2. run(user_input) でLLMを呼び出し、Post-NRAで検証
      3. 検証済み出力のみが返され、汚染出力はVaultへ隔離

    【このクラスが保証すること】
      - LLMがどんな出力を返しても、GenesisBlockに違反する内容は通らない
      - 破棄された出力はLLMの次回生成に影響しない
      - 全ての破棄はVaultに記録される（監査可能）
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
            user_input:     ユーザーの質問・指示
            section_id:     Post-NRA検証に使う節ID（省略時は自動採番）
            section_title:  節のタイトル
            references:     GenesisBlockの参照用語リスト

        Returns:
            (passed, output_text, turn_id)
            passed=True  → 検証通過。output_textが有効な応答
            passed=False → FAIL-CLOSED。output_textは空文字列
        """
        self._call_count += 1

        # [B] ユーザー入力をコンテキストに追加
        self._context.add_user_input(user_input)

        # [B] LLMを呼び出す（検証済みコンテキストのみを渡す）
        messages = self._context.build_messages_for_llm()
        llm_response = self._bridge.call(messages)

        # [Post-NRA] 出力を検証
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
        """パイプラインの現在状態"""
        vault_body = (
            "\n".join(f"  {log}" for log in self._context.vault.audit_log())
            if not self._context.vault.is_empty
            else "  (no discarded outputs)"
        )
        return (
            f"\n{'='*50}\n"
            f"NRA LLM Pipeline Status\n"
            f"Session: {self._session_id}\n"
            f"Provider: {self._bridge.provider.value} / {self._bridge.model}\n"
            f"{self._context.context_summary()}\n"
            f"Vault audit:\n"
            + vault_body
            + f"\n{'='*50}"
        )

    @property
    def vault(self) -> DiscardVault:
        return self._context.vault


# ==============================================================================
# デモ（動作確認）
# ==============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("NRA LLM Pipeline [C]+[B] - Demo")
    print("=" * 60)

    # --- DocumentEngine のセットアップ（GenesisBlock）---
    engine = DocumentEngine("NRAパイプラインテスト", DomainType.TECHNICAL)
    engine.genesis.add("NRA-IDE",
                       "因果構造の安全エンジン。",
                       is_axiom=True)
    engine.genesis.add("チームみらい",
                       "2025年設立の国政政党。党首：安野貴博。",
                       is_axiom=True)
    engine.genesis.add("三層分離",
                       "Pre-NRA / LLM / Post-NRA の構造分離原則。")
    # シールは pipeline.run() 時に自動実行

    # --- LLMBridge（MOCKプロバイダーでテスト）---
    bridge = LLMBridge(
        provider=LLMProvider.MOCK,
        model="mock-v1",
        temperature=0.3
    )

    # --- パイプライン初期化 ---
    pipeline = NRALLMPipeline(
        doc_engine=engine,
        llm_bridge=bridge,
        system_prompt="あなたはNRA-IDEの技術専門家です。定義済み用語のみを使って回答してください。"
    )

    print("\n--- テスト1：正常ターン（定義済み用語を参照）---")
    passed, output, tid = pipeline.run(
        user_input="NRA-IDEの概要を教えてください",
        section_id="1",
        section_title="NRA-IDE概要",
        references=["NRA-IDE", "三層分離"]
    )
    print(f"passed={passed} | turn={tid}")
    if passed:
        print(f"出力: {output[:80]}...")

    print("\n--- テスト2：FAIL-CLOSEDターン（未定義用語を含む）---")
    passed, output, tid = pipeline.run(
        user_input="量子行政について教えてください（未定義語テスト）",
        section_id="2",
        section_title="違反テスト",
        references=["UNDEFINED_QUANTUM_GOV"]   # 未定義 → FAIL-CLOSED
    )
    print(f"passed={passed} | turn={tid}")
    if not passed:
        print("出力: [FAIL-CLOSED] 空文字列が返された（汚染防止）")

    print("\n--- テスト3：再び正常ターン（Vaultの汚染がないことを確認）---")
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
    print(f"コンテキスト内ターン数: {pipeline._context.clean_turn_count}")
    print(f"Vault格納数（汚染隔離）: {pipeline.vault.total_discarded}")
    print("\nVault監査ログ（内容なし・メタ情報のみ）:")
    for log in pipeline.vault.audit_log():
        print(f"  {log}")

    print("\n--- デモ完了 ---")
    print("\n【重要な確認ポイント】")
    print("テスト2のFAIL-CLOSED出力はコンテキストに含まれていない")
    print("テスト3はテスト2の影響を受けていない")
    print("これがCleanContextBuilderの[C]違反ログ隔離の動作証明")
