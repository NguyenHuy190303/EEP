## Blockers however green the tests are: hacks and silent fallbacks

Block the PR on either. Not a suggestion, not a nit. (Rule set adapted from an internal team
code-review skill.)

**A hack is code that works without the author knowing why.**

- A symptom patched where it surfaced instead of where it originates.
- A `sleep`, a retry or a reordering that makes a race go away without naming the race.
- A value special-cased so one input, one test or one customer passes.
- Monkeypatching, reaching into another module's internals, re-declaring a constant that already
  exists elsewhere.
- A workaround for a bug in a dependency with no link to the upstream issue and no condition for
  removing it.
- Anything whose comment is a version of "for some reason this is needed".
- In an LLM agent: a prompt rule, a middleware or `return_direct` added to correct what the model
  did. Ask for one row per patch — symptom → patch → real cause. Several patches with one cause
  mean the design is wrong, not the model (the agent-design row of `eep:engineer-mindset` has the method).

Ask the author to state the mechanism: why does this fix it? If they can't, the diff is a guess.

**A silent fallback hides a failure from the only people who could fix it.**

- `except: pass`, or a catch that logs at debug and continues.
- A default substituted when a dependency fails: empty list, zero, `None`, a stub, a cached value
  of unknown age.
- `or <default>` where the left side failing and the left side being empty mean different things.
- Falling through to a second provider, model or endpoint without saying so in the response or the
  logs.
- A retry loop that exhausts and returns success-shaped output.
- Validation that drops bad records instead of rejecting them.

A fallback is allowed only when it is all four of: **deliberate** (the PR says the failure is
expected and why degrading beats failing), **visible** (logged at warn or error with enough context
to find the cause), **distinguishable** (a flag, a status or a different type, so the caller can
tell a real answer from a degraded one), and **bounded** (a timeout, an attempt count, a staleness
limit). Missing any one, it is a silent fallback.

Raise it by naming the hidden mechanism and what production will show when it fires: which caller
gets what, which log stays quiet, which metric still looks green.

## Comments: carry only what the code can't

Ask to delete: a restatement of the line below, section banners inside a function, commented-out
code, changelog/author/date lines, a `TODO` with no owner and no issue, a comment that explains a
name (rename instead).

A comment earns its place, in one or two lines, when the information cannot live in the code: why
this and not the obvious alternative (what was tried and what it did), a constraint from outside
the file (ordering, protocol quirk, units, vendor limit), a link with the condition for removing a
workaround, or a trap the next person is about to fall into. Longer rationale belongs in the commit
message or PR description.

The missing comment is the more expensive finding. When the diff makes a choice you had to
reconstruct — an ordering, a magic number, a deliberate omission — ask for one line of why.
