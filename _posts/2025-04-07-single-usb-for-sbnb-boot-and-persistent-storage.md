---
tags: [scratchpad]
info: aberto.
date: 2025-04-07
type: post
layout: post
published: true
slug: single-usb-for-sbnb-boot-and-persistent-storage
title: 'Single USB for Sbnb Boot and Persistent Storage'
---
This guide provides comprehensive, step-by-step instructions for configuring a single USB flash drive (or potentially an external USB hard drive) to perform two distinct functions simultaneously:

1.  **Booting the Sbnb Linux Operating System:** The drive will be prepared with a standard UEFI-compatible structure, specifically an EFI System Partition (ESP) containing the Sbnb EFI bootloader (`sbnb.efi`) and necessary configuration files. This allows the server's firmware to locate and start the Sbnb boot process. The `sbnb.efi` file itself is typically a Unified Kernel Image (UKI), bundling the Linux kernel, initramfs, and kernel command line into a single executable file.
2.  **Providing Simple Persistent Storage:** Utilizing a separate partition on the same physical USB drive, formatted with a standard Linux filesystem (`ext4` is used in this guide). This partition is intended to be automatically mounted at the `/mnt/sbnb-data` directory path within the running Sbnb Linux system via a custom boot script (`sbnb-cmds.sh`). This provides a space where data (like container volumes, application data, logs, user files) can persist across reboots of the otherwise ephemeral, RAM-based Sbnb OS.

**Why `ext4` instead of LVM:** Initial analysis suggested LVM might be suitable, but further review of the default Sbnb Linux build configuration indicates the necessary `lvm2` user-space tools are likely missing from the base runtime environment. Without these tools, managing LVM volumes during boot via standard scripts is infeasible unless you create a custom Sbnb build that includes the `lvm2` package. This revised guide therefore uses a standard `ext4` filesystem partition, relying only on basic tools expected to be present in Sbnb.

**Contrasting with Standard Sbnb Workflow:** It's crucial to understand that this guide describes a highly non-standard setup. The intended Sbnb workflow prioritizes resilience, performance, and statelessness:

* Boot the minimal Sbnb OS from simple USB/network.
* Use automation (Ansible) or manual scripts (`sbnb-configure-storage.sh`) post-boot to configure LVM on internal server drives.
* Run workloads utilizing this fast, reliable internal storage. This guide's method compromises these benefits for single-drive convenience under specific constraints.

---

> ***** EXTREME CAUTION: IRREVERSIBLE DATA DESTRUCTION IMMINENT! *****
>
> This procedure involves low-level disk operations (partitioning, formatting) that will completely and **PERMANENTLY ERASE ALL DATA** currently residing on the USB drive you select. There is **NO UNDO** function. Data recovery after accidental formatting is often impossible.
>
> The most critical risk is selecting the **wrong target device**. Mistakenly choosing your computer's internal hard drive (e.g., `/dev/sda`, `/dev/nvme0n1`) instead of the intended USB drive (e.g., `/dev/sdb`, `/dev/sdc`) **WILL RESULT IN CATASTROPHIC AND LIKELY IRRECOVERABLE LOSS OF YOUR OPERATING SYSTEM, APPLICATIONS, AND PERSONAL FILES.**
>
> You **MUST** verify the target device name multiple times using different commands (like `lsblk`, `fdisk`, `parted`) and cross-reference with expected drive sizes and models before executing any partitioning or formatting commands. Proceed with extreme vigilance, double-checking each step, entirely at your own sole risk!

---

## Primary Drawbacks & Warnings (Reiterated & Expanded):

* **Highly Non-Standard & Complex:** Deviates significantly from Sbnb's design. Setup is intricate, runtime behavior depends on precise script execution and timing. Future Sbnb updates might break this.
* **Severe Performance Penalty:** USB storage is inherently slow (latency, throughput, IOPS) compared to internal NVMe/SATA drives. Disk I/O to `/mnt/sbnb-data` will be a major bottleneck.
* **Drastically Reduced Lifespan & Reliability:** USB flash drives will wear out quickly under persistent write load due to limited write cycles, write amplification, and lack of TRIM support. Unsuitable for write-intensive workloads or high reliability needs. Expect eventual failure and data loss without robust backups.
* **Potential Instability & Boot Issues:** Relies on correct partition detection, udev node creation, filesystem integrity, and `sbnb-cmds.sh` execution timing. Failures can leave persistent storage unavailable.

