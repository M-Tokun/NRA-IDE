# regen_nra_llm_pipeline_20260216_190457.py
# FILE: regen_nra_llm_pipeline_20260216_190457.py
# TITLE: NRA Full Pipeline — 律環公理の全4ステップを統合する実行エンジン
# Author: M-Tokuni (https://github.com/M-Tokun/NRA-IDE)
# Date: 2026-02-16 19:04:57 JST
# Temperature: 0.3 (axiom-level coherence)
#
# ============================================================
# 【このファイルが担う律環公理の役割】
#
# 律環公理の4ステップを全て統合して実行する「司令塔」。
#   Step 1: Input     → PreRNAGate.run()
#   Step 2: Stick     → LongRunGuard.check()
#   Step 3: Threshold → CrystallizationEngine.score()
#   Step 4: Slip / FAIL_CLOSED → PipelineResult(ok=True/False)
#
# 【サンドイッチアーキテクチャの全体像】
#
#   ユーザー入力
#       ↓
#   [PreRNAGate] ← 前蓋: 入力の純化（注入・秘密情報の遮断）
#       ↓ PASS / CONVERT
#   [_prompt()] ← GenesisBlockと公理ルールをpromptに埋め込む
#       ↓
#   [LLM呼び出し] ← 確率的生成（ここだけが「線形」の世界）
#       ↓
#   [LongRunGuard] ← 長時間劣化の監視
#       ↓ OK / WARN
#   [CrystallizationEngine] ← 後蓋: 構造検証とスコアリング
#       ↓
#   PipelineResult(ok=True)  → ユーザーへ出力
#   PipelineResult(ok=False) → FAIL_CLOSED（空文字）+ Vaultへ記録
#
# 【Vaultとは何か】
#   FAIL_CLOSEDになった出力の「証拠保全」。
#   なぜFAILになったかを構造的に記録し、改善・最適化への利用を禁止する。
#   append-only: 書き込むだけ。読み返して「学習」することはしない。
#   Causal Diode: 過去の失敗を現在の判断に逆流させない。
#
# ============================================================

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Any

from regen_nra_pre_rna import PreRNAGate, PolicyAction
from regen_nra_longrun_guard import LongRunGuard, GuardConfig
from regen_nra_document_structure_v32 import (
    CrystallizationEngine, CrystallizationConfig,
    GenesisBlock,
)


# ============================================================
# PipelineConfig: パイプライン全体の設定（不変）
# ============================================================
@dataclass(frozen=True)
class PipelineConfig:
    """
    NRAFullPipelineの全設定を格納する不変データクラス。

    crystallization: CrystallizationConfigのインスタンス。
      後蓋（CrystallizationEngine）のスコアリング閾値等を定義。

    guard: GuardConfigのインスタンス。
      LongRunGuardの監視閾値等を定義。

    fail_closed_return (default: ""):
      FAIL_CLOSEDの際に返す文字列。デフォルトは空文字。
      「わからない時は何も言わない」= NRAの本質。
      空文字は「嘘をつかない」という正直な出力。

    vault_raw_max_chars (default: 500):
      VaultにFAIL時の生出力を保存する際の最大文字数。
      FIX: 上限なしでは生出力に秘密情報が含まれていた場合に
      永続的に保存されてしまうリスクがある。
      500文字でキャップして、秘密情報の漏洩を構造的に防ぐ。
    """
    crystallization:     CrystallizationConfig = field(default_factory=CrystallizationConfig)
    guard:               GuardConfig            = field(default_factory=GuardConfig)
    fail_closed_return:  str                    = ""
    vault_raw_max_chars: int                    = 500


# ============================================================
# PipelineResult: パイプラインの実行結果（不変）
# ============================================================
@dataclass(frozen=True)
class PipelineResult:
    """
    NRAFullPipeline.run()の戻り値。

    text: str
      成功時（ok=True）: 結晶化されたLLM出力。
      失敗時（ok=False）: fail_closed_return（通常は空文字）。

    ok: bool
      True  = 全ゲートを通過した（SLIP: 出力を使用してよい）
      False = いずれかのゲートでFAIL_CLOSED（出力を使用してはならない）
      これが律環公理Step 4の最終判定。

    score: float
      CrystallizationEngineが算出したスコア。
      ok=Trueの場合は min_score（0.60）以上。
      ok=Falseの場合は 0.0 または min_score未満。

    reasons: FAILになった理由のリスト（audit用）。

    vault_id: FAILの場合、Vaultへの記録IDを返す。
      「なぜFAILになったか」を後から確認できるようにする。
      改善・最適化への利用は禁止（Causal Diode: 過去の逆流を防ぐ）。
    """
    text:     str
    ok:       bool
    score:    float
    reasons:  List[str]     = field(default_factory=list)
    vault_id: Optional[str] = None


