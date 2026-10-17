## Long or interruptible jobs -- resumable, never silently lossy

A job that can hit a rate limit, preemption, or a multi-hour wall clock needs to survive being
re-run, not just complete once:

- Tag each run so re-running with the same tag resumes instead of restarting from zero.
- On a rate limit or transient failure, pause and retry -- do not treat it as a fatal error.
- Never persist a failed call's output as if it succeeded; a partial result is worse than no result
  because it looks complete.
- Fail loudly on a partial ingest/write rather than silently continuing with incomplete data.
- Commit the raw per-run artifacts (rows, summary, config) alongside the aggregate, not just the
  aggregate -- the aggregate is not reproducible once the raw rows are gone.

## Hugging Face

`HF_API_TOKEN` is the org-scoped token. `HF_TOKEN` is a different, personal one — using it where the
org token is needed fails with a permissions error that reads like a missing repo.

## Choosing the right compute target

Three distinct targets exist. They are not interchangeable.

| Target | Reach it via | Notes |
| --- | --- | --- |
| SkyPilot k8s pool | `sky launch` (everything above) | Whatever shared cluster `sky gpus list` shows for your org — usually near-full. The default choice. |
| On-prem GPU node | your org's kubeconfig context for it | Single node, time-shared between training / generation / eval. Not a SkyPilot cluster. |
| SLURM cluster | SSH via bastion → `sbatch` | Check CPU arch and container runtime (Enroot/SQSH vs Docker) before assuming either. **Never run training or heavy inference on the login node** — admins kill the process. Confirm it is actually in use before starting here. |

Fill in your org's actual endpoint names, kubeconfig context, and bastion host in a local note —
this skill deliberately ships without them so it stays portable across machines and teams.
