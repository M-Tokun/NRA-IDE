# regen_nra_document_structure_v32_20260216_190457.py
# FILE: regen_nra_document_structure_v32_20260216_190457.py
# TITLE: Document Structure + Crystallization — 出力の結晶化と構造検証
# Author: M-Tokuni (https://github.com/M-Tokun/NRA-IDE)
# Date: 2026-02-16 19:04:57 JST
# Temperature: 0.3 (axiom-level coherence)
#
# ============================================================
# 【このファイルが担う律環公理の役割】
#
# 律環公理の4ステップ:
#   Step 1: Input
#   Step 2: Stick
#   Step 3: Threshold ← ★このファイルの主担当（スコアで閾値判定）
#   Step 4: Slip / FAIL_CLOSED ← ValidationResult.okで決定
#
# 【このファイルが解決する問題】
#   LLMは「もっともらしい出力」を確率的に生成する。
#   その出力が律環公理の構造（Crystal + Trace）を満たしているか
#   を検証するのがこのファイルの役割。
#
# 【結晶化（Crystallization）とは何か】
#   「結晶」は不純物を含まない、整合した構造体を指す。
#   LLMの出力から「結晶（Crystal）」を抽出することで、
#   確率的な揺れ（ノイズ）を除去し、構造的に純粋な出力のみを通す。
#
#   Crystal: 出力の本質を2文以内に凝縮したもの
#   Trace:   どのような判断・不変条件を維持したかの記録
#
# 【サンドイッチアーキテクチャにおける位置】
#   PreRNAGate（前蓋）→ LLM → CrystallizationEngine（後蓋）
#   この後蓋がなければ、LLMの確率的出力が直接ユーザーに届く。
#   それは「数学基盤のAIが無理やり答えを出す」状態と同じ。
#
# ============================================================

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import re


# ============================================================
# Section: 出力の一単位（不変）
# ============================================================
@dataclass(frozen=True)
class Section:
    """
    NRAOutput を構成する1つのセクション。frozen=Trueで不変。

    title:
      セクションの識別子。"crystal" と "trace" が必須。
      小文字で統一（大文字小文字の揺れは確率的なノイズ）。

    body:
      セクションの本文。

    references:
      このセクションが参照する公理名のリスト。
      例: ["causal_diode", "fail_closed"]
      GenesisBlockの公理キーと照合することで、
      「この出力が公理に基づいているか」を検証できる。

    【frozen=Trueの理由】
      Causal Diode: 一度確定した出力を事後修正することは逆流（Π⁻¹）。
      セクションは生成時に確定し、変更されない。
    """
    title:      str
    body:       str
    references: List[str] = field(default_factory=list)


# ============================================================
# GenesisBlock: 公理の定義（システムの不変の北極星）
# ============================================================
@dataclass(frozen=True)
class GenesisBlock:
    """
    NRA-IDEシステム全体の公理を定義する不変ブロック。
    「Genesis（創世記）」= すべての判断の出発点。

    allowed_terms:
      出力で使用が推奨される用語リスト。
      「制限された語彙」ではなく「公理に根ざした用語」。
      LLMへのpromptに含めることで、確率的補完ではなく
      構造的な語彙選択を促す。

    axioms:
      公理名と定義のマッピング。
      例: {"causal_diode": "Unidirectional causal flow..."}
      Sectionのreferencesと照合することで、
      「出力が公理に根ざしているか」をスコアリングできる。

    【なぜGenesisBlockが必須か】
      GenesisBlockなしでは CrystallizationEngine.score() が
      強制的にFAIL（score=0.0）を返す。
      「公理の基盤がなければ動かない」= Gear機構の実装。
      公理なき判断は判断ではない。
    """
    allowed_terms: List[str]      = field(default_factory=list)
    axioms:        Dict[str, str] = field(default_factory=dict)


# ============================================================
# NRAOutput: LLMの出力を構造化したもの（不変）
# ============================================================
@dataclass(frozen=True)
class NRAOutput:
    """
    LLMの生テキスト出力を構造化したデータクラス。

    sections: Sectionのリスト。
      最低でも "crystal" と "trace" の2つが必要。
      この2つが揃わない場合、StructureValidatorがFAILを返す。
      Gear機構: 必須リンクが全て揃っていなければ機械は動かない。

    meta: 付加的なメタデータ（オプション）。
      処理時刻・モデル名等を記録できるが、
      判断の基準には使用しない（Effectであり、Causeではない）。
    """
    sections: List[Section]
    meta:     Dict[str, str] = field(default_factory=dict)


# ============================================================
# ValidationResult: 検証結果（不変）
# ============================================================
@dataclass(frozen=True)
class ValidationResult:
    """
    構造検証・スコアリングの結果を格納する不変オブジェクト。

    ok: bool
      True  = 閾値（min_score）を超えた = SLIP（出力を通す）
      False = 閾値未満 = FAIL_CLOSED（空文字を返す）
      これが律環公理Step 4の判断基準。

    score: float
      0.0〜1.0のスコア。
      【重要】: このスコアはOK/FAILの判定に使われるだけで、
      「だいたい0.60に近いから通す」という判定には使わない。
      score >= min_score → ok=True、それ以外 → ok=False。
      境界は境界であり、グラデーションではない。

    reasons: 問題があった場合の理由リスト（append-only）。
      「なぜFAILになったか」を構造的に記録する。
      事後修正禁止（Causal Diode）。
    """
    ok:      bool
    score:   float
    reasons: List[str] = field(default_factory=list)


