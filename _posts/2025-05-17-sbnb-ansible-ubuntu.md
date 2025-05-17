---
tags: [scratchpad]
info: aberto.
date: 2025-05-17
type: post
layout: post
published: true
slug: sbnb-ansible-ubuntu
title: 'SBNB linux within Ubuntu Ansible Playbook'
---
1.  **Python 3 Installation:** This playbook assumes the target Ubuntu 24.04 machine has Python 3 installed. Ansible is written in Python, and its modules are executed on the managed node (even if it’s `localhost`) using the system’s Python interpreter. Ubuntu 24.04 server typically includes Python 3 by default.
2.  **Provided Raw OS Image:** The bootable raw operating system image (e.g., created by mkosi or similar tools) MUST be present at the location specified by `provided_raw_image_path` (default: `/root/IncusOS.raw`) on the target machine. This image should contain a complete filesystem ready to be booted.
3.  **Provided Incus Metadata Archive:** An Incus metadata archive (typically `metadata.tar.xz`) MUST be present at the location specified by `provided_metadata_path` (default: `/root/metadata.tar.xz`) on the target machine. This file describes the image properties to Incus, such as architecture, creation date, and OS details, which are crucial for `incus image import`. (Alternatively, a `metadata.yaml` file can sometimes be used, depending on how the image and metadata were originally packaged, though this playbook assumes `metadata.tar.xz` as per the original context).

