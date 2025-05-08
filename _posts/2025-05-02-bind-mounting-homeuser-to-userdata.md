---
tags: [aid>linux]
info: aberto.
date: 2025-05-02
type: post
layout: post
published: true
slug: bind-mounting-homeuser-to-userdata
title: 'Bind Mounting /home/user to /userdata'
---
This guide explains how to use mount \--bind to make your user's home directory (/home/user) utilize the storage space on a larger partition mounted at /userdata. This method is transparent to most applications.

While mount \--bind is effective, other methods like symbolic links (ln \-s /userdata /home/user) or changing the home directory path directly in /etc/passwd (usermod \-d /userdata user) exist, each with different implications (e.g., symlinks might not be followed by all applications, usermod \-d changes the canonical path). This guide focuses on the mount \--bind approach.

**Assumptions:**

* Your username is user. **Replace user with your actual username throughout.**  
* Your large partition is mounted at /userdata.  
* You want the actual home directory data to reside in a directory named /userdata.

**🛑 IMPORTANT PREREQUISITES 🛑**

* **BACKUP:** **Before starting, create a complete and verified backup of your /home/user directory.** Mistakes can lead to data loss.  
* **LOG OUT USER:** The user whose home directory is being moved (user) **must be completely logged out** from all graphical sessions and terminal logins.  
* **USE TTY / DIFFERENT USER:** Perform these steps from a text console (TTY) or by logging in as a different administrative user (or root). **Do not perform these steps while logged into the graphical session of the user being modified.**  
  * Press Ctrl+Alt+F3 (or F1-F6) to switch to a TTY and log in there as root or another admin user.

**Steps:**

**1\. Create the Target Directory on /userdata**

* Create the directory on the large partition where the home directory data will actually live.  
  sudo mkdir \-p /userdata

**2\. Set Correct Ownership and Permissions**

* Ensure the new directory belongs to the correct user and group and has standard home directory permissions (700 allows read/write/execute only for the owner).  
  \# Replace user:user with your actual username and primary groupname  
  sudo chown user:user /userdata  
  sudo chmod 700 /userdata

**3\. Copy Data from Old Home to New Location**

* Use rsync to copy all files. \-a preserves permissions, ownership, timestamps, etc. \-X preserves extended attributes, \-A preserves ACLs (if used). \--info=progress2 shows overall progress. The trailing slashes on the paths are important.  
  \# Replace paths if your username or target dir name is different  
  sudo rsync \-aXA \--info=progress2 /home/user/ /userdata/

* This might take time depending on the amount of data.

**4\. Verify Copy Integrity (Recommended)**

* **Crucial:** Before modifying the original directory, verify the copy is complete and accurate. Choose one method:  
  * **Method A: diff (Checks for differences)**  
    \# This command should ideally produce no output if the copy is identical.  
    \# It might list minor differences in temporary files if run immediately after rsync.  
    sudo diff \-qr /home/user/ /userdata/

  * **Method B: rsync Dry Run (Checks what *would* be copied)**  
    \# \-n: dry run, \-i: itemize changes, \-c: checksum (slower but thorough)  
    \# This should ideally report "sending incremental file list" and nothing else.  
    sudo rsync \-naic /home/user/ /userdata/

* Investigate any significant reported differences before proceeding.

**5\. Rename the Original Home Directory (Safety Backup)**

* Rename the original directory. This acts as a temporary backup and frees up the /home/user path for the mount point.  
  sudo mv /home/user /home/user.bak

* **Troubleshooting "Device or resource busy":** If you get this error, ensure user is fully logged out. Use these commands to find processes still using the old directory:  
  \# Option 1: List open files in the directory  
  sudo lsof /home/user.bak  
  \# Option 2: List processes using the filesystem/directory  
  sudo fuser \-vm /home/user.bak  
  \# Option 3: General process check for the user  
  ps aux | grep user

  Identify and terminate any remaining processes belonging to user (e.g., sudo kill \<PID\>).

**6\. Create the Empty Mount Point**

* Recreate the original directory path. This empty directory will serve as the mount point.  
  sudo mkdir /home/user

**7\. Set Ownership of the Empty Mount Point**

* **Crucial:** Ensure this *new, empty* /home/user directory has the correct ownership *before* mounting.  
  sudo chown user:user /home/user

**8\. Test the Bind Mount Manually**

* Perform the bind mount temporarily to check if it works.  
  sudo mount \--bind /userdata /home/user

**9\. Verify the Manual Mount**

* Check the contents of /home/user. It should now show the files from /userdata.  
  ls \-la /home/user

* Check the system's mount list to confirm the bind mount is active.  
  mount | grep /home/user

  You should see a line like /userdata on /home/user type none (rw,bind).

**10\. Make the Bind Mount Persistent (Choose ONE method)**

* **Method A: Using /etc/fstab (Traditional)**  
  * Edit /etc/fstab with a text editor like nano:  
    sudo nano /etc/fstab

  * Add the following line at the end. Use tabs or spaces consistently.  
    \# Bind mount user home directory to userdata partition  
    /userdata  /home/user  none  bind  0  0

  * **Warning:** If /userdata is not available early during boot (e.g., requires drivers/services not yet started), this /etc/fstab entry might cause boot delays or failures. Systemd mount units (Method B) handle dependencies better. Adding the nofail option (bind,nofail) allows booting even if the mount fails, but /home/user might be empty, potentially preventing login or causing application issues. Use nofail with caution for home directories.  
  * Save and close the file (Ctrl+O, Enter, Ctrl+X in nano).  
  * **Test fstab Entry:**  
    sudo umount /home/user  \# Unmount the temporary manual mount  
    sudo mount \-a           \# Mount all entries in fstab  
    mount | grep /home/user \# Verify it mounted correctly via fstab

    If mount \-a gives errors, double-check your /etc/fstab syntax.  
