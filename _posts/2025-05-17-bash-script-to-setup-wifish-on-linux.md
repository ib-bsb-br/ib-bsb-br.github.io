---
tags: [scripts>bash,software>linux]
info: aberto.
date: 2025-05-17
type: post
layout: post
published: true
slug: bash-script-to-setup-wifish-on-linux
title: "bash script to setup 'wifish' on Linux"
---
{% codeblock bash %}
#!/bin/bash
# This script automates the setup of 'wifish' on a Debian Bullseye system.
# Version 2: Improved backup, idempotency, and interface detection.
#
# IMPORTANT: This script makes certain assumptions:
# 1. It should be run as root.
# 2. It attempts to auto-detect the Wi-Fi interface. If detection fails or is
#    incorrect, the default "wlan0" is used, or you may need to edit the script
#    or use wifish with the -i flag.
# 3. The active wpa_supplicant configuration file is assumed to be
#    '/etc/wpa_supplicant/wpa_supplicant.conf'. If different, this needs to be changed.
# 4. It will attempt to identify the primary non-root user (UID 1000 or SUDO_USER)
#    to add to the 'netdev' group.
#
# Review these assumptions and the script content before execution.

set -e # Exit immediately if a command exits with a non-zero status.

# --- Configuration ---
DEFAULT_WIFI_INTERFACE="wlan0"
WPA_SUPPLICANT_CONF_FILE="/etc/wpa_supplicant/wpa_supplicant.conf"
WIFI_INTERFACE="" # Will be auto-detected or fall back to DEFAULT_WIFI_INTERFACE

# Determine the primary non-root user to add to the 'netdev' group.
PRIMARY_USER=""
if [ -n "$SUDO_USER" ] && [ "$SUDO_USER" != "root" ]; then # Prefer SUDO_USER if available and not root
    PRIMARY_USER="$SUDO_USER"
elif command -v id >/dev/null && id -u 1000 &>/dev/null; then # Try UID 1000
    PRIMARY_USER_UID1000=$(id -un 1000)
    if [ "$PRIMARY_USER_UID1000" != "root" ]; then # Ensure user 1000 is not root
        PRIMARY_USER="$PRIMARY_USER_UID1000"
    fi
fi
# Fallback to parsing /etc/passwd if PRIMARY_USER is still not set
if [ -z "$PRIMARY_USER" ]; then
    PRIMARY_USER=$(awk -F: '($3>=1000 && $1 != "root" && $1 != "" && $1 != "nobody"){print $1; exit}' /etc/passwd)
fi


# --- Helper Functions ---
log_action() {
    echo "[INFO] $1"
}

log_warning() {
    echo "[WARNING] $1"
}

log_error() {
    echo "[ERROR] $1" >&2
}

# --- Wi-Fi Interface Detection ---
detect_wifi_interface() {
    log_action "Attempting to auto-detect Wi-Fi interface..."
    local detected_iface=""
    # Try with 'iw dev' first, common for Wi-Fi specific tools
    if command -v iw >/dev/null; then
        detected_iface=$(iw dev | awk '$1=="Interface"{print $2; exit}')
    fi

    # If 'iw dev' didn't yield a result, try with 'ip link' for wlan*
    if [ -z "$detected_iface" ] && command -v ip >/dev/null; then
        detected_iface=$(ip -o link show type wlan | awk -F': ' '{print $2; exit}' | awk '{print $1}')
    fi

    # If still no result, try 'ip link' for wlp* (common alternative naming)
    if [ -z "$detected_iface" ] && command -v ip >/dev/null; then
        detected_iface=$(ip -o link show | grep -Eo 'wlp[0-9]+s[0-9]+' | head -n1)
    fi

    if [ -n "$detected_iface" ]; then
        WIFI_INTERFACE="$detected_iface"
        log_action "Detected Wi-Fi interface: $WIFI_INTERFACE. Using this."
    else
        WIFI_INTERFACE="$DEFAULT_WIFI_INTERFACE"
        log_warning "Could not auto-detect Wi-Fi interface. Using default: $WIFI_INTERFACE."
        log_warning "If this is incorrect, review script or use wifish with the '-i <your_interface>' option."
    fi
}


# --- Main Script ---

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
  log_error "This script must be run as root. Please use 'sudo $0' or run as the root user."
  exit 1
