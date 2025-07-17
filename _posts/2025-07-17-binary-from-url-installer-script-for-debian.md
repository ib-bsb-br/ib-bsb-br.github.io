---
tags: [scratchpad]
info: aberto.
date: 2025-07-17
type: post
layout: post
published: true
slug: binary-from-url-installer-script-for-debian
title: 'Binary from URL Installer Script for Debian'
---
{% codeblock bash %}
#!/bin/bash
#
# This script automates the download, verification, and installation of a software
# binary from a direct URL onto a Debian-based system. It provides a flexible
# workflow with an emphasis on security.
#
# Tutorial Name: Secure and Flexible Installer for a Binary from a Direct URL
# Target System: Debian 11 (Bullseye) / Debian 12 (Bookworm) on arm64 or amd64
#
# This script is designed to be run by a non-root user with sudo privileges.
#

# Exit immediately if a command exits with a non-zero status, if an unset variable
# is used, or if a command in a pipeline fails.
set -euo pipefail

# --- Global Variables ---
INSTALL_DIR="/usr/local/bin"
TEMP_DOWNLOAD_DIR=""

# User-provided values will be stored here
binary_url=""
install_name=""
expected_checksum=""
downloaded_filename=""

# --- Helper Functions ---

#
# Ensures the temporary directory is cleaned up on script exit or interruption.
#
cleanup() {
    if [[ -n "${TEMP_DOWNLOAD_DIR}" && -d "${TEMP_DOWNLOAD_DIR}" ]]; then
        echo
        echo "--- Cleaning up temporary directory ---"
        rm -rf "${TEMP_DOWNLOAD_DIR}"
        echo "Temporary directory removed."
    fi
}
trap cleanup EXIT SIGINT SIGTERM

#
# Gathers all necessary information from the user with validation.
#
prompt_for_input() {
    echo "--- Step 1: Gathering Information ---"

    # Prompt for Binary URL
    while [[ -z "$binary_url" ]]; do
        read -r -p "Enter the direct download URL for the binary: " binary_url
        if ! [[ "$binary_url" =~ ^https?:// ]]; then
            echo "Error: Invalid URL. It must start with 'http://' or 'https://'." >&2
            binary_url=""
        fi
    done

    # Prompt for Installation Name and sanitize it immediately
    while [[ -z "$install_name" ]]; do
        read -r -p "Enter the desired command name (e.g., 'dasel', 'hugo'): " install_name
        if [[ -z "$install_name" ]]; then
            echo "Error: Command name cannot be empty." >&2
        else
            # CRITICAL: Sanitize input by using basename to strip any directory
            # information, preventing path traversal vulnerabilities.
            install_name=$(basename "$install_name")
            echo "Info: The sanitized command name will be '${install_name}'."
        fi
    done

    # Ask user if they want to perform the security check
    echo
    echo "For your security, it is highly recommended to verify the integrity of the"
    echo "downloaded file using its SHA256 checksum. This ensures the file has not"
    echo "been corrupted or tampered with during download."
    read -r -p "Perform checksum verification? (YES/no): " perform_check
    if [[ "${perform_check,,}" == "no" ]]; then
        echo "Warning: Skipping security verification. Proceed with caution." >&2
        expected_checksum="skip" # Set a special value to indicate skipping
        return
    fi

    # If verifying, ask for the method
    echo "How do you want to provide the SHA256 checksum?"
    select checksum_method in "Paste the checksum value directly" "Get checksum from a URL (e.g., a checksums.txt file)"; do
        case $checksum_method in
            "Paste the checksum value directly")
                read -r -p "Enter the expected SHA256 checksum value: " expected_checksum
                break
                ;;
            "Get checksum from a URL (e.g., a checksums.txt file)")
                local checksum_url
                read -r -p "Enter the URL of the checksums file: " checksum_url
                echo "Info: Attempting to fetch checksum from ${checksum_url}..."
                downloaded_filename=$(basename "${binary_url}")
                # Fetch checksum from URL, grep for the specific filename, and extract the hash
                expected_checksum=$(curl -sL "${checksum_url}" | grep "${downloaded_filename}" | awk '{print $1}')
                if [[ -z "$expected_checksum" ]]; then
                    echo "Error: Could not find a checksum for '${downloaded_filename}' at the specified URL." >&2
                    exit 1
                fi
                echo "Info: Successfully extracted checksum: ${expected_checksum}"
                break
                ;;
        esac
    done

    # Validate the final checksum value (convert to lowercase for case-insensitivity)
    expected_checksum=${expected_checksum,,}
    if ! [[ "$expected_checksum" =~ ^[a-f0-9]{64}$ ]]; then
        echo "Error: Invalid or missing SHA256 checksum. It must be 64 hexadecimal characters." >&2
        exit 1
    fi
}

