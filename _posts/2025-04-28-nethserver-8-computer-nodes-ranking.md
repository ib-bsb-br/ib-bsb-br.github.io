---
tags: [scratchpad]
info: aberto.
date: 2025-04-28
type: post
layout: post
published: true
slug: nethserver-8-computer-nodes-ranking
title: 'NethServer 8 computer nodes ranking'
---
Here is the order, starting with the machine needing the most resources:

1.  **Node 3: File Sharing & Collaboration (Nextcloud + File Server App)**
    *   **Reasoning:** Nextcloud is often the most resource-hungry application in such setups. It involves a web server, PHP processing, a database, file indexing, potentially real-time services, thumbnail generation, and significant file I/O. Running background jobs and handling many concurrent users heavily utilizes CPU and RAM. The underlying File Server App also adds demand, especially for Disk I/O during file transfers and potential caching (RAM). This node will likely require the most **RAM**, **CPU** power (especially multi-core), high **Disk I/O** performance (SSDs recommended for Nextcloud data/database), and significant **Disk Space**.
2.  **Node 4: Business Applications Platform (LEMP App + Typo3, Redmine, etc.)**
    *   **Reasoning:** Hosting multiple web applications like Typo3 (CMS) and Redmine (Project Management), each with its own database needs, application logic (PHP, potentially Ruby for Redmine), and web server processes (Nginx + PHP-FPM), creates substantial demand. The resource usage is highly dependent on the specific applications and user traffic but can easily rival or exceed Node 3 under heavy load. It requires significant **RAM** (for databases, application caching, PHP processes), **CPU** power, and good **Disk I/O** performance. Disk space depends on the application data.
3.  **Node 2: Active Directory, DNS & DHCP (Samba AD + DNSMasq App)**
    *   **Reasoning:** Samba Active Directory requires a moderate amount of **RAM** to operate efficiently, especially as the user/object count grows. CPU usage spikes during authentication and searches but is often lower during idle periods compared to busy web applications. Disk I/O is important for the AD database, but typically less demanding than a heavily used file server or application database. DNS and DHCP services (via DNSMasq App) are very lightweight. This node needs a solid RAM baseline and reasonable CPU/Disk I/O.
4.  **Node 1: Reverse Proxy & Host Firewall (Traefik + firewalld + Optional VPN)**
    *   **Reasoning:** In its planned configuration using *minimal* `firewalld` and Traefik primarily for routing web traffic, this node is generally the least demanding. Traefik is efficient, and basic firewalling adds little overhead. CPU/RAM usage scales primarily with network traffic volume and the complexity of proxy rules. Disk I/O is minimal unless heavy caching is enabled. **However**, if you were to run a more demanding VPN (like many concurrent OpenVPN sessions via NethSecurity/manual setup) or implement very complex Traefik middleware/caching, its resource needs would increase significantly. Based *only* on the revised plan using `firewalld` and potentially `wg-easy`, it should be the lightest.

**Summary for Allocation:**

*   **Most Powerful Machine:** Assign to **Node 3 (Nextcloud/File Sharing)**. Prioritize RAM, CPU cores, and fast Disk I/O (SSD).
*   **Second Most Powerful Machine:** Assign to **Node 4 (Business Apps)**. Prioritize RAM, CPU, and good Disk I/O.
*   **Moderate Machine:** Assign to **Node 2 (Active Directory)**. Ensure sufficient RAM baseline.
*   **Least Powerful Machine:** Assign to **Node 1 (Reverse Proxy/Firewall)**. Standard resources should suffice unless high traffic/heavy VPN load is expected.