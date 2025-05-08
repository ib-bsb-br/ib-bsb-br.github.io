---
tags: [scratchpad]
info: aberto.
date: 2025-05-08
type: post
layout: post
published: true
slug: installing-incus-os
title: 'installing Incus OS'
---
bibref https://github.com/lxc/incus-os

**I. Introduction to Incus OS and Intel N97 Deployment**

Incus OS is a minimal, immutable operating system designed specifically for running Incus instances (virtual machines and system containers). It prioritizes security through features like UEFI Secure Boot integration, dm-verity for disk integrity, TPM-based disk encryption, and an A/B update mechanism. Incus, a modern system container and virtual machine manager, offers a powerful platform for developing and hosting applications. Deploying Incus OS directly onto bare metal ensures maximum performance and control, transforming the host into a dedicated Incus appliance. Incus OS is designed to take advantage of these hardware security mechanisms to create a "locked down environment".`2`

The Intel N97 processor, part of the Alder Lake-N series, is a 64-bit, quad-core CPU with features suitable for lightweight server tasks, including virtualization.`1` Its low power consumption (12W TDP) makes it an attractive option for always-on home servers or small-scale deployments.`1` This guide focuses on a bare-metal x64 host system with an Intel N97 processor.

**II. Crucial Preliminary Considerations**

*   **Experimental Stage:** Incus OS is in early development. Users should expect potential rough edges and be prepared for troubleshooting. This guide is primarily for testing and evaluation purposes.
*   **Hardware Requirements:**
    *   **x64 Architecture:** The Intel N97 meets this.
    *   **TPM (Trusted Platform Module) 2.0:** This is **mandatory**. A critical point is that systems without a TPM will be flagged by the Incus OS UI, and installation may fail or result in a non-functional state.
    *   **UEFI Firmware:** Incus OS is designed for UEFI systems.
    *   **RAM and Storage:** A minimum of 8GB RAM is recommended (as used in a VM test); 16GB or more for multiple or larger instances. An NVMe or SATA SSD is recommended for the target disk. A separate USB drive is needed for installation media.
*   **Backup Existing Data:** The installation process will erase the target disk. **Ensure all important data from the target N97 machine is backed up before proceeding.**
*   **Separate Linux Machine:** Needed for preparing the USB installation media and seed configuration files.
*   **Flasher Tool:** A "flasher tool" to simplify image writing and seed creation is reportedly planned but may not yet be available. This guide describes the manual method.

**III. Phase 1: Host System UEFI/BIOS Configuration (Intel N97)**

Correct BIOS/UEFI configuration is paramount for a successful Incus OS installation and for enabling its security and virtualization features.

