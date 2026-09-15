#!/usr/bin/env bash
# SessionStart: print a one-line "use when" index of EEP skills so the host checks them before ad-hoc work.
# Reads each SKILL.md frontmatter; no workflow is forced. ponytail: description clipped at first sentence.
root="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
echo "EEP skills (invoke by name, eep:<name> when namespaced) — check this list before ad-hoc work:"
for f in "$root"/skills/*/SKILL.md; do
  name=$(sed -n 's/^name: *//p' "$f" | head -1)
  desc=$(awk '/^---/{c++; next} c==1 && /^description:/{sub(/^description: */,""); d=$0; getline; while ($0 !~ /^[a-z-]+:/ && $0 !~ /^---/) { d=d" "$0; getline }; print d; exit }' "$f" | tr -s ' ' | sed 's/^"//; s/"$//' | cut -d. -f1)
  printf -- "- %s: %s.\n" "$name" "$desc"
done
