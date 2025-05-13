---
tags: [scratchpad]
info: aberto.
date: 2025-04-14
type: post
layout: post
published: true
slug: windows11-incus
title: 'Windows 11 within an Incus VM'
---
Running Windows 11 Enterprise within an Incus VM can be essential for various purposes, such as application compatibility testing, software development in a clean Windows environment, accessing specific Windows-only tools, creating isolated environments for security research, or general desktop use.

This guide focuses on using Incus commands for VM creation and management. Incus abstracts many complexities of direct hypervisor interaction, offering benefits like easier VM lifecycle management, simplified configuration through profiles and instance settings, built-in snapshot capabilities, and streamlined network and storage setup.

**Assumptions:**

*   You have a functional installation of Incus on your Linux host system.
*   Your Incus installation has been initialized (e.g., via `sudo incus admin init`) with at least one storage pool and a network bridge configured.
*   Your host system's CPU supports hardware virtualization (Intel VT-x or AMD-V / AMD-SVM), and these features are enabled in the BIOS/UEFI.
*   Your host system ideally has TPM 2.0 capabilities and Secure Boot enabled in the BIOS/UEFI for full Windows 11 compatibility.
*   You possess sufficient hardware resources (CPU processing power, adequate RAM, and ample Disk Space) to comfortably run both the host Linux system and the Windows 11 Enterprise guest VM.
*   You have a basic understanding of navigating the Linux command line and possess `sudo` privileges or are a member of the `incus-admin` group for managing Incus.

## **1. Prerequisites**

Before embarking on the installation process, ensure all the following prerequisites are met:

*   **Windows 11 Enterprise Installation ISO:** You must possess a legitimate **Windows_11_Enterprise_x64.iso** file (or a similarly named ISO image) containing the 64-bit installation media for Windows 11 Enterprise.
    *   **Licensing:** Ensure you have a valid license for Windows 11 Enterprise. Evaluation versions might be available from the Microsoft Evaluation Center.
    *   This guide cannot provide this copyrighted software. **Crucially, remember the exact, full path to this ISO file on your host Linux system.**
*   **VirtIO Drivers ISO (Essential for Performance):** For optimal disk, network, and guest integration performance, download the latest stable **virtio-win.iso** file. This ISO contains paravirtualized drivers and guest tools. Obtain it from the official Fedora project repository: [https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso](https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso). **Remember the exact, full path to this downloaded file as well.**
*   **Hardware Virtualization Enabled (Essential):** Modern CPUs include hardware features (Intel VT-x or AMD-V / AMD-SVM) that KVM (and thus Incus VMs) use for acceleration. Verify it's enabled in your system's BIOS/UEFI settings and detectable by Linux:
    ```bash
    egrep -c '(vmx|svm)' /proc/cpuinfo
    ```
    The output *must* be 1 or greater. If 0, enable "Virtualization Technology," "VT-x," "AMD-V," or "SVM Mode" in your BIOS/UEFI.
*   **TPM 2.0 Module on Host (Highly Recommended for Windows 11):** Windows 11 officially requires TPM 2.0.
    *   Ensure your host machine has a TPM 2.0 module and it's enabled in the BIOS/UEFI (often listed as "Security Chip," "TPM Device," etc.).
*   **Secure Boot on Host (Recommended for Windows 11):** For enhanced security, ensure Secure Boot is enabled in your host's BIOS/UEFI settings if you intend to use it for the VM.
*   **Sufficient System Resources:**
    *   **RAM:** Windows 11 requires a minimum of 4GB RAM. For Enterprise and smooth operation, allocate at least **8GB or more** to the VM. Ensure your host has enough *additional* RAM.
    *   **CPU:** A modern multi-core 64-bit processor. Allocate at least **2 vCPUs** to the VM, with 4 or more recommended.
    *   **Disk Space:** Windows 11 requires a minimum of 64GB. A virtual disk size of **100GB or more is strongly recommended**. Ensure your Incus storage pool has sufficient free space.

## **2. Install and Initialize Incus (If Not Already Done)**

If Incus is not yet installed and configured, follow these general steps.

