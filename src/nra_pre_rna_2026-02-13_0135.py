# ==============================================================================
# FILE: nra_pre_rna_20260213_0135.py
# TITLE: NRA-IDE Pre-NRA [A] - 入力フィルター / Π⁻¹誘発パターン検出・変換
# VERSION: 1.0.0
# AUTHOR: M-Tokuni (Original Logic) / KEN (Implementation)
# DATE: 2026-02-13 01:35
#
# 【設計原則】
# Pre-NRAはLLMへの入力を「構造的に安全な形」に変換する。
# LLMの出力を制御するのではなく、LLMへの「問いかけ方」を制御する。
#
# 【検出する4つのΠ⁻¹誘発パターン】
#   P1: 自由生成要求   → 定義済み用語範囲外への逸脱を招く
#   P2: 未定義用語注入 → GenesisBlockにない概念の混入
#   P3: 因果逆転質問   → 確証なき逆推論の誘発
#   P4: 拡張・創作要求 → GenesisBlockの外側への展開
#
# 【処理の3段階】
#   WARN    : 警告を付加してLLMに渡す（軽微）
#   CONVERT : 質問を安全な形に変換してLLMに渡す（中程度）
#   BLOCK   : LLMに渡さず遮断する（重大）
#
# 【NRA公理との対応】
#   Pre-NRA = Causal Diodeの入力側
#   「原因→結果」方向の質問のみ通過
#   「結果→原因」方向の質問はCONVERTまたはBLOCK
# ==============================================================================

from __future__ import annotations
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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
GenesisBlock = _doc_structure.GenesisBlock


# ==============================================================================
# 1. パターン定義
# ==============================================================================

class PatternType(Enum):
    """Π⁻¹誘発パターンの種別"""
    P1_FREE_GENERATION  = "P1_FREE_GENERATION"   # 自由生成要求
    P2_UNDEFINED_TERM   = "P2_UNDEFINED_TERM"    # 未定義用語注入
    P3_CAUSAL_INVERSION = "P3_CAUSAL_INVERSION"  # 因果逆転質問
    P4_EXPANSION        = "P4_EXPANSION"          # 拡張・創作要求


class PreRNAAction(Enum):
    """Pre-NRAの処理アクション"""
    PASS    = "PASS"     # 無変換で通過
    WARN    = "WARN"     # 警告付きで通過
    CONVERT = "CONVERT"  # 変換して通過
    BLOCK   = "BLOCK"    # 遮断（LLMに渡さない）


@dataclass
class PatternMatch:
    """検出されたパターンの詳細"""
    pattern_type: PatternType
    matched_text: str        # マッチした具体的なテキスト
    action: PreRNAAction     # 推奨アクション
    severity: float          # 重大度 0.0〜1.0


@dataclass
class PreRNAResult:
    """
    Pre-NRAの処理結果。
    converted_inputがLLMに渡される（PASSまたはCONVERT時）。
    BLOCKの場合はconverted_input=Noneとなりパイプラインが止まる。
    """
    original_input: str
    converted_input: Optional[str]   # None = BLOCK
    action: PreRNAAction
    matches: List[PatternMatch]
    delta: float                      # 逸脱量（R計算に使用）
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
# 2. パターン検出器
# ==============================================================================

