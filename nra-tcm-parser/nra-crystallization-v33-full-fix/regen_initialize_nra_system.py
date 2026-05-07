# regen_initialize_nra_system_20260216_190457.py
# FILE: regen_initialize_nra_system_20260216_190457.py
# TITLE: System Initializer — パイプライン全体の配線と起動
# Author: M-Tokuni (https://github.com/M-Tokun/NRA-IDE)
# Date: 2026-02-16 19:04:57 JST
# Temperature: 0.3 (axiom-level coherence)
#
# ============================================================
# 【このファイルの役割】
#
# NRA-IDEシステム全体を「正しい順序」で初期化する配線ヘルパー。
#
# 【なぜ初期化に専用ファイルが必要か】
#   NRA-IDEは複数のゲートが連携して動作する。
#   各ゲートが「同じGenesisBlockを参照している」ことが
#   Gear機構（全リンクが噛み合う）の大前提。
#
#   もし各ゲートが別々にGenesisBlockを読み込んだ場合:
#     - JSONが更新された時に不整合が生まれる
#     - 「公理Aで判断したPreRNAGate」と
#       「公理Bで判断したCrystallizationEngine」が混在する
#     - これは「歯車の歯の形が違う」状態 = Gear機構の崩壊
#
#   このファイルは「JSONを最初に1回だけ読み、
#   全ゲートに同じGenesisBlockを注入する」ことを保証する。
#
# 【設計原則: JSONが唯一の真実源（Single Source of Truth）】
#   設定値はコードにハードコードせず、JSONから読む。
#   JSONを変更すれば、全ゲートの設定が一括で変わる。
#   これはNRAの「入力が変われば、全ての判断が整合して変わる」原則と同じ。
#
# ============================================================

from __future__ import annotations

import json
from typing import Callable, Optional, Set

from regen_nra_llm_pipeline import NRAFullPipeline, PipelineConfig
from regen_nra_longrun_guard import GuardConfig, LongRunGuard
from regen_nra_document_structure_v32 import (
    CrystallizationConfig,
    CrystallizationEngine,
    GenesisBlock,
)

# デフォルトのJSON設定ファイル（唯一の真実源）
_DEFAULT_JSON = "regen_nra_document_structure.json"


# ============================================================
# load_genesis: GenesisBlockをJSONから読み込む
# ============================================================
def load_genesis(json_path: str = _DEFAULT_JSON) -> GenesisBlock:
    """
    システムJSONから GenesisBlock を読み込む。

    【Fail-Closed設計】
      JSONにキーが存在しない場合: 空リスト/辞書を返す（エラーにしない）。
      ただし空のGenesisBlockでは CrystallizationEngine.score() がFAILを返す。
      「公理が定義されていないシステムは動かない」= Gear機構。

    【読み込む項目】
      system.allowed_terms: 推奨用語リスト
      system.axioms:        公理名と定義のマッピング

    戻り値: GenesisBlock（frozen=True: 不変）
    """
    with open(json_path, encoding="utf-8") as f:
        d = json.load(f)

    sys_block = d.get("system", {})
    return GenesisBlock(
        allowed_terms=sys_block.get("allowed_terms", []),
        axioms=sys_block.get("axioms", {}),
    )


