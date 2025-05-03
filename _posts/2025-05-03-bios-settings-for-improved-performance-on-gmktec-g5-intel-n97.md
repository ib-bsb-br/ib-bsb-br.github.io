---
tags: [scratchpad]
info: aberto.
date: 2025-05-03
type: post
layout: post
published: true
slug: bios-settings-for-improved-performance-on-gmktec-g5-intel-n97
title: 'BIOS settings for improved performance on GMKtec G5 (Intel N97)'
---
Tuning BIOS settings can potentially enhance performance, but it requires careful adjustments and testing, especially on compact systems like the GMKtec G5 with its Intel N97 processor [Intel Alder Lake-N N97 CPU BIOS optimization: organic[1]]. Pushing settings too aggressively can lead to instability, overheating, or reduced component lifespan.

**Important Disclaimers & Prerequisites:**

1.  **Risk:** Modifying BIOS settings beyond defaults carries risks. Proceed at your own discretion. Instability might require resetting the BIOS (CMOS clear, possibly via jumper shorting [User Context]).
2.  **Cooling:** These recommendations assume your GMKtec G5 has adequate cooling. Monitor temperatures closely (e.g., using HWiNFO64) during stress tests. If CPU temperatures consistently exceed LEFTPAREN85-90^\circ CRIGHTPAREN, you *must* relax power limits, voltage offsets, or clock speeds.
3.  **BIOS Version:** Ensure you have the latest GMKtec G5 BIOS installed. Some features, like the 1200 MHz iGPU clock, require specific updates (e.g., build dated May 22 2024 or later [User Context, optimal BIOS settings GMKtec G5 N97 performance: organic[2], optimal BIOS settings GMKtec G5 N97 performance: organic[4]]). Access the BIOS by pressing `Esc` during startup [User Context].
4.  **Incremental Changes:** Apply changes incrementally, testing stability (e.g., with Cinebench R23, Prime95 Small FFTs, 3DMark) after each significant adjustment before proceeding.
5.  **Goal:** These settings aim for higher sustained performance and responsiveness, balancing clock speeds with the N97's thermal and power constraints (12W base TDP [Intel Alder Lake-N N97 CPU BIOS optimization: organic[1], Intel Alder Lake-N N97 CPU BIOS optimization: organic[9]]). They prioritize enabling dynamic boosting mechanisms effectively.

Here are the recommended BIOS settings, categorized by section, targeting improved performance on your GMKtec G5 (Intel N97):

**1. CPU Settings (Advanced → CPU Configuration)**

