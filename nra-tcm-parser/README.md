# NRA-TCM Extractor 1.0

NRA-TCM Extractor selects explainable review candidates from large UTF-8 Markdown and plain-text documents.

It is a deterministic text-processing aid for humans. It is not a semantic summarizer, an NRA-IDE structural evaluator, a measuring instrument, or a safety gate. Its output must be reviewed against the source document.

The current implementation replaces the former language-specific crystallizer scripts with one shared engine and explicit Japanese, English, and combined keyword profiles.

## Features

- Standard-library-only Python implementation
- Streaming input processing
- Stable source order and line numbers
- Explainable scores based on observable text features
- Japanese, English, and combined keyword profiles
- A monotonic threshold: a higher value is always stricter
- Deterministic Markdown reports without timestamps
- No output replacement unless `--force` is explicitly supplied

## Requirements

- Python 3.10 or later
- No third-party packages
- UTF-8 input

## Usage

From the repository root:

```console
python nra-tcm-parser/extract.py INPUT.md
```

The default output is created beside the input as `INPUT_extracted.md`.

Specify the language profile, threshold, and output path when needed:

```console
python nra-tcm-parser/extract.py INPUT.md \
  --language en \
  --threshold 0.70 \
  --output RESULT.md
```

On PowerShell, enter the same options on one line or use PowerShell's continuation syntax.

### Options

| Option | Meaning |
|---|---|
| `--language auto` | Use the combined Japanese and English keyword profile; this is the default |
| `--language ja` | Use the Japanese keyword profile |
| `--language en` | Use the English keyword profile |
| `--threshold VALUE` | Select lines scoring at least `VALUE`, from `0` to `1`; higher is stricter; the default is `0.80` |
| `--output PATH` | Write the report to an explicit path |
| `--force` | Replace an existing output file |

Without `--force`, an existing output is preserved and the command exits with a conflict error. The input path can never be used as the output path.

## Scoring Contract

The extractor assigns a bounded `content_score` from observable features:

- content length on a logarithmic scale, using East Asian characters and Latin word groups as comparable units;
- ratio of letter and number characters to non-whitespace characters;
- Markdown headings, list items, and quotations;
- keywords from the selected language profile;
- a small, decaying bonus after a strongly scored preceding line.

Every selected line includes its score and reasons in the report. The threshold affects selection only; it does not alter feature scoring. Therefore increasing the threshold cannot make selection looser.

English keywords use word and phrase boundaries. Japanese keywords use substring matching. Markdown heading, list, and quotation bonuses are disabled inside fenced or indented code, while keyword and content scoring remain available for code lines.

The score expresses extraction priority, not factual correctness, semantic importance, risk, or an NRA-IDE boundary state.

## Python API

Run Python from the `nra-tcm-parser` directory or add that directory to the module search path:

```python
from nra_tcm import ExtractorConfig, TextExtractor, render_markdown

config = ExtractorConfig(language="en", threshold=0.70)
result = TextExtractor(config).extract(["# Result\n", "Important finding.\n"])
report = render_markdown(result, source_name="example.md", config=config)
```

## Output Contract

The Markdown report records:

- source filename;
- selected language profile and threshold;
- total and non-empty line counts;
- extracted line count and ratio;
- source line number, content score, and reasons for every candidate.

The report preserves selected lines in source order and retains their leading and trailing whitespace, excluding the line-ending sequence. Candidate text is placed inside a dynamically sized Markdown code fence so embedded Markdown or HTML remains review text rather than report structure. The extractor does not combine or claim to summarize the source.

## Scale and Calibration Boundaries

Input lines are consumed incrementally, but every selected candidate is retained in the `ExtractionResult`, and the final Markdown report is assembled in memory. Memory use therefore grows with selected output size. Split exceptionally large, high-retention jobs into bounded inputs when memory is constrained.

The default threshold of `0.80` is an explainable heuristic starting point, not a domain-validated accuracy claim. Tune it against human-reviewed examples for each document class. Scores should not be compared across unrelated domains as if they were calibrated measurements.

## Development and Verification

From the repository root:

```console
python -m unittest tests.test_nra_tcm_extractor -v
```

The expected result is `Ran 21 tests` followed by `OK`. These tests are also included in the repository-wide `python -m unittest discover -v` command and CI workflow.

The tests cover threshold direction, language profiles and word boundaries, Markdown and code regions, source preservation, safe report rendering, CP932 console fallback, UTF-8 failure, output conflicts, explicit replacement, and legacy removal.

## Migration

The shared `nra_tcm` package supersedes the former Japanese v3.1 and English v2 crystallizer implementations. The former `delta`, `tau`, `R`, and `momentum` names are intentionally not part of the new text-extraction API because this tool does not calculate canonical NRA-IDE structural variables.

Previous implementations remain recoverable from Git history instead of being kept as competing current files.

The former experimental v33 LLM pipeline had a different responsibility and is not part of Extractor 1.0. It has also been removed from the current tree; its historical implementation remains available through Git history.

## License

This directory follows the repository's [MIT License](../LICENSE).
