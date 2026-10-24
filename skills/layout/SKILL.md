---
name: layout
description: "Decide where a file, artifact, run or branch goes and what to name it, or reorganize a messy folder with named, reversible moves."
---

# Layout

Use the existing repository layout first. Keep scratch/generated files out of its root. Names should sort and be searchable: date first for dated artifacts, hyphens inside words, underscores between fields; no final/v2/new-copy names.

Place project code/config/tests/docs in the repo. Put expensive non-project-curated results in the user's durable artifact location and add a pointer to the artifact index; MEMORY holds one link to that index. Temporary work is for reproducible intermediates, never the only copy of costly results. A run's log stays with its outputs.

- Creating a normal file: follow its neighbors and the closest instructions; no additional reference needed.
- Naming a branch, experiment/run or durable artifact: read [naming and storage](references/naming-and-storage.md) for the relevant convention.
- Designing docs/spec/report or experiment directory structure: read [directory conventions](references/directory-conventions.md), only the relevant section.
- Starting a new repo or organizing a messy folder: read [organizing](references/organizing.md) and the matching skeleton if useful. An established project keeps its own skeleton.

For reorganization, inspect status and boundaries and show from/to/reason for each move. Unrelated work stays where it is; archive named targets when appropriate. Moves the user explicitly requested go ahead without a second confirmation.
