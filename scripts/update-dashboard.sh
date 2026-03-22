#!/usr/bin/env bash
set -euo pipefail

# Dashboard Update — generates markdown status and optionally updates a GitHub issue
TASKS_DIR="tasks"

count_files() {
  local dir="$1"
  if [ -d "$dir" ]; then
    find "$dir" -name '*.md' -type f | wc -l | tr -d ' '
  else
    echo 0
  fi
}

PENDING=$(count_files "${TASKS_DIR}/epics/pending")
APPROVED=$(count_files "${TASKS_DIR}/epics/approved")
COMPLETE=$(count_files "${TASKS_DIR}/epics/complete")
BACKLOG=$(count_files "${TASKS_DIR}/tickets/backlog")
IN_PROGRESS=$(count_files "${TASKS_DIR}/tickets/in-progress")
DONE=$(count_files "${TASKS_DIR}/tickets/done")

cat <<DASHBOARD
# Pipeline Dashboard

_Updated: $(date -u '+%Y-%m-%d %H:%M UTC')_

## Summary

| Category | Pending | Active | Complete |
|----------|---------|--------|----------|
| Epics    | $PENDING | $APPROVED | $COMPLETE |
| Tickets  | $BACKLOG | $IN_PROGRESS | $DONE |

## Active Tickets

$(if [ -d "${TASKS_DIR}/tickets/in-progress" ]; then
  for f in "${TASKS_DIR}/tickets/in-progress"/*.md; do
    [ -f "$f" ] || continue
    id=$(basename "$f" .md)
    title=$(grep -m1 '^title:' "$f" | sed 's/title: *//; s/^"//; s/"$//')
    echo "- **$id**: $title"
  done
else
  echo "_None_"
fi)

DASHBOARD
