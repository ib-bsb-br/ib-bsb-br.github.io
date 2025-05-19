---
tags: [scratchpad]
info: aberto.
date: 2025-05-19
type: post
layout: post
published: true
slug: maximizing-vm-performance-with-incus-v1
title: 'Maximizing VM Performance with Incus v1'
---
## Quick Reference Guide

This comprehensive guide helps you configure Ubuntu Server 25 and Incus to achieve near-bare-metal performance for a single virtual machine. Follow these steps systematically, testing after each major change.

**Key Performance Factors:**
- CPU isolation and pinning
- Memory allocation and hugepages
- Storage optimization
- Network configuration
- Host OS minimization

**Prerequisites:**
- Ubuntu Server 25 installed
- Administrative (sudo) access
- Basic understanding of Linux system administration
- Hardware with virtualization support (Intel VT-x/AMD-V)
- Backup of any important data

## I. Pre-Implementation Planning

### 1. Hardware Assessment

Before beginning optimizations, assess your hardware capabilities:

```bash
# Check CPU information
lscpu

# Check virtualization support
egrep -c '(vmx|svm)' /proc/cpuinfo  # Should return > 0

# Check IOMMU support (for PCI passthrough)
dmesg | grep -e DMAR -e IOMMU

# Check memory
free -h

# Check storage devices
lsblk -o NAME,SIZE,MODEL,ROTA
```

### 2. Workload Requirements Analysis

Different workloads have different optimization priorities:
- **CPU-intensive workloads**: Focus on CPU isolation and frequency scaling
- **Memory-intensive workloads**: Prioritize hugepages and NUMA optimization
- **I/O-intensive workloads**: Focus on storage and network passthrough
- **Graphics-intensive workloads**: Prioritize GPU passthrough

### 3. Risk Assessment

| Optimization | Performance Benefit | Security Impact | Stability Risk |
|--------------|---------------------|-----------------|----------------|
| CPU isolation | High | Low | Low |
| Disabling CPU mitigations | High | High | Low |
| Hugepages | Medium | Low | Low |
| PCI passthrough | High | Medium | Medium |
| Service disabling | Low | Varies | Medium |

## II. Ubuntu Server Host Optimizations

### 1. Minimal Installation and Service Optimization

Start with the most minimal Ubuntu Server 25 installation:

```bash
# List all enabled services
sudo systemctl list-unit-files --type=service --state=enabled

# Identify non-essential services (examples below)
# - snapd (if not using snaps for Incus)
# - apport (automated crash reporting)
# - motd-news (message of the day updates)
# - unattended-upgrades (if you prefer manual updates)

# Disable non-essential services (example)
sudo systemctl stop snapd.service
sudo systemctl disable snapd.service

# Verify service is disabled
systemctl is-enabled snapd.service  # Should return "disabled"
```

**CAUTION**: Do not disable these essential services:
- systemd-journald
- systemd-logind
- ssh (if you need remote access)
- networking/NetworkManager
- incus-related services

### 2. Firmware and Microcode Updates

Ensure your system firmware and CPU microcode are up-to-date:

```bash
# Install firmware update tools
sudo apt update
sudo apt install -y fwupd intel-microcode  # For Intel CPUs
# OR
sudo apt install -y fwupd amd64-microcode  # For AMD CPUs

# Check for and apply firmware updates
sudo fwupdmgr refresh
sudo fwupdmgr get-updates
sudo fwupdmgr update

# Verify microcode is loaded
dmesg | grep microcode
```

### 3. BIOS/UEFI Configuration

Access your system's BIOS/UEFI settings and configure:

1. **Enable virtualization technologies**:
   - Intel: VT-x, VT-d
   - AMD: AMD-V, AMD-Vi/IOMMU

2. **Disable power-saving features**:
   - C-states beyond C1/C2
   - P-states (or set to OS control)
   - Set power profile to "Performance" or "High Performance"

3. **Memory settings**:
   - Disable memory power saving
   - For NUMA systems: Set appropriate memory interleaving mode

4. **Disable unused devices**:
   - Audio controllers (if not needed)
   - Serial/parallel ports
   - Unused SATA/PCIe controllers

### 4. Kernel Boot Parameters

Modify GRUB configuration to optimize the kernel:

