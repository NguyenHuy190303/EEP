# Core code standards

Apply these with the language's own idioms and the repository's established conventions.

## Structure and ownership

- Organize by domain/capability when behavior changes together; organize technical adapters around a clear boundary.
- Keep dependency direction visible. Domain logic should not import transport, UI, or persistence details unless the existing architecture deliberately combines them.
- Avoid one-implementation interfaces, pass-through layers, generic managers, and extension points without a current caller.
- Keep configuration in its owning source. Do not duplicate mutable values in code, docs, tests, and deployment files.
- Make generated code recognizable and regenerate it through the repository-owned command.

## Functions and logic

- Give a function one coherent responsibility, not an arbitrary line limit.
- Prefer explicit inputs and outputs over hidden global state. Make time, randomness, network, filesystem, and environment dependencies controllable where testing or determinism matters.
- Use guard clauses for invalid and terminal cases. Keep the happy path visible.
- Represent valid states directly with types, enums, tagged/discriminated unions, value objects, or database constraints when the language and project support them.
- Avoid boolean parameters when callers cannot tell what `true` means or when combinations become invalid states.
- Do not catch an error unless the layer can recover, translate it into its contract, add useful context, or guarantee cleanup.

## Algorithms and data structures

- State the input bound and dominant complexity before optimizing. Include memory, allocation, I/O, serialization, and contention where they dominate CPU complexity.
- Choose structures for the operations performed: set/map for membership, queue/deque for ends, heap for top-k, indexed database query for persistent lookup.
- Avoid nested scans over unbounded input. For bounded tiny collections, clear `O(n²)` code can be cheaper than extra machinery.
- Prefer a single clear pass when it reduces work and remains readable. Do not compress control flow into clever chains that hide early termination or error handling.
- Benchmark representative data and release-mode code before claiming a performance win. Report environment and variance.
- Watch numeric overflow, precision, units, Unicode, time zones, clock source, empty input, duplicates, and adversarial input.

## Loops and collections

- Choose a loop when order, early exit, mutation, error handling, backpressure, or resource lifetime matters.
- Choose map/filter/fold style when the transformation is pure, bounded, and clearer in that language.
- Do not allocate intermediate collections in a hot or unbounded path without evidence they are acceptable.
- Never mutate a collection while iterating unless the language/API explicitly defines the behavior.
- Bound polling and retry loops; include cancellation, deadline, and backoff. No silent infinite loops.
- In async code, avoid unbounded fan-out and accidental sequential awaits. State the concurrency limit and ordering semantics.

## State and concurrency

- Minimize shared mutable state. Give each resource and task a clear owner and lifetime.
- State thread/async safety at public boundaries. Use the runtime's structured-concurrency and cancellation model where available.
- Protect the invariant, not individual fields. Keep critical sections small and never hold a lock across blocking/network work unless the design proves it safe.
- Plan for races between timeout, cancellation, retry, shutdown, and completion.

## Tests

- Test contracts, invariants, boundaries, and previously failing behavior. Avoid tests that restate implementation line by line.
- Prefer deterministic fakes at owned boundaries and a small number of real integration tests for contracts that mocks cannot prove.
- Use property-based tests when a real invariant spans a broad input domain; example tests are better when no meaningful property exists.
- A test proves only the inputs, environment, and boundary it exercised. Do not present a unit test as runtime or production evidence.
