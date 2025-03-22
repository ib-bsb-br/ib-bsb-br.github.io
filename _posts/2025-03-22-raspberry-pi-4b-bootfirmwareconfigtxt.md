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
{% codeblock %}
arm_freq=1825
armstub=armstub8-rpi4.bin
avoid_warnings=1
disable_overscan=1
dtoverlay=enable-bt
dtoverlay=smbios
dtoverlay=upstream
dtoverlay=vc4-kms-v3d-pi4,cma-default
dtparam=audio=on
enable_uart=1
force_turbo=1
gpu_freq=575
gpu_mem=32
hdmi_drive=2
hdmi_force_hotplug=1
include extraconfig.txt
include ubootconfig.txt
kernel=u-boot.bin
over_voltage=3
{% endcodeblock %}