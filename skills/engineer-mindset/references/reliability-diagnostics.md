# Reliability, performance, and incident diagnosis

Use for errors, degradation, overload, load tests, latency regressions, resource issues, capacity planning, SRE and resilience reviews. Diagnose; do not attribute root cause from one metric.

## Contents

- Incident reasoning sequence
- Production failure modes to intentionally consider
- Timeouts, retries and overload (checked against primary sources)
- SLOs and postmortems
- Correctness and failure semantics
- Quantitative reasoning (use carefully)
- Minimum useful observability
- Incident answer example shape

## Incident reasoning sequence

1. **Define symptom:** User impact, timeframe, affected slices/tenants/version, expected vs observed behavior, blast radius and severity; separate semantic failure from HTTP failure.
2. **Contain:** Prioritize reversible, safe steps: isolate bad release, rate-limit/load-shed, pause workers, disable feature, route to healthy fallback, restore data safety. Preserve evidence.
3. **Build competing hypotheses:** Favor discriminators rather than a laundry list. Rank with available evidence, not intuition alone.
4. **Select discriminating evidence:** Request/spans across boundaries, queue wait, arrival rate, success/error semantics, pool wait, CPU throttling, disk latency, GPU scheduler, recent changes.
5. **Test falsifiably:** For each hypothesis specify `if true -> expected signal`, `if false -> disconfirming signal`, smallest safe experiment.
6. **Identify mechanism:** Work through timeouts, retries, state, resource limits, config/version changes, load shape. Correlation with deployment suggests investigation; it is not automatic proof.
7. **Fix and validate:** Mitigation, durable fix, regression/fault-injection tests, canary/rollback, SLO recovery, postmortem without blame.

## Production failure modes to intentionally consider

| Symptom | Candidate mechanisms | Useful discriminator |
| --- | --- | --- |
| P99 grows, GPU util stays modest | Queueing, blocking event loop, scheduler fairness, CPU bottleneck, network, DB wait | Separate queue wait, scheduling delay, prefill/decode, API/DB spans |
| Connection exhaustion on autoscale | Per-worker pool multiplication, leaks, long transactions, pooler config | Sum connection budget across replicas and processes; connection hold/wait histogram |
| Client times out but work still completes | Timeout without cancellation; ambiguous commit | Durable job state, idempotency record, external side-effect audit |
| Duplicate charges/jobs | Retry/redelivery race, key scoping, lack of atomic dedupe | Events correlated by logical operation ID and transaction traces |
| Queue depth rising | Arrival > drain rate, hot partitions, slow downstream, retries | Queue oldest age, producer rate, consumer throughput, retries, utilization |
| Scale out makes latency worse | Shared DB, lock contention, connection budget, cache stampede | End-to-end spans, DB plans, pool saturation, dependency QPS |
| GPU OOM at load | Weights+KV cache, batch/token budget, fragmentation | Memory breakdown, max sequences/tokens, scheduling and actual shapes |
| AI benchmark improves but users complain | Dataset leakage, shift, critical-error regression, judge bias | Production slices, audit samples, golden regression, safety metrics |
| A component got faster, users wait the same | Time sits in queueing, tool calls or an external dependency, not the optimized part | End-to-end span breakdown on the user-facing path before choosing what to optimize |
| Bad canary appears 'healthy' | Wrong denominator, low traffic, missing semantic signals | Per-slice user-impact and quality SLI; exposure counts and confidence |

## Timeouts, retries and overload (checked against primary sources)

- **Timeout from the tail, not from habit.** Choose an acceptable false-timeout rate (say 0.1%) and
  set the timeout at the matching downstream percentile (p99.9). Cold starts, first requests and
  scale-from-zero wake-ups are part of that distribution: a 120 s caller timeout in front of a
  worker that takes 123 s to wake fails every first request (field case F2).
- **Retry at one layer.** Three retries at each of five layers is up to 3^5 = 243× the load on the
  bottom service. Cap retries with a local token bucket so a failing dependency gets less traffic,
  not more.
- **Backoff is not overload control.** Delaying requests helps only a bounded set of clients that
  send one after another. Independent callers keep the same arrival rate; against sustained
  overload only shedding or reducing work helps.
- **Metastable failure.** A system can stay down after the trigger is gone because the failure
  feeds itself (retries, cache misses, queue backlog). Fix the loop that sustains it, not only the
  trigger, and be wary of optimizations that help only the normal case.
- **Queues.** Measure message age from the first delivery attempt. Sideline stale or over-quota
  work to its own queue. Long work must respect the visibility timeout, or a second consumer picks
  up the same message and doubles the load.
- **Rollout.** Expand by cohorts (internal → low-risk → important customers), not by big percentage
  jumps; some failures appear only under full load. Let automated health checks decide promotion,
  and instrument a change before shipping it.

## SLOs and postmortems

