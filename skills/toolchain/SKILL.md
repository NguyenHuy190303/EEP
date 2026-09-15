---
name: toolchain
description: Use before installing, adding, upgrading or removing a dependency, creating or repairing a virtualenv or node_modules, writing a Dockerfile or CI install step, or running a project's tooling. Every project is managed by its own lockfile-backed manager — uv for Python, the repo's existing lockfile for JavaScript — never a bare pip install, never the system interpreter, never a hand-edited lockfile.
---

# Toolchain — the env is the lockfile, everywhere

The failure this stops: it works on this Mac, fails in CI, and fails differently in the container,
because three environments were built three ways. One lockfile per project, committed, and every
environment — local, CI, image, GPU cluster — is built from it.

Adding a dependency at all is the last rung: stdlib → platform feature → something already
installed → only then a new package, and the commit message says why.

## Python — `uv`, always

| Intent | Command |
|---|---|
| Add a dependency | `uv add <pkg>` (`--dev` for dev-only, `--optional dev` where dev is an **extra**) — never hand-edit `pyproject.toml` |
| Install what CI installs | `uv sync --locked --extra dev` |
| Run anything in the project env | `uv run <cmd>` |
| One-off tool, not a project dependency | `uvx <tool>` |
| Check the lock matches `pyproject.toml` | `uv lock --check` |

- **A bare `uv sync` uninstalls pytest in these repos** — dev deps here are an *extra*, not a
  dependency-group, so `--group dev` is also wrong. `uv sync --locked --extra dev` is what CI runs.
- `uv.lock` is committed and must agree with `pyproject.toml`; `uv lock --check` fails when it
  drifted. Never edit a lockfile by hand.
- Never `pip install` into the system interpreter, never `sudo pip`, never `pip install --user`,
  never `conda activate` in a repo that has a `uv.lock`. `.venv/` is gitignored, never committed.
- Repos with GPU weights pull gigabytes on sync — for a check that needs no GPU, run the single
  smoke test rather than syncing everything.

## JavaScript — the repo's lockfile names the manager

Detect, do not choose: `pnpm-lock.yaml` → pnpm · `package-lock.json` → npm · `yarn.lock` → yarn.
**One lockfile per repo**; two lockfiles means two machines resolve two different trees, so delete
the stray one rather than letting both live.

| Intent | npm | pnpm | yarn |
|---|---|---|---|
| Install exactly the lock (CI, Docker) | `npm ci` | `pnpm install --frozen-lockfile` | `yarn install --immutable` |
| Add a dependency | `npm install <pkg>` | `pnpm add <pkg>` | `yarn add <pkg>` |
| One-off tool | `npx <tool>` | `pnpm dlx <tool>` | `yarn dlx <tool>` |

Lockfile is committed with the change that caused it. `node_modules/` is never committed. No
global installs (`npm i -g`) for anything a project needs — that is an undeclared dependency.

## Container and GPU cluster — the container is the env, the lock still rules

- Base image pinned by **digest** (`python:3.12-slim@sha256:…`), not a moving tag, and never
  `:latest`.
- Inside the image: copy `pyproject.toml` + `uv.lock`, then `uv sync --locked`. No loose
  `pip install X` lines in a Dockerfile — that is a dependency nobody can reproduce.
- SkyPilot / SLURM tasks install the same way in `setup:`; a task that `pip install`s a list of
  packages inline is how "runs on the cluster, broken locally" happens. See skill `sky-job`.
- The image tag that ran a job goes in that run's `README.md` (skill `layout`), so the run can be
  rebuilt.

## Repos that predate this rule

`Trivita-Speech` and `Trivita-His/h5-chainlit` carry `requirements.txt`, and one `environment.yml`
exists. **Do not convert them as a side effect of an unrelated change.** Record the debt once —
`./ops problem` where the repo has it, otherwise a line in `docs/problems/` — and migrate to
`pyproject.toml` + `uv.lock` the next time work lands in that repo on purpose.

## Check that closes a toolchain change

| Change | Check |
|---|---|
| Added / removed a dependency | `uv lock --check` (or the JS frozen install) + the repo's own test entry point |
| Dockerfile or CI install step | the build runs, and the installed version matches the lock |
| Anything touching a GPU repo's env | say which environment you verified on — local venv is not the cluster |

Secrets and `.env` files are out of scope here: they are governed by the permission rules in
`~/.claude/settings.json` and the Codex permission profile, not by this skill.
