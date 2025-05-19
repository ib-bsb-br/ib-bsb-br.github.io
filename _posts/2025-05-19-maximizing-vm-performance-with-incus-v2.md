---
tags: [scratchpad]
info: aberto.
date: 2025-05-19
type: post
layout: post
published: true
slug: maximizing-vm-performance-with-incus-v2
title: 'Maximizing VM Performance with Incus v2'
---
Incus for Maximum Single VM Performance

**IMPORTANT NOTE:** This guide provides a comprehensive approach to dedicating maximum resources to a single Incus virtual machine. Many values (e.g., `performant-vm`, CPU core lists like `1-7`, memory allocations like `60GiB`, disk paths like `/dev/sdb1`, network interfaces like `enp3s0`) are **examples**. You **MUST** adapt these to your specific hardware, total resources, and virtual machine requirements. Incorrectly applying these settings, especially kernel parameters or PCI passthrough, can lead to system instability or data loss. Proceed with caution and ensure you understand each step.

**I. Ubuntu Server Host Optimizations (The "Lean Hypervisor" Layer)**

The goal is to minimize the host OS's footprint and tune it for optimal resource allocation to the VM.

1.  **Minimal Installation:**
    *   Start with the most minimal Ubuntu Server 25 installation. Avoid desktop environments, graphical tools, or any server roles not strictly required for Incus or essential system management.
    *   During installation, if prompted, deselect optional software bundles. Consider a "netboot" or "minimal ISO" if available.

2.  **Disable Unnecessary Services:**
    *   Audit and disable services that don't contribute to running Incus or the VM.
        ```bash
        sudo systemctl list-unit-files --type=service --state=enabled
        # Example: Disable apport, snapd (if not used for Incus), motd-news
        sudo systemctl stop apport snapd motd-news.timer
        sudo systemctl disable apport snapd motd-news.timer
        ```
    *   Be cautious and ensure you understand a service's role before disabling it.

3.  **Kernel Boot Parameters (GRUB Configuration):**
    *   Modify `/etc/default/grub` and add parameters to `GRUB_CMDLINE_LINUX_DEFAULT`. These significantly impact performance and resource isolation.
        *   **Example for an 8-core CPU (0-7), reserving cores 1-7 for the VM, core 0 for the host:**
            `isolcpus=1-7 nohz_full=1-7 rcu_nocbs=1-7`
        *   **IOMMU (Essential for PCI Passthrough):**
            `intel_iommu=on` (for Intel) or `amd_iommu=on iommu=pt` (for AMD; `iommu=pt` can improve passthrough compatibility).
        *   **CPU P-State Control (for finer frequency management):**
            `intel_pstate=disable` (for Intel, to use `acpi-cpufreq`) or `amd_pstate=passive` (for AMD).
        *   **HugePages (Pre-allocation at boot):**
            `hugepagesz=1G hugepages=30` (Example for 30GB of 1GB pages) or `hugepagesz=2M hugepages=15360` (Example for 30GB of 2MB pages). Adjust `hugepages` count based on VM memory.
        *   **Security vs. Performance (Use with Extreme Caution):**
            `mitigations=off` **SECURITY RISK!** Disables CPU speculative execution mitigations (e.g., Spectre/Meltdown). This can significantly boost performance but makes your system vulnerable. *Only consider this if the machine is in a highly trusted, isolated environment and performance is the absolute priority over security.*
    *   **Combined Example for `GRUB_CMDLINE_LINUX_DEFAULT`:**
        `"quiet splash isolcpus=1-7 nohz_full=1-7 rcu_nocbs=1-7 intel_iommu=on intel_pstate=disable hugepagesz=1G hugepages=30"` (Adapt for your core count, CPU type, and HugePage needs).
    *   After editing `/etc/default/grub`:
        ```bash
        sudo update-grub
        sudo reboot
        ```
    *   **NUMA Consideration:** If your system has multiple NUMA nodes (check with `lscpu`), ensure the cores specified in `isolcpus` belong to the same NUMA node to which you'll also pin the VM's memory and, ideally, passthrough devices.

