---
tags: [scratchpad]
info: aberto.
date: 2025-05-25
type: post
layout: post
published: true
slug: coolice-remote-access-and-file-transfer-sshftp
title: 'coolice remote access and file transfer (ssh/ftp)'
---
**Section 0: Immediate Steps to Secure Your Server Access After Key Compromise**

1.  **Generate a NEW SSH Key Pair on Your LOCAL (Client) Machine:**
    *   Open a terminal on your local computer (the one you use to connect *to* the server).
    *   Use the `ssh-keygen` command. It’s recommended to use Ed25519 keys, or RSA with sufficient bit length.
        *   **For Ed25519 (recommended):**
            ```bash
            ssh-keygen -t ed25519 -C “your_email@example.com”
            ```
        *   **Or, for RSA (4096 bits):**
            ```bash
            ssh-keygen -t rsa -b 4096 -C “your_email@example.com”
            ```
    *   When prompted, you can choose to save the key in the default location (e.g., `~/.ssh/id_ed25519` or `~/.ssh/id_rsa`) or specify a new file.
    *   **IMPORTANT:** When prompted for a passphrase, enter a strong, unique passphrase. This encrypts your new private key on your disk, providing an extra layer of security. You’ll need to enter this passphrase when you use the key, unless you use `ssh-agent`.

2.  **Secure Your NEW Private Key File on Your Local Machine:**
    *   The `ssh-keygen` command usually sets the correct permissions, but verify them. The private key file (e.g., `~/.ssh/id_ed25519`) should only be readable by you:
        ```bash
        chmod 600 ~/.ssh/your_new_private_key_filename
        ```

3.  **Copy Your NEW Public Key to the Server (`dc2.myusadc.com`):**
    *   The easiest way is to use `ssh-copy-id` (if available on your client machine). Replace `your_new_public_key.pub` with the actual filename (e.g., `~/.ssh/id_ed25519.pub`):
        ```bash
        ssh-copy-id -i ~/.ssh/your_new_public_key.pub ibbsbbry@dc2.myusadc.com
        ```
        You will be prompted for `ibbsbbry`’s password on `dc2.myusadc.com` for this one-time operation.
    *   **Manual Method (if `ssh-copy-id` is not available):**
        1.  Display your new public key on your local machine:
            ```bash
            cat ~/.ssh/your_new_public_key.pub
            ```
        2.  Copy the entire output (it’s one long line starting with `ssh-ed25519 ...` or `ssh-rsa ...`).
        3.  Log in to your server `dc2.myusadc.com` using your existing method (e.g., password, or the old key if it still works temporarily).
        4.  On the server, open the `~/.ssh/authorized_keys` file with a text editor (like `nano` or `vim`):
            ```bash
            nano ~/.ssh/authorized_keys
            ```
        5.  Paste the new public key you copied onto a new line in this file. Save and close the file.
        6.  Ensure correct permissions on the server:
            ```bash
            chmod 700 ~/.ssh
            chmod 600 ~/.ssh/authorized_keys
            ```

4.  **Test Login with Your NEW Key:**
    *   From your local machine, try to SSH into the server using your new key. If you set a passphrase, you’ll be prompted for it.
        ```bash
        ssh -i ~/.ssh/your_new_private_key_filename ibbsbbry@dc2.myusadc.com
        ```
        If it works, proceed to the next step.

5.  **Remove the COMPROMISED Public Key from the Server:**
    *   Log in to `dc2.myusadc.com` (preferably with your new key).
    *   Edit the `~/.ssh/authorized_keys` file again:
        ```bash
        nano ~/.ssh/authorized_keys
        ```
    *   Carefully find and delete the line corresponding to the old, compromised public key (the one starting with `ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDHVjjq...`).
    *   Save and close the file.

6.  **Delete the COMPROMISED Private Key:**
    *   Delete the private key file that you accidentally shared from wherever it was stored.
    *   If this key was also stored on your client machine, delete it from there as well.

Once these steps are completed, your server access will be secured with your new, uncompromised SSH key pair.

—

Now, here is the tutorial on how to leverage your server information for remote connections and file transfers, assuming you are using your **new, secure SSH keys**.

**Section 1: Understanding Your Server Information (Recap)**

Based on your command outputs, here’s what we know about your server:

*   **Your Username on the Server:** `ibbsbbry`
*   **Server Hostname:** `dc2.myusadc.com`
*   **Server IP Address (Public):** `15.204.42.250`
*   **Your (Compromised) SSH Public Key on Server:** The one you listed, starting with `ssh-rsa AAAAB3NzaC...`. **This should be removed as per Section 0.**
*   **SSH Port:** Assumed to be the default, port `22`. If it’s different, you’ll need to specify it in your commands.

**Section 2: Connecting Remotely with SSH (Secure Shell)**

SSH allows secure command-line access to your server.

