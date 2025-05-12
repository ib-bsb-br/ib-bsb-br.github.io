---
tags: [scratchpad]
info: aberto.
date: 2025-05-09
type: post
layout: post
published: true
slug: performance-governor-optimizations-script
title: 'Performance Governor optimizations Script'
comment: https://github.com/ChisBread/rk3588-gaming-step-by-step/tree/main/rk3588-enhance
---
This guide presents a comprehensive, single approach to managing CPU, GPU, NPU, and DMC frequency governors on Linux systems, particularly for devices like the RK3588, by setting them to “performance” mode. This method emphasizes robustness, dynamic discovery of hardware, state persistence for reversibility, and proper integration with systemd. It combines the best practices from various methods into one refined solution.

While the context often mentions RK3588, the script and systemd service are designed to be generally applicable to Linux systems, though specific sysfs paths for governors can vary if not covered by the general patterns.

This solution consists of a powerful Bash script that handles the logic of discovering, setting, and restoring governors, and a systemd service unit to manage this script at boot and allow system-level control.

**1. The Bash Script: `/usr/local/bin/performance_governors.sh`**

This script is the core of the solution. Its key features include:
*   **Root Privilege Check:** Ensures it’s run with necessary permissions.
*   **Robust Scripting:** Uses `set -euo pipefail` for strict error handling and `IFS=$’\n\t’` for safer processing of paths.
*   **Variable Protection:** Uses `readonly` for global configuration variables (`STATE_DIR`, `STATE_FILE`, `GOV_PATTERNS`) to prevent accidental modification within the script, enhancing robustness.
*   **Dynamic Governor Discovery:** Automatically finds relevant `cpufreq` (CPU) and `devfreq` (GPU, NPU, DMC, etc.) governor files using general patterns, making it adaptable to different hardware configurations.
*   **State Management:** Before setting governors to “performance,” it saves the current (default) governor for each device to a state file (`/var/lib/performance_governors/default_gov.txt`). This allows for a clean restoration of previous settings.
*   **Comprehensive Actions:**
    *   `start`: Saves current governors and sets all discovered ones to “performance.”
    *   `stop`: Restores the saved governors from the state file.
    *   `restart`: Performs a `stop` then `start`.
    *   `status`: Displays the current governor and the saved (default) governor for each discovered path.
*   **Systemd-Aware Logging:** Uses `systemd-cat` for logging if available, providing integration with the system journal; otherwise, falls back to the standard `logger` utility.

