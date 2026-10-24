---
name: review-pr
description: "Review a PR, branch or diff for correctness, regressions, repository invariants and whether it does what its ticket asked."
---

# Review PR

Review the actual behavior and connected code. This is the one review workflow for the diff.

## Establish the review boundary

1. Read the applicable repository instructions and the nearest `AGENTS.md` or `CLAUDE.md`.
2. Inspect `git status`; preserve unrelated user work.
3. Resolve the exact base and head. If either is inferred, label the inference. Confirm the base
   resolves (`git rev-parse <base>`) and `git diff <base>...<head>` is non-empty before reading
   further or starting a subagent.
4. Read the configured checks before running commands. Run the narrowest relevant check first.
5. Read the diff, then expand to callers, tests, schemas, configuration, and failure paths only
   where the changed behavior crosses those boundaries.

## Two axes: Standards and Spec

The review answers two questions and reports them separately:

- **Standards:** does the change hold up against the concrete failures and repository invariants
  below? This is the core of this skill.
- **Spec:** does the change do what its originating ticket asked?

Code can pass one and fail the other: every standard followed while building the wrong thing, or
exactly the ticket built while breaking an invariant. One merged list lets either axis hide the other.

Find the spec in this order: a ticket key or issue reference in the branch name or commit messages
(`PROJ-123`, `#45`, `Closes #45`), fetched with the tracker the session has (Jira MCP,
`gh issue view`); a path or link the user passed; a spec under `docs/` or `specs/` matching the
branch or feature. With none found, run Standards anyway and report "Spec: no spec found", with one
line offering to run that axis once the user names the ticket.

Run the Spec axis in its own subagent when the harness has one, otherwise as a separate pass under
its own heading. Give it the diff command, the commit list and the spec text, with this brief:
"Report (a) requirements missing or partial, (b) behaviour the spec did not ask for, (c) requirements
that look implemented but are implemented wrong. Quote the spec line and the diff hunk for each.
Under 400 words."

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

Leave formatter, linter, type-checker and test failures to their tools; raise one as a finding only
when its consequence needs context. A passing check proves only the behavior it exercised.

## Evidence standard

Report a finding only when you can name:

- the affected file and tight line range;
- the input or state that reaches the failure;
- the observable consequence; and
- why existing checks do not already rule it out.

A Spec finding instead quotes the spec line and the diff hunk it concerns.

Report under `## Standards` and `## Spec`, each ordered by severity within itself; ranking across the
axes is the merge the split exists to prevent. The summary gives the finding count and the worst
issue per axis. Hacks and silent fallbacks are blockers by definition but still need this evidence.
Put summaries after the findings and state what could not be verified. Edit, comment, approve or
merge only when the user asked for that mutation.

## Project-specific extensions

The closest project-scoped `review-pr` skill may add repository invariants and domain boundaries.
Apply those extensions after this core; they stay in the project skill.

For hacks, silent fallbacks or comment policy, read [team quality](references/team-quality.md). Its checks apply in full: failure handling stays deliberate, visible, distinguishable and bounded.

Only when responding to findings on a PR you wrote, read [responding to review](references/responding-to-review.md).

## Close

End with one sentence naming the reusable boundary the change exposed, or state that no new
boundary was found.
