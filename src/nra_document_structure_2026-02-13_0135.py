# ==============================================================================
# FILE: nra_document_structure_20260213_0135.py
# TITLE: NRA-IDE Document Structure Engine - 構造文書生成・検証エンジン
# VERSION: 1.0.0
# AUTHOR: M-Tokuni (Original Logic) / KEN (Implementation)
# DATE: 2026-02-13 01:35
#
# 【設計原則】
# 本エンジンは NRA-IDE の公理を「構造文書の生成・検証」に適用する。
# 対象：設計書・仕様書・論文・報告書・議案・プロトコル（全ドメイン共通）
#
# 【NRA公理との対応】
#   GenesisBlock  → Causal Diode（定義の固定・逆推論禁止）
#   SectionNode   → Gear機構（前節確定→次節開放）
#   Validator     → R = δ/τ（逸脱量の定量判定）
#   FAIL-CLOSED   → 逸脱節の破棄（曖昧なまま通過させない）
#
# 【使い方】
#   1. DomainConfig でドメイン（医療/技術/法令 等）を設定
#   2. GenesisBlock に定義群を登録（ここが「公理」になる）
#   3. SectionNode を追加して文書を構築
#   4. DocumentEngine.build() で検証済み文書を生成
# ==============================================================================

from __future__ import annotations
import math
import sys
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# ==============================================================================
# 1. ドメイン設定（Domain Tuning）
# ==============================================================================

class DomainType(Enum):
    """
    対応ドメイン一覧。
    各ドメインで τ（制約の厳格度）と R_op（Fail-Closed閾値）が異なる。
    """
    TECHNICAL   = auto()  # 技術仕様書・設計書
    MEDICAL     = auto()  # 医療プロトコル・報告書
    ACADEMIC    = auto()  # 論文・技術白書
    LEGAL       = auto()  # 法令・規約・契約書
    GENERAL     = auto()  # 汎用（デフォルト）


@dataclass(frozen=True)
class DomainConfig:
    """
    ドメイン別パラメータ定義。
    frozen=True → 一度生成したら変更不可（Causal Diode として機能）

    tau:   制約の厚み。大きいほど逸脱に対して厳しい。
    r_op:  Fail-Closed 発動閾値（R = δ/τ がこれを超えたら破棄）
    allow_forward_ref: 前方参照（まだ定義されていない節への参照）を許容するか
    """
    domain: DomainType
    tau: float               # 制約厚み（0.0 〜 1.0）
    r_op: float              # Fail-Closed閾値（通常 0.6〜1.0）
    allow_forward_ref: bool  # 前方参照許容フラグ

    def __post_init__(self):
        # 不正値のガード（構造的に不正な設定を注入させない）
        if not (0.0 < self.tau <= 1.0):
            raise ValueError(f"tau must be in (0, 1]. Got: {self.tau}")
        if not (0.0 < self.r_op <= 1.0):
            raise ValueError(f"r_op must be in (0, 1]. Got: {self.r_op}")


# ドメイン別プリセット（Domain Tuning テーブル）
DOMAIN_PRESETS: Dict[DomainType, DomainConfig] = {
    DomainType.TECHNICAL: DomainConfig(
        domain=DomainType.TECHNICAL,
        tau=0.50,            # 中程度の厳格さ
        r_op=0.80,           # 技術的逸脱は厳しく検出
        allow_forward_ref=True  # 仕様書では前方参照が一般的
    ),
    DomainType.MEDICAL: DomainConfig(
        domain=DomainType.MEDICAL,
        tau=0.60,            # NRA-IDE標準閾値（生命安全基準）
        r_op=0.60,           # 即座にFail-Closed（ゼロ許容に近い）
        allow_forward_ref=False  # 医療では未定義への参照は禁止
    ),
    DomainType.ACADEMIC: DomainConfig(
        domain=DomainType.ACADEMIC,
        tau=0.55,
        r_op=0.75,
        allow_forward_ref=True   # 論文では先行研究への前方参照あり
    ),
    DomainType.LEGAL: DomainConfig(
        domain=DomainType.LEGAL,
        tau=0.70,            # 最も厳格（法令の曖昧さはゼロ許容）
        r_op=0.55,
        allow_forward_ref=False
    ),
    DomainType.GENERAL: DomainConfig(
        domain=DomainType.GENERAL,
        tau=0.41,            # バランス型
        r_op=0.65,
        allow_forward_ref=True
    ),
}


