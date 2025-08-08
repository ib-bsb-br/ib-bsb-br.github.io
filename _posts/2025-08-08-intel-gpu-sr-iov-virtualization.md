---
tags: [scratchpad]
info: aberto.
date: 2025-08-08
type: post
layout: post
published: true
slug: intel-gpu-sr-iov-virtualization
title: 'Intel GPU SR-IOV virtualization'
---
```
#!/bin/bash

# ==============================================================================
# Fully Automated Intel GPU SR-IOV Host Setup Script
#
# This script is a robust, idempotent, and fully automated solution for
# configuring an Ubuntu host for Intel GPU SR-IOV virtualization.
#
# It performs the following actions:
# 1.  Auto-detects the primary Intel GPU.
# 2.  Verifies the system has virtualization and SR-IOV capabilities.
# 3.  Installs all necessary dependencies (git, dkms, etc.).
# 4.  Safely and idempotently configures GRUB with required kernel parameters.
# 5.  Clones, builds, and installs the i915-sriov-dkms driver from source.
# 6.  Configures sysfs to persist Virtual Function (VF) creation on boot.
#
# USAGE:
#   chmod +x setup_sriov_host.sh
#   sudo ./setup_sriov_host.sh [num_vfs]
#
#   [num_vfs] is an optional argument for the number of Virtual Functions.
#   If not provided, it defaults to 7.
#
# ==============================================================================

set -e # Exit immediately if a command exits with a non-zero status.

# --- Configuration & Colors ---
NUM_VFS=${1:-7} # Default to 7 VFs if no argument is provided
DRIVER_REPO="https://github.com/strongtz/i915-sriov-dkms.git"
DKMS_NAME="i915-sriov-dkms"
DKMS_VERSION="1.22.07.20"

# Color codes for output
C_RESET='\033[0m'
C_RED='\033[0;31m'
C_GREEN='\033[0;32m'
C_YELLOW='\033[0;33m'
C_BLUE='\033[0;34m'

# --- Helper Functions ---

# Print a formatted message
log() {
    echo -e "${C_BLUE}INFO:${C_RESET} $1"
}

# Print a success message
success() {
    echo -e "${C_GREEN}SUCCESS:${C_RESET} $1"
}

# Print a warning message
warn() {
    echo -e "${C_YELLOW}WARNING:${C_RESET} $1"
}

# Print an error message and exit
error_exit() {
    echo -e "${C_RED}ERROR:${C_RESET} $1" >&2
    exit 1
}

# Check if the script is run as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
       error_exit "This script must be run as root. Please use sudo."
    fi
}

# Auto-detect the primary Intel GPU's PCI address
autodetect_gpu() {
    log "Detecting primary Intel VGA controller..."
    GPU_PCI_ADDRESS=$(lspci -nn | grep -i 'VGA compatible controller.*Intel' | head -n1 | awk '{print $1}')
    if [[ -z "$GPU_PCI_ADDRESS" ]]; then
        error_exit "Could not find an Intel VGA compatible controller."
    fi
    success "Found Intel GPU at PCI address: $GPU_PCI_ADDRESS"
}

# Verify hardware and kernel support
verify_prerequisites() {
    log "Verifying system prerequisites..."
    # Check for CPU virtualization support
    if ! grep -q -E 'vmx|svm' /proc/cpuinfo; then
        error_exit "CPU virtualization (VT-x/AMD-V) is not enabled in the BIOS."
    fi
    success "CPU virtualization is enabled."

    # Check for SR-IOV capability on the detected GPU
    if ! lspci -vvv -s "$GPU_PCI_ADDRESS" | grep -iq "Single Root I/O Virtualization"; then
        warn "This GPU does not report SR-IOV capabilities. The process may fail."
    else
        success "GPU reports SR-IOV capabilities."
    fi
}


# --- Main Logic Functions ---

install_dependencies() {
    log "Updating package lists and installing dependencies..."
    apt-get update > /dev/null
    apt-get install -y git dkms sysfsutils build-essential linux-headers-$(uname -r)
    success "Dependencies installed."
}

# Safely and idempotently configure GRUB
configure_grub() {
    log "Configuring GRUB for IOMMU and SR-IOV..."
    local GRUB_FILE="/etc/default/grub"
    local PARAMS_TO_ADD=("intel_iommu=on" "i915.enable_guc=3")
    
    local CURRENT_CMDLINE=$(grep "GRUB_CMDLINE_LINUX_DEFAULT" "$GRUB_FILE" | cut -d'"' -f2)
    local NEW_CMDLINE="$CURRENT_CMDLINE"
    local CHANGES_MADE=0

    for param in "${PARAMS_TO_ADD[@]}"; do
        if ! [[ "$CURRENT_CMDLINE" =~ $param ]]; then
            NEW_CMDLINE="$NEW_CMDLINE $param"
            CHANGES_MADE=1
            log "Adding kernel parameter: $param"
        fi
    done

    if [[ $CHANGES_MADE -eq 1 ]]; then
        log "Backing up GRUB config to ${GRUB_FILE}.bak"
        cp "$GRUB_FILE" "${GRUB_FILE}.bak"
        sed -i "s#GRUB_CMDLINE_LINUX_DEFAULT=\"$CURRENT_CMDLINE\"#GRUB_CMDLINE_LINUX_DEFAULT=\"$NEW_CMDLINE\"#" "$GRUB_FILE"
        success "GRUB configuration updated."
    else
        success "GRUB parameters are already correctly configured."
    fi
    
    log "Updating GRUB and initramfs..."
    update-grub
    update-initramfs -u -k all
    success "GRUB and initramfs updated."
}


# Clone, build, and install the DKMS driver from source
clone_and_install_driver() {
    log "Cloning and installing i915-sriov-dkms driver..."
    local DRIVER_DIR="/usr/src/${DKMS_NAME}-${DKMS_VERSION}"

    if [ -d "$DRIVER_DIR" ]; then
        warn "Driver source directory already exists. Assuming it's installed."
        return
    fi

    log "Cloning repository from $DRIVER_REPO..."
    git clone "$DRIVER_REPO" "$DRIVER_DIR"
    
    log "Adding driver to DKMS..."
    dkms add -m "$DKMS_NAME" -v "$DKMS_VERSION"
    log "Building driver with DKMS..."
    dkms build -m "$DKMS_NAME" -v "$DKMS_VERSION"
    log "Installing driver with DKMS..."
    dkms install -m "$DKMS_NAME" -v "$DKMS_VERSION"

    success "SR-IOV DKMS driver installed."
}

# Configure sysfs for persistent VF creation
configure_persistence() {
    log "Configuring sysfs for persistent Virtual Functions..."
    local SYSFS_CONF_FILE="/etc/sysfs.conf"
    local SYSFS_LINE="devices/pci0000:00/${GPU_PCI_ADDRESS}/sriov_numvfs = ${NUM_VFS}"

    if grep -Fxq "$SYSFS_LINE" "$SYSFS_CONF_FILE"; then
        success "sysfs is already configured for persistence."
    else
        log "Adding VF persistence rule to $SYSFS_CONF_FILE"
        echo "" >> "$SYSFS_CONF_FILE"
        echo "# Automatically create ${NUM_VFS} VFs for Intel GPU ${GPU_PCI_ADDRESS}" >> "$SYSFS_CONF_FILE"
        echo "$SYSFS_LINE" >> "$SYSFS_CONF_FILE"
        success "sysfs configured to create ${NUM_VFS} VFs on boot."
    fi
}

# --- Main Execution ---

main() {
    check_root
    log "🚀 Starting Fully Automated SR-IOV Host Setup..."
    log "Will configure the system to create ${C_YELLOW}${NUM_VFS}${C_RESET} Virtual Functions."
    
    autodetect_gpu
    verify_prerequisites
    install_dependencies
    configure_grub
    clone_and_install_driver
    configure_persistence
    
    echo ""
    success "🎉 ========================================================= 🎉"
    success "Host setup is complete."
    warn "A reboot is required to apply all kernel and driver changes."
    warn "Please run 'sudo reboot' now."
    success "🎉 ========================================================= 🎉"
}

main
```