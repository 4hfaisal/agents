#!/usr/bin/env python3
"""
Simple Template Engine for Tech News Digest
Handles template rendering with basic logic
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import re
import sys
sys.path.append(str(Path(__file__).parent))

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