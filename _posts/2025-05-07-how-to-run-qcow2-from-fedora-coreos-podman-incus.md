---
tags: [scratchpad]
info: aberto.
date: 2025-05-07
type: post
layout: post
published: true
slug: how-to-run-qcow2-from-fedora-coreos-podman-incus
title: 'How to run `.qcow2` from Fedora CoreOS + Podman + Incus'
---
**Understanding the Core Technology**

*   **Incus:** Your custom OS includes Incus, a powerful system container and virtual machine manager. For VMs, Incus utilizes QEMU/KVM.
*   **QEMU/KVM:**
    *   **QEMU:** An open-source machine emulator and virtualizer.
    *   **KVM (Kernel-based Virtual Machine):** A Linux kernel module that enables QEMU to use hardware virtualization extensions (Intel VT-x or AMD-V), providing near-native performance. Fedora CoreOS includes KVM support.
*   **`.qcow2`:** This is a disk image format commonly used by QEMU, supporting features like copy-on-write and snapshots.

**Methods to Run a `.qcow2` Image with Incus**

Here are a few methods, ranging from a quick one-off boot to creating a reusable Incus image:

**Prerequisites for all methods:**

1.  **Hardware Virtualization:** Ensure Intel VT-x or AMD-V is enabled in your machine's BIOS/UEFI.
2.  **`.qcow2` File:** The bootable `.qcow2` file must be accessible on your custom OS's filesystem (e.g., copied to your home directory or another accessible path).
3.  **Incus Initialization (One-time):** If you haven't used Incus before, you might need to initialize it. This typically involves setting up a default profile and a storage pool.
    ```bash
    sudo incus admin init
    ```
    Follow the prompts. For simplicity, you can often accept the defaults. This might create a storage pool (e.g., named `default`).
4.  **User Permissions:** While `incus admin init` requires `sudo`, many subsequent `incus` commands can be run by a user added to the `incus-admin` group (or `lxd` if you had a previous LXD installation and it was migrated). If your user is not in this group, you may need to prefix `incus` commands with `sudo`.

---

**Method 1: Direct Boot by Attaching `.qcow2` as a Disk (Recommended for Quick/One-Off Use)**

This method is often the most straightforward for booting an existing `.qcow2` file without converting it into a formal Incus image, especially if your Incus storage pool is of type `dir`.

1.  **Create a VM Instance (without a standard root disk initially):**
    It's often easiest to launch a minimal VM instance using a placeholder image (like a minimal cloud image if you have one aliased, or even a standard image whose disk you'll immediately replace).
    ```bash
    # Launch a VM; 'images:alpine/edge' is just a small image to create the VM config.
    # We will replace its disk.
    incus launch images:alpine/edge my-qcow-vm --vm 
    ```
    *Note: If you have a very minimal image alias or a profile designed for "empty" VMs, you can use that instead.*

2.  **Stop the VM:**
    The VM will likely start automatically. Stop it to modify its disk configuration.
    ```bash
    incus stop my-qcow-vm
    ```

3.  **Remove the Default Root Disk:**
    The VM was created with a root disk from the placeholder image. Remove it.
    ```bash
    incus config device remove my-qcow-vm root
    ```

4.  **Add Your `.qcow2` File as the New Root Disk:**
    This command tells Incus to use your `.qcow2` file as the primary bootable disk for the VM.
    ```bash
    incus config device add my-qcow-vm root disk source=/path/to/your/image.qcow2 boot.priority=1
    ```
    Replace `/path/to/your/image.qcow2` with the actual path to your file.
    *   **Storage Pool Consideration:** This method works best if your Incus storage pool (e.g., `default`) is of type `dir`. For block-based pools (LVM, ZFS, Ceph), Incus might try to import the `.qcow2` content into a new volume in its native format, which is usually fine.

5.  **Start the VM:**
    ```bash
    incus start my-qcow-vm
    ```

6.  **Access the VM Console:**
    ```bash
    incus console my-qcow-vm
    ```
    Press `Ctrl+a q` (or `Ctrl+a c` then `q`) to detach from the console.

---

**Method 2: Importing `.qcow2` into a Custom Storage Volume (More Robust for Block-Based Pools)**

If your storage pool is block-based (e.g., LVM, ZFS), or you want Incus to manage the disk image as a distinct volume, this method is more appropriate. It involves converting the `.qcow2` to a raw format and importing that.

1.  **Identify Your Storage Pool:**
    ```bash
    incus storage list
    ```
    Note the name of your desired storage pool (e.g., `default`).

2.  **Convert `.qcow2` to Raw Format (if needed):**
    Incus's volume import often works best with raw image files.
    ```bash
    qemu-img convert -f qcow2 -O raw /path/to/your/image.qcow2 /tmp/image.raw
    ```
    Replace paths as necessary. Ensure you have enough space in `/tmp` or choose another location.

3.  **Import the Raw Image into an Incus Custom Storage Volume:**
    ```bash
    incus storage volume import <your-pool-name> /tmp/image.raw <name-for-your-volume>
    ```
    For example:
    ```bash
    incus storage volume import default /tmp/image.raw my-custom-boot-volume
    ```
    This creates an Incus storage volume containing the content of your bootable image.

