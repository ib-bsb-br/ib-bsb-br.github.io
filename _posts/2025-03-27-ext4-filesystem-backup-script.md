---
tags: [scratchpad]
info: aberto.
date: 2025-03-27
type: post
layout: post
published: true
slug: ext4-filesystem-backup-script
title: 'ext4 filesystem backup script'
---
```bash
#!/bin/bash
set -e  # Exit on any error

# Configuration
DATE=$(date +%Y-%m-%d)
BACKUP_DEVICE="/dev/sda1"  # Change to your external drive
MOUNT_POINT="/mnt/backup"
BACKUP_DIR="$MOUNT_POINT/opensuse_backups/$DATE"
LOG_FILE="/var/log/opensuse-backup.log"
RETENTION_COUNT=4  # Number of backups to keep

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Redirect all output to log and console
exec > >(tee -a "$LOG_FILE") 2>&1
echo "===== Backup started at $(date) ====="

# Check if backup device exists
if [ ! -b "$BACKUP_DEVICE" ]; then
    echo "ERROR: Backup device $BACKUP_DEVICE not found"
    exit 1
fi

# Create mount point if needed
mkdir -p "$MOUNT_POINT"

# Check if already mounted
if ! mountpoint -q "$MOUNT_POINT"; then
    echo "Mounting backup device..."
    mount "$BACKUP_DEVICE" "$MOUNT_POINT" || {
        echo "ERROR: Failed to mount backup device"
        exit 1
    }
    MOUNTED=true
else
    echo "Backup device already mounted"
    MOUNTED=false
fi

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Check available space (need at least 10GB free)
AVAILABLE_SPACE=$(df -BG "$MOUNT_POINT" | awk 'NR==2 {print $4}' | sed 's/G//')
if [ "$AVAILABLE_SPACE" -lt 10 ]; then
    echo "ERROR: Not enough space on backup device (${AVAILABLE_SPACE}GB available, need at least 10GB)"
    exit 1
fi

# Perform backup with resource constraints
echo "Starting backup to $BACKUP_DIR..."
ionice -c 3 nice -n 19 rsync -aAXHSv --numeric-ids --delete --delete-excluded \
  --bwlimit=10000 --info=progress2 \
  --exclude={"/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*","/media/*","/lost+found","/var/cache/*","/var/tmp/*","*.iso","*.tmp"} \
  / "$BACKUP_DIR/" 2>&1

# Capture rsync exit code
RSYNC_EXIT_CODE=${PIPESTATUS[0]}
if [ $RSYNC_EXIT_CODE -ne 0 ]; then
    echo "ERROR: Backup failed with exit code $RSYNC_EXIT_CODE"
    
    # Cleanup if we mounted the device
    if [ "$MOUNTED" = true ]; then
        echo "Unmounting backup device..."
        umount "$MOUNT_POINT"
    fi
    
    exit $RSYNC_EXIT_CODE
fi

# Verify backup integrity
echo "Verifying backup integrity..."
if [ ! -f "$BACKUP_DIR/etc/fstab" ] || [ ! -f "$BACKUP_DIR/etc/passwd" ]; then
    echo "ERROR: Critical system files missing from backup"
    exit 1
fi

# Rotate backups - keep only the last N
echo "Rotating backups..."
cd "$MOUNT_POINT/opensuse_backups"
BACKUPS=$(ls -1tr | head -n -$RETENTION_COUNT)
if [ -n "$BACKUPS" ]; then
    echo "$BACKUPS" | xargs rm -rf
    echo "Removed old backups: $BACKUPS"
fi

# Cleanup
if [ "$MOUNTED" = true ]; then
    echo "Unmounting backup device..."
    umount "$MOUNT_POINT"
fi

echo "===== Backup completed successfully at $(date) ====="
```

And here are the systemd service and timer files:

```
# /etc/systemd/system/backup-opensuse.service
[Unit]
Description=Backup OpenSUSE to external drive
After=network-online.target local-fs.target
Wants=network-online.target
RequiresMountsFor=/mnt

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup-opensuse.sh
# Resource constraints
IOSchedulingClass=idle
IOSchedulingPriority=7
CPUSchedulingPolicy=idle
CPUSchedulingPriority=19
Nice=19
# Timeout after 12 hours
TimeoutStartSec=12h
# Restart on failure, but not too aggressively
RestartSec=30min
Restart=on-failure
# Security hardening
ProtectSystem=strict
ReadWritePaths=/mnt /var/log
PrivateTmp=true
```

```
# /etc/systemd/system/backup-opensuse.timer
[Unit]
Description=Weekly backup of OpenSUSE

[Timer]
# Run at 2:00 AM on Sundays
OnCalendar=Sun *-*-* 02:00:00
# If system was off when timer should have triggered, run it when system starts
Persistent=true
# Add randomized delay to avoid resource contention
RandomizedDelaySec=30min
# Don't run immediately after boot
AccuracySec=1min

[Install]
WantedBy=timers.target
```

To implement this solution:

1. Save the backup script as `/usr/local/bin/backup-opensuse.sh`
2. Make it executable: `sudo chmod +x /usr/local/bin/backup-opensuse.sh`
3. Save the service file as `/etc/systemd/system/backup-opensuse.service`
4. Save the timer file as `/etc/systemd/system/backup-opensuse.timer`
5. Enable and start the timer:
   ```
   sudo systemctl daemon-reload
   sudo systemctl enable backup-opensuse.timer
   sudo systemctl start backup-opensuse.timer
   ```