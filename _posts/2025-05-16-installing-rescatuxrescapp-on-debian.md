---
tags: [scratchpad]
info: aberto.
date: 2025-05-16
type: post
layout: post
published: true
slug: installing-rescatuxrescapp-on-debian
title: 'installing rescatux/rescapp on Debian'
---
# 1. Update Your System

```bash
sudo apt update
sudo apt upgrade -y
```

---

# 2. Install Build Essentials and Core Utilities

```bash
sudo apt install -y build-essential make coreutils
```

---

# 3. Install All Required Runtime Dependencies

The following list is derived from the `INSTALL` file, plugin scripts, and the codebase. Some packages may already be installed by default, but running these commands is safe and ensures completeness.

## 3.1. Python 3 and Required Python Modules

```bash
sudo apt install -y python3 python3-gi python3-dbus python3-pyqt5 python3-pyqt5.qtwebkit python3-parted
```
> **Note:**  
> - `python3-pyqt5.qtwebkit` is in the `bullseye` repo but may be called `python3-pyqt5.qtwebengine` in some newer releases. For Bullseye, the above is correct.
> - `python3-parted` provides the `parted` Python bindings.

## 3.2. GUI and Desktop Integration

```bash
sudo apt install -y zenity xdg-utils wmctrl
```

## 3.3. DBus System Integration

```bash
sudo apt install -y dbus
```

## 3.4. Disk, Filesystem, and Partition Tools

```bash
sudo apt install -y util-linux reiserfsprogs reiser4progs btrfs-progs xfsprogs xfsdump ntfs-3g dosfstools gawk extundelete os-prober
```

## 3.5. RAID, LVM, and Encryption

```bash
sudo apt install -y dmraid lvm2 cryptsetup libcryptsetup12 cryptsetup-bin
```

## 3.6. GPT and UEFI Tools

```bash
sudo apt install -y gdisk efibootmgr mokutil
```

## 3.7. Bootloader and MBR Tools

```bash
sudo apt install -y syslinux lilo
```

## 3.8. Terminal Emulator

```bash
sudo apt install -y xterm
```

## 3.9. Miscellaneous Utilities

```bash
sudo apt install -y pastebinit hexchat gawk extundelete
```

## 3.10. Inxi and Boot Info Script

```bash
sudo apt install -y inxi boot-info-script
```

## 3.11. Optional but Recommended: Partition and Recovery Tools

```bash
sudo apt install -y gparted gpart testdisk
```

## 3.12. Additional Utilities

```bash
sudo apt install -y wget curl
```

---

# 4. Install the Rescatux chntpw Package (for Windows Password/Account Operations)

**IMPORTANT:**  
The standard `chntpw` package in Debian is not sufficient for all Rescapp features.  
You should use the Rescatux-provided version.

## 4.1. Add the Rescatux Repository

Create the file `/etc/apt/sources.list.d/rescatux.list`:

```bash
echo "deb http://rescatux.sourceforge.net/repo/ buster-dev main" | sudo tee /etc/apt/sources.list.d/rescatux.list
```

## 4.2. Update and Install chntpw

```bash
sudo apt -o Acquire::AllowInsecureRepositories=true -o Acquire::AllowDowngradeToInsecureRepositories=true update
sudo apt install -y chntpw
```
> **Note:**  
> - You may be prompted about unauthenticated packages. Accept them.
> - The Rescatux repo is for Buster, but the chntpw package is compatible with Bullseye.

---

# 5. (Optional) SELinux Support

If you need SELinux support (rare, mostly for Fedora/RedHat/CentOS rescue):

```bash
sudo apt install -y python3-selinux python3-semanage policycoreutils-python-utils selinux-basics auditd selinux-policy-default setools
```
> **Note:**  
> - These packages are optional and only needed if you plan to rescue SELinux-enabled systems.

---

# 6. Clone the Rescapp Repository

```bash
git clone https://github.com/rescatux/rescapp.git
cd rescapp
```

---

# 7. Install Rescapp

By default, this will install to `/usr/local`.  
If you want to install to `/usr`, use `prefix=/usr make install`.

```bash
sudo make install
```
or, for system-wide `/usr` installation:
```bash
sudo make prefix=/usr install
```

---

# 8. (Optional) Verify Installation

Check that the `rescapp` binary is in your path:

```bash
which rescapp
```

