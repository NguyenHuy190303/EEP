# Changelog

## Unreleased

## 1.11.0 (2026-10-24)

- **`investigate` root-cause starts with a red loop** (adapted from mattpocock/skills
  `diagnosing-bugs`, MIT, `skills/investigate/LICENSE`). No hypothesis until one command has been run
  and shown going red on this bug: red-capable, deterministic, tight, agent-runnable. Then tighten it,
  raise the reproduction rate for a flaky bug, and minimise one cut at a time. Temporary probes carry
  a `[DEBUG-xxxx]` tag and are grepped away before the report. New
  `scripts/hitl-loop.template.sh` scripts the steps a person must do. Deployed-service step 3 now
  builds the loop from the event's input or hands over.
- **`review-pr` adds a Spec axis** (adapted from mattpocock/skills `code-review`, MIT,
  `skills/review-pr/LICENSE`). The ticket found from the branch name or commits (any tracker the
  session can read) is checked by its own subagent, or a separate pass where the harness has none:
  missing or partial, not asked for, implemented wrong, each with the spec line and diff hunk.
  Standards and Spec are reported under separate headings and never ranked against each other. The
  base ref and a non-empty diff are checked first.
- **New `engineer-mindset` module `writing-for-agents`** (adapted from mattpocock/skills
  `writing-for-agents` + `SKILL-MECHANICS`, MIT): pointers, one trigger per branch, the information
  ladder, completion criteria, leading words, positive steering, pruning. Routed by a new table row
  and a "writing a skill" trigger in the description.
- **Writing pass over all SKILL.md files** with that module: descriptions drop body-only sentences
  (total 2691 → 2441 characters), prohibitions become positive targets where a positive form exists,
  `cards-readme`, `deepsearch` and `present` gain an explicit "done when", and duplicated tool lines
  in `investigate` are merged. `sentry-cli` is vendored and unchanged; hard guardrails in `cleanup`
  and `toolchain` stay.
- **`design-decision` ADR rule** (adapted from mattpocock/skills `domain-modeling`, MIT): record a
  decision only when it is hard to reverse, surprising without context and a real trade-off; one
  paragraph is enough. Read `GLOSSARY.md` and ADRs in the area before naming options.
- **Repo hygiene for contributors:** `SCOPE.md` (a change cites an observed failure), `.out-of-scope/`
  with five decided rejections, a bug issue form that asks for harness, model, effort and context
  fill, and an "It's working if" column in the README skills table (the duplicate `grill-me` row is
  gone).

## 1.10.0 (2026-10-17)

- **New skill `grill-me`** (adapted from mattpocock/skills, MIT). It interviews the user about a
  plan in rounds over a design tree. Each round asks every question whose prerequisites are
  settled, gives a recommended answer, and looks up facts itself instead of asking. It stops when
  nothing is left assumed. Eval case `evals/grill-me-1/`.
- **Plan-mode hook (Claude Code).** `hooks/hooks.json` runs `hooks/plan-grill.sh` on
  `UserPromptSubmit` while `permission_mode` is `plan`, and after `EnterPlanMode`. It adds context
  pointing to `eep:grill-me`, never blocks, and is skipped for subagents. The Codex manifest does
  not register the hook, so in Codex the skill triggers from its description only.

## 1.9.1 (2026-10-17)

- **Fix: `engineer-mindset` read less evidence on "brief" requests.** 1.9.0 added "read a reference
  only if it changes the verdict". On the release-gate case 2 of 3 runs then skipped
  `references/evidence-gates.md`, scoring a mean of 5.0/9 (no skill 4.5). The cap now limits what is
  written, not what is read. All 3 runs opened the reference and scored a mean of 6.0/9. Trade-off:
  "answer short" replies grew from 166–193 to 205–264 words.
- README before/after now shows per-finding counts across all runs of the shipped version, instead
  of the best single run.

## 1.9.0 (2026-10-17)

- **README rewritten for people who have not met EEP.** It now has a one-line pitch, three install
  paths tested from a clean config (Claude Code marketplace, Codex marketplace, `npx skills`), a
  with/without table from a real eval run, and a plain-language skill table. Companions moved
  into a collapsed section.
