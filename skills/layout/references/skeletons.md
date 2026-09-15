# Skeletons by repo type

Offered when creating a repo or when asked. Each is the widely used shape for that kind of
project, trimmed to what this workspace actually uses. Directories in `[brackets]` are added only
when the need exists — do not pre-create them.

## Service (FastAPI / worker) — what Trivita-Agent already does

```
app/                 the package: routers/, services/, models/, core/ as the code grows
tests/               mirrors app/ ; unit next to the module it tests, e2e/ separate
alembic/             migrations (only if there is a DB)
helm/                chart for the k8s release
docs/                ADRs, runbooks, API notes — one file per topic, dated when it is a record
scripts/             one-off and ops scripts; each has a 1-line header saying what it is for
[eval_cases/]        curated eval set that ships with the service
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
experiments/         <YYYY-MM-DD>_<slug>/ : config.yaml run.log metrics.json README.md
scripts/             CLI entry points: prepare_data.py train.py evaluate.py
reports/             figures and HTML for humans; regenerated from experiments/, not hand-edited
[models/]            local weights, gitignored; README.md holds the HF / cluster pointer
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
| Notebook | `notebooks/<YYYY-MM-DD>_<slug>.ipynb` | `notebooks/2026-09-16_diarization-errors.ipynb` |
| Checkpoint | `<model>_<data>_<step-or-epoch>` | `whisper-large-v3_vi-med-12k_step-8000` |
| Branch | `<type>/<TICKET>-<slug>` | `feat/LP-185-identity-across-pods` |
| Commit | `type(scope): message` | `fix(proctor): keep identity across pod restarts` |
| Script | verb-first, one purpose | `scripts/prepare_data.py`, `scripts/deploy-watch.sh` |
