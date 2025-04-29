---
tags: [scratchpad]
info: aberto.
date: 2025-04-29
type: post
layout: post
published: true
slug: dual-boot-windows-and-ubuntu
title: 'Dual Boot Windows and Ubuntu'
---
bibref https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/

![Image 1: Ubuntu 25 installer](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/ubuntu25install_hu_a1a6c5b5a0a2c31f.webp)

_Ubuntu Plucky Puffin installer_

**Last Updated: April 2025**

Running both Windows 11 and Ubuntu 25.04 on the same computer gives you the best of both worlds. This step-by-step guide makes dual-booting simple, even for beginners!

What Sets This Guide Apart[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#what-sets-this-guide-apart)
-------------------------------------------------------------------------------------------------------------------------

Unlike typical dual-boot tutorials, this guide offers:

*   **UEFI vs. Legacy BIOS** instructions for modern computers
*   **Secure Boot compatibility** solutions
*   **Performance optimization** tips for both operating systems
*   **Advanced partition strategies** for optimal system management
*   **Automated setup scripts** to speed up post-installation configuration
*   **Virtualization options** when dual-boot isn’t ideal
*   **Real-world use case scenarios** to maximize your dual-boot experience

What You’ll Need[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#what-youll-need)
----------------------------------------------------------------------------------------------------

*   A computer with Windows 11 already installed
*   At least 30GB of free space (50GB+ recommended for comfortable usage)
*   A USB drive (8GB or larger)
*   About 30-45 minutes of your time
*   Basic computer knowledge

Part 1: Prepare Your Computer[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#part-1-prepare-your-computer)
------------------------------------------------------------------------------------------------------------------------------

### 1\. Back Up Your Data[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#1-back-up-your-data)

Always back up important files before modifying your system.

*   Use Windows built-in Backup and Restore
*   Consider cloud backup solutions (OneDrive, Google Drive)
*   For critical data, create an external drive backup

### 2\. Check Your System Type: UEFI or Legacy BIOS[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#2-check-your-system-type-uefi-or-legacy-bios)

1.  Press **Win + R**, type `msinfo32`, and press Enter
2.  Look for “BIOS Mode” under System Summary
    *   If it says “UEFI”, follow the UEFI instructions in this guide
    *   If it says “Legacy”, follow the Legacy instructions

### 3\. Create Space for Ubuntu[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#3-create-space-for-ubuntu)

#### Using Disk Management:[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#using-disk-management)

1.  Press **Win + X** and select **Disk Management**
2.  Right-click on your largest partition (usually C:) and select **Shrink Volume**
3.  Enter the amount to shrink (minimum 30000 MB recommended for Ubuntu)
    *   For a more comfortable experience: 50000 MB (50GB)
    *   For developers/power users: 100000 MB (100GB)
4.  Click **Shrink** to create unallocated space

![Image 2: Windows Disk Management showing shrink option](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/shrink-volume-to-partition-ssd-via-disk-management_hu_e99782628afd7c57.webp)

_Shrink your Windows partition to make room for Ubuntu_

#### Alternative: Using Disk Cleanup First (Recommended)[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#alternative-using-disk-cleanup-first-recommended)

Before shrinking, free up space by:

1.  Press **Win + R**, type `cleanmgr` and press Enter
2.  Select your C: drive and click OK
3.  Click “Clean up system files”
4.  Select all items, especially “Windows Update Cleanup” and “Previous Windows installations”
5.  Click OK to reclaim gigabytes of space

### 4\. Disable Fast Startup (Critical Step)[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#4-disable-fast-startup-critical-step)

1.  Go to **Control Panel** → **Power Options** → **Choose what the power buttons do**
2.  Click **Change settings that are currently unavailable**
3.  Uncheck **Turn on fast startup**
4.  Click **Save changes**

![Image 3: Windows Fast Startup disable screen](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/fast-startup-w11_hu_af321ac91b2cf027.webp)

_Disabling Fast Startup prevents issues when dual-booting_

### 5\. Disable BitLocker (If Enabled)[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#5-disable-bitlocker-if-enabled)

If you use BitLocker encryption:

1.  Press **Win + X** and select **PowerShell (Admin)** or **Terminal (Admin)**
2.  Type `manage-bde -status` to check BitLocker status
3.  If enabled, type `manage-bde -off C:` to decrypt your drive
4.  Wait for decryption to complete (may take hours)

> **Note:** You can re-enable BitLocker after Ubuntu installation, but it requires additional configuration.

### 6\. Create Recovery Drive (Recommended)[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#6-create-recovery-drive-recommended)

1.  Search for “Create a recovery drive” in Windows Search
2.  Follow the wizard to create a Windows recovery USB
3.  Store it safely in case you need to restore Windows

Part 2: Create Ubuntu Installation Media[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#part-2-create-ubuntu-installation-media)
--------------------------------------------------------------------------------------------------------------------------------

### 1\. Download Ubuntu 25.04[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#1-download-ubuntu-2504)

Download the Ubuntu 25.04 ISO file from [ubuntu.com/download/desktop](https://releases.ubuntu.com/plucky/)

![Image 4: Ubuntu download page](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/ubuntu25_hu_862f2c5b5afb6a62.webp)

_Download the latest Ubuntu 25.04 ISO file_

### 2\. Verify the ISO (For Extra Security)[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#2-verify-the-iso-for-extra-security)

1.  Download the SHA256SUMS and SHA256SUMS.gpg files from the Ubuntu download page
2.  On Windows, open PowerShell and run:
    
    ```
    Get-FileHash -Algorithm SHA256 -Path path\to\ubuntu-25.04-desktop-amd64.iso
    ```
    
3.  Compare the output hash with the one in the SHA256SUMS file

### 3\. Create Bootable USB[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#3-create-bootable-usb)

#### Using Rufus:[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#using-rufus)

1.  Download and install [Rufus](https://rufus.ie/)
2.  Insert your USB drive
3.  Open Rufus and select your USB drive
4.  Click **SELECT** and choose the Ubuntu ISO file
5.  For UEFI systems: Make sure “GPT” is selected in the partition scheme
6.  Click **START** and select **Write in ISO Image mode**

![Image 5: Rufus software creating bootable USB](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/rufus_hu_d0fa41c42e4cd1b0.webp)

_Rufus will create a bootable Ubuntu USB drive_

#### Alternative: Using Ventoy (Multi-Boot Solution)[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#alternative-using-ventoy-multi-boot-solution)

1.  Download [Ventoy](https://www.ventoy.net/)
2.  Install it to your USB drive
3.  Copy the Ubuntu ISO directly to the USB
4.  You can add multiple ISOs to create a multi-boot USB

Part 3: Install Ubuntu Alongside Windows[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#part-3-install-ubuntu-alongside-windows)
--------------------------------------------------------------------------------------------------------------------------------

### 1\. Adjust UEFI/BIOS Settings[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#1-adjust-uefibios-settings)

1.  Restart your computer
2.  Enter BIOS/UEFI (usually by pressing F2, F12, Del, or Esc during startup)
3.  Make these critical changes:
    *   Disable “Secure Boot” (temporarily)
    *   Set “SATA Operation” to “AHCI” mode if using SSD
    *   Disable “Intel Rapid Storage Technology” if present
    *   Change boot order to prioritize USB
4.  Save and exit

### 2\. Boot from USB[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#2-boot-from-usb)

1.  Restart your computer
2.  Press the boot menu key during startup (F12, F2, or Del - varies by computer)
3.  Select your USB drive from the boot menu
4.  On UEFI systems, select the “UEFI” entry for your USB

### 3\. Start Ubuntu Installation[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#3-start-ubuntu-installation)

1.  Select **Try or Install Ubuntu**
2.  Choose your language and click **Install Ubuntu**
3.  Select keyboard layout and click **Continue**
4.  For wireless connection, connect to your WiFi network

### 4\. Choose Optimal Installation Type[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#4-choose-optimal-installation-type)

#### For Beginners (Automatic Partitioning):[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#for-beginners-automatic-partitioning)

1.  Select **Install Ubuntu alongside Windows Boot Manager**
2.  Click **Install Now**

#### For Advanced Users (Manual Partitioning):[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#for-advanced-users-manual-partitioning)

1.  Select **Something else** for manual partitioning
2.  Create the following partitions in the unallocated space:
    *   EFI partition (if not already present): 512 MB, use as “EFI System Partition”
    *   Root partition (/): 20-30 GB, use as “Ext4”, mount point “/”
    *   Swap partition: Equal to your RAM (for hibernation support), use as “swap”
    *   Home partition (/home): Remaining space, use as “Ext4”, mount point “/home”

### 5\. Confirm Partition Changes[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#5-confirm-partition-changes)

Review the changes and click **Continue**

### 6\. Choose Your Location[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#6-choose-your-location)

Select your time zone on the map

### 7\. Create Your User Account[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#7-create-your-user-account)

Enter your name, computer name, username, and password

**Security Tip:** Use a different password than your Windows account

### 8\. Installation Process[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#8-installation-process)

Wait for the installation to complete (usually 10-15 minutes)

### 9\. Restart Your Computer[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#9-restart-your-computer)

When prompted, remove the USB drive and click **Restart Now**

Part 4: Post-Installation Configuration[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#part-4-post-installation-configuration)
--------------------------------------------------------------------------------------------------------------------------------

### 1\. Re-enable Secure Boot (Optional)[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#1-re-enable-secure-boot-optional)

If you want to use Secure Boot with Ubuntu:

1.  Boot into UEFI settings
2.  Find Secure Boot settings
3.  Enter “Setup Mode” if available
4.  Enable Secure Boot
5.  Save and exit

Ubuntu 25.04 supports Secure Boot, but you may need to manage keys if you encounter boot issues.

### 2\. First Boot and Updates[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#2-first-boot-and-updates)

1.  At the GRUB menu, select Ubuntu
2.  Log in with your credentials
3.  Run system updates:
    
    ```
    sudo apt update && sudo apt upgrade -y
    ```
    

### 3\. Install Ubuntu Restricted Extras[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#3-install-ubuntu-restricted-extras)

For media codecs, fonts, and other proprietary software:

```
sudo apt install ubuntu-restricted-extras
```

### 4\. Install Hardware-Specific Drivers[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#4-install-hardware-specific-drivers)

#### For NVIDIA Graphics:[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#for-nvidia-graphics)

```
sudo ubuntu-drivers autoinstall
```

#### For AMD Graphics:[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#for-amd-graphics)

The open-source drivers are usually included, but you can install the proprietary ones if needed:

```
sudo add-apt-repository ppa:kisak/kisak-mesa
sudo apt update && sudo apt upgrade
```

### 5\. Fix Time Synchronization Issues[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#5-fix-time-synchronization-issues)

To prevent time conflicts between Windows and Ubuntu:

In Ubuntu Terminal:

```
timedatectl set-local-rtc 1 --adjust-system-clock
```

### 6\. Post-Installation Script (Exclusive to This Guide)[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#6-post-installation-script-exclusive-to-this-guide)

Save time with our automated setup script that configures:

*   Optimal power settings
*   Improved performance tweaks
*   Common software installations
*   Proper dual-boot time synchronization

Create a file named `dual-boot-setup.sh`:

```
#!/bin/bash

# Update system
sudo apt update && sudo apt upgrade -y

# Install essential software
sudo apt install -y ubuntu-restricted-extras vlc gimp libreoffice timeshift gnome-tweaks

# Fix time synchronization
timedatectl set-local-rtc 1 --adjust-system-clock

# Optimize SSD if present
if [ -d "/sys/block/nvme0n1" ] || [ -d "/sys/block/sda" ]; then
  sudo apt install -y util-linux
  sudo systemctl enable fstrim.timer
fi

# Improve battery life
sudo apt install -y tlp tlp-rdw
sudo systemctl enable tlp

# Set up auto-cleaning
echo 'APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";' | sudo tee /etc/apt/apt.conf.d/20auto-upgrades

# Performance improvements
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf

# Check and repair GRUB if needed
sudo update-grub

echo "Setup complete! Reboot for changes to take effect."
```

Make it executable and run:

```
chmod +x dual-boot-setup.sh
./dual-boot-setup.sh
```

Part 5: Using Your Dual-Boot System[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#part-5-using-your-dual-boot-system)
--------------------------------------------------------------------------------------------------------------------------------

### 1\. The GRUB Boot Menu[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#1-the-grub-boot-menu)

After restart, you’ll see the GRUB menu where you can select:

*   Ubuntu 25.04
*   Windows 11

![Image 6: Computer with dual boot screen showing Windows 11 and Ubuntu 25.04 logos](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/dual-boot-windows-11-and-ubuntu-create-ubuntu_hu_c604ce75a0d02081.webp)

_The GRUB boot menu lets you choose which operating system to use_

### 2\. Accessing Windows Files from Ubuntu[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#2-accessing-windows-files-from-ubuntu)

Ubuntu can read your Windows files:

1.  Open **Files** in Ubuntu
2.  Look for your Windows drive in the sidebar

**Warning:** Writing to NTFS partitions from Ubuntu may require additional setup:

```
sudo apt install ntfs-3g
```

### 3\. Accessing Ubuntu Files from Windows[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#3-accessing-ubuntu-files-from-windows)

To access Linux files from Windows 11:

1.  Install WSL2 in Windows
2.  Install the WSL Ubuntu extension
3.  Use `\\wsl$\Ubuntu\home\yourusername` in File Explorer

Alternatively, install [Paragon Linux File Systems for Windows](https://www.paragon-software.com/home/linuxfs-windows/)

### 4\. Changing Default Operating System[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#4-changing-default-operating-system)

To change which system boots by default:

#### Graphical Method:[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#graphical-method)

1.  Install GRUB Customizer:
    
    ```
    sudo apt install grub-customizer
    ```
    
2.  Launch GRUB Customizer
3.  Go to “General Settings” tab
4.  Change “Default entry” to your preference
5.  Click Save

#### Terminal Method:[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#terminal-method)

1.  In Ubuntu, open Terminal
2.  Type `sudo nano /etc/default/grub`
3.  Change `GRUB_DEFAULT=0` to your preference (0 is usually Ubuntu)
4.  Set `GRUB_TIMEOUT=10` for a longer selection time
5.  Press Ctrl+X, then Y to save
6.  Run `sudo update-grub`

### 5\. Optimizing Performance in Dual-Boot Configuration[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#5-optimizing-performance-in-dual-boot-configuration)

#### For Windows:[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#for-windows)

1.  Disable indexing on drives shared with Linux
2.  Use Storage Sense to automatically free up space
3.  Disable unnecessary startup programs

#### For Ubuntu:[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#for-ubuntu)

1.  Reduce swappiness for better performance:
    
    ```
    sudo echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
    ```
    
2.  Enable zRAM for better memory management:
    
    ```
    sudo apt install zram-config
    ```
    

Part 6: Advanced Techniques and Alternatives[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#part-6-advanced-techniques-and-alternatives)
--------------------------------------------------------------------------------------------------------------------------------

### 1\. Using Separate Hard Drives (Ideal Setup)[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#1-using-separate-hard-drives-ideal-setup)

If your computer supports multiple drives:

1.  Install Windows on first drive
2.  Install Ubuntu on second drive
3.  Configure BIOS/UEFI boot order or use boot menu to select OS

Benefits:

*   No partition resizing needed
*   Each OS gets a full drive
*   Eliminates most dual-boot conflicts

### 2\. Virtualization as Alternative[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#2-virtualization-as-alternative)

#### Windows as Host:[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#windows-as-host)

1.  Enable virtualization in BIOS/UEFI
2.  Install WSL2 for Linux command-line:
    
    ```
    wsl --install
    ```
    
3.  Or install VirtualBox/VMware for full Ubuntu desktop

#### Ubuntu as Host:[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#ubuntu-as-host)

1.  Install VirtualBox or GNOME Boxes:
    
    ```
    sudo apt install virtualbox
    ```
    
2.  Create Windows 11 VM (requires valid license)

### 3\. Timeshift for System Backup[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#3-timeshift-for-system-backup)

Create system snapshots before major changes:

```
sudo apt install timeshift
sudo timeshift --create --comments "Fresh Ubuntu installation"
```

### 4\. Custom GRUB Theme (Make Your Dual-Boot Stylish)[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#4-custom-grub-theme-make-your-dual-boot-stylish)

1.  Download a theme from [GRUB Themes](https://www.gnome-look.org/browse/cat/109/)
2.  Extract the theme to `/boot/grub/themes/`
3.  Edit GRUB configuration:
    
    ```
    sudo nano /etc/default/grub
    ```
    
4.  Add/modify: `GRUB_THEME="/boot/grub/themes/theme-name/theme.txt"`
5.  Update GRUB:
    
    ```
    sudo update-grub
    ```
    

Part 7: Real-World Use Cases[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#part-7-real-world-use-cases)
----------------------------------------------------------------------------------------------------------------------------

### 1\. Developer Workstation[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#1-developer-workstation)

Optimal configuration:

*   Windows for Adobe Suite, Microsoft Office, and gaming
*   Ubuntu for development (Docker, VS Code, programming languages)
*   Shared data partition in exFAT format
*   Git repositories on the Linux partition

### 2\. Data Science Setup[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#2-data-science-setup)

*   Windows for Power BI and Excel analysis
*   Ubuntu for Python, R, and machine learning frameworks
*   Large data storage on separate drive accessible to both OSs
*   Jupyter notebooks in shared folder

### 3\. Gaming and Multimedia[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#3-gaming-and-multimedia)

*   Windows for AAA gaming titles
*   Ubuntu for day-to-day browsing and work
*   Steam installed on both systems with shared library folder
*   Proton configured for Windows games on Linux

Part 8: Troubleshooting Common Issues[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#part-8-troubleshooting-common-issues)
--------------------------------------------------------------------------------------------------------------------------------

### Windows Not Showing in GRUB Menu[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#windows-not-showing-in-grub-menu)

If Windows doesn’t appear in the boot menu:

1.  Boot into Ubuntu
2.  Open Terminal
3.  Type `sudo os-prober`
4.  Then `sudo update-grub`

### Ubuntu Won’t Boot After Windows Update[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#ubuntu-wont-boot-after-windows-update)

Windows updates may overwrite GRUB. To fix:

1.  Boot from Ubuntu USB in “Try Ubuntu” mode
2.  Open Terminal
3.  Run Boot Repair:
    
    ```
    sudo add-apt-repository ppa:yannubuntu/boot-repair
    sudo apt update
    sudo apt install boot-repair
    boot-repair
    ```
    
4.  Select “Recommended repair”

### Fixing Secure Boot Issues[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#fixing-secure-boot-issues)

If Ubuntu won’t boot with Secure Boot enabled:

1.  Boot into UEFI settings
2.  Disable Secure Boot temporarily
3.  Boot into Ubuntu
4.  Run:
    
    ```
    sudo apt install sbsigntool
    sudo update-secureboot-policy
    ```
    

### Recovering Windows Bootloader[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#recovering-windows-bootloader)

If you need to restore Windows boot without Ubuntu:

1.  Boot from Windows installation media
2.  Select “Repair your computer”
3.  Go to Troubleshoot \> Advanced Options \> Command Prompt
4.  Run:
    
    ```
    bootrec /fixmbr
    bootrec /fixboot
    bootrec /rebuildbcd
    ```
    

Part 9: Uninstalling Either OS (If Needed)[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#part-9-uninstalling-either-os-if-needed)
--------------------------------------------------------------------------------------------------------------------------------

### Removing Ubuntu while keeping Windows:[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#removing-ubuntu-while-keeping-windows)

1.  Boot into Windows
2.  Open Disk Management
3.  Delete the Ubuntu partitions
4.  Expand Windows partition
5.  Repair Windows boot using installation media

### Removing Windows while keeping Ubuntu:[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#removing-windows-while-keeping-ubuntu)

1.  Boot into Ubuntu
2.  Use GParted to delete Windows partitions:
    
    ```
    sudo apt install gparted
    sudo gparted
    ```
    
3.  Expand Ubuntu partitions as needed
4.  Update GRUB:
    
    ```
    sudo update-grub
    ```
    

Conclusion[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#conclusion)
-----------------------------------------------------------------------------------------

Congratulations! You now have a dual-boot system with Windows 11 and Ubuntu 25.04. Enjoy the flexibility of choosing between two powerful operating systems depending on your needs.

Remember that Ubuntu offers amazing performance with lower system requirements than Windows, making it perfect for:

*   Programming
*   Web development
*   Office work
*   Multimedia
*   Gaming (with Steam’s Proton compatibility layer)

This dual-boot setup gives you the freedom to use the best tool for each job, while our performance optimizations ensure both systems run at their best.

### Recommended Next Steps[#](https://merox.dev/blog/windows-11-ubuntu-25-04-dual-boot-guide/#recommended-next-steps)

1.  Set up cloud synchronization across both OSs (Dropbox, OneDrive, etc.)
2.  Configure SSH keys and development environments in Ubuntu
3.  Create your ideal productivity workflow between the two systems
4.  Explore Linux gaming with Proton and Steam

If you have any questions, need help with your specific hardware, or want to share your dual-boot experience, leave a comment below!

* * *