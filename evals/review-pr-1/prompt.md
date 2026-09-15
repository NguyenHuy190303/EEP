---
description: "Runs configured checks, inspects the exact diff and surrounding transaction lifecycle, then returns severity-ordered actionable findings or an explicit no-findings result."
tags: [review-pr]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Review the current branch against main. The diff changes an async FastAPI endpoint and its database transaction. Report only concrete regressions with file and line evidence; do not edit anything.