**Prerequisites:**
*   **SSH Client on Your Local Machine:**
    *   **Linux/macOS:** OpenSSH client is usually pre-installed. Use the `Terminal`.
    *   **Windows:**
        *   Windows 10/11: OpenSSH client can be installed via “Optional Features” or use PowerShell.
        *   Alternatively, use a third-party client like PuTTY.
*   **Your NEW Secure SSH Key Pair:** Generated and configured as per Section 0.

**2.1. Key-Based Authentication (Recommended & Most Secure)**

This uses your private key (on your local client machine) and its corresponding public key (in `~/.ssh/authorized_keys` on the server).

1.  **Ensure Your NEW Public Key is in `authorized_keys` on the Server:** Done in Section 0, Step 3.
2.  **Ensure Your NEW Private Key is Secure on Your Client Machine:**
    *   Stored in a known location (e.g., `~/.ssh/id_ed25519`).
    *   Has correct permissions: `chmod 600 ~/.ssh/your_new_private_key_filename`.
3.  **Connecting:**

    *   **From Linux/macOS Terminal, or Windows PowerShell (with OpenSSH client):**
        Use the server’s hostname or IP address. If your private key is not the default (`~/.ssh/id_rsa` or `~/.ssh/id_ed25519`), or if you have multiple keys, specify it with the `-i` option.
        ```bash
        # If your new key is the default and loaded by the agent or has no passphrase
        ssh ibbsbbry@dc2.myusadc.com
        # OR using IP
        ssh ibbsbbry@15.204.42.250
        # OR specifying your new private key file
        ssh -i ~/.ssh/your_new_private_key_filename ibbsbbry@dc2.myusadc.com
        ```
        **If using a non-standard SSH port (e.g., 2222):**
        ```bash
        ssh -i ~/.ssh/your_new_private_key_filename -p 2222 ibbsbbry@dc2.myusadc.com
        ```
        The first time you connect to a new server, you’ll be asked to verify the host’s fingerprint. Type `yes`. If you used a passphrase for your private key, you’ll be prompted to enter it.

    *   **From Windows using PuTTY:**
        1.  Open PuTTY.
        2.  **Session Tab:**
            *   Host Name (or IP address): `dc2.myusadc.com` or `15.204.42.250`
            *   Port: `22` (or your non-standard port).
        3.  **Connection > SSH > Auth Tab:**
            *   Click “Browse...” next to “Private key file for authentication”.
            *   Select your **new** private key file. PuTTY uses the `.ppk` format. If your new key is in OpenSSH format (e.g., `id_ed25519`), you’ll need to convert it using **PuTTYgen** (comes with PuTTY). Open PuTTYgen, load your OpenSSH private key file, and then “Save private key” as a `.ppk` file.
        4.  (Optional) Go back to “Session”, name your session under “Saved Sessions”, and click “Save”.
        5.  Click “Open”. You’ll be prompted for your username (`ibbsbbry`) and then your private key’s passphrase if it has one.

**2.2. Using `ssh-agent` for Convenience (Optional)**

If your private key has a passphrase, `ssh-agent` can store the decrypted key in memory, so you only need to enter the passphrase once per session.

1.  **Start `ssh-agent` (usually starts automatically on modern systems):**
    ```bash
    eval “$(ssh-agent -s)”
    ```
2.  **Add your new private key to the agent:**
    ```bash
    ssh-add ~/.ssh/your_new_private_key_filename
    ```
    You’ll be prompted for the key’s passphrase once. Now, subsequent `ssh`, `scp`, `sftp` commands using this key won’t ask for the passphrase until the agent stops or the key is removed.

**2.3. Password Authentication (Less Secure - Discouraged if Key Auth is Set Up)**

If key authentication fails or is not configured, and if the server allows password authentication (often disabled for security), you might be prompted for `ibbsbbry`’s password.
```bash
ssh ibbsbbry@dc2.myusadc.com
```
It’s highly recommended to disable password authentication on your server once key-based authentication is working reliably.

**Section 3: Transferring Files Securely**

Always use secure methods like SFTP or SCP, which leverage your SSH connection. **Avoid plain FTP as it’s insecure.**

**3.1. SFTP (SSH File Transfer Protocol) - Interactive Session**

*   **From Linux/macOS Terminal, or Windows PowerShell:**
    ```bash
    sftp ibbsbbry@dc2.myusadc.com
    # OR, if using a non-standard port (e.g., 2222) and specific key:
    sftp -i ~/.ssh/your_new_private_key_filename -P 2222 ibbsbbry@dc2.myusadc.com
    # Note: OpenSSH sftp client often uses -oPort= for non-standard ports:
    # sftp -i ~/.ssh/your_new_private_key_filename -oPort=2222 ibbsbbry@dc2.myusadc.com
    ```
    Common SFTP commands at the `sftp>` prompt:
    *   `put /local/path/file.txt [/remote/path/file.txt]`: Upload.
    *   `get /remote/path/file.txt [/local/path/file.txt]`: Download.
    *   `lpwd`, `pwd`, `lls`, `ls`, `lcd`, `cd`, `mkdir`, `rm`, `help`, `exit`.

