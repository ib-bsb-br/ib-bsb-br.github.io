---
tags: [scratchpad]
info: aberto.
date: 2025-05-29
type: post
layout: post
published: true
slug: bash-script-to-leverage-the-fclones-rust-tool-for-dedup-directories
title: 'bash script to leverage the `fclones` rust tool for dedup directories'
---
{% codeblock bash %}
#!/bin/bash
set -euo pipefail

# Script to install fclones and use it to remove duplicate files from a specified directory.
# This script will:
# 1. Ensure necessary build tools (including for xattr) and Rust/Cargo are installed.
# 2. Install fclones using 'cargo install'.
# 3. Add ~/.cargo/bin to the PATH for the current session and .bashrc for future sessions.
# 4. Set up Bash completions for fclones.
# 5. Run fclones to group and remove duplicate files from the target directory,
#    keeping only unique files and the first encountered copy of duplicates, after user confirmation.
#
# Target Environment: Debian 11 (Bullseye) on ARM64 RK3588
# Tutorial Name: Leveraging `fclones` to remove each and every duplicated file, so, keeping only the uniques and the first copy of the duplicates, from the location named `/home/linaro/Downloads` recursively, with depth 10, on my debian bullseye arm64 rk3588 machine.

# --- Configuration Variables ---
# The tutorial specifies /home/linaro/Downloads.
# This script uses /home/linaro/Downloads for better portability if the username is not 'linaro',
# assuming the script is run by the intended user.
# If you strictly need /home/linaro/Downloads and your username is different, adjust this.
FCLONES_TARGET_DIR="/home/linaro/Downloads"
FCLONES_DEPTH="10"

CARGO_BIN_DIR="$HOME/.cargo/bin"
RUSTUP_INIT_SCRIPT_FILENAME="rustup-init.sh" # Just the filename
BASHRC_FILE="$HOME/.bashrc"
TEMP_DOWNLOAD_DIR="" # Used for rustup-init.sh download, set by mktemp
APT_UPDATED_FLAG=""  # Flag to ensure apt update runs only once

# --- Helper Functions ---

# Function to clean up temporary files on script exit or interruption
cleanup_temp_files() {
    echo "Cleaning up temporary files (if any)..."
    if [ -n "$TEMP_DOWNLOAD_DIR" ] && [ -d "$TEMP_DOWNLOAD_DIR" ]; then
        # shellcheck disable=SC2115 # Known issue with variable in rm -rf, path is controlled by mktemp
        rm -rf "$TEMP_DOWNLOAD_DIR"
        echo "Removed temporary directory: $TEMP_DOWNLOAD_DIR"
    fi
}
# Setup trap for cleanup
trap cleanup_temp_files EXIT SIGINT SIGTERM

# Function to ensure a tool is installed via apt
ensure_tool_installed() {
    local tool_name="$1"
    local package_name="${2:-$tool_name}" # Use second arg as package name if provided, else tool_name
    
    # Check if the command is available first, as some tools might be installed manually
    # or come from packages with different names than the command itself.
    # If checking for a library's dev package, tool_name might be the lib name (e.g. libattr1-dev)
    # and dpkg -s is more reliable.
    if ! dpkg -s "$package_name" >/dev/null 2>&1; then
        echo "Package '$package_name' (for tool/library '$tool_name') not found. Installing..."
        # Run apt update once before first install attempt if not already done
        if [ -z "$APT_UPDATED_FLAG" ]; then
            echo "Updating package lists (first time for this script run)..."
            if ! sudo apt update; then
                echo "Error: Failed to update package lists." >&2
                exit 1
            fi
            APT_UPDATED_FLAG="true" # Set the flag
            echo "Package lists updated successfully."
        fi

        if ! sudo apt install -y "$package_name"; then
            echo "Error: Failed to install '$package_name'." >&2
            exit 1
        fi
        echo "Package '$package_name' installed successfully."
    else
        echo "Package '$package_name' (for tool/library '$tool_name') is already installed."
    fi
}

