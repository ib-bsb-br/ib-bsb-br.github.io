---
tags: [scratchpad]
info: aberto.
date: 2025-05-03
type: post
layout: post
published: true
slug: clear-linux-os-as-a-hypervisor-to-run-the-sbnbvhd-vm
title: 'Clear Linux OS as a hypervisor to run the `sbnb.vhd` VM'
---
This guide presents two main methods:

1.  **Direct QEMU/KVM (Most Minimal):** Using command-line tools directly for the lowest overhead.
2.  **Virt-Manager (User-Friendly Alternative):** Using a graphical tool built on libvirt/QEMU for easier management.

**Prerequisites (Apply to Both Methods)**

1.  **Clear Linux Host:** A working Clear Linux installation.
2.  **Hardware Virtualization:** Ensure Intel VT-x or AMD-V is enabled in your host machine's BIOS/UEFI. Verify with:
    ```bash
    lscpu | grep -E "svm|vmx"
    ```
3.  **Install Essential Bundles:** Install KVM/QEMU, management libraries, and potentially tools for key handling.
    ```bash
    sudo swupd update
    # Installs KVM/QEMU, libvirt, OVMF firmware, basic tools
    sudo swupd bundle-add kvm-host
    # Optional: Install virt-manager GUI if using Method 2
    sudo swupd bundle-add virt-manager-gui
    # Optional: Install mkisofs if using ISO for Tailscale key
    sudo swupd bundle-add cdrtools
    ```
4.  **Enable Libvirt Daemon (Recommended, especially for Method 2):**
    ```bash
    sudo systemctl enable --now libvirtd
    # Verify it's running
    systemctl status libvirtd
    ```
5.  **Obtain `sbnb.vhd`:** Download or copy the `sbnb.vhd` file onto your Clear Linux system.

**Handling the SBNB Tailscale Key**

SBNB requires a `sbnb-tskey.txt` file containing your Tailscale authentication key to establish network connectivity during boot. It typically looks for this file in `/mnt/sbnb/` (from a USB drive) or `/mnt/vmware/` (VMware shared folder). Here are ways to provide it:

*   **Method A: ISO Image (Recommended for Simplicity)**
    1.  Create the key file: `echo "YOUR_TAILSCALE_KEY" > sbnb-tskey.txt`
    2.  Create an ISO (requires `cdrtools` bundle): `mkisofs -o sbnb-key.iso sbnb-tskey.txt`
    3.  Attach this `sbnb-key.iso` as a CD-ROM drive to the VM. SBNB's boot script should find and mount the CD-ROM to read the key.
*   **Method B: Virtual FAT32 USB Drive (More Complex Setup)**
    1.  Create an image file: `dd if=/dev/zero of=sbnb-key.img bs=1M count=10`
    2.  Format it: `mkfs.vfat sbnb-key.img`
    3.  Mount, copy `sbnb-tskey.txt` (ensure exact filename), unmount (see previous response for detailed steps).
    4.  Attach this `sbnb-key.img` as a USB storage device.

**Method 1: Direct QEMU/KVM (Most Minimal)**

This method avoids graphical tools and management layers like libvirt.

1.  **Verify OVMF Path:** The UEFI firmware is essential. Find its path. Common locations:
    *   `/usr/share/qemu/OVMF.fd`
    *   `/usr/share/ovmf/OVMF.fd`
    Check with `ls /usr/share/qemu/*.fd` or `ls /usr/share/ovmf/*.fd`. Ensure the file exists.
2.  **Launch Command:**
    ```bash
    qemu-system-x86_64 \
        -enable-kvm \
        -m 1G \
        -smp 2 \
        -cpu host \
        -bios /usr/share/qemu/OVMF.fd \
        -drive file=sbnb.vhd,format=vpc,if=virtio \
        -cdrom sbnb-key.iso \
        -netdev user,id=net0 \
        -device virtio-net-pci,netdev=net0 \
        -nographic
    ```
    *   `-enable-kvm`: Use hardware virtualization.
    *   `-m 1G`: 1GB RAM (adjust as needed).
    *   `-smp 2`: 2 vCPUs (adjust as needed).
    *   `-cpu host`: Pass through host CPU features (good for performance).
    *   `-bios /path/to/OVMF.fd`: **CRITICAL:** Use the verified path to UEFI firmware.
    *   `-drive file=sbnb.vhd,format=vpc,if=virtio`: Use the VHD directly (`format=vpc`) with the high-performance `virtio` block driver.
    *   `-cdrom sbnb-key.iso`: Attach the Tailscale key ISO (using Method A above). (Alternatively, use `-usb -device usb-storage...` for Method B).
    *   `-netdev user,id=net0 -device virtio-net-pci,netdev=net0`: Basic user-mode networking using `virtio`.
    *   `-nographic`: Run headless. Remove for a graphical console window.

**Method 2: Virt-Manager (User-Friendly Alternative)**

This uses the graphical `virt-manager` tool.

1.  **Launch Virt-Manager:** Open the application (`virt-manager`).
2.  **Create New VM:** Click "File" -> "New Virtual Machine".
3.  **Choose Import:** Select "Import existing disk image".
4.  **Provide Disk Path:** Browse to and select your `sbnb.vhd` file. QEMU/KVM (via libvirt) can often handle VHD directly.
5.  **OS Type:** Choose "Linux" -> "Generic" or a specific version if known (e.g., "Generic Linux 2020").
6.  **Memory/CPU:** Allocate RAM (e.g., 1024 MiB) and CPUs (e.g., 2).
7.  **Customize Before Install:** **Check the box** "Customize configuration before install". Click "Finish".
8.  **Configuration:**
    *   **Overview/Firmware:** **CRITICAL:** Ensure "Firmware" is set to **UEFI** (it might show a path like `/usr/share/qemu/OVMF.fd`).
    *   **Disk:** Select the imported disk (`sbnb.vhd`). Under "Advanced options", ensure "Disk bus" is set to **VirtIO** for best performance. (Use SATA only if VirtIO causes issues).
    *   **Add Hardware (Tailscale Key):**
        *   Click "Add Hardware".
        *   Select "Storage".
        *   Choose "Select or create custom storage".
        *   Device type: "CDROM device".
        *   Click "Manage...", browse to and select your `sbnb-key.iso` (created using Method A above).
        *   Click "Finish".
    *   **NIC:** Ensure the network interface device model is **virtio**.
9.  **Begin Installation:** Click "Begin Installation". The VM will boot using the VHD and the attached ISO for the key.

**Optional: VHD to QCOW2 Conversion**

*   **Why?** While QEMU/KVM can use VHD (`vpc`) directly, converting to QCOW2 (QEMU's native format) can offer better performance and features like snapshots.
*   **How?** `qemu-img convert -p -f vpc -O qcow2 sbnb.vhd sbnb.qcow2`
*   **Usage:** If converted, simply point your QEMU command (`-drive file=sbnb.qcow2,format=qcow2,...`) or `virt-manager` import step to the `.qcow2` file instead of the `.vhd` file. This conversion is **not strictly required** but often recommended.

**Verification**

After starting the VM using either method:

1.  Monitor your Tailscale Admin Console. The new `sbnb-` device should appear.
2.  SSH into the device using its Tailscale IP or MagicDNS name.
3.  Run `sbnb-dev-env.sh` if needed for development tasks.