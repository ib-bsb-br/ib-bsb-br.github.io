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

{% codeblock bash %}
#!/usr/bin/env bash

# ==============================================================================
# Script Name: comprehensive_backup_v3.sh
# Description: Robust tar+zstd backup with pre-checks, progress (pv), optional
#              buffering (mbuffer), exclusions, and detailed exit-code handling.
# Usage:       sudo bash comprehensive_backup_v3.sh
# Requirements: bash, tar, zstd, du, df, awk, numfmt, stat
#               Optional: pv, mbuffer, ionice
# ==============================================================================

set -o pipefail
umask 077
IFS=$'\n\t'

# --- Configuration defaults ---
DEFAULT_SOURCE_DIR="/media/usb0"
DEFAULT_DEST_DIR="/media/usb5"
DEFAULT_FILENAME_BASE="backup_usb0"
DEFAULT_COMPRESSION_LEVEL=9          # 1–19, higher = better compression, slower
DEFAULT_USE_PV="y"
DEFAULT_USE_MBUFFER="y"
DEFAULT_MBUFFER_SIZE="6G"            # e.g., 128M, 512M, 1G, 6G
DEFAULT_EXCLUDE_PATTERNS=()          # e.g., ('./cache/*' '*.tmp')

# --- Helper functions ---
print_separator() {
  printf '%0.s-' {1..70}
  printf '\n'
}

die() {
  printf 'Error: %s\n' "$*" >&2
  exit 1
}

warn() {
  printf 'Warning: %s\n' "$*" >&2
}

info() {
  printf '%s\n' "$*"
}

check_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    die "Required command '$1' not found. Install it (e.g., 'sudo apt install $1')."
  fi
}

read_with_default() {
  # $1 = prompt, $2 = default
  local prompt default reply
  prompt=$1
  default=$2
  read -r -p "$prompt" reply
  if [[ -z $reply ]]; then
    reply=$default
  fi
  printf '%s' "$reply"
}

confirm_yes() {
  # Prompt user; return 0 if yes, 1 otherwise
  local prompt reply
  prompt=$1
  read -r -p "$prompt" reply
  reply=${reply:-n}
  case "${reply,,}" in
    y|yes) return 0 ;;
    *)     return 1 ;;
  esac
}

# --- Root check ---
if [[ $EUID -ne 0 ]]; then
  die "This script must be run with sudo/root privileges."
fi

START_TIME=$(date +%s)

on_exit() {
  local exit_code=$?
  local end_time elapsed h m s
  end_time=$(date +%s)
  elapsed=$((end_time - START_TIME))
  h=$((elapsed / 3600))
  m=$(((elapsed % 3600) / 60))
  s=$((elapsed % 60))
  print_separator
  printf 'Total runtime: %02d:%02d:%02d (exit code %d)\n' "$h" "$m" "$s" "$exit_code"
}
trap on_exit EXIT

# --- Dependency checks ---
print_separator
info "Checking required commands..."
check_command tar
check_command zstd
check_command du
check_command df
check_command awk
check_command numfmt
check_command stat

# Optional tools checked only if used later
OPTIONAL_PV_PRESENT=0
OPTIONAL_MBUFFER_PRESENT=0
if command -v pv >/dev/null 2>&1; then
  OPTIONAL_PV_PRESENT=1
fi
if command -v mbuffer >/dev/null 2>&1; then
  OPTIONAL_MBUFFER_PRESENT=1
fi
info "Core commands available."

# --- Interactive configuration ---
print_separator
info "Configure backup parameters (press Enter for defaults)."

SOURCE_DIR=$(read_with_default "Source directory [${DEFAULT_SOURCE_DIR}]: " "$DEFAULT_SOURCE_DIR")
DEST_DIR=$(read_with_default "Destination directory [${DEFAULT_DEST_DIR}]: " "$DEFAULT_DEST_DIR")
FILENAME_BASE=$(read_with_default "Base filename for archive [${DEFAULT_FILENAME_BASE}]: " "$DEFAULT_FILENAME_BASE")

