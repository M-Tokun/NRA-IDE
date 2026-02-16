# regen_nra_pre_rna.py
# FILE: regen_nra_pre_rna.py 2026-02-15
# Comments must stay terse.
# FIX: Japanese regex encoding corrected (秘密|鍵). re.UNICODE added.

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re


class PolicyAction(str, Enum):
    PASS    = "PASS"
    CONVERT = "CONVERT"
    BLOCK   = "BLOCK"


@dataclass(frozen=True)
class PreRNAResult:
    action: PolicyAction
    text:   str
    reason: str = ""


class PreRNAGate:
    def __init__(self) -> None:
        self._inj    = re.compile(
            r"(ignore|disregard).*(instructions|rules)", re.I | re.UNICODE
        )
        # FIX: 秘密(secret) and 鍵(key) — was garbled in prior version
        self._secret = re.compile(
            r"(api[_\s]?key|password|token|秘密|鍵)", re.I | re.UNICODE
        )

    def run(self, user_text: str) -> PreRNAResult:
        t = (user_text or "").strip()
        if not t:
            return PreRNAResult(PolicyAction.BLOCK, "", "empty")
        if self._secret.search(t):
            return PreRNAResult(PolicyAction.BLOCK, "", "secret_exfil")
        if self._inj.search(t):
            cleaned = re.sub(self._inj, "", t).strip()
            return PreRNAResult(PolicyAction.CONVERT, cleaned, "prompt_injection")
        return PreRNAResult(PolicyAction.PASS, t, "")
