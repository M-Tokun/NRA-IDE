"""Language profiles used by the explainable text extractor."""

from __future__ import annotations

from typing import Dict, Tuple


LANGUAGE_KEYWORDS: Dict[str, Tuple[str, ...]] = {
    "ja": (
        "結論",
        "しかし",
        "重要",
        "核心",
        "特異点",
        "つまり",
        "要するに",
        "結局",
        "まとめると",
        "注意",
        "警告",
        "エラー",
    ),
    "en": (
        "conclusion",
        "however",
        "important",
        "critical",
        "result",
        "warning",
        "error",
        "therefore",
        "in summary",
    ),
}

SUPPORTED_LANGUAGES = ("auto", "ja", "en")


def keywords_for(language: str) -> Tuple[str, ...]:
    """Return a stable keyword tuple for a supported language profile."""
    if language == "auto":
        return tuple(dict.fromkeys(LANGUAGE_KEYWORDS["ja"] + LANGUAGE_KEYWORDS["en"]))
    try:
        return LANGUAGE_KEYWORDS[language]
    except KeyError as exc:
        supported = ", ".join(SUPPORTED_LANGUAGES)
        raise ValueError(f"unsupported language profile: {language!r}; choose {supported}") from exc
