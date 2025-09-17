---
tags: [scratchpad]
info: aberto.
date: 2025-05-28
type: post
layout: post
published: true
slug: root-partition
title: 'Low Root Partition Space on rk3588'
---

{% codeblock bash %}
#!/bin/bash
set -euo pipefail

# ==============================================================================
# Overcoming Low Root Partition Space on rk3588 (Debian 11 / ARM64)
# Phases implemented: Assessment, Cleanup (Phase 2), Analysis (Phase 3),
# and Optional Directory Relocation via bind mounts / APT config (Phase 4).
#
# Target: Debian 11 (Bullseye) on ARM64 RK3588 bare-metal.
# Run as a regular user with sudo privileges, from your home directory.
#
# Safety:
# - No partitioning or flashing (Phase 5) is performed.
# - Potentially risky steps (kernel purges, directory relocation, deletions,
#   journald persistent-limit changes) require explicit confirmation ("yes").
# - Backups of critical files (e.g., /etc/fstab) are made with timestamps.
#
# Idempotency:
# - Re-checks for installed tools and existing mounts.
# - Avoids duplicate /etc/fstab entries (uses a marker comment).
# - Safe to re-run; will skip completed operations when possible.
# ==============================================================================

# ----------------------------- Configuration ----------------------------------
DEFAULT_TARGETS=("/userdata" "/mnt/mSATA")  # Preferred relocation targets (must be mounted)
FSTAB_MARK="# rk3588-space-tool"            # Marker used to identify fstab entries we add
APT_CONF_FILE="/etc/apt/apt.conf.d/99custom_cache.conf"

# ------------------------------ Utilities -------------------------------------
log()  { echo -e "[INFO ] $*"; }
warn() { echo -e "[WARN ] $*" >&2; }
die()  { echo -e "[ERROR] $*" >&2; exit 1; }

confirm() {
  # Usage: confirm "WARNING message"
  local msg="$1"
  echo "$msg"
  read -r -p "Type 'yes' to proceed (anything else to cancel): " _ans
  [[ "${_ans}" == "yes" ]]
}

ensure_tool_installed() {
  # Usage: ensure_tool_installed <binary> [apt-package-name]
  local bin="$1"
  local pkg="${2:-$1}"
  if ! command -v "$bin" >/dev/null 2>&1; then
    log "Installing required tool: $pkg"
    if ! sudo apt install -y "$pkg"; then
      die "Failed to install package: $pkg"
    fi
  fi
}

timestamp() { date +%Y%m%d%H%M%S; }

backup_file() {
  # Usage: backup_file /path/to/file
  local path="$1"
  if [[ -f "$path" ]]; then
    local bak="${path}.bak.$(timestamp)"
    if ! sudo cp -a "$path" "$bak"; then
      die "Failed to backup $path to $bak"
    fi
    log "Backed up $path to $bak"
  fi
}

# ------------------------ Target mount selection ------------------------------
detect_or_choose_target() {
  local chosen=""
  # Prefer default targets if mounted
  for t in "${DEFAULT_TARGETS[@]}"; do
    if mountpoint -q "$t"; then
      chosen="$t"
      break
    fi
  done

  if [[ -z "$chosen" ]]; then
    echo
    warn "No default relocation targets are mounted (${DEFAULT_TARGETS[*]})."
    echo "Available mounts:"
    if ! df -Th; then die "Failed to list filesystems."; fi
    read -r -p "Enter an existing, mounted directory to use as relocation base (or leave blank to skip Phase 4): " custom
    if [[ -n "${custom:-}" ]]; then
      if mountpoint -q "$custom"; then
        chosen="$custom"
      else
        warn "'$custom' is not a mount point. Skipping Phase 4."
      fi
    fi
  fi
  echo "$chosen"
}

# --------------------------- Kernel management --------------------------------
list_installed_kernel_pkgs() {
  # Lists versioned linux-image packages (avoid meta packages)
  dpkg -l 'linux-image-[0-9]*' 2>/dev/null | awk '/^ii/ {print $2}'
}

