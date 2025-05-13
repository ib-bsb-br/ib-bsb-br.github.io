---
tags: [scratchpad]
info: aberto.
date: 2025-05-13
type: post
layout: post
published: true
slug: sbnb-drive-preparation
title: 'SBNB Drive Preparation'
---
This guide presents a unified, comprehensive utility script to prepare SBNB (Secure Bare-Metal Node Bootstrap) Linux bootable drives. It combines robust partitioning, flexible image deployment, and advanced persistent storage configuration into a user-friendly Bash script that orchestrates operations, including a helper Python script for complex configurations. Whether you need a quick standard bootable drive or a complex setup with persistent Docker storage and automated system management, this utility adapts to your needs.

This approach synergizes two powerful methodologies:
1.  A straightforward method for creating standard bootable drives from a local `.raw` image.
2.  A sophisticated process for advanced USB preparation, including partitioning for persistent data and deploying a full suite of configuration files for Docker management, backups, and system health monitoring via a dedicated Python script.

The unified Bash script below (`unified_sbnb_prep.sh`) serves as the main entry point, calling a companion Python script (`deploy_sbn_config.py`) for advanced mode configurations.

## Prerequisites

Before using the script, ensure you have the following on your Linux preparation system:
*   **Bash shell.**
*   **Core Linux utilities:** `lsblk`, `grep`, `sed`, `awk`, `mktemp`, `mount`, `umount`, `cp`, `tee`, `sync`, `dd`, `parted`, `mkfs.vfat`, `mkfs.ext4`, `wipefs`, `findmnt`, `blkid`, `fsck.vfat`, `e2fsck`, `id`, `read`, `sleep`, `xargs`, `partprobe`, `realpath`, `dirname`, `basename`, `cat`, `cmp`, `date`. (The script checks for most of these).
*   **`sudo` privileges:** The script is run as a normal user and will prompt for `sudo` password for privileged operations.
*   **Python 3:** Required for the Advanced Mode. The script will check for `python3`.
*   **`sbnb.raw` file:** (For Simple Mode) A complete raw disk image of SBNB Linux. Example: `/path/to/your/sbnb-v1.0.raw`.
*   **`sbnb.efi` file:** (For Advanced Mode) The SBNB EFI bootloader file (often `BOOTX64.EFI` from a standard SBNB installation or build). Example: `/path/to/your/BOOTX64.EFI`.
*   **(Optional) `sbnb-tskey.txt`:** (For Simple Mode) A local file containing your Tailscale authentication key.
*   **(Optional) Custom `sbnb-cmds.sh`:** (For Simple Mode) A user-provided script to run at boot, which will be copied to the ESP.
*   **(Optional) Tailscale Authentication Key string:** (For Advanced Mode) Your actual Tailscale auth key string (e.g., `tskey-auth-xxxxxxxxxxxx`).

**EXTREME CAUTION:** Disk operations performed by this script are destructive to the target device. ALL DATA on the selected device WILL BE PERMANENTLY LOST. Double-check your target device selection. Proceed at your own risk.

## The Utility Scripts

You will need two files in the same directory:
1.  `unified_sbnb_prep.sh` (The main Bash script provided below)
2.  `deploy_sbn_config.py` (The Python helper script for Advanced Mode, also provided below)

### 1. `unified_sbnb_prep.sh` (Main Bash Script)

Save the following script as `unified_sbnb_prep.sh`:

