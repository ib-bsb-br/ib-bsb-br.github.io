---

tags: [windows]
info: aberto.
date: 2025-01-07
type: post
layout: post
published: true
slug: reset-windows-11-administrator-password
title: 'reset windows 11 administrator password'
---
### **Method 1: Reset Password Using Windows 11 Installation Media**

This method uses the Windows Recovery Environment to reset your password via the Command Prompt.

**What You'll Need:**

- A USB flash drive with at least **8 GB** of space.
- Access to another Windows computer to create the installation media.

**Steps:**

1. **Create Windows 11 Installation Media:**

   - On the other computer, visit the [Microsoft Windows 11 Download Page](https://www.microsoft.com/software-download/windows11).
   - Download the **Windows 11 Installation Media Creation Tool**.
   - Run the tool and select **"Create installation media (USB flash drive, DVD, or ISO file) for another PC"**.
   - Choose your preferred language, edition, and architecture (64-bit).
   - Select **USB flash drive** when prompted and choose your USB drive from the list.
   - Allow the tool to download and create the installation media.

2. **Boot from the USB Drive:**

   - Insert the USB drive into your locked Windows 11 PC.
   - Restart the PC and enter the **BIOS/UEFI settings**. This is usually done by pressing a key during startup, such as **F2**, **F10**, **F12**, **Del**, or **Esc** (check your PC's documentation).
   - In the BIOS/UEFI settings, locate the **Boot** menu and set the USB drive as the first boot device.
   - Save changes and exit the BIOS/UEFI settings. The PC should now boot from the USB drive.

3. **Access the Command Prompt:**

   - When the Windows Setup screen appears, select your language and preferences, then click **Next**.
   - Click on **"Repair your computer"** at the bottom-left corner.
   - Choose **"Troubleshoot"** > **"Advanced options"** > **"Command Prompt"**.

4. **Identify the Windows Installation Drive:**

   - In the Command Prompt, type `diskpart` and press **Enter**.
   - Then type `list volume` and press **Enter**.
   - Identify the drive letter of your Windows installation (it might not be **C:** in this environment).
   - Type `exit` and press **Enter** to leave DiskPart.

5. **Backup and Replace Utility Manager:**

   - Assuming your Windows installation is on **D:**, adjust accordingly if different.
   - Type the following commands, pressing **Enter** after each:

     ```
     D:
     cd \Windows\System32
     ren utilman.exe utilman.exe.bak
     copy cmd.exe utilman.exe
     ```

   - This backs up the Utility Manager executable and replaces it with Command Prompt.

6. **Restart Your Computer:**

   - Type `wpeutil reboot` and press **Enter**, or close the Command Prompt and select **"Continue"** to restart.

7. **Reset Your Password at the Login Screen:**

   - At the login screen, click the **Ease of Access** icon (usually at the bottom-right corner). This will open a Command Prompt window.
   - To list all user accounts, type:

     ```
     net user
     ```

   - Identify your account name from the list.
   - To reset your password, type:

     ```
     net user [YourUsername] [NewPassword]
     ```

     Replace `[YourUsername]` with your actual username and `[NewPassword]` with the password you wish to set.

     For example:

     ```
     net user JohnDoe MyNewPassword123
     ```

   - Close the Command Prompt window.

8. **Log In to Your Account:**

   - Use your new password to log in.

9. **Restore the Original Utility Manager:**

   - After logging in, open **Command Prompt** as an administrator:

     - Click on **Start**, type **cmd**, right-click **Command Prompt**, and select **"Run as administrator"**.

   - Navigate to the System32 directory:

     ```
     cd \Windows\System32
     ```

   - Restore the original Utility Manager:

     ```
     del utilman.exe
     ren utilman.exe.bak utilman.exe
     ```

---

### **Method 2: Use a Reputable Password Reset Tool (e.g., Hiren's BootCD PE)**

**What You'll Need:**

- A USB flash drive with at least **2 GB** of space.
- Access to another computer.

**Steps:**

1. **Download Hiren's BootCD PE:**

   - Visit the [Hiren's BootCD PE Official Website](https://www.hirensbootcd.org/download/) and download the ISO file.

2. **Create a Bootable USB Drive:**

   - Download **Rufus** from [rufus.ie](https://rufus.ie/) and run it.
   - Insert your USB flash drive into the computer.
   - In Rufus:

     - Select your USB drive under **"Device"**.
     - Click **"SELECT"** and choose the Hiren's BootCD PE ISO file.
     - Keep the default settings and click **"START"**.
     - Confirm any prompts to write in ISO mode.

3. **Boot from the USB Drive:**

   - Insert the USB drive into your locked PC.
   - Restart and boot from the USB drive (refer to Method 1, Step 2 for guidance).

4. **Reset the Password Using Hiren's BootCD PE:**

   - Once booted, the Hiren's BootCD PE desktop will appear.
   - Navigate to **Start Menu** > **Security** > **Passwords** > **NT Password Edit**.
   - In **NT Password Edit**:

     - Click **(Re)open** to load the SAM file.
     - Select your user account from the list.
     - Click **"Change Password"**, enter a new password, and confirm it.
     - Click **"Save Changes"**.
     - Close the program.

5. **Restart Your Computer:**

   - Remove the USB drive.
   - Click **Start** > **Power** > **Restart**.
   - Boot into Windows and log in using your new password.

---

### **Method 3: Reset Password Using a Linux Live USB and chntpw**

**What You'll Need:**

- A USB flash drive with at least **4 GB** of space.
- Access to another computer.

**Steps:**

1. **Download a Linux Distribution (e.g., Ubuntu):**

   - Visit the [Ubuntu Download Page](https://ubuntu.com/download/desktop) and download the Ubuntu ISO file.

2. **Create a Bootable Linux USB Drive:**

   - Use **Rufus** to create a bootable USB drive with the Ubuntu ISO (similar to Method 2, Step 2).

3. **Boot into Linux Live Environment:**

   - Insert the USB drive into your locked PC.
   - Restart and boot from the USB drive.

4. **Run Ubuntu Without Installing:**

   - Select **"Try Ubuntu"** when prompted.

5. **Install chntpw Utility:**

   - Ensure your PC is connected to the internet.
   - Open the **Terminal** application.
   - Update package lists:

     ```
     sudo apt update
     ```

   - Install chntpw:

     ```
     sudo apt install chntpw
     ```

6. **Identify and Mount Your Windows Partition:**

   - In Terminal, list the disk partitions:

     ```
     sudo fdisk -l
     ```

   - Identify the partition where Windows is installed (look for a partition of type **NTFS**).

   - Create a mount point:

     ```
     sudo mkdir /mnt/windows
     ```

   - Mount the partition (replace `/dev/sda3` with your Windows partition identifier):

     ```
     sudo mount /dev/sda3 /mnt/windows
     ```

7. **Reset the Password:**

   - Navigate to the Windows System32 config directory:

     ```
     cd /mnt/windows/Windows/System32/config
     ```

   - List user accounts:

     ```
     sudo chntpw -l SAM
     ```

   - Reset your password (replace `YourUsername` with your actual username):

     ```
     sudo chntpw -u YourUsername SAM
     ```

   - Follow the prompts to clear the password or set a new one.

     - Type `1` to **Clear (blank) user password** or `2` to **Edit (set new) user password**.
     - If setting a new password, enter the new password when prompted.

   - Save changes by typing `y` when prompted.

8. **Unmount the Partition and Restart:**

   - Unmount the Windows partition:

     ```
     sudo umount /mnt/windows
     ```

   - Restart your computer:

     ```
     sudo reboot
     ```

   - Remove the USB drive during the reboot.

9. **Log In to Windows:**

   - Use the new or cleared password to log into your account.