COMPRESSION_LEVEL=$(read_with_default "Compression level (1=fast,19=best,default=${DEFAULT_COMPRESSION_LEVEL}): " "$DEFAULT_COMPRESSION_LEVEL")
if ! [[ "$COMPRESSION_LEVEL" =~ ^[1-9]$|^1[0-9]$ ]]; then
  warn "Invalid compression level '$COMPRESSION_LEVEL'; using default ${DEFAULT_COMPRESSION_LEVEL}."
  COMPRESSION_LEVEL=$DEFAULT_COMPRESSION_LEVEL
fi

USE_PV=$(read_with_default "Use 'pv' for progress monitoring? (Y/n) [${DEFAULT_USE_PV}]: " "$DEFAULT_USE_PV")
case "${USE_PV,,}" in
  y|yes) USE_PV="y" ;;
  n|no)  USE_PV="n" ;;
  *)     USE_PV="$DEFAULT_USE_PV" ;;
esac

USE_MBUFFER=$(read_with_default "Use 'mbuffer' for I/O buffering? (Y/n) [${DEFAULT_USE_MBUFFER}]: " "$DEFAULT_USE_MBUFFER")
case "${USE_MBUFFER,,}" in
  y|yes) USE_MBUFFER="y" ;;
  n|no)  USE_MBUFFER="n" ;;
  *)     USE_MBUFFER="$DEFAULT_USE_MBUFFER" ;;
esac

MBUFFER_SIZE=$DEFAULT_MBUFFER_SIZE
if [[ "$USE_MBUFFER" == "y" ]]; then
  if (( OPTIONAL_MBUFFER_PRESENT == 0 )); then
    warn "'mbuffer' not found; disabling mbuffer usage."
    USE_MBUFFER="n"
  else
    MBUFFER_SIZE=$(read_with_default "mbuffer size (e.g., 256M, 1G) [${DEFAULT_MBUFFER_SIZE}]: " "$DEFAULT_MBUFFER_SIZE")
  fi
fi

if [[ "$USE_PV" == "y" && $OPTIONAL_PV_PRESENT -eq 0 ]]; then
  warn "'pv' not found; disabling pv usage."
  USE_PV="n"
fi

# Exclude patterns input
info "Enter exclude patterns one per line (relative to source, e.g., './cache/*', '*.tmp')."
info "Press Enter on an empty line to finish."
EXCLUDE_PATTERNS=()
while :; do
  read -r -p "Exclude pattern (or Enter to finish): " pattern
  if [[ -z $pattern ]]; then
    break
  fi
  EXCLUDE_PATTERNS+=("$pattern")
