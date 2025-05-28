---
tags: [scratchpad]
info: aberto.
date: 2025-05-28
type: post
layout: post
published: true
slug: ip-changing
title: 'changing IP address '
---
This tutorial will guide you through changing your Debian Bullseye machine's IP address from one automatically assigned by DHCP to a static IP address. We'll use your network interface \`enP2p33s0\` (currently \`192.168.15.3/24\`) and your router's gateway (\`192.168.15.1\`) as the basis for examples.

Below is a step-by-step tutorial to change your Debian Bullseye machine’s IP address.

## **1\. Confirm Current Settings & Choose Your Static IP**

* **Current Interface and IP:** Your primary network interface is enP2p33s0, currently using 192.168.15.3/24.  
* **Gateway:** Your router's IP address is 192.168.15.1.  
* **DNS Servers (Current):** Your system logs show you're using 8.8.8.8 and 127.0.0.53. The 127.0.0.53 address means systemd-resolved is active and acting as a local DNS stub resolver. /etc/resolv.conf will point to it, but systemd-resolved forwards queries to upstream DNS servers configured elsewhere (or via DHCP). For a static configuration, you'll explicitly set these upstream servers.

**Choose Your Static IP:**

* It must be in the 192.168.15.x range.  
* It must **not** be 192.168.15.1 (your router).  
* It must **not** be used by another device on your network.  
* **Crucially:** It should be **outside your router's DHCP assignment range**. Log into your ASKEY RTF8115VW router to check its DHCP settings (usually under LAN or DHCP Server sections) and find the range of IPs it assigns automatically (e.g., 192.168.15.100 to 192.168.15.200). Choose an IP outside this range, for example, 192.168.15.50.

**Static IP Details for this Tutorial (Example):**

* **IP Address:** 192.168.15.50  
* **Netmask:** 255.255.255.0 (which is /24 in CIDR notation)  
* **Gateway:** 192.168.15.1  
* **DNS Servers (Example Choices):** 8.8.8.8 (Google) and 1.1.1.1 (Cloudflare). Alternatively, you could use your router's IP as a DNS forwarder, e.g., 192.168.15.1 and 8.8.8.8. *Use the DNS servers you prefer.*

## **2\. Back Up the Current Network Configuration**

Before making any changes, always back up your configuration. If your system uses ifupdown (common on Debian server installations), the main file is /etc/network/interfaces.

sudo cp /etc/network/interfaces /etc/network/interfaces.backup\_$(date \+%F)

If you plan to edit systemd-networkd files or NetworkManager configurations, back up relevant files from /etc/systemd/network/ or /etc/NetworkManager/system-connections/ respectively, if they exist and are being modified.

## **3\. Determine Your Network Management System**

Debian can use different systems to manage network configurations. You need to identify which one is actively managing enP2p33s0:

* ifupdown (via /etc/network/interfaces):  
  Check the contents: cat /etc/network/interfaces.  
  If you see a stanza for enP2p33s0 like auto enP2p33s0 and iface enP2p33s0 inet dhcp, ifupdown is likely managing this interface. This is a traditional method, often default on servers.  
* systemd-networkd:  
  Check its status: sudo systemctl is-active systemd-networkd.  
  If active, check for configuration files in /etc/systemd/network/ (e.g., ls /etc/systemd/network/). A .network file matching your interface might exist.  
* NetworkManager:  
  Check its status: sudo systemctl is-active NetworkManager.  
  If active (common on desktop environments), confirm it's managing the interface: nmcli dev status. Look for enP2p33s0.

This tutorial will primarily cover **Method A (ifupdown)** and **Method B (systemd-networkd)**, with an overview of Method C (NetworkManager). Choose the method appropriate for your system.

## **4\. Method A – Using /etc/network/interfaces (ifupdown)**

This is the traditional Debian method.

**a. Edit the configuration file:**

sudo nano /etc/network/interfaces

b. Modify the stanza for enP2p33s0:  
Find the lines for enP2p33s0. If it's set for DHCP, it might look like:  
auto enP2p33s0  
iface enP2p33s0 inet dhcp

Comment out or delete these lines and add/modify the stanza for a static configuration. If no entry exists, add the following:

\# The primary network interface  
auto enP2p33s0  
iface enP2p33s0 inet static  
    address 192.168.15.50        \# Your chosen static IP  
    netmask 255.255.255.0        \# Your netmask  
    gateway 192.168.15.1         \# Your gateway IP  
    dns-nameservers 8.8.8.8 1.1.1.1 \# Your chosen DNS servers (space separated)  
    \# dns-search yourlocaldomain.example \# Optional: for local domain search

c. Save and Exit:  
In nano, press Ctrl+O (Write Out), then Enter, then Ctrl+X (Exit).  
d. Apply the Changes:  
Restart the networking service:  
sudo systemctl restart networking.service

Or, bring the interface down and then up (may cause a brief disconnection):

sudo ifdown enP2p33s0 && sudo ifup enP2p33s0

*(If ifdown complains or the settings don't apply, another service like NetworkManager might be interfering. If NetworkManager is active and you intend to use ifupdown for this interface, you may need to stop/disable NetworkManager (sudo systemctl stop NetworkManager; sudo systemctl disable NetworkManager) or configure NetworkManager to ignore enP2p33s0 e.g., by adding unmanaged-devices=interface-name:enP2p33s0 to /etc/NetworkManager/NetworkManager.conf and restarting NetworkManager).*

## **5\. Method B – Using systemd-networkd**

If systemd-networkd is managing your network:

a. Create a configuration file:  
File names in /etc/systemd/network/ are typically prefixed with a number (e.g., 10- or 20- for ordering) and end in .network.  
sudo nano /etc/systemd/network/20-wired-static-enP2p33s0.network

**b. Add the following configuration:**

\[Match\]  
Name=enP2p33s0

\[Network\]  
Address=192.168.15.50/24   \# Your static IP with CIDR netmask  
Gateway=192.168.15.1      \# Your gateway  
DNS=8.8.8.8               \# Primary DNS (use your chosen server)  
DNS=1.1.1.1               \# Secondary DNS (use your chosen server)  
\# You can add more DNS= lines if needed  
\# Or use your router as a DNS: DNS=192.168.15.1

**c. Save and Exit.**

**d. Set permissions and restart the service:**

sudo chmod 644 /etc/systemd/network/20-wired-static-enP2p33s0.network  
sudo systemctl enable systemd-networkd \# Ensure it's enabled to start on boot  
sudo systemctl restart systemd-networkd

systemd-resolved (which is active on your system) should pick up these DNS settings from systemd-networkd.

## **6\. Method C – Using NetworkManager (Brief Overview)**

If your system (especially a desktop) uses NetworkManager:

* **Graphical Tool:** Use your desktop environment's network settings GUI. Find your wired connection (enP2p33s0), change its IPv4 settings from "Automatic (DHCP)" to "Manual," and enter your desired IP address, netmask, gateway, and DNS servers. Save and apply.  
* **Text User Interface (**nmtui**):**  
  sudo nmtui

  Navigate to "Edit a connection," select enP2p33s0 (or its connection name), choose "Edit...", change "IPv4 CONFIGURATION" to "Manual," and fill in the Addresses, Gateway, and DNS servers fields. Select "OK" and quit.  
* **Command Line (**nmcli**):** This is more advanced. First, find your connection name: nmcli con show. Let's assume it's "Wired connection 1".  
  sudo nmcli con mod "Wired connection 1" ipv4.method manual ipv4.addresses 192.168.15.50/24 ipv4.gateway 192.168.15.1 ipv4.dns "8.8.8.8 1.1.1.1"  
  sudo nmcli con down "Wired connection 1" && sudo nmcli con up "Wired connection 1"

  *(Note: For ipv4.dns, provide a space-separated list of DNS servers within the quotes).*

## **7\. Test Connectivity**

After applying changes using your chosen method, verify the configuration:

**a. Check IP Address:**

ip \-br addr show enP2p33s0

or

ip addr show enP2p33s0

You should see inet 192.168.15.50/24 (or your chosen static IP) associated with enP2p33s0.

**b. Check Routing Table:**

ip route show

Ensure the default route is via your gateway (e.g., default via 192.168.15.1 dev enP2p33s0).

c. Check DNS Resolution:  
Your /etc/resolv.conf file will likely show nameserver 127.0.0.53. This is expected when systemd-resolved is active. systemd-resolved listens on this local address and forwards DNS queries to the upstream servers you configured. To see the actual upstream DNS servers being used by systemd-resolved:  
resolvectl status

or

systemd-resolve \--status | grep \-A3 'Current DNS Server'

This should show the DNS servers you configured (e.g., 8.8.8.8, 1.1.1.1).

**d. Ping Tests:**

* Ping your gateway:  
  ping \-c 3 192.168.15.1

* Ping an external IP address (tests IP connectivity beyond your LAN):  
  ping \-c 3 8.8.8.8

* Ping a domain name (tests DNS resolution and full internet connectivity):  
  ping \-c 3 google.com

If all these tests pass, your static IP configuration is working correctly.

## **8\. Important Considerations & Reverting**

* **SSH Disconnection:** If you are connected to your Debian machine via SSH, changing its IP address will disconnect your session. Ensure you have physical console access or an alternative way to access the machine if issues arise.  
* **IP Conflicts:** Double-check that the static IP you chose is unique on your network and is **not** within your router's DHCP assignment range to prevent IP address conflicts.  
* **Router's DHCP Reservation (Alternative):** Instead of setting a static IP directly on the Debian machine, you can configure your ASKEY RTF8115VW router to always assign the same IP address to your Debian machine's MAC address. This is often called "DHCP Reservation" or "Static DHCP Lease."  
  * To use this method: Find your enP2p33s0 MAC address (ip link show enP2p33s0). Log into your router, find the DHCP reservation settings, and map the MAC address to your desired IP (e.g., 192.168.15.50).  
  * **Crucially:** If you use DHCP reservation on your router, ensure your Debian machine's network interface (enP2p33s0) is configured to obtain an IP address **automatically via DHCP** (i.e., revert any static IP settings on the Debian machine itself).  
* **Reverting to DHCP:**  
  * Method A (/etc/network/interfaces):  
    Restore your backup:  
    sudo cp /etc/network/interfaces.backup\_YYYY-MM-DD /etc/network/interfaces \# Use your actual backup filename

    Then, change the enP2p33s0 stanza back to:  
    auto enP2p33s0  
    iface enP2p33s0 inet dhcp

    Save, and restart networking: sudo systemctl restart networking.service.  
  * Method B (systemd-networkd):  
    Remove or rename your static .network file (e.g., sudo mv /etc/systemd/network/20-wired-static-enP2p33s0.network /etc/systemd/network/20-wired-static-enP2p33s0.network.disabled).  
    If no other .network file configures enP2p33s0 for DHCP, create one, e.g., /etc/systemd/network/10-dhcp-enP2p33s0.network:  
    \[Match\]  
    Name=enP2p33s0

    \[Network\]  
    DHCP=yes

    Save, and restart: sudo systemctl restart systemd-networkd.  
  * Method C (NetworkManager):  
    Using nmtui or your GUI, change the IPv4 method for the connection back to "Automatic (DHCP)".  
    Using nmcli (replace "Wired connection 1" with your actual connection name):  
    sudo nmcli con mod "Wired connection 1" ipv4.method auto ipv4.addresses "" ipv4.gateway "" ipv4.dns ""  
    sudo nmcli con up "Wired connection 1"