*   **Understanding the Intel N97 Platform for Incus OS:**
    Before proceeding with the installation, it is crucial to understand the capabilities and potential limitations of the Intel N97 platform in the context of running Incus OS.
    *   **Key Intel N97 Features Relevant to Virtualization and Security:** The Intel N97 processor incorporates several hardware features that are essential or beneficial for running a secure and efficient virtualization host with Incus OS. These are foundational to the secure "enclosure" concept.
        *   **Table 1: Intel N97 Key Virtualization and Security Features**
            | Feature Name                                            | Status on Intel N97 (Source) | Criticality/Role for Incus OS Deployment                                                                                                     |
            | :------------------------------------------------------ | :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------- |
            | Intel® Virtualization Technology (VT-x)                 | Yes `1`                      | Essential for all virtualization; enables the CPU to run multiple operating systems (VMs) and enhances container isolation.                  |
            | Intel® Virtualization Technology for Directed I/O (VT-d) | Yes `1`                      | Crucial for PCI device passthrough to Incus virtual machines, allowing VMs direct access to hardware like GPUs, network cards, or storage controllers. |
            | Intel® VT-x with Extended Page Tables (EPT)             | Yes `1`                      | Enhances VM memory management performance by reducing hypervisor overhead, leading to more efficient virtualization.                         |
            | Intel® Boot Guard                                       | Yes `1`                      | Provides hardware-based boot integrity, forming a root of trust. This is a foundational element for Secure Boot, which Incus OS is designed to leverage.`2` |
            | Intel® OS Guard                                         | Yes `1`                      | Protects the operating system kernel from modification by malicious software, contributing to the overall security of the Incus OS environment. |
            | TPM 2.0 Support                                         | Typically present `3`        | Used by Incus OS for features like measured boot (verifying boot components) and TPM-backed full-disk encryption, enhancing system security.`2` |
            | 64-bit Instruction Set                                  | Yes `1`                      | Mandatory for running modern operating systems, including Incus OS and the guest operating systems within Incus instances.                   |
        The presence of these features, confirmed by Intel's official specifications `1` and motherboard documentation (e.g., ASRock NUC-N97 indicating "TPM 2.0 onboard IC" `3`), ensures that the N97 CPU meets the fundamental hardware requirements for a robust Incus OS deployment.
    *   **Potential Performance Considerations and Platform Variability:**
        *   **Single-Channel Memory Architecture:** The Intel N97 processor supports only a single memory channel.`1` Motherboards based on this CPU, such as the ASRock NUC-N97, also specify single-channel DDR4 3200 MHz technology.`3` This could be a performance bottleneck for memory-bandwidth intensive Incus workloads. Using the fastest supported RAM type available for the specific N97 board can help maximize available bandwidth.
        *   **"Embedded" Nature and BIOS Variability:** The Intel N97 is categorized under "Intel® Processor N-series" with a "Vertical Segment" of "Embedded".`1` This can lead to greater variability in BIOS/UEFI implementations across different N97-based systems. User experiences with GMKtec N97 Mini PCs, for instance, have highlighted issues with BIOS interfaces and USB boot behavior.`4` The low power consumption, however, is a significant advantage.

*   **Accessing BIOS/UEFI Setup:**
    This is typically done by pressing a specific key (commonly F2, Delete, ESC, or F10 `6`) immediately after powering on the system. The exact key can vary. For instance, the ASRock NUC-N97 motherboard manual outlines its BIOS structure.`3`

