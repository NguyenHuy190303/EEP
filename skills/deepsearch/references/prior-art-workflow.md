## Mode: before-cook — has someone already done this?

Runs **before** writing code for anything that is not a one-liner: a model, a pipeline, a data
converter, an eval harness, a benchmark, a UI component. The question is not "is my claim true" but
"does the thing already exist". Same tiering discipline: a repo is T1 only after its code was read.

1. **Name the problem as a query**, plus 2–3 synonyms the field uses (`speaker diarization` /
   `who-spoke-when`; `Vietnamese ASR` / `vi speech-to-text`). Queries never contain PII,
   internal hostnames, or anything from a regulated dataset.
2. **Sweep the channels that hold artifacts**, not just prose:

   | Channel | How | Finds |
   |---|---|---|
   | GitHub repos + issues | `gh search repos`, `gh search issues` | implementations, known blockers |
   | Hugging Face Hub | `hf` CLI / API (skill `hf-cli`), model + dataset + Space search | weights, data, demos |
   | PyPI / npm | `pip index versions`, `npm view` | a package that already does it |
   | Papers with Code / arXiv | web | the method, and its reference code |
   | Kaggle / notebooks | web | working end-to-end examples on similar data |

3. **Is this a solved category?** Some problems have a standard answer and the only question is
   *which* standard answer — not whether to build one. See the table below. In a solved category,
   building your own needs a hard constraint that every standard option fails, stated out loud.
4. **Fit before quality.** Write the need as 3–6 concrete requirements *before* opening a
   candidate (inputs, outputs, scale, language, runtime, the hard constraint). A candidate missing
   one hard requirement is **reference only**, however famous — auditing quality first is how a
   100k-star repo gets adopted for a problem it does not solve.
5. **Audit what survives fit.** Stars are a popularity number taken once, usually after one HN
   post; never rank by them. Run `bash scripts/probe.sh <owner>/<repo>` and read it against
   `references/prior-art-audit.md`, which carries the seven signals that actually separate a
   maintained project from a weekend demo or an enterprise funnel — bus factor, whether recent
   issues get answered, real tests and CI, release discipline, commit texture, the code inside two
   core files, and what the README avoids saying. Licence check includes the open-core trap: BSL /
   SSPL / Elastic / "free under $X" are not open, and the feature you need sitting under
   *Enterprise* means the OSS edition is a demo of it. MIT / Apache-2.0 / BSD: use. GPL / AGPL /
   CC-NC / gated: stop and ask. **Age is not a signal**: an unmaintained 2019 CUDA kernel that
   still compiles and has no alternative is a fine dependency. What matters is whether it runs on
   the stack in play, and whether you would ever need upstream to change — if you can read and
   patch it yourself, vendor it and say so.
6. **Output a four-column verdict:**

   | Dùng luôn | Fork / adapt (the one delta) | Tham khảo thôi | Tự làm |
   |---|---|---|---|

   Code is written only for the last column. "Tham khảo thôi" is what keeps a famous but unfit or
   undependable repo from becoming a dependency — read it, cite it, do not import it. Choosing
   **tự làm** is a valid result, not a failed search: say so when the dependency would be a thin
   wrapper you could write in **~50 lines** you understand, when the integration surface is bigger
   than the problem, when fitting it means forking it, or when it drags in a framework for one
   function. This escape hatch covers glue, not whole categories — it never licenses rebuilding
   something from the solved-category table. The comparison is `write + maintain mine` vs `integrate + track upstream + debug
   through someone else's layer + the day it is abandoned`.
7. **Gaps as usual**: which channels were swept, which candidate could not be verified, what was
   not searched and why.

## Solved categories — adopt, never rebuild

The standard answer already exists, was hardened by more people than this team, and rebuilding it
produces a worse version you also have to maintain. Pick among the options; do not write a new one.

| Need | Adopt | Not |
|---|---|---|
| Metrics, alerting, dashboards | Prometheus + Grafana (+ Alertmanager) | a homemade metrics endpoint and a cron that emails |
| LLM tracing, prompt versions, evals | Langfuse (skill `langfuse`) | a table of prompts and a custom trace logger |
| Application errors | Sentry (skill `sentry-cli`) | try/except that writes to a file |
| Traces / instrumentation format | OpenTelemetry | a bespoke span format |
| Log aggregation | the platform's stack (k8s → Loki / ELK) | a log server of your own |
| Background jobs, queues | Celery / RQ / Arq, or Redis Streams | a polling loop over a DB table |
| GPU job lifecycle | SkyPilot | ssh + nohup + a tmux you forget |
| DB schema change | Alembic | hand-written ALTER scripts |
| Deploy / rollout | Helm + ArgoCD | kubectl apply from a laptop |
| Auth, sessions, tokens, hashing, crypto | an IdP or a reviewed library | anything hand-rolled — this is a security boundary |
| Input validation, settings | Pydantic / pydantic-settings | ad-hoc `dict` checks |
| Retry, backoff, timeout | tenacity (or the client's own) | a `while True` with `sleep` |
| Model serving | vLLM / Triton | a Flask wrapper around `model.generate` |
| Packages and environments | `uv`, the repo's lockfile (skill `toolchain`) | a `setup.sh` that pip-installs |

Two ways this table is misread, both wrong: it is **not** a shopping list — adopt only the row whose
need you actually have today; and it does **not** override the audit — "Prometheus" is a category
answer, the specific exporter or chart still gets checked.

Depth: the default is the full sweep with tiers and the audit — a wrong "nothing exists" costs days
of building, and a wrong "this one is fine" costs longer, because it is discovered after the
integration. Trim to one channel only when the user says the thing is throwaway.
