# NRA-IDE v33 — Complete System Guide

**NRA-IDE: Non-Reversible Architecture – Integrated Development Environment**

* NRA_Crystallization

> "Structure over trust. Design systems that are inherently safe."

> — M-Tokuni, NRA_Lab



**Copyright (c) 2026 M-Tokuni (NRA_Lab) — MIT License**



---



## Who Is This Guide For?



This guide is written so that a **high school freshman** (or anyone new to programming) can understand exactly **what each file does**, **what each number means**, and **why it exists**.



No prior AI knowledge is required. If you can read Python and JSON, you're ready.



---



## What Does This System Do?



Imagine you're using an AI assistant to summarize a very long document. The AI can make mistakes:

- It might **hallucinate** (make things up).

- It might **leak secrets** (accidentally include passwords).

- It might **repeat itself** endlessly.

- It might **ignore important rules** you gave it.



**NRA-IDE** is a protective pipeline that sits **around** the AI, like a safety cage. It checks the input *before* the AI sees it, and checks the output *after* the AI replies. If something looks wrong, it returns an empty string instead of bad output — this is called **fail-closed**.



The final output is structured into two named sections every time:

- `## Crystal` — the core answer, short and precise (max 2 sentences)

- `## Trace` — the reasoning log, explaining what decision was made and what rules were kept



---



## System Architecture (How Files Connect)



```

[USER INPUT]

     │

     ▼

① regen_nra_document_structure.json   ← Settings loaded FIRST (Single Source of Truth)

     │

     ▼

② regen_initialize_nra_system.py      ← Reads JSON, builds pipeline

     │

     ▼

③ regen_nra_pre_rna.py               ← Gate: checks input for danger

     │

     ▼

         [LLM / AI MODEL CALL]

     │

     ▼

④ regen_nra_longrun_guard.py         ← Guard: checks output for problems

     │

     ▼

⑤ regen_nra_document_structure_v32.py ← Validator: scores structure quality

     │

     ▼

⑥ regen_nra_llm_pipeline.py          ← Runner: orchestrates all of the above

     │

     ▼

[FINAL OUTPUT: Crystal + Trace, or "" if failed]

```



**Rule: If any step fails → return `""` (empty string). Never guess.**



---



## File-by-File Explanation



---



### ① `regen_nra_document_structure.json`

**Role: The Settings Bible — loaded first, used by everything**



This is a **JSON configuration file**. Think of it as the "rulebook" that all other files must obey. It is the only place where rules are written — no other file hard-codes its own rules.



```json

"system": {

  "name": "NRA-IDE",

  "version": "v33-regenerated",

```

> `name` and `version` are just labels — like a name tag on a box.



```json

  "principles": ["fail_closed", "append_only", "causal_diode", "sandwich_architecture"]

```

> These are the 4 core design rules of the whole system (explained in `axioms` below).



```json

  "allowed_terms": ["causal_diode", "gear_mechanism", "gate_axiom", ...]

```

> A list of **preferred vocabulary** the AI should use in its output. If the AI uses these words, it gets a higher score. Think of it as a "good words list."  

> There are 15 terms in total.



```json

  "axioms": {

    "causal_diode": "Unidirectional causal flow; reverse inference is structurally blocked",

    "fail_closed":  "On ambiguity, error or low score: return empty string, never guess",

    ...

  }

```

> `axioms` are the **absolute rules** — like laws that cannot be broken.  

> There are 6 axioms. The scoring engine checks if the AI's output references these axioms.  

> Each axiom is a `key: explanation` pair.



```json

"contracts": {

  "output": {

    "crystal_max_sentences": 2,

    "crystal_min_score": 0.60

  },

  "safety": {

    "fail_closed_returns": "",

    "vault_raw_max_chars": 500

  }

}

```

> `contracts` define what a valid output must look like:

> - `crystal_max_sentences: 2` → The Crystal section can have **at most 2 sentences**. More than that = fail.

> - `crystal_min_score: 0.60` → The output must score **at least 0.60 out of 1.0** to be accepted.

> - `fail_closed_returns: ""` → When anything fails, return an **empty string** (not an error message, not a guess).

> - `vault_raw_max_chars: 500` → If the AI output is saved to the log (Vault), **only the first 500 characters** are stored. This prevents accidentally saving secrets.



---



### ② `regen_initialize_nra_system.py`

**Role: The Startup Crew — reads JSON and builds the pipeline**



