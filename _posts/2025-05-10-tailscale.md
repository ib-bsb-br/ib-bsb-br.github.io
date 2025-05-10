---
tags: [aid>linux>software]
info: aberto.
date: 2025-05-10
type: post
layout: post
published: true
slug: tailscale
title: 'Tailscale for secure external SSH access'
---
 * Automated Setup & Auth Keys: Tailscale is often installed and brought online automatically in server environments (e.g., during boot as seen in SBNB's boot-sbnb.sh, or via cloud-init). This is facilitated by Tailscale auth keys (e.g., tailscale up --auth-key=YOUR_KEY), which are treated as secrets and allow non-interactive joining of a machine to your tailnet.
 * Tailscale SSH Enabled: The command tailscale up --ssh (or ensuring the node is configured with SSH enabled via tailscale set --ssh=true) is crucial. This allows Tailscale to:
   * Advertise that the node accepts SSH connections via Tailscale.
   * Manage access control based on your Tailscale network's users and Access Control Lists (ACLs).
 * Identity-Based Access (SSO): With Tailscale SSH, users authenticate using their Tailscale identity (often linked to an SSO provider like Google, Microsoft, Okta, etc., as hinted at by SBNB's mention of "Google Auth"). This centralizes authentication.
 * MagicDNS & Machine Names: Tailscale provides a private DNS service (MagicDNS) that allows you to reach your machines using simple, memorable hostnames (e.g., my-debian-server or my-debian-server.your-tailnet-name.ts.net) instead of just IPs.
How This SBNB-Inspired Tailscale Approach Overcomes Prior Gaps:
 * No Port Forwarding or Static Public IP Needed (Gap Fully Overcome):
   * Tailscale creates an encrypted overlay network. Your Debian machine and your client devices connect to this network and can reach each other using their private Tailscale IPs or MagicDNS names, completely bypassing router configurations for port forwarding or the need for a static public IP on the server's internet connection.
 * Simplified Firewall Management (Significantly Simplified & Enhanced):
   * Router Firewall: No inbound rules needed on your internet router.
   * Debian Machine's Local Firewall (e.g., ufw):
     * While Tailscale handles the encrypted tunnel, the openssh-server daemon on your Debian machine still needs to be able to accept connections. Your local firewall must allow incoming traffic to the SSH port (default 22/tcp). A rule like sudo ufw allow ssh or sudo ufw allow 22/tcp is typically sufficient.
     * Tailscale ACLs provide the primary, fine-grained access control layer. Before a connection even reaches your SSH server for local authentication, Tailscale's ACLs will determine if the source user/device is authorized to attempt an SSH connection to the destination server and as which local user(s).
Impact on the SSH Server and Its Authentication:
 * openssh-server (Still a Core Prerequisite):
   * It's crucial to understand that Tailscale SSH doesn't typically replace openssh-server on your Debian machine. openssh-server is the software that provides the actual shell, manages user sessions, and enforces OS-level permissions.
   * Tailscale SSH authenticates the user via their Tailscale identity and then (in common setups) instructs the local openssh-server (often using ephemeral SSH certificates it generates or by its agent initiating a local connection) that the connection is authorized for a specific local user.
   * Therefore, you must have openssh-server installed and running:
     sudo apt update
sudo apt install openssh-server
sudo systemctl enable ssh # Ensures sshd starts on boot
sudo systemctl start ssh  # Starts sshd immediately

 * SSH Authentication (Managed by Tailscale, Simplified on Server):
   * Traditional ~/.ssh/authorized_keys: When primarily using Tailscale SSH with its identity-based authentication and ACLs, the need to meticulously manage authorized_keys files on each server for users connecting via Tailscale is greatly diminished. You're no longer pre-distributing public keys for every user to every server for Tailscale-brokered access.
   * Tailscale Controls Access: Your Tailscale Admin Console's ACLs become the central point for defining:
     * Who (which Tailscale users or groups) can initiate SSH.
     * To where (which Tailscale machines, often identified by tags).
     * As whom (which local Linux user(s) on the target machine).
   * Your original .bashrc's fixmyhome alias for securing ~/.ssh is still excellent for general system hygiene and for any non-Tailscale SSH access methods or service accounts.
Implementing the SBNB-Inspired Tailscale SSH Approach:
 * On your Debian 11 Server:
   * Install openssh-server (as detailed above).
   * Install Tailscale:
     curl -fsSL https://tailscale.com/install.sh | sh
# This script usually detects Debian and installs appropriately.

   * Obtain a Tailscale Auth Key: Go to your Tailscale Admin Console -> "Settings" -> "Keys". Generate an auth key (reusable, ephemeral, or pre-authorized). Treat this key like a password; it's a secret.
   * Join Tailscale & Enable SSH:
     sudo tailscale up \
    --auth-key=YOUR_TAILSCALE_AUTH_KEY \
    --ssh \
    --hostname=my-debian-server # Optional: sets a nice Tailscale hostname
    # --advertise-tags=tag:debian-servers,tag:prod # Optional: for ACLs

     Running tailscale up --ssh tells your Tailscale control plane that this node can be an SSH server. This setting is generally remembered by the node for future connections to the control plane. The SBNB boot-sbnb.sh runs this on boot to ensure it's active. You can also use sudo tailscale set --ssh after an initial up to manage this setting.
 * In Your Tailscale Admin Console (https://www.google.com/search?q=admin.tailscale.com):
   * Verify Machine: Confirm your "my-debian-server" appears in the "Machines" list. You might need to explicitly enable SSH for the machine here if you didn't use --ssh during up and haven't used tailscale set --ssh.
   * Define SSH Access Controls (ACLs): This is critical. Go to "Access Controls". Example ACL entries for SSH:
     {
  // ... other ACLs ...
  "ssh": [
    // Allow members of "dev-group" to SSH to any server tagged "tag:debian-servers"
    // as the "linaro" user, or as themselves if they are not root (autogroup:nonroot).
    {
      "action": "accept",
      "src":    ["autogroup:dev-group"],
      "dst":    ["tag:debian-servers"],
      "users":  ["linaro", "autogroup:nonroot"]
    },
    // Allow a specific user "alice@example.com" to SSH to "my-debian-server"
    // as the "linaro" user.
    {
      "action": "accept",
      "src":    ["alice@example.com"],
      "dst":    ["my-debian-server"], // Use Tailscale hostname
      "users":  ["linaro"]
    }
  ]
}

     * autogroup:nonroot: A special group that allows authenticated Tailscale users to log in as their own username on the target machine, provided that username exists and is not root.
     * Thoroughly review Tailscale's documentation on SSH ACLs.
 * On Your Client Machine (where you SSH from):
   * Install Tailscale: (e.g., curl -fsSL https://tailscale.com/install.sh | sh)
   * Log in to Tailscale:
     sudo tailscale up
# This typically opens a browser for you to authenticate to your Tailscale account.

   * Connect via SSH:
     You can use Tailscale's CLI, which directly understands Tailscale SSH:
     tailscale ssh linaro@my-debian-server

     Or, if your local SSH client is configured (or by default if MagicDNS is working well), standard SSH might also work:
     ssh linaro@my-debian-server

     Using tailscale ssh ... is often preferred as it explicitly uses Tailscale's SSH mechanisms.
