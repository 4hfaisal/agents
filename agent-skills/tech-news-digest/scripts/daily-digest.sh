#!/bin/bash

# Daily Tech News Digest Script
# Main entry point for collecting, summarizing, and sending tech news

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_DIR="$SKILL_DIR/references"
TEMPLATE_DIR="$SKILL_DIR/templates"

cd "$SKILL_DIR"

echo "📰 Starting Tech News Digest - $(date)"
echo "========================================"

# Load configuration
if [ -f "$CONFIG_DIR/sources.yaml" ]; then
    echo "✅ Loaded sources configuration"
else
    echo "❌ Missing sources.yaml configuration"
    exit 1
fi

# Check dependencies
echo "🔍 Checking dependencies..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is required"
    exit 1
fi

if ! command -v /home/faisal/.composio/composio &> /dev/null; then
    echo "❌ Composio CLI is required"
    exit 1
fi

# Run the Python news collector
echo "🚀 Running news collection and processing..."
python3 "$SCRIPT_DIR/news-collector.py"

if [ $? -eq 0 ]; then
    echo "✅ News collection completed successfully"
else
    echo "❌ News collection failed"
    exit 1
fi

# Run LinkedIn monitor
echo "👔 Running LinkedIn monitoring..."
python3 "$SCRIPT_DIR/linkedin-monitor.py"

if [ $? -eq 0 ]; then
    echo "✅ LinkedIn monitoring completed"
else
    echo "⚠️  LinkedIn monitoring had issues (continuing)"
fi

# Check if we have articles to send
if [ -f "$SCRIPT_DIR/output/digest.json" ]; then
    echo "📊 Found $(jq '.articles | length' "$SCRIPT_DIR/output/digest.json") articles"
    
    # Send email via Composio
    echo "📧 Sending email digest..."
    python3 "$SCRIPT_DIR/send-email.py"
    
    if [ $? -eq 0 ]; then
        echo "✅ Email sent successfully!"
        echo "🎉 Daily tech news digest completed"
        exit 0
    else
        echo "❌ Failed to send email"
        exit 1
    fi
else
    echo "⚠️  No articles found to send"
    echo "💤 Skipping email send"
    exit 0
fi