---
name: deepsearch
description: Use for research questions that need sourced answers (library and API behaviour, version differences, pricing, benchmarks, comparing tools, current best practice) and as before-cook BEFORE building, training, writing a pipeline or solving a problem from scratch — sweeps GitHub, Hugging Face Hub, PyPI, Papers with Code and Kaggle for an existing repo, model, dataset, notebook or issue so nothing gets reinvented. Enforces source tiering, records what could not be found, and never lets model memory count as evidence.
---

# Deep search

The failure mode this exists to stop: a fluent, well-organised answer assembled from recollection,
with citations attached afterwards to whatever agrees with it.

## 1. Split the question into checkable claims

Before searching, list the individual claims the answer depends on. Each one is verified separately
and can land on a different tier. A question that cannot be split into claims is a question about
taste — say so and give an opinion labelled as one.

## 2. Sweep more than one way

Different channels answer things the others cannot. Run the ones that apply:

| Channel | Answers |
|---|---|
| Official docs / spec | intended behaviour, current API surface |
| The actual source or artifact — repo, `--help`, `pip show`, installed file | what it really does at the version in play |
| Issue tracker, changelog, release notes | known breakage, when behaviour changed, maintainer intent |
| High-engagement community writing | practice, gotchas, what people hit in production |
| Local measurement | anything about *this* machine, repo, or cluster |

For a library question, prefer the context7 MCP server over general web search — it returns
version-current docs.

## 3. Tier every claim, visibly

- **T1** — official docs or the source itself, read directly.
- **T2** — maintainer issue, changelog, or a repo's real code.
- **T3** — community writing with real engagement; useful, not authoritative.
- **T0** — model memory. **Never evidence.** If a claim is only T0, it is an open question, not an
  answer. This applies hardest to API signatures, CLI flags, version numbers, benchmark figures and
  pricing.

Record the date of a source whenever the answer is version-dependent.

## 4. Say what you could not find

Every deepsearch ends with the claims that stayed unsourced, and where you looked. An answer with no
gaps section is either trivial or dishonest about its coverage.

## 5. Handle disagreement out loud

When sources conflict, present both, then say which wins and on what grounds (recency, tier,
reproducibility). Silently picking one is how a wrong answer gets laundered into a confident one.

## Output

Conclusion first, in the fewest sentences that carry it. Then the claim table (claim → tier →
source → date). Then gaps. Links are markdown links, not bare URLs.

Scale depth to stakes: a flag lookup is one T1 read and two lines of output. A stack comparison that
will be lived with for a year earns the full treatment.

## Mode: before-cook — has someone already done this?

Runs **before** writing code for anything that is not a one-liner: a model, a pipeline, a data
converter, an eval harness, a benchmark, a UI component. The question is not "is my claim true" but
"does the thing already exist". Same tiering discipline: a repo is T1 only after its code was read.

1. **Name the problem as a query**, plus 2–3 synonyms the field uses (`speaker diarization` /
   `who-spoke-when`; `Vietnamese ASR` / `vi speech-to-text`). Queries never contain patient data,
   internal hostnames, or anything from a clinical dataset.
2. **Sweep the channels that hold artifacts**, not just prose:

   | Channel | How | Finds |
   |---|---|---|
   | GitHub repos + issues | `gh search repos`, `gh search issues` | implementations, known blockers |
   | Hugging Face Hub | `hf` CLI / API (skill `hf-cli`), model + dataset + Space search | weights, data, demos |
   | PyPI / npm | `pip index versions`, `npm view` | a package that already does it |
   | Papers with Code / arXiv | web | the method, and its reference code |
   | Kaggle / notebooks | web | working end-to-end examples on similar data |

3. **Fit before quality.** Write the need as 3–6 concrete requirements *before* opening a
   candidate (inputs, outputs, scale, language, runtime, the hard constraint). A candidate missing
   one hard requirement is **reference only**, however famous — auditing quality first is how a
   100k-star repo gets adopted for a problem it does not solve.
4. **Audit what survives fit.** Stars are a popularity number taken once, usually after one HN
   post; never rank by them. Run `bash scripts/probe.sh <owner>/<repo>` and read it against
   `references/prior-art-audit.md`, which carries the seven signals that actually separate a
   maintained project from a weekend demo or an enterprise funnel — bus factor, whether recent
   issues get answered, real tests and CI, release discipline, commit texture, the code inside two
   core files, and what the README avoids saying. Licence check includes the open-core trap: BSL /
   SSPL / Elastic / "free under $X" are not open, and the feature you need sitting under
   *Enterprise* means the OSS edition is a demo of it. MIT / Apache-2.0 / BSD: use. GPL / AGPL /
   CC-NC / gated: stop and ask.
5. **Output a four-column verdict:**

   | Dùng luôn | Fork / adapt (the one delta) | Tham khảo thôi | Tự làm |
   |---|---|---|---|

   Code is written only for the last column. "Tham khảo thôi" is what keeps a famous but unfit or
   undependable repo from becoming a dependency — read it, cite it, do not import it. Choosing
   **tự làm** is a valid result, not a failed search: say so when the dependency would be a thin
   wrapper you could write in ~200 lines you understand, when the integration surface is bigger
   than the problem, when fitting it means forking it, or when it drags in a framework for one
   function. The comparison is `write + maintain mine` vs `integrate + track upstream + debug
   through someone else's layer + the day it is abandoned`.
6. **Gaps as usual**: which channels were swept, which candidate could not be verified, what was
   not searched and why.

Depth: the default is the full sweep with tiers and the audit — a wrong "nothing exists" costs days
of building, and a wrong "this one is fine" costs longer, because it is discovered after the
integration. Trim to one channel only when Huy says the thing is throwaway.