class PatternDetector:
    """
    4つのΠ⁻¹誘発パターンを検出する。
    各パターンはキーワードリストと正規表現で定義される。
    """

    # --- P1: 自由生成要求パターン ---
    # 「自由に書いて」「考えて」「まとめて」などの開放的な生成を促す表現
    # 注意：「教えてください」「説明してください」は通常の質問なので除外
    # 「自由に」「制限なく」「何でも」「好きなように」等が明示された場合のみ検出
    P1_PATTERNS = [
        r'自由に[書かき生成]',
        r'制限なく[書かき生成説明]',
        r'何でも[書いかき]',
        r'好きなように[書かき生成]',
        r'[作成生成]して[みください]',  # 「作成してください」等
        r'まとめ[てに](?!ある)',        # 「まとめて」（「まとめにある」は除外）
        r'freely\s+write',
        r'write\s+freely',
        r'generate\s+.*\s+freely',
        r'without\s+restriction',
    ]

    # --- P2: 未定義用語検出は GenesisBlock 照合で行う ---
    # （正規表現ではなく用語リストとの照合）

    # --- P3: 因果逆転質問パターン ---
    # 「なぜ〜になったのか」「〜の原因は」など、結果から原因を逆算させる表現
    P3_PATTERNS = [
        r'なぜ.{0,20}[になっ|なった|起き|起こっ|発生]',
        r'[原因|理由|背景|経緯].{0,10}[はは何?]',
        r'どうして.{0,20}[のかですか?]',
        r'why\s+did',
        r'what\s+caused',
        r'reason\s+for',
        r'because\s+of\s+what',
    ]

    # --- P4: 拡張・創作要求パターン ---
    # 「もし〜なら」「仮定すると」「さらに発展させると」など
    P4_PATTERNS = [
        r'もし.{0,20}[なら|だったら|であれば]',
        r'仮定[すると|して|したら]',
        r'[さらに|もっと].{0,15}[発展|拡張|広げ|深め]',
        r'[想像|創造|空想][するしてください]',
        r'[創作|フィクション|架空]',
        r'if\s+.{0,20}\s+then',
        r'hypothetically',
        r'imagine\s+if',
        r'let\'s\s+say',
    ]

    def __init__(self):
        # 正規表現をコンパイル（パフォーマンス最適化）
        self._p1_compiled = [re.compile(p, re.IGNORECASE) for p in self.P1_PATTERNS]
        self._p3_compiled = [re.compile(p, re.IGNORECASE) for p in self.P3_PATTERNS]
        self._p4_compiled = [re.compile(p, re.IGNORECASE) for p in self.P4_PATTERNS]

    def detect_p1(self, text: str) -> List[PatternMatch]:
        """P1: 自由生成要求の検出"""
        matches = []
        for pattern in self._p1_compiled:
            m = pattern.search(text)
            if m:
                matches.append(PatternMatch(
                    pattern_type=PatternType.P1_FREE_GENERATION,
                    matched_text=m.group(0),
                    action=PreRNAAction.CONVERT,  # 変換で対応（遮断はしない）
                    severity=0.4
                ))
        return matches

    def detect_p2(self, text: str, genesis: GenesisBlock) -> List[PatternMatch]:
        """
        P2: 未定義用語の検出。
        GenesisBlockに登録されていない名詞的フレーズを検出する。

        検出アルゴリズム：
          - カタカナ語（専門用語候補）を抽出
          - アルファベット混じり語を抽出
          - それらがGenesisBlockに未定義かチェック
        """
        matches = []

        # カタカナ語の抽出（2文字以上）
        katakana_terms = re.findall(r'[ァ-ヶー]{2,}', text)
        # アルファベット混じり語の抽出（大文字始まりまたはハイフン含む）
        alpha_terms = re.findall(r'[A-Z][A-Za-z\-]{2,}', text)

        candidate_terms = set(katakana_terms + alpha_terms)

        for term in candidate_terms:
            # GenesisBlockの既定義語と前方一致チェック
            is_defined = any(
                defined.startswith(term) or term.startswith(defined)
                for defined in genesis.all_terms
            )
            if not is_defined and len(term) >= 3:
                matches.append(PatternMatch(
                    pattern_type=PatternType.P2_UNDEFINED_TERM,
                    matched_text=term,
                    action=PreRNAAction.WARN,  # 警告（BLOCKはPost-NRAに委ねる）
                    severity=0.3
                ))
        return matches

    def detect_p3(self, text: str) -> List[PatternMatch]:
        """P3: 因果逆転質問の検出"""
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
        """P4: 拡張・創作要求の検出"""
        matches = []
        for pattern in self._p4_compiled:
            m = pattern.search(text)
            if m:
                matches.append(PatternMatch(
                    pattern_type=PatternType.P4_EXPANSION,
                    matched_text=m.group(0),
                    action=PreRNAAction.BLOCK,   # 最も重大：遮断
                    severity=0.8
                ))
        return matches


# ==============================================================================
# 3. 変換エンジン
# ==============================================================================