1.  **Install Incus:** Use your Linux distribution's package manager.
    ```bash
    # Example using APT (Debian, Ubuntu, Mint derivatives)
    sudo apt update
    sudo apt install incus
    ```
    For other distributions, refer to the official Incus documentation: [https://linuxcontainers.org/incus/docs/main/installing/](https://linuxcontainers.org/incus/docs/main/installing/).
2.  **Add User to `incus-admin` Group (Recommended):** To manage Incus without `sudo` for every command:
    ```bash
    sudo usermod -aG incus-admin $USER
    ```
    You **must log out completely and log back in** for this group change to take effect. Otherwise, continue using `sudo incus ...`.
3.  **Initialize Incus Daemon (If First Time):** If this is a new Incus setup, initialize the daemon:
    ```bash
    sudo incus admin init
    ```
    Follow the prompts. For storage, `dir` is simple for beginners, while `zfs` or `btrfs` offer advanced features. For networking, creating a new bridge (e.g., `incusbr0`) with NAT is common. This is a one-time setup for the Incus service.
4.  **Verify Incus:**
    ```bash
    incus --version
    incus profile list
    incus storage list
    incus network list
    ```

## **3. Create and Configure the Windows 11 VM Instance**

We'll create an empty VM instance, then configure its properties and devices. Let's name our VM `win11-ent`.

1.  **Create an Empty VM Instance:**
    ```bash
    incus init win11-ent --empty --vm
    ```
    This command creates a new virtual machine instance named `win11-ent` without any pre-installed OS.

2.  **Configure VM Resources and Features:**
    *   **CPU and Memory:**
        ```bash
        incus config set win11-ent limits.cpu 4      # Allocate 4 vCPUs (adjust as needed)
        incus config set win11-ent limits.memory 8GB # Allocate 8GB RAM (adjust as needed)
        ```
    *   **TPM (Trusted Platform Module):** Essential for Windows 11.
        ```bash
        incus config set win11-ent security.tpm=true
        ```
        This enables an emulated TPM device for the VM.
    *   **Secure Boot:** Recommended for Windows 11.
        ```bash
        incus config set win11-ent security.secureboot=true
        ```
        *Note: This requires Secure Boot to be supported and properly configured on your host system and by Incus. If Windows 11 setup fails specifically due to Secure Boot and host-side issues are complex to resolve, you might temporarily set this to `false` for installation, but it's not recommended for production or secure environments.*

3.  **Add Virtual Disk for Windows Installation:**
    Replace `<your_storage_pool_name>` with the name of your Incus storage pool (e.g., `default` if you used that during `incus admin init`).
    ```bash
    incus config device add win11-ent root disk pool=<your_storage_pool_name> size=100GB
    ```
    This adds a 100GB virtual disk to the VM, which will serve as its primary storage.

4.  **Attach Installation ISOs:**
    Replace `/path/to/your/...` with the actual, full paths to your ISO files.
    *   **Windows 11 Installation ISO:**
        ```bash
        incus config device add win11-ent install-iso disk source=/path/to/your/Windows_11_Enterprise_x64.iso boot.priority=10
        ```
        The `boot.priority=10` tells Incus to attempt booting from this virtual CD-ROM first.
    *   **VirtIO Drivers ISO:**
        ```bash
        incus config device add win11-ent virtio-iso disk source=/path/to/your/virtio-win.iso
        ```
        This attaches the VirtIO driver ISO, which will be needed during and after OS installation.

## **4. Start the VM and Install Windows 11**

Now, launch the VM and proceed with the Windows 11 installation.

1.  **Start the VM:**
    ```bash
    incus start win11-ent
    ```
2.  **Access the VM Console:**
    This will open a graphical console window (usually SPICE-based).
    ```bash
    incus console win11-ent --type=vga
    ```
3.  **Windows Setup Process:**
    *   The VM should boot from the attached Windows 11 ISO. You'll see a prompt like "Press any key to boot from CD or DVD...".
    *   Follow the on-screen prompts: select language, time format, and keyboard input.
    *   Click "Install now".
    *   Enter your Windows 11 Enterprise product key or choose "I don't have a product key" for later activation.
    *   Select the edition of Windows 11 Enterprise.
    *   Accept the license terms.
    *   Choose "Custom: Install Windows only (advanced)".
    *   **Disk Selection / VirtIO Driver Loading (Crucial Step):**
        *   At the "Where do you want to install Windows?" screen, the 100GB virtual disk might not be visible initially. This is because Windows 11 doesn't have built-in VirtIO storage drivers, which Incus VMs typically use for best performance.
        *   Click "**Load driver**".
        *   Click "**Browse**".
        *   Navigate to the attached VirtIO ISO (it will appear as a CD/DVD drive, e.g., D: or E:).
        *   Locate the storage driver folder. This is typically `viostor\w11\amd64` (for VirtIO SCSI/block). If using a different VirtIO controller type, the path might vary slightly (e.g., `vioscsi\w11\amd64`). Select the `amd64` subfolder for 64-bit Windows.
        *   Click "OK". Windows should find the "Red Hat VirtIO SCSI controller" (or similar). Select it and click "Next".
        *   The 100GB virtual disk (e.g., "Drive 0 Unallocated Space") should now appear. Select it.
        *   Click "Next". Windows will partition and format the drive and begin copying files.
    *   **Reboots and Configuration:** The VM will reboot several times. Incus should automatically boot from the virtual hard disk after the initial installation phase.
    *   Complete the Out-Of-Box Experience (OOBE): select region, keyboard layout, name your PC, set up user accounts, configure privacy settings, etc.

**Pro Tip:** For managing multiple similar VMs, consider using Incus profiles. You can define common settings (CPU, memory, TPM, Secure Boot, even base devices) in a profile and apply it when creating new VMs: `incus init <vm_name> --empty --vm -p <your_profile_name>`.

## **5. Install VirtIO Drivers & Guest Tools Post-Installation**

Even if Windows 11 installed some basic drivers, installing the full VirtIO guest tools package from the VirtIO ISO is highly recommended for optimal performance and features.

1.  **Log In to Windows 11:** Access your newly installed Windows 11 Enterprise VM.
2.  **Install Guest Tools:**
    *   Open File Explorer. You should see the virtual CD drive containing the VirtIO drivers (e.g., labeled "virtio-win").
    *   Run the **`virtio-win-guest-tools.exe`** installer from the root of the VirtIO ISO. This application will install all relevant VirtIO drivers (Network: NetKVM, Disk/SCSI: viostor/vioscsi, Memory Ballooning: virtio-balloon, Input: vioinput, GPU: viogpu if applicable) and guest services.
    *   Follow the installer prompts. A reboot will likely be required.
3.  **Reboot the VM:** After the installation is complete, **reboot** the Windows 11 VM to ensure all drivers and services are loaded correctly.

**Understanding VirtIO Benefits:**
Paravirtualized drivers like VirtIO provide an optimized communication path between the guest OS and the KVM hypervisor, resulting in:
*   **Faster Disk I/O:** Higher throughput and lower latency.
*   **Improved Network Performance:** Higher throughput and lower latency.
*   **Reduced CPU Overhead:** Less host CPU time spent emulating generic hardware.
*   **Memory Ballooning:** Allows the host to reclaim unused memory from the guest dynamically.
*   **Better Guest Integration:** Features like shared clipboard (if SPICE agent is included and console supports it), stable time, etc.

## **6. Final Steps & Troubleshooting**

With Windows 11 Enterprise installed and optimized:

*   **Detach Installation ISOs (Optional):** Once Windows is stable, you can detach the ISOs if desired.
    ```bash
    incus stop win11-ent # Stop the VM first
    incus config device remove win11-ent install-iso
    # incus config device remove win11-ent virtio-iso # Keep if you might need to repair/reinstall tools
    incus start win11-ent
    ```
*   **Windows Updates & Security:**
    *   Connect your VM to the internet (Incus default NAT bridge usually provides this).
    *   Run Windows Update to install all critical updates and security patches.
    *   Configure Windows Security (Defender) or install preferred third-party security software.
*   **Install Applications:** Install your required software within the VM.
*   **Common Troubleshooting Tips:**
    *   **Permission Denied (Incus commands):** Ensure your user is in the `incus-admin` group and has re-logged in, or use `sudo incus ...`.
    *   **VM Fails to Start/Boot:** Check VM logs: `incus info win11-ent` (for current state), `incus operation log <UUID>` (for failed operations). Check host system logs (`dmesg`, `journalctl -u incus.service`).
    *   **TPM/Secure Boot Issues:** If `security.tpm=true` or `security.secureboot=true` cause boot failures, double-check host BIOS/UEFI settings. Ensure your Incus version fully supports these features for Windows VMs.
    *   **Cannot Find ISO File:** Double-check the `source=` path in `incus config device add ...` commands. Use absolute paths.
    *   **No Network/Disk Access in VM (Post-Install):** Ensure VirtIO drivers are correctly installed (check Device Manager in Windows). Re-run `virtio-win-guest-tools.exe` if necessary.
    *   **Console/Display Issues:** Ensure your host has necessary packages for graphical console (e.g., `spice-client-gtk` or similar).
    *   **Windows Activation:** Ensure network access for activation. Use a valid product key or appropriate volume licensing method.
*   **Incus Advanced Management:**
    *   **Snapshots:** `incus snapshot create win11-ent <snapshot_name>`, `incus snapshot restore win11-ent <snapshot_name>`, `incus delete win11-ent/<snapshot_name>`.
    *   **File Transfer:** `incus file push <source_path> win11-ent/<destination_path_in_vm>`, `incus file pull win11-ent/<source_path_in_vm> <destination_path>` (requires guest agent from VirtIO tools).
    *   **Execute Commands:** `incus exec win11-ent -- cmd.exe /c "ipconfig"` (requires guest agent).
