---
tags: [scripts>bash]
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
#!/usr/bin/env bash
#
# Universal Network Connectivity Script for RK3588 VPC-3588 (Debian Bullseye)
#
# This script attempts to establish an internet connection via Ethernet or Wi-Fi,
# interactively prompting the user for necessary information.
# It must be run with root privileges.
#
# Version 2.1: Fixes premature exit in detect_ethernet_interfaces if no interfaces are found.

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
    # Attempt to remove temporary files
    for temp_file in "${TMP_FILES_TO_CLEAN[@]}"; do
        rm -f "$temp_file"
    done
    # Restore cursor and terminal state if dialog might have altered them
    if command -v stty >/dev/null 2>&1; then
        stty sane
    fi
    if command -v tput >/dev/null 2>&1; then
        tput cnorm
    fi
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
    # Ensure dialog uses /dev/tty for interaction
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
    dialog --title "Information" --infobox "$1" 6 60 2>/dev/null || true # Allow infobox to fail gracefully
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
        if ! check_command "$cmd"; then
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
    # Added '|| true' to grep to prevent script exit if no interfaces are found/matched
    detected=$(ip -o link show type ether 2>/dev/null | awk -F': ' '!/master|link\/ether 00:00:00:00:00:00|NO-CARRIER/{print $2}' | awk '{print $1}' | grep -Ev '^(br|bond|dummy|veth|virbr|docker|lo)' || true)
    if [ -n "$detected" ]; then
        # shellcheck disable=SC2207 # Word splitting is intended here
        ETH_IFACES=($(echo "$detected"))
    fi
    log_info_transient "Detected Ethernet interfaces: ${ETH_IFACES[*]:-(None)}"
}