- **New public eval case `evals/engineer-mindset-release-gate/`.** It has a synthetic fixture, a
  9-point checklist and every scored run, with limits written next to the numbers.
- **`engineer-mindset` restores the five-line cap for "short answer" requests in `SKILL.md`.** The
  2026-10-16 restructure had moved the cap into `references/judgment.md`, which capacity questions
  never open. In blind-graded re-runs the short answers dropped from 270–420 words to 170–190 and
  scored a mean of 4.0/6 (v1.1 anchors: 4.33).
- **`sky-job` and `vietnamese-writing` leave the public plugin.** They depend on one team's GPU
  pool and on Vietnamese prose; references in other skills now point to "the cluster-job skill, if
  installed".
- Manifests: version 1.9.0, keywords for discovery, descriptions without the removed skills.


- **SessionStart skill-index hook removed.** Claude Code and Codex already list every skill with its
  description, so the hook only repeated that list (about 1k tokens at every start and compact).
- **`engineer-mindset` joins EEP and absorbs `design-decision`.** The former standalone skill is now
  `skills/engineer-mindset/modules/design-decision/MODULE.md`, next to the architecture,
  code-standards and module-design modules (module-design keeps its MIT licence from
  mattpocock/skills). The description leads with the design-decision triggers so routing is not
  lost. Team-only material (internal cases, agent-design, Python rules) sits in a gitignored
  `private/` folder and is read only when present.
- **`engineer-mindset` merges an internal principal-engineering doctrine**, gaps only (no new
  verdict scale or parallel principle list): outcome over output and a stopping condition up front
  (principle 1), uncertainty as a depth driver (2), agent reports are claims rather than evidence
  (8), holdout sets and honest denominators (9), post-release outcome ownership (10), and three
  red-team questions. References gain offered load vs completed throughput vs goodput (CCU, RPM and
  MAU do not convert), a scenario ↔ metrics ↔ infrastructure → decision shape for performance
  reports with "inconclusive" mapped to UNCHECKED, agent latency metrics beyond TTFT, expected value
  and stopping conditions, more organizational failure modes, mechanisms over heroics, and Case J.
- **`investigate` gains a `deployed service` mode**: error tracker first, logs and metrics around
  the timestamp, check ingestion before trusting "no logs", reproduce, stop at the telemetry wall.
  Team datasource IDs and query recipes live in `skills/investigate/private/team-debug.md`
  (gitignored).

- **`present` adds W3, showcase: a results page for people who are shown the numbers, not taught
  the mechanism** (evaluation, benchmark, status for leadership). `templates/showcase/render.py`
  turns one `report.json` into the page; every number lives in that file. Blocks: KPI cards, bars
  with a reference line, stacked error bars, composition, tables and confusion matrices, examples
  with word diffs, speaker timelines, tabs, drill-down. An optional second view, "samples to
  re-check", lists every sample with its audio player, reference against each model, metric and
  pass / fail, filters and sort; on timelines a playhead follows the audio and a click seeks
  (`--audio link` copies files next to the page, `--audio embed` inlines them). The build stops when
  evidence is missing: every KPI needs a direction and a denominator, the hero says what the metric
  is not, and the page ends in method + limits + a link to the source run. Light and dark; Be
  Vietnam Pro + IBM Plex Mono embedded (`kit/fonts-showcase.css`, ~200 KB, regenerated by `render.py` if missing; via the new
  `build.py --fonts`). Writing rules for this mode in `references/writing.md`.
- `build.py --shot` shoots pages taller than 8,192 px at 1x: at 2x Chrome blanked everything below
  ~9,950 px, so the look-at-the-screenshot gate passed on a page whose bottom was never seen.

- **`present` style questions end with "None fits — Claude designs it".** On that path the
  layout is free (no template copied); `kit/build.py`, a palette that passes
  `validate_palette.mjs`, and the delivery gate still apply.

