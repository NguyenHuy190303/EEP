# Pipeline skills (spec → tickets → implement)

A chain of skills that owns the whole delivery flow: write the spec, split it into tickets,
implement each ticket, open the PR.

## Why this is out of scope

EEP skills each answer one engineering question (why is it broken, which option, is it ready, does
this diff hold up) and leave the flow to you and your harness. A pipeline has to own state between
stages, a tracker and a definition of "done" per stage; it would make every other skill depend on
it, and the stages that matter for quality (investigate, review-pr, grill-me) already exist on
their own.

## Prior requests

None filed yet. Decided during the 2026-10-18 review of mattpocock/skills (`to-spec`, `to-tickets`,
`implement`, `implement-spec`).

## Instead

Use a pipeline plugin alongside EEP, or write your flow as a few lines in your own `CLAUDE.md`.