### When Might This Be Considered? (Limited Scenarios with Full Risk Acceptance)

* **Temporary Testing/Experimentation ONLY:** Brief evaluations on hardware lacking internal drives.
* **Specific, Very Low-Intensity, Read-Mostly Use Cases:** Infrequent writes, performance irrelevant (e.g., static config kiosk).
* **Absolute Hardware Constraints:** Sealed systems where internal drives are impossible, and risks are fully accepted.

*Even in these limited scenarios, regular, automated, and verified backups are non-negotiable.*

## Prerequisites

* **A Suitable USB Flash Drive:**
    * **Capacity:** Min ~1GB ESP + desired data size (32GB+ recommended).
    * **Quality & Speed:** Reputable brand, USB 3.0+ advised for marginal speed benefit. Endurance matters more than peak speed.
* **A Working Linux System (Preparation Environment):**
    * **Necessity:** Required for partitioning/formatting the target USB safely. openSUSE Tumbleweed assumed.
    * **Live Environment Benefit:** Using a Live USB/CD (e.g., openSUSE Tumbleweed Live) is highly recommended as it provides a non-destructive environment.
* **Sbnb Linux Boot File (`sbnb.efi`):**
    * **Method 1 (Easier):** Run official Sbnb install script on a temporary USB, then copy `/EFI/BOOT/BOOTX64.EFI` from its ESP.
    * **Method 2 (Advanced):** Build Sbnb from source, find `sbnb.efi` in `output/images/`.
* **Root/Sudo Privileges:** Needed on the openSUSE prep system for disk commands.
* **Internet Connection:** May be needed for `zypper`.

## Step-by-Step Instructions

*(Reminder: TRIPLE-CHECK your target device name, e.g., `/dev/sdX`, before every destructive command!)*

### Phase 1: Prepare the Linux Environment (openSUSE Tumbleweed)

1.  **Boot into openSUSE:** Start your preparation environment.
2.  **Install Necessary Tools:** Open a terminal. `zypper refresh` updates package lists. `zypper install` installs tools.
    ```bash
    sudo zypper refresh
    sudo zypper install -y parted lvm2 dosfstools e2fsprogs
    ```
3.  **Identify Target USB Drive:** **CRITICAL SAFETY STEP!** Unplug other USB storage.
    * Insert the target USB drive.
    * Use multiple commands. Compare SIZE and MODEL. Check `dmesg | tail` after plugging in for kernel messages like `sd 2:0:0:0: [sdc] Attached SCSI removable disk`.
    ```bash
    lsblk -d -o NAME,SIZE,MODEL,VENDOR,TYPE | grep 'disk'
    sudo fdisk -l | grep '^Disk /dev/'
    sudo parted -l | grep '^Disk /dev/'
    # Example: If consistently identified as /dev/sdc, use /dev/sdc below.
    ```
    * Visually confirm with YaST Partitioner (`sudo yast2 partitioner`) or GParted (`sudo zypper install -y gparted && sudo gparted`) if preferred. Look for the drive matching the expected size and vendor/model.
    * Assume `/dev/sdX` is your verified target drive. **Replace it carefully!**

### Phase 2: Partition the USB Drive

