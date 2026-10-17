---
name: investigate
description: Use to find why something behaves as it does, what a change would break, where data or a request flows, where time goes, or why a deployed service fails (errors, logs, metrics). Read-first; reports findings rather than fixing as a side effect.
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
| `deployed service` | why a running dev/prod service fails, seen only through telemetry |

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
observation would close each open item. A green local test suite proves the code does not
contradict itself; it does not prove a claim about the running system in production — that needs
an observation from that system.

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

**Comparing two configs/variants is a paired test, not two point estimates.** "77% vs 75.9%" from
two independent runs is noise dressed as a finding. Run both on the same inputs, use a paired test
(McNemar for pass/fail pairs, a paired t-test or Wilcoxon for continuous metrics), and report the
interval and sample size next to the delta. A result that does not clear the test is a null, and a
null with its cost (tokens, dollars, wall time) reported is still useful — it rules something out.
Include at least one negative control: a case that should show no effect, so a wiring bug that
makes everything look like an improvement gets caught before the real comparison is trusted.

### deployed service
A root-cause on a running dev/prod service, where you see it only through telemetry. Work down;
each step is cheaper than the next and most stop at step 2.

1. **Error tracker first** (`eep:sentry-cli` when Sentry is configured): the stack trace, first-seen
   time, the release it started in, event and user counts. Read the error before forming a theory.
2. **Logs and metrics around that timestamp.** Read what happened *before* the error line. Before
   trusting "no logs", check ingestion is alive (event count per few hours over the last day); a
   cliff to zero is a pipeline outage to escalate, not a quiet service. Metrics answer whether it is
   one request or the whole system: error rate, latency, restarts, saturation. If a metric moved at
   a specific minute, find what else changed then.
3. **Reproduce** in local/dev with the input from the event, or say it was not reproduced.
4. **Know the wall.** Telemetry cannot show which version is running, why a pod restarts or is
   OOMKilled, or what config the cluster actually holds. When the evidence points there, stop and
   hand over the error issue, log window, moved metric and the exact question to someone with
   cluster access.

Team specifics (datasource IDs, hosts, query recipes): read `private/team-debug.md` when present.

## Reach for the right tool

Text search finds strings, not call sites — `ast-grep` for structural matches. `gron` makes JSON
greppable. `websocat` tests a WebSocket without writing a script. `hyperfine` for command-level
timing. Whatever observability stack the project actually uses (metrics, error tracking, issue
tracker) beats re-deriving the same facts from logs by hand — check what's configured before
falling back to raw log-diving.

Reach for the CLI before writing a script. `gron` makes JSON greppable; `ast-grep` makes code
structurally searchable; `websocat` tests a WebSocket without a Python harness.