# ==============================================================================
# 2. Genesis Block（文書の公理 = 変更禁止の定義群）
# ==============================================================================

@dataclass
class DefinitionEntry:
    """
    単一の定義エントリ。
    term:       定義対象の用語
    definition: その定義内容（文字列）
    is_axiom:   True なら公理レベル（文書全体を通じて絶対に変更不可）
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
    文書の定義群を管理するクラス。
    NRA-IDE における「Causal Diode」の役割を担う。

    - 一度登録した公理（is_axiom=True）は変更不可
    - 定義されていない用語への参照を検出する
    - 後から矛盾する定義を注入しようとするとエラー
    """

    def __init__(self, domain_config: DomainConfig):
        self._config = domain_config
        self._definitions: Dict[str, DefinitionEntry] = {}
        self._sealed = False  # True になると新規追加不可

    def add(self, term: str, definition: str, is_axiom: bool = False) -> None:
        """定義を追加する。シール後は追加不可。"""
        if self._sealed:
            raise RuntimeError(
                f"GenesisBlock is sealed. Cannot add '{term}' after sealing."
            )
        if term in self._definitions:
            existing = self._definitions[term]
            if existing.is_axiom:
                # 公理の上書きは構造的に禁止（Causal Diode）
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
        GenesisBlockを封印する。
        これ以降、定義の追加・変更は一切禁止される。
        文書生成開始前に必ず呼ぶこと。
        """
        self._sealed = True

    def resolve(self, term: str) -> Optional[DefinitionEntry]:
        """用語の定義を照会する。未定義なら None を返す。"""
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
# 3. Section Node（文書の構造単位）
# ==============================================================================

class SectionStatus(Enum):
    PENDING   = "PENDING"    # 未検証
    PASSED    = "PASSED"     # 検証通過
    FAILED    = "FAILED"     # FAIL-CLOSED（破棄）
    CAVEAT    = "CAVEAT"     # 警告付き通過（Zone B）


@dataclass
class ValidationResult:
    """
    節の検証結果。
    R = δ/τ の計算結果と判定理由を保持する。
    """
    section_id: str
    delta: float           # ゆらぎ量（逸脱の大きさ）
    tau: float             # 制約厚み（ドメイン設定）
    r_ratio: float         # R = δ/τ
    status: SectionStatus
    violations: List[str]  # 検出された違反の一覧
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def zone(self) -> str:
        """Three-Zone Structure に基づくゾーン判定"""
        if self.r_ratio < 0.40:
            return "A (PERMIT)"
        elif self.r_ratio < 1.00:
            return "B (PERMIT_WITH_CAVEAT)"
        else:
            return "C (FAIL-CLOSED)"


@dataclass
class SectionNode:
    """
    文書の1節を表すクラス。
    Gear機構：前節が PASSED/CAVEAT でない限り、この節は評価されない。

    section_id:   節の識別子（例: "1.1", "2.3.1"）
    title:        節のタイトル
    content:      節の本文
    references:   この節が参照する定義・用語のリスト
    depends_on:   前節の section_id（Gear機構の依存関係）
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
# 4. Structure Validator（R = δ/τ による検証エンジン）
# ==============================================================================

