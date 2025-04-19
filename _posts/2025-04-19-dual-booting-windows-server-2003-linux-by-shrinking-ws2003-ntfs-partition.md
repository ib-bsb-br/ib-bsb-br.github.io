---
tags: [scratchpad]
info: aberto.
date: 2025-04-19
type: post
layout: post
published: true
slug: dual-booting-windows-server-2003-linux-by-shrinking-ws2003-ntfs-partition
title: 'Dual-Booting Windows Server 2003 & linux by shrinking WS2003 NTFS Partition'
---
This guide outlines the recommended procedure for installing Windows Server 2003 (on 30GB) and TUXEDO OS (on 60GB) onto a blank 90GB SSD, starting from 100% unallocated space. The standard and generally most effective method is to install the older operating system (Windows Server 2003\) first.

*Alternative Consideration:* Before proceeding, consider if running Windows Server 2003 inside a virtual machine (using software like VirtualBox or VMware) within TUXEDO OS might meet your needs. Virtualization avoids partitioning complexities and better isolates the insecure WS2003 OS, but requires more RAM/CPU resources and may have limitations accessing specific hardware directly. This guide focuses on the dual-boot method.

**Important Prerequisites & Considerations:**

1. **Backup:** Although starting with a blank SSD, ensure you have backups of any important data elsewhere. Mistakes during partitioning can lead to data loss on other drives if not careful.  
2. **Windows Server 2003 Media:** You need the installation media (CD, DVD, or a bootable USB).  
   * *USB Creation Tip:* Creating a bootable USB for WS2003 can be tricky. Tools like Rufus are often recommended; ensure you select the correct options (e.g., MBR partition scheme for the USB if targeting Legacy BIOS boot, appropriate filesystem like NTFS).  
3. **TUXEDO OS Media:** Download the latest TUXEDO OS ISO file from their official website.  
4. **USB Drive:** A separate USB drive (minimum 8GB recommended) for the TUXEDO OS installer.  
5. **BalenaEtcher/Rufus:** Download and install BalenaEtcher or Rufus on another computer to create the bootable TUXEDO OS USB drive.  
6. **Security Warning:** Windows Server 2003 is **extremely outdated, unsupported, and has critical security vulnerabilities.** **DO NOT connect it to the internet or any untrusted network** unless absolutely necessary for an isolated task, and you fully understand the significant risks involved. This setup is strongly advised only for specific, offline, legacy purposes.  
7. **Driver Compatibility:** Modern hardware will likely **lack drivers** for Windows Server 2003\. Verify availability for your specific hardware (chipset, network, storage, graphics) *before* starting. Installation may fail or the OS may be unusable without them. Finding compatible drivers often requires searching archived forums or manufacturer legacy support pages, and may be impossible for very new components.  
8. **Storage Controller Drivers (F6 Drivers):** If your motherboard's SATA controller is set to AHCI or RAID mode in the BIOS/UEFI, the WS2003 installer might not detect the SSD.  
   * **Solution 1 (Recommended):** Set the SATA mode to IDE / Compatibility / Legacy in the BIOS/UEFI *before* starting the WS2003 installation (See Step 2).  
   * **Solution 2 (Complex):** If you must use AHCI/RAID, you'll need to find the specific WS2003 storage controller driver for your motherboard and load it during the early phase of Windows setup (traditionally via floppy disk when prompted by "Press F6 if you need to install a third party SCSI or RAID driver..."). This is often difficult on modern systems without floppy drives.  
9. **BIOS/UEFI Mode & Partitioning:**  
   * WS2003 primarily expects a **Legacy BIOS** environment and **MBR** (Master Boot Record) partitioning. Using Legacy/CSM mode in your firmware settings is strongly recommended for compatibility and simplicity. MBR limits you to 4 primary partitions, or 3 primary and 1 extended partition (which can contain multiple logical partitions).  
   * While WS2003 SP1+ had rudimentary UEFI support, it's often problematic. TUXEDO OS supports both UEFI (with GPT partitioning) and Legacy BIOS (with MBR).  
   * **Recommendation:** Use Legacy BIOS/CSM mode for the entire process. ***Set this before starting.***  
10. **Secure Boot:** If your system supports UEFI, **Secure Boot must be disabled** in the firmware settings, as WS2003 cannot boot with it enabled. It likely also needs to be disabled if using Legacy/CSM mode.

**Procedure:**

**Step 1: Prepare TUXEDO OS Bootable USB**

