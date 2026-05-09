# Tech News Digest Skill

A custom OpenClaw skill that automatically collects, summarizes, and emails daily tech news from multiple sources including LinkedIn company updates.

## 📋 Features

- **Multi-source aggregation**: Collects news from RSS feeds
- **LinkedIn integration**: Monitors company pages for official updates
- **Collapsible summaries**: Email shows first 2 lines with "Show more" toggle
- **AI-powered summarization**: Creates concise article summaries
- **HTML email templates**: Professional email formatting
- **Customizable sources**: Easy to add/remove news sources
- **Keyword filtering**: Focus on specific tech topics
- **Automatic scheduling**: Runs daily via systemd timers

## 🚀 Quick Start

### 1. Test the workflow
```bash
cd ~/.openclaw/workspace/skills/tech-news-digest
./tech-news-test
```

### 2. Customize news sources
Edit: `references/sources.yaml`

### 3. Configure LinkedIn companies
Edit: `references/linkedin-companies.yaml`

### 4. Set up automatic scheduling
```bash
# Run with sudo
sudo bash scripts/setup-systemd.sh
```

## 📊 Configuration

### Sources (references/sources.yaml)
```yaml
sources:
  - name: "TechCrunch"
    url: "https://techcrunch.com/news/"
    type: "rss"
    category: "Startups & Tech News"
    priority: 10

  - name: "Hacker News"
    url: "https://news.ycombinator.com/rss"
    # RSS feeds
    category: "Developer News"
    priority: 9
```

### LinkedIn Companies (references/linkedin-companies.yaml)
```yaml
companies:
  - name: "OpenAI"
    linkedin_url: "https://linkedin.com/company/openai"
    priority: 10

  - name: "GitHub"
    linkedin_url: "https://linkedin.com/company/github"
    priority: 9
```

### Email Settings
```yaml
email:
  recipient: "your-email@gmail.com"
  subject_prefix: "Tech News Digest"
  max_items_per_source: 5
  max_total_items: 15
```

## 🔧 Manual Testing

```bash
# Create sample data and send test email
python3 scripts/test-simple.py
python3 scripts/send-email.py

# Run full workflow test
./tech-news-test
```

## ⚙️ Automatic Scheduling

The skill uses systemd timers for automatic daily execution:

- **Schedule**: Daily at 7:00 AM Riyadh time (4:00 AM UTC)
- **Service**: `tech-news-digest.service`
- **Timer**: `tech-news-digest.timer`

### Management Commands
```bash
# View timer status
systemctl status tech-news-digest.timer

# View service logs
journalctl -u tech-news-digest.service -f

# Manual trigger
bash scripts/daily-digest.sh
```

## 📁 File Structure

```
tech-news-digest/
├── SKILL.md                 # Skill metadata (custom tagged)
├── README.md                # This file
├── scripts/
│   ├── daily-digest.sh      # Main workflow script
│   ├── news-collector.py    # RSS fetching & processing
│   ├── linkedin-monitor.py  # LinkedIn company monitoring
│   ├── send-email.py        # Email composition & sending
│   ├── setup-systemd.sh     # Systemd timer installation
│   ├── test-simple.py       # Sample data generator
│   └── output/              # Generated digest files
├── references/
│   ├── sources.yaml         # News source configuration
│   ├── linkedin-companies.yaml  # LinkedIn companies to monitor
│   └── instructions.md      # Processing guidelines
├── templates/
│   └── email.html          # HTML email template (collapsible)
└── tech-news-test           # Complete workflow test
```

## 🛠️ Dependencies

- **Python 3**: Built-in XML parser (no external packages needed)
- **Composio CLI**: For email sending (`~/.composio/composio`)
- **Active Gmail connection**: Via Composio

## 🔄 GitHub Sync

This skill is tagged with `skill-kind: custom` and will be automatically synchronized with your GitHub skills repository using the `agents-config-sync` skill.

## 📝 Customization

### Adding New Sources
1. Edit `references/sources.yaml`
2. Add new RSS feed entries
3. Set appropriate category and priority

### Adding LinkedIn Companies
1. Edit `references/linkedin-companies.yaml`
2. Add company LinkedIn URLs
3. Set priority for sorting

### Modifying Email Template
1. Edit `templates/email.html`
2. Customize HTML and CSS styling
3. Update collapsible section behavior

### Changing Schedule
1. Edit `tech-news-digest.timer`
2. Modify the `OnCalendar` setting
3. Run `systemctl daemon-reload`

## 🐛 Troubleshooting

### Common Issues

1. **No articles found**: Check RSS feed URLs in `sources.yaml`
2. **Email not sent**: Verify Composio Gmail connection
3. **Timer not running**: Check systemd timer status
4. **LinkedIn updates missing**: Configure companies in `linkedin-companies.yaml`

### Logs
```bash
# View service logs
journalctl -u tech-news-digest.service

# View recent runs
journalctl -u tech-news-digest.service --since "1 hour ago"
```

## 📧 Support

For issues with this skill, check:
- Service logs: `journalctl -u tech-news-digest.service`
- Email configuration: `references/sources.yaml`
- LinkedIn configuration: `references/linkedin-companies.yaml`
- Composio status: `~/.composio/composio connections list`

---

**Skill Tag**: `skill-kind: custom`  
**GitHub Sync**: Compatible with `agents-config-sync`  
**Status**: ✅ Operational