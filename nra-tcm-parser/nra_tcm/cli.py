"""Command-line interface for NRA-TCM Extractor."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import tempfile
from typing import Optional, Sequence

from . import __version__
from .extractor import ExtractorConfig, TextExtractor, render_markdown
from .languages import SUPPORTED_LANGUAGES


EXIT_INPUT_ERROR = 3
EXIT_OUTPUT_CONFLICT = 4
EXIT_IO_ERROR = 5


def _console_print(message: str, *, error: bool = False) -> None:
    stream = sys.stderr if error else sys.stdout
    encoding = getattr(stream, "encoding", None) or "utf-8"
    safe_message = message.encode(encoding, errors="backslashreplace").decode(encoding)
    print(safe_message, file=stream)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nra-tcm-extract",
        description="Extract explainable review candidates from a UTF-8 text file.",
    )
    parser.add_argument("input", type=Path, help="UTF-8 Markdown or plain-text input")
    parser.add_argument("--version", action="version", version=f"NRA-TCM Extractor {__version__}")
    parser.add_argument("-o", "--output", type=Path, help="output Markdown path")
    parser.add_argument(
        "--language",
        choices=SUPPORTED_LANGUAGES,
        default="auto",
        help="keyword profile (default: auto)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.80,
        help="selection threshold from 0 to 1; higher is stricter (default: 0.80)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace an existing output file",
    )
    return parser


def _default_output(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}_extracted.md")


def _write_output(path: Path, content: str, *, force: bool) -> None:
    if not path.parent.exists():
        raise OSError(f"output directory does not exist: {path.parent}")
    if path.exists() and not force:
        raise FileExistsError(path)

    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent, text=True
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if force:
            os.replace(temporary_path, path)
        else:
            os.link(temporary_path, path)
            temporary_path.unlink()
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        config = ExtractorConfig(threshold=args.threshold, language=args.language)
    except ValueError as exc:
        _console_print(f"Configuration error: {exc}", error=True)
        return EXIT_INPUT_ERROR

    input_path = args.input.resolve()
    output_path = (args.output or _default_output(args.input)).resolve()

    if not input_path.is_file():
        _console_print(f"Input error: file not found: {args.input}", error=True)
        return EXIT_INPUT_ERROR
    if input_path == output_path:
        _console_print("Output conflict: input and output paths must differ.", error=True)
        return EXIT_OUTPUT_CONFLICT
    if output_path.exists() and not args.force:
        _console_print(
            f"Output conflict: {output_path} already exists; use --force to replace it.",
            error=True,
        )
        return EXIT_OUTPUT_CONFLICT

    try:
        with input_path.open("r", encoding="utf-8") as stream:
            result = TextExtractor(config).extract(stream)
    except (OSError, UnicodeError) as exc:
        _console_print(f"Input error: {exc}", error=True)
        return EXIT_INPUT_ERROR

    report = render_markdown(result, source_name=input_path.name, config=config)
    try:
        _write_output(output_path, report, force=args.force)
    except FileExistsError:
        _console_print(
            f"Output conflict: {output_path} already exists; use --force to replace it.",
            error=True,
        )
        return EXIT_OUTPUT_CONFLICT
    except OSError as exc:
        _console_print(f"Output error: {exc}", error=True)
        return EXIT_IO_ERROR

    _console_print(
        f"Extracted {len(result.extracted)} of {result.nonempty_lines} non-empty lines: {output_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
