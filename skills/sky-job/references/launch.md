## 1. Preflight — before spending anything

State one line and wait for a go-ahead:

> expected cost · expected duration · stop condition · durable output path

Then:

```bash
sky api info                     # connected to the API server? "Could not connect" = re-login, not a broken pool
sky gpus list                    # the pool is shared and usually near-full — check before assuming capacity
sky status -u -o json            # yours and other people's clusters; reuse beats launching
sky queue <cluster> -o json      # if one is up, what is already running on it
sky launch --dryrun -c <name> task.yaml   # resources + placement without provisioning
```

Use `-o json` whenever a command's output is going to be read by a script or by you; the table
format is for humans and changes between versions.

Smoke-test with the smallest viable config first unless explicitly told to skip it.

**Picking a GPU on a time-shared node:** generic SkyPilot advice is "set `accelerators:` and let
the optimizer choose". That holds across clouds, not on one shared node. The scheduler's allocation
ledger can say a card is empty while processes it does not account for hold most of its memory, and
some cards can be reserved for production by an admission policy that rejects the pin. Pick by the
card's real peak memory over the last day (DCGM / host-level GPU metrics), skip reserved cards, and
pin the card explicitly. The org-specific card map and metric names live in a local note.

## 2. Launch — and the queueing trap

```bash
sky launch -c <name> task.yaml          # always name it; an unnamed cluster is hard to reference
sky exec <name> task.yaml               # rerun on a live cluster: skips provisioning and setup
```

**`sky launch` on a cluster that is already alive queues the job instead of replacing it.** The new
job sits behind the old one and nothing appears to happen. Cancel the old job first:

```bash
sky queue <name> -o json  # find the job id
sky cancel <name> <job-id>
```

**`workdir:` sync is additive.** rsync copies new files but never deletes remote ones, so a rerun
can execute against stale configs or build artifacts. Wipe `~/sky_workdir` on the remote, or clean
the specific paths at the top of `run:`, when a rerun must start clean.

Never relaunch a job that failed until the failure is diagnosed. Read the real log first
(section 5), report the diagnosis, then relaunch. A retry is not a diagnosis.

`sky jobs launch` (managed jobs with automatic recovery) is the generic answer for unattended work.
On a shared pool, confirm managed jobs actually run there (`sky jobs queue` answers without error,
one tiny job completes) before planning around them.
