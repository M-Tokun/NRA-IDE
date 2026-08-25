"""Deterministic, explainable candidate extraction for UTF-8 text.

The extractor deliberately uses text-oriented names instead of NRA-IDE
structural variables.  A higher threshold is always stricter, and every
accepted line carries the observable reasons that contributed to its score.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import re
import unicodedata
from typing import Iterable, List, Optional, Tuple

from .languages import keywords_for


_HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+\S")
_LIST_RE = re.compile(r"^\s*(?:[-+*]|\d+[.)])\s+\S")
_QUOTE_RE = re.compile(r"^\s*>\s*\S")
_FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})(.*)$")


@dataclass(frozen=True)
class ExtractorConfig:
    """Scoring configuration.

    ``threshold`` is bounded to 0..1 and has one meaning: increasing it can
    only make selection stricter.  Context state is derived from raw content
    scores, not from the threshold, so this monotonic property is preserved.
    """

    threshold: float = 0.80
    language: str = "auto"
    context_bonus: float = 0.08
    context_decay: float = 0.55
    context_trigger: float = 0.72

    def __post_init__(self) -> None:
        for name in ("threshold", "context_bonus", "context_decay", "context_trigger"):
            value = getattr(self, name)
            if not math.isfinite(value) or not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be a finite value between 0 and 1")
        keywords_for(self.language)


@dataclass(frozen=True)
class ExtractedLine:
    """One selected source line and the evidence used to select it."""

    line_number: int
    content: str
    content_score: float
    reasons: Tuple[str, ...]


@dataclass(frozen=True)
class ExtractionResult:
    """Stable extraction result in original source order."""

    total_lines: int
    nonempty_lines: int
    extracted: Tuple[ExtractedLine, ...]

    @property
    def extraction_ratio(self) -> float:
        if self.nonempty_lines == 0:
            return 0.0
        return len(self.extracted) / self.nonempty_lines


class TextExtractor:
    """Score lines from observable text features and keep review candidates."""

    def __init__(self, config: Optional[ExtractorConfig] = None) -> None:
        self.config = config or ExtractorConfig()
        selected_keywords = keywords_for(self.config.language)
        self._ja_keywords = tuple(
            keyword.casefold()
            for keyword in selected_keywords
            if any("\u3040" <= char <= "\u9fff" for char in keyword)
        )
        self._en_keyword_patterns = tuple(
            re.compile(
                r"(?<!\w)"
                + r"\s+".join(re.escape(part) for part in keyword.split())
                + r"(?!\w)",
                re.IGNORECASE,
            )
            for keyword in selected_keywords
            if keyword not in self._ja_keywords
        )

    @staticmethod
    def _signal_density(text: str) -> Tuple[int, float]:
        compact = [char for char in text if not char.isspace()]
        if not compact:
            return 0, 0.0
        signal_count = sum(
            1 for char in compact if unicodedata.category(char)[0] in {"L", "N"}
        )
        return signal_count, signal_count / len(compact)

    @staticmethod
    def _content_units(text: str) -> int:
        """Approximate comparable Japanese and English content length.

        Wide and full-width characters count individually. Latin words and
        digit groups count as two units each, avoiding a raw-character bias
        toward English while keeping the calculation inspectable.
        """
        east_asian_units = sum(
            1 for char in text if unicodedata.east_asian_width(char) in {"W", "F"}
        )
        latin_groups = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?|\d+", text)
        return east_asian_units + 2 * len(latin_groups)

    def _has_profile_keyword(self, text: str) -> bool:
        folded = text.casefold()
        return any(keyword in folded for keyword in self._ja_keywords) or any(
            pattern.search(text) for pattern in self._en_keyword_patterns
        )

    def score_line(
        self,
        text: str,
        context_strength: float = 0.0,
        *,
        allow_markdown_structure: bool = True,
    ) -> Tuple[float, Tuple[str, ...]]:
        """Return a bounded content score and its observable reasons.

        ``text`` is scored without changing its source representation.
        ``context_strength`` applies the configured preceding-line bonus.
        ``allow_markdown_structure`` controls only heading, list, and quotation
        bonuses; callers set it false inside fenced or indented code so code
        syntax is not mistaken for document structure.
        """
        source = text.rstrip("\r\n")
        clean = source.strip()
        if not clean:
            return 0.0, ()

        _, density = self._signal_density(clean)
        content_units = self._content_units(clean)
        length_score = min(1.0, math.log1p(content_units) / math.log1p(60))
        score = 0.62 * length_score + 0.28 * density
        reasons: List[str] = ["length", "signal_density"]

        if allow_markdown_structure and _HEADING_RE.match(source):
            score = max(score + 0.25, 0.82)
            reasons.append("markdown_heading")
        elif allow_markdown_structure and _LIST_RE.match(source):
            score += 0.08
            reasons.append("list_item")
        elif allow_markdown_structure and _QUOTE_RE.match(source):
            score += 0.04
            reasons.append("quotation")

        if self._has_profile_keyword(clean):
            score = max(score + 0.22, 0.82)
            reasons.append("profile_keyword")

        if context_strength > 0.0 and self.config.context_bonus > 0.0:
            score += self.config.context_bonus * context_strength
            reasons.append("preceding_context")

        return min(1.0, max(0.0, score)), tuple(reasons)

    def extract(self, lines: Iterable[str]) -> ExtractionResult:
        """Extract candidates while preserving source order and line numbers."""
        total_lines = 0
        nonempty_lines = 0
        extracted: List[ExtractedLine] = []
        context_strength = 0.0
        fence_char: Optional[str] = None
        fence_length = 0

        for total_lines, raw_line in enumerate(lines, start=1):
            source = raw_line.rstrip("\r\n")
            clean = source.strip()
            if not clean:
                context_strength *= self.config.context_decay
                continue

            nonempty_lines += 1
            fence_match = _FENCE_RE.match(source)
            is_fence_open = fence_char is None and fence_match is not None
            is_fence_close = bool(
                fence_char
                and re.match(
                    rf"^\s{{0,3}}{re.escape(fence_char)}{{{fence_length},}}\s*$",
                    source,
                )
            )
            in_fenced_code = fence_char is not None or is_fence_open
            in_indented_code = source.startswith("\t") or source.startswith("    ")
            allow_structure = not in_fenced_code and not in_indented_code

            score, reasons = self.score_line(
                source,
                context_strength,
                allow_markdown_structure=allow_structure,
            )
            if score >= self.config.threshold:
                context_reasons = list(reasons)
                if in_fenced_code:
                    context_reasons.append("fenced_code")
                elif in_indented_code:
                    context_reasons.append("indented_code")
                extracted.append(
                    ExtractedLine(total_lines, source, score, tuple(context_reasons))
                )

            raw_score, _ = self.score_line(
                source,
                0.0,
                allow_markdown_structure=allow_structure,
            )
            if raw_score >= self.config.context_trigger:
                context_strength = 1.0
            else:
                context_strength *= self.config.context_decay

            if is_fence_close:
                fence_char = None
                fence_length = 0
            elif is_fence_open and fence_match is not None:
                marker = fence_match.group(1)
                fence_char = marker[0]
                fence_length = len(marker)

        return ExtractionResult(total_lines, nonempty_lines, tuple(extracted))


def render_markdown(
    result: ExtractionResult,
    *,
    source_name: str,
    config: ExtractorConfig,
) -> str:
    """Render an auditable Markdown report without adding nondeterministic data."""
    source_code = _markdown_code_span(source_name)
    lines: List[str] = [
        "# NRA-TCM Extractor Report",
        "",
        "> Candidate extraction for human review. This is not a summary, structural measurement, or safety decision.",
        "",
        f"- Source: {source_code}",
        f"- Language profile: {_markdown_code_span(config.language)}",
        f"- Threshold: `{config.threshold:.3f}`",
        f"- Total lines: `{result.total_lines}`",
        f"- Non-empty lines: `{result.nonempty_lines}`",
        f"- Extracted lines: `{len(result.extracted)}`",
        f"- Extraction ratio: `{result.extraction_ratio:.3f}`",
        "",
        "## Extracted Candidates",
        "",
    ]

    if not result.extracted:
        lines.append("No line met the configured threshold.")
    else:
        for item in result.extracted:
            reason_text = ", ".join(item.reasons)
            lines.extend([f"### Line {item.line_number}", ""])
            lines.extend(_markdown_fenced_text(item.content))
            lines.extend(
                [
                    "",
                    f"Score: `{item.content_score:.3f}`; reasons: {_markdown_code_span(reason_text)}",
                    "",
                ]
            )

    return "\n".join(lines).rstrip() + "\n"


def _markdown_code_span(value: str) -> str:
    longest = max((len(run) for run in re.findall(r"`+", value)), default=0)
    delimiter = "`" * (longest + 1)
    padding = " " if value.startswith(("`", " ")) or value.endswith(("`", " ")) else ""
    return f"{delimiter}{padding}{value}{padding}{delimiter}"


def _markdown_fenced_text(value: str) -> List[str]:
    longest = max((len(run) for run in re.findall(r"`+", value)), default=0)
    delimiter = "`" * max(3, longest + 1)
    return [f"{delimiter}text", value, delimiter]