* **Method B: Using Systemd Mount Unit (Modern, Recommended)**  
  * Systemd handles dependencies better, ensuring /userdata is likely ready before attempting the bind mount.  
  * Create a systemd mount unit file. The filename should reflect the mount point path. Convert slashes (/) to dashes (-) and escape dashes properly. For /home/user, a good name is home-user.mount.  
    sudo nano /etc/systemd/system/home-user.mount

  * Paste the following content into the file, adjusting paths if needed:  
    \[Unit\]  
    Description=Bind mount /home/user to /userdata  
    RequiresMountsFor=/userdata  
    After=local-fs.target

    \[Mount\]  
    What=/userdata  
    Where=/home/user  
    Type=none  
    Options=bind

    \[Install\]  
    WantedBy=local-fs.target

    * RequiresMountsFor= helps ensure the source is ready.  
    * After= and WantedBy= integrate it into the boot process.  
  * Save and close the file.  
  * **Enable and Test the Systemd Unit:**  
    sudo umount /home/user  \# Unmount the temporary manual mount if still active  
    \# Enable the unit to start on boot and start it now  
    sudo systemctl enable \--now home-user.mount  
    \# Check the status  
    systemctl status home-user.mount  
    mount | grep /home/user \# Verify it mounted correctly

    If there are errors, check the unit file syntax (systemctl status or journalctl \-u home-user.mount might give clues).

**11\. Log In and Test Thoroughly**

* Log out from the TTY (exit or logout).  
* Switch back to the graphical login screen (e.g., Ctrl+Alt+F1 or Ctrl+Alt+F7).  
* Log in as the user user.  
* Test various applications (browser, file manager, terminal), check file access, create/delete test files, and ensure everything works as expected.  
* Open a terminal within the user's session and run df \-h /home/user. The output should show the disk space statistics for the /userdata partition, confirming the redirection is working.  
* **Reboot the system** and log in again to ensure the persistent mount (fstab or systemd) works correctly after a full restart.

**12\. Clean Up (Optional \- Use Caution\!)**

* **Only after extensive testing (including reboots)** and confirming everything works perfectly, you can remove the backup directory.  
* **🛑 Double-check you are deleting the correct directory (.bak)\! 🛑**  
  \# Perform this from a TTY logged in as root or another admin user  
  sudo rm \-rf /home/user.bak

You have now successfully redirected your /home/user directory to use the storage space on /userdata using a persistent bind mount.

# bash script

{% codeblock bash %}
#!/bin/bash

# Script 1 (Revised): Implementing the Tutorial for /home/user to a new data location
# URL Source: https://ib.bsb.br/bind-mounting-homeuser-to-userdata/
# Published Time: 2025-05-02T00:00:00+00:00

set -uo pipefail

# --- Configuration (from script arguments and derivations) ---
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <username> <new_data_path_for_home>"
    echo "  <username>: The username whose home directory is being moved."
    echo "  <new_data_path_for_home>: The full path on the larger partition where the home directory data will actually live."
    echo "                            Example: /mnt/data/johndoe_homedata OR /userdata (if /userdata is dedicated to this user's home data)"
    echo ""
    echo "Example: $0 johndoe /mnt/data/johndoe_homedata"
    exit 1
fi

TARGET_USERNAME="$1"
NEW_DATA_LOCATION="$2" # This is where the actual data will reside on the larger partition.
                       # Tutorial example: data lives directly in /userdata.
                       # For /home/user -> /userdata/user_data_folder, set this to /userdata/user_data_folder

TARGET_USER_PRIMARY_GROUP=$(id -gn "${TARGET_USERNAME}")
if [ $? -ne 0 ] || [ -z "${TARGET_USER_PRIMARY_GROUP}" ]; then
    echo "Error: Could not determine primary group for user ${TARGET_USERNAME}."
    echo "Please ensure the user exists."
    exit 1
fi

OLD_HOME_DIR="/home/${TARGET_USERNAME}"

echo "--- Script Configuration ---"
echo "Target Username:            ${TARGET_USERNAME}"
echo "Primary Group:              ${TARGET_USER_PRIMARY_GROUP}"
echo "Old Home Directory Path:    ${OLD_HOME_DIR}"
echo "New Data Location Path:     ${NEW_DATA_LOCATION}"
echo "----------------------------"
echo ""


# --- Helper Functions ---
ask_confirmation() {
    while true; do
        read -r -p "$1 (yes/no): " choice
        case "$choice" in
            [Yy][Ee][Ss] ) return 0;;
            [Nn][Oo] ) return 1;;
            * ) echo "Please answer yes or no.";;
        esac
    done
}

check_root() {
    if [ "$(id -u)" -ne 0 ]; then
        echo "This script needs to be run as root or with sudo."
        exit 1
    fi
}

# --- Tutorial Steps as Functions ---

step_0_prerequisites() {
    echo "--- Step 0: IMPORTANT PREREQUISITES ---"
    echo "🛑 BEFORE YOU PROCEED: 🛑"
    echo "1. BACKUP: Have you created a COMPLETE AND VERIFIED backup of ${OLD_HOME_DIR}?"
    echo "2. LOG OUT USER: Is the user '${TARGET_USERNAME}' COMPLETELY LOGGED OUT from all graphical and terminal sessions?"
    echo "3. USE TTY / DIFFERENT USER: Are you running this script from a TTY (e.g., Ctrl+Alt+F3) or as a different administrative user (NOT logged into ${TARGET_USERNAME}'s graphical session)?"

    if ! ask_confirmation "Have all prerequisites been met?"; then
        echo "Aborting. Please ensure all prerequisites are met."
        exit 1
    fi
    echo "Prerequisites acknowledged."
}

