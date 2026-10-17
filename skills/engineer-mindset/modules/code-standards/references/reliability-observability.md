# Reliability and observability standards

## Errors and cleanup

- Classify failures as caller error, domain rejection, transient dependency failure, permanent dependency failure, cancellation/deadline, overload, or programmer invariant failure.
- Catch only to recover, translate at a boundary, add actionable context while preserving the cause, or release resources.
- Never use a broad catch to return success, continue with corrupted state, or hide cancellation/system-exit signals.
- Use language-native resource management: context managers, `defer`, RAII, `using`, `try/finally`, or structured task scopes.
- Log an error once at the layer that owns the decision or request. Lower layers return rich errors; higher layers map them to the external contract.

## Deadlines, cancellation, and retries

- Start with an end-to-end deadline based on the caller/user budget. Allocate smaller downstream budgets and reserve time to return a result or compensate.
- Propagate cancellation through network, database, queue, and task boundaries. Cleanup must be safe if completion races with cancellation.
- Give every external call an explicit timeout unless the surrounding deadline is guaranteed and enforced by the library.
- Retry only transient failures. Require idempotency or a deduplication key for side effects.
- Use bounded exponential backoff with jitter, a max attempt/time budget, and retry-after/server hints. Never multiply retries independently across every layer.
- Circuit breakers and hedging need measured failure or tail-latency evidence; they add state, traffic, and new failure modes.

Guidance: [gRPC deadlines](https://grpc.io/docs/guides/deadlines/) and [gRPC retry](https://grpc.io/docs/guides/retry/).

## Capacity and overload

- Bound queue length, concurrency, message/payload size, batch size, memory, connections, and work per request.
- Apply admission control before scarce work. Use backpressure where upstream can slow down; shed or degrade when it cannot.
- Set ownership and shutdown behavior for background tasks. Drain or persist accepted work according to the contract.
- Prevent thundering herds with jitter, single-flight/deduplication, cache expiry spread, and bounded recovery concurrency when evidence warrants it.

## Logs, metrics, and traces

- Prefer structured events with stable names and fields: timestamp, severity, service/component, operation, outcome, correlation/trace ID, and safe domain identifiers.
- Never log secrets, credentials, raw tokens, private keys, or unnecessary sensitive payloads. Define redaction at the source.
- Keep high-cardinality values out of metric labels. Use traces or bounded logs for request/user/entity IDs.
- Metrics answer “how many/how long/how full”; logs explain discrete decisions; traces show causality across boundaries.
- Instrument user-visible success, traffic, latency, errors, saturation, queue age, dropped/retried work, and domain correctness.
- Preserve correlation across HTTP/RPC/events using established conventions rather than custom headers where possible.

Use [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/general/) for current field names and units.

## Alerts

- Page only for urgent, actionable conditions that need a human now. Tie pages to user impact, SLO burn, data integrity, or imminent exhaustion.
- Every page needs an owner, severity, dedup/grouping, runbook or direct diagnostic path, and a condition for resolution.
- Avoid alerting on causes when a higher-level symptom already captures impact, unless the cause requires a distinct action.
- Put capacity trends, chronic toil, weak signals, and non-urgent anomalies into dashboards or tickets.
- Validate alerts with known failure or replay data; a syntactically valid rule is not proof it fires usefully.

Reference: [Google SRE monitoring distributed systems](https://sre.google/sre-book/monitoring-distributed-systems/).
