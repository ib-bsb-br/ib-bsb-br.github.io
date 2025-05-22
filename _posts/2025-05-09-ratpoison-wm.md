---
tags: [aid>linux>software>dotfile]
info: aberto.
date: 2025-05-09
type: post
layout: post
published: true
slug: ratpoison-wm
title: 'Ratpoison WM'
comment: 'https://ozi-blog.ru/nastroyka-pereklyucheniya-rabochih-stolov-v-ratpoison/'
---
## documentation at
`https://ib.bsb.br/ratpoison-documentation/`

### **Step 1: Install Ratpoison and Essential Tools**

First, update your package lists and install Ratpoison. The rpws (Ratpoison Workspace System) script is included with the ratpoison package in Debian Bullseye. Consider installing dmenu for application launching and a basic terminal like xterm or rxvt-unicode.  
`sudo apt update`  
`sudo apt upgrade`  
`sudo apt install ratpoison dmenu xterm # Or rxvt-unicode, etc.`  
`# Install other optional utilities you might find useful:`  
`# sudo apt install alsamixergui bpytop brightnessctl catfish dialog gmrun gsimplecal neofetch `  
`# python3-psutil unclutter viewnior xdotool scrot `  
`# fonts-dejavu fonts-terminus nitrogen picom # (nitrogen for wallpaper, picom for compositing)`

### **Step 2: Create a Ratpoison Session File for LightDM**

LightDM uses .desktop files located in /usr/share/xsessions/ to identify available sessions. Create one for Ratpoison:  
`sudo nano /usr/share/xsessions/ratpoison.desktop`

Add the following content:  
`[Desktop Entry]`  
`Version=1.0`  
`Encoding=UTF-8`  
`Name=Ratpoison`  
`Comment=Minimalist Tiling Window Manager`  
`Exec=ratpoison`  
`TryExec=ratpoison`  
`Icon=`  
`Type=XSession`

Save and close the file (e.g., Ctrl+X, then Y, then Enter in nano).

### **Step 3: Configure LightDM for Ratpoison Autologin**

To ensure LightDM launches Ratpoison for the autologin user, you need to update its configuration. Debian best practices suggest using configuration snippets in /etc/lightdm/lightdm.conf.d/. If you already have an autologin configuration file there (e.g., 50-autologin.conf), modify it. Otherwise, you can edit /etc/lightdm/lightdm.conf directly or create a new snippet.

1. **Edit or Create LightDM Configuration:** For example, to create/edit a dedicated snippet:  
   `sudo nano /etc/lightdm/lightdm.conf.d/60-autologin-ratpoison.conf`  
   Ensure the configuration specifies linaro and sets autologin-session to ratpoison. The autologin-session value should match the filename of the .desktop file created in Step 2 (without the .desktop extension).  
   `[Seat:*]`  
   `autologin-user=linaro`  
   `autologin-user-timeout=0`  
   `autologin-session=ratpoison`  
   If you are editing an existing file that previously specified autologin-session=xfce (or similar), change it to ratpoison. Adding this line explicitly makes the autologin deterministic.  
2. **Note on Session Selection:** While LightDM can sometimes remember the last session selected at the greeter, for an autologin setup, explicitly defining autologin-session is the most reliable method.

### **Step 4: Configure Ratpoison (~/.ratpoisonrc)**

Create and configure the ~/.ratpoisonrc file in the home directory of the autologin user (i.e., /home/linaro/.ratpoisonrc). This file controls Ratpoison’s behavior, keybindings, and startup applications.  
`# Ensure you are the user ‘linaro’ or adjust path accordingly`  
`nano /home/linaro/.ratpoisonrc`

Here’s a comprehensive example configuration:  
`# ~/.ratpoisonrc for linaro`
{% codeblock %}

{% endcodeblock %}

#### ~/.local/bin/*.sh shell scripts

##### `shell/llm_analyze_file.sh`

```bash
#!/bin/bash
# Script to analyze a file with llm (o3-mini) using a specific prompt.
# It will prompt for the file path within the terminal.
# Patched by Gemini to capture all terminal output to clipboard
_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG="/tmp/$(basename "$0" .sh)_terminal_output_$$_${RANDOM}.log"

# Main script logic is executed in a subshell to capture all its output
(
    echo "LLM File Analysis (o3-mini)"
    echo "Enter the full path to the file you want to analyze (Ctrl+D or empty to cancel):"
    read -p "File Path: " FILE_PATH

    if [ -z "$FILE_PATH" ]; then
        echo "No file path entered. Exiting."
    elif [ -f "$FILE_PATH" ]; then
        SYSTEM_PROMPT_TEXT="Use your full analytic capacity to provide a thorough explanation: In what fundamental and causal ways does the file ('$FILE_PATH') consist? Please discuss: (1) Key events or conditions leading to its current state; (2) Its essential or structural nature; (3) Its broader purpose and significance."
        
        echo ""
        echo "Analyzing file: $FILE_PATH"
        echo "Using model: o3-mini"
        echo "Waiting for LLM response..."
        echo ""

        cat "$FILE_PATH" | llm -m o3-mini -s "$SYSTEM_PROMPT_TEXT"
    else
        echo "File not found: $FILE_PATH" >&2
    fi
) > "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" 2>&1

# --- Block to copy terminal log to clipboard and cleanup ---
# This block executes after the main script logic subshell has finished.
if [ -f "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" ]; then # Check if log file was created
    if command -v xclip &>/dev/null; then
        if command -v sed &>/dev/null; then
            # Clean ANSI codes if sed is available and copy
            sed 's/\x1B\[[0-9;]*[JKmsu]//g' "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" | xclip -selection clipboard
            echo "Full terminal output (ANSI codes removed) copied to clipboard."
        else
            # Copy raw content if sed is not available
            xclip -selection clipboard < "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG"
            echo "Full terminal output copied to clipboard (sed not found, ANSI codes not removed)."
        fi
    else
        echo "xclip is not installed; skipping clipboard copy of terminal output."
    fi
    rm -f "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" # Clean up the log file
else
    echo "No terminal output was captured or log file was not created; clipboard not updated."
fi
# --- End of clipboard copy and cleanup block ---

printf '\nLLM command finished. Press any key to close this terminal...'
read -n 1 -s -r
exit 0
```

