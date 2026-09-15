---
type: llm
---

PASS only if ALL of the following hold; FAIL otherwise.
- Uses dedicated trace and span commands before `sentry api`.
- Correlates logs by the supplied trace ID.
- Keeps missing scope or unavailable data explicit.
