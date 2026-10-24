# Results: durable default vs urgency (2026-10-24)

One sample per arm, fresh general-purpose subagent, scored by the main session against the
checklists in `README.md` (not blind; half points for partial). Baseline = `git archive HEAD` at
782d315 (1.11.0).

| Arm | Skill state | Score | Notes |
|---|---|---|---|
| N, baseline | 1.11.0 | 3.5/6 | Cache keyed by `run_id` only (revision flagged as a caveat), no size bound or hit-rate, full `load_dataset`, labelled its own non-urgent answer `tactical`, options table instead of next steps |
| N, new | 1.12.0 | 5.5/6 | Key `(run_id, metric, content_hash, code_version)`, rebuildable store, streaming read, ETag from sha, two next steps with effort; no size bound stated for the store |
| U, new | 1.12.0 draft | 3.5/4 | Quick in-process cache + memo, durable follow-up named; `tactical` only in the decision line, no removal condition |
| U2, new | 1.12.0 | 4/4 | After the urgent bullet asked for `tactical: <why>; remove when <condition>`: label present with removal condition, no multi-layer build |

Limits: single sample, non-blind grader, Claude Code only, no repository fixture.
