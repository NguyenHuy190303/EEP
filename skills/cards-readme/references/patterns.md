# Patterns that render on both the Hub and GitHub

Verified 2026-09-15 by reading rendered cards on the Hub (`Qwen/Qwen3-8B` uses `<a>` + `<img>`
badges; `HuggingFaceFW/fineweb` uses `<center>` + `<img>`) and the Hub docs (`#hf-light-mode-only`,
KaTeX). GitHub renders the same subset. Anything not listed here: push to a private repo and look.

## Section order

**Model card**
1. YAML metadata
2. Hero: `# Name`, tagline, badge row, optional image
3. Highlights (3–5 bullets)
4. Quickstart (one runnable block, version pinned)
5. Model overview (spec table)
6. Results (table + source column; details block for the full breakdown)
7. Training (data, recipe, hardware, time — details block for the full config)
8. Intended use & limitations (specific)
9. License, citation, acknowledgements

**Dataset card**
1. YAML metadata (incl. `configs` and `dataset_info`)
2. Hero + tagline + badges
3. What is in it: one row example, field table
4. Splits and sizes table
5. How it was built (source → filter → dedup, counts per stage)
6. How to load (one block, `datasets` + streaming variant if large)
7. Known limitations, PII/consent handling, license of the source
8. Citation

**GitHub README**
1. Hero + tagline + badges (CI, license, PyPI/npm, docs)
2. Demo image or GIF (≤5 MB, one)
3. Why / what it does (3–5 bullets)
4. Install + 10-line usage
5. Features or architecture (table or one diagram — draw it with archify)
6. Configuration / CLI reference in `<details>`
7. Contributing, license

## Hero block

```html
<div align="center">

# Model Name

**One line: what it is for, who should use it.**

<a href="https://huggingface.co/org/name"><img alt="Model" src="https://img.shields.io/badge/🤗%20Hub-org%2Fname-yellow"></a>
<a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-Apache--2.0-blue"></a>
<a href="https://arxiv.org/abs/XXXX.XXXXX"><img alt="Paper" src="https://img.shields.io/badge/arXiv-XXXX.XXXXX-b31b1b"></a>

</div>
```

Keep the blank lines inside the `<div>` — without them Markdown inside HTML does not render. Use one
shields.io style for every badge (default flat). ≤6 badges.

## Light / dark image pair

Hub (upload via the card editor, then append the fragment):
```markdown
![Logo](https://cdn-uploads.huggingface.co/.../logo-light.png#hf-light-mode-only)
![Logo](https://cdn-uploads.huggingface.co/.../logo-dark.png#hf-dark-mode-only)
```

Hub, already-hosted image:
```html
<img class="dark:hidden" src=".../light.png" alt="…">
<img class="hidden dark:block" src=".../dark.png" alt="…">
```

GitHub:
```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.png">
  <img alt="…" src="docs/logo-light.png" width="480">
</picture>
```

## Results table with source

```markdown
| Benchmark | Metric | Ours | Base | Source |
|---|---|---|---|---|
| GPQA Diamond | acc | **41.2** | 38.0 | [eval log](https://huggingface.co/spaces/…) · 2026-09-10 |
| MMLU-Pro | acc | 58.1 | 58.4 | [leaderboard](https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro) |
```

Bold only the best value in a like-for-like row. A row you cannot source is a row you delete.

## Collapsible details

```html
<details>
<summary><b>Full training configuration</b></summary>

```yaml
learning_rate: 2.0e-5
…
```

</details>
```

Blank lines around the fenced block are required or the Hub renders it as text.

## Spec table

```markdown
| | |
|---|---|
| Architecture | Qwen3, dense, GQA (32 Q / 8 KV) |
| Parameters | 8.2B (6.95B non-embedding) |
| Context | 32,768 native · 131,072 with YaRN |
| Precision | bf16 safetensors |
| Memory (inference, bf16) | ~16.4 GB — `hf-mem` |
```

## Math

Hub renders KaTeX: `$$ … $$` display, `\\( … \\)` inline. GitHub renders `$$ … $$` and `$ … $`.

## Verified-rendering HTML subset

`<div align>`, `<center>`, `<p>`, `<a>`, `<img width/alt/class>`, `<details>/<summary>`, `<b>/<i>`,
`<br>`, `<table>` family, `<picture>/<source>` (GitHub only — the Hub ignores `<source>`, use the
class/fragment method there). `<style>`, `<script>`, inline `style=` beyond simple margins: assume
stripped.