# ============================================================
# Vault: FAIL記録の append-only ストレージ
# ============================================================
class Vault:
    """
    FAILになった出力と理由を記録するappend-onlyストレージ。

    【設計思想: append-only】
      一度記録したものは変更・削除しない。
      これは律環公理の時間的不可逆性（P3）の実装。
      「FAILだったという事実」は消せない。

    【何を記録するか】
      stage:  どのゲートでFAILになったか（"guard" or "validate"）
      events: LongRunGuardが検出したイベント（guardの場合）
      score:  CrystallizationEngineのスコア（validateの場合）
      reasons: FAIL理由のリスト
      raw:    LLMの生出力（先頭500文字のみ: 秘密情報漏洩防止）

    【何に使わないか】
      - LLMの再学習（Causal Diode: 失敗から「学習して最適化」しない）
      - FAILの理由を分析して閾値を緩める（公理の弱体化禁止）
      - 監査・デバッグのみに使用する
    """

    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, Any]] = {}
        self._seq = 0  # シーケンス番号（append-onlyの証拠）

    def put(self, payload: Dict[str, Any]) -> str:
        """
        FAILの記録をVaultに追加する。

        戻り値: vault-000001 形式のID（audit追跡用）
        シーケンス番号は単調増加のみ（過去への書き戻し不可）。
        """
        self._seq += 1
        vid = f"vault-{self._seq:06d}"
        self._store[vid] = payload
        return vid


