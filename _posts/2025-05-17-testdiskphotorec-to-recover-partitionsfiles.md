---
tags: [scratchpad]
info: aberto.
date: 2025-05-17
type: post
layout: post
published: true
slug: testdiskphotorec-to-recover-partitionsfiles
title: 'TestDisk/PhotoRec to Recover Partitions/Files'
---
**Critically Important Disclaimers:**

*   **Data Loss Risk:** Any operation on a damaged or corrupted drive carries an inherent risk of further data loss, especially if incorrect options are chosen. Proceed with extreme caution.
*   **No Guarantee of Success:** Data recovery is not guaranteed. Success depends on the nature and extent of the corruption and the physical health of the SD card.
*   **Patience is Key:** Some scanning processes, particularly `Deeper Search`, can take many hours, or even days for very large or slow/damaged drives. Do not interrupt them unnecessarily.
*   **Command-Line Familiarity:** This guide assumes a basic comfort level with the Linux command-line interface.

---

### **Phase 1: Preparation & Utmost Safety**

**1. Install TestDisk:**
If TestDisk is not already installed on your system, open a terminal and install it.
*   For Debian/Ubuntu-based systems (like Linaro):
    ```bash
    sudo apt update
    sudo apt install testdisk
    ```
*   For Fedora/CentOS/RHEL-based systems:
    ```bash
    sudo dnf install testdisk
    ```

**2. CRITICAL - Create a Disk Image (Highly Recommended):**
Operating directly on a potentially failing or corrupted SD card can worsen the situation or lead to irreversible data loss. The **safest approach** is to create a bit-by-bit image of the SD card on another healthy storage device. You will then run TestDisk on this image file.

*   **Storage Requirement:** You need enough free space on another drive (e.g., your `/mnt/mSATA` drive) to store the image. The image file will be the same size as your SD card (approximately 477.5 GiB).
*   **Identify Your SD Card:** Your logs confirm it as `/dev/sdb`. **Double-check this device name (`lsblk` can help confirm) before proceeding to avoid imaging the wrong drive!**
*   **Unmount SD Card Partitions (if any are mounted):**
    ```bash
    sudo umount /dev/sdb*
    ```
    (The `*` acts as a wildcard for any partitions like `/dev/sdb1`).
*   **Create the Image using `dd`:**
    ```bash
    sudo dd if=/dev/sdb of=/mnt/mSATA/sdb_image.img bs=4M status=progress conv=noerror,sync
    ```
    *   `if=/dev/sdb`: **Input File** (your SD card). Verify this is correct!
    *   `of=/mnt/mSATA/sdb_image.img`: **Output File** (the image). Choose a path and filename that makes sense for you.
    *   `bs=4M`: Sets the block size, which can improve copying speed.
    *   `status=progress`: Shows the progress of the `dd` command.
    *   `conv=noerror,sync`: This is crucial. `noerror` tells `dd` to continue if it encounters read errors on the source drive. `sync` fills input blocks with zeros if there were read errors, ensuring the output image maintains correct offsets.
    *   This process will take a significant amount of time. Be patient.

    **If you successfully create and use an image, all subsequent `testdisk` commands in this guide should target the image file (e.g., `sudo testdisk /mnt/mSATA/sdb_image.img`) instead of `/dev/sdb`.**

**3. If Not Using an Image (Significantly Riskier):**
If you choose to operate directly on `/dev/sdb` (not recommended):
*   Ensure all its partitions are unmounted: `sudo umount /dev/sdb*`
*   Be aware that any mistake or further drive degradation could lead to permanent data loss.

---

### **Phase 2: Launching TestDisk & Initial Setup**

**1. Launch TestDisk:**
Open your terminal.
*   If working on the **SD card directly** (riskier):
    ```bash
    sudo testdisk
    ```
*   If working on the **disk image** (recommended):
    ```bash
    sudo testdisk /mnt/mSATA/sdb_image.img
    ```

**2. Log File Creation:**
TestDisk will first ask about log file creation.
*   Use the arrow keys to select `[ Create ]` (to create a new log file). This is generally recommended for troubleshooting.
*   Press `Enter` to confirm.

**3. Disk Selection:**
A list of detected storage media will be displayed.
*   Use the `Up/Down` arrow keys to navigate and highlight your target:
    *   `/dev/sdb` (should show its size, approx. 477 GiB, and model "Storage Device").
    *   Or, if using an image, `/mnt/mSATA/sdb_image.img`.
*   **Verify your selection carefully.**
*   Ensure `[ Proceed ]` is highlighted at the bottom and press `Enter`.

**4. Partition Table Type Selection:**
TestDisk will attempt to auto-detect the partition table type. Your `fdisk -l` log indicated `Disklabel type: dos`, which means an MBR (Master Boot Record) partition table.
*   Even if TestDisk defaults to `[None]` due to severe corruption, manually select `[ Intel ] Intel/PC partition` (this is for MBR-style partition tables).
*   Press `Enter`.

