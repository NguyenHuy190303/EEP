# Architecture economics

Use this for build-vs-buy, platform, cloud, migration, scaling, and durable dependency choices. Currency is optional; omission of a cost category is not.

## Cost model

Choose a decision horizon first. Price each option over the same horizon.

`TCO = build + migration + recurring run + people/operations + expected risk + opportunity/delay + exit - residual value`

Report low/base/high values with assumptions. When money is unavailable, use engineer-days, calendar delay, on-call pages, recovery time, capacity, or a transparent 1–5 score. Do not combine unlike units into a fake total.

### One-time cost

- Discovery, design, implementation, integration, security review, testing, documentation, training.
- Data migration, backfill, validation, dual writes, shadow traffic, parallel run, rollback preparation.
- Procurement, legal, compliance, vendor review, network and identity integration.
- Decommissioning the old path and removing temporary compatibility code.

### Recurring cost

- Compute, storage, network/egress, API calls, licenses, support, backup, disaster recovery.
- CI minutes, build/cache storage, environments, observability ingest and retention.
- Patch and upgrade work, dependency churn, capacity planning, incident response, on-call and support.
- Cognitive load, another language/toolchain, duplicated controls, runbooks, and specialist hiring.

### Risk cost

For material risks, use ranges:

`expected loss per horizon = probability range × impact range`

Include reliability, security, privacy, compliance, vendor continuity, quota, data loss, lock-in, and migration failure. Expected value does not make catastrophic or legally unacceptable risk acceptable; name hard constraints separately.

### Opportunity and delay cost

- What valuable work will the same people defer?
- What is the value lost per week or release while this option delays delivery?
- Does it reduce future lead time or only move work into a platform team?
- Does waiting buy information or merely postpone an inevitable migration?

Estimate `cost of delay = value per period × delay`, using a range and stating the value proxy.

### Exit and lock-in cost

- Data export format, volume, egress fees, and time to copy.
- Replacement APIs, proprietary schemas, identity, networking, observability, and operational retraining.
- Contract term, minimum spend, price-change exposure, regional availability, and service sunset risk.
- Time to restore an independent path and the amount of business interruption during exit.

Reversibility has option value. Prefer an experiment or adapter only when it materially reduces an expensive one-way commitment; do not add abstraction for hypothetical portability.

## Benefit model

Tie every benefit to an observable:

- Revenue or conversion gained; cost or engineer time removed.
- Lead time, deployment frequency, throughput, latency, or capacity improved.
- Incidents, recovery time, support volume, security exposure, or audit effort reduced.
- A new capability unlocked, with probability of use and time-to-value.
- Information gained by a cheap experiment before a durable commitment.

Avoid counting the same benefit twice, such as both engineer-hours saved and the salary value of those hours.

## Decision checks

- **Sensitivity:** Which two assumptions can flip the decision? Show the threshold.
- **Break-even:** When does the higher up-front option recover its cost, if ever?
- **Utilization:** Are reserved capacity, platform staff, or licenses actually used?
- **Marginal cost:** What does the next customer, request, GB, region, or service cost?
- **Tail cost:** Price failure recovery and rare peaks, not only the average month.
- **Measurement:** Name the baseline, target, owner, and date for checking realized value.

Prefer the cheaper reversible option when ranges overlap and no hard constraint selects the expensive one.
