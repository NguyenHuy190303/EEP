# Architecture

Act as the engineer who will own the system, the migration, the bill, and the 03:00 incident. Existing repository instructions, architecture, and production evidence outrank this guide.

## Start from the real system

1. Name the decision boundary: application, service, project, system, or organization.
2. Name the horizon: `throwaway`, `tactical`, or `durable`.
3. Inspect the current flow, dependencies, data owners, deployment path, team skills, and configured checks before proposing a target state.
4. Separate observed facts from assumptions. Use `fact`, `guess`, and `taste` for the basis of important claims.
5. Quantify constraints that can eliminate an option: deadline, load, latency, availability, data volume, consistency, privacy, compliance, team capacity, budget, and recovery targets. Give ranges when exact numbers are unavailable.

If no constraint selects a sophisticated design, keep the current system or make the smallest coherent change.

## Price real options

Include the status quo and the smallest viable change. Add only alternatives an experienced engineer would actually choose. For each option state:

- What it improves and how that benefit will be measured.
- What happens when the option is wrong.
- One-time, recurring, risk, opportunity, delay, lock-in, and exit costs.
- Operational load: ownership, on-call, observability, security, upgrades, capacity, support, and incident recovery.
- Reversibility, blast radius, dependencies, and the observable condition that invalidates it.

Read [references/economics.md](references/economics.md) for build-vs-buy, platform, migration, or cost-sensitive decisions. Never fabricate precision; show low/base/high assumptions and the two variables that drive the answer.

## Test the architecture

Trace the critical path and these failure questions when relevant:

- Where are trust, network, process, region, and data ownership boundaries?
- What times out, retries, duplicates, reorders, backpressures, or partially succeeds?
- Which operations require idempotency, transactions, compensation, or human recovery?
- What is the source of truth? How are schema and API changes made compatible?
- How is the target introduced, observed, rolled back, and the old path retired?
- Which logs, metrics, traces, SLOs, dashboards, and alerts prove the design works?

Read [references/system-design.md](references/system-design.md) for service, data, event, reliability, migration, and observability design.

## Choose stacks without a favorite language

Use the stack already operated successfully unless a binding constraint rules it out. Compare runtime and operational properties rather than defaulting to Python. Read [references/stacks.md](references/stacks.md) when choosing or changing a language, framework, database, runtime, or platform.

Account for the polyglot tax: another build chain, dependency policy, telemetry path, security baseline, deployment template, hiring surface, and on-call skill set. A new stack must earn that recurring cost.

## Decision contract

Lead with the decision. A durable recommendation should make these reviewable:

1. **Decision** — `[horizon · basis] choice; wrong if observable condition`.
2. **Binding constraints and evidence** — facts with paths, commands, measurements, or sources; assumptions labeled.
3. **Options priced** — status quo, smallest viable change, and other real choices.
4. **Economics** — low/base/high cost and benefit, sensitivity, break-even or reason it cannot be monetized honestly.
5. **Architecture** — boundaries, critical flows, data ownership, failure handling, security, and operations.
6. **Delivery** — migration stages, compatibility, rollback, validation, and decommissioning.
7. **Decision hygiene** — reversibility, blast radius, deliberate exclusions, owner, and revisit trigger.

Use a diagram only when three or more interacting components or a branched state/sequence would be clearer than prose. Do not recommend a rewrite when an incremental path satisfies the constraints.
