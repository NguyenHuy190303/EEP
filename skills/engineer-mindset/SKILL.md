---
name: engineer-mindset
description: Use when choosing an architecture, stack, library, schema, API shape or module boundary, or making a consequential engineering judgment, standards or readiness call. Its module table picks one starting guide (design decision, architecture, code standards, module design, Python, agent design); ordinary local edits follow repository rules.
---

# Engineer mindset

Find the decision that changes the outcome. Scale the investigation to its reversibility and consequences. Follow the user's scope, language and requested answer length; a short verdict stays short.

**When the user asks for a short answer** ("ngắn", "short", "tl;dr"), the whole reply is at most five lines: the verdict, up to three reasons, one next step with its pass/fail line. No drafted messages, no extra sections, no caveat paragraph; offer depth in a follow-up instead. Read a reference only if it changes the verdict.

## Pick the relevant module

Choose from the task and evidence already available. Read one starting module, then only the specific references it calls for. Do not load the table as a checklist or invoke every related skill.

| Request | Read first | Expand only when needed |
|---|---|---|
| Choosing a stack, library, schema, API shape or module boundary | [design decision](modules/design-decision/MODULE.md) | [architecture](modules/architecture/MODULE.md) when the choice is system-level |
| Judgment, trade-off, go/no-go, principal critique | [judgment](references/judgment.md) | Existing domain playbooks below |
| System/service architecture, migration, build vs buy | [architecture](modules/architecture/MODULE.md) | Its economics, stack or system-design reference for that specific decision |
| Code standards, errors, retries, APIs, observability, algorithms or concurrency | [code standards](modules/code-standards/MODULE.md) | Its core, reliability, API or language reference for the affected boundary |
| Python setup, dependencies, scripts or requested tooling migration | `private/python/SKILL.md` when present, otherwise `eep:toolchain` | PEP 723 or project configuration only for the chosen task |
| Module interfaces, deep/shallow modules, testability | [module design](modules/module-design/MODULE.md) | The vocabulary or testability reference selected there |
| LLM tool/skill/harness boundaries, prompt patches or multi-agent design | `private/agent-design/SKILL.md` when present | `private/agent-systems.md` for worked cases |
| Release/readiness verdict based on repo, CI, deploy or telemetry | [evidence gates](references/evidence-gates.md) | [AI/business quality](references/business-and-ai-quality.md) for evaluation criteria |
| Reliability/capacity diagnosis | [reliability diagnostics](references/reliability-diagnostics.md) | [evidence gates](references/evidence-gates.md) for a performance or capacity report; `eep:investigate` for the investigation procedure |
| Cross-team ownership/strategy | [principal leadership](references/principal-leadership.md) | `private/field-cases.md` for a precedent, when present |
| Teach a concept or calibrate the answer | [cases and responses](references/cases-and-responses.md) | [sources](references/sources.md) when provenance matters |

`modules/` holds former standalone skills; read them as modules and resolve their links relative to the module file. `private/` is machine-local team material (gitignored); skip any row whose private file is absent.

## Common decision contract

- Name the decision, owner, constraints and observable success condition. Ask only about a missing fact that changes the result.
- Trace the mechanism and relevant failure boundaries. A passing component test is evidence for that component, not production readiness.
- Compare credible options, including the smallest change or no change. Price failure, operations and reversal; do not invent an alternative to fill a table.
- State `[horizon · basis] choice; wrong if observable condition`, using throwaway/tactical/durable and fact/guess/taste. Name blast radius, next check and rollback when material.
- Report the verdict first with paths, commands or measurements that support it. Preserve validation, error handling and user work; add no ceremony to an ordinary edit.

A diff review belongs to `eep:review-pr`. An explicit standards or architecture review stays in its selected module. Do not stack both workflows unless they answer different requested questions.