# ============================================================
# CrystallizationConfig: 結晶化の閾値設定（不変）
# ============================================================
@dataclass(frozen=True)
class CrystallizationConfig:
    """
    CrystallizationEngineのパラメータ設定。

    max_crystal_sentences (default: 2):
      Crystal セクションの最大文数。
      「本質を2文以内に凝縮できなければ、まだ結晶化できていない」。
      簡潔さは品質の証拠。長い出力は構造的な散漫さを示す。

    min_score (default: 0.60):
      出力を通過させる最低スコア閾値。
      R = δ/τ の閾値に相当。
      この値を「超えたか/超えていないか」のみが判定基準。

    w_axiom_refs (default: 0.20):
      公理参照ボーナスの重み（20%）。
      公理に基づいた出力を評価する。

    w_length (default: 0.20):
      Crystal長さボーナスの重み（20%）。
      1〜140文字: フルボーナス（簡潔で十分な情報量）
      141〜240文字: ハーフボーナス（やや長いが許容範囲）
      240文字超: ボーナスなし（長すぎる = 結晶化不十分）

    w_structure (default: 0.60):
      構造検証スコアの重み（60%）。
      全体スコアの6割が「構造が正しいか」で決まる。
      意味の正しさではなく、構造の正しさが最優先。

    from_dict():
      JSONのcontrats.outputブロックから設定を読み込む。
      JSONが唯一の真実源（Single Source of Truth）。
    """
    max_crystal_sentences: int   = 2
    min_score:             float = 0.60
    w_axiom_refs:          float = 0.20
    w_length:              float = 0.20
    w_structure:           float = 0.60

    @classmethod
    def from_dict(cls, d: Dict) -> "CrystallizationConfig":
        """JSONのcontrats.outputブロックから設定を読み込む。"""
        return cls(
            max_crystal_sentences=d.get("crystal_max_sentences", 2),
            min_score=d.get("crystal_min_score", 0.60),
        )


# ============================================================
# StructureValidator: 構造の基本検証
# ============================================================
class StructureValidator:
    """
    NRAOutputが必須構造（Crystal + Trace）を満たしているか検証する。

    【検証する3つの条件（Gear機構: 全て揃わなければFAIL）】
      1. "crystal" セクションが存在するか
      2. "trace" セクションが存在するか
      3. crystal の文数が max_crystal_sentences 以下か
      4. trace に "decision" が含まれるか
      5. trace に "kept_invariants" または "invariant" が含まれるか

    【スコアの計算】
      基準スコア: 1.0
      問題1つにつき: -0.2（最大-0.8まで）
      最終スコア: max(0.0, 1.0 - 0.2 × 問題数)
    """

    def __init__(self, config: Optional[CrystallizationConfig] = None) -> None:
        self.config = config or CrystallizationConfig()
        # 文分割パターン: 日本語（。）と英語（.!?）の文末記号
        # FIX: 前バージョンで日本語の「。」が文字化けしていた。
        # UTF-8で正しく記述し、re.UNICODEフラグを追加。
        self._sent_split = re.compile(r"[。．.!?]\s*", re.UNICODE)

    def validate(self, out: NRAOutput) -> ValidationResult:
        """
        NRAOutputの構造を検証し、ValidationResultを返す。

        【Gear機構の実装】
          "crystal" か "trace" が欠けた場合は即座にFAIL（score=0.0）。
          スコアを計算するまでもない。歯が欠けた歯車に動力は伝わらない。
        """
        reasons: List[str] = []
        # セクションをタイトルでインデックス化（小文字に統一）
        sec = {s.title.lower(): s for s in out.sections}

        # 必須セクション "crystal" の存在確認
        if "crystal" not in sec:
            return ValidationResult(False, 0.0, ["missing: crystal"])

        # 必須セクション "trace" の存在確認
        if "trace" not in sec:
            return ValidationResult(False, 0.0, ["missing: trace"])

        # crystal の本文が空でないことを確認
        crystal = sec["crystal"].body.strip()
        if not crystal:
            return ValidationResult(False, 0.0, ["empty: crystal"])

        # crystal の文数チェック
        sentences = [x for x in self._sent_split.split(crystal) if x.strip()]
        if len(sentences) > self.config.max_crystal_sentences:
            reasons.append("crystal: too many sentences")

        # trace に判断記録が含まれるか
        trace = sec["trace"].body.lower()
        if "decision" not in trace:
            reasons.append("trace: missing decision")

        # trace に不変条件の記録が含まれるか
        # FIX: "不変" が前バージョンで文字化けしていた。3つの表記に対応。
        if (
            "kept_invariants" not in trace
            and "invariant"       not in trace
            and "不変"            not in trace
        ):
            reasons.append("trace: missing kept_invariants")

        # スコア計算: 問題1つにつき-0.2
        score = 1.0 - min(0.8, 0.2 * len(reasons))
        score = max(0.0, score)
        return ValidationResult(score >= self.config.min_score, score, reasons)