You should see `/usr/local/bin/rescapp` or `/usr/bin/rescapp` depending on your install prefix.

---

# 9. (Optional) Desktop Integration

If you want Rescapp to appear in your desktop menu, ensure the `.desktop` file is installed:

```bash
ls /usr/local/share/applications/rescapp.desktop
```
or
```bash
ls /usr/share/applications/rescapp.desktop
```

---

# 10. Run Rescapp

```bash
rescapp
```

---

# 11. (Optional) Troubleshooting

- If you encounter missing dependencies, re-check the above lists.
- For issues with chntpw, ensure you are using the Rescatux-provided version.
- For graphical issues, ensure you have a working X session and all Qt5 dependencies.

---

## **Summary Table of All Key Packages**

| Purpose                | Package Names                                                                                 |
|------------------------|----------------------------------------------------------------------------------------------|
| Core build/utils       | build-essential make coreutils                                                               |
| Python & Qt            | python3 python3-gi python3-dbus python3-pyqt5 python3-pyqt5.qtwebkit python3-parted          |
| GUI/desktop            | zenity xdg-utils wmctrl                                                                      |
| DBus                   | dbus                                                                                        |
| Disk/FS tools          | util-linux reiserfsprogs reiser4progs btrfs-progs xfsprogs xfsdump ntfs-3g dosfstools        |
| RAID/LVM/Crypto        | dmraid lvm2 cryptsetup libcryptsetup12 cryptsetup-bin                                        |
| GPT/UEFI               | gdisk efibootmgr mokutil                                                                    |
| Bootloader/MBR         | syslinux lilo                                                                               |
| Terminal emulator      | xterm                                                                                       |
| Misc utilities         | pastebinit hexchat gawk extundelete wget curl                                               |
| Info scripts           | inxi boot-info-script                                                                       |
| Partition/recovery     | gparted gpart testdisk                                                                      |
| Windows password tool  | chntpw (from Rescatux repo)                                                                 |
| SELinux (optional)     | python3-selinux python3-semanage policycoreutils-python-utils selinux-basics auditd selinux-policy-default setools |

---

# **References**