---
##### `shell/llm_pipe_selected_sys.sh`

```bash
#!/bin/bash
# Takes selected text (clipboard/primary) and pipes to llm with a user-provided system prompt.
# Patched by Gemini to capture all terminal output to clipboard
_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG="/tmp/$(basename "$0" .sh)_terminal_output_$$_${RANDOM}.log"

# Main script logic is executed in a subshell to capture all its output
(
    # Try to get text from clipboard, then primary selection
    SELECTED_TEXT=$(xclip -o -selection clipboard 2>/dev/null)
    if [ -z "$SELECTED_TEXT" ]; then
        SELECTED_TEXT=$(xclip -o -selection primary 2>/dev/null)
    fi

    if [ -z "$SELECTED_TEXT" ]; then
        echo "Action cancelled: No text found in clipboard or primary selection. Copy text first."
        # This script's original pause and exit for this condition:
        printf '\nPress any key to close...'
        read -n 1 -s -r
        exit 1 # This will exit the subshell
    fi

    echo "Selected text obtained."
    echo "Please enter the System Prompt for the selected text (Ctrl+D or empty to cancel):"
    read -p "System Prompt: " SYSTEM_PROMPT

    if [ -z "$SYSTEM_PROMPT" ]; then
        echo "Action cancelled: No system prompt provided."
    else
        echo ""
        echo "Processing selected text with system prompt: $SYSTEM_PROMPT"
        echo "--- Selected Text Start (first 200 chars) ---"
        echo "$SELECTED_TEXT" | head -c 200
        # echo "$SELECTED_TEXT" # Uncomment to see full selected text
        echo "--- Selected Text End (truncated if long) ---"
        echo "Waiting for LLM response..."
        echo ""

        # Pipe the selected text to llm with the system prompt
        echo "$SELECTED_TEXT" | llm --system "$SYSTEM_PROMPT"
    fi
) > "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" 2>&1

# --- Block to copy terminal log to clipboard and cleanup ---
if [ -f "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" ]; then
    if command -v xclip &>/dev/null; then
        if command -v sed &>/dev/null; then
            sed 's/\x1B\[[0-9;]*[JKmsu]//g' "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" | xclip -selection clipboard
            echo "Full terminal output (ANSI codes removed) copied to clipboard."
        else
            xclip -selection clipboard < "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG"
            echo "Full terminal output copied to clipboard (sed not found, ANSI codes not removed)."
        fi
    else
        echo "xclip is not installed; skipping clipboard copy of terminal output."
    fi
    rm -f "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG"
else
    echo "No terminal output was captured or log file was not created; clipboard not updated."
fi
# --- End of clipboard copy and cleanup block ---

printf '\nLLM command finished. Press any key to close this terminal...'
read -n 1 -s -r
exit 0
```

---
##### `shell/llm_sF11_list_fragments.sh`

```bash
#!/bin/bash
# Lists llm fragments.
# Patched by Gemini to capture all terminal output to clipboard
_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG="/tmp/$(basename "$0" .sh)_terminal_output_$$_${RANDOM}.log"

# Main script logic is executed in a subshell to capture all its output
(
    echo "LLM Fragments List"
    echo "Fetching list..."
    echo ""
    llm fragments list
) > "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" 2>&1

# --- Block to copy terminal log to clipboard and cleanup ---
if [ -f "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" ]; then
    if command -v xclip &>/dev/null; then
        if command -v sed &>/dev/null; then
            sed 's/\x1B\[[0-9;]*[JKmsu]//g' "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" | xclip -selection clipboard
            echo "Full terminal output (ANSI codes removed) copied to clipboard."
        else
            xclip -selection clipboard < "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG"
            echo "Full terminal output copied to clipboard (sed not found, ANSI codes not removed)."
        fi
    else
        echo "xclip is not installed; skipping clipboard copy of terminal output."
    fi
    rm -f "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG"
else
    echo "No terminal output was captured or log file was not created; clipboard not updated."
fi
# --- End of clipboard copy and cleanup block ---

printf '\nLLM command finished. Press any key to close this terminal...'
read -n 1 -s -r
exit 0
```

---
##### `shell/llm_sF12_extract_last.sh`

```bash
#!/bin/bash
# Prompts for a message and sends it to llm with o3-mini, extracting the last code block.
# Patched by Gemini to capture all terminal output to clipboard
_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG="/tmp/$(basename "$0" .sh)_terminal_output_$$_${RANDOM}.log"

# Main script logic is executed in a subshell to capture all its output
(
    echo "LLM Extract Last Code Block (o3-mini)"
    read -p "Enter your prompt: " prompt_text

    if [ -z "$prompt_text" ]; then
        echo "No prompt entered. Exiting."
    else
        llm -m o3-mini --xl "$prompt_text"
    fi
) > "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" 2>&1

# --- Block to copy terminal log to clipboard and cleanup ---
if [ -f "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" ]; then
    if command -v xclip &>/dev/null; then
        if command -v sed &>/dev/null; then
            sed 's/\x1B\[[0-9;]*[JKmsu]//g' "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" | xclip -selection clipboard
            echo "Full terminal output (ANSI codes removed) copied to clipboard."
        else
            xclip -selection clipboard < "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG"
            echo "Full terminal output copied to clipboard (sed not found, ANSI codes not removed)."
        fi
    else
        echo "xclip is not installed; skipping clipboard copy of terminal output."
    fi
    rm -f "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG"
else
    echo "No terminal output was captured or log file was not created; clipboard not updated."
fi
# --- End of clipboard copy and cleanup block ---

printf '\nLLM command finished. Press any key to close this terminal...'
read -n 1 -s -r
exit 0
```

---
##### `shell/llm_sF4_prompt.sh`