*   **Essential Settings to Configure:**
    Once inside the BIOS/UEFI setup utility, several settings must be verified and adjusted.
    *   **Table 2: Recommended BIOS/UEFI Settings for Incus OS on Intel N97**
        | Setting Category      | Typical Setting Name(s) in BIOS (and common variations)        | Recommended Value for Incus OS                                              | Rationale & Importance                                                                                                                               |
        | :-------------------- | :------------------------------------------------------------- | :-------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- |
        | Load Defaults         | Load Optimized Defaults, Load UEFI Defaults                    | Execute this first                                                          | Establishes a clean, known baseline. Intel NUCs often use F9 for this.`6`                                                                              |
        | Virtualization        | Intel® Virtualization Technology, VT-x, Virtualization, SVM Mode | Enabled                                                                     | Core requirement for Incus. Found in "CPU Configuration".`3` N97 supports VT-x.`1`                                                                      |
        | I/O Virtualization    | Intel® VT-d, Directed I/O, IOMMU                               | Enabled                                                                     | Essential for PCIe device passthrough. Often in "Chipset Configuration." N97 supports VT-d.`1`                                                         |
        | TPM                   | Trusted Platform Module, TPM Device, Security Chip, fTPM       | Enabled & Activated (or "Available" / "Owned" depending on BIOS)            | Crucial for Incus OS security (measured boot, disk encryption).`2` Look for "Trusted Computing".`3` ASRock NUC-N97 has onboard TPM 2.0 IC.`3`          |
        | Secure Boot           | Secure Boot Control, Secure Boot                               | Enabled (with keys cleared for "Setup Mode")                                | Incus OS leverages Secure Boot.`2` For first boot, system must be in "Setup Mode" for key enrollment. Found in "Security" or "Boot" sections.`3` |
        | CSM                   | Compatibility Support Module                                   | Disabled                                                                    | Ensure pure UEFI mode.                                                                                                                               |
        | Boot Priority / Order | Boot Option #1, Fixed Boot Order Priorities, Boot Sequence     | 1st: USB Drive (for installation), Then: Internal SSD/NVMe (for installed OS) | To boot from installer, then installed system. N97 USB Boot Quirks: Some N97 BIOSes may require disabling boot priority options to recognize USB.`5` |
        | Hyper-Threading       | Intel® Hyper-Threading Technology, Logical Processor           | N/A or Disabled/Auto                                                        | Intel N97 does not support Hyper-Threading.`1`                                                                                                        |
        | Intel SGX             | Intel® Software Guard Extensions                               | Disabled or Default                                                         | Generally not required for Incus OS.                                                                                                                 |
    *   **Detailed Configuration Steps:**
        1.  **Load Optimized Defaults:** Navigate to "Exit" or "Save & Exit" and select "Load Optimized Defaults." Intel NUC systems often use F9.`6`
        2.  **Enable Intel® Virtualization Technology (VT-x):** Critical. Typically under "CPU Configuration" or "Advanced." Set to `Enabled`. The Intel N97 supports VT-x.`1`
        3.  **Enable Intel® VT-d (Virtualization Technology for Directed I/O):** If separate, also set to `Enabled`. Vital for PCIe passthrough. The N97 supports VT-d.`1`
        4.  **Enable and Configure TPM (Trusted Platform Module):** Locate "TPM" or "Trusted Computing" settings.`3` Ensure TPM 2.0 is `Enabled` and `Activated`. For Incus OS, it must be available for the OS to utilize for features like "TPM measured" boot and "storage encrypted using that TPM state".`2`
        5.  **Configure Secure Boot:** Find "Secure Boot" options.`3` Set Secure Boot to `Enabled`. **Crucially, for the initial installation, set Secure Boot to "Setup Mode."** This often involves an option to "Clear Secure Boot Keys," "Delete All Secure Boot Variables," or "Reset to Setup Mode." This allows Incus OS to enroll its own keys on first boot, as stated in its `README.md`: "On first boot, it will automatically add the relevant Secure Boot key (requires the system be in setup mode)."
        6.  **Disable CSM (Compatibility Support Module):** Ensure the system is in pure UEFI mode, not legacy BIOS compatibility mode.
        7.  **Set Boot Order/Priority (Addressing N97 USB Boot Issues):** Configure the USB drive as the primary boot device for installation.
            *   **Common N97 USB Boot Challenges:** Users of N97-based systems have reported difficulties booting from USB.`5`
            *   **Troubleshooting USB Boot:** First, try setting USB as the first boot option. If it fails, use the system's boot menu (often F7, F10, F11, F12, or ESC – F7 noted for a GMKtec N97 `5`). A specific N97 workaround involved setting both boot priority options to "disabled" to allow USB boot.`5`
        8.  **Review Conflicting/Unnecessary Settings:**
            *   **Virtualization MUST Be Enabled:** Advice to "disable Virtualization - potential for attack"`8` is incorrect for an Incus host. VT-x and VT-d are fundamental.
            *   **Hyper-Threading:** N/A for Intel N97.`1`
            *   **Intel SGX:** Leaving at default (often disabled or auto) is appropriate.

*   **Saving Changes:**
    Navigate to "Exit" or "Save & Exit," select "Save Changes and Exit." Intel NUCs typically use F10.`6`

**IV. Phase 2: Preparing Incus OS Installation Media & Seed Configuration (on Separate Linux Machine)**

*   **Downloading the Official Incus OS Image:**
    1.  Obtain the official Incus OS installation image from trusted sources, typically the official Incus project website or the Incus GitHub repository's "Releases" section.`2` Download the latest raw disk image for x86-64 (e.g., `IncusOS_VERSION.raw.gz`).
    2.  Decompress the image:
        ```bash
        gzip -d IncusOS_VERSION.raw.gz
        ```
        This results in a `.raw` file (e.g., `IncusOS_VERSION.raw`). For clarity, this guide may refer to it as `incus-os-installer.raw`.
    3.  **(Recommended) Verifying Image Integrity:** If checksums (e.g., SHA256) are provided, download the checksum file and verify the downloaded image using a utility like `sha256sum incus-os-installer.raw` and comparing the output.

