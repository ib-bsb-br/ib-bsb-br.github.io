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
# Universal Network Connectivity Script for RK3588 (Debian Bullseye)
# Version 8.1 - Refined Integration and Robustness
#
# Changelog from v8.0:
# - Refined debug_exec temp file handling (local management).
# - Enhanced cleanup function to handle temporary NetworkManager connections.
# - Improved nmcli scan parsing in scan_wifi_networks for better robustness.
# - Minor improvements to wpa_supplicant PID file usage.
# - Updated documentation.
#
# Features:
# - Interactive TUI using 'dialog' for easier configuration
# - Automatic network configuration via Ethernet or Wi-Fi
# - Support for WPA/WPA2/WPA3, WEP, and open networks
# - Hidden SSID support
# - IPv4 and IPv6 configuration
# - Multiple DHCP client support (dhclient, dhcpcd, udhcpc)
# - Multiple Network Management tool support (NetworkManager, wpa_supplicant, iwd)
# - Connection profile management (passwords base64 encoded)
# - Comprehensive error handling, logging, and recovery (e.g., Wi-Fi driver reload)
# - Progress indicators and colored console output
# - Optional package dependency checking and installation
# - Non-interactive mode for automated setups
#
# Requirements:
# - Root privileges
# - 'dialog' utility for interactive mode (will offer to install)
# - Basic utilities: ip, ping, awk, grep, sed, systemctl, mktemp, base64, pkill
# - At least one of: NetworkManager, wpa_supplicant, iwd
# - At least one of: dhclient, dhcpcd, udhcpc
#

# Strict mode
set -euo pipefail
IFS=$'\n\t'

# --- Constants and Configuration ---
readonly SCRIPT_VERSION="8.1"
readonly SCRIPT_NAME="$(basename "$0")"
readonly CONFIG_DIR="/etc/netconnect"
readonly PROFILE_DIR="${CONFIG_DIR}/profiles"
readonly LOG_DIR="/var/log/netconnect"
readonly MAIN_LOG_FILE="${LOG_DIR}/netconnect.log"
readonly LOCK_FILE="/var/run/netconnect.lock"

# Network testing parameters
readonly PING_IP_PRIMARY="8.8.8.8"
readonly PING_IP_SECONDARY="1.1.1.1"
readonly PING_HOSTNAME="google.com"
readonly PING_COUNT=3
readonly PING_TIMEOUT=2 # seconds
readonly DHCP_TIMEOUT=30 # seconds
readonly WIFI_SCAN_TIMEOUT=10 # seconds for wpa_cli scan, nmcli/iw might be faster
readonly WIFI_CONNECT_TIMEOUT=30 # seconds

# Dialog UI settings
DIALOG_CMD="dialog"
DIALOG_AVAILABLE=false
DIALOG_SUCCESS_CODE=0
DIALOG_CANCEL_CODE=1
DIALOG_HELP_CODE=2
DIALOG_EXTRA_CODE=3
DIALOG_ESC_CODE=255
DIALOG_DEFAULT_HEIGHT=15
DIALOG_DEFAULT_WIDTH=70
DIALOG_INPUT_WIDTH=50

# Color codes (disabled if not in terminal or if NON_INTERACTIVE)
if [[ -t 1 && -t 2 ]]; then
    readonly COLOR_RED='\033[0;31m'
    readonly COLOR_GREEN='\033[0;32m'
    readonly COLOR_YELLOW='\033[0;33m'
    readonly COLOR_BLUE='\033[0;34m'
    readonly COLOR_PURPLE='\033[0;35m'
    readonly COLOR_CYAN='\033[0;36m'
    readonly COLOR_RESET='\033[0m'
else
    readonly COLOR_RED=''
    readonly COLOR_GREEN=''
    readonly COLOR_YELLOW=''
    readonly COLOR_BLUE=''
    readonly COLOR_PURPLE=''
    readonly COLOR_CYAN=''
    readonly COLOR_RESET=''
fi

# --- Global Variables ---
declare -a ETH_IFACES=()
declare -a WIFI_IFACES=()
declare -a TMP_FILES_TO_CLEAN=() # For files/items needing cleanup at script exit
declare SELECTED_IFACE=""
declare NM_AVAILABLE=false
declare WPA_CLI_AVAILABLE=false
declare IWD_AVAILABLE=false
declare WPA_SUPPLICANT_SERVICE_ACTIVE=false
declare DHCP_CLIENT=""

DBG=${DBG:-false}
DEBUG_LEVEL=${DEBUG_LEVEL:-1} # 1:basic, 2:verbose, 3:full
DEBUG_LOG_FILE=""
VERBOSE_COMMANDS=${VERBOSE_COMMANDS:-true}
XTRACE_FD=6

NON_INTERACTIVE=false
CONNECTION_TYPE_ARG=""
CHECK_ONLY_ARG=false

# --- Prerequisite Check & Installation ---
check_command() {
    local cmd_to_check="$1"
    if command -v "$cmd_to_check" >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

install_packages_dialog() {
    local missing_packages_to_install=("$@")
    local choice

    if [[ ${#missing_packages_to_install[@]} -eq 0 ]]; then
        return 0 # Nothing to install
    fi

    warning_log "Missing packages: ${missing_packages_to_install[*]}"
    if [[ "$NON_INTERACTIVE" == "false" ]]; then
        local install_prompt_msg="The following essential packages are missing: ${missing_packages_to_install[*]}.\n\nDo you want to try and install them now?\n(Requires an existing temporary internet connection or cached packages)"
        if $DIALOG_AVAILABLE ; then
            "$DIALOG_CMD" --title "Missing Packages" \
                   --yesno "$install_prompt_msg" \
                   12 ${DIALOG_DEFAULT_WIDTH} 2>/dev/tty
            choice=$?
        else # Fallback for when dialog itself might be missing
            read -r -p "$(echo -e "${COLOR_YELLOW}$install_prompt_msg (y/N): ${COLOR_RESET}")" response
            [[ "$response" =~ ^[yY]$ ]] && choice=0 || choice=1
        fi
    else
        info_log "Non-interactive mode: Attempting to install missing packages automatically."
        choice=0 # Auto-yes in non-interactive
    fi

    if [[ $choice -eq $DIALOG_SUCCESS_CODE ]]; then
        info_log "User opted to install missing packages: ${missing_packages_to_install[*]}"
        _show_progress_message "Attempting to install: ${missing_packages_to_install[*]}..." "transient"
        
        # Temporarily allow script to continue if apt-get update fails, but warn
        set +e
        apt-get update -qq
        local apt_update_ec=$?
        set -e
        if [[ $apt_update_ec -ne 0 ]]; then
             error_log "'apt-get update' failed (EC: $apt_update_ec). Package installation might fail."
             _show_progress_message "'apt-get update' failed. Please check your network connection and apt sources." "error"
             # Continue to try install, it might work with cached lists
        fi
        
        # shellcheck disable=SC2068 # We want word splitting for the array
        if apt-get install -y ${missing_packages_to_install[@]}; then
            _show_progress_message "Successfully installed missing packages." "persistent"
            # Re-check for dialog if it was installed
            if [[ " ${missing_packages_to_install[*]} " =~ " dialog " ]] && check_command dialog; then
                DIALOG_AVAILABLE=true
            fi
            return 0
        else
            error_log "Failed to install packages: ${missing_packages_to_install[*]}."
            _show_progress_message "Failed to install some packages. Please install them manually and re-run the script.\nPackages: ${missing_packages_to_install[*]}" "error"
            return 1
        fi
    else
        error_log "User declined package installation or cancelled."
        _show_progress_message "Cannot proceed without essential packages: ${missing_packages_to_install[*]}. Exiting." "error"
        return 1
    fi
}

# --- Logging Functions ---
_log_to_file() {
    if $DBG && [[ -n "$DEBUG_LOG_FILE" ]] && [[ -w "$DEBUG_LOG_FILE" || -w "$(dirname "$DEBUG_LOG_FILE")" ]]; then
        echo -e "$1" >> "$DEBUG_LOG_FILE"
    fi
}

_base_log() {
    local level="$1"
    local color="$2"
    shift 2
    local message="$*"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local log_entry="[$timestamp] [$level] $message"

    _log_to_file "$log_entry"

    if [[ "$level" != "DEBUG" && "$level" != "VERB" && "$level" != "FULL" ]] || $DBG; then
        if [[ "$level" == "DEBUG" && "$DEBUG_LEVEL" -lt 1 ]]; then return; fi
        if [[ "$level" == "VERB" && "$DEBUG_LEVEL" -lt 2 ]]; then return; fi
        if [[ "$level" == "FULL" && "$DEBUG_LEVEL" -lt 3 ]]; then return; fi
        
        if [[ "$NON_INTERACTIVE" == "true" ]] || ! $DIALOG_AVAILABLE || [[ "$level" == "DEBUG" || "$level" == "VERB" || "$level" == "FULL" ]]; then
             echo -e "${color}[$level]${COLOR_RESET} $message" >&2
        fi
    fi
}

debug_log()   { if $DBG && [[ "$DEBUG_LEVEL" -ge 1 ]]; then local caller_info="${BASH_SOURCE[1]##*/}:${FUNCNAME[1]}:${BASH_LINENO[0]}"; _base_log "DEBUG" "$COLOR_BLUE" "[$caller_info] $*"; fi; }
debug_verbose() { if $DBG && [[ "$DEBUG_LEVEL" -ge 2 ]]; then local caller_info="${BASH_SOURCE[1]##*/}:${FUNCNAME[1]}:${BASH_LINENO[0]}"; _base_log "VERB" "$COLOR_CYAN" "[$caller_info] $*"; fi; }
debug_full()    { if $DBG && [[ "$DEBUG_LEVEL" -ge 3 ]]; then local caller_info="${BASH_SOURCE[1]##*/}:${FUNCNAME[1]}:${BASH_LINENO[0]}"; _base_log "FULL" "$COLOR_PURPLE" "[$caller_info] $*"; fi; }
info_log()    { _base_log "INFO" "$COLOR_GREEN" "$@"; }
warning_log() { local caller_info="${BASH_SOURCE[1]##*/}:${FUNCNAME[1]}:${BASH_LINENO[0]}"; _base_log "WARN" "$COLOR_YELLOW" "[$caller_info] $*"; }
error_log()   { local caller_info="${BASH_SOURCE[1]##*/}:${FUNCNAME[1]}:${BASH_LINENO[0]}"; _base_log "ERROR" "$COLOR_RED" "[$caller_info] $*"; }

debug_var() {
    if ! $DBG || [[ "$DEBUG_LEVEL" -lt 2 ]]; then return 0; fi
    local var_name="$1"
    local var_value
    var_value="${!var_name}" # Indirect expansion
    debug_verbose "Variable $var_name = '$var_value' (length: ${#var_value})"
    if [[ "$var_value" =~ [[:cntrl:]] ]]; then # Check for control characters
        debug_log "WARNING: Variable $var_name contains control characters."
        debug_full "Hex dump for $var_name:\n$(echo -n "$var_value" | hexdump -C)"
    fi
}

# --- UI and Progress Functions ---
_show_dialog_message() {
    local type="$1" title="$2" message="$3"
    local height=${4:-8} width=${5:-60}
    local dialog_exit_code=$DIALOG_CANCEL_CODE

    debug_verbose "Showing dialog: type=$type, title='$title', message snippet='${message:0:50}...'"
    if $DIALOG_AVAILABLE && [[ "$NON_INTERACTIVE" == "false" ]]; then
        "$DIALOG_CMD" --cr-wrap --title "$title" --"$type" "$message" "$height" "$width" 2>/dev/tty
        dialog_exit_code=$?
        # Some dialog versions might not clear screen fully on exit
        # clear # Uncomment if needed, but can be disruptive
    else
        echo -e "${COLOR_GREEN}$title:${COLOR_RESET}\n$message" >&2
        if [[ "$type" == "msgbox" || "$type" == "infobox" ]]; then
            dialog_exit_code=$DIALOG_SUCCESS_CODE
        elif [[ "$type" == "yesno" ]]; then
             read -r -p "$(echo -e "${COLOR_YELLOW}$message (y/N): ${COLOR_RESET}")" response
             [[ "$response" =~ ^[yY]$ ]] && dialog_exit_code=$DIALOG_SUCCESS_CODE || dialog_exit_code=$DIALOG_CANCEL_CODE
        fi
    fi
    debug_verbose "Dialog ('$title') exit code: $dialog_exit_code"
    return $dialog_exit_code
}

_show_progress_message() {
    local message="$1"
    local type="${2:-info}" # info, persistent, error, transient
    
    info_log "$message" # Always log it

    if [[ "$NON_INTERACTIVE" == "true" ]]; then return; fi

    case "$type" in
        persistent) _show_dialog_message "msgbox" "Information" "$message" ;;
        error) _show_dialog_message "msgbox" "Error" "$message" 10 70 ;; # Slightly larger for errors
        transient) 
            if $DIALOG_AVAILABLE; then
                "$DIALOG_CMD" --cr-wrap --title "Information" --infobox "$message" 6 60 2>/dev/tty || true
                sleep 1
            else
                echo -e "${COLOR_GREEN}INFO:${COLOR_RESET} $message" >&2; sleep 1;
            fi ;;
        *) _show_dialog_message "msgbox" "Information" "$message" ;;
    esac
}

