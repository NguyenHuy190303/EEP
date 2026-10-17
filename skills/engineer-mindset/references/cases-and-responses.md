# Principal-level examples and response calibrations

These examples illustrate the expected reasoning quality. Do not parrot the example's recommendation into a context with different facts. Figures here are hypothetical unless explicitly labeled as provided evidence.

## Contents

- Case A: "Speech API handles 50 concurrent users; can we safely scale to 500?"
- Case B: "Business document looks clear but QC cannot define expected output"
- Case C: "We should create 12 microservices and Kafka from day one"
- Case D: "Healthcare ASR WER is excellent; can we mark production-ready?"
- Case E: "Explain Dependency Injection like a Principal Engineer"
- Case F: "Trunk-based, GitHub Flow, or GitFlow for a multi-team product?"
- Case G: "We need a distributed data platform with a unified manifest"
- Case H: "PR review of a new async inference endpoint"
- Case I: "Add return_direct and 'EXACTLY ONCE' to stop a duplicate tool call"
- Case J: "The agent is slow; speed up inference"
- Teaching ladder for unfamiliar concepts
- Response restraint

## Case A: "Speech API handles 50 concurrent users; can we safely scale to 500?"

**Weak answer:** "Yes, add GPU replicas, autoscale on utilization, and use Redis."

**Strong answer:** "50 concurrent users" is not yet a capacity measure. Define arrival pattern, audio length and codec distribution, synchronous vs queued endpoint, RPS/job completion rate, successful outcome criteria, p95/p99 and error/timeout policy, observed backlog and resource saturation. Then measure sustainable throughput at multiple loads, including queue age, model scheduler wait, CPU/data loading, DB pool and VRAM. Size the next increment against the first saturated shared dependency. Propose a bounded ramp or canary, not a 10x claim. Keep model quality/error slices fixed during scale test."

**Principal difference:** Unpacks claim -> measurement protocol -> failure domain -> safe decision. Separates demand concurrency from server-side execution concurrency. A legitimate conclusion is "leave the ASR model alone; the bottleneck is how requests are scheduled."

## Case B: "Business document looks clear but QC cannot define expected output"

**Weak answer:** "QC should be flexible and ask PO for more examples."

**Strong answer:** "This is not ready for acceptance dataset generation if the same transcript can legitimately yield two labels. Identify the ambiguous rule, show both interpretations with a one-case counterexample, name the risk, ask policy owner for explicit precedence and a canonical golden output. Meanwhile, QA can build harness, error taxonomy structure and tests for fields that are defined. Record a release gate rather than backfilling business policy in QC."

**Principal difference:** Makes boundary and evidence of ambiguity visible; unblocks parallel work without laundering business decisions.

## Case C: "We should create 12 microservices and Kafka from day one"

**Weak answer:** "Microservices are best practice at scale." or "Always use a monolith."

**Strong answer:** "Which teams own independent bounded contexts? Which subsystems require separate scaling and failure isolation? What are the deploy frequency, traffic profile, on-call maturity, compliance boundaries and consistency requirements? For one small product team, a modular monolith control plane with independently deployed GPU/media workers might minimize change cost; expose contracts to preserve future extraction. If teams are independently shipping at scale with measured contention, separate services selectively. Events need delivery, dedupe, schema and replay semantics; a queue should solve a specific asynchronous business flow."

**Principal difference:** Designs for current constraints and credible evolution; explicit escape criteria.

## Case D: "Healthcare ASR WER is excellent; can we mark production-ready?"

**Weak answer:** "Yes, because average WER is below a competitor."

**Strong answer:** "No release decision is supportable on WER alone. Validate study protocol, dataset provenance and split, accent/noise/code-switching/specialty slices, sample size and confidence, model and decoding version, omissions, negation, medications/doses/numbers, speaker attribution and critical-error rate. Separate model readiness from API reliability, serving capacity, compliance and user workflow. Define which errors require human verification, safe fallback and post-release monitoring. Release thresholds need accountable sign-off, not a number invented by QC or AI engineer."

**Principal difference:** Links component metric to actual cost of error and end-to-end contract.

## Case E: "Explain Dependency Injection like a Principal Engineer"

**Weak answer:** "DI is injecting objects to follow SOLID. Here is a framework snippet."

**Strong answer outline:**
1. **Problem:** Domain logic creating concrete collaborators mixes policy and mechanism; hard to test and change.
2. **Mechanism:** Caller or composition root supplies dependencies through an interface/contract; lifetimes and ownership remain explicit.
3. **Example:** Inject an LLM provider into a service; run tests with a fake that controls latency/errors.
4. **Failure:** Inject a request-scoped mutable DB session into a singleton; concurrent requests share/corrupt state. DI alone does not guarantee safety.
5. **Trade-offs:** Added abstraction/indirection and configuration; simpler direct calls are fine when volatility/test seams are low.
6. **Transfer:** Same principle supports model routing, storage backends and data-processing stages without coupling the business policy to SDKs.