*   **From Windows using a GUI client (e.g., WinSCP, FileZilla):**
    1.  **WinSCP:**
        *   File protocol: `SFTP`
        *   Host name: `dc2.myusadc.com`
        *   Port number: `22` (or your custom port)
        *   User name: `ibbsbbry`
        *   For key auth: Click “Advanced...” > “SSH” > “Authentication”, select your **new** `.ppk` private key file.
        *   Login.
    2.  **FileZilla:**
        *   Host: `sftp://dc2.myusadc.com` (prefix with `sftp://`)
        *   Username: `ibbsbbry`
        *   Port: `22` (or your custom port)
        *   For key auth: `Edit > Settings > Connection > SFTP`, add your **new** private key file (OpenSSH format or `.ppk` often works).
        *   Quickconnect or use Site Manager.

**3.2. SCP (Secure Copy Protocol) - Direct File Copy**

*   **From Linux or macOS Terminal, or Windows PowerShell:**

    *   **Local to Server:**
        ```bash
        scp -i ~/.ssh/your_new_private_key_filename /path/to/local/file.txt ibbsbbry@dc2.myusadc.com:/remote/path/
        # If using a non-standard port (e.g., 2222), use uppercase -P:
        scp -i ~/.ssh/your_new_private_key_filename -P 2222 /path/to/local/file.txt ibbsbbry@dc2.myusadc.com:/remote/path/
        ```
    *   **Server to Local:**
        ```bash
        scp -i ~/.ssh/your_new_private_key_filename -P 2222 ibbsbbry@dc2.myusadc.com:/remote/path/file.txt /local/path/
        ```
    *   **Copy directories recursively with `-r`:**
        ```bash
        scp -r -i ~/.ssh/your_new_private_key_filename -P 2222 /local/directory ibbsbbry@dc2.myusadc.com:/remote/parent_directory/
        ```

**3.3. `rsync` (Advanced File Synchronization)**

`rsync` is powerful for efficiently synchronizing files and directories. It only transfers differences, can resume, and preserves permissions.

*   **Local to Server (archive mode, verbose, compress, progress):**
    ```bash
    rsync -avz —progress -e “ssh -i ~/.ssh/your_new_private_key_filename -p 2222” /path/to/local/source/ ibbsbbry@dc2.myusadc.com:/path/to/remote/destination/
    ```
    (Note the trailing slash on the source `/path/to/local/source/` means “copy the contents of source”).
*   **Server to Local:**
    ```bash
    rsync -avz —progress -e “ssh -i ~/.ssh/your_new_private_key_filename -p 2222” ibbsbbry@dc2.myusadc.com:/path/to/remote/source/ /path/to/local/destination/
    ```

**Section 4: Important General Considerations**

*   **Server-Side Firewall:** Ensure the firewall on `dc2.myusadc.com` (e.g., `ufw`, `firewalld`) allows incoming connections on your SSH port (default 22).
*   **SSH Server Configuration (`sshd_config`):** Located at `/etc/ssh/sshd_config` on the server. Key settings include:
    *   `Port 22` (or your custom port)
    *   `PubkeyAuthentication yes` (essential for key auth)
    *   `PasswordAuthentication no` (recommended once key auth is solid)
    *   `PermitRootLogin no` (recommended)
    If you change `sshd_config`, restart the SSH service (e.g., `sudo systemctl restart sshd`).
*   **Client-Side Private Key Security:** Reiterating: protect your new private key. Use a strong passphrase.

**Section 5: Basic SSH Troubleshooting**

*   **`Connection refused` on port 22 (or custom port):**
    *   Is the server `dc2.myusadc.com` online and reachable (try `ping dc2.myusadc.com`)?
    *   Is the SSH service (`sshd`) running on the server? (Check with `sudo systemctl status sshd` on the server).
    *   Is a firewall on the server or network blocking the SSH port?
*   **`Permission denied (publickey,gssapi-keyex,gssapi-with-mic...)`:**
    *   Is your **new** public key correctly added to `~/.ssh/authorized_keys` on the server?
    *   Are permissions correct on the server: `~/.ssh` (700), `~/.ssh/authorized_keys` (600)?
    *   Are permissions correct for your **new** private key on your client machine (600)?
    *   Are you explicitly telling your SSH client to use the correct new private key (e.g., with `ssh -i ~/.ssh/your_new_key`) if it’s not the default or if `ssh-agent` isn’t managing it?
    *   Check SSH server logs on `dc2.myusadc.com` (often in `/var/log/auth.log` or `/var/log/secure`) for more detailed error messages. Use `ssh -v user@host` (verbose) or `-vvv` (very verbose) on the client for more diagnostic output.
*   **Prompted for password unexpectedly:**
    *   The server might not be configured for public key authentication, or your public key setup is incorrect.
    *   `ssh-agent` might not have your key loaded, or you typed the passphrase incorrectly.