```bash
#!/usr/bin/env bash
# ——————————————————————————
# performance_governors.sh
# Unified script to manage CPU/GPU/NPU/DMC frequency governors.
# Targets devices like RK3588 but designed for general Linux applicability.
# - Requires root (CAP_SYS_ADMIN)
# - Depends on 'util-linux' (for logger) and systemd (for systemd-cat)
# ——————————————————————————

# Exit on error, treat unset variables as error, propagate pipeline errors
set -euo pipefail
# Set Internal Field Separator to newline and tab for safer loops.
# Ensure standard single quotes are used here.
IFS=$'\n\t'

### Verify running as root
# Use standard quotes "" and ensure command substitution is quoted.
if [ "$(id -u)" -ne 0 ]; then
  echo "ERROR: Must be run as root." >&2
  exit 1
fi

# Location to save/restore default governors (use standard quotes)
readonly STATE_DIR="/var/lib/performance_governors"
readonly STATE_FILE="$STATE_DIR/default_gov.txt"

# General patterns covering cpufreq (CPU) and devfreq (other devices) governors
# Use standard quotes ""
readonly GOV_PATTERNS=(
  "/sys/devices/system/cpu/cpufreq/policy*/scaling_governor" # For CPU cores
  "/sys/class/devfreq/*/governor"                             # For GPU, NPU, DMC, etc.
)

# Log function: prefers systemd-cat for journal integration, else falls back to logger.
log() {
  # Use standard quotes ""
  local level="$1"; shift
  local msg="$*"
  if command -v systemd-cat &>/dev/null; then
    # Pipe to systemd-cat to log with specified level and tag
    # Use standard quotes "" and standard single quotes ''
    printf '%s\n' "$msg" | systemd-cat -t performance_governors -p "$level"
  else
    # Fallback to logger if systemd-cat is not available
    # Use standard quotes "" and standard single quotes ''
    logger -t performance_governors -p "user.$level" -- "$msg"
  fi
}

# Discover all existing governor file paths based on GOV_PATTERNS (Enhanced with nullglob).
discover_paths() {
  # Enable nullglob: patterns that match nothing expand to nothing
  shopt -s nullglob
  # Ensure nullglob is turned off again when the function exits
  trap 'shopt -u nullglob' RETURN

  for patt in "${GOV_PATTERNS[@]}"; do
    # $patt is intentionally unquoted for globbing.
    # With nullglob, if $patt matches no files, this loop won't execute for it.
    for f in $patt; do
      # We know 'f' must be an existing file due to nullglob,
      # but the check is harmless and adds clarity.
      [ -f "$f" ] && printf '%s\n' "$f"
    done
  done
  # The trap automatically runs 'shopt -u nullglob' here.
}

# Action: Save current governors and set all to 'performance'.
cmd_start() {
  # Use standard quotes ""
  log info "START: Saving default governors and forcing 'performance' mode."
  mkdir -p "$STATE_DIR" # Ensure state directory exists
  : > "$STATE_FILE"     # Truncate/create state file

  # Read each discovered governor path
  while IFS= read -r path; do
    # Use standard quotes "" and standard single quotes ''
    current_governor=$(<"$path") # Read current governor
    printf '%s\t%s\n' "$path" "$current_governor" >>"$STATE_FILE" # Save path and current governor

    # Attempt to set to 'performance' (use standard quotes)
    if echo "performance" >"$path"; then
      log info "Successfully set 'performance' for: $path"
    else
      # Use standard quotes ""
      log err "FAILED to set 'performance' for: $path"
    fi
  done < <(discover_paths) # Process substitution feeds paths from discover_paths

  # Use standard quotes ""
  log info "START command complete."
}

# Action: Restore governors to their saved default states.
cmd_stop() {
  # Use standard quotes ""
  log info "STOP: Restoring saved default governors."
  if [ ! -r "$STATE_FILE" ]; then
    # Use standard quotes "" and standard parentheses ()
    log warning "State file ($STATE_FILE) not found or not readable. Skipping restore."
    return 1 # Indicate issue if state file is missing
  fi

  # Read path and old governor from state file
  # Use standard single quotes '' for IFS setting specific to read
  while IFS=$'\t' read -r path old_governor; do
    # Use standard quotes ""
    if [ -f "$path" ]; then # Check if path still exists
      # Use standard quotes "" and standard single quotes ''
      if echo "$old_governor" >"$path"; then
        log info "Restored '$old_governor' to: $path"
      else
        # Use standard quotes "" and standard single quotes ''
        log err "FAILED to restore '$old_governor' to: $path"
      fi
    else
      # Use standard quotes ""
      log warning "Path no longer exists, cannot restore for: $path"
    fi
  done <"$STATE_FILE" # Use standard quotes ""

  # Use standard quotes ""
  log info "STOP command complete."
}

# Action: Display current and saved governors.
cmd_status() {
  # Use standard quotes ""
  echo "Governor Status (Current Governor -> Saved Default Governor):"
  declare -A saved_governors # Associative array to hold saved states

  # Populate saved_governors from state file if it exists
  # Use standard quotes ""
  if [ -r "$STATE_FILE" ]; then
    # Use standard single quotes '' for IFS setting specific to read
    while IFS=$'\t' read -r path old_governor; do
      # Use standard quotes ""
      saved_governors["$path"]="$old_governor"
    done <"$STATE_FILE" # Use standard quotes ""
  fi

  # Display status for each discovered governor path
  local found_any=0
  while IFS= read -r path; do
    found_any=1
    # Use standard quotes "" and standard curly braces {}
    current_governor=$(<"$path")
    default_governor="${saved_governors[$path]:-<not_saved>}" # Use <not_saved> if not in state file
    # Use standard quotes "", standard single quotes '', standard parentheses ()
    printf '%-65s : %-15s -> %s\n' "$path" "$current_governor" "$default_governor"
  done < <(discover_paths)

  # Use standard quotes ""
  if [ "$found_any" -eq 0 ]; then
    echo "No governor paths found."
  fi
}

# Display usage instructions.
usage() {
  # Use standard single quotes ''
  cat <<EOF
Usage: $0 {start|stop|restart|status}
  start      Saves current governor settings and sets all to 'performance'.
  stop       Restores previously saved governor settings.
  restart    Executes 'stop' then 'start'.
  status     Displays current vs. saved governor settings for all discovered paths.
EOF
  exit 1
}

# Main command dispatcher.
if [ $# -eq 0 ]; then # Show usage if no arguments
  usage
fi

# Use standard quotes ""
case "$1" in
  start)   cmd_start   ;;
  stop)    cmd_stop    ;;
  restart) cmd_stop; cmd_start ;; # Simple restart: stop then start
  status)  cmd_status  ;;
  *)       usage       ;; # Show usage for unknown commands
esac

```