# Function to ensure Rust and Cargo are installed via rustup
ensure_rust_installed() {
    if command -v cargo >/dev/null 2>&1; then
        echo "Rust and Cargo are already installed and accessible via PATH."
        # Source cargo environment in case it's installed but not in current session's PATH yet
        if [ -f "$HOME/.cargo/env" ]; then
            # shellcheck source=/dev/null
            source "$HOME/.cargo/env"
        fi
        return # Skip rustup installation
    fi

    echo "Rust and Cargo not found in PATH. Installing via rustup..."
    TEMP_DOWNLOAD_DIR=$(mktemp -d) # Create a temporary directory for the script
    local rustup_script_full_path="${TEMP_DOWNLOAD_DIR}/${RUSTUP_INIT_SCRIPT_FILENAME}"

    echo "Downloading Rust installation script to ${rustup_script_full_path}..."
    if ! curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs -o "${rustup_script_full_path}"; then
        echo "Error: Failed to download Rust installation script." >&2
        # TEMP_DOWNLOAD_DIR will be cleaned by the trap
        exit 1
    fi
    
    echo "Running Rust installation script (rustup-init.sh)..."
    # Run rustup-init.sh non-interactively:
    # -y: auto-accepts prompts.
    # --default-toolchain stable: ensures a stable version.
    # --no-modify-path: prevents rustup from modifying shell rc files directly; we handle PATH explicitly.
    if ! sh "${rustup_script_full_path}" -y --default-toolchain stable --no-modify-path; then
        echo "Error: Rust installation failed." >&2
        # TEMP_DOWNLOAD_DIR will be cleaned by the trap
        exit 1
    fi
    
    # TEMP_DOWNLOAD_DIR (and script within) will be cleaned by the trap
    echo "Rust and Cargo installed successfully via rustup."
    
    # Source cargo environment for the current script session
    if [ -f "$HOME/.cargo/env" ]; then
        # shellcheck source=/dev/null
        source "$HOME/.cargo/env"
        echo "Sourced Cargo environment for the current session."
    else
        echo "Warning: Could not source $HOME/.cargo/env. Cargo might not be in PATH for this session."
    fi
}

# Function to add a directory to PATH for current session and persist in .bashrc
add_to_path_if_not_present() {
    local dir_to_add="$1"
    local rc_file="$2"
    
    # For current session
    if [[ ":$PATH:" != *":${dir_to_add}:"* ]]; then
        echo "Adding ${dir_to_add} to PATH for current session..."
        export PATH="${dir_to_add}:$PATH"
    else
        echo "${dir_to_add} is already in PATH for current session."
    fi

    # For future sessions (idempotent check)
    if ! grep -qF --fixed-strings "export PATH=\"${dir_to_add}:\$PATH\"" "$rc_file" && \
       ! grep -qF --fixed-strings "export PATH=\\\"${dir_to_add}:\\\$PATH\\\"" "$rc_file"; then # Check for escaped version too
        echo "Adding ${dir_to_add} to PATH in ${rc_file} for future sessions..."
        # Create .bashrc if it doesn't exist
        touch "$rc_file"
        # Add a comment and the export line
        echo -e "\n# Add ${dir_to_add} to PATH (added by fclones script)\nexport PATH=\"${dir_to_add}:\$PATH\"" >> "$rc_file"
        echo "Please source ${rc_file} or open a new terminal for changes to take full effect in other shells."
    else
        echo "${dir_to_add} is already configured in ${rc_file}."
    fi
}

# --- Main Script ---
echo "Starting fclones installation and usage script..."
echo "Target directory for fclones: ${FCLONES_TARGET_DIR}"
echo "Recursion depth: ${FCLONES_DEPTH}"
echo "---"

# Step 1: Install prerequisite system packages
echo "Ensuring prerequisite system packages are installed..."
ensure_tool_installed "curl"
ensure_tool_installed "build-essential" # For Rust compilation
ensure_tool_installed "pkg-config"      # Often needed by Rust crates with C dependencies
ensure_tool_installed "libssl-dev"      # For crates needing OpenSSL
ensure_tool_installed "git"             # Cargo might need git for some dependencies
ensure_tool_installed "libattr1-dev"    # For xattr support in fclones
echo "System prerequisite check completed."
echo "---"

