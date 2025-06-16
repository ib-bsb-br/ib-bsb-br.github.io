---
tags: [aid>software]
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

# Integrating Restic with Storj for Decentralized Cloud Backups

Storj is a decentralized cloud object storage platform that offers a compelling backend solution for Restic backups due to its distributed architecture, S3 compatibility, end-to-end encryption principles, and potentially competitive pricing. This section provides a comprehensive guide to configuring and using Restic with Storj, primarily leveraging Rclone as the intermediary.

### 1. Introduction to Storj for Restic Users

Storj provides enterprise-grade, globally distributed cloud object storage. Its key features relevant to Restic users include:
*   **Decentralization:** Files are encrypted, erasure-coded, and spread across a vast network of independent storage nodes, enhancing durability and availability.
*   **Security:** Storj emphasizes zero-trust security. When combined with Restic's client-side end-to-end encryption, your backup data remains confidential even from Storj and its node operators.
*   **S3-Compatible API:** Storj offers an Amazon S3-compatible API, allowing tools like Rclone (and by extension, Restic) to interact with it seamlessly.
*   **Native Integration Potential:** Rclone also supports a native Storj integration (via Uplink CLI concepts), which can offer client-side erasure coding for path encryption and potentially optimized performance.
*   **Cost-Effectiveness:** Storj's pricing model (typically per GB stored and per GB downloaded) can be attractive, especially when paired with Restic's efficient deduplication, which minimizes storage footprint.

Using Restic with Storj via Rclone allows you to combine Restic's robust backup features with Storj's resilient and secure decentralized storage.

### 2. Prerequisites

