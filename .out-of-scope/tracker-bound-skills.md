# Skills bound to one issue tracker

Triage, labelling or setup skills that read and write GitHub or GitLab labels, states and sub-issues
as part of their steps.

## Why this is out of scope

EEP is used with Jira, GitHub and no tracker at all. A skill whose steps assume one tracker's
labels is first-class on that tracker and prose-only on the rest. Where a skill needs a ticket
(review-pr's Spec axis), it reads it through whatever tracker access the session already has.

## Prior requests

None filed yet. Decided during the 2026-10-18 review of mattpocock/skills (`triage`, `wayfinder`,
`setup-matt-pocock-skills`).

## Instead

Keep tracker conventions (labels, ticket form, branch naming) in your team's own skill or
`CLAUDE.md`, next to the credentials and IDs they need.