**(Warning: The following `parted` commands are DESTRUCTIVE to `/dev/sdX`. Double-check the device name!)**
```bash
#!/bin/bash

# --- Configuration ---
# Exit immediately if a command exits with a non-zero status.
# Treat unset variables as an error when substituting.
# Pipelines return the exit status of the last command to exit non-zero.
set -euo pipefail

# --- Variables ---
# EFI System Partition (ESP) Label (CRITICAL - must match bootloader config)
ESP_LABEL="sbnb"
# Data Partition Label (Recommended for identification)
DATA_LABEL="SBNB_DATA"
# ESP Size (Adjust if needed, ~1GB is usually sufficient)
ESP_SIZE="1025MiB"
# List of required commands for the script to function
REQUIRED_CMDS=(
    "parted" "mkfs.vfat" "mkfs.ext4" "wipefs" "findmnt" "lsblk"
    "blkid" "fsck.vfat" "e2fsck" "sync" "id" "grep" "read"
    "sleep" "xargs" "umount" "partprobe" "realpath"
)

# --- Functions ---
# Function to check for required commands
check_dependencies() {
    echo "--- Checking for required commands ---"
    local missing_cmds=()
    for cmd in "${REQUIRED_CMDS[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            missing_cmds+=("$cmd")
        fi
    done

    if [ ${#missing_cmds[@]} -ne 0 ]; then
        echo "ERROR: The following required commands are not found:" >&2
        printf " - %s\n" "${missing_cmds[@]}" >&2
        echo "Please install them and try again." >&2
        exit 1
    fi
    echo "All required commands found."
}

# Function to get the base block device for a given path (handles partitions, links, etc.)
get_base_device() {
    local path="$1"
    local resolved_path
    resolved_path=$(realpath "$path") || { echo "ERROR: Cannot resolve path '$path'" >&2; return 1; }
    # lsblk -no pkname gets the parent kernel name (base device)
    lsblk -no pkname "$resolved_path" || { echo "ERROR: Cannot find base device for '$resolved_path' using lsblk." >&2; return 1; }
}

# --- Script Start ---
echo "-----------------------------------------------------"
echo "--- USB Drive Partitioning and Formatting Script ---"
echo "---          (Version 2 - Enhanced Safety)       ---"
echo "-----------------------------------------------------"
echo ""
echo "WARNING: This script is DESTRUCTIVE and will ERASE"
echo "         ALL DATA on the target device."
echo ""

# --- Check for Root Privileges ---
if [ "$(id -u)" -ne 0 ]; then
  echo "ERROR: This script must be run as root (e.g., using sudo)." >&2
  exit 1
fi

# --- Check Dependencies ---
check_dependencies

# --- Check for Device Argument ---
if [ -z "${1:-}" ]; then
  echo "Usage: $0 /dev/sdX"
  echo "ERROR: Please provide the target block device (e.g., /dev/sda, /dev/sdb)." >&2
  echo ""
  echo "Available block devices (excluding ROM, loop, and RAM devices):"
  lsblk -d -o NAME,SIZE,TYPE,MODEL | grep -vE 'rom|loop|ram'
  exit 1
fi

DEVICE="$1"

# --- Validate Device ---
if [ ! -b "$DEVICE" ]; then
  echo "ERROR: '$DEVICE' is not a valid block device." >&2
  exit 1
fi

# --- CRITICAL SAFETY CHECK: Prevent targeting the root filesystem device ---
echo "--- Performing safety checks ---"
ROOT_DEV_PATH=$(findmnt -n -o SOURCE /)
ROOT_BASE_DEV_NAME=$(get_base_device "$ROOT_DEV_PATH") || exit 1 # Exit if function fails
TARGET_BASE_DEV_NAME=$(get_base_device "$DEVICE") || exit 1

# Construct full device paths for comparison
ROOT_BASE_DEV="/dev/${ROOT_BASE_DEV_NAME}"
TARGET_BASE_DEV="/dev/${TARGET_BASE_DEV_NAME}" # Assumes the input $DEVICE is the base device

if [ "$TARGET_BASE_DEV" == "$ROOT_BASE_DEV" ]; then
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" >&2
    echo "FATAL ERROR: Target device '$DEVICE' appears to be the same" >&2
    echo "             device ('$ROOT_BASE_DEV') as the running root" >&2
    echo "             filesystem ('$ROOT_DEV_PATH')." >&2
    echo "             Aborting to prevent data loss." >&2
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" >&2
    exit 1
fi
echo "Safety check passed: Target device '$DEVICE' is not the root filesystem device ('$ROOT_BASE_DEV')."

# Check if the device looks like an SD card reader often used for the OS drive
if [[ "$DEVICE" == /dev/mmcblk* ]]; then
    echo "WARNING: '$DEVICE' looks like an SD card (e.g., /dev/mmcblk0)."
    echo "         Double-check this is not your primary OS drive!"
fi


# --- Confirmation ---
echo ""
echo "Target Device: $DEVICE"
echo "Partitions to be created:"
echo "  1: EFI System Partition (ESP), FAT32, Label: '$ESP_LABEL', Size: $ESP_SIZE, Flags: boot, esp"
echo "  2: Linux Data Partition, ext4, Label: '$DATA_LABEL', Size: Remaining space"
echo ""
read -p "ARE YOU ABSOLUTELY SURE you want to erase '$DEVICE' and proceed? (yes/NO): " CONFIRMATION
CONFIRMATION=${CONFIRMATION:-NO} # Default to NO if user just presses Enter

if [[ "$CONFIRMATION" != "yes" ]]; then
  echo "Operation cancelled by user."
  exit 0
fi

echo ""
echo "--- Proceeding with operations on $DEVICE ---"

# --- Phase 2: Partition the USB Drive ---

# 1. Unmount Existing Partitions
echo ""
echo "--- Unmounting any existing partitions on ${DEVICE}* ---"
# Use findmnt to get mount points and umount them safely
# Also try to unmount the base device itself in case it's loop-mounted etc.
findmnt -n -o TARGET --source "${DEVICE}*" | xargs --no-run-if-empty umount -v -l || echo "Info: No partitions were mounted or umount failed (might be okay)."
umount "$DEVICE" &>/dev/null || true # Attempt to unmount base device, ignore errors
sleep 1 # Give time for umount to settle
lsblk "$DEVICE"

# 2. Wipe Existing Signatures (Recommended)
echo ""
echo "--- Wiping filesystem/partition signatures from $DEVICE ---"
wipefs --all --force "$DEVICE"
sync # Flush kernel buffers to disk to ensure changes are physically written

# 3. Create New GPT Partition Table
echo ""
echo "--- Creating new GPT partition table on $DEVICE ---"
parted "$DEVICE" --script -- mklabel gpt
sync # Flush kernel buffers to disk

# 4. Create EFI System Partition (ESP)
echo ""
echo "--- Creating ESP partition (1) on $DEVICE ---"
parted "$DEVICE" --script -- mkpart "${ESP_LABEL}" fat32 1MiB "${ESP_SIZE}"
parted "$DEVICE" --script -- set 1 boot on
parted "$DEVICE" --script -- set 1 esp on
sync # Flush kernel buffers to disk

# 5. Create Linux Data Partition
echo ""
echo "--- Creating Linux data partition (2) on $DEVICE ---"
# Use the end of the ESP as the start for the data partition
parted "$DEVICE" --script -- mkpart "${DATA_LABEL}" ext4 "${ESP_SIZE}" 100%
sync # Flush kernel buffers to disk
echo "Waiting briefly for kernel to recognize new partitions..."
sleep 2

# Define partition variables (assuming standard naming, e.g., /dev/sda1, /dev/sda2)
# Adding 'p' for NVMe devices (e.g., /dev/nvme0n1p1) - check if base device name contains 'nvme'
if [[ "$DEVICE" == *nvme* ]]; then
    PART_PREFIX="p"
else
    PART_PREFIX=""
fi
ESP_PARTITION="${DEVICE}${PART_PREFIX}1"
DATA_PARTITION="${DEVICE}${PART_PREFIX}2"

# Check if partition devices exist, retry with partprobe if needed
echo "--- Checking for partition device nodes (${ESP_PARTITION}, ${DATA_PARTITION}) ---"
PARTITIONS_FOUND=false
for i in {1..5}; do
    if [ -b "$ESP_PARTITION" ] && [ -b "$DATA_PARTITION" ]; then
        echo "Partition nodes found."
        PARTITIONS_FOUND=true
        break
    fi
    echo "Partition nodes not yet found. Retrying probe (Attempt $i/5)..."
    partprobe "$DEVICE" || echo "Warning: partprobe command failed, continuing check..."
    sleep 1
done

if [ "$PARTITIONS_FOUND" = false ]; then
    echo "ERROR: Partition devices ($ESP_PARTITION, $DATA_PARTITION) not found after partitioning and retries." >&2
    echo "       Please check manually ('lsblk $DEVICE', 'parted $DEVICE print')." >&2
    lsblk "$DEVICE"
    exit 1
fi

# 6. Verify Partitioning
echo ""
echo "--- Verifying partitions on $DEVICE ---"
parted "$DEVICE" --script -- print
echo ""
echo "--- Block device view: ---"
lsblk -o NAME,SIZE,TYPE,FSTYPE,PARTLABEL,MOUNTPOINT,PARTFLAGS "$DEVICE"
echo "----------------------------"
echo "Expected: ${ESP_PARTITION} (~${ESP_SIZE}), Type EFI System, Flags: boot, esp"
echo "Expected: ${DATA_PARTITION} (Remaining size), Type Linux filesystem"
echo "----------------------------"
sleep 2 # Pause for user to review


# --- Phase 3: Format Filesystems ---

# 1. Format EFI Partition
echo ""
echo "--- Formatting ESP partition (${ESP_PARTITION}) as FAT32 with label '${ESP_LABEL}' ---"
mkfs.vfat -F 32 -n "${ESP_LABEL}" "${ESP_PARTITION}"
sync # Flush kernel buffers to disk

# Check filesystem integrity
echo "--- Checking ESP filesystem (fsck.vfat) ---"
FSCK_VFAT_EXIT_CODE=0
fsck.vfat -a "${ESP_PARTITION}" || FSCK_VFAT_EXIT_CODE=$? # Run fsck, capture exit code on failure

if [ $FSCK_VFAT_EXIT_CODE -eq 0 ]; then
  echo "ESP filesystem check passed (or no check performed)."
elif [ $FSCK_VFAT_EXIT_CODE -eq 1 ]; then
  # Exit code 1 usually means errors were found AND corrected.
  echo "WARNING: fsck.vfat found and corrected errors on ESP partition (${ESP_PARTITION}). Check output above."
else
  # Exit codes > 1 typically indicate uncorrected errors.
  echo "ERROR: fsck.vfat reported uncorrectable errors (Exit Code: $FSCK_VFAT_EXIT_CODE) on ESP partition (${ESP_PARTITION})." >&2
  echo "       Cannot proceed safely. Please investigate manually." >&2
  exit 1
fi

# Verify label using blkid
echo "--- Verifying ESP label ---"
if blkid -s LABEL -o value "${ESP_PARTITION}" | grep -q "^${ESP_LABEL}$"; then
    echo "ESP Label '${ESP_LABEL}' verified successfully on ${ESP_PARTITION}."
else
    echo "ERROR: Failed to verify ESP Label '${ESP_LABEL}' on ${ESP_PARTITION}." >&2
    blkid "${ESP_PARTITION}" # Show full blkid output for debugging
    exit 1
fi

# 2. Format Data Partition
echo ""
echo "--- Formatting Data partition (${DATA_PARTITION}) as ext4 with label '${DATA_LABEL}' ---"
mkfs.ext4 -m 0 -L "${DATA_LABEL}" "${DATA_PARTITION}"
sync # Flush kernel buffers to disk

# Check the new ext4 filesystem integrity
echo "--- Checking Data partition filesystem (e2fsck) ---"
# -f forces check even if clean, -y assumes yes to all prompts (use with caution)
E2FSCK_EXIT_CODE=0
e2fsck -f -y "${DATA_PARTITION}" || E2FSCK_EXIT_CODE=$? # Capture exit code on failure

if [ $E2FSCK_EXIT_CODE -eq 0 ]; then
    echo "Data partition filesystem check passed."
elif [ $E2FSCK_EXIT_CODE -eq 1 ]; then
    # Exit code 1 means errors were corrected.
    echo "WARNING: e2fsck found and corrected errors on Data partition (${DATA_PARTITION}). Check output above."
else
    # Exit codes > 1 indicate uncorrected errors.
    echo "ERROR: e2fsck reported uncorrectable errors (Exit Code: $E2FSCK_EXIT_CODE) on Data partition (${DATA_PARTITION})." >&2
    echo "       Cannot proceed safely. Please investigate manually." >&2
    exit 1
fi

# Verify the label using blkid
echo "--- Verifying Data partition label ---"
if blkid -s LABEL -o value "${DATA_PARTITION}" | grep -q "^${DATA_LABEL}$"; then
    echo "Data Label '${DATA_LABEL}' verified successfully on ${DATA_PARTITION}."
else
    echo "ERROR: Failed to verify Data Label '${DATA_LABEL}' on ${DATA_PARTITION}." >&2
    blkid "${DATA_PARTITION}" # Show full blkid output for debugging
    exit 1
fi

echo ""
echo "-----------------------------------------------------"
echo "--- Script finished successfully! ---"
echo "Device: $DEVICE"
echo "Partitions created and formatted:"
lsblk -o NAME,SIZE,TYPE,FSTYPE,LABEL,PARTLABEL,MOUNTPOINT "$DEVICE"
echo "-----------------------------------------------------"

exit 0
```

