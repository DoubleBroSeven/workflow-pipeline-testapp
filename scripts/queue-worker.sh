#!/usr/bin/env bash
set -euo pipefail

# Queue Worker — finds the next free ticket and creates its branches
# A ticket is free when: ac_status=ready AND (depends_on=[] OR all deps in done/)

TASKS_DIR="tasks/tickets"
BACKLOG="${TASKS_DIR}/backlog"
IN_PROGRESS="${TASKS_DIR}/in-progress"
DONE="${TASKS_DIR}/done"

# Ensure we're on development
git checkout development 2>/dev/null || true
git pull origin development --rebase 2>/dev/null || true

# Find next free ticket
find_next_free() {
  for ticket_file in "${BACKLOG}"/*.md; do
    [ -f "$ticket_file" ] || continue

    local ac_status
    ac_status=$(grep -m1 '^ac_status:' "$ticket_file" | sed 's/ac_status: *//')
    [ "$ac_status" = "ready" ] || continue

    local deps
    deps=$(grep -m1 '^depends_on:' "$ticket_file" | sed 's/depends_on: *//')
    if [ "$deps" = "[]" ] || [ -z "$deps" ]; then
      echo "$ticket_file"
      return
    fi

    # Check if all deps are in done/
    local all_done=true
    for dep_id in $(echo "$deps" | tr -d '[]' | tr ',' ' '); do
      dep_id=$(echo "$dep_id" | tr -d ' "'"'"'')
      [ -z "$dep_id" ] && continue
      if [ ! -f "${DONE}/${dep_id}.md" ]; then
        all_done=false
        break
      fi
    done

    if [ "$all_done" = true ]; then
      echo "$ticket_file"
      return
    fi
  done
}

TICKET_FILE=$(find_next_free)
if [ -z "${TICKET_FILE:-}" ]; then
  echo "No free tickets found."
  exit 0
fi

TICKET_ID=$(basename "$TICKET_FILE" .md)
EPIC_ID=$(grep -m1 '^epic:' "$TICKET_FILE" | sed 's/epic: *//')
BRANCH=$(grep -m1 '^branch:' "$TICKET_FILE" | sed 's/branch: *//')
TODAY=$(date -u +%Y-%m-%d)

echo "Picking up ticket: $TICKET_ID (epic: $EPIC_ID)"

# Move ticket to in-progress
mkdir -p "$IN_PROGRESS"
mv "$TICKET_FILE" "${IN_PROGRESS}/${TICKET_ID}.md"
sed -i "s/^status: backlog/status: in-progress/" "${IN_PROGRESS}/${TICKET_ID}.md"
sed -i "s/^started: .*/started: \"$TODAY\"/" "${IN_PROGRESS}/${TICKET_ID}.md"

# Commit ticket move on development
git add tasks/
git commit -m "queue: start $TICKET_ID"
git push origin development

# Create/sync feature branch
EPIC_BRANCH="feature/$EPIC_ID"
git fetch origin "$EPIC_BRANCH" 2>/dev/null || true
if git rev-parse --verify "origin/$EPIC_BRANCH" >/dev/null 2>&1; then
  git checkout "$EPIC_BRANCH"
  git rebase origin/development
else
  git checkout -b "$EPIC_BRANCH" origin/development
fi
git push -u origin "$EPIC_BRANCH"

# Create ticket branch
git checkout -b "$BRANCH" "$EPIC_BRANCH"
git push -u origin "$BRANCH"

echo "Ready for implementation on branch: $BRANCH"
