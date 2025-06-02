---
tags: [scratchpad]
info: aberto.
date: 2025-06-02
type: post
layout: post
published: true
slug: disable-tracker-processes-on-linux
title: 'Disable Tracker processes on linux'
---
{% codeblock bash %}
#!/bin/bash
set -euo pipefail
# -----------------------------------------------------------------------------
# Script Name: disable_tracker.sh
# Purpose   : Disable Tracker processes on Debian 11 (Bullseye) for ARM64 RK3588
#	      This script appends "Hidden=true" to tracker-related autostart files,
#	      updates Tracker settings via gsettings to disable file crawling and
#	      monitoring, and resets the Tracker database.
#
# WARNING   : This operation modifies system autostart files and resets the Tracker
#	      database. If you rely on Tracker for desktop search or metadata indexing,
#	      this action will disable those functions. It is recommended you backup any
#	      critical data/configuration before proceeding.
#
# Usage	    : Run this script from your home directory. You must have sudo privileges.
# -----------------------------------------------------------------------------

# Prompt for explicit user confirmation before proceeding.
read -r -p "WARNING: This will disable Tracker processes by modifying system autostart files and resetting the Tracker database. This may affect desktop search functionality. Do you want to continue? (yes/NO): " confirmation
if [[ "$confirmation" != "yes" ]]; then
    echo "Operation cancelled by user." >&2
    exit 1
fi

# Define an array of Tracker autostart file paths.
autostart_files=(
    "/etc/xdg/autostart/tracker-extract.desktop"
    "/etc/xdg/autostart/tracker-miner-apps.desktop"
    "/etc/xdg/autostart/tracker-miner-fs.desktop"
    "/etc/xdg/autostart/tracker-miner-user-guides.desktop"
    "/etc/xdg/autostart/tracker-store.desktop"
)

echo "Starting Tracker disabling procedure..."

# Iterate over each autostart file and append "Hidden=true" if not already set.
for file in "${autostart_files[@]}"; do
    echo "Processing file: ${file}"
    if [[ -f "$file" ]]; then
	if grep -q -E '^[[:space:]]*Hidden=true' "$file"; then
	    echo "-> 'Hidden=true' already present in ${file}. Skipping."
	else
	    echo -e "\nHidden=true\n" | sudo tee --append "$file" > /dev/null || {
		echo "Error: Failed to modify ${file}." >&2
		exit 1
	    }
	    echo "-> Appended 'Hidden=true' to ${file}."
	fi
    else
	echo "-> Warning: File ${file} does not exist. Skipping."
    fi
done

# Update Tracker settings using gsettings.
echo "Disabling Tracker file crawling..."
if ! gsettings set org.freedesktop.Tracker.Miner.Files crawling-interval -2; then
    echo "Error: Failed to set crawling-interval to -2 via gsettings." >&2
    exit 1
fi
echo "-> Set crawling-interval to -2."

echo "Disabling Tracker file monitors..."
if ! gsettings set org.freedesktop.Tracker.Miner.Files enable-monitors false; then
    echo "Error: Failed to disable file monitors via gsettings." >&2
    exit 1
fi
echo "-> File monitors disabled."

# Reset the Tracker database.
reset_cmd=""
if command -v tracker3 >/dev/null 2>&1; then
    reset_cmd="tracker3 reset --filesystem --rss"
elif command -v tracker >/dev/null 2>&1; then
    reset_cmd="tracker reset --hard"
else
    echo "Warning: Neither 'tracker3' nor 'tracker' is available. Skipping Tracker database reset." >&2
fi

if [[ -n "${reset_cmd}" ]]; then
    echo "Resetting Tracker database with: ${reset_cmd}"
    if ! ${reset_cmd}; then
	echo "Error: Failed to reset Tracker database." >&2
	exit 1
    fi
    echo "-> Tracker database has been reset."
fi

echo "Tracker disabling procedure completed successfully."
exit 0
{% endcodeblock %}