# Step 2: Install Rust and Cargo
ensure_rust_installed
echo "---"

# Step 3: Add Cargo's bin directory to PATH (current session and .bashrc)
add_to_path_if_not_present "${CARGO_BIN_DIR}" "${BASHRC_FILE}"
echo "---"

# Step 4: Install fclones using Cargo
echo "Installing fclones using Cargo..."
if ! command -v cargo >/dev/null 2>&1; then
    echo "Error: cargo command not found even after setup. Installation cannot proceed." >&2
    echo "Please ensure Rust is correctly installed and $CARGO_BIN_DIR is in your PATH." >&2
    exit 1
fi
if ! cargo install fclones; then
    echo "Error: Failed to install fclones using Cargo." >&2
    exit 1
fi
echo "fclones installed successfully via Cargo."
# Verify fclones is now in PATH
if ! command -v fclones >/dev/null 2>&1; then
    echo "Error: fclones installed but not found in PATH. This is unexpected." >&2
    echo "Please check your PATH and $CARGO_BIN_DIR." >&2
    exit 1
fi
fclones --version
echo "---"

# Step 5: Set up Bash completions for fclones
echo "Setting up Bash completions for fclones..."
if ! grep -qF 'eval "$(fclones complete bash)"' "${BASHRC_FILE}"; then
    echo -e '\n# fclones bash completion (added by fclones script)\neval "$(fclones complete bash)"' >> "${BASHRC_FILE}"
    echo "Bash completions for fclones added to ${BASHRC_FILE}."
    echo "Completions will be available in new shell sessions, or after sourcing ${BASHRC_FILE}."
else
    echo "Bash completions for fclones already set up in ${BASHRC_FILE}."
fi
# Enable for current session
eval "$(fclones complete bash)"
echo "Bash completions for fclones enabled for the current session."
echo "---"

# Step 6: Check if target directory exists
echo "Checking target directory: ${FCLONES_TARGET_DIR}..."
if [ ! -d "${FCLONES_TARGET_DIR}" ]; then
    echo "Warning: Target directory ${FCLONES_TARGET_DIR} does not exist."
    echo "fclones might not find any files to process. You may want to create it first."
    # Example of how to offer creation, commented out by default:
    # read -r -p "Create directory ${FCLONES_TARGET_DIR} now? (yes/NO): " create_dir_confirm
    # if [[ "$create_dir_confirm" == "yes" ]]; then
    #    if ! mkdir -p "${FCLONES_TARGET_DIR}"; then
    #       echo "Error: Failed to create directory ${FCLONES_TARGET_DIR}." >&2; exit 1;
    #    fi
    #    echo "Directory ${FCLONES_TARGET_DIR} created."
    # else
    #    echo "Proceeding without creating the directory. fclones may find no files."
    # fi
fi
echo "---"

# Step 7: Execute fclones to remove duplicates
echo "Preparing to remove duplicate files from ${FCLONES_TARGET_DIR} (recursive depth ${FCLONES_DEPTH})."
echo "This operation will keep only unique files and the first encountered copy of any duplicates."
echo ""
# Explicit confirmation for the remove operation
read -r -p "WARNING: This will PERMANENTLY REMOVE duplicate files from '${FCLONES_TARGET_DIR}'. This action is IRREVERSIBLE. Are you absolutely sure you want to continue? (Type 'YES' to proceed): " confirmation
if [[ "$confirmation" != "YES" ]]; then
    echo "Operation cancelled by user. No files will be removed." >&2
    exit 1
fi

echo ""
echo "Proceeding with fclones operation..."
# fclones should be in PATH now
echo "Running: fclones group \"${FCLONES_TARGET_DIR}\" --depth \"${FCLONES_DEPTH}\" | fclones remove"
if ! fclones group "${FCLONES_TARGET_DIR}" --depth "${FCLONES_DEPTH}" | fclones remove; then
    echo "Error: fclones command execution failed. fclones may have printed more specific errors above." >&2
    exit 1
fi
echo "fclones operation completed successfully."
echo "---"

echo "Script finished."
# Trap will handle cleanup of TEMP_DOWNLOAD_DIR
exit 0
{% endcodeblock %}