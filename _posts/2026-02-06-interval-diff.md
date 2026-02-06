---
categories: []
tags:
  - scratchpad
comment: 
info: 
date: '2026-02-06'
type: post
layout: post
published: false
sha: f170324c240e2e73ab2d44081dc6a5139fd37222
slug: interval-diff
title: 'gather github commits diff of interval bash script'
---
```bash
#!/bin/bash
set -euo pipefail

# ==============================================================================
# Script Name: automate_treesheets_mining_agnostic.sh
# Purpose: Automates PyDriller mining tasks across multiple distros.
# Supported Distros (ARM64): Debian 11, Debian 12, OpenSUSE Tumbleweed
# Author: AI Assistant
# ==============================================================================

# --- Configuration Variables ---
REPO_URL="https://github.com/aardappel/treesheets.git"
START_DATE="2026-01-26"
END_DATE="2026-02-05"
OUTPUT_FILENAME="treesheets_concatenated_commits.txt"

PYTHON_SCRIPT_NAME="treesheets_miner.py"
VENV_DIR=".venv_mining"

# --- Helper Functions ---

log_info() {
    echo -e "[\033[1;32mINFO\033[0m] $1"
}

log_warn() {
    echo -e "[\033[1;33mWARN\033[0m] $1"
}

log_error() {
    echo -e "[\033[1;31mERROR\033[0m] $1" >&2
}

cleanup() {
    log_info "Performing cleanup..."
    if [ -d "$VENV_DIR" ]; then
        rm -rf "$VENV_DIR"
        log_info "Removed virtual environment: $VENV_DIR"
    fi
    if [ -f "$PYTHON_SCRIPT_NAME" ]; then
        rm -f "$PYTHON_SCRIPT_NAME"
        log_info "Removed temporary script: $PYTHON_SCRIPT_NAME"
    fi
}

# --- Distro Detection & Package Management ---

identify_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$ID"
    else
        log_error "/etc/os-release not found. Cannot detect distribution."
        exit 1
    fi
}

install_dependencies() {
    local distro
    distro=$(identify_distro)
    
    log_info "Detected Distribution ID: $distro"

    case "$distro" in
        debian)
            # Works for Debian 11 and 12
            log_info "Using APT package manager..."
            # python3-venv is explicitly required on Debian
            local DEB_PKGS=("git" "python3" "python3-pip" "python3-venv")
            
            # Update and install
            if ! sudo apt-get update -q; then
                log_error "apt-get update failed."
                exit 1
            fi
            
            # Check installed status to avoid redundant sudo calls if possible, 
            # but simple 'install -y' is robust.
            if ! sudo apt-get install -y "${DEB_PKGS[@]}"; then
                log_error "Failed to install dependencies on Debian."
                exit 1
            fi
            ;;
            
        opensuse-tumbleweed|opensuse|suse)
            log_info "Using Zypper package manager..."
            # OpenSUSE Tumbleweed: python3 usually includes venv, but explicit checks are safer.
            # git-core is often the base, but 'git' is the meta package.
            local SUSE_PKGS=("git" "python3" "python3-pip")
            
            if ! sudo zypper refresh; then
                log_error "zypper refresh failed."
                exit 1
            fi
            
            if ! sudo zypper install -y "${SUSE_PKGS[@]}"; then
                log_error "Failed to install dependencies on OpenSUSE."
                exit 1
            fi
            ;;
            
        *)
            log_error "Unsupported distribution: $distro"
            log_error "This script currently supports: Debian 11/12, OpenSUSE Tumbleweed."
            exit 1
            ;;
    esac
}

# Set up trap for cleanup
trap cleanup EXIT SIGINT SIGTERM

# --- Main Execution ---

log_info "Starting Distro-Agnostic PyDriller Automation (ARM64)..."

# 1. Dependency Installation (Distro Specific)
# ---------------------------------------------------------
log_info "Step 1: Handling System Dependencies..."
install_dependencies

# 2. Safety Confirmation (Output Overwrite)
# ---------------------------------------------------------
if [ -f "$OUTPUT_FILENAME" ]; then
    log_warn "The target output file '$OUTPUT_FILENAME' already exists."
    read -r -p "WARNING: This file will be overwritten. Continue? (yes/NO): " confirmation
    if [[ "$confirmation" != "yes" ]]; then
        log_error "Operation cancelled by user."
        exit 1
    fi
fi

# 3. Virtual Environment Setup (Standardized)
# ---------------------------------------------------------
log_info "Step 2: Setting up Python Virtual Environment ($VENV_DIR)..."

# Clear old venv if exists to ensure clean state
if [ -d "$VENV_DIR" ]; then
    rm -rf "$VENV_DIR"
fi

# Create venv
# Note: On Debian, this uses python3-venv. On SUSE, this uses the built-in venv module.
if ! python3 -m venv "$VENV_DIR"; then
    log_error "Failed to create virtual environment. Ensure python3-venv is active."
    exit 1
fi

# Activate
set +u
source "$VENV_DIR/bin/activate"
set -u

log_info "Installing PyDriller in virtual environment..."
# Upgrade pip to ensure wheel compatibility on ARM64
pip install --upgrade pip >/dev/null 2>&1 || log_warn "Pip upgrade skipped."

if ! pip install pydriller >/dev/null; then
    log_error "Failed to install PyDriller via pip."
    exit 1
fi

# 4. Generate Python Script (Content Injection)
# ---------------------------------------------------------
log_info "Step 3: Generating mining script..."

cat << EOF > "$PYTHON_SCRIPT_NAME"
from pydriller import Repository
from datetime import datetime
import sys

# CONFIGURATION INJECTED FROM BASH
REPO_URL = "${REPO_URL}"
OUTPUT_FILE = "${OUTPUT_FILENAME}"

# Parse dates (Year, Month, Day)
# Using end of day for the end date
START_DT = datetime.strptime("${START_DATE}", "%Y-%m-%d")
END_DT = datetime.strptime("${END_DATE} 23:59:59", "%Y-%m-%d %H:%M:%S")

def concatenate_commits():
    print(f"Analyzing {REPO_URL}...")
    print(f"Window: {START_DT} to {END_DT}")
    
    repo_mining = Repository(
        path_to_repo=REPO_URL,
        since=START_DT,
        to=END_DT,
        only_in_branch='master'
    )

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        commit_count = 0
        try:
            for commit in repo_mining.traverse_commits():
                commit_count += 1
                header = f"\n{'='*60}\nCOMMIT: {commit.hash}\nDATE: {commit.committer_date}\nMSG: {commit.msg}\n{'='*60}\n"
                
                print(f"Processing: {commit.hash[:7]} - {commit.committer_date}")
                outfile.write(header)

                for modified_file in commit.modified_files:
                    file_header = f"\n--- FILE: {modified_file.filename} ---\n"
                    outfile.write(file_header)
                    
                    if modified_file.diff:
                        outfile.write(modified_file.diff)
                    else:
                        outfile.write("(Binary file or no content change)\n")
        except Exception as e:
            print(f"Error during traversal: {e}")
            sys.exit(1)
                    
    print(f"\nDone! Processed {commit_count} commits.")

if __name__ == "__main__":
    concatenate_commits()
EOF

# 5. Execute Mining
# ---------------------------------------------------------
log_info "Step 4: Executing mining script..."

if python3 "$PYTHON_SCRIPT_NAME"; then
    log_info "Mining completed successfully."
else
    log_error "Mining script failed."
    exit 1
fi

# 6. Final Output
# ---------------------------------------------------------
if [ -f "$OUTPUT_FILENAME" ]; then
    log_info "Success! Output saved to: $(pwd)/$OUTPUT_FILENAME"
else
    log_error "Output file was not generated."
    exit 1
fi

exit 0
```