# Auditing a candidate — separating real from slop

Used by the `before-cook` mode of `deepsearch`, on candidates that already passed fit. The thing
this catches is the one that wastes a week: a repo that looks alive, has stars, and is someone's
weekend project, a demo, or an enterprise funnel.

Before any of this: if the need is in the **solved-category table in SKILL.md** (metrics, LLM
tracing, error tracking, queues, deploys, auth, …), the question is which standard option, not
whether to build one — and only the specific exporter/chart/client gets audited here.

Stars are a popularity measure taken **once**, usually after one HN or X post. They say nothing
about whether the code is maintained, whether it fits, or whether the open part is the real part.
Never rank candidates by stars.

## Order matters: fit first, quality second

Auditing quality before checking fit is how a 100k-star repo gets adopted for a problem it does not
solve. So:

1. **Write the need as 3–6 concrete requirements** before opening any candidate — inputs, outputs,
   scale, language, runtime, the hard constraint (Vietnamese, medical data stays internal, runs on
   H100, no external API).
2. **Score fit against those requirements first.** A candidate that misses one hard requirement is
   *reference only* — read it for ideas, never depend on it — regardless of how good it is.
3. Only what survives fit gets the quality audit below.

## Probe — facts before opinions

```bash
bash probe.sh <owner>/<repo>     # scripts/probe.sh in this skill dir
```

Prints, in one shot: archived/fork, license, created, last push, latest release, stars, forks,
size, the commit distribution across the top 20 contributors, the CI workflows, the number of test
files, and the last 5 issues with their comment counts. Everything below is read off that output
plus a few minutes in the code.

## The signals that actually separate them

| Signal | Alive | Slop / trap |
|---|---|---|
| **Bus factor** — commits across contributors | several people in double digits | `175,31,7,4,3,…` — one author, everyone else fixed a typo. It dies when they lose interest |
| **Issue behaviour**, not issue count | recent issues have maintainer replies; closed by a fix | last 5 issues `comments=0`, or closed by a stale-bot. Nobody is home |
| **Tests and CI** | a `tests/` tree with real cases, CI that runs them | zero test files; CI that only builds a badge or renders a star-history chart |
| **Release discipline** | tags, changelog, semver | `release=NONE` and a README promising v1 "soon"; or a version bumped only to publish |
| **Age** | *not a signal.* Ask instead: does it run on the stack in play, and would you ever need upstream to change? | treating "last commit 2019" as disqualifying — a unique CUDA kernel, a format parser, a reference implementation can be finished software. If you can read and patch it, vendor it |
| **Commit texture** | `fix(scope): concrete thing` referencing issues | a wall of `update`, `wip`, `final`, generated docs commits, or a majority of commits touching README/badges/sponsors rather than code |
| **Code on the inside** — open 2 core files | errors handled, boundaries validated, functions you can follow | one 2000-line file, no error handling, tutorial copy-paste, LLM-generated comments that restate the line below, dead abstractions |
| **What the README does not say** | limits, failure modes, benchmarks with a method | all emoji, badges and claims; no known limitations section; benchmark numbers with no command to reproduce |

## The open-core trap

A repo can be genuinely well engineered and still be the wrong dependency, because the open part is
the funnel and the useful part is sold.

- Check the pricing or feature-matrix page: if the features you need appear under *Enterprise* /
  *Cloud* / *Pro*, the OSS edition is a demo of them, not a smaller version of them.
- Check the licence for a **non-open** licence wearing open clothes: BSL, SSPL, Elastic, "fair
  source", "free for companies under $X". These change what you may do, and they can change again
  on the next release — a relicense is the risk you inherit.
- Check whether SSO, RBAC, audit log, multi-tenancy, or scaling limits are the gated features. Those
  are the classic gates, and they are exactly what a real deployment eventually needs.
- Self-hosting allowed ≠ self-hosting supported: look for whether self-host issues get answered.

## Verdict — four columns, not three

| Dùng luôn | Fork / adapt | Tham khảo thôi | Tự làm |
|---|---|---|---|
| fits every requirement, survives the audit, licence clean | fits, audit ok, one named delta to change — and the fork stays small | good ideas, wrong fit or cannot be depended on (open-core gated, wrong scale, or unmaintained **and** you would need upstream to change) — read it, cite it, do not import it | nothing survives, or the dependency costs more than the code |

**"Tham khảo thôi" is the column that keeps a famous repo from becoming a dependency.** It is the
honest answer for most 100k-star results: they teach you the shape of the solution, they are not
your solution.

## When building it yourself is the right answer

Say so explicitly — it is a valid outcome of the sweep, not a failure to find something:

- The dependency would be a thin wrapper over something you could write in **under ~50 lines**
  you fully understand. Glue only — never a whole solved category (SKILL.md has the table).
- The integration surface (config, adapters, conversions, version pinning) is bigger than the
  problem.
- You would have to fork it to fit, and the fork would drift from upstream immediately.
- It pulls a heavy tree (a framework, a second ORM, a whole runtime) for one function.
- Its failure modes would be yours to debug anyway, but in someone else's code you cannot read.

The cost being compared is **not** "write it" vs "install it". It is `write + maintain what I wrote`
vs `integrate + track upstream + debug through a layer I did not write + the day it is abandoned`.

## Hugging Face specifics

Models and datasets have their own tells — `downloads` last month (not the total), `lastModified`,
`gated`, and how complete the card is. A model card with no eval numbers, no training data
description, and no licence is the same as a repo with no tests. Weights whose claimed numbers come
with no eval command are unverified claims, not results. Prefer an artifact from an org over a
personal account when both exist, and check whether the dataset it was trained on is one you may
legally and contractually use.
