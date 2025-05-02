---
tags: [linux>dotfile]
info: aberto.
date: 2024-11-05
type: post
layout: post
published: true
slug: performance-governors
title: 'performance_governors.sh'
---

First, remove the init.d script registration: `sudo update-rc.d performance_governors.sh remove`

Create a systemd service file: `sudo nano /etc/systemd/system/performance_governors.service`

Add this content:

{% codeblock %}
[Unit]
Description=Set CPU and GPU governor to performance
After=multi-user.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/etc/init.d/performance_governors.sh start
ExecStop=/etc/init.d/performance_governors.sh stop

[Install]
WantedBy=multi-user.target
Reload systemd to recognize the new service:
sudo systemctl daemon-reload

{% endcodeblock %}

Reload systemd to recognize the new service: `sudo systemctl daemon-reload`

Enable and start the service:
`sudo systemctl enable performance_governors`
`sudo systemctl start performance_governors`

Check the status: `sudo systemctl status performance_governors`

{% codeblock bash %}

#!/bin/bash
### BEGIN INIT INFO
# Provides:          performance_governors
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: CPU Performance Governors
# Description:       Script to manage CPU performance governor settings for RK3588
### END INIT INFO

# Source function library
. /lib/lsb/init-functions

# Path to the log file
LOG="/var/log/performance_governors.log"

# Function to write to log
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $1" >> "$LOG"
}

# Function to set governor
set_governor() {
    local path="$1"
    if [ -f "$path" ]; then
        echo performance > "$path" 2>/dev/null
        if [ $? -eq 0 ]; then
            log_message "Successfully set performance governor for $path"
            return 0
        else
            log_message "Failed to set performance governor for $path"
            return 1
        fi
    else
        log_message "Path does not exist: $path"
        return 1
    fi
}

# Function to start the service
do_start() {
    log_message "Starting performance governors"
    
    local governors=(
        "/sys/class/devfreq/fb000000.gpu/governor"
        "/sys/devices/system/cpu/cpufreq/policy0/scaling_governor"
        "/sys/devices/system/cpu/cpufreq/policy4/scaling_governor"
        "/sys/devices/system/cpu/cpufreq/policy6/scaling_governor"
        "/sys/class/devfreq/dmc/governor"
        "/sys/class/devfreq/fdab0000.npu/governor"
    )
    
    local failed=0
    for governor in "${governors[@]}"; do
        set_governor "$governor" || failed=1
    done
    
    if [ $failed -eq 0 ]; then
        log_message "All performance governors set successfully"
        return 0
    else
        log_message "Some governors failed to set"
        return 1
    fi
}

# Function to stop the service (reset to default)
do_stop() {
    log_message "Stopping performance governors (resetting to default)"
    return 0
}

# Function to check status
do_status() {
    local failed=0
    for governor in /sys/devices/system/cpu/cpufreq/policy*/scaling_governor; do
        if [ -f "$governor" ]; then
            current=$(cat "$governor")
            echo "Current governor for $governor: $current"
            [ "$current" != "performance" ] && failed=1
        fi
    done
    return $failed
}

# Main script logic
case "$1" in
    start)
        do_start
        ;;
    stop)
        do_stop
        ;;
    restart)
        do_stop
        do_start
        ;;
    status)
        do_status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit $?

{% endcodeblock %}

