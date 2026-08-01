# PaperTrail — Product Requirements Document

## 1. Overview

PaperTrail is a CLI tool that helps ML researchers and engineers figure out whether they can actually reproduce a paper's results from its linked GitHub repo, and exactly what's missing if they can't.

Given an arXiv paper and its associated GitHub repo, the tool cross-references the paper's stated experimental setup (hyperparameters, dataset, hardware, environment) against what the repo actually provides, and produces a clear, confidence-rated gap report.

## 2. Problem Statement

Reproducibility is a widely acknowledged, unsolved problem in ML research. Papers claim results; repos are supposed to let you get those results yourself. In practice, papers and repos drift apart: hyperparameters go unstated, defaults get changed after publication, dataset links rot, environment details are assumed rather than documented. Today, catching these gaps means manually reading the paper's appendix side-by-side with the repo's README and config files, tedious, error-prone, and something almost every ML practitioner has done at least once out of frustration.

Existing related work (ReproRepo, PaperBench, "What Papers Don't Tell You," Paper2Code) treats this as a benchmark problem for evaluating frontier agents, not a tool a person actually opens and runs. PaperTrail is the practical, personal-use counterpart: a tool you point at a paper and a repo to get an honest answer about what you're missing before you burn hours finding out the hard way.

## 3. Goals

- Build a working, usable CLI tool in about one week
- Fill genuine RAG and agentic-workflow experience gaps (per prior interview prep planning)
- Produce something demoable end-to-end against real papers
- Zero ongoing cost to the builder — no API bills from other people's usage (BYOK model)
- Use current, relevant tooling (open-weight HF models, current embedding models) so the stack itself is a talking point

## 4. Non-Goals (for v1)