```bash
# Edit GRUB configuration
sudo nano /etc/default/grub

# Identify your CPU cores
lscpu

# Determine cores to reserve for host vs. VM
# Example: On an 8-core system (0-7), reserve cores 0-1 for host, 2-7 for VM
```

Add these parameters to `GRUB_CMDLINE_LINUX_DEFAULT`:

```
# For Intel CPUs:
isolcpus=2-7 nohz_full=2-7 rcu_nocbs=2-7 intel_iommu=on iommu=pt

# For AMD CPUs:
isolcpus=2-7 nohz_full=2-7 rcu_nocbs=2-7 amd_iommu=on iommu=pt
```

**Parameter Explanation**:
- `isolcpus=2-7`: Prevents the kernel scheduler from using these cores for general tasks
- `nohz_full=2-7`: Reduces timer interrupts on isolated cores
- `rcu_nocbs=2-7`: Offloads RCU callbacks from isolated cores
- `intel_iommu=on`/`amd_iommu=on`: Enables IOMMU for device passthrough
- `iommu=pt`: Optimizes IOMMU for passthrough performance

**Optional Performance Parameters** (with security implications):
```
# SECURITY RISK - only use in trusted environments:
mitigations=off
```

Apply changes and verify:

```bash
# Update GRUB
sudo update-grub

# Reboot
sudo reboot

# Verify parameters are applied
cat /proc/cmdline
```

### 5. CPU Frequency Scaling

Configure CPU governor for maximum performance:

```bash
# Install CPU frequency utilities
sudo apt update && sudo apt install -y cpufrequtils

# Set performance governor
echo 'GOVERNOR="performance"' | sudo tee /etc/default/cpufrequtils

# Disable ondemand service (conflicts with performance governor)
sudo systemctl disable --now ondemand

# Enable cpufrequtils service
sudo systemctl enable --now cpufrequtils

# Verify settings (should show "performance" for all CPUs)
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

For Intel CPUs with `intel_pstate` driver:

```bash
# Check if using intel_pstate
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_driver

# If using intel_pstate, set performance mode
echo performance | sudo tee /sys/devices/system/cpu/intel_pstate/status
```

### 6. Memory Optimization: Swappiness and Hugepages

#### 6.1 Reduce Swappiness

```bash
# Set swappiness to minimum
sudo sysctl vm.swappiness=1

# Make permanent
echo 'vm.swappiness=1' | sudo tee -a /etc/sysctl.conf

# Verify setting
cat /proc/sys/vm/swappiness  # Should return 1
```

#### 6.2 Configure Hugepages

First, determine your hugepage size and VM memory requirements:

```bash
# Check hugepage size
cat /proc/meminfo | grep Hugepagesize  # Usually 2048 kB (2MB)

# Calculate number of hugepages needed
# Formula: (VM_RAM_in_GB * 1024 + overhead_MB) / hugepage_size_in_MB
# Example for 60GB VM with 2MB pages: (60*1024 + 512) / 2 = 30976
```

Configure hugepages:

```bash
# For 2MB pages (temporary setting)
echo 30976 | sudo tee /proc/sys/vm/nr_hugepages

# Make permanent
echo 'vm.nr_hugepages = 30976' | sudo tee -a /etc/sysctl.conf

# Alternative: Configure via GRUB for 1GB pages
# Add to GRUB_CMDLINE_LINUX_DEFAULT: hugepagesz=1G hugepages=62

# Verify hugepages allocation
cat /proc/meminfo | grep -i huge
```

**Note**: If hugepages allocation fails, try:
1. Allocating fewer pages
2. Rebooting and allocating before memory fragmentation occurs
3. Adding slightly more than needed to account for system usage

### 7. Disk I/O Optimization

#### 7.1 Choose Optimal I/O Scheduler

```bash
# Identify your storage devices
lsblk -d -o NAME,ROTA,MODEL

# Check current scheduler
cat /sys/block/nvme0n1/queue/scheduler  # For NVMe
# OR
cat /sys/block/sda/queue/scheduler  # For SATA

# Set optimal scheduler
# For NVMe:
echo none | sudo tee /sys/block/nvme0n1/queue/scheduler

# For SATA SSD:
echo mq-deadline | sudo tee /sys/block/sda/queue/scheduler

