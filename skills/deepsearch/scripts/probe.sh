#!/usr/bin/env bash
# Health probe for a GitHub repo candidate: facts only, the judgement stays with the reader.
# Usage: bash probe.sh owner/repo   ·  read the output against references/prior-art-audit.md
set -uo pipefail
R="${1:?usage: probe.sh owner/repo}"

gh repo view "$R" --json isArchived,isFork,licenseInfo,createdAt,pushedAt,latestRelease,stargazerCount,forkCount,diskUsage,description \
  --jq '"archived=\(.isArchived) fork=\(.isFork) license=\(.licenseInfo.key // "NONE") created=\(.createdAt[0:10]) lastPush=\(.pushedAt[0:10]) release=\(.latestRelease.tagName // "NONE")@\((.latestRelease.publishedAt // "-")[0:10]) stars=\(.stargazerCount) forks=\(.forkCount) sizeKB=\(.diskUsage)"' || exit 1

# Bus factor: commits per contributor, biggest first. "175,31,7,4,…" = one author's project.
echo "contributors: $(gh api "repos/$R/contributors?per_page=20" --jq '[.[].contributions] | join(",")' 2>/dev/null || echo '?')"

# CI that only renders a badge or a star chart is not CI.
echo "ci: $(gh api "repos/$R/contents/.github/workflows" --jq '[.[].name] | join(",")' 2>/dev/null || echo 'NONE')"

# Tree API, not code search: code search misses paths and needs different auth scopes.
echo "test files: $(gh api "repos/$R/git/trees/HEAD?recursive=1" --jq '[.tree[].path | select(test("(^|/)(tests?|spec|__tests__)/"))] | length' 2>/dev/null || echo '?')"

# comments=0 on every recent issue means nobody is answering, whatever the star count says.
echo "-- last 5 issues --"
gh api "repos/$R/issues?state=all&per_page=8&sort=created&direction=desc" \
  --jq '.[] | select(.pull_request|not) | "  #\(.number) \(.created_at[0:10]) comments=\(.comments) \(.state)\(if .closed_at then " closed="+.closed_at[0:10] else "" end)"' 2>/dev/null | head -5

# Texture: what the last commits actually touch. A wall of "update"/badge/sponsor commits is a tell.
echo "-- last 10 commit subjects --"
gh api "repos/$R/commits?per_page=10" --jq '.[] | "  " + (.commit.message | split("\n")[0])' 2>/dev/null