step_1_create_target_directory() {
    echo "--- Step 1: Create the Target Directory on ${NEW_DATA_LOCATION} ---"
    if [ -d "${NEW_DATA_LOCATION}" ]; then
        echo "Directory ${NEW_DATA_LOCATION} already exists."
        if ! ask_confirmation "Do you want to proceed using the existing directory ${NEW_DATA_LOCATION}?"; then
            echo "Aborting. Please check the target directory."
            exit 1
        fi
    else
        echo "Creating directory: ${NEW_DATA_LOCATION}"
        mkdir -p "${NEW_DATA_LOCATION}"
        if [ $? -ne 0 ]; then echo "Error creating ${NEW_DATA_LOCATION}. Aborting."; exit 1; fi
    fi
    echo "Target directory ready: ${NEW_DATA_LOCATION}"
}

step_2_set_ownership_permissions() {
    echo "--- Step 2: Set Correct Ownership and Permissions for ${NEW_DATA_LOCATION} ---"
    echo "Setting ownership to ${TARGET_USERNAME}:${TARGET_USER_PRIMARY_GROUP} for ${NEW_DATA_LOCATION}"
    chown "${TARGET_USERNAME}:${TARGET_USER_PRIMARY_GROUP}" "${NEW_DATA_LOCATION}"
    if [ $? -ne 0 ]; then echo "Error setting ownership for ${NEW_DATA_LOCATION}. Aborting."; exit 1; fi

    echo "Setting permissions to 700 for ${NEW_DATA_LOCATION} (as per tutorial for user data store)"
    chmod 700 "${NEW_DATA_LOCATION}"
    if [ $? -ne 0 ]; then echo "Error setting permissions for ${NEW_DATA_LOCATION}. Aborting."; exit 1; fi
    echo "Ownership and permissions set for ${NEW_DATA_LOCATION}."
}

step_3_copy_data() {
    echo "--- Step 3: Copy Data from ${OLD_HOME_DIR} to ${NEW_DATA_LOCATION} ---"
    if [ ! -d "${OLD_HOME_DIR}" ]; then
        echo "Error: Original home directory ${OLD_HOME_DIR} does not exist. Cannot copy data."
        echo "This could happen if the script was run before, or the username is incorrect."
        exit 1
    fi
    echo "This might take a while depending on the data size."
    if ! ask_confirmation "Proceed with rsync from ${OLD_HOME_DIR}/ to ${NEW_DATA_LOCATION}/?"; then
        echo "Aborting data copy."
        exit 1
    fi
    rsync -aXA --info=progress2 "${OLD_HOME_DIR}/" "${NEW_DATA_LOCATION}/"
    if [ $? -ne 0 ]; then echo "Error during rsync. Please check messages. Aborting."; exit 1; fi
    echo "Data copy completed."
}

step_4_verify_copy() {
    echo "--- Step 4: Verify Copy Integrity (Recommended) ---"
    echo "Choose a method to verify the copy:"
    echo "  A) diff -qr (shows differences, ideally no output)"
    echo "  B) rsync -naic (dry run, shows what would be copied, ideally nothing significant)"
    read -r -p "Verification method (A/B, or S to skip): " method_choice

    case "$method_choice" in
        [Aa])
            echo "Running: diff -qr \"${OLD_HOME_DIR}/\" \"${NEW_DATA_LOCATION}/\""
            diff -qr "${OLD_HOME_DIR}/" "${NEW_DATA_LOCATION}/"
            echo "Diff command finished. Review output for any significant differences."
            ;;
        [Bb])
            echo "Running: rsync -naic \"${OLD_HOME_DIR}/\" \"${NEW_DATA_LOCATION}/\""
            rsync -naic "${OLD_HOME_DIR}/" "${NEW_DATA_LOCATION}/"
            echo "Rsync dry run finished. Review output."
            ;;
        [Ss])
            echo "Skipping verification. This is not recommended."
            ;;
        *)
            echo "Invalid choice. Skipping verification."
            ;;
    esac
    if ! ask_confirmation "Is the copy verified and correct to proceed?"; then
        echo "Aborting. Please verify the copy manually."
        exit 1
    fi
}

step_5_rename_original_home() {
    echo "--- Step 5: Rename the Original Home Directory (Safety Backup) ---"
    local ORIGINAL_HOME_BACKUP="${OLD_HOME_DIR}.bak"
    echo "Renaming ${OLD_HOME_DIR} to ${ORIGINAL_HOME_BACKUP}"
    if [ -d "${ORIGINAL_HOME_BACKUP}" ]; then
        echo "Error: ${ORIGINAL_HOME_BACKUP} already exists. Please handle this manually."
        exit 1
    fi
    if [ ! -d "${OLD_HOME_DIR}" ]; then
        echo "Error: ${OLD_HOME_DIR} does not exist or is not a directory. Cannot rename."
        echo "This might happen if the script was partially run before. Please check."
        exit 1
    fi
    mv "${OLD_HOME_DIR}" "${ORIGINAL_HOME_BACKUP}"
    if [ $? -ne 0 ]; then
        echo "Error renaming ${OLD_HOME_DIR}. 'Device or resource busy?'"
        echo "Ensure user ${TARGET_USERNAME} is fully logged out."
        echo "You can try to find processes using:"
        echo "  sudo lsof ${OLD_HOME_DIR}"
        echo "  sudo fuser -vm ${OLD_HOME_DIR}"
        echo "  ps aux | grep ${TARGET_USERNAME}"
        echo "Aborting."
        exit 1
    fi
    echo "Original home directory renamed to ${ORIGINAL_HOME_BACKUP}."
}

