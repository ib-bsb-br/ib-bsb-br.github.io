---
tags: [scratchpad]
info: aberto.
date: 2025-08-30
type: post
layout: post
published: true
slug: galaxy-a34-custom-rom
title: 'Galaxy A34 custom ROM'
---
1) Device identification (from your screenshots)
- Manufacturer: Samsung
- Model: Galaxy A34 5G
- Exact model number: SM‑A346M/DSN (Dual SIM; CSC ZTO indicates Brazil open market)
- Software shown: Android 15; One UI 7.0; Android security patch: 1 July 2025; Build/baseband series A346M…DYG1; Phone status: “Oficial” (bootloader not unlocked)
- Likely codename: a34x (confirm with: adb shell getprop ro.product.device and ro.product.vendor.device)
- SoC: MediaTek Dimensity 1080 (relevant for aftermarket support constraints)

2) Core concepts and how they relate to custom ROMs
- Bootloader unlocking: Removes OEM signature enforcement so unsigned images can boot. On Samsung, unlocking is official, wipes data, and permanently trips KNOX (0x1), disabling Samsung Wallet, Secure Folder, and some enterprise features.
- Recovery (stock vs custom): Stock recovery is limited. Custom recovery (e.g., TWRP) enables flashing images/ZIPs, Nandroid backups, and advanced wipes. Samsung devices use Download Mode + Odin/Heimdall for flashing; they do not have standard fastboot.
- Root (Magisk): Optional and independent from installing a ROM/GSI. Commonly done by patching the boot image. Root can help with app workarounds (DenyList) but may affect Play Integrity and security posture.
- AVB/dm‑verity (vbmeta): Verified Boot enforces integrity. Running a GSI often requires disabling verification (flashing a vbmeta with verification/verity disabled).
- Odin/Heimdall vs fastboot: Samsung requires Odin (Windows) or Heimdall (open-source, sometimes less reliable on newer devices). Standard fastboot commands are not available.

3) Compatible custom OS options for SM‑A346M
- Android-based GSIs (Treble, arm64-ab images):
  • PixelOS / Pixel Experience GSI (Pixel-like UX with GMS)
  • LineageOS GSI (AOSP-based with Lineage extras; GApps optional)
  • PHH AOSP GSI (baseline reference GSI)
  • Evolution X GSI (Pixel base with extensive customization)
  Notes: Hardware support depends on Samsung’s vendor; common gaps include IMS/VoLTE/VoWiFi, advanced camera features, fingerprint behavior, NFC.
- Stock-based One UI “debloated”/modded ROMs (if available for A346x):
  • Built from Samsung firmware; retain most hardware features; fewer UX changes; still require unlocking (KNOX 0x1).
- Linux-based mobile OS:
  • Ubuntu Touch and postmarketOS: No known stable, daily-driver ports for Galaxy A34 5G as of commonly available project device lists. Treat any claims as experimental; expect missing telephony/camera/sensors.

4) Comparative analysis (features/stability/usability/community)
- PixelOS / Pixel Experience GSI
  • Features/stability/performance: Pixel UX with integrated Google apps; often polished if vendor supports essentials; potential gaps in IMS/camera/UDFPS on Samsung MTK.
  • Install/user-friendliness: Moderate; similar to other GSIs; out-of-box usability can be high if core hardware works.
  • Development/community: Active projects; GSI tracks vary by maintainer; broad generic support, fewer device-specific fixes.
- LineageOS GSI
  • Features/stability/performance: Clean AOSP+Lineage features; good performance; similar device-specific caveats.
  • Install/user-friendliness: Moderate; GApps optional; privacy-friendly.
  • Development/community: Strong lineage ecosystem; GSI builds are community-driven; support depends on maintainer.
- PHH AOSP GSI
  • Features/stability/performance: Baseline GSI; often gets treble fixes early; performance good when hardware cooperates.
  • Install/user-friendliness: Moderate; good for testing baseline compatibility.
  • Development/community: Very active upstream; device-specific contributions vary.