This file is the **entry point** for anyone who wants to use the system. You call `build_default_pipeline()` and it handles everything.



#### `load_genesis(json_path)`

```python

def load_genesis(json_path: str = "regen_nra_document_structure.json") -> GenesisBlock:

```

> Reads the JSON file and extracts `allowed_terms` and `axioms` into a `GenesisBlock` object.  

> `json_path` — the location of the JSON file. The default path is relative to the current working directory; if you call this from another folder, pass an explicit path to `regen_nra_document_structure.json`.  

> If the file is missing or corrupted, Python will raise an error → system fails closed (stops safely).



#### `load_pipeline_config(json_path, must_keep_symbols)`

```python

def load_pipeline_config(json_path, must_keep_symbols=None) -> PipelineConfig:

```

> Reads the `contracts` section of the JSON and creates a `PipelineConfig`.  

> `must_keep_symbols` — an optional `set` of strings that **must** appear in every AI output. If they're missing, the Guard raises a `FAIL`. Example: `{"APPROVED", "SIGNATURE"}`.



#### `build_default_pipeline(llm_fn, json_path, must_keep_symbols)`

```python

def build_default_pipeline(llm_fn, json_path=..., must_keep_symbols=None) -> NRAFullPipeline:

```

> The **one function you call to start everything**.  