—
- name: Setup Incus and Start VM from Provided Image
  hosts: localhost * Designed to be run directly on the target bare-metal Ubuntu 24.04.
                   * Change to your specific host or group name if targeting remote machines.
  connection: local * Uses the local connection plugin as we are targeting the machine Ansible is run on.
                    * Change to ‘ssh’ if connecting to remote hosts.
  become: yes * Most tasks require elevated (sudo) privileges for system-level changes like package
              * installation, Incus setup, and managing files in /root.
  vars:
    * Path on the target machine where the pre-existing raw OS image is located.
    * The /root/ path is used as an example assuming the image is placed there with root ownership.
    * Adjust if your image is located elsewhere and ensure appropriate read permissions for Ansible.
    provided_raw_image_path: “/root/IncusOS.raw”

    * Path on the target machine where the Incus metadata archive (e.g., metadata.tar.xz) is located.
    * This file is required by `incus image import` to understand the properties of the image.
    provided_metadata_path: “/root/metadata.tar.xz”

    * Temporary path where the .raw image will be converted to .qcow2 format before import.
    * This path should be writable by the user/process performing the qemu-img conversion.
    * Using /root/ here as other critical files are also assumed to be there.
    converted_qcow2_image_path: “/root/os-image.qcow2”

  tasks:
    - name: Check if provided IncusOS.raw image exists on target
      ansible.builtin.stat:
        path: “{{ provided_raw_image_path }}”
      register: raw_image_stat * Registers the result of the stat command into this variable.

    - name: Fail if IncusOS.raw image does not exist
      ansible.builtin.fail:
        msg: “Prerequisite failed: The raw image {{ provided_raw_image_path }} does not exist on the target machine! Please ensure it is present before running this playbook.”
      when: not raw_image_stat.stat.exists * Fails if the ‘exists’ attribute from stat is false.

    - name: Check if provided metadata.tar.xz exists on target
      ansible.builtin.stat:
        path: “{{ provided_metadata_path }}”
      register: metadata_stat

    - name: Fail if metadata.tar.xz does not exist
      ansible.builtin.fail:
        msg: “Prerequisite failed: The metadata archive {{ provided_metadata_path }} does not exist on the target machine! This is required for Incus image import.”
      when: not metadata_stat.stat.exists

    - name: Install essential system dependencies for Incus and image management
      ansible.builtin.apt:
        name:
          * binutils: Provides a collection of binary tools, including ‘ar’, ‘nm’, ‘objdump’, etc.
          *           While not directly used by every step here, it’s a common foundational package.
          - binutils
          * debian-archive-keyring: Contains GPG keys for verifying Debian/Ubuntu archive signatures.
          *                         Ensures authenticity of packages downloaded by apt.
          - debian-archive-keyring
          * qemu-utils: Provides the ‘qemu-img’ utility, which is essential for converting disk image
          *             formats (e.g., from .raw to .qcow2).
          - qemu-utils
          * Note: Incus itself, when installed via the Zabbly script, will pull in its own direct
          * dependencies such as liblxc, bridge-utils, etc.
        state: present * Ensures these packages are installed.
        update_cache: true * Runs ‘apt-get update’ before attempting to install packages.

    - name: Setup Incus (Install and Initialize)
      block: * Groups related tasks for better organization and error handling if needed.
        - name: Check if Incus command is already available
          ansible.builtin.command: incus —version
          register: incus_check * Stores the command’s output, including return code (rc).
          changed_when: false * This task doesn’t change system state, it’s a check.
          failed_when: false * Do not fail the playbook if incus is not found; we’ll install it.

        - name: Download and run Incus installation script (if Incus not found)
          ansible.builtin.shell: * Using shell module for commands involving pipes.
            * This command downloads the Zabbly script for Incus daily builds and executes it with sudo bash.
            * The Zabbly script typically adds a PPA/repository and installs the Incus package.
            cmd: “curl -s https://pkgs.zabbly.com/get/incus-daily | sudo bash”
            warn: false * Suppresses Ansible warnings about using shell for commands like curl.
          when: incus_check.rc != 0 * Only execute if the ‘incus —version’ command failed (rc != 0).

        - name: Check if Incus has been initialized
          ansible.builtin.command: incus profile show default
          * A successfully initialized Incus instance will have a ‘default’ profile.
          * If this command fails, it’s a strong indicator that `incus admin init` hasn’t completed.
          register: incus_init_check_before * Register before potential init
          changed_when: false
          failed_when: false * Don’t fail; use rc to decide if init is needed.

        - name: Initialize Incus daemon using auto configuration (if not already initialized)
          ansible.builtin.command: incus admin init —auto
          * The ‘—auto’ flag configures Incus with sensible defaults. This typically includes:
          * - A default storage pool (e.g., ZFS on a loop device if zfsutils-linux is installed,
          *   or a directory-based pool at /var/lib/incus/storage-pools/default otherwise).
          * - A default network bridge (e.g., `incusbr0`) providing NATed internet access to instances.
          * - Sets up the server for immediate use. For more granular control over storage or networking,
          *   `incus admin init` can be run interactively.
          when: incus_init_check_before.rc != 0 * Only run if the ‘incus profile show default’ command failed.
          changed_when: true * This command inherently changes system state if it runs the initialization.

        - name: Check if Incus socket exists after potential initialization
          ansible.builtin.stat:
            path: /var/lib/incus/unix.socket
          register: incus_socket_stat_after_init

        - name: Ensure Incus socket has 0666 permissions (replicating GHA behavior)
          ansible.builtin.file:
            path: /var/lib/incus/unix.socket
            mode: ‘0666’ * Sets read/write for owner, group, and others.
          * This task runs with ‘become: yes’ due to the play-level setting.
          * The original GHA workflow used ‘sudo chmod 666’.
          * Note: While `0666` permissions replicate the original workflow’s behavior, this is highly
          * permissive. In production environments, it’s strongly recommended to manage access to the
          * Incus socket via group membership (e.g., adding trusted users to the `incus` or `incus-admin`
          * group, which `incus admin init` might help configure or which can be done manually)
          * rather than world-writable permissions.
          when: incus_socket_stat_after_init.stat.exists and (incus_socket_stat_after_init.stat.issock or incus_socket_stat_after_init.stat.islnk)
          * The condition ensures the chmod is only attempted if the socket (or a symlink to it) exists.

    - name: Prepare and Import Provided Incus Image
      block:
        - name: Convert provided .raw image to .qcow2 format
          ansible.builtin.command:
            * qemu-img convert: Utility to convert disk images between formats.
            * -f raw: Specifies the source image format is raw.
            * -O qcow2: Specifies the output image format is QCOW2 (QEMU Copy On Write 2).
            * QCOW2 is a common format for VMs, supporting features like snapshots, thin provisioning,
            * and potentially better performance for some workloads compared to raw images.
            cmd: “qemu-img convert -f raw -O qcow2 {{ provided_raw_image_path }} {{ converted_qcow2_image_path }}”
          changed_when: true * This command creates or overwrites the output qcow2 file.

        - name: Import converted qcow2 image into Incus
          ansible.builtin.command:
            * incus image import: Command to import an image into the Incus image store.
            * —alias incus-os: Assigns an alias ‘incus-os’ to the imported image for easy reference later.
            * {{ provided_metadata_path }}: Path to the metadata archive (e.g., metadata.tar.xz).
            * {{ converted_qcow2_image_path }}: Path to the root filesystem image (now in qcow2 format).
            * If an image with the same alias or fingerprint already exists, this command might error
            * or behave differently based on Incus version. This playbook assumes a fresh import.
            cmd: “incus image import —alias incus-os {{ provided_metadata_path }} {{ converted_qcow2_image_path }}”
          changed_when: true * This command adds a new image to the Incus store.

    - name: Create and Start Incus Virtual Machine
      block:
        - name: Create Incus VM ‘test-incus-os’ from the imported image
          ansible.builtin.command:
            cmd: >
              incus create —quiet —vm incus-os test-incus-os
              -c security.secureboot=false
              -c limits.cpu=2
              -c limits.memory=2GiB
              -d root,size=50GiB
            * —quiet: Suppresses progress output.
            * —vm: Specifies that a virtual machine (not a container) should be created.
            * incus-os: Alias of the image to use (imported in the previous step).
            * test-incus-os: Name for the new VM instance.
            * Configuration options (-c key=value):
            *   security.secureboot=false: Disables Secure Boot for the VM. This is often necessary for
            *                            custom-built or generic images that may not have signed bootloaders
            *                            compatible with the host’s Secure Boot validation.
            *   limits.cpu=2: Allocates a maximum of 2 CPU cores to the VM.
            *   limits.memory=2GiB: Allocates 2 GiB of RAM to the VM.
            * Device options (-d device,properties):
            *   root,size=50GiB: Configures the root disk device, ensuring it has a size of 50 GiB.
            *                    Incus will typically expand the image’s filesystem to fill this size.
          changed_when: true * This command creates a new VM instance.

        - name: Add virtual TPM (Trusted Platform Module) device to ‘test-incus-os’
          ansible.builtin.command:
            cmd: incus config device add test-incus-os vtpm tpm
            * This adds a software-emulated TPM (vTPM) device named ‘vtpm’ of type ‘tpm’ to the VM.
            * A vTPM can be utilized by the guest OS for features like full-disk encryption (e.g., BitLocker, LUKS),
            * measured boot, or other security functionalities that rely on a TPM.
          changed_when: true * This command modifies the VM’s configuration.

        - name: Start the ‘test-incus-os’ VM
          ansible.builtin.command:
            cmd: incus start test-incus-os
          changed_when: true * This command changes the state of the VM to running.

        - name: Wait for the VM to become responsive
          ansible.builtin.command:
            * incus exec <vm_name> — <command>: Executes a command inside the specified VM.
            * /usr/bin/true: A simple command that does nothing and exits with status 0 if successful.
            * This is a common and lightweight way to check if the VM’s OS has booted sufficiently
            * to allow command execution via Incus.
            cmd: incus exec test-incus-os — /usr/bin/true
          register: vm_status * Stores the result of the command.
          until: vm_status.rc == 0 * Loop until the command executes successfully (return code 0).
          retries: 20 * Maximum number of retries.
          delay: 3 * Wait 3 seconds between retries (total wait time up to 60 seconds).
          changed_when: false * This task only checks status, doesn’t change system state.

        - name: Additional pause (1 minute) as per original workflow logic
          ansible.builtin.pause:
            minutes: 1
            * This pause might have been included in the original workflow to allow services
            * or applications inside the newly started VM to fully initialize before proceeding
            * with further tests or operations that might depend on those internal services.
          when: vm_status.rc == 0 * Only pause if the VM became responsive.

        - name: List Incus instances for final verification
          ansible.builtin.command: incus list
          register: incus_list_output
          changed_when: false

        - name: Display current Incus instances
          ansible.builtin.debug:
            var: incus_list_output.stdout_lines * Shows the standard output of ‘incus list’.

    - name: Cleanup temporary qcow2 image (optional step)
      ansible.builtin.file:
        path: “{{ converted_qcow2_image_path }}”
        state: absent * Ensures the file is removed.
      * This step is useful to free up disk space if the converted qcow2 image is no longer needed
      * after being imported into Incus’s storage pool (Incus makes its own copy).
      when: true * Set to ‘false’ or remove this task if you want to keep the qcow2 image for debugging.
      tags:
        - cleanup * Allows skipping this task with —skip-tags cleanup or running only it with —tags cleanup.