fi

detect_wifi_interface # Call detection function

log_action "Starting wifish setup script (v2)..."
log_action "Using Wi-Fi Interface: ${WIFI_INTERFACE}"
log_action "Targeting wpa_supplicant config: ${WPA_SUPPLICANT_CONF_FILE}"

if [ -n "$PRIMARY_USER" ]; then
    log_action "Primary non-root user identified for 'netdev' group: ${PRIMARY_USER}"
else
    log_warning "Could not automatically detect a primary non-root user. Manual 'usermod -a -G netdev youruser' might be required."
fi
echo "---------------------------------------------------------------------"

# Phase 1: Prerequisites and Getting wifish
log_action "Phase 1: Installing prerequisites and getting wifish..."
log_action "Updating package lists (apt update)..."
if ! apt update -qq; then
    log_error "apt update failed. Please check your network connection and apt sources."
    exit 1
fi

log_action "Installing gawk, dialog, git..."
if ! apt install -y gawk dialog git; then
    log_error "Failed to install required packages. Please check apt output for errors."
    exit 1
fi

TEMP_WIFISH_DIR="/tmp/bougyman-wifish_install_temp_$(date +%Y%m%d%H%M%S)"
log_action "Cloning wifish repository to $TEMP_WIFISH_DIR..."
rm -rf "$TEMP_WIFISH_DIR" # Clean up if exists
if ! git clone https://github.com/bougyman/wifish.git "$TEMP_WIFISH_DIR"; then
    log_error "Failed to clone wifish repository. Check internet connection and git."
    exit 1
fi

log_action "Setting execute permissions for scripts in repository..."
(
    cd "$TEMP_WIFISH_DIR"
    chmod +x wifish install.sh test/test.sh
    chmod +x sv/wpa_supplicant/run sv/wpa_supplicant/log/run
)
log_action "Phase 1 complete."
echo "---------------------------------------------------------------------"

# Phase 2: Configuring wpa_supplicant
log_action "Phase 2: Configuring wpa_supplicant..."
log_action "Ensuring wpa_supplicant configuration file directory exists: $(dirname "$WPA_SUPPLICANT_CONF_FILE")"
mkdir -p "$(dirname "$WPA_SUPPLICANT_CONF_FILE")"

if [ ! -f "$WPA_SUPPLICANT_CONF_FILE" ]; then
    log_action "Creating empty wpa_supplicant configuration file: $WPA_SUPPLICANT_CONF_FILE"
    touch "$WPA_SUPPLICANT_CONF_FILE"
fi

TIMESTAMP=$(date +%Y%m%d%H%M%S)
BACKUP_FILE="${WPA_SUPPLICANT_CONF_FILE}.${TIMESTAMP}.bak"
log_action "Backing up current $WPA_SUPPLICANT_CONF_FILE to $BACKUP_FILE..."
if cp "$WPA_SUPPLICANT_CONF_FILE" "$BACKUP_FILE"; then
    log_action "Backup successful: $BACKUP_FILE"
else
    log_warning "Failed to create backup of $WPA_SUPPLICANT_CONF_FILE. Proceeding with caution."
fi

log_action "Configuring 'ctrl_interface' and 'update_config' in $WPA_SUPPLICANT_CONF_FILE for idempotency..."

# Comment out any existing ctrl_interface lines to avoid conflicts
sed -i -E 's/^[[:space:]]*ctrl_interface=.*$/#& (old_ctrl_interface, commented by wifish_setup.sh)/' "$WPA_SUPPLICANT_CONF_FILE"
# Add the correct ctrl_interface line if it's not already present (uncommented)
if ! grep -qFx "ctrl_interface=DIR=/run/wpa_supplicant GROUP=netdev" "$WPA_SUPPLICANT_CONF_FILE"; then
    log_action "Adding 'ctrl_interface=DIR=/run/wpa_supplicant GROUP=netdev' to $WPA_SUPPLICANT_CONF_FILE."
    echo "ctrl_interface=DIR=/run/wpa_supplicant GROUP=netdev" >> "$WPA_SUPPLICANT_CONF_FILE"
else
    log_action "'ctrl_interface=DIR=/run/wpa_supplicant GROUP=netdev' already present or re-added."
fi