```bash
#!/bin/bash
# Prompts for a message and sends it to llm with gpt-4.1.
# Patched by Gemini to capture all terminal output to clipboard
_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG="/tmp/$(basename "$0" .sh)_terminal_output_$$_${RANDOM}.log"

# Main script logic is executed in a subshell to capture all its output
(
    echo "LLM with gpt-4.1"
    read -p "Enter your prompt: " prompt_text

    if [ -z "$prompt_text" ]; then
        echo "No prompt entered. Exiting."
    else
        llm -m gpt-4.1 "$prompt_text"
    fi
) > "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" 2>&1

# --- Block to copy terminal log to clipboard and cleanup ---
if [ -f "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" ]; then
    if command -v xclip &>/dev/null; then
        if command -v sed &>/dev/null; then
            sed 's/\x1B\[[0-9;]*[JKmsu]//g' "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" | xclip -selection clipboard
            echo "Full terminal output (ANSI codes removed) copied to clipboard."
        else
            xclip -selection clipboard < "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG"
            echo "Full terminal output copied to clipboard (sed not found, ANSI codes not removed)."
        fi
    else
        echo "xclip is not installed; skipping clipboard copy of terminal output."
    fi
    rm -f "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG"
else
    echo "No terminal output was captured or log file was not created; clipboard not updated."
fi
# --- End of clipboard copy and cleanup block ---

printf '\nLLM command finished. Press any key to close this terminal...'
read -n 1 -s -r
exit 0
```

---
##### `shell/llm_sF6_system_prompt.sh`

```bash
#!/bin/bash
# Prompts for a system prompt and a main prompt for llm.
# Patched by Gemini to capture all terminal output to clipboard
_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG="/tmp/$(basename "$0" .sh)_terminal_output_$$_${RANDOM}.log"

# Main script logic is executed in a subshell to capture all its output
(
    echo "LLM with System Prompt"
    read -p "Enter SYSTEM prompt: " system_prompt
    if [ -z "$system_prompt" ]; then
        echo "No system prompt entered. Exiting."
        # This script's original pause and exit for this condition:
        printf '\nPress any key to close...'
        read -n 1 -s -r
        exit 1 # This will exit the subshell
    fi

    read -p "Enter MAIN prompt: " main_prompt
    if [ -z "$main_prompt" ]; then
        echo "No main prompt entered. Exiting."
    else
        llm --system "$system_prompt" "$main_prompt"
    fi
) > "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" 2>&1

# --- Block to copy terminal log to clipboard and cleanup ---
if [ -f "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" ]; then
    if command -v xclip &>/dev/null; then
        if command -v sed &>/dev/null; then
            sed 's/\x1B\[[0-9;]*[JKmsu]//g' "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" | xclip -selection clipboard
            echo "Full terminal output (ANSI codes removed) copied to clipboard."
        else
            xclip -selection clipboard < "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG"
            echo "Full terminal output copied to clipboard (sed not found, ANSI codes not removed)."
        fi
    else
        echo "xclip is not installed; skipping clipboard copy of terminal output."
    fi
    rm -f "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG"
else
    echo "No terminal output was captured or log file was not created; clipboard not updated."
fi
# --- End of clipboard copy and cleanup block ---

printf '\nLLM command finished. Press any key to close this terminal...'
read -n 1 -s -r
exit 0
```

---
##### `shell/llm_sF8_fragment.sh`

```bash
#!/bin/bash
# Prompts for a fragment source and a main prompt for llm.
# Patched by Gemini to capture all terminal output to clipboard
_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG="/tmp/$(basename "$0" .sh)_terminal_output_$$_${RANDOM}.log"

# Main script logic is executed in a subshell to capture all its output
(
    echo "LLM with Fragment"
    read -p "Enter fragment source (URL or file path): " fragment_source
    if [ -z "$fragment_source" ]; then
        echo "No fragment source entered. Exiting."
        # This script's original pause and exit for this condition:
        printf '\nPress any key to close...'
        read -n 1 -s -r
        exit 1 # This will exit the subshell
    fi

    read -p "Enter MAIN prompt: " main_prompt
    if [ -z "$main_prompt" ]; then
        echo "No main prompt entered. Exiting."
    else
        llm -f "$fragment_source" "$main_prompt"
    fi
) > "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" 2>&1

# --- Block to copy terminal log to clipboard and cleanup ---
if [ -f "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" ]; then
    if command -v xclip &>/dev/null; then
        if command -v sed &>/dev/null; then
            sed 's/\x1B\[[0-9;]*[JKmsu]//g' "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" | xclip -selection clipboard
            echo "Full terminal output (ANSI codes removed) copied to clipboard."
        else
            xclip -selection clipboard < "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG"
            echo "Full terminal output copied to clipboard (sed not found, ANSI codes not removed)."
        fi
    else
        echo "xclip is not installed; skipping clipboard copy of terminal output."
    fi
    rm -f "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG"
else
    echo "No terminal output was captured or log file was not created; clipboard not updated."
fi
# --- End of clipboard copy and cleanup block ---

printf '\nLLM command finished. Press any key to close this terminal...'
read -n 1 -s -r
exit 0
```

---
##### `shell/llm_sF9_attachment.sh`

```bash
#!/bin/bash
# Prompts for a main prompt and an attachment for llm with gpt-4.1-mini.
# Patched by Gemini to capture all terminal output to clipboard
_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG="/tmp/$(basename "$0" .sh)_terminal_output_$$_${RANDOM}.log"

# Main script logic is executed in a subshell to capture all its output
(
    echo "LLM with Attachment (gpt-4.1-mini)"
    read -p "Enter MAIN prompt: " main_prompt
    if [ -z "$main_prompt" ]; then
        echo "No main prompt entered. Exiting."
        # This script's original pause and exit for this condition:
        printf '\nPress any key to close...'
        read -n 1 -s -r
        exit 1 # This will exit the subshell
    fi

    read -p "Enter attachment (URL or file path): " attachment_source
    if [ -z "$attachment_source" ]; then
        echo "No attachment source entered. Exiting."
    else
        llm -m gpt-4.1-mini "$main_prompt" -a "$attachment_source"
    fi
) > "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" 2>&1

# --- Block to copy terminal log to clipboard and cleanup ---
if [ -f "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" ]; then
    if command -v xclip &>/dev/null; then
        if command -v sed &>/dev/null; then
            sed 's/\x1B\[[0-9;]*[JKmsu]//g' "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG" | xclip -selection clipboard
            echo "Full terminal output (ANSI codes removed) copied to clipboard."
        else
            xclip -selection clipboard < "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG"
            echo "Full terminal output copied to clipboard (sed not found, ANSI codes not removed)."
        fi
    else
        echo "xclip is not installed; skipping clipboard copy of terminal output."
    fi
    rm -f "$_GEMINI_SCRIPT_TERMINAL_OUTPUT_LOG"
else
    echo "No terminal output was captured or log file was not created; clipboard not updated."
fi
# --- End of clipboard copy and cleanup block ---

printf '\nLLM command finished. Press any key to close this terminal...'
read -n 1 -s -r
exit 0
```

