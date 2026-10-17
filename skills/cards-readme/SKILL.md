---
name: cards-readme
description: "Create or overhaul HF model/dataset cards and GitHub READMEs with a first-screen quickstart and traceable claims. Load only the matching artifact specs and optional evidence guidance."
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

Use [workflow and gates](references/workflow-and-gates.md) for collection, validation and final delivery. Preserve check_card.py success, source-backed metrics, rendered inspection and the dataset viewer/schema checks when applicable. Use only checks relevant to the artifact. Skill invocation does not authorize an upload or external write; those need authorization covering the action. Keep script paths anchored at this skill's root.
