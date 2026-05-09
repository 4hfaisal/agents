#!/usr/bin/env python3
"""
Tech News Collector
Fetches news from RSS feeds, applies filters, and prepares for summarization
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any
import re
import xml.etree.ElementTree as ET
import urllib.request
import subprocess

# Simple YAML loader since we can't import yaml
def load_yaml(file_path):
    """Simple YAML parser for basic config files"""
    import re
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Simple YAML parser for our specific format
    config = {}
    current_section = None
    
    for line in content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        if line.endswith(':'):
            current_section = line[:-1].strip()
            config[current_section] = [] if current_section == 'sources' else {}
        elif ':' in line and current_section:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            if current_section == 'sources':
                # Source list item
                if key == '- name':
                    config[current_section].append({'name': value.strip('"\'')})
                elif config[current_section] and key.startswith('  '):
                    last_source = config[current_section][-1]
                    sub_key = key[2:].strip()
                    last_source[sub_key] = value.strip('"\'')
            else:
                # Simple key-value
                config[current_section][key] = value.strip('"\'')
    
    return config

# Configuration
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
CONFIG_DIR = SKILL_DIR / "references"
OUTPUT_DIR = SCRIPT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Load configuration
def load_config() -> Dict[str, Any]:
    """Load sources.yaml configuration"""
    config_path = CONFIG_DIR / "sources.yaml"
    return load_yaml(config_path)

def fetch_rss_feed(feed_url: str, max_items: int = 10) -> List[Dict[str, Any]]:
    """Fetch and parse RSS feed using built-in XML parser"""
    try:
        print(f"📡 Fetching: {feed_url}")
        
        # Fetch RSS feed
        with urllib.request.urlopen(feed_url) as response:
            rss_content = response.read().decode('utf-8')
        
        # Parse XML
        root = ET.fromstring(rss_content)
        
        # Simple RSS parsing (works for most common feeds)
        articles = []
        
        # Check different RSS formats
        items = []
        if root.tag.endswith('rss'):
            # Standard RSS
            channel = root.find('channel')
            if channel is not None:
                items = channel.findall('item')
        elif root.tag.endswith('feed'):
            # Atom feed
            items = root.findall('entry')
        
        for item in items[:max_items]:
            title_elem = item.find('title')
            link_elem = item.find('link')
            description_elem = item.find('description')
            pub_date_elem = item.find('pubDate') or item.find('published')
            
            title = title_elem.text if title_elem is not None else 'No title'
            url = link_elem.text if link_elem is not None else ''
            summary = description_elem.text if description_elem is not None else ''
            published = pub_date_elem.text if pub_date_elem is not None else ''
            
            article = {
                'title': title,
                'url': url,
                'summary': summary,
                'published': published,
                'source': 'RSS Feed'
            }
            articles.append(article)
        
        print(f"✅ Found {len(articles)} articles")
        return articles
        
    except Exception as e:
        print(f"❌ Failed to fetch {feed_url}: {e}")
        return []

def apply_filters(articles: List[Dict[str, Any]], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Apply keyword filters to articles"""
    include_keywords = config.get('keywords', {}).get('include', [])
    exclude_keywords = config.get('keywords', {}).get('exclude', [])
    
    filtered_articles = []
    
    for article in articles:
        title = article['title'].lower()
        summary = article['summary'].lower()
        content = f"{title} {summary}"
        
        # Check exclude filters first
        excluded = any(keyword.lower() in content for keyword in exclude_keywords)
        if excluded:
            continue
            
        # Check include filters (if any)
        if include_keywords:
            included = any(keyword.lower() in content for keyword in include_keywords)
            if not included:
                continue
        
        filtered_articles.append(article)
    
    return filtered_articles

def fetch_linkedin_updates() -> List[Dict[str, Any]]:
    """Run LinkedIn monitor and return updates"""
    try:
        print("👔 Checking LinkedIn for company updates...")
        
        # Run LinkedIn monitor script
        result = subprocess.run([
            'python3', str(SCRIPT_DIR / 'linkedin-monitor.py')
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            # Load LinkedIn updates
            linkedin_path = OUTPUT_DIR / "linkedin-updates.json"
            if linkedin_path.exists():
                with open(linkedin_path, 'r') as f:
                    linkedin_data = json.load(f)
                return linkedin_data.get('updates', [])
        else:
            print(f"⚠️  LinkedIn monitor failed: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⚠️  LinkedIn monitor timed out")
    except Exception as e:
        print(f"⚠️  LinkedIn monitor error: {e}")
    
    return []

def main():
    """Main execution"""
    print("🚀 Starting Tech News Collector")
    print("=" * 40)
    
    # Load configuration
    try:
        config = load_config()
        sources = config.get('sources', [])
        print(f"✅ Loaded {len(sources)} sources")
    except Exception as e:
        print(f"❌ Failed to load configuration: {e}")
        return False
    
    all_articles = []
    
    # Fetch from all sources
    for source in sources:
        if source.get('type') == 'rss':
            articles = fetch_rss_feed(source['url'])
            articles = apply_filters(articles, config)
            
            # Add source info to main_article
            for article in articles:
                article['source_name'] = source['name']
                article['category'] = source.get('category', 'General')
                article['priority'] = source.get('priority', 5)
            
            all_articles.extend(articles)
        
        # Add small delay between requests
        time.sleep(1)
    
    # Fetch LinkedIn updates
    linkedin_articles = fetch_linkedin_updates()
    
    print(f"\n📊 Total articles collected: {len(all_articles)}")
    print(f"👔 LinkedIn updates: {len(linkedin_articles)}")
    
    # Sort by priority and limit total
    all_articles.sort(key=lambda x: x.get('priority', 5), reverse=True)
    max_items = 15  # Default value
    email_config = config.get('email', {})
    if email_config and 'max_total_items' in email_config:
        max_items = int(email_config['max_total_items'])
    final_articles = all_articles[:max_items]
    
    print(f"📨 Final digest: {len(final_articles)} articles")
    
    # Prepare output
    digest = {
        'date': datetime.now().isoformat(),
        'articles': final_articles,
        'linkedin_articles': linkedin_articles,
        'total_sources': len(sources),
        'total_articles_collected': len(all_articles),
        'total_articles_final': len(final_articles),
        'total_linkedin_updates': len(linkedin_articles)
    }
    
    # Save to file
    output_path = OUTPUT_DIR / "digest.json"
    with open(output_path, 'w') as f:
        json.dump(digest, f, indent=2)
    
    print(f"💾 Saved digest to: {output_path}")
    print("✅ Collection completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)