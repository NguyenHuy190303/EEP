---
name: sky-job
description: SkyPilot GPU job lifecycle — preflight, launch, tunnel to the served port, harvest artifacts out of /tmp, tear down. Use before launching or debugging any SkyPilot cluster, vLLM serving job, training run, batch GPU job, or when a sky cluster is already up and behaving unexpectedly. Also covers the two other compute targets (on-prem 8xH100, GB200 SLURM) so the right one gets picked.
---

# SkyPilot job lifecycle

Read the whole file before the first `sky` command that changes state. The gotchas below each cost
real hours to discover; skipping to the launch line is how they get rediscovered.

## 1. Preflight — before spending anything

State one line and wait for a go-ahead:

> expected cost · expected duration · stop condition · durable output path

Then:

```bash
sky gpus list          # the pool is shared and usually near-full — check before assuming capacity
sky status             # is a cluster of yours already up? reuse beats launching
sky queue <cluster>    # if one is up, what is already running on it
```

Smoke-test with the smallest viable config first unless explicitly told to skip it.

## 2. Launch — and the queueing trap

```bash
sky launch -c <name> scripts/serve-<something>.yaml
```

**`sky launch` on a cluster that is already alive queues the job instead of replacing it.** The new
job sits behind the old one and nothing appears to happen. Cancel the old job first:

```bash
sky queue <name>          # find the job id
sky cancel <name> <job-id>
```

Never relaunch a job that failed until the failure is diagnosed. Read the real log first
(section 4), report the diagnosis, then relaunch. A retry is not a diagnosis.

## 3. Reaching the served port — `ports:` is not enough

Declaring `ports:` in the task YAML does **not** expose the port, so `sky status --endpoint` fails
and looks like a broken cluster. Tunnel instead:

```bash
ssh -f -N -L 8901:localhost:8000 <cluster>
export LLM_BASE_URL=http://localhost:8901/v1
```

Pick a local port that is not already taken; `-f -N` backgrounds the tunnel with no shell. Verify
with a single request against `$LLM_BASE_URL/models` before running anything long.

## 4. Harvest — before tearing down, not after

The cluster is the only copy of its logs. Once it is down they are gone.

```bash
sky logs <cluster> <job-id> > <durable-path>/<YYYY-MM-DD>_<slug>_skylog.txt
```

Everything a future session needs must end up outside `/tmp`:
job logs (stdout, stderr, scheduler), metrics, the exact config used, artifact metadata.

Destination: the project's results dir if the result is curated, otherwise
`~/.claude-trivita/projects/<project-slug>/memory/artifacts/`. One pointer line per artifact in the
project's `MEMORY.md`. An artifact without a pointer is saved but lost.

For a failure, quote the real error text from the remote log together with the log's path. If the
job died from quota, preemption, or OOM, name which one and the evidence line that says so.

## 5. Tear down — a required step

```bash
sky down <cluster>
```

Not optional, not "later". An idle GPU cluster bills and blocks the shared pool. Confirm with
`sky status` that it is gone.

Never `sky down --all` — it kills clusters other people are using. Cancel or down by name only.

## Hugging Face

`HF_API_TOKEN` is the org-scoped token. `HF_TOKEN` is a different, personal one — using it where the
org token is needed fails with a permissions error that reads like a missing repo.

## Choosing the right compute target

Three distinct targets exist. They are not interchangeable.

| Target | Reach it via | Notes |
| --- | --- | --- |
| SkyPilot k8s pool — `sky.dev.trivita.ai` | `sky launch` (everything above) | 2 nodes × 8 H100, shared, usually near-full. The default choice. |
| On-prem 8×H100 NVLink node | `KUBECONFIG_VM_TRIVITA_8H100_126` | Single node, time-shared between training / generation / eval. Not a SkyPilot cluster. |
| GB200 SLURM cluster | SSH via bastion → `sbatch` | arm64 Grace CPUs, Enroot/SQSH containers not Docker. **Never run training or heavy inference on the login node** — admins kill the process. Not currently in use; confirm before starting here. |
