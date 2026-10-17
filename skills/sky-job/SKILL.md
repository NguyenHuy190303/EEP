---
name: sky-job
description: "Operate SkyPilot GPU jobs on the shared pool: authorized preflight/launch, bounded monitoring, durable harvest and named teardown. Also route resumable jobs and non-Sky compute targets."
---

# GPU job lifecycle

Choose the current lifecycle step; read that reference before changing state. A launch does not imply permission to spend more than authorized, cancel someone else's work or use another compute target.

- New cluster, task YAML or rerun: [launch](references/launch.md). Preserve cost/duration/stop-condition/output-path authorization, capacity and actual GPU memory checks, the queueing trap and diagnosed failures before retry.
- Existing job, status, logs or served endpoint: [monitor and connect](references/monitor-and-connect.md). Block on streaming logs instead of token-burning polling. A non-zero status is not proof of a specific failure.
- Completion, failure or stopping: [harvest and teardown](references/harvest-and-teardown.md). Save logs, metrics and exact config durably before named teardown; verify release. Autostop with deletion is safe only with durable export already in the job. Never down all targets.
- Long, preemptible, quota-limited work or a non-Sky target: [resumability and targets](references/resumable-and-targets.md). Preserve run identity, partial-failure visibility and the login-node prohibition.

Do not start a long run without an output/harvest plan. Syntax comes from installed command help or official SkyPilot docs; org endpoints, reserved cards and credentials stay in local notes. Do not load every lifecycle chapter for a read-only status question.