*   **Preparing the USB Installation Drive:**
    1.  **USB Drive Selection (Size):** Use a USB drive of **at least 64GB**. This recommendation stems from observations that the Incus OS installer (specifically components like `systemd-repart`) might have expectations about minimum media size for its partitioning operations, beyond just fitting the OS image itself.
    2.  **Identify USB Device Name:** Insert the USB drive. Identify its device name (e.g., `/dev/sdb`, `/dev/sdc`) using `lsblk` or `sudo fdisk -l`. **Be extremely careful to choose the correct device, as the next step will overwrite it.**
    3.  **Writing the Image to USB Drive:**
        *   **Using `dd` (Linux/macOS - Use with Extreme Caution):**
            ```bash
            sudo dd if=incus-os-installer.raw of=/dev/sdX bs=4M status=progress conv=fsync
            ```
            Replace `/dev/sdX` with your USB device path.
        *   **Using Graphical Tools:** Balena Etcher (cross-platform) or Rufus (Windows) `5` are user-friendly alternatives. For Rufus, ensure "Partition scheme" is "GPT" and "Target system" is "UEFI (non CSM)".
    4.  **(Optional) `truncate` Raw Image (Primarily for VM testing):** In some VM test scenarios where the `.raw` file itself acts as the disk, if boot errors related to partition fitting occurred, truncating the `.raw` file to a larger size (e.g., 50GB) *before* writing it to the virtual disk was a workaround. This is less common for physical USB preparation if the USB stick itself is sufficiently large.
        ```bash
        # truncate -s 50G incus-os-installer.raw # Optional, context-dependent
        ```
    5.  **(Optional) GPT Table Relocation for Large USBs:** If the USB is much larger than the image, and boot issues occur, the backup GPT table might be misplaced. Use `sgdisk` on the USB drive (`x` then `e` then `w`) to relocate it to the end of the physical device.

*   **Creating Seed Configuration Files:**
    Incus OS uses a seed configuration (a tarball) to automate setup. The exact filenames expected within the tarball (`install.yaml`, `incus.yaml`, `network.yaml`) should be verified against the official Incus OS documentation for the specific version you are installing, as these can be implementation details.
    1.  **Create `install.yaml` (Installer Options):**
        ```yaml
        # install.yaml
        version: "1.0" 
        force_install: true 
        force_reboot: false 
        # target: 
        #   id: "ata-YOUR_DISK_MODEL_SERIAL" 
        ```
    2.  **Create `incus.yaml` (Incus Daemon Configuration):**
        ```yaml
        # incus.yaml
        version: "1.0" 
        apply_defaults: true 
        certificates:
          - name: "my-remote-admin-client" 
            type: "client"
            certificate: |
              YOUR_SINGLE_LINE_BASE64_ENCODED_DER_CERTIFICATE_CONTENT_HERE
            description: "Certificate for my remote admin machine"
        ```
        *   **Generating Client Certificate in Correct Format (CRITICAL):**
            The certificate content must be **Base64 encoded DER format, WITHOUT PEM headers/footers**.
            To convert a PEM client certificate (e.g., `client.crt`):
            ```bash
            openssl x509 -in client.crt -outform DER | base64 -w0
            ```
            Paste the resulting single line of Base64 text into the `certificate:` field.
    3.  **(Optional) Create `network.yaml` (Static Network Configuration):**
        If omitted, Incus OS attempts DHCP. Example:
        ```yaml
        # network.yaml
        version: "1.0"
        dns:
          hostname: "incus-n97"
        interfaces:
          - name: "br0" 
            hwaddr: "XX:XX:XX:XX:XX:XX" # Physical NIC MAC
            addresses: ["192.168.1.50/24"] 
            routes:
              - to: "0.0.0.0/0" 
                via: "192.168.1.1" 
        ```

