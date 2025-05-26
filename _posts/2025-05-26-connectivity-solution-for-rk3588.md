---
tags: [scratchpad]
info: aberto.
date: 2025-05-26
type: post
layout: post
published: true
slug: connectivity-solution-for-rk3588
title: 'Connectivity Solution for RK3588'
---

# sudo apt install
```
sudo apt install -y dialog network-manager wpasupplicant isc-dhcp-client iproute2 iw iputils-ping wireless-tools procps mawk
```

Section 1: Introduction and Script Objective
The primary objective of this document and the accompanying shell script (universal_connect.sh) is to furnish a robust and interactive solution for establishing internet connectivity on the RK3588 VPC-3588 single-board computer, specifically when operating under Debian Bullseye. This system is designed to address the common challenge encountered when the device is relocated to new physical environments where existing network configurations—be it wired Ethernet or wireless Wi-Fi—are unknown.

The core problem addressed is the unpredictability of network availability and parameters in such new environments. This includes uncertainty regarding the type of connection available (Ethernet or Wi-Fi), the method of IP address assignment (DHCP or static), and the necessary credentials or authentication protocols for secure networks.

The proposed solution is a comprehensive bash script that, when executed with root privileges, systematically attempts various methods to connect to the internet. It prioritizes a user-friendly, interactive approach, prompting for essential information such as Wi-Fi SSIDs, passwords, or static IP details only when necessary. The script leverages standard, widely available Linux networking utilities to maximize compatibility and reliability.

The target hardware, the VPC-3588 motherboard, is based on the Rockchip RK3588 high-performance application processor. This hardware platform is equipped with a Gigabit Ethernet port and a built-in Wi-Fi 6 module, providing the physical interfaces the script will manage. The script is tailored for the Debian Bullseye operating system, considering its typical networking stack.

Key features of the script (Version 2):

Adaptability: Capable of handling both Ethernet and Wi-Fi connections.

Interactivity: Employs a terminal user interface (TUI) using dialog to prompt the user for necessary information.

Multi-tool Approach: Utilizes NetworkManager (via nmcli) if active, with fallbacks to wpa_supplicant (and wpa_cli), dhclient (from isc-dhcp-client), and iproute2 commands (ip).

Systematic Probing: Follows a logical sequence of attempts, starting with simpler methods.

Prerequisite Handling: Checks for and offers to install missing essential packages (e.g., dialog, nmcli).

Robust Error Handling: Includes checks for dialog cancellations and improved logic for various network operations.

WEP Key Flexibility: Correctly handles both ASCII and HEX WEP keys for wpa_supplicant.

rfkill Awareness: Checks if Wi-Fi is soft-blocked and offers to unblock it.

Enhanced User Feedback: Provides more infobox messages during long operations.

Improved Cleanup: Uses a trap to attempt cleanup of temporary files on exit.

The aim to "guarantee an internet connection" is ambitious. While a 100% guarantee is contingent on external factors (e.g., physical network presence, functional internet service from the provider, captive portals), the script endeavors to exhaust all software-controllable avenues.

Section 2: Prerequisites and System Environment
For the connectivity script to function optimally on the RK3588 VPC-3588 running Debian Bullseye:

Essential Software Packages:
The script will check for and offer to install the following if missing (this requires a temporary internet connection or cached packages, and adheres to the warning against full system upgrades on potentially sensitive RK3588 images):

dialog: For the interactive TUI.

network-manager: For nmcli (if NetworkManager is to be used).

wpasupplicant: For wpa_supplicant and wpa_cli (Wi-Fi security).

isc-dhcp-client: For dhclient (or another DHCP client if preferred and adapted in script).

iproute2: For the ip command.

iw: For iw (Wi-Fi scanning and configuration, preferred over iwlist).

iputils-ping: For ping (connectivity testing).

rfkill: For checking and unblocking wireless devices.

Target Hardware Interfaces:
The VPC-3588 motherboard features:

1 x Gigabit Ethernet RJ45 port.

1 x Built-in Wi-Fi 6 module.
The script dynamically identifies these interfaces (e.g., eth0, wlan0).

Debian Bullseye Considerations:
The script checks if NetworkManager is active. If so, nmcli is the preferred tool. Otherwise, it falls back to direct configuration methods.

Section 3: Script Architecture and Operational Flow
The script uses a modular design with bash functions for clarity and reusability.

Core Operational Flow:

Initial Setup:

Checks for root privileges.

Sets up an EXIT trap for cleaning temporary files.

Checks for and offers to install missing prerequisite packages.

Detection Phase:

Detects available Ethernet and Wi-Fi interfaces.

Checks if NetworkManager service is active.

Initial Connectivity Check:

Tests if an internet connection already exists. If so, exits.

Main Menu Loop: Presents options to the user:

Configure Ethernet.

Configure Wi-Fi.

Re-check Internet Connectivity.

Exit.

Ethernet Configuration (handle_ethernet_connection):

Prompts user to select an Ethernet interface if multiple exist.

Offers DHCP configuration:

Uses nmcli if NetworkManager is active.

Falls back to dhclient and ip commands.

If DHCP fails or is skipped, offers static IP configuration:

Prompts for IP/CIDR, gateway, DNS.

Uses nmcli or ip commands.

If local configuration steps seem successful, returns to main loop for a final connectivity check.

Wi-Fi Configuration (handle_wifi_connection):

Prompts user to select a Wi-Fi interface.

Checks rfkill status and offers to unblock.

Scans for Wi-Fi networks (using nmcli or iwlist/iw).

User selects SSID from a list.

Prompts for password based on detected/assumed security (Open, WEP, WPA/WPA2/WPA3-PSK).

Includes specific handling for WEP key types (ASCII/HEX).

Attempts connection using nmcli or wpa_supplicant.

If Wi-Fi association is successful, attempts to get an IP via DHCP (dhclient).

If DHCP fails, offers static IP configuration for the Wi-Fi interface.

If local configuration steps seem successful, returns to main loop for a final connectivity check.

Connectivity Verification (check_internet_connectivity):

Pings a reliable IP address (e.g., 8.8.8.8).

If IP ping is successful, pings a reliable hostname (e.g., google.com) to test DNS.

Reports status to the user. If successful, the script will exit from the main loop.

User Interaction:

All prompts are handled via dialog TUI elements (--menu, --yesno, --inputbox, --passwordbox).

