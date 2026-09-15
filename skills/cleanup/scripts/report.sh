#!/usr/bin/env bash
# What is holding a port, a process, or disk on THIS machine. Reports only — kills nothing.
# Usage: bash report.sh
set -uo pipefail
U=$(id -u); ME=$(id -un)

echo "=== Ports listening (owned by $ME) ==="
printf '  %-12s %-7s %s\n' COMMAND PID ADDRESS
lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null | awk -v me="$ME" 'NR>1 && $3==me {printf "  %-12s %-7s %s\n", $1, $2, $9}' | sort -u -k3 | head -40

echo
echo "=== Processes attached to a terminal (what a shell left behind) ==="
# TTY != ?? is the reliable tell: app helpers and daemons have no controlling terminal.
# A dev server, a tunnel, a training run started in a terminal shows up here.
printf '  %-7s %-9s %-11s %s\n' PID TTY ELAPSED COMMAND
ps -eo pid,tty,etime,command -U "$U" 2>/dev/null \
  | awk 'NR>1 && $2 != "??"' | grep -vE '(^| )(ps|awk|grep|login -pf|-?zsh|-?bash)( |$)' \
  | awk '{pid=$1; tty=$2; et=$3; $1=$2=$3=""; sub(/^ +/,""); printf "  %-7s %-9s %-11s %.90s\n", pid, tty, et, $0}' | head -25

echo
echo "=== tmux ==="
tmux ls 2>/dev/null | sed 's/^/  /' || echo "  no tmux server"

echo
echo "=== Docker / OrbStack ==="
if command -v docker >/dev/null && docker info >/dev/null 2>&1; then
  docker system df | sed 's/^/  /'
  echo
  echo "  -- not running (candidates) --"
  docker ps -a --filter status=exited --filter status=created \
    --format '    {{.Names}}\t{{.Status}}\t{{.Image}}' | head -20
  echo
  echo "  -- RUNNING: never stopped without asking, may hold unsaved state --"
  docker ps --format '    {{.Names}}\t{{.Status}}\t{{.Image}}'
  echo
  echo "  -- volumes: LINKS=0 means no container references it NOW, not that it is junk --"
  docker system df -v 2>/dev/null | sed -n '/Local Volumes space usage/,/^$/p' | sed 's/^/    /' | head -35
else
  echo "  docker not reachable (OrbStack not running?)"
fi

echo
echo "Read against SKILL.md: safe / ask / never. Nothing above has been deleted."
