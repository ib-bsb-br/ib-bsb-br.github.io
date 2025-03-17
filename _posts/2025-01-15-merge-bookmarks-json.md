---

tags: [scratchpad]
info: aberto.
date: 2025-01-15
type: post
layout: post
published: true
slug: merge-bookmarks-json
title: 'Merge Bookmarks JSON'
---
Install `demjson3` using pip:

```bash
pip install demjson3
```

---

**Script:**

```python
import demjson3
import json
import sys
import argparse

def fix_and_parse_snippets(text):
    """
    Parses and fixes JSON snippets within the provided text.
    Returns a list of valid JSON objects.
    """
    # Split the text into potential JSON strings based on curly braces
    snippets = []
    brace_level = 0
    current_snippet = ''
    for char in text:
        current_snippet += char
        if char == '{':
            brace_level += 1
        elif char == '}':
            brace_level -= 1
            if brace_level == 0:
                # Attempt to parse the snippet
                try:
                    parsed = demjson3.decode(current_snippet)
                    snippets.append(parsed)
                    current_snippet = ''
                except demjson3.JSONDecodeError as e:
                    print(f"Error parsing snippet: {e}")
                    current_snippet = ''
                continue
    return snippets

def merge_children(existing_children, new_children):
    """
    Merges new children into existing ones, avoiding duplicates based on GUID.
    """
    existing_guids = {child.get('guid') for child in existing_children}
    for child in new_children:
        if child.get('guid') not in existing_guids and child.get('guid') is not None:
            existing_children.append(child)
            existing_guids.add(child.get('guid'))
        else:
            # Handle duplicates or missing GUIDs if necessary
            existing_children.append(child)  # Optionally append anyway
    return existing_children

def consolidate_bookmarks(json_objects):
    """
    Consolidates multiple bookmark objects into a single bookmarks structure.
    """
    consolidated = {
        "roots": {
            "bookmark_bar": {
                "children": [],
                "date_added": "0",
                "date_modified": "0",
                "id": "1",
                "name": "Bookmarks Bar",
                "type": "folder"
            },
            "other": {
                "children": [],
                "date_added": "0",
                "date_modified": "0",
                "id": "2",
                "name": "Other Bookmarks",
                "type": "folder"
            },
            "synced": {
                "children": [],
                "date_added": "0",
                "date_modified": "0",
                "id": "3",
                "name": "Mobile Bookmarks",
                "type": "folder"
            }
        },
        "version": 1
    }

    for obj in json_objects:
        if 'roots' in obj:
            roots = obj['roots']
            for root_name in ['bookmark_bar', 'other', 'synced']:
                if root_name in roots:
                    existing_children = consolidated['roots'][root_name]['children']
                    new_children = roots[root_name].get('children', [])
                    merged_children = merge_children(existing_children, new_children)
                    consolidated['roots'][root_name]['children'] = merged_children
                    # Update date_added and date_modified if needed
                    consolidated['roots'][root_name]['date_added'] = max(
                        consolidated['roots'][root_name]['date_added'], roots[root_name].get('date_added', "0")
                    )
                    consolidated['roots'][root_name]['date_modified'] = max(
                        consolidated['roots'][root_name]['date_modified'], roots[root_name].get('date_modified', "0")
                    )
        else:
            # If the object is a fragment, add it to 'Other Bookmarks'
            if obj.get('type') in ['folder', 'url']:
                consolidated['roots']['other']['children'].append(obj)

    return consolidated

def main():
    parser = argparse.ArgumentParser(description="Fix and merge malformed Google Chrome bookmarks JSON snippets.")
    parser.add_argument('input_file', help="Path to the input text file containing concatenated JSON snippets.")
    parser.add_argument('output_file', help="Path to the output JSON file for the fixed bookmarks.")
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    # Read the input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_text = f.read()
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)

    # Parse and fix snippets
    json_objects = fix_and_parse_snippets(raw_text)

    if not json_objects:
        print("No valid JSON snippets found.")
        sys.exit(1)

    # Consolidate bookmarks
    consolidated_bookmarks = consolidate_bookmarks(json_objects)

    # Write to the output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(consolidated_bookmarks, f, indent=4, ensure_ascii=False)
        print(f"Fixed bookmarks have been saved to {output_file}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

---

**Instructions to Use the Script:**

1. **Install the Required Library:**

   Install `demjson3` if you haven't already:

   ```bash
   pip install demjson3
   ```

2. **Prepare Your Input File:**

   - Create a text file (e.g., `input_snippets.txt`) containing your concatenated snippets of Chrome bookmarks JSON data.
   - Ensure that the JSON fragments are included as they are, even if they are improperly formatted or concatenated.

3. **Save the Script:**

   - Save the script above into a file named, for example, `fix_bookmarks.py`.

4. **Run the Script:**

   - Open a terminal or command prompt and navigate to the directory containing `fix_bookmarks.py` and `input_snippets.txt`.
   - Run the script using the following command:

     ```bash
     python fix_bookmarks.py input_snippets.txt fixed_bookmarks.json
     ```

     - Replace `input_snippets.txt` with the path to your input file.
     - Replace `fixed_bookmarks.json` with your desired output file name.

5. **Verify the Output:**

   - After running the script, it will generate `fixed_bookmarks.json` containing the consolidated bookmarks.
   - Review the output file to ensure all bookmarks have been included.

6. **Import the Fixed Bookmarks:**

   - You can now import the `fixed_bookmarks.json` file into Google Chrome or use it as needed.
