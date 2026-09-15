---
name: cards-readme
description: Write or overhaul a Hugging Face model card, a Hugging Face dataset card, or a GitHub README so it reads like a top-tier lab release — hero block, badges, quickstart on the first screen, sourced results table — while every number stays traceable. Use when Huy says "model card", "dataset card", "viết README", "README đẹp", "card cho model/dataset", asks to document a checkpoint or dataset before pushing to the Hub, or asks to make an existing README/card prettier. Owns the Hub metadata specs, the card templates, the beauty patterns that render on both Hub and GitHub, and the check that fails on placeholders and unsourced metrics. Uploading goes through hf-cli.
---

# cards-readme

Three outputs, one method: **HF model card**, **HF dataset card**, **GitHub README**. "Beautiful" means
a reader decides in ten seconds whether this is for them and can run it in thirty — not decoration.
Huy's rule §4 applies with no exceptions: a number without a source does not go in the card.

## Workflow

1. **Collect evidence before writing a word.** Read what exists: `config.json` / `generation_config.json`,
   `training_args.bin` or the training script, eval JSONs, `git log`, the current README, the dataset's
   `dataset_info` (run `hf` per the hf-cli skill or `datasets-server` per huggingface-datasets). List what
   you could NOT find. Those sections get omitted, never filled with prose.
2. **Pick the type**, then read only the matching spec + template from `references/`:
   - model card → `modelcard_spec.md` (metadata fields) + `modelcard_template.md` (section skeleton)
   - dataset card → `datasetcard_spec.md` + `datasetcard_template.md`
   - GitHub README → no spec; use the section order in `references/patterns.md`
3. **Metadata YAML first.** Hub UI, filters, widget and license badge all come from it. Minimum that
   makes a card discoverable — model: `license`, `library_name`, `pipeline_tag`, `base_model`, `datasets`,
   `language`, `tags`; dataset: `license`, `pretty_name`, `task_categories`, `language`, `size_categories`,
   `configs` (data files — the viewer needs it). `library_name: transformers` is required explicitly for
   repos created after Aug 2024; the Hub no longer infers it from `config.json`.
4. **Body.** Section order and the HTML that actually renders: `references/patterns.md`. Write the hero
   block, highlights and quickstart first — that is the first screen and the only part most readers see.
5. **Check**, then look:
   ```bash
   python3 ~/Projects/EEP/skills/cards-readme/scripts/check_card.py README.md --type model   # or dataset | readme
   ```
   It validates the frontmatter against the Hub's own validator (needs internet), fails on leftover
   template placeholders, and fails on a results table with no source column or link. Then render it:
   Hub cards → push to a **private** repo with `hf upload` and open the page; GitHub README → open the
   file on a branch or in the desktop app's markdown preview. Check dark mode on the Hub; images that
   only work on white get a `#hf-light-mode-only` / `#hf-dark-mode-only` pair (see patterns).

## Delivery gate — all four

1. `check_card.py` exits 0.
2. No section says "More Information Needed", "TBD", "coming soon". A missing fact is a deleted section.
3. Every metric has: dataset id, metric name, value, and a source (eval log, Space, paper, or the exact
   command). Results from a leaderboard name the leaderboard. Results you ran name the command and date.
4. You looked at the rendered page, both themes on the Hub.

## What makes it read as top-tier

- **Hero block**: centered name, one-line tagline that says what it is *for*, one row of ≤6 badges
  (license, base model, paper, demo, downloads), optional one hero image ≤1 MB.
- **Highlights**: 3–5 bullets, each a concrete claim with a number or a named capability. No adjectives
  without a noun to hold them.
- **Quickstart** within the first screen: one code block that runs as-is, pinned to the library version
  that actually works (`transformers>=4.51` style), with the known-failure error text if there is one.
- **Spec table** instead of prose for size, context length, tokenizer, dtype, hardware footprint
  (use hf-mem for the memory row).
- **Results table** with a source column. Bold the best per row only when the comparison is like-for-like.
- **Collapsible `<details>`** for long training config, full eval breakdowns, prompt templates.
- **Limitations and intended use** stay short and specific — "trained on Vietnamese legal text; not
  evaluated on medical" beats a generic ethics paragraph.
- Dataset cards additionally lead with a **row example** and a **field table** (name, type, description),
  then splits/sizes, then how it was built (source → filter → dedup, with counts at each stage).

## Do not

- Invent, round, or "estimate" benchmark numbers. No number > no source.
- Ship template sections unfilled. The Hub template is a checklist, not a layout.
- Stack more than 6 badges, more than one hero image, or emojis as bullets.
- Use HTML the Hub strips — verified-rendering tags are listed in `patterns.md`; anything else gets a
  test push first.
- Put eval scores only in prose. Structured results go to `model-index` (legacy, still rendered) or
  `.eval_results/*.yaml` (new, see `references/eval_results.md`); the table in the body links to them.
- Upload from this skill. Creating repos, pushing, opening PRs on the Hub is hf-cli's job.

## References

- `references/modelcard_spec.md`, `references/datasetcard_spec.md` — full metadata field list, from
  `huggingface/hub-docs` (fetched 2026-09-15).
- `references/modelcard_template.md`, `references/datasetcard_template.md` — official section
  skeletons from `huggingface_hub`.
- `references/patterns.md` — hero/badge/light-dark/details/table snippets that render on Hub and
  GitHub, and section order per type.
- `references/eval_results.md` — `.eval_results/*.yaml` format (Hub, marked work-in-progress).
- Exemplars worth opening for tone, not for copying: `Qwen/Qwen3-8B`, `HuggingFaceFW/fineweb`.
