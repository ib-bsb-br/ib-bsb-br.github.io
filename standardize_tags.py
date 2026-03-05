#!/usr/bin/env python3
"""
standardize_tags.py

This script scans all Markdown (or .markdown) files in your repository that include Jekyll YAML front matter.
It standardizes the "tags" field so that regardless of its original format – 
  • CSV style (e.g., tags: tag1, tag2, tag3)
  • Inline style (e.g., tags: [tag1, tag2, tag3])
  • Block list style (e.g.,
         tags:
           - tag1
           - tag2
           - tag3)
the tags are rewritten in an inline list format:
    tags: [tag1, tag2, tag3]

Usage:
  python standardize_tags.py
"""

import os
import re

def process_front_matter(front_matter_text):
    """
    Process the YAML front matter text to standardize the "tags" field.
    Recognizes three formats:
      1. CSV style on one line:      tags: tag1, tag2, tag3
      2. Inline style:               tags: [tag1, tag2, tag3]
      3. Block style list:           tags:
                                          - tag1
                                          - tag2
                                          - tag3
    Returns modified front matter text.
    """
    lines = front_matter_text.splitlines()
    processed_lines = []
    i = 0
    tags_handled = False
    # Pattern to catch a line starting with "tags:" possibly followed by content.
    tags_line_regex = re.compile(r'^(tags:\s*)(.*)$')
    
    while i < len(lines):
        line = lines[i]
        match = tags_line_regex.match(line)
        if match and not tags_handled:
            prefix, content = match.group(1), match.group(2).strip()
            tags_list = []
            if content:
                # If content is in inline list format (brackets present)
                if content.startswith('[') and content.endswith(']'):
                    inner = content[1:-1].strip()
                    if inner:
                        tags_list = [t.strip() for t in inner.split(',') if t.strip()]
                else:
                    # Otherwise, treat as CSV style on the same line
                    tags_list = [t.strip() for t in content.split(',') if t.strip()]
                processed_lines.append(f"tags: [{', '.join(tags_list)}]")
                tags_handled = True
            else:
                # Handle block style: read subsequent lines starting with a dash.
                j = i + 1
                while j < len(lines):
                    block_line = lines[j]
                    block_match = re.match(r"^\s*-\s*(.+)$", block_line)
                    if block_match:
                        tags_list.append(block_match.group(1).strip())
                        j += 1
                    else:
                        break
                processed_lines.append(f"tags: [{', '.join(tags_list)}]")
                tags_handled = True
                i = j - 1  # Skip lines already processed in block list.
        else:
            processed_lines.append(line)
        i += 1
    return "\n".join(processed_lines)

def process_markdown_file(filepath):
    """
    Process a single Markdown file:
      • Check for YAML front matter (delimited by '---').
      • Standardize the "tags" field in the front matter.
      • Overwrite the file if changes are made.
    Returns True if file was updated, else False.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ensure file starts with YAML front matter.
    if not content.lstrip().startswith('---'):
        return False

    parts = content.split('---', 2)
    if len(parts) < 3:
        return False  # Malformed front matter.
    
    # parts[0] may be empty; parts[1] is front matter; parts[2] is the rest of the file.
    front_matter = parts[1]
    new_front_matter = process_front_matter(front_matter)
    
    if new_front_matter == front_matter:
        return False  # No changes made.
    
    # Reassemble the file with standardized front matter.
    new_content = f"---\n{new_front_matter}\n---" + parts[2]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def main(root="."):
    updated_files = []
    for dirpath, _, files in os.walk(root):
        for filename in files:
            if filename.lower().endswith((".md", ".markdown")):
                path = os.path.join(dirpath, filename)
                try:
                    if process_markdown_file(path):
                        updated_files.append(path)
                        print(f"Updated: {path}")
                except Exception as error:
                    print(f"Error processing {path}: {error}")
    print(f"\nStandardization complete. {len(updated_files)} file(s) updated.")

if __name__ == '__main__':
    main()
