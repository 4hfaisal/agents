#!/usr/bin/env python3
"""
Simple test script for Tech News Digest
Creates sample data for testing email functionality
"""

import json
from datetime import datetime
from pathlib import Path

def main():
    """Create sample digest for testing"""
    print("🧪 Creating sample tech news digest")
    
    # Create output directory
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Sample tech articles
    sample_articles = [
        {
            'title': 'OpenAI Announces New AI Model',
            'url': 'https://openai.com/blog/new-model',
            'summary': 'OpenAI has launched a groundbreaking new AI model with improved performance and capabilities. This new model represents a significant advancement in artificial intelligence technology and is expected to revolutionize various industries.',
            'published': '2026-04-30T10:00:00Z',
            'source': 'TechCrunch',
            'source_name': 'TechCrunch',
            'category': 'Startups & Tech News',
            'priority': 10
        },
        {
            'title': 'GitHub Introduces AI Pair Programmer',
            'url': 'https://github.blog/ai-pair-programmer',
            'summary': 'GitHub has released an AI-powered pair programming tool that helps developers write better code. The tool integrates with popular IDEs and provides real-time suggestions and code improvements.',
            'published': '2026-04-30T09:30:00Z',
            'summary': 'GitHub has released an AI-powered pair programming tool that helps developers write better code. The tool integrates with popular IDEs and provides real-time suggestions and code improvements.',
            'published': '2026-04-30T09:30:00Z',
            'source': 'GitHub Blog',
            'source_name': 'GitHub Blog',
            'category': 'Development',
            'priority': 9
        },
        {
            'title': 'Major Cloud Provider Outage Resolved',
            'url': 'https://theverge.com/cloud-outage',
            'summary': 'A major cloud service provider experienced a 2-hour outage that affected multiple services worldwide. The outage was caused by a network configuration error and has been fully resolved.',
            'published': '2026-04-30T08:15:00Z',
            'source': 'The Verge',
            'source_name': 'The Verge',
            'category': 'Tech & Culture',
            'priority': 8
        }
    ]
    
    # Sample LinkedIn updates
    linkedin_articles = [
        {
            'title': 'Microsoft Announces Major Azure Update',
            'url': 'https://linkedin.com/company/microsoft/posts/123',
            'summary': 'Microsoft has announced significant updates to Azure cloud platform with new AI capabilities and enhanced security features. These updates will provide developers with more powerful tools for building cloud-native applications.',
            'published': '2026-04-30T11:00:00Z',
            'company': 'Microsoft',
            'type': 'company_update'
        },
        {
            'title': 'Google Cloud Platform Expansion',
            'url': 'https://linkedin.com/company/google/posts/456',
            'summary': 'Google has expanded its cloud platform services to three new regions, providing lower latency and improved performance for customers worldwide. This expansion is part of Google\'s ongoing commitment to global infrastructure development.',
            'published': '2026-04-30T09:45:00Z',
            'company': 'Google',
            'custom': 'news'
        }
    ]
    
    # Create sample digest
    digest = {
        'date': datetime.now().isoformat(),
        'articles': sample_articles,
        'linkedin_articles': linkedin_articles,
        'total_sources': 3,
        'total_articles_collected': 3,
        'total_articles_final': 3,
        'total_linkedin_updates': len(linkedin_articles)
    }
    
    # Save to file
    output_path = output_dir / "digest.json"
    with open(output_path, 'w') as f:
        json.dump(digest, f, indent=2)
    
    print(f"✅ Created sample digest with {len(sample_articles)} articles")
    print(f"👔 Created {len(linkedin_articles)} LinkedIn updates")
    print(f"💾 Saved to: {output_path}")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)