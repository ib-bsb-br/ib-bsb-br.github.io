---
categories: []
tags:
  - scratchpad
comment: 
info: 
date: '2025-12-24'
type: post
layout: post
published: true
sha: 
slug: opengl-status
title: 'verify OpenGL+OpenGL ES within Bullseye'

---
```bash
#!/bin/bash

# Description: Exhaustively lists OpenGL/ES/EGL/Mesa packages and verifies runtime versions.
# OS Target: Debian 11 (Bullseye)

# Define colors for readability
BOLD="\033[1m"
CYAN="\033[36m"
GREEN="\033[32m"
RED="\033[31m"
RESET="\033[0m"

echo -e "${BOLD}==================================================${RESET}"
echo -e "${BOLD} PART 1: EXHAUSTIVE PACKAGE AUDIT${RESET}"
echo -e "${BOLD}==================================================${RESET}"

# 1. SEARCH PATTERN
# We look for: mesa, opengl, libgl(x), libgles, libegl, and nvidia (if present).
# We EXCLUDE: libglib (GNOME core), glibc (C library), and unrelated globs.
SEARCH_REGEX="^(libgl[0-9]|libglx|libgles|libegl|mesa|nvidia|xserver-xorg-video|opengl)"
EXCLUDE_REGEX="(libglib|glibc|syslog|global)"

# 2. DYNAMIC DISCOVERY
# Get list of ALL installed packages matching the regex.
echo -e "${CYAN}[*] Scanning dpkg database for all graphics-related packages...${RESET}\n"

# Format: PackageName Version
# We use grep to filter the list of installed packages.
MATCHING_PACKAGES=$(dpkg-query -W -f='${Package} ${Version}\n' | grep -E "$SEARCH_REGEX" | grep -v -E "$EXCLUDE_REGEX" | sort)

if [ -z "$MATCHING_PACKAGES" ]; then
    echo -e "${RED}[!] No OpenGL/Mesa packages found!${RESET}"
else
    printf "%-40s %-30s\n" "PACKAGE NAME" "INSTALLED VERSION"
    printf "%-40s %-30s\n" "------------" "-----------------"
    echo "$MATCHING_PACKAGES" | awk '{printf "%-40s %s\n", $1, $2}'
fi

echo -e "\n${BOLD}==================================================${RESET}"
echo -e "${BOLD} PART 2: RUNTIME CAPABILITY CHECK${RESET}"
echo -e "${BOLD}==================================================${RESET}"

# 3. RUNTIME VERIFICATION
# Keeps going even if tools are missing.

# Check for glxinfo (Standard OpenGL)
if command -v glxinfo &> /dev/null; then
    echo -e "${GREEN}[*] Testing Standard OpenGL (glxinfo):${RESET}"
    # Extract relevant version lines
    glxinfo | grep -E -i "(OpenGL version|OpenGL renderer|OpenGL vendor|OpenGL core profile version)" | sed 's/^/    /'
else
    echo -e "${RED}[MISSING] 'glxinfo' not found.${RESET} Install 'mesa-utils' to verify runtime OpenGL."
fi

echo ""

# Check for es2_info (OpenGL ES)
if command -v es2_info &> /dev/null; then
    echo -e "${GREEN}[*] Testing OpenGL ES (es2_info):${RESET}"
    # Extract relevant version lines
    es2_info | grep -E -i "(GL_VERSION|GL_RENDERER|GL_VENDOR)" | sed 's/^/    /'
else
    echo -e "${RED}[MISSING] 'es2_info' not found.${RESET} Install 'mesa-utils-extra' to verify runtime OpenGL ES."
fi

echo -e "\n${BOLD}[DONE] Verification complete.${RESET}"
```