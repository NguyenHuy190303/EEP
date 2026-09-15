---
name: design-decision
description: Use when choosing an architecture, a stack, a library, a schema, an API shape, or a module boundary — any decision where a different reasonable choice would change what gets built. Forces constraints before options, prices at least two real alternatives, and names the horizon and the falsifier.
---

# Design a system or pick a stack

The failure mode this exists to stop: a confident recommendation whose binding constraint was never
stated, whose alternatives were strawmen, and whose lifespan nobody agreed on.

## 1. Constraints before options

Write the constraints that actually bind before naming a single option. A constraint is something
that would eliminate a candidate. Typical binders: who maintains this after you, expected load with
a number, deadline, what the team already runs in production, data that cannot leave a boundary,
cost ceiling.

If a constraint that changes the answer is unknown, ask once — at most three questions, together,
with concrete options. Then proceed on the stated assumption rather than blocking.

"No constraint binds here" is a valid and useful finding. Say it, and pick the boring option.

## 2. At least two real options

A rejected option must be one an experienced engineer would genuinely consider. If the alternative
only exists so the recommendation looks reasoned, delete it and say there was only one option.

Order options cheapest-first: already-installed dependency → stdlib/native platform feature → new
small dependency → build it. Stop at the first that satisfies the constraints.

For each option state the **cost when it is wrong**, not only the benefit. A benefit list with no
failure cost is marketing, not design.

## 3. Decide, with the contract

State the choice with the decision contract (see user CLAUDE.md §8):

```
[horizon · basis] <the choice>; wrong if <observable condition>
```

For a one-way door, a `durable` horizon, or anything another person will have to live with, expand
to the full form: binding constraint · options priced · choice and why · falsifier · reversal cost ·
what is deliberately out of scope.

## 4. Persist it only if it will be re-litigated

In a repo with a decision ledger (this workspace: `./ops`), a `durable` choice ends with a ready-to-run
line, not a written file:

```
./ops decide "<title>" --basis fact|guess|taste --who huy,claude
```

`guess` requires `--revisit-when`. Do not run it unattended — hand it over.

`throwaway` and `tactical` choices do not go in the ledger. A ledger that records everything records
nothing.

## Do not

- Propose an abstraction with one implementation, a factory for one product, or config for a value
  that never changes.
- Design for load, tenancy, or extensibility that no stated constraint asks for. If you think the
  constraint is missing, say so in one sentence and design for what was actually stated.
- Add a dependency for what a few lines already in the codebase can do.
- Draw a diagram unless three or more components interact. Two boxes and an arrow is a sentence.
- Recommend a rewrite when the question was about a change.