step_6_create_empty_mount_point() {
    echo "--- Step 6: Create the Empty Mount Point ---"
    echo "Creating empty directory: ${OLD_HOME_DIR}"
    mkdir "${OLD_HOME_DIR}"
    if [ $? -ne 0 ]; then echo "Error creating empty mount point ${OLD_HOME_DIR}. Aborting."; exit 1; fi
    echo "Empty mount point ${OLD_HOME_DIR} created."
}

step_7_set_mount_point_ownership() {
    echo "--- Step 7: Set Ownership of the Empty Mount Point ${OLD_HOME_DIR} ---"
    echo "Setting ownership to ${TARGET_USERNAME}:${TARGET_USER_PRIMARY_GROUP} for ${OLD_HOME_DIR}"
    chown "${TARGET_USERNAME}:${TARGET_USER_PRIMARY_GROUP}" "${OLD_HOME_DIR}"
    if [ $? -ne 0 ]; then echo "Error setting ownership for ${OLD_HOME_DIR}. Aborting."; exit 1; fi
    echo "Ownership set for empty mount point ${OLD_HOME_DIR}."
}

step_8_test_bind_mount() {
    echo "--- Step 8: Test the Bind Mount Manually ---"
    echo "Performing: mount --bind \"${NEW_DATA_LOCATION}\" \"${OLD_HOME_DIR}\""
    mount --bind "${NEW_DATA_LOCATION}" "${OLD_HOME_DIR}"
    if [ $? -ne 0 ]; then echo "Error performing bind mount. Aborting."; exit 1; fi
    echo "Bind mount command executed."
}

step_9_verify_manual_mount() {
    echo "--- Step 9: Verify the Manual Mount ---"
    echo "Contents of ${OLD_HOME_DIR} after mount:"
    ls -la "${OLD_HOME_DIR}"
    echo ""
    echo "Checking mount details for target ${OLD_HOME_DIR} using findmnt:"
    local mount_info
    mount_info=$(findmnt -n -o FSTYPE,OPTIONS -S "${NEW_DATA_LOCATION}" -T "${OLD_HOME_DIR}")

    if [[ -n "$mount_info" && "$mount_info" == *"none"* && "$mount_info" == *"bind"* ]]; then
        echo "Mount verified via findmnt: ${mount_info}"
    else
        echo "Mount verification via findmnt failed or output unexpected."
        echo "findmnt output: '$mount_info'"
        echo "Fallback: Checking 'mount' output:"
        # Normalize paths for grep by removing potential duplicate slashes, though usually not an issue with these vars
        local normalized_new_data_location="${NEW_DATA_LOCATION//\/\//\/}"
        local normalized_old_home_dir="${OLD_HOME_DIR//\/\//\/}"
        if mount | grep -qE "\s${normalized_new_data_location}\s+on\s+${normalized_old_home_dir}\s+type\s+none\s+\(.*bind.*\)"; then
            echo "Mount verified via fallback 'mount | grep'."
        else
            echo "Mount verification failed with fallback 'mount | grep' as well."
            echo "Expected something like: '${normalized_new_data_location} on ${normalized_old_home_dir} type none (rw,bind)' or similar."
            echo "Please check manually. Aborting persistent setup."
            # Attempt to unmount before exiting if mount failed verification
            umount "${OLD_HOME_DIR}" 2>/dev/null || true
            exit 1
        fi
    fi
    echo "Manual mount verified."
}

