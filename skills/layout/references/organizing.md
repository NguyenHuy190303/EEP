## Suggested skeletons — offer, never impose

When starting a new repo, or when asked "how should this be organised", pick the closest skeleton
from `references/skeletons.md` (service · research/data · infra · skills/plugin) and adapt it.
An existing repo is **not** reshuffled to match a skeleton unless asked; the hard rules above are
enough for an existing repo.

## Tidy mode — when asked to clean a folder

1. Inventory: list what is there with size, last modified, and a one-word role guess.
2. Propose moves as a table (`from → to`, reason), grouped by rule 1–3 above. Flag anything that
   looks like a result that cost money (rule 5) — those get a pointer, not a delete.
3. Move only after OK. `git mv` inside a repo so history follows. Never delete — park in
   `_archive/<YYYY-MM-DD>/` and let the user delete.

## Output

The move table or the created tree, then one line per rule that applied. No essay on tidiness.
