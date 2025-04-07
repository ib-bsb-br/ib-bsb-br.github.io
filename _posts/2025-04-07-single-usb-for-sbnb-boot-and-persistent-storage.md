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
# Goal: Single USB for Sbnb Boot and Persistent Storage

This guide is for advanced users who want to run Sbnb Linux from a single USB drive with persistent storage. It details the process of partitioning and formatting the drive, and setting up the necessary boot files and scripts.

This guide provides comprehensive, step-by-step instructions for configuring a single USB flash drive (or potentially an external USB hard drive) to perform two distinct functions simultaneously:

1.  **Booting the Sbnb Linux Operating System:** The drive will be prepared with a standard UEFI-compatible structure, specifically an EFI System Partition (ESP) containing the Sbnb EFI bootloader (`sbnb.efi`) and necessary configuration files. This allows the server's firmware to locate and start the Sbnb boot process. The `sbnb.efi` file itself is typically a Unified Kernel Image (UKI), bundling the Linux kernel, initramfs, and kernel command line into a single executable file.
2.  **Providing Simple Persistent Storage:** Utilizing a separate partition on the same physical USB drive, formatted with a standard Linux filesystem (`ext4` is used in this guide). This partition is intended to be automatically mounted at the `/mnt/sbnb-data` directory path within the running Sbnb Linux system via a custom boot script (`sbnb-cmds.sh`). This provides a space where data (like container volumes, application data, logs, user files) can persist across reboots of the otherwise ephemeral, RAM-based Sbnb OS.

**Important Note on Sbnb Version:** This guide is based on analysis of the Sbnb GitHub repository content provided previously. If you are using a significantly different version of Sbnb Linux, the boot process, script names, expected labels, or available tools might differ. Always consult the documentation specific to your Sbnb version if available, and be prepared to adapt these steps.

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

1.  **Unmount Existing Partitions:**
    ```bash
    echo "--- Unmounting any partitions on /dev/sdX ---"
    findmnt -n -o TARGET --source /dev/sdX* | xargs --no-run-if-empty sudo umount -v -l
    lsblk /dev/sdX
    ```
2.  **Wipe Existing Signatures (Recommended):**
    ```bash
    echo "--- Wiping signatures from /dev/sdX ---"
    sudo wipefs --all --force /dev/sdX
    ```
3.  **Create New GPT Partition Table:** Needed for UEFI and modern features.
    ```bash
    echo "--- Creating new GPT label on /dev/sdX ---"
    sudo parted /dev/sdX --script -- mklabel gpt
    ```
4.  **Create EFI System Partition (ESP):** FAT32, ~1GB. The UEFI firmware identifies this via the `boot` and `esp` flags to find bootloaders.
    ```bash
    echo "--- Creating ESP partition (1) on /dev/sdX ---"
    sudo parted /dev/sdX --script -- mkpart "sbnb-esp" fat32 1MiB 1025MiB
    sudo parted /dev/sdX --script -- set 1 boot on
    sudo parted /dev/sdX --script -- set 1 esp on
    ```
5.  **Create Linux Data Partition:** Uses remaining space. Standard Linux filesystem type (ID `8300`).
    ```bash
    echo "--- Creating Linux data partition (2) on /dev/sdX ---"
    sudo parted /dev/sdX --script -- mkpart "sbnb-data" ext4 1025MiB 100%
    ```
6.  **Verify Partitioning:** Check layout, types, flags, sizes.
    ```bash
    echo "--- Verifying partitions on /dev/sdX ---"
    sudo parted /dev/sdX --script -- print
    echo "--- Block device view: ---"
    lsblk -o NAME,SIZE,TYPE,FSTYPE,PARTLABEL,MOUNTPOINT,PARTFLAGS /dev/sdX
    # Expect /dev/sdX1: ~1G, Type EFI System, PARTFLAGS includes 'boot', 'esp'
    # Expect /dev/sdX2: remaining size, Type Linux
    # Graphical tools should show a small FAT32 partition flagged boot/esp, and a larger second partition.
    ```

### Phase 3: Format Filesystems

1.  **Format EFI Partition (with `sbnb` label):** **CRITICAL LABEL!** `mkfs.vfat` creates FAT32. `-n sbnb` sets the label checked by `boot-sbnb.sh`.
    ```bash
    echo "--- Formatting ESP partition (/dev/sdX1) as FAT32 with label 'sbnb' ---"
    sudo mkfs.vfat -F 32 -n sbnb /dev/sdX1
    # (Optional but recommended) Check filesystem integrity before use.
    echo "--- Checking ESP filesystem (fsck.vfat) ---"
    sudo fsck.vfat -a /dev/sdX1
    # Check fsck exit code (0 = OK, non-zero = errors found/uncorrected)
    if [ $? -ne 0 ]; then echo "WARNING: fsck found errors on ESP partition!"; fi
    # Verify label using blkid (reads filesystem metadata)
    echo "--- Verifying ESP label ---"
    sudo blkid /dev/sdX1 # Output MUST include LABEL="sbnb"
    ```
2.  **Format Data Partition:** `mkfs.ext4` creates ext4. `-L DATA_LABEL` aids identification. `-m 0` maximizes space. Ext4 journaling helps data integrity on unclean shutdown. (Note: F2FS is another option sometimes recommended for flash, but requires Sbnb kernel/tools support and different `mkfs.f2fs` command).
    ```bash
    DATA_PARTITION="/dev/sdX2"
    DATA_LABEL="SBNB_DATA"
    echo "--- Formatting Data partition (${DATA_PARTITION}) as ext4 with label '${DATA_LABEL}' ---"
    sudo mkfs.ext4 -m 0 -L ${DATA_LABEL} ${DATA_PARTITION}
    # (Optional but recommended) Check the new ext4 filesystem integrity.
    echo "--- Checking Data partition filesystem (e2fsck) ---"
    sudo e2fsck -f -y ${DATA_PARTITION} # -f forces check, -y assumes yes
    if [ $? -ne 0 ]; then echo "WARNING: e2fsck found errors on Data partition!"; fi
    # Verify the label using blkid
    echo "--- Verifying Data partition label ---"
    sudo blkid ${DATA_PARTITION} # Output should include LABEL="SBNB_DATA" and TYPE="ext4"
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
    echo "SBNB_TAILSCALE_KEY=tskey-auth-..." | sudo tee /mnt/sbnb-mount/sbnb-tskey.txt > /dev/null
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
        * If device/label exists, try manual mount: `sudo mkdir -p /mnt/sbnb-data && sudo mount /dev/disk/by-label/SBNB_DATA /mnt/sbnb-data`. Check `dmesg` for
