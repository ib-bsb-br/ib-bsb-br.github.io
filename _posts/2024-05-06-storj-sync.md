---
title: 'Rclone: Syncing STORJ Cloud to Local Storage'
date: 2024-05-06 00:00:00 -03:00
categories:
- Tutorial
- Code
tags:
- linux
- scripts
comment: https://rclone.org/s3/#storj
info: aberto.
type: post
layout: post
mermaid: true
---

```
#!/bin/bash

# Define directories and log file locations
LOG_DIR="/var/log/rclone/"
SYNC_LOG="${LOG_DIR}/rclone_sync.log"
ERROR_LOG="${LOG_DIR}/rclone_errors.log"

# Ensure the log directory exists
mkdir -p "${LOG_DIR}"

# Define source, destination, and compare-dest directories
SOURCE_DIR="/userdata/"
DEST_DIR="Storj:transfer/999_SHARED/"
COMPARE_DEST="Storj:transfer/999_SHARED/previous_backups"

# Check if the initial sync has been done
if [ ! -f "${LOG_DIR}/initial_sync_done" ]; then
    # Perform the initial synchronization
    rclone sync "${SOURCE_DIR}" "${DEST_DIR}" --progress -v --log-file="${SYNC_LOG}" 2>>"${ERROR_LOG}"

    # Check the exit status and create a marker file if successful
    if [ $? -eq 0 ]; then
        touch "${LOG_DIR}/initial_sync_done"
        echo "Initial sync completed successfully." >> "${SYNC_LOG}"
    else
        echo "Initial sync encountered an error. Check log for details." >> "${SYNC_LOG}"
        exit 1
    fi
fi

# Perform daily incremental backups using --copy-dest
rclone sync "${SOURCE_DIR}" "${DEST_DIR}" --copy-dest="${COMPARE_DEST}" --progress -v --log-file="${SYNC_LOG}" 2>>"${ERROR_LOG}"

# Check the exit status and log appropriately
if [ $? -eq 0 ]; then
    echo "Incremental sync operation completed successfully."
    echo "Incremental sync operation completed successfully." >> "${SYNC_LOG}"
else
    echo "Incremental sync operation encountered an error. Check log for details."
    echo "Incremental sync operation encountered an error. Check log for details." >> "${SYNC_LOG}"
fi

```

### Automation with Cron

For regular updates, you can automate the synchronization process through a cron job:

```bash
crontab -e
```

Add the following entries to execute the synchronization daily at 9 AM:

```
0 9 * * * /usr/bin/rstorj.sh
```