- **`cards-readme` owns dataset column order and provenance.** The Hub viewer shows parquet schema
  order, so the rule now lives at write time: media (`audio`/`image`/`video`) first, then label,
  facets, per-row provenance, and ids/hashes/paths/`sample_rate` as one block at the end
  (`speaker_id` stays with the facets). Dataset cards get a `## Provenance and reproduction` table:
  code as `org/repo@commit` + command, exact model id, LLM + prompt at a commit, human reviewers by
  name with the Label Studio project/export, or `not recorded`.
- `check_card.py --data PARQUET|DIR|REPO_ID` fails on media not first or ids not last; `--type
  dataset` fails without a provenance section that names a commit, URL, or `not recorded`;
  `--selftest` asserts both.
## 1.8.0 (2026-10-04)

- **`present` ships a pre-built style gallery** (`skills/present/gallery/`), so showing the styles
  costs no tokens. `show.py DEST` rebuilds the sample pages from the templates into
  `DEST/present-gallery/` in about 2 s and copies the committed media (thumbnails, archify render,
  both videos, about 3.5 MB). `show.py --refresh-media` re-shoots the thumbnails after a template
  changes. `SKILL.md` now opens the gallery before asking the style question.
- New `templates/writing/kv-cache.abc.body.html`: the writing A / B / C sample, also in the self-test.
- Video V2 sample re-rendered with the IBM Plex fix.

## 1.7.1 (2026-10-03)

- **`present` restructured for reuse and lower token cost.** `SKILL.md` went from 12 KB to under
  6 KB. It now holds only the ask-first rule, the style catalogue, the workflow, the delivery gate,
  the hard rules, a file map and a maintenance section. Detail moved, unchanged, into
  `references/` (`writing.md`, `palettes.md`, `svg.md`, `infographic.md`), and each
  `templates/<style>/` folder gained a README.
- **Fixed: commands pointed at `/skills/…` when EEP is installed as a skills folder.**
  `CLAUDE_PLUGIN_ROOT` is unset there. `present` and `cards-readme` now use the skill's base
  directory.
- `kit/.ignore` keeps ripgrep (and any agent's repo-wide search) out of the 1.3 MB `fonts.css`.
  The infographic reference exists once, in `references/infographic.md`.
- **New `kit/selftest.py`** rebuilds every shipped example and exits 1 if any fails; CI runs it.
- `SKILL.md` forbids reading `kit/fonts.css` (1.3 MB). The private server URL lives in the user's
  global instructions, never in this repo.

## 1.7.0 (2026-10-03)

- **`present-html` → `present`.** The skill now covers four output types, with a style catalogue
  from one same-topic sample round: writing A/B/C (`kit/ste_check.py`), pages W1/W2, diagrams
  D1/D2 and narrated explainer video V1/V2. It asks the user to pick a style before building;
  the defaults are B, W1, D1 (concept) / D2 (architecture) and V1.
- **New look for pages: the reading room** (paper + Newsreader display serif; dark = deep green).
  It replaces Slate Light / Dracula in `kit/tokens.css`. Every existing component inherits it;
  `templates/specimen.body.html` exercises them all.
- **Diagram routing changed.** Explaining a concept → drawing sheet (`templates/sheet/`, white /
  blueprint). Architecture or stack design → archify. Previously every workflow, sequence and
  data-flow diagram went to archify.
- **New templates**: `templates/explorable/` (TOC + question cards + interactive panel) and
  `templates/video/` (`say` narration → `render(t)` page → headless Chrome frames → ffmpeg, in
  manim's palette, or V2 inked on a drawing sheet with IBM Plex), `templates/explorable-sheet/`
  (W2, light only as sampled) and `templates/archify/` (D2 example). Each ships the KV-cache
  worked example.
- **`build.py`**: new `--css` flag for a template's layout. The theme toggle is also inserted into
  a reading-room `.toc-ft`. The check now requires at least one toggle per page instead of one
  per `.hdr`.
- **`components.css`**: SVG `<text>` without its own `fill` now follows the theme. It used to
  paint black, which made it invisible on dark paper. Four more components were unreadable on
  dark paper and now contrast in both themes: `.diagram .step b`, `.amp .n.hot`, `.step` badges
  and `.grp-tab`.
- **Delivery gate**: open the `http://` URL in the user's browser yourself.

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
