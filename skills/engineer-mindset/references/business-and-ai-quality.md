# Business contracts, QC readiness, and trustworthy AI

Use when the user must decide whether Product/PO/BA requirements are ready for engineering/QC, define acceptance tests, structure APIs, evaluate ML/LLM/agent/speech systems, or authorize release. The purpose is to make expectations testable without QC or developers inventing policy.

## Requirements readiness: stage-specific gates

A specification is not simply 'good' or 'bad'; ask *ready for what stage?* Discovery/prototype, detailed technical design, implementation, test dataset design, QA acceptance, and production rollout have different gates.

**READY:** Core behavior can be implemented and independently verified without guessing high-impact business rules; high-risk negative paths, data fields, state transitions, approvals, ownership, and acceptance thresholds are defined.

**CONDITIONAL:** Work may proceed on isolated, reversible parts with named assumptions; unresolved items have owner, decision date if supplied, and explicit block on dependent build/test/release.

**NOT READY:** A missing rule changes user-facing outcome, clinical/safety behavior, irreversible side effects, security/tenancy, state semantics, success/failure definition, or dataset labels such that different teams could implement contradictory behavior.

Do not invent a universal '80% complete' requirement. If stakeholders agree on ~70-80% common-case specification as a working threshold, still demand explicit treatment of all known safety-critical and irreversible paths. Coverage percentages require a defined scenario inventory and denominator.

## Five-layer handoff review

1. **Business intent and scope:** Who uses it? What problem? What is explicitly excluded? How success is recognized?
2. **Behavior contract:** Inputs, outputs, field meaning, priority and precedence rules, defaults, null/empty/missing, state transitions, authorization, conflicts, negative and boundary cases.
3. **Examples as oracle:** At least a representative happy path, one boundary/ambiguous case, and critical failure/safety cases; each shows actual input and expected output, with rationale tied to written rule. Examples cannot silently create new policy.
4. **Technical surfaces:** API/OpenAPI/schema, request/response examples, status/error semantics, retry/idempotency, timeouts, compatibility/versioning, external dependency, data ownership, SLO constraints where appropriate.
5. **Quality and operations:** Testable acceptance criteria, golden dataset source, coverage and slices, metrics, thresholds owned by business/product, audit and privacy, rollout/rollback, operational response.

## Business ambiguity triage

Classify every uncertainty:
- **BLOCKER:** Two plausible interpretations produce materially different outputs, safety risk, legal/privacy risk, billable events, permissions, or incompatible contracts. Return for owner decision.
- **HIGH-RISK ASSUMPTION:** Can proceed only with recorded owner-approved interim rule and a defined validation/hold point.
- **NONBLOCKER:** UI wording or reversible implementation detail not altering contract; engineering may select a reasonable design and document it.

Represent blocker as: `Observation -> 2+ competing interpretations -> impact on output/tests -> decision required -> proposed owner`. Avoid forwarding a vague 'business unclear'. The PO/BA owns product policy; engineering owns feasibility and technical design; QC owns test design/validation against approved expectations. All three can surface contradictions; none should silently create unapproved business rules.

### Return-to-owner message example

"Status: NOT READY for QC dataset/acceptance design. Rule R4 specifies conditional hospitalization, but does not define the output when the condition is unavailable in transcript data. This yields two valid labels and blocks expected-output generation. Please confirm the precedence rule and add one canonical input/output example. Other fields A/B/C can proceed independently."

Adapt the tone, owners, and terms to the actual organization; never pretend the sample is an existing rule.

## Acceptance criteria and test design

For every meaningful field or operation, define:
- Precondition and source-of-truth data.
- Trigger/action/state transition.
- Expected result or allowed set of results.
- Precedence with conflicting evidence; abstain/escalation rule when the evidence is insufficient.
- Unauthorized/invalid/missing/duplicated/stale data outcome.
- Error taxonomy with failure cause and severity, not merely exception strings.
- Test case IDs tied to rule IDs and specific expected outputs; deterministic vs judgment-based cases separated.

Good acceptance criteria are observable, unambiguous and independent of a specific implementation. A business rule can yield multiple tests. Do not force Gherkin on every team; use it where it sharpens behavior.

## AI / Agent / Speech evaluation: evaluation is a product contract

