---
tags: [scratchpad]
info: aberto.
date: 2025-04-19
type: post
layout: post
published: true
slug: setting-up-ssh-key-based-authentication-on-debian
title: 'Setting Up SSH Key-Based Authentication on Debian'
---
## Prerequisites

### 1. SSH Server

Ensure the OpenSSH server is installed and running on your Debian server:

# Update package list
```
sudo apt update
```
# Install SSH server if not present
```
sudo apt install openssh-server
```
# Check SSH service status
```
sudo systemctl status sshd
```

If it's not active (running), start and enable it to run on boot:
```
sudo systemctl start sshd
```

```
sudo systemctl enable sshd
```

2. SSH Key Pair
You need an SSH key pair on your client machine (the one you'll connect from).
Generate Keys (if you don't have them):
# Recommended: Ed25519 (modern and secure)
```
ssh-keygen -t ed25519
```
# Or: RSA (widely compatible, use 4096 bits)
```
# ssh-keygen -t rsa -b 4096
```

Follow the prompts. You can optionally add a passphrase for extra security. This typically creates:
`~/.ssh/id_ed25519` or `~/.ssh/id_rsa` (Private Key - Never share this file. It's your private identity. Adding a passphrase encrypts this file on your disk, providing an extra layer of security if someone gains access to your client machine.)
`~/.ssh/id_ed25519.pub` or `~/.ssh/id_rsa.pub` (Public Key - This goes on the server)
Identify your Public Key File: Note the path to your public key file (e.g., `~/.ssh/id_ed25519.pub`).

## Steps on the Debian Server

Let's assume you want to set up key-based login for a user named your_user on the server your_debian_server_ip. Replace these with your actual username and server IP/hostname.

Security Note: While possible, enabling direct root login via SSH (even with keys) is generally discouraged. Prefer logging in as a regular user and using sudo.

Method 1: Using ssh-copy-id (Recommended)
This is the easiest and safest method. It automatically copies the key, creates the necessary directory/file, and sets the correct permissions on the server.

Run ssh-copy-id from your Client Machine:
# Replace with your public key file if not the default
```
ssh-copy-id -i ~/.ssh/your_public_key.pub your_user@your_debian_server_ip
```

# If using the default key (e.g., id_rsa.pub, id_ed25519.pub):
```
ssh-copy-id your_user@your_debian_server_ip
```

Enter Password: You will be prompted for your_user's password on the Debian server one last time.

Done: Your public key is now installed in /home/your_user/.ssh/authorized_keys on the server with the correct permissions.

Method 2: Manual Installation (Alternative)
This method involves manually creating the necessary files and setting permissions on the server. It's useful if ssh-copy-id isn't available or if you prefer manual control.
Use this if ssh-copy-id is unavailable or if you need finer control. Perform these steps on the Debian server, logged in as your_user (or as root, carefully adjusting paths and ownership).
Log in to the Debian Server: Access the server using your current method (e.g., password).
Switch to the Target User (if logged in as another user):
su - your_user


Create the .ssh Directory:
mkdir -p ~/.ssh


Set Permissions for .ssh Directory:
chmod 700 ~/.ssh


Add the Public Key to authorized_keys:
Get the content of your public key file (e.g., cat ~/.ssh/id_ed25519.pub on your client). It's one long line starting with ssh-ed25519 or ssh-rsa.
Paste this public key content into ~/.ssh/authorized_keys on the server.
# Option A: Paste directly using echo (replace 'PASTE_PUBLIC_KEY_CONTENT_HERE')
# Ensure the key is pasted exactly, without line breaks within the key itself.
echo "PASTE_PUBLIC_KEY_CONTENT_HERE" >> ~/.ssh/authorized_keys

# Option B: Use a text editor like nano
# nano ~/.ssh/authorized_keys
# (Paste the key content, save [Ctrl+O], and exit [Ctrl+X])


Important: If the file already exists, ensure the new key is added on a new line.
Set Permissions for authorized_keys File:
chmod 600 ~/.ssh/authorized_keys


(If running as root for another user) Set Ownership: Ensure the user owns the directory and file:
# Run this command as root if you created/modified files in another user's home
# chown -R your_user:your_user /home/your_user/.ssh


Testing the Connection
From your client machine, try logging in via SSH. You should now be logged in using your key, without a password prompt.
ssh your_user@your_debian_server_ip


Firewall Configuration (Common Issue)
If you can't connect, a firewall might be blocking SSH (port 22). If you are using ufw (Uncomplicated Firewall) on the Debian server:
Check Status:
sudo ufw status


Allow SSH (if needed): If SSH (port 22) isn't listed as allowed, add a rule:
# Allow by service name (preferred)
sudo ufw allow ssh

# Or allow by port number
# sudo ufw allow 22/tcp

# Reload ufw if necessary
# sudo ufw reload


Troubleshooting Tips
Verbose SSH Output (Client): Run SSH with -v (or -vv, -vvv for more detail) from your client to see detailed connection steps and errors:
ssh -v your_user@your_debian_server_ip


Check Server Logs (Server): Look for SSH-related messages in the authentication log on the Debian server:
sudo tail -f /var/log/auth.log

(Press Ctrl+C to stop following the log). Look for errors related to permissions, ownership, or key validity when you attempt to connect.
Verify Permissions/Ownership (Server): Double-check the permissions and ownership on the server:
ls -ld ~ ~/.ssh ~/.ssh/authorized_keys

Ensure ~/.ssh is 700 (drwx------) and ~/.ssh/authorized_keys is 600 (-rw-------), and both are owned by your_user. Also check the home directory (~) itself isn't world-writable.
Check SSHD Configuration (Server): Ensure public key authentication is enabled in /etc/ssh/sshd_config:
```
sudo grep -iE 'PubkeyAuthentication|AuthorizedKeysFile' /etc/ssh/sshd_config
```

You should see PubkeyAuthentication yes and likely .ssh/authorized_keys within the AuthorizedKeysFile line. If you change this file, restart SSH:
```
sudo systemctl restart sshd
```
