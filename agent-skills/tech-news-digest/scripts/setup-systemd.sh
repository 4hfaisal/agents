#!/bin/bash

# Setup Systemd Timer for Tech News Digest

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

cd "$SKILL_DIR"

echo "⏰ Setting up Tech News Digest Systemd Timer"
echo "============================================"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  Please run with sudo for systemd installation"
    exit 1
fi

# Service and timer files
SERVICE_FILE="$SKILL_DIR/tech-news-digest.service"
TIMER_FILE="$SKILL_DIR/tech-news-digest.timer"
MAIN_SCRIPT="$SCRIPT_DIR/daily-digest.sh"

# Create service file
cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Tech News Digest Service
After=network.target

[Service]
Type=oneshot
ExecStart=$MAIN_SCRIPT
WorkingDirectory=$SKILL_DIR
User=faisal
Group=faisal
StandardOutput=journal
StandardError=journal

# Environment variables
Environment=PYTHONUNBUFFERED=1
Environment=LC_ALL=en_US.UTF-8

# Restart on failure (for oneshot)
Restart=on-failure
RestartSec=60

[Install]
WantedBy=multi-user.target
EOF

# Create timer file (7:00 AM Riyadh time = 4:00 AM UTC)
cat > "$TIMER_FILE" << EOF
[Unit]
Description=Daily Tech News Digest Timer
After=network.target

[Timer]
OnCalendar=*-*-* 04:00:00
Persistent=true
AccuracySec=1min
Unit=tech-news-digest.service

[Install]
WantedBy=timers.target
EOF

echo "📋 Created systemd files:"
echo "   Service: $SERVICE_FILE"
echo "   Timer: $TIMER_FILE"

# Copy to systemd directory
echo "📁 Installing systemd files..."
cp "$SERVICE_FILE" /etc/systemd/system/
cp "$TIMER_FILE" /etc/systemd/system/

# Reload systemd
echo "🔄 Reloading systemd..."
systemctl daemon-reload

# Enable and start timer
echo "🚀 Enabling and starting timer..."
systemctl enable tech-news-digest.timer
systemctl start tech-news-digest.timer

echo "📊 Checking timer status..."
systemctl status tech-news-digest.timer --no-pager

echo ""
echo "✅ Tech News Digest Timer Setup Complete!"
echo ""
echo "📅 Schedule: Daily at 7:00 AM Riyadh Time (4:00 AM UTC)"
echo "📧 Email: Will be sent to faisal.homodi@gmail.com"
echo "📋 Sources: Configured in references/sources.yaml"
echo ""
echo "🔧 Management Commands:"
echo "   View timer status:   systemctl status tech-news-digest.timer"
echo "   View service logs:   journalctl -u tech-news-digest.service -f"
echo "   Test manually:       $MAIN_SCRIPT"
echo "   Stop timer:          systemctl stop tech-news-digest.timer"
echo "   Disable timer:       systemctl disable tech-news-digest.timer"
echo ""
echo "📝 First digest will be sent: Tomorrow at 7:00 AM Riyadh Time"