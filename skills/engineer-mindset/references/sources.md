# Sources and verification status

Checked 2026-10-15/16. "Fetched" means an agent read the page and returned a short verbatim phrase;
the phrases came through a summarizing fetch tool, so re-open the page before quoting it.
Status: **fetched** · **summary only** (paywall) · **memory only** (cited from the primary work,
not re-read; treat as a heuristic) · **not found** · **refuted**.

| # | Principle | Source | Status |
|---|---|---|---|
| 1 | Name the decision and owner; understanding over being right | Will Larson, "Operating at Staff" and "What do Staff engineers actually do?" — https://staffeng.com/guides/operating-at-staff/ | fetched (3-0 verification) |
| 2 | Reversibility sets the depth | Jeff Bezos, 2015 letter to shareholders (Type 1 / Type 2 decisions) — https://s2.q4cdn.com/299287126/files/doc_financials/annual/2015-Letter-to-Shareholders.PDF | fetched |
| 3 | Mechanism before patch; fix the sustaining loop | internal team practice (agent-design and code-review skills); Marc Brooker, post on metastable failures (2021-05-24) — https://brooker.co.za/blog/2021/05/24/metastable.html ; obra/superpowers `systematic-debugging` (MIT) | fetched |
| 4 | Understand before removing | G. K. Chesterton, *The Thing* (1929) | memory only |
| 4 | Observable behaviour is the contract | Hyrum's law — https://www.hyrumslaw.com/ | fetched |
| 5 | Complex systems grow from simple ones | John Gall, *Systemantics* (1975) | memory only |
| 5 | Innovation tokens | Dan McKinley, "Choose Boring Technology" — https://boringtechnology.club/ | fetched |
| 5 | Climb from one call to agents only when needed | Anthropic, "Building effective agents" — https://www.anthropic.com/engineering/building-effective-agents | fetched |
| 5 | Deep modules, interface over implementation | John Ousterhout, *A Philosophy of Software Design* (2018); mattpocock/skills `codebase-design` (MIT) | memory only (book); skill read |
| 6 | Deliberate / visible / distinguishable / bounded fallback | internal team practice (code-review skill) | read |
| 7 | Timeout from tail latency; retry at one layer; queue age | Amazon Builders' Library, "Timeouts, retries, and backoff with jitter" and "Avoiding insurmountable queue backlogs" (now under builder.aws.com) | fetched |
| 7 | Backoff does not fix sustained overload | Marc Brooker, "What is backoff for?" — https://brooker.co.za/blog/2022/08/11/backoff.html | fetched |
| 7 | SLO from user need; error budget; postmortem triggers | Google SRE book ch. 3, 4, 15 — https://sre.google/sre-book/table-of-contents/ | fetched |
| 7 | Cohort rollout; instrument before shipping | Charity Majors, "Shipping software should not be scary" — https://charity.wtf/2018/08/19/shipping-software-should-not-be-scary/ | fetched |
| 8 | A check proves only what it exercised | obra/superpowers `verification-before-completion` (MIT); author's working rules | read |
| 9 | Binary labels; pass bar is a product decision; judge precision/recall | Hamel Husain, "Your AI product needs evals" — https://hamel.dev/blog/posts/evals/ | fetched |
| 9 | Criteria drift | Shankar et al., "Who Validates the Validators?" — https://arxiv.org/abs/2404.12272 | fetched (abstract) |
| 9 | Precision/recall across thresholds; risk-scaled bar | Eugene Yan, "Evals" — https://eugeneyan.com/writing/evals/ | fetched |
| 10 | Short decision records, superseded not deleted | Michael Nygard, "Documenting architecture decisions" (2011) — https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions | fetched |
| 10 | Premortem | Gary Klein, "Performing a project premortem", HBR 2007 | summary only |
| 10 | Horizon · basis · falsifier contract | author's working rules | read |
| — | Context is a budget; ambiguous tools test | Anthropic, "Effective context engineering for AI agents" — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | fetched |
| — | Multi-agent ≈ 15× chat tokens; token use ≈ 80% of variance | Anthropic, "How we built our multi-agent research system" — https://www.anthropic.com/engineering/multi-agent-research-system | fetched |
| — | Actions carry implicit decisions | Cognition, "Don't build multi-agents" — https://cognition.com/blog/dont-build-multi-agents | fetched |
| — | Skills 3 calls vs subagents 4 (one focused request) | LangChain multi-agent docs — https://docs.langchain.com/oss/python/langchain/multi-agent | fetched; the word "lightest" for Skills is **not found** on the page |
| — | Staff tenets list | Amazon Principal Engineering tenets — https://www.amazon.jobs/content/en/teams/principal-engineering/tenets | fetched: nine names, no explanatory text |
| — | Skill form: third-person description, under 500 lines, one-level references, evals first | Anthropic Agent Skills best practices — https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | fetched |
| 8 | Evidence gates: which evidence wins, traceability chain, per-domain false positives (`evidence-gates.md`) | Ported and reworded from a parallel update of this skill built on v0 (evidence-driven-execution, evidence-quality-gates, source-playbooks; 2026-10-15, author not recorded) | not checked against an external source; treat as practice |
| 1–2, 8–10 | Outcome over output, stopping condition, goodput, holdout, agent claims as non-evidence, scenario/metrics/infrastructure report, post-release ownership, mechanisms over heroics | "The Principal Engineering Doctrine" (Vietnamese internal doctrine received 2026-10-17, author not recorded); full text in `private/principal-doctrine.vi.md` when present | not checked against an external source; treat as practice |

## Not used, and why

- "Make it work, make it right, make it fast" attributed to Kent Beck: no primary source found.
- "Glue work is decisive for project success": refuted 1-2 in verification.
- "Side-effecting APIs must be idempotent before retries; never retry 4xx" (attributed to the
  Builders' Library summary): refuted 0-3 as a quote of that source. It is still sound practice,
  but cite it to your own reasoning, not to them.
- Kent Beck, Tidy First "first, after, later, never": only the "never" section was readable.

Research artifacts: deep-research run wf_87e304a2-2cd plus three source-verification passes,
stored with the build of this skill.
