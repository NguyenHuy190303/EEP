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

3. **Qualify each candidate** — license (MIT / Apache-2.0 / BSD: use; GPL / AGPL / CC-NC / gated:
   stop and ask), last commit or update ≤ 12 months, stars or downloads as a *hint* only, runs on
   the stack in play (Python version, CUDA, framework), and whether the README's claim survived
   opening the code.
4. **Output a three-column verdict:**

   | Có sẵn — dùng luôn | Gần đúng — fork / adapt (what must change) | Phải tự làm |
   |---|---|---|

   Code is written only for the third column. The second column names the exact delta, so the
   fork stays small and the upstream stays mergeable.
5. **Gaps as usual**: which channels were swept, which candidate could not be verified, what was
   not searched and why.

Depth: the default is the full sweep with tiers — a wrong "nothing exists" costs days of building.
Trim to one channel only when Huy says the thing is throwaway.