show_progress_spinner() {
    local message="$1"
    local duration_s="${2:-0}"

    if [[ "$NON_INTERACTIVE" == "true" ]] || ! $DIALOG_AVAILABLE; then
        echo -n -e "${COLOR_GREEN}$message${COLOR_RESET}" >&2
        if [[ "$duration_s" -gt 0 ]]; then
            local sleep_interval=0.2 spin_chars="/-\\|"
            local num_steps=$(( (duration_s * 1000) / (sleep_interval * 1000) )) # Integer arithmetic
            for ((i=0; i<num_steps; i++)); do
                echo -n -e " ${spin_chars:i%${#spin_chars}:1}" >&2; sleep "$sleep_interval"; echo -n -e "\b\b" >&2;
            done
            echo -e "  done." >&2
        else echo -e " done." >&2; fi
        return
    fi

    if [[ "$duration_s" -gt 0 ]]; then
        ( local percentage_per_step=$(( 100 / duration_s ));
          for ((i=0; i<=duration_s; i++)); do echo "$(( i * percentage_per_step ))"; sleep 1; done; echo 100;
        ) | "$DIALOG_CMD" --cr-wrap --title "Progress" --gauge "$message" 8 70 0 2>/dev/tty
    else _show_progress_message "$message ...done." "transient"; fi
}

# --- Utility Functions ---
debug_exec() {
    local cmd_string="$*"
    debug_verbose "Executing: $cmd_string"
    local output exit_code
    local tmp_stdout_de tmp_stderr_de # Specific temp files for this function instance

    # Create temp files locally, do not add to global cleanup array
    tmp_stdout_de=$(mktemp "/tmp/netconnect_cmd_stdout.XXXXXX")
    if [[ $? -ne 0 || -z "$tmp_stdout_de" ]]; then error_log "debug_exec: Failed to create stdout temp file"; return 1; fi
    tmp_stderr_de=$(mktemp "/tmp/netconnect_cmd_stderr.XXXXXX")
    if [[ $? -ne 0 || -z "$tmp_stderr_de" ]]; then 
        error_log "debug_exec: Failed to create stderr temp file"; 
        rm -f "$tmp_stdout_de" 2>/dev/null; # Clean up first temp file
        return 1; 
    fi

    # Execute command
    eval "$cmd_string" > "$tmp_stdout_de" 2> "$tmp_stderr_de"
    exit_code=$?
    
    local stdout_content stderr_content
    stdout_content=$(cat "$tmp_stdout_de")
    stderr_content=$(cat "$tmp_stderr_de")

    debug_verbose "Exit code: $exit_code"
    [[ -n "$stdout_content" ]] && debug_full "STDOUT:\n$stdout_content"
    [[ -n "$stderr_content" ]] && debug_full "STDERR:\n$stderr_content"
    
    if [[ $exit_code -ne 0 ]]; then
        debug_log "FAILED command: $cmd_string (Exit Code: $exit_code)"
        [[ -n "$stderr_content" ]] && debug_log "Stderr from failed command was logged in FULL debug."
    fi
    
    # Output the actual stdout of the command for capture by caller
    echo "$stdout_content"
    
    # Cleanup these specific temp files
    rm -f "$tmp_stdout_de" "$tmp_stderr_de" 2>/dev/null || warning_log "debug_exec: Failed to clean up its local temp files."

    return $exit_code
}

create_temp_file() {
    local prefix="${1:-netconnect}" suffix_val="${2:-}"
    local temp_file sane_prefix sane_suffix

    sane_prefix=$(echo "$prefix" | tr -cd '[:alnum:]_-')
    sane_suffix=$(echo "$suffix_val" | tr -cs '[:alnum:]_.-' '_')
    [[ -n "$sane_suffix" && ! "$sane_suffix" =~ ^\. ]] && sane_suffix=".$sane_suffix"

    temp_file=$(mktemp "/tmp/${sane_prefix}.XXXXXX${sane_suffix}")
    if [[ $? -ne 0 || -z "$temp_file" || ! -e "$temp_file" ]]; then
        error_log "Failed to create temporary file (prefix '$sane_prefix', suffix '$sane_suffix')"
        return 1
    fi
    debug_verbose "Created global temporary file: '$temp_file'"
    TMP_FILES_TO_CLEAN+=("$temp_file")
    echo "$temp_file"
    return 0
}

safe_rm() {
    local file_to_remove="$1"
    debug_verbose "safe_rm: Attempting to remove '$file_to_remove'"
    if [[ -z "$file_to_remove" ]]; then warning_log "safe_rm: Empty filename provided."; return 1; fi
    if [[ ! -e "$file_to_remove" ]]; then debug_verbose "safe_rm: File '$file_to_remove' does not exist, skipping."; return 0; fi
    
    local critical_paths=("/" "/bin" "/etc" "/usr" "/var" "/tmp" "/sbin" "/lib" "/boot" "/home" "/root")
    for crit_path in "${critical_paths[@]}"; do
        if [[ "$file_to_remove" == "$crit_path" ]]; then
            error_log "safe_rm: Critical path removal protection for '$file_to_remove'!"
            return 1
        fi
    done
    if [[ "$file_to_remove" =~ (/|([[:alnum:]_-]+)/)\.\. ]]; then # Basic path traversal check
        error_log "safe_rm: Path traversal attempt suspected in '$file_to_remove'!"
        return 1
    fi

    if rm -f "$file_to_remove"; then
        debug_verbose "safe_rm: Successfully removed '$file_to_remove'"
        for i in "${!TMP_FILES_TO_CLEAN[@]}"; do
            if [[ "${TMP_FILES_TO_CLEAN[i]}" == "$file_to_remove" ]]; then
                unset 'TMP_FILES_TO_CLEAN[i]'; break;
            fi
        done
        return 0
    else
        error_log "safe_rm: Failed to remove '$file_to_remove' (Error: $?)"; return 1;
    fi
}

