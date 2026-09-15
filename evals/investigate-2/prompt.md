---
description: "Produces a hop-by-hop flow with protocols and shape changes, separating code inference from runtime observation."
tags: [investigate]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Trace where the tenant_id field travels from an HTTP request through validation, persistence, and an outbound event. Mark anything you cannot observe directly.