```bash
#!/bin/bash

# ==============================================================================
# Unified SBNB Drive Preparation Utility
# Version 1.1
#
# Orchestrates simple SBNB raw image deployment and advanced SBNB drive
# preparation with persistent storage, calling a Python script for complex configs.
#
# This script should be run as a normal user. It will use 'sudo' for
# privileged operations.
# ==============================================================================

set -euo pipefail

# --- Configuration & Constants ---
SBNB_RAW_IMG_DEFAULT="sbnb.raw"
SBNB_EFI_DEFAULT="BOOTX64.EFI" # Or sbnb.efi
SBNB_TSKEY_FILE_DEFAULT="sbnb-tskey.txt" # For simple mode file copy
SBNB_CMDS_FILE_SIMPLE_DEFAULT="sbnb-cmds.sh" # For simple mode file copy

# ESP Label for Advanced Mode (must match Python script's expectations if changed)
ESP_LABEL_ADV="sbnb"
DATA_LABEL_ADV="SBNB_DATA"
ESP_SIZE_ADV="1025MiB" # ESP Size for Advanced Mode

# Temporary mount base (unique per script run)
TEMP_MOUNT_BASE="/mnt/sbnb_usb_creator_mnt_$$"
TEMP_ESP_MOUNT="${TEMP_MOUNT_BASE}/esp"
TEMP_DATA_MOUNT="${TEMP_MOUNT_BASE}/data" # Used in Advanced Mode

# Companion Python script name
PYTHON_DEPLOY_SCRIPT_NAME="deploy_sbn_config.py"

# --- Color Codes ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# --- Helper Functions ---
_log_msg() {
    local color_prefix="$1"
    local type_prefix="$2"
    local message="$3"
    echo -e "${color_prefix}[${type_prefix}]${NC} ${message}"
}
info() { _log_msg "${GREEN}" "INFO" "$1"; }
warn() { _log_msg "${YELLOW}" "WARN" "$1"; }
error_exit() { _log_msg "${RED}" "ERROR" "$1"; exit 1; }
prompt() { read -p "$(echo -e "${BLUE}[PROMPT]${NC} $1")" "$2"; }
prompt_sensitive() {
    echo -e "${BLUE}[PROMPT]${NC} $1"
    read -s "$2"
    echo # Newline after sensitive input
}
confirm_action() {
    local message="$1"
    local confirmation_var_name="$2"
    echo -e "\n${RED}====================== WARNING ======================${NC}"
    echo -e "${RED}${message}${NC}"
    echo -e "${RED}ALL DATA ON THE TARGET DEVICE WILL BE PERMANENTLY DESTROYED!${NC}"
    echo -e "${RED}This operation is IRREVERSIBLE.${NC}"
    echo -e "${RED}=====================================================${NC}"
    prompt "Are you absolutely sure you want to proceed? (Type 'yes' to confirm): " "$confirmation_var_name"
    eval "$confirmation_var_name=\${${confirmation_var_name}:-NO}"
}

check_command() {
    if ! command -v "$1" &> /dev/null; then
        error_exit "Required command '$1' not found. Please install it."
    fi
}

# Trap for cleanup of temporary mount points and base directory
cleanup_trap() {
    info "Initiating cleanup..."
    # Unmount ESP if mounted (used by both modes if successful)
    if mountpoint -q "${TEMP_ESP_MOUNT}" &>/dev/null; then
        info "Unmounting ESP from ${TEMP_ESP_MOUNT}..."
        sudo umount "${TEMP_ESP_MOUNT}" || warn "Failed to unmount ${TEMP_ESP_MOUNT} during cleanup."
    fi
    # Unmount Data if mounted (Advanced Mode)
    if mountpoint -q "${TEMP_DATA_MOUNT}" &>/dev/null; then
        info "Unmounting Data partition from ${TEMP_DATA_MOUNT}..."
        sudo umount "${TEMP_DATA_MOUNT}" || warn "Failed to unmount ${TEMP_DATA_MOUNT} during cleanup."
    fi

    # Remove temporary mount point base directory and its contents
    if [ -d "${TEMP_MOUNT_BASE}" ]; then
        info "Removing temporary mount base ${TEMP_MOUNT_BASE}..."
        sudo rm -rf "${TEMP_MOUNT_BASE}" || warn "Failed to remove ${TEMP_MOUNT_BASE} during cleanup."
    fi
    info "Cleanup finished."
}
trap cleanup_trap EXIT HUP INT TERM


# --- Initial Checks ---
info "Starting Unified SBNB Drive Preparation Utility (Version 1.1)."

if [[ $EUID -eq 0 ]]; then
   error_exit "This script should not be run as root. It uses 'sudo' internally where needed."
fi
check_command "sudo"
info "Testing sudo privileges..."
if ! sudo -v; then # Test sudo privileges early, prompts for password if needed
    error_exit "Failed to obtain sudo privileges. Please check your sudo configuration or password."
fi
info "Sudo privileges obtained."

REQUIRED_CMDS_COMMON=(
    "lsblk" "grep" "sed" "awk" "mktemp" "mount" "umount" "cp" "tee" "sync" "dd"
    "parted" "wipefs" "mkfs.vfat" "mkfs.ext4" "blkid" "fsck.vfat" "e2fsck"
    "partprobe" "python3" "findmnt" "realpath" "dirname" "basename" "cat" "cmp" "date" "xargs"
)
for cmd in "${REQUIRED_CMDS_COMMON[@]}"; do
    check_command "$cmd"
done
info "All common required commands found."

# Check for companion Python script
SCRIPT_DIR=$(dirname "$(realpath "$0")")
PYTHON_DEPLOY_SCRIPT_PATH="${SCRIPT_DIR}/${PYTHON_DEPLOY_SCRIPT_NAME}"
if [ ! -f "${PYTHON_DEPLOY_SCRIPT_PATH}" ]; then
    warn "Companion Python script '${PYTHON_DEPLOY_SCRIPT_NAME}' not found in the same directory as this script."
    warn "Advanced Mode will not be available."
    # We can let the mode selection handle this, or exit if it's critical.
    # For now, just warn and let mode selection proceed.
fi


# --- Mode Selection ---
echo -e "\n${BLUE}Select Operation Mode:${NC}"
echo "  1) Simple Mode: Write a .raw image directly to disk (basic bootable)."
echo "  2) Advanced Mode: Partition disk for ESP + Data, deploy SBNB EFI and full persistent Docker setup."
mode_choice=""
while true; do
    prompt "Enter your choice (1 or 2): " mode_choice
    if [[ "$mode_choice" == "1" ]]; then
        break
    elif [[ "$mode_choice" == "2" ]]; then
        if [ ! -f "${PYTHON_DEPLOY_SCRIPT_PATH}" ]; then
            warn "Cannot select Advanced Mode: Python script '${PYTHON_DEPLOY_SCRIPT_NAME}' is missing."
        else
            break
        fi
    else
        warn "Invalid choice. Please enter 1 or 2."
    fi
done

# --- Disk Selection (Common for both modes) ---
info "Enumerating available block devices..."
mapfile -t devices < <(sudo lsblk -dpno NAME,SIZE,MODEL,TYPE | grep -E 'disk|rom' | grep -v 'loop')

if [ ${#devices[@]} -eq 0 ]; then
    error_exit "No suitable disk devices found."
fi

echo -e "\n${YELLOW}Available Devices:${NC}"
echo "--------------------------------------------------"
for i in "${!devices[@]}"; do
  printf "%3d) %s\n" $((i+1)) "${devices[$i]}"
done
echo "--------------------------------------------------"

selected_disk_path=""
selected_disk_index=""
while true; do
    prompt "Enter the index number of the TARGET disk: " selected_disk_index
    if [[ "$selected_disk_index" =~ ^[0-9]+$ ]] && [ "$selected_disk_index" -ge 1 ] && [ "$selected_disk_index" -le ${#devices[@]} ]; then
        selected_disk_path=$(echo "${devices[$((selected_disk_index-1))]}" | awk '{print $1}')
        info "You selected index $selected_disk_index: $selected_disk_path"
        break
    else
        warn "Invalid input. Please enter a number between 1 and ${#devices[@]}."
    fi
done

# --- Confirmation (Common for both modes) ---
confirmation_main="" # Variable to hold confirmation
confirm_action "You have selected device: $selected_disk_path." "confirmation_main"
if [[ "$confirmation_main" != "yes" ]]; then
  info "Operation cancelled by user." # Not an error, user choice
  exit 0
fi

# --- Unmount existing partitions on selected disk (Common Pre-step) ---
info "Checking for and unmounting any existing partitions on $selected_disk_path..."
# Use findmnt to get mount points and umount them safely
# Also try to unmount the base device itself in case it's loop-mounted etc.
sudo findmnt -n -o TARGET --source "${selected_disk_path}*" | xargs --no-run-if-empty sudo umount -v -l || info "No partitions were mounted or umount failed (might be okay)."
sudo umount "$selected_disk_path" &>/dev/null || true # Attempt to unmount base device, ignore errors
sleep 1 # Give time for umount to settle
info "Finished unmounting checks for $selected_disk_path."


# ==============================================================================
# --- MODE 1: SIMPLE RAW IMAGE WRITER ---
# ==============================================================================
if [[ "$mode_choice" == "1" ]]; then
    info "Entering Simple Mode: Raw Image Writer."

    # Get SBNB Raw Image Path
    sbnb_raw_file_path=""
    prompt "Enter path to the SBNB .raw image file (default: ./${SBNB_RAW_IMG_DEFAULT}): " sbnb_raw_file_path
    sbnb_raw_file_path="${sbnb_raw_file_path:-./${SBNB_RAW_IMG_DEFAULT}}"

    if [ ! -r "$sbnb_raw_file_path" ]; then
        error_exit "SBNB .raw image file not found or not readable: $sbnb_raw_file_path"
    fi
    info "Using .raw image: $sbnb_raw_file_path"

    # Write Image
    info "Writing '$sbnb_raw_file_path' to $selected_disk_path..."
    warn "This may take a while. Please wait..."
    if ! sudo dd if="$sbnb_raw_file_path" of="$selected_disk_path" bs=4M status=progress conv=fsync; then
        error_exit "Failed to write image to $selected_disk_path using dd."
    fi
    info "Image write completed successfully."

    # Partition Recognition
    info "Ensuring partition table is recognized..."
    sudo sync
    if command -v partprobe &> /dev/null; then
        info "Running 'sudo partprobe $selected_disk_path'..."
        sudo partprobe "$selected_disk_path" || warn "'partprobe' failed, but continuing..."
    else
        warn "'partprobe' command not found. System might take longer to recognize partitions."
    fi
    sleep 3

    # Mount ESP to copy optional files
    info "Attempting to identify and mount the first partition (ESP) from the written image..."
    first_partition_path_simple=""
    # Check common naming schemes (sda1, nvme0n1p1, mmcblk0p1)
    if [ -b "${selected_disk_path}1" ]; then first_partition_path_simple="${selected_disk_path}1";
    elif [ -b "${selected_disk_path}p1" ]; then first_partition_path_simple="${selected_disk_path}p1";
    else
        warn "First partition not immediately found, polling for 5 seconds..."
        found_part_simple=false
        for _ in {1..5}; do
            sleep 1
            if [ -b "${selected_disk_path}1" ]; then first_partition_path_simple="${selected_disk_path}1"; found_part_simple=true; break; fi
            if [ -b "${selected_disk_path}p1" ]; then first_partition_path_simple="${selected_disk_path}p1"; found_part_simple=true; break; fi
        done
        if ! $found_part_simple; then
            error_exit "Could not find the first partition device node on $selected_disk_path. Cannot proceed with copying optional files. The drive might still be bootable if the image was self-contained."
        fi
    fi
    info "Identified first partition as: $first_partition_path_simple"

    sudo mkdir -p "${TEMP_ESP_MOUNT}" # Use global temp mount
    info "Mounting $first_partition_path_simple to ${TEMP_ESP_MOUNT}..."
    if ! sudo mount "$first_partition_path_simple" "${TEMP_ESP_MOUNT}"; then
        error_exit "Failed to mount ESP partition $first_partition_path_simple at ${TEMP_ESP_MOUNT}."
    fi
    info "ESP partition successfully mounted at ${TEMP_ESP_MOUNT}"

    # Copy optional Tailscale key
    local_tskey_path_simple_src=""
    prompt "Enter path to local '${SBNB_TSKEY_FILE_DEFAULT}' file (optional, for Tailscale key, press Enter to skip): " local_tskey_path_simple_src
    if [ -n "$local_tskey_path_simple_src" ]; then
        if [ -r "$local_tskey_path_simple_src" ]; then
            target_tskey_path_simple_dest="${TEMP_ESP_MOUNT}/${SBNB_TSKEY_FILE_DEFAULT}"
            info "Found local '$local_tskey_path_simple_src'. Copying to $target_tskey_path_simple_dest..."
            if ! sudo cp "$local_tskey_path_simple_src" "$target_tskey_path_simple_dest"; then
                warn "Failed to copy Tailscale key to ESP. Continuing." # Non-fatal
            else
                info "Tailscale key copied successfully."
            fi
        else
            warn "Optional Tailscale key file '$local_tskey_path_simple_src' not found or not readable. Skipping."
        fi
    else
        info "No local Tailscale key file path provided. Skipping."
    fi

    # Ask for and copy custom simple sbnb-cmds.sh
    custom_script_path_simple_src=""
    prompt "Enter path to custom simple '${SBNB_CMDS_FILE_SIMPLE_DEFAULT}' file (optional, copied to ESP, runs at boot) [Press Enter to skip]: " custom_script_path_simple_src
    if [ -n "$custom_script_path_simple_src" ]; then
        if [ -f "$custom_script_path_simple_src" ] && [ -r "$custom_script_path_simple_src" ]; then
            target_script_path_simple_dest="${TEMP_ESP_MOUNT}/${SBNB_CMDS_FILE_SIMPLE_DEFAULT}"
            info "Copying custom script '$custom_script_path_simple_src' to $target_script_path_simple_dest..."
            if ! sudo cp "$custom_script_path_simple_src" "$target_script_path_simple_dest"; then
                warn "Failed to copy custom script to ESP. Continuing." # Non-fatal
            else
                info "Custom script copied successfully."
            fi
        else
            warn "Custom script file '$custom_script_path_simple_src' not found or not readable. Skipping."
        fi
    else
        info "No custom simple script path provided. Skipping."
    fi

    info "Simple Mode: File copying complete. ESP will be unmounted by cleanup."

# ==============================================================================
# --- MODE 2: ADVANCED PERSISTENT STORAGE SETUP ---
# ==============================================================================
elif [[ "$mode_choice" == "2" ]]; then
    info "Entering Advanced Mode: Persistent Storage Setup."

    # Get SBNB EFI File Path
    sbnb_efi_file_path_adv=""
    prompt "Enter path to the SBNB EFI boot file (e.g., BOOTX64.EFI or sbnb.efi): " sbnb_efi_file_path_adv
    if [ -z "$sbnb_efi_file_path_adv" ]; then
        error_exit "SBNB EFI boot file path cannot be empty for Advanced Mode."
    fi
    if [ ! -r "$sbnb_efi_file_path_adv" ]; then
        error_exit "SBNB EFI boot file not found or not readable: $sbnb_efi_file_path_adv"
    fi
    info "Using SBNB EFI file: $sbnb_efi_file_path_adv"

    # --- Partitioning and Formatting Function ---
    prepare_usb_advanced() {
        local TARGET_DEVICE_FUNC="$1"
        local esp_part_out="" # Variables to store output paths
        local data_part_out=""

        info "--- USB Drive Partitioning and Formatting for Advanced Mode (Target: ${TARGET_DEVICE_FUNC}) ---"
        
        local REQUIRED_CMDS_PREPARE_FUNC=(
          "parted" "mkfs.vfat" "mkfs.ext4" "wipefs" "findmnt" "lsblk"
          "blkid" "fsck.vfat" "e2fsck" "sync" "id" "grep" "read"
          "sleep" "xargs" "umount" "partprobe" "realpath"
        ) # id, read, sleep, xargs not strictly used here but kept from original list for now

        info "Checking dependencies for USB preparation..."
        for cmd_prep_func in "${REQUIRED_CMDS_PREPARE_FUNC[@]}"; do
            check_command "$cmd_prep_func" # Uses global check_command
        done
        info "All USB preparation dependencies found."

        if [ ! -b "$TARGET_DEVICE_FUNC" ]; then
          error_exit "'$TARGET_DEVICE_FUNC' is not a valid block device."
        fi

        info "Performing safety checks for $TARGET_DEVICE_FUNC..."
        local root_dev_path_func
        root_dev_path_func=$(sudo findmnt -n -o SOURCE /) # findmnt might need sudo if run by normal user
        local root_base_dev_name_func
        root_base_dev_name_func=$(sudo lsblk -no pkname "$(sudo realpath "$root_dev_path_func")") || error_exit "Cannot find base device for root FS."
        
        local target_base_dev_name_func
        target_base_dev_name_func=$(sudo lsblk -no pkname "$(sudo realpath "$TARGET_DEVICE_FUNC")") || error_exit "Cannot find base device for target $TARGET_DEVICE_FUNC."

        if [ "/dev/${target_base_dev_name_func}" == "/dev/${root_base_dev_name_func}" ]; then
          error_exit "FATAL ERROR: Target device '$TARGET_DEVICE_FUNC' appears to be the same device as the running root filesystem. Aborting."
        fi
        info "Safety check passed: Target device '$TARGET_DEVICE_FUNC' is not the root filesystem device."

        if [[ "$TARGET_DEVICE_FUNC" == /dev/mmcblk* ]]; then
          warn "'$TARGET_DEVICE_FUNC' looks like an SD card. Double-check this is not your primary OS drive!"
        fi
        
        info "Wiping filesystem/partition signatures from $TARGET_DEVICE_FUNC..."
        sudo wipefs --all --force "$TARGET_DEVICE_FUNC"
        sudo sync

        info "Creating new GPT partition table on $TARGET_DEVICE_FUNC..."
        sudo parted "$TARGET_DEVICE_FUNC" --script -- mklabel gpt
        sudo sync

        info "Creating ESP partition (1) on $TARGET_DEVICE_FUNC..."
        sudo parted "$TARGET_DEVICE_FUNC" --script -- mkpart "${ESP_LABEL_ADV}" fat32 1MiB "${ESP_SIZE_ADV}"
        sudo parted "$TARGET_DEVICE_FUNC" --script -- set 1 boot on
        sudo parted "$TARGET_DEVICE_FUNC" --script -- set 1 esp on
        sudo sync

        info "Creating Linux data partition (2) on $TARGET_DEVICE_FUNC..."
        sudo parted "$TARGET_DEVICE_FUNC" --script -- mkpart "${DATA_LABEL_ADV}" ext4 "${ESP_SIZE_ADV}" 100%
        sudo sync
        info "Waiting briefly for kernel to recognize new partitions..."
        sleep 2

        local part_prefix_func=""
        if [[ "$TARGET_DEVICE_FUNC" == *nvme* ]] || [[ "$TARGET_DEVICE_FUNC" == *mmcblk* ]]; then
          part_prefix_func="p"
        fi
        esp_part_out="${TARGET_DEVICE_FUNC}${part_prefix_func}1"
        data_part_out="${TARGET_DEVICE_FUNC}${part_prefix_func}2"

        info "Checking for partition device nodes (${esp_part_out}, ${data_part_out})..."
        local partitions_found_adv_func=false
        for i_func in {1..5}; do
          if [ -b "$esp_part_out" ] && [ -b "$data_part_out" ]; then
            info "Partition nodes found: $esp_part_out, $data_part_out"
            partitions_found_adv_func=true
            break
          fi
          info "Partition nodes not yet found. Retrying probe (Attempt $i_func/5)..."
          sudo partprobe "$TARGET_DEVICE_FUNC" || warn "Warning: partprobe command failed, continuing check..."
          sleep 1
        done

        if [ "$partitions_found_adv_func" = false ]; then
          sudo lsblk "$TARGET_DEVICE_FUNC"
          error_exit "Partition devices ($esp_part_out, $data_part_out) not found after partitioning and retries."
        fi

        info "Verifying partitions on $TARGET_DEVICE_FUNC..."
        sudo parted "$TARGET_DEVICE_FUNC" --script -- print
        sudo lsblk -o NAME,SIZE,TYPE,FSTYPE,PARTLABEL,MOUNTPOINT,PARTFLAGS "$TARGET_DEVICE_FUNC"
        sleep 1 # Brief pause for user to see

        info "Formatting ESP partition (${esp_part_out}) as FAT32 with label '${ESP_LABEL_ADV}'..."
        sudo mkfs.vfat -F 32 -n "${ESP_LABEL_ADV}" "${esp_part_out}"
        sudo sync
        info "Checking ESP filesystem (fsck.vfat)..."
        local fsck_vfat_exit_code_func=0
        sudo fsck.vfat -a "${esp_part_out}" || fsck_vfat_exit_code_func=$?
        if [ $fsck_vfat_exit_code_func -eq 0 ]; then info "ESP filesystem check passed."; 
        elif [ $fsck_vfat_exit_code_func -eq 1 ]; then warn "fsck.vfat found and corrected errors on ESP.";
        else error_exit "fsck.vfat reported uncorrectable errors (Code: $fsck_vfat_exit_code_func) on ESP."; fi
        if ! sudo blkid -s LABEL -o value "${esp_part_out}" | grep -q "^${ESP_LABEL_ADV}$"; then
            sudo blkid "${esp_part_out}"
            error_exit "Failed to verify ESP Label '${ESP_LABEL_ADV}' on ${esp_part_out}."
        fi
        info "ESP Label '${ESP_LABEL_ADV}' verified."

        info "Formatting Data partition (${data_part_out}) as ext4 with label '${DATA_LABEL_ADV}'..."
        sudo mkfs.ext4 -m 0 -L "${DATA_LABEL_ADV}" "${data_part_out}"
        sudo sync
        info "Checking Data partition filesystem (e2fsck)..."
        local e2fsck_exit_code_func=0
        sudo e2fsck -f -y "${data_part_out}" || e2fsck_exit_code_func=$?
        if [ $e2fsck_exit_code_func -eq 0 ]; then info "Data partition filesystem check passed.";
        elif [ $e2fsck_exit_code_func -eq 1 ]; then warn "e2fsck found and corrected errors on Data partition.";
        else error_exit "e2fsck reported uncorrectable errors (Code: $e2fsck_exit_code_func) on Data partition."; fi
        if ! sudo blkid -s LABEL -o value "${data_part_out}" | grep -q "^${DATA_LABEL_ADV}$"; then
            sudo blkid "${data_part_out}"
            error_exit "Failed to verify Data Label '${DATA_LABEL_ADV}' on ${data_part_out}."
        fi
        info "Data Label '${DATA_LABEL_ADV}' verified."

        info "USB drive partitioning and formatting complete for $TARGET_DEVICE_FUNC."
        # Output the determined partition paths for the caller
        echo "${esp_part_out}"
        echo "${data_part_out}"
        return 0 # Success
    }

    # --- Advanced Mode Execution Flow ---
    # Step 1: Partition and Format the Drive. Capture output paths.
    partition_output=$(prepare_usb_advanced "$selected_disk_path")
    # Extract paths from the last two lines of output
    esp_partition_path_adv=$(echo "$partition_output" | tail -n 2 | head -n 1)
    data_partition_path_adv=$(echo "$partition_output" | tail -n 1)

    if [ ! -b "$esp_partition_path_adv" ] || [ ! -b "$data_partition_path_adv" ]; then
        error_exit "Failed to determine valid ESP or Data partition paths after partitioning."
    fi
    info "Determined ESP partition: $esp_partition_path_adv"
    info "Determined Data partition: $data_partition_path_adv"

    # Step 2: Mount Partitions and Deploy Files
    info "Creating temporary mount points: ${TEMP_ESP_MOUNT}, ${TEMP_DATA_MOUNT}"
    sudo mkdir -p "${TEMP_ESP_MOUNT}"
    sudo mkdir -p "${TEMP_DATA_MOUNT}"

    info "Mounting ESP ${esp_partition_path_adv} to ${TEMP_ESP_MOUNT}..."
    if ! sudo mount "${esp_partition_path_adv}" "${TEMP_ESP_MOUNT}"; then
        error_exit "Failed to mount ESP partition."
    fi
    info "Mounting Data partition ${data_partition_path_adv} to ${TEMP_DATA_MOUNT}..."
    if ! sudo mount "${data_partition_path_adv}" "${TEMP_DATA_MOUNT}"; then
        error_exit "Failed to mount Data partition."
    fi

    info "Creating EFI boot directory structure on ESP..."
    sudo mkdir -p "${TEMP_ESP_MOUNT}/EFI/BOOT"

    info "Copying SBNB EFI file '$sbnb_efi_file_path_adv' to ${TEMP_ESP_MOUNT}/EFI/BOOT/BOOTX64.EFI..."
    if ! sudo cp "$sbnb_efi_file_path_adv" "${TEMP_ESP_MOUNT}/EFI/BOOT/BOOTX64.EFI"; then
        error_exit "Failed to copy SBNB EFI file to ESP."
    fi
    info "SBNB EFI file copied."

    # Get Tailscale Key for Advanced Mode (securely)
    ts_key_adv_content=""
    prompt_sensitive "Enter Tailscale authentication key (tskey-auth-...) for Advanced Mode (input hidden): " ts_key_adv_content
    if [[ -z "$ts_key_adv_content" ]]; then
        warn "No Tailscale key provided. A placeholder will be used in sbnb-tskey.txt."
        ts_key_adv_content="tskey-auth-placeholder-key-not-provided-by-user-REPLACE-MANUALLY"
    fi

    info "Preparing to run Python configuration deployment script..."
    info "Executing Python script '${PYTHON_DEPLOY_SCRIPT_PATH}' to deploy configurations..."
    # Call the external Python script with sudo, passing parameters as arguments
    if sudo python3 "${PYTHON_DEPLOY_SCRIPT_PATH}" \
            --esp-path "${TEMP_ESP_MOUNT}" \
            --data-path "${TEMP_DATA_MOUNT}" \
            --ts-key "${ts_key_adv_content}"; then
        info "Python configuration script executed successfully."
    else
        error_exit "Python configuration script failed. Check output above."
    fi

    info "Advanced Mode: File deployment complete. Syncing data to disk..."
    sudo sync
    info "Partitions will be unmounted by cleanup."

fi # End of mode selection

# --- Final Messages ---
echo -e "\n${BLUE}=====================================================${NC}"
echo -e "${GREEN} SBNB USB Creator Script Finished! ${NC}"
echo -e "${GREEN} Selected device: $selected_disk_path ${NC}"
if [[ "$mode_choice" == "1" ]]; then
    echo -e "${GREEN} Mode: Simple Raw Image Write ${NC}"
elif [[ "$mode_choice" == "2" ]]; then
    echo -e "${GREEN} Mode: Advanced Persistent Storage Setup ${NC}"
    if [[ "$ts_key_adv_content" == "tskey-auth-placeholder-key-not-provided-by-user-REPLACE-MANUALLY" ]]; then
        echo -e "${YELLOW} IMPORTANT: You used a placeholder Tailscale key. ${NC}"
        echo -e "${YELLOW}            You MUST manually edit the 'sbnb-tskey.txt' file on the ESP of ${NC}"
        echo -e "${YELLOW}            the USB drive with your actual key before its first use. ${NC}"
        echo -e "${YELLOW}            (The ESP was mounted at ${TEMP_ESP_MOUNT} during script execution).${NC}"
    fi
fi
echo -e "${GREEN} The script will now perform final cleanup (unmounting temporary mounts). ${NC}"
echo -e "${GREEN} After cleanup, you can safely remove the device: $selected_disk_path ${NC}"
echo -e "${GREEN} Remember to adjust BIOS/UEFI settings to boot from it (UEFI mode, Secure Boot OFF). ${NC}"
echo -e "${BLUE}=====================================================${NC}"

# Explicitly disable trap and call cleanup for controlled exit message flow
# Trap is already set to run on EXIT, so this explicit call is mostly for ensuring messages appear before script truly ends.
# The trap itself will handle the actual unmounting.
# trap - EXIT HUP INT TERM # Not strictly needed if we let the EXIT trap handle it.
# cleanup_trap # Calling it explicitly can be fine, trap will prevent double execution if already running.

info "Script completed. Final cleanup will now occur."
exit 0

```