# For SATA HDD:
echo bfq | sudo tee /sys/block/sda/queue/scheduler
```

Make changes persistent:

```bash
# Create udev rules file
sudo nano /etc/udev/rules.d/60-scheduler.rules

# Add these lines (adjust device patterns as needed)
ACTION=="add|change", KERNEL=="sd[a-z]", ATTR{queue/rotational}=="0", ATTR{queue/scheduler}="mq-deadline"
ACTION=="add|change", KERNEL=="sd[a-z]", ATTR{queue/rotational}=="1", ATTR{queue/scheduler}="bfq"
ACTION=="add|change", KERNEL=="nvme[0-9]*", ATTR{queue/scheduler}="none"
```

#### 7.2 Additional Storage Optimizations

```bash
# Disable disk barriers if using battery-backed cache
# CAUTION: Data loss risk if power failure occurs without proper battery backup
sudo mount -o remount,nobarrier /mount/point  # Only for specific filesystems

# Increase read-ahead for sequential workloads (example for nvme0n1)
sudo blockdev --setra 4096 /dev/nvme0n1
```

### 8. IRQ Affinity

Properly configure IRQ affinity to prevent interrupts from impacting VM performance:

```bash
# Install tools
sudo apt install -y irqbalance

# Disable irqbalance service (we'll manually configure IRQs)
sudo systemctl stop irqbalance
sudo systemctl disable irqbalance

# Identify IRQs and their current affinity
cat /proc/interrupts
```

Create an IRQ affinity script:

```bash
sudo nano /usr/local/bin/set-irq-affinity.sh
```

Add this content (adjust CPU mask for your configuration):

```bash
#!/bin/bash
# This script sets IRQ affinity to host-only CPUs (0-1 in this example)
# CPU mask for cores 0-1: 3 (binary 11)