### Phase 4: Install Sbnb Boot Files and Configuration

1.  **Mount EFI Partition:** Access the ESP filesystem.
    ```bash
    echo "--- Mounting ESP partition ---"
    sudo mkdir -p /mnt/sbnb-mount
    sudo mount /dev/sdX1 /mnt/sbnb-mount
    ```
2.  **Create EFI Boot Directory:** Standard UEFI fallback path.
    ```bash
    echo "--- Creating EFI boot directories ---"
    sudo mkdir -p /mnt/sbnb-mount/EFI/BOOT
    ```
3.  **Copy Sbnb EFI Boot File:** Place the bootloader (`sbnb.efi` as `BOOTX64.EFI`).
    ```bash
    echo "--- Copying Sbnb EFI boot file ---"
    sudo cp sbnb.efi /mnt/sbnb-mount/EFI/BOOT/BOOTX64.EFI
    ```
4.  **(Recommended) Create Sbnb Configuration File:** Place `sbnb-tskey.txt` in ESP root (`/mnt/sbnb-mount/`). The `boot-sbnb.sh` script reads this to configure Tailscale.
    ```bash
    echo "--- Creating Sbnb configuration file (sbnb-tskey.txt) ---"
    echo "tskey-auth-..." | sudo tee /mnt/sbnb-mount/sbnb-tskey.txt > /dev/null
    ```
