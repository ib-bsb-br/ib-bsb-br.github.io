---
tags: [scripts>bash]
info: aberto.
date: 2025-05-26
type: post
layout: post
published: true
slug: network-diag
title: 'network diag'
---
{% codeblock bash %}
#!/bin/bash
#
# network_diagnostics.sh
#
# This script is designed to collect as much information as possible about the
# network connection on a Debian Bullseye machine that uses dynamic IP addresses via DHCP.
#
# Note: Some commands may require root privileges.
#
# Usage:
#   chmod +x network_diagnostics.sh
#   sudo ./network_diagnostics.sh
#
# Feel free to modify or expand this script for your needs.
#

# -----------------------------------------------------------------------------
# Helper function to check if a command exists and print a header
function section_header() {
    echo "========================================"
    echo "$1"
    echo "========================================"
}

# -----------------------------------------------------------------------------
section_header "NETWORK DIAGNOSTICS REPORT"
echo "Report generated on: $(date)"
echo ""

# 1. Basic System Information
echo ">>> SYSTEM INFORMATION"
echo "Hostname: $(hostname)"
echo "Kernel info: $(uname -a)"

if command -v lsb_release >/dev/null 2>&1; then
    echo "Distribution Info:"
    lsb_release -a 2>/dev/null
else
    echo "/etc/issue:"
    cat /etc/issue
fi
echo ""

# 2. Network Interfaces
section_header "NETWORK INTERFACES"
echo "Using 'ip addr show':"
ip addr show
echo ""

if command -v ifconfig >/dev/null 2>&1; then
    echo "Using 'ifconfig -a':"
    ifconfig -a
else
    echo "ifconfig command not found (install net-tools package if needed)."
fi
echo ""

# 3. Routing Table
section_header "ROUTING TABLE"
echo "Using 'ip route show':"
ip route show
echo ""

if command -v netstat >/dev/null 2>&1; then
    echo "Using 'netstat -rn':"
    netstat -rn
else
    echo "netstat command not found (install net-tools package if needed)."
fi
echo ""

# 4. DNS Configuration
section_header "DNS CONFIGURATION"
echo "Contents of /etc/resolv.conf:"
cat /etc/resolv.conf
echo ""

# 5. DHCP Lease Information
section_header "DHCP LEASE INFORMATION"
LEASE_DIR="/var/lib/dhcp"
if [ -d "$LEASE_DIR" ]; then
    foundLease=0
    for lease_file in "$LEASE_DIR"/dhclient*.leases; do
	if [ -f "$lease_file" ]; then
	    echo ">> Lease file: $lease_file"
	    cat "$lease_file"
	    echo "--------------------------------------"
	    foundLease=1
	fi
    done
    if [ $foundLease -eq 0 ]; then
	echo "No DHCP lease files found in $LEASE_DIR."
    fi
else
    echo "DHCP lease directory $LEASE_DIR does not exist."
fi
echo ""

# Additionally, check syslog for recent DHCP-related messages.
section_header "DHCP MESSAGES (SYSLOG)"
if [ -f /var/log/syslog ]; then
    grep -i dhcp /var/log/syslog | tail -n 30
else
    echo "/var/log/syslog not found."
fi
echo ""

# 6. ARP Table
section_header "ARP TABLE"
ip neighbor show
echo ""

# 7. Interface Statistics
section_header "INTERFACE STATISTICS"
ip -s link
echo ""

# 8. Active Network Connections
section_header "ACTIVE NETWORK CONNECTIONS"
if command -v ss >/dev/null 2>&1; then
    ss -tulwn
elif command -v netstat >/dev/null 2>&1; then
    netstat -tulwn
else
    echo "Neither ss nor netstat found."
fi
echo ""

# 9. Internet Connectivity Tests
section_header "INTERNET CONNECTIVITY TESTS"

echo "Ping (IPv4) test to 8.8.8.8:"
ping -c 4 8.8.8.8
echo ""

echo "DNS resolution test (ping google.com):"
ping -c 4 google.com
echo ""

# 10. External IP Detection
section_header "EXTERNAL IP ADDRESS"
if command -v curl >/dev/null 2>&1; then
    echo "Your external IP (via https://api.ipify.org):"
    curl -s https://api.ipify.org
    echo ""
elif command -v wget >/dev/null 2>&1; then
    echo "Your external IP (via https://api.ipify.org):"
    wget -qO- https://api.ipify.org
    echo ""
else
    echo "Neither curl nor wget is installed. Install one to detect your external IP."
fi
echo ""

# 11. Traceroute
section_header "TRACEROUTE TO google.com"
if command -v traceroute >/dev/null 2>&1; then
    traceroute google.com
else
    echo "traceroute command not found. Install it with 'sudo apt install traceroute'."
fi
echo ""

# 12. iptables (Firewall Rules)
section_header "IPTABLES FIREWALL RULES"
if command -v iptables >/dev/null 2>&1; then
    sudo iptables -L -n -v
else
    echo "iptables command not found."
fi
echo ""

# 13. NetworkManager (if applicable)
if command -v nmcli >/dev/null 2>&1; then
    section_header "NETWORKMANAGER DEVICE INFORMATION"
    nmcli device show
    echo ""
fi

section_header "DIAGNOSTICS COMPLETE"
echo "The network diagnostics report is complete."
exit 0
{% endcodeblock %}