**Principal difference:** Can predict the failure and decide *not* to use the pattern.

## Case F: "Trunk-based, GitHub Flow, or GitFlow for a multi-team product?"

**Weak answer:** "Google uses trunk-based, so everyone should." 

**Strong answer:** "First establish release model: single SaaS artifact or supported version lines? CI runtime, integration-test confidence, PR size/age, production deploy cadence, feature flags, ownership and release safety. A SaaS team often benefits from short-lived PRs, protected main, CI and gradual release; this can adopt trunk-based discipline. Maintain release branches when customers require multiple versions. Avoid GitFlow complexity without a real release-train requirement; instrument merge lead time, failed deployments, change failure rate and MTTR."

**Principal difference:** Avoids prestige-driven practices and proposes measurable adoption criteria.

## Case G: "We need a distributed data platform with a unified manifest"

**Weak answer:** "Use S3 + Kafka + Spark + Airflow + MLflow + Kubernetes."

**Strong answer:** "Define distribution boundary, dataset lifecycle, manifest as immutable contract, artifact-addressing/versioning, registry states, provenance/lineage, governance by sensitivity, consumer compatibility and reproducibility. Separate metadata/control plane from payload/data plane; determine direct object-store reads vs signed distribution; specify who can publish, revoke or promote a version. Choose orchestration and compute engines after estimating audio/image/text workloads and failure patterns. Start with one end-to-end consumer contract and prove reproducibility and authorization across teams."

**Principal difference:** Establishes invariants and interfaces before making a tool shopping list.

## Case H: "PR review of a new async inference endpoint"

Prioritize findings like:
- **P0/P1** when a real, traceable correctness or security fault exists: cross-tenant cache, unsynchronized shared mutable state, leaked secrets, side effects retried without dedupe.
- **P1/P2** for reachable reliability problems: synchronous compute blocking the event loop, unbounded tasks, missing cancellation/recovery, pool leak.
- **Recommendation** for maintainability/design: duplicate logic or unnecessary abstraction; tie to cost of change.

Cite exact function/file/line where available. Describe reproduction and effect. Avoid declaring a bug without seeing code or a failing trace. Distinguish suspected issue from confirmed flaw.

## Case I: "Add return_direct and 'EXACTLY ONCE' to stop a duplicate tool call"

**Weak answer:** "Good idea; also add a middleware to repair the arguments."

**Strong answer:** Three patches on symptoms. Write symptom → patch → cause for each; a flow rule in
the prompt is a missing guard (make the write idempotent or gate it in the harness), and an
argument-rewriting middleware hides why fields go missing. Look for the shared cause — tools that
each call an LLM, the model retyping another tool's output, state read from chat history — and
remove it. Verify with the same eval before and after. Worked case: `private/agent-systems.md` when present.

## Case J: "The agent is slow; speed up inference"

**Weak answer:** Tune inference config and serialization, cut DB calls, report a 25% benchmark gain, merge. Users wait about as long as before.

**Strong answer:** "Slow" is a symptom and "inference" is a guessed cause. Break the user-facing request into spans: queue, model, each tool call, external dependencies. Optimize where the time sits, and judge the result on end-to-end latency and task success, not the component benchmark.

**Principal difference:** Solves the problem the user has, not the one the ticket named.

## Teaching ladder for unfamiliar concepts

For any concept (e.g. transaction isolation, event sourcing, idempotency, backpressure, control plane, KV cache):

1. **Definition in plain language, no new jargon.**
2. **A real problem it prevents.**
3. **Underlying mechanics and boundaries.**
4. **A specific failure counterexample.**
5. **At least one alternative and the decision criteria.**
6. **An experiment, code test or telemetry that verifies the claim.**
7. **Transfer to an unrelated stack/domain** to establish genuine understanding.

Scale depth to the request: do not overteach an acronym query.

## Response restraint

- For "review this 2-page document", focus on material gaps; do not demand exhaustive architecture artifacts.
- For "keep it short for the CEO", state risk, capacity, action and decision; no opaque Jira IDs or raw tuning parameters unless necessary.
- For "deep dive", expose causal reasoning and alternatives, not an enormous glossary.
- For "write a message to return task", give a usable, diplomatic message with named blockers and next steps.
- For "critique my proposal", lead with the strongest failure mode, the simplest counterproposal, and what proof could reverse the verdict.
