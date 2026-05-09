#!/usr/bin/env python3
"""
LinkedIn Monitor for Tech News Digest
Monitors LinkedIn company pages for official news and posts
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import re
import urllib.request
from typing import List, Dict, Any

# Configuration
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
CONFIG_DIR = SKILL_DIR / "references"
OUTPUT_DIR = SCRIPT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

def load_linkedin_config() -> Dict[str, Any]:
    """Load LinkedIn companies configuration"""
    config_path = CONFIG_DIR / "linkedin-companies.yaml"
    
    # Simple YAML parser
    config = {}
    current_section = None
    
    try:
        with open(config_path, 'r') as f:
            content = f.read()
        
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if line.endswith(':'):
                current_section = line[:-1].strip()
                config[current_section] = [] if current_section == 'companies' else {}
            elif ':' in line and current_section:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                if current_section == 'companies':
                    if key == '- name':
                        config[current_section].append({'name': value.strip('"\'')})
                    elif config[current_section] and key.startswith('  '):
                        last_company = config[current_section][-1]
                        sub_key = key[2:].strip()
                        last_company[sub_key] = value.strip('"\'')
                else:
                    # Convert numeric values to integers
                    if value.strip('"\'').isdigit():
                        config[current_section][key] = int(value.strip('"\''))
                    else:
                        config[current_section][key] = value.strip('"\'')
    
    except FileNotFoundError:
        print("⚠️  LinkedIn config file not found")
        return {'companies': []}
    except Exception as e:
        print(f"⚠️  Error loading LinkedIn config: {e}")
        return {'companies': []}
    
    return config

def fetch_linkedin_company_updates(company: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Fetch updates from LinkedIn company page (simulated for now)"""
    company_name = company.get('name', '')
    print(f"👔 Monitoring LinkedIn: {company_name}")
    
    # TODO: Implement actual LinkedIn API integration
    # For now, return simulated/placeholder data
    
    # Simulated company updates
    simulated_updates = [
        {
            'title': f"{company_name} Announces New Initiative",
            'summary': f"{company_name} has launched an exciting new project focusing on innovation and growth. This development represents a significant step forward in their strategic roadmap.",
            'url': f"https://linkedin.com/company/{company_name.lower()}/posts/123",
            'published': (datetime.now() - timedelta(hours=2)).isoformat(),
            'company': company_name,
            'type': 'company_update'
        },
        {
            'title': f"{company_name} Quarterly Results Released",
            'summary': f"{company_name} has reported strong quarterly earnings with significant growth across key business segments. The company continues to demonstrate robust performance in the market.",
            'url': f"https://linkedin.com/company/{company_name.lower()}/posts/124",
            'published': (datetime.now() - timedelta(days=1)).isoformat(),
            'company': company_name,
            'type': 'news'
        }
    ]
    
    # Filter by post types
    config = load_linkedin_config()
    include_types = config.get('api_settings', {}).get('include_post_types', [])
    
    if include_types:
        simulated_updates = [
            update for update in simulated_updates 
            if update['type'] in include_types
        ]
    
    print(f"   📊 Found {len(simulated_updates)} updates")
    return simulated_updates

def main():
    """Main LinkedIn monitoring function"""
    print("👔 Starting LinkedIn Company Monitor")
    print("=" * 40)
    
    # Load configuration
    config = load_linkedin_config()
    companies = config.get('companies', [])
    
    if not companies:
        print("⚠️  No companies configured for LinkedIn monitoring")
        return []
    
    print(f"✅ Loaded {len(companies)} companies")
    
    all_updates = []
    
    # Monitor each company
    for company in companies:
        try:
            updates = fetch_linkedin_company_updates(company)
            all_updates.extend(updates)
            
            # Add delay between company checks
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Failed to monitor {company.get('name')}: {e}")
            continue
    
    # Sort by priority and limit
    all_updates.sort(key=lambda x: x.get('published', ''), reverse=True)
    max_per_company = config.get('api_settings', {}).get('max_posts_per_company', 3)
    max_items = max_per_company * len(companies)
    final_updates = all_updates[:max_items]
    
    print(f"📊 Total LinkedIn updates: {len(final_updates)}")
    
    # Save to file
    output_path = OUTPUT_DIR / "linkedin-updates.json"
    with open(output_path, 'w') as f:
        json.dump({
            'date': datetime.now().isoformat(),
            'updates': final_updates,
            'total_companies': len(companies),
            'total_updates_found': len(all_updates),
            'total_updates_final': len(final_updates)
        }, f, indent=2)
    
    print(f"💾 Saved LinkedIn updates to: {output_path}")
    print("✅ LinkedIn monitoring completed!")
    
    return final_updates

if __name__ == "__main__":
    updates = main()
    exit(0 if updates else 1)