class StructureValidator:
    """
    各節を GenesisBlock の定義群と照合し、構造的逸脱を定量化する。

    逸脱量 δ（delta）の算出基準：
      1. 未定義用語への参照     → δ += 0.40（重大違反）
      2. 前方参照（禁止設定時） → δ += 0.30
      3. 内容が空・極端に短い   → δ += 0.20
      4. 節IDの形式不正         → δ += 0.10
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
        節を検証し、ValidationResult を返す。

        completed_sections: すでに PASSED/CAVEAT になった節IDのリスト
                           （Gear機構の依存関係チェックに使用）
        """
        delta = 0.0
        violations: List[str] = []

        # --- [Check 1] Gear機構：依存節の完了チェック ---
        if section.depends_on is not None:
            if section.depends_on not in completed_sections:
                delta += 0.50
                violations.append(
                    f"GEAR_VIOLATION: depends_on '{section.depends_on}' "
                    f"is not yet completed."
                )

        # --- [Check 2] 参照用語の定義存在チェック ---
        for ref_term in section.references:
            if not self._genesis.is_defined(ref_term):
                if not self._config.allow_forward_ref:
                    # 前方参照禁止ドメインでは即座に重大違反
                    delta += 0.40
                    violations.append(
                        f"UNDEFINED_REF: '{ref_term}' is not defined in GenesisBlock."
                    )
                else:
                    # 前方参照許容ドメインでは軽微な警告
                    delta += 0.10
                    violations.append(
                        f"FORWARD_REF_WARNING: '{ref_term}' referenced before definition."
                    )

        # --- [Check 3] コンテンツ密度チェック ---
        # 内容が極端に薄い節は情報密度不足として検出
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

        # --- [Check 4] section_id 形式チェック ---
        # 期待形式：数字とピリオドで構成（例: "1", "2.1", "3.1.2"）
        import re
        if not re.match(r'^\d+(\.\d+)*$', section.section_id):
            delta += 0.10
            violations.append(
                f"FORMAT_VIOLATION: section_id '{section.section_id}' "
                f"should be numeric (e.g., '1.1', '2.3.1')."
            )

        # --- [Step 5] R = δ/τ の計算 ---
        tau = self._config.tau
        r_ratio = delta / tau if tau > 0 else float('inf')

        # --- [Step 6] Three-Zone 判定 ---
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
# 5. Document Engine（統合生成エンジン）
# ==============================================================================

@dataclass
class DocumentOutput:
    """生成された文書の最終出力"""
    title: str
    domain: DomainType
    sections: List[SectionNode]          # 通過した節のみ
    discarded: List[SectionNode]         # FAIL-CLOSEDで破棄された節
    discard_log: List[ValidationResult]  # 破棄ログ（改善・学習への利用禁止）
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_text(self, include_meta: bool = False) -> str:
        """
        検証済み文書をテキスト形式で出力する。
        include_meta=True にすると節ごとの検証スコアも付記される。
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
            lines.append("※ このログは構造検証のみに使用。改善・学習への利用禁止。")
            for vr in self.discard_log:
                lines.append(f"  - [{vr.section_id}] R={vr.r_ratio:.3f} | "
                              f"Violations: {'; '.join(vr.violations)}")

        return "\n".join(lines)

    def integrity_score(self) -> float:
        """
        文書全体の構造整合性スコア（0.0〜1.0）。
        通過率 × 平均Rスコアの逆数で算出。
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
        # R が低いほど（制約から遠いほど）整合性が高い
        coherence = max(0.0, 1.0 - avg_r)
        return round(pass_rate * coherence, 4)


