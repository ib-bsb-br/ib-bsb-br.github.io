---
tags: [scratchpad]
info: aberto.
date: 2025-03-27
type: post
layout: post
published: true
slug: raspberry-pi-3b-bootfirmwareconfigtxt
title: 'raspberry pi 3B /boot/firmware/config.txt'
---
bibref https://ib.bsb.br/raspberry-overclock

{% codeblock %}
[all]
# Basic System Settings
disable_overscan=1
disable_splash=1
auto_initramfs=1

# Display Settings
dtoverlay=vc4-kms-v3d
max_framebuffers=2
disable_fw_kms_setup=1

# Balanced Overclock Settings
arm_freq=1350       # More conservative but still +12.5% performance
core_freq=500       # Reasonable GPU/core boost
sdram_freq=500      # Safer memory frequency
over_voltage=4      # Moderate voltage increase
# force_turbo=0     # Remove line or set to 0 to allow dynamic scaling
# arm_boost removed as it's non-essential

# Safety Parameters
temp_limit=80       # Lower throttling temperature for better protection

# Camera Settings (choose one approach)
camera_auto_detect=0
# start_x=0         # Use only if you need legacy camera support

# GPU Memory
gpu_mem=64         # Good baseline for general use
{% endcodeblock %}