- Evolution X GSI
  • Features/stability/performance: Extensive customization atop Pixel base; may introduce additional complexity.
  • Install/user-friendliness: Moderate; more toggles/settings in daily use.
  • Development/community: Generally active; verify current GSI status for A34 specifically.
- Stock-based One UI debloated ROMs (A346x)
  • Features/stability/performance: Highest chance of keeping camera quality, IMS, fingerprint reliability; performance similar/slightly better due to debloat.
  • Install/user-friendliness: Often simpler via Odin; closest to stock daily experience.
  • Development/community: Availability varies; fewer device-specific ROMs for Samsung MTK midrange vs Snapdragon flagships.

5) General high-level installation procedure (Samsung-specific), including a concrete PixelOS GSI path
Preparation
- Back up all data (unlocking wipes device).
- Battery ≥70%. Install Android Platform-Tools (adb), Samsung USB Driver, Odin (Windows) or Heimdall (Linux/macOS).
- Download full stock firmware for SM‑A346M with your CSC (e.g., ZTO) to allow recovery if needed.
- Enable Developer options; toggle OEM unlocking (may require network connection and time).

Unlock bootloader (irreversible KNOX 0x1)
- Power off. Enter Download Mode (hold Volume Up + Volume Down while connecting USB).
- Long-press Volume Up to unlock; confirm. Device wipes and reboots.
- Minimal setup; verify OEM unlocking shows unlocked.

Low-risk test (if available): DSU Loader
- Developer options → DSU Loader: temporarily boot a PixelOS/PHH GSI without permanent flashing. Test telephony, data, Wi‑Fi/BT, camera, fingerprint. Note: DSU availability may be limited by firmware.

Concrete install: PixelOS GSI via TWRP (requires verified working TWRP for a34x)
- Flash TWRP with Odin
  • Download Mode → Odin: Options: check F. Reset Time; uncheck Auto Reboot.
  • AP: select TWRP .tar for a34x → Start → PASS.
  • Exit Download Mode (Vol Down + Power), then immediately boot to recovery (Vol Up + Power) to prevent stock recovery restore.
- In TWRP: prepare data
  • Allow modifications → Wipe → Format Data (type yes) → Reboot → Recovery.
- Disable AVB/verity (vbmeta)
  • On PC with avbtool:
    - avbtool make_vbmeta_image --output vbmeta_disabled.img --disable_verification --disable_verity
    - tar -H ustar -cvf vbmeta_disabled.tar vbmeta_disabled.img (rename inside tar to vbmeta.img if needed by your Odin packaging)
  • Reboot phone to Download Mode from TWRP → Odin AP: select vbmeta_disabled.tar → Start → PASS.
  • Boot back to TWRP (timed key combo as above).
- Flash PixelOS GSI
  • Copy PixelOS system.img (arm64-ab) to phone (MTP or adb push).
  • TWRP → Install → Install Image → select system.img → choose System Image → swipe to flash.
  • (Optional) Wipe → Advanced Wipe → Dalvik/ART Cache and Cache.
  • Reboot → System. First boot may take 10–15 minutes.
- Post-install checks
  • Test calls/SMS, mobile data/APN, Wi‑Fi/BT/GPS, cameras, mic/speakers, UDFPS, NFC, sensors, IMS (VoLTE/VoWiFi), Play Integrity/DRM apps.
- Updates (dirty flash)
  • Reboot to TWRP → Install Image → flash new PixelOS system.img to System Image → wipe Dalvik/Cache (optional) → reboot.
- Rollback to stock
  • Download Mode → Odin: flash stock BL/AP/CP/CSC (use CSC to full-wipe if necessary) → Start → PASS → reboot. KNOX remains 0x1 permanently.

If no verified TWRP exists for a34x
- Do not proceed with full flashing. Use DSU to evaluate GSIs. Avoid manual super partition repacks unless following a trusted, device-specific guide; risk of hard brick is high.

