---
description: "Grills before planning: asks the whole first frontier as numbered questions with a recommended answer each, keeps dependent questions for later rounds, and writes no plan or code yet."
tags: [grill-me]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Grill me on this before you plan anything. I want to add a `--dry-run` flag and a config file to our small CLI. Today the whole program is:

```python
def greet(name):
    print("hi", name)
```