---

### **Phase 3: Searching for Lost Partitions**

**1. Main Menu - Analyse:**
You are now at TestDisk's main menu.
*   Select `[ Analyse ]` (Analyse current partition structure and search for lost partitions).
*   Press `Enter`.

**2. Current Partition Structure & Quick Search:**
TestDisk will display the current partition structure it can read. Given the logs, this will likely show errors, "No partition found," or the nonsensical partitions from your `fdisk` output.
*   Ensure `[ Quick Search ]` is highlighted at the bottom and press `Enter`.
*   TestDisk might ask: "Search for partitions created under Windows Vista or later? (Y/N)". This question helps TestDisk look for MBR partition signatures that might be placed according to newer standards or by specific operating systems. For exFAT (which your `lsblk -f` log indicated for `sdb`), answering `Y` (Yes) is generally a good starting point. Press `Y`.
*   The Quick Search will begin. This may take some time.

**3. Interpreting Quick Search Results:**
Once the scan completes, TestDisk will list any potential partition candidates it found.
*   **Look for a partition that matches your expected exFAT partition:**
    *   It should be marked as `P` (Primary). Other types include `*` (Primary, bootable), `L` (Logical), `E` (Extended), `D` (Deleted).
    *   It should span a significant portion of your ~477.5 GiB card.
    *   The filesystem type might be identified as `HPFS/NTFS/exFAT` or similar. The partition label (e.g., "samsung500G") might not be directly visible in this partition list but can be confirmed if you successfully list files.
*   **CRUCIAL STEP - Verify by Listing Files:**
    *   Use the `Up/Down` arrow keys to highlight a promising partition candidate.
    *   Press `P` on your keyboard. This attempts to list the files and folders within that found partition.
    *   **If you see your expected files and directory structure:** This is a very positive sign! The partition and its filesystem are likely recoverable. Press `Q` to return to the partition list.
    *   **If the file listing is empty, shows garbage, or you get an error like "Can't open filesystem":** This partition candidate is likely incorrect, or the filesystem within it is also severely damaged. Press `Q` to return to the partition list and try another candidate if available.
*   **If multiple candidates are found:** Use your judgment. For a typical SD card used for storage, you're usually looking for a single, large `P` (Primary) partition. Avoid small, overlapping, or 'Extended' partitions unless you specifically created such a layout. Check start/end sectors for plausibility.

**4. Deeper Search (If Quick Search is Insufficient):**
If `Quick Search` doesn't find your main partition, or if listing files (`P`) doesn't show your data for any found candidates:
*   Ensure you are on the screen listing the (Quick Search) found partitions (or the screen that says no partitions were found).
*   Select `[ Deeper Search ]` from the options at the bottom.
*   Press `Enter`.
*   `Deeper Search` scans the drive much more thoroughly, sector by sector. **This process will take considerably longer (potentially many hours).** Be patient.
*   Once `Deeper Search` completes, it will present another list of partition candidates. Again, for each promising candidate, highlight it and press `P` to list files and verify it's your data. Press `Q` to return from the file listing.

---

### **Phase 4: Recovering Data by Copying Files (Primary & Safest Goal)**

This is the **most recommended first step** to retrieve your data, as it does not modify the source drive/image.

1.  **Access File Listing:**
    *   After a `Quick Search` or `Deeper Search` has found a partition candidate, and you have verified with `P` that it lists your files correctly:
        *   Ensure that correct partition is highlighted in the list.
        *   If you are not already viewing the files (i.e., you pressed `Q` to go back to the partition list), press `P` again to re-enter the file listing for that partition.

2.  **Navigate and Select Files/Folders:**
    *   Inside the file listing:
        *   Use `Up/Down` arrow keys to navigate.
        *   Select `.` to stay in the current directory, `..` (or press the `Left` arrow key) to go to the parent directory.
        *   Press `Right` arrow key or `Enter` to enter a highlighted directory.
    *   **To select items for copying:**
        *   Highlight a single file or folder you want to copy.
        *   Press `:` (colon) to select the currently highlighted item. Selected items usually change color.
        *   Repeat for other individual items if needed.
        *   To select **all** items in the current directory listing, press `a`.

3.  **Copy Selected Files/Folders:**
    *   Once you have selected the desired file(s) or folder(s):
        *   Press `C` (uppercase C) to initiate the copy process for the selected items.
    *   TestDisk will then switch to a file browser showing your system's *other* mounted filesystems. This is where you choose the **destination** for your recovered data.
        *   Navigate to a safe location on a different drive (e.g., a folder like `/mnt/mSATA/recovered_data_from_sdcard/`). **Do NOT save to the original SD card or its image!**
        *   Once you are in the correct destination directory in this browser view, press `C` (uppercase C) **again**. This confirms the destination and starts the actual copying process.
    *   You should see "Copy done!" messages for successfully copied items. If errors occur, note them.
    *   Repeat this process (navigate, select, copy) for all data you need to recover.