### 2. `deploy_sbn_config.py` (Python Helper Script)

Save the following Python script in the same directory as `unified_sbnb_prep.sh`, naming it `deploy_sbn_config.py`:

```python
#!/usr/bin/env python3
# ==============================================================================
# SBNB Configuration Deployment Script (Python Helper)
# Version 1.1
#
# Called by the main Bash script to deploy advanced configurations to
# mounted ESP and Data partitions.
# ==============================================================================
import os
import stat
import sys
import pathlib
import json
import shutil
import argparse
from datetime import datetime

# --- Argument Parsing ---
parser = argparse.ArgumentParser(description="SBNB Advanced Configuration Deployment Script.")
parser.add_argument("--esp-path", required=True, help="Path to the mounted ESP partition.")
parser.add_argument("--data-path", required=True, help="Path to the mounted Data partition.")
parser.add_argument("--ts-key", required=True, help="Tailscale authentication key string.")
args = parser.parse_args()

# --- Configuration: Use parsed arguments ---
ESP_MOUNT = args.esp_path
DATA_MOUNT = args.data_path
SBNB_TSKEY_TXT_CONTENT = args.ts_key

# --- Static Configurations (can be customized further if needed) ---
# These paths are relative to the SBNB system's root after booting,
# accessed here via the mount points.
PERSISTENT_DOCKER_ROOT = f"{DATA_MOUNT}/docker-root"
DOCKER_CONFIG_DIR_ON_TARGET = "/etc/docker" # Path on the target SBNB system
DOCKER_CONFIG_FILE_ON_TARGET = f"{DOCKER_CONFIG_DIR_ON_TARGET}/daemon.json"
DOCKER_CONFIG_BACKUP_SUFFIX = ".sbnb-orig-backup"
DOCKER_DATA_EPHEMERAL_ON_TARGET = "/var/lib/docker" # Path on the target SBNB system
DOCKER_ROOT_PERMISSIONS = 0o711  # rwx--x--x
DOCKER_CONFIG_PERMISSIONS = 0o644 # rw-r--r--

BACKUP_BASE_DIR = f"{DATA_MOUNT}/backups/docker"
BACKUP_KEEP_COUNT = 3
STOP_DOCKER_FOR_BACKUP = 1 # 1 = Stop Docker during backup (safer), 0 = Attempt live backup
BACKUP_DIR_PERMISSIONS = 0o750 # rwxr-x---

VOLUME_CHECK_THRESHOLD_PERCENT = 10
VOLUME_CHECK_PRUNE_LEVEL = 1 # 0=None, 1=Containers/Dangling Images, 2=All Unused Images+Containers

# --- Logging Helper ---
def log_py(level, message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"PYTHON SCRIPT [{timestamp} {level}]: {message}", file=sys.stderr if level == "ERROR" else sys.stdout)

# --- Content Definitions ---
# Note: DATA_MOUNT in these shell scripts refers to how it will be mounted on the SBNB system,
# which corresponds to the DATA_MOUNT variable passed to this Python script.
# Similarly for PERSISTENT_DOCKER_ROOT.

# --- sbnb-cmds.sh Content (Main boot script for Advanced Mode) ---
SBNB_CMDS_SH_CONTENT = f"""#!/bin/sh
# Sbnb Custom Commands Script (Persistent Docker Root - Deployed by Python)
# Version 1.1
# Mounts persistent data, configures Docker data-root, migrates data,
# updates optional scripts, enables systemd units for backup & monitoring.

# Strict error handling
set -e -o pipefail -u

# --- Logging Function (to kernel message buffer on target system) ---
log() {{
    echo "[sbnb-cmds.sh] $1" > /dev/kmsg
}}

log "Starting custom boot commands (Persistent Docker Root v1.1)..."

# --- Check Core Commands (on target system) ---
check_cmds() {{
    local missing_cmd_flag=0
    log "Checking required commands on target system..."
    for cmd_to_check in "$@"; do
        if ! command -v "$cmd_to_check" >/dev/null 2>&1; then
            log "ERROR: Required command '$cmd_to_check' not found on target system."
            missing_cmd_flag=1
        fi
    done
    if [ $missing_cmd_flag -eq 1 ]; then
        log "ERROR: Missing one or more required commands. Cannot proceed."
        exit 1
    fi
    log "All required commands found on target system."
    # Check optional but recommended commands
    if ! command -v jq >/dev/null 2>&1; then
        log "WARNING: 'jq' command not found on target. JSON handling for daemon.json will be less robust."
    else
        log "OK: 'jq' command found on target (recommended)."
    fi
}}
# Define all commands potentially used in this script
check_cmds mountpoint readlink mkdir mount echo sleep rm find ln systemctl mktemp cp mv chmod chown dirname basename jq grep cat cmp date sed ls

# --- Mount Persistent Data Partition ---
# DATA_MOUNT here is the path where the data partition will be mounted on the SBNB system.
# This value is baked in from the Python script's DATA_MOUNT variable.
SBNB_DATA_PARTITION_LABEL="SBNB_DATA" # Must match label set during partitioning
SBNB_DATA_DEVICE_SYMLINK="/dev/disk/by-label/${{SBNB_DATA_PARTITION_LABEL}}"
SBNB_DATA_MOUNT_POINT="{DATA_MOUNT}" # This is the DATA_MOUNT from Python script
MAX_WAIT_SECONDS_FOR_DEVICE=15
WAIT_INTERVAL_SECONDS=1
elapsed_time_device=0

log "Waiting up to ${{MAX_WAIT_SECONDS_FOR_DEVICE}}s for data device (Label: ${{SBNB_DATA_PARTITION_LABEL}})..."
while [ ! -e "${{SBNB_DATA_DEVICE_SYMLINK}}" ]; do
    if [ ${{elapsed_time_device}} -ge ${{MAX_WAIT_SECONDS_FOR_DEVICE}} ]; then
        log "ERROR: Timeout waiting for device ${{SBNB_DATA_DEVICE_SYMLINK}}. Persistent data cannot be mounted."
        exit 1
    fi
    sleep ${{WAIT_INTERVAL_SECONDS}}
    elapsed_time_device=$((elapsed_time_device + WAIT_INTERVAL_SECONDS))
done
SBNB_DATA_DEVICE=$(readlink -f "${{SBNB_DATA_DEVICE_SYMLINK}}")
log "Data partition device resolved to ${{SBNB_DATA_DEVICE}} after ${{elapsed_time_device}}s."

# Ensure mount point directory exists
mkdir -p "${{SBNB_DATA_MOUNT_POINT}}"

log "Attempting to mount ${{SBNB_DATA_DEVICE}} at ${{SBNB_DATA_MOUNT_POINT}}..."
if ! mountpoint -q "${{SBNB_DATA_MOUNT_POINT}}"; then
    # Attempt to mount read-write, noatime, nodiratime
    if mount -o rw,noatime,nodiratime "${{SBNB_DATA_DEVICE}}" "${{SBNB_DATA_MOUNT_POINT}}"; then
        log "Successfully mounted persistent partition at ${{SBNB_DATA_MOUNT_POINT}}."
    else
        log "ERROR: Failed to mount ${{SBNB_DATA_DEVICE}} at ${{SBNB_DATA_MOUNT_POINT}}! Check filesystem and device."
        exit 1
    fi
else
    log "Persistent partition already mounted at ${{SBNB_DATA_MOUNT_POINT}}. Ensuring read-write..."
    # Ensure partition is mounted read-write
    mount -o remount,rw "${{SBNB_DATA_MOUNT_POINT}}" || {{
        log "ERROR: Failed to remount ${{SBNB_DATA_MOUNT_POINT}} as read-write! Docker requires write access."
        exit 1
    }}
fi

# --- Configure Docker to use Persistent Data Directory ---
log "Setting up Docker to use persistent data-root..."

# These paths are on the target SBNB system.
# PERSISTENT_DOCKER_ROOT_PATH is baked in from Python script.
PERSISTENT_DOCKER_ROOT_PATH="{PERSISTENT_DOCKER_ROOT}"
DOCKER_CONFIG_DIR_TARGET="{DOCKER_CONFIG_DIR_ON_TARGET}"
DOCKER_CONFIG_FILE_TARGET="{DOCKER_CONFIG_FILE_ON_TARGET}"
DOCKER_CONFIG_BACKUP_TARGET="{DOCKER_CONFIG_FILE_ON_TARGET}{DOCKER_CONFIG_BACKUP_SUFFIX}"
DOCKER_DATA_EPHEMERAL_TARGET="{DOCKER_DATA_EPHEMERAL_ON_TARGET}"
CONFIG_CHANGED_FLAG=0 # Flag to track if we need to restart docker

# 1. Ensure the persistent Docker data-root directory exists with correct owner/permissions
log "Ensuring persistent Docker data directory exists: ${{PERSISTENT_DOCKER_ROOT_PATH}}"
mkdir -p -m {DOCKER_ROOT_PERMISSIONS:o} "${{PERSISTENT_DOCKER_ROOT_PATH}}"
if [ ! -d "${{PERSISTENT_DOCKER_ROOT_PATH}}" ]; then
    log "ERROR: Failed to create persistent Docker data directory ${{PERSISTENT_DOCKER_ROOT_PATH}}!"
    exit 1
fi
log "Ensuring ownership of ${{PERSISTENT_DOCKER_ROOT_PATH}} is root:root..."
chown root:root "${{PERSISTENT_DOCKER_ROOT_PATH}}" || log "WARNING: Failed to set ownership on ${{PERSISTENT_DOCKER_ROOT_PATH}}. Docker might have issues."
log "Ensuring permissions of ${{PERSISTENT_DOCKER_ROOT_PATH}} are {DOCKER_ROOT_PERMISSIONS:o}..."
chmod {DOCKER_ROOT_PERMISSIONS:o} "${{PERSISTENT_DOCKER_ROOT_PATH}}" || log "WARNING: Failed to set permissions on ${{PERSISTENT_DOCKER_ROOT_PATH}}."
log "Persistent Docker data directory ensured."

# 2. Create/Update Docker daemon configuration (/etc/docker/daemon.json on target)
log "Configuring Docker daemon (${{DOCKER_CONFIG_FILE_TARGET}}) to use data-root: ${{PERSISTENT_DOCKER_ROOT_PATH}}"
mkdir -p "${{DOCKER_CONFIG_DIR_TARGET}}" # Ensure config directory exists

# Backup original config ONCE if it exists and backup doesn't
if [ -f "${{DOCKER_CONFIG_FILE_TARGET}}" ] && [ ! -f "${{DOCKER_CONFIG_BACKUP_TARGET}}" ]; then
    log "Backing up original Docker config to ${{DOCKER_CONFIG_BACKUP_TARGET}}..."
    cp -a "${{DOCKER_CONFIG_FILE_TARGET}}" "${{DOCKER_CONFIG_BACKUP_TARGET}}" || \\
        log "WARNING: Failed to create backup of ${{DOCKER_CONFIG_FILE_TARGET}}."
fi

# --- Safely update daemon.json ---
NEEDS_JSON_UPDATE=0
if command -v jq >/dev/null 2>&1; then # Use jq if available (preferred method)
    log "Using jq to manage daemon.json."
    [ -f "${{DOCKER_CONFIG_FILE_TARGET}}" ] || echo "{{}}" > "${{DOCKER_CONFIG_FILE_TARGET}}" # Ensure file exists for jq
    current_data_root_val=$(jq -r '.["data-root"] // ""' "${{DOCKER_CONFIG_FILE_TARGET}}")
    if [ "$current_data_root_val" != "${{PERSISTENT_DOCKER_ROOT_PATH}}" ]; then
        log "Data-root needs update (jq check). Preparing changes..."
        NEEDS_JSON_UPDATE=1
    else
        log "Docker data-root already correctly set in daemon.json (jq check)."
    fi
    if [ $NEEDS_JSON_UPDATE -eq 1 ]; then
        TMP_JSON_FILE=$(mktemp "${{DOCKER_CONFIG_DIR_TARGET}}/daemon.json.tmp.XXXXXX")
        log "Attempting to merge data-root setting using jq..."
        if jq --arg path_val "${{PERSISTENT_DOCKER_ROOT_PATH}}" '. + {{"data-root": $path_val}}' "${{DOCKER_CONFIG_FILE_TARGET}}" > "${{TMP_JSON_FILE}}"; then
            if jq -e . "${{TMP_JSON_FILE}}" > /dev/null; then # Check if jq produced valid JSON
                if ! cmp -s "${{TMP_JSON_FILE}}" "${{DOCKER_CONFIG_FILE_TARGET}}"; then
                    mv "${{TMP_JSON_FILE}}" "${{DOCKER_CONFIG_FILE_TARGET}}"
                    chmod {DOCKER_CONFIG_PERMISSIONS:o} "${{DOCKER_CONFIG_FILE_TARGET}}"
                    log "Successfully updated daemon.json using jq."
                    CONFIG_CHANGED_FLAG=1
                else
                    log "daemon.json content unchanged after jq merge, removing temp file."
                    rm -f "${{TMP_JSON_FILE}}"
                fi
            else log "ERROR: jq produced invalid JSON output. Config not updated."; rm -f "${{TMP_JSON_FILE}}"; fi
        else jq_exit_code=$?; log "ERROR: jq command failed (exit code $jq_exit_code). Config not updated."; rm -f "${{TMP_JSON_FILE}}"; fi
    fi
else # Fallback logic if jq is NOT available
    log "WARNING: jq not found. Using less robust fallback for daemon.json."
    TARGET_JSON_CONTENT_STR=$(printf '{{%s\\n  "data-root": "%s"%s\\n}}%s\\n' "" "${{PERSISTENT_DOCKER_ROOT_PATH}}" "" "")
    if [ ! -f "${{DOCKER_CONFIG_FILE_TARGET}}" ]; then
        log "daemon.json does not exist. Creating new file with data-root."
        NEEDS_JSON_UPDATE=1
    else
        if ! grep -q '"data-root"\\s*:' "${{DOCKER_CONFIG_FILE_TARGET}}"; then
             log "Existing daemon.json lacks 'data-root' key."
            if ! grep -q '[a-zA-Z0-9]' "${{DOCKER_CONFIG_FILE_TARGET}}" || grep -q '^\\s*{{\\s*}}\\s*$' "${{DOCKER_CONFIG_FILE_TARGET}}"; then
                log "Existing file is simple, overwriting with data-root."
                NEEDS_JSON_UPDATE=1
            else log "ERROR: Existing daemon.json is complex and lacks 'data-root'. Cannot safely update without jq."; NEEDS_JSON_UPDATE=0; fi
        elif ! grep -q '"data-root"\\s*:\\s*"${{PERSISTENT_DOCKER_ROOT_PATH}}"' "${{DOCKER_CONFIG_FILE_TARGET}}"; then
            log "ERROR: Existing daemon.json has 'data-root' but points elsewhere. Cannot safely update without jq."; NEEDS_JSON_UPDATE=0;
        else log "daemon.json exists and data-root seems correct (grep check)."; NEEDS_JSON_UPDATE=0; fi
    fi
    if [ $NEEDS_JSON_UPDATE -eq 1 ]; then
        log "Writing daemon.json (simple method)..."
        TMP_JSON_FILE=$(mktemp "${{DOCKER_CONFIG_DIR_TARGET}}/daemon.json.tmp.XXXXXX")
        echo "$TARGET_JSON_CONTENT_STR" > "${{TMP_JSON_FILE}}"
        if [ $? -eq 0 ]; then mv "${{TMP_JSON_FILE}}" "${{DOCKER_CONFIG_FILE_TARGET}}"; chmod {DOCKER_CONFIG_PERMISSIONS:o} "${{DOCKER_CONFIG_FILE_TARGET}}"; log "Successfully wrote simple daemon.json."; CONFIG_CHANGED_FLAG=1;
        else log "ERROR: Failed to write temporary simple daemon.json! Config not updated."; rm -f "${{TMP_JSON_FILE}}"; fi
    fi
fi
log "Docker daemon configuration check finished."

# 3. Data Migration (Optional): Migrate data from ephemeral location if needed
log "Checking for existing Docker data in ephemeral location (${{DOCKER_DATA_EPHEMERAL_TARGET}})..."
if [ -d "${{DOCKER_DATA_EPHEMERAL_TARGET}}" ] && [ -n "$(ls -A "${{DOCKER_DATA_EPHEMERAL_TARGET}}" | grep -v -e '^lost+found$' -e '^\\.sbnb_persistent_redirect$' -e '^README_DO_NOT_USE\\.txt$' 2>/dev/null)" ]; then
    log "Found potentially significant data in ${{DOCKER_DATA_EPHEMERAL_TARGET}}."
    persistent_dir_is_empty=0
    if [ ! "$(ls -A "${{PERSISTENT_DOCKER_ROOT_PATH}}" | grep -v '^lost+found$' 2>/dev/null)" ]; then persistent_dir_is_empty=1; fi
    if [ $persistent_dir_is_empty -eq 1 ]; then
        log "Persistent location ${{PERSISTENT_DOCKER_ROOT_PATH}} is empty. Migrating data..."
        if systemctl is-active --quiet docker; then log "Stopping Docker service for migration..."; systemctl stop docker || log "WARNING: Failed to stop Docker. Migration proceeding, but data might be inconsistent!"; sleep 3; fi
        log "Starting migration using cp -a -u..."; MIGRATION_SUCCESS_FLAG=0
        if cp -a -u "${{DOCKER_DATA_EPHEMERAL_TARGET}}/." "${{PERSISTENT_DOCKER_ROOT_PATH}}/"; then MIGRATION_SUCCESS_FLAG=1; else log "ERROR: cp -a -u migration failed with exit code $? !"; fi
        if [ $MIGRATION_SUCCESS_FLAG -eq 1 ]; then
            log "Migration completed successfully."
            OLD_DATA_BACKUP_PATH="${{DOCKER_DATA_EPHEMERAL_TARGET}}.migrated.$(date +%Y%m%d_%H%M%S).bak"
            log "Attempting to rename old data directory to ${{OLD_DATA_BACKUP_PATH}}..."
            if mv -T "${{DOCKER_DATA_EPHEMERAL_TARGET}}" "${{OLD_DATA_BACKUP_PATH}}"; then log "Successfully renamed old data directory."; else log "WARNING: Could not rename old data directory ${{DOCKER_DATA_EPHEMERAL_TARGET}}."; fi
            CONFIG_CHANGED_FLAG=1
        else log "ERROR: Data migration failed! Docker data may be incomplete/inconsistent in ${{PERSISTENT_DOCKER_ROOT_PATH}}."; exit 1; fi
    else
        log "Persistent location ${{PERSISTENT_DOCKER_ROOT_PATH}} already contains data. Skipping migration."
        OLD_DATA_BACKUP_PATH="${{DOCKER_DATA_EPHEMERAL_TARGET}}.ignored.$(date +%Y%m%d_%H%M%S).bak"
        log "Attempting to rename unused ephemeral data directory to ${{OLD_DATA_BACKUP_PATH}}..."
        mv -T "${{DOCKER_DATA_EPHEMERAL_TARGET}}" "${{OLD_DATA_BACKUP_PATH}}" || log "WARNING: Could not rename ephemeral data directory ${{DOCKER_DATA_EPHEMERAL_TARGET}}."
    fi
else log "No significant data found in ephemeral location ${{DOCKER_DATA_EPHEMERAL_TARGET}}. No migration needed."; fi
log "Ensuring ephemeral path ${{DOCKER_DATA_EPHEMERAL_TARGET}} exists and is marked as unused."
if [ -d "${{DOCKER_DATA_EPHEMERAL_TARGET}}" ]; then rm -rf "${{DOCKER_DATA_EPHEMERAL_TARGET}}" || log "WARNING: Failed to remove original ephemeral directory after processing."; fi
mkdir -p "${{DOCKER_DATA_EPHEMERAL_TARGET}}"
touch "${{DOCKER_DATA_EPHEMERAL_TARGET}}/.sbnb_persistent_redirect"
echo "Docker data is managed at ${{PERSISTENT_DOCKER_ROOT_PATH}}. This directory should remain empty." > "${{DOCKER_DATA_EPHEMERAL_TARGET}}/README_DO_NOT_USE.txt"
chmod 644 "${{DOCKER_DATA_EPHEMERAL_TARGET}}/README_DO_NOT_USE.txt"; chmod 600 "${{DOCKER_DATA_EPHEMERAL_TARGET}}/.sbnb_persistent_redirect"; log "Data migration check finished."

# 4. Restart Docker Service *if* configuration was changed OR migration occurred
if [ $CONFIG_CHANGED_FLAG -eq 1 ]; then
    log "Configuration or data migration requires Docker restart. Reloading daemon and restarting service..."
    if ! systemctl daemon-reload; then log "ERROR: Failed to reload systemd daemon! Docker restart might fail or use old config."; exit 1; fi
    log "Attempting to restart docker.service..."
    if systemctl restart docker.service; then log "Docker service restarted successfully."; else log "ERROR: Failed to restart Docker service! Check 'journalctl -u docker.service'."; exit 1; fi
else log "No configuration changes or migration. Docker restart not required by this script."; fi
log "Docker setup finished."

# --- Update Optional Development Environment Script ---
# (Using the robust atomic update logic)
TARGET_DEV_ENV_SCRIPT_PATH="/usr/sbin/sbnb-dev-env.sh" # Path on target system
# SOURCE_DEV_ENV_SCRIPT_PATH is on the DATA_MOUNT, so it's persistent.
SOURCE_DEV_ENV_SCRIPT_PATH="${{SBNB_DATA_MOUNT_POINT}}/scripts/sbnb-dev-env.sh"

log "Checking for optional development script update: ${{SOURCE_DEV_ENV_SCRIPT_PATH}}"
if [ -f "${{SOURCE_DEV_ENV_SCRIPT_PATH}}" ] && [ -r "${{SOURCE_DEV_ENV_SCRIPT_PATH}}" ]; then
    log "Source dev script found. Attempting atomic update of ${{TARGET_DEV_ENV_SCRIPT_PATH}}..."
    TARGET_DEV_SCRIPT_DIR=$(dirname "${{TARGET_DEV_ENV_SCRIPT_PATH}}")
    TMP_DEV_SCRIPT_FILE=""
    # Setup trap for cleanup of temp dev script file
    trap 'cleanup_dev_script_trap' EXIT HUP INT QUIT TERM
    cleanup_dev_script_trap() {{
        if [ -n "${{TMP_DEV_SCRIPT_FILE:-}}" ] && [ -f "${{TMP_DEV_SCRIPT_FILE}}" ]; then
            rm -f "${{TMP_DEV_SCRIPT_FILE}}"
            log "Cleaned up temporary dev script file ${{TMP_DEV_SCRIPT_FILE}}"
        fi
        trap - EXIT HUP INT QUIT TERM # Reset this specific trap
    }}
    if [ ! -d "${{TARGET_DEV_SCRIPT_DIR}}" ] || [ ! -w "${{TARGET_DEV_SCRIPT_DIR}}" ]; then log "WARNING: Target directory ${{TARGET_DEV_SCRIPT_DIR}} does not exist or is not writable. Cannot update script.";
    elif ! command -v mktemp >/dev/null 2>&1; then log "WARNING: Required command mktemp not found. Skipping update.";
    else
        TMP_DEV_SCRIPT_FILE=$(mktemp "${{TARGET_DEV_SCRIPT_DIR}}/sbnb-dev-env.sh.XXXXXX")
        if [ -z "${{TMP_DEV_SCRIPT_FILE}}" ] || [ ! -f "${{TMP_DEV_SCRIPT_FILE}}" ]; then log "WARNING: Failed to create temporary file in ${{TARGET_DEV_SCRIPT_DIR}}. Skipping update."; TMP_DEV_SCRIPT_FILE="";
        else
            if cp "${{SOURCE_DEV_ENV_SCRIPT_PATH}}" "${{TMP_DEV_SCRIPT_FILE}}"; then
                if chmod +x "${{TMP_DEV_SCRIPT_FILE}}"; then
                    if mv -T "${{TMP_DEV_SCRIPT_FILE}}" "${{TARGET_DEV_ENV_SCRIPT_PATH}}"; then log "Successfully updated ${{TARGET_DEV_ENV_SCRIPT_PATH}}."; TMP_DEV_SCRIPT_FILE=""; # Clear var so trap doesn't remove final script
                    else log "WARNING: Failed to move temporary file ${{TMP_DEV_SCRIPT_FILE}} to ${{TARGET_DEV_ENV_SCRIPT_PATH}}. Update failed."; fi
                else log "WARNING: Failed to set execute permissions on temporary file ${{TMP_DEV_SCRIPT_FILE}}. Update failed."; fi
            else log "WARNING: Failed to copy content from ${{SOURCE_DEV_ENV_SCRIPT_PATH}} to ${{TMP_DEV_SCRIPT_FILE}}. Update failed."; fi
        fi
        if [ -n "${{TMP_DEV_SCRIPT_FILE:-}}" ] && [ -f "${{TMP_DEV_SCRIPT_FILE}}" ]; then rm -f "${{TMP_DEV_SCRIPT_FILE}}"; fi; TMP_DEV_SCRIPT_FILE=""; # Ensure cleanup if mv failed
    fi
    trap - EXIT HUP INT QUIT TERM # Clear specific trap explicitly
else log "NOTE: Source dev script ${{SOURCE_DEV_ENV_SCRIPT_PATH}} not found or not readable. Skipping update."; fi
log "Update of optional dev script finished."

# --- Enable Systemd Units (Backup/Purge + Health/Volume Checks) ---
SYSTEMD_SOURCE_DIR_PATH="${{SBNB_DATA_MOUNT_POINT}}/systemd" # Units are on persistent data
SYSTEMD_TARGET_DIR_PATH="/etc/systemd/system" # Standard systemd unit dir on target
# TIMERS_WANTS_DIR_PATH="${{SYSTEMD_TARGET_DIR_PATH}}/timers.target.wants" # Not strictly needed to create, systemctl enable handles it

log "Enabling custom systemd units (Source: ${{SYSTEMD_SOURCE_DIR_PATH}})..."
if [ -d "${{SYSTEMD_SOURCE_DIR_PATH}}" ] && [ -r "${{SYSTEMD_SOURCE_DIR_PATH}}" ]; then
    mkdir -p "${{SYSTEMD_TARGET_DIR_PATH}}" # Ensure target systemd dir exists
    # mkdir -p "${{TIMERS_WANTS_DIR_PATH}}" # Not essential, systemctl enable creates links in wants dirs

    linked_any_unit=0; log "Linking systemd unit files..."
    find "${{SYSTEMD_SOURCE_DIR_PATH}}" -maxdepth 1 -type f \\( -name '*.service' -o -name '*.timer' \\) -print0 | while IFS= read -r -d '' source_unit_file; do
        unit_filename=$(basename "${{source_unit_file}}")
        target_unit_link="${{SYSTEMD_TARGET_DIR_PATH}}/${{unit_filename}}"
        log "  Linking ${{unit_filename}} to ${{target_unit_link}}..."
        if ln -sf "${{source_unit_file}}" "${{target_unit_link}}"; then linked_any_unit=1; else log "  WARNING: Failed to link ${{unit_filename}}."; fi
    done

    if [ $linked_any_unit -eq 0 ]; then log "No unit files found in ${{SYSTEMD_SOURCE_DIR_PATH}} to link.";
    else
        log "Reloading systemd daemon after linking units..."
        systemctl daemon-reload || log "WARNING: systemctl daemon-reload failed after linking units."
        log "Enabling systemd timers/services..."
        enabled_any_unit=0
        UNITS_TO_ENABLE_STR="docker-backup.timer docker-purge.timer docker-shutdown-backup.service docker-health-check.timer docker-volume-check.timer"
        final_enabled_units_list=""
        # shellcheck disable=SC2086 # Word splitting is intended here for $UNITS_TO_ENABLE_STR
        for unit_to_enable in $UNITS_TO_ENABLE_STR; do
            if [ -L "${{SYSTEMD_TARGET_DIR_PATH}}/${{unit_to_enable}}" ] && [ -f "${{SYSTEMD_TARGET_DIR_PATH}}/${{unit_to_enable}}" ]; then # Check link exists and points to a file
                log "  Enabling ${{unit_to_enable}}..."
                if systemctl enable "${{unit_to_enable}}"; then enabled_any_unit=1; final_enabled_units_list="${{final_enabled_units_list}} ${{unit_to_enable}}";
                else log "  WARNING: Failed to enable ${{unit_to_enable}}."; fi
            else log "  Skipping enable for ${{unit_to_enable}} (link missing or broken at ${{SYSTEMD_TARGET_DIR_PATH}}/${{unit_to_enable}})."; fi
        done
        if [ $enabled_any_unit -eq 1 ]; then final_enabled_units_list=$(echo "${{final_enabled_units_list}}" | sed 's/^ *//'); log "Systemd units enabled successfully: ${{final_enabled_units_list}}";
        else log "No relevant systemd units were successfully enabled."; fi
    fi
else log "WARNING: Systemd source directory ${{SYSTEMD_SOURCE_DIR_PATH}} not found or not readable. Cannot enable units."; fi
log "Systemd unit setup finished."

# --- Script Finish Logging ---
log "Finished custom boot commands successfully."
# Ensure all traps are cleared if any were missed by specific sections
trap - EXIT HUP INT QUIT TERM
exit 0
"""

# --- Tailscale Key Content (already defined by SBNB_TSKEY_TXT_CONTENT from args) ---

# --- Backup Script ---
BACKUP_DOCKER_SH_CONTENT = f"""#!/bin/sh
# File: {DATA_MOUNT}/scripts/backup-docker.sh
# Backs up the persistent Docker data-root directory.
# Version 1.1
set -e -u

# --- Configuration ---
DOCKER_DATA_DIR_TO_BACKUP="{PERSISTENT_DOCKER_ROOT}" # Source is PERSISTENT root
BACKUP_DEST_DIR="{BACKUP_BASE_DIR}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_ARCHIVE_FILE="${{BACKUP_DEST_DIR}}/docker_backup_${{TIMESTAMP}}.tar.gz"
LATEST_BACKUP_LINK="${{BACKUP_DEST_DIR}}/docker_latest.tar.gz"
STOP_DOCKER_DURING_BACKUP={STOP_DOCKER_FOR_BACKUP} # 1=Stop Docker (safer), 0=Live backup

log_backup() {{ echo "[backup-docker.sh] $1" > /dev/kmsg; }}

# --- Check Commands ---
log_backup "Checking required commands for backup script..."
check_backup_cmds() {{
    local missing_cmd_bk=0
    for cmd_bk in "$@"; do
        if ! command -v "$cmd_bk" >/dev/null 2>&1; then log_backup "ERROR: Command '$cmd_bk' not found."; missing_cmd_bk=1; fi
    done
    [ $missing_cmd_bk -eq 1 ] && exit 1 # Exit if any command is missing
}}
check_backup_cmds date mkdir tar gzip ln mv sleep dirname basename
[ $STOP_DOCKER_DURING_BACKUP -eq 1 ] && check_backup_cmds systemctl # Check systemctl only if stopping docker

NICE_COMMAND_PREFIX=""
if command -v nice >/dev/null 2>&1; then NICE_COMMAND_PREFIX="nice -n 19"; log_backup "Using 'nice' for lower tar priority."; fi

# --- Main Logic ---
log_backup "Starting Docker backup process..."
log_backup "Source:         ${{DOCKER_DATA_DIR_TO_BACKUP}}"
log_backup "Destination:    ${{BACKUP_ARCHIVE_FILE}}"

log_backup "Ensuring backup directory exists: ${{BACKUP_DEST_DIR}}"
mkdir -p "${{BACKUP_DEST_DIR}}"
if [ ! -w "${{BACKUP_DEST_DIR}}" ]; then log_backup "ERROR: Backup directory not writable: ${{BACKUP_DEST_DIR}}"; exit 1; fi

DOCKER_WAS_RUNNING_FLAG=0
if [ $STOP_DOCKER_DURING_BACKUP -eq 1 ]; then
    log_backup "Attempting to stop Docker service..."
    if systemctl is-active --quiet docker.service; then
        DOCKER_WAS_RUNNING_FLAG=1
        log_backup "Docker service is active, stopping..."
        if systemctl stop docker.service; then log_backup "Docker service stopped. Waiting 5s for files to release..."; sleep 5;
        else log_backup "ERROR: Failed to stop Docker service gracefully! Backup might be inconsistent or fail. Aborting."; exit 1; fi
    else log_backup "Docker service already stopped."; fi
fi

log_backup "Creating backup archive..."
if [ -d "${{DOCKER_DATA_DIR_TO_BACKUP}}" ] && [ -r "${{DOCKER_DATA_DIR_TO_BACKUP}}" ]; then
    PARENT_OF_SOURCE_DIR=$(dirname "${{DOCKER_DATA_DIR_TO_BACKUP}}")
    SOURCE_DIR_BASENAME=$(basename "${{DOCKER_DATA_DIR_TO_BACKUP}}")
    log_backup "Archiving '${{SOURCE_DIR_BASENAME}}' from parent '${{PARENT_OF_SOURCE_DIR}}'..."
    # shellcheck disable=SC2086 # Allow word splitting for $NICE_COMMAND_PREFIX
    if ${{NICE_COMMAND_PREFIX}} tar --warning=no-file-changed -czf "${{BACKUP_ARCHIVE_FILE}}" -C "${{PARENT_OF_SOURCE_DIR}}" "${{SOURCE_DIR_BASENAME}}"; then
        log_backup "Backup archive created successfully: ${{BACKUP_ARCHIVE_FILE}}"
        if [ -s "${{BACKUP_ARCHIVE_FILE}}" ]; then # Verify backup file exists and is not empty
            log_backup "Updating latest backup link..."
            ln -sfT "${{BACKUP_ARCHIVE_FILE}}" "${{LATEST_BACKUP_LINK}}.tmp" && mv -Tf "${{LATEST_BACKUP_LINK}}.tmp" "${{LATEST_BACKUP_LINK}}"
            if [ $? -eq 0 ]; then log_backup "Updated latest link to point to ${{BACKUP_ARCHIVE_FILE}}.";
            else log_backup "WARNING: Failed to update latest backup link."; rm -f "${{LATEST_BACKUP_LINK}}.tmp"; fi
        else log_backup "WARNING: Backup file seems invalid (empty/missing): ${{BACKUP_ARCHIVE_FILE}}. Removing."; rm -f "${{BACKUP_ARCHIVE_FILE}}"; fi
    else tar_exit_code_val=$?; log_backup "ERROR: tar command failed with exit code ${{tar_exit_code_val}}! Backup failed."; rm -f "${{BACKUP_ARCHIVE_FILE}}"; fi
else log_backup "WARNING: Docker data directory not found or not readable: ${{DOCKER_DATA_DIR_TO_BACKUP}}. Skipping backup."; fi

if [ $DOCKER_WAS_RUNNING_FLAG -eq 1 ]; then
    log_backup "Restarting Docker service..."
    if ! systemctl start docker.service; then log_backup "WARNING: Failed to restart Docker service after backup.";
    else log_backup "Docker service restarted."; fi
fi
log_backup "Docker backup process finished."
exit 0
"""

# --- Purge Script ---
PURGE_DOCKER_BACKUPS_SH_CONTENT = f"""#!/bin/sh
# File: {DATA_MOUNT}/scripts/purge-docker-backups.sh
# Removes old Docker backups, keeping the last N.
# Version 1.1
set -e -u

BACKUP_PURGE_DIR="{BACKUP_BASE_DIR}"
KEEP_BACKUP_COUNT={BACKUP_KEEP_COUNT}

log_purge() {{ echo "[purge-docker-backups.sh] $1" > /dev/kmsg; }}

check_purge_cmds() {{ local missing_cmd_prg=0; for cmd_prg in "$@"; do if ! command -v "$cmd_prg" >/dev/null 2>&1; then log_purge "ERROR: Command '$cmd_prg' not found."; missing_cmd_prg=1; fi; done; [ $missing_cmd_prg -eq 1 ] && exit 1; }};
check_purge_cmds find wc sort head cut xargs rm mkdir date

log_purge "Purging old Docker backups in ${{BACKUP_PURGE_DIR}}, keeping ${{KEEP_BACKUP_COUNT}}..."
if ! [ "$KEEP_BACKUP_COUNT" -ge 0 ] 2>/dev/null; then log_purge "ERROR: KEEP_BACKUP_COUNT (${{KEEP_BACKUP_COUNT}}) is invalid."; exit 1; fi
if ! mkdir -p "${{BACKUP_PURGE_DIR}}"; then log_purge "ERROR: Failed to create backup directory ${{BACKUP_PURGE_DIR}}!"; exit 1; fi
if [ ! -d "${{BACKUP_PURGE_DIR}}" ] || [ ! -r "${{BACKUP_PURGE_DIR}}" ] || [ ! -w "${{BACKUP_PURGE_DIR}}" ]; then log_purge "ERROR: Cannot access backup directory ${{BACKUP_PURGE_DIR}}!"; exit 1; fi

log_purge "Counting existing backup files..."
current_backup_count=$(find "${{BACKUP_PURGE_DIR}}" -maxdepth 1 -name 'docker_backup_*.tar.gz' -type f -print 2>/dev/null | wc -l)
find_exit_code_val=$?
if [ $find_exit_code_val -ne 0 ]; then log_purge "WARNING: find command failed (${{find_exit_code_val}}) while counting backups. Skipping purge."; exit 0; fi
log_purge "Found ${{current_backup_count}} backup files."

if [ "$current_backup_count" -gt "$KEEP_BACKUP_COUNT" ]; then
    num_to_delete=$(( current_backup_count - KEEP_BACKUP_COUNT ))
    log_purge "Need to delete ${{num_to_delete}} oldest backup(s)."
    log_purge "Identifying oldest backups to delete..."
    # Use find -printf with null terminators for safe filename handling
    delete_operation_output=$(find "${{BACKUP_PURGE_DIR}}" -maxdepth 1 -name 'docker_backup_*.tar.gz' -type f -printf '%T@ %p\\0' 2>/dev/null | \\
        sort -zn | head -zn "${{num_to_delete}}" | cut -z -d' ' -f2- | xargs -0 -r rm -v -- 2>&1)
    rm_exit_code_val=$?
    if [ $rm_exit_code_val -eq 0 ]; then
        log_purge "Purge completed successfully."
        if [ -n "$delete_operation_output" ]; then log_purge "Deleted files:"; echo "$delete_operation_output" | while IFS= read -r line_out || [ -n "$line_out" ]; do log_purge "  $line_out"; done; fi
    else log_purge "WARNING: Purge command (rm) failed (exit code ${{rm_exit_code_val}}). Check output below."; log_purge "rm output:"; echo "$delete_operation_output" | while IFS= read -r line_out || [ -n "$line_out" ]; do log_purge "  $line_out"; done; fi
else log_purge "${{current_backup_count}} backups found <= ${{KEEP_BACKUP_COUNT}}. No backups purged."; fi
log_purge "Backup purge process finished."
exit 0
"""

# --- Health Check Script ---
DOCKER_HEALTH_CHECK_SH_CONTENT = f"""#!/bin/sh
# File: {DATA_MOUNT}/scripts/docker-health-check.sh
# Checks Docker daemon health, responsiveness, and data-root configuration.
# Version 1.1
set -e -u

PERSISTENT_DOCKER_ROOT_HEALTH="{PERSISTENT_DOCKER_ROOT}"
DOCKER_CONFIG_FILE_HEALTH="{DOCKER_CONFIG_FILE_ON_TARGET}" # Path on target system

log_health() {{ echo "[docker-health-check] $1" | tee /dev/kmsg; }} # Log to kmsg and stdout/stderr

log_health "Starting Docker health check..."
check_health_cmds() {{ for cmd_hc in "$@"; do if ! command -v "$cmd_hc" >/dev/null 2>&1; then log_health "ERROR: Command '$cmd_hc' not found."; exit 1; fi; done }};
check_health_cmds systemctl docker

log_health "Checking if docker.service is active..."
if ! systemctl is-active --quiet docker.service; then
    log_health "WARNING: Docker service is not running. Attempting restart..."
    if systemctl restart docker.service; then log_health "Docker service restarted successfully."; sleep 5; # Give time to fully start
    else log_health "ERROR: Failed to restart inactive Docker service!"; exit 1; fi
fi

log_health "Checking Docker daemon responsiveness via 'docker info'..."
if ! docker info > /dev/null 2>&1; then
    log_health "WARNING: Docker service is running but 'docker info' command failed. Attempting restart..."
    if systemctl restart docker.service; then log_health "Docker service restarted successfully."; sleep 5; # Give it time
        if ! docker info > /dev/null 2>&1; then log_health "ERROR: Docker daemon still not responding after restart! Requires manual investigation."; exit 1;
        else log_health "Docker daemon is now responsive after restart."; fi
    else log_health "ERROR: Failed to restart unresponsive Docker service!"; exit 1; fi
else log_health "Docker daemon is responsive."; fi

log_health "Checking configured Docker data-root directory..."
CURRENT_DOCKER_ROOT_INFO=$(docker info --format '{{{{.DockerRootDir}}}}' 2>/dev/null || echo "ERROR_GETTING_DOCKER_INFO")
if [ "$CURRENT_DOCKER_ROOT_INFO" = "ERROR_GETTING_DOCKER_INFO" ]; then log_health "ERROR: Could not determine Docker's current data-root using 'docker info'. Health check incomplete."; exit 1;
elif [ "$CURRENT_DOCKER_ROOT_INFO" != "$PERSISTENT_DOCKER_ROOT_HEALTH" ]; then
    log_health "CRITICAL ERROR: Docker is using incorrect data-root!"
    log_health "  Expected: $PERSISTENT_DOCKER_ROOT_HEALTH"
    log_health "  Actual:   $CURRENT_DOCKER_ROOT_INFO"
    log_health "  This indicates a problem in $DOCKER_CONFIG_FILE_HEALTH or Docker failed to apply it. Manual intervention required."
    exit 1
else log_health "Docker is correctly using the persistent data-root: $PERSISTENT_DOCKER_ROOT_HEALTH"; fi
log_health "Docker health check completed successfully."
exit 0
"""

# --- Volume Check Script ---
# Define prune command based on configuration
if VOLUME_CHECK_PRUNE_LEVEL == 0:
    PRUNE_COMMAND_STR = "echo 'Automatic pruning disabled (Level 0).'" # No-op
elif VOLUME_CHECK_PRUNE_LEVEL == 1:
    # Prune stopped containers and dangling images only
    PRUNE_COMMAND_STR = "docker container prune -f && docker image prune -f"
elif VOLUME_CHECK_PRUNE_LEVEL >= 2:
    # Prune stopped containers and *all* unused images (more aggressive)
    PRUNE_COMMAND_STR = "docker container prune -f && docker image prune -a -f"
else: # Default to level 1 if invalid config
    PRUNE_COMMAND_STR = "docker container prune -f && docker image prune -f"

DOCKER_VOLUME_CHECK_SH_CONTENT = f"""#!/bin/sh
# File: {DATA_MOUNT}/scripts/docker-volume-check.sh
# Checks free space on the Docker persistent volume and optionally prunes resources.
# Version 1.1
set -e -u

DOCKER_ROOT_VOLUME_CHECK="{PERSISTENT_DOCKER_ROOT}"
MIN_FREE_PERCENT_VOLUME_CHECK={VOLUME_CHECK_THRESHOLD_PERCENT}
PRUNE_COMMAND_TO_RUN="{PRUNE_COMMAND_STR}" # Baked in from Python

log_volume() {{ echo "[docker-volume-check] $1" | tee /dev/kmsg; }}

log_volume "Checking Docker volume free space: ${{DOCKER_ROOT_VOLUME_CHECK}}"
check_volume_cmds() {{ for cmd_vc in "$@"; do if ! command -v "$cmd_vc" >/dev/null 2>&1; then log_volume "ERROR: Command '$cmd_vc' not found."; exit 1; fi; done }};
check_volume_cmds df awk sed docker # Need docker if pruning is enabled

if [ ! -d "$DOCKER_ROOT_VOLUME_CHECK" ]; then log_volume "ERROR: Docker root directory not found: $DOCKER_ROOT_VOLUME_CHECK"; exit 1; fi

log_volume "Calculating free space..."
df_output_str=$(df -P "$DOCKER_ROOT_VOLUME_CHECK" | awk 'NR==2 {{print $4, $2}}' 2>/dev/null) # Available Total (1K blocks)
if [ -z "$df_output_str" ]; then log_volume "ERROR: Failed to get disk usage using df for $DOCKER_ROOT_VOLUME_CHECK"; exit 1; fi
avail_kb_val=$(echo "$df_output_str" | awk '{{print $1}}'); total_kb_val=$(echo "$df_output_str" | awk '{{print $2}}')

if [ -z "$total_kb_val" ] || [ "$total_kb_val" -le 0 ]; then log_volume "WARNING: Total disk size reported as zero or invalid for $DOCKER_ROOT_VOLUME_CHECK. Cannot calculate percentage."; exit 0; fi
free_percent_val=$(( (avail_kb_val * 100) / total_kb_val ))
total_size_hr_val=$(df -h "$DOCKER_ROOT_VOLUME_CHECK" | awk 'NR==2 {{print $2}}'); avail_size_hr_val=$(df -h "$DOCKER_ROOT_VOLUME_CHECK" | awk 'NR==2 {{print $4}}')
log_volume "Volume Stats: Total=${{total_size_hr_val}}, Available=${{avail_size_hr_val}}, Free=${{free_percent_val}}%"

if [ "$free_percent_val" -lt "$MIN_FREE_PERCENT_VOLUME_CHECK" ]; then
    log_volume "WARNING: Low disk space! Free: ${{free_percent_val}}% (Threshold: ${{MIN_FREE_PERCENT_VOLUME_CHECK}}%)"
    if [ {VOLUME_CHECK_PRUNE_LEVEL} -gt 0 ]; then # Check if pruning is enabled
        log_volume "Attempting automatic prune (Level: {VOLUME_CHECK_PRUNE_LEVEL}). Command: ${{PRUNE_COMMAND_TO_RUN}}"
        prune_command_output=$({PRUNE_COMMAND_STR} 2>&1) || prune_command_exit_code=$?
        if [ "${{prune_command_exit_code:-0}}" -eq 0 ]; then log_volume "Docker prune command executed successfully.";
        else log_volume "WARNING: Docker prune command finished with exit code ${{prune_command_exit_code}}."; fi
        log_volume "Prune output:"; echo "$prune_command_output" | while IFS= read -r line_prune_out || [ -n "$line_prune_out" ]; do log_volume "  $line_prune_out"; done
        log_volume "Recalculating space after cleanup..."
        df_output_str=$(df -P "$DOCKER_ROOT_VOLUME_CHECK" | awk 'NR==2 {{print $4, $2}}' 2>/dev/null)
        avail_kb_val=$(echo "$df_output_str" | awk '{{print $1}}'); total_kb_val=$(echo "$df_output_str" | awk '{{print $2}}')
        if [ "$total_kb_val" -gt 0 ]; then free_percent_val=$(( (avail_kb_val * 100) / total_kb_val )); else free_percent_val=0; fi
        avail_size_hr_val=$(df -h "$DOCKER_ROOT_VOLUME_CHECK" | awk 'NR==2 {{print $4}}')
        log_volume "Space after cleanup: Available=${{avail_size_hr_val}}, Free=${{free_percent_val}}%"
        if [ "$free_percent_val" -lt "$MIN_FREE_PERCENT_VOLUME_CHECK" ]; then log_volume "ERROR: Space still critically low after cleanup! Manual intervention likely required.";
        else log_volume "Space is now above threshold after cleanup."; fi
    else log_volume "Automatic pruning is disabled (Level 0). Manual cleanup needed."; fi
else log_volume "Sufficient free space available (${{free_percent_val}}%)."; fi
log_volume "Docker volume check completed."
exit 0
"""

# --- Systemd Units (Content definitions remain the same as previous version, ensure paths are correct) ---
# Backup Service
DOCKER_BACKUP_SERVICE_CONTENT = f"""# File: {DATA_MOUNT}/systemd/docker-backup.service
[Unit]
Description=Backup Docker Data ({PERSISTENT_DOCKER_ROOT})
Documentation=file://{DATA_MOUNT}/scripts/backup-docker.sh
Requires=mnt-sbnb-data.mount
After=mnt-sbnb-data.mount docker.service

[Service]
Type=oneshot
ExecStart=/bin/sh {DATA_MOUNT}/scripts/backup-docker.sh
"""
# Backup Timer
DOCKER_BACKUP_TIMER_CONTENT = f"""# File: {DATA_MOUNT}/systemd/docker-backup.timer
[Unit]
Description=Daily Docker Backup Timer ({PERSISTENT_DOCKER_ROOT})
Requires=docker-backup.service

[Timer]
OnCalendar=*-*-* 05:00:00
AccuracySec=1h
Persistent=true
RandomizedDelaySec=600
Unit=docker-backup.service

[Install]
WantedBy=timers.target
"""
# Purge Service
DOCKER_PURGE_SERVICE_CONTENT = f"""# File: {DATA_MOUNT}/systemd/docker-purge.service
[Unit]
Description=Purge Old Docker Backups ({BACKUP_BASE_DIR})
Documentation=file://{DATA_MOUNT}/scripts/purge-docker-backups.sh
Requires=mnt-sbnb-data.mount
After=mnt-sbnb-data.mount

[Service]
Type=oneshot
ExecStart=/bin/sh {DATA_MOUNT}/scripts/purge-docker-backups.sh
"""
# Purge Timer
DOCKER_PURGE_TIMER_CONTENT = f"""# File: {DATA_MOUNT}/systemd/docker-purge.timer
[Unit]
Description=Daily Docker Backup Purge Timer
Requires=docker-purge.service

[Timer]
OnCalendar=*-*-* 06:00:00
AccuracySec=1h
Persistent=true
RandomizedDelaySec=300
Unit=docker-purge.service

[Install]
WantedBy=timers.target
"""
# Shutdown Backup Service
DOCKER_SHUTDOWN_BACKUP_SERVICE_CONTENT = f"""# File: {DATA_MOUNT}/systemd/docker-shutdown-backup.service
[Unit]
Description=Backup Docker Data ({PERSISTENT_DOCKER_ROOT}) on Shutdown (Best Effort)
Documentation=file://{DATA_MOUNT}/scripts/backup-docker.sh
DefaultDependencies=no
Requires=mnt-sbnb-data.mount docker.service
After=mnt-sbnb-data.mount docker.service network.target
Before=shutdown.target reboot.target halt.target kexec.target umount.target final.target

[Service]
Type=oneshot
RemainAfterExit=true
TimeoutStopSec=180
ExecStop=/bin/sh {DATA_MOUNT}/scripts/backup-docker.sh

[Install]
WantedBy=shutdown.target reboot.target halt.target kexec.target
"""
# Health Check Service
DOCKER_HEALTH_SERVICE_CONTENT = f"""# File: {DATA_MOUNT}/systemd/docker-health-check.service
[Unit]
Description=Docker Health Check Service
Documentation=file://{DATA_MOUNT}/scripts/docker-health-check.sh
Requires=mnt-sbnb-data.mount docker.service
After=mnt-sbnb-data.mount docker.service

[Service]
Type=oneshot
ExecStart=/bin/sh {DATA_MOUNT}/scripts/docker-health-check.sh
"""
# Health Check Timer
DOCKER_HEALTH_TIMER_CONTENT = f"""# File: {DATA_MOUNT}/systemd/docker-health-check.timer
[Unit]
Description=Regular Docker Health Check Timer
Requires=docker-health-check.service

[Timer]
OnBootSec=5min
OnUnitActiveSec=15min
AccuracySec=1min
Unit=docker-health-check.service

[Install]
WantedBy=timers.target
"""
# Volume Check Service
DOCKER_VOLUME_SERVICE_CONTENT = f"""# File: {DATA_MOUNT}/systemd/docker-volume-check.service
[Unit]
Description=Docker Volume Space Check Service ({PERSISTENT_DOCKER_ROOT})
Documentation=file://{DATA_MOUNT}/scripts/docker-volume-check.sh
Requires=mnt-sbnb-data.mount docker.service
After=mnt-sbnb-data.mount docker.service

[Service]
Type=oneshot
ExecStart=/bin/sh {DATA_MOUNT}/scripts/docker-volume-check.sh
"""
# Volume Check Timer
DOCKER_VOLUME_TIMER_CONTENT = f"""# File: {DATA_MOUNT}/systemd/docker-volume-check.timer
[Unit]
Description=Regular Docker Volume Check Timer
Requires=docker-volume-check.service

[Timer]
OnBootSec=10min
OnUnitActiveSec=1h
AccuracySec=5min
Unit=docker-volume-check.service

[Install]
WantedBy=timers.target
"""

# --- Dictionary of Files to Create ---
# Defines all files to be generated by this Python script
FILES_TO_CREATE_PY = {
    # --- ESP Files ---
    f"{ESP_MOUNT}/sbnb-cmds.sh": {
        "content": SBNB_CMDS_SH_CONTENT, "permissions": 0o755 # rwxr-xr-x
    },
    f"{ESP_MOUNT}/sbnb-tskey.txt": {
        "content": SBNB_TSKEY_TXT_CONTENT, "permissions": 0o600 # rw-------
    },
    # --- Data Partition Files ---
    # Helper Scripts (ensure parent 'scripts' dir is created)
    f"{DATA_MOUNT}/scripts/backup-docker.sh": {
        "content": BACKUP_DOCKER_SH_CONTENT, "permissions": 0o750 # rwxr-x---
    },
    f"{DATA_MOUNT}/scripts/purge-docker-backups.sh": {
        "content": PURGE_DOCKER_BACKUPS_SH_CONTENT, "permissions": 0o750
    },
    f"{DATA_MOUNT}/scripts/docker-health-check.sh": {
        "content": DOCKER_HEALTH_CHECK_SH_CONTENT, "permissions": 0o750
    },
    f"{DATA_MOUNT}/scripts/docker-volume-check.sh": {
        "content": DOCKER_VOLUME_CHECK_SH_CONTENT, "permissions": 0o750
    },
    # Systemd Units (ensure parent 'systemd' dir is created)
    f"{DATA_MOUNT}/systemd/docker-backup.service": {
        "content": DOCKER_BACKUP_SERVICE_CONTENT, "permissions": 0o644 # rw-r--r--
    },
    f"{DATA_MOUNT}/systemd/docker-backup.timer": {
        "content": DOCKER_BACKUP_TIMER_CONTENT, "permissions": 0o644
    },
    f"{DATA_MOUNT}/systemd/docker-purge.service": {
        "content": DOCKER_PURGE_SERVICE_CONTENT, "permissions": 0o644
    },
    f"{DATA_MOUNT}/systemd/docker-purge.timer": {
        "content": DOCKER_PURGE_TIMER_CONTENT, "permissions": 0o644
    },
    f"{DATA_MOUNT}/systemd/docker-shutdown-backup.service": {
        "content": DOCKER_SHUTDOWN_BACKUP_SERVICE_CONTENT, "permissions": 0o644
    },
    f"{DATA_MOUNT}/systemd/docker-health-check.service": {
        "content": DOCKER_HEALTH_SERVICE_CONTENT, "permissions": 0o644
    },
    f"{DATA_MOUNT}/systemd/docker-health-check.timer": {
        "content": DOCKER_HEALTH_TIMER_CONTENT, "permissions": 0o644
    },
    f"{DATA_MOUNT}/systemd/docker-volume-check.service": {
        "content": DOCKER_VOLUME_SERVICE_CONTENT, "permissions": 0o644
    },
    f"{DATA_MOUNT}/systemd/docker-volume-check.timer": {
        "content": DOCKER_VOLUME_TIMER_CONTENT, "permissions": 0o644
    },
}

# --- Global counters for create_files status ---
warning_count_py_global = 0
fail_count_py_global = 0

# --- Main Python Script Logic ---
def check_python_script_prerequisites():
    """Verify script prerequisites before attempting file creation."""
    log_py("INFO", "--- Checking Python Script Prerequisites ---")
    prereqs_passed = True
    # UID check is handled by Bash script calling this with sudo.
    # Here we check if the mount points passed as arguments are valid.
    
    base_directories_to_check = {ESP_MOUNT: "ESP", DATA_MOUNT: "Data"}
    for dir_path_str, dir_name_str in base_directories_to_check.items():
        dir_path_obj = pathlib.Path(dir_path_str)
        log_py("INFO", f"Checking {dir_name_str} mount point: {dir_path_str}...")
        if not dir_path_obj.is_dir():
            log_py("ERROR", f"Base {dir_name_str} directory '{dir_path_str}' does not exist or is not a directory.")
            prereqs_passed = False
        # This script runs as root (called by sudo python3), so it should have write access if mounted correctly.
        # We can still check os.access for sanity.
        elif not os.access(dir_path_obj, os.W_OK | os.X_OK):
            log_py("ERROR", f"Base {dir_name_str} directory '{dir_path_str}' is not writable/executable by current user (root). Check mount options or permissions.")
            prereqs_passed = False
        else:
            log_py("INFO", f"OK: Base {dir_name_str} directory '{dir_path_str}' exists and is accessible.")

    # Check for optional but recommended commands needed by *generated* scripts (on target)
    # This is informational for the user running this Python script.
    # The actual check happens in sbnb-cmds.sh on the target.
    if shutil.which("jq"): # Checks on the system running this Python script
        log_py("INFO", "Host check: 'jq' command found (recommended for robust daemon.json handling by generated script).")
    else:
        log_py("WARN", "Host check: 'jq' command not found. Generated sbnb-cmds.sh will use less robust methods for daemon.json.")

    if not prereqs_passed:
        log_py("ERROR", "Python Script Prerequisites not met. Aborting script.")
        sys.exit(1)
    log_py("INFO", "--- Python Script Prerequisites OK ---")
    return True

def create_files_python_script():
    """Creates directories and files as defined in FILES_TO_CREATE_PY."""
    global warning_count_py_global, fail_count_py_global # Declare intent to modify globals
    log_py("INFO", "\n--- Python Script: Starting File Creation Process ---")
    num_success_created = 0
    warning_count_py_global = 0 
    fail_count_py_global = 0    

    # Ensure the base backup directory exists first with correct permissions
    try:
        log_py("INFO", f"\nEnsuring base backup directory exists: {BACKUP_BASE_DIR}")
        # Create directory with specific permissions (rwxr-x---)
        os.makedirs(BACKUP_BASE_DIR, mode=BACKUP_DIR_PERMISSIONS, exist_ok=True)
        # Explicitly set permissions in case it already existed with different ones
        current_backup_dir_perm = stat.S_IMODE(os.stat(BACKUP_BASE_DIR).st_mode)
        if current_backup_dir_perm != BACKUP_DIR_PERMISSIONS:
            log_py("INFO", f"  Adjusting permissions on {BACKUP_BASE_DIR} to {BACKUP_DIR_PERMISSIONS:o}...")
            os.chmod(BACKUP_BASE_DIR, BACKUP_DIR_PERMISSIONS)
        log_py("INFO", f"OK: Backup directory ensured: {BACKUP_BASE_DIR} with permissions {BACKUP_DIR_PERMISSIONS:o}")
    except OSError as e_os:
        log_py("ERROR", f"Failed to create or set permissions on {BACKUP_BASE_DIR}: {e_os}")
        sys.exit(1) # Critical failure
    except Exception as e_exc:
        log_py("ERROR", f"An unexpected error occurred ensuring backup directory: {e_exc}")
        sys.exit(1) # Critical failure

    # Process the files dictionary
    for file_path_to_create_str, file_details in FILES_TO_CREATE_PY.items():
        file_path_obj = pathlib.Path(file_path_to_create_str)
        did_write_succeed = False 

        try:
            file_content_str = file_details.get("content") 
            file_permissions_oct = file_details.get("permissions")
            if file_permissions_oct is None: # Should not happen with current dict
                file_permissions_oct = 0o644 if file_content_str is not None else 0o755
                log_py("INFO", f"No specific permission for {file_path_obj}, using default {file_permissions_oct:o}.")
        except KeyError as e_key:
            log_py("ERROR", f"\nConfiguration error - Missing '{e_key}' key for entry {file_path_to_create_str}. Skipping.")
            fail_count_py_global += 1
            continue
        
        log_py("INFO", f"\nProcessing: {file_path_obj}")

        # 1. Create parent directories robustly
        try:
            parent_directory_path = file_path_obj.parent
            if not parent_directory_path.is_dir():
                log_py("INFO", f"  Creating parent directory: {parent_directory_path}")
                os.makedirs(parent_directory_path, mode=0o755, exist_ok=True) # Default rwxr-xr-x for new dirs
            # Ensure existing parent has standard 755 permissions (important for scripts/systemd dirs)
            if stat.S_IMODE(os.stat(parent_directory_path).st_mode) != 0o755:
                 os.chmod(parent_directory_path, 0o755)
        except OSError as e_os_parent:
            log_py("ERROR", f"  Failed to create or set permissions on parent directory {parent_directory_path}: {e_os_parent}")
            fail_count_py_global += 1; continue 
        
        # 2. Write the file content
        if file_content_str is not None: # It's a file
            try:
                log_py("INFO", f"  Writing content to {file_path_obj}...")
                file_path_obj.write_text(file_content_str, encoding='utf-8')
                log_py("INFO", f"  Successfully wrote: {file_path_obj}")
                did_write_succeed = True
            except IOError as e_io:
                log_py("ERROR", f"  Failed to write file {file_path_obj}: {e_io}")
                fail_count_py_global += 1; continue 
        else: # Should be a directory (content is None) - not used in current FILES_TO_CREATE_PY
            log_py("WARN", f"  Content is None for {file_path_obj}, assuming directory creation (not typical for this script).")
            try:
                os.makedirs(file_path_obj, mode=file_permissions_oct, exist_ok=True)
                if stat.S_IMODE(os.stat(file_path_obj).st_mode) != file_permissions_oct: os.chmod(file_path_obj, file_permissions_oct)
                did_write_succeed = True
            except OSError as e_os_dir:
                log_py("ERROR", f"  Failed to create/set permissions on directory {file_path_obj}: {e_os_dir}"); fail_count_py_global += 1; continue

        # 3. Set permissions (only if write/dir creation succeeded)
        if did_write_succeed:
            try:
                current_file_perm = stat.S_IMODE(os.stat(file_path_obj).st_mode)
                if current_file_perm != file_permissions_oct:
                    log_py("INFO", f"  Setting permissions to {file_permissions_oct:o} (currently {current_file_perm:o})...")
                    os.chmod(file_path_obj, file_permissions_oct)
                log_py("INFO", f"  Successfully set/verified permissions for: {file_path_obj}")
                num_success_created += 1 
            except OSError as e_os_chmod:
                log_py("WARN", f"  Failed to set permissions on {file_path_obj}: {e_os_chmod}")
                warning_count_py_global += 1 
    
    # --- Summary ---
    log_py("INFO", "\n--- Python Script: File Creation Summary ---")
    log_py("INFO", f"Successfully processed (created/permissioned): {num_success_created} items")
    log_py("INFO", f"Items processed but with warnings:             {warning_count_py_global}")
    log_py("INFO", f"Failed operations (write/dir/parent):          {fail_count_py_global}")
    log_py("INFO", "-----------------------------------------------\n")

    if fail_count_py_global > 0:
        log_py("ERROR", "Fatal errors occurred during file creation by Python script. Deployment incomplete.")
        return False # Fatal errors occurred
    if warning_count_py_global > 0:
        log_py("WARN", "Deployment completed by Python script, but with warnings. Please review the output above.")
        # Decide if warnings are acceptable to return True
    return True


# --- Python Script Execution Entry Point ---
if __name__ == "__main__":
    log_py("INFO", "=====================================================================")
    log_py("INFO", " SBNB Advanced Configuration Deployment Script (Python Helper v1.1) ")
    log_py("INFO", "=====================================================================")
    log_py("INFO", f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_py("INFO", f"Target ESP Mount: {ESP_MOUNT}")
    log_py("INFO", f"Target Data Mount: {DATA_MOUNT}")
    log_py("INFO", "This script is intended to be called by 'unified_sbnb_prep.sh'.")
    log_py("INFO", "=====================================================================\n")

    if check_python_script_prerequisites():
        if create_files_python_script():
            log_py("INFO", "\nSBNB configuration file deployment completed successfully by Python script.")
            if "placeholder-key-not-provided-by-user" in SBNB_TSKEY_TXT_CONTENT:
                 log_py("WARN", "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                 log_py("WARN", "!!! CRITICAL: A placeholder Tailscale key was used. You MUST replace    !!!")
                 log_py("WARN", f"!!!           the content of '{ESP_MOUNT}/sbnb-tskey.txt' with your actual key! !!!")
                 log_py("WARN", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            sys.exit(0) # Success
        else:
            # Errors already logged by create_files_python_script
            sys.exit(1) # Failure due to fatal errors
    else:
        # Errors logged by check_python_script_prerequisites
        sys.exit(1) # Failure due to prerequisites
```