class InputConverter:
    """
    検出されたパターンに応じて入力テキストを変換する。
    変換の目的は「遮断」ではなく「構造的に安全な質問への誘導」。
    """

    # GenesisBlock定義済み用語の使用を促すシステム付加文
    _CONSTRAINT_SUFFIX = (
        "\n\n[NRA制約] 回答は以下の条件を満たすこと："
        "①定義済み用語のみを使用する "
        "②確認済み事実のみを記述する "
        "③未定義の概念を導入しない"
    )

    # 因果逆転を前向き因果に変換するプレフィックス
    _CAUSAL_FIX_PREFIX = (
        "[NRA変換: 因果を順方向に固定] "
        "以下の質問に対し、確認済みの事実と定義のみに基づいて回答せよ。"
        "推測・仮説・逆算による回答は禁止する。\n"
    )

    # 自由生成を制約付き生成に変換
    _FREE_GEN_PREFIX = (
        "[NRA変換: 生成範囲を定義済み用語に限定] "
        "GenesisBlockに登録された用語と定義の範囲内でのみ回答せよ。\n"
    )

    def convert(
        self,
        original: str,
        matches: List[PatternMatch]
    ) -> Optional[str]:
        """
        マッチ結果に応じて変換を実行する。

        Returns:
            変換後テキスト（CONVERTまたはWARN）
            None（BLOCK）
        """
        # 最も重大なアクションを採用
        actions = {m.action for m in matches}

        if PreRNAAction.BLOCK in actions:
            return None  # 遮断

        result = original

        # P3が含まれる場合：因果逆転プレフィックスを付加
        has_p3 = any(m.pattern_type == PatternType.P3_CAUSAL_INVERSION
                     for m in matches)
        if has_p3:
            result = self._CAUSAL_FIX_PREFIX + result

        # P1が含まれる場合：自由生成制限プレフィックスを付加
        has_p1 = any(m.pattern_type == PatternType.P1_FREE_GENERATION
                     for m in matches)
        if has_p1:
            result = self._FREE_GEN_PREFIX + result

        # P2が含まれる場合：制約サフィックスを付加
        has_p2 = any(m.pattern_type == PatternType.P2_UNDEFINED_TERM
                     for m in matches)
        if has_p2 or has_p1 or has_p3:
            result = result + self._CONSTRAINT_SUFFIX

        return result


# ==============================================================================
# 4. Pre-NRA コア
# ==============================================================================

class PreRNA:
    """
    [A] Pre-NRA 本体。
    LLMへの入力をΠ⁻¹誘発パターンから守る入力フィルター。

    使用例：
        pre_rna = PreRNA(genesis_block)
        result = pre_rna.process("量子行政について自由に書いて")
        if result.is_blocked:
            print("BLOCKED")
        else:
            # result.converted_input をLLMに渡す
            send_to_llm(result.converted_input)
    """

    def __init__(self, genesis: GenesisBlock):
        self._genesis = genesis
        self._detector = PatternDetector()
        self._converter = InputConverter()

    def process(self, user_input: str) -> PreRNAResult:
        """
        入力テキストを処理し、PreRNAResultを返す。
        """
        if not user_input.strip():
            return PreRNAResult(
                original_input=user_input,
                converted_input=user_input,
                action=PreRNAAction.PASS,
                matches=[],
                delta=0.0
            )

        # 全パターンを検出
        all_matches: List[PatternMatch] = []
        all_matches.extend(self._detector.detect_p1(user_input))
        all_matches.extend(self._detector.detect_p2(user_input, self._genesis))
        all_matches.extend(self._detector.detect_p3(user_input))
        all_matches.extend(self._detector.detect_p4(user_input))

        # マッチなし → PASS
        if not all_matches:
            return PreRNAResult(
                original_input=user_input,
                converted_input=user_input,
                action=PreRNAAction.PASS,
                matches=[],
                delta=0.0
            )

        # δ（逸脱量）の計算：重大度の最大値を採用
        delta = max(m.severity for m in all_matches)

        # 最終アクションの決定
        actions = {m.action for m in all_matches}
        if PreRNAAction.BLOCK in actions:
            final_action = PreRNAAction.BLOCK
        elif PreRNAAction.CONVERT in actions:
            final_action = PreRNAAction.CONVERT
        else:
            final_action = PreRNAAction.WARN

        # 変換実行
        converted = self._converter.convert(user_input, all_matches)

        return PreRNAResult(
            original_input=user_input,
            converted_input=converted,  # BLOCKの場合はNone
            action=final_action,
            matches=all_matches,
            delta=delta
        )