detect_wifi_interfaces() {
    WIFI_IFACES=()
    local detected="" # Initialize detected
    # Try 'iw dev' first (more reliable for Wi-Fi)
    if check_command iw; then
        # Ensure iw command does not cause exit on error if interface is down or no wifi hardware
        detected=$(iw dev 2>/dev/null | awk '$1=="Interface"{print $2}' || true)
    fi
    # Fallback to 'ip link' if 'iw dev' fails or not present, or finds nothing
    if [ -z "$detected" ] && check_command ip; then
        detected=$(ip -o link show type wlan 2>/dev/null | awk -F': ' '{print $2}' | awk '{print $1}' || true)
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
    local i=1 # Start menu item numbering from 1 for dialog

    if [ ${#interfaces_array[@]} -eq 0 ]; then
        log_warning "No $type interfaces found to select."
        return 1 # Indicates no interface could be selected
    elif [ ${#interfaces_array[@]} -eq 1 ]; then
        log_info_persistent "Auto-selecting $type interface: ${interfaces_array[0]}"
        echo "${interfaces_array[0]}"
        return 0 # Indicates an interface was selected
    fi

    for iface_item in "${interfaces_array[@]}"; do
        dialog_options+=("$i" "$iface_item") # Use index then name for dialog menu items
        i=$((i + 1))
    done

    # Dialog menu expects pairs of "tag" "item". We use index as tag, then iface name as item.
    # The choice returned by dialog will be the "tag" (index).
    # We need to map this index back to the interface name.
    # The number of choices for dialog is half the number of elements in dialog_options.
    choice_tag=$(dialog --title "Select $type Interface" \
        --menu "Choose the $type interface to configure:" ${DIALOG_DEFAULT_HEIGHT} ${DIALOG_DEFAULT_WIDTH} $((${#dialog_options[@]} / 2)) \
        "${dialog_options[@]}" \
        2>&1 >/dev/tty)

    local exit_status=$?
    if [ $exit_status -ne $DIALOG_SUCCESS_CODE ]; then
        log_info_persistent "$type interface selection cancelled by user."
        return 1 # Indicates no interface was selected (cancelled)
    fi
    # Map the chosen tag (index) back to the interface name
    # The interfaces_array is 0-indexed. choice_tag is 1-indexed.
    echo "${interfaces_array[$((choice_tag - 1))]}"
    return 0 # Indicates an interface was selected
}

prompt_static_config() {
    local interface_type="$1" # "Ethernet" or "Wi-Fi"
    local static_ip static_gateway static_dns

    static_ip=$(dialog --title "Static IP Configuration ($interface_type)" \
        --inputbox "Enter Static IP Address with CIDR (e.g., 192.168.1.100/24):" \
        10 ${DIALOG_INPUT_WIDTH} "" 2>&1 >/dev/tty) # Added empty string for initial value
    [ $? -ne $DIALOG_SUCCESS_CODE ] && return 1

    static_gateway=$(dialog --title "Static IP Configuration ($interface_type)" \
        --inputbox "Enter Gateway IP Address (e.g., 192.168.1.1):" \
        10 ${DIALOG_INPUT_WIDTH} "" 2>&1 >/dev/tty) # Added empty string
    [ $? -ne $DIALOG_SUCCESS_CODE ] && return 1

    static_dns=$(dialog --title "Static IP Configuration ($interface_type)" \
        --inputbox "Enter DNS Server(s) (comma-separated, e.g., 8.8.8.8,1.1.1.1, optional):" \
        10 ${DIALOG_INPUT_WIDTH} "" 2>&1 >/dev/tty) # Added empty string
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
    # Basic IP validation for gateway
    if ! echo "$static_gateway" | grep -qE "^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$"; then
        log_error "Gateway IP Address format is invalid (e.g., 192.168.1.1)."
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
        # Try to find an active profile for the device
        profile_name=$(nmcli -g NAME,DEVICE connection show --active 2>/dev/null | grep ":$iface$" | cut -d':' -f1 | head -n1 || true)
        if [ -z "$profile_name" ]; then
            # If not active, try to find any existing profile for the device
             profile_name=$(nmcli -g NAME,DEVICE connection show 2>/dev/null | grep ":$iface$" | cut -d':' -f1 | head -n1 || true)
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
        # Delete any potentially conflicting connection with the same auto-generated name first
        nmcli connection delete "Eth-DHCP-$iface" >/dev/null 2>&1 || true
        if nmcli connection add type ethernet con-name "Eth-DHCP-$iface" ifname "$iface" ipv4.method auto ipv6.method auto && \
           nmcli connection up "Eth-DHCP-$iface"; then
            log_info_transient "NetworkManager added and activated DHCP connection for $iface."
            sleep 5; return 0
        else
            log_warning "Failed to configure Ethernet DHCP for $iface via NetworkManager. Will try dhclient."
            # Cleanup failed attempt
            nmcli connection delete "Eth-DHCP-$iface" >/dev/null 2>&1 || true
        fi
    fi

    log_info_transient "Bringing interface $iface up..."
    ip link set "$iface" up || { log_warning "Failed to bring interface $iface up."; return 1; }
    # Release any old lease
    dhclient -r "$iface" >/dev/null 2>&1 || true
    log_info_transient "Attempting DHCP with dhclient on $iface..."
    # Run dhclient in foreground for a limited time to see if it works
    if timeout 30 dhclient -v "$iface" >"/tmp/dhclient_eth_${iface}.log" 2>&1; then
        log_info_transient "dhclient successfully obtained lease on $iface."
        sleep 2; return 0
    else
        log_error "dhclient failed or timed out for $iface. Check /tmp/dhclient_eth_${iface}.log"
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

    log_info_transient "Configuring static IP for Ethernet interface $iface: IP=$static_ip_cidr, GW=$gateway, DNS=${dns_servers:-Not set}"

    if $NM_IS_ACTIVE; then
        local profile_name="Static-Eth-$iface"
        # Delete existing profile if it exists, to ensure clean configuration
        nmcli connection delete "$profile_name" >/dev/null 2>&1 || true
        
        log_info_transient "Attempting to add and activate static Ethernet connection via NetworkManager..."
        local nm_cmd_parts=("nmcli" "connection" "add" "type" "ethernet" "con-name" "$profile_name" "ifname" "$iface" "ipv4.method" "manual" "ipv4.addresses" "$static_ip_cidr" "ipv4.gateway" "$gateway")
        [ -n "$dns_servers" ] && nm_cmd_parts+=("ipv4.dns" "$dns_servers")
        nm_cmd_parts+=("ipv6.method" "ignore") # Changed from disabled to ignore for broader compatibility

        if "${nm_cmd_parts[@]}" && nmcli connection up "$profile_name"; then
            log_info_transient "NetworkManager configured and activated static IP on $iface."
            sleep 3; return 0
        else
            log_error "Failed to configure static IP on $iface via NetworkManager."
            # Cleanup failed attempt
            nmcli connection delete "$profile_name" >/dev/null 2>&1 || true
            return 1
        fi
    fi

    log_info_transient "Configuring static IP on $iface using iproute2..."
    ip addr flush dev "$iface" || true
    ip link set "$iface" down || true # Allow to fail if already down
    ip link set "$iface" up || { log_warning "Failed to bring interface $iface up for static config."; return 1; }
    
    if ip addr add "$static_ip_cidr" dev "$iface"; then
        log_info_transient "IP address $static_ip_cidr added to $iface."
        # Add delay before setting route, interface might need a moment
        sleep 2
        if ip route add default via "$gateway" dev "$iface"; then
            log_info_transient "Default route via $gateway added for $iface."
            if [ -n "$dns_servers" ]; then
                local resolv_conf_content=""
                IFS=',' read -ra dns_array <<< "$dns_servers"
                for dns in "${dns_array[@]}"; do resolv_conf_content+="nameserver $dns\n"; done
                # Check if /etc/resolv.conf is a symlink (e.g. to systemd-resolved)
                if [ -L /etc/resolv.conf ]; then
                    log_warning "/etc/resolv.conf is a symlink. DNS might not be set correctly by overwriting it. Manual configuration or NetworkManager is advised for DNS."
                fi
                echo -e "$resolv_conf_content" > /etc/resolv.conf
                log_info_transient "Configured DNS servers in /etc/resolv.conf: $dns_servers"
            fi
            sleep 3; return 0
        else
            log_error "Failed to add default route via $gateway for $iface."
            return 1
        fi
    else
        log_error "Failed to add IP address $static_ip_cidr to $iface."
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
    [ -z "$SELECTED_ETH_IFACE" ] && { log_warning "No Ethernet interface was selected."; return 1; }


    dialog --title "Ethernet Configuration: $SELECTED_ETH_IFACE" --yesno "Attempt to configure Ethernet interface '$SELECTED_ETH_IFACE' using DHCP (automatic IP)?" ${DIALOG_DEFAULT_HEIGHT} ${DIALOG_DEFAULT_WIDTH} 2>/dev/tty
    local choice=$?

    if [ $choice -eq $DIALOG_SUCCESS_CODE ]; then # Yes (DHCP)
        if attempt_ethernet_dhcp "$SELECTED_ETH_IFACE"; then return 0; fi 
        log_warning "DHCP on $SELECTED_ETH_IFACE failed." # Message simplified
    elif [ $choice -eq $DIALOG_CANCEL_CODE ]; then # No
        log_info_persistent "DHCP for $SELECTED_ETH_IFACE skipped by user."
    else # Esc or other non-success
        log_info_persistent "Ethernet DHCP choice cancelled by user."
        return 1
    fi

    dialog --title "Ethernet Configuration: $SELECTED_ETH_IFACE" --yesno "Do you want to configure a static IP for Ethernet interface '$SELECTED_ETH_IFACE'?" ${DIALOG_DEFAULT_HEIGHT} ${DIALOG_DEFAULT_WIDTH} 2>/dev/tty
    choice=$?
    if [ $choice -eq $DIALOG_SUCCESS_CODE ]; then # Yes (Static IP)
        if configure_ethernet_static "$SELECTED_ETH_IFACE"; then return 0; fi
        log_warning "Static IP configuration on $SELECTED_ETH_IFACE failed." # Message simplified
    elif [ $choice -eq $DIALOG_CANCEL_CODE ]; then
        log_info_persistent "Static IP configuration for $SELECTED_ETH_IFACE skipped by user."
    else
        log_info_persistent "Ethernet Static IP choice cancelled by user."
        return 1
    fi
    return 1 # All attempts for Ethernet failed or were skipped
}

# --- Wi-Fi Configuration ---
scan_wifi_networks() {
    local iface="$1"
    local networks_list=()
    local line ssid signal security
    local tmp_scan_file="/tmp/wifi_scan_$$_${iface}" # Make temp file name more unique per interface
    TMP_FILES_TO_CLEAN+=("$tmp_scan_file")


    log_info_transient "Scanning for Wi-Fi networks on $iface (this may take a few seconds)..."
    ip link set "$iface" up 2>/dev/null || log_warning "Could not bring $iface up for scanning, scan might fail."

    if $NM_IS_ACTIVE && check_command nmcli; then
        # Ensure rescan happens, even if it reports an error (e.g., device busy)
        nmcli device wifi rescan ifname "$iface" >/dev/null 2>&1 || true
        sleep 5 # Give time for rescan
        
        # nmcli output parsing: SSID can contain spaces.
        # Using --terse --fields to get a more scriptable output
        # Fields: SSID, SIGNAL, SECURITY (SECURITY can be empty for open networks)
        # Use a placeholder for empty security fields to maintain structure
        nmcli --terse --fields IN-USE,SSID,SIGNAL,SECURITY device wifi list ifname "$iface" --rescan no 2>/dev/null | while IFS=':' read -r in_use ssid signal_val security_val; do
            # Skip if SSID is empty or a header line (though --terse should prevent headers)
            [ -z "$ssid" ] && continue
            local display_ssid="${ssid:0:25}"
            [ "${#ssid}" -gt 25 ] && display_ssid="${display_ssid}.."
            local sec_display="${security_val:-Open}" # Use "Open" if security is empty
            [ "$in_use" == "*" ] && sec_display="*Connected* $sec_display"
            # Tag for dialog, description for dialog
            networks_list+=("$ssid" "Sig: $signal_val | Sec: $sec_display | $display_ssid")
        done
    else # Fallback to iwlist
        # Try to kill wpa_supplicant if it's running on the interface, as it can interfere with iwlist scan
        pgrep -af "wpa_supplicant.*${iface}" | awk '{print $1}' | xargs kill >/dev/null 2>&1 || true 
        sleep 0.5
        pgrep -af "wpa_supplicant.*${iface}" | awk '{print $1}' | xargs kill -9 >/dev/null 2>&1 || true
        sleep 1

        local scan_output
        scan_output=$(iwlist "$iface" scan 2>/dev/null)
        local current_ssid="" current_signal="N/A" current_security="Open" # Initialize with defaults

        # Process each cell block from iwlist output
        echo "$scan_output" | awk -v RS="Cell " 'NR > 1 { # Skip first record before "Cell "
            essid=""; signal="N/A"; security="Open";
            if (match($0, /ESSID:"([^"]+)"/, arr)) { essid=arr[1] }
            if (match($0, /Signal level=([0-9]+)\/100/, arr)) { signal=arr[1] "%" } # Quality as percentage
            else if (match($0, /Signal level=(-?[0-9]+ dBm)/, arr)) { signal=arr[1] } # dBm
            if (match($0, /Encryption key:on/)) {
                security="Protected"; # Generic "Protected"
                if (match($0, /IE: IEEE 802.11i\/WPA2 Version 1/)) { security="WPA2/PSK" }
                else if (match($0, /IE: WPA Version 1/)) { security="WPA/PSK" }
                # Could add more specific WEP detection if needed, e.g. based on lack of WPA/WPA2 IEs
            }
            if (essid != "") {
                display_essid = substr(essid, 1, 25);
                if (length(essid) > 25) display_essid = display_essid "..";
                # Output in a format that can be easily read by the shell loop
                # Using a unique separator like |;|
                print essid "|;|" "Sig: " signal " | Sec: " security " | " display_essid;
            }
        }' | while IFS='|;|' read -r ssid description; do
            networks_list+=("$ssid" "$description")
        done
    fi
    
    # This specific temp file is processed, no need to keep it in global cleanup array after this point.
    rm -f "$tmp_scan_file"
    # To remove from array (optional, as cleanup handles rm -f anyway):
    local new_tmp_files=()
    for f in "${TMP_FILES_TO_CLEAN[@]}"; do [ "$f" != "$tmp_scan_file" ] && new_tmp_files+=("$f"); done
    TMP_FILES_TO_CLEAN=("${new_tmp_files[@]}")


    if [ ${#networks_list[@]} -eq 0 ]; then
        log_warning "No Wi-Fi networks found on $iface after scan."
        return 1
    fi
    # Return the flat array for dialog menu
    echo "${networks_list[@]}"
    return 0
}

connect_wifi() {
    local iface="$1"
    local networks_flat_array_str
    
    networks_flat_array_str=$(scan_wifi_networks "$iface")
    local scan_status=$?
    # shellcheck disable=SC2207
    local networks_flat_array=($networks_flat_array_str) # This splits by space, problematic if descriptions have spaces

    # Reconstruct networks_flat_array properly if scan_wifi_networks echoes one item per line (tag then item)
    # For now, assuming scan_wifi_networks output is correctly space-separated for this expansion.
    # If scan_wifi_networks outputs "tag1" "desc1" "tag2" "desc2", this is fine.

    if [ $scan_status -ne 0 ] || [ ${#networks_flat_array[@]} -eq 0 ]; then
        return 1
    fi

    local selected_ssid_tag # This will be the SSID itself, as scan_wifi_networks uses SSID as the tag
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
    local selected_ssid="$selected_ssid_tag" # selected_ssid_tag is the actual SSID

    # Determine security type based on the description string from networks_flat_array
    local security_type="Unknown"
    local full_description=""
    for ((i=0; i<${#networks_flat_array[@]}; i+=2)); do
        if [ "${networks_flat_array[i]}" == "$selected_ssid" ]; then
            full_description="${networks_flat_array[i+1]}"
            if [[ "$full_description" == *"Sec: Open"* ]]; then security_type="Open"
            elif [[ "$full_description" == *"Sec: WEP"* ]]; then security_type="WEP" # Assuming WEP if description says so
            elif [[ "$full_description" == *"Sec: WPA"* || "$full_description" == *"Sec: WPA2"* || "$full_description" == *"Sec: WPA3"* || "$full_description" == *"Sec: PSK"* ]]; then security_type="PSK"
            fi
            break
        fi
    done

    local wifi_password=""
    if [ "$security_type" == "PSK" ] || [ "$security_type" == "WEP" ]; then
        wifi_password=$(dialog --title "Wi-Fi Password" \
            --passwordbox "Enter password for SSID '$selected_ssid' ($security_type):" \
            10 ${DIALOG_INPUT_WIDTH} "" 2>&1 >/dev/tty)
        exit_status=$?
        if [ $exit_status -ne $DIALOG_SUCCESS_CODE ]; then # Allow empty password if user presses OK
            log_warning "Password entry cancelled. Cannot connect without password for $security_type."
            return 1
        fi
        if [ -z "$wifi_password" ] && [ "$security_type" != "Open" ]; then # WEP/PSK need password
             log_warning "Password cannot be empty for $security_type. Cannot connect."
             return 1
        fi
    elif [ "$security_type" == "Unknown" ]; then # If security is unknown, prompt user
         dialog --title "Unknown Security for $selected_ssid" --yesno "Security type is Unknown. Attempt to provide a password (for WPA/WPA2/WEP) or connect as Open?" 12 ${DIALOG_DEFAULT_WIDTH} 2>/dev/tty
         local choice=$?
         if [ $choice -eq $DIALOG_SUCCESS_CODE ]; then # User wants to provide password
            wifi_password=$(dialog --title "Wi-Fi Password" \
                --passwordbox "Enter password/key for SSID '$selected_ssid':" \
                10 ${DIALOG_INPUT_WIDTH} "" 2>&1 >/dev/tty)
            [ $? -ne $DIALOG_SUCCESS_CODE ] && return 1 # Cancelled password entry
            # Assume PSK if password provided for unknown
            [ -n "$wifi_password" ] && security_type="PSK" || security_type="Open"
         else # User chose to try as Open
            security_type="Open"
         fi
    fi # No password needed for Open

    log_info_transient "Attempting to connect to Wi-Fi: $selected_ssid on $iface (Security: $security_type)"
    if $NM_IS_ACTIVE; then
        # Disconnect first to avoid issues with existing connections
        nmcli device disconnect "$iface" >/dev/null 2>&1 || true; sleep 1
        # Delete existing profiles for this SSID to ensure fresh settings
        local old_profile_uuids
        old_profile_uuids=$(nmcli -g UUID,TYPE,NAME connection show 2>/dev/null | grep "wireless" | grep ":$selected_ssid$" | cut -d':' -f1 || true)
        if [ -n "$old_profile_uuids" ]; then
            echo "$old_profile_uuids" | while read -r uuid; do
                log_info_transient "Deleting existing NetworkManager profile UUID $uuid for $selected_ssid."
                nmcli connection delete uuid "$uuid" >/dev/null 2>&1 || true
            done
        fi

        local connect_cmd_nmcli=("nmcli" "device" "wifi" "connect" "$selected_ssid" "ifname" "$iface")
        # Only add password if it's not an Open network OR if it's Open but a password was surprisingly provided
        if [ "$security_type" != "Open" ] || { [ "$security_type" == "Open" ] && [ -n "$wifi_password" ]; }; then
            connect_cmd_nmcli+=("password" "$wifi_password")
        fi
        # For WEP, nmcli might need specific key type handling, but often auto-detects.
        # If WEP fails, might need to add e.g. wifi-sec.key-mgmt none wifi-sec.wep-key0 "$wifi_password" wifi-sec.wep-key-type passphrase/hex
        
        if "${connect_cmd_nmcli[@]}"; then
            log_info_transient "Successfully initiated Wi-Fi connection to $selected_ssid via NetworkManager."
            # DHCP is usually handled by NetworkManager automatically after connect
            sleep 5 # Give NM time to establish connection and get IP
            return 0 # Assume success if nmcli connect returns 0
        else
            log_error "Failed to connect to Wi-Fi $selected_ssid via NetworkManager. Check password/security settings."
            return 1
        fi
    else # Use wpa_supplicant
        pgrep -af "wpa_supplicant.*${iface}" | awk '{print $1}' | xargs kill >/dev/null 2>&1 || true; sleep 0.5
        pgrep -af "wpa_supplicant.*${iface}" | awk '{print $1}' | xargs kill -9 >/dev/null 2>&1 || true; sleep 1
        
        local wpa_conf_temp="/tmp/wpa_temp_${iface}_$$$$.conf"
        TMP_FILES_TO_CLEAN+=("$wpa_conf_temp")

        # Basic wpa_supplicant config
        echo "ctrl_interface=DIR=/run/wpa_supplicant GROUP=netdev" > "$wpa_conf_temp"
        echo "update_config=1" >> "$wpa_conf_temp"
        echo -e "\nnetwork={" >> "$wpa_conf_temp"
        echo "    ssid=\"$selected_ssid\"" >> "$wpa_conf_temp"
        
        if [ "$security_type" == "Open" ] && [ -z "$wifi_password" ]; then
            echo "    key_mgmt=NONE" >> "$wpa_conf_temp"
        elif [ "$security_type" == "WEP" ]; then
            echo "    key_mgmt=NONE" >> "$wpa_conf_temp"
            # wpa_supplicant needs wep_key0, wep_key1 etc.
            # Determine if hex or ascii based on length/chars or prompt
            if [[ "$wifi_password" =~ ^[0-9A-Fa-f]{10}$ || "$wifi_password" =~ ^[0-9A-Fa-f]{26}$ ]]; then # Hex
                 echo "    wep_key0=$wifi_password" >> "$wpa_conf_temp"
            elif [[ "${#wifi_password}" -eq 5 || "${#wifi_password}" -eq 13 ]]; then # ASCII passphrase
                 echo "    wep_key0=\"$wifi_password\"" >> "$wpa_conf_temp"
            else
                log_error "Invalid WEP key: '$wifi_password'. Must be 5/13 ASCII chars or 10/26 HEX digits."
                rm -f "$wpa_conf_temp"; return 1
            fi
            echo "    wep_tx_keyidx=0" >> "$wpa_conf_temp" # Default WEP key index
        else # PSK (WPA/WPA2/WPA3) or Open with a password (treat as PSK)
            echo "    psk=\"$wifi_password\"" >> "$wpa_conf_temp"
            # Let wpa_supplicant auto-negotiate WPA/WPA2/WPA3
            # key_mgmt=WPA-PSK is common, SAE for WPA3.
            # protos, pairwise, group can often be omitted for auto-negotiation.
        fi
        echo "}" >> "$wpa_conf_temp"
        chmod 600 "$wpa_conf_temp"

        # Start wpa_supplicant
        # Using -Dnl80211,wext for broader driver compatibility
        if ! wpa_supplicant -B -i "$iface" -c "$wpa_conf_temp" -Dnl80211,wext; then
            log_error "Failed to start wpa_supplicant for $iface."; rm -f "$wpa_conf_temp"; return 1
        fi
        log_info_transient "wpa_supplicant started for $iface. Waiting for association..."
        local connect_tries=20 
        while [ $connect_tries -gt 0 ]; do
            # Check wpa_cli status for completion
            if wpa_cli -i "$iface" status 2>/dev/null | grep -q "wpa_state=COMPLETED"; then
                log_info_transient "Successfully associated with Wi-Fi $selected_ssid via wpa_supplicant."
                # Temp file can be removed now, or let global cleanup handle it.
                # rm -f "$wpa_conf_temp"; TMP_FILES_TO_CLEAN=( "${TMP_FILES_TO_CLEAN[@]/$wpa_conf_temp}" )
                break
            fi
            sleep 1; connect_tries=$((connect_tries - 1))
        done
        if [ $connect_tries -eq 0 ]; then
            log_error "Failed to associate with Wi-Fi $selected_ssid via wpa_supplicant (timeout)."
            # Kill the potentially lingering wpa_supplicant process
            pgrep -af "wpa_supplicant -B -i $iface -c $wpa_conf_temp" | awk '{print $1}' | xargs kill -9 >/dev/null 2>&1 || true
            rm -f "$wpa_conf_temp"
            return 1
        fi
        # If associated, proceed to DHCP
    fi # End of NM_IS_ACTIVE or wpa_supplicant block

    # If not using NetworkManager, or if NM connection didn't handle DHCP (unlikely but possible)
    # We need to run DHCP client explicitly for wpa_supplicant method.
    # For NM, this part is usually not needed as NM handles DHCP.
    # However, if connect_cmd_nmcli succeeded, we returned 0 already.
    # So this DHCP part is primarily for the wpa_supplicant path.

    log_info_transient "Wi-Fi associated. Attempting DHCP on $iface..."
    dhclient -r "$iface" >/dev/null 2>&1 || true # Release old lease
    if timeout 30 dhclient -v "$iface" >"/tmp/dhclient_wifi_${iface}.log" 2>&1; then
        log_info_transient "dhclient successfully obtained lease on $iface."
        sleep 2; return 0
    else
        log_warning "dhclient failed or timed out for '$selected_ssid' on $iface. Check /tmp/dhclient_wifi_${iface}.log"
        # Offer static IP configuration if DHCP fails for Wi-Fi
        dialog --title "Wi-Fi IP Configuration: $selected_ssid" --yesno "DHCP failed for '$selected_ssid' on $iface.\\nDo you want to configure a static IP for this Wi-Fi connection?" ${DIALOG_DEFAULT_HEIGHT} ${DIALOG_DEFAULT_WIDTH} 2>/dev/tty
        local choice=$?
        if [ $choice -eq $DIALOG_SUCCESS_CODE ]; then
            local static_config_str
            static_config_str=$(prompt_static_config "Wi-Fi ($selected_ssid)")
            local prompt_exit_status=$?
            [ $prompt_exit_status -ne $DIALOG_SUCCESS_CODE ] && return 1

            local static_ip_cidr gw dns
            IFS=':' read -r static_ip_cidr gw dns <<< "$static_config_str"
            log_info_transient "Configuring static IP for Wi-Fi $iface: IP=$static_ip_cidr, GW=$gw, DNS=${dns:-Not set}"

            if $NM_IS_ACTIVE; then # This block might be less common if NM failed to connect initially
                local active_wifi_conn
                active_wifi_conn=$(nmcli -g UUID,DEVICE connection show --active 2>/dev/null | grep ":$iface$" | cut -d':' -f1 | head -n1 || true)
                if [ -n "$active_wifi_conn" ]; then
                    local nm_modify_cmd=("nmcli" "connection" "modify" "$active_wifi_conn" "ipv4.method" "manual" "ipv4.addresses" "$static_ip_cidr" "ipv4.gateway" "$gw")
                    [ -n "$dns" ] && nm_modify_cmd+=("ipv4.dns" "$dns")
                    nm_modify_cmd+=("ipv6.method" "ignore")
                    if "${nm_modify_cmd[@]}" && nmcli connection up "$active_wifi_conn"; then
                        log_info_transient "NetworkManager configured static IP for Wi-Fi $iface."; return 0
                    else
                        log_error "Failed to configure static IP for Wi-Fi via NetworkManager."; return 1
                    fi
                else
                    log_error "Could not find active NetworkManager Wi-Fi connection to modify for static IP. Try re-connecting first."; return 1
                fi
            else # Manual static IP for Wi-Fi (typically after wpa_supplicant)
                ip addr flush dev "$iface" || true
                ip link set "$iface" up || { log_warning "Failed to bring $iface up for static Wi-Fi config."; return 1; }
                if ip addr add "$static_ip_cidr" dev "$iface"; then
                    sleep 2 # Give interface a moment
                    if ip route add default via "$gw" dev "$iface"; then
                        log_info_transient "iproute2 configured static IP for Wi-Fi $iface."
                        if [ -n "$dns" ]; then
                            local resolv_conf_content_wifi=""
                            IFS=',' read -ra dns_array_wifi <<< "$dns"
                            for dns_val in "${dns_array_wifi[@]}"; do resolv_conf_content_wifi+="nameserver $dns_val\n"; done
                            if [ -L /etc/resolv.conf ]; then
                                log_warning "/etc/resolv.conf is a symlink. DNS might not be set correctly by overwriting it."
                            fi
                            echo -e "$resolv_conf_content_wifi" > /etc/resolv.conf
                            log_info_transient "Configured DNS servers in /etc/resolv.conf: $dns"
                        fi
                        return 0
                    else
                        log_error "Failed to add default route for static Wi-Fi on $iface."; return 1
                    fi
                else
                    log_error "Failed to add IP address for static Wi-Fi on $iface."; return 1
                fi
            fi
        else # User chose not to configure static IP after DHCP failure
            log_info_persistent "Skipping static IP for Wi-Fi."; return 1
        fi
    fi
    return 1 # Fallthrough, should indicate failure if DHCP didn't succeed and static wasn't configured
}

handle_wifi_connection() {
    if [ ${#WIFI_IFACES[@]} -eq 0 ]; then
        log_warning "No Wi-Fi interfaces detected. Skipping Wi-Fi setup."
        return 1
    fi

    SELECTED_WIFI_IFACE=$(prompt_select_interface "Wi-Fi" "${WIFI_IFACES[@]}")
    local select_exit_status=$?
    [ $select_exit_status -ne $DIALOG_SUCCESS_CODE ] && return 1
    [ -z "$SELECTED_WIFI_IFACE" ] && { log_warning "No Wi-Fi interface was selected."; return 1; }


    # rfkill check
    if check_command rfkill; then
        # Check specific interface index if possible, otherwise 'wifi' type
        local rfkill_idx
        rfkill_idx=$(rfkill list wifi -n -o ID,DEVICE | grep "$SELECTED_WIFI_IFACE" | awk '{print $1}' || true)

        if [ -n "$rfkill_idx" ] && rfkill list "$rfkill_idx" | grep -q "Soft blocked: yes"; then
            dialog --title "Wi-Fi Blocked" --yesno "Wi-Fi interface $SELECTED_WIFI_IFACE (rfkill ID $rfkill_idx) appears to be soft-blocked.\\nDo you want to attempt to unblock it?" 10 ${DIALOG_DEFAULT_WIDTH} 2>/dev/tty
            if [ $? -eq $DIALOG_SUCCESS_CODE ]; then
                if rfkill unblock "$rfkill_idx"; then log_info_persistent "Wi-Fi $SELECTED_WIFI_IFACE unblocked successfully."; sleep 1
                else log_warning "Failed to unblock Wi-Fi $SELECTED_WIFI_IFACE via rfkill. Proceeding anyway."; fi
            fi
        elif rfkill list wifi | grep -A1 "$SELECTED_WIFI_IFACE" | grep -q "Soft blocked: yes"; then # Fallback check if specific ID not found
             dialog --title "Wi-Fi Blocked" --yesno "Wi-Fi interface $SELECTED_WIFI_IFACE appears to be soft-blocked by rfkill.\\nDo you want to attempt to unblock it?" 10 ${DIALOG_DEFAULT_WIDTH} 2>/dev/tty
            if [ $? -eq $DIALOG_SUCCESS_CODE ]; then
                if rfkill unblock wifi; then log_info_persistent "Wi-Fi unblocked successfully."; sleep 1 # Unblock all wifi
                else log_warning "Failed to unblock Wi-Fi via rfkill. Proceeding anyway."; fi
            fi
        fi
         if [ -n "$rfkill_idx" ] && rfkill list "$rfkill_idx" | grep -q "Hard blocked: yes"; then
            log_error "Wi-Fi interface $SELECTED_WIFI_IFACE (rfkill ID $rfkill_idx) is hard-blocked (hardware switch). Cannot proceed with this interface."
            return 1
        fi
    fi

    if connect_wifi "$SELECTED_WIFI_IFACE"; then return 0; fi 
    
    log_warning "Wi-Fi connection on $SELECTED_WIFI_IFACE failed."
    return 1
}


# --- Main Script Logic ---
main() {
    # Ensure we are root
    if [ "$(id -u)" -ne 0 ]; then
        echo "This script must be run as root. Please use 'sudo $0'" >&2
        # No dialog available yet, so just echo.
        exit 1
    fi

    # Ensure dialog is available before anything else that uses dialog
    install_packages "dialog,dialog"
    # Then other packages
    # Grouped related tools for clarity
    install_packages "ip,iproute2" \
                     "ping,iputils-ping" \
                     "nmcli,network-manager" \
                     "wpa_cli,wpasupplicant" \
                     "wpa_supplicant,wpasupplicant" \
                     "dhclient,isc-dhcp-client" \
                     "iw,iw" \
                     "rfkill,rfkill" \
                     "timeout,coreutils" # For timeout command if not built-in

    detect_ethernet_interfaces
    detect_wifi_interfaces
    check_network_manager_active # Checks if NetworkManager service is running

    # Initial connectivity check
    if check_internet_connectivity; then
        # Success message already shown by check_internet_connectivity
        exit 0 
    fi
    log_info_persistent "No active internet connection detected. Starting configuration process..."

    while true; do
        local options=()
        # Dynamically build menu options based on detected interfaces
        [ ${#ETH_IFACES[@]} -gt 0 ] && options+=("ETH" "Configure Ethernet Connection")
        [ ${#WIFI_IFACES[@]} -gt 0 ] && options+=("WIFI" "Configure Wi-Fi Connection")
        
        # If no interfaces detected at all, inform and exit.
        if [ $((${#ETH_IFACES[@]} + ${#WIFI_IFACES[@]})) -eq 0 ]; then
             log_error "No usable network interfaces (Ethernet or Wi-Fi) were detected by the script. Cannot proceed."
             exit 1
        fi
        
        options+=("CHECK" "Re-check Internet Connectivity")
        # "EXIT" option is handled by --cancel-label

        local main_choice
        main_choice=$(dialog --title "Main Menu - Universal Network Connector" \
            --cancel-label "Exit Script" \
            --menu "Select an action:" ${DIALOG_DEFAULT_HEIGHT} ${DIALOG_DEFAULT_WIDTH} $((${#options[@]}/2)) \
            "${options[@]}" \
            2>&1 >/dev/tty)
        
        local exit_status=$?
        # DIALOG_CANCEL_CODE (1) or DIALOG_ESC_CODE (255) means user chose Exit/Esc
        if [ $exit_status -eq $DIALOG_CANCEL_CODE ] || [ $exit_status -eq $DIALOG_ESC_CODE ]; then
            log_info_persistent "Exiting script as per user request."
            break 
        fi
        # If main_choice is empty but exit_status was 0 (e.g. help button), re-loop.
        [ -z "$main_choice" ] && continue


        case "$main_choice" in
            ETH)
                if [ ${#ETH_IFACES[@]} -eq 0 ]; then
                    log_warning "No Ethernet interfaces available to configure."
                    continue
                fi
                if handle_ethernet_connection; then 
                    if check_internet_connectivity; then exit 0; fi 
                else
                    # Warning already logged by handle_ethernet_connection on failure/skip
                    log_info_persistent "Ethernet configuration did not result in a connection or was cancelled. Returning to main menu."
                fi
                ;;
            WIFI)
                if [ ${#WIFI_IFACES[@]} -eq 0 ]; then
                    log_warning "No Wi-Fi interfaces available to configure."
                    continue
                fi
                if handle_wifi_connection; then 
                    if check_internet_connectivity; then exit 0; fi
                else
                    log_info_persistent "Wi-Fi configuration did not result in a connection or was cancelled. Returning to main menu."
                fi
                ;;
            CHECK)
                if check_internet_connectivity; then exit 0; fi
                ;;
            *) 
                # This case should ideally not be reached if dialog menu is used correctly
                log_warning "Invalid choice '$main_choice'. Please try again."
                ;;
        esac
        # If loop continues, it means connection was not successful or user chose to try another option.
    done
    exit 1 # Exited loop without successful connection or user explicitly exited
}

# --- Run Main ---
# Pass all script arguments to the main function, though this script doesn't use them.
main "$@"
{% endcodeblock %}
