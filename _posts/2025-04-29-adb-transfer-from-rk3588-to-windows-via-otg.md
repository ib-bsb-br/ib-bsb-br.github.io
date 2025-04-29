---
tags: [scratchpad]
info: aberto.
date: 2025-04-29
type: post
layout: post
published: true
slug: adb-transfer-from-rk3588-to-windows-via-otg
title: 'ADB transfer from RK3588 to Windows via OTG'
---
This guide explains how to use the Android Debug Bridge (adb) utility within Windows 11 PowerShell to copy selected folders from your Rockchip RK3588 device to your PC for backup, utilizing a USB OTG (On-The-Go) connection.

**1\. Prerequisites:**

* **ADB Installed and PATH Configured on Windows 11:**  
  * Download the "SDK Platform Tools for Windows" from the official Android Developers website: [https://developer.android.com/tools/releases/platform-tools](https://developer.android.com/tools/releases/platform-tools)  
  * Extract the downloaded ZIP file to a stable location (e.g., C:\\platform-tools).  
  * Add the full path to this folder (e.g., C:\\platform-tools) to your Windows system's Path environment variable. This allows you to run adb commands from any PowerShell window without navigating to the folder first. This makes using ADB much more convenient as you don't need to type the full path to adb.exe every time.  
    * Search for "Edit the system environment variables" in the Windows search bar and open it.  
    * Click on "Environment Variables...".  
    * Under "System variables" (recommended) or "User variables", find and select the Path variable, then click "Edit...".  
    * Click "New" and paste the full path to your platform-tools folder.  
    * Click "OK" on all open windows.  
    * **Important:** Close and reopen any currently open PowerShell windows for the change to take effect. Verify by opening a new PowerShell window and typing adb version.  
* **Rockchip USB Drivers:**  
  * Install the necessary USB drivers for your RK3588 device on Windows 11\. These often come from the device manufacturer or can be found in Rockchip driver packs (e.g., DriverAssitant). While Windows might install generic drivers, specific Rockchip drivers are often more reliable. Ensure the driver supports ADB connections.  
  * Check Windows **Device Manager** after connecting the device. Look for entries like "ADB Interface", "Android Device", or specific Rockchip devices, ensuring there are no yellow warning icons indicating driver issues.  
* **USB Debugging Enabled on RK3588:**  
  * **If running Android:**  
    * Go to Settings \> About phone (or About device).  
    * Tap on the Build number seven times until you see "You are now a developer\!".  
    * Go back to the main Settings menu, find System \> Developer options.  
    * Enable Developer options (if not already enabled).  
    * Find and enable USB debugging. Confirm any security prompts.  
  * **If running Linux:** Ensure the adbd (ADB Daemon) service is installed and running. Configuration might involve enabling/starting a systemd service (e.g., systemctl enable \--now adbd) or an init script. The USB OTG port also needs to be configured for peripheral/device mode, potentially via Device Tree Overlays (.dtbo). Consult your specific Linux distribution's documentation for the RK3588.  
* **USB OTG Cable and Connection:**  
  * Connect the RK3588 device to your Windows 11 PC using a USB cable plugged into the **designated OTG port** on the RK3588 device. This specific port allows the RK3588 to act as a USB *peripheral* (like a phone connecting to a PC), which is necessary for ADB connection *to* the PC. Standard USB host ports (Type-A) on the RK3588 will likely not work for this purpose. Check your board's documentation to identify the correct port (often USB-C or Micro-USB).

**2\. Verify ADB Connection:**

* Open **Windows PowerShell** (you can search for it in the Start menu or right-click the Start button).  
* Type the following command and press Enter:  
  adb devices

* **Authorize Connection (First Time):** Look at the screen of your RK3588 device. A prompt should appear asking "Allow USB debugging?" showing your PC's RSA key fingerprint. Check the box "Always allow from this computer" (recommended) and tap "Allow" or "OK".  
* **Run adb devices again.** You should see your device listed with its serial number and "device" next to it:  
  List of devices attached  
  RK3588\_SERIAL\_NUMBER    device

* **Troubleshooting Connection Status:**  
  * **unauthorized**: You missed or denied the authorization prompt on the RK3588. Check the device screen, disconnect/reconnect, or use "Revoke USB debugging authorizations" in Developer Options on the device and try again.  
  * **offline**: Often a driver or connection issue. Check drivers, cable, and OTG port. Try adb kill-server followed by adb start-server. Check Device Manager on Windows.  
  * **Empty List**: Check drivers, cable (ensure it's the OTG port), USB debugging setting on the device. Check Device Manager for unrecognized devices. Ensure adbd is running if using Linux.

**3\. Identify Folders on RK3588:**

* You need the exact path of the folders you want to copy *on the RK3588 device*. Remember that paths on Android/Linux are **case-sensitive**.  
* Use the adb shell command to explore the device's filesystem:  
  adb shell

* Inside the shell (you'll see a prompt like rk3588:/ $), use standard Linux commands:  
  * ls: List directory contents (use ls \-l for more details).  
  * cd \<directory\>: Change directory.  
  * pwd: Print the current working directory (shows the full path).  
* **Common Locations (Android):**  
  * /sdcard/ (Internal shared storage, often links to /storage/emulated/0/)  
  * /sdcard/DCIM/ (Camera photos/videos)  
  * /sdcard/Download/  
  * /sdcard/Documents/  
  * /sdcard/Pictures/  
* Note down the full path for each folder you want to back up (e.g., /sdcard/Documents).  
* Type exit and press Enter to leave the adb shell.

**4\. Transfer Folders using adb pull:**

* The command to copy files or folders *from* the Android device *to* your Windows PC is adb pull.  
* **Syntax:**  
  adb pull \<path\_on\_device\> \<path\_on\_windows\_pc\>

* **Understanding the Destination Path:**  
  * When you run adb pull /device/source/folder C:\\PC\\dest, ADB copies the folder *into* C:\\PC\\dest. The result is C:\\PC\\dest\\folder.  
  * If the final component of the PC path (dest in this example) doesn't exist, adb pull will attempt to create it.  
* **Create Base Destination Folder (Recommended):** Create a main folder on your Windows PC to store all the backups, e.g.:  
  mkdir C:\\RK3588\_Backup

* **Execute the Transfer (Single Folder):** Run the adb pull command for the desired folder.  
  * **Example:** Copy /sdcard/Documents from the device into the C:\\RK3588\_Backup folder on your PC (resulting in C:\\RK3588\_Backup\\Documents):  
    adb pull /sdcard/Documents C:\\RK3588\_Backup

  * **Example:** Copy /sdcard/DCIM into the same base backup folder:  
    adb pull /sdcard/DCIM C:\\RK3588\_Backup

  * **Paths with Spaces:** If any path (on the device or PC) contains spaces, enclose the *entire path* in double quotes:  
    adb pull "/sdcard/My Work Files" "C:\\RK3588\_Backup"

    (This will create C:\\RK3588\_Backup\\My Work Files)  
* Wait for each command to complete. Transfer time depends on the amount of data.

**4.1 Transferring Multiple Folders (PowerShell Script \- Optional):**

If you need to back up many folders regularly, scripting is more efficient.

1. **Create a List:** Define the source folders on the RK3588 device in a PowerShell array.  
2. **Define Destination:** Specify the base backup folder on your Windows PC.  
3. **Loop and Pull:** Use ForEach-Object to iterate through the list and run adb pull for each folder.  
* **Example PowerShell Script:**  
  \# \--- Configuration \---  
  \# List of full paths to folders on the RK3588 device to back up  
  $sourceFolderPaths \= @(  
      "/sdcard/Documents",  
      "/sdcard/DCIM",  
      "/sdcard/Pictures",  
      "/sdcard/Download",  
      "/sdcard/My Work Files" \# Example with spaces  
  )

  \# Base destination folder on your Windows PC  
  $destinationBaseFolder \= "C:\\RK3588\_Backup"

  \# \--- Execution \---  
  Write-Host "Starting RK3588 folder backup..."

  \# Create the base destination folder if it doesn't exist  
  if (-not (Test-Path $destinationBaseFolder)) {  
      Write-Host "Creating destination folder: $destinationBaseFolder"  
      New-Item \-ItemType Directory \-Force \-Path $destinationBaseFolder  
  }

  \# Loop through each source folder path  
  $sourceFolderPaths | ForEach-Object {  
      $sourceFolder \= $\_  
      Write-Host "Attempting to pull '$sourceFolder' to '$destinationBaseFolder'..."

      \# Construct the adb pull command (handles spaces using quotes if needed)  
      \# Note: We pull the folder \*into\* the base destination directory.  
      adb pull "$sourceFolder" "$destinationBaseFolder"

      \# Basic error check (adb pull doesn't have reliable exit codes for success/failure)  
      \# You might need more robust checking for production scripts  
      if ($LASTEXITCODE \-ne 0\) {  
          Write-Warning "Potential issue pulling '$sourceFolder'. Check ADB output."  
      } else {  
          Write-Host "Successfully pulled '$sourceFolder'." \-ForegroundColor Green  
      }  
  }

  Write-Host "Backup process completed."

* **How to Use:**  
  1. Open PowerShell.  
  2. Copy and paste the script directly into the PowerShell window, or save it as a .ps1 file (e.g., backup\_rk3588.ps1) and run it using .\\backup\_rk3588.ps1. (You might need to adjust PowerShell's execution policy first: Set-ExecutionPolicy RemoteSigned \-Scope CurrentUser. This command may be required due to Windows security settings that prevent running scripts downloaded from the internet or created locally. Using \-Scope CurrentUser is generally safer as it only affects your user account, not the entire system. Pasting the script directly into an open PowerShell window usually bypasses this check.).  
  3. Modify the $sourceFolderPaths array and $destinationBaseFolder variable as needed.

**5\. Verify the Backup:**

* Navigate to your destination folder on Windows (e.g., C:\\RK3588\_Backup) using File Explorer.  
* Check that the folders (e.g., Documents, DCIM) have been copied and contain the expected files.

**6\. Troubleshooting:**

* **Device Not Found/Offline/Unauthorized:** See Step 2 troubleshooting. Double-check drivers, cable, OTG port, USB debugging status, and PC authorization on the device. Restarting both devices can help. Try adb kill-server then adb start-server.  
* **Permission Denied during adb pull:**  
  * You might not have permission to access certain system folders (e.g., /data/data/). Standard adb pull usually works for user-accessible storage like /sdcard/. Accessing protected areas might require root access on the RK3588 device (adb root, if supported and enabled).  
  * Ensure PowerShell has permissions to write to the destination folder on Windows. Try running PowerShell as Administrator or choosing a destination folder in your user profile (e.g., C:\\Users\\YourUsername\\Documents\\RK3588\_Backup).  
* **File Not Found / No such file or directory:**  
  * Double-check the exact path on the device using adb shell ls. Remember paths are **case-sensitive**.  
  * Ensure you are using forward slashes (/) for the device path.  
* **Slow Transfer:** Transfer speeds depend on the USB connection speed (USB 2.0 vs 3.0/3.1 for the OTG port and PC port), the device's internal storage speed, and the number/size of files. Large transfers take time.  
* **Transfer Interrupted:** If a pull command is interrupted (e.g., cable disconnect), it will likely need to be rerun for that specific folder. ADB pull doesn't typically resume automatically.

**7\. Alternative Methods (Briefly):**

While adb pull is direct and scriptable, other methods exist:

* **Network Transfer:** If SSH is enabled on the RK3588 (common on Linux), tools like scp or rsync can be used over the network. File managers with network support (SMB/SFTP) can also work.  
* **Synchronization Tools:** Apps like Syncthing can keep folders synchronized between devices automatically over the network.  
* **GUI ADB Tools:** Various third-party applications provide a graphical interface for ADB operations, including file transfer.

By following these steps, you should be able to successfully use ADB in PowerShell to back up selected folders from your RK3588 device to your Windows 11 computer via the USB OTG connection. Remember to disable USB debugging when not needed for security.