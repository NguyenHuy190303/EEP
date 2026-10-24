---
name: cards-readme
description: "Create or overhaul a Hugging Face model card, dataset card or GitHub README, with a first-screen quickstart and every claim traced to its source."
---

# Cards and READMEs

Collect the actual artifact facts before writing. Omit unsupported claims and empty template sections. Every metric needs its dataset, definition and source; preserve license and provenance uncertainty. Quickstart and useful capability information belong on the first screen.

## Select the artifact and optional detail

- Model card: existing `references/modelcard_spec.md` and `references/modelcard_template.md`.
- Dataset card: existing `references/datasetcard_spec.md`, `references/datasetcard_template.md` and [dataset quality](references/dataset-quality.md). Media/schema order belongs in the parquet, not just its card. Keep label provenance and reproduction evidence.
- GitHub README: relevant section of existing `references/patterns.md`; no Hub-only metadata workflow.
- For composition/first-screen choices: [card composition](references/card-composition.md).
- Only when a chart answers the reader's question: [charts](references/charts.md), with values from the source table and real rendering/palette checks.
- For benchmark claims: [benchmark evidence](references/benchmark-evidence.md), including what the result does not prove.

Use [workflow and gates](references/workflow-and-gates.md) for collection, validation and final delivery, running only the checks relevant to the artifact. Done when `check_card.py` passes, every metric names its dataset, definition and source, and the rendered page (plus the dataset viewer and schema, for a dataset) was inspected. An upload or other external write needs the user's authorization for that action. Anchor script paths at this skill's root.