Cancellations (Esc key or "Cancel" button) are handled, allowing the user to back out of operations.

Section 4: The Comprehensive Connectivity Bash Script
The full bash script is provided in the "Universal Network Connectivity Script v2 (Bash)" immersive code document. Please refer to that document for the complete code.

Section 5: Execution and Usage Guide
Preparing the Script:

Save the Script: Copy the bash script code into a file named universal_connect.sh on your RK3588 system.

nano universal_connect.sh

Paste the script, save, and exit (Ctrl+X, then Y, then Enter in nano).

Make it Executable:

chmod +x universal_connect.sh

Running the Script:
The script requires root privileges. Execute it with sudo:

sudo ./universal_connect.sh

Navigating Interactive Prompts:

Use Arrow Keys to navigate options in menus.

Use Tab Key to switch between buttons (e.g., <OK>, <Cancel>) and input fields.

Press Enter to select an option or activate a button.

Press Esc to cancel a dialog (usually defaults to the "Cancel" or "No" action).

Follow the on-screen prompts to:

Allow installation of missing packages (if any).

Select network interfaces.

Choose connection methods (DHCP/Static).

Select Wi-Fi networks and enter passwords/keys.

Provide static IP details if needed.

Expected Outcomes:

Success: A message confirming internet connectivity. The script will then exit.

Failure: If no connection can be established after trying the selected options, the script will allow you to try other options or exit. Error messages will provide some guidance.

User Cancellation: The script will exit if you cancel out of critical selection prompts or choose "Exit" from the main menu.

Section 6: Advanced Customization and Troubleshooting
Modifying Script Defaults:
Variables at the beginning of the script like PING_IP_TARGET, PING_HOSTNAME_TARGET, PING_COUNT, and PING_TIMEOUT can be edited for custom needs.

Troubleshooting Common Issues:

No Interfaces Found: Check physical connections (cables, antennas). Use ip link show and dmesg to check for hardware/driver issues.

Wi-Fi Scan Fails or Shows No Networks:

Run sudo rfkill unblock wifi manually if the script's attempt fails or if you suspect an rfkill issue.

Ensure you are in range of an AP. Check dmesg for Wi-Fi driver messages.

Password Rejected (Wi-Fi): Double-check password, case sensitivity, and keyboard layout.

DHCP Failed: Verify router/DHCP server functionality. Check script-generated logs like /tmp/dhclient_eth.log or /tmp/dhclient_wifi.log (these are temporary and might not persist if the script exits cleanly). System logs (journalctl -u isc-dhcp-client or journalctl -u NetworkManager) are more definitive.

Static IP Configured, No Internet: Re-verify all static IP details (IP, CIDR, Gateway, DNS). Ensure gateway is pingable.

dialog display issues: Ensure your terminal supports UTF-8 and has appropriate dimensions.

Log Review for Deeper Diagnosis:

Kernel: dmesg

NetworkManager: sudo journalctl -u NetworkManager

wpa_supplicant: sudo journalctl -u wpa_supplicant (or specific service instance)

DHCP Client: sudo journalctl | grep dhclient or check /var/log/syslog.

External Factors:
Remember, the script cannot overcome:

Physical layer problems (bad cables, faulty hardware).

ISP outages.

Captive portals requiring web browser login.

MAC address filtering on the router.

Networks requiring HTTP/SOCKS proxy configurations.

Section 7: Conclusion and Best Practices
This revised universal_connect.sh script provides a more robust and user-friendly tool for establishing network connectivity on your RK3588 VPC-3588 in diverse environments.

Recommendations:

Persistence: For networks you use regularly, configure them permanently using Debian's standard tools (nmcli profiles are usually persistent; for ifupdown, edit /etc/network/interfaces).

Package Management: Be cautious with system-wide upgrades on specialized embedded images. Update specific network-related packages if necessary and known to be safe: sudo apt-get update && sudo apt-get install --only-upgrade <package_name>.

Security: The script prompts for passwords at runtime. nmcli generally stores them securely via NetworkManager's mechanisms. Temporary wpa_supplicant configuration files created by the script are deleted after use.

This script serves as an advanced "first-response" tool for network setup. Once a connection is made, you can use standard Linux utilities for further management and troubleshooting.

# script

{% codeblock bash %}
#!/bin/bash
#
# Universal Network Connectivity Script for RK3588 VPC-3588 (Debian Bullseye)
#
# This script attempts to establish an internet connection via Ethernet or Wi-Fi,
# interactively prompting the user for necessary information.
# It must be run with root privileges.
#
# Version 2: Incorporates fixes for dialog exit codes, WEP key handling,
#            safer package installation, rfkill checks, and improved flow.

# --- Script Setup ---
# Exit immediately if a command exits with a non-zero status.
set -e
# Treat unset variables as an error when substituting.
# set -u # Can be too strict for optional dialog inputs, handle manually.
# The return value of a pipeline is the status of the last command to exit
# with a non-zero status, or zero if no command exited with a non-zero status.
set -o pipefail

# --- Global Variables ---
ETH_IFACES=()
WIFI_IFACES=()
SELECTED_ETH_IFACE=""
SELECTED_WIFI_IFACE=""
NM_IS_ACTIVE=false
DIALOG_SUCCESS_CODE=0
DIALOG_CANCEL_CODE=1
DIALOG_HELP_CODE=2
DIALOG_EXTRA_CODE=3
DIALOG_ESC_CODE=255 # Standard for Esc key
DIALOG_DEFAULT_HEIGHT=15
DIALOG_DEFAULT_WIDTH=70
DIALOG_INPUT_WIDTH=50

# Ping targets for connectivity check
PING_IP_TARGET="8.8.8.8"
PING_HOSTNAME_TARGET="google.com"
PING_COUNT=3
PING_TIMEOUT=2 # seconds

# Temporary files management
TMP_FILES_TO_CLEAN=()

# --- Cleanup Function ---
cleanup() {
    local exit_code=$?
    for temp_file in "${TMP_FILES_TO_CLEAN[@]}"; do
        rm -f "$temp_file"
    done
    # Restore cursor if dialog messed it up
    stty sane
    tput cnorm
    echo "Script exited (Code: $exit_code). Cleanup performed."
    # If error, allow user to see last message from dialog if any
    if [ $exit_code -ne 0 ] && [ $exit_code -ne 130 ]; then # 130 is Ctrl+C
      read -rp "Press Enter to close terminal..."
    fi
}
trap cleanup EXIT # Handles normal exit and exit due to set -e
trap 'echo "Script interrupted by user (SIGINT/SIGTERM)."; exit 130' SIGINT SIGTERM