cleanup() {
    local exit_code=$?
    debug_log "Cleanup: Script exiting with code $exit_code"
    local item_processed_flags=() # To avoid processing an item multiple times if it appears due to error

    # Process special cleanup items first (like nmcli connections)
    local remaining_items=()
    for item_idx in "${!TMP_FILES_TO_CLEAN[@]}"; do
        local item="${TMP_FILES_TO_CLEAN[$item_idx]}"
        if [[ -z "$item" ]] || [[ " ${item_processed_flags[*]} " =~ " ${item_idx} " ]]; then continue; fi

        if [[ "$item" == nmcli_con_del_* ]]; then
            local con_name_to_del="${item#nmcli_con_del_}"
            if [[ -n "$con_name_to_del" ]] && $NM_AVAILABLE; then
                info_log "Cleaning up temporary NetworkManager connection: $con_name_to_del"
                nmcli connection delete id "$con_name_to_del" >/dev/null 2>&1 || \
                    warning_log "Failed to delete temporary NM connection '$con_name_to_del' during cleanup."
            fi
            item_processed_flags+=("$item_idx")
        else
            remaining_items+=("$item") # It's a file path for safe_rm
        fi
    done
    
    # Update TMP_FILES_TO_CLEAN with only file paths remaining
    TMP_FILES_TO_CLEAN=("${remaining_items[@]}")

    # Regular file cleanup
    if [[ ${#TMP_FILES_TO_CLEAN[@]} -gt 0 ]]; then
        debug_verbose "Cleaning up ${#TMP_FILES_TO_CLEAN[@]} temporary file(s): ${TMP_FILES_TO_CLEAN[*]}"
        for temp_file in "${TMP_FILES_TO_CLEAN[@]}"; do
            [[ -n "$temp_file" ]] && safe_rm "$temp_file"
        done
    else
        debug_verbose "No standard temporary files registered for cleanup."
    fi
    
    [[ -f "$LOCK_FILE" ]] && safe_rm "$LOCK_FILE"
    
    if [[ -t 1 ]]; then
      stty sane 2>/dev/null || debug_verbose "stty sane failed"
      tput cnorm 2>/dev/null || debug_verbose "tput cnorm failed"
    fi
    
    if $DBG && [[ -n "$DEBUG_LOG_FILE" ]]; then
        set +x
        eval "exec $XTRACE_FD>&-" 2>/dev/null || debug_verbose "Failed to close XTRACE_FD $XTRACE_FD"
        info_log "Script exited (Code: $exit_code). Debug log: $DEBUG_LOG_FILE"
        [[ -t 2 ]] && echo -e "${COLOR_CYAN}Debug log available at: $DEBUG_LOG_FILE${COLOR_RESET}" >&2
    else
        info_log "Script exited (Code: $exit_code)."
    fi
    exit "$exit_code"
}
trap cleanup EXIT
# SIGINT/SIGTERM are more complex; a simple message is fine, cleanup will run on EXIT.
trap 'error_log "Script interrupted by SIGINT/SIGTERM."; exit 130' SIGINT SIGTERM


check_root() {
    if [[ $EUID -ne 0 ]]; then
        error_log "This script must be run as root"
        _show_progress_message "ERROR: This script must be run as root. Usage: sudo $SCRIPT_NAME [options]" "error"
        exit 1
    fi
}

acquire_lock() {
    if [[ -f "$LOCK_FILE" ]]; then
        local pid; pid=$(cat "$LOCK_FILE" 2>/dev/null)
        if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
            error_log "Another instance is already running (PID: $pid)"; exit 1;
        fi
        safe_rm "$LOCK_FILE" # Stale lock file
    fi
    echo $$ > "$LOCK_FILE" || { error_log "Failed to create lock file: $LOCK_FILE"; exit 1; }
}

init_directories() {
    local dirs=("$CONFIG_DIR" "$PROFILE_DIR" "$LOG_DIR")
    for dir in "${dirs[@]}"; do
        if [[ ! -d "$dir" ]]; then
            debug_log "Creating directory: $dir"
            mkdir -p "$dir" || warning_log "Could not create directory: $dir."
        fi
    done
    touch "$MAIN_LOG_FILE" 2>/dev/null || warning_log "Main log file $MAIN_LOG_FILE is not writable."
}

sanitize_iface_name() {
    local val="$1"; val=$(echo -n "$val" | tr -cd '[:alnum:]_-'); echo "$val"
}

sanitize_dialog_output() {
    local val="$1"; val=$(echo -n "$val" | tr -cd '[:print:]\n\r'); val=$(echo -n "$val" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'); echo "$val"
}

# --- User Interaction Functions (Dialog-based with fallbacks) ---
prompt_user_input() {
    local prompt_text="$1" default_value="${2:-}" is_password="${3:-false}"
    local input_value="" dialog_exit_status

    if $DIALOG_AVAILABLE && [[ "$NON_INTERACTIVE" == "false" ]]; then
        local dialog_option="--inputbox"; [[ "$is_password" == "true" ]] && dialog_option="--passwordbox"
        local temp_out; temp_out=$(create_temp_file "dialog_input") || return 1

        "$DIALOG_CMD" --cr-wrap --title "Input Required" "$dialog_option" "$prompt_text" \
            10 ${DIALOG_INPUT_WIDTH} "$default_value" 2> "$temp_out"
        dialog_exit_status=$?
        
        input_value=$(sanitize_dialog_output "$(cat "$temp_out")")
        safe_rm "$temp_out"

        if [[ $dialog_exit_status -ne $DIALOG_SUCCESS_CODE ]]; then
            info_log "User cancelled input for: $prompt_text"; return 1;
        fi
    else
        local read_options=""; [[ "$is_password" == "true" ]] && read_options="-s"
        local prompt_full="$prompt_text"; [[ -n "$default_value" ]] && prompt_full+=" [$default_value]"
        prompt_full+=": "
        
        read -r $read_options -p "$(echo -e "${COLOR_YELLOW}$prompt_full${COLOR_RESET}")" input_value
        [[ "$is_password" == "true" ]] && echo >&2
        [[ -z "$input_value" && -n "$default_value" ]] && input_value="$default_value"
    fi
    echo "$input_value"; return 0
}

prompt_yes_no() {
    local prompt_text="$1" default_choice="${2:-n}"
    local response_code=$DIALOG_CANCEL_CODE

    if $DIALOG_AVAILABLE && [[ "$NON_INTERACTIVE" == "false" ]]; then
        local default_opt=""; [[ "$default_choice" == "n" ]] && default_opt="--defaultno"
        "$DIALOG_CMD" --cr-wrap --title "Confirmation" --yesno "$prompt_text" 8 ${DIALOG_DEFAULT_WIDTH} ${default_opt} 2>/dev/tty
        response_code=$?
    else
        local yn_prompt="[y/N]"; [[ "$default_choice" == "y" ]] && yn_prompt="[Y/n]"
        read -r -p "$(echo -e "${COLOR_YELLOW}$prompt_text $yn_prompt: ${COLOR_RESET}")" response
        response="${response:-$default_choice}"
        [[ "$response" =~ ^[yY]$ ]] && response_code=$DIALOG_SUCCESS_CODE || response_code=$DIALOG_CANCEL_CODE
    fi
    [[ $response_code -eq $DIALOG_SUCCESS_CODE ]] && return 0 || return 1
}

prompt_select_option() {
    local prompt_text="$1"; shift
    local -a options_array=("$@") # Pairs: "tag1" "description1" ...
    local selected_tag="" dialog_exit_status

    if [[ $((${#options_array[@]} % 2)) -ne 0 || ${#options_array[@]} -eq 0 ]]; then
        error_log "prompt_select_option: Options array error."; return 1;
    fi
    if [[ ${#options_array[@]} -eq 2 && "$NON_INTERACTIVE" == "false" ]]; then
        info_log "Auto-selecting only option: ${options_array[1]}"; echo "${options_array[0]}"; return 0;
    fi

    if $DIALOG_AVAILABLE && [[ "$NON_INTERACTIVE" == "false" ]]; then
        local temp_out; temp_out=$(create_temp_file "dialog_menu") || return 1
        "$DIALOG_CMD" --cr-wrap --title "Select Option" --menu "$prompt_text" \
            ${DIALOG_DEFAULT_HEIGHT} ${DIALOG_DEFAULT_WIDTH} $((${#options_array[@]} / 2)) \
            "${options_array[@]}" 2> "$temp_out"
        dialog_exit_status=$?
        selected_tag=$(sanitize_dialog_output "$(cat "$temp_out")")
        safe_rm "$temp_out"
        if [[ $dialog_exit_status -ne $DIALOG_SUCCESS_CODE ]]; then info_log "User cancelled selection."; return 1; fi
    else
        echo -e "${COLOR_YELLOW}$prompt_text${COLOR_RESET}" >&2
        local display_options_tags=()
        for ((i=0; i < ${#options_array[@]}; i+=2)); do
            echo "  $((i/2 + 1)). ${options_array[i+1]} (${options_array[i]})" >&2
            display_options_tags+=("${options_array[i]}")
        done
        local choice_num
        while true; do
            read -r -p "$(echo -e "${COLOR_YELLOW}Enter choice (1-$((${#options_array[@]}/2))): ${COLOR_RESET}")" choice_num
            if [[ "$choice_num" =~ ^[0-9]+$ && "$choice_num" -ge 1 && "$choice_num" -le $((${#options_array[@]}/2)) ]]; then
                selected_tag="${display_options_tags[$((choice_num-1))]}"; break
            else echo -e "${COLOR_RED}Invalid choice.${COLOR_RESET}" >&2; fi
        done
    fi
    echo "$selected_tag"; return 0
}

# --- Network Detection Functions ---
# (detect_network_tools, detect_ethernet_interfaces, detect_wifi_interfaces from v8.0 are largely okay)
# Minor refinement to detect_wifi_interfaces to ensure unique entries robustly
detect_network_tools() {
    info_log "Detecting available network management tools..."
    NM_AVAILABLE=false; WPA_CLI_AVAILABLE=false; IWD_AVAILABLE=false; DHCP_CLIENT=""

    if check_command nmcli && systemctl is-active NetworkManager >/dev/null 2>&1; then
        NM_AVAILABLE=true; info_log "NetworkManager (nmcli) is available and active."
    else info_log "NetworkManager (nmcli) is not active or not found."; fi
    
    if check_command wpa_cli; then
        WPA_CLI_AVAILABLE=true; info_log "wpa_supplicant (wpa_cli command) is available."
    else info_log "wpa_supplicant (wpa_cli command) not found."; fi
    
    if check_command iwctl && systemctl is-active iwd >/dev/null 2>&1; then
        IWD_AVAILABLE=true; info_log "iwd (iwctl) is available and active."
    else info_log "iwd (iwctl) is not active or not found."; fi
    
    for client in dhclient dhcpcd udhcpc; do
        if check_command "$client"; then DHCP_CLIENT="$client"; info_log "DHCP client found: $client"; break; fi
    done
    if [[ -z "$DHCP_CLIENT" ]]; then warning_log "No DHCP client found. DHCP may fail."; fi
}

detect_ethernet_interfaces() {
    debug_log "Detecting Ethernet interfaces..."
    ETH_IFACES=()
    local detected_output
    detected_output=$(debug_exec "ip -o link show type ether 2>/dev/null | awk -F': ' '!/master|link\\/ether 00:00:00:00:00:00/{print \$2}' | awk '{print \$1}' | grep -Ev '^(lo|br|bond|dummy|veth|virbr|docker|tun|tap|vlan|vxlan|macvlan|macvtap|nlmon|gre|ipip|sit|ip6tnl|rename|wg)' || true")
    if [[ -n "$detected_output" ]]; then
        while IFS= read -r iface; do
            local iface_clean; iface_clean=$(sanitize_iface_name "$iface")
            if [[ -n "$iface_clean" && "$iface_clean" == "$iface" && -e "/sys/class/net/$iface_clean/device" && ! -e "/sys/class/net/$iface_clean/virtual" ]]; then
                ETH_IFACES+=("$iface_clean"); debug_verbose "Added Ethernet interface: '$iface_clean'"
            elif [[ -n "$iface" ]]; then warning_log "Skipped potentially invalid/virtual Ethernet interface: '$iface'"; fi
        done <<< "$detected_output"
    fi
    info_log "Ethernet interfaces found: ${ETH_IFACES[*]:-(None)}"
}

detect_wifi_interfaces() {
    debug_log "Detecting Wi-Fi interfaces..."
    WIFI_IFACES=()
    local detected_output="" unique_wifi_ifaces_map # Use map for uniqueness

    declare -A unique_wifi_ifaces_map # Associative array for unique interface names

    # Try 'iw dev' first
    if check_command iw; then
        debug_verbose "Attempting Wi-Fi detection with 'iw dev'"
        detected_output=$(debug_exec "iw dev 2>/dev/null | awk '\$1==\"Interface\"{print \$2}' || true")
        if [[ -n "$detected_output" ]]; then
            while IFS= read -r iface; do
                local iface_clean; iface_clean=$(sanitize_iface_name "$iface")
                if [[ -n "$iface_clean" && "$iface_clean" == "$iface" && -d "/sys/class/net/${iface_clean}/wireless" ]]; then
                    unique_wifi_ifaces_map["$iface_clean"]=1
                fi
            done <<< "$detected_output"
        fi
    fi
    
    # Fallback to 'ip link' if 'iw dev' found nothing or 'iw' not present
    if [[ ${#unique_wifi_ifaces_map[@]} -eq 0 ]] && check_command ip; then
        debug_verbose "Attempting Wi-Fi detection with 'ip link' (fallback)"
        detected_output=$(debug_exec "ip -o link show 2>/dev/null | awk -F': ' '/wlan|wifi|wlp/{gsub(/@.*/, \"\", \$2); print \$2}' | awk '{print \$1}' | grep -E '^(wlan|wlp|wifi)' || true")
         if [[ -n "$detected_output" ]]; then
            while IFS= read -r iface; do
                local iface_clean; iface_clean=$(sanitize_iface_name "$iface")
                if [[ -n "$iface_clean" && "$iface_clean" == "$iface" && -d "/sys/class/net/${iface_clean}/wireless" ]]; then
                     unique_wifi_ifaces_map["$iface_clean"]=1
                fi
            done <<< "$detected_output"
        fi
    fi
    
    # Populate WIFI_IFACES array from the unique map keys
    for iface_key in "${!unique_wifi_ifaces_map[@]}"; do
        WIFI_IFACES+=("$iface_key")
        debug_verbose "Added Wi-Fi interface: '$iface_key'"
    done
    info_log "Wi-Fi interfaces found: ${WIFI_IFACES[*]:-(None)}"
}


# --- Interface Management Functions ---
# (ensure_interface_up from v8.0 is largely okay, minor logging tweaks if needed)
ensure_interface_up() {
    local iface="$1" type="${2:-ethernet}" max_attempts=3 attempt=1
    debug_log "Ensuring interface $iface (type: $type) is up..."
    if [[ "$type" == "wifi" ]] && check_command rfkill; then
        if rfkill list wifi 2>/dev/null | grep -i "$iface" -A2 | grep -q "Hard blocked: yes"; then error_log "Wi-Fi $iface hard-blocked."; return 1; fi
        if rfkill list wifi 2>/dev/null | grep -i "$iface" -A2 | grep -q "Soft blocked: yes"; then info_log "Wi-Fi $iface soft-blocked. Unblocking..."; debug_exec "rfkill unblock wifi"; sleep 1; fi
    fi
    if $NM_AVAILABLE; then
        local nm_state; nm_state=$(nmcli -g GENERAL.STATE device show "$iface" 2>/dev/null || echo "unknown")
        if [[ "$nm_state" == *"unmanaged"* ]]; then debug_log "$iface unmanaged by NM. Setting managed..."; nmcli device set "$iface" managed yes 2>/dev/null || true; sleep 2; fi
    fi
    while [[ $attempt -le $max_attempts ]]; do
        debug_log "Bringing up $iface (attempt $attempt/$max_attempts)..."
        debug_exec "ip link set \"$iface\" down" 2>/dev/null || true; sleep 0.5
        if debug_exec "ip link set \"$iface\" up"; then
            local wait_time=0 max_wait=5 current_state
            while [[ $wait_time -lt $max_wait ]]; do
                current_state=$(ip link show "$iface" 2>/dev/null | grep -Po '(?<=state )\w+' || echo "UNKNOWN")
                debug_verbose "$iface state: $current_state (wait: $wait_time)"
                case "$current_state" in UP) debug_log "$iface is UP."; return 0 ;;
                    DORMANT) if [[ "$type" == "wifi" ]]; then debug_log "$iface DORMANT (OK for Wi-Fi)."; return 0; fi ;;
                    UNKNOWN) debug_log "$iface UNKNOWN (assuming OK)."; return 0 ;; esac
                sleep 1; ((wait_time++)); done
            debug_log "$iface up, but state $current_state after $max_wait s."; return 0;
        else warning_log "'ip link set $iface up' failed (attempt $attempt)."; fi
        if [[ "$type" == "wifi" && $attempt -gt 1 ]]; then
            local driver; driver=$(basename "$(readlink -f "/sys/class/net/$iface/device/driver" 2>/dev/null)" 2>/dev/null || echo "")
            if [[ -n "$driver" ]]; then _show_progress_message "Reloading Wi-Fi driver $driver for $iface..." "transient"; debug_exec "pkill -f \"wpa_supplicant.*$iface\"" || true;
                if debug_exec "modprobe -r $driver" 2>/dev/null; then sleep 2; if debug_exec "modprobe $driver"; then sleep 3; info_log "Driver $driver reloaded."; debug_exec "ip link set \"$iface\" up" || true; else warning_log "Failed to load $driver."; fi
                else warning_log "Failed to remove $driver."; fi
            else debug_log "No driver module found for $iface."; fi
        fi
        ((attempt++)); if [[ $attempt -le $max_attempts ]]; then sleep 2; fi; done
    error_log "Failed to bring up $iface after $max_attempts attempts."; return 1
}

# --- Ethernet Configuration Functions ---
# (configure_dhcp, configure_static_ip, configure_ethernet from v8.0 are largely okay, will benefit from debug_exec fix)
# Example: configure_dhcp (core logic unchanged, benefits from fixed debug_exec)
configure_dhcp() {
    local iface="${1}"
    info_log "Configuring DHCP on $iface..."
    ensure_interface_up "$iface" "ethernet" || return 1
    if $NM_AVAILABLE; then
        local nm_state=$(nmcli -g GENERAL.STATE device show "$iface" 2>/dev/null || echo "unknown")
        if [[ "$nm_state" != *"unmanaged"* ]]; then
            debug_log "Attempting DHCP with NetworkManager for $iface."
            local profile_name="netconnect-dhcp-$iface-$$"
            nmcli con delete id "$profile_name" >/dev/null 2>&1 || true # Clean previous temp
            if nmcli connection add type ethernet con-name "$profile_name" ifname "$iface" ipv4.method auto ipv6.method auto connection.autoconnect no >/dev/null 2>&1; then
                TMP_FILES_TO_CLEAN+=("nmcli_con_del_$profile_name")
                if nmcli connection up "$profile_name" >/dev/null 2>&1; then
                    show_progress_spinner "Obtaining IP via NetworkManager on $iface" 5 & local ppid=$!; disown $ppid 2>/dev/null; wait $ppid 2>/dev/null
                    sleep 2; if ip addr show dev "$iface" | grep -q "inet "; then info_log "DHCP OK via NM."; return 0;
                    else warning_log "NM connected but no IP."; nmcli connection delete id "$profile_name" >/dev/null 2>&1 || true; fi
                else warning_log "NM 'con up $profile_name' failed."; nmcli connection delete id "$profile_name" >/dev/null 2>&1 || true; fi
            else warning_log "NM 'con add' for DHCP failed."; fi
        else debug_log "NM reports $iface unmanaged, skipping NM for DHCP."; fi
    fi
    if [[ -z "$DHCP_CLIENT" ]]; then error_log "No DHCP client for $iface."; return 1; fi
    debug_log "Attempting DHCP with $DHCP_CLIENT for $iface"
    case "$DHCP_CLIENT" in dhclient) debug_exec "dhclient -r \"$iface\"" || true ;; dhcpcd) debug_exec "dhcpcd -k \"$iface\"" || true ;; esac; sleep 1
    local dhcp_cmd_success=false
    show_progress_spinner "Obtaining IP via $DHCP_CLIENT on $iface" "$DHCP_TIMEOUT" & local ppid2=$!; disown $ppid2 2>/dev/null
    case "$DHCP_CLIENT" in
        dhclient) timeout "$DHCP_TIMEOUT" dhclient -v "$iface" >/dev/null 2>&1 && dhcp_cmd_success=true ;;
        dhcpcd)   timeout "$DHCP_TIMEOUT" dhcpcd -w "$iface" >/dev/null 2>&1 && dhcp_cmd_success=true ;;
        udhcpc)   timeout "$DHCP_TIMEOUT" udhcpc -i "$iface" -q -f -n >/dev/null 2>&1 && dhcp_cmd_success=true ;;
    esac; wait $ppid2 2>/dev/null
    if $dhcp_cmd_success; then sleep 2; if ip addr show dev "$iface" | grep -q "inet "; then info_log "DHCP OK via $DHCP_CLIENT."; return 0;
        else error_log "$DHCP_CLIENT OK, but no IP on $iface."; return 1; fi
    else error_log "DHCP failed via $DHCP_CLIENT for $iface."; return 1; fi
}

configure_static_ip() {
    local iface="${1}"
    info_log "Configuring static IP on $iface..."
    local ip_addr_cidr gateway dns_servers
    if [[ "$NON_INTERACTIVE" == "true" ]]; then error_log "Static IP not supported in non-interactive mode here."; return 1; fi
    ip_addr_cidr=$(prompt_user_input "Enter IP address with CIDR (e.g., 192.168.1.100/24)") || return 1
    if [[ -z "$ip_addr_cidr" ]] || ! echo "$ip_addr_cidr" | grep -qE "^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2}$"; then error_log "Invalid IP/CIDR: $ip_addr_cidr"; return 1; fi
    gateway=$(prompt_user_input "Enter gateway IP (e.g., 192.168.1.1)") || return 1
    if [[ -z "$gateway" ]] || ! echo "$gateway" | grep -qE "^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$"; then error_log "Invalid Gateway: $gateway"; return 1; fi
    dns_servers=$(prompt_user_input "Enter DNS servers (comma-sep, optional)" "8.8.8.8,1.1.1.1") || dns_servers="8.8.8.8,1.1.1.1"
    ensure_interface_up "$iface" "ethernet" || return 1
    if $NM_AVAILABLE; then
        local nm_state=$(nmcli -g GENERAL.STATE device show "$iface" 2>/dev/null || echo "unknown")
        if [[ "$nm_state" != *"unmanaged"* ]]; then
            debug_log "Attempting static IP with NetworkManager for $iface."
            local profile_name="netconnect-static-$iface-$$"; nmcli con delete id "$profile_name" >/dev/null 2>&1 || true
            local nm_cmd_add=(nmcli con add type ethernet con-name "$profile_name" ifname "$iface" ipv4.method manual ipv4.addresses "$ip_addr_cidr" ipv4.gateway "$gateway")
            [[ -n "$dns_servers" ]] && nm_cmd_add+=(ipv4.dns "$dns_servers"); nm_cmd_add+=(ipv6.method auto connection.autoconnect no)
            if "${nm_cmd_add[@]}" >/dev/null 2>&1; then TMP_FILES_TO_CLEAN+=("nmcli_con_del_$profile_name");
                if nmcli con up "$profile_name" >/dev/null 2>&1; then info_log "Static IP OK via NM."; return 0;
                else warning_log "NM 'con up $profile_name' static failed."; nmcli con delete id "$profile_name" >/dev/null 2>&1 || true; fi
            else warning_log "NM 'con add' static failed."; fi
        else debug_log "NM reports $iface unmanaged, skipping NM for static IP."; fi
    fi
    debug_log "Configuring static IP manually for $iface using iproute2"
    debug_exec "ip addr flush dev \"$iface\"" || true; debug_exec "ip route flush dev \"$iface\"" || true
    if ! debug_exec "ip addr add \"$ip_addr_cidr\" dev \"$iface\""; then error_log "Failed to add IP $ip_addr_cidr to $iface"; return 1; fi
    debug_exec "ip route del default" 2>/dev/null || true 
    if ! debug_exec "ip route add default via \"$gateway\" dev \"$iface\""; then error_log "Failed to add default route via $gateway"; debug_exec "ip addr del \"$ip_addr_cidr\" dev \"$iface\"" || true; return 1; fi
    if [[ -n "$dns_servers" ]]; then if ! configure_dns "$dns_servers" "$iface"; then warning_log "Manual DNS config failed, IP/GW set."; fi; else info_log "No DNS servers for manual config."; fi
    info_log "Static IP OK via iproute2."; return 0
}

configure_ethernet() {
    local iface_to_configure="${1:-}"
    if [[ ${#ETH_IFACES[@]} -eq 0 ]]; then _show_progress_message "No Ethernet interfaces available." "warning"; return 1; fi
    if [[ -z "$iface_to_configure" ]]; then
        if [[ "$NON_INTERACTIVE" == "true" ]]; then iface_to_configure="${ETH_IFACES[0]}"; info_log "Non-interactive: selected Ethernet $iface_to_configure";
        else local opts=(); for eth in "${ETH_IFACES[@]}"; do opts+=("$eth" "$eth"); done; iface_to_configure=$(prompt_select_option "Select Ethernet interface:" "${opts[@]}") || return 1; fi
        [[ -z "$iface_to_configure" ]] && { info_log "No Ethernet interface selected."; return 1; }
    elif ! [[ " ${ETH_IFACES[*]} " =~ " ${iface_to_configure} " ]]; then error_log "Specified Ethernet '$iface_to_configure' not found."; return 1; fi
    SELECTED_IFACE="$iface_to_configure"; info_log "Configuring Ethernet: $SELECTED_IFACE"
    local cfg_choice="dhcp"; if [[ "$NON_INTERACTIVE" == "false" ]]; then cfg_choice=$(prompt_select_option "Method for $SELECTED_IFACE:" "dhcp" "DHCP (Auto)" "static" "Static IP (Manual)") || return 1; fi
    case "$cfg_choice" in
        dhcp) if configure_dhcp "$SELECTED_IFACE"; then return 0; else warning_log "DHCP failed for $SELECTED_IFACE."; if [[ "$NON_INTERACTIVE" == "false" ]] && prompt_yes_no "DHCP failed. Try static IP?" "n"; then return configure_static_ip "$SELECTED_IFACE"; fi; return 1; fi ;;
        static) if configure_static_ip "$SELECTED_IFACE"; then return 0; else warning_log "Static IP failed for $SELECTED_IFACE."; return 1; fi ;;
        *) error_log "Invalid Ethernet config choice."; return 1 ;;
    esac
}

configure_dns() {
    local dns_servers_csv="$1" interface_context="${2:-}"
    [[ -z "$dns_servers_csv" ]] && { debug_log "No DNS servers provided."; return 0; }
    info_log "Configuring DNS: $dns_servers_csv"
    if [[ -f /etc/resolv.conf && ! -L /etc/resolv.conf ]]; then local bak="/etc/resolv.conf.bak.$(date +%s)"; if cp /etc/resolv.conf "$bak" 2>/dev/null; then debug_log "Backed up /etc/resolv.conf to $bak"; else warning_log "Failed to backup /etc/resolv.conf"; fi; fi
    local -a dns_arr; IFS=',' read -r -a dns_arr <<< "$dns_servers_csv"
    if systemctl is-active systemd-resolved >/dev/null 2>&1 && check_command resolvectl; then
        local eff_iface="global"; if [[ -n "$interface_context" ]] && ip link show "$interface_context" >/dev/null 2>&1; then local idx; idx=$(cat "/sys/class/net/$interface_context/ifindex" 2>/dev/null); [[ -n "$idx" ]] && eff_iface="$idx"; fi
        if debug_exec "resolvectl dns \"$eff_iface\" ${dns_arr[*]}"; then info_log "DNS OK via systemd-resolved for $eff_iface."; debug_exec "resolvectl flush-caches"; return 0; else warning_log "systemd-resolved failed."; fi
    fi
    if check_command resolvconf; then
        local res_iface="${interface_context:-netconnect_dns}"; local res_input=""; for dns in "${dns_arr[@]}"; do res_input+="nameserver $dns\n"; done
        echo "" | resolvconf -d "$res_iface" 2>/dev/null || true 
        if echo -e "$res_input" | resolvconf -a "$res_iface" 2>/dev/null; then info_log "DNS OK via resolvconf for $res_iface."; resolvconf -u 2>/dev/null || true; return 0; else warning_log "resolvconf failed."; fi
    fi
    if [[ -L /etc/resolv.conf ]]; then warning_log "/etc/resolv.conf is symlink. Direct write risky."; if $NM_AVAILABLE; then warning_log "NM active, should handle DNS."; fi; return 1; fi
    local res_content="# Generated by $SCRIPT_NAME at $(date)\n"; for dns in "${dns_arr[@]}"; do res_content+="nameserver $dns\n"; done
    if [[ -w /etc/resolv.conf ]] || ( [[ ! -e /etc/resolv.conf ]] && [[ -w /etc ]] ); then
        if echo -e "$res_content" > /etc/resolv.conf; then info_log "DNS OK via direct write to /etc/resolv.conf."; warning_log "Direct write may be overwritten."; return 0; else error_log "Failed direct write to /etc/resolv.conf."; return 1; fi
    else error_log "Cannot write /etc/resolv.conf (permissions)."; return 1; fi
}

# --- Wi-Fi Configuration Functions ---
# (ensure_wpa_supplicant_running, scan_wifi_networks, connect_wifi, configure_wifi, save_network_profile from v8.0 are complex.
# Key changes for v8.1:
# - scan_wifi_networks: nmcli part uses -g or -t -f for robust parsing.
# - ensure_wpa_supplicant_running: use PID file for termination if available.
# )

ensure_wpa_supplicant_running() {
    local iface="$1"
    debug_log "Ensuring wpa_supplicant is running for $iface..."
    if ! $WPA_CLI_AVAILABLE; then error_log "wpa_cli not found."; install_packages_dialog "wpa_cli,wpasupplicant" || return 1; check_command wpa_cli && WPA_CLI_AVAILABLE=true || { error_log "wpa_cli still not available."; return 1; }; fi
    if $NM_AVAILABLE || $IWD_AVAILABLE; then debug_log "NM or iwd active, assuming they handle supplicant needs."; if $WPA_CLI_AVAILABLE; then if debug_exec "wpa_cli -i \"$iface\" status"; then WPA_SUPPLICANT_SERVICE_ACTIVE=true; return 0; else WPA_SUPPLICANT_SERVICE_ACTIVE=false; return 0; fi; fi; return 0; fi
    
    local pid_file="/var/run/wpa_supplicant_${iface}.pid"
    if [[ -f "$pid_file" ]]; then local pid_val; pid_val=$(cat "$pid_file" 2>/dev/null); if [[ -n "$pid_val" ]] && kill -0 "$pid_val" 2>/dev/null; then if debug_exec "wpa_cli -i \"$iface\" status"; then debug_log "wpa_supplicant running (PID $pid_val) and responsive."; WPA_SUPPLICANT_SERVICE_ACTIVE=true; return 0; else warning_log "wpa_supplicant (PID $pid_val) running but unresponsive. Killing..."; kill "$pid_val" 2>/dev/null; sleep 1; fi; else debug_log "Stale PID file $pid_file. Removing."; rm -f "$pid_file"; fi; fi
    debug_exec "pkill -f \"wpa_supplicant.*[[:space:]]-i[[:space:]]*$iface\"" || true; sleep 1

    local wpa_conf="/etc/wpa_supplicant/wpa_supplicant-${iface}.conf" wpa_ctrl="/run/wpa_supplicant"
    mkdir -p "$(dirname "$wpa_conf")" "$wpa_ctrl"; if [[ ! -f "$wpa_conf" ]]; then echo -e "ctrl_interface=DIR=${wpa_ctrl} GROUP=netdev\nupdate_config=1\nap_scan=1" > "$wpa_conf"; chmod 600 "$wpa_conf"; fi
    info_log "Starting wpa_supplicant for $iface..."; local drvs=("nl80211" "wext") started=false
    for drv in "${drvs[@]}"; do debug_log "Trying wpa_supplicant for $iface with driver $drv"
        if debug_exec "wpa_supplicant -B -P \"$pid_file\" -i \"$iface\" -c \"$wpa_conf\" -D\"$drv\""; then sleep 2; if debug_exec "wpa_cli -i \"$iface\" status"; then info_log "wpa_supplicant started (driver $drv)."; started=true; break; else warning_log "wpa_supplicant started (driver $drv) but wpa_cli cannot connect. Killing."; local kpid; kpid=$(cat "$pid_file" 2>/dev/null); if [[ -n "$kpid" ]]; then kill "$kpid" 2>/dev/null; else pkill -f "wpa_supplicant.*[[:space:]]-i[[:space:]]*$iface.*-D$drv"; fi; sleep 1; fi
        else warning_log "Failed to start wpa_supplicant (driver $drv)."; fi; done
    if ! $started; then error_log "Failed to start wpa_supplicant for $iface."; WPA_SUPPLICANT_SERVICE_ACTIVE=false; return 1; fi
    WPA_SUPPLICANT_SERVICE_ACTIVE=true; return 0
}

scan_wifi_networks() {
    local iface="$1"
    info_log "Scanning for Wi-Fi networks on $iface..."
    local temp_scan_file; temp_scan_file=$(create_temp_file "wifi_scan_${iface}") || return 1
    ensure_interface_up "$iface" "wifi" || { safe_rm "$temp_scan_file"; return 1; }
    
    # This global associative array will be populated.
    # Bash functions don't easily return arrays, so this is a common pattern.
    # Caller (configure_wifi) must be aware of this.
    declare -gA unique_networks_scan_result=() # Ensure it's an assoc. array
    unique_networks_scan_result=() # Clear previous results

    # Method 1: NetworkManager (refined parsing)
    if $NM_AVAILABLE; then
        local nm_dev_state; nm_dev_state=$(nmcli -g GENERAL.STATE device show "$iface" 2>/dev/null || echo "unknown")
        if [[ "$nm_dev_state" != *"unavailable"* && "$nm_dev_state" != *"unmanaged"* ]]; then
            debug_log "Scanning with NetworkManager on $iface..."
            nmcli device wifi rescan ifname "$iface" >/dev/null 2>&1 || true; sleep "$WIFI_SCAN_TIMEOUT"
            # Use -g (generic) or -t -f for machine-readable output
            # nmcli -g SSID,SECURITY,SIGNAL,FREQ dev wifi list ifname "$iface" --rescan no
            local nm_scan_output; nm_scan_output=$(nmcli -t -f SSID,SECURITY,SIGNAL,FREQ dev wifi list ifname "$iface" --rescan no 2>/dev/null || true)
            if [[ -n "$nm_scan_output" ]]; then
                debug_log "Parsing NetworkManager scan results..."
                while IFS=':' read -r ssid security signal freq _; do
                    # nmcli -t -f might escape colons in SSID with \:
                    ssid="${ssid//\\:/ៈ}" # Temp replace escaped colon
                    ssid="${ssid//:/ }" # Replace non-escaped colons (should not happen in SSID field with -f)
                    ssid="${ssid//ៈ/:}" # Restore escaped colon
                    [[ -z "$ssid" || "$ssid" == "--" ]] && continue
                    local desc="Sig: ${signal}% | Sec: ${security:-Open} | Freq: ${freq}"
                    unique_networks_scan_result["$ssid"]="$desc"
                done <<< "$nm_scan_output"
                if [[ ${#unique_networks_scan_result[@]} -gt 0 ]]; then info_log "Wi-Fi scan via NM OK."; cat "$temp_scan_file"; return 0; fi # temp_scan_file not used here
            else warning_log "NM scan on $iface yielded no results."; fi
        else warning_log "NM reports $iface $nm_dev_state, skipping NM scan."; fi
    fi

    # Method 2: wpa_cli (v8.0 logic was decent, ensure robust parsing)
    if $WPA_CLI_AVAILABLE && [[ ${#unique_networks_scan_result[@]} -eq 0 ]]; then
        debug_log "Scanning with wpa_cli on $iface..."
        ensure_wpa_supplicant_running "$iface" || warning_log "wpa_supplicant not running, wpa_cli scan might fail."
        if wpa_cli -i "$iface" scan >/dev/null 2>&1; then sleep "$WIFI_SCAN_TIMEOUT";
            local wpa_scan_raw; wpa_scan_raw=$(wpa_cli -i "$iface" scan_results 2>/dev/null | tail -n +2)
            if [[ -n "$wpa_scan_raw" ]]; then debug_log "Parsing wpa_cli scan results..."
                echo "$wpa_scan_raw" | awk -F'\t' 'NF>=5 {ssid_val=substr($0, index($0,$5)); flags=$4; sec="Open"; if(flags ~ /WPA2-PSK/||flags ~ /RSN-PSK/)sec="WPA2-PSK"; else if(flags ~ /WPA-PSK/)sec="WPA-PSK"; else if(flags ~ /WEP/)sec="WEP"; else if(flags ~ /SAE/)sec="WPA3-SAE"; if(ssid_val!=""&&ssid_val!="\\x00"&&flags~/ESS/){gsub(/^"|"$/,"",ssid_val);gsub(/[[:cntrl:]]/,"",ssid_val);sig_val=$3;sq=sig_val;if(sig_val<=-100)sq=0;else if(sig_val>=-50)sq=100;else sq=2*(sig_val+100); printf "%s|%s|%s|%s\n",ssid_val,sec,sq,$2;}}' > "$temp_scan_file"
                if [[ -s "$temp_scan_file" ]]; then 
                    while IFS='|' read -r ssid security signal freq; do unique_networks_scan_result["$ssid"]="Sig: ${signal}% | Sec: ${security} | Freq: ${freq}"; done < "$temp_scan_file"
                    if [[ ${#unique_networks_scan_result[@]} -gt 0 ]]; then info_log "Wi-Fi scan via wpa_cli OK."; return 0; fi
                fi
            else warning_log "wpa_cli scan yielded no results."; fi
        else warning_log "wpa_cli scan command failed."; fi
    fi
    
    # Method 3: iw (fallback, parsing is simplified)
    if check_command iw && [[ ${#unique_networks_scan_result[@]} -eq 0 ]]; then
        debug_log "Scanning with iw on $iface..."
        local iw_scan_raw; iw_scan_raw=$(iw dev "$iface" scan 2>/dev/null || true)
        if [[ -n "$iw_scan_raw" ]]; then debug_log "Parsing iw scan results..."
            echo "$iw_scan_raw" | awk '/^BSS / {if(cs!="")pn();cb=substr($2,1,17);cs="";csig="";cf="";csec="Open";} /\tSSID: / {cs=substr($0,index($0,$2));} /\tsignal: / {csig=sprintf("%.0f",$2);} /\tfreq: / {cf=$2;} /\tRSN:/ {csec="WPA2";} /\tWPA:/ {if(csec=="Open")csec="WPA";} /\tPrivacy: / {if($2=="on"&&csec=="Open")csec="WEP";} /\tcapability:.*ESS/{ie=1;} END{if(cs!="")pn();} function pn(){if(ie&&cs!~/^\\x00/){gsub(/[[:cntrl:]]/,"",cs);sq=csig;if(csig<=-100)sq=0;else if(csig>=-50)sq=100;else sq=2*(csig+100);printf "%s|%s|%s|%s\n",cs,csec,sq,cf;}ie=0;}' > "$temp_scan_file"
            if [[ -s "$temp_scan_file" ]]; then
                while IFS='|' read -r ssid security signal freq; do unique_networks_scan_result["$ssid"]="Sig: ${signal}% | Sec: ${security} | Freq: ${freq}"; done < "$temp_scan_file"
                if [[ ${#unique_networks_scan_result[@]} -gt 0 ]]; then info_log "Wi-Fi scan via iw OK."; return 0; fi
            fi
        else warning_log "iw scan yielded no results."; fi
    fi

    safe_rm "$temp_scan_file"
    if [[ ${#unique_networks_scan_result[@]} -eq 0 ]]; then error_log "All Wi-Fi scanning methods failed or no networks found."; return 1; fi
    return 0 # unique_networks_scan_result is populated
}

connect_wifi() {
    local iface="$1" ssid="$2" password="${3:-}" security_type="${4:-}" is_hidden="${5:-false}"
    info_log "Attempting to connect to Wi-Fi: '$ssid' on $iface (Sec: ${security_type:-auto}, Hidden: $is_hidden)"
    ensure_interface_up "$iface" "wifi" || return 1
    if $NM_AVAILABLE; then debug_log "Trying NM for '$ssid'..."
        local nm_cmd=("nmcli" "dev" "wifi" "connect" "$ssid" "ifname" "$iface"); [[ -n "$password" ]] && nm_cmd+=("password" "$password"); [[ "$is_hidden" == "true" ]] && nm_cmd+=("hidden" "yes")
        local nm_con="netconnect-$ssid-$$"; nm_cmd+=("name" "$nm_con"); nmcli con delete id "$nm_con" >/dev/null 2>&1 || true
        show_progress_spinner "Connecting '$ssid' via NM" "$WIFI_CONNECT_TIMEOUT" & local ppid=$!; disown $ppid 2>/dev/null
        if "${nm_cmd[@]}" >/dev/null 2>&1; then wait $ppid 2>/dev/null; TMP_FILES_TO_CLEAN+=("nmcli_con_del_$nm_con"); sleep 3; if nmcli -t -f GENERAL.STATE dev show "$iface" 2>/dev/null | grep -q "100 (connected)" && ip addr show dev "$iface" | grep -q "inet "; then info_log "NM connected to '$ssid'."; return 0; else warning_log "NM connected to '$ssid' but no IP/full state."; nmcli con delete id "$nm_con" >/dev/null 2>&1 || true; fi
        else wait $ppid 2>/dev/null; warning_log "NM failed to connect to '$ssid'."; nmcli con delete id "$nm_con" >/dev/null 2>&1 || true; fi
    fi
    if $WPA_CLI_AVAILABLE; then debug_log "Trying wpa_cli for '$ssid'..."
        ensure_wpa_supplicant_running "$iface" || return 1
        wpa_cli -i "$iface" list_networks | grep "$ssid" | awk '{print $1}' | while read -r nid; do wpa_cli -i "$iface" remove_network "$nid" >/dev/null 2>&1; done
        local net_id; net_id=$(wpa_cli -i "$iface" add_network | tail -1); if ! [[ "$net_id" =~ ^[0-9]+$ ]]; then error_log "Failed to add net via wpa_cli for '$ssid'."; return 1; fi
        wpa_cli -i "$iface" set_network "$net_id" ssid "\"$ssid\"" >/dev/null; [[ "$is_hidden" == "true" ]] && wpa_cli -i "$iface" set_network "$net_id" scan_ssid 1 >/dev/null
        local km_set=false; if [[ -n "$security_type" ]]; then case "$security_type" in Open)wpa_cli -i "$iface" set_network "$net_id" key_mgmt NONE >/dev/null;km_set=true;; WEP)wpa_cli -i "$iface" set_network "$net_id" key_mgmt NONE >/dev/null;wpa_cli -i "$iface" set_network "$net_id" wep_key0 "\"$password\"" >/dev/null;wpa_cli -i "$iface" set_network "$net_id" wep_tx_keyidx 0 >/dev/null;km_set=true;; *PSK)wpa_cli -i "$iface" set_network "$net_id" key_mgmt WPA-PSK >/dev/null;wpa_cli -i "$iface" set_network "$net_id" psk "\"$password\"" >/dev/null;km_set=true;; *SAE)wpa_cli -i "$iface" set_network "$net_id" key_mgmt SAE >/dev/null;wpa_cli -i "$iface" set_network "$net_id" sae_password "\"$password\"" >/dev/null;km_set=true;; esac; fi
        if [[ -z "$password" && "$security_type" != "Open" && "$km_set" == "false" ]]; then warning_log "No pass for secured '$ssid' ($security_type)."; elif [[ -n "$password" && "$km_set" == "false" ]]; then wpa_cli -i "$iface" set_network "$net_id" psk "\"$password\"" >/dev/null; fi
        wpa_cli -i "$iface" enable_network "$net_id" >/dev/null; wpa_cli -i "$iface" select_network "$net_id" >/dev/null
        show_progress_spinner "Connecting '$ssid' via wpa_cli" "$WIFI_CONNECT_TIMEOUT" & local ppid_wpa=$!; disown $ppid_wpa 2>/dev/null
        local conn_wpa=false wpa_tries=$((WIFI_CONNECT_TIMEOUT/2)); for ((i=0;i<wpa_tries;i++)); do local st; st=$(wpa_cli -i "$iface" status 2>/dev/null); if echo "$st"|grep -q "wpa_state=COMPLETED"; then conn_wpa=true;break; fi; if echo "$st"|grep -q "reason=WRONG_KEY"; then error_log "wpa_cli: WRONG KEY for '$ssid'."; break; fi; sleep 2; done; wait $ppid_wpa 2>/dev/null
        if $conn_wpa; then info_log "wpa_cli associated '$ssid'. DHCP..."; wpa_cli -i "$iface" save_config >/dev/null 2>&1 || warning_log "Failed to save wpa_supplicant config."; if configure_dhcp "$iface"; then return 0; else error_log "wpa_cli associated, DHCP failed."; if [[ "$NON_INTERACTIVE" == "false" ]] && prompt_yes_no "DHCP failed for '$ssid'. Static IP?" "n"; then if configure_static_ip "$iface"; then return 0; fi; fi; fi
        else warning_log "wpa_cli connect to '$ssid' failed."; fi; wpa_cli -i "$iface" remove_network "$net_id" >/dev/null 2>&1
    fi
    if $IWD_AVAILABLE; then debug_log "Trying iwd for '$ssid'..."
        local iw_cmd=("iwctl" "--no-pager" "station" "$iface" "connect" "$ssid"); [[ -n "$password" ]] && iw_cmd+=("--passphrase" "$password")
        show_progress_spinner "Connecting '$ssid' via iwd" "$WIFI_CONNECT_TIMEOUT" & local ppid_iwd=$!; disown $ppid_iwd 2>/dev/null
        if debug_exec "${iw_cmd[@]}"; then wait $ppid_iwd 2>/dev/null; sleep 3; if iwctl station "$iface" show 2>/dev/null | grep -q "State.*connected" && ip addr show dev "$iface" | grep -q "inet "; then info_log "iwd connected to '$ssid'."; return 0; else warning_log "iwd connected but no IP/full state."; fi
        else wait $ppid_iwd 2>/dev/null; warning_log "iwd failed to connect to '$ssid'."; fi
    fi
    error_log "All Wi-Fi connection methods failed for '$ssid'."; return 1
}

# Global associative array for scan results, populated by scan_wifi_networks
declare -gA unique_networks_scan_result=()
configure_wifi() {
    local iface_to_configure="${1:-}"
    unique_networks_scan_result=() # Clear previous
    if [[ ${#WIFI_IFACES[@]} -eq 0 ]]; then _show_progress_message "No Wi-Fi interfaces." "warning"; return 1; fi
    if [[ -z "$iface_to_configure" ]]; then
        if [[ "$NON_INTERACTIVE" == "true" ]]; then iface_to_configure="${WIFI_IFACES[0]}"; info_log "Non-interactive: selected Wi-Fi $iface_to_configure";
        else local opts=(); for wf in "${WIFI_IFACES[@]}"; do opts+=("$wf" "$wf"); done; iface_to_configure=$(prompt_select_option "Select Wi-Fi interface:" "${opts[@]}") || return 1; fi
        [[ -z "$iface_to_configure" ]] && { info_log "No Wi-Fi interface selected."; return 1; }
    elif ! [[ " ${WIFI_IFACES[*]} " =~ " ${iface_to_configure} " ]]; then error_log "Specified Wi-Fi '$iface_to_configure' not found."; return 1; fi
    SELECTED_IFACE="$iface_to_configure"; info_log "Configuring Wi-Fi: $SELECTED_IFACE"
    _show_progress_message "Scanning for networks on $SELECTED_IFACE..." "transient"
    if ! scan_wifi_networks "$SELECTED_IFACE"; then # Populates global unique_networks_scan_result
        if [[ "$NON_INTERACTIVE" == "false" ]] && prompt_yes_no "No networks found. Connect to hidden?" "n"; then
            local h_ssid h_pass h_sec="WPA2-PSK"; h_ssid=$(prompt_user_input "Hidden SSID:") || return 1; [[ -z "$h_ssid" ]] && { error_log "Hidden SSID empty."; return 1; }
            h_pass=$(prompt_user_input "Password for '$h_ssid' (empty for open):" "" true); if [[ -z "$h_pass" ]]; then h_sec="Open"; if ! prompt_yes_no "Connect to '$h_ssid' as Open?" "y"; then return 1; fi; fi
            return connect_wifi "$SELECTED_IFACE" "$h_ssid" "$h_pass" "$h_sec" "true"
        fi; _show_progress_message "No Wi-Fi networks found/selected for $SELECTED_IFACE." "warning"; return 1;
    fi
    if [[ ${#unique_networks_scan_result[@]} -eq 0 ]]; then _show_progress_message "No Wi-Fi networks from scan." "warning"; return 1; fi
    local -a dlg_scan_opts=(); for skey in "${!unique_networks_scan_result[@]}"; do local s_trunc="$skey"; [[ ${#s_trunc} -gt 30 ]] && s_trunc="${s_trunc:0:27}..."; dlg_scan_opts+=("$skey" "$s_trunc (${unique_networks_scan_result[$skey]})"); done
    if [[ "$NON_INTERACTIVE" == "true" ]]; then error_log "Interactive Wi-Fi selection not supported here in non-interactive. Use profiles."; return 1; fi
    local sel_ssid_tag; sel_ssid_tag=$(prompt_select_option "Select Wi-Fi network on $SELECTED_IFACE:" "${dlg_scan_opts[@]}") || return 1; [[ -z "$sel_ssid_tag" ]] && { info_log "No network selected."; return 1; }
    local sel_desc="${unique_networks_scan_result[$sel_ssid_tag]}" sel_sec="WPA2-PSK"; if [[ "$sel_desc" =~ Sec:[[:space:]]*([^[:space:]]+) ]]; then sel_sec="${BASH_REMATCH[1]}"; elif [[ "$sel_desc" =~ Open ]]; then sel_sec="Open"; fi
    local wf_pass=""; if ! [[ "$sel_sec" =~ ^(Open|--)$ || -z "$sel_sec" ]]; then wf_pass=$(prompt_user_input "Password for '$sel_ssid_tag':" "" true) || return 1; if [[ "$sel_sec" != "WEP" && ${#wf_pass} -lt 8 && -n "$wf_pass" ]]; then if ! prompt_yes_no "Password for '$sel_ssid_tag' short. Continue?" "y"; then return 1; fi; elif [[ -z "$wf_pass" ]]; then if ! prompt_yes_no "Empty pass for secured '$sel_ssid_tag'. Treat as Open?" "n"; then return 1; else sel_sec="Open"; fi; fi; fi
    if connect_wifi "$SELECTED_IFACE" "$sel_ssid_tag" "$wf_pass" "$sel_sec" "false"; then save_network_profile "$SELECTED_IFACE" "$sel_ssid_tag" "$wf_pass" "$sel_sec" "false"; return 0; fi
    return 1
}

save_network_profile() {
    local iface="$1" ssid="$2" password="$3" security="$4" hidden="$5"
    local safe_fn="${ssid//[^a-zA-Z0-9._-]/_}"; [[ -z "$safe_fn" ]] && safe_fn="unnamed_ssid"
    local pf="${PROFILE_DIR}/${iface}_${safe_fn}.conf"; debug_log "Saving profile: $pf"
    mkdir -p "$PROFILE_DIR" 2>/dev/null || warning_log "Could not create $PROFILE_DIR"
    (umask 077; cat > "$pf" <<EOF
# Profile for SSID: $ssid on $iface by $SCRIPT_NAME v$SCRIPT_VERSION at $(date -Iseconds)
INTERFACE="$iface"
SSID="$ssid"
SECURITY="$security"
HIDDEN="$hidden"
$( [[ -n "$password" ]] && echo "PASSWORD_ENC=\"$(echo -n "$password" | base64)\"" )
EOF
    ) && info_log "Profile saved: $pf" || error_log "Failed to save profile $pf"
}

# --- Connectivity Check ---
# (check_connectivity from v8.0 is largely okay)
check_connectivity() {
    local test_type="${1:-full}"
    _show_progress_message "Checking network connectivity..." "transient"
    local ping_tgt_ip="$PING_IP_PRIMARY"; if ! ping -c 1 -W "$PING_TIMEOUT" "$ping_tgt_ip" >/dev/null 2>&1; then ping_tgt_ip="$PING_IP_SECONDARY"; fi
    if ping -c "$PING_COUNT" -W "$PING_TIMEOUT" "$ping_tgt_ip" >/dev/null 2>&1; then info_log "✓ IP connectivity to $ping_tgt_ip OK."; if [[ "$test_type" == "basic" ]]; then return 0; fi
        if ping -c "$PING_COUNT" -W "$PING_TIMEOUT" "$PING_HOSTNAME" >/dev/null 2>&1; then info_log "✓ DNS for $PING_HOSTNAME OK."; if check_command curl; then if curl -s --connect-timeout 5 -L "http://$PING_HOSTNAME" >/dev/null 2>&1; then info_log "✓ HTTP to $PING_HOSTNAME OK."; else warning_log "HTTP to $PING_HOSTNAME failed (curl)."; fi; fi; _show_progress_message "Network UP (IP, DNS, HTTP tested)." "persistent"; return 0;
        else warning_log "DNS for $PING_HOSTNAME failed."; _show_progress_message "Network PARTIAL (IP OK, DNS FAILED)." "warning"; return 2; fi
    else warning_log "No IP connectivity to $PING_IP_PRIMARY or $PING_IP_SECONDARY."; _show_progress_message "Network DOWN (No IP connectivity)." "error"; return 1; fi
}

# --- Main Script Functions ---
# (usage, parse_arguments, show_network_status, main from v8.0 are largely okay but need to use new prompt functions and integrate argument handling better)
usage() {
    local usage_text="Usage: sudo $SCRIPT_NAME [OPTIONS]

Universal Network Connectivity Script v$SCRIPT_VERSION

Configure Ethernet/Wi-Fi. Uses 'dialog' for TUI if available.

OPTIONS:
  -h, --help             Show help and exit.
  -v, --version          Show version and exit.
  -d, --debug            Enable full debug (level 3).
  --debug-level LEVEL    Set debug level (1:basic, 2:verbose, 3:full).
  -V, --verbose          Alias for --debug-level 2.
  -n, --non-interactive  Run non-interactively (auto-config).
  -i, --interface IFACE  Specify interface to configure.
  -t, --type TYPE        Specify type ('ethernet'|'wifi') for -i.
  -c, --check-only       Check connectivity, don't configure.
  --ssid SSID            (Wi-Fi) SSID to connect to (used with -i, -t wifi).
  --password PASS        (Wi-Fi) Password for SSID.
  --security SEC         (Wi-Fi) Security (WPA2-PSK, Open, WEP, WPA3-SAE).
  --hidden               (Wi-Fi) SSID is hidden.
  --install-deps         Check/install dependencies then exit.
  --status               Show network status and exit.

EXAMPLES:
  sudo $SCRIPT_NAME                     # Interactive mode
  sudo $SCRIPT_NAME -n                  # Non-interactive auto
  sudo $SCRIPT_NAME -i eth0 -t ethernet # Configure eth0
  sudo $SCRIPT_NAME -i wlan0 -t wifi --ssid \"MyNet\" --password \"MyPass\" 
"
    if $DIALOG_AVAILABLE && [[ "$NON_INTERACTIVE" == "false" ]]; then _show_dialog_message "msgbox" "Help - $SCRIPT_NAME v$SCRIPT_VERSION" "$usage_text" 25 78; else echo -e "$usage_text"; fi
}

parse_arguments() {
    declare -g cli_ssid="" cli_password="" cli_security="" cli_hidden=false # For direct Wi-Fi args
    # Reset flags that might be set if script is sourced/re-run in same shell
    DBG=false; DEBUG_LEVEL=1; NON_INTERACTIVE=false; SELECTED_IFACE=""; CONNECTION_TYPE_ARG=""; CHECK_ONLY_ARG=false
    INSTALL_DEPS_ARG=false; SHOW_STATUS_ARG=false

    while [[ $# -gt 0 ]]; do
        case "$1" in -h|--help) usage; exit 0 ;; -v|--version) echo "$SCRIPT_NAME v$SCRIPT_VERSION"; exit 0 ;;
            -d|--debug) DBG=true; DEBUG_LEVEL=3; shift ;;
            --debug-level) DBG=true; if [[ "$2" =~ ^[1-3]$ ]]; then DEBUG_LEVEL="$2"; else echo "Invalid debug level: $2" >&2; exit 1; fi; shift 2 ;;
            -V|--verbose) DBG=true; DEBUG_LEVEL=2; shift ;;
            -n|--non-interactive) NON_INTERACTIVE=true; shift ;;
            -i|--interface) SELECTED_IFACE="$2"; shift 2 ;;
            -t|--type) CONNECTION_TYPE_ARG=$(echo "$2"|tr '[:upper:]' '[:lower:]'); shift 2 ;;
            -c|--check-only) CHECK_ONLY_ARG=true; shift ;;
            --ssid) cli_ssid="$2"; shift 2 ;; --password) cli_password="$2"; shift 2 ;;
            --security) cli_security="$2"; shift 2 ;; --hidden) cli_hidden=true; shift ;;
            --install-deps) INSTALL_DEPS_ARG=true; shift ;; --status) SHOW_STATUS_ARG=true; shift ;;
            *) _base_log "ERROR" "$COLOR_RED" "Unknown option: $1"; usage; exit 1 ;;
        esac; done
    if [[ -n "$cli_ssid" ]]; then if [[ -z "$SELECTED_IFACE" || "$CONNECTION_TYPE_ARG" != "wifi" ]]; then _base_log "ERROR" "$COLOR_RED" "--ssid requires -i <wifi-iface> and -t wifi."; usage; exit 1; fi; if [[ "$NON_INTERACTIVE" == "true" ]]; then info_log "Direct Wi-Fi params for non-interactive: $SELECTED_IFACE, SSID:$cli_ssid"; declare -g DIRECT_WIFI_SSID="$cli_ssid"; declare -g DIRECT_WIFI_PASS="$cli_password"; declare -g DIRECT_WIFI_SEC="$cli_security"; declare -g DIRECT_WIFI_HIDDEN="$cli_hidden"; else warning_log "--ssid etc. for non-interactive use primarily."; fi; fi
}

show_network_status() {
    _show_progress_message "Gathering network status..." "transient"
    local status_text=""
    status_text+="\n=== Network Status ===\n"
    status_text+="\n--- Network Interfaces (ip -br addr) ---\n$(ip -br addr show 2>/dev/null || echo "Failed to get interface addresses.")\n"
    status_text+="\n--- Routing Table (ip route) ---\n$(ip route show 2>/dev/null || echo "Failed to get routing table.")\n"
    status_text+="\n--- DNS Configuration (/etc/resolv.conf) ---\n"
    if [[ -f /etc/resolv.conf ]]; then status_text+="$(grep -v '^#' /etc/resolv.conf | grep 'nameserver' || echo "No nameservers in /etc/resolv.conf.")"; else status_text+="/etc/resolv.conf not found."; fi
    status_text+="\n"
    if systemctl is-active systemd-resolved >/dev/null 2>&1 && check_command resolvectl; then status_text+="\n--- Systemd-Resolved Status ---\n$(resolvectl status 2>/dev/null || echo "Failed to get resolvectl status.")\n"; fi
    status_text+="\n--- Connectivity Test ---\n" # check_connectivity will print its own messages
    if $DIALOG_AVAILABLE && [[ "$NON_INTERACTIVE" == "false" ]]; then _show_dialog_message "msgbox" "Network Status" "$status_text" 20 75; else echo -e "$status_text"; fi
    check_connectivity "full"
}

main() {
    # Global flags that parse_arguments will set.
    declare -g INSTALL_DEPS_ARG=false SHOW_STATUS_ARG=false
    parse_arguments "$@"
    if $DBG; then mkdir -p "$LOG_DIR" 2>/dev/null; DEBUG_LOG_FILE="${LOG_DIR}/netconnect_debug_$(date +%Y%m%d_%H%M%S)_$$.log"; if ! touch "$DEBUG_LOG_FILE" 2>/dev/null; then echo "WARN: Cannot write debug log $DEBUG_LOG_FILE" >&2; DEBUG_LOG_FILE=""; else _base_log "INFO" "$COLOR_GREEN" "Debug mode L$DEBUG_LEVEL. Log: $DEBUG_LOG_FILE"; eval "exec $XTRACE_FD>>\"\$DEBUG_LOG_FILE\""; export BASH_XTRACEFD="$XTRACE_FD"; set -x; fi; fi
    debug_log "Script $SCRIPT_NAME v$SCRIPT_VERSION started (PID $$)"; debug_var_array=("NON_INTERACTIVE" "SELECTED_IFACE" "CONNECTION_TYPE_ARG" "CHECK_ONLY_ARG"); for v in "${debug_var_array[@]}"; do debug_var "$v"; done
    check_root; acquire_lock; init_directories
    if check_command dialog; then DIALOG_AVAILABLE=true; debug_log "Dialog available."; else DIALOG_AVAILABLE=false; info_log "Dialog not found. Basic prompts."; if [[ "$NON_INTERACTIVE" == "false" ]]; then install_packages_dialog "dialog,dialog" || info_log "Proceeding without dialog."; fi; fi
    if ! $DIALOG_AVAILABLE || [[ "$NON_INTERACTIVE" == "true" ]]; then echo -e "${COLOR_GREEN}=== $SCRIPT_NAME v$SCRIPT_VERSION ===${COLOR_RESET}\n" >&2; else "$DIALOG_CMD" --cr-wrap --title "$SCRIPT_NAME" --msgbox "Welcome to Universal Network Connectivity Script v$SCRIPT_VERSION" 8 60 2>/dev/tty; fi
    if $INSTALL_DEPS_ARG; then info_log "Checking/installing dependencies..."; local deps=("dialog,dialog" "ip,iproute2" "ping,iputils-ping" "curl,curl" "nmcli,network-manager" "wpa_cli,wpasupplicant" "iw,iw"); install_packages_dialog "${deps[@]}"; exit 0; fi
    detect_network_tools; detect_ethernet_interfaces; detect_wifi_interfaces
    if $SHOW_STATUS_ARG; then show_network_status; exit 0; fi
    if check_connectivity "basic"; then info_log "✓ Internet connection active."; if $CHECK_ONLY_ARG; then exit 0; fi; if [[ "$NON_INTERACTIVE" == "false" ]]; then if ! prompt_yes_no "Connection active. Reconfigure?" "n"; then exit 0; fi; else info_log "Non-interactive: Exiting, connection active."; exit 0; fi; else info_log "No active connection. Proceeding..."; if $CHECK_ONLY_ARG; then exit 1; fi; fi

    if [[ "$NON_INTERACTIVE" == "true" ]]; then info_log "Non-interactive mode..."; local connected=false
        if [[ -n "$SELECTED_IFACE" && -n "$CONNECTION_TYPE_ARG" ]]; then info_log "Configuring specified $SELECTED_IFACE ($CONNECTION_TYPE_ARG)..."
            if [[ "$CONNECTION_TYPE_ARG" == "ethernet" ]]; then if configure_ethernet "$SELECTED_IFACE"; then check_connectivity && connected=true; fi
            elif [[ "$CONNECTION_TYPE_ARG" == "wifi" ]]; then if [[ -n "${DIRECT_WIFI_SSID:-}" ]]; then if connect_wifi "$SELECTED_IFACE" "$DIRECT_WIFI_SSID" "${DIRECT_WIFI_PASS:-}" "${DIRECT_WIFI_SEC:-}" "${DIRECT_WIFI_HIDDEN:-false}"; then check_connectivity && connected=true; fi; else info_log "No direct SSID for $SELECTED_IFACE. Trying profiles..."; for pf in "${PROFILE_DIR}/${SELECTED_IFACE}_"*.conf; do if [[ -f "$pf" ]]; then debug_log "Profile: $pf"; local PI PS PSEC PPASSENC PHID; source "$pf"; PI="${INTERFACE:-}"; PS="${SSID:-}"; PSEC="${SECURITY:-}"; PPASSENC="${PASSWORD_ENC:-}"; PHID="${HIDDEN:-false}"; if [[ "$PI" == "$SELECTED_IFACE" && -n "$PS" ]]; then local pp; [[ -n "$PPASSENC" ]] && pp=$(echo "$PPASSENC"|base64 -d); if connect_wifi "$SELECTED_IFACE" "$PS" "$pp" "$PSEC" "$PHID"; then if check_connectivity; then connected=true; break; fi; fi; fi; fi; done; fi; fi
        fi
        if ! $connected; then info_log "Specified config failed or no specific args. Trying auto..."; for eth_if in "${ETH_IFACES[@]}"; do if configure_dhcp "$eth_if"; then if check_connectivity; then connected=true; break; fi; fi; done
            if ! $connected && [[ ${#WIFI_IFACES[@]} -gt 0 ]]; then for wifi_if in "${WIFI_IFACES[@]}"; do for pf in "${PROFILE_DIR}/${wifi_if}_"*.conf; do if [[ -f "$pf" ]]; then debug_log "Profile: $pf for $wifi_if"; local PI PS PSEC PPASSENC PHID; source "$pf"; PI="${INTERFACE:-}"; PS="${SSID:-}"; PSEC="${SECURITY:-}"; PPASSENC="${PASSWORD_ENC:-}"; PHID="${HIDDEN:-false}"; if [[ "$PI" == "$wifi_if" && -n "$PS" ]]; then local pp; [[ -n "$PPASSENC" ]] && pp=$(echo "$PPASSENC"|base64 -d); if connect_wifi "$wifi_if" "$PS" "$pp" "$PSEC" "$PHID"; then if check_connectivity; then connected=true; break 2; fi; fi; fi; fi; done; done; fi
        fi
        if $connected; then info_log "✓ Non-interactive connection OK."; exit 0; else error_log "Non-interactive connection FAILED."; exit 1; fi
    fi

    while true; do echo; local menu_opts=(); if [[ ${#ETH_IFACES[@]} -gt 0 ]]; then menu_opts+=("ETH" "Ethernet (${#ETH_IFACES[@]})"); fi; if [[ ${#WIFI_IFACES[@]} -gt 0 ]]; then menu_opts+=("WIFI" "Wi-Fi (${#WIFI_IFACES[@]})"); fi; menu_opts+=("STATUS" "Network Status" "CHECK" "Re-check Connectivity" "EXIT" "Exit");
        local choice; choice=$(prompt_select_option "Select action:" "${menu_opts[@]}") || { info_log "Exiting (cancel)."; exit 0; }
        case "$choice" in
            ETH) if [[ ${#ETH_IFACES[@]} -gt 0 ]]; then if configure_ethernet "$SELECTED_IFACE"; then check_connectivity && _show_progress_message "Ethernet OK!" "persistent" && exit 0; fi; else _show_progress_message "No Ethernet." "warning"; fi; SELECTED_IFACE="";;
            WIFI) if [[ ${#WIFI_IFACES[@]} -gt 0 ]]; then if configure_wifi "$SELECTED_IFACE"; then check_connectivity && _show_progress_message "Wi-Fi OK!" "persistent" && exit 0; fi; else _show_progress_message "No Wi-Fi." "warning"; fi; SELECTED_IFACE="";;
            STATUS) show_network_status ;; CHECK) check_connectivity ;; EXIT) info_log "User Exit."; exit 0 ;; *) error_log "Invalid choice: $choice" ;;
        esac
        if ! check_connectivity "basic"; then if ! prompt_yes_no "Connection failed/none. Try again?" "y"; then error_log "Exiting (failed attempts)."; exit 1; fi; fi
    done
    exit 1 # Should not reach
}

# Run main function
main "$@"
{% endcodeblock %}