5.  **(Crucial) Handle Data Partition Mounting via `sbnb-cmds.sh`:**
    * **Context & Goal:** Sbnb boots -> systemd -> `sbnb.service` -> `boot-sbnb.sh` -> mounts ESP to `/mnt/sbnb` -> executes `/mnt/sbnb/sbnb-cmds.sh`. This script mounts the data partition (labeled `SBNB_DATA`) to `/mnt/sbnb-data`.
    * **Device Detection Timing:** There's a potential race: the kernel/udev might not have created the `/dev/disk/by-label/SBNB_DATA` symlink or the `/dev/sdX2` node exactly when the script runs. The wait loop mitigates this.
    * **Default Script Conflict Uncertainty:** The `boot-sbnb.sh` excerpt doesn't show conflicting actions at its execution point. However, other early boot mechanisms could exist in Sbnb. If `/mnt/sbnb-data` behaves unexpectedly, investigate potential early boot scripts/services related to storage in your Sbnb version (advanced).
    * **`sbnb-cmds.sh` Script (Wait Loop & Logging):** Create this in the ESP root (`/mnt/sbnb-mount/` during prep).
```bash
#!/bin/sh
# Custom sbnb-cmds.sh for USB Persistent Partition setup (No LVM)
# Mounts partition labeled DATA_LABEL to MOUNT_POINT after waiting for device.
# For debugging, uncomment 'set -x' to trace command execution.
# set -x

# Function to log messages consistently to kernel buffer (dmesg) and console (tty)
log_msg() {
  echo "sbnb-cmds.sh: $1" | tee /dev/kmsg
}

log_msg "--- Running Custom USB Partition Mount Script ---"

# --- Configuration ---
MOUNT_POINT="/mnt/sbnb-data"  # Target directory for persistent data
DATA_LABEL="SBNB_DATA"        # Filesystem label of the data partition (MUST match mkfs.ext4 -L)
# Alternative: Use UUID for potentially more stable identification if labels change/conflict
# Get UUID using 'sudo blkid /dev/sdX2' on prep machine, then set:
# DATA_UUID="YOUR-UUID-HERE"
MAX_WAIT_SECONDS=15           # Max time (seconds) to wait for the device node/label
WAIT_INTERVAL=1               # Check frequency (seconds)
MOUNT_OPTS="defaults,noatime,nodiratime" # Mount options (noatime/nodiratime reduce writes on flash)
# --- End Configuration ---

DATA_DEVICE=""                # Will hold the found device path

# --- Wait Loop for Device ---
# Attempts to find the device by label or UUID (if configured).
# Waits because device node creation by kernel/udev might be delayed.
elapsed_wait=0
log_msg "Waiting up to ${MAX_WAIT_SECONDS}s for device (Label: ${DATA_LABEL:-N/A})..."
while [ -z "$DATA_DEVICE" ] && [ $elapsed_wait -lt $MAX_WAIT_SECONDS ]; do
  # Check for device using the label symlink first (usually faster if udev ran)
  label_path="/dev/disk/by-label/${DATA_LABEL}"
  if [ -e "$label_path" ]; then
      # Readlink -f resolves the symlink to the actual device path (e.g., /dev/sdb2)
      DATA_DEVICE=$(readlink -f "$label_path")
      log_msg "Found device via label symlink: $label_path -> $DATA_DEVICE"
      break # Exit loop
  fi

  # Fallback: Use blkid command to scan for the label (can be slower)
  blkid_device=$(blkid -L "${DATA_LABEL}" 2>/dev/null)
  if [ -n "$blkid_device" ]; then
      DATA_DEVICE="$blkid_device"
      log_msg "Found device via blkid label lookup: $DATA_DEVICE"
      break # Exit loop
  fi

  # (Add similar checks here using DATA_UUID if using UUID instead of Label)

  # Device not found yet, wait before next check
  sleep $WAIT_INTERVAL
  elapsed_wait=$((elapsed_wait + WAIT_INTERVAL))
done

# --- Mount Logic ---
# Proceed only if a device path was successfully determined
if [ -n "$DATA_DEVICE" ] && [ -e "$DATA_DEVICE" ]; then
  log_msg "Data partition device resolved to ${DATA_DEVICE} after ${elapsed_wait}s."

  # Check if the target directory is already a mount point
  if ! mountpoint -q "$MOUNT_POINT"; then
    log_msg "Attempting to mount $DATA_DEVICE at $MOUNT_POINT with options: $MOUNT_OPTS..."
    # Ensure the target directory exists
    mkdir -p "$MOUNT_POINT"
    # Mount the device
    if mount -o "$MOUNT_OPTS" "$DATA_DEVICE" "$MOUNT_POINT"; then
      log_msg "Successfully mounted persistent partition at $MOUNT_POINT."
    else
      mount_exit_code=$?
      log_msg "ERROR: Failed to mount $DATA_DEVICE at $MOUNT_POINT (exit code: $mount_exit_code). Check filesystem type/integrity (run fsck?). See dmesg for details." >&2
    fi
  else
    # Mount point exists, verify if it's the correct device
    log_msg "$MOUNT_POINT is already a mount point. Checking device..."
    # Check /proc/mounts for the currently mounted device at MOUNT_POINT
    if grep -qs "$DATA_DEVICE $MOUNT_POINT" /proc/mounts; then
          log_msg "Persistent partition already correctly mounted at $MOUNT_POINT."
    else
          mounted_dev=$(grep -s "$MOUNT_POINT" /proc/mounts | awk '{print $1}')
          log_msg "ERROR: $MOUNT_POINT is already mounted, but by '$mounted_dev' NOT '$DATA_DEVICE'! Check system configuration." >&2
    fi
  fi
else
  # Device wasn't found within the timeout
  log_msg "ERROR: Data partition device (Label: ${DATA_LABEL:-N/A}) not found after waiting ${MAX_WAIT_SECONDS}s. Cannot mount persistent storage." >&2
fi

mkdir -p /etc/docker
cp /mnt/sbnb-data/docker/docker-daemon.json.template /etc/docker/daemon.json

log_msg "--- Finished Custom USB Partition Mount Script ---"
# Exit 0 ensures the rest of the Sbnb boot sequence continues
exit 0
```
    * Place script content into `/mnt/sbnb-mount/sbnb-cmds.sh`.
    * Make executable: `sudo chmod +x /mnt/sbnb-mount/sbnb-cmds.sh`.