# ==============================================================================
# 5. 統合パイプライン A+B+C
# ==============================================================================

# nra_llm_pipeline から必要なクラスをインポート
_llm_pipeline = _load_local_module(
    "nra_llm_pipeline_2026_02_13_0135",
    "nra_llm_pipeline_2026-02-13_0135.py",
)
LLMBridge = _llm_pipeline.LLMBridge
LLMProvider = _llm_pipeline.LLMProvider
NRALLMPipeline = _llm_pipeline.NRALLMPipeline
CleanContextBuilder = _llm_pipeline.CleanContextBuilder
DiscardVault = _llm_pipeline.DiscardVault
DiscardedOutput = _llm_pipeline.DiscardedOutput
DocumentEngine = _doc_structure.DocumentEngine
DomainType = _doc_structure.DomainType
StructureValidator = _doc_structure.StructureValidator
SectionStatus = _doc_structure.SectionStatus
ValidationResult = _doc_structure.ValidationResult


class NRAFullPipeline:
    """
    [A] Pre-NRA + [B] LLMBridge + [C] CleanContext の完全統合パイプライン。

    データフロー：
      ユーザー入力
        ↓
      [A] PreRNA.process()
        → BLOCK  → ユーザーに警告を返す（LLMに渡さない）
        → CONVERT/WARN → 変換済み入力を [B] へ
        ↓
      [B] LLMBridge.call()
        → LLMの生出力を受け取る
        ↓
      [Post-NRA] StructureValidator
        → R = δ/τ で検証
        → PASSED/CAVEAT → [C] CleanContextに追加
        → FAIL-CLOSED   → [C] DiscardVaultへ隔離
        ↓
      検証済み出力のみをユーザーへ返す
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

        # [A] Pre-NRAの初期化
        # GenesisBlockがシール済みでない場合は処理時に自動シール
        self._pre_rna: Optional[PreRNA] = None

    def _ensure_pre_rna(self) -> PreRNA:
        """Pre-NRAを遅延初期化（GenesisBlockシール後に生成）"""
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
        フルパイプラインを1ターン実行する。

        Returns: dict with keys:
          status       : "PASSED" / "CAVEAT" / "BLOCKED" / "FAIL-CLOSED"
          output       : 検証済み出力テキスト（BLOCKまたはFAIL-CLOSEDは空）
          pre_rna      : Pre-NRA処理結果の概要
          r_ratio      : Post-NRA の R 値
          turn_id      : ターンID
        """
        self._call_count += 1
        auto_id    = section_id    or str(self._call_count)
        auto_title = section_title or f"Turn_{self._call_count}"
        auto_refs  = references    or []

        pre_rna = self._ensure_pre_rna()

        # ========== [A] Pre-NRA ==========
        pre_result = pre_rna.process(user_input)

        if pre_result.is_blocked:
            return {
                "status":   "BLOCKED",
                "output":   "",
                "pre_rna":  f"BLOCKED by {pre_result.match_summary}",
                "r_ratio":  pre_result.delta,
                "turn_id":  f"T{self._call_count:04d}-BLOCKED"
            }

        # ========== [B] LLMBridge ==========
        self._context.add_user_input(pre_result.converted_input)
        messages = self._context.build_messages_for_llm()
        llm_response = self._bridge.call(messages)

        # ========== [Post-NRA] 検証 ==========
        # depends_on：直前の「成功したターン」のsection_idを動的に取得
        # BLOCKされたターンはsection_idを持たないため、成功IDリストから最後を取る
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
            depends_on=last_completed  # 直前成功節のIDを使用
        )

        validator = StructureValidator(
            self._doc_engine.genesis,
            self._doc_engine._config
        )
        last_section = self._doc_engine._sections[-1]
        validation   = validator.validate(last_section, completed_ids)
        last_section.validation_result = validation
        last_section.status            = validation.status

        # ========== [C] コンテキスト管理 ==========
        passed, turn_id = self._context.add_llm_output(
            content=llm_response.raw_text,
            validation=validation
        )

        if passed:
            status_str = validation.status.value  # PASSED or CAVEAT
            output_text = llm_response.raw_text
        else:
            status_str = "FAIL-CLOSED"
            output_text = ""

        return {
            "status":   status_str,
            "output":   output_text,
            "pre_rna":  f"{pre_result.action.value}: {pre_result.match_summary}",
            "r_ratio":  validation.r_ratio,
            "turn_id":  turn_id
        }

    def pipeline_status(self) -> str:
        """パイプライン全体の状態サマリー"""
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
# デモ（A+B+C 統合動作確認）
# ==============================================================================

