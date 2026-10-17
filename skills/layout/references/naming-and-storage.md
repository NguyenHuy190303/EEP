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
   one exists (`2026-09-16_TICKET-123-identity-eval`). Checkpoints and datasets are not committed —
   `.gitignore` them and put their real location (your HF org, cluster path, or
   `memory/artifacts`) in that README.
4. **Branches: `<type>/<TICKET>-<slug>`.** Types: `feat` · `fix` · `chore` · `docs` · `exp` ·
   `refactor`. Ticket omitted when there is none (`exp/whisper-vi-lora`). Commits follow
   Conventional Commits: `type(scope): message`. Not `feature/`, not `bugfix/`, not bare `develop2`.
5. **Where a thing lives** — decide once:

   | Thing | Lives in |
   |---|---|
   | Code, config, tests, docs, small eval sets | the repo |
   | Result that cost GPU/quota/money, not project-curated | `~/.claude/projects/<slug>/memory/artifacts/` + pointer in the artifact index, linked once from `MEMORY.md` |
   | Weights, large datasets | your HF org or the cluster volume; repo holds only the pointer |
   | Build context, scratch, re-downloadable | `/tmp` (swept after 3 days — nothing expensive stays there alone) |

6. **Do not create when editing will do.** No scaffolding "for later", no empty `utils/`, no second
   script that does what the first one does with one flag changed. A new file earns its place by
   having a role the existing ones cannot carry.
