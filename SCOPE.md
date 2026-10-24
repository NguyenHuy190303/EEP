# Scope

EEP is a small, curated set of engineering skills. Issues track changes to those skills; each one is
judged against the bar below.

## The bar

An issue or PR stays open when it clears both parts:

1. **Observed failure.** It describes something that went wrong in a real session: what you ran, what
   the skill did, what you expected. "It would be better if…" is a hypothesis; bring the session
   where it went wrong.
2. **Fits EEP.** It matches nothing in [`.out-of-scope/`](.out-of-scope/), and it is not a config
   option, a harness-specific branch or a tweak for one person's workflow. Those belong in your own
   `CLAUDE.md` / `AGENTS.md`, or in a fork.

Size is irrelevant: a one-word fix and a rewrite face the same bar. A new skill also needs at least
one eval case in [`evals/`](evals/) that shows it changes an answer.

## Already decided

Each file in [`.out-of-scope/`](.out-of-scope/) records one rejected concept, the reason, every
request for it so far, and what to do instead. Read them before filing:

- [`pipeline-skills.md`](.out-of-scope/pipeline-skills.md)
- [`tracker-bound-skills.md`](.out-of-scope/tracker-bound-skills.md)
- [`bundled-skill-sets.md`](.out-of-scope/bundled-skill-sets.md)
- [`tdd-skill.md`](.out-of-scope/tdd-skill.md)
- [`router-skill.md`](.out-of-scope/router-skill.md)

A request matching one of them is closed with a link to the file and added to its prior requests.
