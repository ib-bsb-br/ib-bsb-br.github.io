# This script replaces the placeholder and clear_search text in the pagefind-ui.js file with new specified values.

#!/usr/bin/env python3

import re
import os

# Path to the pagefind-ui.js file
FILE = "_site/pagefind/pagefind-ui.js"

# Original expression to find
ORIGINAL_EXPRESSION = r'placeholder:"Search",clear_search:"Clear"'

# Replacement expression
NEW_EXPRESSION = r'placeholder:"long-term",clear_search:"X"'

# Ensure the file exists before attempting to open it
if not os.path.exists(FILE):
    print(f"Error: The file {FILE} does not exist.")
    exit(1)

# Read the contents of the file
with open(FILE, 'r') as f:
    content = f.read()

# Perform the replacement using regex
new_content = re.sub(ORIGINAL_EXPRESSION, NEW_EXPRESSION, content)

# Write the modified content back to the file
with open(FILE, 'w') as f:
    f.write(new_content)

print("Replacement complete.")