#### ~/.rpbar.ini

```
[program]
# Window name for rpbar
win_name = rpbar

# Path for the communication socket with rpbarsend
# /tmp/ is generally standard and should work on Debian.
socket_path = /tmp/rpbarsocket

# Separator for program title (likely for ratpoison integration)
sep = $)@=

# Buffer size for communication with ratpoison
bufsize = 2048

# Timeout in seconds for communication
timeout_s = 5

[display]
# Whether rpbar is on the top (1) or bottom (0) of the screen
top = 0

# The Xorg screen (monitor) to display the bar on.
# '0' is typically the primary monitor. Adjust if you have multiple monitors
# and want it on a different one (e.g., 1 for secondary).
# Use `xrandr` to list screens if unsure.
screen = 0 ; Defaulting to primary screen, adjust if needed.

# Padding around the top/bottom of the text within the bar
padding = 4

# Left/right padding for elements like buttons
button_margin = 10

# Padding specifically for the status bar text area
status_padding = 30

# Font string for the bar (e.g., "Font Family Name:size=POINT_SIZE").
# CRITICAL: Ensure "Intel One Mono" is installed on your Debian Bullseye system.
# If not, replace with an available font (e.g., "DejaVu Sans Mono:size=10", "Liberation Mono:size=10", "Monospace:size=10").
# Check availability with `fc-list | grep "Your Font Name"`
font_str = Intel One Mono:size=13 ; ### VERIFY THIS FONT IS INSTALLED OR CHANGE IT ###

[color]
bordercolor = #d7d7d7
bgcolor = #353535
fgcolor = #d7d7d7
mainbgcolor = #d4ccb9
mainfgcolor = #45363b
statusbgcolor = #d7d7d7
statusfgcolor = #353535
```

#### **Configure dratmenu.py (/home/linaro/.local/bin/dratmenu.py)**

{% codeblock python %}
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
dratmenu.py: A dmenu-based window switcher for the Ratpoison Window Manager.