# ============================================================
# load_pipeline_config: PipelineConfigをJSONから読み込む
# ============================================================
def load_pipeline_config(
    json_path:         str              = _DEFAULT_JSON,
    must_keep_symbols: Optional[Set[str]] = None,
) -> PipelineConfig:
    """
    システムJSONの contracts ブロックから PipelineConfig を読み込む。

    【JSON構造との対応】
      contracts.output.crystal_max_sentences → CrystallizationConfig.max_crystal_sentences
      contracts.output.crystal_min_score     → CrystallizationConfig.min_score
      contracts.safety.fail_closed_returns   → PipelineConfig.fail_closed_return
      contracts.safety.vault_raw_max_chars   → PipelineConfig.vault_raw_max_chars

    【must_keep_symbols】
      外部から注入できる「必須シンボル」のセット。
      LongRunGuardのGear機構（必須リンク）として機能する。
      Noneの場合は必須シンボルなし（チェックをスキップ）。

    戻り値: PipelineConfig（frozen=True: 不変）
    """
    with open(json_path, encoding="utf-8") as f:
        d = json.load(f)

    contracts = d.get("contracts", {})
    output    = contracts.get("output", {})
    safety    = contracts.get("safety", {})

    # CrystallizationConfigをJSONから構築
    crystal_cfg = CrystallizationConfig.from_dict(output)

    # GuardConfigを構築（must_keep_symbolsを外部から注入可能）
    guard_cfg = GuardConfig(must_keep=must_keep_symbols)

    return PipelineConfig(
        crystallization=crystal_cfg,
        guard=guard_cfg,
        fail_closed_return=safety.get("fail_closed_returns", ""),
        vault_raw_max_chars=safety.get("vault_raw_max_chars", 500),
    )


# ============================================================
# build_default_pipeline: システム全体を正しい順序で初期化する
# ============================================================
def build_default_pipeline(
    llm_fn:            Callable[[str], str],
    json_path:         str                   = _DEFAULT_JSON,
    must_keep_symbols: Optional[Set[str]]    = None,
) -> NRAFullPipeline:
    """
    NRA-IDEパイプライン全体の「正規の起動手順」。

    【この関数が唯一の公式エントリポイント】
      NRAFullPipelineを直接インスタンス化することも可能だが、
      それはGear機構（全ゲートが同じGenesisBlockを参照する）を
      保証しない。
      この関数を使うことで、「正しい配線」が保証される。

    【初期化の順序が重要】
      FIX: 前バージョンでは run() ごとにGenesisBlockが読み込まれていた。
      修正後: __init__時に1回だけ読み込み、全ての run() で共有する。

      順序:
        1. JSONを読む（load_genesis）
        2. JSONを読む（load_pipeline_config）
        3. GenesisBlockをNRAFullPipelineに注入
        → 全ゲートが同じ公理（GenesisBlock）を参照する状態が完成

    【llm_fn（LLM呼び出し関数）の注入】
      LLM自体はパイプラインの「一部品」に過ぎない。
      どのLLMを使うかはこの関数の外で決める。
      これにより、LLMをモックに差し替えてテストすることが容易になる。
      （Gear機構: どの歯車を使うかと、歯車の噛み合い方は別の問題）

    戻り値: 起動済みの NRAFullPipeline インスタンス
    """
    # Step 1: GenesisBlock（公理の基盤）をJSONから読み込む
    genesis = load_genesis(json_path)

    # Step 2: 全ゲートの設定をJSONから読み込む
    cfg = load_pipeline_config(json_path, must_keep_symbols)

    # Step 3: 全コンポーネントに同じGenesisBlockを注入して起動
    return NRAFullPipeline(
        llm_fn=llm_fn,
        config=cfg,
        guard=LongRunGuard(cfg.guard),
        engine=CrystallizationEngine(cfg.crystallization),
        genesis=genesis,   # FIX: 初期化時に注入（run()ごとではない）
    )


# ============================================================
# 使用例（新人AIへの参考）
# ============================================================
#
# # LLM呼び出し関数を定義（実際のAPIに差し替える）
# def my_llm(prompt: str) -> str:
#     return "## Crystal\nThis is the crystallized output.\n## Trace\ndecision: approved. kept_invariants: causal_diode."
#
# # パイプラインを起動
# pipeline = build_default_pipeline(llm_fn=my_llm)
#
# # 実行
# result = pipeline.run("ユーザーの入力テキスト")
#
# if result.ok:
#     print("出力:", result.text)
# else:
#     print("FAIL_CLOSED: 出力なし")
#     print("理由:", result.reasons)
#     if result.vault_id:
#         print("Vault記録ID:", result.vault_id)
#
# ============================================================
