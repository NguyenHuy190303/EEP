# Writing for agents

Adapted from mattpocock/skills `writing-for-agents` and `SKILL-MECHANICS` (MIT, see `LICENSE`).

Applies to any text an agent consumes: a `SKILL.md`, its description, a module or reference, a
`CLAUDE.md`/`AGENTS.md` line, a subagent brief. The goal is that the agent takes the same *process*
on every run, not that it produces the same words.

## Pointers decide when material is reached

A **pointer** is a line held in context that names out-of-context material and the condition for
reaching it: a skill description, a table row naming a module, a `CLAUDE.md` line naming a doc. Its
*wording*, not its target, decides whether the agent reaches the material. A must-read target behind
a weak pointer is a variance bug; sharpen the pointer first, and inline the material only if
sharpening fails.

An always-loaded pointer is paid on every turn, so prune it hardest:

- **Front-load the trigger word**, the one the user actually types.
- **One trigger per branch.** A branch is a distinct case the material handles. Synonyms of one
  branch are that branch written twice; keep one.
- **Cut identity the body already carries.**

**Invocation.** A model-invoked skill keeps a model-facing description (permanent context cost,
autonomous reach). A skill that only ever fires by hand can set `disable-model-invocation: true`
(Claude Code; `policy.allow_implicit_invocation: false` in Codex `agents/openai.yaml`): zero context
cost, but the human must remember it exists. When one skill needs another, write "call the Skill tool
with `<plugin>:<name>`", one call per skill; a bare `/name` mention is read less reliably.

## Place each piece on the ladder

1. **In-file steps:** what the agent does, in order.
2. **In-file reference:** rules and facts consulted on demand; a flat list of peer rules is fine.
3. **Disclosed reference:** a separate file behind a pointer, loaded only when the pointer fires.

Inline what every branch needs; disclose what only some branches reach. Keep a concept's definition,
rules and caveats under one heading. A file that is too long thins attention even when every line is
live; the cure is disclosure and splitting by branch, not trimming words.

## Every step ends on a completion criterion

- **Clarity:** the agent can tell done from not done. "Understanding reached" invites premature
  completion; "one command, already run, that goes red on this bug" does not. Sharpen the bound
  before hiding later steps; hiding only works across a real context boundary (a subagent or a
  handoff).
- **Demand:** "every caller accounted for" drives more legwork than "list the callers". The
  strongest criteria are both checkable and exhaustive.

## Leading words

A **leading word** is a compact concept the model already knows that stands in for a passage:
*tight* for "fast, deterministic, low-overhead"; *red* for "a loop you believe catches the bug";
*tracer bullet* for a thin end-to-end slice. Repeat the word, not its definition. Prefer an existing
word to a coined one: a coined word recruits no priors and costs its definition every time. Look for
triads spelled out at several sites and sentences that gesture at one idea; each can collapse into
one word.

## Steer positively

A prohibition puts the forbidden behaviour into context and makes it more available. State the target
behaviour instead ("write one-line comments", not "don't write long comments"). Keep a prohibition
only as a hard guardrail with no positive phrasing, and pair it with the positive target.

## Prune

- **Single source of truth.** Each meaning lives in one place, so a behaviour change is a one-place
  edit. Duplication costs tokens and inflates that meaning's weight.
- **Leave the environment's facts to the environment.** `--help`, config files, `package.json`
  scripts and the directory layout are already sources of truth; a document that restates them is a
  cache that goes stale. Write what the agent cannot find by looking: the unwritten convention, the
  reason behind a choice, the gotcha no config confesses.
- **Hunt no-ops sentence by sentence.** A sentence the model already obeys by default pays load to
  say nothing. Delete the whole sentence rather than trimming words. The test is model-relative:
  settle disagreement by running the document (an eval case), not by debate. A leading word too weak
  to beat the default (*be thorough*) is a no-op too; replace it with a stronger one (*relentless*).
- **Prune for relevance.** Lines go stale as behaviour changes. Without pruning, documents collect
  sediment because adding feels safe and removing feels risky.

## Done when

Each changed pointer names its branches with one trigger each; each step has a checkable criterion;
no sentence restates the environment or a default; prohibitions that remain have a positive target
beside them; and the eval cases for the touched skill were re-run or listed as UNCHECKED.