This script fetches the list of current windows from Ratpoison, presents them
in dmenu for selection, and then tells Ratpoison to switch to the chosen window.
It is updated for Python 3 and aims for robustness.
"""

import subprocess
import sys
import shlex # For safer command construction if needed, though not strictly required here

# --- Configuration ---

# Separator string used internally to parse Ratpoison output.
# IMPORTANT: This exact string MUST NOT appear in any window number, class, or title.
# Using a complex, unlikely sequence to minimize collision risk.
SEP = "~!@#DRATMENU_SEP#@!~"

# Separator used *within dmenu* to separate the hidden window number from the visible text.
# A tab character is often a good choice as it's unlikely to be the *first* character
# in the formatted display string and easy to split on.
DMENU_SEP = '\t'

# dmenu appearance settings (adjust as needed)
# Font examples:
# FONT = "-*-terminus-*-r-*-*-14-*-*-*-*-*-*-*"
# FONT = "-*-jetbrains mono-*-r-*-*-14-*-*-*-*-*-*-*"
FONT = 'Intel One Mono:size=13' # Default Terminus
NORMAL_BG = '#002b36'      # Solarized Dark base03
SELECTED_BG = '#859900'    # Solarized Dark green
NUM_LINES = '20'           # Number of lines dmenu shows vertically

# --- Helper Function ---

def run_subprocess(command_list, input_data=None):
    """
    Runs a subprocess, handling text encoding/decoding and errors.

    Args:
        command_list (list): The command and its arguments.
        input_data (str, optional): String data to pass to the command's stdin. Defaults to None.

    Returns:
        subprocess.CompletedProcess: The result object from subprocess.run.

    Raises:
        FileNotFoundError: If the command is not found.
        subprocess.CalledProcessError: If the command returns a non-zero exit code.
        Exception: For other unexpected errors during execution.
    """
    try:
        result = subprocess.run(
            command_list,
            input=input_data,
            capture_output=True, # Capture stdout and stderr
            text=True,           # Work with text (auto encodes input, decodes output)
            check=True,          # Raise CalledProcessError on non-zero exit codes
            encoding='utf-8'     # Explicitly use UTF-8
        )
        return result
    except FileNotFoundError:
        print(f"Error: Command '{command_list[0]}' not found. Is it installed and in your PATH?", file=sys.stderr)
        raise # Re-raise the exception to be caught by the main logic
    except subprocess.CalledProcessError as e:
        # check=True raises this, stderr is part of the exception object
        print(f"Error running command: {' '.join(e.cmd)}", file=sys.stderr)
        print(f"Return code: {e.returncode}", file=sys.stderr)
        if e.stderr:
            print(f"Stderr: {e.stderr.strip()}", file=sys.stderr)
        # Don't raise here if we want to handle specific return codes (like dmenu cancel) later
        # For now, let the main logic handle specific cases if needed, otherwise re-raise
        raise
    except Exception as e:
        print(f"An unexpected error occurred running {' '.join(command_list)}: {e}", file=sys.stderr)
        raise

# --- Main Logic ---

def main():
    # 1. Get window list from Ratpoison
    # Format: %n<SEP>%c<SEP>%t (number, class, title)
    rp_list_cmd = ['ratpoison', '-c', f"windows %n{SEP}%c{SEP}%t"]
    try:
        rp_result = run_subprocess(rp_list_cmd)
    except (FileNotFoundError, subprocess.CalledProcessError, Exception):
        sys.exit(1) # Error message already printed by run_subprocess

    # Process the output from Ratpoison
    stdout_str = rp_result.stdout.strip()
    if not stdout_str:
        print("No ratpoison windows found.", file=sys.stderr)
        sys.exit(0)

    lines = stdout_str.split('\n')
    windows_data = [] # Store tuples of (number, class, title)
    for i, ln in enumerate(lines):
        parts = ln.split(SEP)
        if len(parts) == 3:
            windows_data.append(parts)
        else:
            print(f"Warning: Skipping malformed line {i+1} from ratpoison (separator issue?): {ln}", file=sys.stderr)

    if not windows_data:
        print("No valid window data parsed from ratpoison.", file=sys.stderr)
        sys.exit(1)

    # 2. Format window list for dmenu
    # Format for dmenu input: "<number><DMENU_SEP><formatted_display_string>"
    # The <number> part is hidden by dmenu but used for selection later.
    dmenu_input_lines = []
    for num, current, title in windows_data:
        # Format the part visible in dmenu
        display_str = f"{num.rjust(3)} {current.ljust(10)[:10]} {title}"
        # Prepend the raw number and the dmenu separator
        dmenu_input_lines.append(f"{num}{DMENU_SEP}{display_str}")

    dmenu_input_text = '\n'.join(dmenu_input_lines)

    # 3. Pipe the list to dmenu and get the selection
    dmenu_cmd = ['dmenu', '-i',                # Case-insensitive
                 '-sb', SELECTED_BG,         # Selected background
                 '-nb', NORMAL_BG,           # Normal background
                 '-fn', FONT,                # Font
                 '-l', NUM_LINES]            # Lines to display

    try:
        # We expect dmenu might return 1 if the user cancels (e.g., Esc)
        # So, we temporarily disable check=True and handle return codes manually
        dmenu_result = subprocess.run(
            dmenu_cmd,
            input=dmenu_input_text,
            capture_output=True,
            text=True,
            encoding='utf-8'
            # check=False # Default, handle return code below
        )

        if dmenu_result.returncode == 1:
            # User cancelled dmenu (e.g., pressed Esc)
            print("dmenu cancelled by user.", file=sys.stderr)
            sys.exit(0)
        elif dmenu_result.returncode != 0:
            # Other dmenu error
            print(f"Error running dmenu.", file=sys.stderr)
            print(f"Return code: {dmenu_result.returncode}", file=sys.stderr)
            if dmenu_result.stderr:
                print(f"Stderr: {dmenu_result.stderr.strip()}", file=sys.stderr)
            sys.exit(1)

        selection = dmenu_result.stdout.strip()

    except FileNotFoundError:
        print(f"Error: Command 'dmenu' not found. Is it installed and in your PATH?", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred running dmenu: {e}", file=sys.stderr)
        sys.exit(1)

    # 4. Extract the *actual* window number from the selection
    if not selection:
        # Should not happen if return code was 0, but check anyway
        print("dmenu returned success but selection is empty.", file=sys.stderr)
        sys.exit(1)

    try:
        # Split the selected line ONLY at the first dmenu separator
        # The first part is the raw window number we embedded
        sel_number = selection.split(DMENU_SEP, 1)[0]

        # Basic validation that it looks like a number
        if not sel_number.isdigit():
             raise ValueError("Extracted selection number is not a digit.")

    except (IndexError, ValueError) as e:
        print(f"Error: Could not parse window number from dmenu selection.", file=sys.stderr)
        print(f"Selected line: '{selection}'", file=sys.stderr)
        print(f"Reason: {e}", file=sys.stderr)
        sys.exit(1)

    # 5. Tell Ratpoison to select the chosen window
    rp_select_cmd = ['ratpoison', '-c', f'select {sel_number}']
    try:
        run_subprocess(rp_select_cmd)
    except (FileNotFoundError, subprocess.CalledProcessError, Exception):
        # Error message already printed by run_subprocess
        sys.exit(1)

    # Success!
    sys.exit(0)

if __name__ == "__main__":
    main()
{% endcodeblock %}

#### **Configure ratpoison.py (/home/linaro/.local/bin/ratpoison.py)**

```python
import os
ratpoison = os.getenv('RATPOISON') or 'ratpoison'
def rp_command( *args ):
    p = os.popen( ratpoison + ' -c ' + '"' + (' '.join(  args  ) ) + '"', 'r' )
    r = p.readlines();
    p.close();
    return r


def rp_abort( *args ): return rp_command ( 'abort ' +  ' '.join( args ) )
def rp_addhook( *args ): return rp_command ( 'addhook ' +  ' '.join( args ) )
def rp_alias( *args ): return rp_command ( 'alias ' +  ' '.join( args ) )
def rp_banish( *args ): return rp_command ( 'banish ' +  ' '.join( args ) )
def rp_chdir( *args ): return rp_command ( 'chdir ' +  ' '.join( args ) )
def rp_clrunmanaged( *args ): return rp_command ( 'clrunmanaged ' +  ' '.join( args ) )
def rp_colon( *args ): return rp_command ( 'colon ' +  ' '.join( args ) )
def rp_curframe( *args ): return rp_command ( 'curframe ' +  ' '.join( args ) )
def rp_definekey( *args ): return rp_command ( 'definekey ' +  ' '.join( args ) )
def rp_undefinekey( *args ): return rp_command ( 'undefinekey ' +  ' '.join( args ) )
def rp_delete( *args ): return rp_command ( 'delete ' +  ' '.join( args ) )
def rp_delkmap( *args ): return rp_command ( 'delkmap ' +  ' '.join( args ) )
def rp_echo( *args ): return rp_command ( 'echo ' +  ' '.join( args ) )
def rp_escape( *args ): return rp_command ( 'escape ' +  ' '.join( args ) )
def rp_exec( *args ): return rp_command ( 'exec ' +  ' '.join( args ) )
def rp_execa( *args ): return rp_command ( 'execa ' +  ' '.join( args ) )
def rp_execf( *args ): return rp_command ( 'execf ' +  ' '.join( args ) )
def rp_fdump( *args ): return rp_command ( 'fdump ' +  ' '.join( args ) )
def rp_focus( *args ): return rp_command ( 'focus ' +  ' '.join( args ) )
def rp_focusprev( *args ): return rp_command ( 'focusprev ' +  ' '.join( args ) )
def rp_focusdown( *args ): return rp_command ( 'focusdown ' +  ' '.join( args ) )
def rp_exchangeup( *args ): return rp_command ( 'exchangeup ' +  ' '.join( args ) )
def rp_exchangedown( *args ): return rp_command ( 'exchangedown ' +  ' '.join( args ) )
def rp_exchangeleft( *args ): return rp_command ( 'exchangeleft ' +  ' '.join( args ) )
def rp_exchangeright( *args ): return rp_command ( 'exchangeright ' +  ' '.join( args ) )
def rp_swap( *args ): return rp_command ( 'swap ' +  ' '.join( args ) )
def rp_focuslast( *args ): return rp_command ( 'focuslast ' +  ' '.join( args ) )
def rp_focusleft( *args ): return rp_command ( 'focusleft ' +  ' '.join( args ) )
def rp_focusright( *args ): return rp_command ( 'focusright ' +  ' '.join( args ) )
def rp_focusup( *args ): return rp_command ( 'focusup ' +  ' '.join( args ) )
def rp_frestore( *args ): return rp_command ( 'frestore ' +  ' '.join( args ) )
def rp_fselect( *args ): return rp_command ( 'fselect ' +  ' '.join( args ) )
def rp_gdelete( *args ): return rp_command ( 'gdelete ' +  ' '.join( args ) )
def rp_getenv( *args ): return rp_command ( 'getenv ' +  ' '.join( args ) )
def rp_gmerge( *args ): return rp_command ( 'gmerge ' +  ' '.join( args ) )
def rp_gmove( *args ): return rp_command ( 'gmove ' +  ' '.join( args ) )
def rp_gnew( *args ): return rp_command ( 'gnew ' +  ' '.join( args ) )
def rp_gnewbg( *args ): return rp_command ( 'gnewbg ' +  ' '.join( args ) )
def rp_gnumber( *args ): return rp_command ( 'gnumber ' +  ' '.join( args ) )
def rp_grename( *args ): return rp_command ( 'grename ' +  ' '.join( args ) )
def rp_gnext( *args ): return rp_command ( 'gnext ' +  ' '.join( args ) )
def rp_gprev( *args ): return rp_command ( 'gprev ' +  ' '.join( args ) )
def rp_gother( *args ): return rp_command ( 'gother ' +  ' '.join( args ) )
def rp_gravity( *args ): return rp_command ( 'gravity ' +  ' '.join( args ) )
def rp_groups( *args ): return rp_command ( 'groups ' +  ' '.join( args ) )
def rp_gselect( *args ): return rp_command ( 'gselect ' +  ' '.join( args ) )
def rp_help( *args ): return rp_command ( 'help ' +  ' '.join( args ) )
def rp_hsplit( *args ): return rp_command ( 'hsplit ' +  ' '.join( args ) )
def rp_info( *args ): return rp_command ( 'info ' +  ' '.join( args ) )
def rp_kill( *args ): return rp_command ( 'kill ' +  ' '.join( args ) )
def rp_lastmsg( *args ): return rp_command ( 'lastmsg ' +  ' '.join( args ) )
def rp_license( *args ): return rp_command ( 'license ' +  ' '.join( args ) )
def rp_link( *args ): return rp_command ( 'link ' +  ' '.join( args ) )
def rp_listhook( *args ): return rp_command ( 'listhook ' +  ' '.join( args ) )
def rp_meta( *args ): return rp_command ( 'meta ' +  ' '.join( args ) )
def rp_msgwait( *args ): return rp_command ( 'msgwait ' +  ' '.join( args ) )
def rp_newkmap( *args ): return rp_command ( 'newkmap ' +  ' '.join( args ) )
def rp_newwm( *args ): return rp_command ( 'newwm ' +  ' '.join( args ) )
def rp_next( *args ): return rp_command ( 'next ' +  ' '.join( args ) )
def rp_nextscreen( *args ): return rp_command ( 'nextscreen ' +  ' '.join( args ) )
def rp_number( *args ): return rp_command ( 'number ' +  ' '.join( args ) )
def rp_only( *args ): return rp_command ( 'only ' +  ' '.join( args ) )
def rp_other( *args ): return rp_command ( 'other ' +  ' '.join( args ) )
def rp_prev( *args ): return rp_command ( 'prev ' +  ' '.join( args ) )
def rp_prevscreen( *args ): return rp_command ( 'prevscreen ' +  ' '.join( args ) )
def rp_quit( *args ): return rp_command ( 'quit ' +  ' '.join( args ) )
def rp_ratinfo( *args ): return rp_command ( 'ratinfo ' +  ' '.join( args ) )
def rp_ratrelinfo( *args ): return rp_command ( 'ratrelinfo ' +  ' '.join( args ) )
def rp_banishrel( *args ): return rp_command ( 'banishrel ' +  ' '.join( args ) )
def rp_ratwarp( *args ): return rp_command ( 'ratwarp ' +  ' '.join( args ) )
def rp_ratrelwarp( *args ): return rp_command ( 'ratrelwarp ' +  ' '.join( args ) )
def rp_ratclick( *args ): return rp_command ( 'ratclick ' +  ' '.join( args ) )
def rp_rathold( *args ): return rp_command ( 'rathold ' +  ' '.join( args ) )
def rp_readkey( *args ): return rp_command ( 'readkey ' +  ' '.join( args ) )
def rp_redisplay( *args ): return rp_command ( 'redisplay ' +  ' '.join( args ) )
def rp_remhook( *args ): return rp_command ( 'remhook ' +  ' '.join( args ) )
def rp_remove( *args ): return rp_command ( 'remove ' +  ' '.join( args ) )
def rp_removeup( *args ): return rp_command ( 'removeup ' +  ' '.join( args ) )
def rp_removedown( *args ): return rp_command ( 'removedown ' +  ' '.join( args ) )
def rp_removeleft( *args ): return rp_command ( 'removeleft ' +  ' '.join( args ) )
def rp_removeright( *args ): return rp_command ( 'removeright ' +  ' '.join( args ) )
def rp_resize( *args ): return rp_command ( 'resize ' +  ' '.join( args ) )
def rp_restart( *args ): return rp_command ( 'restart ' +  ' '.join( args ) )
def rp_rudeness( *args ): return rp_command ( 'rudeness ' +  ' '.join( args ) )
def rp_select( *args ): return rp_command ( 'select ' +  ' '.join( args ) )
def rp_set( *args ): return rp_command ( 'set ' +  ' '.join( args ) )
def rp_setenv( *args ): return rp_command ( 'setenv ' +  ' '.join( args ) )
def rp_shrink( *args ): return rp_command ( 'shrink ' +  ' '.join( args ) )
def rp_sfrestore( *args ): return rp_command ( 'sfrestore ' +  ' '.join( args ) )
def rp_source( *args ): return rp_command ( 'source ' +  ' '.join( args ) )
def rp_sselect( *args ): return rp_command ( 'sselect ' +  ' '.join( args ) )
def rp_startup_message( *args ): return rp_command ( 'startup_message ' +  ' '.join( args ) )
def rp_time( *args ): return rp_command ( 'time ' +  ' '.join( args ) )
def rp_title( *args ): return rp_command ( 'title ' +  ' '.join( args ) )
def rp_tmpwm( *args ): return rp_command ( 'tmpwm ' +  ' '.join( args ) )
def rp_unalias( *args ): return rp_command ( 'unalias ' +  ' '.join( args ) )
def rp_unmanage( *args ): return rp_command ( 'unmanage ' +  ' '.join( args ) )
def rp_unsetenv( *args ): return rp_command ( 'unsetenv ' +  ' '.join( args ) )
def rp_verbexec( *args ): return rp_command ( 'verbexec ' +  ' '.join( args ) )
def rp_version( *args ): return rp_command ( 'version ' +  ' '.join( args ) )
def rp_vsplit( *args ): return rp_command ( 'vsplit ' +  ' '.join( args ) )
def rp_warp( *args ): return rp_command ( 'warp ' +  ' '.join( args ) )
def rp_windows( *args ): return rp_command ( 'windows ' +  ' '.join( args ) )
def rp_cnext( *args ): return rp_command ( 'cnext ' +  ' '.join( args ) )
def rp_cother( *args ): return rp_command ( 'cother ' +  ' '.join( args ) )
def rp_cprev( *args ): return rp_command ( 'cprev ' +  ' '.join( args ) )
def rp_dedicate( *args ): return rp_command ( 'dedicate ' +  ' '.join( args ) )
def rp_describekey( *args ): return rp_command ( 'describekey ' +  ' '.join( args ) )
def rp_inext( *args ): return rp_command ( 'inext ' +  ' '.join( args ) )
def rp_iother( *args ): return rp_command ( 'iother ' +  ' '.join( args ) )
def rp_iprev( *args ): return rp_command ( 'iprev ' +  ' '.join( args ) )
def rp_prompt( *args ): return rp_command ( 'prompt ' +  ' '.join( args ) )
def rp_sdump( *args ): return rp_command ( 'sdump ' +  ' '.join( args ) )
def rp_sfdump( *args ): return rp_command ( 'sfdump ' +  ' '.join( args ) )
def rp_undo( *args ): return rp_command ( 'undo ' +  ' '.join( args ) )
def rp_redo( *args ): return rp_command ( 'redo ' +  ' '.join( args ) )
def rp_putsel( *args ): return rp_command ( 'putsel ' +  ' '.join( args ) )
def rp_getsel( *args ): return rp_command ( 'getsel ' +  ' '.join( args ) )
def rp_commands( *args ): return rp_command ( 'commands ' +  ' '.join( args ) )
```

#### .Xresources

```
! +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
! title      Nord XResources                                    +
! project    nord-xresources                                    +
! version    0.1.0                                              +
! repository https://github.com/arcticicestudio/nord-xresources +
! author     Arctic Ice Studio                                  +
! email      development@arcticicestudio.com                    +
! copyright  Copyright (C) 2016                                 +
! +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#define nord0 #2E3440
#define nord1 #3B4252
#define nord2 #434C5E
#define nord3 #4C566A
#define nord4 #D8DEE9
#define nord5 #E5E9F0
#define nord6 #ECEFF4
#define nord7 #8FBCBB
#define nord8 #88C0D0
#define nord9 #81A1C1
#define nord10 #5E81AC
#define nord11 #BF616A
#define nord12 #D08770
#define nord13 #EBCB8B
#define nord14 #A3BE8C
#define nord15 #B48EAD

*.foreground:   nord4
*.background:   nord0
*.cursorColor:  nord4
*fading: 0
*fadeColor: nord3

*.color0: nord1
*.color1: nord11
*.color2: nord14
*.color3: nord13
*.color4: nord9
*.color5: nord15
*.color6: nord8
*.color7: nord5
*.color8: nord3
*.color9: nord11
*.color10: nord14
*.color11: nord13
*.color12: nord9
*.color13: nord15
*.color14: nord7
*.color15: nord6
```
#### Setting Up `rpws` for Desktop Switching

To configure desktop switching with `rpws`, you will need to add the following line to your `~/.ratpoisonrc` file:

```sh
exec rpws init N -k
```

Where `N` is the number of desktops you wish to create (at least 2). The `-k` flag is optional and is only necessary if you want to use predefined keybindings for switching desktops and managing windows.

When `rpws` is initialized, it will create `N` desktops, and by default, it assigns the following keybindings:

- `Alt+F(N)` - Switch to desktop `N` (e.g., `Alt+F1` switches to the first desktop).
- `Ctrl+Alt+Right` - Go to the next desktop.
- `Ctrl+Alt+Left` - Go to the previous desktop.
- `Ctrl+Alt+Windows+F(N)` - Move the current window to desktop `N`.
- `Ctrl+Alt+>` - Move the window to the next desktop.
- `Ctrl+Alt+<` - Move the window to the previous desktop.

However, you may find these keybindings inconvenient or difficult to use. In that case, you can customize them to suit your preferences.

#### Customizing `rpws` Hotkeys

To customize the keybindings, add the following lines to your `~/.ratpoisonrc` file:

```sh
# Initialize 6 desktops
exec rpws init 6

# Switch desktops with the Windows+digit combination
definekey top s-1 exec rpws 1
definekey top s-2 exec rpws 2
definekey top s-3 exec rpws 3
definekey top s-4 exec rpws 4
definekey top s-5 exec rpws 5
definekey top s-6 exec rpws 6

# Move windows to desktops using Windows+F(N)
definekey top s-F1 exec rpws move1
definekey top s-F2 exec rpws move2
definekey top s-F3 exec rpws move3
definekey top s-F4 exec rpws move4
definekey top s-F5 exec rpws move5
definekey top s-F6 exec rpws move6

# Move between desktops with Windows+Right/Left
definekey top s-Right exec rpws next
definekey top s-Left exec rpws prev

# Move window to next/previous desktop using Windows+Up/Down
definekey top s-Up exec rpws movenext
definekey top s-Down exec rpws moveprev
```

##### Keybinding Legend:
- `C` stands for **Ctrl**
- `S` stands for the **Windows** key
- `M` stands for **Alt**

For example, `C-S-M-q` represents pressing `Ctrl + Windows + Alt + q` in sequence.

### **Step 5: Configure User-Specific X Settings (~/.xsessionrc)**

The ~/.xsessionrc file (in /home/linaro/) is executed when your X session starts via LightDM. It’s useful for setting environment variables or running commands like xrandr before Ratpoison loads. This file must be executable.  
`nano /home/linaro/.xsessionrc`

Add your configurations, for example:  
{% codeblock %}
#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
# set -e

# Optional: Uncomment to log script execution for debugging
LOG_FILE=~/xsessionrc_debug.log
echo "$(date): .xsessionrc started" >> "$LOG_FILE"

# Define custom mode for DP-1 (1152x864 @ 60Hz)
# Ensure standard spaces are used in the modeline string.
# Modeline: "1152x864_60.00" 81.75 1152 1216 1336 1520 864 867 871 897 -hsync +vsync
xrandr --newmode "1152x864_60.00" 81.75 1152 1216 1336 1520 864 867 871 897 -hsync +vsync # 2>&1 | tee -a "$LOG_FILE"

# Define custom mode for HDMI-1 (2560x1080 @ 60Hz)
# Modeline: "2560x1080_60.00" 230.00 2560 2720 2992 3424 1080 1083 1093 1120 -hsync +vsync
xrandr --newmode "2560x1080_60.00" 230.00 2560 2720 2992 3424 1080 1083 1093 1120 -hsync +vsync # 2>&1 | tee -a "$LOG_FILE"

# Add the new modes to the respective outputs
xrandr --addmode DP-1 "1152x864_60.00" # 2>&1 | tee -a "$LOG_FILE"
xrandr --addmode HDMI-1 "2560x1080_60.00" # 2>&1 | tee -a "$LOG_FILE"

# Apply the modes and set the layout.
# NOTE: The command below sets DP-1 as primary.
# Your comment "# makes HDMI-1 primary" conflicts with this.
# Adjust --primary flag if HDMI-1 should be the primary display.
xrandr \
    --output DP-1 --primary --mode "1152x864_60.00" --below HDMI-1 \
    --output HDMI-1 --mode "2560x1080_60.00" # 2>&1 | tee -a "$LOG_FILE"

# Example: Start a key remapper or other background utility
# xmodmap /home/ linaro/.Xmodmap

# Example: Set an environment variable
# export QT_QPA_PLATFORMTHEME=qt5ct

echo "$(date): .xsessionrc finished successfully" >> "$LOG_FILE"
{% endcodeblock %}

Make it executable:  
`chmod +x /home/linaro/.xsessionrc`

### **Step 6: (Optional but Recommended) Remove XFCE4**

If you no longer need XFCE4 and want to free up disk space, you can remove its packages. **Be cautious** and review the packages to be removed before confirming.  
`# Identify XFCE4 meta-packages and components`  
`sudo apt purge xfce4 xfce4-goodies libxfce4ui-utils xfce4-panel xfce4-session xfce4-settings xfconf xfdesktop4 xfwm4 thunar mousepad parole ristretto`  
`# This list might need adjustment based on your specific XFCE4 installation.`  
`# Always review the list of packages apt proposes to remove.`  
`sudo apt autoremove`  
`sudo apt clean`

### **Step 7: Verify the Setup**

Reboot your system or restart LightDM to apply changes:  
`sudo systemctl restart lightdm`

Your system should automatically log in linaro directly into a Ratpoison session.  
**Troubleshooting:**

* LightDM logs: /var/log/lightdm/lightdm.log and seat-specific logs (e.g., /var/log/lightdm/seat0-greeter.log).  
* Xorg logs: ~/.local/share/xorg/Xorg.0.log (for user sessions) or /var/log/Xorg.0.log.  
* Session errors: Check ~/.xsession-errors (in /home/linaro/) for issues from ~/.xsessionrc or session startup.

### **Alternative: Manual Start with startx (If Not Using LightDM)**

If you choose not to use LightDM or wish to start Ratpoison manually from a TTY (console login):

1. Ensure xinit is installed: sudo apt install xinit.  
2. Create or edit ~/.xinitrc (in /home/linaro/.xinitrc):  
   `nano /home/linaro/.xinitrc`  
   Add:  

```
#!/bin/sh
# ~/.xinitrc for linaro

# Source user-specific X settings if desired (contents similar to .xsessionrc)
# if [ -f /home/linaro/.xprofile_custom ]; then
#  . /home/linaro/.xprofile_custom
# fi
# For xrandr, etc., you might call them directly here or source .xsessionrc
if [ -f /home/linaro/.xsessionrc ]; then
  . /home/linaro/.xsessionrc
fi

exec ratpoison
```

4. Make it executable: `chmod +x /home/linaro/.xinitrc`
5. Log in to a TTY as linaro and run startx.

This approach bypasses LightDM. The primary focus of this guide is the LightDM autologin method.
