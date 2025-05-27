---
tags:
- aid>software>linux
info: aberto.
date: 2025-02-28
type: post
layout: post
published: true
slug: fileserver
title: '`simple-fileserver` on RK3588'
comment: https://github.com/heathcliff26/simple-fileserver
---


## 1. Introduction

The `simple-fileserver` application is a lightweight static file server implemented using Go's `http.FileServer`. It's designed for simplicity, making it suitable for serving static content without the overhead of a full-featured web server. This guide focuses on building and running `simple-fileserver` directly from its source code on an RK3588 ARM64 device running Debian Bullseye.

The RK3588 ARM64 platform provides a powerful foundation for hosting applications like `simple-fileserver`. With an octa-core ARM CPU, ample RAM, and high-speed networking capabilities, it's essential to leverage this hardware effectively while ensuring security and performance, especially when running applications directly on the host.

---

## 2. Understanding `simple-fileserver`

### Key Characteristics

-   **Simplicity**: Serves static files with minimal configuration.
-   **No Built-in Compression**: Does not compress files before serving.
-   **Basic Directory Listing**: Provides a simple directory listing unless disabled via the `-no-index` flag.
-   **No Authentication**: Lacks built-in mechanisms for authentication or authorization. Rely on a reverse proxy for this if needed.
-   **Single Instance Serving**: Designed to serve files without advanced scaling features.

### Limitations and Risks of Direct Execution

-   **Security Risks**: As highlighted in the `simple-fileserver` README.md (HEATHCLIFF26, 2023), direct execution is **not recommended** by the author due to the risk of path traversal vulnerabilities. This means a malicious actor could potentially access files outside the intended webroot if the server is not meticulously configured and secured.
-   **Lack of Advanced Features**: Does not support features like caching, advanced compression, or dynamic content.
-   **Manual Process Management**: Without container orchestration, managing the application lifecycle (start, stop, restart, logging) requires direct OS-level intervention (e.g., `systemd` services, manual process management).

---

## 3. Deployment Approach: Direct Execution on RK3588

This guide focuses exclusively on building `simple-fileserver` from source and running the compiled binary directly on your RK3588 Debian Bullseye system.

**Warning:** This approach bypasses the isolation benefits of containerization. You are responsible for securing the host system and the application. The path traversal vulnerability mentioned is a serious concern. Ensure your `-webroot` is an isolated directory containing only public files, and run the server as an unprivileged user.

---

## 4. Setting Up `simple-fileserver`

### 4.1 Prerequisites

