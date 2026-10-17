# API and event standards

## HTTP and RPC contracts

- Design resources and operations around domain semantics. Keep transport models separate from persistence models when coupling would expose internal change.
- Validate syntax, shape, size, authorization, and domain invariants at the boundary. Return stable machine-readable errors without internal secrets.
- Use HTTP method safety/idempotency and status semantics as specified; do not invent retry behavior from intuition.
- Use idempotency keys or an equivalent durable request identity for retriable side effects.
- Pagination needs deterministic ordering, bounded page size, and cursor/offset semantics that remain valid under concurrent changes.
- Define deadlines, cancellation, rate/size limits, partial success, and async job status explicitly.
- Evolve compatibly: prefer additive optional fields; define unknown-field behavior; version only when compatibility cannot be preserved.
- Keep OpenAPI/protobuf/schema definitions at the repository's source of truth and verify generated clients/servers through the owned workflow.

Primary references: [RFC 9110 HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110), [RFC 9457 Problem Details](https://www.rfc-editor.org/rfc/rfc9457.html), and [OpenAPI Specification](https://spec.openapis.org/oas/latest.html).

## Events, queues, and webhooks

- State whether delivery is at-most-once, at-least-once, or effectively-once at a defined boundary. “Exactly once” needs the boundary and mechanism.
- Give every event stable `id`, `type`, `source`, schema/version, event time, subject/key, and trace/correlation context where applicable.
- Producers publish facts that happened; commands request work. Name them accordingly.
- Consumers must define duplicate, late, out-of-order, unknown-version, and poison-message behavior.
- Make handlers idempotent with an atomic business write/deduplication record, inbox/outbox, or a domain-specific invariant where needed.
- Ordering is scoped to a partition/key and retained only as long as the broker and consumer contract guarantee it.
- Bound retries and send terminal failures to an owned recovery path. A dead-letter queue without an owner, alert, replay procedure, and retention policy is storage for ignored failures.
- Schemas evolve additively when possible. Test producer/consumer compatibility across deployed versions.
- Secure webhooks with authenticated signatures, replay protection, timestamp tolerance, key rotation, and bounded payloads; acknowledge only after the contract's durability point.

Use [CloudEvents](https://cloudevents.io/) when a portable event envelope is useful; do not add it solely to rename an existing stable contract.

## Contract review

Trace at least one success, validation failure, authorization failure, timeout, dependency failure, duplicate, retry, and partial-success path. Review the producer and every known consumer; label consumers outside the repository as unverified.
