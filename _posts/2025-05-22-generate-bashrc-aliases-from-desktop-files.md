---
tags: [scratchpad]
info: aberto.
date: 2025-05-22
type: post
layout: post
published: true
slug: generate-bashrc-aliases-from-desktop-files
title: 'Generate `.bashrc` aliases from .desktop files'
---
{% codeblock bash %}
#!/bin/bash

# Script to extract Exec= lines from .desktop files
# and create a list of bash aliases in a deterministic order.

# --- Configuration ---
DESKTOP_DIR="/home/linaro/.local/share/applications"
OUTPUT_FILE="/home/linaro/desktop-exec-alias.txt"
ALIAS_COUNTER=0
# --- End Configuration ---

echo "--- Script Starting ---"
echo "Desktop directory: $DESKTOP_DIR"
echo "Output file: $OUTPUT_FILE"

# Ensure the target directory for .desktop files exists
if [ ! -d "$DESKTOP_DIR" ]; then
    echo "Error: Directory $DESKTOP_DIR does not exist." >&2
    exit 1
fi
echo "Desktop directory confirmed to exist."

# Clear or create the output file for a fresh list
# This ensures that if the script is run multiple times,
# the output file contains only the latest aliases.
> "$OUTPUT_FILE"
echo "Output file initialized (cleared or created)."

echo "Finding .desktop files..."
# Find all files ending with .desktop in the specified directory.
# -print0 outputs filenames null-terminated.
# sort -z sorts null-terminated input (ensures deterministic order of aliases).
# The while loop with IFS= and read -r -d $'\0'
# robustly handles filenames that might contain spaces or special characters.
find "$DESKTOP_DIR" -name "*.desktop" -type f -print0 | sort -z | while IFS= read -r -d $'\0' desktop_file; do
    echo "----------------------------------------" # Separator for each file
    echo "Processing file: $desktop_file" # DEBUG

    # Try to get the Exec line using grep first for debugging
    # This helps see if the line is even present in a way grep recognizes
    echo "Attempting to grep '^Exec=' from file..." # DEBUG
    grep_exec_line=$(grep '^Exec=' "$desktop_file") # DEBUG
    if [ -n "$grep_exec_line" ]; then
        echo "DEBUG: grep found the following Exec line(s):" # DEBUG
        echo "$grep_exec_line" # DEBUG
    else
        echo "DEBUG: grep did NOT find any line starting with 'Exec='" # DEBUG
    fi

    # Original sed command to extract the value
    echo "Attempting to extract Exec value with sed..." # DEBUG
    exec_value=$(sed -n 's/^Exec=//p' "$desktop_file" | head -n 1)
    
    if [ -n "$exec_value" ]; then
        echo "DEBUG: sed extracted value: '$exec_value'" # DEBUG
        # Append the alias command to the output file.
        # Single quotes around '$exec_value' are important to preserve
        # the command exactly as it is, including spaces and special characters,
        # when writing to the alias file.
        echo "alias $ALIAS_COUNTER='$exec_value'" >> "$OUTPUT_FILE"
        ALIAS_COUNTER=$((ALIAS_COUNTER + 1)) # Increment the alias number
    else
        echo "DEBUG: sed did NOT extract any value for Exec=" # DEBUG
        # Output a warning to the standard error stream if an Exec line
        # couldn't be found or its value was empty in a specific .desktop file.
        echo "Warning: Could not extract Exec value from $desktop_file (or line was not found/empty after 'Exec=')" >&2
    fi
done

echo "----------------------------------------"
echo "File processing loop finished."
echo "Alias list generation complete."
echo "Output saved to: $OUTPUT_FILE"
echo "Total aliases generated: $ALIAS_COUNTER" # Shows actual count
echo "--- Script Finished ---"

exit 0
{% endcodeblock %}