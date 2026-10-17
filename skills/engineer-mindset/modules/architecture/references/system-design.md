# System design checks

Load the sections that match the decision. Repository-specific invariants win.

## Boundaries and demand

- Draw components around ownership and failure boundaries, not fashionable layers.
- Record request/event path, protocol, payload shape, authentication, validation, persistence, and ownership at every boundary.
- Quantify average and peak load, payload and dataset size, growth, burst shape, fan-out, latency budget, and concurrency.
- State availability, durability, RTO, RPO, retention, residency, and consistency needs. Avoid “high scale” without a number.

## Data

- Give each fact one source of truth and an owner.
- Choose schema and storage from access patterns, lifecycle, correctness, and recovery needs.
- State transaction boundaries and invariants before splitting data across services.
- Plan compatible schema evolution, backfill, validation, deletion, backup, restore, and audit.
- Treat caches, search indexes, warehouses, and vector stores as derived data unless explicitly authoritative.

## APIs and events

- Make contracts explicit and evolvable. Prefer additive changes and tolerant readers.
- Budget end-to-end deadlines; each downstream call gets less than the caller's remaining budget.
- Retry only transient, safe or idempotent operations with bounded exponential backoff and jitter.
- Give event handlers deduplication, idempotency, ordering assumptions, poison-message handling, and replay policy.
- Isolate non-critical side effects from critical-path success. Define partial-success and compensation behavior.

Primary standards: [HTTP Semantics RFC 9110](https://www.rfc-editor.org/rfc/rfc9110), [Problem Details RFC 9457](https://www.rfc-editor.org/rfc/rfc9457), [OpenAPI](https://spec.openapis.org/oas/latest.html), [CloudEvents](https://cloudevents.io/), [gRPC deadlines](https://grpc.io/docs/guides/deadlines/), and [gRPC retries](https://grpc.io/docs/guides/retry/).

## Reliability and security

- Enumerate dependency, process, host, zone, region, quota, credential, and human failure modes.
- Define overload behavior: admission control, queue bounds, backpressure, shedding, degradation, and recovery.
- Make retry storms, thundering herds, split brain, clock skew, duplicate delivery, and stale reads explicit where plausible.
- Map trust boundaries, least privilege, secret lifecycle, tenant isolation, abuse paths, audit needs, and sensitive data exposure.
- Prefer a tested recovery path over redundant components whose failover is unowned.

## Operations and observability

- Assign ownership, on-call capability, support path, SLO, capacity limit, runbook, and upgrade cadence.
- Instrument user-visible success, latency, traffic, errors, and saturation. Add domain correctness signals where infrastructure health can be green while the product is wrong.
- Use structured logs, metrics, and traces with stable correlation; control cardinality and never emit secrets.
- Alert on urgent, actionable symptoms tied to user impact or SLO burn. Dashboards can carry diagnostic detail.

References: [Google SRE monitoring](https://sre.google/sre-book/monitoring-distributed-systems/) and [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/general/).

## Migration

Prefer an incremental sequence: establish compatibility → observe old behavior → shadow or backfill → canary → shift traffic/data → verify → remove fallback → decommission. Every stage needs entry criteria, success metrics, abort condition, rollback path, and owner.

Include dual-run and cleanup cost. A migration is incomplete while the old system, bridge, or duplicate source of truth remains operational.

Use architecture fitness functions only for properties that tooling can verify repeatedly: dependency direction, schema compatibility, latency/error budget, forbidden data flow, or deployment constraints. Keep judgment-heavy qualities in review, not brittle tests.
