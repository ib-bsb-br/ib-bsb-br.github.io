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

# --- Configuration ---
# !!! IMPORTANT: SET THESE VARIABLES BEFORE RUNNING !!!
TARGET_USERNAME="user"                     # Replace with the actual username
TARGET_USER_PRIMARY_GROUP="user"           # Replace with the user's primary group
OLD_HOME_DIR="/home/${TARGET_USERNAME}"
# This is where the actual data will reside on the larger partition.
# The tutorial implies /userdata is the mount point of the large partition,
# and the user's data is copied directly into it.
NEW_DATA_LOCATION="/userdata" # Tutorial example: data lives directly in /userdata
                              # For /home/user -> /userdata/user_data_folder, set this to /userdata/user_data_folder

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
    ORIGINAL_HOME_BACKUP="${OLD_HOME_DIR}.bak"
    echo "Renaming ${OLD_HOME_DIR} to ${ORIGINAL_HOME_BACKUP}"
    if [ -d "${ORIGINAL_HOME_BACKUP}" ]; then
        echo "Error: ${ORIGINAL_HOME_BACKUP} already exists. Please handle this manually."
        exit 1
    fi
    mv "${OLD_HOME_DIR}" "${ORIGINAL_HOME_BACKUP}"
    if [ $? -ne 0 ]; then
        echo "Error renaming ${OLD_HOME_DIR}. 'Device or resource busy?'"
        echo "Ensure user ${TARGET_USERNAME} is fully logged out."
        echo "You can try to find processes using:"
        echo "  lsof ${OLD_HOME_DIR}" # Tutorial used .bak here, but at this stage .bak might not exist if mv failed
        echo "  fuser -vm ${OLD_HOME_DIR}"
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
    # findmnt -S <source> -T <target>
    # For a bind mount, <source> is NEW_DATA_LOCATION, <target> is OLD_HOME_DIR
    # We expect FSTYPE to be 'none' and 'bind' to be in options.
    local mount_info
    mount_info=$(findmnt -n -o FSTYPE,OPTIONS -S "${NEW_DATA_LOCATION}" -T "${OLD_HOME_DIR}")
    
    if [[ -n "$mount_info" && "$mount_info" == *"none"* && "$mount_info" == *"bind"* ]]; then
        echo "Mount verified via findmnt: ${mount_info}"
    else
        echo "Mount verification via findmnt failed or output unexpected."
        echo "findmnt output: '$mount_info'"
        echo "Fallback: Checking 'mount' output:"
        mount | grep "${OLD_HOME_DIR}"
        if ! mount | grep -qE "\s${NEW_DATA_LOCATION//\/\//\/}\s+on\s+${OLD_HOME_DIR//\/\//\/}\s+type\s+none\s+\(rw,bind\)"; then
            echo "Mount verification failed. Expected '${NEW_DATA_LOCATION} on ${OLD_HOME_DIR} type none (rw,bind)' or similar."
            echo "Please check manually. Aborting persistent setup."
            umount "${OLD_HOME_DIR}" 2>/dev/null
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

    FSTAB_ENTRY="${NEW_DATA_LOCATION} ${OLD_HOME_DIR} none bind 0 0"
    SYSTEMD_UNIT_NAME="home-${TARGET_USERNAME}.mount" # As per tutorial suggestion for /home/user
    SYSTEMD_UNIT_FILE="/etc/systemd/system/${SYSTEMD_UNIT_NAME}"

    echo "Unmounting temporary manual mount: umount \"${OLD_HOME_DIR}\""
    umount "${OLD_HOME_DIR}"
    if [ $? -ne 0 ]; then echo "Warning: Could not unmount ${OLD_HOME_DIR}. This might interfere with testing the persistent mount."; fi

    case "$persist_choice" in
        [Aa])
            echo "Adding to /etc/fstab: ${FSTAB_ENTRY}"
            if grep -qF "${OLD_HOME_DIR} " /etc/fstab; then # Check with space
                echo "An entry for ${OLD_HOME_DIR} might already exist in /etc/fstab. Please check manually."
                if ! ask_confirmation "Proceed with adding the new line anyway?"; then
                    echo "Aborting fstab modification."
                    exit 1
                fi
            fi
            echo -e "\n# Bind mount ${TARGET_USERNAME} home directory to ${NEW_DATA_LOCATION}\n${FSTAB_ENTRY}" >> /etc/fstab
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
            echo "WARNING: If ${NEW_DATA_LOCATION} is not available early during boot, this might cause issues. Consider using 'nofail' option with caution or systemd."
            ;;
        [Bb])
            echo "Creating systemd mount unit: ${SYSTEMD_UNIT_FILE}"
            # RequiresMountsFor should ideally be the mountpoint that provides NEW_DATA_LOCATION.
            # For simplicity here, using NEW_DATA_LOCATION itself, assuming it's either a mountpoint
            # or on a filesystem that systemd can determine dependencies for.
            cat > "${SYSTEMD_UNIT_FILE}" << EOF
[Unit]
Description=Bind mount ${OLD_HOME_DIR} to ${NEW_DATA_LOCATION}
RequiresMountsFor=${NEW_DATA_LOCATION}
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
            systemctl enable --now "${SYSTEMD_UNIT_NAME}"
            if [ $? -ne 0 ]; then echo "Error enabling/starting systemd unit. Check status. Aborting."; exit 1; fi
            
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
    echo "2. Switch to the graphical login screen (Ctrl+Alt+F1 or F7)."
    echo "3. Log in as the user '${TARGET_USERNAME}'."
    echo "4. Test various applications, file access, create/delete files."
    echo "5. Open a terminal as '${TARGET_USERNAME}' and run 'df -h ${OLD_HOME_DIR}' - it should show stats for the partition hosting ${NEW_DATA_LOCATION}."
    echo "6. CRITICAL: Reboot the system and log in again as '${TARGET_USERNAME}' to ensure the persistent mount works after a full restart."
}

step_12_cleanup() {
    echo "--- Step 12: Clean Up (Optional - Use Caution!) ---"
    ORIGINAL_HOME_BACKUP="${OLD_HOME_DIR}.bak"
    echo "After extensive testing (including reboots) and confirming everything works perfectly,"
    echo "you can remove the backup directory: ${ORIGINAL_HOME_BACKUP}"
    echo "🛑 Double-check you are deleting the correct directory! 🛑"
    echo "Command to run MANUALLY from a TTY as root/admin: rm -rf \"${ORIGINAL_HOME_BACKUP}\""
}

# --- Main Script Execution ---
check_root

echo "This script will guide you through bind mounting ${OLD_HOME_DIR} to use storage from ${NEW_DATA_LOCATION}."
echo "Based on the tutorial from https://ib.bsb.br/bind-mounting-homeuser-to-userdata/"
echo ""
if ! ask_confirmation "Do you understand the risks and want to proceed?"; then
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

echo "Script finished. PLEASE FOLLOW THE TESTING AND CLEANUP INSTRUCTIONS CAREFULLY."
{% endcodeblock %}