step_10_make_persistent() {
    echo "--- Step 10: Make the Bind Mount Persistent ---"
    echo "Choose a method for persistence:"
    echo "  A) /etc/fstab (Traditional)"
    echo "  B) Systemd Mount Unit (Modern, Recommended)"
    read -r -p "Persistence method (A/B): " persist_choice

    local FSTAB_ENTRY="${NEW_DATA_LOCATION} ${OLD_HOME_DIR} none bind 0 0"
    local SYSTEMD_UNIT_NAME="home-${TARGET_USERNAME}.mount" # As per tutorial suggestion for /home/user
    local SYSTEMD_UNIT_FILE="/etc/systemd/system/${SYSTEMD_UNIT_NAME}"

    echo "Unmounting temporary manual mount: umount \"${OLD_HOME_DIR}\""
    umount "${OLD_HOME_DIR}"
    if [ $? -ne 0 ]; then
        echo "Warning: Could not unmount ${OLD_HOME_DIR}. This might interfere with testing the persistent mount."
        echo "If the next step fails, it might be because the mount point is still in use from the manual test."
    fi

    case "$persist_choice" in
        [Aa])
            echo "Adding to /etc/fstab: ${FSTAB_ENTRY}"
            # Check for existing mount point in fstab to avoid duplicates
            if grep -qE "^\s*[^#].*\s+${OLD_HOME_DIR}\s+" /etc/fstab; then
                echo "An entry for ${OLD_HOME_DIR} might already exist in /etc/fstab. Please check manually."
                cat /etc/fstab | grep "${OLD_HOME_DIR}"
                if ! ask_confirmation "Proceed with adding the new line anyway?"; then
                    echo "Aborting fstab modification."
                    exit 1
                fi
            fi
            # Ensure there's a newline before adding the entry, if the file doesn't end with one
            if [ -n "$(tail -c1 /etc/fstab)" ]; then echo "" >> /etc/fstab; fi
            echo -e "\n# Bind mount ${TARGET_USERNAME} home directory to ${NEW_DATA_LOCATION} (added by script)\n${FSTAB_ENTRY}" >> /etc/fstab
            echo "Testing fstab entry: mount \"${OLD_HOME_DIR}\""
            mount "${OLD_HOME_DIR}" # Test specific mount from fstab
            if [ $? -ne 0 ]; then echo "Error during 'mount \"${OLD_HOME_DIR}\"'. Check /etc/fstab syntax. Aborting."; exit 1; fi

            local mount_info_fstab
            mount_info_fstab=$(findmnt -n -o FSTYPE,OPTIONS -S "${NEW_DATA_LOCATION}" -T "${OLD_HOME_DIR}")
            if [[ -n "$mount_info_fstab" && "$mount_info_fstab" == *"none"* && "$mount_info_fstab" == *"bind"* ]]; then
                echo "Mount via fstab verified: ${mount_info_fstab}"
            else
                 echo "Mount via fstab failed verification with findmnt. Please check /etc/fstab and system logs. Aborting."; exit 1;
            fi
            echo "/etc/fstab method configured and tested."
            echo "WARNING: If ${NEW_DATA_LOCATION} is not available early during boot (e.g., on a LUKS encrypted partition not yet unlocked, or a slow-to-mount network share), this might cause boot delays or failures."
            echo "Consider using the 'nofail' option in /etc/fstab (e.g., 'bind,nofail') WITH CAUTION for home directories, as it might lead to an empty home if the mount fails."
            ;;
        [Bb])
            echo "Creating systemd mount unit: ${SYSTEMD_UNIT_FILE}"
            local underlying_mount_for_new_data
            underlying_mount_for_new_data=$(df --output=target "${NEW_DATA_LOCATION}" 2>/dev/null | tail -n 1)

            if [ -z "${underlying_mount_for_new_data}" ] || [ ! -d "${underlying_mount_for_new_data}" ] || [ "${underlying_mount_for_new_data}" = "-" ]; then
                echo "Warning: Could not reliably determine the underlying mount point for ${NEW_DATA_LOCATION} using 'df'."
                echo "Using ${NEW_DATA_LOCATION} directly for RequiresMountsFor in systemd unit. This is usually fine."
                underlying_mount_for_new_data="${NEW_DATA_LOCATION}"
            else
                echo "Determined underlying mount point for ${NEW_DATA_LOCATION} as '${underlying_mount_for_new_data}' for systemd unit."
            fi

            cat > "${SYSTEMD_UNIT_FILE}" << EOF
[Unit]
Description=Bind mount ${OLD_HOME_DIR} to ${NEW_DATA_LOCATION}
# Documentation: man systemd.mount
# Ensures that the filesystem providing the source directory is mounted.
RequiresMountsFor=${underlying_mount_for_new_data}
# After these targets are reached. local-fs.target is for local file systems.
# remote-fs.target might be relevant if NEW_DATA_LOCATION is on a network filesystem.
After=local-fs.target remote-fs.target

[Mount]
What=${NEW_DATA_LOCATION}
Where=${OLD_HOME_DIR}
Type=none
Options=bind

[Install]
WantedBy=local-fs.target remote-fs.target
EOF
            echo "Reloading systemd daemon, enabling and starting the unit."
            systemctl daemon-reload
            if [ $? -ne 0 ]; then echo "Error during systemctl daemon-reload. Aborting."; exit 1; fi
            systemctl enable --now "${SYSTEMD_UNIT_NAME}"
            if [ $? -ne 0 ]; then echo "Error enabling/starting systemd unit ${SYSTEMD_UNIT_NAME}. Check status. Aborting."; exit 1; fi

            echo "Checking status of ${SYSTEMD_UNIT_NAME}:"
            systemctl status "${SYSTEMD_UNIT_NAME}" --no-pager
            local mount_info_systemd
            mount_info_systemd=$(findmnt -n -o FSTYPE,OPTIONS -S "${NEW_DATA_LOCATION}" -T "${OLD_HOME_DIR}")

            if systemctl is-active -q "${SYSTEMD_UNIT_NAME}" && [[ -n "$mount_info_systemd" && "$mount_info_systemd" == *"none"* && "$mount_info_systemd" == *"bind"* ]]; then
                echo "Systemd mount unit active and verified: ${mount_info_systemd}"
            else
                 echo "Systemd mount unit failed or mount not active/verified. Please check status and journal (journalctl -u ${SYSTEMD_UNIT_NAME}). Aborting."; exit 1;
            fi
            echo "Systemd mount unit configured and tested."
            ;;
        *)
            echo "Invalid choice. No persistent method configured. The mount is currently not active."
            exit 1
            ;;
    esac
}

step_11_test_thoroughly() {
    echo "--- Step 11: Log In and Test Thoroughly ---"
    echo "The script has completed the mount setup."
    echo "NOW, YOU MUST:"
    echo "1. Log out from this TTY/admin session."
    echo "2. Switch to the graphical login screen (e.g., Ctrl+Alt+F1 or F7)."
    echo "3. Log in as the user '${TARGET_USERNAME}'."
    echo "4. Test various applications, file access, create/delete files."
    echo "5. Open a terminal as '${TARGET_USERNAME}' and run 'df -h \"${OLD_HOME_DIR}\"' - it should show stats for the partition hosting ${NEW_DATA_LOCATION}."
    echo "6. CRITICAL: Reboot the system and log in again as '${TARGET_USERNAME}' to ensure the persistent mount works after a full restart."
}

