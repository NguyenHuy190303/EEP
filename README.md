# EEP — Easy Engineer Plugin

Huy's own agent skills, one copy, loaded by Claude Code and Codex as the plugin `eep`.
Third-party skills (archify, the Hugging Face marketplace ones) stay outside — they have their own installers.

| Skill | Use when |
|---|---|
| `investigate` | why something behaves as it does, blast radius, data/request flow, where the time goes |
| `design-decision` | choosing architecture/stack/library/schema — constraints first, ≥2 priced options, horizon + falsifier |
| `deepsearch` | research needing sourced answers; model memory is never evidence. Mode `before-cook`: before building anything, sweep GitHub / HF Hub / PyPI / Papers with Code / Kaggle for an existing repo, model, dataset, notebook |
| `review-pr` | evidence-first review of a PR/branch/diff |
| `present-html` | any HTML page (report, spec, memo, dashboard); owns the 2-theme kit |
| `cards-readme` | HF model card, dataset card, GitHub README |
| `sentry-cli` | inspecting Sentry issues/events/traces via the CLI |
| `sky-job` | SkyPilot GPU job lifecycle |
| `vietnamese-writing` | before any Vietnamese prose |
| `cleanup` | port in use, forgotten dev server / tunnel, disk filling, Docker or OrbStack junk, stray tmux / nohup — reports and tiers safe · ask · never, deletes nothing unasked; local machine only |
| `toolchain` | installing / adding / upgrading a dependency, making a venv or node_modules, writing a Dockerfile or CI install step — uv for Python, the repo's lockfile for JS, container pinned by digest |
| `layout` | creating dirs / files / experiments / branches, naming anything, tidying a folder — root stays clean, dates sort, `type/TICKET-slug`; skeletons per repo type in `references/` |

## Install

Claude Code — loads in place from the skills directory (`eep@skills-dir`), edits to `SKILL.md` are live:

```bash
ln -sfn ~/Projects/EEP ~/.claude/skills/eep
```

Codex — local marketplace, then install (Codex copies into its cache; after editing, bump `version` in both `plugin.json` and re-run the second line):

```bash
codex plugin marketplace add ~/Projects/EEP
codex plugin add eep@eep
```

Plugin skills are namespaced: `eep:investigate`, `/eep:review-pr`. Descriptions still trigger by content.

## Check

```bash
claude plugin validate .            # manifest + skill frontmatter
bash hooks/skill-index.sh           # what the SessionStart hook prints
claude plugin eval . --runs 1       # behaviour evals (spends tokens; 9 cases, with/without baseline)
```

Evals live in `evals/<skill>-<n>/` in the native `claude plugin eval` format: `prompt.md` + `graders/criteria.md` (llm rubric) + `graders/skill-fired.md` (was the skill actually invoked).

## Layout

```
.claude-plugin/plugin.json      Claude manifest (name = namespace)
.claude-plugin/marketplace.json local marketplace, source "./"
.codex-plugin/plugin.json       Codex manifest (same skills/, same hooks/)
skills/<name>/SKILL.md          the skills; references/, kit/, scripts/ beside them
hooks/hooks.json                SessionStart → hooks/skill-index.sh
evals/                          claude plugin eval cases
```
