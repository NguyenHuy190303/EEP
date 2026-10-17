---
name: review-pr
description: "Review a PR, branch or diff for concrete correctness, regressions and repository invariants. Report actionable evidence; use team extensions only where relevant."
---

# Review PR

Review the actual behavior and connected code. Do not stack other generic review workflows for the same diff.

## Establish the review boundary

1. Read the applicable repository instructions and the nearest `AGENTS.md` or `CLAUDE.md`.
2. Inspect `git status`; preserve unrelated user work.
3. Resolve the exact base and head. If either is inferred, label the inference.
4. Read the configured checks before running commands. Run the narrowest relevant check first.
5. Read the diff, then expand to callers, tests, schemas, configuration, and failure paths only
   where the changed behavior crosses those boundaries.

## Ask the root question

When a PR adds a defensive mechanism—validation, retry, cache, secret storage, a new setting, or a
limit—ask what specific failure it prevents and whether that failure exists here. Extra machinery
without a matching failure mode adds maintenance cost and can create a new defect.

## Review for concrete failures

- **Logic:** unreachable branches, inverted conditions, wrong-type comparisons, missing cases, or
  behavior that contradicts a repository invariant.
- **Data growth:** nested scans, repeated parsing or I/O inside loops, and unbounded collections on
  paths whose input grows in production.
- **External data:** unchecked indexing, keys, casts, dates, shapes, dtypes, optional values, or
  assumptions about another service's response.
- **Failure handling:** swallowed exceptions, lost tracebacks, ambiguous logs, retries without a
  stop condition, and side effects that can break a critical path.
- **Concurrency and resources:** blocking I/O inside async code, per-request client creation,
  leaked sessions, missing rollback, or background work that outlives its dependencies.
- **Language traps:** mutable defaults, late-binding closures, shallow copies of nested state, and
  accidental eager materialization of large inputs.
- **Placement and reuse:** duplicated helpers, business logic in transport layers, new vocabulary
  for an existing domain concept, or a file that violates the repository's established layout.
- **Compatibility:** callers, tests, fixtures, migrations, serialized data, API consumers, flags,
  dashboards, and operational tooling that depend on the changed shape.

Do not repeat a formatter, linter, type-checker, or test failure as a manual finding unless the
consequence needs context. A passing check proves only the behavior it exercised.

## Evidence standard

Report a finding only when you can name:

- the affected file and tight line range;
- the input or state that reaches the failure;
- the observable consequence; and
- why existing checks do not already rule it out.

Order findings by severity; hacks and silent fallbacks are blockers by definition but still need
this evidence. Keep summaries after the findings and state what could not be verified. Do not edit,
comment, approve, or merge unless the user asked for that mutation.

## Project-specific extensions

The closest project-scoped `review-pr` skill may add repository invariants and domain boundaries.
Apply those extensions after this core; they must not be copied back into the global skill.

For hacks, silent fallbacks or comment policy, read [team quality](references/team-quality.md). Preserve deliberate, visible, distinguishable and bounded failure handling; do not weaken these checks when using the shorter entrypoint.

Only when responding to findings on a PR you wrote, read [responding to review](references/responding-to-review.md).

## Close

End with one sentence naming the reusable boundary the change exposed, or state that no new
boundary was found.
