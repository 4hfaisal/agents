---
skill-kind: custom
owner: Faisal Al Homodi
created: 2026-03-26
last-updated: 2026-03-28
category: [productivity, calendar, events]
name: event-tracker
description: Track conferences and events, check monthly for upcoming dates over next 12 months, and prompt user to decide on attendance. Web lookup event details and confirm with user before adding to events.md. Use when adding new events to track, running monthly reviews, or checking event status/attendance history. Maintains events.md in the workspace with URLs, status tracking, and decision log.
---

# Event Tracker

This skill manages Faisal's conference and event attendance planning, including monthly reminders to decide on upcoming events.

## Overview

The event tracker maintains a single source of truth at `workspace/events.md` that contains:
- List of events with URLs, locations, and typical timing
- Current attendance status for each event
- Decision log with reasoning

## File Structure

The `events.md` file uses a markdown table format:
- **Event Name**: Conference/event name
- **URL**: Official website
- **Location**: Event location
- **Typical Timing**: When it usually occurs (e.g., "Q1 annually", "June")
- **Status**: interested, planning, committed, declined, attended, cancelled
- **Notes**: Any additional context

## Workflow

### Adding a New Event

When Faisal mentions wanting to track an event:
1. Check if event already exists in events.md
2. Search the web for the event to find official information
3. Extract key details: name, official URL, location, typical timing, **and exact upcoming dates**
   - Always find and confirm specific dates (day, month, year) for the next occurrence
   - For events with multiple editions, list all upcoming editions with dates
   - Check if any upcoming events fall within the next 12 months
4. Present findings to Faisal and confirm this is the correct event and URL
   - Show event name, URL, location, typical timing, and exact upcoming dates
   - Highlight events occurring in the next 12 months
   - Wait for explicit confirmation before proceeding
5. Once confirmed, add event to events.md with all details including exact dates in Notes
6. Set status to `interested`
5. Once confirmed, add event to events.md with all details including exact dates in Notes
6. Set status to `interested`
7. Confirm to user that event has been added

### Monthly Review Process

Run monthly check (typically around mid-month):
1. Read events.md
2. Identify passed events (compare today's date with event dates in Notes)
   - For events that have passed (status: planning, committed, interested):
     - Ask Faisal: "Did you attend [Event Name]? What was your outcome?"
     - Update status: `attended` or `declined` based on response
     - Add outcome to Decision Log
3. For each `interested` event (non-passed):
   - Visit the URL to check upcoming dates in next 12 months
   - Find exact dates (day, month, year) for upcoming editions
   - If dates are announced, report to Faisal with details
   - Prompt: "Are you interested in attending [Event Name] on [Dates] in [Location]?"
4. Update status in events.md based on response:
   - If yes → `planning` (update Notes with exact dates)
   - If no → `declined` (add to decision log)
5. For `planning` events, check if actions are needed (registration, travel) and update exact dates if changed
6. Display summary with passed events marked with ⏰

### Updating Status

Always update the status field in events.md when decisions are made.
Add entries to the Decision Log section with date, decision, and reasoning.

### Checking Event Status

To review current tracked events:
1. Read events.md
2. Parse exact dates from Notes field for each event
3. Categorize events:
   - **Passed events** (date has passed): Mark with ⏰ emoji in display
   - **Upcoming events** (date is current or future)
4. Report summary by status:
   - Planning/committed events (upcoming)
   - Interested events (waiting for dates)
   - Declined events (recent decisions)
   - Attended events (history)
   - Passed events (recently completed)

### Handling Passed Events

When checking event status, identify events that have already passed:
1. Compare event dates with today's date
2. For events with status `planning`, `committed`, or `interested` that have passed:
   - Ask Faisal for the outcome: "Did you attend [Event Name]? What was the outcome?"
   - Update status accordingly:
     - If attended → `attended`
     - If didn't attend → `declined`
   - Add to Decision Log with the outcome
3. Always display passed events with a **⏰** indicator when showing the event list

## Display Indicators

Use these emojis to visually indicate event state:
- ⏰ = Event date has passed
- 📅 = Upcoming event with confirmed dates
- 🎯 = Currently in planning phase
- ✅ = Committed/registered
- ❌ = Declined/decided not to attend

## Notes

- Keep the table sorted by upcoming date for planning/committed events
- When visiting event URLs for date checks, verify information is current
- Decision log is valuable for tracking patterns and avoiding repeat research
- Typical timing field helps with proactive date checking even when official dates aren't announced
