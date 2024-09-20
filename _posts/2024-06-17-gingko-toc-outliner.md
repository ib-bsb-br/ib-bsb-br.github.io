---
title: Gingko JSON ToC outliner
date: 2024-06-17
tags: scripts
comment: gingkowriter.com
info: fechado.
type: post
layout: post
mermaid: true
---

```python
import json

def add_outline(data, level=0, parent_index=None):
    """
    Recursively adds an outline to the JSON data.

    Args:
        data: The JSON data (list or dictionary).
        level: The current level of nesting (0-based).
        parent_index: The index of the parent element (None for root).

    Returns:
        The modified JSON data with the outline added.
    """
    if parent_index is None:
        parent_index = []

    if isinstance(data, list):
        for index, item in enumerate(data):
            data[index] = add_outline(item, level, parent_index + [index + 1])
    elif isinstance(data, dict):
        if 'content' in data:
            if level == 0:
                outline_prefix = f"{parent_index[-1] - 1}) TITLE"
            else:
                sections = '.'.join(map(str, parent_index[1:]))
                outline_prefix = f"{'.'.join(map(str, parent_index))})"
                if level == 1:
                    outline_prefix = f"{parent_index[-1]}) CHAPTER {parent_index[-1]}"
                else:
                    outline_prefix += f" CHAPTER {parent_index[1]} - {'SUB' * (level - 2)}SECTION {sections}"
            data['content'] = f"{outline_prefix}\n***\n{data['content']}"

        if 'children' in data:
            data['children'] = add_outline(data['children'], level + 1, parent_index)

    return data

if __name__ == "__main__":
    # Load JSON from a file
    with open('input.json', 'r') as f:
        data = json.load(f)

    # Process the JSON to add the outline
    outlined_data = add_outline(data)

    # Save the resulting JSON to a file
    with open('output.json', 'w') as f:
        json.dump(outlined_data, f, indent=2)

    # Optionally, print the resulting JSON
    print(json.dumps(outlined_data, indent=2))
```