```

**Explanation of How to Use (Expanded):**

1.  **Save the Playbook:** Save the content above into a file named, for example, `setup_incus_from_provided_image.yml` on the machine you’ll use to run Ansible (this could be the target Ubuntu 24.04 machine itself if `connection: local`).

2.  **Prepare Prerequisites on the Target Ubuntu 24.04 Machine:**
    *   **Python 3:** Ensure Python 3 is installed. For Ubuntu 24.04 Server, it’s typically present. You can check with `python3 —version`. If missing (unlikely for a server OS), install it: `sudo apt update && sudo apt install python3`.
    *   **Raw OS Image:** Place your bootable raw OS image (e.g., `IncusOS.raw`) at the exact path specified in the `provided_raw_image_path` variable (default: `/root/IncusOS.raw`). Ensure this file is readable by the root user (as the playbook uses `become: yes`).
    *   **Incus Metadata Archive:** Place the corresponding Incus metadata archive (e.g., `metadata.tar.xz` or potentially a `metadata.yaml`) at the path specified in `provided_metadata_path` (default: `/root/metadata.tar.xz`). This file is crucial for Incus to understand the image’s properties.

3.  **Install Ansible on the Control Machine (or Target if running locally):**
    *   If you are running the playbook directly on the target Ubuntu 24.04 machine (using `connection: local`), install Ansible on it:
        ```bash
        sudo apt update && sudo apt install -y ansible
        ```
    *   If you are running Ansible from a separate control node to manage the Ubuntu 24.04 machine remotely, ensure Ansible is installed on your control node.

4.  **Run the Ansible Playbook:**
    *   **Locally on the Target Machine:**
        Navigate to the directory where you saved `setup_incus_from_provided_image.yml` and run:
        ```bash
        sudo ansible-playbook setup_incus_from_provided_image.yml
        ```
        You generally need `sudo` when using `connection: local` and `become: yes` because:
        a.  The playbook performs privileged operations (package installs, service management, file operations in `/root`).
        b.  `connection: local` means Ansible uses the privileges of the user executing `ansible-playbook`. If that user is not root, `become` will attempt to use `sudo` to elevate privileges.
        If your regular user has passwordless `sudo` configured for all necessary commands, you might be able to run it without the `sudo` prefix, and Ansible’s `become` mechanism will handle the elevation.
    *   **From a Remote Ansible Control Node:**
        If you’ve configured `hosts` in the playbook to point to your remote Ubuntu 24.04 machine (e.g., `myubuntuserver`) and have an Ansible inventory file (`your_inventory_file`) set up with SSH access to the target:
        ```bash
        ansible-playbook -i your_inventory_file setup_incus_from_provided_image.yml
        ```
        Ensure the user specified in your inventory for the target host (e.g., `ansible_user=your_ssh_user`) has `sudo` privileges, as `become: yes` will be used on the remote host.

5.  **Useful Ansible Playbook Flags:**
    *   **Dry Run (Check Mode):** To see what changes Ansible *would* make without actually executing them. This is highly recommended before running a new playbook for the first time.
        ```bash
        sudo ansible-playbook setup_incus_from_provided_image.yml —check
        ```
    *   **Show Differences:** To see the exact changes that would be made to files (useful with or without `—check`). This helps understand what content is being modified.
        ```bash
        sudo ansible-playbook setup_incus_from_provided_image.yml —diff
        ```
    *   **Verbosity:** Increase verbosity for more detailed output, which can be helpful for troubleshooting (e.g., `-v` for basic, `-vv` for more detail, `-vvv` for connection debug, `-vvvv` for even more).
        ```bash
        sudo ansible-playbook setup_incus_from_provided_image.yml -vv
        ```
    *   **Tags:** To run or skip specific parts of the playbook. For example, to skip the cleanup task:
        ```bash
        sudo ansible-playbook setup_incus_from_provided_image.yml —skip-tags cleanup
        ```
        Or to run *only* the cleanup task (assuming other tasks have completed successfully before):
        ```bash
        sudo ansible-playbook setup_incus_from_provided_image.yml —tags cleanup
        ```

6.  **Troubleshooting Incus:**
    *   If you encounter issues with Incus services not starting correctly or VM misbehavior, checking the Incus daemon logs is a good first step:
        ```bash
        sudo journalctl -u incus.service -n 100 —no-pager
        ```
    *   For issues specific to an instance after it’s created:
        ```bash
        incus info test-incus-os —show-log
        ```
    *   You can also try to access the console of the VM:
        ```bash
        incus console test-incus-os —type=pty
        ```

**Summary of Key Changes and Simplifications (Expanded):**

*   **No Build Process:** The most significant characteristic of this playbook is the complete removal of tasks related to source code checkout (Git), Go language setup, `pipx` and `mkosi` installation, and the `make` command for building the OS image. This is because the core assumption now is that `IncusOS.raw` is pre-built and provided directly on the target system.
*   **Direct Image Usage:** The playbook now directly consumes the user-provided `/root/IncusOS.raw` and an associated `/root/metadata.tar.xz` (or `metadata.yaml` if adapted). This makes the playbook much simpler if an image generation pipeline already exists separately.
*   **Simplified Dependencies:** The list of system packages installed via `apt` is reduced to only those essential for image conversion (`qemu-utils`) and general system health/repository access (`binutils`, `debian-archive-keyring`), as Incus’s own installation script (from Zabbly) handles its specific dependencies like `liblxc1`, `squashfs-tools`, etc.
*   **Focus on Incus Setup and VM Lifecycle:** The playbook’s primary operational focus shifts to robustly installing and initializing Incus, converting the provided raw image to the `qcow2` format (which offers benefits like thin provisioning and snapshot capabilities), importing this image into the Incus image store with a clear alias, and then proceeding with VM creation, specific configuration (like adding a vTPM for enhanced guest security), startup, and responsiveness checks.
*   **Prerequisite Validation:** Explicit `ansible.builtin.stat` tasks are included at the beginning to verify the existence of the crucial `IncusOS.raw` and `metadata.tar.xz` files. The playbook will fail early with a clear message if these prerequisites are not met, which significantly improves usability and aids in rapid error diagnosis.
*   **Variable Simplification:** The `vars` section is streamlined, primarily defining the paths to the pre-existing image and metadata files, making it easy for the user to configure these critical inputs.
*   **Optional Cleanup:** A tagged task for cleaning up the intermediate `os-image.qcow2` file is included. This is good practice as Incus makes its own copy of the image in its storage pool, so the temporary qcow2 file may no longer be needed and can be removed to save disk space. The use of tags gives the user fine-grained control over this step.
