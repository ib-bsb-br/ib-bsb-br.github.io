---
tags: [scratchpad]
info: aberto.
date: 2025-05-18
type: post
layout: post
published: true
slug: sharing-files-with-miniserve-http-server-and-netbird
title: 'sharing files with `miniserve` HTTP server and `netbird`'
---
### 1. Introduction to `miniserve`

As detailed in its `README.md`, `miniserve` is a "CLI tool to serve files and dirs over HTTP." It's designed to be small, self-contained, and cross-platform, making it ideal for quickly sharing files. Built in Rust, it offers good performance. Key features include serving single files or entire directories, MIME type handling, authentication, folder downloads, file uploading, directory creation, themes, QR code support, TLS, and read-only WebDAV support.

### 2. Prerequisites

*   **RK3588 Device**: An ARM64 device (e.g., Orange Pi 5, Rock 5B).
*   **Operating System**: Debian Bullseye (or compatible) installed.
*   **Basic Linux Knowledge**: Command line, package installation, file editing.
*   **Root/Sudo Access**.
*   **Internet Connectivity**.
*   **`netbird` Account**: You'll need a `netbird.io` account.

---

### 3. Phase 1: RK3588 Debian Bullseye Preparation

Ensure your Debian Bullseye system is ready.

#### System Update
Log in via SSH and run:
```bash
sudo apt update
sudo apt full-upgrade -y
sudo apt autoremove -y
sudo apt clean
# Consider a reboot if kernel updates occurred: sudo reboot
```

#### Essential Tools
Install common utilities if not already present:
```bash
sudo apt install -y curl wget git ca-certificates gnupg
```

---

### 4. Phase 2: `netbird` Installation and Configuration

`netbird` creates a secure peer-to-peer VPN.

#### Install `netbird` Client
The recommended way to install `netbird` on Linux is using their installation script:
```bash
curl -fsSL https://pkgs.netbird.io/install.sh | sudo bash
```
This script will typically detect your OS (Debian), add the necessary repository and GPG key, and install the `netbird` package.

