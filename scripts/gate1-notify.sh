#!/usr/bin/env bash
set -euo pipefail

# Gate 1 Notification — posts review link to dashboard issue
EPIC_SLUG="${1:?Usage: gate1-notify.sh <epic-slug>}"
EPIC_FILE="tasks/epics/pending/${EPIC_SLUG}.md"

if [ ! -f "$EPIC_FILE" ]; then
  echo "Epic file not found: $EPIC_FILE"
  exit 1
fi

TITLE=$(grep -m1 '^title:' "$EPIC_FILE" | sed 's/title: *//; s/^"//; s/"$//')
EFFORT=$(grep -m1 '^effort:' "$EPIC_FILE" | sed 's/effort: *//')
IMPACT=$(grep -m1 '^impact:' "$EPIC_FILE" | sed 's/impact: *//')

echo "Gate 1 review needed for epic: $TITLE"
echo "  Effort: $EFFORT | Impact: $IMPACT"
echo "  Review the epic file and change status to 'approved' to proceed."