1. **Task:** What business decision, generated field, speech transcription/diarization/TTS result or agent action is evaluated? What is the ground truth or permissible alternative?
2. **Unit of analysis:** Utterance, word, critical term, speaker segment, field, document, tool call, episode, user task or end-to-end workflow. Align metric to harm and UX.
3. **Dataset:** Provenance, consent/privacy, training/dev/test separation, contamination/leakage checks, realistic distributions, sample sizes, annotation protocol, label version, difficult/edge/negative cases, failure and abstention cases.
4. **Slices:** Acoustic noise, device, accent/dialect, code-switching, length, domain vocabulary, rare clinical names/numbers, intent ambiguity, tenant, workflow path; for agents, multi-step workflows, tool failures, long context and incomplete input. Choose relevant groups, not a rote checklist.
5. **Metrics:** Core quality plus critical error rate, false-positive/false-negative asymmetry, completeness, calibration if meaningful, latency, cost and operational reliability. WER alone may miss wrong drug dose/negation; success rate alone may hide risky tool actions. For agents, measure TTFT, time to first meaningful response, tool latency, end-to-end latency and task success together: an early token on a useless answer is not a good experience.
6. **Evaluator quality:** Human agreement, rubric clarity, adjudication, LLM-as-judge bias, reproducibility, data/model/prompt/tool version lineage, confidence intervals or uncertainty where relevant.
7. **Causal interpretation:** Separate component eval from end-to-end; hold protocol constant for A/B comparison, avoid tuning to test set (keep a holdout set or workload you never iterate on for the published number), investigate distribution shift and systematic failure clusters.
8. **Safety and release:** Human approval, abstention/verification for high-stakes fields, safe fallback, approval thresholds owned by accountable stakeholders, regression gate, monitoring and rollback trigger.

For healthcare AI, never turn model inference into medical fact or authorize release solely from aggregate accuracy. Consider negation, laterality, dosage, temporal qualifiers, patient attribution, clinical recommendations, mandated actions, and conditional statements. Protect sensitive transcripts and evidence in test reports.

## Validating evaluators, labels and judges

- Label outcomes pass/fail rather than on a 1-5 scale; the pass-rate bar is a product decision,
  scaled to risk, and need not be 100%.
- An LLM judge, labeler or reviewer is a model with its own error rate. Before its output touches a
  gold set or a release decision, measure precision and recall against a human-checked sample, and
  report both rather than raw agreement (raw agreement looks good on imbalanced classes). Field case
  F5: 16 of 22 LLM-flagged speaker errors were real.
- For classifiers, report precision and recall across thresholds; a good AUC does not guarantee a
  usable threshold when class scores overlap.
- Criteria drift: people refine the criteria while grading, and some criteria can be defined only
  after seeing outputs. Version the rubric; regrade when it changes.
- Check independence: a test set built from the same sources as training or tuning data measures
  memory, not generalization (field case F6: 1.3% of one internal benchmark was independent).
- You can never stop looking at data: read real failures each iteration, not only the metric.

## Interface/contract review specifics

- Confirm OpenAPI is consistent with current implementation and examples; swagger existence is not proof contract quality.
- Name endpoint/payload schema/version, optional vs nullable, units, enumerations, authentication/authorization, pagination, ordering, error status/body, rate limits, idempotency, request/operation deadlines, callbacks/webhooks or polling state semantics, backward compatibility.
- Distinguish transport success (HTTP 200/202) from semantic AI correctness or completed asynchronous operation.
- Include reproducible examples (e.g. curl) only when user asks or they materially aid handoff; never fabricate real keys, URLs, benchmarks or response fields.
- Separate model capability, quality benchmark, service capacity and business readiness. One cannot substitute for another.

## Release gate output

Provide a short table or focused paragraphs:

| Finding | Gate | Evidence/ambiguity | Action needed | Owner |
| --- | --- | --- | --- | --- |
| Undefined result on conditional rule | BLOCKER | Two legitimate expected outputs | Confirm decision hierarchy; add golden case | PO/BA |
| Missing p95 on representative load | CONDITIONAL | Only single-request timing exists | Define workload and load-test target | Engineering/SRE |
| UI copy difference only | NONBLOCKER | Does not change acceptance policy | Resolve in implementation review | UI team |

Use actual findings only. Then specify which tasks may proceed, which cannot, and what evidence will upgrade the gate.