- Set the SLO from what users need, not from current performance; that locks in heroics. Keep the
  internal target tighter than the published one, and do not run far more reliable than the SLO:
  users build on the reliability you actually deliver.
- The error budget governs launch pace: as it shrinks, slow launches gradually; failures outside
  your code (network, provider) spend it too.
- Agree postmortem triggers before incidents. A monitoring failure is itself a trigger. A
  postmortem that nobody reviewed has no effect; the review is part of it.

## Correctness and failure semantics

- Network timeouts do not tell whether the server committed. Cancellation of a future is not proof downstream work stopped.
- Define retries at one controlled layer where possible, with budget, overall deadline and idempotency; exponential backoff alone is not a solution to overload.
- Use bounded concurrency, admission control, queue limits, fairness and backpressure. Rate limit, concurrency limit, quota, and worker capacity are different dimensions.
- Plan graceful shutdown, draining, lease recovery, replay, poison-message isolation, outbox processing and multi-version compatibility.
- Treat database isolation and business invariants separately; transactions help only inside their guarantee boundary.
- For partial outages, specify which features safely degrade, which must fail closed, and what users see.

## Quantitative reasoning (use carefully)

- **Little's Law:** For a stable system with consistent boundaries and time units, average concurrency L = arrival/completion rate lambda * mean system time W. This is descriptive, not a proof of max CCU and not safe during unbounded backlog growth.
- **Utilization and tails:** High saturation and burstiness can cause p95/p99 to spike far earlier than the average would imply. Measure waiting and service time separately.
- **Offered, completed, goodput:** Offered load is what arrives; completed throughput is what
  finishes; goodput is what finishes correctly within the latency target. A service offered
  100 RPS that completes 40 RPS on time has 40 RPS of capacity. A few seconds at peak is not
  sustained capacity. CCU does not convert to RPM without the arrival pattern and service time,
  and MAU does not convert to capacity without a usage model.
- **Capacity:** Describe workload distribution (e.g. audio length, tokens, payload, background tasks), traffic arrival pattern, ramp and duration, warm/cold state, resource contention, success criteria, and sustained operating point. Do not infer capacity from GPU/CPU percentage alone. Report shape: `evidence-gates.md`, performance and capacity claims.
- **Load-test protocol:** Define open-loop vs closed-loop, coordinated omission risk, per-request timeouts, clients/generators saturation, warmup, run length, percentiles, sample size, error definitions, hardware/model version and contention. Report results at multiple load points including break point when safe.
- **Resource budget:** Compute per-process/worker connection and memory pools multiplied by replicas, plus system margin and shared-dependency capacity. Document units.
- **Cost:** Include provisioned capacity, data transfer, storage/retention, observability, engineering/on-call toil, p95/p99 experience, and cost per successful business outcome or per useful inference. Include the headroom reliability needs and the marginal cost of the next traffic increment. A cheaper resource metric that raises failures, toil or engineering time can raise total cost.
- **Uncertainty:** Describe confidence, sample count, confidence interval or variance when meaningful. No invented precision, no universal p95 target.

## Minimum useful observability

Track four golden signals: latency, traffic, errors, saturation. Connect metrics -> structured logs -> traces through a correlation scheme without exposing secrets or sensitive user content. Treat high-cardinality request IDs as trace/log attributes rather than indiscriminate metric labels. Define user-facing SLI separately from technical acceptance (e.g. 202 Accepted is not completed transcription). Measure business/semantic correctness alongside infrastructure health for AI systems.

Prefer a small set of diagnostic telemetry that can decisively locate a bottleneck:
- Request acceptance and completed business-operation throughput by tenant/workload/model/version.
- E2E latency and breakdown: admission wait, queue wait, DB, network, inference prefill/decode, postprocess.
- Failed vs abandoned vs timed-out vs cancelled vs later-completed logical operations.
- Resources: CPU throttle, RSS/page faults, pool checkout time, disk read/write latency, network time, GPU/VRAM occupancy, batching/tokens/s.
- Queue oldest age, retries, duplicate suppression, DLQ, reconcilers and number of stalled jobs.
- Release/feature-flag/version annotations and per-slice quality guardrails.

## Incident answer example shape

**Observed:** "At 80 concurrent clients p99 increases, but GPU telemetry is not high." This is an observation, not diagnosis.

**Hypotheses:** (1) worker/queue bottleneck; (2) blocking API loop; (3) prefill/decode scheduling inefficiency; (4) DB or storage wait. Rank only if observations support it.

**Discriminators:** Compare queue wait with inference spans; event-loop lag; active vs waiting jobs; CPU throttle; token distributions; GPU KV occupancy and scheduling wait; DB pool wait.

**Now:** Protect healthy traffic via admission limit and bounded queue, avoiding blanket retry storms. Do not advise unsafe production experiments without safeguards.

**Next:** Repeat a controlled reproducible run with identical workload and version, capture E2E breakdown; fix the verified bottleneck, then retest quality/latency/cost simultaneously.