6) Significant risks
- KNOX 0x1: Permanent; disables Samsung Wallet, Secure Folder, some enterprise features even after relocking.
- Warranty/service: Likely voided by unlocking/rooting.
- Bricking: Soft bricks recoverable via Odin; hard bricks (no Download Mode) may require hardware repair.
- Data loss: Unlocking and some flashes wipe data.
- Functionality regressions on GSIs: IMS/VoLTE/VoWiFi, advanced camera features, UDFPS, NFC, and DRM levels may degrade or fail.
- Security posture: Verified Boot guarantees weakened; Play Integrity may fail; some banking/streaming apps may not work.
- EFS/modem risk: Do not touch EFS/modem partitions; corruption can break IMEI/baseband.

7) Device-specific resources (verify current status for A34 5G/SM‑A346x)
- XDA Developers forums (search device-specific threads): https://forum.xda-developers.com/
- TWRP devices list (check if A34 5G is supported): https://twrp.me/Devices/
- PHH Treble docs/issues (GSI guidance): https://github.com/phhusson/treble_experimentations
- Android Platform-Tools (adb): https://developer.android.com/tools/releases/platform-tools
- Odin (Windows; obtain from reputable sources) and Samsung USB Driver (Samsung support portals)
- Heimdall (open-source flashing tool): https://github.com/Benjamin-Dobell/Heimdall
- Ubuntu Touch devices: https://devices.ubuntu-touch.io/
- postmarketOS devices: https://wiki.postmarketos.org/wiki/Devices
- Stock firmware (for recovery): use reputable firmware repositories for SM‑A346M with your CSC (e.g., ZTO)

ABNT-style references
- GOOGLE. Android Platform-Tools (adb). Available at: <https://developer.android.com/tools/releases/platform-tools>. Accessed on: 30 August 2025.
- TWRP. Team Win Recovery Project – Devices. Available at: <https://twrp.me/Devices/>. Accessed on: 30 August 2025.
- XDA DEVELOPERS. Forums. Available at: <https://forum.xda-developers.com/>. Accessed on: 30 August 2025.
- PHHUSSON. Treble Experimentations. Available at: <https://github.com/phhusson/treble_experimentations>. Accessed on: 30 August 2025.
- HEIMDALL. Heimdall flashing tool. Available at: <https://github.com/Benjamin-Dobell/Heimdall>. Accessed on: 30 August 2025.
- UBPORTS. Ubuntu Touch devices. Available at: <https://devices.ubuntu-touch.io/>. Accessed on: 30 August 2025.
- POSTMARKETOS. Devices list. Available at: <https://wiki.postmarketos.org/wiki/Devices>. Accessed on: 30 August 2025.

8) Synthesis and recommendation (balancing Linux interest with stability)
- If you prioritize stability and full hardware support: stay on stock One UI or consider a reputable stock-based debloated ROM for A346x (if available). Best chance to retain camera quality, IMS/VoLTE, fingerprint reliability, and DRM levels.
- If you want a different UX and accept trade-offs: trial PixelOS/Pixel Experience or LineageOS GSIs via DSU if available. If essential functions work, proceed with the TWRP-based PixelOS GSI installation flow above, including vbmeta disable. Expect potential IMS/camera/UDFPS quirks.
- Linux OS: For A34 5G, treat Ubuntu Touch/postmarketOS as experimental/unavailable for daily use; consider a secondary, well-supported device if mobile Linux is a primary goal.

Critical precautions
- Back up thoroughly; unlocking wipes data.
- Understand KNOX 0x1 is permanent.
- Keep full stock firmware for SM‑A346M (your CSC) ready for Odin recovery.
- Verify any recovery/ROM is explicitly for a34x/SM‑A346x; avoid cross-device images.
- Verify checksums; download only from original maintainer sources.
- Test essentials immediately after flashing; if critical features fail, roll back to stock.