4.  **Exiting File Listing/Copy Mode:**
    *   Press `Q` to go back from the file listing to the partition list.

---

### **Phase 5: Attempting to Write Partition Table (Optional, Secondary, Riskier Goal)**

**Only attempt this phase if:**
*   You have **already successfully copied all your important files** to a safe location using Phase 4.
*   OR you are working on a **disk image** and are comfortable with the risk of potentially making the image unreadable if the wrong structure is written.
*   This step attempts to repair the SD card's (or image's) partition table so it might be recognized by the system normally.

1.  **Select the Correct Partition(s) for Writing:**
    *   In the list of partitions found by TestDisk (after Quick or Deeper Search), ensure the partition(s) that correctly showed your files with `P` are highlighted.
    *   The status should typically be `P` (Primary). If TestDisk misidentified a partition type (e.g., a Linux partition as FAT), you could *cautiously* use `T` to change its type, but for a standard exFAT data drive, this is usually not necessary and best avoided unless you are certain.
2.  **Proceed to Write:**
    *   Once you are confident in the selected partition structure, press `Enter` to continue from the partition list screen (if you are not already on the screen with the `[ Write ]` option).
3.  **Write the Partition Table:**
    *   Select `[ Write ]` from the options at the bottom and press `Enter`.
    *   TestDisk will ask for confirmation: "Write partition table, confirm? (Y/N)".
    *   **Think carefully.** If you are sure, press `Y` to confirm and write the new partition table.
4.  **Post-Write Action:**
    *   TestDisk will usually advise that you need to reboot your computer for the changes to take effect if you operated on `/dev/sdb` directly.
    *   Select `[ Quit ]` and exit TestDisk.

---

### **Phase 6: Post-Recovery Actions**

1.  **Verify Recovered Data:**
    *   Thoroughly check the files you copied (from Phase 4) to your recovery drive. Open various file types to ensure they are intact and not corrupted.

2.  **If You Wrote a New Partition Table (Phase 5):**
    *   **If working on `/dev/sdb` directly:** Reboot your computer.
    *   After rebooting (or if working on an image, you might try to mount it using loopback devices), check if the system now recognizes the SD card and its partition(s).
    *   If accessible, **immediately back up any remaining data you couldn't copy via TestDisk's file copy, if any.**
    *   **Run `fsck` (Filesystem Check):**
        *   Identify the partition (e.g., `/dev/sdb1`).
        *   Unmount it if mounted: `sudo umount /dev/sdb1`
        *   Run the filesystem check for exFAT:
            ```bash
            sudo fsck.exfat /dev/sdb1
            ```
            (or `sudo exfatfsck /dev/sdb1` depending on your system's exFAT utilities).
        *   Follow any prompts. This can repair minor filesystem inconsistencies.

3.  **Future of the SD Card:**
    *   **If data recovery was successful but the card showed severe corruption:** This SD card is highly suspect. Its reliability is questionable.
    *   **Consider a Full Reformat:** After ensuring all data is safe, you might try a full (low-level) reformat of the SD card to see if it can be made stable. This involves deleting all partitions, creating a new partition table, and then formatting. Tools like `gparted` (GUI) or `fdisk`/`mkfs.exfat` (CLI) can be used.
        *   **Example of zeroing out (ERASES EVERYTHING ON /dev/sdb - EXTREME CAUTION):**
            ```bash
            # sudo dd if=/dev/zero of=/dev/sdb bs=4M status=progress
            ```
            **TRIPLE CHECK `of=/dev/sdb` IS CORRECT BEFORE RUNNING!**
        *   Then create a new partition table (e.g., MBR with `fdisk`) and format (e.g., `mkfs.exfat`).
    *   **If the card continues to exhibit problems:** Discard it to prevent future data loss. It's likely at the end of its life or has irreparable hardware issues.

---

### **Phase 7: If TestDisk Fails to Recover Partitions or List Files**

If TestDisk's `[ Analyse ]` features (even `Deeper Search`) cannot find a usable partition structure, or if the filesystem within a found partition is too damaged to list files:

*   **Consider PhotoRec:**
    *   PhotoRec is a file data recovery software that comes bundled with TestDisk (you can usually run it with `sudo photorec`).
    *   It works differently: it ignores the filesystem and carves files directly from the raw data based on known file headers and footers.
    *   **Pros:** Can often recover files even when the filesystem is completely destroyed.
    *   **Cons:** Recovers files without their original filenames, directory structure, or timestamps. Files are typically renamed and sorted by type into output directories.
    *   PhotoRec is also menu-driven. You'll select the disk/image, choose file types to search for (you can often select all or specific ones like .jpg, .doc, etc.), and specify a destination directory for recovered files.