# --- Logging Functions ---
_show_dialog_message() {
    local type="$1"
    local title="$2"
    local message="$3"
    local height=${4:-8}
    local width=${5:-60}
    dialog --title "$title" --"$type" "$message" "$height" "$width" 2>/dev/tty
    return $?
}

log_info_persistent() { # Requires user to press OK
    echo "[INFO] $1"
    _show_dialog_message "msgbox" "Information" "$1"
}

log_info_transient() { # Auto-closes
    echo "[INFO] $1"
    # Infobox clears screen, so echo first, then show infobox briefly
    dialog --title "Information" --infobox "$1" 6 60 2>/dev/null
    sleep 1 # Give time for user to see infobox
}

log_msg() { # Requires user to press OK
    echo " $1"
    _show_dialog_message "msgbox" "Message" "$1"
}

log_error() { # Requires user to press OK
    echo "[ERROR] $1" >&2
    _show_dialog_message "msgbox" "Error" "$1"
}

log_warning() { # Requires user to press OK
    echo "[WARNING] $1"
    _show_dialog_message "msgbox" "Warning" "$1"
}

# --- Prerequisite Checks ---
check_command() {
    command -v "$1" >/dev/null 2>&1
}

install_packages() {
    local missing_packages_to_install=()
    local package_info_array=("$@") # Store args in an array

    for pkg_info in "${package_info_array[@]}"; do
        IFS=',' read -r cmd pkg_name <<< "$pkg_info"
        if! check_command "$cmd"; then
            missing_packages_to_install+=("$pkg_name")
        fi
    done

    if [ ${#missing_packages_to_install[@]} -gt 0 ]; then
        dialog --title "Missing Packages" --yesno "The following essential packages are missing: ${missing_packages_to_install[*]}.\\n\\nDo you want to try and install them now?\\n(Requires an existing temporary internet connection or cached packages)" 12 ${DIALOG_DEFAULT_WIDTH} 2>/dev/tty
        local choice=$?
        if [ $choice -eq $DIALOG_SUCCESS_CODE ]; then
            log_info_transient "Attempting to install missing packages: ${missing_packages_to_install[*]}..."
            # Adhere to [1] warning: NO apt-get upgrade
            if apt-get update -qq; then
                if apt-get install -y "${missing_packages_to_install[@]}"; then
                    log_info_persistent "Successfully installed missing packages."
                else
                    log_error "Failed to install some packages after update. Please install them manually and re-run the script.\\nPackages: ${missing_packages_to_install[*]}"
                    exit 1
                fi
            else
                log_error "'apt-get update' failed. Cannot install packages. Please check your network connection and apt sources, then re-run the script."
                exit 1
            fi
        else
            log_error "Cannot proceed without essential packages: ${missing_packages_to_install[*]}. Exiting."
            exit 1
        fi
    fi
}

# --- Network Interface and Manager Detection ---
detect_ethernet_interfaces() {
    ETH_IFACES=()
    local detected
    # Using ip -o link filters better than ifconfig -a which might not be installed
    # Filters for common Ethernet prefixes and excludes virtual/bridge interfaces
    # Also exclude interfaces that are part of a bridge (master) or bond
    detected=$(ip -o link show type ether | awk -F': ' '!/master|link\/ether 00:00:00:00:00:00|NO-CARRIER/{print $2}' | awk '{print $1}' | grep -Ev '^(br|bond|dummy|veth|virbr|docker|lo)')
    if [ -n "$detected" ]; then
        # shellcheck disable=SC2207 # Word splitting is intended here
        ETH_IFACES=($(echo "$detected"))
    fi
    log_info_transient "Detected Ethernet interfaces: ${ETH_IFACES[*]:-(None)}"
}

detect_wifi_interfaces() {
    WIFI_IFACES=()
    local detected
    # Try 'iw dev' first (more reliable for Wi-Fi)
    if check_command iw; then
        detected=$(iw dev 2>/dev/null | awk '$1=="Interface"{print $2}')
    fi
    # Fallback to 'ip link' if 'iw dev' fails or not present
    if [ -z "$detected" ] && check_command ip; then
        detected=$(ip -o link show type wlan 2>/dev/null | awk -F': ' '{print $2}' | awk '{print $1}')
    fi

    if [ -n "$detected" ]; then
        # shellcheck disable=SC2207
        WIFI_IFACES=($(echo "$detected"))
    fi
    log_info_transient "Detected Wi-Fi interfaces: ${WIFI_IFACES[*]:-(None)}"
}

check_network_manager_active() {
    if check_command systemctl && systemctl is-active --quiet NetworkManager; then
        NM_IS_ACTIVE=true
        log_info_transient "NetworkManager service is active."
    else
        NM_IS_ACTIVE=false
        log_info_transient "NetworkManager service is not active or not found."
    fi
}

# --- User Interaction and Selection ---
prompt_select_interface() {
    local type="$1"
    shift
    local interfaces_array=("$@")
    local dialog_options=()
    local choice
    local i=0

    if [ ${#interfaces_array[@]} -eq 0 ]; then
        log_warning "No $type interfaces found to select."
        return 1 # Indicates no interface could be selected
    elif [ ${#interfaces_array[@]} -eq 1 ]; then
        log_info_persistent "Auto-selecting $type interface: ${interfaces_array[0]}"
        echo "${interfaces_array[0]}"
        return 0 # Indicates an interface was selected
    fi

    for iface_item in "${interfaces_array[@]}"; do
        dialog_options+=("$iface_item" "Use $iface_item")
        i=$((i + 1))
    done

    choice=$(dialog --title "Select $type Interface" \
        --menu "Choose the $type interface to configure:" ${DIALOG_DEFAULT_HEIGHT} ${DIALOG_DEFAULT_WIDTH} "$i" \
        "${dialog_options[@]}" \
        2>&1 >/dev/tty)

    local exit_status=$?
    if [ $exit_status -ne $DIALOG_SUCCESS_CODE ]; then
        log_info_persistent "$type interface selection cancelled by user."
        return 1 # Indicates no interface was selected (cancelled)
    fi
    echo "$choice"
    return 0 # Indicates an interface was selected
}

prompt_static_config() {
    local interface_type="$1" # "Ethernet" or "Wi-Fi"
    local static_ip static_gateway static_dns

    static_ip=$(dialog --title "Static IP Configuration ($interface_type)" \
        --inputbox "Enter Static IP Address with CIDR (e.g., 192.168.1.100/24):" \
        10 ${DIALOG_INPUT_WIDTH} 2>&1 >/dev/tty)
    [ $? -ne $DIALOG_SUCCESS_CODE ] && return 1

    static_gateway=$(dialog --title "Static IP Configuration ($interface_type)" \
        --inputbox "Enter Gateway IP Address (e.g., 192.168.1.1):" \
        10 ${DIALOG_INPUT_WIDTH} 2>&1 >/dev/tty)
    [ $? -ne $DIALOG_SUCCESS_CODE ] && return 1

    static_dns=$(dialog --title "Static IP Configuration ($interface_type)" \
        --inputbox "Enter DNS Server(s) (comma-separated, e.g., 8.8.8.8,1.1.1.1, optional):" \
        10 ${DIALOG_INPUT_WIDTH} 2>&1 >/dev/tty)
    [ $? -ne $DIALOG_SUCCESS_CODE ] && return 1 # Even if DNS is optional, cancellation here means stop.

    if [[ -z "$static_ip" || -z "$static_gateway" ]]; then
        log_error "Static IP and Gateway cannot be empty."
        return 1
    fi
    # Basic IP/CIDR validation (does not check for valid IP format, but ensures CIDR is plausible)
    if ! echo "$static_ip" | grep -qE "/[0-9]{1,2}$"; then
        log_error "Static IP must be in CIDR notation (e.g., 192.168.1.100/24)."
        return 1
    fi

    echo "$static_ip:$static_gateway:$static_dns"
    return 0
}


# --- Connectivity Check ---
check_internet_connectivity() {
    log_info_transient "Checking internet connectivity..."
    # Test 1: Ping a reliable IP address
    if ping -c ${PING_COUNT} -W ${PING_TIMEOUT} "${PING_IP_TARGET}" >/dev/null 2>&1; then
        log_info_transient "Successfully pinged IP address (${PING_IP_TARGET}). Basic connectivity OK."
        # Test 2: Ping a reliable hostname (tests DNS resolution)
        if ping -c ${PING_COUNT} -W ${PING_TIMEOUT} "${PING_HOSTNAME_TARGET}" >/dev/null 2>&1; then
            log_msg "Internet connection established and DNS resolution working (pinged ${PING_HOSTNAME_TARGET})."
            return 0 # Success
        else
            log_warning "Successfully pinged IP, but DNS resolution failed (cannot ping ${PING_HOSTNAME_TARGET}). Check DNS settings."
            return 2 # DNS issue
        fi
    else
        log_warning "Failed to ping IP address (${PING_IP_TARGET}). No basic network connectivity."
        return 1 # No basic connectivity
    fi
}

# --- Ethernet Configuration ---
attempt_ethernet_dhcp() {
    local iface="$1"
    log_info_transient "Attempting DHCP on Ethernet interface: $iface"

    if $NM_IS_ACTIVE; then
        local profile_name
        profile_name=$(nmcli -g NAME,DEVICE connection show --active | grep ":$iface$" | cut -d':' -f1 | head -n1)
        if [ -z "$profile_name" ]; then
             profile_name=$(nmcli -g NAME,DEVICE connection show | grep ":$iface$" | cut -d':' -f1 | head -n1)
        fi

        if [ -n "$profile_name" ]; then
            log_info_transient "Found existing NetworkManager profile '$profile_name' for $iface. Ensuring DHCP and activating..."
            if nmcli connection modify "$profile_name" ipv4.method auto ipv6.method auto && \
               nmcli connection up "$profile_name" ifname "$iface"; then
                log_info_transient "NetworkManager activated DHCP profile '$profile_name' for $iface."
                sleep 5; return 0
            else
                log_warning "Failed to activate DHCP profile '$profile_name' for $iface via NetworkManager. Trying to add a new one."
            fi
        fi
        log_info_transient "Attempting to add and activate a new DHCP Ethernet connection for $iface via NetworkManager..."
        if nmcli connection add type ethernet con-name "Eth-DHCP-$iface" ifname "$iface" ipv4.method auto ipv6.method auto && \
           nmcli connection up "Eth-DHCP-$iface"; then
            log_info_transient "NetworkManager added and activated DHCP connection for $iface."
            sleep 5; return 0
        else
            log_warning "Failed to configure Ethernet DHCP for $iface via NetworkManager. Will try dhclient."
        fi
    fi

    log_info_transient "Bringing interface $iface up..."
    ip link set "$iface" up
    dhclient -r "$iface" >/dev/null 2>&1 || true
    log_info_transient "Attempting DHCP with dhclient on $iface..."
    if dhclient -v "$iface" >/tmp/dhclient_eth.log 2>&1; then
        log_info_transient "dhclient successfully obtained lease on $iface."
        sleep 2; return 0
    else
        log_error "dhclient failed to obtain lease on $iface. Check /tmp/dhclient_eth.log"
        return 1
    fi
}

configure_ethernet_static() {
    local iface="$1"
    local config_str
    
    config_str=$(prompt_static_config "Ethernet")
    local prompt_exit_status=$?
    [ $prompt_exit_status -ne $DIALOG_SUCCESS_CODE ] && return 1

    local static_ip_cidr gateway dns_servers
    IFS=':' read -r static_ip_cidr gateway dns_servers <<< "$config_str"

    log_info_transient "Configuring static IP for Ethernet interface $iface: IP=$static_ip_cidr, GW=$gateway, DNS=$dns_servers"

    if $NM_IS_ACTIVE; then
        local profile_name="Static-Eth-$iface"
        nmcli connection delete "$profile_name" >/dev/null 2>&1 || true
        
        log_info_transient "Attempting to add and activate static Ethernet connection via NetworkManager..."
        local nm_cmd_parts=("nmcli" "connection" "add" "type" "ethernet" "con-name" "$profile_name" "ifname" "$iface" "ipv4.method" "manual" "ipv4.addresses" "$static_ip_cidr" "ipv4.gateway" "$gateway")
        [ -n "$dns_servers" ] && nm_cmd_parts+=("ipv4.dns" "$dns_servers")
        nm_cmd_parts+=("ipv6.method" "disabled")

        if "${nm_cmd_parts[@]}" && nmcli connection up "$profile_name"; then
            log_info_transient "NetworkManager configured and activated static IP on $iface."
            sleep 3; return 0
        else
            log_error "Failed to configure static IP on $iface via NetworkManager."
            nmcli connection delete "$profile_name" >/dev/null 2>&1 || true
            return 1
        fi
    fi

    log_info_transient "Configuring static IP on $iface using iproute2..."
    ip addr flush dev "$iface" || true
    ip link set "$iface" down
    ip link set "$iface" up
    if ip addr add "$static_ip_cidr" dev "$iface" && \
       ip route add default via "$gateway" dev "$iface"; then
        log_info_transient "iproute2 configured IP address and gateway on $iface."
        if [ -n "$dns_servers" ]; then
            local resolv_conf_content=""
            IFS=',' read -ra dns_array <<< "$dns_servers"
            for dns in "${dns_array[@]}"; do resolv_conf_content+="nameserver $dns\n"; done
            echo -e "$resolv_conf_content" > /etc/resolv.conf
            log_info_transient "Configured DNS servers in /etc/resolv.conf: $dns_servers"
        fi
        sleep 3; return 0
    else
        log_error "Failed to configure static IP on $iface using iproute2."
        return 1
    fi
}

handle_ethernet_connection() {
    if [ ${#ETH_IFACES[@]} -eq 0 ]; then
        log_warning "No Ethernet interfaces detected. Skipping Ethernet setup."
        return 1 # Failure to find usable interface
    fi

    SELECTED_ETH_IFACE=$(prompt_select_interface "Ethernet" "${ETH_IFACES[@]}")
    local select_exit_status=$?
    [ $select_exit_status -ne $DIALOG_SUCCESS_CODE ] && return 1 # User cancelled selection

    dialog --title "Ethernet Configuration" --yesno "Attempt to configure Ethernet interface '$SELECTED_ETH_IFACE' using DHCP (automatic IP)?" ${DIALOG_DEFAULT_HEIGHT} ${DIALOG_DEFAULT_WIDTH} 2>/dev/tty
    local choice=$?

    if [ $choice -eq $DIALOG_SUCCESS_CODE ]; then # Yes (DHCP)
        if attempt_ethernet_dhcp "$SELECTED_ETH_IFACE"; then return 0; fi # Return 0 if DHCP step succeeded locally
        log_warning "DHCP on $SELECTED_ETH_IFACE failed locally."
    elif [ $choice -eq $DIALOG_CANCEL_CODE ]; then # No
        log_info_persistent "Skipping DHCP for $SELECTED_ETH_IFACE."
    else # Esc or other non-success
        log_info_persistent "Ethernet DHCP choice cancelled by user."
        return 1
    fi

    dialog --title "Ethernet Configuration" --yesno "Do you want to configure a static IP for Ethernet interface '$SELECTED_ETH_IFACE'?" ${DIALOG_DEFAULT_HEIGHT} ${DIALOG_DEFAULT_WIDTH} 2>/dev/tty
    choice=$?
    if [ $choice -eq $DIALOG_SUCCESS_CODE ]; then # Yes (Static IP)
        if configure_ethernet_static "$SELECTED_ETH_IFACE"; then return 0; fi # Return 0 if static config step succeeded locally
        log_warning "Static IP configuration on $SELECTED_ETH_IFACE failed locally."
    else
        log_info_persistent "Skipping static IP configuration for $SELECTED_ETH_IFACE."
    fi
    return 1 # All attempts for Ethernet failed or were skipped
}

# --- Wi-Fi Configuration ---
scan_wifi_networks() {
    local iface="$1"
    local networks_list=()
    local line ssid signal security
    local tmp_scan_file="/tmp/wifi_scan_$$"
    TMP_FILES_TO_CLEAN+=("$tmp_scan_file")


    log_info_transient "Scanning for Wi-Fi networks on $iface (this may take a few seconds)..."
    ip link set "$iface" up 2>/dev/null || log_warning "Could not bring $iface up for scanning."

    if $NM_IS_ACTIVE && check_command nmcli; then
        nmcli device wifi rescan ifname "$iface" >/dev/null 2>&1 || true 
        sleep 5 # Give time for rescan
        
        # nmcli default output is column-based. Parsing needs to be careful.
        # Using -g for specific fields is more robust if available and works as expected.
        # Let's try a slightly more robust parsing for default output:
        nmcli -f SSID,SIGNAL,SECURITY dev wifi list ifname "$iface" --rescan no | \
            tail -n +2 | grep -v "^\*" | grep -v "^\-\-" | \
            awk 'BEGIN {OFS=";"} { $1=$1; ssid=""; for(i=1;i<=NF-2;i++) ssid=(ssid==""?$i:ssid FS $i); gsub(/^[ \t]+|[ \t]+$/, "", ssid); gsub(/^[ \t]+|[ \t]+$/, "", $(NF-1)); gsub(/^[ \t]+|[ \t]+$/, "", $NF); if (ssid!="") print ssid,$(NF-1),$NF}' > "$tmp_scan_file"
        
        while IFS=';' read -r ssid signal security_field; do
            if [ -n "$ssid" ] && [ "$ssid" != "--" ]; then
                local display_ssid="${ssid:0:25}"
                [ "${#ssid}" -gt 25 ] && display_ssid="${display_ssid}.."
                networks_list+=("$ssid" "Sig: $signal | Sec: ${security_field:-Open} | $display_ssid")
            fi
        done < "$tmp_scan_file"

    else # Fallback to iwlist
        pgrep -af "wpa_supplicant.*${iface}" | awk '{print $1}' | xargs kill >/dev/null 2>&1 || true # Try graceful kill first
        sleep 0.5
        pgrep -af "wpa_supplicant.*${iface}" | awk '{print $1}' | xargs kill -9 >/dev/null 2>&1 || true # Force kill if still running
        sleep 1

        local scan_output
        scan_output=$(iwlist "$iface" scan 2>/dev/null)
        local current_ssid="" current_signal="" current_security="Open"

        while IFS= read -r line; do
            if [[ "$line" == *"ESSID:"* ]]; then
                [ -n "$current_ssid" ] && networks_list+=("$current_ssid" "Sig: ${current_signal:-N/A} | Sec: $current_security | ${current_ssid:0:25}${current_ssid:25:..}")
                current_ssid=$(echo "$line" | sed -e 's/.*ESSID:"\(.*\)"/\1/')
                current_signal="N/A"; current_security="Open" # Reset for new AP
            elif [[ "$line" == *"Quality="* ]]; then
                current_signal=$(echo "$line" | sed -n -e 's/.*Signal level=\(-\?[0-9]* dBm\).*/\1/p' -e 's/.*Quality=\([0-9]*\/[0-9]*\).*/\1/p')
            elif [[ "$line" == *"Encryption key:on"* ]]; then
                current_security="Protected" 
            elif [[ "$line" == *"IE: IEEE 802.11i/WPA2 Version 1"* ]]; then
                current_security="WPA2/PSK" # Assume PSK
            elif [[ "$line" == *"IE: WPA Version 1"* ]]; then
                current_security="WPA/PSK"  # Assume PSK
            # Add more specific IE parsing for WPA3 (SAE) if needed
            fi
        done <<< "$scan_output"
        [ -n "$current_ssid" ] && networks_list+=("$current_ssid" "Sig: ${current_signal:-N/A} | Sec: $current_security | ${current_ssid:0:25}${current_ssid:25:..}")
    fi
    
    rm -f "$tmp_scan_file"
    TMP_FILES_TO_CLEAN=( "${TMP_FILES_TO_CLEAN[@]/$tmp_scan_file}" )


    if [ ${#networks_list[@]} -eq 0 ]; then
        log_warning "No Wi-Fi networks found on $iface after scan."
        return 1
    fi

    echo "${networks_list[@]}"
    return 0
}

connect_wifi() {
    local iface="$1"
    local networks_flat_array_str
    
    networks_flat_array_str=$(scan_wifi_networks "$iface")
    local scan_status=$?
    # shellcheck disable=SC2207
    local networks_flat_array=($networks_flat_array_str)

    if [ $scan_status -ne 0 ] || [ ${#networks_flat_array[@]} -eq 0 ]; then
        return 1
    fi

    local selected_ssid_tag
    selected_ssid_tag=$(dialog --title "Select Wi-Fi Network" \
        --menu "Choose the Wi-Fi network (SSID) to connect to on $iface:" \
        $((DIALOG_DEFAULT_HEIGHT + 5)) ${DIALOG_DEFAULT_WIDTH} $((${#networks_flat_array[@]} / 2)) \
        "${networks_flat_array[@]}" \
        2>&1 >/dev/tty)
    
    local exit_status=$?
    if [ $exit_status -ne $DIALOG_SUCCESS_CODE ]; then
        log_info_persistent "Wi-Fi network selection cancelled."
        return 1
    fi
    local selected_ssid="$selected_ssid_tag"

    local security_type="Unknown"
    for ((i=0; i<${#networks_flat_array[@]}; i+=2)); do
        if [ "${networks_flat_array[i]}" == "$selected_ssid" ]; then
            if [[ "${networks_flat_array[i+1]}" == *"Sec: Open"* ]]; then security_type="Open"
            elif [[ "${networks_flat_array[i+1]}" == *"Sec: WEP"* ]]; then security_type="WEP"
            elif [[ "${networks_flat_array[i+1]}" == *"Sec: WPA"* || "${networks_flat_array[i+1]}" == *"Sec: WPA2"* || "${networks_flat_array[i+1]}" == *"Sec: WPA3"* || "${networks_flat_array[i+1]}" == *"Sec: PSK"* ]]; then security_type="PSK"
            fi
            break
        fi
    done

    local wifi_password=""
    if [ "$security_type" == "PSK" ] || [ "$security_type" == "WEP" ]; then
        wifi_password=$(dialog --title "Wi-Fi Password" \
            --passwordbox "Enter password for SSID '$selected_ssid' ($security_type):" \
            10 ${DIALOG_INPUT_WIDTH} 2>&1 >/dev/tty)
        exit_status=$?
        if [ $exit_status -ne $DIALOG_SUCCESS_CODE ] || [ -z "$wifi_password" ]; then
            log_warning "Password entry cancelled or empty. Cannot connect."
            return 1
        fi
    elif [ "$security_type" == "Unknown" ]; then
         dialog --title "Unknown Security" --yesno "Security type for '$selected_ssid' is unknown or complex (e.g. Enterprise/EAP). Attempt to connect as an open network or provide a password?" 12 ${DIALOG_DEFAULT_WIDTH} 2>/dev/tty
         local choice=$?
         if [ $choice -eq $DIALOG_SUCCESS_CODE ]; then
            wifi_password=$(dialog --title "Wi-Fi Password" \
                --passwordbox "Enter password/key for SSID '$selected_ssid' (if any):" \
                10 ${DIALOG_INPUT_WIDTH} 2>&1 >/dev/tty)
            [ $? -ne $DIALOG_SUCCESS_CODE ] && return 1
         else
            security_type="Open"
         fi
    fi

    log_info_transient "Attempting to connect to Wi-Fi: $selected_ssid on $iface"
    if $NM_IS_ACTIVE; then
        nmcli device disconnect "$iface" >/dev/null 2>&1 || true; sleep 1
        local old_profile_uuid
        old_profile_uuid=$(nmcli -g UUID,TYPE,NAME connection show | grep "wireless" | grep ":$selected_ssid$" | cut -d':' -f1 | head -n1)
        [ -n "$old_profile_uuid" ] && { log_info_transient "Deleting existing NetworkManager profile for $selected_ssid."; nmcli connection delete uuid "$old_profile_uuid" >/dev/null 2>&1 || true; }

        local connect_cmd_nmcli=("nmcli" "device" "wifi" "connect" "$selected_ssid" "ifname" "$iface")
        if [ "$security_type" != "Open" ] || { [ "$security_type" == "Open" ] && [ -n "$wifi_password" ]; }; then # If not open, or open but password provided
            connect_cmd_nmcli+=("password" "$wifi_password")
        fi
        
        if "${connect_cmd_nmcli[@]}"; then
            log_info_transient "Successfully initiated Wi-Fi connection to $selected_ssid via NetworkManager."
        else
            log_error "Failed to connect to Wi-Fi $selected_ssid via NetworkManager. Check password/security."
            return 1
        fi
    else # Use wpa_supplicant
        pgrep -af "wpa_supplicant.*${iface}" | awk '{print $1}' | xargs kill >/dev/null 2>&1 || true; sleep 0.5
        pgrep -af "wpa_supplicant.*${iface}" | awk '{print $1}' | xargs kill -9 >/dev/null 2>&1 || true; sleep 1
        
        local wpa_conf_temp="/tmp/wpa_temp_${iface}_$$$$.conf"
        TMP_FILES_TO_CLEAN+=("$wpa_conf_temp")

        echo "ctrl_interface=DIR=/run/wpa_supplicant GROUP=netdev" > "$wpa_conf_temp"
        echo "update_config=1" >> "$wpa_conf_temp"
        echo -e "\nnetwork={" >> "$wpa_conf_temp"
        echo "    ssid=\"$selected_ssid\"" >> "$wpa_conf_temp"
        if [ "$security_type" == "Open" ] && [ -z "$wifi_password" ]; then
            echo "    key_mgmt=NONE" >> "$wpa_conf_temp"
        elif [ "$security_type" == "WEP" ]; then
            dialog --title "WEP Key Type" --yesno "Is the WEP key '$wifi_password' in HEXADECIMAL format (e.g., 1A2B3C4D5E)?" 8 ${DIALOG_DEFAULT_WIDTH} 2>/dev/tty
            local is_hex=$?
            if [ $is_hex -eq $DIALOG_SUCCESS_CODE ]; then # Yes, it's HEX
                if ! [[ "$wifi_password" =~ ^[0-9A-Fa-f]{10}$ || "$wifi_password" =~ ^[0-9A-Fa-f]{26}$ ]]; then
                    log_error "Invalid HEX WEP key length. Must be 10 or 26 hex digits."; rm -f "$wpa_conf_temp"; return 1
                fi
                echo "    wep_key0=$wifi_password" >> "$wpa_conf_temp"
            else # No, it's ASCII
                if ! [[ "${#wifi_password}" -eq 5 || "${#wifi_password}" -eq 13 ]]; then
                    log_error "Invalid ASCII WEP key length. Must be 5 or 13 characters."; rm -f "$wpa_conf_temp"; return 1
                fi
                echo "    wep_key0=\"$wifi_password\"" >> "$wpa_conf_temp"
            fi
            echo "    key_mgmt=NONE" >> "$wpa_conf_temp"
        else # PSK (WPA/WPA2/WPA3)
            echo "    psk=\"$wifi_password\"" >> "$wpa_conf_temp"
            echo "    key_mgmt=WPA-PSK WPA-PSK-SHA256 SAE" >> "$wpa_conf_temp" # Broad compatibility
            echo "    proto=RSN WPA" >> "$wpa_conf_temp"
            echo "    pairwise=CCMP TKIP" >> "$wpa_conf_temp"
            echo "    group=CCMP TKIP" >> "$wpa_conf_temp"
        fi
        echo "}" >> "$wpa_conf_temp"
        chmod 600 "$wpa_conf_temp"

        if ! wpa_supplicant -B -i "$iface" -c "$wpa_conf_temp" -Dnl80211,wext; then
            log_error "Failed to start wpa_supplicant for $iface."; rm -f "$wpa_conf_temp"; return 1
        fi
        log_info_transient "wpa_supplicant started for $iface. Waiting for association..."
        local connect_tries=20 # Increased timeout
        while [ $connect_tries -gt 0 ]; do
            if wpa_cli -i "$iface" status 2>/dev/null | grep -q "wpa_state=COMPLETED"; then
                log_info_transient "Successfully associated with Wi-Fi $selected_ssid via wpa_supplicant."
                rm -f "$wpa_conf_temp"; TMP_FILES_TO_CLEAN=( "${TMP_FILES_TO_CLEAN[@]/$wpa_conf_temp}" )
                break
            fi
            sleep 1; connect_tries=$((connect_tries - 1))
        done
        if [ $connect_tries -eq 0 ]; then
            log_error "Failed to associate with Wi-Fi $selected_ssid via wpa_supplicant."
            pgrep -af "wpa_supplicant -B -i $iface -c $wpa_conf_temp" | awk '{print $1}' | xargs kill -9 >/dev/null 2>&1 || true
            rm -f "$wpa_conf_temp"; TMP_FILES_TO_CLEAN=( "${TMP_FILES_TO_CLEAN[@]/$wpa_conf_temp}" )
            return 1
        fi
    fi

    log_info_transient "Wi-Fi associated. Attempting DHCP on $iface..."
    dhclient -r "$iface" >/dev/null 2>&1 || true
    if dhclient -v "$iface" >/tmp/dhclient_wifi.log 2>&1; then
        log_info_transient "dhclient successfully obtained lease on $iface."
        sleep 2; return 0
    else
        log_warning "dhclient failed for '$selected_ssid' on $iface. Check /tmp/dhclient_wifi.log"
        dialog --title "Wi-Fi IP Configuration" --yesno "DHCP failed for '$selected_ssid' on $iface.\\nDo you want to configure a static IP for this Wi-Fi connection?" ${DIALOG_DEFAULT_HEIGHT} ${DIALOG_DEFAULT_WIDTH} 2>/dev/tty
        local choice=$?
        if [ $choice -eq $DIALOG_SUCCESS_CODE ]; then
            local static_config_str
            static_config_str=$(prompt_static_config "Wi-Fi ($selected_ssid)")
            local prompt_exit_status=$?
            [ $prompt_exit_status -ne $DIALOG_SUCCESS_CODE ] && return 1

            local static_ip_cidr gw dns
            IFS=':' read -r static_ip_cidr gw dns <<< "$static_config_str"
            log_info_transient "Configuring static IP for Wi-Fi $iface: IP=$static_ip_cidr, GW=$gw, DNS=$dns"

            if $NM_IS_ACTIVE; then
                local active_wifi_conn
                active_wifi_conn=$(nmcli -g UUID,DEVICE connection show --active | grep ":$iface$" | cut -d':' -f1 | head -n1)
                if [ -n "$active_wifi_conn" ]; then
                    local nm_modify_cmd=("nmcli" "connection" "modify" "$active_wifi_conn" "ipv4.method" "manual" "ipv4.addresses" "$static_ip_cidr" "ipv4.gateway" "$gw")
                    [ -n "$dns" ] && nm_modify_cmd+=("ipv4.dns" "$dns")
                    nm_modify_cmd+=("ipv6.method" "disabled")
                    if "${nm_modify_cmd[@]}" && nmcli connection up "$active_wifi_conn"; then
                        log_info_transient "NetworkManager configured static IP for Wi-Fi $iface."; return 0
                    else
                        log_error "Failed to configure static IP for Wi-Fi via NetworkManager."; return 1
                    fi
                else
                    log_error "Could not find active NetworkManager Wi-Fi connection to modify for static IP."; return 1
                fi
            else 
                ip addr flush dev "$iface" || true; ip link set "$iface" up
                if ip addr add "$static_ip_cidr" dev "$iface" && ip route add default via "$gw" dev "$iface"; then
                    log_info_transient "iproute2 configured static IP for Wi-Fi $iface."
                    if [ -n "$dns" ]; then
                        local resolv_conf_content_wifi=""
                        IFS=',' read -ra dns_array_wifi <<< "$dns"
                        for dns_val in "${dns_array_wifi[@]}"; do resolv_conf_content_wifi+="nameserver $dns_val\n"; done
                        echo -e "$resolv_conf_content_wifi" > /etc/resolv.conf
                        log_info_transient "Configured DNS servers in /etc/resolv.conf: $dns"
                    fi
                    return 0
                else
                    log_error "Failed to configure static IP for Wi-Fi $iface using iproute2."; return 1
                fi
            fi
        else
            log_info_persistent "Skipping static IP for Wi-Fi."; return 1
        fi
    fi
    return 1 # Fallthrough, should indicate failure
}

handle_wifi_connection() {
    if [ ${#WIFI_IFACES[@]} -eq 0 ]; then
        log_warning "No Wi-Fi interfaces detected. Skipping Wi-Fi setup."
        return 1
    fi

    SELECTED_WIFI_IFACE=$(prompt_select_interface "Wi-Fi" "${WIFI_IFACES[@]}")
    local select_exit_status=$?
    [ $select_exit_status -ne $DIALOG_SUCCESS_CODE ] && return 1

    # rfkill check
    if check_command rfkill; then
        if rfkill list wifi | grep -A1 "$SELECTED_WIFI_IFACE" | grep -q "Soft blocked: yes"; then
            dialog --title "Wi-Fi Blocked" --yesno "Wi-Fi interface $SELECTED_WIFI_IFACE appears to be soft-blocked by rfkill.\\nDo you want to attempt to unblock it?" 10 ${DIALOG_DEFAULT_WIDTH} 2>/dev/tty
            if [ $? -eq $DIALOG_SUCCESS_CODE ]; then
                if rfkill unblock wifi; then log_info_persistent "Wi-Fi unblocked successfully."; sleep 1
                else log_warning "Failed to unblock Wi-Fi via rfkill. Proceeding with scan anyway."; fi
            fi
        fi
    fi

    if connect_wifi "$SELECTED_WIFI_IFACE"; then return 0; fi # Return 0 if Wi-Fi connection steps succeeded locally
    
    log_warning "Wi-Fi connection on $SELECTED_WIFI_IFACE failed locally."
    return 1
}


# --- Main Script Logic ---
main() {
    if [ "$(id -u)" -ne 0 ]; then
      echo "This script must be run as root. Please use 'sudo $0'" >&2
      exit 1
    fi

    # Ensure dialog is available before anything else
    install_packages "dialog,dialog"
    # Then other packages
    install_packages "nmcli,network-manager" \
                     "wpa_cli,wpasupplicant" \
                     "wpa_supplicant,wpasupplicant" \
                     "dhclient,isc-dhcp-client" \
                     "ip,iproute2" \
                     "iw,iw" \
                     "ping,iputils-ping" \
                     "rfkill,rfkill"

    detect_ethernet_interfaces
    detect_wifi_interfaces
    check_network_manager_active

    if check_internet_connectivity; then
        exit 0 # Already connected, success message shown by check_internet_connectivity
    fi
    log_info_persistent "No active internet connection detected. Starting configuration process..."

    while true; do
        local options=()
        [ ${#ETH_IFACES[@]} -gt 0 ] && options+=("ETH" "Configure Ethernet Connection")
        [ ${#WIFI_IFACES[@]} -gt 0 ] && options+=("WIFI" "Configure Wi-Fi Connection")
        options+=("CHECK" "Re-check Internet Connectivity")
        options+=("EXIT" "Exit Script")

        if [ $((${#ETH_IFACES[@]} + ${#WIFI_IFACES[@]})) -eq 0 ]; then
             log_error "No usable network interfaces (Ethernet or Wi-Fi) were detected. Cannot proceed."
             exit 1
        fi
        
        local main_choice
        main_choice=$(dialog --title "Main Menu - Universal Network Connector" \
            --cancel-label "Exit" \
            --menu "Select an action:" ${DIALOG_DEFAULT_HEIGHT} ${DIALOG_DEFAULT_WIDTH} $((${#options[@]}/2)) \
            "${options[@]}" \
            2>&1 >/dev/tty)
        
        local exit_status=$?
        if [ $exit_status -ne $DIALOG_SUCCESS_CODE ] || [ "$main_choice" == "EXIT" ]; then
            log_info_persistent "Exiting script as per user request or cancellation."
            break 
        fi

        case "$main_choice" in
            ETH)
                if handle_ethernet_connection; then # Returns 0 if local config steps were successful
                    if check_internet_connectivity; then exit 0; fi # Final check and exit if good
                else
                    log_warning "Ethernet configuration attempt did not succeed locally or was cancelled."
                fi
                ;;
            WIFI)
                if handle_wifi_connection; then # Returns 0 if local config steps were successful
                    if check_internet_connectivity; then exit 0; fi # Final check and exit if good
                else
                    log_warning "Wi-Fi configuration attempt did not succeed locally or was cancelled."
                fi
                ;;
            CHECK)
                if check_internet_connectivity; then exit 0; fi
                ;;
            *) # Should not happen with dialog menu
                log_warning "Invalid choice. Please try again."
                ;;
        esac
        # If loop continues, it means connection was not successful or user chose to try another option.
    done
    exit 1 # Exited loop without successful connection
}

# --- Run Main ---
main "$@"

{% endcodeblock %}
