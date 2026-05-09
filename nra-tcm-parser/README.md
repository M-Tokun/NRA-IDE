

# NRA-TCM Parser

**Dynamic Text Extraction & Filtering Tool for Long Documents**



## 1. Overview

**NRA-TCM Parser** is a Python-based utility designed to process large-scale text documents (1500+ pages / 1M tokens).



Unlike simple truncation or standard summarization, this tool utilizes **Adaptive Thresholding** and **Structure-Based Weighting** to identify and extract high-value information. It efficiently separates "core content" from "noise" based on the document's structure and semantic density, making it ideal for analyzing technical documentation, logs, and academic papers.



## 2. Key Features



### 🔹 Adaptive Context Filtering (Dynamic Threshold)

The system does not use a fixed filter. It dynamically adjusts its sensitivity based on the **Contextual Density (Momentum)** of the text.

- **High Density:** When relevant information clusters, the filter relaxes to capture details.

- **Low Density:** When noise increases, the filter tightens to skip irrelevant sections.

This mimics a human reader's ability to "skim" or "read deeply" depending on the content's quality.



### 🔹 Singularity Detection (Keyword Recovery)

Even in sections with low context scores, the system actively scans for **Critical Keywords** (e.g., "Conclusion", "However", "Important", "Error").

This ensures that vital warnings or insights are never missed, even if they appear in otherwise less important sections.



### 🔹 Hierarchical Weighting

This tool leverages Markdown structure (`#`, `##`, `###`).

It applies a weighting algorithm where deeper indentation levels (often containing specific details or root causes) are prioritized over generic high-level headings.



## 3. Requirements

- **Python 3.8+**

- **Standard Library Only** (`os`, `sys`, `re`, `math`, `dataclasses`)

- No external dependencies required.



## 4. Usage



### Basic Command

Run the script with your target Markdown or Text file.



```bash

python nra_crystallizer_EN_v2.py input_document.md



```



### Output



A structured report will be generated in the same directory:



* `input_document_Crystallized_EN_YYYY-MMDD.md`



The report is divided into:



1. **Critical Highlights:** Key insights detected via keywords.

2. **Contextual Extracts:** Information preserved by the adaptive filter.



## 5. Configuration (Tuning)



You can adjust the filtering sensitivity by modifying `BASE_TAU` in the script.



```python

# nra_crystallizer_EN_v2.py : Line 15

BASE_TAU = 0.45  # Recommended for English documents



```



| Value | Mode | Description |

| --- | --- | --- |

| **0.35** | **Strict** | Extracts only the most critical points. |

| **0.45** | **Standard** | **Recommended for English.** Balances context and brevity. |

| **0.55** | **Loose** | Retains more details and supporting text. |



*Note: For English text, the default `BASE_TAU` is slightly higher than the Japanese version due to differences in token density.*



## 6. Supported Formats



To ensure accurate parsing, please use structured text formats.



* ✅ **Supported:** `.md` (Markdown), `.txt` (Plain Text)

* 🚫 **Unsupported:** `.pdf`, `.doc`, `.html` (Please convert to Markdown first)



## 7. License



This project is licensed under the **MIT License**.



* **Free to Use:** You are free to use, modify, and distribute this software for personal, academic, or commercial purposes.

* **Attribution:** Please retain the copyright notice (`Copyright (c) 2026 M-Tokuni`) in any distributions.

* **Disclaimer:** This software is provided "as is", without warranty of any kind. The author is not liable for any damages or data loss arising from its use.



**Copyright (c) 2026 M-Tokuni (NRA_Lab)**