4.  **CPU Governor and Frequency:**
    *   Set the CPU frequency scaling governor to `performance` for all cores (as host activity on isolated cores will be minimal, and dedicated cores should run at max).
        ```bash
        sudo apt update && sudo apt install -y cpufrequtils
        echo 'GOVERNOR="performance"' | sudo tee /etc/default/cpufrequtils
        sudo systemctl disable ondemand # Or other conservative governors
        sudo systemctl enable --now cpufrequtils
        # Verify: cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
        ```

5.  **Memory: Swappiness and HugePages (Runtime):**
    *   **Swappiness:** Reduce the host's tendency to swap.
        ```bash
        sudo sysctl vm.swappiness=1
        # Make permanent: echo 'vm.swappiness=1' | sudo tee -a /etc/sysctl.conf
        ```
    *   **HugePages (Runtime allocation if not done via kernel params or for adjustment):**
        1.  Determine hugepage size: `cat /proc/meminfo | grep Hugepagesize` (usually 2MB or 1GB)
        2.  Allocate (example for 15360 pages of 2MB size, totaling ~30GB):
            ```bash
            echo 15360 | sudo tee /proc/sys/vm/nr_hugepages
            # Make permanent: echo 'vm.nr_hugepages=15360' | sudo tee -a /etc/sysctl.conf
            # Ensure hugetlbfs is mounted: sudo mount -t hugetlbfs none /dev/hugepages (if not already)
            ```

6.  **Disk I/O Scheduler:**
    *   For NVMe drives, `none` is often best. For SATA SSDs, `mq-deadline` or `kyber`.
        ```bash
        # Check current scheduler for nvme0n1:
        cat /sys/block/nvme0n1/queue/scheduler
        # Set to none for nvme0n1:
        echo none | sudo tee /sys/block/nvme0n1/queue/scheduler
        ```
    *   **Make persistent via udev rules:** Create `/etc/udev/rules.d/60-ioschedulers.rules`:
        ```
        ACTION=="add|change", KERNEL=="nvme[0-9]*n[0-9]*", ATTR{queue/scheduler}="none"
        ACTION=="add|change", KERNEL=="sd[a-z]", ATTR{queue/scheduler}="mq-deadline"
        ```
        Reload rules: `sudo udevadm control --reload-rules && sudo udevadm trigger`

7.  **IRQ Affinity (Advanced):**
    *   Pin interrupts from high-throughput devices (NICs, storage controllers for VM) to host-reserved CPU cores (e.g., core 0 if `isolcpus=1-7`).
        1.  Identify device IRQs: `cat /proc/interrupts`
        2.  Disable `irqbalance` service: `sudo systemctl disable --now irqbalance`
        3.  Manually set affinity (e.g., pin IRQ `<irq_num>` to CPU0, mask is `1`):
            `echo 1 | sudo tee /proc/irq/<irq_num>/smp_affinity` (Replace `<irq_num>`)

8.  **BIOS/UEFI Settings:**
    *   Enable virtualization technologies: Intel VT-x, AMD-V.
    *   Enable IOMMU: Intel VT-d, AMD IOMMU/Vi.
    *   Disable aggressive power-saving features (deep C-states beyond C1/C2, BIOS-controlled frequency scaling if it interferes with OS control). Set power profiles to "Maximum Performance" or "OS Controlled."
    *   Disable unused integrated peripherals (serial ports, audio).
    *   For NUMA systems: Ensure settings promote locality (e.g., memory interleaving might be "NUMA-aware" or "channel specific").

9.  **Consider `tuned` Utility:**
    *   `tuned` can apply system-wide tuning profiles.
        ```bash
        sudo apt install -y tuned
        sudo tuned-adm profile virtual-host
        ```
    *   Review the profile and customize further if needed. Manual settings above might override or complement `tuned`.

