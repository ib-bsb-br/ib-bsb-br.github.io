---
tags: [scratchpad]
info: aberto.
date: 2025-04-30
type: post
layout: post
published: true
slug: 4-node-nethserver-8-homelab
title: '4-node NethServer 8 homelab'
---
NethServer 8 (NS8) marks a significant evolution from its predecessors, embracing a modern **Container Orchestrator** architecture. Instead of a monolithic system, NS8 focuses on managing containerized Apps, offering flexibility but requiring a different deployment mindset compared to NethServer 7 (NS7).

This guide provides a practical example of deploying a multi-node NS8 environment based on community discussions and official documentation (particularly the NS7 vs NS8 comparison [1], which users should note was marked "Work In Progress" and details may evolve). It outlines a 4-node setup designed to separate core services for clarity and potential scalability, using only features and concepts described in the source material.

**Key Architectural Concepts & Assumptions (Based on Provided Sources):**

*   **NS8 Architecture:** NethServer 8 operates primarily as a **Container Orchestrator**. Most core services and third-party applications run as containerized **Apps**. NS8's main role is managing the lifecycle and configuration of these Apps [1].
*   **NethSecurity Role:** Advanced gateway and firewall features (like complex rules, Quality of Service (QoS), network zones, integrated VPN servers with account provider integration, Multi-WAN) are *not* part of NS8's core. These functions are handled by the separate **NethSecurity** project ([https://nethsecurity.org/](https://nethsecurity.org/)) [1]. This guide assumes NethSecurity is **not** deployed unless explicitly mentioned.
*   **Operating System:** This guide assumes **Rocky Linux 9** (or a similar RHEL 9 derivative or Debian 12) as the base OS for all nodes.
*   **Network:** We assume a simple, flat network topology (e.g., `192.168.1.0/24`).

---

## Node 1: Reverse Proxy & Host Firewall

*   **IP Example:** `192.168.1.10`
*   **Goal:** Act as the entry point for web traffic using the built-in Traefik reverse proxy, manage basic host-level firewall rules, and potentially host a simple VPN solution.