pick_kernels_to_purge() {
  # Excludes current kernel and retains one fallback (highest remaining version)
  local current="$(uname -r)"
  mapfile -t imgs < <(list_installed_kernel_pkgs)
  # Filter out current
  local candidates=()
  for p in "${imgs[@]}"; do
    [[ "$p" == *"$current"* ]] && continue
    candidates+=("$p")
  done
  if (( ${#candidates[@]} == 0 )); then
    echo ""
    return 0
  fi
  # Keep the highest version as fallback
  local highest
  highest="$(printf '%s\n' "${candidates[@]}" | sort -V | tail -1)"
  local to_purge=()
  for p in "${candidates[@]}"; do
    [[ "$p" == "$highest" ]] && continue
    to_purge+=("$p")
  done
  printf "%s\n" "${to_purge[@]}"
}

# ------------------------- Journald configuration -----------------------------
maybe_set_journald_limits() {
  echo
  read -r -p "Set persistent journald limits (e.g., SystemMaxUse=200M, SystemKeepFree=200M)? (yes/NO): " jset
  if [[ "$jset" != "yes" ]]; then
    log "Skipping persistent journald limits."
    return 0
  fi

  local conf="/etc/systemd/journald.conf"
  backup_file "$conf"

  # Ensure keys exist or are updated (uncomment and set values)
  local tmp="$(mktemp)"
  if ! sudo cp -a "$conf" "$tmp"; then
    die "Failed to copy $conf to $tmp"
  fi

  # Update or append settings
  sudo awk '
    BEGIN { sysmax=0; keepfree=0; }
    /^#?SystemMaxUse=/ { print "SystemMaxUse=200M"; sysmax=1; next }
    /^#?SystemKeepFree=/ { print "SystemKeepFree=200M"; keepfree=1; next }
    { print }
    END {
      if (!sysmax) print "SystemMaxUse=200M";
      if (!keepfree) print "SystemKeepFree=200M";
    }
  ' "$tmp" | sudo tee "$conf" >/dev/null || die "Failed to update $conf"

  if ! sudo systemctl restart systemd-journald; then
    die "Failed to restart systemd-journald after updating limits"
  fi
  log "Configured journald limits and restarted systemd-journald."
}

# ---------------------------- Relocation helpers ------------------------------
safe_service_stop_if_present() {
  # Stop a service if it exists (ignore errors). Usage: safe_service_stop_if_present rsyslog
  local svc="$1"
  if sudo systemctl list-unit-files | awk '{print $1}' | grep -qx "${svc}.service"; then
    sudo systemctl is-active --quiet "$svc" && sudo systemctl stop "$svc" || true
  fi
}

safe_service_start_if_present() {
  local svc="$1"
  if sudo systemctl list-unit-files | awk '{print $1}' | grep -qx "${svc}.service"; then
    sudo systemctl start "$svc" || true
  fi
}

ensure_rsync() { ensure_tool_installed rsync rsync; }

append_fstab_bind_once() {
  # Usage: append_fstab_bind_once <src> <dst>
  local src="$1" dst="$2"
  local line="$src $dst none bind,nofail 0 0 $FSTAB_MARK"
  backup_file /etc/fstab
  if grep -Fq "$FSTAB_MARK" /etc/fstab | grep -q "."; then
    :
  fi
  if grep -Eq "^[^#]*[[:space:]]${dst}[[:space:]]" /etc/fstab; then
    log "fstab already contains a mount for $dst; not adding duplicate."
  else
    echo "$line" | sudo tee -a /etc/fstab >/dev/null || die "Failed to append bind mount to /etc/fstab"
    log "Added bind mount to /etc/fstab: $line"
  fi
}

relocate_bind() {
  # Usage: relocate_bind <source_dir> <base_target_mount>
  # Copies source to base_target_mount/<safe_name>, bind-mounts back, updates fstab.
  local src="$1"
  local base="$2"

  [[ -d "$src" ]] || die "Source directory does not exist: $src"
  mountpoint -q "$src" && { warn "$src is already a mount point; skipping."; return 0; }
  ensure_rsync

  # Disallow critical system dirs (never relocate)
  case "$src" in
    /|/bin|/sbin|/lib|/lib32|/lib64|/libx32|/etc|/dev|/proc|/sys|/run|/boot)
      die "Refusing to relocate critical system directory: $src"
      ;;
  esac

  local safe_name
  safe_name="$(echo "$src" | sed 's#^/##; s#[/ ]#_#g')"
  local dst="${base}/${safe_name}"

  log "Preparing relocation of $src -> $dst (via bind mount)"

  if ! confirm "WARNING: Relocating $src. A copy will be made to $dst and then bind-mounted back. Proceed?"; then
    warn "User cancelled relocation of $src."
    return 0
  fi

  if ! sudo mkdir -p "$dst"; then die "Failed to create destination $dst"; fi

  # Special handling for /var/log (quiesce rsyslog; minimize journald writes)
  if [[ "$src" == "/var/log" ]]; then
    safe_service_stop_if_present rsyslog
    sudo journalctl --flush || true
  fi

  log "Copying data from $src to $dst (preserving permissions, xattrs, ACLs)..."
  if ! sudo rsync -aAX --delete "$src"/ "$dst"/; then
    [[ "$src" == "/var/log" ]] && safe_service_start_if_present rsyslog
    die "rsync failed when copying $src to $dst"
  fi

  local backup="${src}.old.$(timestamp)"
  log "Renaming original $src to $backup ..."
  if ! sudo mv "$src" "$backup"; then
    [[ "$src" == "/var/log" ]] && safe_service_start_if_present rsyslog
    die "Failed to rename $src to $backup"
  fi

  if ! sudo mkdir -p "$src"; then
    sudo mv "$backup" "$src" || true
    [[ "$src" == "/var/log" ]] && safe_service_start_if_present rsyslog
    die "Failed to create mount point $src"
  fi

  log "Bind-mounting $dst onto $src ..."
  if ! sudo mount --bind "$dst" "$src"; then
    warn "Bind mount failed; attempting rollback..."
    sudo rm -rf "$src" || true
    sudo mv "$backup" "$src" || true
    [[ "$src" == "/var/log" ]] && safe_service_start_if_present rsyslog
    die "Bind mount failed for $src"
  fi

  append_fstab_bind_once "$dst" "$src"

  # Restart services if needed
  if [[ "$src" == "/var/log" ]]; then
    if ! sudo systemctl restart systemd-journald; then
      warn "Failed to restart systemd-journald."
    fi
    safe_service_start_if_present rsyslog
  fi

  # Verify
  if ! mountpoint -q "$src"; then
    die "Verification failed: $src is not a mount point after relocation"
  fi

  log "Relocation of $src completed successfully."
  echo "A backup of the original directory remains at: $backup"
  if confirm "OPTIONAL: Delete the backup $backup now to free space? (Irreversible)"; then
    if ! sudo rm -rf "$backup"; then
      warn "Failed to remove backup $backup; please remove manually later."
    else
      log "Backup $backup removed."
    fi
  else
    log "Backup retained at $backup."
  fi
}

relocate_apt_cache() {
  # Usage: relocate_apt_cache <base_target_mount>
  local base="$1"
  local new_dir="${base}/apt_cache"
  log "Configuring APT cache to use: $new_dir"

  if ! sudo mkdir -p "${new_dir}/partial"; then
    die "Failed to create ${new_dir}/partial"
  fi

  backup_file "$APT_CONF_FILE"

  # Inspect existing settings across apt.conf.d
  local existing
  existing="$(grep -RhoE '^\s*Dir::Cache::Archives\s+"[^"]+"/;' /etc/apt/apt.conf.d 2>/dev/null || true)"

  if [[ -n "$existing" ]]; then
    echo "Existing APT cache dir setting(s):"
    echo "$existing"
    if ! confirm "Update APT cache directory to ${new_dir}/ in all occurrences?"; then
      warn "User chose not to update APT cache settings."
      return 0
    fi
    # Update all occurrences to point at the new path
    while IFS= read -r file; do
      backup_file "$file"
      sudo sed -i -E "s|^\s*Dir::Cache::Archives\s+\"[^\"]+\";|Dir::Cache::Archives \"${new_dir}/\";|g" "$file" || die "Failed to update $file"
    done < <(grep -Rl 'Dir::Cache::Archives' /etc/apt/apt.conf.d 2>/dev/null || true)
  else
    # Create our own conf if none exists
    echo "Dir::Cache::Archives \"${new_dir}/\";" | sudo tee "$APT_CONF_FILE" >/dev/null || die "Failed to write $APT_CONF_FILE"
    log "Created $APT_CONF_FILE to set APT cache directory."
  fi

  # Optionally move current cache contents
  if ls -1 /var/cache/apt/archives/*.deb >/dev/null 2>&1; then
    if confirm "Move existing .deb files from /var/cache/apt/archives to ${new_dir}/ ?"; then
      ensure_rsync
      if ! sudo rsync -a --remove-source-files /var/cache/apt/archives/*.deb "${new_dir}/"; then
        warn "Failed to move some .deb files; you can move them manually."
      fi
    fi
  fi

  # Clean old cache location’s partial
  sudo rm -rf /var/cache/apt/archives/partial/* 2>/dev/null || true
  log "APT cache relocation configured."
}

# ------------------------------- Main Flow ------------------------------------
log "Starting low disk space mitigation tool for RK3588 (Debian 11)."
echo
log "Phase 1: Assessment (df -Th, lsblk, journal disk-usage)"
if ! df -Th; then die "df -Th failed"; fi
echo "-------------------------------------------"
if ! lsblk; then die "lsblk failed"; fi
echo "-------------------------------------------"
if command -v journalctl >/dev/null 2>&1; then
  sudo journalctl --disk-usage || true
fi

# Phase 2: Cleanup
echo
log "Phase 2: Standard System Cleanup"
initial_avail_kb="$(df -k / | awk 'NR==2{print $4}')"
initial_use_pct="$(df -h / | awk 'NR==2{print $5}')"

log "Cleaning APT cache..."
if ! sudo apt clean; then die "apt clean failed"; fi

log "Removing orphaned packages..."
if ! sudo apt autoremove --purge -y; then die "apt autoremove --purge failed"; fi

# Optional old kernel purge
mapfile -t purge_list < <(pick_kernels_to_purge || true)
if (( ${#purge_list[@]} > 0 )); then
  echo "Old kernel packages that can be purged (keeping current and one fallback):"
  printf '  %s\n' "${purge_list[@]}"
  if confirm "Purge the above old kernel packages now?"; then
    # try to purge headers matching those images as well
    headers=()
    for img in "${purge_list[@]}"; do
      hdr="${img/linux-image/linux-headers}"
      dpkg -s "$hdr" >/dev/null 2>&1 && headers+=("$hdr") || true
    done
    log "Purging: ${purge_list[*]} ${headers[*]:-}"
    if ! sudo apt purge -y "${purge_list[@]}" "${headers[@]:-}"; then
      warn "Some kernel packages failed to purge."
    fi
  else
    log "Skipping old kernel purge."
  fi
else
  log "No old kernel packages found to purge."
fi

# Journal vacuum (non-destructive to active logs)
log "Vacuuming journal logs older than 7 days (if persistent journaling is enabled)..."
sudo journalctl --vacuum-time=7d || true

# Clean /var/tmp (older than 7 days)
log "Cleaning files older than 7 days in /var/tmp ..."
sudo find /var/tmp -type f -mtime +7 -print -delete || warn "Some /var/tmp files could not be removed."

# Summarize freed space
final_avail_kb="$(df -k / | awk 'NR==2{print $4}')"
freed_kb=$(( final_avail_kb - initial_avail_kb ))
freed_mb=$(( freed_kb / 1024 ))
final_use_pct="$(df -h / | awk 'NR==2{print $5}')"
log "Cleanup complete. Freed approximately ${freed_mb} MB (root usage: $initial_use_pct -> $final_use_pct)."

# Offer persistent journald limits
maybe_set_journald_limits

# Phase 3: Analysis
echo
log "Phase 3: Disk Usage Analysis (top directories/files on /)"
ensure_tool_installed numfmt coreutils
echo "Top 15 directories under / (one level):"
sudo du -x -k -d1 / 2>/dev/null | sort -rn | head -n 15 | numfmt --to=iec --field 1 || warn "Directory size listing failed."
echo "-------------------------------------------"
echo "Top 15 directories under /var (one level):"
sudo du -x -k -d1 /var 2>/dev/null | sort -rn | head -n 15 | numfmt --to=iec --field 1 || true
echo "-------------------------------------------"
echo "Largest files on / (>500M):"
sudo find / -xdev -type f -size +500M -printf '%s %p\n' 2>/dev/null | sort -nr | head -n 15 | numfmt --to=iec --field 1 || true

# ncdu (interactive)
if confirm "OPTIONAL: Launch ncdu (interactive) to explore disk usage on / now? (You can quit ncdu with 'q')"; then
  ensure_tool_installed ncdu ncdu
  sudo ncdu -x /
fi

# Phase 4: Optional Relocation
echo
log "Phase 4: Optional Directory Relocation (bind mounts / APT cache)"
RELOC_BASE="$(detect_or_choose_target)"
if [[ -z "$RELOC_BASE" ]]; then
  log "No relocation base selected. Skipping Phase 4."
  log "All done."
  exit 0
fi

# Show target capacity
log "Relocation target: $RELOC_BASE"
df -Th "$RELOC_BASE" || warn "Could not show target filesystem capacity."

if ! confirm "IMPORTANT: Ensure you have backups. Proceed with relocation tasks on '$RELOC_BASE'?"; then
  log "User skipped Phase 4."
  exit 0
fi

# Menu-driven relocation loop
while true; do
  echo
  echo "Choose a relocation task (base: $RELOC_BASE):"
  echo "  1) Relocate APT cache (/var/cache/apt/archives) using apt.conf"
  echo "  2) Relocate /var/log (bind mount)"
  echo "  3) Relocate /opt (bind mount)"
  echo "  4) Relocate /usr/local (bind mount)"
  echo "  5) Relocate /srv (bind mount)"
  echo "  6) Relocate a custom directory (bind mount)"
  echo "  7) Done (exit Phase 4)"
  read -r -p "Enter choice [1-7]: " choice
  case "$choice" in
    1)
      relocate_apt_cache "$RELOC_BASE"
      ;;
    2)
      relocate_bind "/var/log" "$RELOC_BASE"
      ;;
    3)
      relocate_bind "/opt" "$RELOC_BASE"
      ;;
    4)
      relocate_bind "/usr/local" "$RELOC_BASE"
      ;;
    5)
      relocate_bind "/srv" "$RELOC_BASE"
      ;;
    6)
      read -r -p "Enter absolute directory path to relocate (e.g., /var/lib/myapp): " custom_src
      if [[ -z "${custom_src:-}" || "${custom_src:0:1}" != "/" ]]; then
        warn "Please enter an absolute path."
      else
        relocate_bind "$custom_src" "$RELOC_BASE"
      fi
      ;;
    7)
      break
      ;;
    *)
      warn "Invalid choice. Please select 1-7."
      ;;
  esac
done

echo
log "Post-relocation verification:"
df -Th /
df -Th "$RELOC_BASE" || true
mount | grep -E "(/var/log|/opt|/usr/local|/srv)" || true

log "Completed. Consider rebooting to validate persistent mounts and confirm system logging is healthy."
exit 0
{% endcodeblock %}

## **1\. Introduction: Addressing Root Partition Space on rk3588**

### **Overview of the Low Space Issue**

This guide addresses the common and critical issue of low disk space on the root partition (/dev/root) of rk3588-based arm64 machines running Debian Bullseye. A reported usage of 81% on /dev/root signifies an impending problem that can lead to various system malfunctions. These include, but are not limited to, system instability, an inability to install essential updates or new software packages, significant performance degradation, and the potential failure of critical system services. Prompt and methodical action is required to mitigate these risks.

### **Importance of a Methodical Approach for rk3588 Systems**

The rk3588, an advanced ARM System-on-Chip (SoC), is frequently utilized in embedded devices and single-board computers. These systems typically employ eMMC (embedded MultiMediaCard) for primary storage and utilize boot mechanisms such as U-Boot, along with MASKROM or Loader mode for OS flashing via USB OTG. These characteristics differentiate them significantly from standard x86-based personal computers. Direct manipulation of eMMC partitions, particularly the root partition, is inherently more complex and carries substantial risks if not executed with precision and an understanding of the platform's specifics. Such operations often necessitate specialized tools and procedures unique to Rockchip SoCs.1 Attempting to apply standard desktop partitioning tools directly to a live eMMC root partition can lead to an unbootable system.

### **Guide Structure**

This document outlines a phased strategy to reclaim disk space on the /dev/root partition. The approach begins with low-risk, software-based cleanup methods that often yield significant results. It then progresses to more involved techniques, such as identifying and relocating large directories. Finally, it details the high-risk, last-resort option of resizing the root partition through a complete firmware re-flashing process. Each phase will build upon the previous, emphasizing data safety and system integrity throughout.

## **2\. Phase 1: Initial System Assessment and Essential Precautions**

Before attempting any modifications, a thorough assessment of the current system state and implementation of robust backup strategies are paramount. These preliminary steps are crucial for ensuring data integrity and providing a recovery path should any subsequent procedures encounter issues.

### **Verifying Current Disk Usage**

To accurately diagnose the low space condition, it is essential to verify the current disk usage. The following commands provide detailed information about the storage layout and utilization:

* **df \-Th**: This command lists all mounted filesystems, their types (e.g., ext4, btrfs), total size, used space, available space, usage percentage, and mount points. Particular attention should be paid to the entry corresponding to /dev/root or the specific eMMC partition mounted as the root filesystem.  
* **lsblk**: This utility displays block devices (such as eMMC, SD cards, USB drives) in a hierarchical tree format. It helps in identifying the eMMC device, typically named /dev/mmcblkX (where X is a number, e.g., /dev/mmcblk0 or /dev/mmcblk2 2), and its partition structure.

Interpreting the output from these commands will confirm which partition is serving as /dev/root and its current level of capacity utilization.

### **Critical: Data Backup Strategies for rk3588**

**A full and verified backup is an absolute prerequisite before proceeding with any operations beyond basic package cleaning (Phase 3), especially when considering directory relocation (Phase 4\) or partition resizing (Phase 5).**

Backing up eMMC storage on an rk3588 system can present challenges compared to traditional desktop systems. Full, image-level backups often require booting into a separate recovery environment or using platform-specific tools.

**Recommended Backup Methods:**

* **User Data Backup:** At a minimum, all critical user data, typically located in /home, and any custom application data stored in other directories, must be backed up to external storage. This could be a USB drive, a network-attached storage (NAS) device, or a cloud storage solution.  
* **System Configuration:** Key system configuration files, primarily located under /etc, should also be backed up. This includes configurations for networking, installed services, and user accounts.  
* **eMMC Image Backup (Advanced):**  
  * **Using dd from a Live Environment:** If the rk3588 board supports booting from an alternative medium (e.g., an SD card) and that live environment can access the eMMC with appropriate drivers, the dd utility can be used to create a raw image of the eMMC partitions. This method is complex and requires a compatible live system.  
  * **Using rkdeveloptool:** The Rockchip development tool, rkdeveloptool, provides functionality to read individual partitions from the eMMC when the device is in MASKROM or Loader mode.3 The command rkdeveloptool read-partition \<partition\_name\> \<output\_filename.img\> can be used to back up partitions such as uboot, trust, boot, rootfs, and userdata.4 This requires connecting the device to a host PC via USB OTG and booting it into the appropriate low-level mode. Having these raw partition images is invaluable for recovery, especially if partition table modifications are planned.

### **Understanding MASKROM/OTG Flashing Implications**

MASKROM mode is a built-in, low-level recovery mechanism in Rockchip SoCs, including the rk3588. It allows the device to communicate with a host PC via a USB OTG connection for firmware flashing, even if the primary bootloader or operating system is corrupted.1 This mode is the ultimate recovery pathway if the system becomes unbootable due\_to\_errors during advanced space reclamation procedures.

Familiarity with the procedure to enter MASKROM or Loader mode on the specific rk3588 device (often involving pressing and holding a 'RECOVERY' or 'MASKROM' button during power-on or reset while connected via USB OTG 1) is a critical safety net. If operations in Phases 4 or 5 lead to a non-booting system, MASKROM mode provides the means to re-flash the original firmware or a known-good backup, thereby recovering the device. This understanding is directly relevant to the system's design, which includes OS flashing via OTG/MASKROM. This precaution ensures that even if severe issues arise, a path to restoration is available, aligning with best practices for embedded system administration.

## **3\. Phase 2: Standard System Cleanup (Low-Risk, High-Impact)**

This phase focuses on standard Debian system maintenance tasks that are generally safe and can often free up a considerable amount of disk space. These should be the first actions taken to alleviate pressure on the root partition.

### **Leveraging apt for Package Management**

The Advanced Package Tool (APT) is Debian's primary package management system. Over time, its cache and automatically installed dependencies can consume significant disk space.

* **sudo apt update**: Before any cleaning operations, it is essential to update the local package index to ensure APT has the latest information about available packages and their dependencies.  
* **sudo apt clean**: This command removes downloaded Debian package files (.deb) from the APT cache, typically located in /var/cache/apt/archives/.6 These files are retained after package installation and can accumulate, occupying valuable space. This operation is very safe and does not remove any installed packages or their configurations.  
* **sudo apt autoremove \--purge**: This command is crucial for removing packages that were automatically installed to satisfy dependencies for other packages but are no longer required by any installed software.6 The \--purge option ensures that not only are these orphaned packages removed, but their system-wide configuration files are also deleted, further freeing up space.8 This is a standard maintenance task that helps keep the system lean.

### **Managing Linux Kernels**

Debian systems, by default, retain multiple Linux kernel versions. This allows users to boot into an older, known-good kernel if a newer version introduces instability or hardware compatibility issues. However, each kernel image, its corresponding headers, and associated modules consume substantial space, primarily in /boot (which is part of the root partition in many embedded setups) and /lib/modules/.6

* **Identifying Current and Installed Kernels:**  
  * uname \-r: Displays the version of the currently running kernel.8 **It is imperative that this kernel is NOT removed.**  
  * dpkg \-l "linux-image\*" "linux-headers\*" or dpkg \--list | grep linux-image: These commands list all installed kernel image and header packages, showing their status and version.6  
  * ls /boot/: Lists the contents of the /boot directory, which includes kernel image files (typically named vmlinuz-\<version\>) and initial RAM filesystem images (initrd.img-\<version\>).8  
* **Safely Purging Old Kernels:**  
  * While sudo apt autoremove is designed to remove old, unneeded kernels, its behavior can sometimes be inconsistent, occasionally leaving more kernels than necessary or failing to remove any.6 Therefore, manual verification and potential purging are recommended.  
  * **Manual Purge Command:** To remove a specific old kernel and its headers, use: sudo apt purge \<kernel\_image\_package\_name\> \<kernel\_headers\_package\_name\> For example: sudo apt purge linux-image-5.10.0-X-arm64 linux-headers-5.10.0-X-arm64.  
  * **Caution:** It is strongly advised to retain the currently running kernel and at least one other known-good previous kernel version as a fallback.6 Removing all but the current kernel can leave the system unbootable if the active kernel encounters an issue.  
  * The directories under /usr/lib/modules/ corresponding to old and unused kernel versions can also be manually removed if apt purge does not handle them, but this should be done with extreme caution and only after the corresponding kernel packages are purged.7

The variability in apt autoremove's effectiveness for kernel cleanup underscores the need for manual checks. Relying solely on autoremove might not reclaim all possible space from old kernels. A manual review of installed kernels, followed by a careful purge of unneeded older versions (while preserving the running and a backup kernel), is a more reliable strategy for maximizing space recovery from this source.

### **Controlling Systemd Journal Logs**

The systemd-journald service collects and manages system logs. These logs, stored by default in /var/log/journal/ (if persistent storage is enabled) or /run/log/journal/ (for volatile storage), can grow significantly over time, especially on active systems or those with verbose logging configurations.10

* **Assessing Journal Disk Usage:**  
  * sudo journalctl \--disk-usage: This command reports the total disk space currently occupied by archived and active journal files.10  
* **Vacuuming Journal Files (Immediate Cleanup):** journalctl provides options to manually reduce the size of the journal by removing older entries. These operations are non-destructive to currently active log files but will remove archived data.  
  * sudo journalctl \--vacuum-size=XM: Reduces the total size of journal files to a specified limit, e.g., 200M for 200 Megabytes or 1G for 1 Gigabyte.10  
  * sudo journalctl \--vacuum-time=Xd: Deletes archived journal entries older than the specified time period, e.g., 7d for 7 days, 2weeks for two weeks.10  
  * sudo journalctl \--vacuum-files=N: Retains only the N most recent journal files, deleting older ones.10  
* **Persistent Journal Configuration (Long-Term Management):** To prevent excessive log growth in the future, systemd-journald can be configured by editing its configuration file, /etc/systemd/journald.conf. Key parameters for controlling disk usage include 10:  
  * SystemMaxUse=XM: Sets an absolute maximum disk space that persistent journal files can occupy.  
  * SystemKeepFree=YM: Ensures that at least YM of disk space is kept free on the filesystem where the journal is stored.  
  * SystemMaxFileSize=ZM: Limits the maximum size of individual journal files before they are rotated.  
  * RuntimeMaxUse=, RuntimeKeepFree=, RuntimeMaxFileSize=: Similar options for volatile journals stored in /run/log/journal.  
  * Compress=yes: Enables compression for older journal entries, saving space at the cost of some CPU overhead during compression/decompression. After modifying /etc/systemd/journald.conf, the systemd-journald service must be restarted to apply the changes: sudo systemctl restart systemd-journald.

The following table summarizes common journalctl vacuuming options for quick reference:

**Table: Common journalctl \--vacuum-\* Options**

| Option | Description | Example Command |
| :---- | :---- | :---- |
| \--disk-usage | Show current journal disk usage | sudo journalctl \--disk-usage |
| \--vacuum-size=XM | Reduce journal size to X Megabytes/Gigabytes | sudo journalctl \--vacuum-size=500M |
| \--vacuum-time=Xd | Delete logs older than X days/weeks/months | sudo journalctl \--vacuum-time=2weeks |
| \--vacuum-files=N | Keep only the N most recent journal files | sudo journalctl \--vacuum-files=5 |

### **General System File Cleanup**

Beyond package management and system logs, other areas can accumulate unnecessary files:

* /tmp and /var/tmp: These directories are intended for temporary files. While /tmp is often configured as a tmpfs (RAM-based filesystem) and cleared on reboot, /var/tmp typically persists. Old files in /var/tmp can be manually removed.  
* Old Application Logs in /var/log/: Besides the systemd journal, applications may write their own logs to /var/log/. Check for excessively large files (e.g., \*.log.1, \*.gz). Ensure logrotate is properly configured for these applications to manage log file sizes and rotation.  
* User-specific caches: Directories like \~/.cache within user home directories can accumulate large amounts of cached data from applications. While not directly on /dev/root if /home is separate, if /home is part of /dev/root, these should be investigated.

## **4\. Phase 3: Identifying and Analyzing Large Space Consumers**

After performing standard system cleanup, if the root partition space is still critically low, the next step is to identify precisely which directories and files are consuming the most space. This targeted analysis will guide further reclamation efforts.

### **Using ncdu for Interactive Disk Usage Analysis**

ncdu (Ncurses Disk Usage) is a powerful and user-friendly disk usage analyzer that provides an interactive way to navigate the filesystem and identify space hogs.12

* **Installation:** ncdu is available in Debian Bullseye repositories and can be installed using: sudo apt install ncdu The package is available for the arm64 architecture.13  
* **Usage:**  
  * The recommended command to analyze the root filesystem is: sudo ncdu \-x / The \-x option is crucial as it confines the scan to the filesystem of the specified directory (in this case, /), preventing ncdu from traversing into other mounted filesystems (e.g., separate /home, /data, or network mounts).12 This ensures the analysis focuses solely on the root partition's contents.  
  * Upon completion of the scan (which may take some time depending on the size and number of files), ncdu presents a sorted list of files and directories by size.  
  * **Navigation and Interaction** 12**:**  
    * Use the **arrow keys** (up/down) to navigate the list.  
    * Press **Enter** or the **right arrow key** to enter a selected directory and view its contents.  
    * Press the **left arrow key**, h, or \< to go up to the parent directory.  
    * **Sorting:** Press s to sort by size (default), n by name, C by item count, and M (capital M) by modification time. Pressing the sort key again toggles ascending/descending order.  
    * **Deleting:** Press d to delete a selected file or directory (use with extreme caution, especially when running as root). ncdu will ask for confirmation.  
    * **Information:** Press i to show detailed information about the selected item.  
    * **Help:** Press ? to display the built-in help screen.  
* ncdu allows for a quick and effective drill-down into the directory structure to pinpoint the largest consumers of disk space, which might not be obvious from standard du output alone.

### **Alternative Analysis with du and find**

For users who prefer command-line tools for non-interactive analysis or for use in scripts, du (disk usage) and find are standard utilities that can provide similar information.

* To display the total size of top-level directories within the root filesystem, sorted by size in human-readable format: sudo du \-sh /\* | sort \-rh | head \-n 20 This command lists the top 20 largest directories directly under /. The depth can be adjusted (e.g., sudo du \-sh /var/\*) to inspect specific subdirectories.  
* To find individual files larger than a certain size (e.g., 1GB) anywhere on the root filesystem: sudo find / \-xdev \-type f \-size \+1G \-print0 | xargs \-0 du \-h The \-xdev option ensures find does not descend into directories on other filesystems, similar to ncdu \-x. The size (+1G) can be adjusted (e.g., \+500M for 500 Megabytes).

While ncdu offers a more convenient interactive experience, proficiency with du and find remains a valuable skill for system administrators, providing flexibility for various diagnostic scenarios. These tools can help identify large log files, forgotten backups, or unexpectedly large application data directories that were not addressed by the standard cleanup in Phase 2\.

## **5\. Phase 4: Advanced Space Reclamation \- Relocating Directories (Medium to High-Risk)**

If significant space is still required after general cleanup and analysis, relocating large directories from the root partition to another storage location (e.g., a separate userdata partition if available and sufficiently spacious, or an external USB drive) can be an effective strategy. However, this phase involves higher risks and requires careful execution.

### **Disclaimer: Risks and Considerations**

Moving system directories, particularly those under /var or /usr, is a non-trivial operation that can lead to an unbootable system if not performed correctly.14 Several factors contribute to this risk:

* **System Stability:** Critical system services and the boot process itself depend on specific directory structures and file locations. Incorrectly moving these can break dependencies.  
* **Boot Process Dependencies:** Some directories are accessed very early in the boot sequence, potentially before all filesystems (including the target partition for relocation) are mounted. Relocating such directories requires ensuring they are available when needed, often through methods like bind mounts configured in /etc/fstab.  
* **Permissions and Ownership:** File and directory permissions, ownership, and extended attributes (like SELinux contexts or AppArmor profiles, if enabled) must be meticulously preserved during the copy process. Tools like rsync \-aX or cp \-aR are generally suitable for this.14  
* **OTG/MASKROM Awareness:** Given the rk3588 platform, if a directory relocation attempt fails and renders the system unbootable, recovery will likely involve using MASKROM/Loader mode to re-flash the firmware, as discussed in Phase 1\. Users must be prepared for this eventuality.

### **Identifying Suitable Directories for Relocation**

Based on the analysis from Phase 3 (ncdu or du/find), identify large directories that are candidates for relocation.

* **Good candidates often include:**  
  * /var/cache/apt/archives/: Can become very large if not regularly cleaned by apt clean. Relocating this directory or configuring APT to use a different cache location is a common practice.14  
  * /var/log/: If systemd journald configuration is insufficient to control its size, or if other applications generate voluminous logs in this directory.18  
  * /opt/: Frequently used for installing third-party software packages that are not part of the core OS. These can sometimes be quite large and are often safe to move, provided the applications within are not critical for the early boot process.20  
  * /srv/: If the system is used to serve large amounts of data (e.g., web server content, FTP files), this directory might be a candidate.  
  * /usr/local/: Often contains manually compiled software or locally installed packages, which can accumulate.  
  * While /home is usually on a separate partition in server setups, if it resides on the root partition and is large, its relocation methods 16 are directly applicable to other directories.  
* **Poor candidates (generally avoid moving from the root partition):** Core system directories like /bin, /sbin, /lib, /etc, /dev, /proc, /sys, and /run. The /boot directory should also not be moved from the root partition unless it's being migrated to a dedicated boot partition, which is a more complex scenario not covered here for an already installed system.

### **Prerequisites for Relocation**

* **Target Location:** A pre-existing, formatted partition with sufficient free space is required. This could be another partition on the eMMC (e.g., a userdata partition that can be partially repurposed) or an external storage device (e.g., USB drive, NVMe SSD if the rk3588 board supports it).  
* **Caution for rk3588 eMMC:** Creating new partitions or resizing existing ones on the live eMMC boot device without a full re-flash (Phase 5\) is highly risky and generally not recommended for embedded systems. This guide assumes the target partition *already exists* or the user is relocating to external storage. If the target is on the eMMC and needs creation/resizing, refer to Phase 5\.

### **Methods for Relocation**

Several methods can be used to relocate directories. The choice depends on the directory's criticality and the desired level of system integration.

* Bind Mounts (Recommended for System Integrity):  
  A bind mount makes a directory or an existing mount point appear as if it's also located at another path within the filesystem hierarchy.14 The kernel treats a bind-mounted directory much like a regularly mounted filesystem, making this method generally more robust and transparent for system directories compared to symbolic links.23  
  * **Process (e.g., relocating /var/log to /mnt/new\_storage/var\_log\_content):**  
    1. **Enter Single-User Mode:** To ensure no processes are actively writing to /var/log, boot into single-user mode or rescue target: sudo systemctl rescue.target or sudo init 1\.18 This stops most services.  
    2. **Create Target Directory:** On the new storage location, create the directory that will hold the contents of /var/log: sudo mkdir \-p /mnt/new\_storage/var\_log\_content.  
    3. **Copy Data:** Use rsync to copy the data, preserving all attributes: sudo rsync \-avX /var/log/ /mnt/new\_storage/var\_log\_content/ The trailing slash on the source /var/log/ is important for rsync to copy the contents of the directory, not the directory itself. The \-a flag archives (preserves permissions, ownership, timestamps, etc.), \-v provides verbose output, and \-X preserves extended attributes.14  
    4. **Verify Copied Data:** Thoroughly check that all data has been copied correctly to /mnt/new\_storage/var\_log\_content/.  
    5. **Rename Original Directory:** Once confident in the copy, rename the original /var/log to serve as a temporary backup: sudo mv /var/log /var/log.old.  
    6. **Create New Empty Mount Point:** Create an empty directory at the original location to serve as the mount point for the bind mount: sudo mkdir /var/log.  
    7. **Configure /etc/fstab for Permanent Mount:** Add the following line to /etc/fstab to make the bind mount persistent across reboots 14: /mnt/new\_storage/var\_log\_content /var/log none bind 0 0  
    8. **Mount the Bind Mount:** Apply the new fstab entry or mount it manually: sudo mount \-a or sudo mount /var/log.  
    9. **Verify Operation:** Reboot the system. Check that /var/log is now sourced from /mnt/new\_storage/var\_log\_content and that system logging functions correctly.  
    10. **Remove Old Directory:** Once everything is confirmed to be working correctly after a reboot and some uptime, the /var/log.old directory can be removed: sudo rm \-rf /var/log.old.  
* Symbolic Links (Use with Caution for System Directories):  
  A symbolic link (symlink) is a special type of file that acts as a pointer to another file or directory.17 While simpler to create than bind mounts, symlinks can sometimes cause issues with certain applications or during the early stages of the boot process, especially if they point to locations on filesystems that are not yet mounted.14  
  * **Process (e.g., relocating /var/cache/apt/archives to /mnt/new\_storage/apt\_cache\_content):**  
    1. **Create Target Directory:** sudo mkdir \-p /mnt/new\_storage/apt\_cache\_content.  
    2. **Move Data:** (Ensure apt is not running) sudo mv /var/cache/apt/archives/\* /mnt/new\_storage/apt\_cache\_content/ (or use rsync then rm) sudo rmdir /var/cache/apt/archives (if empty after moving contents)  
    3. **Create Symbolic Link:** sudo ln \-s /mnt/new\_storage/apt\_cache\_content /var/cache/apt/archives.17  
  * For critical system directories, bind mounts are generally preferred over symlinks due to their greater transparency and robustness.14  
* Configuring apt.conf for APT Cache (Specific to APT):  
  For /var/cache/apt/archives/, APT itself provides a configuration option to change its cache location, which is often the cleanest method.14  
  1. Create the new cache destination, including a partial subdirectory: sudo mkdir \-p /mnt/new\_storage/my\_apt\_cache/partial  
  2. Edit or create a custom APT configuration file, e.g., /etc/apt/apt.conf.d/99custom\_cache.conf:  
     Dir::Cache::Archives "/mnt/new\_storage/my\_apt\_cache/";

  3. Move existing archives (optional, or let apt clean remove old ones and new downloads go to the new location): sudo mv /var/cache/apt/archives/\* /mnt/new\_storage/my\_apt\_cache/ sudo apt clean (to clear the old default location). This method avoids filesystem-level redirection (bind mounts or symlinks) for APT's cache.

The choice between a bind mount and a symbolic link is significant. Bind mounts are integrated at a lower level by the kernel and are generally more reliable for directories that are essential for system operation or are accessed early in the boot process (such as components of /var). Symbolic links, while simpler, might not be resolved correctly in all situations, particularly before the target filesystem is mounted or within chroot environments.14 For /var/cache/apt/archives, the apt.conf method is the most elegant and application-aware solution.

Regardless of the method chosen, performing these operations in single-user mode or rescue target (systemctl rescue.target) is highly recommended.18 This minimizes the risk of data corruption or service failures that could occur if files are moved while actively being used by the system.

**Table: Comparison of Directory Relocation Methods**

| Feature/Method | Bind Mount | Symbolic Link | APT apt.conf (for apt cache) |
| :---- | :---- | :---- | :---- |
| **Mechanism** | Kernel-level directory mirroring | Filesystem pointer | Application-specific configuration |
| **Pros** | Robust for system dirs, transparent to apps, better for chroots 23 | Simpler to create, works for files & dirs | Cleanest for APT, no FS manipulation |
| **Cons** | Root-only manipulation, slightly more complex 24 | Can break with some tools/early boot 14, less transparent | Only for APT cache |
| **Best Use Cases** | /var/log, /opt (if critical services depend on it early) | /var/cache/apt/archives (alternative), non-critical user data | /var/cache/apt/archives (preferred) |
| **Relative Risk** | Medium (if done carefully) | Medium-High (for system dirs), Low (for user data) | Low |
| **fstab Entry?** | Yes (e.g., /path/to/source /target none bind) | No (symlink is persistent itself) | No (apt.conf change is persistent) |

## **6\. Phase 5: Extreme Measures \- Root Partition Resizing via Re-flashing (Highest Risk)**

This phase describes the process of resizing the root partition (/dev/root) on the eMMC by modifying the device's partition table and re-flashing the firmware. This is the most invasive and highest-risk procedure detailed in this guide and should only be considered as a last resort if all previous methods are insufficient to resolve the low space issue.

**Strong Warning:**

* **Data Loss is Certain:** This procedure involves re-partitioning the eMMC, which will erase all data on the partitions being modified or re-flashed. A complete and verified backup of all critical data (as outlined in Phase 1\) is absolutely essential. Without it, data recovery will be impossible.  
* **Risk of Bricking:** Incorrect execution, such as flashing an incompatible loader, a malformed parameter file, or interrupting the flashing process, can lead to a "bricked" device, rendering it unbootable. Recovery might only be possible if MASKROM mode remains accessible.  
* **Expertise Required:** This operation should only be attempted by users with a thorough understanding of the Rockchip rk3588 platform, eMMC partitioning, firmware structure, and the use of flashing tools like rkdeveloptool.

Directly resizing a live root partition on an eMMC device using tools like GParted (which are primarily designed for x86 systems and may not boot or function correctly on ARM SoCs for this purpose 25) is generally not feasible or safe and can lead to filesystem corruption.27 The correct method for rk3588 involves defining a new partition layout and re-flashing.

### **Overview of rk3588 eMMC Partitioning**

Rockchip-based devices, including the rk3588, utilize a "parameter" file to define the partition layout on the eMMC storage.3 This text file specifies partition names, their sizes, and often their starting offsets on the eMMC. For systems using the GUID Partition Table (GPT), this file is typically named parameter-gpt.txt or similar, and will contain an entry like TYPE: GPT.29

The CMDLINE entry within the parameter file often contains an mtdparts string that describes the partition layout, for example: mtdparts=rk29xxnand:0x00002000@0x00004000(uboot),0x00002000@0x00006000(misc),....29 In this format, 0x\<hex\_size\> represents the partition size, 0x\<hex\_start\_offset\> is its starting location, and (name) is the partition label. Modifying the root partition size involves carefully editing these values.

The primary tool for low-level interaction with Rockchip devices in MASKROM or Loader mode is rkdeveloptool.3 It is used for flashing bootloaders, the parameter file (which defines the partition table), and individual partition images.

### **Conceptual Steps for Re-partitioning and Re-flashing**

The following steps provide a conceptual overview. Specific file names, offsets, and commands may vary based on the rk3588 board vendor and firmware version. Always refer to the official documentation for the specific device.

1. **Obtain Necessary Files:**  
   * The correct rkdeveloptool binary for the host operating system.  
   * The appropriate loader file for the rk3588 SoC (e.g., rk3588\_spl\_loader\_vX.Y.Z.bin, MiniLoaderAll.bin).2  
   * The parameter.txt or parameter-gpt.txt file corresponding to the device's current firmware or a known-good base image. This file will be modified.  
   * Image files for all essential partitions: uboot.img, trust.img, boot.img (containing the kernel and device tree), and a new rootfs.img (Debian Bullseye for arm64). An image for userdata.img might also be needed, or it can be created as an empty partition to be formatted later.2  
2. **Complete eMMC Backup (Reiteration of Phase 1):** Before any modification, use rkdeveloptool read-partition \<partition\_name\> \<filename.img\> in MASKROM/Loader mode to back up *every* existing partition (e.g., loader, parameter, uboot, trust, boot, rootfs, userdata, and any others specific to the device). This is the most reliable way to preserve the original state.  
3. **Modify the parameter.txt File:** This is the most critical step for resizing. Carefully edit the parameter.txt file to reflect the new desired partition sizes.  
   * Identify the line defining rootfs and userdata (or any subsequent partitions).  
   * Adjust the size of rootfs. If increasing rootfs, the starting offset of userdata (and any partitions after it) must be increased accordingly. The size of userdata (or the last partition) may need to be reduced to ensure the total allocated space does not exceed the eMMC capacity.  
   * Example (conceptual, based on mtdparts format seen in 29): Original: ...\<size\_A\>@\<offset\_A\>(partA),\<size\_rootfs\>@\<offset\_rootfs\>(rootfs),\<size\_userdata\>@\<offset\_userdata\>(userdata)... Modified: ...\<size\_A\>@\<offset\_A\>(partA),\<NEW\_size\_rootfs\>@\<offset\_rootfs\>(rootfs),\<NEW\_size\_userdata\>@\<NEW\_offset\_userdata\>(userdata)...  
   * All size and offset values are typically in hexadecimal and may represent sectors (512 bytes) or blocks of a different size. This must be handled with extreme precision. Ensure partitions are contiguous and do not overlap.  
   * Modifying the parameter file incorrectly is a primary cause of flashing failures.  
4. **Prepare a New rootfs.img:**  
   * Since the rootfs partition size is changing, the original rootfs.img (even if backed up) might not be suitable. Flashing an old, smaller rootfs.img to a newly enlarged partition will result in unused space within that partition.  
   * Ideally, obtain or build a fresh Debian Bullseye arm64 rootfs.img that is either pre-sized for the new larger partition or is a minimal image that can be expanded post-flash.  
5. **Enter MASKROM/Loader Mode:**  
   * Connect the rk3588 device to the host PC via USB OTG.  
   * Follow the device-specific procedure to boot into MASKROM or Loader mode (e.g., holding the RECOVERY button while powering on or pressing RESET 1). The host PC should detect a new USB device.  
6. **Flash with rkdeveloptool:** The sequence of commands is critical:  
   * Download initial bootloader (SPL): sudo rkdeveloptool db \<loader\_file.bin\>.3  
   * (Optional, device-dependent) Upgrade loader/write IDB loader: sudo rkdeveloptool ul \<loader\_file.bin\>.3  
   * Write the modified partition table: sudo rkdeveloptool gpt \<modified\_parameter-gpt.txt\>.3 (Some tools might use rkdeveloptool write-partition-table \<modified\_parameter.txt\>).  
   * Flash individual partition images to their new offsets as defined in the modified parameter file. The command can be rkdeveloptool wl \<hex\_offset\> \<image\_file.img\> or rkdeveloptool write-partition \<partition\_name\> \<image\_file.img\> if the tool can parse names from the parameter file.3  
     * sudo rkdeveloptool write-partition uboot uboot.img  
     * sudo rkdeveloptool write-partition trust trust.img  
     * sudo rkdeveloptool write-partition boot boot.img  
     * sudo rkdeveloptool write-partition rootfs \<new\_rootfs.img\>  
     * sudo rkdeveloptool write-partition userdata userdata.img (if flashing userdata)  
   * Reset the device: sudo rkdeveloptool rd.3  
7. **Post-Flash Operations:**  
   * The first boot after re-flashing may take longer as the system initializes.  
   * If a generic or smaller rootfs.img was flashed to the newly enlarged rootfs partition, the filesystem within it will need to be resized to utilize the full space. Once the system boots, this can often be done with sudo resize2fs /dev/root (or the actual block device for the rootfs, e.g., /dev/mmcblkXpY). This command expands an ext2/3/4 filesystem to fill the partition it resides on.27  
   * Restore user data and system configurations from the backups made in Phase 1\.

Understanding the role of each partition is vital when modifying the parameter file and flashing. Omitting a critical partition or flashing it to the wrong location will likely result in an unbootable device.

**Table: Key rk3588 eMMC Partitions and Their Purpose**

| Partition Name | Typical Content/Function | Criticality | Notes (rk3588 specific where known) |
| :---- | :---- | :---- | :---- |
| loader | First stage bootloader (SPL \- Secondary Program Loader) | Critical | e.g., rk3588\_spl\_loader\_\*.bin, MiniLoaderAll.bin 2 |
| parameter | Partition table definition data | Critical | Defines layout; flashed by rkdeveloptool gpt or equivalent |
| uboot | Second stage bootloader (U-Boot image) | Critical | uboot.img 29 |
| trust | TrustZone/security firmware (e.g., ATF, OP-TEE) | Critical | trust.img 29 |
| misc | Miscellaneous data, often for recovery/boot mode flags | Important | misc.img 29 |
| dtbo | Device Tree Blob Overlays | Important | dtbo.img 2 |
| boot | Kernel image, Device Tree Blob (DTB), initramfs (optional) | Critical | boot.img 29 |
| recovery | Recovery system image (if implemented) | Optional | recovery.img 29 |
| rootfs | The main root filesystem (e.g., Debian Bullseye) | Critical | rootfs.img 29 |
| userdata | User data, applications; often mounted at /userdata or /data | Varies | userdata.img (can be flashed empty and formatted later) 30 |

The process of resizing the root partition on an rk3588's eMMC is fundamentally a firmware re-flashing operation that rewrites the partition table based on a modified parameter file. This is distinct from live partition resizing common on x86 systems. The parameter file acts as the blueprint for the eMMC's structure, and any changes to it necessitate re-flashing not only the partition table itself but also all essential bootloader stages and operating system images to ensure their correct placement and function according to the new layout. This interdependency means that a change in the parameter file (the cause) requires a comprehensive re-flash of related components (the effect) for the system to boot and operate correctly.

## **7\. Phase 6: Post-Resolution Monitoring and Best Practices**

After successfully implementing one or more of the preceding phases to alleviate the low disk space issue on the /dev/root partition, it is crucial to verify the results and establish practices for ongoing monitoring and prevention.

### **Verifying Reclaimed Space**

Immediately after completing any cleanup, relocation, or re-flashing procedures, verify the amount of space reclaimed on the root partition. Use the df \-Th command:  
df \-Th /  
or  
df \-Th /dev/root  
Compare the "Avail" and "Use%" columns with the values recorded in Phase 1 to quantify the improvement.

### **Ongoing Disk Space Monitoring**

Proactive monitoring is key to preventing future low-space emergencies.

* **Regular Manual Checks:** Periodically run df \-h and, if necessary, sudo ncdu \-x / to keep an eye on disk space consumption trends.  
* **Automated Monitoring/Alerts:** For systems in continuous operation, consider implementing automated monitoring scripts or tools (e.g., Nagios, Zabbix, or custom scripts using cron) that can send alerts if disk usage on /dev/root exceeds a predefined threshold (e.g., 80% or 85%).

### **Preventative Measures for the Future**

Adopting good system hygiene practices can significantly reduce the likelihood of the root partition filling up again.

* **Regular System Maintenance:**  
  * Periodically execute sudo apt update && sudo apt clean && sudo apt autoremove \--purge to remove cached package files and orphaned dependencies.  
  * Routinely check and manage old kernels if apt autoremove is not consistently effective.  
* **Log Management:**  
  * Ensure systemd-journald is configured with appropriate size limits (e.g., SystemMaxUse) in /etc/systemd/journald.conf to prevent unbounded growth of system logs.  
  * Verify that logrotate is active and correctly configured for other application logs in /var/log/.  
* **Mindful Software Installation and Usage:**  
  * Be cautious when installing large software packages, especially from third-party sources or compiled manually. Understand where they store their data and cache.  
  * If applications allow, configure them to use alternative storage locations (e.g., a separate userdata partition or external storage) for large datasets, caches, or temporary files, rather than the root partition.  
* **Developer Practices (if applicable):**  
  * For users developing applications for the rk3588 platform, profile resource consumption, including disk space usage, during development and testing. Optimize applications to minimize their storage footprint on the root filesystem.  
  * Avoid storing large, volatile data directly within the application's installation directory on the root partition if it can be placed on a more suitable data partition.

By addressing the immediate low space problem and implementing these preventative measures, the long-term stability and performance of the rk3588 Debian Bullseye system can be significantly enhanced. This transforms a reactive troubleshooting effort into a proactive system administration strategy.

## **8\. Appendix**

This appendix provides supplementary information relevant to managing an rk3588 system.

### **Glossary of rk3588-Specific Terms**

* **eMMC (embedded MultiMediaCard):** A type of flash memory commonly used as primary storage in embedded systems and SoCs like the rk3588.  
* **MASKROM Mode:** A low-level boot mode embedded in the SoC's ROM. It allows the device to accept firmware flashing commands via USB OTG, even if the eMMC bootloaders are corrupted. It's a fundamental recovery mechanism for Rockchip devices.31  
* **OTG Flashing (On-The-Go Flashing):** The process of flashing firmware to the device using its USB OTG port, typically when the device is in MASKROM or Loader mode.  
* **rkdeveloptool:** A command-line utility provided by Rockchip for communicating with devices in MASKROM/Loader mode. It is used to download bootloaders, flash partition tables, and write partition images to eMMC or other storage.3  
* **Parameter File (parameter.txt / parameter-gpt.txt):** A text file used in Rockchip firmware to define the partition layout on the eMMC. It specifies partition names, sizes, and starting offsets.29  
* **U-Boot (Universal Bootloader):** A popular open-source bootloader commonly used in embedded systems, including rk3588 devices. It is responsible for initializing hardware and loading the operating system kernel.29  
* **SPL (Secondary Program Loader):** An initial, small bootloader stage often loaded by the MASKROM, which then initializes DRAM and loads the main bootloader (U-Boot). Sometimes referred to as the "miniloader".2  
* **GPT (GUID Partition Table):** A modern standard for the layout of partition tables on a physical storage device. Used by many rk3588 firmware images.2

### **Links to Relevant Rockchip Documentation and Community Resources**

For further information and support specific to the rk3588 board in use, consult the following types of resources:

* **Board Vendor Wikis:** Manufacturers like Radxa, FriendlyElec, Orange Pi, etc., provide detailed wikis and documentation for their rk3588-based boards (e.g.2).  
* **Rockchip Open Source Wiki:** opensource.rock-chips.com (or similar official Rockchip developer sites) often contain core documentation about SoCs and tools.3  
* **Community Forums:** Forums associated with the board vendor (e.g., Radxa Forum 42) or broader Arm/Linux communities (e.g., Armbian forums, if applicable) can be invaluable for troubleshooting and sharing experiences.43

### **Troubleshooting Common Issues**

* **rkdeveloptool Fails to Detect Device:**  
  * Ensure the device is correctly put into MASKROM or Loader mode. The procedure can be timing-sensitive.  
  * Verify USB OTG cable and port are functional.  
  * On Linux hosts, ensure udev rules are correctly set up for Rockchip devices, or run rkdeveloptool with sudo.  
  * On Windows hosts, ensure the correct Rockchip USB drivers are installed.1  
* **System Fails to Boot After Kernel Removal:**  
  * If too many kernels were removed, or the only remaining kernel is faulty, the system may not boot.  
  * Recovery might involve booting from an SD card (if supported by the board and U-Boot) into a compatible Linux environment. From there, it might be possible to mount the eMMC root partition, chroot into it, and reinstall a known-good kernel package (linux-image-...). This is an advanced procedure.  
  * Alternatively, re-flashing the boot and rootfs partitions via MASKROM mode might be necessary.  
* **Errors During apt Operations:**  
  * Network issues: Ensure the device has internet connectivity.  
  * Corrupted package lists: Try sudo rm \-rf /var/lib/apt/lists/\* followed by sudo apt update.  
  * Broken packages: sudo apt \--fix-broken install might resolve some dependency issues.

## **9\. Conclusions and Recommendations**

The issue of low disk space on the /dev/root partition of an rk3588 arm64 Debian Bullseye system, while critical, can be systematically addressed. This guide has outlined a phased approach, starting with low-risk cleanup operations and progressing to more complex and potentially risky procedures.

**Key Recommendations:**

1. **Prioritize Safety:** Before undertaking any significant modifications, especially those involving directory relocation (Phase 4\) or eMMC re-partitioning (Phase 5), **a comprehensive data backup is non-negotiable**. Understanding the MASKROM/Loader mode recovery process for the specific rk3588 device is also a crucial preparatory step.  
2. **Start with Low-Risk Methods:** Always begin with standard system cleanup procedures outlined in Phase 2\. Utilizing apt clean and apt autoremove \--purge, managing old Linux kernels carefully, and controlling systemd journal log sizes can often free up substantial space with minimal risk.  
3. **Analyze Before Acting:** Employ tools like ncdu (Phase 3\) to accurately identify the largest consumers of disk space. This targeted analysis will inform which specific directories or file types are the primary cause of the low space condition, allowing for more effective remediation.  
4. **Approach Directory Relocation with Caution:** If relocating directories (Phase 4\) is deemed necessary, prefer bind mounts over symbolic links for system-critical directories due to their enhanced robustness. Always perform such operations in single-user mode or rescue target to ensure system stability. For specific cases like the APT cache, application-level configurations (e.g., apt.conf) are the preferred method.  
5. **Reserve Partition Resizing as a Last Resort:** Re-flashing the eMMC to resize partitions (Phase 5\) is a high-risk operation that guarantees data loss on affected partitions and can render the device unbootable if not executed perfectly. This should only be attempted if all other methods fail and the user possesses the necessary expertise and has exhausted all other options. Meticulous adherence to the rk3588 platform's specific flashing procedures, including correct modification of the parameter file and use of rkdeveloptool, is essential.  
6. **Implement Proactive Monitoring and Maintenance:** Once the immediate space issue is resolved, establish a routine of ongoing disk space monitoring and preventative maintenance (Phase 6). Regular cleanups, log management, and mindful software installation will help prevent recurrence of the problem.

By following this structured approach, users can effectively manage and resolve low disk space issues on their rk3588 Debian Bullseye systems, ensuring continued stability and performance. The specific nature of embedded ARM SoCs like the rk3588 necessitates a greater degree of caution and platform-specific knowledge compared to managing disk space on standard desktop systems.

#### **Works cited**

1. RK3588-POE-SBC/RK3588\_Update\_Firmware.md at main \- GitHub, accessed May 28, 2025, [https://github.com/industrialtablet/RK3588-POE-SBC/blob/main/RK3588\_Update\_Firmware.md](https://github.com/industrialtablet/RK3588-POE-SBC/blob/main/RK3588_Update_Firmware.md)  
2. Template:RK3588-BuildFromSource \- FriendlyELEC WiKi, accessed May 28, 2025, [https://wiki.friendlyelec.com/wiki/index.php/Template:RK3588-BuildFromSource](https://wiki.friendlyelec.com/wiki/index.php/Template:RK3588-BuildFromSource)  
3. Rkdeveloptool \- Rockchip open source Document, accessed May 28, 2025, [https://opensource.rock-chips.com/wiki\_Rkdeveloptool](https://opensource.rock-chips.com/wiki_Rkdeveloptool)  
4. rkdeveloptool \- rockusb bootloader utility \- Ubuntu Manpage, accessed May 28, 2025, [https://manpages.ubuntu.com/manpages/noble/man1/rkdeveloptool.1.html](https://manpages.ubuntu.com/manpages/noble/man1/rkdeveloptool.1.html)  
5. Rock5/install/spi \- Radxa Wiki, accessed May 28, 2025, [https://wiki.radxa.com/Rock5/install/spi](https://wiki.radxa.com/Rock5/install/spi)  
6. How to remove old kernels? : r/debian \- Reddit, accessed May 28, 2025, [https://www.reddit.com/r/debian/comments/1hg7zeo/how\_to\_remove\_old\_kernels/](https://www.reddit.com/r/debian/comments/1hg7zeo/how_to_remove_old_kernels/)  
7. ReduceDebian \- Debian Wiki, accessed May 28, 2025, [https://wiki.debian.org/ReduceDebian](https://wiki.debian.org/ReduceDebian)  
8. Delete Old Unused Kernels in Debian and Ubuntu \- Tutorialspoint, accessed May 28, 2025, [https://www.tutorialspoint.com/how-to-delete-old-unused-kernels-in-debian-and-ubuntu](https://www.tutorialspoint.com/how-to-delete-old-unused-kernels-in-debian-and-ubuntu)  
9. How to Check the Linux Kernel Version \- Liquid Web, accessed May 28, 2025, [https://www.liquidweb.com/blog/how-to-check-the-kernel-version-in-linux-ubuntu-centos/](https://www.liquidweb.com/blog/how-to-check-the-kernel-version-in-linux-ubuntu-centos/)  
10. Managing Journal Size \- The Ultimate Guide To Logging \- Loggly, accessed May 28, 2025, [https://www.loggly.com/ultimate-guide/managing-journal-size/](https://www.loggly.com/ultimate-guide/managing-journal-size/)  
11. Systemd logs (\`journalctl\`) are too large and slow \- Ask Ubuntu, accessed May 28, 2025, [https://askubuntu.com/questions/1012912/systemd-logs-journalctl-are-too-large-and-slow](https://askubuntu.com/questions/1012912/systemd-logs-journalctl-are-too-large-and-slow)  
12. How to Use ncdu to Find Disk-Hogging Directories in Linux, accessed May 28, 2025, [https://www.howtogeek.com/how-to-use-ncdu-to-find-disk-hogging-directories-in-linux/](https://www.howtogeek.com/how-to-use-ncdu-to-find-disk-hogging-directories-in-linux/)  
13. Debian \-- Details of package ncdu in bullseye, accessed May 28, 2025, [https://packages.debian.org/bullseye/ncdu](https://packages.debian.org/bullseye/ncdu)  
14. debian \- How to move /var to another existing partition? \- Server Fault, accessed May 28, 2025, [https://serverfault.com/questions/429937/how-to-move-var-to-another-existing-partition](https://serverfault.com/questions/429937/how-to-move-var-to-another-existing-partition)  
15. Comprehensive Guide to Understanding and Optimizing Linux File Systems, accessed May 28, 2025, [https://systemdesignschool.io/blog/linux-file-systems](https://systemdesignschool.io/blog/linux-file-systems)  
16. How to Convert a /Home Directory to Partition in Linux \- Tecmint, accessed May 28, 2025, [https://www.tecmint.com/convert-home-directory-partition-linux/](https://www.tecmint.com/convert-home-directory-partition-linux/)  
17. How do I change the location of the apt-get archive? \- Ask Ubuntu, accessed May 28, 2025, [https://askubuntu.com/questions/391296/how-do-i-change-the-location-of-the-apt-get-archive](https://askubuntu.com/questions/391296/how-do-i-change-the-location-of-the-apt-get-archive)  
18. How to move or relocate /var folder to a new partition in Linux | Support \- SUSE, accessed May 28, 2025, [https://www.suse.com/support/kb/doc/?id=000018399](https://www.suse.com/support/kb/doc/?id=000018399)  
19. Moving /var/log/ \- Nagios Support, accessed May 28, 2025, [https://support.nagios.com/kb/article/moving-var-log-473.html](https://support.nagios.com/kb/article/moving-var-log-473.html)  
20. Can I move /opt to the / partition? \- Ask Ubuntu, accessed May 28, 2025, [https://askubuntu.com/questions/351345/can-i-move-opt-to-the-partition](https://askubuntu.com/questions/351345/can-i-move-opt-to-the-partition)  
21. Moving /opt etc to another partition... \- LinuxQuestions.org, accessed May 28, 2025, [https://www.linuxquestions.org/questions/slackware-14/moving-opt-etc-to-another-partition-473613/](https://www.linuxquestions.org/questions/slackware-14/moving-opt-etc-to-another-partition-473613/)  
22. How to Move Your Linux home Directory to Another Drive \- How-To Geek, accessed May 28, 2025, [https://www.howtogeek.com/442101/how-to-move-your-linux-home-directory-to-another-hard-drive/](https://www.howtogeek.com/442101/how-to-move-your-linux-home-directory-to-another-hard-drive/)  
23. What is the difference between a symlink and binding with fstab? \- Unix & Linux Stack Exchange, accessed May 28, 2025, [https://unix.stackexchange.com/questions/35084/what-is-the-difference-between-a-symlink-and-binding-with-fstab](https://unix.stackexchange.com/questions/35084/what-is-the-difference-between-a-symlink-and-binding-with-fstab)  
24. When should you use a bind mount over a symbolic link? \- YouTube, accessed May 28, 2025, [https://www.youtube.com/watch?v=gQA59bPTgYE](https://www.youtube.com/watch?v=gQA59bPTgYE)  
25. GParted Live on USB, accessed May 28, 2025, [https://gparted.org/liveusb.php](https://gparted.org/liveusb.php)  
26. GParted \-- Live CD/USB/PXE/HD, accessed May 28, 2025, [https://gparted.org/livecd.php](https://gparted.org/livecd.php)  
27. partitioning \- Cannot resize rootfs partition on a emmc memory \- Ask ..., accessed May 28, 2025, [https://askubuntu.com/questions/1146510/cannot-resize-rootfs-partition-on-a-emmc-memory](https://askubuntu.com/questions/1146510/cannot-resize-rootfs-partition-on-a-emmc-memory)  
28. Extend root filesystem using CLI parted & resize2fs \- Raspberry Pi Forums, accessed May 28, 2025, [https://forums.raspberrypi.com/viewtopic.php?t=45265](https://forums.raspberrypi.com/viewtopic.php?t=45265)  
29. 2\. Compile Linux Firmware (kernel-5.10) — Firefly Wiki, accessed May 28, 2025, [https://wiki.t-firefly.com/en/ROC-RK3588-PC/linux\_compile.html](https://wiki.t-firefly.com/en/ROC-RK3588-PC/linux_compile.html)  
30. Rockchip Parameter File | Vicharak, accessed May 28, 2025, [https://docs.vicharak.in/vicharak\_sbcs/vaaman/vaaman-linux/linux-development-guide/rockchip-parameter-file/](https://docs.vicharak.in/vicharak_sbcs/vaaman/vaaman-linux/linux-development-guide/rockchip-parameter-file/)  
31. Flashing eMMC Image \- LUCKFOX WIKI, accessed May 28, 2025, [https://wiki.luckfox.com/Luckfox-Pico-Pi/Flash-image/](https://wiki.luckfox.com/Luckfox-Pico-Pi/Flash-image/)  
32. Expanding the Root Partition \- General \- ArmSoM Community, accessed May 28, 2025, [https://forum.armsom.org/t/expanding-the-root-partition/257](https://forum.armsom.org/t/expanding-the-root-partition/257)  
33. Repartitioning the internal/app partition \- XDA Forums, accessed May 28, 2025, [https://xdaforums.com/t/repartitioning-the-internal-app-partition.3251960/](https://xdaforums.com/t/repartitioning-the-internal-app-partition.3251960/)  
34. Rock/flash the image \- Radxa Wiki, accessed May 28, 2025, [https://wiki.radxa.com/Rock/flash\_the\_image](https://wiki.radxa.com/Rock/flash_the_image)  
35. CM3588 \- FriendlyELEC WiKi, accessed May 28, 2025, [https://wiki.friendlyelec.com/wiki/index.php/CM3588](https://wiki.friendlyelec.com/wiki/index.php/CM3588)  
36. Template:RK3588-UpdateLog \- FriendlyELEC WiKi, accessed May 28, 2025, [https://wiki.friendlyelec.com/wiki/index.php/Template:RK3588-UpdateLog](https://wiki.friendlyelec.com/wiki/index.php/Template:RK3588-UpdateLog)  
37. Rock/resize linux rootfs \- Radxa Wiki, accessed May 28, 2025, [https://wiki.radxa.com/Rock/resize\_linux\_rootfs](https://wiki.radxa.com/Rock/resize_linux_rootfs)  
38. Template:RockchipCommonLinuxTips \- FriendlyELEC WiKi, accessed May 28, 2025, [https://wiki.friendlyelec.com/wiki/index.php/Template:RockchipCommonLinuxTips](https://wiki.friendlyelec.com/wiki/index.php/Template:RockchipCommonLinuxTips)  
39. Flash BootLoader to SPI Nor Flash \- Radxa Docs, accessed May 28, 2025, [https://docs.radxa.com/en/rock5/lowlevel-development/bootloader\_spi\_flash](https://docs.radxa.com/en/rock5/lowlevel-development/bootloader_spi_flash)  
40. Linux SDK Configuration introduction — Firefly Wiki, accessed May 28, 2025, [https://wiki.t-firefly.com/en/Core-3588J/linux\_sdk.html](https://wiki.t-firefly.com/en/Core-3588J/linux_sdk.html)  
41. Boot option \- Rockchip open source Document, accessed May 28, 2025, [https://opensource.rock-chips.com/wiki\_Boot\_option](https://opensource.rock-chips.com/wiki_Boot_option)  
42. RK3588 / Rock pi 5 /Development? \- Radxa forum, accessed May 28, 2025, [https://forum.radxa.com/t/rk3588-rock-pi-5-development/7123/1000](https://forum.radxa.com/t/rk3588-rock-pi-5-development/7123/1000)  
43. Radxa Rock Pi 5c (Rockchip RK3588S2) or FriendlyElec CM3588 plus (Rockchip RK3588) for NAS? : r/HomeNAS \- Reddit, accessed May 28, 2025, [https://www.reddit.com/r/HomeNAS/comments/1kv8glo/radxa\_rock\_pi\_5c\_rockchip\_rk3588s2\_or/](https://www.reddit.com/r/HomeNAS/comments/1kv8glo/radxa_rock_pi_5c_rockchip_rk3588s2_or/)