## How to Use the Unified Utility

1.  **Save the Scripts:**
    *   Copy the main Bash script and save it as `unified_sbnb_prep.sh`.
    *   Copy the Python helper script and save it as `deploy_sbn_config.py` **in the same directory** as `unified_sbnb_prep.sh`.
2.  **Make Bash Script Executable:** Open a terminal and run `chmod +x unified_sbnb_prep.sh`. (The Python script does not need to be made executable directly by the user).
3.  **Run the Script:** Execute the main Bash script as a normal user:
    ```bash
    ./unified_sbnb_prep.sh
    ```
    The script will prompt for `sudo` password when needed for privileged operations.
4.  **Follow Prompts:** The script will guide you through selecting a mode and providing necessary information.

### Simple Mode Instructions:

This mode is for creating a standard SBNB bootable drive by writing a complete `sbnb.raw` disk image to a target USB/disk.
1.  When prompted, choose option `1` for Simple Mode.
2.  Enter the full path to your `sbnb.raw` disk image file (e.g., `/home/user/sbnb.raw`).
3.  (Optional) Enter the path to a local `sbnb-tskey.txt` file if you want to include a Tailscale key.
4.  Select the target USB/disk device from the listed available devices. **Be extremely careful with this selection.**
5.  Confirm the destructive operation by typing `yes`.
6.  (Optional) Enter the path to a local custom script (e.g., `my-custom-boot.sh`) if you want it copied to the ESP as `sbnb-cmds.sh` to run at boot.
7.  The script will then write the image and copy optional files.

