# Architecture judgment playbook

Use for system design, architectural critique, technology choices, code organization, infrastructure decisions, and full-stack AI systems. Choose relevant lenses, not every item.

## Decision order

1. **Domain and behavior:** What must remain true? Who owns the decision and data? Which states and transitions exist? What is explicitly out of scope?
2. **Constraints and distributions:** User and tenant counts, peak/burst, request classes, size distributions, latency/SLO, compliance, locality, budget, deploy frequency, engineers on call. Average alone is misleading.
3. **Logical boundaries:** Bounded contexts, contracts, invariants, data authority, control plane, data plane, tenancy, trust and blast-radius boundaries.
4. **Execution path:** Which pieces run synchronously? Which need durable async work? Where are CPU, network, DB, storage, queue, GPU, and human approval costs?
5. **Failure semantics:** What happens if any step fails *after* an earlier step committed? Cancellation, duplicate delivery, stale readers, version skew, permission changes.
6. **Evolution path:** What will likely change, and what is expensive to reverse? What can we defer until measured?

## Architectural choices: default biases and escape conditions

| Choice | Good starting point | Escalate when | Costs / traps |
| --- | --- | --- | --- |
| In-process function / modular monolith | Same team, shared deploy, moderate scale | Independent scaling/deploy/ownership or distinct reliability domains are proven needs | Code coupling requires boundaries; splitting too early introduces network failure and ops overhead |
| Synchronous RPC / HTTP | Caller needs immediate answer, modest dependency chain | Long tasks, fan-out, variable latency or independent consumers | Timeouts, cascading failures, partial work, tight availability coupling |
| Durable queue / jobs | Work can complete later with explicit job lifecycle | Need replayable event streams, multiple consumers, large ordered logs | Queue is a buffer, not added compute; must define ACK, dedupe, retention, DLQ, fairness |
| Events | A completed business fact has legitimate independent subscribers | Consumer projections, audits, decoupled workflows | Delivery duplicates/order, eventual consistency, version contracts, outbox |
| CQRS | Read/write needs differ materially | Read models cannot meet constraints with normal indexing/caches | Duplicated models, data freshness, projection recovery |
| Event sourcing | History-as-truth and replay are domain requirements | Auditable transitions demand replay semantics | Migration, schema evolution, replay, operational burden |
| Dedicated service/microservice | Clear bounded context + team/on-call ownership | Need independent safety, scaling or deploy cadence | Distributed transactions, observability, contracts, duplicated infra |
| Cache | Safe staleness window and hot read demand | Measured backend bottleneck | Invalidations, stampedes, cache key tenancy/permissions, stale policy |
| Database replica/shard | Read scale/locality/capacity demonstrably constrained | Primary cannot meet SLO with simpler tuning | Consistency lag, migration, query routing, failover and dual writes |
| Canary + flags | Observable progressive production change | Sensitive/irreversible data changes require additional migration gates | Feature flags are not a substitute for schema compatibility or rollback planning |

Never conflate event-driven programming, an event-driven architecture, and event sourcing. Kafka is a technology, not an architectural requirement. CQRS does not require event sourcing; async does not guarantee non-blocking execution.

## Programming and module design

- Prefer high cohesion, low coupling, stable domain vocabulary, narrow interfaces, and explicit ownership/lifetime.
- Apply dependency injection and ports/adapters when protecting a meaningful volatile boundary (DB, provider, clock, external gateway) or enabling test isolation. Do not generate interfaces for everything reflexively.
- Evaluate SOLID, composition, functional core / imperative shell, state machines, and dependency inversion as reasoning tools rather than certification badges.
- Distinguish domain state, orchestration, presentation, adapter, and persistence. Never hide a multi-step state mutation behind a deceptively pure function.
- State assumptions for cache lifetime, transaction scope, resource cleanup, mutable shared state, thread/async safety, and request isolation.
- Review schema evolution with mixed-version clients and servers. Prefer expand -> migrate/backfill -> contract where zero-downtime compatibility is required.
- Reject abstraction if it does not reduce total lifetime complexity or protect a real boundary. A small direct implementation can be the best engineering choice.
- Deep modules: judge a module by how much behaviour sits behind how little interface. Deletion test: if deleting it makes complexity reappear across callers, it earned its place; if complexity vanishes, it was a pass-through. One adapter is a hypothetical seam, two is a real one. ([module design](../modules/module-design/MODULE.md) has the full vocabulary.)
- Hyrum's law: with enough users every observable behaviour is depended on. In schema and API changes, review timing, ordering, defaults and error text, not only the documented fields.