1.  **Install Base OS:** Start with a minimal installation of Rocky Linux 9.
2.  **Set Static IP:** Configure a static IP address using `nmtui` or `nmcli`.
    *   Example: IP `192.168.1.10/24`, Gateway `192.168.1.1`, DNS `192.168.1.11` (pointing to Node 2 once it's up) [2].
3.  **Install NS8 Core:** Download and run the official installation script. **Always obtain the current script URL from the official NS8 documentation [3]**. The command format is generally:
    ```bash
    # Example format - get current URL from docs!
    curl <official-install-script-url> | sudo bash
    ```
4.  **Initial Cluster Creation:** Access the web UI at `https://192.168.1.10/cluster-admin/`. Follow the prompts to **create the initial cluster**. Set the cluster FQDN (e.g., `cluster.lab.local`), confirm the network CIDR, and set the administrator password [3]. This node becomes the first member of the cluster.
5.  **Configure Host Firewall (Basic):** NS8 uses a **"Minimal: Firewalld"** approach for host protection [1]. Open necessary ports using `firewall-cmd` or the Cockpit interface (usually accessible via `https://<IP>:9090`). For web traffic proxied through this node:
    ```bash
    sudo firewall-cmd --add-service=http --permanent
    sudo firewall-cmd --add-service=https --permanent
    sudo firewall-cmd --reload
    ```
    *Note:* Remember, complex firewalling requires **NethSecurity** [1].
6.  **Configure Reverse Proxy (Traefik):** NS8 utilizes Traefik, configured primarily via **"HTTP Routes"** defined within the NS8 UI, typically under App settings or a dedicated Proxy section [1, 4]. Routes are automatically managed for most installed NS8 Apps.
    *Note:* Proxying external services (e.g., custom containers, services on other machines) typically requires manual Traefik configuration files (e.g., `.yaml` or `.toml` placed in a designated directory), bypassing the standard NS8 UI management [1]. This is considered an advanced topic.
7.  **Configure VPN (Limited Options):** NS8 Core does not include integrated VPN servers like OpenVPN or WireGuard out-of-the-box. Manual OS-level VPN setups are generally unsupported via the UI [1]. Based on the NS7/NS8 comparison [1], options include:
    *   **`wg-easy` App:** Install this third-party WireGuard App from the Software Center. *Limitation:* It lacks integration with NS8 Account Providers (users must be managed separately within the app).
    *   **NethSecurity:** Deploying NethSecurity provides robust **OpenVPN Roadwarrior** capabilities fully integrated with account providers.
    *   **(Manual Container):** Advanced users could deploy and manage their own VPN solution in a container, but this falls outside standard NS8 App management.

—

## Node 2: Active Directory, DNS & DHCP

*   **IP Example:** `192.168.1.11`
*   **Goal:** Provide Active Directory (AD) authentication services, internal DNS resolution, and optionally DHCP services using NS8 Apps.

1.  **Install Base OS & Set Static IP:** Follow the same steps as Node 1 (Steps 1 & 2). Set a static IP (e.g., `192.168.1.11/24`). Initially, point its DNS to your router (e.g., `192.168.1.1`) or an external resolver.
2.  **Install NS8 Core:** Follow the same step as Node 1 (Step 3) to install the core components.
3.  **Join Existing Cluster:** Access this node’s web UI at `https://192.168.1.11/`. Instead of creating a new cluster, choose the option to **join an existing cluster**. You will likely need to provide the address of an existing cluster member (e.g., Node 1’s IP or FQDN) and the cluster administrator credentials set during Node 1’s setup [3].
4.  **Install Account Provider (Active Directory):** From the NS8 Software Center, install the **”Samba Active Directory”** App. During setup, configure your AD domain name (e.g., `ad.lab.local`) and administrator password [5].
    *   *Important Limitations [1]:*
        *   AD Replication: Joining multiple instances of this App for replication **does not automatically synchronize SysVol or Group Policies (GPOs)** between them. This is a significant limitation compared to traditional AD replication and impacts high availability strategies for GPOs and logon scripts. Manual procedures might be required for full redundancy.
        *   Local OpenLDAP Alternative: If you choose the local OpenLDAP provider instead of AD, be aware it’s typically **not accessible to services outside the NS8 cluster** [1].
5.  **Configure DNS:** DNS resolution for your internal network can be provided by:
    *   The **”AD Account Provider” App** itself (integrates AD zones automatically).
    *   A separate **”DNSMasq” App** [1].
    Configure clients and other NS8 nodes to use this node’s IP (`192.168.1.11`) for DNS. (Alternatively, NethSecurity also offers DNS services [1]).
6.  **Configure DHCP:** If needed, install the **”DNSMasq” App** [1] to provide DHCP services. Configure the DHCP scope, lease times, default gateway (e.g., `192.168.1.1`), and DNS server (this node’s IP, `192.168.1.11`) within the App’s UI. Remember to disable any other DHCP server (like on your router) on the network segment. (Alternatively, NethSecurity also offers DHCP services [1]). Consult the specific App’s documentation for detailed configuration steps.

—

## Node 3: File Sharing & Collaboration

*   **IP Example:** `192.168.1.12`
*   **Goal:** Host Nextcloud for collaboration and standard SMB/CIFS file shares, integrating with the AD on Node 2.

1.  **Install Base OS & Set Static IP:** Follow Steps 1 & 2 from Node 1. Set a static IP (e.g., `192.168.1.12/24`). Configure its DNS to point to Node 2 (`192.168.1.11`).
2.  **Install NS8 Core:** Follow Step 3 from Node 1.
3.  **Join Existing Cluster:** Follow Step 3 from Node 2 to join this node to the cluster.
4.  **Install Nextcloud App:** Install the official **”Nextcloud”** App from the Software Center. During configuration, connect it to the external Active Directory account provider running on Node 2 [6]. In the App’s Proxy settings [4, 6], define the FQDN for accessing Nextcloud (e.g., `cloud.lab.local`). Ensure a DNS A record exists (on Node 2) pointing `cloud.lab.local` to the IP of the Reverse Proxy (Node 1: `192.168.1.10`).
    *Note:* Automatic configuration/discovery for CalDAV and CardDAV clients **is unconfirmed** in the NS8 context according to the comparison document [1]; manual client configuration might be necessary. Consult the Nextcloud App’s documentation for specifics.
5.  **Install File Server App (SMB):** Install the **”File Server”** App to provide SMBv2/v3 shares integrated with the AD account provider [1]. Configure shared folders and permissions through the App’s UI. Consult the specific App’s documentation for detailed configuration steps.
    *   *Limitations [1]:*
        *   **Recycle Bin:** Enabling the recycle bin feature for shares requires **Command Line Interface (CLI)** configuration. Refer to community guides linked in the source comparison [1].
        *   **Access Control Lists (ACLs):** UI-based permission management is primarily **”limited to a group”**. Applying fine-grained ACLs typically requires using **”3rd-party tools”** on the command line (e.g., `setfacl`) [1].

—

## Node 4: Business Applications Platform

*   **IP Example:** `192.168.1.13`
*   **Goal:** Host various web-based business applications (e.g., Typo3 CMS, Redmine project management) leveraging NS8’s container orchestration capabilities.

1.  **Install Base OS & Set Static IP:** Follow Steps 1 & 2 from Node 1. Set a static IP (e.g., `192.168.1.13/24`). Configure its DNS to point to Node 2 (`192.168.1.11`).
2.  **Install NS8 Core:** Follow Step 3 from Node 1.
3.  **Join Existing Cluster:** Follow Step 3 from Node 2 to join this node to the cluster.
4.  **Install Web Server (LEMP App):** Since NS8 is a **”Container Orchestrator”** [1], you install a containerized web stack as an App. Look for a suitable **”LEMP” App** (Linux, Nginx, MariaDB/MySQL, PHP) or similar stack in the Software Center (this might be from NethForge or other third-party repositories) [1]. **Verify availability and specific features in the Software Center**. Install the chosen App and configure PHP versions, Nginx virtual hosts, database settings, etc., *within* this App according to its specific documentation [1].
5.  **Deploy Applications:**
    *   Place your application code (Typo3, Redmine) into the appropriate web root directory exposed as a volume by the LEMP App.
    *   Configure databases for your applications within the MariaDB/MySQL instance running inside the LEMP App container.
    *   Follow the specific documentation for the chosen LEMP App and your applications [1].
    *   *Container Focus [1]:* For complex applications, deploying them using their official Docker images might be preferable. However, integrating and managing custom containers seamlessly within the NS8 UI/API framework isn’t explicitly detailed in the source material [1] and may require manual Docker/Podman commands or custom orchestration configurations.
6.  **Configure SFTP Access (SFTPGo App):** For secure file transfers, install the **`SFTPGo` App** [1]. Configure users, permissions, storage backends, and restrictions within the SFTPGo App’s interface for granular control [1]. Consult the specific App’s documentation for detailed configuration steps.
7.  **Configure Firewall (Host):** Only open ports directly on Node 4’s host firewall (`firewall-cmd` or Cockpit) if services need direct external access *not* going through the Node 1 reverse proxy. Most web traffic should be directed to Node 1.
8.  **Integrate with AD (Manual/App-Specific):** Configure individual applications (e.g., within Typo3’s backend or Redmine’s administration settings) to use LDAP authentication against the Active Directory server on Node 2, if the application supports it. This typically requires providing the LDAP server address (`192.168.1.11`), base DN, and potentially installing LDAP client tools within the application’s container environment.
9.  **Reverse Proxy Access (Configure on Node 1):** On Node 1 (the Reverse Proxy), configure **”HTTP Routes”** [4] via the NS8 UI. Point specific FQDNs (e.g., `typo3.lab.local`, `redmine.lab.local`) to the internal services running on Node 4 (e.g., `http://192.168.1.13:<LEMP_App_Port>`). As noted earlier, managing routes for non-NS8 managed containers/services might require manual Traefik configuration [1]. Ensure DNS A records exist (on Node 2) pointing these FQDNs to the IP of Node 1 (`192.168.1.10`).

—

## Summary

This multi-node setup illustrates how NethServer 8’s container-based, App-centric architecture can be used to build a modular server environment based on the provided scenario. It leverages specific Apps for core functionalities, relies on Traefik (via HTTP Routes) for proxied access, utilizes minimal host firewalls, and clearly distinguishes its role from the more comprehensive network security features offered by the NethSecurity project. Understanding these architectural differences [1] and the specific limitations noted is key to successfully deploying and managing NS8.

Always refer to the official NethServer 8 documentation and community resources for the latest information, detailed App configurations, and potential updates to features and limitations, especially considering that some source information [1] was marked as work-in-progress.

**References:**

\[1] NS7 vs NS8 Feature Comparison (Work In Progress): [https://community.nethserver.org/t/wip-ns7-vs-ns8-feature-comparison/23258](https://community.nethserver.org/t/wip-ns7-vs-ns8-feature-comparison/23258) \
\[2] OS Network Setup Documentation: [https://docs.nethserver.org/projects/ns8/en/latest/os_network.html](https://docs.nethserver.org/projects/ns8/en/latest/os_network.html) \
\[3] NS8 Installation Guide: [https://docs.nethserver.org/projects/ns8/en/latest/install.html](https://docs.nethserver.org/projects/ns8/en/latest/install.html) \
\[4] NS8 Proxy App Documentation: [https://docs.nethserver.org/projects/ns8/en/latest/proxy.html](https://docs.nethserver.org/projects/ns8/en/latest/proxy.html) \
\[5] NS8 User Domains Documentation: [https://docs.nethserver.org/projects/ns8/en/latest/user_domains.html](https://docs.nethserver.org/projects/ns8/en/latest/user_domains.html) \
\[6] NS8 Nextcloud App Documentation: [https://docs.nethserver.org/projects/ns8/en/latest/nextcloud.html](https://docs.nethserver.org/projects/ns8/en/latest/nextcloud.html)