***

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––
1) Bash Script: `/usr/local/bin/performance_governors.sh`  
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––
```bash
#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# performance_governors.sh
# Manage CPU/GPU/NPU/DMC frequency governors on RK3588 (Debian Bullseye arm64)
# - Requires root (CAP_SYS_ADMIN)
# - Depends on 'util-linux' (logger) and systemd
# -----------------------------------------------------------------------------
set -euo pipefail
IFS=$'\n\t'

### Verify running as root
if [ "$(id -u)" -ne 0 ]; then
  echo "ERROR: Must be run as root." >&2
  exit 1
fi

# Location to save/restore default governors
STATE_DIR="/var/lib/performance_governors"
STATE_FILE="$STATE_DIR/default_gov.txt"

# Patterns covering cpufreq and devfreq governors
readonly GOV_PATTERNS=(
  "/sys/devices/system/cpu/cpufreq/policy*/scaling_governor"
  "/sys/class/devfreq/*/governor"
)

# Log function: prefer systemd-cat, else fallback to logger
log() {
  local level="$1"; shift
  local msg="$*"
  if command -v systemd-cat &>/dev/null; then
    printf '%s\n' "$msg" | systemd-cat -t performance_governors -p "$level"
  else
    logger -t performance_governors -p "user.$level" -- "$msg"
  fi
}

# Discover all existing governor file paths
discover_paths() {
  for patt in "${GOV_PATTERNS[@]}"; do
    for f in $patt; do
      [ -f "$f" ] && printf '%s\n' "$f"
    done
  done
}

cmd_start() {
  log info "START: Saving defaults & forcing performance"
  mkdir -p "$STATE_DIR"
  : > "$STATE_FILE"  # truncate

  while IFS= read -r path; do
    current=$(<"$path")
    printf '%s\t%s\n' "$path" "$current" >>"$STATE_FILE"
    if echo performance >"$path"; then
      log info "Set 'performance' → $path"
    else
      log err  "FAILED to set performance → $path"
    fi
  done < <(discover_paths)

  log info "START complete."
}

cmd_stop() {
  log info "STOP: Restoring saved governors"
  if [ ! -r "$STATE_FILE" ]; then
    log warning "No state file; skipping restore"
    return 1
  fi
  while IFS=$'\t' read -r path old; do
    if [ -f "$path" ]; then
      if echo "$old" >"$path"; then
        log info "Restored '$old' → $path"
      else
        log err  "FAILED restore '$old' → $path"
      fi
    else
      log warning "Path missing; skip $path"
    fi
  done <"$STATE_FILE"
  log info "STOP complete."
}

cmd_status() {
  echo "Governor status (current → saved):"
  declare -A saved
  [ -r "$STATE_FILE" ] && while IFS=$'\t' read -r p o; do saved["$p"]="$o"; done <"$STATE_FILE"

  while IFS= read -r path; do
    cur=$(<"$path")
    def="${saved[$path]:-<undef>}"
    printf '%-60s : %s → %s\n' "$path" "$cur" "$def"
  done < <(discover_paths)
}

usage() {
  cat <<EOF
Usage: $0 {start|stop|restart|status}
  start      Save defaults and set all governors to 'performance'
  stop       Restore saved defaults
  restart    Run 'stop' then 'start'
  status     Display current vs saved governors
EOF
  exit 1
}

# Main dispatcher
[ $# -ge 1 ] || usage
case "$1" in
  start)   cmd_start   ;;
  stop)    cmd_stop    ;;
  restart) cmd_stop; cmd_start ;;
  status)  cmd_status  ;;
  *)       usage       ;;
esac
```

References:  
– Kernel devfreq docs: https://www.kernel.org/doc/html/latest/driver-api/devfreq.html  
– `systemd.service` manual: https://www.freedesktop.org/software/systemd/man/systemd.service.html

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––
2) systemd Service Unit: `/etc/systemd/system/performance_governors.service`  
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––
```ini
[Unit]
Description=Performance Governors for CPU/GPU/NPU/DMC (RK3588)
After=multi-user.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/performance_governors.sh start
ExecStop=/usr/local/bin/performance_governors.sh stop
ExecReload=/usr/local/bin/performance_governors.sh restart
RemainAfterExit=yes
# On failure, log and stay failed (use 'systemctl reset-failed' to clear)
Restart=no

[Install]
WantedBy=multi-user.target
```

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––
3) Installation Steps  
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––
1. Install prerequisites:
   ```bash
   sudo apt update
   sudo apt install -y util-linux systemd
   ```
2. Copy script & set permissions:
   ```bash
   sudo cp performance_governors.sh /usr/local/bin/
   sudo chmod 755 /usr/local/bin/performance_governors.sh
   ```
3. Copy unit file:
   ```bash
   sudo cp performance_governors.service /etc/systemd/system/
   ```
4. Reload systemd, enable & start:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable performance_governors.service
   sudo systemctl start  performance_governors.service
   ```
5. Verify:
   ```bash
   sudo systemctl status performance_governors.service
   sudo /usr/local/bin/performance_governors.sh status
   ```
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––