*   **Packaging Seed Data and Writing to USB Media:**
    1.  **Create Tarball:** A common name for the tarball in test scripts is `seed.install.tar`.
        ```bash
        tar -cvf seed.install.tar install.yaml incus.yaml # Add network.yaml if used
        ```
    2.  **Write the Seed Tarball to the USB Drive:**
        This uses a specific offset. Build scripts often use an offset of `4196352` with a block size of `512`. This offset, derived from project build scripts, typically places the seed data at the beginning of a dedicated seed partition located after the ESP (often 2GB in size).
        ```bash
        sudo dd if=seed.install.tar of=/dev/sdX seek=4196352 bs=512 conv=notrunc
        ```
        (Replace `/dev/sdX` with your USB device name). `conv=notrunc` is vital.

**V. Phase 3: Incus OS Installation on the Target Host (Intel N97)**

*   **Final UEFI/BIOS Boot Configuration for USB Boot:**
    Ensure the USB drive is the primary boot device, Secure Boot is enabled and in Setup Mode, and TPM 2.0 is enabled.

*   **Booting from USB and Secure Boot Enrollment:**
    The system should boot from the USB. On first boot with Secure Boot in Setup Mode, Incus OS will attempt to enroll its Secure Boot keys. This might involve one or two automatic reboots.

*   **Navigating the Incus OS Installer:**
    A TUI will likely appear. The installer reads the seed data, identifies the target disk, partitions it, and copies OS files automatically. It's expected to handle full-disk encryption (leveraging TPM `2`) and dm-verity `2` automatically.

*   **Installation Process Details:**
    The installer partitions and formats the target disk, copies Incus OS system files, installs the bootloader to the ESP, and configures the base system, potentially interacting with the TPM and enrolling Secure Boot keys.`2`

*   **Completion and Reboot:**
    Upon completion, a message will prompt for media removal (unless `force_reboot: true`). Remove the USB installation drive. Reboot manually if needed.

**VI. Phase 4: First Boot, System Verification, and Initial Incus Setup**

*   **First Boot into Installed Incus OS:**
    (Optional: Enter UEFI/BIOS and set your internal disk as primary boot device). The system boots from the internal disk. `incus-osd` (the Incus OS daemon) starts and applies the seed configuration. If `apply_defaults: true` was set, it initializes ZFS, default Incus networking, and trusts your client certificate. If no `network.yaml` was provided, Incus OS itself attempts DHCP. It may download applications like Incus itself.

*   **Retrieving and Storing Disk Encryption Recovery Key (Vital):**
    The root filesystem is encrypted. Retrieve the recovery key.
    From your remote client (after establishing access):
    ```bash
    incus query my-n97-incus-os:/1.0/system/encryption
    ```
    The JSON output will contain `config.recovery_keys`. **Store these keys securely offline.** A TUI warning on the console may persist until retrieved.

*   **Verifying Incus Remote Access:**
    Find the Incus OS host's IP. From your client machine:
    ```bash
    incus remote add my-n97-incus-os <IP_OF_INCUS_OS_HOST>:8443
    # You will likely be prompted to accept the server's certificate fingerprint.
    incus list my-n97-incus-os:
    ```

*   **Verifying Incus Service Status:**
    `incus-osd` is the Incus OS management daemon, which in turn manages the main `incus` service. Check the status of the primary Incus service (e.g., `incus.service` or `incusd.service` - consult Incus OS documentation for the exact name):
    ```bash
    sudo systemctl status incus.service # Or the appropriate service name
    # Check logs if needed:
    sudo journalctl -u incus.service # Or the appropriate service name
    ```

