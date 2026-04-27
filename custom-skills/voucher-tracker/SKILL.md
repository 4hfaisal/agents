---
skill-kind: custom
owner: Faisal Al Homodi
created: 2026-03-28
last-updated: 2026-03-28
category: [personal, finance, tracking]
name: voucher-tracker
description: Track voucher numbers, issuer names, and expiry dates provided by the user. Add new vouchers, view all active vouchers, and report any vouchers expiring within the next 6 months. Use when the user wants to add a voucher, check their voucher list, or get an expiry report.
---

# Voucher Tracker

## Overview

Maintains a persistent list of vouchers in `vouchers.md` inside this skill folder. Each voucher has a number, issuer, expiry date, and optional notes. Supports adding new vouchers, listing all vouchers, and reporting those expiring within the next 6 months.

## Voucher Data File

All vouchers are stored in:
```
/Users/faisal/Claude Code/skills/voucher-tracker/vouchers.md
```

Create this file if it does not exist using the template in the **Data Format** section below.

## Workflow

### Adding a voucher
When the user provides voucher details:
1. Read `vouchers.md`
2. Append a new row to the table with: voucher number, issuer, expiry date, status (`Active`), and any notes
3. Write the updated file back
4. Confirm to the user: voucher number, issuer, and expiry date

### Listing all vouchers
1. Read `vouchers.md`
2. Display the full table sorted by expiry date (soonest first)

### Expiry report (next 6 months)
When the user asks for an expiry report or asks which vouchers are expiring soon:
1. Read `vouchers.md`
2. Calculate the date 6 months from today
3. Filter all rows where `Expiry Date` falls between today and that date and `Status = Active`
4. Sort results by expiry date ascending (most urgent first)
5. Present as a formatted table with a count and a warning for any expiring within 30 days
6. If no vouchers are expiring in 6 months, say so explicitly

### Marking a voucher as used/expired
When the user says a voucher has been redeemed or expired:
1. Find the matching row by voucher number
2. Update `Status` to `Used` or `Expired`
3. Write the updated file back
4. Confirm the change

## Data Format

`vouchers.md` uses this structure:

```markdown
# Vouchers

| Voucher Number | Issuer | Expiry Date | Status | Notes |
|----------------|--------|-------------|--------|-------|
| EXAMPLE-001 | Acme Corp | 2026-12-31 | Active | Gift card |
```

- **Voucher Number** — exact code or reference number as provided
- **Issuer** — company or person who issued the voucher
- **Expiry Date** — ISO format `YYYY-MM-DD`
- **Status** — `Active`, `Used`, or `Expired`
- **Notes** — optional free text (leave blank if none)

## Expiry Warning Thresholds

| Timeframe | Action |
|-----------|--------|
| ≤ 30 days | Flag as `⚠️ URGENT` |
| 31–90 days | Flag as `🔔 Soon` |
| 91–180 days | Flag as `📅 Upcoming` |

## Example Interactions

```
"Add voucher VC-2026-88X from Emirates, expires 2026-09-15"
"Show me all my vouchers"
"Which vouchers are expiring in the next 6 months?"
"Mark voucher VC-2026-88X as used"
```

## Notes

- Always use ISO date format `YYYY-MM-DD` for expiry dates
- If the user provides a date in another format, convert it before saving
- Never delete rows — use `Status` to mark vouchers as `Used` or `Expired`
- Today's date must be used as the reference point for all expiry calculations
