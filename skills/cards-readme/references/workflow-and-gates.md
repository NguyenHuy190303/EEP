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
   When data needs a visual comparison or explanation, follow **Evidence-led charts** below.
5. **Check**, then look:
   ```bash
   python3 $SKILL_DIR/scripts/check_card.py README.md --type model   # or dataset | readme; $SKILL_DIR = this skill's base directory
   python3 $SKILL_DIR/scripts/check_card.py README.md --type dataset --data out/   # parquet file, dir, or repo id
   ```
   It validates the frontmatter against the Hub's own validator (needs internet), fails on leftover
   template placeholders, and fails on a results table with no source column or link. Then render it:
   Hub cards → push to a **private** repo with `hf upload` and open the page; GitHub README → open the
   file on a branch or in the desktop app's markdown preview. Check dark mode on the Hub; images that
   only work on white get a `#hf-light-mode-only` / `#hf-dark-mode-only` pair (see patterns).

## Delivery gate — all of them

1. `check_card.py` exits 0.
2. No section says "More Information Needed", "TBD", "coming soon". A missing fact is a deleted section.
3. Every metric has: dataset id, metric name, value, and a source (eval log, Space, paper, or the exact
   command). Results from a leaderboard name the leaderboard. Results you ran name the command and date.
4. You looked at the rendered page, both themes on the Hub.
5. Dataset: `--data` passes on the parquet before the push, and after the push the viewer order
   (`https://datasets-server.huggingface.co/info?dataset=<repo>`, with token for private repos)
   matches. The card has a provenance section that passes the check.
6. If charts are included, their values agree with the source table, and the exported images were
   inspected at the card's reading width in light and dark contexts. State any rendering or palette
   check that could not run; do not describe an unperformed check as passed.

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