step_12_cleanup() {
    echo "--- Step 12: Clean Up (Optional - Use Caution!) ---"
    local ORIGINAL_HOME_BACKUP="${OLD_HOME_DIR}.bak"
    echo "After extensive testing (including reboots) and confirming everything works perfectly,"
    echo "you can remove the backup directory: ${ORIGINAL_HOME_BACKUP}"
    echo "🛑 Double-check you are deleting the correct directory! 🛑"
    echo "Command to run MANUALLY from a TTY as root/admin: rm -rf \"${ORIGINAL_HOME_BACKUP}\""
}

# --- Main Script Execution ---
check_root

echo "This script will guide you through bind mounting ${OLD_HOME_DIR} to use storage from ${NEW_DATA_LOCATION}."
echo "It is based on the tutorial from https://ib.bsb.br/bind-mounting-homeuser-to-userdata/"
echo "Please ensure you have read and understood the implications of this operation."
echo ""
if ! ask_confirmation "Do you understand the risks and want to proceed with configuring for user '${TARGET_USERNAME}' and data location '${NEW_DATA_LOCATION}'?"; then
    echo "Aborting."
    exit 0
fi

step_0_prerequisites
step_1_create_target_directory
step_2_set_ownership_permissions
step_3_copy_data
step_4_verify_copy
step_5_rename_original_home
step_6_create_empty_mount_point
step_7_set_mount_point_ownership
step_8_test_bind_mount
step_9_verify_manual_mount
step_10_make_persistent
step_11_test_thoroughly
step_12_cleanup

echo ""
echo "Script finished. PLEASE FOLLOW THE TESTING AND CLEANUP INSTRUCTIONS CAREFULLY."
echo "Remember to reboot and test thoroughly before considering removal of ${OLD_HOME_DIR}.bak."
{% endcodeblock %}

# standalone bash script for fixing step 9 issues