# ============================================================
# NRAFullPipeline: 律環公理の全4ステップを統合する実行エンジン
# ============================================================
class NRAFullPipeline:
    """
    NRA-IDEの中核。律環公理の4ステップを順番に実行する。

    【依存関係の注入（Dependency Injection）】
      各ゲート（PreRNAGate, LongRunGuard, CrystallizationEngine）は
      外部から注入される。デフォルトはNRA標準設定。
      テスト時はモック（偽物）を注入して各ゲートを個別に検証できる。

    【GenesisBlockの管理】
      FIX: GenesisBlockは初期化時（__init__）に注入され、
      全ての run() 呼び出しで共有される。
      以前は run() ごとに別々のGenesisBlockが使われていた（バグ）。
      1システム = 1GenesisBlock = 全ゲートが同じ公理を参照する。
      これがGear機構（全リンクが同じ公理に噛み合う）の実装。
    """

    def __init__(
        self,
        llm_fn:   Callable[[str], str],       # LLM呼び出し関数（外部注入）
        config:   Optional[PipelineConfig]         = None,
        pre_gate: Optional[PreRNAGate]             = None,
        guard:    Optional[LongRunGuard]           = None,
        engine:   Optional[CrystallizationEngine]  = None,
        vault:    Optional[Vault]                  = None,
        genesis:  Optional[GenesisBlock]           = None,  # FIX: 初期化時に注入
    ) -> None:
        self.llm_fn   = llm_fn
        self.cfg      = config   or PipelineConfig()
        self.pre_gate = pre_gate or PreRNAGate()
        self.guard    = guard    or LongRunGuard(self.cfg.guard)
        self.engine   = engine   or CrystallizationEngine(self.cfg.crystallization)
        self.vault    = vault    or Vault()
        self.genesis  = genesis  # FIX: 全run()で共有される公理の基盤

    def _prompt(self, user_text: str, genesis: Optional[GenesisBlock]) -> str:
        """
        LLMへ渡すpromptを構築する。

        【GenesisBlockによる制約の注入】
          ルール（rules）をpromptの先頭に埋め込むことで、
          LLMの確率的生成を「公理の制約内」に誘導する。
          ただしLLMは依然として確率的であり、
          後段のCrystallizationEngineが最終的な品質保証を行う。

        【なぜallowed_termsを先頭8つのみに制限するか】
          長すぎるpromptはLLMの注意を分散させる。
          最も重要な公理用語8つを優先することで、
          「エネルギーを核心に集中させる」設計。
        """
        rules = [
            "Output headings: ## Crystal and ## Trace.",
            f"Crystal: <= {self.cfg.crystallization.max_crystal_sentences} sentences.",
            "Trace: include 'decision' and 'kept_invariants'.",
        ]
        if genesis and genesis.allowed_terms:
            rules.append("Prefer allowed terms: " + ", ".join(genesis.allowed_terms[:8]))
        return "\n".join(rules) + "\n\nUSER:\n" + user_text

    def _safe_raw(self, raw: str) -> str:
        """
        LLMの生出力をVault保存用に安全な長さに切り詰める。

        FIX: vault_raw_max_chars（デフォルト500文字）でキャップ。
        秘密情報がLLMの出力に混入していた場合でも、
        Vaultへの永続的保存を防ぐ。
        構造的な情報セキュリティの実装。
        """
        cap = self.cfg.vault_raw_max_chars
        return raw[:cap] + ("…[truncated]" if len(raw) > cap else "")

    def run(
        self,
        user_text: str,
        genesis:   Optional[GenesisBlock] = None,
    ) -> PipelineResult:
        """
        律環公理の4ステップを実行する主関数。

        【引数】
          user_text: ユーザーの入力テキスト
          genesis:   呼び出し時に一時的に上書きするGenesisBlock（オプション）
                     通常は初期化時のgenesisを使用する。

        【実行フロー】
          Step 1: PreRNAGate → BLOCK なら即 FAIL_CLOSED
          Step 2: LLM呼び出し → 生出力を取得
          Step 2: LongRunGuard → FAIL なら Vault記録 + FAIL_CLOSED
          Step 3: CrystallizationEngine → スコア計算
          Step 4: score < min_score なら Vault記録 + FAIL_CLOSED
                  score >= min_score なら SLIP（出力を返す）

        【FAIL_CLOSEDは失敗ではない】
          PipelineResult(ok=False) は「問題が検出された」という正直な出力。
          数学基盤のAIは「何かを返さなければならない」と感じる。
          NRA-IDEは「不能性を正直に返す」ことを正解とする。
        """
        # FIX: 呼び出し時のgenesisが優先。なければ初期化時のgenesisを使用。
        effective_genesis = genesis or self.genesis

        # --------------------------------------------------
        # Step 1: PreRNAGate（入力の純化）
        # --------------------------------------------------
        pre = self.pre_gate.run(user_text)
        if pre.action == PolicyAction.BLOCK:
            # 入力がBLOCKされた → パイプライン全体をFAIL_CLOSED
            # Vault記録なし（入力段階のFAILは秘密情報を含む可能性があるため）
            return PipelineResult(
                self.cfg.fail_closed_return, False, 0.0, [f"pre:{pre.reason}"]
            )

        # --------------------------------------------------
        # Step 2-前半: LLM呼び出し
        # --------------------------------------------------
        # ここだけが「確率的（線形）」の世界。
        # promptに公理ルールを埋め込んで制約を与えるが、
        # LLMの出力は依然として確率的。後段のゲートが品質保証を担う。
        raw = self.llm_fn(self._prompt(pre.text, effective_genesis))

        # --------------------------------------------------
        # Step 2-後半: LongRunGuard（構造劣化の監視）
        # --------------------------------------------------
        events = self.guard.check(raw)
        if self.guard.advise(events).startswith("Return empty"):
            # FAIL_CLOSEDを指示 → Vaultに記録して空文字を返す
            vid = self.vault.put({
                "stage":  "guard",
                "events": [e.__dict__ for e in events],
                "raw":    self._safe_raw(raw),  # FIX: 500文字でキャップ
            })
            return PipelineResult(
                self.cfg.fail_closed_return, False, 0.0, ["guard:fail"], vault_id=vid
            )

        # --------------------------------------------------
        # Step 3: CrystallizationEngine（構造検証とスコアリング）
        # --------------------------------------------------
        out = self.engine.parse_plaintext(raw)      # 生テキストをNRAOutputに変換
        vr  = self.engine.score(out, effective_genesis)  # 総合スコアリング

        if not vr.ok:
            # スコアが閾値未満 → Vaultに記録して空文字を返す
            vid = self.vault.put({
                "stage":   "validate",
                "score":   vr.score,
                "reasons": vr.reasons,
                "raw":     self._safe_raw(raw),  # FIX: 500文字でキャップ
            })
            return PipelineResult(
                self.cfg.fail_closed_return, False, vr.score, vr.reasons, vault_id=vid
            )

        # --------------------------------------------------
        # Step 4: SLIP（全ゲートを通過 → 結晶化された出力を返す）
        # --------------------------------------------------
        # ここに到達した出力は:
        #   - 入力が正当（PreRNAGate: PASS/CONVERT）
        #   - 構造的劣化なし（LongRunGuard: OK/WARN）
        #   - 公理構造を満たし、スコア >= 0.60（CrystallizationEngine）
        # この3条件を全て満たした場合のみ、出力が「通過」する。
        return PipelineResult(raw, True, vr.score, vr.reasons)
