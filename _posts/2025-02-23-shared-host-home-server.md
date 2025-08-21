---
tags: [scratchpad]
info: aberto.
date: 2025-02-23
type: post
layout: post
published: true
slug: shared-host-home-server
title: 'shared host + home server'
---
Use the shared host as your primary platform for public web capabilities, centralizing management in DirectAdmin, and offload specialized or resource‑intensive tasks to your Debian home server. This approach maximizes the features you’ve paid for while preserving flexibility.

Core use of the shared host
- Websites and deployment
  - Use DirectAdmin for your public‑facing sites and one‑click deployments (e.g., WordPress, Joomla) via the Enriched App Installer where available.
  - Store and serve static files, images, and downloads from the shared host to benefit from its potentially faster CDN or caching features.
- Domain and SSL
  - Let the shared host control DNS (zones, subdomains, email routing).
  - Ensure SSL certificates are active for the main domain and all subdomains.
- Security Center and platform features
  - Enable and monitor the Security Center (automatic DDoS protection, antivirus/antimalware, web application firewall).
  - Leverage daily and weekly remote backups (2,000+ km away) and restore using Jetbackup tools in DirectAdmin.

Subdomains for organization and compatibility
- In DirectAdmin (Domain Setup → Create Subdomain), create subdomains (e.g., blog.example.com, dev.example.com) and manage each as a mini‑site with its own docroot, SSL, and, if permitted, custom Nginx directives.
- If supported, assign different PHP versions per subdomain using Multiple Hardened Versions to meet varied application requirements.

Integrating the Debian home server
- When to use Debian
  - Run applications requiring root access, custom packages, or technologies not supported on shared hosting (e.g., Docker/Incus, specialized databases, advanced caching).
  - Offload CPU/RAM/disk‑intensive or long‑running jobs (e.g., continuous data processing, media conversions) to avoid stressing shared host limits.
- Lightweight, easy‑to‑integrate examples
  - PrivateBin (minimalist pastebin for sensitive notes), tt‑rss (RSS aggregator), syncthing (file sync).
- Home networking prerequisites
  - If behind a home router, configure port forwarding (typically 80/443) and consider dynamic DNS if your IP changes. Use Let’s Encrypt certificates and firewall rules for any publicly accessible service.

Interoperation patterns (host ↔ Debian)
- Data exchange and triggers
  - Use secure APIs or scheduled tasks (cron + SSH/scp), and have the shared host trigger URLs on Debian (cron or webhooks) to enqueue or run specialized jobs.
- DNS routing to Debian
  - For services that must resolve to Debian (e.g., specializedapp.example.com), create an A or CNAME record to point to the Debian server’s public IP or dynamic DNS.
- Reverse proxy via shared host (use with caution)
  - First confirm with your hosting provider whether custom Nginx includes/location directives are permitted in DirectAdmin. If disallowed, use a subdomain instead.
  - If permitted, add a proxy location on the main domain and test end‑to‑end. Example:
    ```nginx
    location /my-special-app/ {
      proxy_pass https://your-debian-ip-or-ddns/;
      proxy_set_header Host $host;
      proxy_redirect off;
    }
    ```
  - After configuring, place a simple test file on Debian and access it via the proxied path. If errors persist, recheck settings or fall back to a subdomain pointing directly at Debian.

Backups, synchronization, and restoration
- Host‑side protection
  - Use built‑in backups and Jetbackup’s remote snapshots (2,000+ km away) as primary restore points.
  - Mirror critical backups from the host to Debian via cron (e.g., scp/rsync) for offsite redundancy under your control.
- Debian‑side synchronization
  - For large media or datasets hosted on Debian, optionally sync to the shared host (rsync or FTP) so visitors benefit from host‑side delivery.
- Restoration steps
  - Shared host: Restore via DirectAdmin’s tools or contact provider support; if you maintain an authorized restore script, follow provider policies.
  - Debian: Reinstall the OS and services if needed, then restore data/configurations from your backups.

Security and maintenance
- Shared host
  - Keep one‑click‑installed apps and platform components updated; enforce HTTPS everywhere; use strong, unique passwords for DirectAdmin and SFTP.
  - Keep WAF and malware scanning active; review logs and security dashboards regularly.
- Debian
  - Restrict exposure with firewall rules (ufw/iptables) and enable intrusion prevention (fail2ban).
  - Disable password authentication and use SSH key‑based access only.
  - Keep the system patched:
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```
  - Use valid TLS certificates (e.g., Let’s Encrypt) for all public endpoints.

Monitoring, limits, and scaling
- Observe host limits and health
  - Monitor physical memory (e.g., 2 GB) and inode usage (e.g., 250,000), along with logs and resource graphs in DirectAdmin.
- Optimize and plan growth
  - Offload heavy analytics/conversions/background jobs to Debian as needs grow.
  - Where available, use staging sites, caching features, or installed modules; remember “unlimited” resources often have fair usage policies.
  - If concurrency/performance needs outgrow the shared plan, evaluate a VPS or dedicated upgrade.
