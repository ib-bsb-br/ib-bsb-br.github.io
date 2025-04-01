---
tags: [maybe]
info: aberto.
date: 2025-04-01
type: post
layout: post
published: true
slug: to-boot-multiple-operating-systems-portably-using-ventoy
title: 'to boot multiple operating systems portably using ventoy'
---
* **How it Works:** You install Ventoy onto the external drive once. It creates boot partitions and leaves the remaining space as a large data partition (usually exFAT or NTFS). You then simply copy your OS installer `*.iso` files, WinPE images (`*.iso` or `*.wim`), and even full Windows installations packaged in virtual hard disk files (`*.vhd` or `*.vhdx`) onto this data partition. When you boot from the Ventoy drive, it scans the data partition and presents a menu listing all compatible files, allowing you to boot directly from them.
* **Pros:**
    * Extremely easy to set up and manage – just copy/delete files to add/remove OS options.
    * No complex manual partitioning required for each OS.
    * Excellent compatibility with UEFI (including Secure Boot) and Legacy BIOS modes.
    * Supports a wide variety of image types (`.iso`, `.wim`, `.img`, `.vhd`, `.vhdx`).
    * Supports persistence for many Linux live ISOs (saving changes across boots, requires creating a persistence file).
    * Can directly boot full Windows installations from VHD(x) files.
* **Cons:**
    * Slight boot overhead compared to a direct installation (usually negligible).
    * Performance of OSs running from VHD(x) depends on the VHD type (fixed vs. dynamic), the underlying drive speed, and the USB connection.
    * While compatibility is high, rare niche ISOs might have issues.
* **Setup Steps:**
    1.  Download the Ventoy tool from the official website.
    2.  Run the tool and install Ventoy onto your 1TB external HDD (this will erase the drive initially!). Choose the desired partition scheme (MBR for legacy, GPT for UEFI recommended).
    3.  Once Ventoy is installed, the drive will appear with a large partition. Copy your desired files onto this partition:
        * Linux ISOs (e.g., `ubuntu-lts.iso`)
        * Windows Installer ISOs (e.g., `windows11.iso`, `windows81.iso`)
        * WinPE ISOs or WIMs.
        * **For full Windows installs (Win 11/8.1 To Go style):** Create a VHD(x) file first:
            * **Method A (Recommended): Install directly to VHD:**
                * Use `Disk Management` (diskmgmt.msc) in Windows to create a new VHD(x) file (choose VHDX, Fixed size for better performance, allocate sufficient space like 64GB+).
                * Attach the created VHD(x) file in Disk Management (it will appear as a new uninitialized disk). Initialize it (GPT recommended) and create a simple volume (format NTFS).
                * Boot your computer using a standard Windows Installer USB/ISO (you can even boot the Windows ISO via Ventoy itself).
                * At the "Where do you want to install Windows?" screen, press `Shift+F10` to open Command Prompt. Use `diskpart` commands to list volumes (`list volume`) identify the drive letter of your attached VHD, and select the correct partition.
                * Proceed with the installation, selecting the partition on the attached VHD as the target.
                * After installation completes *inside the VHD*, detach the VHD in Disk Management.
            * **Method B (Capture Existing):** Use a tool like `disk2vhd` (from Microsoft Sysinternals) to capture an existing Windows installation into a VHD(x) file.
            * Copy the final `*.vhdx` file onto the Ventoy data partition.
    4.  Safely eject the drive. Boot your target computer from the USB drive. Ventoy's menu should appear, allowing you to select and boot your desired OS image or VHD.