1. On a working computer, install and run BalenaEtcher or Rufus.  
2. Select the downloaded TUXEDO OS ISO file.  
3. Select the target USB drive (double-check it's the correct one\!).  
4. Use the recommended settings to write the ISO in a bootable format. Wait for completion.

**Step 2: Configure BIOS/UEFI Settings**

1. Enter your computer's BIOS/UEFI setup utility (common keys: DEL, F2, F10, F12, ESC during startup).  
2. **Set Boot Mode:** Navigate to Boot options. Select **Legacy** or **CSM** mode. Disable UEFI boot if possible, or set Legacy as the priority. This aligns best with WS2003's expectation of MBR partitioning.  
3. **Disable Secure Boot:** Find the Secure Boot option (often under Security or Boot tabs) and set it to **Disabled**.  
4. **Set SATA Mode:** Find SATA Configuration/Mode. If available, set it to **IDE** or **Compatibility** (instead of AHCI or RAID) to improve chances of WS2003 detecting the drive without extra drivers.  
5. **Set Boot Order:** Configure the boot device order to prioritize your Windows Server 2003 installation media (e.g., CD/DVD drive or the WS2003 USB).  
6. Save changes and exit the BIOS/UEFI setup.

**Step 3: Install Windows Server 2003 (First Partition)**

1. Boot the computer from the Windows Server 2003 installation media.  
2. Follow initial prompts (loading files, license agreement). If you encounter the "Press F6..." prompt for drivers and didn't set IDE mode, you may need to provide storage drivers (see Prerequisite 8).  
3. When you reach the disk selection/partitioning screen:  
   * You should see the 90GB drive listed as unallocated space.  
   * Select the unallocated space.  
   * Choose the option to create a new partition (e.g., press 'C').  
   * Enter the size for the Windows partition: approximately **30720 MB** (which is 30 GB).  
   * The installer will create the partition. Select it and choose to format it using the **NTFS** file system.  
   * Select this newly created 30GB NTFS partition as the installation target for Windows.  
   * **Crucially, leave the remaining \~60GB as unallocated space.** Do not create or format this space yet.  
4. Proceed with the Windows Server 2003 installation. This may involve several reboots. Let it complete fully.  
5. Verify that Windows boots successfully on its own. Install essential drivers (chipset, graphics) if possible *now*, especially if network drivers aren't available yet. Then, shut down the computer.

**Step 4: Prepare for TUXEDO OS Installation**

1. Enter the BIOS/UEFI setup again.  
2. Change the boot order to prioritize the **USB Drive** (containing the TUXEDO OS installer).  
3. Save changes and exit.

**Step 5: Install TUXEDO OS (Second Partition)**

1. Boot the computer from the TUXEDO OS USB drive.  
2. Select the option to **Install TUXEDO OS**.  
3. Follow initial setup steps (language, keyboard, network \- connecting now helps install updates).  
4. At the "Installation type" screen:  
   * **Select the manual partitioning option** (e.g., "Something else", "Manual partitioning"). **Do not** use automatic options.  
   * You'll see the partition table: the 30GB NTFS partition and the \~60GB "free space".  
   * Select the free space. Click "+" or "Add" to create partitions:  
     * **Root Partition (/):**  
       * Size: Use most of the \~60GB (e.g., 55000MB-60000MB, leave space only if creating separate swap).  
       * Type: Primary or Logical (In MBR with one Windows primary partition, you can use Primary here, or Logical if you also create a swap partition as Primary/Logical).  
       * Location: Beginning of this space.  
       * Use as: **ext4 journaling file system**  
       * Mount point: **/**  
     * **(Optional) Swap Partition:**  
       * Size: Depends on RAM (e.g., 4096 MB \= 4GB). Modern Linux can use a swap file instead, often created automatically if no swap partition exists.  
       * Type: Primary or Logical.  
       * Location: End of this space.  
       * Use as: **swap area**  
     * *MBR Note:* Remember the limit of 4 primary partitions on an MBR disk. Your setup (Win Primary \+ Linux Root Primary \+ Swap Logical/Primary) should fit.  
   * **Bootloader Installation Location:** This is **critical**. Find the dropdown menu for "Device for boot loader installation". Select the main drive itself, **not** a partition. It will be like /dev/sda or /dev/nvme0n1. **Do not select /dev/sda1 or similar.** Installing GRUB to the drive's boot record (e.g., /dev/sda, the MBR) replaces the default boot code with GRUB, which can then chainload either Windows or Linux. Installing to a partition (e.g., /dev/sda1) puts GRUB in that partition's boot sector, which the MBR doesn't automatically load, leaving the original Windows bootloader in charge and unaware of Linux.  
5. Carefully review the partitioning plan. Confirm and proceed with installation.  
6. Complete the remaining prompts (timezone, user account creation).

**Step 6: First Boot & Verification**

1. When installation finishes, remove the USB drive and reboot.  
2. The **GRUB boot menu** should appear. It should list TUXEDO OS and Windows Server 2003 (possibly named generically).  
3. Test booting into TUXEDO OS (usually the default).  
4. Reboot, select the Windows entry from GRUB, and test booting into WS2003.  
5. *Troubleshooting:* If the GRUB menu doesn't appear, or Windows won't boot from GRUB, you may need to boot back into the TUXEDO OS live USB and use a tool like "Boot Repair" to fix the bootloader configuration.

**Post-Installation:**

* Install any remaining necessary drivers within both operating systems. Finding WS2003 drivers will likely remain the biggest challenge.  
* Configure TUXEDO OS (updates, software).  
* **Final Security Reminder:** Keep the Windows Server 2003 installation **offline** and isolated as much as humanly possible due to its severe security risks.

You should now have a functional, albeit unconventional, dual-boot system.

# Shrinking WS2003 NTFS Partition using **parted** and **ntfsresize**

This guide details how to shrink an existing Windows Server 2003 NTFS partition using command-line tools from a Linux rescue environment booted to RAM. This is an alternative to using graphical tools like GParted.

**Warning:** Directly manipulating partitions and filesystems with command-line tools like parted and ntfsresize is powerful but carries **significant risk**. A mistake in device names, sizes, or commands can lead to **complete data loss** or prevent Windows from booting. **Back up any critical data before starting**, even on a relatively fresh installation. Proceed with extreme caution and double-check every command before execution. This guide assumes you are comfortable working in a Linux command-line environment.

**Prerequisites:**

1. **Bootable Linux Rescue Media:** You need a USB drive or CD/DVD with a Linux rescue system. **SystemRescue** (available at www.system-rescue.org) is a recommended option known to include the necessary tools. Other options include Finnix, or a standard Linux distribution's live session. The environment **must** include the parted utility and the ntfs-3g package (which provides ntfsresize).  
2. **Target Disk/Partition Knowledge:** You need to know the device name for your SSD (e.g., /dev/sda, /dev/nvme0n1) and the partition number of the Windows installation (e.g., 1 for /dev/sda1).  
3. **Desired Size:** Know the target size for the Windows partition (e.g., \~30GB \= 30720MB).

**Steps:**

**Step 1: Boot into Linux Rescue Environment**

1. Insert your prepared Linux rescue media (USB/CD).  
2. Boot your computer from this media. You may need to adjust the BIOS/UEFI boot order.  
3. Once the rescue environment has loaded (usually to a command prompt or a basic desktop), open a terminal window. You will typically need root privileges for these commands, so use sudo before each command or switch to root using sudo su or su \-.

**Step 2: Identify Target Disk and Partition**

1. Use one of the following commands to list disks and partitions and identify your target Windows partition. Note the device name (e.g., /dev/sda) and partition number (e.g., 1).  
   sudo parted \-l  
   \# or  
   sudo lsblk  
   \# or  
   sudo fdisk \-l

2. Look for the partition formatted with NTFS that corresponds to your Windows installation (likely the largest one currently). Let's assume it's /dev/sda1 for the rest of this guide. Replace /dev/sda1 and /dev/sda with your actual device names throughout this guide.

**Step 3: Resize the NTFS Filesystem (Crucial First Step)**

parted modifies the partition table boundary but doesn't safely shrink the actual NTFS filesystem data structures. You *must* shrink the filesystem first using ntfsresize.

1. **Check Minimum Size:** See the smallest size the filesystem can currently be resized to.  
   sudo ntfsresize \--info /dev/sda1

   Note the "Lowest possible new size". Your target size (30720MB) must be larger than this.  
2. **Check Filesystem:** Perform a check for errors.  
   sudo ntfsresize \--check /dev/sda1

   * **If errors are reported:** Do not proceed with resizing yet. You must fix the filesystem first.  
     * Reboot into Windows Server 2003\.  
     * Open an **Administrator** Command Prompt (Start \-\> Run \-\> cmd, then right-click Command Prompt icon and "Run as administrator", or use equivalent method for WS2003).  
     * Run: chkdsk c: /f  
     * Press Y to schedule the check for the next restart.  
     * Reboot Windows. Let chkdsk run during startup.  
     * **Important:** Sometimes Windows needs to boot *again* after the chkdsk completes before the filesystem is marked clean. Reboot Windows one more time.  
     * Boot back into your Linux Rescue Media and run sudo ntfsresize \--check /dev/sda1 again. This is crucial to confirm that the chkdsk in Windows successfully fixed the errors *before* you attempt the actual resize. Do not skip this verification step. Repeat the chkdsk process if errors persist. Do not proceed with resizing until \--check reports no errors.  
3. **Perform Filesystem Resize (Dry Run Recommended):** Simulate the resize to your target size (e.g., 30720MB \= 30GB). Use the M suffix for Megabytes.  
   \# Replace 30720M with your desired size in Megabytes  
   sudo ntfsresize \--no-action \--size 30720M /dev/sda1

   Review the output carefully. If it looks correct and reports no issues, proceed.  
4. **Perform Actual Filesystem Resize:** Execute the resize command without \--no-action.  
   \# Replace 30720M with your desired size in Megabytes  
   sudo ntfsresize \--size 30720M /dev/sda1

   This shrinks the NTFS filesystem data structures *within* the current partition boundary. Wait for it to complete.

Step 4: Resize the Partition Boundary using parted

Now that the filesystem inside is smaller, you can move the partition's end boundary using parted.

1. Start parted: Open parted targeting your disk (not the partition).  
   sudo parted /dev/sda

2. **Set Units:** Set the display unit to Megabytes for easier understanding (MiB might be technically more aligned, but MB is often sufficient).  
   (parted) unit mb

3. **Print Partition Table:** View the current partitions, noting the Number, Start, and End of your Windows partition (let's assume it's number 1).  
   (parted) print

4. **Resize Partition:** Use the resizepart command. It needs the partition *number* and the new *end position* (in MB).  
   * **Buffer Explanation:** The new end position must be slightly *larger* than the size you used with ntfsresize (e.g., 30720M). This small buffer (e.g., 30-100MB) is crucial. It ensures the partition boundary safely encompasses all the resized filesystem data, accounting for filesystem metadata near the end and potential minor rounding differences between ntfsresize and parted. Setting it too small risks cutting off the filesystem.  
   * Calculate the new end point. If ntfsresize used 30720M, a safe end point might be 30800MB.  
   * **Caution:** The resizepart command directly modifies your disk's partition table based *only* on the numbers you provide. Double-check the partition number and the calculated end position before proceeding.  
   * Execute the command (replace 1 with your partition number and 30800 with your calculated end point in MB):  
     \# Example: Resizing partition number 1 to end at 30800MB  
     (parted) resizepart 1 30800

   * parted may give warnings (e.g., about the filesystem possibly needing checks); read them carefully. Since you already resized with ntfsresize and will check with chkdsk, these specific warnings after resizepart are usually expected.  
5. **Verify:** Print the partition table again within parted to confirm the End position has changed as intended.  
   (parted) print

6. Quit parted: Exit the tool. Changes are saved automatically upon execution of commands like resizepart.  
   (parted) quit

**Step 5: Final Checks and Reboot**

1. **Verify Partition Size:** Check the partition table again outside parted using OS tools.  
   sudo parted \-l  
   \# or  
   sudo lsblk

   You should see /dev/sda1 now has a size close to 30GB (around 30800MB in our example).  
2. **(Optional but Recommended) Filesystem Check:** Run ntfsresize \--check one last time from Linux.  
   sudo ntfsresize \--check /dev/sda1

3. **Reboot:** Remove the rescue media and reboot the computer.  
   sudo reboot

**Step 6: Check Windows**

1. Allow Windows Server 2003 to boot. It might run chkdsk automatically during startup.  
2. Once booted, open an **Administrator** Command Prompt (Start \-\> Run \-\> cmd, then right-click Command Prompt icon and "Run as administrator", or use equivalent method for WS2003).  
3. Schedule a full disk check to ensure filesystem consistency after the resize:  
   chkdsk c: /f

4. Press Y and Enter to schedule the check for the next restart.  
5. Reboot Windows again. Let chkdsk run fully during startup.  
6. After the check completes and Windows boots successfully, open Disk Management (diskmgmt.msc) to visually confirm the C: drive partition is now approximately 30GB, and you have \~60GB of unallocated space following it.

If Windows boots correctly, chkdsk runs without major errors, and the partition size is right in Disk Management, you have successfully shrunk the partition using command-line tools. You can now proceed with installing TUXEDO OS into the newly created unallocated space as per the original dual-boot guide.