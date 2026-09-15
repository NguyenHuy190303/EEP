---
name: sentry-cli
version: 0.42.2
description: Guide for using the Sentry CLI to inspect issues, events, traces, spans, logs, projects, organizations, releases, dashboards, and API resources. Use whenever a task needs Sentry data or Sentry CLI authentication, targeting, troubleshooting, or mutations; prefer dedicated CLI commands before raw API calls.
requires:
  bins: ["sentry"]
  auth: true
---

# Sentry CLI

Use the `sentry` CLI directly. It normally detects authentication, organization, and project from
the working directory; add explicit targets only when detection fails or selects the wrong scope.

## Operating rules

- Prefer a dedicated command such as `sentry issue view`, `sentry trace view`, or
  `sentry log list` before `sentry api`.
- Use `sentry schema` to discover API resources and endpoints.
- Use `--json --fields ...` for machine-readable, bounded output and `--limit` for lists.
- Run `<command> --help` before inventing a flag or field.
- Verify the selected organization/project before a mutation.
- Never print, copy, or persist authentication tokens. Let the CLI manage credentials.
- Get user confirmation immediately before destructive commands such as `project delete` or
  starting a trial.

Exit-code ranges: 10–19 auth, 20–29 input, 30–39 API, 40–49 unavailable feature, 50–59 operation,
and 60–69 command-specific. Read stderr before deciding whether to retry.

## Common workflows

### Investigate an issue

```bash
sentry issue list --query "is:unresolved" --limit 5
sentry issue view PROJECT-123
sentry issue explain PROJECT-123
sentry issue plan PROJECT-123
```

Use the short issue ID (`PROJECT-123`), not the numeric database ID.

### Trace performance and logs

```bash
sentry trace list --period 1h --limit 5
sentry trace view <trace-id>
sentry span list <trace-id>
sentry trace logs <trace-id>
sentry log list --query "severity:error"
```

### Capture events locally

```bash
sentry local run -- npm run dev
sentry local -f ai
```

Without a DSN, Spotlight events stay local. With a DSN, verify the actual SDK configuration before
making privacy or quota claims.

### Manage a release

```bash
sentry release create <org>/<version> --project <project>
sentry release set-commits <org>/<version> --auto
sentry release finalize <org>/<version>
sentry release deploy <org>/<version> production
```

The positional value is `<org-slug>/<version>` and the version must match `Sentry.init({ release })`.
`--auto` needs a repository integration and a full local Git checkout; use `--local` when that is
the intended source of commit history.

### Use an uncovered API

```bash
sentry schema <resource>
sentry api /api/0/organizations/<org>/
```

Use `sentry api` only after confirming that a dedicated command does not expose the needed data.

## Load references progressively

Read only the file matching the requested command family:

- Identity and scope: `references/auth.md`, `references/org.md`, `references/project.md`,
  `references/team.md`.
- Investigation: `references/issue.md`, `references/event.md`, `references/trace.md`,
  `references/span.md`, `references/log.md`, `references/replay.md`, `references/feedback.md`.
- Delivery: `references/release.md`, `references/build.md`, `references/sourcemap.md`,
  `references/debug-files.md`, `references/proguard.md`, `references/dart-symbol-map.md`,
  `references/react-native.md`, `references/code-mappings.md`.
- Operations: `references/alert.md`, `references/monitor.md`, `references/dashboard.md`,
  `references/snapshots.md`.
- Discovery and advanced use: `references/schema.md`, `references/api.md`,
  `references/explore.md`, `references/platform.md`, `references/info.md`, `references/init.md`,
  `references/cli.md`, `references/local.md`, `references/conversation.md`, `references/repo.md`,
  `references/trial.md`.

When a reference and live `--help` output disagree, treat the installed CLI as the source of truth
and report the version observed.

## Output contract

Lead with the requested result. Include the exact command, target scope, and material limitations
when they support the conclusion. Do not claim a Sentry state changed unless output confirmed it.