*   **Initializing the Incus Service (Relationship to Seed):**
    If `apply_defaults: true` was used in `incus.yaml` and the seed was processed successfully, the Incus daemon (storage pools, default network, etc.) should be automatically configured. In this case, running `sudo incus admin init` is generally **not required** for the initial setup.
    The `incus admin init` command is used for:
    *   Manual initial configuration if `apply_defaults: false` was set or if the seed was not used/failed.
    *   Reconfiguring an existing Incus setup.
    *   Advanced or custom setups beyond the seed defaults.
    If needed, `sudo incus admin init` interactively configures clustering, storage pools (ZFS, Btrfs, etc.), network bridges, and remote access settings.

**VII. Phase 5: Extended Verification - Launching Your First Incus Instance**

*   **Listing Available Images:**
    ```bash
    incus image list images: -r my-n97-incus-os
    ```
*   **Launching Test Instances:**
    *   **System Container:** `incus launch images:alpine/edge test-alpine-container -r my-n97-incus-os`
    *   **OCI Container:** `incus launch oci-docker:nginx nginx-oci-test -r my-n97-incus-os`
    *   **Virtual Machine:** `incus launch images:ubuntu/22.04 test-ubuntu-vm --vm -r my-n97-incus-os`
*   **Checking Instance Status:**
    ```bash
    incus list -r my-n97-incus-os
    ```
*   **Accessing Instances:**
    ```bash
    incus exec test-alpine-container -- sh -r my-n97-incus-os
    ```
*   **Basic Network Test from Within an Instance:**
    ```bash
    ping -c 3 google.com
    ```

**VIII. Phase 6: Troubleshooting**

*   **TPM Mandatory:** No TPM 2.0 will lead to failure or a non-functional state.
*   **Secure Boot Setup Mode:** Essential for initial key enrollment.
*   **Seed File Errors:** YAML syntax (indentation) and certificate format (Base64 DER) are common pitfalls.
*   **USB Boot Problems:**
    *   Check BIOS boot order, try boot menu (F7, F10, etc.).`5`
    *   N97 specific: Try setting boot priority options to "disabled" in BIOS.`5`
    *   Recreate USB media, try different tools.
    *   For very large USBs, consider `sgdisk` to relocate backup GPT.
    *   Installer might not clean up USB stick partitions after an install (re-image USB for new attempt).
*   **Image Size Issues:**
    *   USB stick must be large enough (>=64GB recommended due to installer repart behavior).
    *   Target internal disk should be sufficiently large (e.g., 50GB+).
*   **GitHub Rate Limiting:** During first boot, Incus OS might download components. Repeated attempts from the same IP can hit rate limits.
*   **System Overheating (N97 Mini PCs):** Ensure adequate ventilation. Check for BIOS updates for thermal management.`4`
*   **Installer Failures:** Check disk/network connections. Try DHCP if static IP fails. Consult Incus OS release notes.
*   **`incusd` Service Failures:** Check logs. Review seed files or `incus admin init` choices.
*   **Cannot Launch Instances:** Check storage pool, network, image integrity, host resources, instance logs.
*   **BIOS Version Issues:** Outdated BIOS can cause instability.`4, 6` Check manufacturer for updates.

**IX. Phase 7: Conclusion and Next Steps**

Successfully installing and configuring Incus OS on an Intel N97 bare-metal host establishes a robust, secure, and minimal platform for Incus containers and virtual machines.

*   **Pointers for Further Learning:**
    *   **Official Incus Documentation:** The primary resource (typically on `linuxcontainers.org`).
    *   **Community Resources:** Linux Containers Forum,`9` Incus Subreddit.`11`
    *   **Advanced Incus Features:** Profiles, snapshots, device passthrough (utilizing N97's VT-d `1`), clustering,`2` alternative storage backends (Linstor `9`), OCI container management.`2`
    *   **Automation Tools:** `incus-deploy` `2` (Ansible/Terraform scripts), IncusScripts `10` (community scripts).

*   **Maintaining Your Incus OS Deployment:**
    *   **Regular Updates:** Incus OS (via its A/B mechanism) and the Incus package itself (Incus has monthly feature releases and LTS versions `2`).
    *   **System Monitoring:** Host resources and Incus pool usage. Review Incus logs.
    *   **Backup Strategy:** Incus configuration and instance data.