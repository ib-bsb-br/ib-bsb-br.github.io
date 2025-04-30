---
tags: [scratchpad]
info: aberto.
date: 2025-04-30
type: post
layout: post
published: true
slug: sbnbscriptsinstall-linuxsh
title: 'sbnb/scripts/install-linux.sh'
---
{% codeblock bash %}
#!/bin/bash

# ==============================================================================
# Sbnb Linux Bootable USB/Disk Creation Script (Local Mode)
# ==============================================================================
#
# Description:
#   This script automates the creation of a bootable Sbnb Linux drive on Linux.
#   It uses an existing 'sbnb.raw' disk image file located in the same
#   directory as this script.
#
# Features:
#   - Uses local 'sbnb.raw' file (required).
#   - Uses local 'sbnb-tskey.txt' file if present (optional Tailscale key).
#   - Prompts for a custom script ('sbnb-cmds.sh') to run at boot (optional).
#   - Lists all detected disk-like devices for selection.
#   - Performs necessary unmounting before writing.
#   - Writes the image using 'dd' with progress display.
#   - Mounts the ESP partition to copy optional files.
#   - Includes robust cleanup via 'trap'.
#
# Requirements:
#   - Bash shell
#   - Core utilities: lsblk, grep, sed, awk, mktemp, mount, umount, cp, tee, sync
#   - 'sudo' privileges for disk operations (dd, mount, umount, partprobe).
#   - GNU 'dd' (for status=progress).
#   - 'partprobe' utility (recommended, for partition table re-scan).
#   - 'sbnb.raw' file in the same directory as the script.
#
# More info: https://github.com/sbnb-io/sbnb
#
# WARNING: THIS SCRIPT WILL COMPLETELY OVERWRITE THE SELECTED DISK.
#          ALL DATA ON THE SELECTED DISK WILL BE PERMANENTLY LOST.
#          DOUBLE-CHECK YOUR SELECTION BEFORE CONFIRMING.
#
# ==============================================================================

# Exit immediately if a command exits with a non-zero status
set -e

# --- Configuration ---
SBNB_RAW_FILE="sbnb.raw"
SBNB_TSKEY_FILE="sbnb-tskey.txt"
SBNB_CMDS_FILE="sbnb-cmds.sh" # Target name on ESP for custom script

# --- Color Codes ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# --- Helper Functions ---
info() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }
prompt() { read -p "$(echo -e "${BLUE}[PROMPT]${NC} $1")" "$2"; }

# --- Initial Checks ---
info "Starting Sbnb Linux Bootable Drive Creation Script."

# Check for root privileges (needed for sudo operations)
if [[ $EUID -eq 0 ]]; then
   error "This script should not be run as root. It uses 'sudo' where needed."
   exit 1
fi
if ! command -v sudo &> /dev/null; then
    error "'sudo' command not found. Please install it."
    exit 1
fi
# Test sudo privileges early
if ! sudo -v; then
    error "Failed to obtain sudo privileges. Please check your sudo configuration."
    exit 1
fi

# Check for required local sbnb.raw file
SbnbRawPath="./${SBNB_RAW_FILE}"
if [ ! -r "$SbnbRawPath" ]; then
  error "'$SBNB_RAW_FILE' not found or not readable in the current directory (${PWD})."
  exit 1
fi
info "Found required file: $SbnbRawPath"

# Check for optional local sbnb-tskey.txt file
localTsKeyPath="./${SBNB_TSKEY_FILE}"
if [ -r "$localTsKeyPath" ]; then
  info "Found optional Tailscale key file: $localTsKeyPath"
  useLocalTsKey=true
else
  warn "Optional Tailscale key file ('$SBNB_TSKEY_FILE') not found or not readable. Skipping."
  useLocalTsKey=false
fi

# --- Disk Selection ---
info "Enumerating available block devices (disks, USB drives, etc.)..."
# Use lsblk: -d (devices only), -p (full paths), -o (columns), -n (no header)
# Filter for type 'disk' or 'rom'. Exclude loop devices explicitly.
mapfile -t devices < <(lsblk -dpno NAME,SIZE,MODEL,TYPE | grep -E 'disk|rom' | grep -v 'loop')

