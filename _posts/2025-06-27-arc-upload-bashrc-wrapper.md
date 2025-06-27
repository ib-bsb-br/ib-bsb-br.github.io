---
tags: [scratchpad]
info: aberto.
date: 2025-06-27
type: post
layout: post
published: true
slug: arc-bash
title: 'ARC upload `.bashrc` wrapper'
---
Add this to your ~/.bashrc file:
``` 
# ==============================================================================
# The "Ultimate" Command Output Uploader (v6.0)
#
# PHILOSOPHY: True effectiveness is completeness of information and precision of
# control. This version captures everything a command outputs (stdout & stderr)
# and provides clear, actionable diagnostics on failure.
# ==============================================================================
upload() {
  # Check for UPLOAD_URL once to avoid repeated errors.
  if [ -z "$UPLOAD_URL" ]; then
      echo "❌ FAIL: UPLOAD_URL environment variable is not set." >&2
      return 1
  fi

  # Generate a clean, timestamped filename from the command arguments.
  local remote_filename="$(echo "$*" | tr -s ' /|><&;()$' '_')_$(date +'%F_%T').txt"

  echo "▶️  Executing: '${*}'"
  echo "⏫ Uploading all output (stdout & stderr) as '${remote_filename}'"
  echo "------------------------------------------------------------------"

  # Execute in a subshell with pipefail for accurate error codes.
  (
    set -o pipefail
    # CRITICAL: `2>&1` merges stderr into stdout, ensuring all output is
    # captured and piped to curl for a complete log.
    eval "$@" 2>&1 | curl --silent --show-error -f -F "fileToUpload=@-;filename=${remote_filename}" "$UPLOAD_URL"
  )

  local exit_code=$?
  if [ $exit_code -eq 0 ]; then
    echo "✅ OK"
  else
    # Provide nuanced feedback by checking against known curl error codes.
    case $exit_code in
      6)  echo "❌ UPLOAD FAIL (Code $exit_code): Could not resolve host. Check URL/DNS." >&2 ;;
      7)  echo "❌ UPLOAD FAIL (Code $exit_code): Failed to connect to host." >&2 ;;
      22) echo "❌ UPLOAD FAIL (Code $exit_code): HTTP error (4xx/5xx). Check server." >&2 ;;
      *)  echo "❌ COMMAND FAIL (Code $exit_code): The command itself failed." >&2 ;;
    esac
    return $exit_code
  fi
}
```