### Advanced Mode Instructions:

This mode is for preparing a USB/disk with a dedicated EFI System Partition (ESP) and a separate data partition for persistent storage. It then deploys a comprehensive SBNB configuration for Docker persistence, backups, and monitoring using the `deploy_sbn_config.py` helper.

1.  When prompted, choose option `2` for Advanced Mode.
2.  Enter the full path to your SBNB EFI boot file (e.g., `/path/to/your/BOOTX64.EFI`).
3.  Select the target USB/disk device for partitioning and setup. **Be extremely careful.**
4.  Confirm the destructive partitioning operation by typing `yes`. The script will then partition and format the drive, and automatically determine the ESP and Data partition device names.
5.  The script will create temporary mount points, mount these partitions, and copy the SBNB EFI file to the ESP as `/EFI/BOOT/BOOTX64.EFI`.
6.  You will be prompted to enter your Tailscale authentication key (input will be hidden). If you skip this or provide an empty string, a placeholder key will be written. **If a placeholder is used, you MUST manually edit `sbnb-tskey.txt` on the ESP of the USB drive with your actual key before its first use.**
7.  The `deploy_sbn_config.py` script will then be executed to deploy all necessary configuration files, including `sbnb-cmds.sh` on the ESP, and helper scripts/systemd units on the data partition.
8.  Once complete, the script will unmount the partitions during cleanup.