6.  **Unmount the EFI Partition:**
    ```bash
    echo "--- Unmounting ESP partition ---"
    # Ensure buffers are flushed before unmounting
    sync
    sudo umount /mnt/sbnb-mount
    ```

### Phase 4.5: Backing Up Data (CRITICAL!)

* **Why Essential:** High risk of USB drive failure. Backups are mandatory.
* **Strategy:** Automate regular backups of `/mnt/sbnb-data`.
* **File Data Backup (`rsync`):** Ensure the backup destination (NAS, cloud, another server) has sufficient free space.
    ```bash
    # Example: From Sbnb to backup-server (requires ssh key auth)
    rsync -avz --delete --progress --human-readable /mnt/sbnb-data/ user@backup-server:/path/to/backups/sbnb-usb-data/
    ```
* **Frequency:** Daily recommended for active data.
* **Automation:** Use cron/systemd timers or remote triggers.
* **Testing Restores:** Vital! Don't assume backups work.
    * **Conceptual Restore:** Boot Linux Live env -> Mount backup source -> Mount target USB data partition (new/reformatted) to `/mnt/restore` -> `sudo rsync -av --progress /path/to/backup/sbnb-usb-data/ /mnt/restore/` -> Verify restored files (count, size, checksums, spot checks).
* **Verification:** Use tools like `diff -r`, `md5sum`, or `sha256sum` to compare restored files against originals or known good copies.
* *Untested backups provide a false sense of security.*

