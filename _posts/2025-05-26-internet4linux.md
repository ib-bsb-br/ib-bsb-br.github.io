---
tags: [scripts>bash]
info: aberto.
date: 2025-05-26
type: post
layout: post
published: true
slug: internet4linux
title: 'Internet Connectivity Solution for linux'
---

# sudo apt install
```
sudo apt install -y dialog network-manager wpasupplicant isc-dhcp-client iproute2 iw iputils-ping wireless-tools procps mawk
```

# bash wifi.sh

{% codeblock bash %}
#!/usr/bin/env bash
#
# Universal Network Connectivity Script for RK3588 VPC-3588 (Debian Bullseye)
#
# This script attempts to establish an internet connection via Ethernet or Wi-Fi,
# interactively prompting the user for necessary information.
# It must be run with root privileges.
#
# Version 3.2: Corrected premature 'fi' tokens in scan_wifi_networks.

# --- Script Setup ---
set -e
set -o pipefail

# --- Debug Configuration ---
DEBUG_LEVEL=${DEBUG_LEVEL:-1} # 0=off, 1=basic, 2=verbose, 3=full (used if DBG is true)
DBG=${DBG:-false}             # Global debug flag, can be set by --debug argument
DEBUG_LOG_FILE=""             # Initialized globally, set in main if DBG is true
VERBOSE_COMMANDS=${VERBOSE_COMMANDS:-true} # Set to false to disable command verbosity in debug_exec if DBG is true
XTRACE_FD=6                   # File descriptor for xtrace output

# --- Global Variables ---
ETH_IFACES=()
WIFI_IFACES=()
SELECTED_ETH_IFACE=""
SELECTED_WIFI_IFACE=""
NM_IS_ACTIVE=false
DIALOG_SUCCESS_CODE=0
DIALOG_CANCEL_CODE=1
DIALOG_HELP_CODE=2 # Not explicitly used by this script's dialog calls
DIALOG_EXTRA_CODE=3 # Not explicitly used
DIALOG_ESC_CODE=255 # Standard for Esc key
DIALOG_DEFAULT_HEIGHT=15
DIALOG_DEFAULT_WIDTH=70
DIALOG_INPUT_WIDTH=50

PING_IP_TARGET="8.8.8.8"
PING_HOSTNAME_TARGET="google.com"
PING_COUNT=3
PING_TIMEOUT=2

TMP_FILES_TO_CLEAN=()

# --- Logging Functions ---
_log_to_file() {
    if $DBG && [ -n "$DEBUG_LOG_FILE" ]; then
        echo -e "$1" >> "$DEBUG_LOG_FILE"
    fi
}

debug_log() {
    if ! $DBG; then return 0; fi

    local level_tag="$1"; shift
    local message="$*"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local caller_info="${BASH_SOURCE[1]##*/}:${FUNCNAME[1]}:${BASH_LINENO[0]}"
    local log_entry="[$timestamp] [$level_tag] [$caller_info] $message"

    echo -e "$log_entry" >&2 # Debug logs always go to stderr
    _log_to_file "$log_entry" # And to file if DBG and DEBUG_LOG_FILE is set
}

debug_basic() { if $DBG && [ "$DEBUG_LEVEL" -ge 1 ]; then debug_log "DEBUG" "$@"; fi; }
debug_verbose() { if $DBG && [ "$DEBUG_LEVEL" -ge 2 ]; then debug_log "VERB" "$@"; fi; }
debug_full() { if $DBG && [ "$DEBUG_LEVEL" -ge 3 ]; then debug_log "FULL" "$@"; fi; }

info_log() {
    local message="$*"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local log_entry="[$timestamp] [INFO] $message"
    echo -e "$log_entry" >&2
    _log_to_file "$log_entry"
}

error_log() {
    local message="$*"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local caller_info="${BASH_SOURCE[1]##*/}:${FUNCNAME[1]}:${BASH_LINENO[0]}"
    local log_entry="[$timestamp] [ERROR] [$caller_info] $message"
    echo -e "$log_entry" >&2
    _log_to_file "$log_entry"
}

warning_log() {
    local message="$*"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local caller_info="${BASH_SOURCE[1]##*/}:${FUNCNAME[1]}:${BASH_LINENO[0]}"
    local log_entry="[$timestamp] [WARN] [$caller_info] $message"
    echo -e "$log_entry" >&2
    _log_to_file "$log_entry"
}

debug_exec() {
    local cmd_string="$*"
    debug_verbose "Executing: $cmd_string"

    if $DBG && $VERBOSE_COMMANDS && [ "$DEBUG_LEVEL" -ge 2 ]; then
        local output exit_code
        # Using a subshell to capture output and exit code reliably
        output=$( (eval "$cmd_string") 2>&1)
        exit_code=$?
        
        debug_verbose "Exit code: $exit_code"
        [ -n "$output" ] && debug_full "Output:\n$output"
        
        if [ $exit_code -ne 0 ]; then
            debug_basic "FAILED command: $cmd_string (Exit Code: $exit_code)"
        fi
        echo "$output" 
        return $exit_code
    else
        eval "$cmd_string"
        return $?
    fi
}

debug_var() {
    if ! $DBG || [ "$DEBUG_LEVEL" -lt 2 ]; then return 0; fi
    local var_name="$1"
    local var_value="${!var_name}"
    debug_verbose "Variable $var_name = '$var_value' (length: ${#var_value})"

    if [[ "$var_value" =~ [[:cntrl:]] ]]; then
        debug_basic "WARNING: Variable $var_name contains control characters."
        debug_full "Hex dump for $var_name:\n$(echo -n "$var_value" | hexdump -C)"
    fi
}

# --- Safe File Operations ---
create_temp_file() {
    local prefix="${1:-tmpfile}"
    local suffix_val="${2:-}" # e.g., ".log" or "list"
    local temp_file
    
    local sane_prefix
    sane_prefix=$(echo "$prefix" | tr -cs '[:alnum:]_-' '_')
    local sane_suffix
    sane_suffix=$(echo "$suffix_val" | tr -cs '[:alnum:]_.-' '_')

    # mktemp requires XXXXXX at end of template. Suffix is appended by mktemp if specified.
    # Ensure suffix starts with a dot if it's meant as an extension and not empty.
    if [[ -n "$sane_suffix" && ! "$sane_suffix" =~ ^\. ]]; then
        sane_suffix=".$sane_suffix"
    fi
    
    temp_file=$(mktemp "/tmp/${sane_prefix}.XXXXXX${sane_suffix}")

    if [ -z "$temp_file" ] || [ ! -f "$temp_file" ] && [ ! -d "$temp_file" ]; then
        error_log "Failed to create temporary file with prefix '$sane_prefix' and suffix '$sane_suffix'"
        return 1
    fi

    debug_verbose "Created temporary file: '$temp_file'"
    TMP_FILES_TO_CLEAN+=("$temp_file")
    echo "$temp_file"
    return 0
}