**2. The Systemd Service Unit: `/etc/systemd/system/performance_governors.service`**

This service file allows systemd to manage the script.
*   `Type=oneshot`: Indicates the script runs once and exits.
*   `RemainAfterExit=yes`: Tells systemd to consider the service “active” even after the `ExecStart` process finishes, as the script’s effects (changed governors) persist.
*   `ExecStart`, `ExecStop`, `ExecReload`: Map directly to the script’s `start`, `stop`, and `restart` actions.
*   Dependencies (`After`, `Wants`): Ensures the service starts at an appropriate time during boot.
*   `Restart=no`: The `Restart=no` directive ensures that if the script fails during startup (e.g., cannot set a governor), systemd will not attempt to restart it automatically. This is generally preferred for configuration services where a failure might indicate a deeper issue requiring manual investigation rather than repeated, potentially problematic, attempts.

```ini
[Unit]
Description=Performance Governors Management (CPU/GPU/NPU/DMC)
Documentation=man:performance_governors.sh
# Start after basic system services are up.
After=multi-user.target
# Removed Wants=network-online.target (usually not needed for governors)

[Service]
Type=oneshot
ExecStart=/usr/local/bin/performance_governors.sh start
ExecStop=/usr/local/bin/performance_governors.sh stop
ExecReload=/usr/local/bin/performance_governors.sh restart
RemainAfterExit=yes
# On failure, log and stay failed. Use 'systemctl reset-failed performance_governors.service' to clear.
Restart=no

[Install]
WantedBy=multi-user.target
```

**3. Installation and Management Instructions**

1.  **Install Prerequisites** (if not already present):
    The script uses standard utilities. `util-linux` (for `logger`) and `systemd` (for `systemd-cat` and service management) are typically core components of modern Linux distributions.
    ```bash
    # On Debian/Ubuntu based systems, these are usually pre-installed.
    # sudo apt update
    # sudo apt install -y util-linux systemd 
    ```

2.  **Save the Bash Script:**
    Copy the script code above and save it as `performance_governors.sh` in a temporary location.

3.  **Install the Bash Script:**
    Move it to `/usr/local/bin/` and make it executable:
    ```bash
    sudo cp performance_governors.sh /usr/local/bin/performance_governors.sh
    sudo chmod 755 /usr/local/bin/performance_governors.sh
    ```

4.  **Save the Systemd Service Unit:**
    Copy the systemd unit content above and save it as `performance_governors.service` in a temporary location.

5.  **Install the Systemd Service Unit:**
    Move it to `/etc/systemd/system/`:
    ```bash
    sudo cp performance_governors.service /etc/systemd/system/performance_governors.service
    ```

6.  **Reload Systemd, Enable and Start the Service:**
    *   `daemon-reload`: Makes systemd aware of the new service file.
    *   `enable`: Ensures the service starts automatically on boot.
    *   `start`: Starts the service immediately for the current session.
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable performance_governors.service
    sudo systemctl start performance_governors.service
    ```

7.  **Verify Operation:**
    Check the service status and the governor settings:
    ```bash
    sudo systemctl status performance_governors.service
    sudo /usr/local/bin/performance_governors.sh status
    ```
    You can also check individual governor files, e.g., `cat /sys/devices/system/cpu/cpufreq/policy0/scaling_governor`.

**4. Using the Script Manually**

Once installed, you can also manage the governors manually using the script:
*   **Set to performance:** `sudo /usr/local/bin/performance_governors.sh start`
*   **Restore defaults:** `sudo /usr/local/bin/performance_governors.sh stop`
*   **Check status:** `sudo /usr/local/bin/performance_governors.sh status`
*   **Restart (stop then start):** `sudo /usr/local/bin/performance_governors.sh restart`