if [ ${#devices[@]} -eq 0 ]; then
    error "No suitable disk devices found."
    exit 1
fi

echo -e "${YELLOW}Available Devices:${NC}"
echo "--------------------------------------------------"
for i in "${!devices[@]}"; do
  printf "%3d) %s\n" $((i+1)) "${devices[$i]}"
done
echo "--------------------------------------------------"

selectedDiskIndex=""
while true; do
    prompt "Enter the index number of the target device: " selectedDiskIndex
    if [[ "$selectedDiskIndex" =~ ^[0-9]+$ ]] && [ "$selectedDiskIndex" -ge 1 ] && [ "$selectedDiskIndex" -le ${#devices[@]} ]; then
        selectedDrive=$(echo "${devices[$((selectedDiskIndex-1))]}" | awk '{print $1}')
        info "You selected index $selectedDiskIndex: $selectedDrive"
        break
    else
        warn "Invalid input. Please enter a number between 1 and ${#devices[@]}."
    fi
done

# --- Confirmation ---
echo -e "${RED}====================== WARNING ======================${NC}"
echo -e "${RED}You have selected device: $selectedDrive${NC}"
echo -e "${RED}ALL DATA ON THIS DEVICE WILL BE PERMANENTLY DESTROYED!${NC}"
echo -e "${RED}=====================================================${NC}"
prompt "Are you absolutely sure you want to proceed? (yes/no): " confirmation
if [[ "$confirmation" != "yes" ]]; then
  error "Operation cancelled by user."
  exit 1
fi

# --- Unmount Partitions ---
info "Checking for and unmounting partitions on $selectedDrive..."
# Use lsblk -lnpo NAME to get full paths of partitions, suppress errors if none exist
mounted_count=0
for partition_path in $(lsblk -lnpo NAME "$selectedDrive" 2>/dev/null || true); do
    # Check if the partition is currently mounted
    if mount | grep -q "^$partition_path "; then # Check for exact match followed by space
        info "Unmounting partition $partition_path..."
        sudo umount "$partition_path"
        mounted_count=$((mounted_count + 1))
    fi
done
if [ $mounted_count -gt 0 ]; then
    info "Finished unmounting partitions."
else
    info "No mounted partitions found on $selectedDrive."
fi

# --- Write Image ---
info "Writing '$SBNB_RAW_FILE' to $selectedDrive..."
warn "This may take a while. Please wait..."
# Use bs=4M (often faster), status=progress (GNU dd), conv=fsync (sync data+metadata at end)
if ! sudo dd if="$SbnbRawPath" of="$selectedDrive" bs=4M status=progress conv=fsync; then
    error "Failed to write image to $selectedDrive using dd."
    exit 1
fi
info "Image write completed successfully."

# --- Partition Recognition ---
info "Ensuring partition table is recognized..."
sync # Ensure all buffers are flushed
# Attempt to re-read partition table. partprobe is common.
if command -v partprobe &> /dev/null; then
    info "Running 'partprobe' to update partition table..."
    sudo partprobe "$selectedDrive" || warn "'partprobe' failed, but continuing..."
else
    warn "'partprobe' command not found. The system might take longer to recognize partitions."
fi
sleep 3 # Give the system a moment

# --- Mount ESP Partition ---
info "Attempting to identify and mount the first partition (ESP)..."
# Determine expected partition name (handles common schemes like sda1, nvme0n1p1, mmcblk0p1)
firstPartition=""
# Check for pattern like /dev/sda1, /dev/hda1
if [ -b "${selectedDrive}1" ]; then
    firstPartition="${selectedDrive}1"
# Check for pattern like /dev/nvme0n1p1, /dev/mmcblk0p1
elif [ -b "${selectedDrive}p1" ]; then
    firstPartition="${selectedDrive}p1"
else
    # Poll briefly in case detection was slow
    warn "First partition not immediately found, polling for 5 seconds..."
    found=false
    for _ in {1..5}; do
        sleep 1
        if [ -b "${selectedDrive}1" ]; then firstPartition="${selectedDrive}1"; found=true; break; fi
        if [ -b "${selectedDrive}p1" ]; then firstPartition="${selectedDrive}p1"; found=true; break; fi
    done
    if ! $found; then
        error "Could not find the first partition device node (${selectedDrive}1 or ${selectedDrive}p1)."
        error "Cannot proceed with copying files to ESP."
        exit 1
    fi
fi
info "Identified first partition as: $firstPartition"

# Create temporary mount point
tempMountDir=$(mktemp -d -t sbnb-esp-XXXXXX)

# Setup trap for cleanup BEFORE attempting mount
trap 'cleanup' EXIT HUP INT TERM
cleanup() {
    info "Cleaning up..."
    # Check if mount point exists and is mounted before trying to unmount
    if [ -d "$tempMountDir" ] && mountpoint -q "$tempMountDir"; then
        sudo umount "$tempMountDir" 2>/dev/null || warn "Failed to unmount $tempMountDir during cleanup."
    fi
    if [ -d "$tempMountDir" ]; then
        rmdir "$tempMountDir" 2>/dev/null || warn "Failed to remove temporary directory $tempMountDir during cleanup."
    fi
}

# Mount the partition
info "Mounting $firstPartition to $tempMountDir..."
if ! sudo mount "$firstPartition" "$tempMountDir"; then
    error "Failed to mount ESP partition $firstPartition at $tempMountDir."
    # Trap will handle cleanup
    exit 1
fi
info "ESP partition successfully mounted at $tempMountDir"
espPath="$tempMountDir"

# --- Copy Files to ESP ---

# Copy Tailscale key if local file exists
if [ "$useLocalTsKey" = true ]; then
  targetTsKeyPath="$espPath/$SBNB_TSKEY_FILE"
  info "Copying local '$SBNB_TSKEY_FILE' to $targetTsKeyPath..."
  if ! sudo cp "$localTsKeyPath" "$targetTsKeyPath"; then
      error "Failed to copy Tailscale key to ESP."
      # Trap will handle cleanup
      exit 1
  fi
  # Note: FAT32 doesn't store standard Linux permissions well. Ownership/perms might not be critical here.
  info "Tailscale key copied successfully."
fi

# Ask for and copy custom script if provided
customScriptPath=""
prompt "Enter path to custom script file (optional, saved as '$SBNB_CMDS_FILE' on drive, runs at boot) [Press Enter to skip]: " customScriptPath

if [ -n "$customScriptPath" ]; then
  if [ -f "$customScriptPath" ] && [ -r "$customScriptPath" ]; then
    targetScriptPath="$espPath/$SBNB_CMDS_FILE"
    info "Copying custom script '$customScriptPath' to $targetScriptPath..."
    if ! sudo cp "$customScriptPath" "$targetScriptPath"; then
        error "Failed to copy custom script to ESP."
        # Trap will handle cleanup
        exit 1
    fi
    # Optional: Make executable if needed, though FAT32 might ignore it. Boot process might source it instead.
    # sudo chmod +x "$targetScriptPath"
    info "Custom script copied successfully."
  else
    warn "Custom script file '$customScriptPath' not found or not readable. Skipping."
  fi
else
  info "No custom script path provided. Skipping."
fi

# --- Final Steps ---
info "File copying complete."
# Unmounting and cleanup is handled by the trap on exit

echo -e "${BLUE}=========================================${NC}"
echo -e "${GREEN} Operation completed successfully! ${NC}"
echo -e "${GREEN} You can now safely remove the device: $selectedDrive ${NC}"
echo -e "${GREEN} Remember to adjust BIOS/UEFI settings to boot from it. ${NC}"
echo -e "${BLUE}=========================================${NC}"

# Explicitly disable trap before normal exit to avoid double cleanup message
trap - EXIT HUP INT TERM
cleanup # Perform cleanup explicitly on successful exit

exit 0
{% endcodeblock %}