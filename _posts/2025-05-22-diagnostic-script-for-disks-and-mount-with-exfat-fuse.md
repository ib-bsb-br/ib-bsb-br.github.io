---
tags: [scratchpad]
info: aberto.
date: 2025-05-22
type: post
layout: post
published: true
slug: diagnostic-script-for-disks-and-mount-with-exfat-fuse
title: 'Diagnostic script for disks and mount with `exfat-fuse`'
---
1.  **Install `exfat-fuse`:**
    ```bash
    sudo apt install exfat-fuse
    ```
2.  **Mount using FUSE:**
    *   **For root ownership:**
        ```bash
        sudo mount -t fuse.exfat -o uid=0,gid=0,rw,noatime,allow_other UUID="69AF-5F99" /mnt/my_external_hdd
        ```
        Or directly:
        ```bash
        sudo mount.exfat-fuse -o uid=0,gid=0,rw,noatime,allow_other /dev/sdb /mnt/my_external_hdd
        ```
    *   **For specific non-root user ownership (e.g., UID/GID 1000):**
        ```bash
        sudo mount -t fuse.exfat -o uid=1000,gid=1000,rw,noatime,allow_other UUID="69AF-5F99" /mnt/my_external_hdd
        ```
        Or directly:
        ```bash
        sudo mount.exfat-fuse -o uid=1000,gid=1000,rw,noatime,allow_other /dev/sdb /mnt/my_external_hdd
        ```
    *   `allow_other`: This FUSE-specific option is important if you want users other than the one who mounted the filesystem (in this case, root, even if `uid`/`gid` are set for appearance) to access it.

3.  **Unmounting FUSE filesystems:**
    To unmount a filesystem mounted with `exfat-fuse` (or `fuse.exfat`), you use:
    ```bash
    sudo fusermount -u /mnt/my_external_hdd
    ```

# Script to gather extensive diagnostic information about a specified disk device.

