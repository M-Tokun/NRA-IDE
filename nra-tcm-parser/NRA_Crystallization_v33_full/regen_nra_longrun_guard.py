# regen_nra_longrun_guard.py
# FILE: regen_nra_longrun_guard.py 2026-02-15
# Comments must stay terse.
# FIX: _seen dict bounded to prevent unbounded memory growth in long sessions.

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Set, Dict
import re


_MAX_SEEN: int = 8000  # hard cap on trigram history size


@dataclass(frozen=True)
class GuardConfig:
    warn_drop_ratio:        float          = 0.15
    fail_drop_ratio:        float          = 0.30
    checkpoint_chars:       int            = 2000
    max_repeat_trigram_hits: int           = 8
    must_keep:              Optional[Set[str]] = None


@dataclass(frozen=True)
class GuardEvent:
    level:  str
    reason: str


class LongRunGuard:
    def __init__(self, config: Optional[GuardConfig] = None) -> None:
        self.cfg      = config or GuardConfig()
        self._last_len: Optional[int]   = None
        self._seen:     Dict[str, int]  = {}

    def _trigrams(self, text: str) -> Iterable[str]:
        tokens = re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE)
        for i in range(len(tokens) - 2):
            yield " ".join(tokens[i:i + 3])

    def _trim_seen(self) -> None:
        """FIX: drop single-occurrence entries first; full reset if still over cap."""
        if len(self._seen) >= _MAX_SEEN:
            self._seen = {k: v for k, v in self._seen.items() if v >= 2}
        if len(self._seen) >= _MAX_SEEN:
            self._seen = {}

    def check(self, text: str) -> List[GuardEvent]:
        t  = text or ""
        n  = len(t)
        ev: List[GuardEvent] = []

        if self._last_len is not None and self._last_len > 0:
            drop = (self._last_len - n) / self._last_len
            if drop >= self.cfg.fail_drop_ratio:
                ev.append(GuardEvent("FAIL", f"compression_drop>={self.cfg.fail_drop_ratio:.2f}"))
            elif drop >= self.cfg.warn_drop_ratio:
                ev.append(GuardEvent("WARN", f"compression_drop>={self.cfg.warn_drop_ratio:.2f}"))

        if self.cfg.must_keep:
            missing = [s for s in self.cfg.must_keep if s not in t]
            if missing:
                ev.append(GuardEvent("FAIL", "missing_symbols"))

        self._trim_seen()
        hits = 0
        for tri in self._trigrams(t[-4000:]):
            c = self._seen.get(tri, 0) + 1
            self._seen[tri] = c
            if c >= 3:
                hits += 1
        if hits >= self.cfg.max_repeat_trigram_hits:
            ev.append(GuardEvent("WARN", "repetition_trigram"))

        if self._last_len is None or n - self._last_len >= self.cfg.checkpoint_chars:
            self._last_len = n

        if not ev:
            ev.append(GuardEvent("OK", "clean"))
        return ev

    def advise(self, events: List[GuardEvent]) -> str:
        levels = {e.level for e in events}
        if "FAIL" in levels:
            return "Return empty output. Do not guess."
        if "WARN" in levels:
            return "Keep structure. Do not shorten aggressively. Avoid repetition."
        return ""