# Comment out any existing update_config lines
sed -i -E 's/^[[:space:]]*update_config=.*$/#& (old_update_config, commented by wifish_setup.sh)/' "$WPA_SUPPLICANT_CONF_FILE"
# Add the correct update_config line if it's not already present (uncommented)
if ! grep -qFx "update_config=1" "$WPA_SUPPLICANT_CONF_FILE"; then
    log_action "Adding 'update_config=1' to $WPA_SUPPLICANT_CONF_FILE."
    echo "update_config=1" >> "$WPA_SUPPLICANT_CONF_FILE"
else
    log_action "'update_config=1' already present or re-added."
fi

log_action "Securing $WPA_SUPPLICANT_CONF_FILE permissions (chmod 600)..."
chmod 600 "$WPA_SUPPLICANT_CONF_FILE"

USER_MODIFIED_LOGIN_MESSAGE=""
if [ -n "$PRIMARY_USER" ]; then
    log_action "Ensuring 'netdev' group exists and adding user '$PRIMARY_USER' to it..."
    if ! getent group netdev >/dev/null; then
        log_action "Group 'netdev' does not exist. Creating it..."
        if ! groupadd --system netdev; then # Use --system for system groups if appropriate
            log_warning "Could not create group 'netdev'. Manual creation (groupadd netdev) might be needed."
        else
            log_action "Group 'netdev' created."
        fi
    fi
    # Check if user is already in group to avoid unnecessary usermod message
    if ! groups "$PRIMARY_USER" | grep -q '\bnetdev\b'; then
        if ! usermod -a -G netdev "$PRIMARY_USER"; then
             log_warning "Failed to add user '$PRIMARY_USER' to 'netdev' group. Check permissions or do it manually."
        else
            USER_MODIFIED_LOGIN_MESSAGE="User '$PRIMARY_USER' has been added to the 'netdev' group. IMPORTANT: '$PRIMARY_USER' MUST log out and log back in for this change to take effect."
            log_action "$USER_MODIFIED_LOGIN_MESSAGE"
        fi
    else
        log_action "User '$PRIMARY_USER' is already a member of the 'netdev' group."
        USER_MODIFIED_LOGIN_MESSAGE="User '$PRIMARY_USER' is a member of 'netdev'. If this membership is recent, a logout/login might still be needed for all services to recognize it."

    fi
else
    USER_MODIFIED_LOGIN_MESSAGE="IMPORTANT: Could not automatically determine a primary non-root user. Please manually add your regular user to the 'netdev' group (e.g., 'sudo usermod -a -G netdev yourusername') and then log out and log back in."
    log_warning "$USER_MODIFIED_LOGIN_MESSAGE"
fi

log_action "Attempting to restart wpa_supplicant for interface '$WIFI_INTERFACE'..."
WPA_RESTARTED_MANUALLY_MSG="If wpa_supplicant was restarted, it should pick up the new configuration. If not, a manual restart of wpa_supplicant or a system reboot might be necessary."

SERVICE_NAME="wpa_supplicant@${WIFI_INTERFACE}.service"
SERVICE_EXISTS=false
if systemctl list-unit-files | grep -q "^${SERVICE_NAME}"; then # More precise grep
    SERVICE_EXISTS=true
fi

if [ "$SERVICE_EXISTS" = true ]; then
    log_action "${SERVICE_NAME} found."
    if systemctl is-active --quiet "${SERVICE_NAME}"; then
        log_action "Restarting ${SERVICE_NAME} via systemd..."
        if ! systemctl restart "${SERVICE_NAME}"; then
            log_warning "Failed to restart ${SERVICE_NAME}. Check 'systemctl status ${SERVICE_NAME}' and 'journalctl -u ${SERVICE_NAME}'."
        fi
    else
        log_action "${SERVICE_NAME} exists but is not active. Attempting to enable and start it..."
        if ! systemctl enable "${SERVICE_NAME}" --now; then
             log_warning "Failed to enable and start ${SERVICE_NAME}. Check status and journal."
        fi
    fi