```bash
#!/bin/bash

# All outputs will be concatenated into a single text file.

# --- Configuration ---
DEVICE="/dev/sdb"
OUTPUT_FILE="/home/linaro/sdb.txt"
TESTDISK_CWD_LOG_FILE="testdisk.log" # TestDisk creates this in the Current Working Directory

# --- Pre-flight Checks ---

# Ensure the script is executed with root privileges
if [ "$(id -u)" -ne 0 ]; then
  echo "This script requires root privileges to access raw disk devices." >&2
  echo "Please run it using sudo: sudo $0" >&2
  exit 1
fi

# Initialize the output file (do this before device check so errors can be logged to it)
echo "Disk Diagnostics for $DEVICE - Report generated on $(date)" > "$OUTPUT_FILE"
echo "========================================================================" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Verify that the specified device exists and is a block device
if [ ! -b "$DEVICE" ]; then
    echo "Error: The device $DEVICE does not exist or is not a block device." | tee -a "$OUTPUT_FILE" >&2
    exit 1
fi

# --- Helper Function ---

# Function to execute a command, log its output/errors, and check its exit status
run_and_log() {
  local description="$1"
  local command_to_run="$2"
  local tool_name="${3:-}" # Optional: simple name of the tool for 'command -v' check

  echo "Executing: $description" # Console feedback

  # If a tool name is provided, check if it's installed
  if [ -n "$tool_name" ]; then
    if ! command -v "$tool_name" &> /dev/null; then
      echo "------------------------------------------------------------------------" >> "$OUTPUT_FILE"
      echo "Command: $command_to_run (SKIPPED)" >> "$OUTPUT_FILE"
      echo "Warning: Tool '$tool_name' not found. Please install it and try again." >> "$OUTPUT_FILE"
      echo "Skipping: $description (tool '$tool_name' not found)"
      echo "------------------------------------------------------------------------" >> "$OUTPUT_FILE"
      echo "" >> "$OUTPUT_FILE"
      return
    fi
  fi
  
  echo "------------------------------------------------------------------------" >> "$OUTPUT_FILE"
  echo "Command: $command_to_run" >> "$OUTPUT_FILE"
  echo "Output:" >> "$OUTPUT_FILE"
  
  # Using eval to correctly handle commands with pipes, redirections, and other shell constructs
  # This is generally safe when command_to_run strings are hardcoded within the script.
  eval "$command_to_run" >> "$OUTPUT_FILE" 2>&1
  local exit_status=$?
  
  if [ $exit_status -ne 0 ]; then
    echo "" >> "$OUTPUT_FILE" # Ensure warning is on a new line if command produced output
    echo "Warning: Command exited with status $exit_status." >> "$OUTPUT_FILE"
  fi
  
  echo "" >> "$OUTPUT_FILE"
  echo "------------------------------------------------------------------------" >> "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"
}

# --- Script Main Body ---

echo "Starting diagnostic data collection for $DEVICE."
echo "All output will be directed to $OUTPUT_FILE."
echo "Please note: Some operations may take a significant amount of time."
echo ""

# --- Section 1: Core Investigation Tools ---
echo ">>> Section: Core Investigation Tools <<<" >> "$OUTPUT_FILE"; echo "" >> "$OUTPUT_FILE"

run_and_log "fdisk -l (List partition table)" "fdisk -l $DEVICE" "fdisk"
run_and_log "parted print (Display detailed partition information)" "parted -s $DEVICE print" "parted"
run_and_log "sfdisk -d (Dump partition table structure)" "sfdisk -d $DEVICE" "sfdisk"
run_and_log "sfdisk --verify (Verify partition table consistency)" "sfdisk --verify $DEVICE" "sfdisk"
run_and_log "blkid $DEVICE (Show block device attributes for $DEVICE)" "blkid $DEVICE" "blkid"
run_and_log "blkid (Show block device attributes for all devices - for context)" "blkid" "blkid"
run_and_log "file -s $DEVICE (Determine data type/filesystem signature of $DEVICE)" "file -s $DEVICE" "file"
run_and_log "lsblk -f $DEVICE (List block devices with filesystem info for $DEVICE)" "lsblk -f $DEVICE" "lsblk"

# --- Section 2: Disk Health and Low-Level Analysis Tools ---
echo ">>> Section: Disk Health and Low-Level Analysis Tools <<<" >> "$OUTPUT_FILE"; echo "" >> "$OUTPUT_FILE"

echo "Note: For 'smartctl', the 'smartmontools' package is typically required." | tee -a "$OUTPUT_FILE"
run_and_log "smartctl -a (S.M.A.R.T. health data)" "smartctl -a $DEVICE" "smartctl"

run_and_log "dd + hexdump (Inspect first 512 bytes - MBR area)" "dd if=$DEVICE bs=512 count=1 | hexdump -C" "dd" # hexdump is part of bsdmainutils or similar
# Reduced count for strings scan to 10MB to keep script execution time reasonable
run_and_log "dd + strings (Scan first 10MB for printable strings)" "dd if=$DEVICE bs=1M count=10 status=none | strings" "dd" # strings is part of binutils

echo "Note: For 'gdisk', the 'gdisk' package is typically required." | tee -a "$OUTPUT_FILE"
run_and_log "gdisk -l (GPT partition table list - also checks MBR)" "gdisk -l $DEVICE" "gdisk"

# --- Section 3: Filesystem-Specific and Recovery-Oriented Tools ---
echo ">>> Section: Filesystem-Specific and Recovery-Oriented Tools <<<" >> "$OUTPUT_FILE"; echo "" >> "$OUTPUT_FILE"

echo "Note: For 'gpart', the 'gpart' package is typically required." | tee -a "$OUTPUT_FILE"
run_and_log "gpart (Attempt to guess PC-type hard disk partitions)" "gpart $DEVICE" "gpart"

echo "Note: For 'mmls', the 'sleuthkit' package is typically required." | tee -a "$OUTPUT_FILE"
run_and_log "mmls (Display partition layout using The Sleuth Kit)" "mmls $DEVICE" "mmls"

# --- Section 4: TestDisk Logging ---
echo ">>> Section: TestDisk Logging <<<" >> "$OUTPUT_FILE"; echo "" >> "$OUTPUT_FILE"
echo "Note: For 'testdisk', the 'testdisk' package is typically required." | tee -a "$OUTPUT_FILE"
echo "Attempting to run TestDisk with logging to capture initial analysis..." | tee -a "$OUTPUT_FILE"
echo "TestDisk will create '$TESTDISK_CWD_LOG_FILE' in the current working directory: $(pwd)" | tee -a "$OUTPUT_FILE"

# Remove old log file if it exists to ensure a fresh log for this run
rm -f "$TESTDISK_CWD_LOG_FILE"

# Check if testdisk command exists before trying to run
if command -v testdisk &> /dev/null; then
    echo "------------------------------------------------------------------------" >> "$OUTPUT_FILE"
    echo "Command: testdisk /debug /log $DEVICE" >> "$OUTPUT_FILE"
    echo "Output (TestDisk's own log '$TESTDISK_CWD_LOG_FILE' will be appended below if created):" >> "$OUTPUT_FILE"
    
    # Run TestDisk. It should perform analysis, log to its file, and exit.
    # Suppress its direct stdout/stderr as the primary log data goes to its own file.
    testdisk /debug /log $DEVICE > /dev/null 2>&1
    testdisk_exit_status=$?

    if [ $testdisk_exit_status -ne 0 ]; then
        echo "Warning: TestDisk command may not have completed successfully (exit status: $testdisk_exit_status)." >> "$OUTPUT_FILE"
    fi

    if [ -f "$TESTDISK_CWD_LOG_FILE" ]; then
      echo "" >> "$OUTPUT_FILE"
      echo "Appending content of $TESTDISK_CWD_LOG_FILE (created by TestDisk):" >> "$OUTPUT_FILE"
      cat "$TESTDISK_CWD_LOG_FILE" >> "$OUTPUT_FILE"
      echo "" >> "$OUTPUT_FILE"
      echo "Temporary log file '$TESTDISK_CWD_LOG_FILE' has been appended and will now be removed." | tee -a "$OUTPUT_FILE" # Also to console
      rm "$TESTDISK_CWD_LOG_FILE"
    else
      echo "Warning: TestDisk log file ('$TESTDISK_CWD_LOG_FILE') was not found in the current directory after execution." >> "$OUTPUT_FILE"
      echo "TestDisk may not have run as expected or created the log file." >> "$OUTPUT_FILE"
    fi
    echo "------------------------------------------------------------------------" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
else
    echo "------------------------------------------------------------------------" >> "$OUTPUT_FILE"
    echo "Command: testdisk /debug /log $DEVICE (SKIPPED)" >> "$OUTPUT_FILE"
    echo "Warning: Tool 'testdisk' not found. Please install it and try again." >> "$OUTPUT_FILE"
    echo "Skipping: TestDisk logging (tool 'testdisk' not found)"
    echo "------------------------------------------------------------------------" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
fi

# --- Section 5: Kernel Messages ---
echo ">>> Section: Kernel Messages (dmesg) <<<" >> "$OUTPUT_FILE"; echo "" >> "$OUTPUT_FILE"
# Construct a grep pattern to match the base device name (e.g., sdb) and the full path (e.g., /dev/sdb)
# This helps capture messages that might refer to the disk in different ways.
DEVICE_BASENAME=$(basename "$DEVICE")
run_and_log "dmesg (Kernel messages related to $DEVICE)" \
            "dmesg | grep -Ei --binary-files=text \"($DEVICE_BASENAME|$DEVICE)\" || echo 'No specific dmesg entries found for $DEVICE or $DEVICE_BASENAME'" \
            "dmesg" # grep is usually available

# --- Completion ---
echo "" | tee -a "$OUTPUT_FILE" # Final blank line in file for spacing
echo "Diagnostic script for $DEVICE has completed." | tee -a "$OUTPUT_FILE"
echo "All collected information has been saved to: $OUTPUT_FILE" | tee -a "$OUTPUT_FILE"
echo "Please review the contents of this file carefully."

exit 0
```