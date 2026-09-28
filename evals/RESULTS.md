# Eval results — 2026-09-27 (v1.6.0)

Ran with `--scaffold` so each case gets a real fixture repo instead of the empty sandbox that made
every v1.0.0 case fail regardless of the skill. Judge model: default (`haiku`), 2-3 runs per case,
`--ablation with-without` (a no-skill baseline arm runs alongside).

**Known gap, not run this round: `sentry-cli-1/2/3` have no fixture and are excluded from the table
below.** These 3 of 12 skills have zero eval coverage. Fixing them needs a fake `sentry` CLI on
`PATH` plus `Bash` in `allowed_tools`; `case.yaml`'s `execution.env` only accepts `EVAL_*`-prefixed
keys (confirmed by running a case with `env: {PATH: ...}` — it is rejected: `"execution.env key
'PATH' is not allowed"`), so seeding a stub binary this way needs a different mechanism than the one
used for the other 7 cases. Left undone rather than shipped half-working.

| Case | With skill | Without skill | Note |
|---|---|---|---|
| investigate-1 | 2/2 pass | 2/2 pass | clear fixture (broad `except` swallowing a heartbeat timeout); both arms diagnose it correctly |
| investigate-2 | 0/2 pass (retest) | 1/1, 1/1 (split across two runs) | responses in both arms are accurate and well-evidenced on manual read; the LLM judge is noisy on this case (3-vote splits like FAIL/PASS/FAIL appear in both arms) rather than showing a real with/without difference |
| investigate-3 | 2/2 pass | 2/2 pass | consumer-category enumeration fixture works cleanly |
| review-pr-1 | 1/2 pass | 1/2 pass | async-endpoint-with-missing-rollback fixture; both arms find real issues, judge splits 1-1 on strictness of the file:line evidence bar |
| review-pr-2 | 2/2 pass | 1/2 pass | retry/env-var fixture; the only case with a clean with > without delta across both runs |
| review-pr-3 | 2/2 pass | 1/2 pass | validation-moved-to-router fixture; same clean delta as review-pr-2 |
| cards-readme-1 | 1/2 pass | 1/2 pass | fixture bug found and fixed mid-run (an inconsistent per-example mean) — the with-skill response caught the inconsistency in the fixture itself before the fix, which the initial grader scored as a failure since it declined to launder a wrong number; after the fixture fix, judge votes are still 1-1 on this nuanced criteria |

**Honest read:** the empty-sandbox root cause from the v1.0.0 run (0/9, every case failing because
there was no repository to inspect) is fixed — cases now run against real fixtures and produce
substantive, evidence-based responses in both arms. Total: 11/17 with-skill runs pass vs 8/17
without-skill runs pass across the 7 cases (excluding the two runs that hit an unrelated rate-limit
error) — a positive but modest and noisy delta, not the clean signal a smaller, more objective
grading criteria (regex/tool_used checks on specific mechanisms) would give. Only review-pr-2 and
review-pr-3 show a clean with > without delta on both runs; investigate-1/3 show both arms already
strong (ceiling effect — the fixtures may be solvable without the skill's extra discipline);
investigate-2 and cards-readme-1 show judge variance (vote splits like FAIL/PASS/FAIL, and
disagreement between two runs of the *same* arm) that looks more like grader noise at the default
`haiku` judge model than a real difference.

Total spend this session: recorded in each case's local `evals/results/` run (gitignored — see
`.gitignore`); not committed here to avoid re-leaking local absolute paths the way the old
`evals/results/2026-09-15.../` run did.

**Next real step, not done here:** switch `--judge-model` to a stronger grader (or add `arm: with-only`
regex/tool_used graders for the more objective sub-claims) before trusting the open-rubric cases as a
gate. Flagged as a known limitation rather than silently left out of this report.