# Set default affinity for all IRQs to cores 0-1
for irq in $(cat /proc/interrupts | grep -v CPU | awk '{print $1}' | sed s/\://g); do
  if [ -f /proc/irq/$irq/smp_affinity ]; then
    echo "Setting IRQ $irq affinity to 3 (CPU 0-1)"
    echo 3 > /proc/irq/$irq/smp_affinity
  fi
done

# For devices used by the VM via passthrough, you might want different settings
# Example: If passing through a NIC with IRQ 40, you might want it on the VM's CPUs
# echo 252 > /proc/irq/40/smp_affinity  # Binary 11111100 = CPUs 2-7
```

Make the script executable and run at boot:

```bash
sudo chmod +x /usr/local/bin/set-irq-affinity.sh

# Add to /etc/rc.local or create a systemd service
sudo nano /etc/systemd/system/irqaffinity.service
```

Add this content:

```
[Unit]
Description=Set IRQ Affinity
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/set-irq-affinity.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable irqaffinity.service
sudo systemctl start irqaffinity.service

# Verify IRQ affinity
cat /proc/irq/*/smp_affinity
```

### 9. System-wide Tuning with tuned

```bash
# Install tuned
sudo apt install -y tuned

# Apply virtual-host profile
sudo tuned-adm profile virtual-host

# Verify active profile
sudo tuned-adm active  # Should show "Current active profile: virtual-host"
```

For advanced users, create a custom tuned profile:

```bash
# Create custom profile directory
sudo mkdir -p /etc/tuned/vm-host-custom

# Create profile configuration
sudo nano /etc/tuned/vm-host-custom/tuned.conf
```

Add this content (adjust as needed):

```
[main]
include=virtual-host

[cpu]
force_latency=1
governor=performance
energy_perf_bias=performance

[vm]
transparent_hugepages=never

[sysctl]
vm.swappiness=1
kernel.sched_min_granularity_ns=10000000
kernel.sched_wakeup_granularity_ns=15000000
```

Apply the custom profile:

```bash
sudo tuned-adm profile vm-host-custom

# Verify
sudo tuned-adm active
```

## III. Incus Virtual Machine Configuration

### 1. Incus Installation and Basic Setup

If not already installed:

```bash
# Add Incus repository
sudo apt update
sudo apt install -y curl gpg
curl -fsSL https://pkgs.zabbly.com/key.asc | sudo gpg --dearmor -o /etc/apt/keyrings/zabbly.gpg
echo "deb [arch=amd64,arm64 signed-by=/etc/apt/keyrings/zabbly.gpg] https://pkgs.zabbly.com/incus/stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/incus-stable.list

# Install Incus
sudo apt update
sudo apt install -y incus

# Initialize Incus
sudo incus admin init
```

### 2. CPU Configuration

Create or configure your VM with optimal CPU settings:

```bash
# Create a new VM (example)
incus init images:ubuntu/24.04 YOUR_VM_NAME --vm -c limits.cpu=2-7

# Or configure existing VM
incus config set YOUR_VM_NAME limits.cpu 2-7
incus config set YOUR_VM_NAME limits.cpu.allowance 100%
incus config set YOUR_VM_NAME limits.cpu.priority 10

# Enable CPU host passthrough for best performance
incus config set YOUR_VM_NAME security.guest.features.cpu.host_passthrough true

# For NUMA systems, pin to specific node
incus config set YOUR_VM_NAME limits.cpu.nodes 0
```

Verify CPU configuration:

```bash
incus config show YOUR_VM_NAME | grep -i cpu
```

### 3. Memory Configuration

Configure VM memory for optimal performance:

```bash
# Set memory limit (adjust based on your system)
incus config set YOUR_VM_NAME limits.memory 60GiB

# Enforce hard memory limits
incus config set YOUR_VM_NAME limits.memory.enforce hard

# Enable hugepages (after configuring on host)
incus config set YOUR_VM_NAME limits.memory.hugepages true

# For NUMA systems, pin memory to same node as CPUs
incus config set YOUR_VM_NAME limits.memory.nodes 0
```

Verify memory configuration:

```bash
incus config show YOUR_VM_NAME | grep -i memory
```

### 4. Storage Configuration

#### 4.1 Direct Device Passthrough (Best Performance)

```bash
# Identify available block devices
lsblk

# Pass through entire disk or partition
incus config device add YOUR_VM_NAME root disk source=/dev/sdb path=/
```

#### 4.2 Storage Pool Configuration

```bash
# Create a storage pool (if not already created)
incus storage create vm-storage zfs source=/dev/sdc

# Create a volume
incus storage volume create vm-storage vm-disk size=100GiB

# Add to VM
incus config device add YOUR_VM_NAME root disk pool=vm-storage source=vm-disk path=/

# Optimize disk settings
incus config device set YOUR_VM_NAME root limits.read 0
incus config device set YOUR_VM_NAME root limits.write 0
incus config device set YOUR_VM_NAME root limits.disk.priority 10
```

For advanced disk performance:

```bash
# Disable cache for direct I/O
incus config device set YOUR_VM_NAME root cache none

# Set appropriate I/O mode
incus config device set YOUR_VM_NAME root io native
```

### 5. Network Configuration

#### 5.1 PCI Passthrough (Best Performance)

First, identify the network device:

```bash
# List PCI devices
lspci -nnk | grep -i ethernet

# Identify the device name
ip link show
```

Configure PCI passthrough:

```bash
# Add the device to the VM
incus config device add YOUR_VM_NAME eth0 nic nictype=physical parent=enp3s0

# If using SR-IOV (for supported NICs)
# First create virtual functions on host
echo 4 | sudo tee /sys/class/net/enp3s0/device/sriov_numvfs

# Then assign a VF to the VM
incus config device add YOUR_VM_NAME eth0 nic nictype=sriov parent=enp3s0
```

#### 5.2 Macvlan Configuration (Good Performance)

```bash
# Add macvlan interface
incus config device add YOUR_VM_NAME eth0 nic nictype=macvlan parent=enp3s0

# Enable multi-queue for better performance
incus config device set YOUR_VM_NAME eth0 queues 8
```

Verify network configuration:

```bash
incus config show YOUR_VM_NAME | grep -A 10 "devices:"
```

### 6. GPU Passthrough (For Graphics Workloads)

If you need GPU acceleration in your VM:

```bash
# Identify GPU
lspci -nnk | grep -i vga

# Ensure IOMMU is enabled and GPU is in its own IOMMU group
find /sys/kernel/iommu_groups/ -type l | sort -n

# Add GPU to VM (example for NVIDIA GPU at 01:00.0)
incus config device add YOUR_VM_NAME gpu gpu pci=0000:01:00.0
```

For NVIDIA GPUs, you may need to hide the virtualization:

```bash
# Hide KVM from NVIDIA driver
incus config set YOUR_VM_NAME raw.qemu '-cpu host,kvm=off'
```

### 7. Guest OS Optimization

Start the VM and perform guest-side optimizations:

```bash
# Start the VM
incus start YOUR_VM_NAME

# Access VM console
incus console YOUR_VM_NAME
```

Inside the VM, install and configure:

```bash
# Install QEMU guest agent
sudo apt update
sudo apt install -y qemu-guest-agent
sudo systemctl enable --now qemu-guest-agent

# Install virtio drivers (usually pre-installed on Linux guests)
lsmod | grep virtio  # Should show multiple virtio modules

# Optimize I/O scheduler inside guest
echo none | sudo tee /sys/block/vda/queue/scheduler

# Set CPU governor to performance
sudo apt install -y cpufrequtils
echo 'GOVERNOR="performance"' | sudo tee /etc/default/cpufrequtils
sudo systemctl enable --now cpufrequtils
```

## IV. Verification and Benchmarking

### 1. Host Verification

```bash
# Verify kernel parameters
cat /proc/cmdline

# Check CPU isolation
ps -eo psr,pid,comm | sort -n | head -20  # Should show most processes on cores 0-1

# Verify hugepages allocation
cat /proc/meminfo | grep -i huge

# Check CPU governor
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# Verify QEMU process CPU affinity
ps aux | grep qemu
taskset -cp $(pgrep -f "qemu.*YOUR_VM_NAME")  # Should show it's running on isolated cores
```

### 2. VM Verification

```bash
# Check VM status and resource allocation
incus info YOUR_VM_NAME

# Monitor VM resource usage
incus top YOUR_VM_NAME
```

Inside the VM:

```bash
# Check CPU information
lscpu

# Verify memory allocation
free -h

# Check for virtualization-specific hardware
lspci

# Examine kernel messages for hardware detection
dmesg | grep -i virt
```

### 3. Performance Benchmarking

#### 3.1 CPU Benchmarks

```bash
# Install benchmarking tools
sudo apt install -y sysbench

# CPU benchmark
sysbench cpu --cpu-max-prime=20000 --threads=$(nproc) run

# Compare with host performance (run same test on host)
```

#### 3.2 Memory Benchmarks

```bash
# Memory benchmark
sysbench memory --memory-block-size=1K --memory-total-size=100G --threads=$(nproc) run
```

#### 3.3 Disk I/O Benchmarks

```bash
# Install fio
sudo apt install -y fio

# Random read/write test
fio --name=random-rw --ioengine=libaio --direct=1 --bs=4k --iodepth=64 --size=4G --numjobs=4 --rw=randrw --group_reporting

# Sequential read test
fio --name=seq-read --ioengine=libaio --direct=1 --bs=1M --iodepth=16 --size=4G --numjobs=1 --rw=read --group_reporting
```

#### 3.4 Network Benchmarks

```bash
# Install iperf3
sudo apt install -y iperf3

# Run iperf3 server on one machine
iperf3 -s

# Run client on the other machine
iperf3 -c SERVER_IP -P 4 -t 30
```

## V. Monitoring and Maintenance

### 1. Ongoing Performance Monitoring

Set up basic monitoring:

```bash
# Install monitoring tools
sudo apt install -y sysstat htop iotop

# Configure sysstat collection
sudo systemctl enable --now sysstat
```

For advanced monitoring, consider:
- Prometheus + Grafana
- Netdata
- Telegraf + InfluxDB + Grafana

### 2. Update Management

Create a maintenance plan:

1. **Kernel Updates**: Test in a non-production environment first, as they may affect:
   - CPU isolation settings
   - IOMMU functionality
   - PCI passthrough behavior

2. **Incus Updates**: Check release notes for changes that might affect VM configuration

3. **Firmware Updates**: Periodically check for and apply firmware/microcode updates

### 3. Backup Strategy

Implement a VM backup strategy:

```bash
# Create a snapshot
incus snapshot YOUR_VM_NAME snapshot1

# Export the snapshot
incus export YOUR_VM_NAME/snapshot1 /path/to/backup/location/vm-backup.tar.gz
```

Consider automating backups with a script:

```bash
#!/bin/bash
# VM backup script
DATE=$(date +%Y%m%d)
SNAPSHOT_NAME="backup-$DATE"
VM_NAME="YOUR_VM_NAME"
BACKUP_DIR="/path/to/backups"

# Create snapshot
incus snapshot $VM_NAME $SNAPSHOT_NAME

# Export snapshot
incus export $VM_NAME/$SNAPSHOT_NAME $BACKUP_DIR/$VM_NAME-$DATE.tar.gz

# Clean up old snapshots (keep last 5)
incus info $VM_NAME | grep snapshot | sort | head -n -5 | while read -r line; do
  SNAP=$(echo $line | awk '{print $1}')
  incus delete $VM_NAME/$SNAP
done
```

## VI. Troubleshooting Common Issues

### 1. VM Performance Issues

If VM performance is not as expected:

```bash
# Check if CPU isolation is working
ps -eo psr,pid,comm | grep -v "^[0-1]"  # Should show minimal processes on isolated cores

# Check if VM processes are on isolated cores
ps -eo psr,pid,comm | grep qemu  # Should show on isolated cores

# Check for CPU throttling
grep -i throttling /var/log/syslog

# Monitor for resource contention
sudo apt install -y perf
sudo perf top  # Look for unexpected system activity
```

### 2. PCI Passthrough Issues

If PCI passthrough doesn't work:

```bash
# Verify IOMMU is enabled
dmesg | grep -e DMAR -e IOMMU

# Check IOMMU groups
find /sys/kernel/iommu_groups/ -type l | sort -n

# Ensure device is properly bound to vfio-pci
lspci -nnk | grep -A3 "PCI_ID_OF_DEVICE"
```

### 3. Memory Allocation Issues

If hugepages allocation fails:

```bash
# Check memory fragmentation
cat /proc/buddyinfo

# Try allocating hugepages early in boot process
# Add to GRUB_CMDLINE_LINUX_DEFAULT: hugepagesz=2M hugepages=30976

# Or try 1GB hugepages if supported
# Add to GRUB_CMDLINE_LINUX_DEFAULT: hugepagesz=1G hugepages=62
```

## VII. Advanced Optimizations

### 1. CPU Pinning Fine-Tuning

For multi-socket NUMA systems, further optimize CPU pinning:

```bash
# Identify NUMA topology
numactl --hardware

# Pin emulator threads to host CPUs
incus config set YOUR_VM_NAME raw.qemu '-object iothread,id=iothread0 -object iothread,id=iothread1'

# For VMs with many vCPUs, consider topology awareness
incus config set YOUR_VM_NAME raw.qemu '-smp 6,sockets=1,cores=6,threads=1'
```

### 2. Storage I/O Fine-Tuning

For storage-intensive workloads:

```bash
# Add dedicated I/O threads
incus config device set YOUR_VM_NAME root io.threads 4

# For ZFS storage pools, optimize ARC cache
echo "options zfs zfs_arc_max=4294967296" | sudo tee /etc/modprobe.d/zfs.conf  # Limit to 4GB
sudo systemctl restart zfs-import-cache

# For multi-queue block device support
incus config device set YOUR_VM_NAME root queues 4
```

### 3. Real-Time Kernel (For Latency-Sensitive Workloads)

For workloads requiring minimal latency:

```bash
# Install real-time kernel
sudo apt install -y linux-image-rt-amd64

# Update GRUB to boot with RT kernel
sudo update-grub

# After reboot, verify RT kernel
uname -a  # Should show "PREEMPT_RT"

# Set RT priorities for VM
sudo chrt -f -p 80 $(pgrep -f "qemu.*YOUR_VM_NAME")
```

### 4. Power Management Optimization

Balance performance and power consumption:

```bash
# Install power management tools
sudo apt install -y powertop

# Run powertop calibration
sudo powertop --calibrate

# Generate optimized settings
sudo powertop --auto-tune

# Apply only to non-isolated cores (advanced)
for cpu in 0 1; do
  echo performance | sudo tee /sys/devices/system/cpu/cpu$cpu/cpufreq/scaling_governor
done
```

## VIII. Specialized Configurations

### 1. High-Performance Computing (HPC) VM

For scientific computing workloads:

```bash
# Enable CPU features like AVX, AVX2, AVX512
incus config set YOUR_VM_NAME raw.qemu '-cpu host,+avx,+avx2,+avx512f,+avx512dq,+avx512bw,+avx512vl'

# Optimize memory access
echo 0 | sudo tee /proc/sys/kernel/numa_balancing  # Disable automatic NUMA balancing
```

### 2. Gaming VM Configuration

For gaming workloads:

```bash
# Enable CPU features for gaming
incus config set YOUR_VM_NAME raw.qemu '-cpu host,kvm=off,hv_vendor_id=1234567890ab,hv_relaxed,hv_spinlocks=0x1fff,hv_vapic,hv_time'

# Add gaming-optimized kernel parameters to host
# Add to GRUB_CMDLINE_LINUX_DEFAULT: clocksource=tsc tsc=reliable

# Inside VM, optimize for gaming
echo 1 | sudo tee /proc/sys/kernel/sched_child_runs_first
```

### 3. Database VM Configuration

For database workloads:

```bash
# Optimize I/O scheduler for database workloads
echo kyber | sudo tee /sys/block/nvme0n1/queue/scheduler

# Set I/O priorities
ionice -c 1 -n 0 -p $(pgrep -f "qemu.*YOUR_VM_NAME")

# Inside VM, optimize memory management
echo 'vm.dirty_ratio = 10' | sudo tee -a /etc/sysctl.conf
echo 'vm.dirty_background_ratio = 5' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

## IX. Security Considerations

### 1. Mitigating Security Risks

When using performance-enhancing but security-reducing options:

```bash
# If using mitigations=off, implement network isolation
sudo ufw enable
sudo ufw default deny incoming
sudo ufw allow ssh
sudo ufw allow from TRUSTED_IP_ADDRESS

# Consider running VM in isolated VLAN
incus network create isolated-net --type=bridge
incus network attach isolated-net YOUR_VM_NAME eth0
```

### 2. Secure PCI Passthrough

When passing through PCI devices:

```bash
# Ensure device firmware is up-to-date
sudo apt install -y pciutils
sudo update-pciids
lspci -vvv | grep -i "firmware"

# For GPU passthrough, consider firmware security
sudo apt install -y vgabios
```

### 3. VM Isolation

Enhance VM isolation:

```bash
# Disable unnecessary VM features
incus config set YOUR_VM_NAME security.guest.features.secureboot false
incus config set YOUR_VM_NAME security.guest.features.smm false

# Enable nested virtualization only if needed
incus config set YOUR_VM_NAME security.guest.features.nested false
```

## X. Migration and Backup Strategies

### 1. VM Migration Preparation

Prepare your VM for potential migration:

```bash
# Use consistent device naming
incus config device set YOUR_VM_NAME root path=/dev/vda

# Document all passthrough devices
incus config show YOUR_VM_NAME > vm_config_backup.txt

# Create a migration-ready snapshot
incus snapshot YOUR_VM_NAME migration-ready
```

### 2. Comprehensive Backup Strategy

Implement a comprehensive backup strategy:

```bash
# Create backup script with verification
cat > /usr/local/bin/vm-backup.sh << 'EOF'
#!/bin/bash
set -e

VM_NAME="YOUR_VM_NAME"
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d-%H%M%S)
SNAPSHOT_NAME="backup-$DATE"
BACKUP_FILE="$BACKUP_DIR/$VM_NAME-$DATE.tar.gz"
LOG_FILE="$BACKUP_DIR/backup-$DATE.log"

echo "Starting backup of $VM_NAME at $(date)" | tee -a "$LOG_FILE"

# Create snapshot
incus snapshot "$VM_NAME" "$SNAPSHOT_NAME" 2>&1 | tee -a "$LOG_FILE"

# Export snapshot
incus export "$VM_NAME/$SNAPSHOT_NAME" "$BACKUP_FILE" 2>&1 | tee -a "$LOG_FILE"

# Verify backup integrity
tar -tzf "$BACKUP_FILE" > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "Backup verified successfully" | tee -a "$LOG_FILE"
else
  echo "ERROR: Backup verification failed!" | tee -a "$LOG_FILE"
  exit 1
fi

# Clean up old snapshots (keep last 5)
for SNAP in $(incus info "$VM_NAME" | grep "backup-" | sort | head -n -5 | awk '{print $1}'); do
  echo "Removing old snapshot: $SNAP" | tee -a "$LOG_FILE"
  incus delete "$VM_NAME/$SNAP" 2>&1 | tee -a "$LOG_FILE"
done

echo "Backup completed successfully at $(date)" | tee -a "$LOG_FILE"
EOF

chmod +x /usr/local/bin/vm-backup.sh
```

Set up automated backups:

```bash
# Create systemd timer for regular backups
cat > /etc/systemd/system/vm-backup.service << EOF
[Unit]
Description=Backup Incus VM
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/vm-backup.sh
User=root

[Install]
WantedBy=multi-user.target
EOF

cat > /etc/systemd/system/vm-backup.timer << EOF
[Unit]
Description=Run VM backup daily

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

sudo systemctl enable --now vm-backup.timer
```

## XI. Long-term Maintenance and Evolution

### 1. Performance Monitoring Dashboard

Set up a comprehensive monitoring solution:

```bash
# Install Prometheus and node_exporter
sudo apt install -y prometheus prometheus-node-exporter

# Install Grafana
sudo apt install -y apt-transport-https software-properties-common
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
sudo apt update
sudo apt install -y grafana

# Enable and start services
sudo systemctl enable --now prometheus prometheus-node-exporter grafana-server

# Access Grafana at http://your-server-ip:3000 (default: admin/admin)
# Add Prometheus as a data source and import VM monitoring dashboards
```

### 2. Update Management Strategy

Create a systematic update process:

```bash
# Create update testing script
cat > /usr/local/bin/test-updates.sh << 'EOF'
#!/bin/bash
set -e

VM_NAME="YOUR_VM_NAME"
SNAPSHOT_NAME="pre-update-$(date +%Y%m%d)"

# Create pre-update snapshot
incus snapshot "$VM_NAME" "$SNAPSHOT_NAME"

# Apply updates
sudo apt update
sudo apt upgrade -y

# Run performance tests
# Add your benchmarking commands here

# If tests fail, restore snapshot
# incus restore "$VM_NAME" "$SNAPSHOT_NAME"
EOF

chmod +x /usr/local/bin/test-updates.sh
```

### 3. Documentation and Knowledge Base

Maintain comprehensive documentation:

```bash
# Create documentation directory
mkdir -p ~/vm-documentation

# Document current configuration
incus config show YOUR_VM_NAME > ~/vm-documentation/vm-config.txt
cat /proc/cmdline > ~/vm-documentation/kernel-parameters.txt
lspci -vvv > ~/vm-documentation/pci-devices.txt
cat /etc/default/grub > ~/vm-documentation/grub-config.txt

# Document performance baseline
sysbench cpu --cpu-max-prime=20000 --threads=$(nproc) run > ~/vm-documentation/cpu-baseline.txt
fio --name=random-rw --ioengine=libaio --direct=1 --bs=4k --iodepth=64 --size=4G --numjobs=4 --rw=randrw --group_reporting > ~/vm-documentation/disk-baseline.txt
```

## XII. Conclusion and Final Checklist

### 1. Performance Optimization Checklist

Before considering your optimization complete, verify:

- [ ] CPU isolation is working (processes stay on designated cores)
- [ ] VM is using hugepages (check with `incus info`)
- [ ] Storage performance meets expectations (verify with `fio`)
- [ ] Network performance meets expectations (verify with `iperf3`)
- [ ] VM startup and operation is stable
- [ ] Backup and recovery procedures are tested
- [ ] Monitoring is in place
- [ ] Documentation is complete

### 2. Final Thoughts

Remember that performance optimization is an ongoing process:

1. **Measure First**: Always benchmark before and after changes
2. **Incremental Changes**: Make one change at a time and test
3. **Document Everything**: Keep detailed records of all configurations
4. **Security Balance**: Understand the security implications of performance optimizations
5. **Workload Adaptation**: Be prepared to adjust optimizations as workloads change

By systematically applying these optimizations to both the Ubuntu Server host and Incus VM configuration, you can achieve virtual machine performance very close to bare-metal, with minimal overhead from the virtualization layer.