## Post-Setup Steps (After Script Completion)

1.  **Safely Eject (Conceptual):** After the script and its cleanup trap complete, the USB drive is prepared.
2.  **BIOS/UEFI Configuration:**
    *   Insert the USB drive into your target server.
    *   Enter the server's BIOS/UEFI setup utility (DEL, F2, F10, F12, ESC, etc.).
    *   Ensure **UEFI Mode** is enabled.
    *   Disable **CSM (Compatibility Support Module)** or **Legacy Boot Mode**.
    *   Disable **Secure Boot** (SBNB EFI files are typically not signed).
    *   Set the USB drive (e.g., "UEFI: USB Device Name") as the **primary boot device**.
    *   Save changes and exit.
3.  **Boot and Verify:**
    *   The server should boot from the SBNB USB drive.
    *   **For Advanced Mode:**
        *   Monitor boot process (console/`kmsg`) for `sbnb-cmds.sh` logs.
        *   After boot, SSH into SBNB.
        *   Verify data partition mount: `lsblk -f`, `df -hT | grep '/mnt/sbnb-data'`.
        *   Verify Docker data root: `sudo docker info | grep "Docker Root Dir"`. (Should be `/mnt/sbnb-data/docker-root` or as configured).
        *   Check systemd timers: `sudo systemctl list-timers --all | grep docker`.
        *   Check logs:
            ```bash
            sudo journalctl -t sbnb-cmds.sh --no-pager --since "10 minutes ago"
            sudo journalctl -t backup-docker.sh --no-pager --since "10 minutes ago"
            # etc. for other helper scripts
            ```
        *   If you used a placeholder Tailscale key, ensure you have updated `sbnb-tskey.txt` on the ESP (can be done by mounting the ESP on another Linux system if needed before first boot, or on the SBNB system itself if accessible).