### Phase 5: Boot and Verify

1.  **Safely Eject:** Eject USB from prep system.
2.  **Configure Server BIOS/UEFI:** Enter setup (DEL, F2, F10, F12, etc.). Ensure UEFI Mode ON, CSM/Legacy OFF, Secure Boot OFF. Set "UEFI: USB..." as first boot device. Save & Exit.
3.  **Boot Sbnb Linux.**
4.  **Verify Operation:**
    * Monitor Boot: Watch console for `sbnb-cmds.sh` logs, errors.
    * SSH into Sbnb.
    * Check Mounts:
        ```bash
        lsblk -o NAME,SIZE,TYPE,FSTYPE,LABEL,MOUNTPOINT # Look for mount at /mnt/sbnb-data
        df -hT | grep -E 'Filesystem|/mnt/sbnb-data'     # Check usage/type
        mount | grep /mnt/sbnb-data                      # Check mount options (rw, noatime)
        findmnt /mnt/sbnb-data                           # Another way to check mount info
        ```
    * Test Persistence:
        ```bash
        # After SSHing in:
        TIMESTAMP=$(date)
        echo "Sbnb USB Persistence test - $TIMESTAMP" | sudo tee /mnt/sbnb-data/persistence_test.txt > /dev/null
        sync && echo "Synced data to disk."
        echo "File created. Content:" && sudo cat /mnt/sbnb-data/persistence_test.txt
        echo "Rebooting server now..." && sudo reboot

        # --- Wait for reboot and reconnect via SSH ---
        echo "Checking for file after reboot..."
        if [ -f /mnt/sbnb-data/persistence_test.txt ]; then
          echo "SUCCESS: File found. Content:" && sudo cat /mnt/sbnb-data/persistence_test.txt
          sudo rm /mnt/sbnb-data/persistence_test.txt # Clean up
        else
          echo "FAILURE: File NOT FOUND after reboot! Persistence failed."
        fi
        ```

