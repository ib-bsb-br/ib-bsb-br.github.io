---
tags: [scratchpad]
info: aberto.
date: 2025-05-12
type: post
layout: post
published: true
slug: backup-bash-script
title: 'backup bash script'
---
```
#!/bin/bash

# ==============================================================================
# Script Name: comprehensive_backup_v2.sh
# Description: Archives (tar) and compresses (zstd) files from a source
#              directory to a destination file. Offers configuration for
#              compression level, progress view (pv), I/O buffering (mbuffer),
#              and exclusions. Includes pre-checks and basic verification steps.
# Author:      AI Assistant
# Version:     2.0
# Usage:       sudo bash comprehensive_backup_v2.sh
# Requirements: bash, sudo, tar, zstd, pv, mbuffer, coreutils (du, df, awk, numfmt, stat)
# ==============================================================================

# --- Script Setup ---
# Exit immediately if a command exits with a non-zero status.
# set -e
# Treat unset variables as an error when substituting.
# set -u
# Cause pipelines to return the exit status of the last command that exited with a non-zero status,
# or zero if no command exited with a non-zero status.
set -o pipefail

# --- Configuration ---
DEFAULT_SOURCE_DIR="/media/usb0"
DEFAULT_DEST_DIR="/media/usb5"
DEFAULT_FILENAME_BASE="backup_usb0"
DEFAULT_COMPRESSION_LEVEL=9 # Good balance (1-19)
DEFAULT_USE_PV="y"
DEFAULT_USE_MBUFFER="y"
DEFAULT_MBUFFER_SIZE="6G" # e.g., 128M, 256M, 512M, 1G
DEFAULT_EXCLUDE_PATTERNS=() # Add patterns like: ('./cache/*' '*.tmp')

# --- Helper Functions ---
check_command() {
  if ! command -v "$1" &> /dev/null; then
    echo "Error: Required command '$1' not found. Please install it (e.g., using 'sudo apt install $1')." >&2
    exit 1
  fi
}

print_separator() {
  printf -- '-%.0s' {1..70}; printf '\n'
}

# --- Root Check ---
if [[ $EUID -ne 0 ]]; then
   echo "Error: This script must be run with sudo privileges for accurate size checks and potentially writing to protected locations." >&2
   exit 1
fi

# --- Dependency Check ---
print_separator
echo "Checking required commands..."
check_command tar
check_command zstd
check_command pv
check_command mbuffer
check_command du
check_command df
check_command awk
check_command numfmt
check_command stat
echo "All required commands found."

# --- User Input / Configuration Override ---
print_separator
echo "Configure Backup Parameters (Press Enter for defaults):"

read -p "Source directory [${DEFAULT_SOURCE_DIR}]: " SOURCE_DIR
SOURCE_DIR=${SOURCE_DIR:-$DEFAULT_SOURCE_DIR}

read -p "Destination directory [${DEFAULT_DEST_DIR}]: " DEST_DIR
DEST_DIR=${DEST_DIR:-$DEFAULT_DEST_DIR}

read -p "Base filename for archive [${DEFAULT_FILENAME_BASE}]: " FILENAME_BASE
FILENAME_BASE=${FILENAME_BASE:-$DEFAULT_FILENAME_BASE}

read -p "Compression level (1=fastest, 19=best, default=${DEFAULT_COMPRESSION_LEVEL}): " COMPRESSION_LEVEL
COMPRESSION_LEVEL=${COMPRESSION_LEVEL:-$DEFAULT_COMPRESSION_LEVEL}
# Basic validation for compression level
if ! [[ "$COMPRESSION_LEVEL" =~ ^[1-9]$|^1[0-9]$ ]]; then # Regex for 1-19
  echo "Invalid compression level. Using default: ${DEFAULT_COMPRESSION_LEVEL}"
  COMPRESSION_LEVEL=$DEFAULT_COMPRESSION_LEVEL
fi

read -p "Use 'pv' for progress monitoring? (Y/n) [${DEFAULT_USE_PV}]: " USE_PV
USE_PV=${USE_PV:-$DEFAULT_USE_PV}

read -p "Use 'mbuffer' for I/O buffering? (y/N) [${DEFAULT_USE_MBUFFER}]: " USE_MBUFFER
USE_MBUFFER=${USE_MBUFFER:-$DEFAULT_USE_MBUFFER}
MBUFFER_SIZE=$DEFAULT_MBUFFER_SIZE
if [[ "${USE_MBUFFER,,}" == "y" ]]; then
  read -p "mbuffer size (e.g., 256M, 1G) [${DEFAULT_MBUFFER_SIZE}]: " MBUFFER_SIZE_INPUT
  MBUFFER_SIZE=${MBUFFER_SIZE_INPUT:-$DEFAULT_MBUFFER_SIZE}
fi

# Exclude pattern input
echo "Enter exclude patterns one by one (relative to source, e.g., './cache/*', '*.tmp'). Press Enter on empty line to finish."
EXCLUDE_PATTERNS=()
while true; do
    read -p "Exclude pattern (or Enter to finish): " pattern
    if [[ -z "$pattern" ]]; then
        break
    fi
    EXCLUDE_PATTERNS+=("$pattern")
done
if [ ${#EXCLUDE_PATTERNS[@]} -eq 0 ]; then
    EXCLUDE_PATTERNS=("${DEFAULT_EXCLUDE_PATTERNS[@]}") # Use default if none entered
fi


# --- Pre-Checks ---
print_separator
echo "Performing Pre-Checks..."

# Check directories
if [ ! -d "$SOURCE_DIR" ]; then
  echo "Error: Source directory '$SOURCE_DIR' not found or not a directory." >&2
  exit 1
fi
if [ ! -d "$DEST_DIR" ]; then
  echo "Error: Destination directory '$DEST_DIR' not found or not a directory." >&2
  exit 1
fi
# Optional: Check if they are mount points (informational)
if ! mountpoint -q "$SOURCE_DIR"; then
    echo "Info: Source directory '$SOURCE_DIR' does not appear to be a distinct mount point."
fi
if ! mountpoint -q "$DEST_DIR"; then
    echo "Info: Destination directory '$DEST_DIR' does not appear to be a distinct mount point."
fi

# Check source size
echo "Calculating source size (this may take a while)..."
SRC_SIZE_BYTES=$(du -sb "$SOURCE_DIR" 2>/dev/null)
DU_EXIT_CODE=$?
if [ $DU_EXIT_CODE -ne 0 ] || [ -z "$SRC_SIZE_BYTES" ]; then
    echo "Error: Could not determine source size (du exit code: $DU_EXIT_CODE). Check permissions for '$SOURCE_DIR'." >&2
    exit 1
fi
SRC_SIZE_BYTES=$(echo "$SRC_SIZE_BYTES" | awk '{print $1}') # Extract number
SRC_SIZE_HUMAN=$(numfmt --to=iec $SRC_SIZE_BYTES)
echo "Source size: ${SRC_SIZE_HUMAN} (${SRC_SIZE_BYTES} bytes)"

# Check if source seems empty
if [ "$SRC_SIZE_BYTES" -le 4096 ]; then # 4096 is typical size of an empty directory metadata
    echo "Warning: Source directory size is very small. It might be empty or contain only empty subdirectories."
fi

# Check destination space
DEST_AVAIL_BYTES=$(df --output=avail -B1 "$DEST_DIR" 2>/dev/null | awk 'NR==2{print $1}')
DF_EXIT_CODE=$?
if [ $DF_EXIT_CODE -ne 0 ] || [ -z "$DEST_AVAIL_BYTES" ]; then
    echo "Error: Could not determine destination available space (df exit code: $DF_EXIT_CODE). Check path '$DEST_DIR'." >&2
    exit 1
fi
DEST_AVAIL_HUMAN=$(numfmt --to=iec $DEST_AVAIL_BYTES)
echo "Destination available space: ${DEST_AVAIL_HUMAN} (${DEST_AVAIL_BYTES} bytes)"

# Space warning
if [ "$SRC_SIZE_BYTES" -gt "$DEST_AVAIL_BYTES" ]; then
  print_separator
  echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
  echo "!!! WARNING: Source size (${SRC_SIZE_HUMAN}) is LARGER than available"
  echo "!!!          destination space (${DEST_AVAIL_HUMAN})."
  echo "!!! This operation will ONLY succeed if the data compresses"
  echo "!!! significantly (below ${DEST_AVAIL_HUMAN}). Consider using a higher"
  echo "!!! compression level (current: ${COMPRESSION_LEVEL}) or freeing up space."
  echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
  print_separator
elif [ "$DEST_AVAIL_BYTES" -lt "$((SRC_SIZE_BYTES / 2))" ]; then # Heuristic: Warn if available space is less than half the source size
  echo "Warning: Available destination space (${DEST_AVAIL_HUMAN}) is less than half the source size. Ensure compression is effective."
fi

# Construct final destination path and check for collision
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DEST_FILENAME="${FILENAME_BASE}_L${COMPRESSION_LEVEL}_${TIMESTAMP}.tar.zst"
DEST_FILE_PATH="${DEST_DIR}/${DEST_FILENAME}"

if [ -e "$DEST_FILE_PATH" ]; then
    echo "Error: Destination file '$DEST_FILE_PATH' already exists." >&2
    read -p "Do you want to overwrite it? (y/N): " OVERWRITE_CONFIRM
    if [[ "${OVERWRITE_CONFIRM,,}" != "y" ]]; then
        echo "Aborted by user."
        exit 0
    fi
    echo "Overwriting existing file."
fi

# Final confirmation
print_separator
echo "Backup Summary:"
echo "  Source:      $SOURCE_DIR ($SRC_SIZE_HUMAN)"
echo "  Destination: $DEST_FILE_PATH"
echo "  Compression: Level $COMPRESSION_LEVEL"
echo "  Progress View: ${USE_PV}"
echo "  IO Buffering: ${USE_MBUFFER} (Size: $MBUFFER_SIZE)"
if [ ${#EXCLUDE_PATTERNS[@]} -gt 0 ]; then
    echo "  Exclusions:  ${EXCLUDE_PATTERNS[*]}"
fi
print_separator

read -p "Do you want to proceed with the backup? (y/N): " CONFIRM_PROCEED
if [[ "${CONFIRM_PROCEED,,}" != "y" ]]; then
  echo "Aborted by user."
  exit 0
fi

# --- Build and Execute the Command Pipeline ---
print_separator
echo "Building and executing the command pipeline..."

# Start with tar command (relative paths within archive)
TAR_CMD=("tar" "-cf" "-")

# Add exclude patterns
for pattern in "${EXCLUDE_PATTERNS[@]}"; do
    TAR_CMD+=("--exclude=${pattern}")
done

# Specify source directory context and content
TAR_CMD+=("-C" "$SOURCE_DIR" ".")

# Build the pipeline string array for clarity and execution
PIPELINE_STAGES=()
PIPELINE_STAGES+=("$(printf '%q ' "${TAR_CMD[@]}")") # Stage 0: tar

# Add pv if requested
if [[ "${USE_PV,,}" == "y" ]]; then
  PIPELINE_STAGES+=("| pv -s $SRC_SIZE_BYTES") # Stage 1: pv
fi

# Add mbuffer if requested
if [[ "${USE_MBUFFER,,}" == "y" ]]; then
  PIPELINE_STAGES+=("| mbuffer -m $MBUFFER_SIZE") # Stage 2 (or 1 if no pv): mbuffer
fi

# Add zstd command
PIPELINE_STAGES+=("| zstd -T0 -${COMPRESSION_LEVEL} -o '${DEST_FILE_PATH}'") # Final Stage: zstd

# Combine stages into a single command string for execution
FULL_PIPELINE_CMD="${PIPELINE_STAGES[*]}"

# Check if running inside screen/tmux
if [[ -z "$STY" && -z "$TMUX" ]]; then
    echo "Warning: Not running inside screen or tmux."
    echo "For long operations, it's highly recommended to run this script"
    echo "within a 'screen' or 'tmux' session to prevent interruptions."
    read -p "Press Enter to continue anyway, or Ctrl+C to stop and restart in screen/tmux."
fi

echo "Starting backup process... This may take a very long time."
echo "Executing: ${FULL_PIPELINE_CMD}"

# Execute the pipeline using bash -c
# Capture PIPESTATUS immediately after execution
bash -c "$FULL_PIPELINE_CMD"; PIPE_STATUS=("${PIPESTATUS[@]}")
EXECUTION_EXIT_CODE=$? # Overall exit code (affected by pipefail)

# --- Post-Execution ---
print_separator
echo "Backup process finished."

# Check exit codes from the pipeline
FINAL_EXIT_CODE=0
STAGE_NAMES=("tar") # Start with tar
if [[ "${USE_PV,,}" == "y" ]]; then STAGE_NAMES+=("pv"); fi
if [[ "${USE_MBUFFER,,}" == "y" ]]; then STAGE_NAMES+=("mbuffer"); fi
STAGE_NAMES+=("zstd")

echo "Checking pipeline exit codes: ${PIPE_STATUS[*]}"
for i in "${!PIPE_STATUS[@]}"; do
    stage_name=${STAGE_NAMES[$i]:-"unknown_stage_$i"}
    exit_code=${PIPE_STATUS[$i]}
    if [ "$exit_code" -ne 0 ]; then
        echo "Error: Pipeline stage '${stage_name}' failed with exit code $exit_code." >&2
        FINAL_EXIT_CODE=$exit_code # Report the first non-zero exit code
    fi
done

# Double check overall exit code if pipefail was active
if [ "$FINAL_EXIT_CODE" -eq 0 ] && [ "$EXECUTION_EXIT_CODE" -ne 0 ]; then
     echo "Warning: Overall pipeline check reported failure (exit code $EXECUTION_EXIT_CODE), but individual stages seemed okay. Check results carefully." >&2
     # Use the overall code if it indicates failure and individual checks didn't
     FINAL_EXIT_CODE=$EXECUTION_EXIT_CODE
fi


if [ "$FINAL_EXIT_CODE" -eq 0 ]; then
    echo "Pipeline completed successfully (basic check)."
    COMPRESSED_SIZE_BYTES=$(stat -c%s "$DEST_FILE_PATH" 2>/dev/null)
    COMPRESSED_SIZE_HUMAN=$(numfmt --to=iec $COMPRESSED_SIZE_BYTES 2>/dev/null || echo "N/A")
    echo "Archive saved to: ${DEST_FILE_PATH}"
    echo "Compressed size:  ${COMPRESSED_SIZE_HUMAN} (${COMPRESSED_SIZE_BYTES:-N/A} bytes)"
    print_separator
    echo "IMPORTANT: Please verify the integrity of the archive:"
    echo "1. Test compression: zstd -t '${DEST_FILE_PATH}'"
    echo "2. List contents (optional, takes time/CPU): tar --list -I zstd -f '${DEST_FILE_PATH}' | less"
    print_separator
else
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" >&2
    echo "!!! ERRORS DETECTED during the backup process (Exit Code: ${FINAL_EXIT_CODE})." >&2
    echo "!!! The archive file '${DEST_FILE_PATH}' may be incomplete or corrupt." >&2
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" >&2
    exit $FINAL_EXIT_CODE
fi

exit 0
```