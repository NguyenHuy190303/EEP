# Results: metric registry (2026-10-24)

One sample per arm, fresh general-purpose subagent, scored by the main session against the
8-point checklist in `README.md` (not blind; half points for partial). Baseline = `git archive HEAD`
at 782d315 (1.11.0).

| Arm | Skill state | Score | Misses |
|---|---|---|---|
| A | 1.11.0 (HEAD) | 4.5/8 | 1 partial (registry without label/unit/direction), 2 (no aggregation rule), 3 (rejected long form), 4 partial (pinned revision, still full download), 5 partial (columns from keys, no unit formatting) |
| B | + `object-design.md`, `frontend.md`, registry and data-driven views | 6.5/8 | 3 (per-run JSON dict, wide-schema risk not named), 4 partial (pinned revision, still `load_dataset` download); did not reach `stacks.md` |
| B2 | + pointer from the registry section to the `stacks.md` data rules | 8/8 | none |

B → B2 was a routing fix: the long-form and read-in-place rules existed in `stacks.md`, but nothing
on the path the model took pointed there. Limits: single sample, non-blind grader, Claude Code only.
