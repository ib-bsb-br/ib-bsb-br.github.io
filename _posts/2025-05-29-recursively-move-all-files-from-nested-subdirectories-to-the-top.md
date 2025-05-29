---
tags: [scratchpad]
info: aberto.
date: 2025-05-29
type: post
layout: post
published: true
slug: recursively-move-all-files-from-nested-subdirectories-to-the-top
title: 'Recursively move all files from nested subdirectories to the top'
---
```bash
#!/bin/bash
#
# flatten.sh: Recursively move all files from nested subdirectories to the root of the specified directory.
#
# How it works:
#   1. Validates that exactly one argument (the path to the target directory) is provided.
#   2. Checks if the target directory exists and is writable.
#   3. Uses the 'find' command with -mindepth 2 to locate files not on the top-level.
#   4. For each file, it attempts to move the file to the target directory.
#      - If a file with the same basename exists, a Unix timestamp is prefixed to the filename to avoid overwriting.
#   5. Optionally removes empty directories left over from the file moves.
#
# Usage:
#   ./flatten.sh /path/to/target_directory
#

# Check that exactly one argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 /path/to/target_directory"
    exit 1
fi

TARGET_DIR="$1"

# Verify that TARGET_DIR exists and is a directory
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' does not exist."
    exit 1
fi

# Check if TARGET_DIR is writable
if [ ! -w "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' is not writable. Please adjust permissions."
    exit 1
fi

echo "Processing files in '$TARGET_DIR'..."

# Use find to locate all files in subdirectories (depth >= 2)
# -mindepth 2 ensures that files in the top-level directory are not included.
# -print0 and IFS= read -r -d '' handle filenames containing spaces or special characters.
find "$TARGET_DIR" -mindepth 2 -type f -print0 | while IFS= read -r -d '' file; do
    base=$(basename "$file")
    dest="$TARGET_DIR/$base"

    # If a file with the same name exists, modify the filename by appending a timestamp to avoid overwriting.
    if [ -e "$dest" ]; then
        # Append a timestamp to the original filename. Note: This is not a guarantee against collisions if files are moved very quickly.
        timestamp=$(date +%s)
        dest="$TARGET_DIR/${timestamp}_$base"
        echo "Note: '$base' already exists. Renaming moved file to '$(basename "$dest")'."
    fi

    # Attempt to move the file and capture any errors.
    if mv "$file" "$dest"; then
        echo "Moved: '$file' -> '$dest'"
    else
        echo "Error moving: '$file'" >&2
    fi
done

# Optional Cleanup: Remove any empty directories that remain in TARGET_DIR.
# This may remove folders that are no longer needed. Comment out this section if unwanted.
find "$TARGET_DIR" -type d -empty -delete

echo "All eligible files have been moved to '$TARGET_DIR'."
```