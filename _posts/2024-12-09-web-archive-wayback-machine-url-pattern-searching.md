---
tags: tools, cloud
info: aberto.
date: 2024-12-09
type: post
layout: post
published: true
slug: web-archive-wayback-machine-url-pattern-searching
title: Web Archive Wayback Machine URL Pattern Searching
comment: https://web.archive.org/web/*/example.com/wp-content/uploads/*/*
---

## Understanding Web Archives

The Internet Archive's Wayback Machine is a digital archive of the World Wide Web, containing over 700 billion web pages saved over time. This guide focuses on advanced searching techniques using URL patterns to discover archived content.

## Core Concepts

### What is URL Pattern Searching?
URL pattern searching allows you to discover archived content by using wildcards (*) to match multiple URLs following a pattern. Instead of searching for exact URLs, you can search for all URLs matching certain criteria.

### Understanding Wildcards
The asterisk (*) represents any number of characters in a URL. For example:
- `*.pdf` matches any URL ending in .pdf
- `images/*` matches anything in the images directory
- `wp-content/*` matches all content in wp-content and its subdirectories

## Basic Search Patterns

### Standard Format
```
```

Where:
- `[timestamp]` is optional (use * for all times)
- `[domain]` is the website's domain
- `[path]` is the partial URL path
- Final `*` matches remaining characters

### Timestamp Formats
- `*` - Search across all times
- `2023*` - Only 2023 captures
- `202301*` - Only January 2023
- `20230115*` - Only January 15, 2023

## Advanced Search Techniques

### 1. Directory Traversal
Search entire directory structures:
```
```
This matches:
- /wp-content/uploads/2023/01/file.pdf
- /wp-content/uploads/images/photo.jpg
- Any file in any subdirectory under uploads

### 2. File Type Discovery
Find specific file types:
```
https://web.archive.org/web/*/example.com/*/document*.pdf
https://web.archive.org/web/*/example.com/*/*/report*.doc
```

### 3. Hidden Content Discovery
Common patterns for finding sensitive content:
```
https://web.archive.org/web/*/example.com/*backup*
https://web.archive.org/web/*/example.com/*archive*
https://web.archive.org/web/*/example.com/*/old/*
```

## Understanding Results

### Response Codes
- 200: Successfully archived page
- 404: Page not found when archived
- 403: Access forbidden
- 503: Service unavailable

### CDX API Access
For programmatic searching, use the CDX API:
```
https://web.archive.org/cdx/search/cdx?url=example.com/*&output=json
```

Parameters:
- `url`: URL pattern to search
- `output`: Response format (json, text)
- `limit`: Maximum results
- `from`: Start date
- `to`: End date

## Rate Limiting and Ethics

### Usage Guidelines
- Limit to 1 request per second
- Use the CDX API for bulk queries
- Respect robots.txt restrictions
- Check archive.org's terms of service

### Ethical Considerations
- Don't use for accessing intentionally removed content
- Respect copyright and intellectual property
- Consider site owners' privacy intentions

## Practical Examples

### 1. Finding Uploaded Documents
To find all PDF documents uploaded in 2023:
```
https://web.archive.org/web/2023*/example.com/*/uploads/*.pdf
```

### 2. Discovering Media Files
To find images in various subdirectories:
```
https://web.archive.org/web/*/example.com/*/images/*.jpg
https://web.archive.org/web/*/example.com/*/media/*.png
```

### 3. Locating Configuration Files
Search for potential configuration files:
```
https://web.archive.org/web/*/example.com/*.config
https://web.archive.org/web/*/example.com/*.ini
```

## Best Practices

1. **Start Broad, Then Refine**
   Begin with wide patterns:
   ```
   https://web.archive.org/web/*/example.com/*
   ```
   Then narrow based on findings:
   ```
   https://web.archive.org/web/*/example.com/specific-directory/*
   ```

2. **Use Multiple Patterns**
   Combine searches:
   ```
   https://web.archive.org/web/*/example.com/*backup*
   https://web.archive.org/web/*/example.com/*archive*
   https://web.archive.org/web/*/example.com/old-*
   ```

3. **Document Your Findings**
   Create a log of successful patterns:
   ```
   Domain: example.com
   Pattern: /wp-content/uploads/*
   Found: 900 files
   Types: PDF, DOC, JPG
   ```

## Common Pitfalls

1. **Too Many Wildcards**
   Bad:
   ```
   https://web.archive.org/web/*/*/*/*
   ```
   Good:
   ```
   https://web.archive.org/web/*/example.com/specific-path/*
   ```

2. **Inefficient Patterns**
   Bad:
   ```
   https://web.archive.org/web/*/example.com/*.*.pdf
   ```
   Good:
   ```
   https://web.archive.org/web/*/example.com/*/*.pdf
   ```

## Troubleshooting

1. **No Results Found**
   - Check domain spelling
   - Verify site was archived
   - Try removing path segments
   - Use CDX API to verify captures

2. **Too Many Results**
   - Add date restrictions
   - Specify subdirectories
   - Use more specific patterns
   - Filter by file type

3. **Access Denied**
   - Check robots.txt
   - Verify URL format
   - Consider site blocks
   - Check rate limiting

## Advanced Features

### CDX Query Examples
```
# Get all PDF files from 2023
curl "https://web.archive.org/cdx/search/cdx?url=example.com/*.pdf&from=2023&to=2024"

# Find all uploads in a directory
curl "https://web.archive.org/cdx/search/cdx?url=example.com/uploads/*&output=json"
```

### Pattern Combinations
Create complex searches:
```
https://web.archive.org/web/*/example.com/*/(backup|archive|old)/*.(pdf|doc|zip)
```

## Resources

1. Monitor the Internet Archive's documentation for updates
2. Join archival communities for pattern sharing
3. Document successful patterns for future reference
4. Stay informed about web archiving practices