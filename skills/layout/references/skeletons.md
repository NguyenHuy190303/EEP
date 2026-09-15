# Skeletons by repo type

Offered when creating a repo or when asked. Each is the widely used shape for that kind of
project, trimmed to what this workspace actually uses. Directories in `[brackets]` are added only
when the need exists — do not pre-create them.

## Service (FastAPI / worker) — what Trivita-Agent already does

```
app/                 the package: routers/, services/, models/, core/ as the code grows
tests/
  unit/              mirrors app/ (app/services/x.py -> tests/unit/services/test_x.py)
  integration/       needs a real DB / service
  e2e/               drives the deployed thing
alembic/             migrations (only if there is a DB)
helm/                chart for the k8s release
docs/
  decisions/         D-00xx via ./ops decide      (or docs/adr/ when the repo has no ./ops)
  problems/          P-00xx via ./ops problem
  runbooks/          how to operate it; every record file starts with its date
scripts/             ops + one-off; scripts/<job>/ once >3 files serve one job; 1-line header each
[eval_cases/]        curated eval set that ships with the service (small, committed)
[scratchpad/]        <TICKET>-<slug>/ quick trials; gitignored; emptied when the ticket closes
Makefile             test / lint / format / run — the intended entry point
pyproject.toml  uv.lock  Dockerfile  compose.yaml  README.md  .gitignore
```

## Research / data (training, eval, ASR, data engineering) — Cookiecutter Data Science, trimmed

```
src/<pkg>/           importable code: data/, features/, models/, eval/ as needed
data/
  raw/               as received, never edited (gitignored; README points to the source)
  interim/           cleaned / converted, reproducible from raw by a script
  processed/         model-ready
notebooks/           <YYYY-MM-DD>_<slug>.ipynb ; exploration only, no code other files import
experiments/         <YYYY-MM-DD>_<slug>/ : config.yaml run.log metrics.json README.md  (hypothesis runs)
outputs/             <YYYY-MM-DD>_<slug>/ : results + run.log together, gitignored     (production runs)
scripts/             CLI entry points: prepare_data.py train.py evaluate.py ; scripts/<job>/ when >3
tests/               unit/ mirrors src/<pkg>/ ; integration/ for anything touching real data or GPU
reports/             figures and HTML for humans; regenerated from experiments/, not hand-edited
[configs/]           <slug>.yaml, only once >=2 runs share one; each run still copies its resolved config
[models/]            local weights, gitignored; README.md holds the HF / cluster pointer
[scratchpad/]        <TICKET>-<slug>/ quick trials; gitignored
pyproject.toml  uv.lock  Makefile  README.md  DATA_SOURCES.md  .gitignore
```

`DATA_SOURCES.md` lists every external source with URL, license, date fetched, and the script
that fetches it. Clinical audio and transcripts never leave `trivitaai` / the cluster (user
CLAUDE.md autoMode environment) — the README says where they are, it does not contain them.

## Infra (Helm, ArgoCD, k8s) — what Trivita-cicd already does

```
helm/<chart>/        one chart per deployable
argocd/              Application manifests, one per env
k8s/                 raw manifests that are not chart-managed
example/             copy-paste starting points, clearly marked as examples
README.md            how a change gets from PR to app-uat to prod
```

## Skills / plugin repo — what EEP already does

```
.claude-plugin/ .codex-plugin/   manifests
skills/<name>/SKILL.md           one dir per skill; references/ kit/ scripts/ beside it
hooks/                           hooks.json + scripts
evals/<skill>-<n>/               claude plugin eval cases
README.md
```

## Naming cheatsheet

| Thing | Pattern | Example |
|---|---|---|
| Dated artifact | `<YYYY-MM-DD>_<slug>_<what>.<ext>` | `2026-09-16_asr-bench_wer.json` |
| Experiment dir | `experiments/<YYYY-MM-DD>_<slug>/` | `experiments/2026-09-16_LP-185-identity-eval/` |
| Pipeline output dir | `outputs/<YYYY-MM-DD>_<slug>/` (+ `run.log` inside) | `outputs/2026-09-16_crawl-shorts/` |
| Scratch dir | `scratchpad/<TICKET>-<slug>/` (gitignored) | `scratchpad/LP-57-voice-flag-off/` |
| Decision / problem record | `docs/decisions/D-00xx…` · `docs/problems/P-00xx…` via `./ops` | `docs/decisions/D-0036-…` |
| Notebook | `notebooks/<YYYY-MM-DD>_<slug>.ipynb` | `notebooks/2026-09-16_diarization-errors.ipynb` |
| Checkpoint | `<model>_<data>_<step-or-epoch>` | `whisper-large-v3_vi-med-12k_step-8000` |
| Branch | `<type>/<TICKET>-<slug>` | `feat/LP-185-identity-across-pods` |
| Commit | `type(scope): message` | `fix(proctor): keep identity across pod restarts` |
| Script | verb-first, one purpose | `scripts/prepare_data.py`, `scripts/deploy-watch.sh` |