Before you begin, ensure you have the following:
1.  **A Storj Account:** Sign up at [Storj.io](https://storj.io/signup?partner=restic). New accounts often come with a free trial allowance.
2.  **Restic Installed:** Download and install the Restic binary for your operating system from the [official Restic releases page](https://github.com/restic/restic/releases) or via your system's package manager. Ensure it's in your PATH.
3.  **Rclone Installed:** Download and install Rclone from the [official Rclone website](https://rclone.org/install/). Ensure it's in your PATH.

### 3. Rclone Configuration for Storj

Rclone is the bridge between Restic and Storj. You need to configure an Rclone "remote" that points to your Storj account. Storj can be accessed by Rclone in two main ways. The **S3-Compatible Gateway** (Method 1) is often simpler to set up if you're familiar with S3 credentials and offers broad compatibility. The **Native Storj Integration** (Method 2) uses Storj's Uplink protocols, may offer client-side erasure coding for path encryption, and could have different performance characteristics. Choose the method that best fits your technical comfort and requirements.

#### 3.1. Method 1: Configuring Rclone for Storj via S3-Compatible Gateway

This method uses Storj's S3-compatible API endpoint and requires S3 credentials (access key and secret key).

**Step 1: Generate S3 Credentials in Storj Console**
1.  Log in to your Storj account.
2.  Navigate to **Access Keys** (or a similarly named section for S3 credentials).
3.  Create a new Access Key.
    *   Give it a descriptive name (e.g., `restic-backup-s3-creds`).
    *   Set appropriate permissions (Read, Write, List, Delete for the buckets Restic will use).
    *   Note down the **Access Key ID**, **Secret Access Key**, and the **S3 Gateway Endpoint** (e.g., `gateway.storjshare.io`).

**Step 2: Configure Rclone Remote for S3 Gateway**
You can configure Rclone by editing its configuration file directly (find its location with `rclone config file`) or by using the interactive `rclone config` setup.

*   **Editing `rclone.conf` directly:**
    Add a new remote section to your `rclone.conf` file (e.g., `~/.config/rclone/rclone.conf`):
    ```ini
    [storj_s3]
    type = s3
    provider = Storj
    access_key_id = YOUR_STORJ_ACCESS_KEY_ID
    secret_access_key = YOUR_STORJ_SECRET_ACCESS_KEY
    endpoint = gateway.storjshare.io
    # Optional: Define a specific region if needed, though often not required for Storj's global gateway
    # region = us-east-1
    # Optional: Storj docs sometimes recommend disabling checksum for S3 gateway with rclone
    # disable_checksum = true
    # Optional: Rclone's 'chunk_size' (e.g., '64M') controls how Rclone itself chunks large files (Restic packs in this case) 
    # for multipart upload to S3-compatible storage. This is distinct from Restic's '--pack-size'. 
    # Adjusting Rclone's 'chunk_size' might be relevant for optimizing uploads of very large Restic packs 
    # over unstable connections, but Restic's default pack handling is usually sufficient.
    # chunk_size = 64M 
    ```
    Replace `YOUR_STORJ_ACCESS_KEY_ID` and `YOUR_STORJ_SECRET_ACCESS_KEY` with the credentials you generated.

*   **Using `rclone config` (Interactive):**
    1.  Run `rclone config`.
    2.  Choose `n` for a new remote.
    3.  Enter a name, e.g., `storj_s3`.
    4.  For "Type of storage to configure," choose `s3` (Amazon S3 Compliant Storage Providers).
    5.  For "S3 Provider," choose `Storj`.
    6.  Enter your `access_key_id` and `secret_access_key`.
    7.  For "Endpoint for S3 API," enter the Storj S3 gateway (e.g., `gateway.storjshare.io`).
    8.  You can typically leave other options (region, location_constraint, acl) as default or blank unless you have specific requirements.
    9.  Save the configuration.

#### 3.2. Method 2: Configuring Rclone for Native Storj Integration (Uplink)

This method uses Storj's native protocols via the Uplink library integrated into Rclone. It might offer client-side erasure coding and potentially different performance characteristics. It typically uses an Access Grant or an API Key and Encryption Passphrase.

**Step 1: Obtain Native Access Credentials**
*   **Access Grant:** This is a serialized string that bundles permissions, API key, satellite address, and encryption passphrase. You might generate this via the Uplink CLI or receive it if someone is granting you access.
*   **API Key & Encryption Passphrase:** You can generate an API key from the Storj console and then use it with your chosen encryption passphrase.

**Step 2: Configure Rclone Remote for Native Storj**
Use the `rclone config` interactive setup:
1.  Run `rclone config`.
2.  Choose `n` for a new remote.
3.  Enter a name, e.g., `storj_native`.
4.  For "Type of storage to configure," find and choose `storj` (Storj Decentralized Cloud Storage).
5.  Rclone will then prompt for the authentication method:
    *   **Existing Access Grant:** If you have an access grant string, choose this option and paste the grant.
    *   **New Access Grant (API Key & Passphrase):** If you have an API key and want to use a new or existing encryption passphrase:
        *   Select the appropriate satellite address (e.g., `us-central-1.storj.io`, `europe-west-1.storj.io`, `asia-east-1.storj.io`).
        *   Enter your API Key.
        *   Enter your encryption passphrase (this is critical for encrypting/decrypting file paths and metadata *before* Restic's own encryption layer).
6.  Review the summary and save the configuration.
    *   *Note:* Remote-specific tuning flags for the native Storj Rclone remote (like a hypothetical `upload_nolarge_chunks = true`) would be added directly to this remote's section in `rclone.conf` if needed, rather than typically passed via `restic -o rclone.args`.

**Step 3: Verify Rclone Remote**
After configuring, test your Rclone remote:
```bash
rclone lsd storj_s3:  # or storj_native:
# This should list any buckets you have. If it's a new account, it will be empty.
```

### 4. Restic Repository Setup on Storj

**Step 1: Create a Storj Bucket**
Restic needs a bucket (and optionally a path within it) to store its repository. Use Rclone to create a bucket if it doesn't exist.
```bash
# Replace 'your-restic-bucket' with your desired bucket name
# Replace 'storj_s3' with your configured Rclone remote name (storj_s3 or storj_native)
rclone mkdir storj_s3:your-restic-bucket
```
Bucket names must be globally unique if using the S3 gateway, or unique within your project for native access.

**Step 2: Initialize the Restic Repository**
Now, initialize the Restic repository within the bucket using the Rclone backend.
Choose a strong, unique password for your Restic repository. **Losing this Restic password means your backup data is irrecoverably lost, regardless of Storj access.**

```bash
# Define your Restic repository location using the Rclone remote
# Format: rclone:<rclone-remote-name>:<bucket-name>/<path-within-bucket>
# The path-within-bucket is optional but recommended for organization.
export RESTIC_REPOSITORY="rclone:storj_s3:your-restic-bucket/my-server-backups"

# Set your Restic password (choose one method)
export RESTIC_PASSWORD='your-super-strong-restic-password'
# OR use a password file:
# echo 'your-super-strong-restic-password' > ~/.restic-storj-pass
# chmod 600 ~/.restic-storj-pass
# export RESTIC_PASSWORD_FILE=~/.restic-storj-pass

# Initialize the repository
restic init
```
On success, Restic will confirm repository creation.

### 5. Backup Operations with Storj

With the repository initialized, you can start backing up data.

```bash
# Example: Backing up your home directory
restic backup ~/ --verbose --tag home_backup_$(date +%Y%m%d)

# Example: Backing up specific project directories
restic backup /srv/projectA /var/www/projectB --verbose --tag web_projects
```

**Storj-Specific Optimizations and Considerations:**

*   **Pack Size (`--pack-size`):**
    The Storj documentation (from `raw_data`) recommends setting Restic's pack size to 60 MiB. This is suggested because it aligns well with Storj's underlying segment sizes (often around 64MiB), potentially minimizing padding or overhead per segment and improving storage efficiency or transfer performance on their network.
    ```bash
    restic backup /data/to/backup --pack-size=60
    ```
    While Restic might be "not very precise" and actual pack files may be slightly larger, this is a good target.

*   **Rclone Options via Restic (`-o` or `--option`):**
    You can pass arguments to the underlying `rclone serve restic` command that Restic invokes. These are best used for flags affecting the `serve` command itself or general Rclone behavior during that operation.
    *   **Connection Parallelism (`rclone.connections`):**
        The Storj documentation draft mentions: `Passing -o rclone.connections=1 reduces the Rclone parallelism to a single upload. The Storj backend will still open multiple connections to storage nodes. Use this option to reduce the stress on your router in case of failing uploads with the default parallelism.`
        ```bash
        restic -o rclone.connections=1 backup /data/to/backup
        ```
        Conversely, on very stable, high-bandwidth connections, you *might* experiment with higher values (e.g., `rclone.connections=4` or `8`), but monitor for errors. The default for Restic's Rclone backend is 5 connections.
    *   **Bandwidth Limiting (via `rclone.args`):**
        If backups saturate your internet connection or cause instability, you can limit Rclone's bandwidth by passing the `--bwlimit` flag to Rclone:
        ```bash
        # Limit to 5 MiB/s
        restic -o rclone.args="serve restic --stdio --bwlimit 5M" backup /data/to/backup
        ```
    *   **Other Rclone Arguments (`rclone.args`):**
        For other Rclone flags specific to the `rclone serve restic` command:
        ```bash
        restic -o rclone.args="serve restic --stdio --stats 1m" backup /data/to/backup
        # --stats 1m would make rclone print transfer stats every minute during the 'serve restic' operation.
        ```

*   **Unix Root Backups:**
    When backing up the root directory (`/`) on Unix systems, always use `--one-file-system` to prevent Restic from trying to back up virtual filesystems like `/proc`, `/sys`, or other mounted filesystems you don't intend to include:
    ```bash
    sudo restic backup / --one-file-system --exclude /mnt --exclude /media --exclude /var/cache --exclude /tmp
    ```

### 6. Restore Operations from Storj

Restoring data is straightforward:

```bash
# Restore the latest snapshot to ~/restore_dir
restic restore latest --target ~/restore_dir --verbose

# Restore a specific snapshot by ID
restic restore <snapshot_ID> --target ~/restore_dir

# Restore specific files/folders from the latest snapshot
restic restore latest --target ~/restore_dir --include "/path/within/snapshot/to/file.txt" --include "/another/path/*"
```
**Considerations:**
*   **Egress Costs:** Restoring large amounts of data from any cloud storage, including Storj, will incur download (egress) bandwidth charges. Factor this into your recovery plan.
*   **Time:** Download speeds will depend on your internet connection, Storj network performance, and the number/size of files.

### 7. Repository Maintenance on Storj

Regular maintenance is crucial for managing storage space and ensuring repository health.

*   **Forgetting Old Snapshots (`restic forget`):**
    Define a retention policy to remove old, unneeded snapshots. Always use `--prune` with `forget` when interacting with cloud backends to reclaim space.
    ```bash
    # Keep the last 7 daily, 4 weekly, 6 monthly, 1 yearly snapshots, and prune data
    restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --keep-yearly 1 --prune

    # Forget a specific snapshot and prune
    # restic forget <snapshot_ID> --prune
    ```
*   **Checking Repository Integrity (`restic check`):**
    Periodically verify the repository's consistency.
    ```bash
    restic check
    ```
    For a more thorough check that reads all data packs (slower and incurs more download operations/costs on cloud storage):
    ```bash
    restic check --read-data
    # Or check a subset of data:
    # restic check --read-data-subset=10%
    ```

### 8. Performance Considerations and Troubleshooting with Storj

Based on community discussions (e.g., the Storj forum thread in `raw_data`):
*   **"Successful puts less than success threshold" Errors:** This error, sometimes seen with Rclone and Storj, indicates that Rclone couldn't upload enough erasure-coded pieces of a segment to enough storage nodes to meet the success threshold.
    *   **Possible Causes:** Network instability, router issues (too many connections), very slow individual nodes, or aggressive Rclone transfer settings.
    *   **Mitigation:**
        *   Try reducing Rclone's parallelism: `restic -o rclone.connections=1 ...`
        *   Limit bandwidth: `restic -o rclone.args="serve restic --stdio --bwlimit <rate>" ...`
        *   Ensure your Rclone and Restic versions are up-to-date.
        *   Check the Storj status page and community forums for any ongoing network issues.
*   **Upload/Download Speeds:**
    *   Heavily dependent on your internet connection's upload/download capacity.
    *   Storj's decentralized nature means performance can vary.
    *   Small files can have higher per-file overhead than large files. Restic's packing helps, but very numerous tiny files can still be slower.
    *   Initial backups are often slower than subsequent incremental backups due to Restic's deduplication.
*   **Rclone & Restic Logging:**
    *   To get detailed logs from Rclone during a Restic operation, you can instruct Restic to pass logging flags to Rclone:
        ```bash
        restic -o rclone.args="serve restic --stdio -vv --log-file /tmp/rclone-restic.log" backup ...
        ```
        This will make Rclone itself very verbose. Inspect `/tmp/rclone-restic.log`.
    *   For debugging Restic's own operations and progress, use Restic's verbosity flags (e.g., `restic -vv backup ...`) or set `export RESTIC_PROGRESS_FPS=10` for more frequent progress updates from Restic.

Refer to the [Storj Community Forum](https://forum.storj.io/) for ongoing discussions and support, particularly the thread mentioned in the initial draft: [Two more Tech Previews - RClone and Restic](https://forum.storj.io/t/two-more-tech-previews-rclone-and-restic/6072) (though note this thread is from 2020 and information may have evolved).

### 9. Security and Cost Considerations

*   **Security:**
    *   **Restic's End-to-End Encryption:** Your data is encrypted on your machine *before* it's sent to Rclone and then to Storj. Only you, with the Restic repository password, can decrypt it. A key benefit of Restic's client-side encryption is that Storj (or any cloud provider used as a backend) only ever stores encrypted blobs of data. They cannot access your actual file contents or metadata, ensuring a high degree of privacy.
    *   **Storj's Security:** Storj further encrypts data segments and distributes them. If using native Rclone integration with an encryption passphrase, that adds another layer for metadata path encryption.
    *   **Access Credentials:** Protect your Storj S3 credentials, Access Grants, API keys, and especially your Restic repository password diligently.
*   **Cost:**
    *   **Storage:** Storj charges for the amount of data stored per month (after erasure coding, so 1GB of your data might consume ~2.7GB on the network, but you are typically billed for the 1GB). Restic's deduplication significantly reduces the actual data stored over time for versioned backups.
    *   **Egress (Download):** Storj charges for data downloaded from the network. This is relevant for restores.
    *   **Operations:** There might be minor charges for certain API operations, but these are usually less significant for typical Restic usage.
    *   Always refer to the [official Storj pricing page](https://storj.io/dcs/pricing) for current details. Restic's efficiency helps in making Storj a cost-effective option for long-term, secure backups.

# Integrating Restic with Google Drive for Cloud backups and maintenance

The **`gdrive-backup`** script is for *adding* data to your backup, while the **`gdrive-maintenance`** script is for *managing* that data to ensure it remains healthy and efficient over the long term.

{% codeblock bash %}
#!/bin/bash
#
# This script automates the setup for a "Backup-First" model using rclone and restic.
# It intelligently installs/upgrades the latest tools, interactively guides the user
# through the complex rclone Google Drive authentication, verifies success at each
# step, and deploys easy-to-use scripts for backups and maintenance.
#
# Target System: Debian 11 (Bullseye) on ARM64 RK3588
# Executed from: User's home directory (~/)

# --- Strict Mode & Error Handling ---
set -euo pipefail

# --- Global Configuration (Can be customized) ---
RESTIC_REPO_PATH="ResticBackups/my-linux-desktop"
RESTIC_PASSWORD_FILE="$HOME/.config/restic/gdrive_password"
USER_SCRIPT_DIR="$HOME/bin"
BACKUP_SCRIPT_NAME="gdrive-backup"
MAINTENANCE_SCRIPT_NAME="gdrive-maintenance"

# This will be determined dynamically.
RCLONE_REMOTE_NAME=""

# --- Color Setup ---
setup_colors() {
    if tput setaf 1 >/dev/null 2>&1; then
        C_RESET=$(tput sgr0); C_INFO=$(tput setaf 2); C_WARN=$(tput setaf 3)
        C_ACTION=$(tput setaf 6); C_ERROR=$(tput setaf 1); C_BOLD=$(tput bold)
    else
        C_RESET=""; C_INFO=""; C_WARN=""; C_ACTION=""; C_ERROR=""; C_BOLD=""
    fi
}

# --- Helper Functions ---

cleanup_on_exit() {
    if [ -n "${TEMP_DOWNLOAD_DIR:-}" ] && [ -d "$TEMP_DOWNLOAD_DIR" ]; then
        echo; echo "${C_INFO}INFO: Cleaning up temporary directory...${C_RESET}"
        rm -rf "$TEMP_DOWNLOAD_DIR"
    fi
}

ensure_tool_installed() {
    local tool_name="$1"
    local package_name="${2:-$tool_name}"
    if ! command -v "$tool_name" >/dev/null 2>&1; then
        echo "${C_INFO}INFO: Tool '${C_BOLD}$tool_name${C_RESET}${C_INFO}' not found. Installing '${C_BOLD}$package_name${C_RESET}${C_INFO}'...${C_RESET}"
        if ! sudo apt-get install -y "$package_name"; then
            echo "${C_ERROR}ERROR: Failed to install '$package_name'. Please install it manually.${C_RESET}" >&2; exit 1
        fi
        echo "${C_INFO}SUCCESS: '$package_name' installed.${C_RESET}"
    else
        echo "${C_INFO}INFO: Tool '${C_BOLD}$tool_name${C_RESET}${C_INFO}' is already installed.${C_RESET}"
    fi
}

ensure_path() {
    echo "${C_INFO}INFO: Ensuring '${C_BOLD}$USER_SCRIPT_DIR${C_RESET}${C_INFO}' is in your PATH...${C_RESET}"
    mkdir -p "$USER_SCRIPT_DIR"
    if [[ ":$PATH:" != *":$USER_SCRIPT_DIR:"* ]]; then
        echo "${C_WARN}WARNING: '${C_BOLD}$USER_SCRIPT_DIR${C_RESET}${C_WARN}' is not in your active PATH.${C_RESET}"
        local profile_file="$HOME/.profile"
        if [ -f "$HOME/.bash_profile" ]; then profile_file="$HOME/.bash_profile"; elif [ -f "$HOME/.zshrc" ]; then profile_file="$HOME/.zshrc"; elif [ -f "$HOME/.bashrc" ]; then profile_file="$HOME/.bashrc"; fi
        if ! grep -q 'export PATH="$HOME/bin:$PATH"' "$profile_file"; then
            echo "${C_ACTION}ACTION: Adding PATH export to '${C_BOLD}$profile_file${C_RESET}${C_ACTION}'.${C_RESET}"
            { echo ''; echo '# Add local bin directory to PATH'; echo 'export PATH="$HOME/bin:$PATH"'; } >> "$profile_file"
            echo "${C_WARN}You must run '${C_BOLD}source \"$profile_file\"${C_RESET}${C_WARN}' or restart your terminal for changes to take effect.${C_RESET}"
        fi
    fi
}

install_restic() {
    echo "${C_INFO}INFO: Checking Restic version...${C_RESET}"
    local latest_version installed_version
    latest_version=$(curl -s "https://api.github.com/repos/restic/restic/releases/latest" | jq -r .tag_name | sed 's/v//')
    installed_version=$(restic version 2>/dev/null | awk '{print $2}' || echo "0.0.0")

    if dpkg --compare-versions "$installed_version" "lt" "$latest_version"; then
        echo "${C_INFO}INFO: A new Restic version (${C_BOLD}$latest_version${C_RESET}${C_INFO}) is available (you have $installed_version). Upgrading...${C_RESET}"
        local restic_url
        restic_url=$(curl -s "https://api.github.com/repos/restic/restic/releases/latest" | jq -r '.assets[] | select(.name | contains("linux_arm64.bz2")) | .browser_download_url')
        if [ -z "$restic_url" ]; then echo "${C_ERROR}ERROR: Could not find Restic ARM64 release URL.${C_RESET}" >&2; exit 1; fi

        echo "${C_INFO}INFO: Downloading from: ${C_BOLD}$restic_url${C_RESET}"
        local TEMP_DOWNLOAD_DIR; TEMP_DOWNLOAD_DIR=$(mktemp -d)
        curl -Lfo "${TEMP_DOWNLOAD_DIR}/restic.bz2" "${restic_url}"
        bunzip2 "${TEMP_DOWNLOAD_DIR}/restic.bz2"
        sudo mv "${TEMP_DOWNLOAD_DIR}/restic" /usr/local/bin/restic
        sudo chmod +x /usr/local/bin/restic
        echo "${C_INFO}SUCCESS: Restic upgraded to version $(restic version | awk '{print $2}').${C_RESET}"
    else
        echo "${C_INFO}INFO: Your Restic version (${C_BOLD}$installed_version${C_RESET}${C_INFO}) is up to date.${C_RESET}"
    fi
}

configure_rclone_remote() {
    local gdrive_remotes
    gdrive_remotes=$(rclone listremotes | sed 's/://' || true)

    if [ -n "$gdrive_remotes" ]; then
        echo "${C_ACTION}ACTION: Found existing rclone remotes. Please choose one or create a new one:${C_RESET}"
        select remote in $gdrive_remotes "CREATE_A_NEW_REMOTE"; do
            if [ "$remote" == "CREATE_A_NEW_REMOTE" ]; then
                break # Break to the creation part
            elif [ -n "$remote" ]; then
                RCLONE_REMOTE_NAME=$remote
                return
            else
                echo "${C_ERROR}Invalid selection.${C_RESET}"
            fi
        done
    fi

    # This section runs if no remotes exist or user chose to create a new one
    echo
    echo "${C_ACTION}------------------------- IMPORTANT: Rclone Setup Instructions -------------------------${C_RESET}"
    echo "${C_WARN}You will now be guided through creating a Google Drive remote.${C_RESET}"
    echo "1. When prompted for 'name', choose a simple name (e.g., 'gdrive_hub')."
    echo "2. When prompted for 'Storage', select 'drive' (Google Drive)."
    echo "3. For 'client_id' and 'client_secret', you must provide your own credentials from the Google Cloud Console."
    echo "   ${C_ERROR}CRITICAL: When you copy your Client ID, copy ONLY the ID string, like:${C_RESET}"
    echo "   ${C_BOLD}1234567890-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com${C_RESET}"
    echo "   ${C_ERROR}DO NOT paste the full URL or anything else.${C_RESET}"
    echo "4. For all other options, pressing Enter for the default is usually safe."
    echo "5. Your web browser should open for you to authorize the connection."
    echo "${C_ACTION}--------------------------------------------------------------------------------------${C_RESET}"
    read -r -p "Press ENTER to begin..."
    
    rclone config
    
    # After creation, ask the user to confirm the name of the new remote
    echo "${C_ACTION}ACTION: Please enter the name of the remote you just created:${C_RESET}"
    read -r RCLONE_REMOTE_NAME
    if [ -z "$RCLONE_REMOTE_NAME" ]; then
        echo "${C_ERROR}ERROR: No remote name provided. Exiting.${C_RESET}" >&2
        exit 1
    fi
}

# --- Main Execution ---

main() {
    setup_colors
    trap cleanup_on_exit EXIT SIGINT SIGTERM

    echo "${C_BOLD}====================================================================${C_RESET}"
    echo "${C_BOLD}=== Robust Rclone + Restic Backup Setup for Debian             ===${C_RESET}"
    echo "${C_BOLD}====================================================================${C_RESET}"
    echo

    # --- Step 1: Install Prerequisites ---
    echo "--- [Step 1/7] Installing prerequisite tools..."
    sudo apt-get update -qq
    ensure_tool_installed "curl" "curl"
    ensure_tool_installed "unzip" "unzip"
    ensure_tool_installed "rclone" "rclone"
    ensure_tool_installed "jq" "jq"
    ensure_tool_installed "bunzip2" "bzip2"
    echo

    # --- Step 2: Ensure PATH is configured ---
    echo "--- [Step 2/7] Verifying PATH environment..."
    ensure_path
    echo

    # --- Step 3: Install/Upgrade Restic ---
    echo "--- [Step 3/7] Installing/Upgrading Restic..."
    install_restic
    echo

    # --- Step 4: Configure Rclone Remote ---
    echo "--- [Step 4/7] Configuring Rclone remote for Google Drive..."
    configure_rclone_remote
    echo

    # --- Step 5: Verify Rclone Authentication ---
    echo "--- [Step 5/7] Verifying rclone authentication for '${C_BOLD}${RCLONE_REMOTE_NAME}${C_RESET}'..."
    while ! rclone lsd "${RCLONE_REMOTE_NAME}:" >/dev/null 2>&1; do
        echo "${C_ERROR}ERROR: Rclone cannot authenticate with '${C_BOLD}${RCLONE_REMOTE_NAME}${C_RESET}${C_ERROR}'.${C_RESET}"
        echo "${C_WARN}This is likely due to an incomplete or incorrect initial setup.${C_RESET}"
        echo "${C_ACTION}ACTION: Let's try to fix this by reconnecting the remote.${C_RESET}"
        read -r -p "Press ENTER to run 'rclone config reconnect ${RCLONE_REMOTE_NAME}:'..."
        rclone config reconnect "${RCLONE_REMOTE_NAME}:"
        echo "${C_INFO}INFO: Re-checking connection...${C_RESET}"
    done
    echo "${C_INFO}SUCCESS: Rclone authentication for '${C_BOLD}${RCLONE_REMOTE_NAME}${C_RESET}${C_INFO}' is working.${C_RESET}"
    echo

    # --- Step 6: Setup Restic Repository & Password ---
    local restic_repository="rclone:${RCLONE_REMOTE_NAME}:${RESTIC_REPO_PATH}"
    echo "--- [Step 6/7] Setting up Restic repository and password..."
    echo "Configuration that will be used:"
    echo "  - Rclone Remote:  ${C_BOLD}$RCLONE_REMOTE_NAME${C_RESET}"
    echo "  - Repository Path:  ${C_BOLD}$restic_repository${C_RESET}"
    echo "  - Password File:    ${C_BOLD}$RESTIC_PASSWORD_FILE${C_RESET}"
    
    mkdir -p "$(dirname "$RESTIC_PASSWORD_FILE")"
    if [ ! -f "$RESTIC_PASSWORD_FILE" ]; then
        echo "${C_ACTION}ACTION: Please create a new, strong password for your backup repository.${C_RESET}"
        read -s -p "Enter repository password: " restic_pass; echo
        read -s -p "Confirm password: " restic_pass_confirm; echo
        if [ "$restic_pass" = "$restic_pass_confirm" ] && [ -n "$restic_pass" ]; then
            echo "$restic_pass" > "$RESTIC_PASSWORD_FILE" && chmod 600 "$RESTIC_PASSWORD_FILE"
            echo "${C_INFO}SUCCESS: Password file created.${C_RESET}"
        else
            echo "${C_ERROR}ERROR: Passwords do not match or are empty. Please re-run the script.${C_RESET}" >&2; exit 1
        fi
    else
        echo "${C_INFO}INFO: Existing password file found. Using it.${C_RESET}"
    fi

    if restic -r "$restic_repository" --password-file "$RESTIC_PASSWORD_FILE" cat config >/dev/null 2>&1; then
        echo "${C_INFO}INFO: Restic repository already initialized. Skipping.${C_RESET}"
    else
        echo "${C_WARN}WARNING: Restic repository not found. Initializing...${C_RESET}"
        if ! restic -r "$restic_repository" --password-file "$RESTIC_PASSWORD_FILE" init; then
            echo "${C_ERROR}ERROR: Failed to initialize restic repository.${C_RESET}" >&2; exit 1
        fi
        echo "${C_INFO}SUCCESS: Restic repository initialized.${C_RESET}"
    fi
    echo

    # --- Step 7: Deploy User Scripts ---
    echo "--- [Step 7/7] Deploying helper scripts to '${C_BOLD}$USER_SCRIPT_DIR${C_RESET}'..."
    # Deploy Backup Script
    cat << EOF > "${USER_SCRIPT_DIR}/${BACKUP_SCRIPT_NAME}"
#!/bin/bash
set -euo pipefail
if [ -z "\${1:-}" ] || [ "\$1" == "--help" ]; then echo "Usage: \$(basename "\$0") /path/to/backup"; exit 1; fi
if [ ! -d "\$1" ]; then echo "Error: Path '\$1' is not a valid directory." >&2; exit 1; fi
echo "--- Starting Restic Backup for '\$1' ---"
restic -r "${restic_repository}" --password-file "${RESTIC_PASSWORD_FILE}" --verbose \\
    -o rclone.connections=8 -o rclone.drive-skip-gdocs=true \\
    backup "\$1" --tag "\$(date +%Y%m%d)"
echo "--- Backup Finished ---"
EOF
    chmod +x "${USER_SCRIPT_DIR}/${BACKUP_SCRIPT_NAME}"
    echo "${C_INFO}SUCCESS: Deployed '${C_BOLD}${BACKUP_SCRIPT_NAME}${C_RESET}${C_INFO}'.${C_RESET}"

    # Deploy Maintenance Script
    cat << EOF > "${USER_SCRIPT_DIR}/${MAINTENANCE_SCRIPT_NAME}"
#!/bin/bash
set -euo pipefail
echo "--- Restic Repository Maintenance ---"
echo "Repository: ${restic_repository}"
echo
PS3="Please choose a maintenance action: "
select action in "Check Integrity" "Prune Old Snapshots" "Exit"; do
    case \$action in
        "Check Integrity")
            echo "--- Running integrity check... ---"
            restic -r "${restic_repository}" --password-file "${RESTIC_PASSWORD_FILE}" check
            echo "--- Check complete. ---"; break;;
        "Prune Old Snapshots")
            echo "--- Applying retention policy (keep 7 daily, 4 weekly, 12 monthly) and pruning... ---"
            restic -r "${restic_repository}" --password-file "${RESTIC_PASSWORD_FILE}" forget \\
                --keep-daily 7 --keep-weekly 4 --keep-monthly 12 --keep-yearly 99 --prune
            echo "--- Prune complete. ---"; break;;
        "Exit") break;;
        *) echo "Invalid option \$REPLY";;
    esac
done
EOF
    chmod +x "${USER_SCRIPT_DIR}/${MAINTENANCE_SCRIPT_NAME}"
    echo "${C_INFO}SUCCESS: Deployed '${C_BOLD}${MAINTENANCE_SCRIPT_NAME}${C_RESET}${C_INFO}'.${C_RESET}"
    echo
    echo "${C_BOLD}=========================== SETUP COMPLETE ===========================${C_RESET}"
    echo
    echo "${C_INFO}You are now ready to back up your data!${C_RESET}"
    echo "${C_WARN}If this is a new terminal, remember to run '${C_BOLD}source ~/.profile${C_RESET}${C_WARN}' (or similar).${C_RESET}"
    echo
    echo "  ${C_ACTION}To run a backup:${C_RESET}              ${C_BOLD}${BACKUP_SCRIPT_NAME} /path/to/your/data${C_RESET}"
    echo "  ${C_ACTION}To run repository maintenance:${C_RESET}   ${C_BOLD}${MAINTENANCE_SCRIPT_NAME}${C_RESET}"
    echo
}

main
exit 0
{% endcodeblock %}

## The Backup Script: `gdrive-backup`

This script is your day-to-day tool. Its only job is to take a directory you specify and back it up securely to your Google Drive repository.

```bash
#!/bin/bash
set -euo pipefail
if [ -z "${1:-}" ] || [ "$1" == "--help" ]; then echo "Usage: $(basename "$0") /path/to/backup"; exit 1; fi
if [ ! -d "$1" ]; then echo "Error: Path '$1' is not a valid directory." >&2; exit 1; fi
echo "--- Starting Restic Backup for '$1' ---"
restic -r "rclone:gdrive_hub:ResticBackups/my-linux-desktop" --password-file "/home/linaro/.config/restic/gdrive_password" --verbose \
    -o rclone.connections=8 -o rclone.drive-skip-gdocs=true \
    backup "$1" --tag "$(date +%Y%m%d)"
echo "--- Backup Finished ---"
```

#### Line-by-Line Explanation:

1.  `#!/bin/bash`: This is the "shebang." It tells the system to execute this script using the Bash interpreter.
2.  `set -euo pipefail`: This is a crucial line for safety, especially in a backup script.
    * `set -e`: Exit immediately if any command fails. This prevents the script from continuing in an unpredictable state if a step goes wrong.
    * `set -u`: Treat unset variables as an error. This catches typos in variable names.
    * `set -o pipefail`: If a command in a pipeline fails, the entire pipeline's exit status is that of the failed command.
3.  `if [ -z "${1:-}" ] ...`: This is the first input validation.
    * `$1` is the first argument you pass to the script (e.g., in `gdrive-backup /home/linaro/Documents`, `$1` is `/home/linaro/Documents`).
    * This line checks if you provided an argument. If `$1` is empty (`-z`) or if you asked for help (`--help`), it prints the correct usage instructions and exits.
4.  `if [ ! -d "$1" ] ...`: This is the second input validation. It checks if the argument you provided is actually a directory (`-d`). If not, it prints an error and exits.
5.  `echo "--- Starting..."`: A simple message to let you know the backup process has started.
6.  The `restic ...` command is the main event. Let's break down its components:
    * `restic`: The backup program itself.
    * `-r "rclone:gdrive_hub:..."`: Specifies the **r**epository. This tells restic to use the `rclone` backend to connect to your remote named `gdrive_hub` and find the `ResticBackups/my-linux-desktop` folder inside it.
    * `--password-file "..."`: Tells restic where to find the repository password. This is much more secure than typing it every time or saving it in a script.
    * `--verbose`: Makes restic print more detailed information about what it's doing, which files it's scanning, and its progress.
    * `-o rclone.connections=8`: The `-o` flag passes an **o**ption to the rclone backend. This specifically tells rclone to use up to 8 parallel connections to upload data, which can significantly speed up your backup.
    * `-o rclone.drive-skip-gdocs=true`: Another option passed to rclone. This is very important for Google Drive. It tells rclone to ignore Google's proprietary files (Docs, Sheets, Slides) because they can't be downloaded as regular files and would cause errors.
    * `backup "$1"`: This is the core command. It tells restic to perform a `backup` on the directory you provided (`$1`).
    * `--tag "$(date +%Y%m%d)"`: This applies a label, or **tag**, to this specific backup snapshot. The `$(date +%Y%m%d)` part dynamically generates the current date in `YYYYMMDD` format (e.g., `20250616`). This is useful for finding backups from a specific day later on.

## The Maintenance Script: `gdrive-maintenance`

A backup system needs care. This script provides an easy-to-use menu for two critical maintenance tasks: checking for corruption and cleaning up old backups.

```bash
#!/bin/bash
set -euo pipefail
echo "--- Restic Repository Maintenance ---"
echo "Repository: rclone:gdrive_hub:ResticBackups/my-linux-desktop"
echo
PS3="Please choose a maintenance action: "
select action in "Check Integrity" "Prune Old Snapshots" "Exit"; do
    case $action in
        "Check Integrity")
            # ...
            ;;
        "Prune Old Snapshots")
            # ...
            ;;
        "Exit") break;;
        *) echo "Invalid option $REPLY";;
    esac
done
```

#### Explanation of Components:

1.  `select action in ...`: This is a special Bash loop that creates an interactive menu. It displays the options ("Check Integrity", etc.) numbered, and waits for you to type a number and press Enter. The chosen text is put into the `$action` variable.
2.  `case $action in ... esac`: This statement checks the value of the `$action` variable and runs the code for the matching option.

##### **Option 1: Check Integrity**

```bash
restic -r "..." --password-file "..." check
```

* The `restic check` command is vital. It scans the entire repository on Google Drive, verifies all the data structures, and ensures there is no corruption. It confirms that the data you've backed up can be successfully restored. It's a good idea to run this periodically (e.g., once a month).

##### **Option 2: Prune Old Snapshots**

```bash
restic -r "..." --password-file "..." forget \
    --keep-daily 7 --keep-weekly 4 --keep-monthly 12 --keep-yearly 99 --prune
```

* This is a two-part command combined into one (`forget` and `prune`).
* `forget`: This command applies a retention policy. The `--keep-*` flags tell it which backup snapshots to keep:
    * `--keep-daily 7`: Keep the last 7 daily backups (one for each of the last 7 days that has a backup).
    * `--keep-weekly 4`: Keep the last 4 weekly backups (one for each of the last 4 weeks).
    * `--keep-monthly 12`: Keep the last 12 monthly backups.
    * `--keep-yearly 99`: Keep the last 99 yearly backups (effectively forever).
* `--prune`: After `forget` has decided which snapshots to remove, `--prune` does the actual cleanup. It scans the repository and permanently deletes all the data chunks that are no longer needed by any of the remaining snapshots, freeing up space on your Google Drive.