# ============================================================
# CrystallizationEngine: 総合スコアリングと結晶化
# ============================================================
class CrystallizationEngine:
    """
    NRAOutputを総合的にスコアリングし、
    「結晶化された出力」として通過させるか判定する後蓋。

    【スコアの構成（合計最大1.0）】
      構造スコア（60%）: StructureValidatorによる基本検証
      公理参照ボーナス（20%）: GenesisBlockの公理を参照しているか
      長さボーナス（20%）: Crystalが適切な長さか

    【GenesisBlockが必須な理由】
      公理のないスコアリングは「基盤のない判断」。
      Gear機構: GenesisBlockなしではスコア=0.0（即FAIL）。

    parse_plaintext():
      LLMが返す生テキストを NRAOutput に変換する静的メソッド。
      ## Crystal / ## Trace というマークダウン見出しを解析する。
    """

    def __init__(self, config: Optional[CrystallizationConfig] = None) -> None:
        self.config    = config or CrystallizationConfig()
        self.validator = StructureValidator(self.config)

    def score(self, out: NRAOutput, genesis: Optional[GenesisBlock] = None) -> ValidationResult:
        """
        NRAOutputを総合スコアリングする。

        【GenesisBlockなしの場合】
          FIX: genesis=None の場合、スコアを強制的に0.0にする。
          理由: 公理の基盤なしに「良い出力」は定義できない。
          これはFAIL_CLOSEDであり、エラーではなく「公理違反」の正直な記録。
        """
        base = self.validator.validate(out)

        # GenesisBlockなし → 即FAIL（公理の基盤が存在しない）
        if not genesis:
            return ValidationResult(
                False, 0.0, list(base.reasons) + ["genesis: missing"]
            )

        # 公理キーのセット（スコアリング用）
        ax_keys = {k.lower() for k in genesis.axioms.keys()}

        # 全セクションのreferencesを集約
        refs: List[str] = []
        for s in out.sections:
            refs.extend([r.lower() for r in (s.references or [])])

        # 公理参照ヒット数（最大3でフルボーナス）
        hit = sum(1 for r in refs if r in ax_keys)

        # Crystal本文の長さ
        crystal = next(
            (s.body for s in out.sections if s.title.lower() == "crystal"), ""
        ).strip()
        n_chars = len(crystal)

        # 公理参照ボーナス（最大w_axiom_refs=0.20）
        ax_bonus = min(1.0, hit / 3.0) * self.config.w_axiom_refs

        # 長さボーナス（最大w_length=0.20）
        len_bonus = 0.0
        if 1 <= n_chars <= 140:
            len_bonus = 1.0 * self.config.w_length     # フルボーナス
        elif 141 <= n_chars <= 240:
            len_bonus = 0.5 * self.config.w_length     # ハーフボーナス

        # 総合スコア = 構造スコア×0.60 + 公理参照×0.20 + 長さ×0.20
        score = base.score * self.config.w_structure + ax_bonus + len_bonus
        score = max(0.0, min(1.0, score))

        # 閾値判定: score >= min_score かつ 構造検証OK → 結晶化成功
        ok = base.ok and score >= self.config.min_score
        reasons = list(base.reasons)
        if hit == 0:
            reasons.append("refs: no axiom hit")
        return ValidationResult(ok, score, reasons)

    @staticmethod
    def parse_plaintext(text: str) -> NRAOutput:
        """
        LLMが返す生テキストを NRAOutput に変換する。

        【パーサーの動作】
          ## で始まる見出し行をセクション区切りとして認識する。
          見出しがない先頭部分は "crystal" セクションとして扱う。

        例:
          入力テキスト:
            Some introduction text
            ## Crystal
            The core insight here.
            ## Trace
            decision: approved. kept_invariants: causal_diode.

          出力:
            NRAOutput(sections=[
              Section("crystal", "Some introduction text"),
              Section("crystal", "The core insight here."),
              Section("trace", "decision: approved. kept_invariants: causal_diode.")
            ])

        【設計思想】
          LLMが返す構造を「あるがまま」に解析する。
          意味的な解釈や補完は行わない（Causal Diode）。
          構造が期待通りでなければ、後段のvalidateがFAILを返す。
        """
        sections: List[Section] = []
        title = "crystal"   # 見出しなし部分のデフォルトタイトル
        buf:   List[str]    = []

        for line in (text or "").splitlines():
            m = re.match(r"^\s*##+\s*(.+?)\s*$", line)
            if m:
                # 見出し行: 前のバッファをセクションとして確定
                if buf:
                    sections.append(Section(title, "\n".join(buf).strip()))
                title = m.group(1).strip().lower()
                buf   = []
            else:
                buf.append(line)

        # 残りのバッファを最後のセクションとして確定
        if buf:
            sections.append(Section(title, "\n".join(buf).strip()))

        return NRAOutput(sections=sections)