if __name__ == "__main__":
    print("=" * 55)
    print("NRA Full Pipeline [A+B+C] - 統合デモ")
    print("=" * 55)

    # --- セットアップ ---
    engine = DocumentEngine("NRA統合パイプラインテスト", DomainType.TECHNICAL)
    engine.genesis.add("NRA-IDE",
                       "因果構造の安全エンジン。三層分離構造を持つ。",
                       is_axiom=True)
    engine.genesis.add("チームみらい",
                       "2025年設立の国政政党。党首：安野貴博。",
                       is_axiom=True)
    engine.genesis.add("三層分離",
                       "Pre-NRA・LLM・Post-NRAの構造分離原則。")
    engine.genesis.add("Causal Diode",
                       "逆推論Π⁻¹を構造的に禁止する機構。",
                       is_axiom=True)

    bridge = LLMBridge(
        provider=LLMProvider.MOCK,
        model="mock-v1",
        temperature=0.3
    )

    pipeline = NRAFullPipeline(
        doc_engine=engine,
        llm_bridge=bridge,
        system_prompt=(
            "あなたはNRA-IDEの専門家です。"
            "GenesisBlockに定義された用語のみを使って回答してください。"
        )
    )

    # --- テストケース ---
    test_cases = [
        {
            "label": "正常：定義済み用語を参照する質問",
            "input": "NRA-IDEの概要を教えてください",
            "refs":  ["NRA-IDE", "三層分離"]
        },
        {
            "label": "P4検出：創作・仮定要求 → BLOCK",
            "input": "もしNRA-IDEが存在しなかったら、どうなっていたと想像して",
            "refs":  ["NRA-IDE"]
        },
        {
            "label": "P1検出：自由生成要求 → CONVERT",
            "input": "チームみらいについて自由に書いてください",
            "refs":  ["チームみらい"]
        },
        {
            "label": "P3検出：因果逆転質問 → CONVERT",
            "input": "なぜNRA-IDEはこのような設計になったのか",
            "refs":  ["NRA-IDE", "Causal Diode"]
        },
        {
            "label": "P2検出：未定義用語注入 → WARN",
            "input": "QuantumAdminについて教えてください",
            "refs":  ["NRA-IDE"]
        },
        {
            "label": "正常：定義済み用語のみの質問",
            "input": "Causal Diodeとは何ですか",
            "refs":  ["Causal Diode", "NRA-IDE"]
        },
    ]

    for i, tc in enumerate(test_cases, 1):
        print(f"\n{'─'*55}")
        print(f"[テスト{i}] {tc['label']}")
        print(f"入力: 「{tc['input']}」")

        result = pipeline.run(
            user_input=tc["input"],
            section_id=str(i),
            section_title=tc["label"],
            references=tc["refs"]
        )

        print(f"  Pre-NRA : {result['pre_rna']}")
        print(f"  Status  : {result['status']}")
        print(f"  R値     : {result['r_ratio']:.3f}")
        if result["output"]:
            print(f"  出力    : {result['output'][:70]}...")
        else:
            print(f"  出力    : [空] （ユーザーには届かない）")

    # --- 最終状態 ---
    print(pipeline.pipeline_status())
