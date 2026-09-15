---
description: "Tests the retry and configuration choices against concrete failure modes, repository conventions, and operational cost rather than praising defensive code by default."
tags: [review-pr]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Self-review my local diff before I open a PR. It adds a retry and a new environment variable around an external API call. Check whether those mechanisms solve a real failure mode.
