"""NRA-TCM Extractor public API.

This package extracts review candidates from UTF-8 text.  It is not an
NRA-IDE structural evaluator, measuring instrument, or safety gate.
"""

from .extractor import (
    ExtractedLine,
    ExtractionResult,
    ExtractorConfig,
    TextExtractor,
    render_markdown,
)

__version__ = "1.0.0"

__all__ = [
    "ExtractedLine",
    "ExtractionResult",
    "ExtractorConfig",
    "TextExtractor",
    "render_markdown",
    "__version__",
]