## Key Features of Components

This unified utility leverages the strengths of several well-designed components:

*   **Main Orchestrator (`unified_sbnb_prep.sh`):**
    *   User-friendly mode selection and interactive prompts.
    *   Robust disk selection and common pre-steps.
    *   Handles Simple Mode logic directly (raw image writing, optional file copies).
    *   For Advanced Mode, performs robust partitioning and formatting (`prepare_usb_advanced` function) with critical OS drive safety checks.
    *   Manages mounting/unmounting of partitions.
    *   Securely prompts for sensitive data (Tailscale key).
    *   Calls the Python helper script for complex configuration deployment.
    *   Comprehensive cleanup of temporary resources.

*   **Python Configuration Deployer (`deploy_sbn_config.py`):**
    *   Receives parameters (mount paths, keys) from the Bash script.
    *   Generates a sophisticated `sbnb-cmds.sh` for the ESP, which runs at boot on the SBNB system to:
        *   Mount the persistent data partition by label.
        *   Configure Docker to use a persistent `data-root`.
        *   Optionally migrate existing Docker data.
        *   Atomically update an optional development script.
        *   Link and enable systemd units.
    *   Deploys `sbnb-tskey.txt` to the ESP.
    *   Deploys helper shell scripts and systemd units to the data partition for Docker backup, purging, health checks, and volume monitoring.

## Conclusion

This Unified SBNB Drive Preparation Utility provides a flexible, robust, and more maintainable solution for SBNB Linux deployment. By offering distinct modes and separating complex configuration logic into a Python helper, it caters to both simple needs and advanced, persistent setups, while prioritizing safety and comprehensive functionality. Remember to always double-check your target device and understand the operations being performed.