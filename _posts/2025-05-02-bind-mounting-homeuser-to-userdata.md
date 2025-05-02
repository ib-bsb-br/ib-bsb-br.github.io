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