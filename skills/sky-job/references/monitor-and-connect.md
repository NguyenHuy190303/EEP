## 3. Monitor — block on the job, never poll

```bash
sky logs <cluster> <job-id> > <log-file>   # streams until the job ends; run it in the background, read the file
sky logs <cluster> <job-id> --status       # returns at once: exit 0 = succeeded, non-zero = anything else
sky logs <cluster> <job-id> --tail 100     # last lines only, after the fact
```

`sleep` + `sky queue` in a loop wastes tokens and races the scheduler: block on the streaming
`sky logs` instead. `--status` does not wait; it reports the current state. Its non-zero codes are
documented inconsistently (v0.14.0rc1 `--help` lists 100 failed / 101 not finished / 102 not found /
103 cancelled in one place and "1 for all other statuses" in another), so branch on zero vs non-zero
only.

## 4. Reaching the served port — `ports:` is not enough

Generic SkyPilot advice says to set `ports:` and open the security group. On the shared pool this
skill was written against, declaring `ports:` in the task YAML does **not** expose the port, so `sky status --endpoint` fails
and looks like a broken cluster. Tunnel instead:

```bash
ssh -f -N -L 8901:localhost:8000 <cluster>
export LLM_BASE_URL=http://localhost:8901/v1
```

Pick a local port that is not already taken; `-f -N` backgrounds the tunnel with no shell. Verify
with a single request against `$LLM_BASE_URL/models` before running anything long.
