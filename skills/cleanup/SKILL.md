---
name: cleanup
description: Use when a port is already in use, a background dev server or tunnel was left running, disk is filling up, Docker or OrbStack has accumulated containers, images, build cache or volumes, a tmux or nohup process is still alive after work finished, or Huy asks to tidy up the machine. Reports what is holding each resource, tiers it safe / ask / never, and deletes nothing until he says so.
---

# Cleanup — local machine only

The reason this exists is not `docker system prune` — that is one command. It is that the popular
cleanup commands delete the wrong things: `docker system prune -a --volumes` takes the local dev
database with it, and `kill $(lsof -ti:8777)` kills a LaunchAgent that restarts 15 seconds later,
so the port looks cleaned and is not.

Remote resources are **out of scope**: SkyPilot clusters, k8s pods and anything that costs money
belong to skill `sky-job`, which has its own gates. Never `sky down --all`, never
`kubectl delete` from here.

## Always: report first

```bash
bash scripts/report.sh
```

Prints listening ports with the process holding each one, processes still attached to a terminal
(the reliable tell for "a shell left this behind" — daemons and app helpers have no controlling
terminal), tmux sessions, and the Docker table with containers, volumes and reclaimable sizes.
It deletes nothing.

Then present a table: **what · how much it frees · tier · the exact command**, and wait. Even the
safe tier is proposed, not executed, unless Huy already said go.

## Tiers

### Safe — rebuildable from a command, no state inside

| Thing | Command | Note |
|---|---|---|
| Build cache | `docker builder prune -f` | usually the biggest number by far; rebuilds on next build |
| Dangling images (`<none>`) | `docker image prune -f` | untagged layers from replaced builds |
| Exited containers | `docker rm <name>` (name them) or `docker container prune -f` | a container is not state; its **volume** is |
| Finished compose project | `docker compose -p <project> down` (no `-v`) | stops and removes containers, keeps volumes |

### Ask — cheap to delete, expensive or impossible to get back

- **Running containers.** Something may be mid-write. Name it, say what it belongs to, ask.
- **Images that are slow to rebuild**: GPU/ML bases, anything multi-GB or built from a private
  registry. Freeing 700 MB to spend 10 minutes rebuilding is a bad trade — say the trade out loud.
- **Terminal processes**: a dev server (`npm run dev`, `uvicorn --reload`), an SSH tunnel, a
  training run. Show PID, elapsed time and the full command; Huy decides. `SIGTERM` first
  (`kill <pid>`), `SIGKILL` (`kill -9`) only after it refuses.
- **tmux sessions**: `tmux attach -t <name>` and look before `tmux kill-session`. A session holding
  a half-finished run is not junk.

### Never automatically

- **Docker volumes.** They are the only place local state lives — dev databases, MinIO buckets,
  Redis dumps. `LINKS=0` means no container references it *right now*, not that it is junk: a
  `compose down` leaves its data volume at 0 links and `compose up` expects it back. **Never**
  `docker system prune --volumes`, never `docker volume prune`. List them with owner and size;
  delete only a volume Huy names, one at a time.
- **Anything this session did not start**, unless Huy says whose it is. Another terminal, another
  person's tunnel, an editor's language server.
- **Processes under launchd.** The reports server on `:8777` is the LaunchAgent
  `ai.trivita.reports` with `KeepAlive` — killing the PID achieves nothing. To actually stop it:
  `launchctl bootout gui/$(id -u)/ai.trivita.reports`. Same shape for anything else in
  `~/Library/LaunchAgents`.
- **`/tmp` artifacts that were never persisted.** Check the durable-storage rule first (user
  CLAUDE.md §2) — an expensive result living only there gets copied out before anything is removed.

## Port already in use

```bash
lsof -nP -iTCP:<port> -sTCP:LISTEN       # who holds it — read the command, do not kill blind
```

Then decide by owner: your own dev server → stop it in its terminal; a container → `docker stop`;
a LaunchAgent → `launchctl bootout`; something you do not recognise → report it, do not kill it.
Never `kill -9 $(lsof -ti:<port>)` as a reflex: it skips the question of what that process was
doing, and on a supervised process it is a no-op with extra steps.

## Output

The table, the reclaimable total, then the commands actually run and what they freed. Report the
real numbers (`docker system df` before and after), not "cleaned up".
