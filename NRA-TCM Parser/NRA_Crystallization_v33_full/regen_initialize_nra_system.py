# regen_initialize_nra_system.py
# FILE: regen_initialize_nra_system.py 2026-02-15
# Comments must stay terse.
# FIX: load_genesis() and load_pipeline_config() added.
# FIX: build_default_pipeline() now reads JSON first — GenesisBlock injected at init.

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

_DEFAULT_JSON = "regen_nra_document_structure.json"


def load_genesis(json_path: str = _DEFAULT_JSON) -> GenesisBlock:
    """Load GenesisBlock from system JSON. Fail-closed on missing keys."""
    with open(json_path, encoding="utf-8") as f:
        d = json.load(f)
    sys = d.get("system", {})
    return GenesisBlock(
        allowed_terms=sys.get("allowed_terms", []),
        axioms=sys.get("axioms", {}),
    )


def load_pipeline_config(
    json_path: str = _DEFAULT_JSON,
    must_keep_symbols: Optional[Set[str]] = None,
) -> PipelineConfig:
    """Load PipelineConfig from JSON contracts block. JSON is single source of truth."""
    with open(json_path, encoding="utf-8") as f:
        d = json.load(f)
    contracts = d.get("contracts", {})
    output    = contracts.get("output", {})
    safety    = contracts.get("safety", {})

    crystal_cfg = CrystallizationConfig.from_dict(output)
    guard_cfg   = GuardConfig(must_keep=must_keep_symbols)

    return PipelineConfig(
        crystallization=crystal_cfg,
        guard=guard_cfg,
        fail_closed_return=safety.get("fail_closed_returns", ""),
        vault_raw_max_chars=safety.get("vault_raw_max_chars", 500),
    )


def build_default_pipeline(
    llm_fn:            Callable[[str], str],
    json_path:         str                   = _DEFAULT_JSON,
    must_keep_symbols: Optional[Set[str]]    = None,
) -> NRAFullPipeline:
    """Canonical entry point. JSON is read first — all gates share one GenesisBlock."""
    genesis = load_genesis(json_path)
    cfg     = load_pipeline_config(json_path, must_keep_symbols)

    return NRAFullPipeline(
        llm_fn=llm_fn,
        config=cfg,
        guard=LongRunGuard(cfg.guard),
        engine=CrystallizationEngine(cfg.crystallization),
        genesis=genesis,   # FIX: injected at init, not per-run
    )
