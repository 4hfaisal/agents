#!/bin/bash
# Monthly Event Review Helper
# This script helps perform monthly reviews of tracked events

WORKSPACE="${1:-$HOME/.openclaw/workspace-emma}"
EVENTS_FILE="$WORKSPACE/events.md"
MONTHS_AHEAD="${2:-12}"

echo "=== Monthly Event Review ==="
echo "Looking ahead $MONTHS_AHEAD months from: $(date +%Y-%m-%d)"
echo ""

if [ ! -f "$EVENTS_FILE" ]; then
  echo "ERROR: events.md not found at $EVENTS_FILE"
  exit 1
fi

echo "Events to check:"
echo "- Extract events with status 'interested' or 'planning'"
echo "- Visit each URL to check dates in next $MONTHS_AHEAD months"
echo "- Prompt user for attendance decisions"
echo "- Update status in events.md"
