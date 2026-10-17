## 5. Harvest — before tearing down, not after

The cluster is the only copy of its logs. Once it is down they are gone.

```bash
sky logs <cluster> <job-id> > <durable-path>/<YYYY-MM-DD>_<slug>_skylog.txt
```

Everything a future session needs must end up outside `/tmp`:
job logs (stdout, stderr, scheduler), metrics, the exact config used, artifact metadata.

Destination: the project's results dir if the result is curated, otherwise
`~/.claude/projects/<project-slug>/memory/artifacts/`. Record each artifact in the
project's `memory/artifacts/INDEX.md`; keep one link to that ledger in `MEMORY.md`. An artifact without a pointer is saved but lost.

For a failure, quote the real error text from the remote log together with the log's path. If the
job died from quota, preemption, or OOM, name which one and the evidence line that says so.

## 6. Tear down — a required step

```bash
sky down <cluster>
```

Not optional, not "later". An idle GPU cluster bills and blocks the shared pool. Confirm with
`sky status` that it is gone.

**Autostop with `--down` (`sky launch … -i <min> --down`) deletes the logs with the cluster.** It is
the right default for releasing a shared pool only when the job itself copies its logs and artifacts
to durable storage (a bucket mount, object store) as the last step of `run:`. Without that step,
harvest by hand (section 5), then `sky down`. A finished cluster with a long autostop window still
holds its cards until the window ends.

Never `sky down --all` — it kills clusters other people are using. Cancel or down by name only.
