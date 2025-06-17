---
tags: [aid>software>linux]
info: aberto.
date: 2025-05-10
type: post
layout: post
published: true
slug: tigerbird
title: 'NetBird Cloud & TigerVNC: Secure SSH & VNC Access'
---
## NetBird Cloud & TigerVNC for Secure Remote Access

This guide details how to use NetBird Cloud in conjunction with TigerVNC to establish secure command-line (SSH) and graphical desktop (VNC) access to your Debian-based servers. It refactors a previous guide that focused on Tailscale, adapting the principles and steps for NetBird Cloud.

**Always refer to the official NetBird Cloud documentation ([netbird.io](https://netbird.io)) for the most current installation commands and feature details, as cloud services and their tools evolve.**

**Part 1: Secure Command-Line Access (SSH via NetBird Cloud)**

Secure command-line access via SSH is a cornerstone of server management. NetBird Cloud significantly enhances its security and ease of use by creating a private, peer-to-peer encrypted network.

**1.1. Key NetBird Cloud Benefits for SSH:**
*   **No Public SSH Port Exposure**: Your server's SSH port (default 22) does not need to be open on your internet router. NetBird creates a secure overlay network, meaning only authenticated and authorized peers on your NetBird network can reach the server.
*   **Simplified Firewall Management**: While the local firewall on the Debian machine (e.g., `ufw`) still needs to allow SSH traffic (e.g., `sudo ufw allow ssh`), NetBird Access Controls become the primary gatekeeper for *which peers* on your NetBird network can even attempt to connect.
*   **Identity-Based Access**: Authenticate using your NetBird identity, which supports Single Sign-On (SSO) with providers like Google, Microsoft, and GitHub. NetBird Access Controls define which peers (associated with users/groups) can connect to which machines.
*   **Private DNS**: Access servers using simple, stable hostnames (e.g., `my-debian-server.netbird.self`) within your NetBird network, instead of relying on potentially changing IP addresses.
*   **Automated Setup**: NetBird agents can be brought online automatically using setup keys, facilitating non-interactive joining to your NetBird network, which is ideal for scripted deployments.
*   **Peer-to-peer connections & encryption**: All traffic between your devices on the NetBird network is end-to-end encrypted using WireGuard®.

**1.2. Core Components for SSH Access:**
*   **`openssh-server`**: This must be installed and running on the Debian server. NetBird provides the secure transport layer for your existing SSH connections; `openssh-server` handles the SSH protocol itself.
    ```bash
    sudo apt update
    sudo apt install openssh-server
    sudo systemctl enable --now ssh
    ```
*   **NetBird Agent**: Installed on both the server and client machines.

**1.3. Implementation Steps for SSH over NetBird Cloud:**

1.  **On the Debian Server:**
    *   Install `openssh-server` (as shown above).
    *   **Install NetBird Agent:**
        The recommended method for Debian is often to add NetBird's package repository and install via `apt`. Always check the [official NetBird installation guide](https://docs.netbird.io/how-to/installation) for the latest instructions.
        *Example (verify on netbird.io):*
        ```bash
        # Add NetBird repository (command may vary)
        # sudo curl -sSL https://pkgs.netbird.io/debian/gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/netbird-archive-keyring.gpg
        # echo "deb [signed-by=/usr/share/keyrings/netbird-archive-keyring.gpg] https://pkgs.netbird.io/debian stable main" | sudo tee /etc/apt/sources.list.d/netbird.list
        sudo apt update
        sudo apt install netbird
        ```
        Alternatively, a script-based installation might be available:
        ```bash
        # curl -fsSL https://pkgs.netbird.io/install.sh | sudo bash
        ```
    *   **Obtain a NetBird Setup Key:** Go to your NetBird Management Portal (e.g., `app.netbird.io`), navigate to the "Setup Keys" tab, and create a new key.
    *   **Join NetBird:**
        ```bash
        sudo netbird up --setup-key YOUR_NETBIRD_SETUP_KEY --hostname my-debian-server
        ```
        The `--hostname` flag helps identify the peer in the NetBird UI and can influence its DNS name. You can also assign the server to **Groups** in the NetBird Management Portal for easier policy management, especially as your network grows.

2.  **In Your NetBird Management Portal (e.g., `app.netbird.io`):**
    *   Verify the machine (`my-debian-server`) appears in the "Peers" list.
    *   **Define Access Controls (Policies):** Navigate to "Access Control" -> "Policies". Create a policy to allow SSH traffic. NetBird policies apply to 'Peers' (devices), which are enrolled by users.
        *   **Name:** e.g., "Allow SSH to Debian Servers"
        *   **Action:** `Accept`
        *   **Sources:** Select the NetBird **Groups** (e.g., `group:developers`) or individual **Peers** that should be allowed to initiate SSH connections.
        *   **Destinations:** Select the NetBird **Group** containing `my-debian-server` (e.g., `group:production-servers`) or `my-debian-server` itself by its peer name.
        *   **Protocol:** `TCP`
        *   **Ports (Destination Ports):** `22`
        *   Ensure the policy is enabled.

3.  **On Your Client Machine:**
    *   Install the NetBird Agent (follow the same installation steps as for the server, appropriate for your client's OS).
    *   **Log in to NetBird:**
        ```bash
        sudo netbird up
        ```
        This command will typically open a browser window for you to authenticate with your chosen SSO provider.
    *   **Connect via SSH:** Use the server's NetBird Private DNS name (usually ending in `.netbird.self`) and the local Linux username on the server.
        ```bash
        ssh localuser@my-debian-server.netbird.self
        # Replace 'localuser' with the actual username on the Debian server.
        # Replace 'my-debian-server.netbird.self' with the server's NetBird DNS name.
        ```

---

**Part 2: Secure Graphical Desktop Access (VNC over NetBird Cloud)**

For tasks requiring a graphical desktop environment, VNC is a common solution. By routing VNC traffic over your NetBird network, you gain security and connectivity benefits similar to those for SSH, notably avoiding public VNC port exposure.

**2.1. Why VNC?**
VNC (Virtual Network Computing) allows you to view and interact with a remote computer's graphical desktop environment. This is useful for applications that don't have a command-line interface or for tasks that are easier to perform graphically.

**2.2. Key NetBird Cloud Benefits for VNC:**
*   **No Public VNC Port Exposure**: The VNC server port (commonly 5900, 5901, etc.) does not need to be open on your internet router. NetBird creates a secure, encrypted tunnel directly to the VNC server peer on your NetBird network.
*   **Simplified Firewall Management**: Your local firewall on the Debian machine (`ufw`) must allow traffic to the VNC port *from the NetBird interface*. NetBird Access Controls then determine which NetBird peers can reach this port on the server over the NetBird network.
*   **Private DNS**: Connect to your VNC server using its NetBird Private DNS name (e.g., `my-debian-server.netbird.self:1` or `my-debian-server.netbird.self:5901`).

**2.3. Core TigerVNC Components:**
You'll need a VNC server on the remote machine and a VNC viewer on your local machine. TigerVNC is a high-performance, open-source VNC implementation.

*   **VNC Server Options:**
    *   **`Xvnc`**: Creates a *virtual* desktop session, independent of any physical display. Ideal for headless servers.
    *   **`x0vncserver`**: Shares an *existing* X display (e.g., the physical console display or an active X11 session).

*   **VNC Server Management & Configuration:**
    *   **`vncsession`**: A script to manage `Xvnc` sessions, often integrated with systemd for user services. Configuration is typically in `$HOME/.config/tigervnc/config` (user-specific) or `/etc/tigervnc/vncserver-config-defaults`.
        *Example user config (`$HOME/.config/tigervnc/config`):*
        ```
        # geometry=1920x1080
        # depth=24
        # securitytypes=VncAuth,TLSVnc # Default often includes TLSVnc
        # session=xfce # Specify your installed desktop environment
        ```
    *   **`vncconfig`**: A utility to configure and control a *running* instance of `Xvnc`.
    *   **`vncpasswd`**: Crucial for setting the password to access VNC desktops. This must be run by the Linux user who will own the VNC session.
        ```bash
        # As the VNC user (e.g., 'localuser')
        vncpasswd # Stores obfuscated password in $HOME/.vnc/passwd or $HOME/.config/tigervnc/passwd
        ```

*   **VNC Client:**
    *   **`vncviewer`**: The client application used to connect to the VNC server.

**2.4. Implementation Steps for VNC over NetBird Cloud:**

**2.4.1. Setting up a Virtual Desktop with `Xvnc` (via `vncsession`)**
This is suitable for headless servers or creating independent graphical sessions. Using a systemd service is highly recommended for persistence.

1.  **On the Debian Server (as `root` or with `sudo`):**
    *   Ensure the NetBird Agent is installed and running (see section 1.3).
    *   Install a Desktop Environment (if not already present). XFCE is a good lightweight option:
        ```bash
        sudo apt update
        sudo apt install xfce4 xfce4-goodies
        ```
    *   Install TigerVNC Server components:
        ```bash
        sudo apt install tigervnc-standalone-server tigervnc-common
        ```
    *   **Configure VNC User and Password (as the intended VNC user, e.g., `localuser`):**
        If you are `root`, switch to the user: `su - localuser`
        ```bash
        vncpasswd # Set the VNC-specific password
        # (Optional) Create/edit $HOME/.config/tigervnc/config as shown in section 2.3
        ```
        If you switched user, type `exit` to return to your previous shell.

    *   **Start the VNC Server Session (Persistent Session with Systemd Recommended):**
        As the VNC user (`localuser`), create a systemd user service file: `~/.config/systemd/user/tigervnc@.service`:
        ```ini
        [Unit]
        Description=TigerVNC remote desktop server for %I
        After=network-online.target netbird.service # Ensure NetBird is up

        [Service]
        Type=forking
        # Use %h for user's home directory in ExecStart path
        ExecStart=/usr/bin/vncsession %i -SecurityTypes VncAuth,TLSVnc -rfbauth %h/.config/tigervnc/passwd -geometry 1920x1080 -localhost no
        ExecStop=/usr/bin/vncsession -kill %i
        Restart=on-failure
        RestartSec=5

        [Install]
        WantedBy=default.target
        ```
        *Note on `-localhost no`*: This ensures `Xvnc` listens on all interfaces, including the NetBird virtual interface.
        Then, as the VNC user (ensure lingering is enabled: `sudo loginctl enable-linger localuser` – this allows systemd user services to run even when the user `localuser` is not actively logged in):
        ```bash
        systemctl --user daemon-reload
        systemctl --user enable --now tigervnc@:1 # Starts VNC on display :1 (port 5901)
        # To check status: systemctl --user status tigervnc@:1
        ```
    *   **Configure Local Firewall (`ufw`):**
        Allow incoming connections to the VNC port (e.g., 5901 for display :1) *specifically from the NetBird interface*. First, identify your NetBird interface name (e.g., `wt0`, `nb-xxxx`) using `ip link show` or `nmcli device show`.
        ```bash
        # Replace 'YOUR_NETBIRD_INTERFACE' with the actual interface name
        sudo ufw allow in on YOUR_NETBIRD_INTERFACE to any port 5901 proto tcp
        ```

**2.4.2. Sharing an Existing X Display with `x0vncserver`**
This is for sharing a display that is already active (e.g., a physical monitor).

1.  **On the Debian Server:**
    *   Ensure NetBird Agent is installed and running.
    *   Ensure an X server is running with the session you want to share.
    *   Install `tigervnc-scraping-server` (usually provides `x0vncserver`):
        ```bash
        sudo apt install tigervnc-scraping-server
        ```
    *   **Set VNC Password (as the user whose X session will be shared):** `vncpasswd`
    *   **Start `x0vncserver` (as the user owning the X session):**
        This command needs to be run from within the active X session or with the `DISPLAY` environment variable correctly set.
        ```bash
        x0vncserver -rfbauth $HOME/.config/tigervnc/passwd -SecurityTypes VncAuth,TLSVnc -display :0 -localhost no
        ```
    *   **Configure Local Firewall (`ufw`):**
        Allow incoming connections to the VNC port (default 5900 if `x0vncserver` attaches to display :0) from the NetBird interface.
        ```bash
        # Replace 'YOUR_NETBIRD_INTERFACE' with the actual interface name
        sudo ufw allow in on YOUR_NETBIRD_INTERFACE to any port 5900 proto tcp
        ```

**2.4.3. NetBird Access Controls for VNC Access**
In your NetBird Management Portal ("Access Control" -> "Policies"):
*   Create a new policy or modify an existing one.
*   **Name:** e.g., "Allow VNC to Debian Servers"
*   **Action:** `Accept`
*   **Sources:** Select the NetBird **Groups** or individual **Peers** allowed to initiate VNC connections.
*   **Destinations:** Select the NetBird **Group** containing `my-debian-server` or `my-debian-server` itself.
*   **Protocol:** `TCP`
*   **Ports (Destination Ports):** `5901` (for `Xvnc` on display :1) or `5900` (for `x0vncserver` on display :0). Create separate rules or use a port list if multiple VNC displays are active.
*   Ensure the policy is enabled.

**2.4.4. Connecting from the Client Machine**

1.  Ensure the NetBird Agent is installed on your client and you are logged in (`sudo netbird up`).
2.  Install a VNC Viewer (e.g., `tigervnc-viewer` on Linux, or RealVNC Viewer, TightVNC Viewer on other OSes).
    ```bash
    # For Debian/Ubuntu clients
    sudo apt install tigervnc-viewer
    ```
3.  Connect using the VNC Viewer to the server's NetBird Private DNS name and display/port:
    *   For `Xvnc` on display `:1`: `my-debian-server.netbird.self:1` (or `my-debian-server.netbird.self:5901`)
    *   For `x0vncserver` on display `:0`: `my-debian-server.netbird.self:0` (or `my-debian-server.netbird.self:5900`)
    You will be prompted for the VNC password set on the server.

**2.5. VNC Security Considerations:**
*   **`SecurityTypes` Parameter for TigerVNC:**
    *   `VncAuth`: Basic password authentication. The password itself is not sent in cleartext but the VNC protocol's own encryption for this is not considered strong by modern standards.
    *   `TLSVnc`: Encapsulates the VNC protocol within TLS, providing strong encryption for the VNC session itself. This requires X.509 certificates on the server (TigerVNC can generate self-signed ones).
*   **Interaction with NetBird Encryption:** NetBird Cloud provides strong, end-to-end WireGuard® encryption for all traffic between peers on your NetBird network. This means your VNC traffic is already well-protected.
    *   Using `VncAuth` over NetBird is often considered sufficient due to NetBird's robust underlying encryption.
    *   Opting for `TLSVnc` provides an *additional layer* of security directly within the VNC protocol. This offers defense-in-depth, which could be beneficial if, hypothetically, the NetBird agent on an endpoint were compromised or if you wanted VNC security independent of the overlay network for any reason. However, it adds complexity to the VNC server setup (certificate management).

---

**Key Features, Benefits, and Improvements of this NetBird-based Framework**

*   **Comprehensive Access:** Provides secure solutions for both command-line (SSH) and graphical desktop (VNC) access.
*   **Unified Security Layer:** NetBird Cloud acts as a common security and connectivity backbone, leveraging peer-to-peer encryption, SSO integration, and centralized access policies.
*   **Reduced Attack Surface:** Eliminates the need to expose SSH or VNC ports directly to the public internet, drastically minimizing vulnerability to external threats.
*   **Centralized Network Access Control:** NetBird Access Controls (Policies) manage network reachability to services (SSH, VNC ports) based on peer identity and group membership. Application-level authentication (SSH keys, VNC passwords) remains distinct and is handled by the respective services.
*   **Simplified Connectivity:** NetBird's Private DNS allows using consistent, human-readable hostnames for all connections within the private network.
*   **Flexibility & Modernity:** Users can choose the appropriate remote access method, secured by a modern, zero-trust networking solution.
*   **Builds on Proven Technology:** Leverages NetBird (for secure overlay networking using WireGuard®) and TigerVNC (a robust, open-source VNC implementation).

**Hypothesis Evaluation:**
The initial hypothesis that a comprehensive Secure Remote Access framework can be constructed by integrating TigerVNC with NetBird Cloud's security model (analogous to a previous Tailscale-based framework) is **strongly supported**. This guide successfully demonstrates the merging of these components, showcasing how NetBird can secure both SSH and VNC traffic effectively.

---

**Limitations and Areas for Further Development**

*   **VNC Authentication vs. NetBird Identity:** VNC session authentication (password) is separate from the NetBird SSO identity. There's no direct SSO into the VNC session itself.
*   **VNC Performance:** While generally good, VNC performance can vary based on network latency, bandwidth, display resolution, and desktop environment complexity.
*   **Complexity of VNC Server & Desktop Environment Setup:** Detailed configuration of desktop environments and advanced VNC server tuning can be intricate and OS-dependent.
*   **Granularity of VNC Session Control:** Fine-grained control *within* an active VNC session (e.g., clipboard sharing, read-only access) is managed by TigerVNC's capabilities, not by NetBird Access Controls.

---

**Broader Implications of this Framework for Secure Remote Access Practices**

*   **Enhanced Productivity:** Offers flexible, secure, and easy-to-use access to essential tools, boosting remote work capabilities.
*   **Simplified IT Administration:** Centralizes network access control via the NetBird Management Portal, reducing the complexity of managing firewalls and individual VPN configurations.
*   **Improved Security Posture:** Significantly enhances security by adopting zero-trust principles, ensuring that only authenticated and explicitly authorized peers can connect to services.
*   **Shift Towards Modern Solutions:** Encourages the adoption of modern, software-defined perimeter solutions like NetBird Cloud over traditional VPNs or direct public exposure of services.

---

**Actionable Next Steps for Implementing, Refining, and Further Developing this Framework**

1.  **Detailed Implementation Guides:**
    *   Create specific tutorials for various desktop environments (KDE, GNOME) used with `vncsession` and systemd user services over NetBird.
    *   Develop a more focused guide for `x0vncserver` scenarios, perhaps including auto-starting it within a desktop session.
2.  **Refinement and Advanced Configuration:**
    *   Provide advanced NetBird Access Control policy examples (e.g., restricting access based on specific source peer IPs within the NetBird network, though group-based access is generally preferred for scalability).
    *   Include a dedicated troubleshooting section for common VNC-over-NetBird and SSH-over-NetBird issues.
    *   Detail the setup of `TLSVnc` with self-signed or CA-signed certificates for users desiring that additional VNC-specific encryption layer.
    *   Explore and document the use of NetBird's "Network Routes" and "DNS Forwarding" features for scenarios involving access to legacy networks or services through a NetBird peer acting as a gateway.