*   **Turbo Ratio Limits / Performance CPU Ratio:** Ensure Turbo Boost is **Enabled**. If manual ratio control is available, you can *try* setting the max ratio to **36** (for the N97's 3.6 GHz max boost [Intel Alder Lake-N N97 CPU BIOS optimization: organic[1]]). Monitor stability and thermals closely if setting manually. `Auto` is safer.
*   **C-State Control / CPU C-State Support:** **Enabled**. While disabling C-states is common advice for minimizing latency on high-end desktops, a user report for this specific GMKtec G5 N97 suggests enabling C-states is *necessary* for the CPU to properly reach its turbo boost frequencies [optimal BIOS settings GMKtec G5 N97 performance: organic[1]]. Enabling them allows the CPU to enter low-power states when idle, reducing heat and power consumption, which can paradoxically help sustain boost clocks longer under load in a thermally constrained system.
*   **Intel SpeedStep Technology (EIST):** **Enabled**. This allows the CPU to dynamically adjust its clock speed based on load, which is essential for managing power consumption and heat. Disabling it forces high clocks constantly, likely leading to faster thermal throttling and potentially *lower* sustained performance.
*   **Hyper-Threading Technology:** **Enabled** (The N97 is 4 Cores / 4 Threads, so this specific setting might not be present or applicable as it doesn't have Hyper-Threading like Core i-series CPUs, but ensure core enablement reflects 4C/4T).
*   **CPU Voltage Offset:** Start with **Auto** or **0 mV**. If experiencing instability at target clocks/power limits, *or* if trying to slightly *reduce* heat, you can cautiously experiment with small offsets *if the BIOS permits*. Try LEFTPAREN \pm 10 RIGHTPARENmV to LEFTPAREN \pm 25 RIGHTPARENmV increments, testing thoroughly after each change. Positive offset LEFTPAREN (+) RIGHTPAREN *might* improve stability at higher clocks but increases heat/power. Negative offset LEFTPAREN (-) RIGHTPAREN reduces heat/power but might reduce stability. Granularity might differ from the "±100 MHz" mentioned for frequency [User Context].
*   **Power Limits (PL1/PL2):** This is critical for performance in thermally limited systems.
    *   **Package Power Limit 2 (PL2):** Set to **15W** to **18W**. This defines the short-term boost power. Start lower (15W) [Intel Alder Lake-N N97 CPU BIOS optimization: organic[2]] and increase only if thermals remain under control during bursts (e.g., application loading, short benchmarks).
    *   **Package Power Limit 1 (PL1):** Set to **12W** to **15W**. This defines the sustained power limit. Matching it to the N97's base TDP (12W [Intel Alder Lake-N N97 CPU BIOS optimization: organic[1]]) is the safest start. You can try increasing towards your stable PL2 value (e.g., 15W) if cooling allows sustained operation without throttling.
    *   **PL1 Time Window (Tau):** Leave at **Auto** or **28 seconds** if configurable. This determines how long PL2 can be maintained before dropping to PL1.
*   **AVX Ratio Offset:** Set to **0** or **Auto**. Setting 0 ensures AVX workloads run at the full target frequency, but monitor heat as AVX instructions are power-hungry.

**2. Memory (Advanced → DRAM Configuration)**

*   **XMP Profile:** Select **Profile 1** (or the highest available profile) if using compatible DDR5-4800 SODIMMs [User Context] to automatically configure optimal frequency, timings, and voltage (likely 1.1V or slightly higher per XMP spec).
*   **Memory Frequency:** Ensure it's running at **DDR5-4800 MHz**. If XMP doesn't work or isn't available, set this manually.
*   **Timings (tCL, tRCD, tRP, tRAS):** Leave on **Auto** or XMP defaults unless you are experienced with manual memory tuning. Tighter timings offer minor gains but risk instability.
*   **Command Rate:** **Auto** (often defaults to 2T for compatibility, 1T might be slightly faster but harder to stabilize).

**3. Integrated GPU (Advanced → North Bridge or System Agent Configuration)**

*   **iGPU Maximum Frequency Override:** If available and you have the updated BIOS, set to **1200 MHz** [User Context, optimal BIOS settings GMKtec G5 N97 performance: organic[2]]. Leave on Auto if unsure or using an older BIOS.
*   **DVMT Pre-Allocated:** **Auto** or **256MB**. The operating system will dynamically allocate more memory as needed (up to half the system RAM typically). Setting higher pre-allocation (e.g., 512MB) is usually unnecessary unless specific applications demand it.
*   **iGPU Power Limit:** If tunable, set to the **Maximum** available setting or leave on **Auto**.

**4. Storage & I/O (Advanced → Onboard Devices Configuration)**

*   **M.2 PCIe Link Speed:** Ensure set to **Gen4 x4** for maximum NVMe SSD performance [User Context].
*   **SATA Mode Selection:** **AHCI** (unless you specifically set up a RAID array, which is unlikely in this mini-PC).
*   **USB Port Configuration:** Leave **Enabled** unless you have a specific reason to disable a port. Disabling unused USB 2.0 ports offers negligible performance benefits [Previous Response Analysis].

**5. Boot (Boot → Boot Configuration)**

*   **Fast Boot / Quick Boot:** **Enabled** to speed up POST [User Context].
*   **CSM (Compatibility Support Module):** **Disabled** for pure UEFI boot (required for features like Secure Boot and generally preferred for modern OSes).
*   **Boot Order:** Set your primary OS drive (NVMe SSD) as the first boot device.

**6. Security & Virtualization (Security → Security Settings)**

*   **TPM Device Selection / Security Device Support:** **Enabled** (Set to Intel PTT - Platform Trust Technology [User Context]) for Windows 11 compatibility and security features like BitLocker.
*   **Intel Virtualization Technology (VT-x):** **Enabled** [User Context]. Disabling this offers minimal (if any) power savings [Previous Response Analysis] and prevents running virtual machines or WSL2/Hyper-V. Leave it enabled unless you are certain you will *never* need virtualization.

**7. Power Management (Advanced → ACPI Settings or Platform Power Management) (Continued)**

*   **ACPI Sleep State / Standby Mode:** Leave at **Auto** or enable **S3 (Suspend to RAM)** or **Modern Standby/S0ix Low Power Idle** if available and desired [User Context]. Disabling sleep states hinders power saving during idle or sleep periods and often has no benefit for peak performance. While disabling might slightly speed up wake times, it comes at the cost of higher power drain when the system is supposed to be sleeping. Keep defaults unless you encounter specific issues with sleep/wake functionality.
*   **Wake-on-LAN (WOL):** **Disabled** unless you specifically need this feature.
*   **ErP Ready:** **Disabled** usually allows USB power during S5/S4 states (for charging, etc.). Enable ErP for stricter power saving in off/hibernate states (often disables USB power). Set according to your preference; minimal performance impact.

**8. Saving, Testing, and Verification**

*   **Save Changes:** Once you have configured the settings, navigate to the **Save & Exit** menu, select **Save Changes and Reset** (or similar wording), and confirm. The system will reboot with the new settings applied.
*   **Stress Testing:** This is crucial. After booting into the OS, run stability tests to ensure the system can handle sustained load with the new settings:
    *   **CPU:** Prime95 (Small FFTs test for maximum heat/power) or Cinebench R23 (multi-core test run for 10-30 minutes).
    *   **GPU:** FurMark or Unigine Heaven/Superposition benchmark loops.
    *   **Combined:** Run a demanding game or application, or a simultaneous CPU and GPU test (though less common).
*   **Monitoring:** While stress testing, use monitoring software like **HWiNFO64** (Sensors window) to watch:
    *   **CPU Temperatures:** Core temperatures should ideally stay below LEFTPAREN85-90^\circ CRIGHTPAREN under sustained load. Consistent temperatures above this indicate inadequate cooling or overly aggressive settings.
    *   **CPU Clock Speeds:** Verify if the CPU reaches and sustains the expected boost clocks (up to 3.6 GHz for brief periods, potentially lower sustained clocks depending on PL1 and thermals).
    *   **Power Consumption:** Observe Package Power to see if it respects the PL1/PL2 limits you set.
    *   **Throttling:** Check for flags indicating Thermal Throttling, Power Limit Throttling (PL1/PL2), or Current/EDP Limit Throttling. If throttling occurs frequently, you may need to lower power limits, reduce voltage offset, or improve cooling.
*   **Troubleshooting:** If the system becomes unstable (crashes, fails to boot):
    *   Re-enter the BIOS and revert the last change you made.
    *   If you cannot enter the BIOS, you may need to perform a **CMOS reset**. This usually involves unplugging the PC, removing the small coin-cell battery from the motherboard for a minute, or shorting specific "CMOS_CLR" jumper pins/pads on the motherboard as per the GMKtec G5 manual or documentation [User Context]. This will restore BIOS settings to factory defaults.

Remember, BIOS tuning is an iterative process. The optimal settings for your specific GMKtec G5 might require some experimentation based on your cooling, silicon lottery, and workload. Start with these recommendations and adjust based on careful testing and monitoring. Good luck!