safe_rm() {
    local file_to_remove="$1"
    debug_verbose "Attempting to remove: '$file_to_remove'"

    if [ -z "$file_to_remove" ]; then
        warning_log "safe_rm: Empty filename provided."
        return 1
    fi
    if [ ! -e "$file_to_remove" ]; then
         debug_verbose "File does not exist, skipping removal: '$file_to_remove'"
         return 0
    fi

    if [ ${#file_to_remove} -gt 255 ]; then
        error_log "safe_rm: Filename too long to remove: '$file_to_remove'"
        return 1
    fi
    if [[ "$file_to_remove" =~ (\.\./|/\.\.) ]]; then
        error_log "safe_rm: Path traversal attempt suspected: '$file_to_remove'"
        return 1
    fi
    if [[ "$file_to_remove" == "/" ]] || [[ "$file_to_remove" == "/bin" ]] || [[ "$file_to_remove" == "/etc" ]] ; then
        error_log "safe_rm: Critical path removal protection: '$file_to_remove'"
        return 1
    fi

    if rm -f "$file_to_remove"; then
        debug_verbose "Successfully removed: '$file_to_remove'"
        return 0
    else
        error_log "Failed to remove: '$file_to_remove' (Error: $?)"
        return 1
    fi
}

# --- Cleanup Function ---
cleanup() {
    local exit_code=$?
    debug_basic "Cleanup: Script exiting with code $exit_code"
    
    if [ ${#TMP_FILES_TO_CLEAN[@]} -gt 0 ]; then
        debug_verbose "Cleaning up ${#TMP_FILES_TO_CLEAN[@]} temporary file(s): ${TMP_FILES_TO_CLEAN[*]}"
        for temp_file in "${TMP_FILES_TO_CLEAN[@]}"; do
            safe_rm "$temp_file"
        done
    else
        debug_verbose "No temporary files registered for cleanup."
    fi

    if command -v stty >/dev/null 2>&1; then
        stty sane 2>/dev/null || debug_verbose "stty sane failed (expected on some exits)"
    fi
    if command -v tput >/dev/null 2>&1; then
        tput cnorm 2>/dev/null || debug_verbose "tput cnorm failed (expected on some exits)"
    fi
    
    # Stop xtrace and close its FD if it was used
    if $DBG && [ -n "$DEBUG_LOG_FILE" ]; then
        set +x # Turn off xtrace
        # Close the xtrace file descriptor
        eval "exec $XTRACE_FD>&-" 2>/dev/null || debug_verbose "Failed to close XTRACE_FD $XTRACE_FD"
        info_log "Script exited (Code: $exit_code). Debug log available at: $DEBUG_LOG_FILE"
        echo "Debug log available at: $DEBUG_LOG_FILE" >&2
    else
        info_log "Script exited (Code: $exit_code). Cleanup performed."
    fi

    if [ $exit_code -ne 0 ] && [ $exit_code -ne 130 ]; then # 130 is SIGINT/SIGTERM
        # Only prompt if running in an interactive terminal
        if [ -t 0 ] && [ -t 1 ]; then # Check if stdin and stdout are terminals
            read -rp "Press Enter to close terminal..." </dev/tty
        fi
    fi
    exit $exit_code
}
trap cleanup EXIT
trap 'error_log "Script interrupted by user (SIGINT/SIGTERM)."; exit 130' SIGINT SIGTERM

# --- Dialog UI Functions ---
_show_dialog_message() {
    local type="$1"
    local title="$2"
    local message="$3"
    local height=${4:-8}
    local width=${5:-60}
    
    debug_verbose "Showing dialog: type=$type, title='$title', message snippet='${message:0:50}...'"
    dialog --title "$title" --"$type" "$message" "$height" "$width" 2>/dev/tty
    local dialog_exit_code=$?
    debug_verbose "Dialog ('$title') exit code: $dialog_exit_code"
    return $dialog_exit_code
}

log_info_persistent() { info_log "$1"; _show_dialog_message "msgbox" "Information" "$1"; }
log_info_transient() { info_log "$1"; dialog --title "Information" --infobox "$1" 6 60 2>/dev/tty || true; sleep 1; } # Allow infobox to fail gracefully
log_msg() { info_log "$1"; _show_dialog_message "msgbox" "Message" "$1"; }
log_error() { error_log "$1"; _show_dialog_message "msgbox" "Error" "$1"; }
log_warning() { warning_log "$1"; _show_dialog_message "msgbox" "Warning" "$1"; }

# --- Prerequisite Checks ---
check_command() {
    local cmd_to_check="$1"
    debug_verbose "Checking for command: $cmd_to_check"
    if command -v "$cmd_to_check" >/dev/null 2>&1; then
        debug_verbose "Command '$cmd_to_check' found."
        return 0
    else
        debug_basic "Command '$cmd_to_check' not found."
        return 1
    fi
}

install_packages() {
    local missing_packages_to_install=()
    local pkg_info cmd pkg_name choice
    
    debug_basic "Checking required packages: $@"
    for pkg_info in "$@"; do
        IFS=',' read -r cmd pkg_name <<< "$pkg_info"
        debug_verbose "Checking for command '$cmd' (package '$pkg_name')"
        if ! check_command "$cmd"; then
            debug_basic "Missing command '$cmd' for package '$pkg_name'"
            missing_packages_to_install+=("$pkg_name")
        fi
    done

    if [ ${#missing_packages_to_install[@]} -gt 0 ]; then
        warning_log "Missing packages: ${missing_packages_to_install[*]}"
        dialog --title "Missing Packages" \
               --yesno "The following essential packages are missing: ${missing_packages_to_install[*]}.\\n\\nDo you want to try and install them now?\\n(Requires an existing temporary internet connection or cached packages)" \
               12 ${DIALOG_DEFAULT_WIDTH} 2>/dev/tty
        choice=$?
        debug_basic "Install prompt choice code: $choice"

        if [ $choice -eq $DIALOG_SUCCESS_CODE ]; then
            info_log "User opted to install missing packages: ${missing_packages_to_install[*]}"
            log_info_transient "Attempting to install: ${missing_packages_to_install[*]}..."
            
            if debug_exec "apt-get update -qq"; then
                if debug_exec "apt-get install -y ${missing_packages_to_install[@]}"; then
                    log_info_persistent "Successfully installed missing packages."
                else
                    error_log "Failed to install packages: ${missing_packages_to_install[*]} after apt-get update."
                    log_error "Failed to install some packages. Please install them manually and re-run the script.\\nPackages: ${missing_packages_to_install[*]}"
                    exit 1
                fi
            else
                error_log "'apt-get update' failed. Cannot install packages."
                log_error "'apt-get update' failed. Please check your network connection and apt sources, then re-run the script."
                exit 1
            fi
        else
            error_log "User declined package installation or cancelled."
            log_error "Cannot proceed without essential packages: ${missing_packages_to_install[*]}. Exiting."
            exit 1
        fi
    else
        debug_basic "All required packages are present."
    fi
}

# --- Network Interface and Manager Detection ---
detect_ethernet_interfaces() {
    debug_basic "Detecting Ethernet interfaces..."
    ETH_IFACES=()
    local detected_output
    # Improved detection: exclude virtual interfaces more reliably, handle interfaces without carrier initially
    detected_output=$(debug_exec "ip -o link show type ether 2>/dev/null | awk -F': ' '!/master|link\\/ether 00:00:00:00:00:00/{print \$2}' | awk '{print \$1}' | grep -Ev '^(lo|br|bond|dummy|veth|virbr|docker|tun|tap|vlan|vxlan|macvlan|macvtap|nlmon|gre|ipip|sit|ip6tnl)' || true")
    
    debug_full "Raw detected ethernet interfaces output: '$detected_output'"
    if [ -n "$detected_output" ]; then
        while IFS= read -r iface; do
            iface_clean=$(echo "$iface" | tr -cd '[:alnum:]_-') # Allow hyphens and underscores
            if [[ -n "$iface_clean" && "$iface_clean" == "$iface" ]]; then
                ETH_IFACES+=("$iface_clean")
                debug_verbose "Added Ethernet interface: '$iface_clean'"
            elif [ -n "$iface" ]; then
                 warning_log "Skipped potentially invalid Ethernet interface name: '$iface'"
            fi
        done <<< "$detected_output"
    fi
    log_info_transient "Detected Ethernet interfaces: ${ETH_IFACES[*]:-(None)}"
}

detect_wifi_interfaces() {
    debug_basic "Detecting Wi-Fi interfaces..."
    WIFI_IFACES=()
    local detected_output=""

    if check_command iw; then
        debug_verbose "Attempting Wi-Fi detection with 'iw dev'"
        detected_output=$(debug_exec "iw dev 2>/dev/null | awk '\$1==\"Interface\"{print \$2}' || true")
        debug_full "Raw detected Wi-Fi interfaces output (iw): '$detected_output'"
    fi
    
    if [ -z "$detected_output" ] && check_command ip; then # Fallback if 'iw' fails or not present
        debug_verbose "Attempting Wi-Fi detection with 'ip link' (fallback)"
        # 'type wlan' is more specific for Wi-Fi than just 'type ether'
        detected_output=$(debug_exec "ip -o link show type wlan 2>/dev/null | awk -F': ' '{print \$2}' | awk '{print \$1}' || true")
        debug_full "Raw detected Wi-Fi interfaces output (ip): '$detected_output'"
    fi

    if [ -n "$detected_output" ]; then
        while IFS= read -r iface; do
            iface_clean=$(echo "$iface" | tr -cd '[:alnum:]_-') # Allow hyphens and underscores
            if [[ -n "$iface_clean" && "$iface_clean" == "$iface" ]]; then
                WIFI_IFACES+=("$iface_clean")
                debug_verbose "Added Wi-Fi interface: '$iface_clean'"
            elif [ -n "$iface" ]; then
                warning_log "Skipped potentially invalid Wi-Fi interface name: '$iface'"
            fi
        done <<< "$detected_output"
    fi
    log_info_transient "Detected Wi-Fi interfaces: ${WIFI_IFACES[*]:-(None)}"
}

check_network_manager_active() {
    debug_basic "Checking NetworkManager service status..."
    if check_command systemctl && systemctl is-active --quiet NetworkManager; then
        NM_IS_ACTIVE=true
        info_log "NetworkManager service is active."
        log_info_transient "NetworkManager service is active."
    else
        NM_IS_ACTIVE=false
        info_log "NetworkManager service is not active or not found."
        log_info_transient "NetworkManager service is not active or not found."
    fi
    debug_var "NM_IS_ACTIVE"
}

# --- User Interaction and Selection (Robust Dialog Handling) ---
prompt_select_interface() {
    local type="$1"; shift
    local interfaces_array=("$@")
    local dialog_options=() choice_tag i=1 selected_interface=""

    debug_basic "Prompting user to select $type interface. Available: ${interfaces_array[*]}"
    debug_var "type"

    if [ ${#interfaces_array[@]} -eq 0 ]; then
        log_warning "No $type interfaces found to select."; return 1
    elif [ ${#interfaces_array[@]} -eq 1 ]; then
        selected_interface="${interfaces_array[0]}"
        log_info_persistent "Auto-selecting $type interface: $selected_interface"
        echo "$selected_interface"; return 0
    fi

    for iface_item in "${interfaces_array[@]}"; do dialog_options+=("$i" "$iface_item"); i=$((i + 1)); done
    debug_verbose "Dialog options for $type selection: ${dialog_options[*]}"

    exec 3>&1 
    choice_tag=$(dialog --title "Select $type Interface" \
        --menu "Choose the $type interface to configure:" \
        ${DIALOG_DEFAULT_HEIGHT} ${DIALOG_DEFAULT_WIDTH} $((${#dialog_options[@]} / 2)) \
        "${dialog_options[@]}" 2>&1 1>&3) 
    local dialog_exit_status=$?
    exec 3>&- 

    debug_basic "$type interface selection: dialog exit status: $dialog_exit_status, captured tag: '$choice_tag'"

    if [ $dialog_exit_status -ne $DIALOG_SUCCESS_CODE ]; then
        log_info_persistent "$type interface selection cancelled by user."; return 1
    fi
    
    local choice_tag_cleaned
    choice_tag_cleaned=$(echo "$choice_tag" | tr -cd '0-9') # Ensure only digits
    if [ -z "$choice_tag_cleaned" ] || ! [[ "$choice_tag_cleaned" =~ ^[0-9]+$ ]] || \
       [ "$choice_tag_cleaned" -lt 1 ] || [ "$choice_tag_cleaned" -gt $((${#dialog_options[@]} / 2)) ]; then
        error_log "Invalid or empty selection tag received from $type interface menu: '$choice_tag'"
        log_warning "Invalid selection from $type interface menu."; return 1
    fi
    
    selected_interface="${interfaces_array[$((choice_tag_cleaned - 1))]}"
    debug_basic "User selected $type interface: '$selected_interface'"
    echo "$selected_interface"; return 0
}

prompt_static_config() {
    local interface_type="$1" 
    local static_ip="" static_gateway="" static_dns=""
    local dialog_exit_status

    debug_basic "Prompting for static IP configuration for $interface_type"

    exec 3>&1
    static_ip=$(dialog --title "Static IP Configuration ($interface_type)" \
        --inputbox "Enter Static IP Address with CIDR (e.g., 192.168.1.100/24):" \
        10 ${DIALOG_INPUT_WIDTH} "" 2>&1 1>&3)
    dialog_exit_status=$?
    exec 3>&-
    debug_basic "Static IP dialog exit: $dialog_exit_status, value: '$static_ip'"
    [ $dialog_exit_status -ne $DIALOG_SUCCESS_CODE ] && { log_info_persistent "Static IP entry cancelled."; return 1; }

    exec 3>&1
    static_gateway=$(dialog --title "Static IP Configuration ($interface_type)" \
        --inputbox "Enter Gateway IP Address (e.g., 192.168.1.1):" \
        10 ${DIALOG_INPUT_WIDTH} "" 2>&1 1>&3)
    dialog_exit_status=$?
    exec 3>&-
    debug_basic "Gateway dialog exit: $dialog_exit_status, value: '$static_gateway'"
    [ $dialog_exit_status -ne $DIALOG_SUCCESS_CODE ] && { log_info_persistent "Gateway entry cancelled."; return 1; }

    exec 3>&1
    static_dns=$(dialog --title "Static IP Configuration ($interface_type)" \
        --inputbox "Enter DNS Server(s) (comma-separated, e.g., 8.8.8.8,1.1.1.1, optional):" \
        10 ${DIALOG_INPUT_WIDTH} "" 2>&1 1>&3)
    dialog_exit_status=$?
    exec 3>&-
    debug_basic "DNS dialog exit: $dialog_exit_status, value: '$static_dns'"
    # If DNS entry is cancelled (ESC or Cancel button), dialog_exit_status will be non-zero.
    # In this case, static_dns (captured from dialog's stdout) will be empty.
    # So, we just proceed, and if static_dns is empty, no DNS will be configured.
    if [ $dialog_exit_status -ne $DIALOG_SUCCESS_CODE ]; then
        log_info_persistent "DNS entry cancelled or skipped, DNS will not be set."
        static_dns="" # Ensure it's empty if cancelled
    fi

    if [[ -z "$static_ip" || -z "$static_gateway" ]]; then
        log_error "Static IP and Gateway cannot be empty."; return 1;
    fi
    if ! echo "$static_ip" | grep -qE "/[0-9]{1,2}$"; then
        log_error "Static IP must be in CIDR notation (e.g., 192.168.1.100/24)."; return 1;
    fi
    if ! echo "$static_gateway" | grep -qE "^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$"; then
        log_error "Gateway IP Address format is invalid (e.g., 192.168.1.1)."; return 1;
    fi
    if [ -n "$static_dns" ]; then
        IFS=',' read -ra dns_array <<< "$static_dns"
        for dns_entry in "${dns_array[@]}"; do
            # Trim whitespace from dns_entry
            dns_entry_trimmed=$(echo "$dns_entry" | awk '{$1=$1};1')
            if ! echo "$dns_entry_trimmed" | grep -qE "^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$"; then
                log_error "DNS Server IP Address format is invalid: '$dns_entry_trimmed'."; return 1;
            fi
        done
    fi
    
    debug_verbose "Static config collected: IP='$static_ip', GW='$static_gateway', DNS='$static_dns'"
    echo "$static_ip:$static_gateway:$static_dns"; return 0
}

# --- Connectivity Check ---
check_internet_connectivity() {
    log_info_transient "Checking internet connectivity..."
    debug_basic "Pinging IP: $PING_IP_TARGET, Host: $PING_HOSTNAME_TARGET"

    if debug_exec "ping -c ${PING_COUNT} -W ${PING_TIMEOUT} \"${PING_IP_TARGET}\"" >/dev/null 2>&1; then
        info_log "Successfully pinged IP address (${PING_IP_TARGET}). Basic connectivity OK."
        log_info_transient "Ping to IP ${PING_IP_TARGET} successful."
        if debug_exec "ping -c ${PING_COUNT} -W ${PING_TIMEOUT} \"${PING_HOSTNAME_TARGET}\"" >/dev/null 2>&1; then
            log_msg "Internet connection established and DNS resolution working (pinged ${PING_HOSTNAME_TARGET})."
            return 0
        else
            warning_log "DNS resolution failed (cannot ping ${PING_HOSTNAME_TARGET}). Check DNS settings."
            log_warning "Successfully pinged IP, but DNS resolution failed for ${PING_HOSTNAME_TARGET}. Check DNS settings."; return 2 # Special code for DNS failure
        fi
    else
        warning_log "Failed to ping IP address (${PING_IP_TARGET}). No basic network connectivity."
        log_warning "Failed to ping IP address (${PING_IP_TARGET}). No basic network connectivity."; return 1
    fi
}

# --- Ethernet Configuration ---
attempt_ethernet_dhcp() {
    local iface="$1"
    debug_basic "Attempting DHCP on Ethernet interface: $iface. NM_IS_ACTIVE=$NM_IS_ACTIVE"
    log_info_transient "Attempting DHCP on Ethernet interface: $iface"

    if $NM_IS_ACTIVE; then
        local profile_name
        # Try to find an active connection for the device first
        profile_name=$(nmcli -g NAME,DEVICE connection show --active 2>/dev/null | grep -E ":$iface$" | cut -d':' -f1 | head -n1 || true)
        [ -z "$profile_name" ] && profile_name=$(nmcli -g NAME,DEVICE connection show 2>/dev/null | grep -E ":$iface$" | cut -d':' -f1 | head -n1 || true)
        debug_verbose "NM existing profile for $iface: '$profile_name'"

        if [ -n "$profile_name" ]; then
            log_info_transient "Found existing NM profile '$profile_name' for $iface. Ensuring DHCP and activating..."
            # Modify to DHCP and then activate
            if debug_exec "nmcli connection modify \"$profile_name\" ipv4.method auto ipv6.method auto" && \
               debug_exec "nmcli connection up \"$profile_name\" ifname \"$iface\""; then
                log_info_transient "NetworkManager activated DHCP profile '$profile_name' for $iface."; sleep 5; return 0
            else
                warning_log "Failed to activate existing DHCP profile '$profile_name' for $iface via NM. Trying to add a new one."
            fi
        fi
        
        log_info_transient "Attempting to add and activate a new DHCP Ethernet connection for $iface via NetworkManager..."
        local new_profile_name="Eth-DHCP-$iface-$(date +%s)" # Make profile name more unique
        nmcli connection delete "$new_profile_name" >/dev/null 2>&1 || true # Clean up if it somehow exists
        if debug_exec "nmcli connection add type ethernet con-name \"$new_profile_name\" ifname \"$iface\" ipv4.method auto ipv6.method auto" && \
           debug_exec "nmcli connection up \"$new_profile_name\""; then
            log_info_transient "NetworkManager added and activated DHCP connection for $iface."; sleep 5; return 0
        else
            warning_log "Failed to configure Ethernet DHCP for $iface via NetworkManager. Will try dhclient."
            nmcli connection delete "$new_profile_name" >/dev/null 2>&1 || true # Cleanup failed attempt
        fi
    fi

    log_info_transient "Bringing interface $iface up..."
    if ! debug_exec "ip link set \"$iface\" up"; then log_warning "Failed to bring interface $iface up."; return 1; fi
    # Release any old lease for the interface
    debug_exec "dhclient -r \"$iface\"" >/dev/null 2>&1 || true 
    
    local dhclient_log
    dhclient_log=$(create_temp_file "dhclient_eth_${iface}" "log")
    [ $? -ne 0 ] && { error_log "Failed to create dhclient log file."; dhclient_log="/dev/null"; } # Proceed even if log creation fails

    log_info_transient "Attempting DHCP with dhclient on $iface..."
    if debug_exec "timeout 30 dhclient -v \"$iface\"" >"$dhclient_log" 2>&1; then
        log_info_transient "dhclient successfully obtained lease on $iface."
        debug_full "dhclient log for $iface:\n$(cat "$dhclient_log")"; sleep 2; return 0
    else
        error_log "dhclient failed or timed out for $iface. Log: $dhclient_log"
        log_error "dhclient failed or timed out for $iface. Check log: $dhclient_log"
        debug_full "dhclient log for $iface on failure:\n$(cat "$dhclient_log")"; return 1
    fi
}

configure_ethernet_static() {
    local iface="$1" config_str prompt_exit_status static_ip_cidr gateway dns_servers
    debug_basic "Configuring static Ethernet for $iface. NM_IS_ACTIVE=$NM_IS_ACTIVE"
    
    config_str=$(prompt_static_config "Ethernet ($iface)")
    prompt_exit_status=$?
    [ $prompt_exit_status -ne 0 ] && return 1
    debug_verbose "Static config string from prompt: '$config_str'"

    IFS=':' read -r static_ip_cidr gateway dns_servers <<< "$config_str"
    log_info_transient "Configuring static IP for Ethernet $iface: IP=$static_ip_cidr, GW=$gateway, DNS=${dns_servers:-Not set}"

    if $NM_IS_ACTIVE; then
        local profile_name="Static-Eth-$iface-$(date +%s)" nm_cmd_parts=() # Make profile name more unique
        nmcli connection delete "$profile_name" >/dev/null 2>&1 || true 
        
        log_info_transient "Attempting to add/activate static Ethernet connection via NetworkManager..."
        nm_cmd_parts=("nmcli" "connection" "add" "type" "ethernet" "con-name" "$profile_name" "ifname" "$iface" "ipv4.method" "manual" "ipv4.addresses" "$static_ip_cidr" "ipv4.gateway" "$gateway")
        [ -n "$dns_servers" ] && nm_cmd_parts+=("ipv4.dns" "$dns_servers")
        nm_cmd_parts+=("ipv6.method" "ignore") # Typically ignore IPv6 for simple static setups

        if debug_exec "${nm_cmd_parts[@]}" && debug_exec "nmcli connection up \"$profile_name\""; then
            log_info_transient "NetworkManager configured and activated static IP on $iface."; sleep 3; return 0
        else
            error_log "Failed to configure static IP on $iface via NetworkManager."
            log_error "NM static IP configuration failed for $iface."
            nmcli connection delete "$profile_name" >/dev/null 2>&1 || true; return 1 # Cleanup failed attempt
        fi
    fi

    # Fallback to iproute2 if NM is not active or failed
    log_info_transient "Configuring static IP on $iface using iproute2..."
    debug_exec "ip addr flush dev \"$iface\"" || true # Clear existing IPs
    debug_exec "ip link set \"$iface\" down" || true # Take interface down before reconfiguring
    if ! debug_exec "ip link set \"$iface\" up"; then log_warning "Failed to bring interface $iface up for static config."; return 1; fi
    
    if debug_exec "ip addr add \"$static_ip_cidr\" dev \"$iface\""; then
        log_info_transient "IP address $static_ip_cidr added to $iface."; sleep 2
        # Remove existing default routes for this interface before adding a new one
        debug_exec "ip route del default dev \"$iface\"" 2>/dev/null || true
        if debug_exec "ip route add default via \"$gateway\" dev \"$iface\""; then
            log_info_transient "Default route via $gateway added for $iface."
            if [ -n "$dns_servers" ]; then
                local resolv_conf_content=""
                IFS=',' read -ra dns_array <<< "$dns_servers"
                for dns in "${dns_array[@]}"; do 
                    dns_trimmed=$(echo "$dns" | awk '{$1=$1};1') # Trim whitespace
                    resolv_conf_content+="nameserver $dns_trimmed\n"
                done
                
                if [ -L /etc/resolv.conf ] && ! command -v resolvconf >/dev/null 2>&1 && ! command -v systemd-resolve >/dev/null 2>&1; then
                    warning_log "/etc/resolv.conf is a symlink. Overwriting it for DNS might be overridden if not managed by resolvconf or systemd-resolved."
                    log_warning "/etc/resolv.conf is a symlink. DNS might not be set correctly by overwriting it."
                fi
                # This is a direct overwrite, might be temporary if NetworkManager or systemd-resolved is running
                echo -e "$resolv_conf_content" > /etc/resolv.conf
                info_log "Configured DNS servers in /etc/resolv.conf: $dns_servers (manual iproute2 mode)"
                log_info_transient "DNS servers set in /etc/resolv.conf: $dns_servers"
            fi
            sleep 3; return 0
        else
            error_log "Failed to add default route via $gateway for $iface."
            log_error "Failed to add default route for $iface."; return 1
        fi
    else
        error_log "Failed to add IP address $static_ip_cidr to $iface."
        log_error "Failed to add IP address to $iface."; return 1
    fi
}

handle_ethernet_connection() {
    local select_exit_status choice
    debug_basic "Handling Ethernet connection. Detected interfaces: ${#ETH_IFACES[@]}"
    if [ ${#ETH_IFACES[@]} -eq 0 ]; then
        log_warning "No Ethernet interfaces detected. Skipping Ethernet setup."; return 1
    fi

    SELECTED_ETH_IFACE=$(prompt_select_interface "Ethernet" "${ETH_IFACES[@]}")
    select_exit_status=$?
    debug_basic "Ethernet interface selection: exit_status=$select_exit_status, SELECTED_ETH_IFACE='$SELECTED_ETH_IFACE'"
    [ $select_exit_status -ne 0 ] && return 1
    [ -z "$SELECTED_ETH_IFACE" ] && { log_warning "No Ethernet interface was actually selected."; return 1; }

    dialog --title "Ethernet Configuration: $SELECTED_ETH_IFACE" \
           --yesno "Attempt to configure '$SELECTED_ETH_IFACE' using DHCP (automatic IP)?" \
           ${DIALOG_DEFAULT_HEIGHT} ${DIALOG_DEFAULT_WIDTH} 2>/dev/tty
    choice=$?
    if [ $choice -eq $DIALOG_SUCCESS_CODE ]; then
        if attempt_ethernet_dhcp "$SELECTED_ETH_IFACE"; then return 0; fi
        log_warning "DHCP on $SELECTED_ETH_IFACE failed. Offering static IP."
    elif [ $choice -eq $DIALOG_CANCEL_CODE ]; then # User selected "No" for DHCP
        log_info_persistent "DHCP for $SELECTED_ETH_IFACE skipped by user."
    else # ESC or other dialog error
        log_info_persistent "Ethernet DHCP choice cancelled or dialog error."; return 1
    fi

    # Offer static IP if DHCP failed or was skipped
    dialog --title "Ethernet Configuration: $SELECTED_ETH_IFACE" \
           --yesno "Do you want to configure a static IP for '$SELECTED_ETH_IFACE'?" \
           ${DIALOG_DEFAULT_HEIGHT} ${DIALOG_DEFAULT_WIDTH} 2>/dev/tty
    choice=$?
    if [ $choice -eq $DIALOG_SUCCESS_CODE ]; then
        if configure_ethernet_static "$SELECTED_ETH_IFACE"; then return 0; fi
        log_warning "Static IP configuration on $SELECTED_ETH_IFACE failed."
    elif [ $choice -eq $DIALOG_CANCEL_CODE ]; then # User selected "No" for Static IP
        log_info_persistent "Static IP configuration for $SELECTED_ETH_IFACE skipped by user."
    else # ESC or other dialog error
        log_info_persistent "Ethernet Static IP choice cancelled or dialog error."; return 1
    fi
    
    debug_basic "Ethernet configuration for $SELECTED_ETH_IFACE did not succeed."; return 1
}

# --- Wi-Fi Configuration (Robust Scanning) ---
scan_wifi_networks() {
    local iface="$1"
    local networks_list=() 
    local tmp_scan_file
    
    debug_basic "Scanning Wi-Fi networks on interface: $iface. NM_IS_ACTIVE=$NM_IS_ACTIVE"
    log_info_transient "Scanning for Wi-Fi networks on $iface (this may take a few seconds)..."

    tmp_scan_file=$(create_temp_file "wifi_scan_${iface}" "list")
    if [ $? -ne 0 ] || [ -z "$tmp_scan_file" ]; then
        error_log "Failed to create temporary file for Wi-Fi scan on $iface."; return 1
    fi

    # Ensure interface is up for scanning, but don't fail if it errors (might be already up or managed)
    debug_exec "ip link set \"$iface\" up" 2>/dev/null || warning_log "Could not bring $iface up for scanning, scan might be incomplete."

    if $NM_IS_ACTIVE && check_command nmcli; then
        debug_verbose "Using nmcli for Wi-Fi scan on $iface."
        # Request a rescan if possible
        debug_exec "nmcli device wifi rescan ifname \"$iface\"" >/dev/null 2>&1 || true 
        sleep 3 # Give some time for the rescan to populate

        # nmcli output: IN-USE:SSID:BARS:SECURITY (BARS is signal strength as string like '▂▄▆_')
        # Awk processes this to: SSID\0Description\n
        # Robustly parse nmcli terse output, handling colons in SSIDs.
        # The strategy is to identify fixed position fields from the right (SECURITY, BARS)
        # and assume the middle part is the SSID.
        debug_exec "nmcli -t -f IN-USE,SSID,BARS,SECURITY device wifi list ifname \"$iface\" --rescan no" 2>/dev/null | \
        awk -F: '
            # awk script for nmcli output processing
            # Input format: IN-USE:SSID:BARS:SECURITY (SSID can contain colons)
            # Output format for mapfile: SSID\0Description\n
            BEGIN { OFS="\0"; ORS="\n" }
            {
                if (NF < 4) { # Expect at least 4 fields (e.g. *:OpenSSID:strength:Open)
                    # Handle cases with empty SSID or unexpected format if necessary
                    # print "AWK_NMCLI_PARSE_WARN: Skipping line due to insufficient fields: " $0 > "/dev/stderr";
                    next;
                }

                in_use_field = $1;
                # Reconstruct SSID: from $2 up to $(NF-2)
                ssid_field = $2;
                for (i = 3; i <= NF - 2; i++) {
                    ssid_field = ssid_field ":" $i;
                }
                
                # Remove potential escaping if nmcli added any (unlikely with -t)
                # gsub(/\\:/, ":", ssid_field); # Example if nmcli escaped colons in SSID

                bars_field = $(NF-1); # Second to last field
                security_field = $NF;   # Last field

                if (ssid_field == "") next; # Skip if SSID is empty after reconstruction

                # Create display SSID (truncated)
                display_ssid = substr(ssid_field, 1, 25);
                if (length(ssid_field) > 25) display_ssid = display_ssid "..";

                # Format security display string
                sec_display = (security_field == "" ? "Open" : security_field);
                # Prepend *Connected* if IN-USE is '*'
                if (in_use_field == "*") sec_display = "*Connected* " sec_display;

                # Construct description string
                description = "Sig: " bars_field " | Sec: " sec_display " | " display_ssid;
                
                # Output SSID and Description, null-separated, newline-terminated
                print ssid_field, description;
            }
        ' > "$tmp_scan_file"
        # CORRECTED: Check command status without premature 'fi'
        [ $? -ne 0 ] && error_log "nmcli scan or awk processing failed for $iface."

    elif check_command iwlist; then
        debug_verbose "Using iwlist for Wi-Fi scan on $iface."
        # Try to kill any existing wpa_supplicant for this interface to ensure iwlist can scan
        pgrep -af "wpa_supplicant.*${iface}" | awk '{print $1}' | xargs -r kill >/dev/null 2>&1 || true; sleep 0.5
        pgrep -af "wpa_supplicant.*${iface}" | awk '{print $1}' | xargs -r kill -9 >/dev/null 2>&1 || true; sleep 1

        debug_exec "iwlist \"$iface\" scan" 2>/dev/null | \
        awk -v RS="Cell " '
            # awk script for iwlist output processing
            # Input: iwlist scan output, record separated by "Cell "
            # Output format for mapfile: SSID\0Description\n
            NR > 1 { # Skip first record as it is not a cell
                essid=""; signal="N/A"; security="Open";
                # Extract ESSID
                if (match($0, /ESSID:"([^"]+)"/, arr_essid)) { essid=arr_essid[1] }
                # Clean control characters from ESSID
                gsub(/[[:cntrl:]]/, "", essid);
                if (essid == "") next; # Skip if no ESSID

                # Extract Signal Quality/Level
                if (match($0, /Quality=([0-9]+\/[0-9]+).*Signal level=(-?[0-9]+ dBm)/, arr_sig)) { signal=arr_sig[1] " (" arr_sig[2] ")" }
                else if (match($0, /Signal level=(-?[0-9]+ dBm)/, arr_sig)) { signal=arr_sig[1] }
                else if (match($0, /Quality=([0-9]+\/[0-9]+)/, arr_sig)) { signal=arr_sig[1] }

                # Determine Security Type
                if (match($0, /Encryption key:on/)) {
                    security="Protected"; # Generic
                    # More specific checks for WPA/WPA2/WEP
                    # This logic is a bit simplistic; WPA/WPA2 is usually in IEs
                    if (!match($0, /IE: IEEE 802.11i\/WPA2/) && !match($0, /IE: WPA Version 1/)) {
                         security="WEP"; 
                    }
                }
                # Prioritize WPA2/WPA detection from IEs
                if (match($0, /IE: IEEE 802.11i\/WPA2 Version 1/)) { security="WPA2/PSK" } 
                else if (match($0, /IE: WPA Version 1/)) { security="WPA/PSK" } 
                # Note: WPA3/SAE detection from iwlist is less reliable, may need "IE:.*SAE"

                # Create display ESSID (truncated)
                display_essid = substr(essid, 1, 25);
                if (length(essid) > 25) display_essid = display_essid "..";
                
                # Construct description string
                description = "Sig: " signal " | Sec: " security " | " display_essid;
                
                # Output SSID and Description, null-separated, newline-terminated
                printf "%s\0%s\n", essid, description;
            }' > "$tmp_scan_file"
        # CORRECTED: Check command status without premature 'fi'
        [ $? -ne 0 ] && error_log "iwlist scan or awk processing failed for $iface."
    else
        error_log "No suitable tool (nmcli or iwlist) found for Wi-Fi scanning on $iface."
        safe_rm "$tmp_scan_file"; TMP_FILES_TO_CLEAN=("${TMP_FILES_TO_CLEAN[@]/$tmp_scan_file}"); return 1
    fi # This 'fi' now correctly closes the entire if/elif/else structure.
    
    # Read into array using null delimiter, expecting pairs (SSID, Description)
    mapfile -t -d $'\0' networks_list < "$tmp_scan_file"
    local mapfile_status=$?
    debug_full "mapfile status: $mapfile_status. Networks list size: ${#networks_list[@]}"
    
    # Remove the temporary file from the global cleanup list as it's processed here
    safe_rm "$tmp_scan_file"
    TMP_FILES_TO_CLEAN=("${TMP_FILES_TO_CLEAN[@]/$tmp_scan_file}") # Remove from global list

    if [ ${#networks_list[@]} -eq 0 ]; then
        log_warning "No Wi-Fi networks found on $iface after scan, or error reading scan data."
        return 1
    fi

    debug_basic "Wi-Fi scan on $iface found $((${#networks_list[@]}/2)) networks."
    if $DBG && [ "$DEBUG_LEVEL" -ge 3 ]; then
        for ((i=0; i < ${#networks_list[@]}; i+=2)); do
            debug_full "Scan result: SSID='${networks_list[i]}', DESC='${networks_list[i+1]}'"
        done
    fi
    
    # Print the flat array (SSID\nDescription\nSSID\nDescription...) for connect_wifi to mapfile again
    printf "%s\n" "${networks_list[@]}"; return 0
}

connect_wifi() {
    local iface="$1" networks_flat_array_str networks_flat_array=()
    local scan_status selected_ssid security_type full_description wifi_password exit_status choice
    local wpa_conf_temp connect_tries static_config_str static_ip_cidr gw dns_val
    local resolv_conf_content_wifi dns_array_wifi active_wifi_conn nm_modify_cmd

    debug_basic "Attempting to connect Wi-Fi on interface: $iface. NM_IS_ACTIVE=$NM_IS_ACTIVE"

    networks_flat_array_str=$(scan_wifi_networks "$iface")
    scan_status=$? 
    
    if [ $scan_status -ne 0 ] || [ -z "$networks_flat_array_str" ]; then
        log_warning "Failed to retrieve Wi-Fi networks or no networks found for $iface."; return 1
    fi
    # networks_flat_array_str is already newline separated from printf in scan_wifi_networks
    mapfile -t networks_flat_array <<< "$networks_flat_array_str"
    debug_verbose "Retrieved ${#networks_flat_array[@]} items for Wi-Fi selection dialog."

    # Ensure we have pairs for the dialog menu (SSID, Description)
    if [ $((${#networks_flat_array[@]} % 2)) -ne 0 ]; then
        error_log "Wi-Fi scan data is malformed (not in pairs). Cannot proceed."
        return 1
    fi

    exec 3>&1
    selected_ssid=$(dialog --title "Select Wi-Fi Network ($iface)" \
        --menu "Choose the Wi-Fi network (SSID) to connect to:" \
        $((DIALOG_DEFAULT_HEIGHT + 5)) ${DIALOG_DEFAULT_WIDTH} $((${#networks_flat_array[@]} / 2)) \
        "${networks_flat_array[@]}" 2>&1 1>&3)
    exit_status=$?
    exec 3>&-
    debug_basic "Wi-Fi selection dialog: exit_status=$exit_status, selected_ssid_tag='$selected_ssid'"

    if [ $exit_status -ne $DIALOG_SUCCESS_CODE ] || [ -z "$selected_ssid" ]; then
        log_info_persistent "Wi-Fi network selection cancelled or empty."; return 1
    fi

    # Determine security type based on the description string from the scan
    security_type="Unknown" # Default
    for ((i=0; i<${#networks_flat_array[@]}; i+=2)); do
        if [ "${networks_flat_array[i]}" == "$selected_ssid" ]; then
            full_description="${networks_flat_array[i+1]}"
            debug_verbose "Full description for '$selected_ssid': '$full_description'"
            # More specific security type detection based on common patterns
            if [[ "$full_description" == *"Sec: Open"* ]]; then security_type="Open"
            elif [[ "$full_description" == *"Sec: WEP"* ]]; then security_type="WEP"
            elif [[ "$full_description" == *"Sec: WPA2/PSK"* || "$full_description" == *"Sec: WPA2"* ]]; then security_type="PSK" # WPA2 implies PSK for consumer
            elif [[ "$full_description" == *"Sec: WPA/PSK"* || "$full_description" == *"Sec: WPA"* ]]; then security_type="PSK" # WPA implies PSK
            elif [[ "$full_description" == *"Sec: PSK"* ]]; then security_type="PSK"
            elif [[ "$full_description" == *"Sec: WPA3"* || "$full_description" == *"Sec: SAE"* ]]; then security_type="PSK" # WPA3/SAE often needs PSK input method
            elif [[ "$full_description" == *"Sec: Protected"* && "$security_type" == "Unknown" ]]; then security_type="PSK" # Generic fallback
            fi; break
        fi
    done
    debug_basic "Determined security type for '$selected_ssid': $security_type"

    wifi_password=""
    if [ "$security_type" == "PSK" ] || [ "$security_type" == "WEP" ]; then
        exec 3>&1
        wifi_password=$(dialog --title "Wi-Fi Password" \
            --passwordbox "Enter password for SSID '$selected_ssid' ($security_type):" \
            10 ${DIALOG_INPUT_WIDTH} "" 2>&1 1>&3)
        exit_status=$?
        exec 3>&-
        debug_basic "Password dialog exit: $exit_status"
        if [ $exit_status -ne $DIALOG_SUCCESS_CODE ]; then
            log_warning "Password entry cancelled. Cannot connect to $security_type network."; return 1
        fi
        # Allow empty password for WEP if user insists, though unlikely to work
        if [ "$security_type" == "PSK" ] && [ -z "$wifi_password" ]; then
             log_warning "Password cannot be empty for $security_type. Cannot connect."; return 1
        fi
    elif [ "$security_type" == "Unknown" ]; then # If security is still unknown, prompt
        dialog --title "Unknown Security for $selected_ssid" \
               --yesno "Security type is Unknown. Attempt to provide a password (for WPA/WEP/PSK types) or connect as Open network?" \
               12 ${DIALOG_DEFAULT_WIDTH} 2>/dev/tty
        choice=$?
        if [ $choice -eq $DIALOG_SUCCESS_CODE ]; then # User wants to provide password
            exec 3>&1
            wifi_password=$(dialog --title "Wi-Fi Password" \
                --passwordbox "Enter password/key for SSID '$selected_ssid':" \
                10 ${DIALOG_INPUT_WIDTH} "" 2>&1 1>&3)
            exit_status=$?
            exec 3>&-
            [ $exit_status -ne $DIALOG_SUCCESS_CODE ] && { log_warning "Password entry cancelled."; return 1; }
            [ -n "$wifi_password" ] && security_type="PSK" || security_type="Open" # Assume PSK if password provided
        else # User wants to try as Open, or cancelled
            security_type="Open"
        fi
        debug_basic "Security for 'Unknown' network, after prompt: $security_type"
    fi
    debug_var "wifi_password" # Be careful logging passwords, even to debug logs

    log_info_transient "Attempting to connect to Wi-Fi: $selected_ssid on $iface (Security: $security_type)"
    if $NM_IS_ACTIVE; then
        debug_verbose "Using NetworkManager to connect to Wi-Fi."
        debug_exec "nmcli device disconnect \"$iface\"" >/dev/null 2>&1 || true; sleep 1 # Disconnect first
        
        # Delete existing connections for this SSID to avoid conflicts or using old passwords
        local old_profile_uuids
        old_profile_uuids=$(nmcli -g UUID,TYPE,NAME connection show 2>/dev/null | grep -E "wireless|802-11-wireless" | grep ":$selected_ssid$" | cut -d':' -f1 || true)
        if [ -n "$old_profile_uuids" ]; then
            echo "$old_profile_uuids" | while read -r uuid_to_delete; do
                info_log "Deleting existing NM profile UUID $uuid_to_delete for SSID '$selected_ssid'."
                debug_exec "nmcli connection delete uuid \"$uuid_to_delete\"" >/dev/null 2>&1 || true
            done
        fi

        local connect_cmd_nmcli=("nmcli" "device" "wifi" "connect" "$selected_ssid" "ifname" "$iface")
        # Only add password if security type suggests it or if password is not empty (for "Open" with password attempts)
        if { [ "$security_type" != "Open" ] && [ -n "$wifi_password" ]; } || \
           { [ "$security_type" == "Open" ] && [ -n "$wifi_password" ]; }; then # Handles case where user forces password for "Open"
            connect_cmd_nmcli+=("password" "$wifi_password")
        fi
        # For WEP, nmcli might need specific syntax if 'password' isn't enough.
        # if [ "$security_type" == "WEP" ]; then connect_cmd_nmcli+=("wep-key-type" "passphrase"); fi # Example

        if debug_exec "${connect_cmd_nmcli[@]}"; then
            log_info_transient "Successfully initiated Wi-Fi connection to $selected_ssid via NetworkManager."; sleep 5; return 0 
        else
            error_log "Failed to connect to Wi-Fi $selected_ssid via NetworkManager."
            log_error "NM Wi-Fi connection failed for '$selected_ssid'. Check password/security."; return 1
        fi
    else 
        # Manual connection using wpa_supplicant
        debug_verbose "Using wpa_supplicant to connect to Wi-Fi."
        pgrep -af "wpa_supplicant.*${iface}" | awk '{print $1}' | xargs -r kill >/dev/null 2>&1 || true; sleep 0.5
        pgrep -af "wpa_supplicant.*${iface}" | awk '{print $1}' | xargs -r kill -9 >/dev/null 2>&1 || true; sleep 1
        
        wpa_conf_temp=$(create_temp_file "wpa_temp_${iface}" "conf")
        if [ $? -ne 0 ] || [ -z "$wpa_conf_temp" ]; then error_log "Failed to create wpa_supplicant temp conf file."; return 1; fi

        # Basic wpa_supplicant configuration
        echo "ctrl_interface=DIR=/run/wpa_supplicant GROUP=netdev" > "$wpa_conf_temp"
        echo "update_config=1" >> "$wpa_conf_temp"
        echo -e "\nnetwork={" >> "$wpa_conf_temp"
        echo "    ssid=\"$selected_ssid\"" >> "$wpa_conf_temp"
        
        if [ "$security_type" == "Open" ] && [ -z "$wifi_password" ]; then
            echo "    key_mgmt=NONE" >> "$wpa_conf_temp"
        elif [ "$security_type" == "WEP" ]; then
            echo "    key_mgmt=NONE" >> "$wpa_conf_temp"
            # Handle WEP key (hex or passphrase)
            if [[ "$wifi_password" =~ ^[0-9A-Fa-f]{10}$ || "$wifi_password" =~ ^[0-9A-Fa-f]{26}$ ]]; then # Hex key
                echo "    wep_key0=$wifi_password" >> "$wpa_conf_temp"
            elif [[ "${#wifi_password}" -eq 5 || "${#wifi_password}" -eq 13 ]]; then # ASCII passphrase
                echo "    wep_key0=\"$wifi_password\"" >> "$wpa_conf_temp"
            else
                error_log "Invalid WEP key format for '$selected_ssid'. Expected 5/13 ASCII or 10/26 HEX chars."; 
                log_error "Invalid WEP key format."; return 1
            fi
            echo "    wep_tx_keyidx=0" >> "$wpa_conf_temp" # Default WEP key index
        else # Assume PSK (WPA/WPA2/WPA3-SAE)
            echo "    psk=\"$wifi_password\"" >> "$wpa_conf_temp"
            # For WPA3-SAE, you might need: key_mgmt=SAE or WPA-PSK SAE
            # if [[ "$security_type_from_scan" == "WPA3" ]]; then echo "    key_mgmt=SAE" >> "$wpa_conf_temp"; fi
        fi
        echo "}" >> "$wpa_conf_temp"
        chmod 600 "$wpa_conf_temp" # wpa_supplicant requires restricted permissions
        debug_full "wpa_supplicant config file $wpa_conf_temp content:\n$(cat "$wpa_conf_temp")"

        # Start wpa_supplicant in background
        # -Dnl80211,wext are common drivers, nl80211 is preferred
        if ! debug_exec "wpa_supplicant -B -i \"$iface\" -c \"$wpa_conf_temp\" -Dnl80211,wext"; then
            error_log "Failed to start wpa_supplicant for $iface."; return 1
        fi
        log_info_transient "wpa_supplicant started. Waiting for association with $selected_ssid..."
        connect_tries=20 # Wait up to 20 seconds for association
        while [ $connect_tries -gt 0 ]; do
            if wpa_cli -i "$iface" status 2>/dev/null | grep -q "wpa_state=COMPLETED"; then
                log_info_transient "Associated with $selected_ssid via wpa_supplicant."; break
            fi
            sleep 1; connect_tries=$((connect_tries - 1))
            debug_verbose "wpa_supplicant association tries left for $selected_ssid: $connect_tries"
        done
        if [ $connect_tries -eq 0 ]; then
            error_log "Failed to associate with $selected_ssid via wpa_supplicant (timeout)."
            log_error "wpa_supplicant association timed out for '$selected_ssid'."
            # Kill the lingering wpa_supplicant process
            pgrep -af "wpa_supplicant -B -i $iface -c $wpa_conf_temp" | awk '{print $1}' | xargs -r kill -9 >/dev/null 2>&1 || true
            return 1
        fi
    fi 

    # If not using NetworkManager (which handles DHCP itself), run dhclient
    if ! $NM_IS_ACTIVE; then
        log_info_transient "Wi-Fi associated ($selected_ssid). Attempting DHCP on $iface..."
        debug_exec "dhclient -r \"$iface\"" >/dev/null 2>&1 || true # Release old lease
        
        local dhclient_wifi_log
        dhclient_wifi_log=$(create_temp_file "dhclient_wifi_${iface}" "log")
        [ $? -ne 0 ] && { error_log "Failed to create dhclient log file."; dhclient_wifi_log="/dev/null"; }

        if debug_exec "timeout 30 dhclient -v \"$iface\"" >"$dhclient_wifi_log" 2>&1; then
            log_info_transient "dhclient successfully obtained lease on $iface for $selected_ssid."
            debug_full "dhclient log for $iface (Wi-Fi):\n$(cat "$dhclient_wifi_log")"; sleep 2; return 0
        else 
            warning_log "dhclient failed or timed out for '$selected_ssid' on $iface. Log: $dhclient_wifi_log"
            debug_full "dhclient log for $iface (Wi-Fi) on failure:\n$(cat "$dhclient_wifi_log")"
            
            # Offer static IP configuration if DHCP fails
            dialog --title "Wi-Fi IP Configuration: $selected_ssid" \
                   --yesno "DHCP failed for '$selected_ssid' on $iface.\\nDo you want to configure a static IP for this Wi-Fi connection?" \
                   ${DIALOG_DEFAULT_HEIGHT} ${DIALOG_DEFAULT_WIDTH} 2>/dev/tty
            choice=$?
            if [ $choice -eq $DIALOG_SUCCESS_CODE ]; then
                static_config_str=$(prompt_static_config "Wi-Fi ($selected_ssid)")
                exit_status=$?
                [ $exit_status -ne 0 ] && return 1 # User cancelled static config

                IFS=':' read -r static_ip_cidr gw dns_val <<< "$static_config_str"
                log_info_transient "Configuring static IP for Wi-Fi $iface ($selected_ssid): IP=$static_ip_cidr, GW=$gw, DNS=${dns_val:-Not set}"
                
                debug_exec "ip addr flush dev \"$iface\"" || true
                if ! debug_exec "ip link set \"$iface\" up"; then log_warning "Failed to bring $iface up for static Wi-Fi."; return 1; fi
                if debug_exec "ip addr add \"$static_ip_cidr\" dev \"$iface\""; then
                    sleep 2 
                    debug_exec "ip route del default dev \"$iface\"" 2>/dev/null || true
                    if debug_exec "ip route add default via \"$gw\" dev \"$iface\""; then
                        log_info_transient "iproute2 configured static IP for Wi-Fi $iface ($selected_ssid)."
                        if [ -n "$dns_val" ]; then
                            resolv_conf_content_wifi=""
                            IFS=',' read -ra dns_array_wifi <<< "$dns_val"
                            for dns_entry in "${dns_array_wifi[@]}"; do 
                                dns_entry_trimmed=$(echo "$dns_entry" | awk '{$1=$1};1')
                                resolv_conf_content_wifi+="nameserver $dns_entry_trimmed\n"
                            done
                            if [ -L /etc/resolv.conf ] && ! command -v resolvconf >/dev/null 2>&1 && ! command -v systemd-resolve >/dev/null 2>&1; then
                                 warning_log "/etc/resolv.conf is a symlink. Overwriting for DNS may be temporary."
                                 log_warning "/etc/resolv.conf is a symlink. DNS set via script might be overridden."
                            fi
                            echo -e "$resolv_conf_content_wifi" > /etc/resolv.conf
                            info_log "Configured DNS servers for Wi-Fi $iface in /etc/resolv.conf: $dns_val"
                        fi
                        return 0
                    else error_log "Failed to add default route for static Wi-Fi on $iface."; return 1; fi
                else error_log "Failed to add IP address for static Wi-Fi on $iface."; return 1; fi
            else 
                log_info_persistent "Static IP configuration for Wi-Fi '$selected_ssid' skipped by user."; return 1;
            fi 
        fi 
    fi 
    debug_basic "Wi-Fi connection attempt for '$selected_ssid' on $iface concluded."; return 1 # Fallthrough if NM handled DHCP or other cases
}

handle_wifi_connection() {
    local select_exit_status rfkill_idx rfkill_output
    debug_basic "Handling Wi-Fi connection. Detected interfaces: ${#WIFI_IFACES[@]}"
    if [ ${#WIFI_IFACES[@]} -eq 0 ]; then
        log_warning "No Wi-Fi interfaces detected. Skipping Wi-Fi setup."; return 1
    fi

    SELECTED_WIFI_IFACE=$(prompt_select_interface "Wi-Fi" "${WIFI_IFACES[@]}")
    select_exit_status=$?
    debug_basic "Wi-Fi interface selection: exit_status=$select_exit_status, SELECTED_WIFI_IFACE='$SELECTED_WIFI_IFACE'"
    [ $select_exit_status -ne 0 ] && return 1
    [ -z "$SELECTED_WIFI_IFACE" ] && { log_warning "No Wi-Fi interface was actually selected."; return 1; }

    # Check rfkill status
    if check_command rfkill; then
        # Get rfkill output: ID DEVICE TYPE SOFT HARD
        rfkill_output=$(debug_exec "rfkill list wifi -n -o ID,DEVICE,SOFT,HARD")
        # Find the ID for the selected interface
        rfkill_idx=$(echo "$rfkill_output" | grep -w "$SELECTED_WIFI_IFACE" | awk '{print $1}' || true)
        debug_verbose "rfkill_idx for $SELECTED_WIFI_IFACE: '$rfkill_idx'"

        if [ -n "$rfkill_idx" ]; then 
            # Check soft block: field 3 (SOFT) for the given ID
            if echo "$rfkill_output" | awk -v id="$rfkill_idx" '$1 == id && $3 == "blocked" {print "softblocked"}' | grep -q "softblocked"; then 
                dialog --title "Wi-Fi Soft Blocked" \
                       --yesno "$SELECTED_WIFI_IFACE (rfkill ID $rfkill_idx) is soft-blocked. Attempt to unblock?" \
                       10 ${DIALOG_DEFAULT_WIDTH} 2>/dev/tty
                if [ $? -eq $DIALOG_SUCCESS_CODE ]; then
                    if debug_exec "rfkill unblock $rfkill_idx"; then
                        log_info_persistent "$SELECTED_WIFI_IFACE (ID $rfkill_idx) unblocked."; sleep 1
                    else log_warning "Failed to unblock $SELECTED_WIFI_IFACE (ID $rfkill_idx)."; fi
                fi
            fi
            # Check hard block: field 4 (HARD) for the given ID
            if echo "$rfkill_output" | awk -v id="$rfkill_idx" '$1 == id && $4 == "blocked" {print "hardblocked"}' | grep -q "hardblocked" ; then 
                error_log "$SELECTED_WIFI_IFACE (ID $rfkill_idx) is hard-blocked (hardware switch)."
                log_error "$SELECTED_WIFI_IFACE (ID $rfkill_idx) is hard-blocked by a physical switch. Cannot proceed with this interface."; return 1
            fi
        fi
    fi

    if connect_wifi "$SELECTED_WIFI_IFACE"; then return 0; fi 
    
    log_warning "Wi-Fi connection on $SELECTED_WIFI_IFACE failed or was cancelled."; return 1
}

# --- Main Script Logic ---
main() {
    # Handle --debug argument first
    if [[ "$1" == "--debug" ]]; then
        DBG=true
        DEBUG_LEVEL=3 
        DEBUG_LOG_FILE="/tmp/universal_net_connect_$(date +%Y%m%d_%H%M%S)_$$.log"
        # Initialize xtrace logging to file descriptor $XTRACE_FD
        # This must be done before `set -x`
        # Ensure the FD is available and not used by dialog's redirections later
        # Using a temporary file for xtrace and then appending to main log might be safer
        # For now, direct redirection. Ensure $XTRACE_FD is high enough (e.g., 6, 7, 8, 9).
        eval "exec $XTRACE_FD>>\"\$DEBUG_LOG_FILE\""
        export BASH_XTRACEFD="$XTRACE_FD" # Tell Bash to use this FD for xtrace
        set -x # Start xtrace
        info_log "Debug mode activated. Log file: $DEBUG_LOG_FILE. DEBUG_LEVEL=$DEBUG_LEVEL. Xtrace on FD $XTRACE_FD."
        shift # Consume the --debug argument
    elif [ -n "$DEBUG_LOG_FILE_ENV" ]; then # Allow setting log file via environment
        DEBUG_LOG_FILE="$DEBUG_LOG_FILE_ENV"; DBG=true 
        info_log "Logging to ENV specified file: $DEBUG_LOG_FILE. DEBUG_LEVEL=$DEBUG_LEVEL."
    fi

    info_log "Universal Network Connectivity Script v3.1 started. UID: $(id -u)"
    if [ "$(id -u)" -ne 0 ]; then
        error_log "Script not run as root."
        # Avoid dialog here as it might not be installed yet
        echo "This script must be run as root. Please use 'sudo $0'" >&2; exit 1
    fi
    debug_basic "Running as root."

    # Install dialog first as it's crucial for user interaction
    install_packages "dialog,dialog" 
    # Then other packages
    install_packages "ip,iproute2" "ping,iputils-ping" "nmcli,network-manager" \
                     "wpa_cli,wpasupplicant" "wpa_supplicant,wpasupplicant" \
                     "dhclient,isc-dhcp-client" "iw,iw" "iwlist,wireless-tools" \
                     "rfkill,rfkill" "timeout,coreutils" "awk,gawk" 

    detect_ethernet_interfaces
    detect_wifi_interfaces
    check_network_manager_active 

    if check_internet_connectivity; then
        info_log "Internet connection already active. Exiting."; exit 0 
    fi
    log_info_persistent "No active internet connection detected. Starting configuration process..."

    local options=() main_choice main_dialog_exit_status
    while true; do
        options=() 
        [ ${#ETH_IFACES[@]} -gt 0 ] && options+=("ETH" "Configure Ethernet Connection")
        [ ${#WIFI_IFACES[@]} -gt 0 ] && options+=("WIFI" "Configure Wi-Fi Connection")
        
        if [ $((${#ETH_IFACES[@]} + ${#WIFI_IFACES[@]})) -eq 0 ]; then
            log_error "No usable network interfaces (Ethernet or Wi-Fi) were detected. Cannot proceed."; exit 1
        fi
        
        options+=("CHECK" "Re-check Internet Connectivity")
        debug_verbose "Main menu options: ${options[*]}"

        exec 3>&1
        main_choice=$(dialog --title "Main Menu - Universal Network Connector" \
            --cancel-label "Exit Script" \
            --menu "Select an action:" ${DIALOG_DEFAULT_HEIGHT} ${DIALOG_DEFAULT_WIDTH} $((${#options[@]}/2)) \
            "${options[@]}" 2>&1 1>&3)
        main_dialog_exit_status=$?
        exec 3>&-
        debug_basic "Main menu dialog: exit_status=$main_dialog_exit_status, choice_tag='$main_choice'"
        
        if [ $main_dialog_exit_status -ne $DIALOG_SUCCESS_CODE ]; then 
            log_info_persistent "Exiting script as per user request from main menu."; break 
        fi
        [ -z "$main_choice" ] && { log_warning "No option selected from main menu. Please try again."; continue; }

        case "$main_choice" in
            ETH)
                if [ ${#ETH_IFACES[@]} -eq 0 ]; then log_warning "No Ethernet interfaces available."; continue; fi
                if handle_ethernet_connection; then 
                    if check_internet_connectivity; then exit 0; fi 
                else log_info_persistent "Ethernet configuration did not result in a connection or was cancelled."; fi
                ;;
            WIFI)
                if [ ${#WIFI_IFACES[@]} -eq 0 ]; then log_warning "No Wi-Fi interfaces available."; continue; fi
                if handle_wifi_connection; then 
                    if check_internet_connectivity; then exit 0; fi
                else log_info_persistent "Wi-Fi configuration did not result in a connection or was cancelled."; fi
                ;;
            CHECK) if check_internet_connectivity; then exit 0; fi ;;
            *) log_warning "Invalid choice '$main_choice' from main menu. This should not happen." ;;
        esac
    done
    info_log "Exited main loop. Script finished."
    exit 1 # Exit with 1 if loop is broken without successful connection
}

# Pass all script arguments to main
main "$@"
{% endcodeblock %}
