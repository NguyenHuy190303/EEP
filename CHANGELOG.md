# Changelog

## 1.6.2 (2026-09-28)

- The 1.6.0 scrub was incomplete in two ways an independent re-audit caught: (1) three commits made
  *after* the scrub (1.6.0 and 1.6.1's own commits) were themselves authored with the company email,
  because the repo's local git config still pointed at it — the earlier mailmap rewrite only fixed
  commits that already existed, not the identity used for new ones; (2) the local absolute path
  `/Users/<name>/Projects/EEP`, committed in the old (already-deleted) v1.0.0 eval-results run, was
  still recoverable from history — only removed from the current tree, never rewritten out of the
  commits that carried it. Both are now fixed: repo-local `user.email` corrected, history rewritten
  again (`git-filter-repo --mailmap` + `--replace-text` + `--replace-message`), tags recreated to
  point at the new commit hashes, and force-pushed. Verified via the GitHub API (not just local
  `git log`) that every commit on the remote now shows the personal email and no local path.
- Corrected `evals/RESULTS.md`: it previously said only `sentry-cli` (3 of 12 skills) had no eval
  coverage. The accurate count is 8 of 12 skills with zero eval directory at all
  (`design-decision`, `deepsearch`, `present-html`, `sky-job`, `vietnamese-writing`, `cleanup`,
  `toolchain`, `layout`); `sentry-cli` specifically has case files but no working fixture, which is
  a narrower and less serious gap than "no eval at all." Fixed to report the real number.

## 1.6.0 (2026-09-27)

- Scrubbed employer infrastructure and personal references from the whole repo, including git
  history (Tailscale endpoint, internal SkyPilot/kubeconfig names, internal repo/HF-org names,
  company email). Hardcoded `~/Projects/EEP` paths replaced with `${CLAUDE_PLUGIN_ROOT}`.
- Added `LICENSE` (MIT, matching the manifest's existing claim).
- Dropped the broken v1.0.0 eval run (0/9 pass — cases ran against an empty sandbox with no
  fixture repo, so no case could be satisfied regardless of the skill).
- Rebuilt the `investigate` and `review-pr` eval cases as `case.yaml` with a `scaffold_script` that
  seeds a real fixture repo per case, so the cases are actually satisfiable.
- Strengthened `investigate` (paired comparisons + negative controls for perf claims),
  `design-decision` (cheap-gate/expensive-truth pairing and typed-vs-silent error handling for
  ML/agent decisions), `review-pr` (answering pushback with a concrete counterexample; an outside-PR
  Problem/Fix/Testing format), `cards-readme` (benchmark sections must state what they do not
  prove), `sky-job` (resumable long jobs: tag-based resume, never persist failed calls, fail loud on
  partial ingest), and `toolchain` (keep the installable core small; heavy deps behind extras).
- Added CI (`claude plugin validate`, the palette test, shellcheck on every `.sh` script).

## 1.5.0 (2026-09-16)

- Added `cleanup`: local-machine port/process/tmux/Docker triage, tiered safe/ask/never, remote
  resources stay with `sky-job`.

## 1.2.0 – 1.3.0 (2026-09-16)

- Added `toolchain` (uv for Python, JS follows the repo's lockfile, digest-pinned containers).
- `deepsearch` gained the `before-cook` prior-art-sweep mode: `scripts/probe.sh`, the solved-category
  adopt-never-rebuild table, and explicit build-it-yourself criteria.

## 1.1.0 – 1.1.3 (2026-09-16)

- Added `layout`: root-clean rule, dated experiment/output directories, `type/TICKET-slug` branch
  naming, per-directory conventions, numbered `docs/spec/` reading order.

## 1.0.0 – 1.0.1 (2026-09-15)

- Initial release: nine skills as one Claude Code + Codex plugin (`investigate`, `design-decision`,
  `deepsearch`, `review-pr`, `present-html`, `cards-readme`, `sentry-cli`, `sky-job`,
  `vietnamese-writing`).
