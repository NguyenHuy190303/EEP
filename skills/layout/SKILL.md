---
name: layout
description: Use when creating a directory, file, experiment run, branch, or repo, when naming anything (artifact, checkpoint, script, notebook), or when asked to tidy a messy folder. Holds the one set of conventions for where things go and what they are called — repo root stays clean, dates sort, branches carry type and ticket — plus suggested skeletons per repo type.
---

# Layout — where it goes, what it is called

The failure this exists to stop: `output_test/`, `asr.json`, `tts-output.wav`, `shorts_retry.log`
and an `.xlsx` all sitting in a repo root, and three branch prefixes meaning the same thing.
Tidiness is not aesthetics; it is what lets someone (including me, next week) find the thing
without asking.

## Hard rules — apply always, no need to ask

1. **Root stays clean.** Only manifests and entry points live at repo root: `README.md`,
   `pyproject.toml` / `package.json`, lockfile, `Makefile`, `.gitignore`, `Dockerfile`,
   `compose.yaml`, CI config, and the top-level dirs. Logs, data, media, notebooks, outputs,
   one-off scripts, spreadsheets: never at root — each goes into a directory named for its
   **role** (`data/`, `scripts/`, `notebooks/`, `experiments/`, `docs/`), not for its file type.
2. **Names sort and grep.** Fields separated by `_`, words inside a field by `-`; date first when
   time matters: `<YYYY-MM-DD>_<slug>_<what>.<ext>` (same rule as `memory/artifacts`). Language
   rules win inside code: Python modules `snake_case`, TS files as the repo already does. Never
   `final`, `v2`, `new`, `copy`, `tmp`, `test2`, `latest` in a name — the version is the date or
   git, and "latest" is a symlink, not a filename.
3. **One experiment, one dated folder.** `experiments/<YYYY-MM-DD>_<slug>/` containing
   `config.yaml` (what was run), `run.log`, `metrics.json` (numbers, machine-readable), and a
   `README.md` of ≤5 lines: goal, result, conclusion, what to do next. Slug carries the ticket when
   one exists (`2026-09-16_LP-185-identity-eval`). Checkpoints and datasets are not committed —
   `.gitignore` them and put their real location (HF org `trivitaai`, cluster path, or
   `memory/artifacts`) in that README.
4. **Branches: `<type>/<TICKET>-<slug>`.** Types: `feat` · `fix` · `chore` · `docs` · `exp` ·
   `refactor`. Ticket omitted when there is none (`exp/whisper-vi-lora`). Commits follow
   Conventional Commits: `type(scope): message`. Not `feature/`, not `bugfix/`, not bare `develop2`.
5. **Where a thing lives** — decide once:

   | Thing | Lives in |
   |---|---|
   | Code, config, tests, docs, small eval sets | the repo |
   | Result that cost GPU/quota/money, not project-curated | `~/.claude/projects/<slug>/memory/artifacts/` + pointer line in `MEMORY.md` |
   | Weights, large datasets | HF org `trivitaai` or the cluster volume; repo holds only the pointer |
   | Build context, scratch, re-downloadable | `/tmp` (swept after 3 days — nothing expensive stays there alone) |

6. **Do not create when editing will do.** No scaffolding "for later", no empty `utils/`, no second
   script that does what the first one does with one flag changed. A new file earns its place by
   having a role the existing ones cannot carry.

## Per-directory rules — decided with Huy 2026-09-16

| Directory | Rule |
|---|---|
| `tests/` | Mirrors the package: `tests/unit/` repeats the tree of `app/` or `src/<pkg>/` (`app/services/x.py` → `tests/unit/services/test_x.py`); `tests/integration/` needs a real DB or service; `tests/e2e/` drives the deployed thing. Never tests beside the module. |
| `docs/` | The ops ledger when the repo has `./ops`: `docs/decisions/` (D-00xx), `docs/problems/` (P-00xx). Otherwise `docs/adr/` for decisions. `docs/runbooks/` for how-to-operate. Every record file starts with its date. No loose `notes.md`. |
| `scripts/` | Plural. Flat until more than 3 files serve one job, then `scripts/<job>/` (`scripts/ops/`, `scripts/audio-bench/`). First line of every script says what it is for. Not a place for library code — that goes in the package. |
| `outputs/` | What a **pipeline run** produces (crawl, convert, batch inference): `outputs/<YYYY-MM-DD>_<slug>/` holding the results **and** `run.log` together — a log separated from its output is a log of nothing. Gitignored; the README of the run says where the durable copy went. `experiments/` is for runs that test a hypothesis; `outputs/` for runs that just produce. |
| `experiments/` | Rule 3 above. |
| `notebooks/` | `<YYYY-MM-DD>_<slug>.ipynb`. Exploration only: nothing imports from a notebook; code that survives moves into the package. |
| `configs/` | Exists only once ≥2 runs share a config; `configs/<slug>.yaml`. Each run still copies its **resolved** config into its own dir, so a run reproduces without `configs/` history. |
| `data/` | Research repos: `raw/` (as received, never edited, gitignored) → `interim/` (rebuildable by a script) → `processed/` (model-ready), plus `DATA_SOURCES.md`. Service repos: only small curated fixtures or eval sets, committed; anything larger is a pointer. |
| `scratchpad/` | Allowed for quick trials beside real code: `scratchpad/<TICKET>-<slug>/`. **Gitignored.** Emptied when the ticket closes; anything worth keeping is promoted into the package, `experiments/`, or `docs/`. |
| `models/` | Local weights, gitignored; `README.md` holds the HF (`trivitaai`) or cluster pointer. |
| `_archive/` | Tidy mode parks here (`_archive/<YYYY-MM-DD>/`) instead of deleting. Huy deletes. |
| `logs/` | Does not exist. A log lives with the run that wrote it (`experiments/…/run.log`, `outputs/…/run.log`); a service's logs go to the platform (k8s / Sentry / Grafana), not into the repo. |

## Suggested skeletons — offer, never impose

When starting a new repo, or when asked "how should this be organised", pick the closest skeleton
from `references/skeletons.md` (service · research/data · infra · skills/plugin) and adapt it.
An existing repo is **not** reshuffled to match a skeleton unless Huy asks; the hard rules above are
enough for an existing repo.

## Tidy mode — when asked to clean a folder

1. Inventory: list what is there with size, last modified, and a one-word role guess.
2. Propose moves as a table (`from → to`, reason), grouped by rule 1–3 above. Flag anything that
   looks like a result that cost money (rule 5) — those get a pointer, not a delete.
3. Move only after OK. `git mv` inside a repo so history follows. Never delete — park in
   `_archive/<YYYY-MM-DD>/` and let Huy delete.

## Output

The move table or the created tree, then one line per rule that applied. No essay on tidiness.
