# Tech News Digest Processing Instructions

## Workflow Overview

1. **Source Collection**: Gather news from configured RSS feeds
2. **Content Filtering**: Apply keyword filters (include/exclude)
3. **Content Extraction**: Extract article content from URLs
4. **AI Summarization**: Create concise summaries using language models
5. **Email Composition**: Format summaries into HTML email
6. **Email Delivery**: Send via Composio Gmail

## Processing Rules

### Content Collection
- Fetch latest 10 items from each RSS feed
- Respect source priority ordering
- Handle HTTP errors gracefully with retries

### Content Filtering
- Include articles matching ANY include keywords
- Exclude articles matching ANY exclude keywords  
- Case-insensitive matching
- Filter before summarization to save tokens

### Summarization Guidelines
- **Length**: 2-3 sentences per article
- **Focus**: Key developments, funding amounts, product launches
- **Style**: Professional but engaging
- **Exclude**: Marketing fluff, repetitive information

### Email Formatting
- **Subject**: `Tech News Digest - YYYY-MM-DD`
- **Structure**: Group by source category
- **Each Item**: Title, summary, source link
- **Footer**: Sent by OpenClaw Tech News Digest

## Error Handling

- **Failed Sources**: Skip and continue with others
- **Rate Limits**: Implement 1-second delays between requests
- **Empty Digest**: Send "No news today" notification
- **API Failures**: Fallback to simple title+link format

## Performance Considerations

- **Cache**: Consider 1-hour caching for repeated runs
- **Parallel**: Process sources in parallel when possible
- **Token Budget**: Limit summaries to ~1000 tokens total
- **Rate Limits**: Respect source website rate limits