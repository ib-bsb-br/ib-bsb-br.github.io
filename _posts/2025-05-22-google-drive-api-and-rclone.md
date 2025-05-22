---
tags: [scratchpad]
info: aberto.
date: 2025-05-22
type: post
layout: post
published: true
slug: google-drive-api-and-rclone
title: 'Google Drive API and `rclone`'
---
**Step 1: Install `rclone`**
```bash
sudo apt install rclone
```

**Step 2: Configure `rclone` for Google Drive (with Own API Credentials - Highly Recommended)**

Using rclone's default API credentials can lead to rate-limiting errors during large transfers. Creating your own is more reliable.

1.  **Create your own Google API Client ID and Secret for `rclone`:**
    Follow the official `rclone` guide: [https://rclone.org/drive/#making-your-own-client-id](https://rclone.org/drive/#making-your-own-client-id)
    This process involves using the Google Cloud Console. It might seem complex, but it's a one-time setup that significantly improves reliability for large transfers. Keep your generated `client_id` and `client_secret` handy.

2.  **Run `rclone config`:**
    ```bash
    rclone config
    ```
    Follow the interactive prompts:
    *   `n` (New remote)
    *   `name>`: Enter a short name (e.g., `gdrive_backup`)
    *   `Storage>`: Type `drive` or select the number for Google Drive.
    *   `client_id>`: **Enter the Client ID you created.**
    *   `client_secret>`: **Enter the Client Secret you created.**
    *   `scope>`: Choose `1` (Full access all files).
    *   `root_folder_id>`: Press Enter (leave blank for full Drive access, or specify a folder ID if desired).
    *   `service_account_file>`: Press Enter (leave blank).
    *   `Edit advanced config? (y/n)>`: `n`
    *   `Use auto config? (y/n)>`: `y`
        *   This will attempt to open a browser for authentication. If on a headless server, copy the URL it provides into a browser on another machine, authenticate, and then copy the verification code back to `rclone`.
    *   `Configure this as a Shared Drive (Team Drive)? (y/n)>`: `n` (unless you are using a Shared Drive).
    *   Review the summary and if OK, choose `y`.
    *   `q` (Quit config).

**Step 3: Prepare for the Long Transfer (Using `screen` or `tmux`)**

A 500GiB upload can take many hours or even days. If your SSH session disconnects, the `rclone` process will terminate. Use a terminal multiplexer like `screen` or `tmux` to prevent this.

*   **Using `screen` (simpler for beginners):**
    1.  Install if needed: `sudo apt install screen`
    2.  Start a new screen session: `screen -S rclone_upload_session`
    3.  You are now "inside" the screen session. Run your `rclone` command here.
    4.  To detach (leave it running in the background): Press `Ctrl+A`, then `d`.
    5.  To reattach later: `screen -r rclone_upload_session`

**Step 4: Perform a Dry Run (Crucial Safety Check)**

Before transferring any data, simulate the process to see what `rclone` *would* do.
Let's assume you want to copy everything to a folder named `My500GB_External_Backup` on your Google Drive.

```bash
# Ensure you are in your screen/tmux session
rclone copy /mnt/my_external_hdd gdrive_backup:My500GB_External_Backup --dry-run -P --check-first --checksum --skip-links --verbose --log-file=rclone_dry_run_$(date +%Y%m%d_%H%M%S).log
```
*   `gdrive_backup:My500GB_External_Backup`: Replace `gdrive_backup` with your rclone remote name.
*   `--dry-run`: Simulates the copy.
*   `-P` (or `--progress`): Shows progress.
*   `--check-first`: Checks all source/destination files before starting.
*   `--checksum`: Uses checksums for comparison (more reliable than just size/modtime).
*   `--skip-links`: Ignores symbolic links.
*   `--verbose`: More detailed output.
*   `--log-file`: Logs all output. **Review this log carefully.**

**If the dry run output looks correct and shows no errors, proceed.**

**Step 5: Execute the Full Data Transfer**

Remove `--dry-run` and add more robustness flags:

```bash
# Ensure you are in your screen/tmux session
rclone copy /mnt/my_external_hdd gdrive_backup:My500GB_External_Backup \
    -P \
    --check-first \
    --checksum \
    --skip-links \
    --verbose \
    --log-file=rclone_upload_$(date +%Y%m%d_%H%M%S).log \
    --stats 1m \
    --retries 5 \
    --low-level-retries 10 \
    --buffer-size 64M \
    --drive-chunk-size 64M \
    --transfers 4
```
*   **New/Important Flags:**
    *   `--log-file`: **Essential for diagnosing any issues during the long transfer.**
    *   `--stats 1m`: Prints transfer stats every minute.
    *   `--retries 5`: Retries failed file transfers up to 5 times.
    *   `--low-level-retries 10`: Retries low-level operations (like single HTTP requests).
    *   `--buffer-size 64M`: In-memory buffer per transfer. Adjust based on your RAM (e.g., 32M, 128M).
    *   `--drive-chunk-size 64M`: Uploads large files to Google Drive in 64MB chunks. Can significantly improve speed for large files (default is 8M). Max is 256M.
    *   `--transfers 4`: Number of files to transfer in parallel. Default is 4. Adjust based on your internet upload speed and CPU (e.g., 2-8).

Monitor progress via the terminal and the log file (`tail -f rclone_upload_...log`). Be patient.

**Step 6: Verify the Upload (Critical!)**

After `rclone copy` finishes, you **must** verify that all data was transferred correctly.

```bash
# Ensure you are in your screen/tmux session
rclone check /mnt/my_external_hdd gdrive_backup:My500GB_External_Backup \
    -P \
    --checksum \
    --one-way \
    --log-file=rclone_check_$(date +%Y%m%d_%H%M%S).log \
    --verbose
```
*   `rclone check`: Compares source and destination.
*   `--checksum`: **Crucial for verifying data integrity.** Compares files based on content hashes.
*   `--one-way`: Checks that every file in the source exists and is identical in the destination. It won't report extra files in the destination (which is fine after a `copy`).
*   `--log-file`: Logs the verification process.

Review the `rclone_check` log. Ideally, it should report 0 differences or only differences that are explainable (e.g., files skipped by `--skip-links`). Any unexpected "missing on destination" or "files differ" entries need investigation.

---

**Phase 3: Safely Unmounting the External Hard Drive**

**Step 1: Flush Disk Caches**

Before unmounting, ensure all cached data is written to the disk:
```bash
sync
sync
```
Running `sync` (some do it twice for good measure) flushes filesystem buffers.

**Step 2: Unmount the Drive**

1.  Ensure your terminal is not currently in the mount point directory:
    ```bash
    cd ~
    ```
2.  Unmount:
    ```bash
    sudo umount /mnt/my_external_hdd
    ```
    Or by device/UUID: `sudo umount UUID="69AF-5F99"`

**Step 3: Troubleshooting Unmount Issues ("target is busy")**

If you get a "target is busy" error:
*   Make sure no terminal or application is using `/mnt/my_external_hdd`.
*   Use these commands to find the culprit process(es):
    ```bash
    sudo lsof +D /mnt/my_external_hdd
    # OR
    sudo fuser -vmM /mnt/my_external_hdd
    ```    Close the identified applications or (carefully) kill the processes.
*   As a last resort, a "lazy unmount" can be used, but ensure `sync` was run:
    `sudo umount -l /mnt/my_external_hdd`

Once successfully unmounted, you can safely disconnect the USB drive.