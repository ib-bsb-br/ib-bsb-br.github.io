---
tags: [scratchpad]
info: aberto.
date: 2025-05-13
type: post
layout: post
published: true
slug: restic-to-transfer-files
title: 'restic to transfer files'
---
This guide uses the following specific paths:
*   **Source File:** `/opt/data_files/original_large.img`
*   **External Drive Mount Point:** `/media/my_external_drive`
*   **Restic Repository on External Drive:** `/media/my_external_drive/restic_img_repo`
*   **Final Destination for Restored File:** `/media/my_external_drive/final_copied_image.img`

Adjust these paths to match your actual file locations and drive configuration.

---

# Using `restic` to Transfer a Large `.img` File in Debian

## 1. Install `restic`

If `restic` is not already installed:
```bash
sudo apt update
sudo apt install restic -y
```

## 2. Set Repository Password

`restic` encrypts all data in its repository. You need to set a password for it. Choose a strong, unique password and **store it securely**. If you lose this password, your backed-up data will be irrecoverable.

Export the password as an environment variable for the current terminal session:
```bash
export RESTIC_PASSWORD='your-chosen-strong-password'
```
(Replace `'your-chosen-strong-password'` with your actual password). You'll need to do this in any new terminal or add it to your shell's startup file (e.g., `~/.bashrc`) for persistence.

## 3. Initialize the `restic` Repository

Create the `restic` repository on your external drive. This only needs to be done once for a new repository.
```bash
restic -r /media/my_external_drive/restic_img_repo init
```
**Expected output on success:**
```
created restic repository XXXXXXXX at /media/my_external_drive/restic_img_repo

Please note that knowledge of your password is required to access
the repository. Losing your password means that your data is
irreversibly lost.
```

## 4. Back Up the `.img` File to the Repository

This step copies the source file into the `restic` repository. `restic` shows progress and can resume if interrupted; simply re-run the same command.
```bash
restic -r /media/my_external_drive/restic_img_repo backup /opt/data_files/original_large.img --verbose
```
*   `-r /media/my_external_drive/restic_img_repo`: Specifies the repository.
*   `backup /opt/data_files/original_large.img`: Backs up the specified file.
*   `--verbose`: Provides detailed progress (percentage, speed, ETA).

Note the snapshot ID outputted upon completion (e.g., `snapshot abcdef01 saved`). You can usually use `latest` instead of the ID.

## 5. Restore the `.img` File from the Repository

This step extracts the file from the repository to a standard file on your external drive.
`restic` restores files with their original path structure relative to the backup root, under the `--target` directory.

```bash
restic -r /media/my_external_drive/restic_img_repo restore latest --target /media/my_external_drive/restore_temp --include /opt/data_files/original_large.img --verbose
```
*   `restore latest`: Restores from the most recent snapshot.
*   `--target /media/my_external_drive/restore_temp`: Base directory for restoration. A temporary directory name is used here for clarity before the final move.
*   `--include /opt/data_files/original_large.img`: Specifies only this file should be restored from the snapshot.

This command will restore the file to: `/media/my_external_drive/restore_temp/opt/data_files/original_large.img`.

## 6. Move the Restored File to its Final Location

Move the restored file from the temporary restoration path to your desired final path and name.
```bash
mv /media/my_external_drive/restore_temp/opt/data_files/original_large.img /media/my_external_drive/final_copied_image.img
```
After the move, you can remove the temporary directory structure if it's empty:
```bash
rmdir -p /media/my_external_drive/restore_temp/opt/data_files
```
(The `-p` option removes parent directories if they become empty).

## 7. Verify File Integrity

Compare checksums of the original source file and the final restored file.
```bash
sha256sum /opt/data_files/original_large.img /media/my_external_drive/final_copied_image.img
```
The two checksums **must match exactly**. You can also use `md5sum`.

## Important Notes

*   **Password:** Your `RESTIC_PASSWORD` is vital. Loss of the password means loss of data.
*   **Disk Space:** The external drive needs space for the `restic` repository (roughly the size of the `.img` file) AND for the fully restored `.img` file simultaneously during this process.
*   **`restic` is a Backup Tool:** This method uses backup/restore. The repository contains a versioned, deduplicated, and encrypted copy.
*   **Metadata:** `restic` preserves file permissions and modification times.
*   **Interrupts:** `restic backup` and `restic restore` operations are generally resumable by re-running the same command.
*   **Cleanup (Optional):** If you no longer need the backup in the `restic` repository after confirming the transfer:
    1.  List snapshots: `restic -r /media/my_external_drive/restic_img_repo snapshots`
    2.  Forget the snapshot(s) and prune data: `restic -r /media/my_external_drive/restic_img_repo forget <SNAPSHOT_ID_or_latest> --prune`
    3.  To completely remove the repository: `rm -rf /media/my_external_drive/restic_img_repo` (Use `rm -rf` with extreme caution).