Alternatively, for manual installation, refer to the [official Netbird documentation](https://netbird.io/docs/installation/overview), as steps can change.

#### Log in to `netbird`
Once installed, connect your RK3588 to your `netbird` network:

*   **Method 1: Interactive Login (if you have easy browser access):**
    ```bash
    sudo netbird up
    ```
    This will provide a URL. Open it in a browser on any device, log in to your `netbird` account, and authorize the RK3588.

*   **Method 2: Setup Key (Recommended for headless servers):**
    1.  In your `netbird` admin dashboard (app.netbird.io), go to "Setup Keys."
    2.  Create a new key (reusable or one-time, as needed). Copy the generated key.
    3.  On your RK3588, run:
        ```bash
        sudo netbird up --setup-key YOUR_COPIED_SETUP_KEY
        ```

#### Verify `netbird` Connection & Identify IP
Check the `netbird` status on your RK3588:
```bash
sudo netbird status
```
This command will show if the client is connected and will display its `netbird` IP address (e.g., `100.x.y.z`). Note this IP.
You can also use:
```bash
ip addr show netbird0 # Or the interface name shown by 'netbird status'
```

#### Enable `netbird` Service
Ensure `netbird` starts on boot:
```bash
sudo systemctl enable --now netbird
```

---

### 5. Phase 3: `miniserve` Installation on ARM64

#### Option A: Using Pre-compiled Binaries (Recommended)
`miniserve` provides pre-built `aarch64-unknown-linux-musl` (statically linked, good portability) or `aarch64-unknown-linux-gnu` binaries.

1.  **Find the Latest Release:** Go to `https://github.com/svenstaro/miniserve/releases`.
2.  **Download the ARM64 Binary:**
    On your RK3588 (replace `<VERSION>` and adjust binary name if needed):
    ```bash
    VERSION="0.29.0" # Check for the actual latest version!
    # Choose musl for static linking or gnu
    BINARY_FILENAME="miniserve-${VERSION}-aarch64-unknown-linux-musl"
    # BINARY_FILENAME="miniserve-${VERSION}-aarch64-unknown-linux-gnu"

    cd /tmp
    wget "https://github.com/svenstaro/miniserve/releases/download/v${VERSION}/${BINARY_FILENAME}" -O miniserve-arm64
    ```
3.  **Make Executable and Install:**
    ```bash
    chmod +x miniserve-arm64
    sudo mv miniserve-arm64 /usr/local/bin/miniserve
    ```
4.  **Verify:** `miniserve --version`

#### Option B: Building from Source with `cargo`
1.  **Install Rust & Build Tools:**
    ```bash
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    source "$HOME/.cargo/env" # Or re-login/open new terminal
    sudo apt install -y build-essential pkg-config libssl-dev # For GNU target
    ```
2.  **Install `miniserve`:**
    ```bash
    cargo install --locked miniserve
    ```
    The binary will be in `$HOME/.cargo/bin/miniserve`. Ensure this is in your `PATH` or move the binary to `/usr/local/bin/`.
3.  **Verify:** `$HOME/.cargo/bin/miniserve --version` (or `miniserve --version` if in PATH).

#### Option C: Using Docker
`miniserve` offers multi-arch Docker images.
1.  **Install Docker:**
    The simplest way is often the convenience script:
    ```bash
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker your_user # Add your user to docker group, re-login after
    ```
    Alternatively, follow manual instructions from the [Docker Debian documentation](https://docs.docker.com/engine/install/debian/).
2.  **Run `miniserve`:**
    ```bash
    # Replace /host/path/to/share with the actual path on your RK3588
    docker run -d --name my-miniserve \
      -v /host/path/to/share:/data:ro \
      -p <YOUR_NETBIRD_IP>:<PORT>:8080 \
      --restart unless-stopped \
      docker.io/svenstaro/miniserve /data -p 8080
    ```
    *   `-d`: Run detached.
    *   `--name my-miniserve`: Name the container.
    *   `-v /host/path/to/share:/data:ro`: Mounts your host directory read-only (`:ro`) into the container. Remove `:ro` for uploads.
    *   `-p <YOUR_NETBIRD_IP>:<PORT>:8080`: Binds `miniserve`'s port `8080` inside the container to a specific `<PORT>` on your RK3588's `<YOUR_NETBIRD_IP>`.
    *   `--restart unless-stopped`: For persistence.
    *   `/data -p 8080`: Tells `miniserve` inside the container to serve `/data` on port `8080`.
    *   **Note on Volume Permissions:** If `miniserve` inside Docker (often runs as non-root) can't read `/host/path/to/share`, ensure the host path has appropriate read permissions for the user/group ID `miniserve` runs as in the container, or explore Docker's user mapping options.

*(The rest of this tutorial focuses on non-Docker systemd setup for `miniserve`)*

---

### 6. Phase 4: Running `miniserve`

#### Create a Directory to Serve
```bash
mkdir -p /srv/miniserve_data # Or your preferred location
echo "Hello from miniserve on RK3588 via Netbird!" > /srv/miniserve_data/index.html
sudo chown -R your_user:your_user /srv/miniserve_data # Change 'your_user' if needed
```

#### Manual Test Run (Binding to `netbird` IP)
Replace `<YOUR_NETBIRD_IP>` and `<PORT>` (e.g., 8080).
```bash
miniserve -i <YOUR_NETBIRD_IP> -p <PORT> /srv/miniserve_data
```
Test access from another `netbird` device: `http://<YOUR_NETBIRD_IP>:<PORT>`. Press `CTRL+C` to stop.

#### Setting up `miniserve` as a `systemd` Service

1.  **Obtain and Place the `systemd` Unit File:**
    Create `/etc/systemd/system/miniserve@.service` (ensure `miniserve` binary path is correct):
    ```ini
    [Unit]
    Description=miniserve for %i
    After=network-online.target netbird.service
    Wants=network-online.target netbird.service

    [Service]
    ExecStart=/usr/local/bin/miniserve -- %I # Verify this path to miniserve

    # Security Hardening
    IPAccounting=yes
    # IPAddressAllow/Deny are removed here as miniserve will bind to a specific IP.
    # If miniserve were to bind 0.0.0.0, you'd use IPAddressAllow for Netbird subnet.
    DynamicUser=yes
    PrivateTmp=yes
    PrivateUsers=yes
    PrivateDevices=yes
    NoNewPrivileges=true
    ProtectSystem=strict
    ProtectHome=read-only # Change to 'no' or use a dedicated user if serving from /home
    ProtectClock=yes
    ProtectControlGroups=yes
    ProtectKernelLogs=yes
    ProtectKernelModules=yes
    ProtectKernelTunables=yes
    ProtectProc=invisible
    CapabilityBoundingSet=CAP_NET_BIND_SERVICE CAP_DAC_READ_SEARCH

    [Install]
    WantedBy=multi-user.target
    ```

2.  **Dedicated User for `miniserve` (Optional but Recommended):**
    If `DynamicUser=yes` is problematic for permissions, or you prefer explicit control:
    ```bash
    sudo groupadd --system miniserve-runner
    sudo useradd --system -g miniserve-runner -d /var/empty -s /bin/false miniserve-runner
    ```
    Then, in your systemd override (next step), you'll add `User=miniserve-runner` and `Group=miniserve-runner`.

3.  **Determine and Escape the Path to Serve:**
    Example: For `/srv/miniserve_data`:
    ```bash
    systemd-escape /srv/miniserve_data
    ```
    This might output `srv-miniserve_data`. This is your `<escaped-path>`.

4.  **Create `systemd` Override File for Custom Options:**
    Use `sudo systemctl edit miniserve@<escaped-path>.service`. Add:
    ```ini
    [Service]
    # If using a dedicated user:
    # User=miniserve-runner
    # Group=miniserve-runner

    # Clear default ExecStart
    ExecStart=
    # Set our custom ExecStart. Replace <YOUR_NETBIRD_IP> and <PORT>.
    # Add other miniserve flags as needed (e.g., --auth, -u, --tls-cert).
    ExecStart=/usr/local/bin/miniserve -i <YOUR_NETBIRD_IP> -p <PORT> --title "RK3588 Files" -- %I
    ```
    Ensure `/usr/local/bin/miniserve` is the correct absolute path to your `miniserve` binary.

5.  **File System Permissions for the Served Directory:**
    The user `miniserve` runs as (either dynamic or `miniserve-runner`) needs read access to `/srv/miniserve_data` and its contents.
    If using `miniserve-runner`:
    ```bash
    sudo chown -R miniserve-runner:miniserve-runner /srv/miniserve_data
    sudo chmod -R u=rX,g=rX,o-rwx /srv/miniserve_data # Read/execute for user/group
    ```
    If `DynamicUser=yes` and serving from outside standard system paths (like `/srv`), you might need `setfacl` for more granular permissions if `chown` is not desired, or ensure the path is world-readable (less secure).

6.  **Reload `systemd`, Enable, and Start the Service:**
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable --now miniserve@<escaped-path>.service
    ```

7.  **Check Service Status:**
    ```bash
    sudo systemctl status miniserve@<escaped-path>.service
    sudo journalctl -u miniserve@<escaped-path>.service -f
    ```

---

### 7. Phase 5: Accessing `miniserve` and Other Services via `netbird`

#### Accessing `miniserve`
From another device on your `netbird` network, use your browser:
`http://<YOUR_NETBIRD_IP>:<PORT>` (or `https://` if you configured TLS).

#### Accessing SSH, FTP, etc.
Services like SSH on your RK3588 are now accessible via its `netbird` IP from other peers in your `netbird` network:
```bash
ssh your_rk3588_user@<YOUR_NETBIRD_IP>
```
Similarly for FTP or other services configured to listen on the `netbird` IP or `0.0.0.0`.

---

### 8. Phase 6: Advanced `miniserve` Configuration & Security

#### Key `miniserve` Features
Consult `miniserve --help` and the `README.md`.
*   **Authentication:** `--auth username:password` or `--auth-file /path/auth.txt`. Highly recommended.
    Example for systemd override: `ExecStart=... --auth "admin:$(openssl passwd -1 'securepass')" -- %I`
*   **TLS (HTTPS):** `--tls-cert /path/cert.pem --tls-key /path/key.pem`.
    See "TLS Certificate Generation with SAN" below.
*   **File Uploads:** `-u` or `-u /allowed/subdir`. Use with caution regarding permissions.
*   **Directory Creation:** `--mkdir` (requires uploads).
*   **WebDAV:** `--enable-webdav` for read-only WebDAV access. This can be a good alternative to FTP for file management over HTTP.

#### TLS Certificate Generation with SAN
For self-signed certificates to work well with modern browsers (even over `netbird`), include a Subject Alternative Name (SAN) for the IP.
1.  Create a directory for certs: `sudo mkdir -p /etc/miniserve/tls; cd /etc/miniserve/tls`
2.  Generate key and cert (replace `<YOUR_NETBIRD_IP>`):
    ```bash
    sudo openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem \
      -sha256 -days 3650 -nodes \
      -subj "/CN=<YOUR_NETBIRD_IP>" \
      -addext "subjectAltName = IP:<YOUR_NETBIRD_IP>"
    ```
3.  Set permissions (if `miniserve` runs as `miniserve-runner`):
    ```bash
    sudo chown -R miniserve-runner:miniserve-runner /etc/miniserve/tls
    sudo chmod 600 /etc/miniserve/tls/key.pem
    sudo chmod 644 /etc/miniserve/tls/cert.pem
    ```
4.  Update your systemd override `ExecStart` with:
    `--tls-cert /etc/miniserve/tls/cert.pem --tls-key /etc/miniserve/tls/key.pem`
5.  Access via `https://<YOUR_NETBIRD_IP>:<PORT>`. You'll need to accept the self-signed certificate warning in your browser.

#### Firewall (UFW on RK3588)
```bash
sudo apt install -y ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh # Essential for remote access
# Allow miniserve port ONLY from Netbird interface (e.g., netbird0)
sudo ufw allow in on netbird0 to any port <PORT> proto tcp 
sudo ufw enable
sudo ufw status verbose
```

#### `netbird` Access Controls
Utilize `netbird`'s dashboard to create access policies, restricting which peers can connect to your RK3588 and on which ports/protocols for fine-grained security.

#### Regular Updates
Keep Debian, `netbird`, and `miniserve` updated.
```bash
sudo apt update && sudo apt full-upgrade -y
# For miniserve from cargo: cargo install --locked miniserve
# For Netbird: usually updates via apt if repo was added.
```

---

### 9. Phase 7: Troubleshooting

*   **`miniserve` Service Issues:**
    *   `sudo systemctl status miniserve@<escaped-path>.service`
    *   `sudo journalctl -u miniserve@<escaped-path>.service -n 100 --no-pager --follow`
    *   Check `miniserve` binary path and permissions.
    *   Manually run the `ExecStart` command from the systemd unit (as the correct user if specified) to see direct errors.
*   **`netbird` Connectivity:**
    *   `sudo netbird status` on all relevant peers.
    *   Ping `netbird` IPs between peers.
    *   Check `netbird` admin dashboard for peer status and access rules.
*   **Firewall:**
    *   Temporarily `sudo ufw disable` to isolate firewall issues. If it works, your UFW rules need adjustment. Re-enable UFW.
    *   Check UFW logs: `sudo less /var/log/ufw.log`.
*   **Permissions:** Double-check that the user `miniserve` runs as has read (and write, if uploads enabled) permissions for the target directories.