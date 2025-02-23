---
tags: [scratchpad]
info: aberto.
date: 2025-02-23
type: post
layout: post
published: true
slug: overclocking-your-raspberry-pi-3b
title: 'Overclocking your Raspberry Pi 3B'
---
Overclocking your Raspberry Pi 3B is done by editing its configuration file so that the system boots with higher-than-standard clock settings. However, please note that overclocking can lead to instability, increased temperatures, and might void your warranty. Ensure you have adequate cooling (a good heatsink and possibly a fan) and monitor your Pi’s temperature (using a tool like vcgencmd measure_temp) after making changes.

Here’s how to overclock your Pi:

1. Back Up Your Data  
 • Before making any changes, back up your important data in case the system becomes unstable.

2. Edit the Configuration File  
 • Open a terminal.  
 • Edit the file /boot/config.txt with your favorite text editor (e.g., nano):  
  sudo nano /boot/config.txt  
 • Scroll down (or add at the end) to include the overclocking settings.

3. Add Overclocking Parameters  
For a Raspberry Pi 3B, users commonly experiment with settings like the following. (Your mileage may vary; if you experience instability, dial back the settings.) For example, you might add:

  # Overclock settings for Raspberry Pi 3B  
  arm_freq=1400  
  core_freq=500  
  over_voltage=6  

• arm_freq increases the CPU frequency (the default for the Pi 3B is 1200 MHz).  
• core_freq sets the GPU’s “core” clock frequency.  
• over_voltage helps stabilize the overclock at higher speeds by increasing the voltage (even a small increase may be needed).  
  Note: Some users also add force_turbo=1 to keep the CPU running at maximum speed at all times, but doing so may lead to higher power consumption and additional heat and can void warranty claims regarding performance.

4. Save and Reboot  
 • Save your changes (in nano, press Ctrl+O, Enter, then Ctrl+X).  
 • Reboot your Raspberry Pi:  
  sudo reboot

5. Test Stability and Monitor Temperature  
 • After rebooting, test your system. If you encounter crashes or unusual behavior, reduce the overclock settings (lower arm_freq or lower over_voltage) until you find stable values.  
 • Monitor temperature with:  
  vcgencmd measure_temp  
  and consider additional cooling if temperatures are high.

6. Customize as Needed  
Since you’re running X11 with ratpoison as your window manager, note that these overclock settings affect the entire system, not just the graphical environment. Fine-tune based on your performance needs and stability.

Remember, every Raspberry Pi’s silicon and cooling solution may behave differently with overclocking, so it’s important to experiment incrementally and carefully. Enjoy the extra performance, but always keep an eye on system stability and temperature!

***

```
Overclocking on a Raspberry Pi 3B is done by editing the boot configuration file (config.txt) on the SD card. However, there are a few important notes and cautions:

1) Overclocking can void warranties (especially if you enable force_turbo=1).  
2) Each individual board behaves differently; some might not be stable at higher frequencies.  
3) Ensure you have adequate power (5V at 2.5–3A) and cooling (heatsinks, fan) to manage extra heat.  
4) There is no official “Overclock” option in raspi-config for Pi 3B—overclocking must be done manually.

────────────────────────────────────────────────────────────────
STEP-BY-STEP: Edit config.txt
────────────────────────────────────────────────────────────────
1. Open /boot/config.txt in a text editor:
   sudo nano /boot/config.txt

2. Add or modify lines for overclocking; for example:
   over_voltage=4
   arm_freq=1350
   gpu_freq=400
   #force_turbo=1

   • over_voltage sets how much extra voltage to supply to the CPU (range 0–6). Each step of 1 = +0.025 V. 4 is a moderate increase.  
   • arm_freq sets CPU frequency (in MHz). 1350–1400 MHz is common for mild to moderate overclocks on Pi 3B.  
   • gpu_freq sets the GPU core frequency (in MHz). Typical values range ~300–400 MHz.  
   • force_turbo=1 forces the CPU/GPU to run at the specified frequencies even when idle (voids warranty).  

3. Save and exit (Ctrl+O, Enter, Ctrl+X).

4. Reboot to apply changes:
   sudo reboot

────────────────────────────────────────────────────────────────
Monitoring Temperature & Stability
────────────────────────────────────────────────────────────────
• Check temperature:
  vcgencmd measure_temp
  – Aim to keep under ~70–80°C under load.  

• Check CPU frequency:
  watch -n 1 cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
  – Updates every second to see if you’re hitting your target clock.  

• Watch for undervoltage or throttling warnings in:
  dmesg | grep -i volt
  – If you see undervoltage warnings, ensure your power supply can deliver stable 5V 2.5A+.

If the system becomes unstable (freezes, unexpected reboots), either reduce frequency or increase over_voltage slightly. Always keep an eye on temperatures and stability. Each Pi board’s “safe” overclock margin can vary.  

────────────────────────────────────────────────────────────────
Tips
────────────────────────────────────────────────────────────────
• Use a proper heat sink (or a heat sink + fan) to keep CPU/GPU cool.  
• Start with small increments for arm_freq (e.g., go from 1200 to 1250, 1300, etc.) and test.  
• If you need a bit more stability at higher clocks, gradually raise over_voltage (not recommended to exceed 6).  
• force_turbo=1 locks the CPU at full speed, but it will void your warranty “bit” in the OTP memory. Consider leaving it off unless you need constant high performance.  

That’s it! With the config.txt approach, you can manually tune your Raspberry Pi 3B for a stable overclock in your X11 + ratpoison environment.
```