**II. Incus Virtual Machine Configuration (Maximizing Resource Allocation)**

Configure the Incus VM (`performant-vm` in examples) to claim and efficiently use resources.

1.  **CPU Allocation, Pinning, and Model:**
    *   **`limits.cpu`**: Assign specific isolated host physical cores (e.g., host cores 1-7).
        ```bash
        incus config set performant-vm limits.cpu 1-7
        ```
    *   **`limits.cpu.allowance`**: Ensure 100% usage of assigned cores.
        ```bash
        incus config set performant-vm limits.cpu.allowance 100%
        ```
    *   **`limits.cpu.priority`**: Higher priority for VM tasks.
        ```bash
        incus config set performant-vm limits.cpu.priority 10
        ```
    *   **CPU Model Passthrough (Expose Host CPU Features):**
        ```bash
        incus config set performant-vm security.guest.features.cpu.host_passthrough=true
        ```
    *   **NUMA Pinning (If host cores 1-7 are on NUMA node 0):**
        ```bash
        incus config set performant-vm limits.cpu.nodes 0
        ```

2.  **Memory Allocation:**
    *   **`limits.memory`**: Allocate desired RAM (e.g., 60GiB for a 64GB system, leaving 4GB for host).
        ```bash
        incus config set performant-vm limits.memory 60GiB
        ```
    *   **`limits.memory.hugepages`**: Enable VM to use host-configured HugePages.
        ```bash
        incus config set performant-vm limits.memory.hugepages true
        ```
        Ensure `limits.memory` is a multiple of the hugepage size.
    *   **`limits.memory.enforce`**: Ensure VM gets its allocated memory.
        ```bash
        incus config set performant-vm limits.memory.enforce hard
        ```
    *   **NUMA Pinning (Pin memory to the same NUMA node as CPUs, e.g., node 0):**
        ```bash
        incus config set performant-vm limits.memory.nodes 0
        ```

3.  **Disk I/O Performance:**
    *   **Storage Backend:**
        *   **Direct Block Device Passthrough (Recommended for single disk performance):**
            ```bash
            # Example: Pass through /dev/sdb1 as the VM's root disk
            incus config device add performant-vm rootdisk disk source=/dev/sdb1 path=/
            ```
        *   **Or, LVM/ZFS Pool (Flexible, good for SSD/NVMe):**
            ```bash
            # Assuming 'mypool' is an existing LVM or ZFS storage pool on a fast device
            # incus storage volume create mypool vm_root_disk --type=block size=100GiB
            # incus config device add performant-vm rootdisk disk pool=mypool source=vm_root_disk path=/
            # For ZFS, consider pool/dataset tuning: atime=off, recordsize=128k (or match workload)
            # zfs set recordsize=128k mypool/virtual-machines/performant-vm.block # Example
            # zfs set atime=off mypool/virtual-machines/performant-vm.block # Example
            ```
    *   **Disk Cache Options for the device:**
        ```bash
        incus config device set performant-vm rootdisk cache none
        ```
    *   **I/O Mode:**
        ```bash
        incus config device set performant-vm rootdisk io writethrough
        # Modern QEMU often defaults well. `io_uring` is preferred if host kernel & QEMU support it;
        # Incus may enable this automatically or via raw.qemu if needed for specific tuning.
        ```
    *   Ensure the VM uses `virtio-blk` or `virtio-scsi` (usually default).

