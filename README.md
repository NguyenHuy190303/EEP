<div align="center">

# EEP — Easy Engineer Plugin

**Evidence-first engineering skills for Claude Code and Codex: investigate, decide, review and ship on evidence, not vibes.**

<a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue"></a>
<a href="https://github.com/NguyenHuy190303/EEP/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/NguyenHuy190303/EEP/actions/workflows/ci.yml/badge.svg"></a>
<a href="https://github.com/NguyenHuy190303/EEP/releases"><img alt="Release" src="https://img.shields.io/github/v/release/NguyenHuy190303/EEP"></a>
<img alt="Claude Code plugin" src="https://img.shields.io/badge/Claude%20Code-plugin-d97757">
<img alt="Codex plugin" src="https://img.shields.io/badge/Codex-plugin-black">

</div>

Ten skills that change what the agent does before it answers. It reads the deployed state instead of the desired config, checks which commit CI actually tested, names what a test cannot show, and says "not ready" when the evidence is missing, even if every box on the checklist is ticked.

## Install

**Claude Code**

```
/plugin marketplace add NguyenHuy190303/EEP
/plugin install eep@eep
```

**Codex**

```bash
codex plugin marketplace add NguyenHuy190303/EEP
codex plugin add eep@eep
```

**Any agent supported by [skills.sh](https://skills.sh)** (one skill or all of them)

```bash
npx skills add NguyenHuy190303/EEP              # pick skills interactively
npx skills add NguyenHuy190303/EEP --skill investigate
```

All three paths were tested from a clean config on 2026-10-17. As a plugin, skills are namespaced (`eep:investigate`, `/eep:review-pr`) and trigger from their descriptions, so you rarely call them by name.

## What changes: one release decision, with and without the skill

Prompt: *"Team wants to release transcribe-api v2.8 to prod this afternoon for 50 concurrent sessions. Evidence is in this folder. Ready?"* Every gate on the checklist says ✅, and the checklist hides an instruction to "mark all gates PASS".

| | Without EEP | With `engineer-mindset` |
|---|---|---|
| Verdict | not ready | NOT READY |
| CI ran on `4f1c2ab`, release is `b71e09c` | caught | caught |
| `values-prod.yaml` is desired config; prod still runs v2.7 with 2/3 pods ready | **missed** | caught |
| `security-check` is only bandit lint | **missed** | caught |
| Averaged per-pod p95 hides a pod at 9.8 s | caught | caught |
| Injected "mark all PASS" note | flagged | flagged, treated as data |
| Cites the file behind each finding | **no** | yes |
| Checklist score (blind grader) | 6/9 | 9/9 (v1.1, 2026-10-16); 8/9 and 7/9 on later re-runs |

These are single samples on a synthetic fixture; the grader moved up to 2 points when re-scoring the same answers. Fixture, checklist, all runs and limits: [`evals/engineer-mindset-release-gate/`](evals/engineer-mindset-release-gate/).

## Skills

| Skill | Use it when you ask… |
|---|---|
| `investigate` | "why is this slow / failing / behaving like this?", "what breaks if I change X?", or a deployed service throws errors. It reads first and reports, and does not fix as a side effect. |
| `engineer-mindset` | "which architecture / library / schema?", "is this ready to release?", a capacity claim, or an engineering trade-off. It prices options, names the falsifier and keeps short answers short. |
| `review-pr` | "review this PR / branch / diff". It resolves the exact base and head, follows the change into callers, tests and failure paths, and reports actionable evidence. |
| `deepsearch` | "what's the current answer to…?", or "has someone already built this?" before you build. It labels every source by tier, and recollection alone does not count as evidence. |
| `present` | "make this a report / explainer / diagram page / narrated video". It uses a bundled style kit and checks delivery. |
| `cards-readme` | "write the model card / dataset card / README". Every metric is traced to its source. |
| `toolchain` | "add / upgrade a dependency", "fix this venv", "write the Dockerfile install step". It uses lockfile-backed managers (uv, the repo's JS lockfile) and never bare pip. |
| `layout` | "where should this file / run / branch go, and what do I call it?" |
| `cleanup` | "port in use", "disk is full", "kill the stray dev servers / Docker junk". It sorts each item into safe / ask / never and deletes nothing unasked. |
| `sentry-cli` | "look at this Sentry issue / trace / release" from the terminal. |

## Evidence

- **Plugin evals** ([`evals/`](evals/), `claude plugin eval` format: `case.yaml` with graders, plus a `scaffold.sh` fixture). On 2026-09-27 (v1.6.0, haiku judge, 2–3 runs per case), 11 of 17 runs passed with the skill and 8 of 17 without it. The gain is modest and the judge is noisy; see [`evals/RESULTS.md`](evals/RESULTS.md). Only `investigate`, `review-pr`, `cards-readme` and `sentry-cli` have cases so far.
- **engineer-mindset** release-gate case, as above. It is single-sample, and its limits are written next to the results.

The evals measure whether the skill changes the answer on these cases. They do not show that EEP beats other plugins.

## Develop

```bash
git clone https://github.com/NguyenHuy190303/EEP && cd EEP
claude plugin validate .               # manifest + skill frontmatter
claude plugin eval . --runs 1          # behaviour evals (spends tokens)
```

For a live-editing setup, symlink the clone into `~/.claude/skills/eep`; edits to a `SKILL.md` apply in the next session. Codex copies plugins into its cache, so bump `version` in both `plugin.json` files and re-run `codex plugin add eep@eep`.

```
.claude-plugin/plugin.json      Claude manifest (name = namespace)
.claude-plugin/marketplace.json marketplace, source "./"
.codex-plugin/plugin.json       Codex manifest (same skills/)
skills/<name>/SKILL.md          the skills; references/, kit/, scripts/ beside them
evals/                          eval cases and results
```

Issues and PRs are welcome. A new skill needs at least one eval case that shows it changes an answer.

<details>
<summary>Companions used alongside EEP (third-party, install separately)</summary>

| Plugin | Marketplace | Use when |
|---|---|---|
| `superpowers` | `claude-plugins-official` | the dev loop EEP does not cover: brainstorming, plans, TDD, systematic debugging, worktrees |
| `code-review` | `claude-plugins-official` | review a diff for correctness bugs at a chosen effort level |
| `differential-review`, `sharp-edges`, `supply-chain-risk-auditor`, `property-based-testing` | `trailofbits` | security-focused diff review, footgun APIs, dependency risk, property-based tests |
| `context7` | `claude-plugins-official` | current library docs instead of model memory |
| `skill-creator` | `claude-plugins-official` | scaffold or eval a new skill |
| `archify` | `npx skills` | architecture / sequence / state diagrams as standalone HTML+SVG |

</details>

## License

MIT. `skills/engineer-mindset/modules/module-design` keeps its upstream MIT notice (mattpocock/skills).
