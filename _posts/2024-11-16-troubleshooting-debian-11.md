---
tags: software>linux
info: aberto.
date: 2024-11-16
type: post
layout: post
published: true
slug: troubleshooting-debian-11
title: 'Troubleshooting Debian 11'
---
Systematic approach to troubleshoot and resolve slow performance issues on a Debian 11

### 1. Immediate Actions

If your system is extremely slow, try these first:

* **Recovery Mode:** Boot into recovery mode (usually by pressing Esc, Shift, or F2 during boot). This starts the system with minimal services, potentially bypassing the performance issue.
* **Kill Resource-Intensive Processes:** If you can access a terminal, use `top` to identify and stop processes consuming excessive resources: `sudo pkill -STOP <process_name>`.
* **Clear System Cache:**  `sudo sync && sudo echo 3 > /proc/sys/vm/drop_caches`


### 2. Basic Diagnostics

* **CPU Usage:** `top` (or `htop` if installed) - Look for processes consistently using a high percentage of CPU.
* **Memory Usage:** `free -h` - Check for low available memory, which could indicate excessive swapping.
* **Disk I/O:** `iostat` - High `%util` values suggest disk bottlenecks.

### 3.  Rockchip/ARM64 Specific Checks

* **CPU Governor:** `cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor` -  Should be `performance`. If not: `echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor`
* **Thermal Throttling:** `cat /sys/class/thermal/thermal_zone*/temp` - Check for overheating.

### 4. Software and Configuration Diagnostics

* **Boot Logs:** `dmesg | less` - Look for errors or warnings during boot.
* **System Logs:** `journalctl -p err -b` - Check for recent errors.  For specific services: `journalctl -u <service_name>`.
* **Package Management Logs:**
    * `less /var/log/apt/history.log` - Review recent installations or updates.
    * `less /var/log/dpkg.log` - Check for package installation errors.
* **Recently Modified Files:** `sudo find /etc -type f -mtime -7 -ls` (lists files modified in the last 7 days).


### 5. Advanced Troubleshooting

* **Hardware Checks:**  `sensors` (if installed) to monitor hardware temperatures and voltages.  Consider running `memtester` to check for memory issues.
* **Detailed System Information:** Install `sysstat`: `sudo apt install sysstat`.  Use `sar` to collect detailed system performance data.
* **Live Boot Environment:** Boot from a Debian Live USB/SD card to test if the slowdown persists, which could indicate a hardware problem.

### 6. Prevention

* **Regular Backups:** Use `timeshift` (or similar tools) to create system snapshots: `sudo timeshift --create --comments "Before making changes"`.
* **System Updates:** Keep your system updated: `sudo apt update && sudo apt upgrade -y`.
* **Configuration Management:** Use version control (e.g., Git) or dedicated tools like `etckeeper` to track changes to configuration files.


### 7. Reconstructing Changes (If Necessary)

If the above steps don't pinpoint the cause, you can try to reconstruct your recent changes:

* **Command History:** `history`
* **Audit Logs (if configured):** `ausearch -k <event_key>`