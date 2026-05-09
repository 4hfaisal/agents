#!/usr/bin/env python3
"""
Email Sender for Tech News Digest
Sends formatted HTML email via Composio CLI
"""

import json
import subprocess
import tempfile
import os
from datetime import datetime
from pathlib import Path
import yaml
import re
from typing import Dict, Any

# Configuration
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
CONFIG_DIR = SKILL_DIR / "references"
TEMPLATE_DIR = SKILL_DIR / "templates"
OUTPUT_DIR = SCRIPT_DIR / "output"

def load_config():
    """Load configuration"""
    config_path = CONFIG_DIR / "sources.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def load_digest():
    """Load collected digest"""
    digest_path = OUTPUT_DIR / "digest.json"
    with open(digest_path, 'r') as f:
        return json.load(f)

def render_email_template(digest: dict) -> str:
    """Render HTML email template"""
    template_path = TEMPLATE_DIR / "email.html"
    
    with open(template_path, 'r') as f:
        template = f.read()
    
    # Group articles by category
    articles_by_category = {}
    for article in digest['articles']:
        category = article.get('category', 'General')
        if category not in articles_by_category:
            articles_by_category[category] = []
        articles_by_category[category].append(article)
    
    # Get LinkedIn articles
    linkedin_articles = digest.get('linkedin_articles', [])
    
    # Prepare context
    context = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'item_count': str(len(digest['articles']) + len(linkedin_articles)),
        'generated_at': datetime.now().isoformat(),
        'articles_by_category': articles_by_category,
        'linkedin_articles': linkedin_articles
    }
    
    # Render template
    return render_template(template, context)

def render_template(template: str, context: Dict[str, Any]) -> str:
    """Render template with context"""
    
    # Replace simple variables
    for key, value in context.items():
        if isinstance(value, str):
            template = template.replace(f'{{{{{key}}}}}', value)
        elif isinstance(value, (int, float)):
            template = template.replace(f'{{{{{key}}}}}', str(value))
    
    # Handle category loops
    if 'articles_by_category' in context:
        categories_html = ""
        for category, articles in context['articles_by_category'].items():
            category_html = f"""
            <div class="section">
                <h2>{category}</h2>
                {render_articles(articles)}
            </div>
            """
            categories_html += category_html
        
        template = template.replace(
            "{% for category, articles in articles_by_category.items() %}", 
            categories_html
        )
    
    # Handle LinkedIn section
    linkedin_articles = context.get('linkedin_articles', [])
    if linkedin_articles:
        linkedin_html = f"""
        <div class="linkedin-section">
            <h2>LinkedIn Updates</h2>
            {render_articles(linkedin_articles, is_linkedin=True)}
        </div>
        """
        template = template.replace(
            "{% if linkedin_articles %}",
            linkedin_html
        )
    else:
        template = template.replace(
            "{% if linkedin_articles %}",
            ""
        )
    
    # Remove template tags
    template = template.replace("{% endfor %}", "")
    template = template.replace("{% endif %}", "")
    
    return template

def render_articles(articles: list, is_linkedin: bool = False) -> str:
    """Render articles HTML"""
    articles_html = ""
    
    for i, article in enumerate(articles):
        summary_class = "summary-collapsed"
        summary_id = f"{'linkedin' if is_linkedin else 'summary'}-{i}"
        
        # Determine if we need toggle
        summary_length = len(article.get('summary', ''))
        toggle_html = ""
        if summary_length > 100:
            toggle_html = f"<span class=\"toggle-summary\" onclick=\"toggleSummary('{summary_id}')\">📄 Show more</span>"
        
        # Meta info
        if is_linkedin:
            meta_html = f"👔 {article.get('company', 'Unknown')} • ⏰ {article.get('published', '')} • 🔗 <a href=\"{article.get('url', '')}\">View on LinkedIn</a>"
        else:
            meta_html = f"📍 {article.get('source', 'Unknown')} • ⏰ {article.get('published', '')} • 🔗 <a href=\"{article.get('url', '')}\">Read more</a>"
        
        article_html = f"""
        <div class="article">
            <h3><a href="{article.get('url', '')}" target="_blank">{article.get('title', 'No title')}</a></h3>
            <p class="{summary_class}" id="{summary_id}">{article.get('summary', '')}</p>
            {toggle_html}
            <div class="meta">
                {meta_html}
            </div>
        </div>
        """
        
        articles_html += article_html
    
    return articles_html

def send_email_via_composio(html_content: str, config: dict):
    """Send email using Composio CLI"""
    email_config = config.get('email', {})
    recipient = email_config.get('recipient', 'faisal.homodi@gmail.com')
    subject_prefix = email_config.get('subject_prefix', 'Tech News Digest')
    
    subject = f"{subject_prefix} - {datetime.now().strftime('%Y-%m-%d')}"
    
    # Create temporary HTML file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(html_content)
        temp_file = f.name
    
    try:
        # Use Composio CLI to send email
        cmd = [
            '/home/faisal/.composio/composio',
            'execute',
            'GMAIL_SEND_EMAIL',
            '-d', json.dumps({
                'recipient_email': recipient,
                'subject': subject,
                'body': html_content,
                'is_html': True
            })
        ]
        
        print(f"📧 Sending email to: {recipient}")
        print(f"📝 Subject: {subject}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Email sent successfully via Composio")
            return True
        else:
            print(f"❌ Composio CLI failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Email send timed out")
        return False
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False
    finally:
        # Cleanup temp file
        try:
            os.unlink(temp_file)
        except:
            pass

def main():
    """Main execution"""
    print("📧 Starting Email Sender")
    print("=" * 30)
    
    try:
        # Load configuration and digest
        config = load_config()
        digest = load_digest()
        
        print(f"📊 Processing {len(digest['articles'])} articles")
        
        # Render HTML template
        html_content = render_email_template(digest)
        print(f"📝 Generated HTML email ({len(html_content)} characters)")
        
        # Send email
        success = send_email_via_composio(html_content, config)
        
        if success:
            print("✅ Email process completed!")
            return True
        else:
            print("❌ Email process failed")
            return False
            
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)