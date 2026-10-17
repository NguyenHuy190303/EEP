# Code standards

Repository instructions, existing architecture, formatters, linters, build tools, and public contracts are the source of truth. Do not introduce a formatter, dependency, layer, exception policy, or language-wide rewrite merely to match this guide.

## Establish context

1. Identify every language, runtime, framework, and generated-code boundary in scope from manifests and source files.
2. Read the relevant implementation, callers, tests, configuration, and configured checks.
3. Distinguish an existing local convention from a defect that threatens correctness, security, operability, or a public contract.
4. Preserve user changes and generated outputs. Change the smallest shared point that fixes the real issue.

Use [references/stacks.md](references/stacks.md) for stack-specific idioms and primary language guidance. Never translate a Python pattern mechanically into Go, Rust, TypeScript, Java/Kotlin, C#, C/C++, SQL, shell, mobile, frontend, data, or infrastructure code.

## Standards that cross languages

- Make names describe domain intent and units; keep one source of truth for thresholds and policies.
- Keep modules cohesive around ownership and change reasons. Avoid circular dependencies and generic `utils` dumping grounds.
- Prefer simple data flow and early exits. Remove accidental nesting before adding abstractions.
- Validate untrusted input at the boundary; preserve typed/domain invariants internally.
- Keep side effects explicit. Separate pure calculation from I/O when it makes behavior easier to verify.
- Comments explain a non-obvious reason or constraint, not the syntax.
- Use standard-library and existing-project features before a new dependency.

Read [references/core.md](references/core.md) for functions, modules, logic, algorithms, loops, concurrency, and tests.

## Distributed and operational behavior

For network, queue, async, background, or production-facing code, inspect the whole call budget and failure path. A local `try/catch` is not a reliability design.

- Bound external work with a deadline or cancellation signal that propagates.
- Retry only classified transient failures when the operation is safe or idempotent.
- Preserve error causes and context; do not swallow failures or log the same failure at every layer.
- Bound queues, concurrency, memory, payloads, and cardinality. Define overload behavior.
- Emit structured telemetry that helps answer what failed, where, for whom, and with which correlation ID without leaking secrets.
- Alert on urgent, actionable user impact or SLO burn; use dashboards and tickets for slower signals.

Read [references/reliability-observability.md](references/reliability-observability.md) when code touches errors, `try/catch`, deadlines, retries, cancellation, logs, metrics, traces, alerts, concurrency, or backpressure.

## APIs and events

Read [references/api-events.md](references/api-events.md) when changing an HTTP/RPC contract, public schema, webhook, event, queue consumer, or versioning policy. Check compatibility, validation, idempotency, ordering, deduplication, and partial failure across producer and consumer boundaries.

## Review output

Report only actionable findings tied to evidence. Order by correctness/security/data loss, public-contract regression, reliability/operability, performance with measured impact, then maintainability.

For each finding give location, trigger, consequence, and the smallest credible fix. Label unmeasured performance claims and external consumers as unverified. Avoid style findings already handled by configured tools unless the tool cannot express the rule.

After a change, run the narrowest configured check that exercises the behavior, inspect the diff, and state exactly what remains unverified.
