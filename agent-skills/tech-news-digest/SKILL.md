---
skill-kind: custom
owner: Faisal Al Homodi
created: 2026-04-30
last-updated: 2026-04-30
category: [productivity, news, automation, email]
name: tech-news-digest
description: Daily tech news digest that collects, summarizes, and emails tech news from multiple sources
---

# Skill: Tech News Digest

Automated daily tech news collection, summarization, and email delivery.

## Description

This skill automatically gathers tech news from various sources, summarizes the content, and sends a formatted HTML email digest every day at 7:00 AM Riyadh time (4:00 AM UTC).

## Features

- **Multi-source aggregation**: Collects news from RSS feeds, tech blogs, and news sites
- **LinkedIn integration**: Monitors company pages for official news and updates
- **Collapsible summaries**: Email shows first 2 lines with "Show more" toggle
- **AI summarization**: Uses language models to create concise summaries
- **HTML email templates**: Professional email formatting with source attribution
- **Customizable sources**: Easy to add/remove news sources
- **Keyword filtering**: Focus on specific tech topics or companies
- **Automatic scheduling**: Runs daily via systemd timers

## Usage

### Run Daily Digest
```bash
tech-news-daily
```

### Test Email (Manual Run)
```bash
tech-news-test
```

### Configure Sources
Edit: `references/sources.yaml`

### Customize Email Template
Edit: `templates/email.html`

## Configuration Files

- `scripts/daily-digest.sh` - Main execution script
- `scripts/news-collector.py` - News gathering and processing
- `references/sources.yaml` - News source configuration
- `references/instructions.md` - Processing instructions
- `templates/email.html` - HTML email template
- `tech-news-digest.service` - Systemd service
- `tech-news-digest.timer` - Systemd timer

## Setup

1. **Install dependencies**: Python packages for RSS parsing
2. **Configure sources**: Edit `references/sources.yaml`
3. **Set up email**: Ensure Composio Gmail connection is active
4. **Install timer**: Run setup script for automatic scheduling

## GitHub Sync

This skill is tagged with `skill-kind: custom` and will be automatically synchronized with your GitHub skills repository using the `agents-config-sync` skill.

## Examples

```bash
# Manual test run
cd ~/.openclaw/workspace/skills/tech-news-digest
python3 scripts/news-collector.py

# Install automatic scheduling
bash scripts/setup-systemd.sh
```

## Notes

- Requires active Composio Gmail connection
- Customize sources based on your tech interests
- HTML template can be modified for branding
- Summary quality depends on source content availability