elif [ -f "/etc/network/interfaces" ] && grep -q "iface ${WIFI_INTERFACE} inet" /etc/network/interfaces; then # More specific grep
    log_action "Attempting to restart network interface ${WIFI_INTERFACE} via ifdown/ifup..."
    ifdown "${WIFI_INTERFACE}" >/dev/null 2>&1 || true # Ignore errors if already down
    if ! ifup "${WIFI_INTERFACE}"; then
        log_warning "ifup ${WIFI_INTERFACE} failed. Manual network reconfiguration might be needed. Check /etc/network/interfaces configuration."
    fi
else
    WPA_RESTARTED_MANUALLY_MSG="Could not determine how wpa_supplicant is managed for '${WIFI_INTERFACE}' (no specific systemd service or /etc/network/interfaces entry found). A manual restart of wpa_supplicant or a system reboot might be necessary to apply configuration changes."
    log_warning "$WPA_RESTARTED_MANUALLY_MSG"
fi
log_action "Phase 2 complete."
echo "---------------------------------------------------------------------"

# Phase 3: Implementing wifish (System-Wide Installation)
log_action "Phase 3: Installing wifish system-wide..."
(
    cd "$TEMP_WIFISH_DIR"
    log_action "Running install.sh from wifish repository (current directory: $(pwd))..."
    if ! ./install.sh; then
        log_error "wifish install.sh script failed. Please check output for errors."
        log_action "Cleaning up temporary directory $TEMP_WIFISH_DIR..."
        rm -rf "$TEMP_WIFISH_DIR"
        exit 1
    fi
)
log_action "wifish's install.sh completed."
if [ -f "$TEMP_WIFISH_DIR/test/test.sh" ]; then
    log_action "The wifish repository includes a test script: $TEMP_WIFISH_DIR/test/test.sh"
    log_action "You can explore running it manually from the '$TEMP_WIFISH_DIR' directory if desired (e.g., './test/test.sh')."
    log_action "Note: This test script typically mocks wpa_cli and runs its own checks."
fi
log_action "Phase 3 complete."
echo "---------------------------------------------------------------------"

# Phase 4: Using wifish (Information for the user)
log_action "Phase 4: Information on using wifish..."
log_action "wifish should now be installed and available as the 'wifish' command."
log_action "Example usage (as the non-root user, AFTER they have logged back in if their group membership was changed):"
log_action "  wifish list"
log_action "  wifish menu"
log_action "  wifish connect \"Your_Network_SSID\""
log_action " "
log_action "If wifish needs to target a specific interface (detected/defaulted to '${WIFI_INTERFACE}'), use:"
log_action "  wifish -i ${WIFI_INTERFACE} menu"
log_action "or set the environment variable for the session:"
log_action "  export WPA_CLI_INTERFACE=${WIFI_INTERFACE}  (unset with 'unset WPA_CLI_INTERFACE')"
log_action " "
log_action "IMPORTANT NOTE ON IP ADDRESS:"
log_action "wifish handles the Wi-Fi connection (association). After connecting,"
log_action "your system still needs an IP address to access the internet."
log_action "If not configured automatically, run as root (or with sudo):"
log_action "  dhclient ${WIFI_INTERFACE}"
log_action "(Or use another DHCP client like 'dhcpcd5' if installed and preferred, or check 'systemd-networkd' if active)."
log_action "Phase 4 complete."
echo "---------------------------------------------------------------------"

# Final messages
log_action "wifish setup script finished."
if [ -n "$USER_MODIFIED_LOGIN_MESSAGE" ]; then
    log_action "$USER_MODIFIED_LOGIN_MESSAGE"
fi
log_action "$WPA_RESTARTED_MANUALLY_MSG"
log_action " "
log_action "To test, AFTER the designated user ('${PRIMARY_USER:-your regular user}') has potentially logged out and back in:"
log_action "1. Open a new terminal as that user."
log_action "2. Run 'wpa_cli status'. It should show connection details without needing sudo."
log_action "3. Run 'wifish list' or 'wifish menu'."
log_action " "
log_action "The script used Wi-Fi interface '${WIFI_INTERFACE}'. If this was incorrect,"
log_action "use wifish with the '-i <your_actual_interface>' flag."

log_action "Cleaning up temporary directory $TEMP_WIFISH_DIR..."
rm -rf "$TEMP_WIFISH_DIR"

log_action "Setup complete. Backup of wpa_supplicant config (if it existed) is at: $BACKUP_FILE"
echo "---------------------------------------------------------------------"

exit 0
{% endcodeblock %}
