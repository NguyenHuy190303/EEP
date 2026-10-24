---
name: grill-me
description: "Interview the user relentlessly about a plan, design or idea until both sides share one understanding. Use when the user says 'grill me' or wants a plan stress-tested, and whenever plan mode is active, before writing the plan."
---

# Grill me

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Word each question so "yes" accepts your recommended answer. Write the round in the reply language the user's instructions set, else in the user's language.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it. Keep going while it runs: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Act on it once the user confirms you have reached a shared understanding.

## In plan mode

The EEP plan-mode hook points here whenever plan mode is on. Grill first, then write the plan from the settled tree.

- One session per plan. On later turns, continue the open session instead of starting over.
- The user can stop it at any point ("skip", "enough", "just plan"). Then list the decisions still open as assumptions in the plan.
- A small change with no real decision left needs no rounds. Say so in one line and write the plan.

Source: mattpocock/skills `grill-me` + `grilling` (MIT, see LICENSE).
