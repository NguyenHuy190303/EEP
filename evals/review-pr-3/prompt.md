---
description: "Checks placement, callers, schemas, fixtures, serialized data, and external consumers while preserving a tight evidence standard."
tags: [review-pr]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Review this refactor that moves validation from a service into the HTTP router and changes a response field from optional to required. Trace the impact beyond the edited files.