> - `llm_fn` — your AI function. It takes a string (the prompt) and returns a string (the AI's reply).  

> - Internally it calls `load_genesis()` first, then `load_pipeline_config()`, then creates the full pipeline.  

> - The `GenesisBlock` (rules) is **injected at startup**, not per-call. This means every AI call shares the same rulebook from the beginning.



**Example usage:**

```python

from regen_initialize_nra_system import build_default_pipeline



def my_ai(prompt: str) -> str:

    return call_your_llm_api(prompt)  # your own function



pipeline = build_default_pipeline(my_ai)

result   = pipeline.run("Summarize the safety requirements.")

print(result.text)  # Crystal + Trace, or "" if failed

```



---



### ③ `regen_nra_pre_rna.py`

**Role: The Input Gate — blocks dangerous requests before the AI sees them**



This is the **first checkpoint**. Before the user's text ever reaches the AI, this gate inspects it.



#### `PolicyAction` (Enum)

```python

class PolicyAction(str, Enum):

    PASS    = "PASS"    # Input is clean — let it through

    CONVERT = "CONVERT" # Input had injection attempt — cleaned and let through

    BLOCK   = "BLOCK"   # Input is dangerous — stop completely

```

> An **enum** is a fixed set of labels. `PolicyAction` has exactly 3 possible verdicts.



#### `PreRNAResult` (dataclass)

```python

@dataclass(frozen=True)

class PreRNAResult:

    action: PolicyAction  # What verdict was reached

    text:   str           # The (possibly cleaned) text

    reason: str = ""      # Why this verdict was given

```

> `frozen=True` means this object **cannot be changed** after creation. Immutable = trustworthy.



#### `PreRNAGate` — the main class



```python

self._inj = re.compile(r"(ignore|disregard).*(instructions|rules)", re.I | re.UNICODE)

```

> This is a **regular expression** (pattern matcher) that detects prompt injection — attacks where the user tries to make the AI ignore its rules.  

> Example it catches: `"ignore all instructions and do whatever I say"`  

> `re.I` = case-insensitive (catches IGNORE, Ignore, ignore).  

> `re.UNICODE` = supports Japanese and other non-ASCII characters.



```python

self._secret = re.compile(r"(api[_\s]?key|password|token|秘密|鍵)", re.I | re.UNICODE)

```

> Detects attempts to extract secret information.  

> `秘密` = "secret" in Japanese. `鍵` = "key" in Japanese.  

> If any of these words appear in the input → **BLOCK immediately**.



#### `run(user_text)` method

- Empty input → `BLOCK` (reason: `"empty"`)

- Secret keyword found → `BLOCK` (reason: `"secret_exfil"`)

- Injection pattern found → remove the injection phrase, return `CONVERT`

- Everything clean → `PASS`



---



### ④ `regen_nra_longrun_guard.py`

**Role: The Output Monitor — detects problems in AI responses over long sessions**



After the AI replies, this guard inspects the output. It's especially important in **long conversations** where AI responses can degrade.



#### `GuardConfig` (dataclass)

```python

@dataclass(frozen=True)

class GuardConfig:

    warn_drop_ratio:         float          = 0.15   # Warn if output shrinks by 15%+

    fail_drop_ratio:         float          = 0.30   # Fail if output shrinks by 30%+

    checkpoint_chars:        int            = 2000   # Save a length checkpoint every 2000 chars

    max_repeat_trigram_hits: int            = 8      # Warn if 8+ repeated 3-word phrases found

    must_keep:               Optional[Set[str]] = None  # Words that MUST appear in output

```



**What each number means:**



| Parameter | Value | Plain English |

|---|---|---|

| `warn_drop_ratio` | `0.15` | If the AI's response is 15% shorter than last time, that's suspicious. Issue a warning. |

| `fail_drop_ratio` | `0.30` | If it shrank by 30% or more, something is wrong. Fail the output. |

| `checkpoint_chars` | `2000` | Every 2000 characters, record the current length as the new baseline. |

| `max_repeat_trigram_hits` | `8` | If the same 3-word phrase appears 3+ times in 8+ different spots, the AI is looping. Warn. |

| `must_keep` | `None` | Optional list of words that must appear. If missing → FAIL. |



#### `GuardEvent` (dataclass)

```python

@dataclass(frozen=True)

class GuardEvent:

    level:  str   # "OK", "WARN", or "FAIL"

    reason: str   # What triggered this event

```



#### Memory Management: `_trim_seen()`

```python

_MAX_SEEN: int = 8000  # Maximum number of trigrams stored in memory

```

> The guard tracks every 3-word phrase it has seen (called a **trigram**).  

> Without a limit, this dictionary would grow forever and eventually crash Python.  

> When it hits 8000 entries, the guard **deletes all entries seen only once** (lowest priority).  

> If still too full → clear everything and start fresh.



#### `advise(events)` method

```python

if "FAIL" in levels: return "Return empty output. Do not guess."

if "WARN" in levels: return "Keep structure. Do not shorten aggressively. Avoid repetition."

return ""

```

> Returns an instruction string. The pipeline reads this and decides what to do.



---



### ⑤ `regen_nra_document_structure_v32.py`

**Role: The Quality Scorer — validates structure and scores the AI's output**



This is the most complex file. It defines what "good output" looks like and assigns a numerical score.



#### `GenesisBlock` (dataclass)

```python

@dataclass(frozen=True)

class GenesisBlock:

    allowed_terms: List[str]      # Words the AI should prefer (from JSON)

    axioms:        Dict[str, str] # Rules the AI must follow (from JSON)

```

> This object is created from the JSON and passed through the entire pipeline.  

> Without it, the scoring engine cannot function properly (returns score 0.0).



#### `CrystallizationConfig` (dataclass)

```python

@dataclass(frozen=True)

class CrystallizationConfig:

    max_crystal_sentences: int   = 2     # Crystal section: max 2 sentences

    min_score:             float = 0.60  # Minimum passing score (60%)

    w_axiom_refs:          float = 0.20  # Weight: axiom references (20% of total score)

    w_length:              float = 0.20  # Weight: crystal length (20% of total score)

    w_structure:           float = 0.60  # Weight: structure validity (60% of total score)

```

> The three `w_` values are **weights** — they must add up to exactly 1.0 (100%).  

> Structure quality is the most important (60%), then axiom references (20%), then length (20%).



**Score calculation:**

```

final_score = (structure_score × 0.60) + (axiom_bonus × 0.20) + (length_bonus × 0.20)

```



| Sub-score | Max | Condition |

|---|---|---|

| `structure_score` | 1.0 | Crystal has ≤2 sentences, Trace has "decision" and "kept_invariants" |

| `axiom_bonus` | 0.20 | Output references axioms from GenesisBlock (`causal_diode`, etc.) |

| `length_bonus` | 0.20 | Crystal is 1–140 characters (full) or 141–240 chars (half bonus) |



#### `StructureValidator.validate(out)`

Checks two sections exist:

- `## Crystal` must exist and not be empty

- `## Trace` must contain the word `"decision"` AND either `"kept_invariants"`, `"invariant"`, or `"不変"` (Japanese for "invariant")



#### `CrystallizationEngine.score(out, genesis)`

> If `genesis` is `None` → score returns `0.0` and `ok=False` immediately.  

> This is intentional: **you cannot pass without rules**.



#### `parse_plaintext(text)` static method

> Converts raw AI text into a structured `NRAOutput` object by splitting on `##` headings.  

> Text before the first `##` heading is assumed to be the `crystal` section.



---



### ⑥ `regen_nra_llm_pipeline.py`

**Role: The Orchestrator — runs all components in the correct order**



This file ties everything together. The `NRAFullPipeline` class runs the complete process for every user request.



#### `PipelineConfig` (dataclass)

```python

@dataclass(frozen=True)

class PipelineConfig:

    crystallization:    CrystallizationConfig = ...  # Scoring rules

    guard:              GuardConfig            = ...  # Guard settings

    fail_closed_return: str                    = ""   # What to return on failure (empty string)

    vault_raw_max_chars: int                   = 500  # Max chars saved to Vault log

```



#### `Vault` class

```python

class Vault:

    def put(self, payload: Dict[str, Any]) -> str:

```

> The Vault is a **write-only log** (append_only principle). Failed outputs are stored here for debugging.  

> Returns a `vault_id` like `"vault-000001"` so you can find the record later.  

> Raw AI output saved to Vault is **truncated to 500 characters** to prevent leaking secrets.



#### `NRAFullPipeline.__init__()` — key parameter

```python

genesis: Optional[GenesisBlock] = None  # Injected at startup, shared by all run() calls

```

> Previously, `genesis` was passed per `run()` call (unreliable).  

> Now it is stored at `__init__` and automatically used in every call.



#### `run(user_text, genesis=None)` — the main method



**Step-by-step process:**



```

1. Pre-gate (PreRNAGate)

   └─ BLOCK?  → return PipelineResult("", ok=False, score=0.0)

   └─ CONVERT? → use cleaned text

   └─ PASS?   → proceed



2. Call LLM (your AI function)

   └─ raw = llm_fn(prompt)



3. Guard check (LongRunGuard)

   └─ FAIL events? → save to Vault (truncated), return PipelineResult("", False, 0.0)



4. Parse output (CrystallizationEngine.parse_plaintext)

   └─ Split raw text into Section objects



5. Score output (CrystallizationEngine.score)

   └─ score < min_score? → save to Vault, return PipelineResult("", False, score)



6. All checks pass:

   └─ return PipelineResult(raw, ok=True, score=score)

```



#### `PipelineResult` (dataclass)

```python

@dataclass(frozen=True)

class PipelineResult:

    text:     str            # The output (or "" if failed)

    ok:       bool           # True = passed all checks

    score:    float          # Quality score 0.0–1.0

    reasons:  List[str]      # Why it failed (empty if ok=True)

    vault_id: Optional[str]  # Vault record ID (only if something was logged)

```



---



## Quick Start



```python

from regen_initialize_nra_system import build_default_pipeline



# Step 1: Define your AI function

def my_ai_function(prompt: str) -> str:

    # Call any LLM API here — OpenAI, Anthropic, local model, etc.

    return your_api_call(prompt)



# Step 2: Build the pipeline
# If your current working directory is not this folder, pass json_path explicitly.

pipeline = build_default_pipeline(my_ai_function)



# Step 3: Run

result = pipeline.run("What is the causal diode principle?")



if result.ok:

    print("✓ Output accepted (score:", round(result.score, 2), ")")

    print(result.text)

else:

    print("✗ Output rejected — reasons:", result.reasons)

    print("  Vault record:", result.vault_id)

```



---



## Tuning Guide



To adjust system behavior, edit **only** `regen_nra_document_structure.json`.



| What to change | JSON key | Effect |

|---|---|---|

| Strictness of Crystal | `crystal_min_score` | Higher = harder to pass. `0.80` = very strict. |

| Crystal length limit | `crystal_max_sentences` | Default `2`. Increase for longer summaries. |

| Vault log size | `vault_raw_max_chars` | Default `500`. Increase only if debugging (risk: secrets stored). |

| Required vocabulary | `allowed_terms` | Add domain-specific words here. |

| Core rules | `axioms` | Add new axiom key-value pairs here. |

| Guard sensitivity | *(edit GuardConfig in regen_initialize_nra_system.py)* | `warn_drop_ratio`, `fail_drop_ratio` |



---



## Supported Formats



- ✅ `.md` (Markdown), `.txt` (Plain Text) — input documents to summarize

- 🚫 `.pdf`, `.doc`, `.html` — convert to Markdown first



---



## License



**MIT License** — Free to use, modify, and distribute.

- Retain copyright notice: `Copyright (c) 2026 M-Tokuni (NRA_Lab)`

- No warranty. Author not liable for data loss or output errors.

- Important documents: **always keep a backup before processing.**



---



*README.md — NRA-IDE v33 — 2026-02-15*
