---
tags: [scratchpad]
info: aberto.
date: 2025-05-24
type: post
layout: post
published: true
slug: rk3588-customization
title: 'RK3588 Customization'
---
## **0\. Before You Begin: Critical Considerations**

Modifying the core software of an embedded system like the VPC-3588, which is based on the Rockchip RK3588 SoC , involves advanced procedures that carry inherent risks. Before attempting any of the operations detailed in this report, it is crucial to understand and adhere to the following precautions:

* **Backup Everything:** This cannot be overstated. Before flashing new firmware, updating kernels, modifying bootloaders, or making any significant changes to the filesystem, create comprehensive backups. This includes:  
  * Bootloader components (e.g., idbloader.img, u-boot.itb).  
  * The entire eMMC or SD card if possible (using tools like dd or rkdeveloptool).  
  * Kernel and Device Tree Blob (DTB).  
  * Critical configuration files from your root filesystem.  
  * User data.  
* **Serial Console Access:** A USB-to-TTL serial console is an indispensable tool for debugging low-level issues. It provides access to U-Boot prompts, kernel boot messages, and a shell even if networking or graphical interfaces are non-functional. Ensure you have one and know how to use it with the VPC-3588.  
* **Use Correct Tools and Firmware:** Always verify that any tools (like rkdeveloptool), firmware images (U-Boot, kernel, full OS images), and loader files (e.g., SPL loaders for MaskROM mode) are specifically designed or compatible with the Rockchip RK3588 SoC and, critically, with the VPC-3588 motherboard. Using incorrect versions or files for different hardware is a primary cause of "bricking" a device. The information in this document often refers to general RK3588 practices or examples from other board vendors (e.g., Firefly , Radxa ); **always consult official Liontron documentation for the VPC-3588 if available, as their specific procedures, tools, or partition layouts may differ.** The provided Liontron links are primarily product pages and may not contain in-depth SDK or developer guides.  
* **Understand the Risks:** Operations like flashing firmware directly to eMMC, especially in MaskROM mode, can render the device unbootable if done incorrectly or if the image is corrupted. While MaskROM mode often provides a recovery path, it's not foolproof. Proceed with caution and ensure you understand each step.  
* **Stable Power Supply:** Ensure the VPC-3588 has a stable and adequate power supply during any flashing or update operation. Power loss during these critical moments can lead to data corruption or a bricked device.  
* **Rockchip Technical Reference Manual (TRM):** For the most in-depth hardware-level details about the RK3588 SoC, including boot sequences, memory maps, and peripheral operations, the Rockchip RK3588 Technical Reference Manual (TRM) is the definitive source. While direct access to the full TRM can sometimes be restricted, parts of it or summaries may be available through various online developer communities or upon request from Rockchip or board vendors.

This document outlines procedures for advanced users and developers. If you are unsure about any step, seek clarification from vendor documentation or experienced community members before proceeding.

## **1\. Introduction: The RK3588 Platform and Customization Overview**

The Rockchip RK3588 is a high-performance System-on-Chip (SoC) featuring a multi-core ARM CPU (Quad Cortex-A76 \+ Quad Cortex-A55), a capable Mali G610 MC4 GPU, and a powerful NPU for AI acceleration. The VPC-3588 motherboard leverages this SoC for various embedded applications. This report details advanced software modification and management techniques for this platform, covering kernel upgrades, bootloader handling, custom module integration, distribution analysis, and low-level recovery methods.  
A typical boot sequence on an RK3588 system involves several stages:

1. **BootROM (MaskROM):** Code embedded within the SoC that executes on power-on. It attempts to load the next stage bootloader from a predefined sequence of storage media (e.g., SPI flash, eMMC, SD card). If no valid bootloader is found, or if forced by hardware, it enters MaskROM USB mode.  
2. **SPL (Secondary Program Loader) / TPL (Tertiary Program Loader):** A small piece of code (often part of idbloader.img) loaded by the BootROM. Its primary role is to initialize DRAM and load the main U-Boot image.  
3. **U-Boot:** A versatile open-source bootloader. It initializes more hardware, provides a command-line interface, and is responsible for loading the Linux kernel, Device Tree Blob (DTB), and an optional initramfs into memory and then transferring execution to the kernel.  
4. **Linux Kernel:** The core of the operating system, managing hardware and software resources.  
5. **Root Filesystem:** Contains the user-space applications, libraries, and system utilities that form the complete operating environment (e.g., Debian Bullseye).

Understanding this hierarchy is crucial when performing modifications, as changes at one level can impact subsequent stages. The procedures outlined below address various aspects of this software stack.

## **2\. System Software Upgrades**

This section covers upgrading core software components: the Linux kernel, the C standard library (libc6), and the entire Debian distribution.

