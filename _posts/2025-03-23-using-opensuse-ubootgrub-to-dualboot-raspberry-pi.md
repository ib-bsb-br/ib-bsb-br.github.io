---
tags: [scratchpad]
info: aberto.
date: 2025-03-23
type: post
layout: post
published: true
slug: using-opensuse-ubootgrub-to-dualboot-raspberry-pi
title: 'using openSUSE uboot/grub to dualboot raspberry pi'
---
──────────────────────────────
1. BACK UP AND PREPARE

 • Before you begin, back up your current SD card image. Use a tool such as dd or a disk imaging utility on your desktop so you can revert to a known–good state if something goes wrong.

 • Make sure you have a working Linux system (or live USB) with partitioning tools (like fdisk, gdisk, or the graphical tool GParted) and text editors.

──────────────────────────────
2. UNDERSTANDING THE DEFAULT PARTITION SCHEME

openSUSE Tumbleweed for the Raspberry Pi typically uses a partition layout similar to:

 – An EFI System Partition (ESP) formatted as FAT32; usually between 100 MB and 500 MB in size.  
 – A root filesystem partition (often Btrfs or ext4) that holds the operating system.  
 – Optionally, a separate /home partition if you chose a custom install.

It is essential that you keep the ESP intact because the boot chain (U‑Boot loads the EFI bootloader, which then invokes GRUB) resides there. (See discussion on recommended EFI sizes in [Reddit](https://www.reddit.com/r/openSUSE/comments/1ddf3dx/efi_partition_size_and_other_things/).)

──────────────────────────────
3. PLANNING THE DUAL-BOOT SETUP

Decide how you want to install the second OS. Your options include:  

 a. Shrinking the existing root (or /home) partition to make space for a new “root” partition for the second OS.  
 b. Using an SD card with extra physical space so you can create a new partition(s) for the second OS.

Because the ESP is shared, you’ll be adding the new OS’s boot files (or chainloader entry) to the same ESP without overwriting openSUSE’s files. (For strategy ideas, see [HCL:Raspberry_Pi4](https://en.opensuse.org/HCL:Raspberry_Pi4).)

──────────────────────────────
4. MODIFYING THE PARTITION LAYOUT

Step 4.1. Examine your current partitions  
 Open a terminal and use, for example: 

  # lsblk  
  # fdisk -l /dev/mmcblk0

You should see something like:  
  • /dev/mmcblk0p1 – EFI partition (FAT32)  
  • / dev/mmcblk0p2 – root partition (Btrfs/ext4)  

Step 4.2. Resize the existing partition(s)  
 • Unmount the partition(s) that need resizing. If your root is mounted, you may need to use a live USB environment.  
 • Launch GParted or use command-line tools (e.g., parted) to shrink the root partition. For example, in GParted:  
  – Select the root partition, choose “Resize/Move”, and shrink it to leave free space at the end of the SD card.  
 • Apply the changes and note the new free (unallocated) space.

Step 4.3. Create a new partition for the second OS  
 • Within the unallocated space, create a new primary partition. (For Linux, you can choose ext4 or Btrfs as desired.)  
 • Label it (for example, “SECOND_OS_ROOT”) so that you can identify it later.  

Note: Always verify the partition table (using fdisk or GParted preview) so that the ESP remains unaltered.

──────────────────────────────
5. INSTALLING THE SECOND OS INTO THE NEW PARTITION

There are several ways to install the second OS onto the new partition. One common method is:

 a. Prepare an installation image (or manually extract the OS root filesystem) for the second OS on your desktop.  
 b. Mount the new partition and extract/copy the OS files. For example:

  # mkdir /mnt/second_os  
  # mount /dev/mmcblk0p3 /mnt/second_os  
  # rsync -aHAX --exclude={"/dev/*","/proc/*","/sys/*","/tmp/*","/run/*"} /path/to/second_os_root/ /mnt/second_os/

 c. Make sure that the new OS’s fstab (or boot configuration) points to the correct partitions (using UUIDs is recommended) and that it has its own bootable kernel and initrd available.

──────────────────────────────
6. THE BOOT CHAIN: U‑BOOT, EFI, GRUB, AND UEFI WORKAROUND

openSUSE on the Pi uses a U‑Boot binary (often named u-boot.bin) stored in the EFI partition. Under certain conditions (or known bugs), you might need to replace this file with an updated version from a mirror (see [Linux Kamarada’s guide](https://linuxkamarada.com/en/2020/12/26/tumbleweed-needs-a-workaround-to-boot-on-the-raspberry-pi-4/)). If you notice boot issues (for example, “Waiting for PHY auto negotiation…” messages), then:

 • Download the updated u-boot.bin (from a reliable source such as the openSUSE ARM mailing list archives).  
 • Mount the ESP (if not already mounted, for example, as /boot/efi):

  # mount /dev/mmcblk0p1 /boot/efi

 • Backup the original and copy the new file:

  # cp /boot/efi/u-boot.bin /boot/efi/u-boot.bin.bak  
  # cp /path/to/new/u-boot.bin /boot/efi/u-boot.bin

 Make sure that after the boot, openSUSE still boots normally before proceeding with GRUB changes.

──────────────────────────────
7. CONFIGURING GRUB FOR DUAL-BOOT

Now you must modify GRUB’s configuration so that when the Pi boots, you can choose which OS to start.

Step 7.1. Identify the kernel and initrd files for the second OS  
 Place these files on a location accessible via the EFI partition if needed or directly from the new root partition (it’s common to store the second OS’s boot files in its own /boot folder).

Step 7.2. Edit GRUB’s custom configuration  
 In openSUSE, you can add a manual menu entry in “/etc/grub.d/40_custom” (or a similar custom script file). For example, add the following entry:

  ----------------------------------------
  menuentry "Second OS" {
   insmod part_gpt
   insmod fat
   # If your second OS kernel and initrd are stored in the new partition mounted at /boot/second_os,
   # adjust the search command to match the UUID or label of that partition.
   search --no-floppy --fs-uuid --set=root YOUR_SECOND_OS_UUID
   echo "Loading second OS kernel..."
   linux /boot/second_os/vmlinuz root=UUID=YOUR_SECOND_OS_ROOT_UUID ro quiet
   echo "Loading second OS initrd..."
   initrd /boot/second_os/initrd.img
  }
  ----------------------------------------

 Here, replace YOUR_SECOND_OS_UUID and YOUR_SECOND_OS_ROOT_UUID with the correct UUIDs. To find a partition’s UUID, run:

  # blkid /dev/mmcblk0p3

Step 7.3. Update the GRUB configuration file  
 After saving your custom entry, update GRUB:

  # grub2-mkconfig -o /boot/grub2/grub.cfg

 (Depending on your system, you may use “grub2-mkconfig” or “update-grub”.) This command scans the system and integrates the custom menu entry into GRUB.

──────────────────────────────
8. FINAL STEPS AND TESTING

 • Reboot your Raspberry Pi. At the GRUB menu, you should now see an entry for “Second OS”. Using a keyboard (or if you’ve enabled network/serial access), select it.

 • Test booting into both operating systems. If you experience issues:
  – Revisit the UUIDs in the GRUB entry.  
  – Ensure that the second OS’s kernel and initrd files are correctly referenced.  
  – Check boot logs (from both GRUB and systemd) for errors.

 • If necessary, adjust parameters (such as removing “quiet” or adding “console=ttyAMA0” for serial debug messages) to help troubleshoot any boot issues.

──────────────────────────────
9. TROUBLESHOOTING AND NOTES

 • If the Pi does not boot without an HDMI display (a common quirk), add the following line to the ESP’s config.txt (found in /boot/efi on the FAT32 partition):

  hdmi_force_hotplug=1

 • Be mindful that modifications to the EFI partition affect both OS’s boot processes. Always back up the entire ESP before making changes.

 • Dual-booting on embedded systems may require iterative debugging. Tools such as a serial console can be invaluable, and reviewing messages from GRUB or U-Boot is essential.

──────────────────────────────
SUMMARY

This tutorial outlined how to:
 1. Back up your existing installation.
 2. Assess and shrink your partition layout while preserving the EFI System Partition.
 3. Create a new partition and install a second OS by copying its root filesystem.
 4. Replace or update u-boot.bin (if needed) in the EFI partition.
 5. Manually add a GRUB menuentry (in /etc/grub.d/40_custom) referencing your second OS’s kernel, initrd, and root partition.
 6. Update GRUB and test your dual-boot configuration.

By following these steps carefully, you can maintain openSUSE Tumbleweed’s native boot chain while adding support for another OS.