- Not a hosted public website (may come later, once the core engine is validated)
- Not a benchmark or research contribution — not trying to beat PaperBench/ReproRepo numbers
- Not multi-language repo support — Python-only for v1
- Not full snippet execution/testing in v1 (that's Stage 2 scope)
- Not a general-purpose paper QA / chat tool

## 5. User & Use Case

Primary user: an ML researcher, grad student, or engineer (including the builder, who has lived this problem through his own interpretability research) who has found a paper they want to reproduce and has the linked GitHub repo, and wants to know, before investing real time, what's likely to work and what's likely to be missing or mismatched.

Core use case: `papertrail check <arxiv-url> <repo-url>` → structured report.

## 6. Staged Scope

### Stage 1 — Gap Finder (primary deliverable, build this solidly)

Given a paper + repo, produce a checklist-style report:
- Which hyperparameters the paper states, and whether the repo's defaults/configs match, are missing, or mismatch
- Whether the paper's dataset is linked, publicly accessible, and referenced/handled in the repo
- Whether the environment/dependencies are fully specified (pinned requirements, documented hardware/software versions)
- Confidence-tagged findings: high-confidence (deterministic structural matches) vs. lower-confidence (LLM-inferred from prose)

### Stage 2 — Sandboxed Run Attempt (stretch goal, attempt only after Stage 1 is solid)

- Spin up the repo in an isolated Docker container
- Attempt install + a minimal run using the extracted config
- On error, feed the error back into an agent loop that checks it against paper/README context and retries (bounded retry count, e.g. max 3 attempts)
- This is the higher-risk, higher-reward piece — genuine observe-error-adjust-retry agentic behavior, but with real security (arbitrary repo code execution) and flakiness considerations

## 7. Architecture

### 7.1 Pipeline (Stage 1)

1. **Paper ingestion** — accept an arXiv URL or local PDF; extract text via `pymupdf`; isolate relevant sections (experimental setup, hyperparameter tables, dataset description, hardware/environment notes) using section-header heuristics first, LLM-assisted if heuristics come up short
2. **Structured extraction (F2)** — LLM call over the isolated paper sections, outputs structured JSON: hyperparameters (name, value), dataset name + link if present, hardware/environment notes. This is the highest-risk step and should be prototyped against real papers before the rest of the pipeline is built.
3. **Repo ingestion (F3)** — clone the repo; parse README (Markdown); parse config files (YAML/JSON) and entry-point script argument defaults via Python's `ast` module; extract `requirements.txt`/`environment.yml`
4. **Cross-reference engine (F4)** — diff extracted paper hyperparameters against actual repo defaults (matched / missing / mismatched, with fuzzy name-normalization, e.g. paper's "Dropout Prob" vs. repo's `lora_dropout` flag); check dataset link liveness and repo-side handling; check environment/dependency completeness
5. **Report generation (F5)** — human-readable checklist (CLI-printed + saved Markdown/JSON report), confidence-tagged per finding
6. **CLI packaging (F6)** — `pip install`-able, `papertrail check <arxiv-url> <repo-url>` command

### 7.2 Tech Stack

| Component | Choice | Notes |
|---|---|---|
| Language | Python | matches existing strength |
| PDF parsing | `pymupdf` (fitz) | handles arXiv PDFs including basic layout |
| LLM (primary) | Claude API via BYOK | user supplies their own key via env var; best extraction quality |
| LLM (fallback) | Local open-weight HF model (Qwen3 or Llama 3.x instruct, 7-8B class) | used when no API key is set; free, weaker on messy/prose-heavy extraction |
| Repo/code parsing | Python `ast` module | config defaults, argparse parsing |
| Embeddings (if needed for report search/history) | `sentence-transformers` (e.g. BGE/E5 variant) | current, strong, free |
| Vector DB (optional, v1.1+) | Chroma | embedded, no server; adds value once supporting search across multiple past reports, not required for a single paper+repo run |
| Backend/CLI framework | FastAPI (if any local API surface is needed) + standard Python CLI (e.g. `click` or `argparse`) | |
| Sandboxing (Stage 2) | Docker | isolated container per run attempt |

### 7.3 BYOK / Cost Model

- CLI reads API key from environment variable (e.g. `ANTHROPIC_API_KEY`) or a config file / `--api-key` flag
- If a key is present → use Claude for extraction (best quality)
- If no key is present → fall back to local HF model (free, functional, lower accuracy on ambiguous prose)
- No usage ever routes through or is paid for by the builder; standard BYOK pattern used by comparable dev CLIs
- Builder's own API key is used only for development/testing/demo purposes

## 8. Validation / Prototyping Findings

An initial manual prototype was run against the LoRA paper (arXiv:2106.09685) and its repo (`microsoft/LoRA`), chosen as a "clean, well-documented" test case.

**Result:** cross-referencing the paper's Table 11 (GPT-2 hyperparameters) against the repo's README reproduction command showed near-perfect structural matches (batch size, learning rate, weight decay, epochs, warmup steps, LoRA rank/alpha, label smoothing all matched exactly). Notably, the repo's README also pins `--random_seed 110`, a detail not surfaced in the paper's hyperparameter table, exactly the kind of subtle, real gap the tool is meant to catch.

**Conclusion:** the core cross-referencing mechanic is sound on well-documented pairs. Remaining open question, to validate next: how the pipeline degrades on a messier, less-documented paper+repo pair (recommended as a follow-up prototyping pass before or during Day 1 of the build).

## 9. Success Criteria (v1)

- Runs end-to-end on at least 3-5 real, distinct paper+repo pairs without crashing
- Produces at least one genuinely useful, non-obvious finding per test paper (something a careful human might miss on first read)
- Confidence tagging meaningfully distinguishes reliable structural findings from LLM-inferred guesses
- Works in both BYOK and local-fallback modes
- Installable and runnable via a documented CLI command

## 10. Build Plan (rough day-by-day)

| Day | Focus |
|---|---|
| 1 | Paper ingestion + LLM-based hyperparameter/setup extraction (F1, F2). Prototype against 2-3 more real papers, including at least one messy one, before proceeding. |
| 2 | Repo ingestion (F3): README, config, `ast`-based argument parsing. Cross-reference engine v1 (F4). |
| 3 | Dataset/environment checks. Refine extraction accuracy based on Day 1 findings. |
| 4 | Report generation (F5). Validate against 3-5 real paper+repo pairs; fix what breaks. |
| 5 | CLI packaging (F6): BYOK/local-fallback config, `pip install`-able package. |
| 6 | Stage 2 attempt (F7), if Days 1-5 are on schedule: Docker sandboxing, minimal run attempt, bounded error-feedback retry loop. |
| 7 | Polish, write-up (including explicit acknowledgment of related prior work: ReproRepo, PaperBench, etc.), demo recording. |

## 11. Risks

- **Extraction quality on messy/inconsistent papers** — the biggest open risk; papers vary wildly in how (and whether) they state reproduction details. Mitigate by prototyping against a deliberately messy paper early.
- **Doc-to-code / paper-to-code linking ambiguity** — fuzzy name matching (paper prose vs. repo flag names) needs to be robust enough not to produce false mismatches.
- **Local fallback model quality** — meaningfully weaker than Claude on nuanced prose extraction; should be clearly labeled as lower-confidence in output.
- **Stage 2 scope creep** — sandboxed execution is a real security and flakiness surface; strictly time-boxed and treated as optional stretch, not core deliverable.

## 12. Positioning Note

This tool is explicitly framed as a practical companion to, not a competitor with, existing academic reproducibility research (ReproRepo, PaperBench, Paper2Code, "What Papers Don't Tell You"). Those are benchmarks measuring whether frontier agents can do this at scale; PaperTrail is the tool a person actually runs today when they're stuck on one specific paper. This distinction should be stated explicitly in the project README.
