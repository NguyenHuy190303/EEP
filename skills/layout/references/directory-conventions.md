## Per-directory rules — decided conventions

| Directory | Rule |
|---|---|
| `tests/` | Mirrors the package: `tests/unit/` repeats the tree of `app/` or `src/<pkg>/` (`app/services/x.py` → `tests/unit/services/test_x.py`); `tests/integration/` needs a real DB or service; `tests/e2e/` drives the deployed thing. Never tests beside the module. |
| `docs/` | Four kinds of document, four subdirs — never mixed: **`spec/`** living documents, **ordered by a 2-digit prefix** (below); **`decisions/`** + **`problems/`** the ops ledger (D-00xx, P-00xx via `./ops`; `adr/` when the repo has no `./ops`); **`runbooks/`** how to operate; **`reports/`** dated, write-once outputs for humans — standups, findings, journals, postmortems — `<YYYY-MM-DD>_<slug>.<ext>`. The doc *styling* kit is not stored here: `present` embeds it into each page from its own `kit/` folder. Images and diagrams a spec references go in `docs/assets/<spec-slug>/`. No loose `notes.md`, no `build/` that mixes kinds. |

### `docs/spec/` — numbered, living, undated

`<NN>_<slug>.md` or `.html`, `NN` from `00`, in **reading order** — the number is the order someone
new should read them, not a date and not an ID. Living documents: overwritten in place, never
suffixed `_v2` or `_final`; the history is git's job.

```
docs/spec/
  00_overview.md            what the system is, one screen, links onward
  01_architecture.html      subsystems and how they talk
  02_speech.html            one page per subsystem, in reading order
  03_computer-vision.html
  10_design-system/         a spec big enough for several pages gets a numbered DIRECTORY
    00_tokens.md            colour, type, spacing — numbering restarts inside
    01_components.md
    02_patterns.md
    tokens.css              the file the frontend actually imports; spec and app read one file
```

- **Gaps on purpose.** Number in tens once a section exists (`10_`, `20_`) so a page inserted later
  does not renumber its neighbours. Renumbering breaks every link that points at the old name.
- `.md` when it is text and diffs matter; `.html` when it carries diagrams, tables, or is meant to
  be read in a browser — built through `present`, and then `00_overview` links to it.
- A spec that needs more than one page becomes a numbered directory, numbering restarts at `00`
  inside. `docs/spec/10_design-system/` is the one for the product UI.
- No `index.html`: `00_overview` is the index, and `ls` already sorts the rest.
| `scripts/` | Plural. Flat until more than 3 files serve one job, then `scripts/<job>/` (`scripts/ops/`, `scripts/audio-bench/`). First line of every script says what it is for. Not a place for library code — that goes in the package. |
| `outputs/` | What a **pipeline run** produces (crawl, convert, batch inference): `outputs/<YYYY-MM-DD>_<slug>/` holding the results **and** `run.log` together — a log separated from its output is a log of nothing. Gitignored; the README of the run says where the durable copy went. `experiments/` is for runs that test a hypothesis; `outputs/` for runs that just produce. |
| `experiments/` | Rule 3 above. |
| `notebooks/` | `<YYYY-MM-DD>_<slug>.ipynb`. Exploration only: nothing imports from a notebook; code that survives moves into the package. |
| `configs/` | Exists only once ≥2 runs share a config; `configs/<slug>.yaml`. Each run still copies its **resolved** config into its own dir, so a run reproduces without `configs/` history. |
| `data/` | Research repos: `raw/` (as received, never edited, gitignored) → `interim/` (rebuildable by a script) → `processed/` (model-ready), plus `DATA_SOURCES.md`. Service repos: only small curated fixtures or eval sets, committed; anything larger is a pointer. |
| `scratchpad/` | Allowed for quick trials beside real code: `scratchpad/<TICKET>-<slug>/`. **Gitignored.** Emptied when the ticket closes; anything worth keeping is promoted into the package, `experiments/`, or `docs/`. |
| `models/` | Local weights, gitignored; `README.md` holds the HF org or cluster pointer. |
| `_archive/` | Tidy mode parks here (`_archive/<YYYY-MM-DD>/`) instead of deleting. the user deletes. |
| `logs/` | Does not exist. A log lives with the run that wrote it (`experiments/…/run.log`, `outputs/…/run.log`); a service's logs go to the platform (k8s / Sentry / Grafana), not into the repo. |