```
#!/bin/bash

# --- Configuration Variables ---
# These values are based on the information provided in the original query.
OLD_HOME_DIR="/home/linaro"
NEW_DATA_LOCATION="/mnt/mSATA/linaro"
TARGET_USERNAME="linaro"

# --- Helper Functions ---

# Function to check if the script is run as root
check_root() {
    if [ "$(id -u)" -ne 0 ]; then
        echo "ERROR: This script must be run as root. Please use sudo." >&2
        exit 1
    fi
}

# Function to ask for user confirmation
ask_confirmation() {
    local prompt_message="$1"
    local response
    while true; do
        # Ensure prompt_message is displayed correctly, even if it contains spaces
        read -r -p "${prompt_message} (yes/no): " response
        case "$response" in
            [Yy][Ee][Ss]|[Yy])
                return 0 # True (success)
                ;;
            [Nn][Oo]|[Nn])
                return 1 # False (failure)
                ;;
            *)
                echo "Please answer yes or no."
                ;;
        esac
    done
}

# --- Main Function to Make Bind Mount Persistent ---
step_10_make_persistent() {
    echo "--- Step 10: Make the Bind Mount Persistent ---"
    echo "This script will configure the bind mount to be persistent across reboots."
    echo "It assumes that:"
    echo "  1. The source data directory ('${NEW_DATA_LOCATION}') exists and contains the data."
    echo "  2. The target mount point directory ('${OLD_HOME_DIR}') exists and is empty (or ready to be mounted over)."
    echo ""
    echo "Target user: ${TARGET_USERNAME}"
    echo "Old home directory (mount point): ${OLD_HOME_DIR}"
    echo "New data location (source for bind mount): ${NEW_DATA_LOCATION}"
    echo ""

    echo "Choose a method for persistence:"
    echo "  A) /etc/fstab (Traditional)"
    echo "  B) Systemd Mount Unit (Modern, Recommended for systems using systemd)"
    read -r -p "Persistence method (A/B): " persist_choice

    # Define systemd unit name and file path locally based on TARGET_USERNAME.
    # This aligns with common practice for user-specific home directory mounts.
    local FSTAB_ENTRY="${NEW_DATA_LOCATION} ${OLD_HOME_DIR} none bind 0 0"
    local SYSTEMD_UNIT_NAME="home-${TARGET_USERNAME}.mount"
    local SYSTEMD_UNIT_FILE="/etc/systemd/system/${SYSTEMD_UNIT_NAME}"

    echo ""
    echo "Checking if '${OLD_HOME_DIR}' is currently mounted..."
    if mountpoint -q "${OLD_HOME_DIR}"; then
        echo "'${OLD_HOME_DIR}' is currently mounted. Attempting to unmount it..."
        umount "${OLD_HOME_DIR}"
        if [ $? -ne 0 ]; then
            echo "WARNING: Could not unmount ${OLD_HOME_DIR}."
            echo "This might be because it's in use or due to other issues."
            echo "Continuing might lead to problems with the persistent mount setup."
            if ! ask_confirmation "Attempt to proceed with persistence setup anyway?"; then
                echo "Aborting persistence setup due to unmount failure."
                exit 1
            fi
            echo "Proceeding despite unmount warning. Ensure '${OLD_HOME_DIR}' is not actively used by another process."
        else
            echo "'${OLD_HOME_DIR}' unmounted successfully."
        fi
    else
        echo "'${OLD_HOME_DIR}' is not currently a mount point. No unmount needed before setting up persistence."
    fi
    echo ""

    case "$persist_choice" in
        [Aa])
            echo "--- Configuring persistence via /etc/fstab ---"
            echo "Proposed fstab entry: ${FSTAB_ENTRY}"

            if grep -qE "^\s*[^#].*\s+${OLD_HOME_DIR}\s+" /etc/fstab; then
                echo "WARNING: An entry for '${OLD_HOME_DIR}' might already exist in /etc/fstab:"
                grep --color=always -E "^\s*[^#].*\s+${OLD_HOME_DIR}\s+" /etc/fstab
                if ! ask_confirmation "Proceed with adding the new line anyway (this could lead to duplicates)?"; then
                    echo "Aborting fstab modification."
                    exit 1
                fi
            fi

            local FSTAB_BACKUP_FILE="/etc/fstab.bak.$(date +%Y%m%d-%H%M%S)"
            echo "Backing up /etc/fstab to '${FSTAB_BACKUP_FILE}'..."
            if cp /etc/fstab "${FSTAB_BACKUP_FILE}"; then
                echo "Backup successful."
            else
                echo "ERROR: Failed to backup /etc/fstab. Aborting."
                exit 1
            fi

            echo "Adding entry to /etc/fstab..."
            # Ensure there's a newline before adding the entry, if the file doesn't end with one
            if [ -n "$(tail -c1 /etc/fstab)" ]; then printf "\n" >> /etc/fstab; fi
            printf "# Bind mount for %s home directory (%s to %s) - Added by script on %s\n%s\n" \
                "${TARGET_USERNAME}" "${NEW_DATA_LOCATION}" "${OLD_HOME_DIR}" "$(date)" "${FSTAB_ENTRY}" >> /etc/fstab
            echo "Entry added."

            echo "Testing fstab entry by attempting to mount '${OLD_HOME_DIR}'..."
            mount "${OLD_HOME_DIR}" # This will use /etc/fstab to find the entry
            if [ $? -ne 0 ]; then
                echo "ERROR: 'mount \"${OLD_HOME_DIR}\"' failed. Check /etc/fstab syntax and ensure '${NEW_DATA_LOCATION}' is accessible."
                echo "You may need to restore /etc/fstab from '${FSTAB_BACKUP_FILE}'. Aborting."
                exit 1
            fi
            echo "Mount test successful."

            local mount_info_fstab
            mount_info_fstab=$(findmnt -n -o FSTYPE,OPTIONS -S "${NEW_DATA_LOCATION}" -T "${OLD_HOME_DIR}")
            if [[ -n "$mount_info_fstab" && "$mount_info_fstab" == *"none"* && "$mount_info_fstab" == *"bind"* ]]; then
                echo "Mount via fstab verified with findmnt: ${mount_info_fstab}"
            else
                 echo "ERROR: Mount via fstab failed verification with findmnt. Output: '${mount_info_fstab}'"
                 echo "Please check /etc/fstab, system logs, and ensure '${OLD_HOME_DIR}' is correctly mounted."
                 echo "You may need to restore /etc/fstab from '${FSTAB_BACKUP_FILE}'. Aborting."
                 exit 1
            fi
            echo "/etc/fstab method configured and tested successfully."
            echo "WARNING: If '${NEW_DATA_LOCATION}' is on a filesystem that is not available early during boot"
            echo "(e.g., encrypted partition not yet unlocked, network share), this fstab entry might cause boot delays or failures."
            echo "Consider using the 'nofail' option in /etc/fstab (e.g., 'none bind,nofail 0 0') WITH CAUTION for home directories,"
            echo "as it might lead to an empty home if the mount fails silently."
            ;;
        [Bb])
            echo "--- Configuring persistence via systemd mount unit ---"
            echo "Systemd unit name: ${SYSTEMD_UNIT_NAME}"
            echo "Systemd unit file: ${SYSTEMD_UNIT_FILE}"

            # Determine the mount point that provides NEW_DATA_LOCATION for RequiresMountsFor
            local actual_mount_path_for_dependency
            actual_mount_path_for_dependency=$(findmnt -n -o TARGET --target "${NEW_DATA_LOCATION}")

            if [ -z "${actual_mount_path_for_dependency}" ] || [ ! -d "${actual_mount_path_for_dependency}" ]; then
                echo "WARNING: Could not reliably determine the underlying mount point for '${NEW_DATA_LOCATION}' using 'findmnt'."
                echo "This can happen if '${NEW_DATA_LOCATION}' is not on a standard mount or is deeply nested."
                echo "Falling back to using '${NEW_DATA_LOCATION}' itself for 'RequiresMountsFor'."
                echo "If '${NEW_DATA_LOCATION}' is not the actual mount point of its filesystem (e.g., it's a directory on '/data' which is mounted),"
                echo "this systemd unit might not have the correct dependency ordering. Manual adjustment may be needed."
                actual_mount_path_for_dependency="${NEW_DATA_LOCATION}"
            else
                echo "Determined underlying mount point for '${NEW_DATA_LOCATION}' as '${actual_mount_path_for_dependency}' for systemd unit's RequiresMountsFor."
            fi

            # Ensure the target directory for the unit file exists
            mkdir -p "$(dirname "${SYSTEMD_UNIT_FILE}")"

            if [ -f "${SYSTEMD_UNIT_FILE}" ]; then
                local SYSTEMD_UNIT_BACKUP_FILE="${SYSTEMD_UNIT_FILE}.bak.$(date +%Y%m%d-%H%M%S)"
                echo "WARNING: Systemd unit file '${SYSTEMD_UNIT_FILE}' already exists."
                echo "Backing it up to '${SYSTEMD_UNIT_BACKUP_FILE}' before overwriting..."
                if cp "${SYSTEMD_UNIT_FILE}" "${SYSTEMD_UNIT_BACKUP_FILE}"; then
                    echo "Backup successful."
                else
                    echo "ERROR: Failed to backup existing systemd unit file. Aborting."
                    exit 1
                fi
            fi

            echo "Creating systemd mount unit file '${SYSTEMD_UNIT_FILE}'..."
            # Note: For home directories, local-fs.target is usually appropriate.
            # If NEW_DATA_LOCATION were on a network share, remote-fs.target and network-online.target
            # would be more relevant for After= and WantedBy=.
            cat > "${SYSTEMD_UNIT_FILE}" << EOF
[Unit]
Description=Bind mount ${OLD_HOME_DIR} to ${NEW_DATA_LOCATION} for user ${TARGET_USERNAME}
Documentation=man:systemd.mount(5) man:systemd.special(7)
# Ensures that the filesystem providing the source directory (${NEW_DATA_LOCATION}) is mounted.
# This should be the actual mount point path where NEW_DATA_LOCATION resides.
RequiresMountsFor=${actual_mount_path_for_dependency}
# Attempt to mount after the underlying filesystem is available.
After=local-fs.target

[Mount]
What=${NEW_DATA_LOCATION}
Where=${OLD_HOME_DIR}
Type=none
Options=bind

[Install]
WantedBy=local-fs.target
EOF
            echo "Systemd unit file created."

            echo "Reloading systemd daemon..."
            systemctl daemon-reload
            if [ $? -ne 0 ]; then echo "ERROR: systemctl daemon-reload failed. Aborting."; exit 1; fi
            echo "Daemon reloaded."

            echo "Enabling systemd unit '${SYSTEMD_UNIT_NAME}' (to start on boot)..."
            systemctl enable "${SYSTEMD_UNIT_NAME}"
            if [ $? -ne 0 ]; then echo "ERROR: Failed to enable systemd unit '${SYSTEMD_UNIT_NAME}'. Check logs. Aborting."; exit 1; fi
            echo "Unit enabled."

            echo "Starting systemd unit '${SYSTEMD_UNIT_NAME}' now..."
            systemctl start "${SYSTEMD_UNIT_NAME}"
            if [ $? -ne 0 ]; then
                echo "ERROR: Failed to start systemd unit '${SYSTEMD_UNIT_NAME}'."
                echo "Check status with: systemctl status '${SYSTEMD_UNIT_NAME}'"
                echo "Check journal with: journalctl -u '${SYSTEMD_UNIT_NAME}'"
                echo "Aborting."
                exit 1
            fi
            echo "Unit started."

            echo "Verifying status of '${SYSTEMD_UNIT_NAME}'..."
            if systemctl is-active -q "${SYSTEMD_UNIT_NAME}"; then
                echo "Systemd unit '${SYSTEMD_UNIT_NAME}' is active."
            else
                echo "ERROR: Systemd unit '${SYSTEMD_UNIT_NAME}' is NOT active after start."
                echo "Check status with: systemctl status '${SYSTEMD_UNIT_NAME}'"
                echo "Check journal with: journalctl -u '${SYSTEMD_UNIT_NAME}'"
                echo "Aborting."
                exit 1
            fi

            local mount_info_systemd
            mount_info_systemd=$(findmnt -n -o FSTYPE,OPTIONS -S "${NEW_DATA_LOCATION}" -T "${OLD_HOME_DIR}")
            if [[ -n "$mount_info_systemd" && "$mount_info_systemd" == *"none"* && "$mount_info_systemd" == *"bind"* ]]; then
                echo "Systemd mount unit verified with findmnt: ${mount_info_systemd}"
            else
                 echo "ERROR: Systemd mount failed verification with findmnt. Output: '${mount_info_systemd}'"
                 echo "Please check system logs and unit status. Aborting."
                 exit 1
            fi
            echo "Systemd mount unit configured, started, and tested successfully."
            ;;
        *)
            echo "Invalid choice. No persistent method configured."
            echo "If '${OLD_HOME_DIR}' was unmounted, it remains unmounted."
            exit 1
            ;;
    esac
}

# --- Main Script Execution ---
echo "Standalone Script for Making a Bind Mount Persistent"
echo "===================================================="
echo "This script configures a persistent bind mount using /etc/fstab or a systemd unit."
echo "It assumes the source data directory and target mount point directory already exist."
echo ""

# 1. Check if running as root
check_root
echo "Running as root. Proceeding..."
echo ""

# 2. Execute the persistence setup
step_10_make_persistent

echo ""
echo "--- Script Finished Successfully ---"
echo "The chosen persistence method has been configured and initially tested."
echo "IMPORTANT: Thorough testing is now required:"
echo "1. If this is a home directory for '${TARGET_USERNAME}', log out and log back in as that user."
echo "2. Verify all file access, application functionality, and create/delete test files."
echo "3. CRITICAL: Reboot the system entirely."
echo "4. After reboot, log in again as '${TARGET_USERNAME}' (if applicable) and repeat all verifications."
echo "   Ensure 'df -h \"${OLD_HOME_DIR}\"' shows usage from the filesystem hosting '${NEW_DATA_LOCATION}'."
echo ""
echo "If issues arise:"
echo "  - For fstab: Check '/etc/fstab' and system boot logs. Restore from '${FSTAB_BACKUP_FILE:-/etc/fstab.bak...}' if needed."
echo "  - For systemd: Check 'systemctl status ${SYSTEMD_UNIT_NAME:-home-$TARGET_USERNAME.mount}' and 'journalctl -u ${SYSTEMD_UNIT_NAME:-home-$TARGET_USERNAME.mount}'."
echo "    Restore the unit file from '${SYSTEMD_UNIT_FILE:-/etc/systemd/system/home-$TARGET_USERNAME.mount}.bak...' if needed."

exit 0
```
