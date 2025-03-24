---
tags: [hardware>raspberry]
info: aberto.
date: 2025-02-23
type: post
layout: post
published: true
slug: raspberry-overclock
title: 'Overclocking Raspberry Pi 3B (debian), 4B (openSUSE)'
---
bibref https://ib.bsb.br/raspberry-pi-4b-bootfirmwareconfigtxt

# Overclocking Raspberry Pi 4B on openSUSE Tumbleweed (aarch64)

## Important Considerations

- Overclocking may void your warranty and reduce hardware lifespan.
- Ensure proper cooling (heatsink and fan) and a stable power supply (official Raspberry Pi USB-C power supply recommended).
- Always back up your data and configuration files before proceeding.

## Step-by-Step Guide

### 1. Install Necessary Tools

```bash
sudo zypper install nano lm_sensors stress-ng
```

### 2. Backup Current Configuration

```bash
sudo cp /boot/efi/config.txt ~/config.txt.backup
```

### 3. Edit Configuration File

On openSUSE Tumbleweed, the configuration file is typically located at:

```bash
sudo nano /boot/efi/config.txt
```

### 4. Recommended Overclock Settings

Start conservatively to ensure stability:

**Safe Settings (Recommended):**

```
arm_freq=1750
over_voltage=2
gpu_freq=550
```

**Moderate Settings (Requires Good Cooling):**

```
arm_freq=1900
over_voltage=4
gpu_freq=600
```

**Aggressive Settings (Advanced Users Only, Excellent Cooling Required):**

```
arm_freq=2000
over_voltage=6
gpu_freq=650
```

### 5. Save and Reboot

Save changes (`Ctrl+O`, `Enter`, `Ctrl+X`) and reboot:

```bash
sudo reboot
```

## Monitoring and Testing Stability

### Check CPU Frequency

```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
```

### Monitor Temperature

```bash
watch -n 1 "cat /sys/class/thermal/thermal_zone0/temp | awk '{print \$1/1000}'"
```

### Stress Test (5-10 minutes initially)

```bash
stress-ng --cpu 4 --timeout 300s
```

If instability occurs (crashes, overheating, errors), revert to lower settings.

## Troubleshooting and Recovery

- If the system fails to boot, mount the SD card on another computer and restore the backup:

  ```bash
  sudo cp ~/config.txt.backup /boot/efi/config.txt
  ```

- Check kernel logs for errors:

  ```bash
  dmesg | grep -i error
  ```

- Check for undervoltage warnings:

  ```bash
  dmesg | grep -i voltage
  ```

***

# Overclocking Raspberry Pi 3B on Debian

## Overview

Overclocking your Raspberry Pi 3B involves editing its configuration file to boot with higher-than-standard clock settings. Be aware that overclocking can cause instability, higher temperatures, and may void your warranty. Adequate cooling and temperature monitoring are essential.

## Step-by-Step Guide

### 1. Back Up Your Data

- Before making any changes, back up your important data in case the system becomes unstable.

### 2. Edit the Configuration File

- Open a terminal
- Edit the file /boot/config.txt with your favorite text editor:
  
  ```bash
  sudo nano /boot/config.txt
  ```
  
- Scroll down (or add at the end) to include the overclocking settings

### 3. Add Overclocking Parameters

For a Raspberry Pi 3B, common overclocking settings include:

```bash
# Overclock settings for Raspberry Pi 3B  
arm_freq=1400  
core_freq=500  
over_voltage=6
```

- `arm_freq` increases the CPU frequency (the default for the Pi 3B is 1200 MHz)
- `core_freq` sets the GPU's "core" clock frequency
- `over_voltage` helps stabilize the overclock at higher speeds by increasing the voltage

> **Note:** Some users add `force_turbo=1` to keep the CPU at maximum speed constantly, but this increases power consumption and heat, and can void warranty claims regarding performance.

### 4. Save and Reboot

- Save your changes (in nano, press Ctrl+O, Enter, then Ctrl+X)
- Reboot your Raspberry Pi:
  
  ```bash
  sudo reboot
  ```

### 5. Test Stability and Monitor Temperature

- After rebooting, test your system for stability
- If you encounter crashes or unusual behavior, reduce the overclock settings until stable
- Monitor temperature with:
  
  ```bash
  vcgencmd measure_temp
  ```
  
- Consider additional cooling if temperatures are high