* **2.1. Upgrading the Linux Kernel (e.g., from 5.10)** Upgrading the Linux kernel on an RK3588 system like the VPC-3588 can be done in several ways, depending on the source of the kernel and the build system used. The stock kernel is often version 5.10 for RK3588 platforms. Newer kernel versions (e.g., 6.1 or later mainline versions) may offer improved hardware support, new features, or security patches.  
  * **2.1.1. Using Armbian or Similar Build Systems:** If using a distribution like Armbian, kernel upgrades are often managed through its package manager (apt) or build tools. Armbian provides different kernel branches (e.g., legacy, vendor, current, edge).  
    * To switch between kernel branches or update within a branch, you typically use apt to install the desired kernel image, headers, and DTB packages. For example, to switch from a legacy kernel to a vendor kernel, commands might resemble: sudo apt install linux-image-vendor-rockchip-rk3588 linux-dtb-vendor-rockchip-rk3588 linux-u-boot-\<board\>-vendor. (Note: Replace \<board\> with the specific board identifier used by Armbian for the VPC-3588, if available.)  
    * Building a custom kernel with Armbian involves using its build framework, selecting the board (e.g., a similar RK3588 board if VPC-3588 isn't directly listed), choosing the kernel branch, and potentially customizing the kernel configuration using kernel-config.  
  * **2.1.2. Using Vendor SDKs (e.g., Firefly SDK):** If a vendor SDK (like Firefly's for their RK3588 boards ) is used or adapted for the VPC-3588, kernel upgrades involve rebuilding the kernel within that SDK.  
    1. **Obtain Newer Kernel Source:** This might involve updating the SDK's kernel repository or manually integrating a newer kernel version.  
    2. **Configure:** Use the SDK's mechanism to configure the kernel (e.g., make menuconfig or modifying defconfig files specified in board configuration makefiles like RK\_KERNEL\_DEFCONFIG and RK\_KERNEL\_DEFCONFIG\_FRAGMENT ).  
    3. **Build:** Compile the kernel using the SDK's build scripts (e.g., ./build.sh kernel or ./build.sh extboot ).  
    4. **Package and Flash:** The SDK will typically produce a kernel image (boot.img, kernel.img, or part of a unified update.img) that needs to be flashed to the appropriate partition on the eMMC.  
  * **2.1.3. Manual Kernel Compilation (Mainline or Custom Source):** This is the most involved method.  
    1. **Get Kernel Source:** Clone the desired kernel tree (e.g., mainline Linux from kernel.org or a specific RK3588-focused branch).  
    2. **Toolchain:** Set up an AArch64 cross-compiler (e.g., gcc-aarch64-linux-gnu).  
    3. **Configuration:**  
       * Start with a base configuration for RK3588 (e.g., arch/arm64/configs/defconfig and vendor-specific fragments or a known good .config for a similar RK3588 board).  
       * Use make ARCH=arm64 CROSS\_COMPILE=aarch64-linux-gnu- menuconfig to customize.  
    4. **Build:** make ARCH=arm64 CROSS\_COMPILE=aarch64-linux-gnu- Image dtbs modules \-j$(nproc)  
    5. **Installation:**  
       * Copy the compiled Image (e.g., arch/arm64/boot/Image) and the relevant DTB (arch/arm64/boot/dts/rockchip/rk3588-\*.dtb) to the boot partition or package them into a boot image format recognized by U-Boot.  
       * Install modules to the rootfs: make ARCH=arm64 CROSS\_COMPILE=aarch64-linux-gnu- INSTALL\_MOD\_PATH=/path/to/rootfs modules\_install.  
       * Update U-Boot boot scripts/configuration if necessary to point to the new kernel/DTB.  
* **2.2. Updating libc6 (GNU C Library)** Updating libc6 (the GNU C Library) is a critical operation and is almost always tied to a full distribution upgrade (e.g., Debian Bullseye to Bookworm). **Attempting to upgrade libc6 in isolation from a distribution upgrade is extremely dangerous and highly discouraged, as it can very easily lead to an unstable, partially upgraded, or completely unbootable system due to ABI incompatibilities with other system libraries and applications.** If a newer libc6 is required, the proper procedure is to perform a full distribution upgrade as detailed in the next section.  
* **2.3. Upgrading from Debian Bullseye (e.g., to Debian Bookworm)** Upgrading a Debian-based system like the one likely on the VPC-3588 (assuming it ships with Bullseye, which is common for kernel 5.10 era devices ) to a newer release like Bookworm involves several steps. This process applies to ARM64 systems.  
  1. **Backup:** Before starting, ensure a full system backup is made. This is critical.  
  2. **Update Current System:** Make sure your current Bullseye system is fully up-to-date:  
     `sudo apt update`  
     `sudo apt upgrade`  
     `sudo apt full-upgrade`  
     `sudo apt autoremove`  
     Reboot if a kernel update occurred.  
  3. **Modify APT Sources:** Change all instances of bullseye to bookworm in /etc/apt/sources.list and any files in /etc/apt/sources.list.d/. A common command to do this for the main sources file is: sudo sed \-i 's/bullseye/bookworm/g' /etc/apt/sources.list. Ensure that non-free-firmware is included if your hardware requires it (it often does for Wi-Fi, Bluetooth, GPU, etc. on embedded boards). The line might look like: deb http://deb.debian.org/debian/ bookworm main contrib non-free-firmware.  
  4. **Update Package Lists for New Release:** sudo apt update  
  5. **Perform the Upgrade:** This is a two-step process for major upgrades:  
     * Minimal upgrade: sudo apt upgrade \--without-new-pkgs (This step is sometimes recommended, but apt full-upgrade is often sufficient directly).  
     * Full distribution upgrade: sudo apt full-upgrade. This command will handle installing new packages, removing obsolete ones, and resolving dependencies for Bookworm. You will likely be prompted about configuration file changes (choose carefully or review diffs) and restarting services. It's advisable not to run essential services during the upgrade.  
  6. **Reboot:** Once the upgrade completes, reboot the system: sudo reboot. The system should now boot into Debian Bookworm, likely with a newer kernel (e.g., Linux 6.x series).  
  7. **Post-Upgrade Cleanup:** Remove any obsolete packages: sudo apt \--purge autoremove.  
  8. **Verify:** Check the OS version: cat /etc/os-release.

  **Important Considerations for Distribution Upgrades on Embedded Systems:**

  * **Vendor Kernels/Drivers:** If the system relies on a specific vendor kernel or proprietary drivers not well-supported by the new distribution's mainline kernel, issues can arise. This is why using a distribution like Armbian, which often manages these complexities, can be beneficial. If upgrading a vendor-provided OS, check their documentation for supported upgrade paths.  
  * **Bootloader:** Ensure U-Boot is capable of booting the newer kernel if it changes significantly. Usually, this is not an issue if U-Boot is reasonably up-to-date.  
  * **NVIDIA Drivers (if applicable):** If any proprietary NVIDIA drivers are installed (unlikely for RK3588's integrated Mali GPU, but mentioned in generic Debian upgrade guides), they might need special handling or reinstallation.

## **3\. U-Boot Bootloader Management: Backup, Restore, and Unbricking**

The U-Boot bootloader is critical for system startup. It resides on the eMMC (or SPI flash, if used for primary boot) at specific offsets. Knowing how to back up, restore, and re-flash U-Boot is essential for recovery from "bricking" incidents where the bootloader gets corrupted. The primary tool for low-level flash access on Rockchip devices is rkdeveloptool.

* **3.1. Understanding U-Boot Components and Layout on RK3588** Rockchip boot often involves:  
  * idbloader.img: Contains the SPL (Secondary Program Loader) and TPL (Tertiary Program Loader), responsible for basic hardware initialization like DDR RAM. This is loaded by the SoC's internal BootROM.  
  * u-boot.itb (or similar, e.g., uboot.img): The main U-Boot binary, often packaged as an FIT (Flattened Image Tree) image. These are typically flashed to specific sector offsets on the boot media (e.g., eMMC). Common offsets for RK3588 are :  
  * idbloader.img: Often at sector 64 (0x40).  
  * u-boot.itb: Often at sector 16384 (0x4000). A combined image, sometimes named u-boot-rockchip.bin or rkspi\_loader.img, might also be used, containing both idbloader.img and u-boot.itb at their respective internal offsets, and this combined image is then flashed starting at sector 0 or 64 depending on the specific image and target (SPI vs eMMC). **Crucially, these offsets (e.g., 64s for idbloader.img, 16384s for u-boot.itb) are typical for some RK3588 U-Boot deployments but *must* be verified for the specific U-Boot binaries and partition layout intended for the VPC-3588. Incorrect offsets will lead to a non-booting device.** Consult official Liontron documentation for the VPC-3588 or analyze a working device if possible.  
* **3.2. Backing Up U-Boot** If the system is bootable and you have root access, you can use dd to back up U-Boot components directly from the eMMC device (e.g., /dev/mmcblkX). However, using rkdeveloptool with the device in Loader mode (if U-Boot is running) or MaskROM mode (if it's not) is generally safer and more common for these critical, raw partitions.  
  * **3.2.1. Using rkdeveloptool (Device in Loader/MaskROM Mode):**  
    1. Put the VPC-3588 into MaskROM mode (see Section 3.3.2) or ensure it's in Loader mode (detected by rkdeveloptool ld).  
    2. If in MaskROM mode, download the appropriate SPL loader: sudo rkdeveloptool db /path/to/rk3588\_spl\_loader.bin (The exact loader filename may vary, e.g., rk3588\_spl\_loader\_v1.08.111.bin or rk3588\_spl\_loader\_v1.15.113.bin ).  
    3. Read the idbloader partition (example: assuming it's 16320 sectors, which is (16383-64+1) sectors, and starts at sector 64): sudo rkdeveloptool read 64 $((16383 \- 64 \+ 1)) idbloader\_backup.img (This calculates size in sectors; rkdeveloptool read takes start sector and *byte count*. So, sudo rkdeveloptool read 64 $(( (16383 \- 64 \+ 1\) \* 512 )) idbloader\_backup.img)  
    4. Read the u-boot partition (example: assuming it's 16384 sectors and starts at sector 16384): sudo rkdeveloptool read 16384 $(( (32767 \- 16384 \+ 1\) \* 512 )) uboot\_backup.itb Alternatively, if your partition table is recognized and U-Boot partitions are named (e.g., "uboot", "idbloader"), you might use: sudo rkdeveloptool read-partition uboot uboot\_backup.img sudo rkdeveloptool read-partition idbloader idbloader\_backup.img (if such a partition name exists) Store these backup files securely.  
* **3.3. Restoring/Unbricking U-Boot** This procedure is typically done when the device fails to boot due to a corrupted bootloader. MaskROM mode is essential here.  
  * **3.3.1. Prerequisites:**  
    * Known-good U-Boot image files (idbloader.img, u-boot.itb, or a combined image like u-boot-rockchip.bin or rkspi\_loader.img) specific to the RK3588 and ideally for the VPC-3588.  
    * rkdeveloptool installed on a host PC.  
    * The correct SPL loader binary for RK3588 (e.g., rk3588\_spl\_loader\_vX.Y.Z.bin).  
  * **3.3.2. Procedure for Entering MaskROM Mode on RK3588 Devices:** The exact method to enter MaskROM mode can vary slightly depending on the specific board design of the VPC-3588. **Consult the official Liontron documentation for the VPC-3588 for the precise procedure.** General methods for RK3588-based devices include :  
    1. **Power Off:** Ensure the device is completely powered off. Disconnect the power supply.  
    2. **Hardware Trigger:**  
       * **MaskROM Button:** If the VPC-3588 motherboard has a dedicated MaskROM button (often labeled "Recovery", "Mask", or similar), press and hold this button.  
       * **Test Points/Jumpers:** If no button is present, the board's schematics or technical documentation may indicate specific test points on the PCB that need to be shorted (e.g., with tweezers or a jumper wire).  
    3. **Connect USB:** While maintaining the hardware trigger (holding the button or shorting points), connect a USB cable from the host PC to the VPC-3588's USB OTG port (this is often a specific Type-C port, check the VPC-3588 specs ).  
    4. **Apply Power:** Connect the power supply to the VPC-3588.  
    5. **Release Trigger:** After a few seconds (typically 2-5 seconds once power is applied and USB is connected), release the MaskROM button or remove the short from the test points. The device should now be in MaskROM mode. Verify on the host PC by running sudo rkdeveloptool ld. The output should list the device and indicate "Maskrom" mode.  
  * **3.3.3. Flashing U-Boot Components:**  
    1. **Enter MaskROM Mode:** As described above.  
    2. **Download SPL Loader:** sudo rkdeveloptool db /path/to/rk3588\_spl\_loader.bin (e.g., rk3588\_spl\_loader\_v1.08.111.bin or rk3588\_spl\_loader\_v1.15.113.bin)  
    3. **Flash idbloader.img (if flashing separately):** sudo rkdeveloptool wl 0x40 /path/to/idbloader.img (0x40 is decimal 64\)  
    4. **Flash u-boot.itb (if flashing separately):** sudo rkdeveloptool wl 0x4000 /path/to/u-boot.itb (0x4000 is decimal 16384\)  
    5. **Alternatively, Flash Combined Image (e.g., u-boot-rockchip.bin for eMMC or rkspi\_loader.img for SPI):**  
       * For eMMC, a combined image might be flashed starting at sector 64: sudo rkdeveloptool wl 0x40 /path/to/u-boot-rockchip.bin  
       * For SPI flash, a combined image is often flashed starting at sector 0: sudo rkdeveloptool wl 0 /path/to/rkspi\_loader.img **Again, verify the correct image type and target offset for the VPC-3588.**  
    6. **Reset Device:** sudo rkdeveloptool rd The device should now attempt to boot with the newly flashed U-Boot. If it still fails, double-check the image files, offsets, and MaskROM procedure. Erasing the flash (e.g., rkdeveloptool ef ) might be necessary in some extreme cases before re-flashing, but this is a destructive operation that will wipe all data.

## **4\. Kernel Customization: KVM, Patches, and Modules**

This section details how to customize the kernel by enabling features like KVM, applying patches, and building/integrating kernel modules. This often requires a kernel source tree and a build environment.

* **4.1. Enabling KVM (Kernel-based Virtual Machine)** KVM allows the Linux kernel to function as a hypervisor. For ARM64, specific kernel configuration options are needed.  
  * **4.1.1. Kernel Configuration:** Within your kernel source tree (whether from a vendor SDK, Armbian, or mainline), invoke the kernel configuration menu (e.g., make ARCH=arm64 CROSS\_COMPILE=aarch64-linux-gnu- menuconfig). Navigate to:  
    * Virtualization \---\>  
      * Enable Kernel-based Virtual Machine (KVM) support (CONFIG\_KVM).  
      * Ensure related options like KVM for ARMv8 virtual machine support are selected.  
    * Also ensure general virtualization support is enabled:  
      * Processor type and features \---\>  
        * Virtualization extensions (CONFIG\_VIRTUALIZATION). Other relevant options might include CONFIG\_HAVE\_KVM\_IRQCHIP, CONFIG\_HAVE\_KVM\_IRQFD. The exact naming and location can vary slightly between kernel versions. Some kernel configurations for RK3588 might already have KVM options enabled by default (e.g., CONFIG\_HAVE\_KVM=y).  
  * **4.1.2. Building and Deploying the Kernel:** After saving the configuration, rebuild the kernel and modules as described in Section 2.1. Deploy the new kernel, DTB, and modules to the VPC-3588. For Armbian, the process involves using ./compile.sh BOARD=\<board\> BRANCH=\<branch\> kernel-config to modify the configuration, then ./compile.sh BOARD=\<board\> BRANCH=\<branch\> kernel to build the kernel packages.  
  * **Note on KVM on ARM:** KVM on ARM relies on hardware virtualization extensions (e.g., ARMv8 virtualization extensions). The RK3588's Cortex-A76/A55 cores support these. Nested virtualization (running KVM inside a KVM guest) might also be configurable.  
* **4.2. Applying Patches to the Kernel Source** Patches (.patch or .diff files) are used to apply specific changes to the kernel source, such as bug fixes, backported features, or custom modifications.  
  * **4.2.1. Within a Build System (SDK/Armbian):**  
    * **Vendor SDKs (e.g., Firefly):** SDKs often have a dedicated directory for patches or a mechanism to apply them during the build. The Firefly SDK structure doesn't explicitly detail a patch directory in the overview, but modifications would typically be integrated by altering configuration files or directly modifying source. Some build systems might look for .patch files in specific locations. The general patch utility is used.  
    * **Armbian:** The Armbian build system has a userpatches directory. Patches placed here (e.g., in userpatches/kernel/\<family\>-\<branch\>/) can be automatically applied during the kernel build process. The structure and naming conventions within userpatches are important.  
  * **4.2.2. Manual Patch Application:**  
    1. Navigate to the root of your kernel source directory.  
    2. Use the patch command: patch \-p1 \< /path/to/your/patchfile.patch. The \-p1 option strips the first leading directory component from filenames in the patch (e.g., a/kernel/file.c becomes kernel/file.c), which is common for kernel patches.  
    3. After applying, rebuild the kernel.  
  * **Note on Patch Complexity:** Sourcing, creating, or backporting the correct .patch file for your specific kernel version and desired functionality is often a complex development task in itself, requiring careful code analysis and testing beyond the mechanical application of the patch.  
* **4.3. Building and Integrating Out-of-Tree Kernel Modules** Out-of-tree modules are compiled separately from the main kernel source tree. This is common for proprietary drivers or custom modules not yet mainlined.  
  * **4.3.1. Prerequisites:**  
    * **Kernel Headers or Prepared Source:** You need the kernel headers package corresponding to your running kernel (e.g., linux-headers-$(uname \-r)) or a fully prepared kernel source tree (configured and make modules\_prepare run). The Module.symvers file from the original kernel build is crucial for symbol versioning and must match.  
    * **Cross-Compiler:** The same AArch64 cross-compiler used for the kernel.  
  * **4.3.2. Module Source and Makefile:** The module source code will have its own Makefile. A typical Makefile for an out-of-tree module (your\_module.c) might look like:  
    `obj-m += your_module.o`  
    `# Add other source files if your_module consists of multiple files:`  
    `# your_module-objs := file1.o file2.o`

    `all:`  
        `make -C /path/to/prepared/kernel/source M=$(PWD) ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- modules`

    `clean:`  
        `make -C /path/to/prepared/kernel/source M=$(PWD) ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- clean`  
    Replace /path/to/prepared/kernel/source with the actual path to the kernel headers/sources (e.g., /usr/src/linux-headers-$(uname \-r)/ or your custom build directory) and aarch64-linux-gnu- with the correct cross-compiler prefix.  
  * **4.3.3. Compilation:** Navigate to the module's source directory and run make.  
  * **4.3.4. Deployment:**  
    * Copy the resulting your\_module.ko file to the target device's root filesystem, typically into a directory like /lib/modules/$(uname \-r)/extra/ or /lib/modules/$(uname \-r)/kernel/drivers/your\_category/.  
    * On the target device, run sudo depmod \-a to update the module dependency list.  
    * Load the module using sudo modprobe your\_module.  
  * **Note on Module Compatibility:** Ensuring an out-of-tree module's source code is compatible with your target kernel's version, configuration (including enabled options and symbol versions via Module.symvers), and architecture is crucial for successful compilation and loading.  
  * **Integrating into Build Systems:**  
    * **Vendor SDKs (e.g., Firefly):** SDKs might have specific ways to include out-of-tree modules in the overall build, often by adding them to a Buildroot or Yocto configuration if those are used for the rootfs.  
    * **Armbian:** The Armbian build system allows for adding custom packages, which could include out-of-tree modules. This might involve creating a custom package definition or using hooks in the userpatches directory.

The choice of build system significantly influences how kernel customizations are managed. Vendor SDKs and community build frameworks like Armbian offer different structured approaches to incorporate configuration changes and patches. Enabling an in-tree module like KVM is largely a matter of correct kernel configuration within that build system. In contrast, building and integrating out-of-tree modules generally requires more manual setup, including ensuring the kernel sources are correctly prepared and that the Module.symvers file from the original kernel build matches, as this file contains critical symbol versioning information necessary for the module to load correctly.

## **5\. Distribution Analysis and Customization**

Understanding the specifics of a vendor-supplied Linux distribution and being able to deploy a fully customized distribution are advanced tasks that provide significant control over the system. This section covers methods for comparing a vendor's Debian Bullseye distribution against a vanilla version and leveraging MaskROM mode for deploying custom images.

* **5.1. Extracting Vendor Modifications from a Debian Bullseye Distro** The goal here is to identify any customizations, additions, or removals made by the board vendor (Liontron or their upstream provider for the VPC-3588) compared to a standard Debian Bullseye ARM64 installation. This process is an investigative one, combining several techniques.  
  * **5.1.1. Comparing Installed Package Lists:** A primary method is to compare the list of installed packages.  
    1. On the VPC-3588 running the vendor's Debian Bullseye: dpkg \--get-selections | sort \> /tmp/vpc3588\_vendor\_packages.txt  
    2. On a reference "vanilla" Debian Bullseye ARM64 system (this could be a virtual machine, another RK3588 board with a clean Debian install, or a chroot environment built with debootstrap): dpkg \--get-selections | sort \> /tmp/vanilla\_bullseye\_packages.txt  
    3. Transfer these files to a common location and compare them: diff \-u /tmp/vpc3588\_vendor\_packages.txt /tmp/vanilla\_bullseye\_packages.txt \> /tmp/package\_differences.txt This package\_differences.txt file will highlight packages added by the vendor, packages potentially removed, or packages present at different versions. This can reveal custom drivers, utilities, or libraries specific to the VPC-3588.  
  * **5.1.2. Comparing Configuration Files:** Vendor modifications often reside in configuration files, primarily within the /etc directory, but also potentially in /usr/local/ or /opt/.  
    1. Obtain access to the root filesystems of both the vendor system and the vanilla system. This might involve mounting their storage (e.g., eMMC images) on a development host or using rsync to create copies.  
    2. Use diff recursively to identify differing files and directories. For a summary of differences in /etc: sudo diff \-qr /mnt/vendor\_rootfs/etc /mnt/vanilla\_rootfs/etc \> /tmp/etc\_diff\_summary.txt  
    3. For files identified as different, perform a detailed comparison: sudo diff \-u /mnt/vendor\_rootfs/etc/some\_config\_file /mnt/vanilla\_rootfs/etc/some\_config\_file. Key areas to scrutinize include:  
    * Network settings: /etc/network/interfaces, /etc/NetworkManager/system-connections/, /etc/systemd/network/.  
    * Udev rules for device handling: /etc/udev/rules.d/.  
    * Kernel module loading and options: /etc/modules-load.d/, /etc/modprobe.d/.  
    * Bootloader configurations if stored in /boot/ (e.g., extlinux.conf).  
    * Custom startup scripts: /etc/init.d/ (for SysVinit scripts, though less common with systemd), systemd service unit files in /etc/systemd/system/ and /lib/systemd/system/.  
    * Vendor-specific applications or scripts: Often found in /usr/local/bin/, /usr/local/sbin/, or /opt/.  
  * **5.1.3. Analyzing Kernel and Bootloader Differences:**  
    * **Kernel:**  
      * On the running vendor system, the kernel's configuration can often be retrieved from /proc/config.gz. Uncompress this and compare it to a vanilla Debian Bullseye ARM64 kernel configuration for a similar kernel version (if known).  
      * Examine the output of dmesg for messages indicating custom drivers, unique hardware identifiers, or specific initialization sequences.  
      * If the vendor provides kernel source code or patches, these can be directly compared against the corresponding mainline kernel version to pinpoint modifications.  
    * **U-Boot:** Comparing U-Boot binaries is difficult without source. If the vendor provides U-Boot source or patches , these can be compared against a generic RK3588 U-Boot source tree. Otherwise, differences might be inferred from U-Boot environment variables or boot script behavior observed via the serial console.  
  * **5.1.4. Device Tree (DTS) Modifications:** The Device Tree Blob (DTB) is critical for describing the hardware to the kernel. Vendor customizations for specific peripherals, pin configurations, or enabled interfaces on the VPC-3588 will be encoded here.  
    1. The compiled DTB is usually located in /boot/dtbs/rockchip/ (or a similar path) on the vendor system, often named something like rk3588-vpc-3588.dtb.  
    2. Decompile this binary DTB back into a human-readable Device Tree Source (DTS) format using the Device Tree Compiler (dtc): dtc \-I dtb \-O dts /path/to/vendor.dtb \-o /tmp/vendor.dts  
    3. Compare this vendor.dts with a generic RK3588 DTS for a similar reference board or from the mainline kernel sources. Look for custom device nodes, properties (e.g., status \= "okay";), clock settings, pinmux configurations, and regulator definitions that are unique to the VPC-3588. Board-specific DTS files are common in vendor SDKs; for instance, the Firefly SDK structure points to a specific DTS file via the RK\_KERNEL\_DTS variable (e.g., roc-rk3588-pc.dts or roc-rk3588s-pc.dts). Liontron would similarly have a DTS tailored for the VPC-3588.

This process of identifying vendor modifications is iterative. Static analysis of packages and configuration files provides a baseline, while dynamic analysis (observing runtime behavior, dmesg, loaded modules via lsmod) can reveal further customizations. It's important to understand that "extracting the diff" in this context primarily means *identifying these differences* rather than creating a single, universally applicable patch file that transforms a vanilla distro into the vendor's version, as the latter is a significantly more complex undertaking.**Table: Checklist for Comparing Vendor and Vanilla Debian Distributions**

| Area of Comparison | Tools/Commands | What to Look For |
| :---- | :---- | :---- |
| Package Manager Database | dpkg \--get-selections, diff | Added/removed packages, version differences, vendor-specific repositories. |
| /etc Configuration Files | diff \-qr, diff \-u | Modified system settings, network configs, service units, udev rules, module configs, custom scripts. |
| /usr/local/, /opt/ | ls, diff \-r | Vendor-added applications, libraries, or scripts not managed by dpkg. |
| Kernel Configuration & Logs | /proc/config.gz, dmesg, lsmod | Custom kernel config options, loaded modules (especially proprietary ones), unique boot messages, hardware-specific driver parameters. |
| U-Boot (if accessible) | Serial console U-Boot commands (printenv, boot scripts) | Custom environment variables, non-standard boot sequences, specific hardware initialization commands. |
| Device Tree (DTB/DTS) | dtc (decompiler), diff | Custom device nodes, enabled/disabled peripherals, pinmux settings, clock configurations, regulator settings specific to the VPC-3588. |

* **5.2. Leveraging MaskROM Mode for Custom Distribution Deployment** MaskROM mode provides a low-level interface to flash a complete custom distribution image onto the VPC-3588, bypassing any existing software on the eMMC or other boot media. This offers maximum flexibility but also requires careful preparation of the image.  
  * **5.2.1. Preparing a Custom Distribution Image:** The custom distribution image must be a bootable, raw disk image (often with a .img extension) or a set of partition images compatible with rkdeveloptool.  
    * **Image Creation:** This image can be built using various methods:  
      * **Vendor SDKs:** Tools like the Firefly SDK can produce complete firmware images (often as update.img or individual partition images).  
      * **Armbian Build System:** Armbian can generate full OS images for RK3588 boards.  
      * **Manual Creation:** Using tools like debootstrap to create a minimal Debian/Ubuntu rootfs, then manually installing a kernel, configuring U-Boot, and packaging it into a disk image.  
    * **Image Contents:** The image must contain all necessary components for booting:  
      * A compatible U-Boot bootloader (or this can be flashed separately as per Section 3.3).  
      * A Linux kernel compiled for the RK3588 and configured for the VPC-3588.  
      * The correct Device Tree Blob (DTB) for the VPC-3588.  
      * A complete root filesystem.  
      * A valid partition table (typically GPT) that U-Boot and the kernel can interpret.  
  * **5.2.2. Flashing the Custom Image via MaskROM Mode:**  
    1. **Enter MaskROM Mode:** Follow the procedure specific to the VPC-3588 to enter MaskROM mode (as detailed in Section 3.3.2). **Consult Liontron's official documentation for the VPC-3588 for the exact method.**  
    2. **Connect to PC:** Connect the VPC-3588 to the host PC via its USB OTG port.  
    3. **Verify Detection:** Use sudo rkdeveloptool ld to confirm the device is detected in MaskROM mode.  
    4. **Download SPL Loader:** Download the appropriate Rockchip SPL loader (flash helper) to the device's RAM: sudo rkdeveloptool db /path/to/rk3588\_spl\_loader.bin. (e.g., rk3588\_spl\_loader\_v1.08.111.bin or rk3588\_spl\_loader\_v1.15.113.bin).  
    5. **Flash the Image:**  
       * **Single Raw Image (update.img or full disk image):** If the custom\_distro.img is a complete raw disk image (containing GPT, bootloader, kernel, rootfs at their correct internal offsets), it is typically flashed starting at sector 0 of the target storage (e.g., eMMC): sudo rkdeveloptool wl 0 /path/to/custom\_distro.img. Some tools or vendor procedures might use upgrade\_tool uf update.img for a packaged update.img.  
       * **Partition-by-Partition Flashing:** If the custom distribution is provided as separate partition images (e.g., boot.img, rootfs.img), a partition table might need to be written first (e.g., using rkdeveloptool write-partition-table or rkdeveloptool gpt with a parameter.txt or similar file defining the layout ). Then, individual partitions can be flashed using commands like: sudo rkdeveloptool write-partition rootfs /path/to/rootfs.img or its alias sudo rkdeveloptool wlx rootfs /path/to/rootfs.img. It's important to note that when flashing raw images, especially to offset 0 in MaskROM mode, the tool writes directly to the beginning of the physical media. Some older tools or modes might have implicit offsets (e.g., AndroidTool in Rockusb mode might add 0x2000 sectors ), but rkdeveloptool in MaskROM mode writing to sector 0 should target the true start of the device.  
    6. **Reboot:** After flashing, reset the device: sudo rkdeveloptool rd.  
  * **5.2.3. Considerations for Custom Image Deployment:**  
    * **Partition Table Integrity:** The custom image must contain, or be preceded by flashing, a valid and correctly structured GPT partition table that both U-Boot and the Linux kernel can parse to locate the necessary partitions (boot, rootfs, etc.).  
    * **Bootloader and Kernel Compatibility:** The U-Boot version within the image (or flashed separately) must be capable of booting the kernel included in the image. The kernel, in turn, must be compiled with the correct drivers and configuration for the VPC-3588 hardware, and the DTB must accurately describe this hardware.  
    * **Target Storage Media:** Ensure the image is built and flashed correctly for the intended primary boot device (e.g., eMMC). If booting from NVMe SSD is intended, the SPI flash must contain a U-Boot version capable of NVMe boot.

Flashing a full custom distribution via MaskROM mode provides a powerful method to completely redefine the software environment of the VPC-3588. This bypasses any vendor-imposed update mechanisms or existing OS constraints. However, this level of control demands a thorough understanding of the image's structure and its compatibility with the target hardware, as an incorrectly prepared or flashed image will likely result in a non-booting system (though typically recoverable again via MaskROM).

## **6\. Essential Tools and Low-Level Operations**

Effective low-level interaction with Rockchip RK3588-based systems like the VPC-3588 heavily relies on specialized tools and an understanding of fundamental recovery mechanisms. rkdeveloptool and MaskROM mode are central to these operations.

* **6.1. Mastering rkdeveloptool** rkdeveloptool is a command-line utility developed by Rockchip for communicating with Rockchip SoCs over USB, primarily when the device is in a special bootloader mode (Loader mode or MaskROM mode). It allows for reading from and writing to the device's flash storage, downloading bootloader components, and managing partitions.  
  * **6.1.1. Installation from Source:** While some distributions might package rkdeveloptool, building from source ensures the latest version or a specific fork is used.  
    1. **Dependencies:** Install necessary development libraries, typically libusb-1.0-0-dev, libudev-dev, dh-autoreconf, and pkg-config.  
    2. **Clone Source:** Obtain the source code from the official Rockchip Linux repository or a relevant fork: git clone https://github.com/rockchip-linux/rkdeveloptool  
    3. **Build and Install:** Navigate into the cloned directory and execute the build commands: ./autogen.sh (if present, or autoreconf \-i) ./configure make sudo make install (or sudo cp rkdeveloptool /usr/local/bin/ followed by sudo ldconfig). Ensure udev rules are set up correctly (e.g., by copying 99-rk-rockusb.rules from the source to /etc/udev/rules.d/ and reloading rules ) to allow user access or for rkdeveloptool to function without needing sudo for every command, though using sudo is common practice.  
  * **6.1.2. Key Commands and Usage:** The following table summarizes essential rkdeveloptool commands, crucial for managing the VPC-3588. It is advisable to consult the tool's help output (rkdeveloptool \-h or rkdeveloptool \--help ) for the precise syntax supported by the installed version, as minor variations can exist.**Table: rkdeveloptool Command Reference for RK3588**

| Command | Arguments | Description | Example Usage | Key References |
| :---- | :---- | :---- | :---- | :---- |
| ld / list | (none) | List connected Rockchip devices in Loader or MaskROM mode. | sudo rkdeveloptool ld |  |
| db | \<loader\_file.bin\> | Download Bootloader/Flash Helper (SPL) to device RAM. Essential for MaskROM operations. | sudo rkdeveloptool db rk3588\_spl\_loader.bin |  |
| wl | \<start\_sector\> \<image\_file.img\> | Write LBA: Writes image\_file.img to flash starting at start\_sector (512-byte sectors). | sudo rkdeveloptool wl 0x40 idbloader.img |  |
| wlx / write-partition | \<partition\_name\> \<image\_file.img\> | Write Partition by Name: Writes image\_file.img to the partition named partition\_name in GPT. | sudo rkdeveloptool wlx rootfs rootfs.img |  |
| rl / read | \<start\_sector\> \<num\_bytes\> \<output\_file\> | Read LBA: Reads num\_bytes from flash starting at start\_sector into output\_file. | sudo rkdeveloptool read 64 8355840 idbloader\_backup.img (8355840 bytes \= 16320 sectors \* 512\) |  |
| read-partition | \<partition\_name\> \<output\_file\> | Read Partition by Name: Reads the content of partition\_name into output\_file. | sudo rkdeveloptool read-partition uboot uboot\_backup.img |  |
| rd / reset / reboot | (none, or subcode) | Reset/Reboot Device: Reboots the connected Rockchip device. rd is often an alias for reset 0\. | sudo rkdeveloptool rd |  |
| ef / erase-flash | (none) | Erase Flash: Erases the entire flash memory. **Use with extreme caution.** | sudo rkdeveloptool ef |  |
| gpt / write-partition-table | \<partition\_definition\_file.txt\> | Write GPT: Writes a new partition table to the device based on the definition file. | sudo rkdeveloptool gpt partitions.txt |  |
| ppt / list-partitions | (none) | Print Partition Table: Displays the current GPT entries on the device. | sudo rkdeveloptool ppt |  |
| ul / upgrade-loader | \<loader\_file.bin\> | Upgrade Loader: Updates the bootloader software on the device's flash (e.g., SPI flash or eMMC boot area). | sudo rkdeveloptool ul new\_bootloader.bin |  |
| reboot-maskrom | (none) | Reset the device and attempt to trigger MaskROM mode. | sudo rkdeveloptool reboot-maskrom |  |

It is important to use the correct loader file (.bin for the db command) specific to the RK3588 SoC, as this small program downloaded into the SoC's SRAM is responsible for initializing DRAM and handling further USB communication for flashing operations. Without successfully executing the db command in MaskROM mode, most other flash read/write operations will fail.

* **6.2. Understanding and Utilizing MaskROM Mode** MaskROM mode is a fundamental recovery and initial programming mechanism embedded within the Rockchip RK3588 SoC.  
  * **6.2.1. Purpose and Capabilities:**  
    * **Low-Level Access:** MaskROM mode is initiated by the SoC's internal BootROM code. It is activated if the primary boot media (e.g., eMMC, SD card, SPI flash) is found to be empty or contains a corrupted/invalid bootloader, or it can be triggered by a specific hardware action.  
    * **USB Communication:** When in MaskROM mode, the SoC listens for commands over a designated USB interface (typically the OTG port). A host PC running rkdeveloptool can then communicate with the SoC.  
    * **Primary Use Cases:**  
      * Initial programming of devices with blank flash memory (factory programming).  
      * Unbricking devices where the bootloader or entire flash content has been corrupted.  
      * Low-level diagnostics and direct flash memory access.  
  * **6.2.2. Procedures for Entering MaskROM Mode on RK3588 Devices:** The exact method to enter MaskROM mode can vary slightly depending on the specific board design of the VPC-3588. **Always consult the official Liontron documentation for the VPC-3588 for the precise procedure.** General procedures for RK3588-based devices include :  
    1. **Power Off:** Ensure the device is completely powered off. Disconnect the power supply.  
    2. **Hardware Trigger:**  
       * **MaskROM Button:** If the VPC-3588 motherboard has a dedicated MaskROM button (often labeled "Recovery", "Mask", or similar), press and hold this button.  
       * **Test Points/Jumpers:** If no button is present, the board's schematics or technical documentation may indicate specific test points on the PCB that need to be shorted (e.g., with tweezers or a jumper wire). For example, on some boards, grounding the SPI flash CLK pin might be a method.  
    3. **Connect USB:** While maintaining the hardware trigger (holding the button or shorting points), connect a USB cable from the host PC to the VPC-3588's USB OTG port (check VPC-3588 specs for which port this is ).  
    4. **Apply Power:** Connect the power supply to the VPC-3588.  
    5. **Release Trigger:** After a few seconds (typically 2-5 seconds once power is applied and USB is connected), release the MaskROM button or remove the short from the test points. The device should now be in MaskROM mode. This can be verified on the host PC by running sudo rkdeveloptool ld. The output should list the device and indicate "Maskrom" mode.  
  * **6.2.3. Recovery and Initial Programming Scenarios:** Once the VPC-3588 is in MaskROM mode and communicating with rkdeveloptool, several recovery and programming operations can be performed:  
    * **Flashing a Complete Factory Image:** If a full factory firmware image (.img file or update.img) is available, it can be written to the eMMC, effectively restoring the device to its original state or installing a new OS from scratch (as detailed in Section 5.2).  
    * **Restoring Corrupted Bootloader:** This is a common unbricking procedure. Known-good bootloader components (idbloader.img, u-boot.itb, or a combined image) can be flashed to their correct offsets on the eMMC or SPI flash, as described in Section 3.3.  
    * **Erasing Flash Memory:** The entire eMMC or SPI flash can be erased (e.g., using rkdeveloptool ef or by writing zeros ) to ensure a clean state before flashing new firmware. This is often a prerequisite if the existing partition table or data is severely corrupted.  
    * **Low-Level Partition Management:** The partition table (GPT) can be rewritten if it's damaged, using rkdeveloptool gpt or rkdeveloptool write-partition-table.

MaskROM mode, combined with rkdeveloptool, forms a powerful toolkit for developers and advanced users, providing a safety net for recovering from most software-related bricking incidents and offering complete control over the device's flash storage contents from the earliest boot stages.

## **7\. Conclusion and Best Practices**

The Rockchip RK3588 SoC, as implemented in the VPC-3588 motherboard, offers a powerful and versatile platform for a wide range of embedded applications. The procedures detailed in this report—spanning kernel and distribution upgrades, bootloader management, kernel customization with modules and patches, distribution analysis, and the use of low-level tools like rkdeveloptool in conjunction with MaskROM mode—empower advanced users and developers to tailor the system extensively to their specific requirements. However, these advanced operations necessitate a thorough understanding of the underlying system architecture and carry inherent risks if not performed with caution, as highlighted in the "Before You Begin" section.

* **7.1. Summary of Key Procedures and Capabilities** This report has outlined methodologies for several critical system modification tasks:  
  * **System Upgrades:** Upgrading the Linux kernel from versions like 5.10 to newer releases, performing Debian distribution upgrades (e.g., Bullseye to Bookworm), and understanding that libc6 updates are best handled as part of a full distribution upgrade due to severe risks if done in isolation.  
  * **Bootloader Management:** Properly backing up, cloning, and restoring the U-Boot bootloader, particularly using rkdeveloptool and MaskROM mode for unbricking scenarios. The critical nature of bootloader component offsets (idbloader.img, u-boot.itb) and the need to verify them for the specific board have been emphasized.  
  * **Kernel Customization:** Enabling in-kernel features like KVM through kernel configuration, applying external patches to the kernel source (noting the complexity of patch creation/sourcing), and integrating out-of-tree kernel modules (highlighting compatibility requirements), adapting to different build systems (vendor SDKs vs. Armbian).  
  * **Distribution Analysis:** Techniques for comparing a vendor-supplied Debian distribution against a vanilla version to identify customizations across package lists, configuration files, and the Device Tree.  
  * **MaskROM and rkdeveloptool:** Leveraging MaskROM mode for low-level device access and firmware flashing, and mastering rkdeveloptool for these operations. The indispensable role of the SPL loader (downloaded via the db command) in MaskROM operations was highlighted.

The RK3588 platform, while highly capable, requires significant technical expertise for such deep modifications. The ecosystem, with its mix of vendor-specific SDKs (which may or may not be publicly available or fully documented for the VPC-3588 by Liontron ) and broader community efforts (like Armbian ), means developers must often synthesize information from multiple sources.

* **7.2. General Recommendations for Working with RK3588 Systems like VPC-3588** Adherence to best practices is crucial when performing advanced operations on embedded systems:  
  * **Backup Diligently:** (Reiterated from "Before You Begin") Before any operation that modifies the flash storage, create comprehensive backups.  
  * **Utilize a Serial Console:** (Reiterated from "Before You Begin") Indispensable for low-level debugging.  
  * **Verify Image and Tool Compatibility for VPC-3588:** (Reiterated from "Before You Begin") Always ensure that firmware images, kernel binaries, U-Boot images, and tools are specifically intended for the RK3588 SoC and, critically, confirmed or adapted for the Liontron VPC-3588 motherboard. **Consult Liontron's official documentation as the primary source for VPC-3588 specific information.**  
  * **Proceed with Caution and Incrementally:** Low-level flashing operations carry risks. Understand each command before execution. When possible, make changes incrementally and test thoroughly after each step.  
  * **Consult Vendor and Community Resources:** Leverage official documentation and support from Liontron and Rockchip when available. Additionally, the collective knowledge within community forums (e.g., Armbian , Radxa , Firefly ) can provide practical insights, solutions to common problems, and experiences from other users working with RK3588 platforms.  
* **7.3. The Path Forward: Integration, Continuous Learning, and Contribution** The tasks discussed in this report, while presented individually, are often interconnected. For example, a distribution upgrade might necessitate a kernel upgrade for optimal compatibility, and adding custom kernel modules requires a correctly configured kernel build environment. True mastery lies in understanding these interdependencies and planning modifications holistically. The embedded Linux landscape, including support for SoCs like the RK3588, is constantly evolving with new kernel versions, updated distributions, and improved tools. Continuous learning and staying abreast of these developments are essential. The "safety net" provided by MaskROM mode and rkdeveloptool is a significant asset for developers working with Rockchip platforms. It means that most software-induced "bricking" is recoverable, fostering a more confident environment for experimentation and deep customization, provided the recovery procedures themselves are well understood and the correct board-specific methods (especially for entering MaskROM mode on the VPC-3588) are followed. If novel solutions, patches, or configurations are developed for the VPC-3588, sharing these findings with relevant communities can benefit the broader ecosystem.

#### **Works cited**

1\. Rockchip \- Wikipedia, https://en.wikipedia.org/wiki/Rockchip 2\. List of Rockchip products \- Wikipedia, https://en.wikipedia.org/wiki/List\_of\_Rockchip\_products 3\. Linux SDK Configuration introduction — Firefly Wiki, https://wiki.t-firefly.com/en/ROC-RK3588-PC/linux\_sdk.html 4\. Welcome to ROC-RK3588-PC Manual — Firefly Wiki, https://wiki.t-firefly.com/en/ROC-RK3588-PC/index.html 5\. 2\. Compile Linux Firmware (kernel-5.10) — Firefly Wiki, https://wiki.t-firefly.com/en/ROC-RK3588S-PC/linux\_compile.html 6\. rkdeveloptool man \- Linux Command Library, https://linuxcommandlibrary.com/man/rkdeveloptool 7\. Install Armbian and Proxmox on the OrangePi5+ (RK3588) – JF's ..., https://codingfield.com/blog/2024-01/install-armbian-and-proxmox-on-orangepi5plus/ 8\. rkdeveloptool \- Radxa Docs, https://docs.radxa.com/en/compute-module/cm3/low-level-dev/rkdeveloptool 9\. Linux Host | Radxa Docs, https://docs.radxa.com/en/rock5/rock5c/low-level-dev/maskrom/linux 10\. Flash BootLoader to SPI Nor Flash \- Radxa Docs, https://docs.radxa.com/en/rock5/lowlevel-development/bootloader\_spi\_flash 11\. Partitions are overwritten by rkdeveloptool flash \- 5B/5B+ \- Radxa forum, https://forum.radxa.com/t/partitions-are-overwritten-by-rkdeveloptool-flash/24573 12\. Rockpi4/install/rockchip-flash-tools \- Radxa Wiki, https://wiki.radxa.com/Rockpi4/install/rockchip-flash-tools 13\. Maskrom mode | Radxa Docs, https://docs.radxa.com/en/compute-module/cm5/radxa-os/low-level-dev/cm5io-maskrom-mode 14\. Maskrom Mode | Radxa Docs, https://docs.radxa.com/en/rock3/rock3c/low-level-dev/3c-maskrom 15\. upstream\_uboot.md · main · hardware-enablement / Rockchip upstream enablement efforts / Notes for Rockchip 3588 · GitLab \- Explore projects, https://gitlab.collabora.com/hardware-enablement/rockchip-3588/notes-for-rockchip-3588/-/blob/main/upstream\_uboot.md 16\. PineNote: Flashing \- PINE64, https://pine64.org/documentation/PineNote/Development/Flashing/ 17\. VPC-3588: RK3588-Liontron \- ARM based embedded platforms for ..., http://en.liontron.cn/showinfo-128-226-0.html 18\. Radxa ROCK 5C \- Rockchip \- LibreELEC Forum, https://forum.libreelec.tv/thread/29214-radxa-rock-5c/ 19\. Introduce ROCK 5B \- ARM Desktop level SBC \- ROCK 5 Series \- Radxa Community, https://forum.radxa.com/t/introduce-rock-5b-arm-desktop-level-sbc/8361?page=11 20\. RK3588 Mini-ITX Industrial Motherboard VPC-3588 – Antallia, https://genovaindustrial.com/products/liontron-vpc-3588-motherboard 21\. liontron package \- All Versions \- pub.dev, https://pub.dev/packages/liontron/versions 22\. Downloads \- LIONTRON Lithium Batteries, https://liontron.com/en/downloads/ 23\. ROCKNIX/rk3588-uboot \- GitHub, https://github.com/ROCKNIX/rk3588-uboot 24\. RK3588 Technical Reference Manual（whole）-16rd \- Mobile version, https://m.16rd.com/thread-586416-1-1.html 25\. RK3588 | Datasheet | Rockchip | LCSC Electronics, https://lcsc.com/datasheet/lcsc\_datasheet\_2411220327\_Rockchip-RK3588\_C5156490.pdf 26\. Rockchip RK3588 TRM V1.0-Part1-20220309 | PDF \- Scribd, https://www.scribd.com/document/622093243/Rockchip-RK3588-TRM-V1-0-Part1-20220309 27\. WAFER-RK3588, https://www.ieiworld.com/en/product/model.php?II=1036 28\. SoC: RK3588 \- Armbian, https://www.armbian.com/soc/rk3588/ 29\. Kernel switching from 5.10 legacy to 6.1 vendor in existing Armbian installation, https://forum.armbian.com/topic/41473-kernel-switching-from-510-legacy-to-61-vendor-in-existing-armbian-installation/ 30\. updating the kernel with a custom armbian one with kernel ..., https://forum.armbian.com/topic/49107-updating-the-kernel-with-a-custom-armbian-one-with-kernel-configuration-for-kvm/ 31\. Moving Linux Kernel to 6.1 \- Page 12 \- Raspberry Pi Forums, https://forums.raspberrypi.com/viewtopic.php?t=344246\&start=275 32\. guide to set up a KVM development environment on 64-bit ARMv8 processors, http://www.virtualopensystems.com/en/solutions/guides/kvm-on-armv8/ 33\. Live Migrating from Raspberry Pi OS bullseye to Debian bookworm | www.complete.org, https://www.complete.org/live-migrating-from-raspberry-pi-os-bullseye-to-debian-bookworm/ 34\. How to Upgrade from Debian 11 Bullseye to Debian 12 Bookworm \- LinuxCapable, https://linuxcapable.com/how-to-upgrade-from-debian-11-bullseye-to-debian-12-bookworm/ 35\. rockchip-linux/rkdeveloptool \- GitHub, https://github.com/rockchip-linux/rkdeveloptool 36\. rkdeveloptool \- rockusb bootloader utility \- Ubuntu Manpage, https://manpages.ubuntu.com/manpages/noble/man1/rkdeveloptool.1.html 37\. Mobile & Embedded \- Flashing Firmware to Rockchip Devices from a Linux PC \- Leon Anavi, https://anavi.org/article/288/ 38\. Feature Request: Support smart AM60 RK3588 · Issue \#1215 · Joshua-Riek/ubuntu-rockchip \- GitHub, https://github.com/Joshua-Riek/ubuntu-rockchip/issues/1215 39\. Notes: Build U-Boot for Rock5b \- yrzr, https://yrzr.github.io/notes-build-uboot-for-rock5b/ 40\. \[meta-rockchip,3/4\] remove /boot partition from wic:bootimg-paritition \- Patchwork, https://patchwork.yoctoproject.org/comment/17452/ 41\. How to recursively compare Linux files \- LabEx, https://labex.io/tutorials/linux-how-to-recursively-compare-linux-files-419715 42\. CM3588 \- FriendlyELEC WiKi, https://wiki.friendlyelec.com/wiki/index.php/CM3588 43\. RK3588 maskrom boot \- MNT Pocket Reform, https://community.mnt.re/t/rk3588-maskrom-boot/3286 44\. \[GIT PULL\] arm64 updates for 5.10 \- The Linux-Kernel Archive, https://lkml.rescloud.iu.edu/2010.1/01664.html 45\. Running nested guests with KVM — The Linux Kernel 5.10.0-rc1+ documentation, https://www.infradead.org/\~mchehab/kernel\_docs/virt/kvm/running-nested-guests.html 46\. Documentation/applying-patches.txt \- Programming Languages Research Group: Git \- firefly-linux-kernel-4.4.55.git/blob, http://plrg.eecs.uci.edu/git/?p=firefly-linux-kernel-4.4.55.git;a=blob;f=Documentation/applying-patches.txt;hb=d7f6884ae0ae6e406ec3500fcde16e8f51642460 47\. hyper-systems/armbian: Armbian Linux build framework \- GitHub, https://github.com/hyper-systems/armbian 48\. Welcome to the Armbian build framework documentation\!, https://docs.armbian.com/Developer-Guide\_Welcome/ 49\. Custom Kernel \- Armbian build framework, https://forum.armbian.com/topic/3094-custom-kernel/ 50\. Files · rk3588/firefly · Firefly-Linux / kernel \- GitLab, https://gitlab.com/firefly-linux/kernel/-/tree/rk3588/firefly?ref\_type=heads 51\. Building out-of-tree kernel modules: preparing legacy-rk35xx kernel ..., https://forum.armbian.com/topic/35556-building-out-of-tree-kernel-modules-preparing-legacy-rk35xx-kernel-source/ 52\. Steps to build out of tree kernel modules using Yocto SDK \- Embedded Guru, http://embeddedguruji.blogspot.com/2019/03/steps-to-build-out-of-tree-kernel.html 53\. Building Kernel modules that work with official distributions \- Armbian forum, https://forum.armbian.com/topic/33291-building-kernel-modules-that-work-with-official-distributions/ 54\. How to use dpkg to compare two Linux servers \- Unix Tutorial, https://unixtutorial.org/how-to-use-dpkg-to-compare-two-linux-servers/ 55\. 10 Best File Comparison and Difference (Diff) Tools in Linux \- Tecmint, https://www.tecmint.com/best-linux-file-diff-tools-comparison/ 56\. Debian \-- Details of package diffutils in sid, https://packages.debian.org/sid/diffutils 57\. Debian \-- Details of package diffutils in buster, https://packages.debian.org/buster/diffutils 58\. Comparing Directories (Comparing and Merging Files) \- GNU, http://www.gnu.org/s/diffutils/manual/html\_node/Comparing-Directories.html 59\. Add debian-rootfs operating-system element (414765) · Gerrit Code Review, https://review.opendev.org/c/openstack/diskimage-builder/+/414765/ 60\. Petalinux compare config from one build to another \- AMD Adaptive Support, https://adaptivesupport.amd.com/s/question/0D52E00006hpNHiSAM/petalinux-compare-config-from-one-build-to-another?language=en\_US 61\. U-Boot on RK3588 says "Bad Linux ARM64 Image magic\!" : r/AlpineLinux \- Reddit, https://www.reddit.com/r/AlpineLinux/comments/1jaehf9/uboot\_on\_rk3588\_says\_bad\_linux\_arm64\_image\_magic/ 62\. Using the Armbian Build Environment \- Orange Pi 5 Plus, https://forum.armbian.com/topic/49294-using-the-armbian-build-environment/ 63\. Building and installing Armbian on the AIO-3588Q board, https://forum.armbian.com/topic/47291-building-and-installing-armbian-on-the-aio-3588q-board/ 64\. flash\_emmc.md.txt \- Firefly, https://wiki.t-firefly.com/ROC-RK3328-CC/\_sources/flash\_emmc.md.txt 65\. RKNN Installation | Radxa Docs, https://docs.radxa.com/en/rock5/rock5c/app-development/rknn\_install