#
# Checks for prerequisites and potential conflicts before proceeding.
#
pre_flight_checks() {
    echo
    echo "--- Step 2: Performing System Checks ---"

    if [[ "$(id -u)" -eq 0 ]]; then
        echo "Error: This script must be run as a non-root user with sudo privileges." >&2
        exit 1
    fi

    if command -v "${install_name}" >/dev/null 2>&1; then
        echo "Warning: A command named '${install_name}' already exists at: $(command -v "${install_name}")"
        read -r -p "Do you want to overwrite it? (yes/NO): " confirm
        if [[ "${confirm,,}" != "yes" ]]; then
            echo "Operation cancelled by user."
            exit 0
        fi
        echo "Info: Proceeding with overwrite."
    fi

    echo "Updating package lists and ensuring 'curl' and 'coreutils' are installed..."
    if ! sudo apt-get update -qq && sudo apt-get install -y -qq curl coreutils; then
        echo "Error: Failed to update package lists or install required packages." >&2
        exit 1
    fi
    echo "Prerequisites are satisfied."
}

#
# Handles the download and optional verification of the binary.
#
fetch_and_verify_binary() {
    echo
    echo "--- Step 3: Downloading and Verifying Binary ---"

    TEMP_DOWNLOAD_DIR=$(mktemp -d -p "$HOME" generic_install_XXXXXX)
    cd "${TEMP_DOWNLOAD_DIR}"
    echo "Created temporary download directory at: ${TEMP_DOWNLOAD_DIR}"

    if [[ -z "$downloaded_filename" ]]; then
        downloaded_filename=$(basename "${binary_url}")
    fi

    echo "Downloading binary from URL..."
    # Capture stderr to a variable on failure for better error reporting
    local curl_error
    if ! curl_error=$(curl --fail --show-error -L -o "${downloaded_filename}" "${binary_url}" 2>&1); then
        echo "Error: Failed to download the binary from ${binary_url}" >&2
        echo "Curl reported: ${curl_error}" >&2
        exit 1
    fi
    echo "Download completed: ${downloaded_filename}"

    # Perform verification only if the user opted in
    if [[ "$expected_checksum" != "skip" ]]; then
        echo "Verifying file integrity with SHA256 checksum..."
        local actual_checksum
        actual_checksum=$(sha256sum "${downloaded_filename}" | awk '{print $1}')

        if [[ "${actual_checksum}" != "${expected_checksum}" ]]; then
            echo "Error: Checksum verification FAILED!" >&2
            echo "The downloaded file may be corrupted or tampered with." >&2
            echo "Expected: ${expected_checksum}" >&2
            echo "Actual:   ${actual_checksum}" >&2
            exit 1
        fi
        echo "Checksum verification successful. The file is authentic."
    fi
}

#
# Gives the binary executable permissions and moves it to the install directory.
#
install_binary() {
    echo
    echo "--- Step 4: Installing Binary ---"

    echo "Setting executable permission on the binary..."
    if ! chmod +x "${downloaded_filename}"; then
        echo "Error: Failed to set executable permission on ${downloaded_filename}." >&2
        exit 1
    fi

    echo "Installing '${install_name}' to ${INSTALL_DIR}/${install_name} (requires sudo)..."
    if ! sudo mv "${downloaded_filename}" "${INSTALL_DIR}/${install_name}"; then
        echo "Error: Failed to move the binary to ${INSTALL_DIR}." >&2
        echo "Please check your sudo permissions and if the target directory is writable." >&2
        exit 1
    fi
}

# --- Main Execution ---
main() {
    prompt_for_input
    pre_flight_checks
    fetch_and_verify_binary
    install_binary

    cd "$HOME"

    echo
    echo "--- Installation Complete! ---"
    echo "'${install_name}' has been successfully installed to ${INSTALL_DIR}/${install_name}"
    echo "You can now use the '${install_name}' command from any directory."
    echo "Verify the installation by running: ${install_name} --version (if supported)"
}

main "$@"
{% endcodeblock %}