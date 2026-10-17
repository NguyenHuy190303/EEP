# Multi-stack architecture guide

Choose from evidence, not language preference. First check the repository's existing runtime, deployment, telemetry, security baseline, lockfiles, team ownership, and production history.

## Selection dimensions

Compare candidates on delivery speed, correctness model, latency/throughput, startup and memory, concurrency, ecosystem maturity, debugging, build and CI cost, security maintenance, deployment footprint, library/API compatibility, hiring, on-call familiarity, and exit cost.

Reject a benchmark that does not resemble the actual workload. A faster runtime rarely pays for a new operational ecosystem by itself.

| Stack | Strong fit | Costs to price |
|---|---|---|
| TypeScript/JavaScript | Browser/full-stack product work, Node I/O services, teams sharing types and tooling | Runtime type boundaries, event-loop blocking, dependency churn, memory and cold starts |
| Python | ML/data ecosystem, automation, scientific work, API services where delivery and libraries dominate | CPU throughput, packaging/native wheels, GIL/concurrency model, runtime validation and memory |
| Go | Network services, CLIs, platform agents, simple concurrency, static deployment | Less expressive domain modeling, GC/tail latency, repetitive error handling, ecosystem gaps |
| Rust | Systems, security-sensitive parsers, low latency, embedded/edge, high efficiency | Learning curve, compile time, unsafe/FFI review, smaller hiring pool and some library gaps |
| Java/Kotlin/JVM | Large domain services, mature enterprise/data ecosystems, long-lived high-throughput systems | Runtime tuning, startup/memory, framework complexity, build times and upgrade surface |
| C#/.NET | Enterprise services, Microsoft ecosystem, productive async services, cross-platform applications | Platform/library fit outside team norms, runtime footprint, upgrade and hiring context |
| C/C++ | Native libraries, embedded, hard real-time or hardware/ABI constraints | Memory safety, build portability, dependency management, specialist review and incident risk |
| Swift/Kotlin mobile | Native platform integration, offline/mobile lifecycle, device performance | Two client stacks, release-store latency, backward compatibility, device matrix |
| SQL + database-native features | Integrity, joins, filtering, aggregation, queues/locks suited to the chosen database | Vendor semantics, migration/locking, query-plan drift, operational coupling |
| Streaming/data platforms | Durable event history, high-volume pipelines, multiple asynchronous consumers | Ordering semantics, replay, schema governance, state, storage, on-call and cluster cost |
| Serverless/managed services | Spiky load, small team, fast delivery, low operations at modest scale | Quotas, cold starts, observability, unit-price slope, egress, local testing and lock-in |
| Containers/Kubernetes | Shared platform already operated, mixed workloads, scheduling/network policy needs | Platform team, upgrades, cluster capacity, security, debugging and control-plane toil |

## Polyglot gate

Add a language or platform only when a measured constraint cannot be met reasonably by an existing stack, or when a mature ecosystem removes more recurring work than the new stack creates. Name the component boundary, owner, build/deploy path, telemetry, security policy, upgrade path, and fallback before adoption.

For mixed systems, keep contracts language-neutral. Use schema/code generation only when the repository already owns the generator and its compatibility workflow.

Recheck current official language and framework guidance when the decision depends on a recent release. Do not encode “latest” versions in an architecture recommendation without verifying them.