done
if ((${#EXCLUDE_PATTERNS[@]} == 0)); then
  EXCLUDE_PATTERNS=("${DEFAULT_EXCLUDE_PATTERNS[@]}")
fi

# --- Pre-checks ---
print_separator
info "Performing pre-checks..."

# Directory checks
[[ -d $SOURCE_DIR ]] || die "Source directory '$SOURCE_DIR' does not exist or is not a directory."
[[ -d $DEST_DIR ]]   || die "Destination directory '$DEST_DIR' does not exist or is not a directory."

if ! mountpoint -q "$SOURCE_DIR"; then
  warn "Source directory '$SOURCE_DIR' is not a dedicated mount point."
fi
if ! mountpoint -q "$DEST_DIR"; then
  warn "Destination directory '$DEST_DIR' is not a dedicated mount point."
fi

# Source size
info "Calculating source size (du -sb)..."
if ! SRC_SIZE_LINE=$(du -sb -- "$SOURCE_DIR" 2>/dev/null); then
  die "Could not determine source size with du -sb '$SOURCE_DIR'."
fi
SRC_SIZE_BYTES=$(awk '{print $1}' <<<"$SRC_SIZE_LINE")
if [[ -z $SRC_SIZE_BYTES ]]; then
  die "Failed to parse source size from du output."
fi
SRC_SIZE_HUMAN=$(numfmt --to=iec "$SRC_SIZE_BYTES")
info "Source size: ${SRC_SIZE_HUMAN} (${SRC_SIZE_BYTES} bytes)"

if (( SRC_SIZE_BYTES <= 4096 )); then
  warn "Source directory size is very small; it may be effectively empty."
fi

# Destination free space
if ! DEST_AVAIL_BYTES=$(df --output=avail -B1 -- "$DEST_DIR" 2>/dev/null | awk 'NR==2{print $1}'); then
  die "Could not determine destination available space for '$DEST_DIR'."
fi
if [[ -z $DEST_AVAIL_BYTES ]]; then
  die "Failed to parse destination available space."
fi
DEST_AVAIL_HUMAN=$(numfmt --to=iec "$DEST_AVAIL_BYTES")
info "Destination available space: ${DEST_AVAIL_HUMAN} (${DEST_AVAIL_BYTES} bytes)"

if (( SRC_SIZE_BYTES > DEST_AVAIL_BYTES )); then
  print_separator
  warn "Source size (${SRC_SIZE_HUMAN}) is larger than destination free space (${DEST_AVAIL_HUMAN})."
  warn "Backup will only succeed if compression reduces data below available space."
elif (( DEST_AVAIL_BYTES < SRC_SIZE_BYTES / 2 )); then
  warn "Destination free space is less than half the source size; ensure compression is effective."
fi

# Destination file path
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DEST_FILENAME="${FILENAME_BASE}_L${COMPRESSION_LEVEL}_${TIMESTAMP}.tar.zst"
DEST_FILE_PATH="${DEST_DIR%/}/$DEST_FILENAME"

if [[ -e $DEST_FILE_PATH ]]; then
  if confirm_yes "Destination file '$DEST_FILE_PATH' exists. Overwrite? (y/N): "; then
    warn "Overwriting existing file."
  else
    info "Aborting."
    exit 0
  fi
fi

# --- Summary and confirmation ---
print_separator
info "Backup summary:"
info "  Source:      $SOURCE_DIR ($SRC_SIZE_HUMAN)"
info "  Destination: $DEST_FILE_PATH"
info "  Compression: zstd level $COMPRESSION_LEVEL"

PROGRESS_STR="pv disabled"
[[ $USE_PV == y ]] && PROGRESS_STR="pv enabled"
BUFFER_STR="none"
[[ $USE_MBUFFER == y ]] && BUFFER_STR="mbuffer ($MBUFFER_SIZE)"

info "  Progress:    $PROGRESS_STR"
info "  IO buffer:   $BUFFER_STR"

if ((${#EXCLUDE_PATTERNS[@]} > 0)); then
  info "  Exclusions:  ${EXCLUDE_PATTERNS[*]}"
fi
print_separator

if ! confirm_yes "Proceed with backup? (y/N): "; then
  info "Aborted by user."
  exit 0
fi

# Optionally lower priority for the backup process
if confirm_yes "Lower CPU/IO priority for backup (recommended on busy systems)? (y/N): "; then
  if command -v ionice >/dev/null 2>&1; then
    ionice -c3 -p "$$" >/dev/null 2>&1 || warn "ionice failed to adjust I/O priority."
  fi
  renice 10 -p "$$" >/dev/null 2>&1 || true
fi

# --- Build tar command array ---
TAR_CMD=(tar -cf -)
for pattern in "${EXCLUDE_PATTERNS[@]}"; do
  TAR_CMD+=(--exclude="$pattern")
done
TAR_CMD+=(-C "$SOURCE_DIR" .)

# --- Execute backup pipeline ---
print_separator
PIPE_DESC="tar | "
[[ $USE_PV == y ]] && PIPE_DESC+="pv | "
[[ $USE_MBUFFER == y ]] && PIPE_DESC+="mbuffer | "
PIPE_DESC+="zstd"
info "Starting backup process..."
info "Running $PIPE_DESC ..."
print_separator

PIPE_STATUS=()
EXECUTION_EXIT_CODE=0

run_pipeline() {
  if [[ $USE_PV == y && $USE_MBUFFER == y ]]; then
    "${TAR_CMD[@]}" \
      | pv -s "$SRC_SIZE_BYTES" \
      | mbuffer -m "$MBUFFER_SIZE" \
      | zstd -T0 "-${COMPRESSION_LEVEL}" -o "$DEST_FILE_PATH"
  elif [[ $USE_PV == y && $USE_MBUFFER != y ]]; then
    "${TAR_CMD[@]}" \
      | pv -s "$SRC_SIZE_BYTES" \
      | zstd -T0 "-${COMPRESSION_LEVEL}" -o "$DEST_FILE_PATH"
  elif [[ $USE_PV != y && $USE_MBUFFER == y ]]; then
    "${TAR_CMD[@]}" \
      | mbuffer -m "$MBUFFER_SIZE" \
      | zstd -T0 "-${COMPRESSION_LEVEL}" -o "$DEST_FILE_PATH"
  else
    "${TAR_CMD[@]}" \
      | zstd -T0 "-${COMPRESSION_LEVEL}" -o "$DEST_FILE_PATH"
  fi
}

run_pipeline
EXECUTION_EXIT_CODE=$?
PIPE_STATUS=("${PIPESTATUS[@]}")

print_separator
info "Backup process finished."
info "Checking pipeline exit codes: ${PIPE_STATUS[*]:-none}"

STAGE_NAMES=("tar")
if [[ $USE_PV == y ]]; then STAGE_NAMES+=("pv"); fi
if [[ $USE_MBUFFER == y ]]; then STAGE_NAMES+=("mbuffer"); fi
STAGE_NAMES+=("zstd")

FINAL_EXIT_CODE=0
for i in "${!PIPE_STATUS[@]}"; do
  stage_name=${STAGE_NAMES[$i]:-stage_$i}
  stage_status=${PIPE_STATUS[$i]}
  if [[ $stage_status -ne 0 ]]; then
    printf 'Error: Stage %s failed with exit code %d\n' "$stage_name" "$stage_status" >&2
    if [[ $FINAL_EXIT_CODE -eq 0 ]]; then
      FINAL_EXIT_CODE=$stage_status
    fi
  fi
done

if [[ $FINAL_EXIT_CODE -eq 0 && $EXECUTION_EXIT_CODE -ne 0 ]]; then
  warn "Overall pipeline exit code is $EXECUTION_EXIT_CODE despite all stages reporting success."
  FINAL_EXIT_CODE=$EXECUTION_EXIT_CODE
fi

if [[ $FINAL_EXIT_CODE -ne 0 ]]; then
  printf 'Backup FAILED (exit code %d). Archive may be incomplete: %s\n' "$FINAL_EXIT_CODE" "$DEST_FILE_PATH" >&2
  exit "$FINAL_EXIT_CODE"
fi

info "Pipeline completed successfully."

# --- Post-execution: report size and optional verification ---
if ! COMPRESSED_SIZE_BYTES=$(stat -c%s -- "$DEST_FILE_PATH" 2>/dev/null); then
  warn "Could not stat archive '$DEST_FILE_PATH'."
else
  COMPRESSED_SIZE_HUMAN=$(numfmt --to=iec "$COMPRESSED_SIZE_BYTES")
  info "Archive saved to: $DEST_FILE_PATH"
  info "Compressed size:  ${COMPRESSED_SIZE_HUMAN} (${COMPRESSED_SIZE_BYTES} bytes)"
fi

print_separator
info "Verification commands:"
info "  zstd -t \"$DEST_FILE_PATH\""
info "  tar --list -I zstd -f \"$DEST_FILE_PATH\" | less"

if confirm_yes "Run 'zstd -t' now to test archive integrity? (y/N): "; then
  print_separator
  info "Running: zstd -t \"$DEST_FILE_PATH\""
  if zstd -t "$DEST_FILE_PATH"; then
    info "Integrity test PASSED."
  else
    warn "Integrity test FAILED."
  fi
fi

exit 0
{% endcodeblock %}
