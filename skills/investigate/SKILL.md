---
name: investigate
description: Use when the question is why something behaves as it does, what a change would break, where data or a request actually flows, or where the time goes. Covers root-cause analysis, blast-radius/impact analysis, data and network flow tracing, and performance investigation. Read-first — reports findings rather than fixing as a side effect.
---

# Investigate

Pick the mode from the question. They share the discipline below and differ in what counts as
coverage.

| Mode | Question |
|---|---|
| `root-cause` | why is it broken |
| `impact` | if I change this, what breaks |
| `flow` | where does this data / request actually go |
| `perf` | where does the time go |

## Shared discipline

**Restate the symptom in observables.** Log line, exit code, error text, a measured number, a
screenshot. Not "the WebSocket is flaky" but the actual close code and the count. If the symptom is
only reported second-hand, say so and find the observable before theorising.

**Draw the boundary early.** Two lists: what is ruled out and by what evidence, what is still in
scope. An investigation without a shrinking boundary is a tour.

**Every claim carries its evidence inline** — `path/to/file.py:214`, or the command and its real
output. Anything you concluded rather than observed is labelled as inference. Never paraphrase an
error; paste it.

**Separate root cause from contributing condition from symptom.** Naming a contributing condition as
the root cause is the most common way an investigation ends early and the bug comes back.

**Close with what is open.** What is now established, what is still UNCHECKED, and specifically what
observation would close each open item. A green local test does not close a claim about a running
system (user CLAUDE.md §4b).

**Do not fix while investigating** unless the fix is one line and obviously correct, or you were
asked to. Report first. A fix mid-investigation destroys the evidence for whether it was the cause.

## Mode specifics

### root-cause
Reproduce when the failure is observable and reproducing costs less than the fix. When it is not
reproducible — flaky, production-only, unsafe — say so and name the strongest proxy you used instead.
Do not build a reproduction harness larger than the bug.

Work backwards from the observable to the first point where the invariant was already violated. That
point, not the crash site, is where the root cause lives.

### impact
Text search finds strings; it does not find call sites. Use `ast-grep` for structural matches, and
the LSP tool where a code-intelligence plugin is active. Grep is the fallback, and its misses are
your responsibility to state.

Coverage is not just callers. Sweep: callers · tests · fixtures · migrations · config and env vars ·
serialised data already on disk or in a queue · anything outside the repo that consumes the shape
(HTTP clients, events, DB schema, dashboards, alerts).

Say plainly what you could not enumerate — consumers outside the repo usually cannot be, and a
confident "nothing else uses this" is the failure mode here.

### flow
Follow the data, not the directory tree. One line per hop:
`where → where (protocol, shape of the payload)`. Note where the shape changes, where it is
validated, and where it is persisted. Mark hops you inferred from code but did not observe.

A diagram only when there are three or more hops and at least one branch.

### perf
State the budget and the current baseline before proposing anything. Optimising without a budget
produces work nobody asked for.

Measure before attributing. `hyperfine` for commands, in-process timing for hot paths. Report where
the time went as a breakdown that sums to the total, and say what environment it was measured on —
a laptop number is not a pod number.

## Tools available on this machine

`rg` `fd` `ast-grep` · `jq` `gron` `jless` `yq` · `curl` `httpie` `websocat` `dig` `lsof` `tcpdump`
`nc` · `psql` `redis-cli` `sqlite3` · `kubectl` `helm` `argocd` `docker` · `hyperfine` · `gh` ·
MCP: grafana (metrics, logs), sentry (errors), atlassian (Jira, Confluence), chrome (browser).

Reach for the CLI before writing a script. `gron` makes JSON greppable; `ast-grep` makes code
structurally searchable; `websocat` tests a WebSocket without a Python harness.
