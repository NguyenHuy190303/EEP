---
description: "Uses the dedicated issue command with bounded JSON fields and lets the CLI auto-detect scope before adding explicit targets."
tags: [sentry-cli]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Show me the five newest unresolved Sentry issues for the current project and return only short ID, title, level, and event count.
