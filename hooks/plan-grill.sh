#!/usr/bin/env bash
# Plan mode -> eep:grill-me. Fires on UserPromptSubmit while permission_mode is "plan"
# (user toggled plan mode) and on PostToolUse of EnterPlanMode (the model entered it).
# Main conversation only. Adds context only; never blocks. No jq: grep is enough for two fields.
input=$(cat)
# Subagents cannot talk to the user; grilling belongs to the main conversation.
printf '%s' "$input" | grep -q '"agent_id"' && exit 0
event=$(printf '%s' "$input" | grep -oE '"hook_event_name"[[:space:]]*:[[:space:]]*"[A-Za-z]+"' | head -1 | sed -E 's/.*"([A-Za-z]+)"$/\1/')
case "$event" in
  UserPromptSubmit)
    printf '%s' "$input" | grep -qE '"permission_mode"[[:space:]]*:[[:space:]]*"plan"' || exit 0 ;;
  PostToolUse) ;;
  *) exit 0 ;;
esac
msg="Plan mode is active, so the EEP grill-me rule applies: the first planning step is the Skill tool call eep:grill-me, before the plan file is written. If a grill-me session is already running in this conversation, it continues instead of restarting. The plan is written only after the grilling frontier is empty or the user declines more questions."
printf '{"hookSpecificOutput":{"hookEventName":"%s","additionalContext":"%s"}}\n' "$event" "$msg"
