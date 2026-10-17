# Stack-specific standards

Load only the sections present in the repository. Existing project configuration and current official documentation win.

## Python

- Follow configured Ruff/Black/style settings; otherwise use [PEP 8](https://peps.python.org/pep-0008/) as baseline.
- Use context managers for resources, narrow exceptions, exception chaining, explicit timezone-aware time, and immutable/value-oriented domain types where useful.
- In async code, keep blocking I/O off the event loop, propagate cancellation, bound task fan-out, and use task groups/timeout contexts supported by the project's Python version.
- Use vectorization only when it improves a measured data workload; clear loops are correct for orchestration and small collections.

## TypeScript and JavaScript

- Use the repository's formatter/linter and the strictest TypeScript options it already supports. Validate data crossing runtime boundaries; static types do not validate JSON.
- Prefer discriminated unions for state, `unknown` before validation, immutable transformations where clear, and explicit ownership of shared state.
- Propagate `AbortSignal`/deadlines, avoid blocking the event loop, handle rejected promises once, and bound concurrent promises.
- In frontend code, preserve semantic HTML, keyboard access, focus, accessible names, server/client boundaries, and one owner for state.

Reference: [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html).

## Go

- Follow `gofmt`, [Effective Go](https://go.dev/doc/effective_go), and the project's lint policy.
- Pass `context.Context` at request boundaries; do not store it in structs. Propagate cancellation and deadlines.
- Wrap errors with context and preserve identity for `errors.Is/As`. Do not log and return the same error at every layer.
- Make goroutine ownership, shutdown, channel close responsibility, and concurrency bounds explicit. Avoid a goroutine per unbounded item.

## Rust

- Follow `rustfmt`, project Clippy policy, and the [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/).
- Model invalid states out with enums/newtypes. Use `Result`/`?`, preserve sources, and reserve panic for broken invariants or unrecoverable startup conditions defined by the application.
- Keep ownership and lifetimes simple at public APIs. Minimize and document each `unsafe` block's invariant; audit FFI boundaries.
- In async code, avoid blocking executors, bound spawned tasks/channels, and reason about cancellation safety and dropped futures.

## Java and Kotlin

- Use repository format/checkstyle and established framework patterns. Prefer explicit domain types, immutable data, and constructor injection at real boundaries.
- Use checked/unchecked exceptions consistently with the codebase; preserve causes and translate only at contract boundaries.
- Propagate deadlines/cancellation through futures, coroutines, clients, and database calls. Bound executors and queues.
- For Kotlin, use structured coroutines and sealed types; do not mix blocking work into coroutine dispatchers without an explicit dispatcher.

References: [Google Java Style](https://google.github.io/styleguide/javaguide.html) and [Kotlin coding conventions](https://kotlinlang.org/docs/coding-conventions.html).

## C# and .NET

- Follow the repository formatter/analyzers and [.NET coding conventions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions).
- Keep async paths async; avoid sync-over-async. Propagate `CancellationToken` and set operation budgets.
- Dispose owned resources with `using`/`await using`; do not create a new `HttpClient` per request when the application provides a factory or long-lived client.
- Use nullable reference analysis and result/domain types where they clarify expected failures; preserve exception causes for unexpected failures.

## C and C++

- Follow the project's compiler warnings, formatter, sanitizers, and [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines).
- Prefer RAII, value semantics, bounds-aware views, smart pointers for ownership, and no owning raw pointers in C++.
- Make allocation, lifetime, aliasing, overflow, integer conversion, ABI, and thread ownership explicit. Check every external length and return value.
- Use exceptions or status/results consistently with the codebase; never allow exceptions across C/FFI boundaries.

## SQL and persistence

- Put integrity in schema constraints when the database can enforce it. Define transaction boundaries around business invariants.
- Parameterize values. Review query plans and realistic cardinality before adding indexes; account for write amplification and lock/migration cost.
- Avoid unbounded reads and N+1 access. Make ordering explicit for pagination and deterministic jobs.
- Treat migrations as deployment code: compatible rollout, lock/time estimate, backfill, validation, rollback/forward-fix, and backup/restore evidence.

## Shell, CI, and infrastructure

- Use the repository's shell and ShellCheck policy. Quote expansions, use arrays for argument lists, avoid parsing `ls`, handle temp files and cleanup, and do not expose secrets in argv or logs.
- `set -e` is not complete error handling; understand pipelines, conditionals, traps, and the exact shell in CI.
- Keep CI and infrastructure declarative, least-privileged, pinned where supply-chain risk matters, and idempotent. Preview plans and target named resources; avoid destructive all-target commands.
- Keep environment-specific values in the owning configuration system and verify generated/rendered output before apply.

## Mobile, data, and ML

- Mobile work must respect lifecycle, offline state, permissions, battery/network constraints, cancellation, background limits, accessibility, and store-release compatibility.
- Data pipelines need schema/data quality checks, lineage, replay/backfill, partition strategy, late-data policy, idempotency, and cost per run.
- ML code needs reproducible data/model versions, leakage checks, representative evaluation, deterministic seeds where possible, hardware/runtime budgets, monitoring for drift and failure, and a non-model fallback where the product requires it.