4.  **Network I/O Performance:**
    *   **PCI Passthrough (SR-IOV or Full NIC for best performance):**
        1.  Identify NIC PCI address: `lspci -nnk | grep -i ethernet`
        2.  (If SR-IOV) Create Virtual Function (VF) on the host.
        3.  Add to Incus VM (replace `enp3s0f0` with your host physical NIC or VF name):
            ```bash
            incus config device add performant-vm eth0 nic nictype=physical parent=enp3s0f0
            ```
    *   **`macvtap` (Good performance if PCI passthrough isn't feasible):**
        ```bash
        # Replace enp2s0 with your host physical interface
        incus config device add performant-vm eth0 nic nictype=macvtap parent=enp2s0 mode=bridge
        ```
        (`mode=bridge` allows host-guest communication. `private` or `vepa` modes restrict this).
    *   **Multi-Queue `virtio-net` (N = number of vCPUs, or power of 2):**
        ```bash
        incus config device set performant-vm eth0 queues.rx 4
        incus config device set performant-vm eth0 queues.tx 4
        # Or if your Incus version supports a combined key:
        # incus config device set performant-vm eth0 queues 4
        ```

5.  **Guest OS Considerations:**
    *   Install `qemu-guest-agent` inside the VM for better integration (shutdown, time sync, etc.).
        *   Debian/Ubuntu guests: `sudo apt install qemu-guest-agent`
        *   RHEL/CentOS guests: `sudo yum install qemu-guest-agent`
    *   Ensure the guest OS uses virtio drivers for disk, network, etc. (standard for modern Linux).

6.  **Disable Unused Virtual Hardware:**
    *   Review `incus config show performant-vm --expanded`.
    *   If a USB tablet or other unneeded devices are present by default, consider removing them if not used:
        ```bash
        # incus config device remove performant-vm <device_name_from_expanded_config>
        ```

7.  **`raw.qemu` (Use Sparingly for Advanced QEMU Options):**
    *   For QEMU options not directly exposed by Incus. This is for advanced users.
        ```bash
        # Example: incus config set performant-vm raw.qemu "-some-qemu-option value"
        ```

**III. Verification and Monitoring**

1.  **Host Verification:**
    *   Kernel parameters applied: `cat /proc/cmdline`
    *   CPU topology/NUMA: `lscpu`
    *   HugePages status: `cat /proc/meminfo | grep -i huge`
    *   QEMU process affinity (find PID of `performant-vm`'s QEMU process with `ps aux | grep qemu` or `incus info performant-vm --resources`): `taskset -cp <qemu_pid>` (should show affinity to isolated cores).
    *   I/O scheduler for devices: `cat /sys/block/nvme0n1/queue/scheduler`

2.  **Incus Verification:**
    *   Full VM configuration: `incus config show performant-vm --expanded`
    *   VM status and resources: `incus info performant-vm` and `incus info performant-vm --resources`

3.  **Guest Verification (Inside the VM):**
    *   CPU info: `lscpu`
    *   Memory: `free -h`, `cat /proc/meminfo | grep -i huge` (to see if guest is using hugepages from host)
    *   Kernel messages for hardware/driver info: `dmesg`
    *   Run relevant benchmarks (disk: `fio`; network: `iperf3`; CPU: `sysbench`, Phoronix Test Suite).

4.  **Continuous Monitoring:**
    *   **Host:** `htop` (observe CPU usage on isolated vs. host cores), `vmstat`, `iostat`, `perf top` (for deep dives).
    *   **Incus:** `incus top` (for Incus-specific metrics).

**IV. General Workflow & Considerations**

*   **Iterate and Benchmark:** Performance tuning is often iterative. Change one major setting at a time and benchmark to observe its impact. What works best can be workload-dependent.
*   **Stability is Paramount:** While aiming for maximum performance, ensure the host and VM remain stable. An unstable host means an unstable VM.
*   **Documentation:** Document your specific changes and system configuration.
*   **Recovery Plan:** Before major GRUB or system config changes, ensure you have a way to recover (e.g., bootable USB, familiarity with recovery mode).
*   **Incus Documentation:** Specific commands and configuration keys can evolve. Always refer to the official Incus documentation for your version if you encounter discrepancies or need more detail.

By systematically applying these optimizations, you can significantly reduce overhead from both Ubuntu Server and Incus, allowing your primary virtual machine (`performant-vm`) to utilize the maximum available hardware resources and achieve performance much closer to bare-metal.