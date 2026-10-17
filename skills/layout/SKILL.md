---
name: layout
description: "Place and name project files, artifacts and runs consistently. For reorganizing existing folders, preserve user work and propose named reversible moves."
---

# Layout

Use the existing repository layout first. Keep scratch/generated files out of its root. Names should sort and be searchable: date first for dated artifacts, hyphens inside words, underscores between fields; no final/v2/new-copy names.

Place project code/config/tests/docs in the repo. Put expensive non-project-curated results in the user's durable artifact location and add a pointer to the artifact index; MEMORY holds one link to that index. Temporary work is for reproducible intermediates, never the only copy of costly results. A run's log stays with its outputs.

- Creating a normal file: follow its neighbors and the closest instructions; no additional reference needed.
- Naming a branch, experiment/run or durable artifact: read [naming and storage](references/naming-and-storage.md) for the relevant convention.
- Designing docs/spec/report or experiment directory structure: read [directory conventions](references/directory-conventions.md), only the relevant section.
- Starting a new repo or organizing a messy folder: read [organizing](references/organizing.md) and the matching skeleton if useful. Never impose a new skeleton on an established project.

For reorganization, inspect status and boundaries, show from/to/reason, and respect authorization already given. Never delete unrelated work; archive named targets when appropriate. Do not ask again to perform moves explicitly requested by the user.