4.  **Clean up the temporary raw file:**
    ```bash
    rm /tmp/image.raw
    ```

5.  **Launch a VM Using the Custom Volume:**
    You'll create a VM instance and tell it to use this custom volume as its root disk.
    ```bash
    # Create a VM instance (similar to Method 1, using a placeholder)
    incus launch images:alpine/edge my-custom-vol-vm --vm
    incus stop my-custom-vol-vm
    incus config device remove my-custom-vol-vm root

    # Add the custom volume as the root disk
    incus config device add my-custom-vol-vm root disk pool=<your-pool-name> source=<name-for-your-volume> boot.priority=1
    # Example:
    # incus config device add my-custom-vol-vm root disk pool=default source=my-custom-boot-volume boot.priority=1

    incus start my-custom-vol-vm
    ```

6.  **Access the VM Console:**
    ```bash
    incus console my-custom-vol-vm
    ```

---

**Method 3: Creating a Reusable Incus Image from `.qcow2` (For Frequent Use)**

If you plan to launch multiple VMs from this same `.qcow2` image, creating a proper Incus image is efficient.

1.  **Prepare a `metadata.yaml` File:**
    This file describes your image to Incus. Create a file named `metadata.yaml` in the same directory as your `.qcow2` file (or a temporary directory where you copy the `.qcow2`):
    ```yaml
    architecture: x86_64  # Or your image's architecture (e.g., aarch64)
    creation_date: $(date +%s) # This will be replaced by actual date in next step
    properties:
      os: "MyQcow2OS" # A friendly name for the OS
      description: "Bootable qcow2 image"
      architecture: "x86_64" # Repeat architecture here
    # Add other properties if known, like 'release', 'variant', etc.
    ```
    You can generate the `creation_date` dynamically:
    ```bash
    cat <<EOF > metadata.yaml
    architecture: $(uname -m) # Or specify explicitly e.g. x86_64
    creation_date: $(date +%s)
    properties:
      os: "MyQcow2OS"
      description: "My custom bootable qcow2"
      architecture: "$(uname -m)" # Or specify explicitly
    EOF
    ```

2.  **Create a Tarball:**
    Package the `.qcow2` file (e.g., `my-image.qcow2`) and `metadata.yaml` into a `.tar.gz` file. The `.qcow2` file should be named `root.img` or `disk.img` inside the tarball for some Incus versions, or more generally, Incus will pick up the largest file as the root disk if it's a qcow2. For simplicity, let's assume your qcow2 is `my-os.qcow2`. You might need to rename it to `root.qcow2` or ensure it's the clear candidate.
    A common practice is to name the image file `root.qcow2` within the tarball.
    ```bash
    # Assuming your qcow2 is my-os.qcow2
    cp /path/to/your/my-os.qcow2 . # Copy to current directory
    mv my-os.qcow2 root.qcow2      # Rename for clarity within tarball
    tar -czvf my-incus-image.tar.gz root.qcow2 metadata.yaml
    ```

3.  **Import the Tarball as an Incus Image:**
    ```bash
    incus image import my-incus-image.tar.gz --alias my-bootable-qcow-image
    ```
    This makes the image available in your local Incus image store.

4.  **Clean up Temporary Files:**
    ```bash
    rm root.qcow2 metadata.yaml my-incus-image.tar.gz
    ```

5.  **Launch a VM from the New Incus Image:**
    ```bash
    incus launch my-bootable-qcow-image my-new-vm --vm
    ```

6.  **Access the VM Console:**
    ```bash
    incus console my-new-vm
    ```

---

**Alternative: Direct QEMU/KVM (Bypassing Incus Management)**

While Incus is the recommended and integrated way on your custom OS, you *could* use QEMU/KVM directly. This gives raw access but lacks Incus's management features (networking, storage, snapshots, etc.).

1.  **Ensure QEMU/KVM Utilities are Installed:**
    On Fedora CoreOS, if not already present as a dependency of Incus, you might need to install them:
    ```bash
    sudo rpm-ostree install qemu-system-x86 # For x86_64
    # May require a reboot
    # sudo systemctl reboot
    ```
    However, `incus` typically pulls in `qemu-kvm` or similar packages.

2.  **Run with `qemu-system-x86_64`:**
    ```bash
    qemu-system-x86_64 \
        -enable-kvm \
        -m 2048 \
        -smp 2 \
        -hda /path/to/your/image.qcow2 \
        -boot d \
        -vga std \
        -net nic -net user,hostfwd=tcp::2222-:22 # Example networking
    ```
    This is more manual and generally not preferred if Incus is available.

**Podman's Role**

Podman is for managing OCI/Docker-compatible *containers*, not full virtual machines from `.qcow2` images. It operates at a different level of virtualization (OS-level virtualization, sharing the host kernel) compared to the hardware virtualization used by Incus for VMs.

**Conclusion**

Your Fedora CoreOS + Podman + Incus system is well-equipped to run `.qcow2` Linux images. **Using Incus (Method 1 or 2 for direct use, Method 3 for reusability) is the most integrated and recommended approach.** It provides a robust management layer over QEMU/KVM, allowing you to easily launch and manage these VMs right after your system boots.