-   **RK3588 ARM64 Device**: Ensure your device is running Debian 11 Bullseye or a compatible ARM64 Linux distribution.
-   **Go Toolchain (Version 1.24.0 or newer)**: `simple-fileserver` requires Go 1.24.0 or newer as per its `go.mod` file (HEATHCLIFF26, 2023). Debian Bullseye's default `golang-go` package might be older. It's recommended to install Go from the official binaries:
    1.  Visit the official Go downloads page: [golang.org/dl/](https://golang.org/dl/)
    2.  Download the ARM64 Linux tarball for the required Go version (e.g., `go1.24.3.linux-arm64.tar.gz` at the time of writing).
    3.  Install Go to `/usr/local`:
        ```bash
        # Example for Go 1.24.3 (replace with the latest stable version if different)
        wget https://golang.org/dl/go1.24.3.linux-arm64.tar.gz 
        sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.24.3.linux-arm64.tar.gz
        ```
    4.  Add Go to your `PATH`. Add the following line to your `~/.bashrc` or `~/.zshrc` (or system-wide in `/etc/profile.d/go.sh`):
        ```bash
        export PATH=$PATH:/usr/local/go/bin
        ```
    5.  Apply the changes and verify:
        ```bash
        source ~/.bashrc # Or the relevant profile file, or logout and login
        go version
        ```
-   **Git**: For cloning the source code repository.
    ```bash
    sudo apt update
    sudo apt install git
    ```
-   **Build Essentials**: (Usually present, but good to ensure)
    ```bash
    sudo apt install build-essential make
    ```
-   **Internet Access**: Required to clone the repository and download Go modules.
-   **(Optional) SSL Certificates**: If you plan to serve content over HTTPS directly or via a reverse proxy.

### 4.2 Cloning the Repository

Clone the `simple-fileserver` source code from GitHub:

```bash
git clone https://github.com/heathcliff26/simple-fileserver.git
cd simple-fileserver
```

### 4.3 Building the Binary

The repository includes a `Makefile` and a build script (`hack/build.sh`) (HEATHCLIFF26, 2023) that simplifies compilation. Using `make build` is recommended as it typically incorporates version information and other build flags defined in `hack/build.sh`.

1.  **Navigate to the cloned repository directory**:
    ```bash
    cd simple-fileserver # If not already there
    ```

2.  **Build using the Makefile**:
    ```bash
    make build
    ```
    This command executes `hack/build.sh`, which should correctly detect the ARM64 architecture and build a static binary.

3.  **Locate and Install the Binary**:
    The compiled binary will be in `bin/simple-fileserver`. Copy it to a standard location:
    ```bash
    sudo cp ./bin/simple-fileserver /usr/local/bin/simple-fileserver
    sudo chmod +x /usr/local/bin/simple-fileserver
    ```

---

## 5. Running the Server

### 5.1 Initial Run (Testing)

Before setting up a permanent service, test the server from your terminal.

1.  **Create a directory for your web content** (standardizing on `/srv/simplefs-webroot/public` for examples):
    ```bash
    sudo mkdir -p /srv/simplefs-webroot/public
    echo "Hello from simple-fileserver on RK3588!" | sudo tee /srv/simplefs-webroot/public/index.html
    # Ensure the user who will run the server can read this (see Security section)
    # For testing, you can temporarily make it world-readable if running as your own user:
    # sudo chmod -R a+rX /srv/simplefs-webroot
    ```

2.  **Run the compiled binary**:
    ```bash
    /usr/local/bin/simple-fileserver \
      -webroot /srv/simplefs-webroot/public \
      -port 8080 \
      -log
    ```
    -   The server will listen on port `8080`.
    -   `-log` enables request logging to standard output.

    Access `http://<RK3588_IP_ADDRESS>:8080` in a browser. Press `Ctrl+C` to stop.

### 5.2 Running as a Dedicated Non-Root User (Recommended)

This is crucial for security and is detailed in Section 10. The server should not run as `root`.

---

## 6. Configuring `simple-fileserver`

Configuration is via command-line arguments or environment variables (`cmd/cmd.go`, HEATHCLIFF26, 2023). Command-line arguments take precedence.

### 6.1 Command-Line Arguments

| Argument     | Description                                                                                                                                 |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| `-webroot`   | **Required**. Absolute path to the root directory to serve files from.                                                                      |
| `-port`      | Port for the server to listen on (default `8080`).                                                                                          |
| `-cert`      | Path to SSL certificate file (enables HTTPS directly).                                                                                      |
| `-key`       | Path to SSL private key file (required if `-cert` is used).                                                                                 |
| `-log`       | Enables logging of HTTP requests.                                                                                                           |
| `-no-index`  | Disables directory listing. If a directory doesn't contain an `index.html`, a 404 error is returned instead of listing the directory's contents. |
| `-version`   | Displays version information and exits.                                                                                                     |

### 6.2 Environment Variables

| Environment Variable     | Description                                                           |
|--------------------------|-----------------------------------------------------------------------|
| `SFILESERVER_WEBROOT`    | Same as `-webroot`.                                                   |
| `SFILESERVER_PORT`       | Same as `-port`.                                                      |
| `SFILESERVER_CERT`       | Same as `-cert`.                                                      |
| `SFILESERVER_KEY`        | Same as `-key`.                                                       |
| `SFILESERVER_LOG`        | Same as `-log` (set to `true` or `1`).                                |
| `SFILESERVER_NO_INDEX`   | Same as `-no-index` (set to `true` or `1`).                           |

### 6.3 Using Command-Line Arguments vs Environment Variables

Environment variables are useful for `systemd` service files or scripts.

**Example using environment variables:**
```bash
export SFILESERVER_WEBROOT=/srv/simplefs-webroot/public
export SFILESERVER_PORT=8080
export SFILESERVER_LOG=true
/usr/local/bin/simple-fileserver
```

---

## 7. Organizing Your Files

A structured approach simplifies management and security.

```
/srv/simplefs-webroot/  # Base directory for content served by simple-fileserver
├── public/             # This would be your -webroot (e.g., for HTTP/S access)
│   ├── documents/
│   ├── images/
│   └── downloads/
└── restricted/         # Content NOT directly served or served with specific SSL/auth
    ├── sensitive-docs/
```
-   **`-webroot`**: Always use an absolute path. Ensure this directory *only* contains files intended for public access via `simple-fileserver`.

---

## 8. SSL Configuration

### 8.1 Using a Reverse Proxy with SSL (**Recommended**)

A reverse proxy (Nginx, Caddy, Apache) enhances security and flexibility.

#### 8.1.1 Setting Up Nginx as a Reverse Proxy

1.  **Install Nginx**: `sudo apt update && sudo apt install nginx`
2.  **Configure Nginx**: Create `/etc/nginx/sites-available/simple-fileserver-proxy`:
    ```nginx
    server {
        listen 80;
        server_name example.com www.example.com; # Replace with your domain
        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name example.com www.example.com; # Replace with your domain

        # SSL Certificate paths (Certbot will manage these)
        ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

        # Strong SSL Settings (Refer to Mozilla SSL Configuration Generator for current best practices)
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_prefer_server_ciphers off;
        ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384';
        
        # Add HSTS header (after confirming everything works)
        # add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

        location / {
            proxy_pass http://127.0.0.1:8080; # Assuming simple-fileserver on port 8080
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_buffering off; # Can be useful for large file streaming
        }
    }
    ```
3.  **Enable and Restart Nginx**:
    ```bash
    sudo ln -s /etc/nginx/sites-available/simple-fileserver-proxy /etc/nginx/sites-enabled/
    sudo nginx -t && sudo systemctl restart nginx
    ```
    Run `simple-fileserver` listening on `127.0.0.1:8080` (e.g., as `simplefsuser`).

#### 8.1.2 Obtaining SSL Certificates with Let's Encrypt

1.  **Install Certbot**: `sudo apt install certbot python3-certbot-nginx`
2.  **Obtain Certificate**: `sudo certbot --nginx -d example.com -d www.example.com` (replace with your domain)
3.  **Test Renewal**: `sudo certbot renew --dry-run`

### 8.2 Direct SSL Termination (Use with Caution)

Less secure and flexible for production.

1.  **Prepare SSL Certificates**: Store `cert.pem` and `key.pem` (e.g., in `/etc/simple-fileserver/ssl/`).
    ```bash
    sudo mkdir -p /etc/simple-fileserver/ssl
    # Copy your cert.pem and key.pem here
    # Example: sudo cp /path/to/your/cert.pem /path/to/your/key.pem /etc/simple-fileserver/ssl/
    # Ensure simplefsuser (see Section 10.1) can read them:
    sudo chown -R root:simplefsuser /etc/simple-fileserver/ssl
    sudo chmod 0750 /etc/simple-fileserver/ssl # Directory permissions
    sudo chmod 0640 /etc/simple-fileserver/ssl/cert.pem
    sudo chmod 0600 /etc/simple-fileserver/ssl/key.pem # Key must be private
    ```
2.  **Run with SSL**:
    ```bash
    # As simplefsuser (or the user you configured)
    sudo -u simplefsuser /usr/local/bin/simple-fileserver \
      -webroot /srv/simplefs-webroot/public \
      -port 8443 \
      -cert /etc/simple-fileserver/ssl/cert.pem \
      -key /etc/simple-fileserver/ssl/key.pem \
      -log
    ```
    Open port `8443` in your firewall.

---

## 9. Performance Optimization

### 9.1 System Tuning

-   **Max Open Files**: Edit `/etc/security/limits.conf`:
    ```
    *         soft  nofile  65535
    *         hard  nofile  65535
    simplefsuser soft  nofile  65535 
    simplefsuser hard  nofile  65535
    ```
    Apply with logout/login or set `LimitNOFILE` in systemd service. Temp: `ulimit -n 65535`.
-   **Network Buffers**: In `/etc/sysctl.conf` (or `/etc/sysctl.d/99-local.conf`):
    ```
    net.core.rmem_max=16777216
    net.core.wmem_max=16777216
    ```
    Apply: `sudo sysctl -p`.
-   **Memory Management**: In `/etc/sysctl.conf` (or `/etc/sysctl.d/99-local.conf`):
    ```
    vm.vfs_cache_pressure=50
    vm.swappiness=10
    ```
    Apply: `sudo sysctl -p`.

### 9.2 File System Optimization

-   **Fast File System**: `ext4` or `XFS` on SSD/NVMe.
-   **Mount Options** (in `/etc/fstab` for the `/srv/simplefs-webroot` partition, if separate):
    `defaults,noatime,nodiratime,discard` (discard for SSDs). Remount or reboot.

### 9.3 ARM64-Specific Optimizations

-   **CPU Scaling**: Set governor to `performance` for high load, or `ondemand`/`schedutil` for balance. Check with `cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor`.
-   **Monitoring**: Use `htop`, `iotop`, `dstat`, `perf`.
-   **Updates**: Keep kernel and firmware updated via `sudo apt update && sudo apt upgrade`.

---

## 10. Security Best Practices for Bare-Metal Deployment

### 10.1 Dedicated Non-Root User

**Crucial.**
1.  **Create User**:
    ```bash
    sudo adduser --system --group --no-create-home --shell /usr/sbin/nologin simplefsuser
    ```
2.  **Binary Permissions**: (Assuming binary at `/usr/local/bin/simple-fileserver`)
    ```bash
    sudo chown root:simplefsuser /usr/local/bin/simple-fileserver
    sudo chmod 750 /usr/local/bin/simple-fileserver # rwxr-x---
    ```
3.  **Webroot & SSL Permissions**:
    ```bash
    sudo mkdir -p /srv/simplefs-webroot/public
    sudo chown -R simplefsuser:simplefsuser /srv/simplefs-webroot
    sudo find /srv/simplefs-webroot -type d -exec chmod 750 {} \; # Dirs: rwxr-x---
    sudo find /srv/simplefs-webroot -type f -exec chmod 640 {} \; # Files: rw-r----
    # For direct SSL (certs in /etc/simple-fileserver/ssl/):
    sudo mkdir -p /etc/simple-fileserver/ssl
    sudo chown -R root:simplefsuser /etc/simple-fileserver/ssl
    sudo chmod 0750 /etc/simple-fileserver/ssl # Directory permissions
    sudo chmod 0640 /etc/simple-fileserver/ssl/*cert.pem # Or your cert name
    sudo chmod 0600 /etc/simple-fileserver/ssl/*key.pem  # Or your key name
    ```
4.  **Run as `simplefsuser`**: Via `sudo -u simplefsuser ...` or `User=simplefsuser` in systemd.

### 10.2 Firewall Configuration

(Using UFW as an example)
```bash
# If simple-fileserver direct on 8080:
sudo ufw allow 8080/tcp
# If Nginx reverse proxy for HTTP/HTTPS:
# sudo ufw allow http 
# sudo ufw allow https
sudo ufw enable
sudo ufw status
```

### 10.3 Strict File Permissions and Webroot Management

-   `simplefsuser` needs *only read* access to webroot files, *execute* on directories within the webroot.
-   The `-webroot` argument must be an absolute path to an isolated directory containing *only* files intended for public access.
-   **Never** point `-webroot` to `/`, `~`, `/tmp`, or any other sensitive system directory.

### 10.4 Path Traversal Vulnerability Mitigation

1.  **Run as unprivileged `simplefsuser`**. This is the primary mitigation.
2.  **Correct and absolute `-webroot` path** definition.
3.  **Strict file system permissions** for `simplefsuser`, preventing access outside its designated areas.
4.  **Reverse Proxy** can add a layer of path normalization and request filtering.
5.  **Chroot (Advanced)**, see below, for an additional strong layer of filesystem isolation.

**The application-level risk noted by the author remains the primary concern if the Go `http.FileServer` itself has issues or `simple-fileserver`'s argument handling is flawed, allowing interpretation of ".." sequences to escape the defined webroot, even if ultimately limited by OS permissions.**

### 10.5 Chroot (Advanced)

Restricts the server's view of the filesystem to a specific directory, making path traversal outside this "jail" significantly harder.
Since `simple-fileserver` is built as a static Go binary (due to `CGO_ENABLED=0` in its build process, as seen in `hack/build.sh`), setting up a chroot jail is simpler as there are minimal dynamic library dependencies to copy into the jail.
This involves creating a jail directory, copying the binary, the webroot content into the jail, and potentially a few essential device nodes like `/dev/null`, `/dev/random`, `/dev/urandom` if strictly needed by the Go runtime for specific operations (though often Go uses syscalls directly for these). Running the server would then involve the `chroot` command. This is an advanced setup.

### 10.6 Regular Audits and Source Updates

-   Periodically audit file permissions and configurations.
-   Monitor logs for suspicious activity (if `-log` is enabled and logs are captured).
-   Keep your Debian Bullseye system updated: `sudo apt update && sudo apt full-upgrade`.
-   Periodically check the `simple-fileserver` GitHub repository for updates or security notices. If updates are available, you'll need to `git pull` the changes and rebuild the binary (see Section 11.5).

---

## 11. Maintenance Procedures

### 11.1 Stopping and Restarting the Service

-   **Manual Foreground**: `Ctrl+C`.
-   **Manual Background (`&`)**: `pgrep -u simplefsuser -f simple-fileserver` then `sudo kill <PID>`.
-   **Systemd**: See below.

### 11.2 Managing with `systemd` (Recommended for Production)

Create `/etc/systemd/system/simple-fileserver.service`:
```ini
[Unit]
Description=Simple File Server
After=network.target

[Service]
Type=simple
User=simplefsuser
Group=simplefsuser

# Option 1: Command-line arguments
ExecStart=/usr/local/bin/simple-fileserver -port 8080 -webroot /srv/simplefs-webroot/public -log

# Option 2: Environment variables (uncomment and adjust ExecStart if preferred)
# Environment="SFILESERVER_PORT=8080"
# Environment="SFILESERVER_WEBROOT=/srv/simplefs-webroot/public"
# Environment="SFILESERVER_LOG=true"
# ExecStart=/usr/local/bin/simple-fileserver

Restart=on-failure
RestartSec=5s

# Logging to journald
StandardOutput=journal
StandardError=journal

# Security Hardening
ProtectSystem=full
PrivateTmp=true
NoNewPrivileges=true
ProtectHome=read-only # Or true if webroot is not under /home; 'read-only' is safer.
# Ensure simplefsuser can read its webroot and SSL certs if used
ReadOnlyPaths=/srv/simplefs-webroot/public
# If using direct SSL with certs in /etc/simple-fileserver/ssl:
ReadOnlyPaths=/etc/simple-fileserver/ssl

[Install]
WantedBy=multi-user.target
```
**Reload, Enable, Start**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable simple-fileserver.service
sudo systemctl start simple-fileserver.service
```
**Manage**: `sudo systemctl status/stop/start/restart simple-fileserver.service`
**Logs**: `sudo journalctl -u simple-fileserver.service -f` (to follow logs)

### 11.3 Regular Tasks (Including Log Management)

-   **Monitor Disk Usage**: `du -sh /srv/simplefs-webroot/public`.
-   **Identify Large Files**: `find /srv/simplefs-webroot/public -type f -printf "%s\t%p\n" | sort -nr | head -n 20`.
-   **Log Management**:
    -   If using `systemd` with `StandardOutput=journal`, logs go to `journald`. `journald` has its own size limits and rotation (configurable in `/etc/systemd/journald.conf`). You can view logs with `journalctl -u simple-fileserver.service`.
    -   If you redirect `simple-fileserver` output to a custom log file (not recommended if using systemd's journal integration), use `logrotate` to manage log file sizes. Create a config in `/etc/logrotate.d/simple-fileserver`:
        ```
        /var/log/simple-fileserver.log { # Adjust path to your custom log file
            daily
            rotate 7
            compress
            delaycompress
            missingok
            notifempty
            create 640 simplefsuser simplefsuser # Or appropriate user/group
        }
        ```

### 11.4 Backup Strategy

A script to backup web content and critical configurations. Store this script, for example, at `/usr/local/sbin/backup_simplefs.sh`.

```bash
#!/bin/bash
BACKUP_DIR="/opt/backups/simplefs" # Choose a secure backup location
WEBROOT_DIR="/srv/simplefs-webroot/public"
NGINX_CONFIG_DIR="/etc/nginx"
SYSTEMD_SERVICE_FILE="/etc/systemd/system/simple-fileserver.service"
SSL_CERTS_DIR="/etc/letsencrypt" # If using Let's Encrypt with Nginx
DIRECT_SSL_CERTS_DIR="/etc/simple-fileserver/ssl" # If using direct SSL

TIMESTAMP=$(date +%Y%m%d-%H%M%S)

mkdir -p "$BACKUP_DIR"

# Backup web content
echo "Backing up webroot..."
sudo tar czf "$BACKUP_DIR/sfs_webroot-$TIMESTAMP.tar.gz" -C "$(dirname "$WEBROOT_DIR")" "$(basename "$WEBROOT_DIR")"

# Backup Nginx configs (if used)
if [ -d "$NGINX_CONFIG_DIR/sites-enabled/simple-fileserver-proxy" ]; then # Check if proxy config exists
  echo "Backing up Nginx configuration..."
  sudo tar czf "$BACKUP_DIR/sfs_nginx_config-$TIMESTAMP.tar.gz" "$NGINX_CONFIG_DIR"
fi

# Backup systemd service file (if used)
if [ -f "$SYSTEMD_SERVICE_FILE" ]; then
  echo "Backing up systemd service file..."
  sudo cp "$SYSTEMD_SERVICE_FILE" "$BACKUP_DIR/simple-fileserver.service-$TIMESTAMP"
fi

# Backup Let's Encrypt SSL certs (if used)
if [ -d "$SSL_CERTS_DIR/live/example.com" ]; then # Check for your specific domain
  echo "Backing up Let's Encrypt SSL certificates..."
  sudo tar czf "$BACKUP_DIR/sfs_letsencrypt_ssl_certs-$TIMESTAMP.tar.gz" -C /etc letsencrypt
fi

# Backup Direct SSL certs (if used)
if [ -d "$DIRECT_SSL_CERTS_DIR" ] && [ "$(ls -A $DIRECT_SSL_CERTS_DIR)" ]; then
  echo "Backing up direct SSL certificates..."
  sudo tar czf "$BACKUP_DIR/sfs_direct_ssl_certs-$TIMESTAMP.tar.gz" -C /etc simple-fileserver/ssl
fi

echo "Backup completed to $BACKUP_DIR"

# Optional: Remove old backups (e.g., older than 30 days)
find "$BACKUP_DIR" -name "sfs_*-*.tar.gz" -mtime +30 -exec sudo rm {} \;
find "$BACKUP_DIR" -name "simple-fileserver.service-*" -mtime +30 -exec sudo rm {} \;

```
Make it executable: `sudo chmod +x /usr/local/sbin/backup_simplefs.sh`.
Automate with a cron job (run `sudo crontab -e`):
```cron
0 2 * * * /usr/local/sbin/backup_simplefs.sh > /var/log/simplefs_backup.log 2>&1
```

### 11.5 Updating the Application

1.  Navigate to the cloned `simple-fileserver` repository:
    `cd /path/to/cloned/simple-fileserver/repo`
2.  Pull the latest changes:
    `git pull origin main` (or the relevant branch/tag)
3.  Rebuild the binary:
    `make build`
4.  Copy the new binary to its operational location:
    `sudo cp ./bin/simple-fileserver /usr/local/bin/simple-fileserver`
5.  Restart the service:
    `sudo systemctl restart simple-fileserver.service` (if using systemd)

---

## 12. Troubleshooting Guide

1.  **Server Won't Start / Binary Not Found or Not Executable**
    -   **Symptoms**: Command not found, permission denied.
    -   **Solutions**:
        -   Verify binary path (`/usr/local/bin/simple-fileserver`).
        -   Check execute permissions: `ls -l /usr/local/bin/simple-fileserver`.
        -   If using `systemd`, verify `ExecStart` path and check logs: `sudo journalctl -u simple-fileserver.service -n 50 --no-pager`.

2.  **Port Conflicts**
    -   **Symptoms**: "address already in use".
    -   **Solutions**: `sudo netstat -tulpn | grep :<port_number>`. Change `-port` or stop conflicting service.

3.  **File Not Found Errors (404)**
    -   **Symptoms**: Browser shows 404.
    -   **Solutions**:
        -   Verify `-webroot` path is correct, absolute (e.g., `/srv/simplefs-webroot/public`).
        -   Check file existence within webroot.
        -   Case sensitivity: `File.txt` != `file.txt`.
        -   Permissions: Ensure `simplefsuser` has read access to webroot files and execute access to directories.
        -   If `-no-index` used, ensure `index.html` exists for directory access.

4.  **Permission Denied Errors (Logs or Terminal)**
    -   **Symptoms**: Service fails to start, or logs show permission issues.
    -   **Solutions**:
        -   `simplefsuser` needs read access to webroot and its contents.
        -   `simplefsuser` needs read access to SSL certificate and key files (if direct SSL).
        -   Check `systemd` sandboxing options (`ReadOnlyPaths`, `ProtectHome`).

5.  **Slow File Access**
    -   **Symptoms**: Delays.
    -   **Solutions**: Optimize files, check network (`iperf3`), system resources (`htop`, `iotop`), apply performance optimizations (Section 9).