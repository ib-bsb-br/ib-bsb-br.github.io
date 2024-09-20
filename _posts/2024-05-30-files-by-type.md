---
title: Organize files by their extensions
date: 2024-05-30 00:00:00 -03:00
categories:
- Code
tags:
- linux
- scripts
comment: 
info: aberto.
type: post
layout: post
---

```bash
#!/bin/bash

# Check if the folder name is provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <folder>"
  exit 1
fi

FOLDER="$1"

# Check if the provided argument is a directory
if [ ! -d "$FOLDER" ]; then
  echo "Error: $FOLDER is not a directory."
  exit 1
fi

# Change to the specified directory
cd "$FOLDER" || exit

# Get a list of unique file extensions
file_extensions=$(find . -type f | sed -n 's/.*\.\([a-zA-Z0-9]*\)$/\1/p' | sort | uniq)

# Create directories for each file extension and move files
for ext in $file_extensions; do
  mkdir -p "$ext"
  find . -type f -name "*.$ext" -exec mv {} "$ext" \;
done

echo "Files have been organized by file type."
```

### How to Use the Script

1. Save the script to a file, for example, `organize_files.sh`.
2. Make the script executable:
   ```bash
   chmod +x organize_files.sh
   ```
3. Run the script with the target folder as an argument:
   ```bash
   ./organize_files.sh <folder>
   ```
