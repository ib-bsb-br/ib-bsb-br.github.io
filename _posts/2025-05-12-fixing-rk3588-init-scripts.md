---
tags: [aid>software>linux>rockchip]
info: aberto.
date: 2025-05-12
type: post
layout: post
published: true
slug: fixing-rk3588-init-scripts
title: 'Fixing rk3588 Init Scripts'
---
## What's Happening

You encountered warnings about two scripts in your `/etc/init.d/` directory:
- `mount_usb.sh`
- `gobinet_boot.sh`

These warnings occurred because:

1. When enabling a service, Debian uses a tool called `insserv` to analyze all init scripts and determine their proper boot order.
2. This tool requires LSB (Linux Standard Base) headers in each script to understand dependencies and run order.
3. Your scripts lack these headers, causing the warnings.

**Understanding the Core Problem**

*   **LSB Tags:** SysV init scripts (those in `/etc/init.d/`) use special comment blocks (`### BEGIN INIT INFO ... ### END INIT INFO`) called LSB headers. These headers tell the system (via tools like `insserv` or `systemd`'s compatibility layer) about the service's dependencies, what runlevels it should start/stop in, and provide descriptions. The warnings you saw mean these headers are missing or incomplete.
*   **`mount_usb.sh`:** This script's logic (`if [ $ACTION == "add" ]`) indicates it's designed to react to dynamic hardware events (USB stick plugged in/out). This is the job of `udev`, not the static boot sequence managed by init scripts.
*   **`gobinet_boot.sh`:** This script, which runs `quectel-CM` after a delay, is a more traditional candidate for a boot service, but it needs the proper LSB structure.

---

**Part 1: Refactoring `mount_usb.sh` (The `udev` Approach)**

This script should not be in `/etc/init.d/`. We'll move its logic to a helper script called by a `udev` rule.

**Step 1.1: Create/Move the Helper Script**

Let's place the helper script in `/usr/local/sbin/`, a standard location for locally installed system administration scripts.

Original script location: `/etc/init.d/mount_usb.sh`
New helper script location: `/usr/local/sbin/mount_usb_helper.sh`

```bash
sudo mv /etc/init.d/mount_usb.sh /usr/local/sbin/mount_usb_helper.sh
sudo chmod +x /usr/local/sbin/mount_usb_helper.sh
```

Now, replace the content of `/usr/local/sbin/mount_usb_helper.sh` with this improved version:

```bash
#!/bin/bash

# Helper script to auto-mount/unmount USB VFAT drives, intended to be called by udev.
# $1 (DEVNAME): Device name (e.g., sdb1) passed by the udev rule via %k.
# $ACTION:      Environment variable (add/remove) set by udev.

DEVNAME="${1}"
MOUNT_BASE="/mnt/media" # Or your preferred base path
MOUNT_POINT="${MOUNT_BASE}/${DEVNAME}"
LOG_TAG="usb-mount-helper" # For syslog

# Function for logging to syslog (and optionally a dedicated file)
log_message() {
    logger -t "${LOG_TAG}" -- "$1" # -- ensures message isn't mistaken for options
    # Optional: echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "/var/log/${LOG_TAG}.log"
}

if [ -z "$DEVNAME" ]; then
    log_message "Error: Device name not provided. Exiting."
    exit 1
fi

# Create the base mount directory if it doesn't exist
if [ ! -d "${MOUNT_BASE}" ]; then
    mkdir -p "${MOUNT_BASE}"
    if [ $? -ne 0 ]; then
        log_message "Error: Could not create base mount directory ${MOUNT_BASE}. Exiting."
        exit 1
    fi
fi

if [ "$ACTION" == "add" ]; then
    log_message "Add event for /dev/${DEVNAME}."

    # Check if already mounted using findmnt for reliability
    if findmnt --source "/dev/${DEVNAME}" --target "${MOUNT_POINT}" > /dev/null; then
        log_message "/dev/${DEVNAME} already mounted at ${MOUNT_POINT}. Skipping."
        exit 0
    fi

    if [ ! -d "${MOUNT_POINT}" ]; then
        mkdir -p "${MOUNT_POINT}"
        if [ $? -ne 0 ]; then
            log_message "Error: Could not create mount point ${MOUNT_POINT}. Exiting."
            exit 1
        fi
    fi

    # Give the system a moment if needed (sometimes helpful for newly appeared devices)
    sleep 1

    # Mount options:
    # - iocharset=utf8: For correct filename encoding.
    # - uid=$(id -u linaro), gid=$(id -g linaro): Mounts as user 'linaro'.
    #   Replace 'linaro' with your desired username or a system user.
    #   Alternatively, use gid=plugdev (if users are in plugdev group) and appropriate fmask/dmask.
    # - fmask=0137, dmask=0027: File/Dir permissions.
    #   fmask=0137 -> owner=rw, group=r, other= --- (640)
    #   dmask=0027 -> owner=rwx, group=rx, other= --- (750)
    #   Adjust as needed. E.g., fmask=0117, dmask=0007 for rwx for owner, rwx for group.
    # - nofail: Prevents boot errors if USB device is problematic or not mountable.
    # - flush: Mounts VFAT with frequent flushing, good for removable media.
    # - sync: Can be used, but 'flush' is often preferred for VFAT on removable media.
    #         Using 'sync' for all I/O can slow things down significantly.
    #         The original script used 'sync' *after* mount, which is less effective.
    USER_NAME="linaro" # CHANGE THIS to your target user if needed
    USER_ID=$(id -u "$USER_NAME")
    GROUP_ID=$(id -g "$USER_NAME")

    if [ -z "$USER_ID" ] || [ -z "$GROUP_ID" ]; then
        log_message "Error: Could not determine UID/GID for user '$USER_NAME'. Mounting with defaults."
        mount -t vfat -o "iocharset=utf8,nofail,flush" "/dev/${DEVNAME}" "${MOUNT_POINT}"
    else
        mount -t vfat -o "iocharset=utf8,uid=${USER_ID},gid=${GROUP_ID},fmask=0137,dmask=0027,nofail,flush" "/dev/${DEVNAME}" "${MOUNT_POINT}"
    fi

    if [ $? -eq 0 ]; then
        log_message "Successfully mounted /dev/${DEVNAME} to ${MOUNT_POINT}."
    else
        log_message "Error: Failed to mount /dev/${DEVNAME} to ${MOUNT_POINT}. Cleaning up directory."
        rmdir "${MOUNT_POINT}" 2>/dev/null # Attempt to remove if empty
        exit 1
    fi

elif [ "$ACTION" == "remove" ]; then
    log_message "Remove event for device that might be mounted at ${MOUNT_POINT} (was /dev/${DEVNAME})."

    # Check if the specific device is mounted at the expected point
    if findmnt --source "/dev/${DEVNAME}" --target "${MOUNT_POINT}" > /dev/null; then
        umount -f "${MOUNT_POINT}" # Force unmount
        if [ $? -eq 0 ]; then
            log_message "Successfully unmounted ${MOUNT_POINT}."
        else
            log_message "Warning: Failed to unmount ${MOUNT_POINT}. Attempting lazy unmount."
            umount -l "${MOUNT_POINT}" # Lazy unmount as a fallback
            if [ $? -eq 0 ]; then
                log_message "Successfully lazy unmounted ${MOUNT_POINT}."
            else
                log_message "Error: Failed to lazy unmount ${MOUNT_POINT}."
            fi
        fi
    elif findmnt "${MOUNT_POINT}" > /dev/null; then
        # The mount point exists but isn't our device, or our device was already unmounted.
        log_message "Mount point ${MOUNT_POINT} is in use by another device or /dev/${DEVNAME} already unmounted. Won't force unmount other devices."
    else
        log_message "Mount point ${MOUNT_POINT} not found or not mounted. Skipping unmount logic."
    fi

    # Remove the directory if it exists and is empty
    if [ -d "${MOUNT_POINT}" ]; then
        if [ -z "$(ls -A "${MOUNT_POINT}")" ]; then # Check if directory is empty
            rmdir "${MOUNT_POINT}"
            if [ $? -eq 0 ]; then
                log_message "Successfully removed directory ${MOUNT_POINT}."
            else
                log_message "Note: Directory ${MOUNT_POINT} not empty after unmount or error removing."
            fi
        else
            log_message "Note: Directory ${MOUNT_POINT} is not empty. Not removing."
        fi
    fi
else
    log_message "Warning: Unknown or no ACTION ('$ACTION') for device /dev/$DEVNAME. Nothing to do."
fi

exit 0
```

**Step 1.2: Create the `udev` Rule**

Create a new file named `/etc/udev/rules.d/85-automount-usb-vfat.rules`:

```
# Udev rule for automatically mounting/unmounting VFAT USB block devices

# Match USB block devices (e.g., partitions on USB sticks) that are VFAT
# SUBSYSTEMS=="usb": Ensures the device is on the USB bus.
# SUBSYSTEM=="block": Ensures it's a block device.
# DRIVERS=="sd": Further refinement for SCSI-like devices (common for USB storage).
# KERNEL=="sd[a-z]*[0-9]": Matches partitions like sdb1, sdc1. Using sd[a-z]* instead of sd[b-z] for more generality if system disk is nvme.
# ENV{ID_FS_TYPE}=="vfat": Only act on VFAT filesystems.
# ACTION=="add": Trigger on device addition.
# RUN+="/usr/local/sbin/mount_usb_helper.sh %k": Execute helper. %k is kernel name (e.g., sdb1).
ACTION=="add", SUBSYSTEMS=="usb", SUBSYSTEM=="block", DRIVERS=="sd", KERNEL=="sd[a-z]*[0-9]", ENV{ID_FS_TYPE}=="vfat", RUN+="/usr/local/sbin/mount_usb_helper.sh %k"

# Rule for removal. Simpler match as we mainly care about the KERNEL name passed to the script.
ACTION=="remove", SUBSYSTEMS=="usb", SUBSYSTEM=="block", DRIVERS=="sd", KERNEL=="sd[a-z]*[0-9]", RUN+="/usr/local/sbin/mount_usb_helper.sh %k"

```
*Self-correction:* The `KERNEL=="sd[a-z]*[0-9]"` combined with `SUBSYSTEMS=="usb"` is generally safe. If your main system disk is also USB and named e.g. `sda`, you might add `ATTRS{removable}=="1"` to only target removable USB block devices, or refine the `KERNEL` pattern like `sd[b-z]*[0-9]`.

**Step 1.3: Apply `udev` Changes**
1.  Reload `udev` rules:
    ```bash
    sudo udevadm control --reload-rules
    ```
2.  Trigger `udev` for existing devices (or just re-plug your USB device):
    ```bash
    sudo udevadm trigger
    ```
Now, when you plug in a VFAT USB drive, it should be automatically mounted by your user `linaro` (or the user you configured) under `/mnt/media/DEVICE_NAME`. Logs will go to syslog tagged with `usb-mount-helper`.

---

**Part 2: Refactoring `gobinet_boot.sh` (SysV init script with LSB)**

This script will remain in `/etc/init.d/` but will be made LSB-compliant.

**Step 2.1: Edit `/etc/init.d/gobinet_boot.sh`**

Replace its content with:

```bash
#!/bin/sh
### BEGIN INIT INFO
# Provides:          gobinet-boot
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Should-Start:      $network # If quectel-CM *needs* basic networking already up.
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Initialize Quectel GobiNet device
# Description:       This service waits for a specified time and then runs
#                    the quectel-CM command to initialize GobiNet hardware.
#                    The Quectel module might provide network connectivity.
### END INIT INFO

# PATH should only include /usr/* if it runs after the mountnfs.sh script
PATH=/sbin:/usr/sbin:/bin:/usr/bin
DESC="Quectel GobiNet initialization"
NAME=gobinet-boot # LSB 'Provides' name
DAEMON_COMMAND=/sbin/quectel-CM # The command to run
SCRIPTNAME=/etc/init.d/gobinet_boot.sh # Actual script name
PIDFILE=/var/run/${NAME}.pid
LOGFILE=/var/log/${NAME}.log
SLEEP_DURATION=60 # Original sleep duration

# Exit if the command is not installed
[ -x "$DAEMON_COMMAND" ] || { echo "$DAEMON_COMMAND not found or not executable."; exit 1; }

# Read configuration variable file if it is present
[ -r /etc/default/$NAME ] && . /etc/default/$NAME

# Load the VERBOSE setting and other rcS variables
. /lib/init/vars.sh

# Define LSB log_* functions.
. /lib/lsb/init-functions

# Function to log messages with timestamp
_log_msg() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOGFILE"
    log_action_msg "$1" # For console via LSB
}

#
# Function that starts the service
#
do_start()
{
    # Check if already running based on PID file and process
    if [ -f "$PIDFILE" ] && ps -p "$(cat "$PIDFILE")" > /dev/null 2>&1; then
        _log_msg "$DESC ($NAME) is already running (PID $(cat $PIDFILE))."
        return 1 # LSB code for already running
    fi

    _log_msg "Starting $DESC ($NAME)..."

    # This subshell runs the sleep and the command in the background.
    # IMPORTANT: This PID management is basic. If quectel-CM is a true daemon,
    # it should create its own PID file. If it does, modify this script to use that.
    (
        _log_msg "Subshell: Sleeping for $SLEEP_DURATION seconds before running $DAEMON_COMMAND."
        sleep "$SLEEP_DURATION"
        _log_msg "Subshell: Executing $DAEMON_COMMAND."
        # Redirect quectel-CM's stdout and stderr to the log file
        "$DAEMON_COMMAND" >> "$LOGFILE" 2>&1
        _log_msg "Subshell: $DAEMON_COMMAND finished or daemonized. Subshell exiting."
        # If quectel-CM daemonizes and creates its own PID, this outer PID is not useful after this point.
    ) &
    # Store the PID of the backgrounded subshell
    echo $! > "$PIDFILE"

    if [ $? -eq 0 ]; then
        _log_msg "$DESC ($NAME) started (subshell PID $!). Check $LOGFILE for $DAEMON_COMMAND output."
        return 0 # Success
    else
        _log_msg "Failed to start $DESC ($NAME) subshell."
        rm -f "$PIDFILE" # Clean up PID file on failure
        return 2 # LSB code for generic error
    fi
}

#
# Function that stops the service
#
do_stop()
{
    _log_msg "Stopping $DESC ($NAME)..."

    if [ ! -f "$PIDFILE" ]; then
        _log_msg "$DESC ($NAME) PID file not found. Assuming not running or already stopped."
        return 1 # LSB code for not running
    fi

    PID_TO_KILL=$(cat "$PIDFILE")
    if ! ps -p "$PID_TO_KILL" > /dev/null 2>&1; then
        _log_msg "$DESC ($NAME) (PID $PID_TO_KILL from PID file) not running. Removing stale PID file."
        rm -f "$PIDFILE"
        return 1 # LSB code for not running
    fi

    # Attempt to stop the process found in the PID file.
    # This will kill the subshell. If quectel-CM daemonized and detached,
    # this won't stop the actual quectel-CM daemon unless it's a child of the subshell
    # and gets killed when the subshell (its parent) is terminated.
    # For a true daemon, you'd need to know its actual PID or have it respond to signals.
    # The `start-stop-daemon --stop` utility is more robust if the process behaves like a daemon.
    # However, we are targeting the subshell's PID here.
    kill "$PID_TO_KILL"
    # Allow some time for the process to terminate
    sleep 2

    if ! ps -p "$PID_TO_KILL" > /dev/null 2>&1; then
        _log_msg "$DESC ($NAME) (PID $PID_TO_KILL) stopped successfully."
        rm -f "$PIDFILE"
        return 0 # Success
    else
        _log_msg "Failed to stop $DESC ($NAME) (PID $PID_TO_KILL) with SIGTERM. Sending SIGKILL."
        kill -9 "$PID_TO_KILL"
        sleep 1
        if ! ps -p "$PID_TO_KILL" > /dev/null 2>&1; then
            _log_msg "$DESC ($NAME) (PID $PID_TO_KILL) killed successfully."
            rm -f "$PIDFILE"
            return 0 # Success
        else
            _log_msg "Error: Failed to kill $DESC ($NAME) (PID $PID_TO_KILL) even with SIGKILL."
            return 2 # LSB code for generic error
        fi
    fi
}

#
# Function that gets the status of the service
#
do_status()
{
    # status_of_proc -p "$PIDFILE" "$DAEMON_COMMAND" "$NAME"
    # The above LSB function is good if DAEMON_COMMAND is the actual long-running process name.
    # Since we are managing a subshell, we'll check the PID from the file.
    if [ -f "$PIDFILE" ]; then
        SERVICE_PID=$(cat "$PIDFILE")
        if ps -p "$SERVICE_PID" > /dev/null 2>&1; then
            log_success_msg "$DESC ($NAME) is running with PID $SERVICE_PID."
            # You could add more info here, e.g., check if quectel-CM is also running if it's a child.
            exit 0 # LSB code for running
        else
            log_failure_msg "$DESC ($NAME) PID file exists, but process $SERVICE_PID is not running. Stale PID file?"
            exit 1 # LSB code for not running but PID file exists (stale)
        fi
    else
        log_failure_msg "$DESC ($NAME) is not running (no PID file)."
        exit 3 # LSB code for not running
    fi
}


case "$1" in
  start)
    do_start
    exit $?
    ;;
  stop)
    do_stop
    exit $?
    ;;
  status)
    do_status
    ;;
  restart|force-reload)
    _log_msg "Restarting $DESC ($NAME)..."
    do_stop
    # Allow some time for graceful shutdown before restarting
    sleep 2
    do_start
    exit $?
    ;;
  *)
    echo "Usage: $SCRIPTNAME {start|stop|status|restart}" >&2
    exit 3
    ;;
esac

exit 0
```

**Step 2.2: Make the script executable**
```bash
sudo chmod +x /etc/init.d/gobinet_boot.sh
```

**Step 2.3: Test the script**
```bash
sudo /etc/init.d/gobinet_boot.sh start
sudo /etc/init.d/gobinet_boot.sh status
# Wait for more than SLEEP_DURATION to see if quectel-CM runs
sudo /etc/init.d/gobinet_boot.sh status
sudo /etc/init.d/gobinet_boot.sh stop
```
Check `/var/log/gobinet-boot.log` for output.

**Step 2.4: Update System's Understanding of the Service**
If you had previously enabled it with `systemd-sysv-install` or `update-rc.d`, systemd might still have an old version of its generated unit.
```bash
sudo systemctl daemon-reload
# If you want to ensure it's enabled for boot (using systemd's SysV generator):
sudo systemctl enable gobinet_boot.sh # Or it might be gobinet-boot based on 'Provides'
```
The `insserv` warnings for `gobinet_boot.sh` should now be gone.

**Important Notes for `gobinet_boot.sh`:**
*   **`quectel-CM` Behavior:** The provided script assumes `quectel-CM` is a command that either:
    1.  Initializes hardware and then exits.
    2.  Starts its own daemon process and detaches correctly (in which case the PID in `/var/run/gobinet-boot.pid` is only for the initial subshell).
    If `quectel-CM` is meant to run continuously as a foreground process *managed by the init script*, the init script would need to be more complex, likely using `start-stop-daemon` to manage it directly.
*   **Dependencies (`Required-Start`, `Should-Start`):**
    *   `$remote_fs $syslog`: Standard, almost always needed.
    *   `$network`: Added as `Should-Start`. If `/sbin/quectel-CM` *needs* the network to be up before it can configure the Quectel modem, this is appropriate. If the Quectel modem *provides* a primary network interface, then this script should likely start *before* the generic `$network` target, or it might be part of a more specific modem management service. You might need to remove `$network` or change it to something like `Before=network.target` in a systemd unit.
*   **`sleep 60`:** This mimics the original script's delay. In a production environment, especially with systemd, you'd ideally look for ways to trigger `quectel-CM` based on device availability or other events rather than a fixed sleep, if possible.

---

**Part 3: The Systemd Native Unit Approach (Recommended for Debian Bullseye)**

While the above steps fix the LSB warnings for your SysV init scripts, Debian Bullseye uses `systemd` as its primary init system. Creating native `systemd` unit files is the modern, more robust, and flexible way to manage services.

**3.1 For `gobinet_boot.sh` functionality -> `gobinet-boot.service`**

Create `/etc/systemd/system/gobinet-boot.service`:

```ini
[Unit]
Description=Quectel GobiNet Initialization Service
Documentation=man:quectel-CM(8) # If a man page exists
# If it needs to run after basic network configuration is attempted:
# After=network.target syslog.target
# If it needs to run before network-online.target is reached:
# Before=network-online.target
# If the GobiNet modem *provides* network, dependencies might be more complex
# or it might be better integrated with ModemManager or netplan/ifupdown.
# For now, let's assume it runs after basic system services are up.
After=syslog.target local-fs.target

[Service]
Type=oneshot # Assumes quectel-CM initializes and exits, or is a self-daemonizing script.
RemainAfterExit=yes # If Type=oneshot, and we consider the 'service' up after the command.
ExecStartPre=/bin/sleep 60 # The original delay
ExecStart=/sbin/quectel-CM
StandardOutput=journal+console # Log to systemd journal and console
StandardError=journal+console

# If quectel-CM is a true daemon that forks and manages its own PID:
# Type=forking
# PIDFile=/var/run/quectel-cm.pid # Path to the PID file quectel-CM creates
# ExecStart=/sbin/quectel-CM <options_if_any>
# GuessMainPID=no # If PIDFile is accurate

# If quectel-CM runs in foreground and systemd should manage it:
# Type=simple
# ExecStart=/sbin/quectel-CM
# Restart=on-failure # Optional: restart if it fails

[Install]
WantedBy=multi-user.target # Start when multi-user target is reached
```

**To use this systemd service:**
1.  Create the file `/etc/systemd/system/gobinet-boot.service` with the content above.
2.  **Disable the SysV init script if you previously enabled it:**
    ```bash
    sudo systemctl disable gobinet_boot.sh # Or update-rc.d gobinet_boot.sh remove
    sudo rm /etc/init.d/gobinet_boot.sh # Optionally remove the old script
    ```
3.  Reload systemd: `sudo systemctl daemon-reload`
4.  Enable the new service: `sudo systemctl enable gobinet-boot.service`
5.  Start it: `sudo systemctl start gobinet-boot.service`
6.  Check status: `sudo systemctl status gobinet-boot.service` and `journalctl -u gobinet-boot.service`

**Advantages of systemd unit for `gobinet-boot`:**
*   **Clearer Dependencies:** `After=`, `Before=`, `Wants=`, `Requires=` offer fine-grained control.
*   **Better Process Management:** `Type=` (simple, forking, oneshot, etc.) correctly defines how systemd handles the process.
*   **Resource Control:** Can set CPU/memory limits, etc.
*   **Integrated Logging:** Output goes directly to the systemd journal.
*   **Simpler Syntax:** Often more straightforward than complex shell scripting for service management.

**3.2 For `mount_usb.sh` functionality (udev is still key)**

The `udev` approach for `mount_usb.sh` is already good and leverages `systemd-udevd.service`. You don't typically create a separate `.service` file for each `udev` `RUN+=` script unless the script needs to start a long-running service managed by systemd. Your helper script is short-lived, so the current udev method is fine.

*Advanced Systemd Automount:*
For truly on-demand mounting managed by systemd (where the mount only happens when the directory is accessed), you could explore systemd `.automount` and `.mount` units. This is more complex to set up than the udev script but offers different benefits. For your current VFAT use case, the udev + helper script is a good balance of simplicity and functionality.

---

**Summary of Recommendations:**

1.  **For `mount_usb.sh`:**
    *   Definitely move it out of `/etc/init.d/`.
    *   Use the `udev` rule and the improved `/usr/local/sbin/mount_usb_helper.sh` script provided above. This addresses the LSB warnings by removing the script from `insserv`'s scope and makes it function correctly.

2.  **For `gobinet_boot.sh`:**
    *   **Option A (Improved SysV):** Use the refactored `/etc/init.d/gobinet_boot.sh` provided. This will fix the LSB warnings.
    *   **Option B (Recommended - Systemd Native):** Create the `gobinet-boot.service` unit file as described. Disable/remove the old SysV script. This is the more modern and robust solution for Debian Bullseye.

By implementing these changes, your system will be cleaner, the `insserv` warnings will be resolved, and your scripts (or their systemd equivalents) will function more reliably and correctly. Remember to carefully test the behavior of `quectel-CM` to choose the best `Type=` and PID management strategy if you opt for the systemd unit.