## Distributed/data correctness probes

- For operations involving multiple writes, name the invariant, transaction boundary, allowed isolation anomalies, ordering, deduplication, and recovery semantics.
- For idempotency: choose a logical operation key scoped by tenant and operation; protect concurrent first writes atomically; define payload fingerprint, in-progress response, result replay, key lifetime, failure behavior. Separate 'effect once' from 'execution once'.
- For DB + event publishing: recognize dual-write; consider transactional outbox with consumer dedupe. Do not claim 'exactly once' across arbitrary external side effects.
- For retries: account for transient vs persistent error, status/Retry-After, absolute deadline, retry amplification, backoff/jitter, load shedding, and ambiguous prior success.
- For locks/leases: consider expiry, fencing, races, orphaned tasks. For business workflows across services, evaluate compensation versus stronger transaction boundaries.
- For long work: explicitly model PENDING / RUNNING / SUCCEEDED / FAILED / CANCELLED, claim/lease semantics, heartbeats, retry count, poison work, and orphan reconciliation.
- Authenticated != authorized. Model object/tenant/field/tool-level access on workers, caches, search/vector retrieval and object storage, not just API middleware.

## Trace all the way to physical execution

The following are *dimensions and subsystems*, not a strictly ordered stack:

| Subsystem | Key resource or contract | Diagnostic traps |
| --- | --- | --- |
| API / reverse proxy | Admission, headers, TLS, deadlines, routing | HTTP 200 can hide semantically wrong results; 202 does not mean job completed |
| Application runtime | Event loop, threads/processes, GC, blocking I/O | `async def` with sync blocking calls; long CPU work in event loop |
| CPU / OS | Scheduling, caches, context switches, page faults | CPU percentages hide throttling, contention, and per-core hotspots |
| RAM | Object heap, page cache, pools, fragmentation | Memory growth may be cache, retained objects or leak; resident != allocated |
| DB / WAL / indexes | Transactions, MVCC, locks, query plans, connections | More replicas/pods can exhaust DB connections; transaction isolation matters |
| Disk / object store | IOPS, bandwidth, durability, checksums, decode | Fast GPU can idle behind storage or preprocessing |
| Network | RTT, DNS, TCP/TLS, throughput, retries, packet loss | 'Intra-cluster' is still a partial-failure boundary |
| Queue / stream | Delivery, offsets/ACK, ordering, backlog and oldest age | Backlog can grow when arrivals exceed service rate |
| GPU / VRAM | Model weights, activations, KV cache, kernels, bandwidth | GPU utilization is not end-to-end throughput or saturation proof |
| Model server (e.g. vLLM) | Prefill/decode, batching, scheduler, KV policy, token budgets | CCU without input/output token distributions is misleading |
| Deployment / control plane | Desired state, orchestration, rollout, reconciliation | Container scheduler does not automatically optimize model-serving internals |

For inference, consider TTFT, TPOT/inter-token latency, end-to-end response latency, input/output token distributions, request concurrency, batching, model size, quantization, memory footprint, cold starts, and failure recovery. For speech, also audio length, sample rate, stream vs batch, silence/noise, ASR/TTS/diarization-specific error measures and real-time factor where applicable.

## Architecture review questions worth asking

- What is the highest-cost invariant violation? Can it occur during partial failure even when every unit test passes?
- Is a new distributed boundary solving a demonstrated scaling/ownership problem, or shifting in-process complexity into the network?
- If we add 10x API replicas, which shared resources become the bottleneck or new failure amplifier?
- If a tenant changes permissions after enqueue but before execution, which authorization policy applies?
- Is our schema or event change backward/forward compatible during rolling deployment and rollback?
- Which dependency has the weakest SLA, and how does that flow into our actual SLO?
- What is the smallest reversible experiment to separate the leading architectures?

## Recommendation shape

Specify (1) design and boundary, (2) correctness guarantees and what is *not* guaranteed, (3) proof needed to hit SLO/workload, (4) failure-handling and observability, (5) rollout/migration/rollback, (6) complexity cost and triggers to evolve the architecture.
