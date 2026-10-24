# Frontend structure

The same maintainability rules as [object design](object-design.md), expressed in the framework's own
idiom: components, hooks/composables, stores and services. React function components are not
classes; Angular services with DI are native there. The repository's framework, folder layout and
state library win. Visual and interaction design belongs to `impeccable`; this file covers how the
code is divided.

## Layers and dependency direction

Each layer depends only on the ones below it:

1. **View components** render props and emit events. No fetching, no business rules.
2. **State owners** (custom hooks, composables, stores, Angular services) hold one piece of state,
   its loading/error lifecycle and the actions that change it.
3. **Domain logic** in plain TypeScript: pricing, validation, permissions, formatting rules. No
   framework imports, so it is tested without rendering.
4. **API clients** are adapters: they own URLs, auth headers, retries and mapping from wire format to
   domain types, validated at the boundary (zod, valibot or the repository's validator).

A rule that appears inside a component and also inside a second component belongs in layer 3.

## State

- **One owner per piece of state**, placed at the lowest common ancestor of the components that
  read it. Lift it only when a second reader appears.
- **Derive instead of syncing.** A value computable from props or other state is computed during
  render (memoized when measured as expensive); an effect that copies state into state is a bug
  source.
- **Server state lives in the data-fetching layer** (TanStack Query, SWR, RTK Query, the framework's
  loader) with its cache keys; client state holds only what the server does not own: UI mode,
  drafts, selection.
- **URL state for anything shareable**: filters, tabs, pagination, selected record.
- Model exclusive states as a discriminated union (`{status: 'loading'} | {status: 'error', error} |
  {status: 'ready', data}`), so an impossible combination does not type-check.

## Views driven by data

When the set of columns, fields, series or filters can grow (metric dashboards, score tables, admin
grids), the view renders from descriptors, the pattern behind tools that pivot scores by name.

- The API response carries the descriptors from the owning registry (see
  [object design](object-design.md#open-sets-one-registry)) next to the values, for example
  `{metrics: [{name, label, unit, lowerIsBetter}], rows: [{runId, values: {wer: 0.07}}]}`.
- Columns, headers, sort direction and formatting map over the descriptors. Formatters are keyed by
  unit with a default; a missing value renders as a placeholder. No type, column list or switch names
  an individual metric.
- The backend reads the owning store (warehouse, object store, dataset hub) and shapes the response;
  upstream credentials stay server-side.
- Done when a new variant added at the source appears in the view with zero frontend edits.

## Components

- **One job per component**, named for what it shows (`InvoiceTable`, `PaymentStatusBadge`). Split
  when parts change for different reasons, not at a line count.
- **Compose with children and slots** rather than adding a boolean prop per variation. Exclusive
  variants become one `variant` union prop; independent options stay separate props.
- **Props are the interface.** Keep them few and domain-typed; pass the event (`onApprove(id)`),
  not a setter from the parent. A component that needs props only to forward them is a pass-through;
  use composition or the state owner's context instead.
- **Shared design-system components** stay free of feature logic; feature components wrap them.
- Colocate by feature: component, hook, domain logic, tests and styles of one feature in one folder;
  promote to `shared/` when a second feature imports it.

## Effects and side effects

- Effects synchronize with something outside React/the framework (subscription, DOM API, timer).
  Event-driven work runs in the event handler.
- Every effect that subscribes, fetches or starts a timer cleans up and handles an aborted or stale
  response (`AbortController`, ignore flag or the data layer's cancellation).
- Server/client boundary: keep secrets, data access and heavy dependencies on the server side of the
  framework's split (server components, loaders, API routes).

## Tests

- Test through what the user sees and does (Testing Library queries by role and label, Playwright for
  flows); the rendered output and emitted events are the interface.
- Unit-test domain logic in layer 3 directly; mock the network at the API-client seam (MSW or the
  client's fake), not inside components.

## Smells and the smallest fix

| Smell | Smallest in-scope fix |
|---|---|
| Component fetches, transforms and renders in one body | Move fetching into a hook or loader, rules into a domain function |
| Prop drilling through three or more layers that do not use the prop | Composition (pass the child) or a scoped context |
| Same state held in two places and kept in sync by an effect | Keep one owner; derive the other |
| Boolean props that conflict (`isPrimary` and `isDanger`) | One `variant` union prop |
| API response shape used directly in views | Map to a domain type in the API client |
