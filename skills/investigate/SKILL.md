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
output. Anything you concluded rather than observed is labelled as inference. Paste errors verbatim.

**Separate root cause from contributing condition from symptom.** Naming a contributing condition as
the root cause is the most common way an investigation ends early and the bug comes back.

**Close with what is open.** What is now established, what is still UNCHECKED, and specifically what
observation would close each open item. A green local test suite proves the code does not
contradict itself; it does not prove a claim about the running system in production — that needs
an observation from that system.

**Report before fixing.** Fix during an investigation only when the fix is one line and obviously
correct, or you were asked to; a mid-investigation fix destroys the evidence for whether it was the
cause.

## Mode specifics

### root-cause
**Build a red loop before forming any theory.** The loop is one command (a failing test, a curl
against a dev server, a CLI call diffed against a fixture, a replayed captured payload, a
`git bisect run` script) that goes red on *this* bug. The step is done when you have run it, shown
the invocation and its real output, and it is:

- **red-capable:** it drives the real code path and asserts the user's exact symptom, so it turns
  green only when this bug is gone;
- **deterministic:** the same verdict every run;
- **tight:** seconds per run, with only the setup the bug needs;
- **agent-runnable:** it runs unattended. Where a person must act, script their part with
  [`scripts/hitl-loop.template.sh`](scripts/hitl-loop.template.sh) so the loop stays structured.

No red-capable command, no hypothesis. Then tighten it: cache setup and narrow the scope for speed,
assert the specific symptom rather than "did not crash", pin time, seed randomness and isolate
filesystem and network. For a flaky bug, raise the reproduction rate instead of chasing a clean
repro: loop the trigger 100×, parallelise, add load, narrow the timing window. A 50% bug is
debuggable; a 1% bug is not yet.

Once red, minimise: cut inputs, config, data and steps one at a time, re-running after each cut.
Done when removing any remaining element turns the loop green.

When no loop is possible (production-only, unsafe, no access, no way to run commands), say so, list
what you tried, and ask for access to an environment that reproduces it, a redacted captured
artifact (HAR, log dump, core dump), or permission for temporary instrumentation. Name the strongest
proxy you used instead (logs, a stack trace read against the code) and state that the cause was not
reproduced.

Work backwards from the observable to the first point where the invariant was already violated. That
point, not the crash site, is where the root cause lives.

Tag every temporary probe with one prefix per investigation, e.g. `[DEBUG-a4f2]`, and remove them
before reporting; `rg '\[DEBUG-a4f2\]'` returning nothing is the proof. Loop scripts and harnesses
live in a scratch location outside the repo's tracked files; the report lists any that remain, and a
failing test worth keeping is offered as the regression test rather than left behind. Show commands and output
with secrets replaced by `<REDACTED>`, and build the loop on environment variables so credentials
stay out of it.

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
3. **Build the loop** by replaying the event's input in local/dev, held to the root-cause gate above.
   When no loop can be built, say so and hand over as in step 4.
4. **Know the wall.** Telemetry cannot show which version is running, why a pod restarts or is
   OOMKilled, or what config the cluster actually holds. When the evidence points there, stop and
   hand over the error issue, log window, moved metric and the exact question to someone with
   cluster access.

Team specifics (datasource IDs, hosts, query recipes): read `private/team-debug.md` when present.

## Reach for the right tool

Reach for a CLI before writing a script: `gron` makes JSON greppable, `websocat` tests a WebSocket
(`ast-grep` and `hyperfine` are under impact and perf). Whatever
observability stack the project already runs (metrics, error tracking, issue tracker) answers faster
than re-deriving the same facts from raw logs; check what is configured first.