## Troubleshooting

* **Doesn't Boot / No Bootable Device:**
    * Re-verify BIOS settings (UEFI, Secure Boot OFF, Boot Order).
    * Re-verify USB Prep: Partitions (`parted print`), ESP flags (`boot`,`esp`), ESP filesystem label (`blkid /dev/sdX1` -> `LABEL="sbnb"`), EFI file path (`/EFI/BOOT/BOOTX64.EFI`).
    * Try different USB ports (check if port provides sufficient power). Test drive health on prep machine (`fsck`, `badblocks -nvs /dev/sdX`). Recreate drive meticulously.
* **Data Partition Not Mounted / `/mnt/sbnb-data` Empty:**
    * Check boot logs (`journalctl -b`, console) for `sbnb-cmds.sh` errors ("Device... not found", "Failed to mount"). Check `dmesg` for USB errors (`dmesg | grep -iE 'usb|sdX'`) or filesystem errors (`dmesg | grep -i ext4`).
    * SSH in:
        * Verify partition & label: `sudo blkid`, `ls -l /dev/disk/by-label/`. Is `SBNB_DATA` present? Does it point to the correct device?
        * If label wrong/missing: Re-label from prep env (`sudo e2label /dev/sdX2 SBNB_DATA`).
        * If device/label exists, try manual mount: `sudo mkdir -p /mnt/sbnb-data && sudo mount /dev/disk/by-label/SBNB_DATA /mnt/sbnb-data`. Check `dmesg` for errors (e.g., `mount: wrong fs type, bad option, bad superblock`). If manual mount works, debug `sbnb-cmds.sh` (add `set -x`, check paths, loop duration, check script permissions `ls -l /mnt/sbnb/sbnb-cmds.sh`).
        * Run filesystem check (unmounted): `sudo e2fsck -f /dev/disk/by-label/SBNB_DATA`.
        * Check kernel modules: `lsmod | grep ext4`. Is the module loaded? Check `dmesg` for errors loading filesystem modules.
* **Poor Performance / Drive Failure:**
    * **Performance:** Inherent limitation.
    * **Lifespan/Failure:** Monitor `dmesg` for I/O errors. Restore from verified backups upon failure. This setup will wear out consumer flash drives with persistent writes.

## Final Recommendation

This guide details a complex, non-standard configuration fraught with performance and reliability risks. While it provides a technically feasible path for single-drive boot and persistence under specific constraints, users should strongly prefer the standard Sbnb architecture using reliable internal server storage whenever possible. Evaluate the trade-offs carefully before committing to this approach.
