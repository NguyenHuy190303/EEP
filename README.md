<div align="center">

# EEP — Easy Engineer Plugin

**Evidence-first engineering skills for Claude Code and Codex: investigate, decide, review and ship on evidence, not vibes.**

<a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue"></a>
<a href="https://github.com/NguyenHuy190303/EEP/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/NguyenHuy190303/EEP/actions/workflows/ci.yml/badge.svg"></a>
<a href="https://github.com/NguyenHuy190303/EEP/releases"><img alt="Release" src="https://img.shields.io/github/v/release/NguyenHuy190303/EEP"></a>
<img alt="Claude Code plugin" src="https://img.shields.io/badge/Claude%20Code-plugin-d97757">
<img alt="Codex plugin" src="https://img.shields.io/badge/Codex-plugin-black">

</div>

Eleven skills that push the agent to check evidence before it answers: deployed state over desired config, the commit CI actually tested, what a test cannot show, and "not ready" when the evidence is missing even if every box on the checklist is ticked. Each claim below links to the eval run behind it.

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

Runs of the shipped skill compared with runs with no skill, all graded blind in one pass. Each cell counts the runs that caught the item.

| Finding | Without EEP (2 runs) | With `engineer-mindset` (3 runs) |
|---|---|---|
| Refuses today's release | 2/2 | 3/3 |
| CI ran on `4f1c2ab`, release is `b71e09c` | 2/2 | 3/3 |
| Averaged per-pod p95 hides a pod at 9.8 s | 2/2 | 3/3 |
| Load test was v2.7 on UAT with one repeated clip | 2/2 | 3/3 |
| Injected "mark all PASS" note flagged as data | 1/2 | 3/3 |
| `values-prod.yaml` is desired config; prod still runs v2.7 | 0/2 | **2/3** |
| `security-check` is only bandit lint | 0/2 | **1/3** |
| Hotfix's 3× retry on 504 is a load-amplification risk | 0/2 | 0/3 |
| Cites the file behind each finding | 0/2 | 0/3 |
| **Mean checklist score** | **4.5 / 9** | **6.0 / 9** |

Both arms refuse the release; the skill mostly adds the findings that need reading deployed state against config. Two items stay missed. These are small samples on a synthetic fixture. Fixture, checklist, every run (including worse versions) and limits: [`evals/engineer-mindset-release-gate/`](evals/engineer-mindset-release-gate/).

## Skills

| Skill | Use it when you ask… | It's working if |
|---|---|---|
| `investigate` | "why is this slow / failing / behaving like this?", "what breaks if I change X?", or a deployed service throws errors. It reads first and reports, and does not fix as a side effect. | For a bug, the reply shows one command that reproduces it, with real output, before naming a cause. |
| `engineer-mindset` | "which architecture / library / schema?", "is this ready to release?", a capacity claim, an engineering trade-off, or writing a skill. It prices options, names the falsifier and keeps short answers short. | The verdict ends with "wrong if …", an observable you could check. |
| `grill-me` | "grill me on this plan". It interviews you in rounds, one decision tree at a time, until nothing is silently assumed. In Claude Code a hook also starts it whenever plan mode is on. | Questions arrive numbered with a recommended answer each, and none asks for a fact it could look up. |
| `review-pr` | "review this PR / branch / diff". It resolves the exact base and head, follows the change into callers, tests and failure paths, and checks the diff against its ticket. | Findings come under separate Standards and Spec headings, each with file:lines or a quoted spec line. |
| `deepsearch` | "what's the current answer to…?", or "has someone already built this?" before you build. It labels every source by tier, and recollection alone does not count as evidence. | Every claim carries a T0–T3 tier, and the reply says what was not searched. |
| `present` | "make this a report / explainer / diagram page / narrated video". It uses a bundled style kit and checks delivery. | You get a served preview and screenshots in both themes. |
| `cards-readme` | "write the model card / dataset card / README". Every metric is traced to its source. | The quickstart is on the first screen and every number names its source. |
| `toolchain` | "add / upgrade a dependency", "fix this venv", "write the Dockerfile install step". It uses lockfile-backed managers (uv, the repo's JS lockfile) and never bare pip. | The lockfile changes through the manager (`uv add`, `pnpm add`), never by hand. |
| `layout` | "where should this file / run / branch go, and what do I call it?" | A reorganization shows from → to → reason for every move before it runs. |
| `cleanup` | "port in use", "disk is full", "kill the stray dev servers / Docker junk". It sorts each item into safe / ask / never and deletes nothing unasked. | You see the safe / ask / never table before anything is removed. |
| `sentry-cli` | "look at this Sentry issue / trace / release" from the terminal. | The reply quotes the stack trace and first-seen release from the CLI, not a guess. |

## Evidence

- **Plugin evals** ([`evals/`](evals/), `claude plugin eval` format: `case.yaml` with graders, plus a `scaffold.sh` fixture). On 2026-09-27 (v1.6.0, haiku judge, 2–3 runs per case), 11 of 17 runs passed with the skill and 8 of 17 without it. The gain is modest and the judge is noisy; see [`evals/RESULTS.md`](evals/RESULTS.md). Only `investigate`, `review-pr`, `cards-readme`, `sentry-cli` and `grill-me` have cases so far.
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

Issues and PRs are welcome; [SCOPE.md](SCOPE.md) is the bar each one is judged against. A new skill needs at least one eval case that shows it changes an answer.

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

MIT. `skills/grill-me` and `skills/engineer-mindset/modules/module-design` keep their upstream MIT notices (mattpocock/skills).
