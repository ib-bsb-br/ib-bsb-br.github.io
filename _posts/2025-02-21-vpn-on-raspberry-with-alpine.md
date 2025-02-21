---
tags: [scratchpad]
info: aberto.
date: 2025-02-21
type: post
layout: post
published: true
slug: vpn-on-raspberry-with-alpine
title: 'VPN on Raspberry with Alpine'
---
# 1 – Prepare Hardware and Flash Alpine Linux

1. Gather a Raspberry Pi 3B, a microSD card (≥8 GB), and a reliable power supply (5 V, 2.5 A or more). 2. Download the official Alpine Linux image for Raspberry Pi (e.g., “alpine-rpi-3.17.0-armhf.iso”) from the Alpine Linux website. 3. Flash the image onto the microSD card using dd (Linux) or a similar flashing tool: 
`umount /dev/sdX*`

`dd if=alpine-rpi-3.17.0-armhf.iso of=/dev/sdX bs=4M status=progress &amp;&amp; sync`
(Replace /dev/sdX with your actual device name.) 4. Insert the card into the Pi 3B and power it on. 5. When prompted, log in as root and run the Alpine setup process: 
`setup-alpine`
Follow prompts to configure keyboard, timezone, network, hostname, etc.
• “sys” mode: Installs Alpine on the SD card.
• “diskless” mode: Runs from RAM; changes require “lbu commit.”

# 2 – System Update and Required Package Installation

1. Update Alpine and upgrade any existing packages: 
`apk update &amp;&amp; apk upgrade`
2. Install essential packages for PiVPN operation: 
`apk add bash curl git nano iptables iproute2 openvpn wireguard-tools tcpdump`
3. (Optional) For cryptographic key generation to have sufficient entropy: 
`apk add haveged`
Then start and enable haveged: 
`rc-service haveged start`

`rc-update add haveged default`


# 3 – Enable Tunnels, IP Forwarding, and Persist Settings

1. Ensure the “tun” module is loaded immediately: 
`modprobe tun`

`echo "tun" &gt; /etc/modules-load.d/tun.conf`
2. Enable IP forwarding so VPN traffic can flow properly: 
`sysctl -w net.ipv4.ip_forward=1`

`sysctl -w net.ipv6.conf.all.forwarding=1`
Persist these in /etc/sysctl.conf or /etc/sysctl.d/ so they reapply on reboot: net.ipv4.ip_forward=1 net.ipv6.conf.all.forwarding=1 3. (Optional) For diskless mode users, commit changes: 
`lbu commit`

# 4 – Static IP (Recommended)

1. (Optional, but strongly recommended) Assign a static address to your Raspberry Pi 3B: 
`nano /etc/network/interfaces`
Example stanza: auto eth0 iface eth0 inet static address 192.168.1.100 netmask 255.255.255.0 gateway 192.168.1.1 Adjust according to your LAN’s configuration. 2. Restart networking or reboot to confirm changes: 
`ifdown eth0 &amp;&amp; ifup eth0`
or: 
`reboot`

# 5 – Run the PiVPN Installer

1. Switch to Bash (if not already): 
`bash`
2. Download and run the PiVPN script: 
`curl -L https://install.pivpn.io | bash`
3. Follow PiVPN’s interactive prompts:
• Choose “OpenVPN” or “WireGuard” as your VPN protocol.
• If using OpenVPN: The installer configures EasyRSA, server certificate, keys.
• If using WireGuard: The script sets up keys and default conf parameters.
• Specify your selected UDP port (1194 for OpenVPN, 51820 for WireGuard) or accept defaults.
• Pick a DNS provider (e.g., Google’s 8.8.8.8).
• Let PiVPN adjust iptables rules automatically.

# 6 – Configure Services to Start on Boot

1. For OpenVPN: 
`rc-update add openvpn default`

`rc-service openvpn start`
2. For WireGuard (depending on your interface name, e.g., wg0): 
`rc-update add wg-quick.default default`

`rc-service wg-quick.default start`
(If the wg-quick service is present; otherwise configure manually under /etc/conf.d/.)

# 7 – Creating and Managing VPN Client Profiles

1. Add a client profile (example: client1): 
`pivpn add -n client1`
OpenVPN → generates client1.ovpn; WireGuard → generates client1.conf. 2. Transfer this file safely to the client device (SCP/USB).

# 8 – Router Port Forwarding

1. In your home router’s UI, locate Port Forwarding:
• OpenVPN: - Protocol: UDP - External Port: 1194 - Internal IP: 192.168.1.100 - Internal Port: 1194
• WireGuard: - Protocol: UDP - External Port: 51820 - Internal IP: 192.168.1.100 - Internal Port: 51820 2. Save or apply settings and reboot router if needed.

# 9 – Testing Your VPN

1. Securely transfer the generated client configuration file to an external device:
• For OpenVPN: `scp /root/ovpns/client1.ovpn user@remote-device:/home/user/Documents/`
• For WireGuard, similarly transfer `client1.conf`.

2. On your computer or mobile device, install the respective VPN client:
• OpenVPN: Use the official OpenVPN client.
• WireGuard: Install the official WireGuard client.

3. Import the configuration file into the VPN client.

4. Connect to the VPN and verify connectivity by checking:
• The tunnel's IP address assignment.
• Your public IP change via an IP lookup service.
• Access to local network resources (if configured).

# 10 – Maintenance and Troubleshooting

1. Check service logs:
• OpenVPN logs: tail -f /var/log/openvpn.log
• WireGuard info: wg show 2. Tweak or review iptables rules; changes can be saved with: 
`rc-update add iptables`

`service iptables save`
3. Update the system regularly: 
`apk update &amp;&amp; apk upgrade`
4. For diskless mode, always: 
`lbu commit`
after changes to persist them. 5. If encountering issues, use: 
`tcpdump -i eth0 port 1194 (OpenVPN)`

`tcpdump -i eth0 port 51820 (WireGuard)`
to capture traffic and help debug.