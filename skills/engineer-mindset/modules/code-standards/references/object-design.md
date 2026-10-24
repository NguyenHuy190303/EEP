# Object design

Classes, objects and their relationships, judged by one test: the next change lands in one place.
Terms follow [module design](../../module-design/references/vocabulary.md): module, interface, seam,
adapter. The repository's existing object style wins over this file.

## When a class earns its keep

- A class **owns an invariant and the state it protects**: an `Order` that cannot be paid twice, a
  `RateLimiter` whose window and count change together. Callers change that state only through
  methods that keep the invariant true.
- Otherwise write functions over plain data: a frozen dataclass, record, struct or typed object.
  A class with no state, or only getters and setters, is a namespace or a bag; make it a module of
  functions or a value type.
- A **value object** (money with currency, a time range, a validated ID) is immutable, compares by
  value and is valid from construction. Use one wherever a primitive needs a unit or a rule.
- An **entity** has identity and lifecycle; keep its transitions as named methods (`approve()`,
  `cancel(reason)`), each checking the current state.

## Responsibility and collaboration

- **One reason to change** per class, named in domain words. `InvoiceService`, `Manager`, `Helper`
  and `Processor` usually name a pile; split by the decision each part owns.
- **Tell, don't ask.** Callers ask the object to act (`account.withdraw(amount)`) rather than read
  its fields, decide and write them back. Logic that reads another object's fields more than its own
  belongs in that object (feature envy).
- **Talk to direct collaborators.** A chain like `order.customer.address.city` couples the caller to
  three structures; expose the fact the caller needs (`order.shipping_city()`).
- **Constructors are cheap and leave the object valid.** No I/O, no network, no hidden globals.
  Expensive or fallible creation goes in a named factory (`Client.connect(config)`), so tests can
  build the object directly.
- **Inject a dependency at a real boundary** (clock, network, storage, third party), as
  [testability](../../module-design/references/testability.md) shows. Construct in-process
  collaborators directly; a container or DI framework is used only where the repository already has
  one.

## Composition, inheritance and polymorphism

- **Compose by default.** Hold a collaborator and delegate to it. Add behaviour by wrapping
  (decorator) or by passing a strategy, which keeps each piece testable alone.
- **Inherit only for a true is-a** where every subtype can stand in for the parent without the caller
  checking which one it got. Keep hierarchies one level deep below an abstract base; code reuse alone
  is a reason to compose.
- **Polymorphism replaces a type switch** when two or more real variants exist and new ones keep
  arriving (payment providers, export formats). For a closed, small set, a discriminated union or
  enum with an exhaustive match keeps every case visible in one place; this is the
  two-adapters rule from module design applied to types.
- **Abstract interfaces need two implementations today**, typically production plus a test fake at an
  external boundary. With one implementation, depend on the concrete class and extract the interface
  when the second one appears.

## Open sets: one registry

When variants keep arriving (metrics, score types, export formats, report columns), define each
variant once as a value object that carries everything any consumer needs: identity, label, unit,
direction (higher or lower is better), aggregation rule and the compute function. Compute, storage,
API and UI all iterate that registry; none of them lists a variant by name.

- **The registry is the single source of truth across layers.** Publish its descriptors with the
  data (a `metrics.json` beside the results, or descriptors in the API response) so a consumer in
  another language reads them instead of copying them.
- **Carry the aggregation rule.** A ratio metric stores numerator and denominator per row and
  aggregates as `sum(errors) / sum(total)`; a mean of per-row ratios over-weights short items (WER
  over utterances, DER over recordings). Metrics with no such pair declare their aggregate (`mean`,
  `p95`) explicitly.
- **Store and load the measurements by the data rules** in [stacks](stacks.md#mobile-data-and-ml):
  long form so a new metric adds rows, and the source dataset read in place at a pinned revision
  rather than copied to disk.
- **New variants compute incrementally**: adding one computes only that variant over existing runs
  ([incremental compute](caching-and-resources.md#incremental-compute)).
- **Consumers tolerate unknown and missing variants**: an unknown unit falls back to a plain number,
  an older run without the new metric shows a placeholder.
- **Done when** adding one variant is one registry entry plus a rerun, and a grep for its name finds
  only the registry, its compute function and its tests.

Example: `METRICS = [Metric("wer", "WER", "ratio", lower_is_better=True, count=wer_counts), ...]`;
adding KER is one more `Metric(...)` line, and the table gains a KER column with no frontend edit.

## Python specifics

- `@dataclass(frozen=True)` for value objects (add `slots=True` on Python 3.10+); `enum.Enum`/
  `Literal` plus `match` for closed variants.
- `typing.Protocol` at a real seam, so adapters need no shared base; `abc.ABC` when two or more
  substitutable subclasses must honour one enforced contract. Shared helper code goes into a composed
  collaborator.
- Module-level functions are the default unit; a class appears when state and invariant appear.
  Use `@property` for derived values, and keep setters off value objects.

## Smells and the smallest fix

Report these at the maintainability priority in the module's review order, each with the change
that it makes expensive.

| Smell | Evidence | Smallest in-scope fix |
|---|---|---|
| God class | One class changes in most unrelated PRs; many fields used by disjoint method groups | Extract the method group with its fields into a collaborator |
| Feature envy | A method mostly reads another object's data | Move the method to the data's owner |
| Shotgun surgery | One rule change edits many classes | Gather the rule into one owner |
| Anemic model + service | Entities are field bags; services enforce their rules | Move each rule into the entity it guards |
| Deep or base-class-for-reuse hierarchy | Subclasses override to undo parent behaviour | Replace with composition or a strategy |
| Speculative interface | One implementation, no test fake | Inline the interface into the concrete class |

Refactor only the part the current task touches; name larger structural debt in the report instead
of fixing it in the same diff.