class DocumentEngine:
    """
    文書生成の統合エンジン。
    GenesisBlock → SectionNode → Validator → DocumentOutput の
    パイプラインを管理する。

    使用例:
        engine = DocumentEngine("技術仕様書", DomainType.TECHNICAL)
        engine.genesis.add("NRA-IDE", "因果構造安全エンジン", is_axiom=True)
        engine.genesis.seal()
        engine.add_section("1", "概要", "本書はNRA-IDEの仕様を記述する。",
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
        """節を追加する。GenesisBlock がシール済みである必要はない（build時にチェック）"""
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
        文書を生成する。
        1. GenesisBlock を自動シール（未シールの場合）
        2. 各節を順序通りに検証
        3. PASSED/CAVEAT のみを採用、FAILED は Discard Log へ
        """
        # GenesisBlock が未シールなら自動シール
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
                # FAIL-CLOSED: 破棄
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
# 6. デモ（動作確認 & 使用例）
# ==============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("NRA Document Structure Engine v1.0 - Demo")
    print("=" * 60)

    # --- 例1: 技術仕様書（TECHNICAL ドメイン）---
    print("\n[Example 1] 技術仕様書 / TECHNICAL Domain\n")

    engine = DocumentEngine("NRA-IDE 技術仕様書 v1.0", DomainType.TECHNICAL)

    # GenesisBlock に定義を登録（公理として固定）
    engine.genesis.add("NRA-IDE",    "因果構造の安全エンジン。意味・最適化を扱わない。", is_axiom=True)
    engine.genesis.add("Causal Diode", "逆推論（Π⁻¹）を構造的に禁止する機構。",         is_axiom=True)
    engine.genesis.add("Fail-Closed",  "R ≥ R_op 時に出力を遮断する安全機構。",          is_axiom=True)
    engine.genesis.add("R",            "R = δ/τ。逸脱量と制約厚みの比率。")
    engine.genesis.add("δ",            "ゆらぎ量。入力の構造的逸脱を表す。")
    engine.genesis.add("τ",            "制約厚み。ドメイン別に設定される閾値パラメータ。")
    # シールは build() 時に自動実行されるが、明示的に呼ぶことも可能
    engine.genesis.seal()

    # 節を追加
    engine.add_section(
        "1", "概要",
        "本書は NRA-IDE の構造仕様を記述する。意味・最適化・履歴は扱わない。",
        references=["NRA-IDE"]
    )
    engine.add_section(
        "2", "コアコンポーネント",
        "NRA-IDE は Pre-RNA / LLM / Post-RNA の三層分離構造を持つ。",
        references=["NRA-IDE"],
        depends_on="1"
    )
    engine.add_section(
        "2.1", "Causal Diode",
        "Causal Diode は逆推論（Π⁻¹）を構造的に禁止する。"
        "順方向因果のみを許可し、効果から原因を逆算することを禁止する。",
        references=["Causal Diode", "NRA-IDE"],
        depends_on="2"
    )
    engine.add_section(
        "2.2", "Fail-Closed 機構",
        "R = δ/τ を計算し、R ≥ R_op の場合は即座に出力を遮断する。"
        "遮断はエラーではなく構造的正しさの維持である。",
        references=["Fail-Closed", "R", "δ", "τ"],
        depends_on="2"
    )
    # 意図的な不正節（未定義参照）
    engine.add_section(
        "3", "未定義用語テスト",
        "このセクションは存在しない用語「UNDEFINED_TERM」を参照している。",
        references=["UNDEFINED_TERM"],
        depends_on="2.2"
    )
    # Gear違反テスト（依存節が存在しない）
    engine.add_section(
        "4", "Gear違反テスト",
        "このセクションは完了していない節 '99' に依存している。",
        references=["NRA-IDE"],
        depends_on="99"
    )
    engine.add_section(
        "5", "結論",
        "NRA-IDE は因果構造の安全エンジンである。"
        "定義された公理から逸脱する節は Fail-Closed によって構造的に排除される。",
        references=["NRA-IDE", "Fail-Closed"],
        depends_on="2.2"
    )

    # 文書生成
    output = engine.build()

    # 結果表示
    print(output.to_text(include_meta=True))
    print(f"\n文書整合性スコア: {output.integrity_score():.4f}")

    # --- 例2: 医療プロトコル（MEDICAL ドメイン）---
    print("\n" + "=" * 60)
    print("[Example 2] 医療プロトコル / MEDICAL Domain\n")

    med_engine = DocumentEngine("ICU バイタル監視プロトコル", DomainType.MEDICAL)
    med_engine.genesis.add("Threshold_0.6",
                           "NRA標準安全閾値。R ≥ 0.6 で即座にアラート発動。",
                           is_axiom=True)
    med_engine.genesis.add("バイタルサイン",
                           "血圧・心拍数・体温・SpO2・呼吸数の5項目。")
    med_engine.genesis.add("アラート",
                           "異常検知時に医療スタッフへ通知するシグナル。")

    med_engine.add_section(
        "1", "目的",
        "本プロトコルはICU患者のバイタルサインを連続監視し、"
        "Threshold_0.6 を超過した場合にアラートを発動する手順を定める。",
        references=["バイタルサイン", "Threshold_0.6", "アラート"]
    )
    med_engine.add_section(
        "2", "監視項目",
        "監視対象はバイタルサインの5項目とする。"
        "各項目は1分間隔で自動計測される。",
        references=["バイタルサイン"],
        depends_on="1"
    )
    # 前方参照禁止ドメインで未定義参照を試みる
    med_engine.add_section(
        "3", "禁止参照テスト",
        "このセクションは定義されていない用語「UNDEFINED_MEDICAL_TERM」を使用している。",
        references=["UNDEFINED_MEDICAL_TERM"],
        depends_on="2"
    )
    med_engine.add_section(
        "3.1", "アラート発動条件",
        "R = δ/τ を計算し R ≥ 0.6 となった場合、アラートを即座に発動する。"
        "AIは発動の最終判断を行わず、判断権は担当医師に帰属する。",
        references=["アラート", "Threshold_0.6"],
        depends_on="2"
    )

    med_output = med_engine.build()
    print(med_output.to_text(include_meta=True))
    print(f"\n文書整合性スコア: {med_output.integrity_score():.4f}")

    print("\n--- デモ完了 ---")
