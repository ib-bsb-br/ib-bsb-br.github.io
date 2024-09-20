---
tags:
  - linux
info: aberto.
date: 2024-08-02
type: post
layout: post
published: true
slug: how-to-use-the-dd-command-to-create-a-bootable-usb-drive-from-an-iso-file-on-a-linux-based-system
title: 'How to use the `dd` command to create a bootable USB drive from an ISO file on a Linux-based system'
---

### Prerequisites

1. **ISO File**: Ensure you have downloaded the Windows ISO file you want to use.
2. **USB Drive**: Insert a USB drive into your computer. Confirm that it has sufficient space for the ISO file and back up any important data, as this process will erase the USB drive.
3. **Terminal Access**: You need access to a terminal or command line interface.

### Step-by-Step Guide

#### Step 1: Identify the USB Drive

1. Open a terminal.
2. Run the following command to list all connected drives:

   ```bash
   lsblk
   ```

   This command displays a list of block devices. Identify your USB drive by its size and name, which will typically be listed as `/dev/sdb`, `/dev/sdc`, etc. Ensure you correctly identify the USB drive to avoid overwriting other drives.

#### Step 2: Unmount the USB Drive

Before writing to the USB drive, you need to unmount it. Replace `/dev/sdX1` with the actual partition of your USB drive (e.g., `/dev/sdb1`).

```bash
sudo umount /dev/sdX1
```

If your USB drive has multiple partitions, you may need to unmount all of them. You can unmount all partitions of the USB drive using:

```bash
sudo umount /dev/sdX*
```

#### Step 3: Write the ISO to the USB Drive

Now, you can use the `dd` command to write the ISO file to the USB drive. Replace `/path/to/your.iso` with the path to your ISO file and `/dev/sdX` with your USB drive (without the partition number).

```bash
sudo dd if=/path/to/your.iso of=/dev/sdX bs=4M status=progress
```

- `if=`: Input file (the ISO file).
- `of=`: Output file (the USB drive).
- `bs=4M`: Sets the block size to 4 megabytes, which can speed up the process.
- `status=progress`: Displays the progress of the operation.

**Important Note**: Ensure that you do not include a partition number (like `sdX1`) in the `of=` parameter, as writing to a partition instead of the whole drive can lead to an incomplete or non-bootable USB.

#### Step 4: Wait for the Process to Complete

The `dd` command will take some time to complete, depending on the size of the ISO and the speed of your USB drive. Once it finishes, you will see a summary of how many bytes were copied.

#### Step 5: Sync and Eject the USB Drive

After the `dd` command completes, it’s a good practice to ensure all data is written to the USB drive before removing it. Run the following command:

```bash
sync
```

This command flushes the file system buffers, ensuring that all data is written to the USB drive.

Now you can safely eject the USB drive:

```bash
sudo eject /dev/sdX
```

### Important Considerations

- **Double-Check Device Names**: Be very careful with the `of=` parameter. If you specify the wrong device, you could overwrite important data on your hard drive.
- **Data Loss Warning**: This process will erase all data on the specified USB drive. Make sure to back up any important files before proceeding.
- **Booting from USB**: After creating the bootable USB drive, you can boot from it by changing the boot order in your BIOS/UEFI settings. You may need to press a specific key (like F2, F12, ESC, or DEL) during startup to access the boot menu.