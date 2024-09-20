---
title: PYragraphs
date: 2024-02-05 01:00:00 -02:00
categories:
- Code
tags:
- scripts
comment: https://www.textfixer.com/tools/convert-line-breaks.php
info: fechado.
type: post
layout: post
---

```
import re

def renumber_paragraphs(text):
    # Function to replace the paragraph tags with numbering
    def replace_tags(match):
        replace_tags.counter += 1
        return f'<p{replace_tags.counter}>{match.group(1)}</p{replace_tags.counter}>'
    
    # Initialize a counter attribute on the replace_tags function
    replace_tags.counter = 0
    
    # Use a regular expression to find each paragraph and call replace_tags to number it
    new_text = re.sub(r'<p>(.*?)</p>', replace_tags, text, flags=re.DOTALL)
    return new_text

# Sample usage with the provided input text (assuming it's loaded in a variable called `input_text`)
input_text = """
<p>Paragraph 1 text here.</p>
<p>Paragraph 2 text here.</p>
... (other paragraphs) ...
<p>Last paragraph text here.</p>
"""

# Call the function and print the output
output_text = renumber_paragraphs(input_text)
print(output_text)
```
