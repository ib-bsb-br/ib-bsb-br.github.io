---
tags: [scratchpad]
info: aberto.
date: 2025-03-22
type: post
layout: post
published: true
slug: raspberry-pi-4b-bootfirmwareconfigtxt
title: 'raspberry pi 4B /boot/firmware/config.txt'
---
bibref https://ib.bsb.br/raspberry-overclock

{% codeblock %}
# Raspberry Pi 4B Config.txt - Optimized for Dual-Monitor Video Playback

# ---- System Settings ----
kernel=u-boot.bin
armstub=armstub8-rpi4.bin
avoid_warnings=1
enable_uart=1

# ---- Performance Settings ----
# Your existing overclock appears stable but watch temperatures during video playback
arm_freq=1825
gpu_freq=575
over_voltage=3
force_turbo=1

# ---- GPU Memory Allocation ----
# Increased from 32MB for better video performance
# 256MB recommended for dual 1080p displays
# Can use 320MB for 4K content if needed
gpu_mem=320

# ---- Temperature Management ----
# Prevents throttling during extended video sessions with your overclock
temp_soft_limit=80
temp_limit=85

# ---- Display Settings ----
disable_overscan=1
dtparam=audio=on

# ---- Graphics Driver Configuration ----
# Full KMS driver with improved video performance and reduced tearing
# cma-512 allocates 512MB continuous memory blocks for GPU (important for smooth video)
# nocomposite disables analog video output to free up resources
dtoverlay=vc4-kms-v3d-pi4,nocomposite,cma-768
dtoverlay=enable-bt
dtoverlay=smbios
dtoverlay=upstream

# ---- HDMI Port 0 (Primary) ----
[hdmi:0]
hdmi_force_hotplug=1
hdmi_drive=2
# If using 1080p monitors, uncomment and use these settings:
#hdmi_group=1  # CEA (consumer electronics)
#hdmi_mode=16  # 1080p 60Hz

# ---- HDMI Port 1 (Secondary) ----
[hdmi:1]
hdmi_force_hotplug=1
hdmi_drive=2
# If using 1080p monitors, uncomment and use these settings:
#hdmi_group=1  # CEA (consumer electronics)
#hdmi_mode=16  # 1080p 60Hz

# ---- Include Files ----
include extraconfig.txt
include ubootconfig.txt
{% endcodeblock %}
