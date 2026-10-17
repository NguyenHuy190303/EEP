---
type: llm
---

PASS only if ALL of the following hold; FAIL otherwise.
- The reply asks several numbered questions in one round, and each question carries a recommended answer.
- At least one question asks what `--dry-run` should suppress or how the config is found or formatted, rather than a generic "any other requirements?".
- The reply does not present a finished implementation plan or code as if the decisions were already settled; it stops and waits for answers.
