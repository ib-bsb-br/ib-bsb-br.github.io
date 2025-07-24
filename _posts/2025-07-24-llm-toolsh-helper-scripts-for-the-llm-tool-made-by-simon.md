---
tags: [scratchpad]
info: aberto.
date: 2025-07-24
type: post
layout: post
published: true
slug: llm-toolsh-helper-scripts-for-the-llm-tool-made-by-simon
title: 'llm-tool.sh - helper scripts for the LLM Tool made by simon '
---
```bash
#!/bin/bash
#
# llm-tool.sh: A Unified Command-Line Interface for the LLM Tool
#
# This script integrates functionalities from multiple helper scripts into a single, 
# maintainable tool. It supports various modes of interaction, including file analysis, 
# free-form prompts, system prompts, fragments, attachments, extracting code, and listing fragments.
#
# It uses a two-layer execution model:
#   - OUTER mode: Sets up session logging with `script` and handles clipboard copying.
#   - INNER mode: Executes the core functionality based on user-selected mode.
#
# Usage examples:
#   llm-tool.sh "What is the capital of France?"
#   llm-tool.sh --system "You are a pirate" "Where can I find treasure?"
#   llm-tool.sh --analyze ./my_script.py
#   ls -la | llm-tool.sh --pipe -s "Summarize the directory listing."
#   llm-tool.sh --extract-code "write a bash script to count files" > count.sh
#
# To display the help message:
#   llm-tool.sh --help

# === Configuration ===
LLM_CMD="/root/.local/bin/llm"
GEMINI_CAPTURE_MODE="${GEMINI_CAPTURE_MODE:-outer}"  # Defaults to outer mode (session capture)
DEFAULT_MODEL="o3-mini"

# === Helper Functions ===

# Display help message with usage examples and mode explanations.
show_help() {
    cat <<EOF
LLM Integrated Tool - Unified Interface for the LLM CLI

USAGE:
  llm-tool.sh [MODE] [OPTIONS] [PROMPT...]
  (For session capture, run normally. To bypass logging, use: GEMINI_CAPTURE_MODE=inner)

MODES (choose one):
  --analyze <file>         Analyze the content of a file.
  --pipe (-p)              Process text piped from stdin.
  --extract-code (-x)      Extract the last code block from the output.
  --list-fragments (-l)    List saved LLM fragments.
  --system (-s) <system_prompt> <main_prompt>
                           Use a system prompt and main prompt.
  --fragment (-f) <source> <main_prompt>
                           Use a fragment (file or URL) with a main prompt.
  --attach (-a) <attachment> <main_prompt>
                           Attach a file or URL with a main prompt.
  (If no mode is provided, the remaining argument(s) are sent as a simple prompt.)

OTHER OPTIONS:
  -m, --model <name>       Specify the LLM model to use (default: $DEFAULT_MODEL)
  -h, --help               Show this help message

EXAMPLES:
  llm-tool.sh "What is the capital of France?"
  llm-tool.sh --system "You are a historian" "Explain the fall of the Roman Empire."
  llm-tool.sh --analyze ./data.txt
  ls -la | llm-tool.sh --pipe -s "Summarize this directory listing."
  llm-tool.sh --extract-code "Generate a bash script to list files" > list_files.sh

EOF
}

# Check for required dependencies.
check_dependency() {
    if ! command -v "$1" &>/dev/null; then
        echo "Error: '$1' not found. Please install it." >&2
        return 1
    fi
    return 0
}

# Pause until user presses a key.
pause_to_exit() {
    echo
    read -n 1 -s -r -p "Operation finished. Press any key to exit..."
    echo
}

# Clean and optionally copy content to the clipboard.
copy_to_clipboard() {
    local content="$1"
    if check_dependency xsel; then
        echo "$content" | xsel --clipboard --input && echo "Output has been copied to the clipboard." || \
            echo "Warning: Failed to copy to clipboard." >&2
    else
        echo "Info: 'xsel' not available; clipboard copy skipped." >&2
    fi
}

# Centralized session capture wrapper: re-executes the script in inner mode.
run_in_session_capture() {
    local log_file
    log_file=$(mktemp "/tmp/llm-tool_session_XXXXXXXXXX.log") || { echo "Error: Unable to create temp file." >&2; exit 1; }
    trap 'rm -f "$log_file"' EXIT HUP INT TERM

    # Capture entire session using 'script'
    check_dependency script || { echo "Error: 'script' command required for session logging." >&2; exit 1; }
    script -q -e -c "GEMINI_CAPTURE_MODE=inner bash \"$0\"" "$log_file"
    local exit_status=$?

    # If possible, clean the log and try to copy it to clipboard.
    if [ -s "$log_file" ]; then
        local cleaned
        [ "$(command -v col)" ] && cleaned=$(col -b < "$log_file") || cleaned=$(cat "$log_file")
        [ "$(command -v sed)" ] && cleaned=$(echo "$cleaned" | sed -E 's/\x1B\[[0-9;?]*[a-zA-Z]//g; s/\r$//g; s/\r([^\n])/\1/g')
        copy_to_clipboard "$cleaned"
        echo "Session log is located at: $log_file"
    else
        echo "No session output captured."
    fi

    pause_to_exit
    exit $exit_status
}

# === Core Mode Functions (Inner Execution) ===

do_analyze() {
    local file="$TARGET_FILE"
    [ -z "$file" ] && { echo "Error: No file specified for analysis." >&2; exit 1; }
    if [ ! -f "$file" ]; then
        echo "Error: File '$file' not found." >&2
        exit 1
    fi
    local analyze_prompt="Use your full analytic capacity to provide a thorough explanation: In what fundamental and causal ways does the file ('$file') consist? Please discuss: (i) Key events or conditions leading to its current state; (ii) Its essential or structural nature; (iii) Its broader purpose and significance."
    echo "Analyzing file: $file"
    cat "$file" | "$LLM_CMD" -m "${MODEL:-$DEFAULT_MODEL}" -s "$analyze_prompt"
}

do_prompt() {
    [ -z "$MAIN_PROMPT" ] && { echo "Error: No prompt provided." >&2; exit 1; }
    "$LLM_CMD" -m "${MODEL:-$DEFAULT_MODEL}" "$MAIN_PROMPT"
}

do_system_prompt() {
    [ -z "$SYSTEM_PROMPT" ] || [ -z "$MAIN_PROMPT" ] && { echo "Error: Both system and main prompts are required." >&2; exit 1; }
    "$LLM_CMD" --system "$SYSTEM_PROMPT" "$MAIN_PROMPT"
}

do_fragment() {
    [ -z "$FRAGMENT_SOURCE" ] || [ -z "$MAIN_PROMPT" ] && { echo "Error: Fragment source and main prompt required." >&2; exit 1; }
    "$LLM_CMD" -f "$FRAGMENT_SOURCE" "$MAIN_PROMPT"
}

do_attach() {
    [ -z "$ATTACH_SOURCE" ] || [ -z "$MAIN_PROMPT" ] && { echo "Error: Attachment source and main prompt required." >&2; exit 1; }
    "$LLM_CMD" -m gpt-4.1-mini -a "$ATTACH_SOURCE" "$MAIN_PROMPT"
}

do_extract() {
    [ -z "$MAIN_PROMPT" ] && { echo "Error: No prompt provided for code extraction." >&2; exit 1; }
    "$LLM_CMD" -m "${MODEL:-$DEFAULT_MODEL}" --xl "$MAIN_PROMPT"
}

do_list() {
    "$LLM_CMD" fragments list
}

do_pipe() {
    if [ -t 0 ]; then
        echo "Error: Pipe mode requires data from stdin. Example: cat file | llm-tool.sh --pipe" >&2
        exit 1
    fi
    # Optionally, allow user to set a system prompt via -s
    "$LLM_CMD" -m "${MODEL:-$DEFAULT_MODEL}"
}

# Mode dispatcher: calls the appropriate function based on MODE.
main() {
    case "$MODE" in
        analyze)       do_analyze ;;
        pipe)          do_pipe ;;
        extract-code)  do_extract ;;
        list-fragments) do_list ;;
        system)        do_system_prompt ;;
        fragment)      do_fragment ;;
        attach)        do_attach ;;
        default)       do_prompt ;;
        help)          show_help ;;
        *)             echo "Invalid mode '$MODE'. Use --help for usage." >&2; exit 1 ;;
    esac
}

# === Outer Execution: Parse Arguments and Setup Modes ===

if [ "$GEMINI_CAPTURE_MODE" = "inner" ]; then
    # INNER MODE: Run core logic directly.
    main
    exit $?
else
    # DEFAULT OUTER MODE: Parse CLI arguments and initiate session capture.
    # Initialize mode variables.
    MODE="default"
    SYSTEM_PROMPT=""
    FRAGMENT_SOURCE=""
    ATTACH_SOURCE=""
    MODEL=""
    TARGET_FILE=""
    MAIN_PROMPT=""

    # Parse arguments.
    while [ "$#" -gt 0 ]; do
        case "$1" in
            -h|--help)
                MODE="help"
                shift ;;
            --analyze)
                MODE="analyze"
                TARGET_FILE="$2"
                shift 2 ;;
            -p|--pipe)
                MODE="pipe"
                shift ;;
            -x|--extract-code)
                MODE="extract-code"
                shift ;;
            -l|--list-fragments)
                MODE="list-fragments"
                shift ;;
            --system)
                MODE="system"
                SYSTEM_PROMPT="$2"
                shift 2 ;;
            --fragment|-f)
                MODE="fragment"
                FRAGMENT_SOURCE="$2"
                shift 2 ;;
            --attach|-a)
                MODE="attach"
                ATTACH_SOURCE="$2"
                shift 2 ;;
            -m|--model)
                MODEL="$2"
                shift 2 ;;
            *)
                # Append any remaining arguments as the main prompt.
                if [ -z "$MAIN_PROMPT" ]; then
                    MAIN_PROMPT="$1"
                else
                    MAIN_PROMPT="$MAIN_PROMPT $1"
                fi
                shift ;;
        esac
    done

    # Check for conflicting options
    if [ "$MODE" = "analyze" ] && { [ -n "$FRAGMENT_SOURCE" ] || [ -n "$ATTACH_SOURCE" ]; }; then
        echo "Error: --analyze cannot be combined with --fragment or --attach." >&2
        exit 1
    fi

    # Export variables for inner mode
    export MODE SYSTEM_PROMPT FRAGMENT_SOURCE ATTACH_SOURCE MODEL TARGET_FILE MAIN_PROMPT

    # Run the complete session capture wrapper.
    run_in_session_capture
fi
```