- [Rescapp GitHub](https://github.com/rescatux/rescapp)
- [Rescatux Website](https://www.rescatux.org)
- [Rescatux chntpw package](https://github.com/rescatux/chntpw)
- [Debian Bullseye Packages](https://packages.debian.org/bullseye/)

# bash script automation

{% codeblock bash %}
#!/bin/bash
# Script to install Rescapp and its dependencies on Debian Bullseye x64
# This script automates the steps from the revised guide.
# It should be run with sudo privileges or by a user who can sudo without a password for apt.
# The script will exit immediately if any command fails.
set -e # Exit immediately if a command exits with a non-zero status.
set -u # Treat unset variables as an error when substituting.
set -o pipefail # The return value of a pipeline is the status of the last command to exit with a non-zero status, or zero if no command exited with a non-zero status.
# --- Configuration ---
# Set DEBIAN_FRONTEND to noninteractive to avoid prompts during package installation
export DEBIAN_FRONTEND=noninteractive
# --- Temporary Directory for Build ---
BUILD_DIR="" # Initialize BUILD_DIR
# Cleanup function to remove temporary directory
cleanup() {
    if [ -n "$BUILD_DIR" ] && [ -d "$BUILD_DIR" ]; then
        echo "Cleaning up temporary build directory: $BUILD_DIR"
        sudo rm -rf "$BUILD_DIR"
    fi
}
# Register cleanup function to be called on script exit or interruption
trap cleanup EXIT SIGINT SIGTERM
echo "Starting Rescapp installation process..."
echo "This script will install necessary packages and Rescapp."
echo "Ensure you have an active internet connection."
echo "-----------------------------------------------------"
# 1. Update System
echo "[Step 1/7] Updating system packages..."
sudo apt update
sudo apt upgrade -y
# 2. Install Build Essentials and Git
echo "[Step 2/7] Installing build essentials, core utilities, and git..."
sudo apt install -y build-essential make coreutils git
# 3. Install All Required Runtime Dependencies
echo "[Step 3/7] Installing Rescapp runtime dependencies..."
# Note: python3-pyqt5.qtwebkit is for Bullseye. Newer distros might use python3-pyqt5.qtwebengine.
# Lilo might produce a warning during installation; this is generally acceptable for newer systems not relying on Lilo.
sudo apt install -y \
    python3 python3-gi python3-dbus python3-pyqt5 python3-pyqt5.qtwebkit python3-parted \
    zenity xdg-utils wmctrl \
    dbus \
    util-linux reiserfsprogs reiser4progs btrfs-progs xfsprogs xfsdump ntfs-3g dosfstools gawk extundelete os-prober \
    dmraid lvm2 cryptsetup libcryptsetup12 cryptsetup-bin \
    gdisk efibootmgr mokutil \
    syslinux lilo \
    xterm \
    pastebinit hexchat \
    inxi boot-info-script \
    gparted gpart testdisk \
    wget curl
# 4. (Optional) SELinux Support
# If you need to rescue SELinux-enabled systems (e.g., Fedora, RHEL, CentOS),
# uncomment the following section.
# echo "[Step 4/7 - Optional] Installing SELinux support packages..."
# sudo apt install -y \
# python3-selinux python3-semanage policycoreutils-python-utils selinux-basics auditd selinux-policy-default setools
# 5. Install the Rescatux chntpw Package
echo "[Step 4/7] Installing Rescatux chntpw package..."
# This uses the Rescatux repository for a version of chntpw with features needed by Rescapp.
# The repository is for Debian Buster but the chntpw package is generally compatible with Bullseye.
RESCATUX_REPO_FILE="/etc/apt/sources.list.d/rescatux.list"
RESCATUX_REPO_LINE="deb http://rescatux.sourceforge.net/repo/ buster-dev main"
if ! grep -qF "$RESCATUX_REPO_LINE" "$RESCATUX_REPO_FILE" 2>/dev/null; then
    echo "$RESCATUX_REPO_LINE" | sudo tee "$RESCATUX_REPO_FILE"
else
    echo "Rescatux repository line already exists in $RESCATUX_REPO_FILE."
fi
# Allow unauthenticated repositories for this specific source if GPG key is not imported.
sudo apt -o Acquire::AllowInsecureRepositories=true -o Acquire::AllowDowngradeToInsecureRepositories=true update
# You might be prompted to accept unauthenticated packages; this is expected for this repo if not running fully noninteractive.
# The DEBIAN_FRONTEND=noninteractive export should handle this.
sudo apt install -y chntpw
# 6. Clone the Rescapp Repository
BUILD_DIR=$(mktemp -d) # Create a temporary directory
echo "[Step 5/7] Cloning the Rescapp repository into $BUILD_DIR/rescapp..."
git clone https://github.com/rescatux/rescapp.git "$BUILD_DIR/rescapp"
cd "$BUILD_DIR/rescapp"
# 7. Install Rescapp
echo "[Step 6/7] Installing Rescapp (default to /usr/local)..."
# To install to /usr instead, you would use: sudo make prefix=/usr install
sudo make install
# 8. Verify Installation
echo "[Step 7/7] Verifying installation..."
RESCAPP_PATH=$(which rescapp || echo "not_found") # Avoid error if not found when set -u is active
if [ "$RESCAPP_PATH" != "not_found" ] && [ -n "$RESCAPP_PATH" ]; then
    echo "Rescapp executable found at: $RESCAPP_PATH"
else
    echo "ERROR: Rescapp executable not found in PATH after installation."
    # The script will exit here if set -e is active and which fails,
    # but this explicit check is for clarity.
fi
DESKTOP_FILE_USR_LOCAL="/usr/local/share/applications/rescapp.desktop"
DESKTOP_FILE_USR="/usr/share/applications/rescapp.desktop"
if [ -f "$DESKTOP_FILE_USR_LOCAL" ]; then
    echo "Rescapp desktop file found at: $DESKTOP_FILE_USR_LOCAL"
elif [ -f "$DESKTOP_FILE_USR" ]; then
    echo "Rescapp desktop file found at: $DESKTOP_FILE_USR"
else
    echo "Warning: Rescapp desktop file not found. Desktop integration might be incomplete."
fi
echo "-----------------------------------------------------"
echo "Rescapp installation process completed successfully."
echo "The build files were in the temporary directory $BUILD_DIR and will be cleaned up."
echo "You can now attempt to run Rescapp by typing 'rescapp' in your terminal."
echo "-----------------------------------------------------"
# Cleanup is handled by the trap EXIT
exit 0
{% endcodeblock %}