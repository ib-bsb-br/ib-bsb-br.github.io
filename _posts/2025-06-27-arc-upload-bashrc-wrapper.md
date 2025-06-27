---
tags: [scratchpad]
info: aberto.
date: 2025-06-27
type: post
layout: post
published: true
slug: arc-upload-bashrc-wrapper
title: 'ARC upload `.bashrc` wrapper'
---
Add this to your ~/.bashrc file:
``` 
# ==============================================================================
# Definitive Command Output Uploader (v3.0)
#
# Description:
# Securely and efficiently executes any command, streaming its stdout directly
# to a remote server for upload.
#
# Features:
# - Secure: Executes commands safely without `eval`.
# - Scalable: Streams output directly, using minimal memory for large outputs.
# - Robust Error Handling: Uses `pipefail` to report the true exit code of
#   the executed command, not the upload tool.
# - Configurable: Uses an environment variable for the upload URL.
# - Filename Generation: Creates a clean, timestamped filename.
#
# Usage:
#   export UPLOAD_URL="https://arcreformas.com.br/upload.php"
#   upload [command-to-execute] [args...]
#
# Example:
#   upload journalctl -u ssh
#   upload cat /var/log/syslog
# ==============================================================================
upload() {
  # 1. Configuration and Argument Checks
  if [ -z "$UPLOAD_URL" ]; then
    echo "[Upload Error] UPLOAD_URL environment variable is not set." >&2
    return 1
  fi
  if [ $# -eq 0 ]; then
    echo "[Upload Error] No command provided. Usage: upload [command] [args...]" >&2
    return 1
  fi

  # 2. Filename Generation
  local timestamp=$(date +'%Y-%m-%d_%H-%M-%S')
  # Use $* here to get a single string for the filename.
  local sanitized_command=$(echo "$*" | tr -s ' /|><&;()$' '_')
  local remote_filename="${sanitized_command}_${timestamp}.txt"

  # 3. Execution and Streaming Upload
  echo "▶️  Executing: '$@'"
  echo "⏫ Streaming output as '$remote_filename' to $UPLOAD_URL"
  echo "------------------------------------------------------------------"

  # Set `pipefail` to ensure the pipeline's exit code is that of the
  # first command to fail, not the last. The `()` creates a subshell
  # so this setting is temporary and doesn't affect the user's main shell.
  (
    set -o pipefail
    # Use "$@" here to safely pass all arguments to the command.
    # The command's stdout is streamed directly to curl's stdin.
    "$@" | curl --progress-bar -f -F "fileToUpload=@-;filename=${remote_filename}" "$UPLOAD_URL"
  )

  # 4. Final Status Reporting
  local exit_code=$?
  if [ $exit_code -eq 0 ]; then
    echo -e "\n------------------------------------------------------------------\n✅ Command and upload successful."
  else
    # pipefail makes it possible to distinguish command failures from curl failures.
    # See https://curl.se/docs/manpage.html for curl exit codes.
    if [ $exit_code -eq 22 ]; then # 4xx/5xx HTTP error
        echo -e "\n------------------------------------------------------------------\n❌ Upload failed: Server returned an error." >&2
    elif [ $exit_code -eq 6 ]; then # Couldn't resolve host
        echo -e "\n------------------------------------------------------------------\n❌ Upload failed: Could not resolve host. Check URL or network." >&2
    else
        echo -e "\n------------------------------------------------------------------\n❌ Command failed with exit code $exit_code." >&2
    fi
    return $exit_code
  fi
}
``` 
In-Depth Breakdown of Key Improvements
 * (set -o pipefail; ...): This is the most critical improvement.
   * set -o pipefail: This shell option changes the behavior of pipelines. Normally, a pipeline's exit code is that of the last command (curl). With pipefail, the exit code is that of the rightmost command to exit with a non-zero status. If your command fdisk -l fails, the pipeline's exit code will reflect that failure, even if curl never ran.
   * Subshell (): We wrap the entire operation in a subshell. This is crucial because set -o pipefail is a setting we only want to apply temporarily for this one command. The subshell acts as a sandbox; once it exits, the pipefail setting vanishes and does not affect your main terminal session.
 * "$@" | curl ...: This is the core of the streaming architecture.
   * "$@": This safely executes the command and its arguments. There is no eval. There is no storing of output in a variable.
   * |: The standard output of your command is piped as it's generated directly to the standard input of curl. This uses a trivial amount of memory, regardless of whether the output is 1 kilobyte or 100 gigabytes.
 * local exit_code=$?: After the subshell finishes, we immediately capture its exit code. Thanks to pipefail, this variable now holds a meaningful value reflecting the success or failure of the entire operation, which allows for much more precise error reporting.
4. Advanced Usage and Handling Edge Cases
A) Interactive Commands (sudo, ssh)
This script will not work with commands that prompt for interactive input on the terminal (like a password). The sudo prompt would be piped to curl, and the script would hang.
Solution: Authenticate before you run the upload. The sudo command has a flag to "prime" the authentication timer.
# Wrong way - this will hang
upload sudo apt update

# Right way - authenticate first, then upload
sudo -v # This will prompt for a password if needed.
upload sudo apt update

B) Needing to See Output While Uploading
The current script consumes the output. If you want to see it on your screen and upload it, we must bring back tee and process substitution. You can create a second, specialized function for this.
```
# Add this function to .bashrc for "see and upload" scenarios
upload_tee() {
  if [ -z "$UPLOAD_URL" ] || [ $# -eq 0 ]; then
      upload # Reuse the main function to show usage errors
      return 1
  fi
  local timestamp=$(date +'%Y-%m-%d_%H-%M-%S')
  local sanitized_command=$(echo "$*" | tr -s ' /|><&;()$' '_')
  local remote_filename="${sanitized_command}_${timestamp}.txt"
  
  echo "▶️  Executing: '$@' (Output will be shown and uploaded)"
  echo "⏫ Uploading as '$remote_filename'"
  echo "------------------------------------------------------------------"
  
  (
    set -o pipefail
    # tee splits the stream: one copy goes to the screen (stdout of tee),
    # the other goes to curl via the pipe.
    "$@" | tee >(curl -f -F "fileToUpload=@-;filename=${remote_filename}" "$UPLOAD_URL" >/dev/null)
  )
  # Note: Error reporting is less precise here because tee can mask curl's exit code.
  # This version prioritizes convenience over perfect error reporting.
}
``` 