---
type: llm
---

PASS only if ALL of the following hold; FAIL otherwise.
- Uses `sentry issue list` rather than raw API access.
- Requests JSON with only needed fields and limits results to five.
- Does not expose authentication material.
