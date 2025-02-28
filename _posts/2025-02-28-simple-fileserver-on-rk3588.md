---
tags: [scratchpad]
info: aberto.
date: 2025-02-28
type: post
layout: post
published: true
slug: simple-fileserver-on-rk3588
title: '`simple-fileserver` on RK3588'
---
# Comprehensive Guide: Deploying and Managing `simple-fileserver` on RK3588 ARM64

This guide provides detailed instructions for deploying and managing `simple-fileserver` on the RK3588 ARM64 platform, emphasizing best practices for performance, security, and maintenance. The RK3588's robust hardware makes it an excellent choice for hosting high-performance applications, but it's crucial to implement applications securely and efficiently.

**Table of Contents**

1. [Introduction](#1-introduction)
2. [Understanding `simple-fileserver`](#2-understanding-simple-fileserver)
3. [Deployment Options](#3-deployment-options)
    - 3.1 [Containerized Deployment (Recommended)](#31-containerized-deployment-recommended)
    - 3.2 [Direct Execution (Not Recommended)](#32-direct-execution-not-recommended)
4. [Setting Up `simple-fileserver`](#4-setting-up-simple-fileserver)
    - 4.1 [Prerequisites](#41-prerequisites)
    - 4.2 [Downloading or Building the Image](#42-downloading-or-building-the-image)
    - 4.3 [Running the Server](#43-running-the-server)
5. [Configuring `simple-fileserver`](#5-configuring-simple-fileserver)
    - 5.1 [Command-Line Arguments](#51-command-line-arguments)
    - 5.2 [Environment Variables](#52-environment-variables)
    - 5.3 [Using Command-Line Arguments vs Environment Variables](#53-using-command-line-arguments-vs-environment-variables)
6. [Organizing Your Files](#6-organizing-your-files)
7. [SSL Configuration](#7-ssl-configuration)
    - 7.1 [Using a Reverse Proxy with SSL (Recommended)](#71-using-a-reverse-proxy-with-ssl-recommended)
        - 7.1.1 [Setting Up Nginx as a Reverse Proxy](#711-setting-up-nginx-as-a-reverse-proxy)
        - 7.1.2 [Obtaining SSL Certificates with Let's Encrypt](#712-obtaining-ssl-certificates-with-lets-encrypt)
    - 7.2 [Direct SSL Termination (Not Recommended for Production)](#72-direct-ssl-termination-not-recommended-for-production)
8. [Performance Optimization](#8-performance-optimization)
    - 8.1 [System Tuning](#81-system-tuning)
    - 8.2 [File System Optimization](#82-file-system-optimization)
    - 8.3 [ARM64-Specific Optimizations](#83-arm64-specific-optimizations)
9. [Security Best Practices](#9-security-best-practices)
    - 9.1 [Running as a Non-Root User](#91-running-as-a-non-root-user)
    - 9.2 [Firewall Configuration](#92-firewall-configuration)
    - 9.3 [Access Control](#93-access-control)
10. [Maintenance Procedures](#10-maintenance-procedures)
    - 10.1 [Stopping and Restarting the Container](#101-stopping-and-restarting-the-container)
    - 10.2 [Regular Tasks](#102-regular-tasks)
    - 10.3 [Backup Strategy](#103-backup-strategy)
11. [Troubleshooting Guide](#11-troubleshooting-guide)
12. [Alternative File Servers](#12-alternative-file-servers)
13. [Conclusion](#13-conclusion)

---

## 1. Introduction

The `simple-fileserver` application is a lightweight static file server implemented using Go's `http.FileServer`. It's designed for simplicity and ease of deployment, making it suitable for serving static content without the overhead of a full-featured web server.

The RK3588 ARM64 platform provides a powerful foundation for hosting applications like `simple-fileserver`. With an octa-core ARM CPU, ample RAM, and high-speed networking capabilities, it's essential to leverage this hardware effectively while ensuring security and performance.

---

## 2. Understanding `simple-fileserver`

### Key Characteristics

- **Simplicity**: Serves static files with minimal configuration.
- **No Built-in Compression**: Does not compress files before serving.
- **Basic Directory Listing**: Provides a simple directory listing unless disabled.
- **No Authentication**: Lacks built-in mechanisms for authentication or authorization.
- **Single Instance Serving**: Designed to serve files without scaling features.

### Limitations

- **Security Risks When Run Outside a Container**: Susceptible to path traversal vulnerabilities if not properly isolated.
- **Lack of Advanced Features**: Does not support features like caching, compression, or dynamic content.

---

## 3. Deployment Options

### 3.1 Containerized Deployment (**Recommended**)

Running `simple-fileserver` within a container provides an added layer of security by isolating the application from the host system. Containers help mitigate path traversal vulnerabilities and make deployment more manageable.

### 3.2 Direct Execution (**Not Recommended**)

Directly executing `simple-fileserver` on the host system is **strongly discouraged** due to significant security risks, especially path traversal vulnerabilities. This method should only be used in controlled environments where security is not a concern.

---

## 4. Setting Up `simple-fileserver`

### 4.1 Prerequisites

- **RK3588 ARM64 Device**: Ensure your device is running Debian 11 Bullseye or a compatible ARM64 Linux distribution.
- **Container Engine**: Install Docker or Podman for container management.
- **SSL Certificates**: (Optional) Obtain SSL certificates if you plan to serve content over HTTPS.
- **Internet Access**: Required to pull container images or download source code.

### 4.2 Downloading or Building the Image

#### Downloading the Image

Pull the latest `simple-fileserver` image from a container registry:

```bash
# Using Docker
docker pull ghcr.io/heathcliff26/simple-fileserver:latest

# Using Podman
podman pull ghcr.io/heathcliff26/simple-fileserver:latest
```

#### Building the Image Locally

If you prefer to build the image locally:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/heathcliff26/simple-fileserver.git
   cd simple-fileserver
   ```

2. **Build the Image**:

   ```bash
   # Using Docker
   docker build -t simple-fileserver:latest .

   # Using Podman
   podman build -t simple-fileserver:latest .
   ```

### 4.3 Running the Server

#### Public Content (Unsecured HTTP)

```bash
# Create a directory for your web content
mkdir -p ~/served-files/public

# Run the container
podman run -d \
  --name simple-fileserver \
  -p 8080:8080 \
  -v ~/served-files/public:/webroot:Z \
  ghcr.io/heathcliff26/simple-fileserver:latest \
  -webroot /webroot \
  -port 8080 \
  -log
```

**Notes:**

- The `:Z` option is for SELinux contexts; omit if not applicable.
- Replace `podman` with `docker` if using Docker.
- The `--name simple-fileserver` assigns a name to the container for easier management.

---

## 5. Configuring `simple-fileserver`

### 5.1 Command-Line Arguments

| Argument     | Description                                                                                                                                 |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| `-webroot`   | **Required**. Root directory to serve files from.                                                                                           |
| `-port`      | Port for the server to listen on (default `8080`).                                                                                          |
| `-cert`      | Path to SSL certificate file (enables HTTPS).                                                                                               |
| `-key`       | Path to SSL private key file (required if `-cert` is used).                                                                                 |
| `-log`       | Enables logging of HTTP requests.                                                                                                           |
| `-no-index`  | Disables directory listing. If a directory doesn't contain an `index.html`, a 404 error is returned instead of listing the directory's contents. |
| `-version`   | Displays version information and exits.                                                                                                     |

### 5.2 Environment Variables

Alternatively, you can set configuration options using environment variables:

| Environment Variable     | Description                                                           |
|--------------------------|-----------------------------------------------------------------------|
| `SFILESERVER_WEBROOT`    | Same as `-webroot`.                                                   |
| `SFILESERVER_PORT`       | Same as `-port`.                                                      |
| `SFILESERVER_CERT`       | Same as `-cert`.                                                      |
| `SFILESERVER_KEY`        | Same as `-key`.                                                       |
| `SFILESERVER_LOG`        | Same as `-log`.                                                       |
| `SFILESERVER_NO_INDEX`   | Same as `-no-index`.                                                  |

### 5.3 Using Command-Line Arguments vs Environment Variables

- **Precedence**: Command-line arguments take precedence over environment variables.
- **Usage**: Use environment variables for easier configuration in container environments.

**Example using environment variables:**

```bash
podman run -d \
  --name simple-fileserver \
  -p 8080:8080 \
  -v ~/served-files/public:/webroot:Z \
  -e SFILESERVER_WEBROOT=/webroot \
  -e SFILESERVER_PORT=8080 \
  -e SFILESERVER_LOG=true \
  ghcr.io/heathcliff26/simple-fileserver:latest
```

---

## 6. Organizing Your Files

It's important to organize your files logically to simplify management and enhance security.

```bash
served-files/
├── public/
│   ├── documents/
│   ├── images/
│   └── downloads/
└── restricted/
    ├── sensitive-docs/
    └── data/
```

- **Public**: Contains files accessible over HTTP.
- **Restricted**: Contains content that requires protection, which should be served over HTTPS or behind authentication layers.

---

## 7. SSL Configuration

### 7.1 Using a Reverse Proxy with SSL (**Recommended**)

For production environments, it's recommended to use a reverse proxy like Nginx or Apache to handle SSL termination and forward requests to `simple-fileserver`. This setup enhances security and allows for better management of SSL certificates.

#### 7.1.1 Setting Up Nginx as a Reverse Proxy

1. **Install Nginx**:

   ```bash
   sudo apt update
   sudo apt install nginx
   ```

2. **Configure Nginx to Proxy Requests**

   Create a new configuration file for your site, e.g., `/etc/nginx/sites-available/simple-fileserver`:

   ```nginx
   server {
       listen 80;
       server_name example.com;
       return 301 https://$host$request_uri;
   }

   server {
       listen 443 ssl;
       server_name example.com;

       ssl_certificate     /etc/ssl/certs/your_certificate.crt;
       ssl_certificate_key /etc/ssl/private/your_private.key;

       location / {
           proxy_pass http://localhost:8080;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. **Enable the Configuration and Restart Nginx**:

   ```bash
   sudo ln -s /etc/nginx/sites-available/simple-fileserver /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

#### 7.1.2 Obtaining SSL Certificates with Let's Encrypt

1. **Install Certbot**:

   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```

2. **Obtain and Install the SSL Certificate**:

   ```bash
   sudo certbot --nginx -d example.com
   ```

3. **Verify SSL Renewal**:

   Certbot sets up automatic renewal. You can test it with:

   ```bash
   sudo certbot renew --dry-run
   ```

### 7.2 Direct SSL Termination (**Not Recommended for Production**)

If you prefer to run `simple-fileserver` with SSL directly, you can do so, but it's not recommended for production use due to security concerns.

```bash
# Generate or provide your SSL certificate and key
mkdir -p ~/ssl
# Place cert.pem and key.pem in ~/ssl

# Run the server with SSL
podman run -d \
  --name simple-fileserver-ssl \
  -p 8443:8443 \
  -v ~/served-files/restricted:/webroot:Z \
  -v ~/ssl:/ssl:Z \
  ghcr.io/heathcliff26/simple-fileserver:latest \
  -webroot /webroot \
  -port 8443 \
  -cert /ssl/cert.pem \
  -key /ssl/key.pem \
  -log
```

**Note**: Ensure that the `-port` flag matches the mapped port (`8443`) and that SSL certificates are correctly mounted.

---

## 8. Performance Optimization

### 8.1 System Tuning

Optimize system parameters to enhance performance.

- **Increase Maximum Open Files**:

  ```bash
  sudo sh -c 'echo "* - nofile 65535" >> /etc/security/limits.conf'
  ulimit -n 65535
  ```

- **Adjust Network Buffers**:

  ```bash
  sudo sysctl -w net.core.rmem_max=16777216
  sudo sysctl -w net.core.wmem_max=16777216
  sudo sh -c 'echo "net.core.rmem_max=16777216" >> /etc/sysctl.conf'
  sudo sh -c 'echo "net.core.wmem_max=16777216" >> /etc/sysctl.conf'
  ```

- **Modify Memory Management Settings**:

  ```bash
  sudo sysctl -w vm.vfs_cache_pressure=50
  sudo sysctl -w vm.swappiness=10
  sudo sh -c 'echo "vm.vfs_cache_pressure=50" >> /etc/sysctl.conf'
  sudo sh -c 'echo "vm.swappiness=10" >> /etc/sysctl.conf'
  ```

### 8.2 File System Optimization

- **Use a Fast File System**: Use `ext4` or `XFS` on SSD storage for better performance.
- **Mount Options**:

  - `noatime` and `nodiratime`: Disables updating access times to reduce disk I/O.
  - `discard`: Enables TRIM on SSDs.
  
  Update `/etc/fstab` accordingly:

  ```fstab
  /dev/sda1  /served-files  ext4  defaults,noatime,nodiratime,discard  0  2
  ```

  Then remount or reboot:

  ```bash
  sudo mount -o remount /served-files
  ```

### 8.3 ARM64-Specific Optimizations

- **CPU Scaling**: Ensure CPU frequency scaling is enabled and configured for performance.
- **Use Performance Monitoring Tools**: Utilize tools like `perf`, `htop`, or `dstat` to monitor system performance.
- **Update Kernel and Firmware**: Ensure the system is using the latest kernel and firmware for optimal performance and hardware support.

---

## 9. Security Best Practices

### 9.1 Running as a Non-Root User

To run the container as a non-root user, modify the Dockerfile to include a non-root user:

```dockerfile
FROM ghcr.io/heathcliff26/simple-fileserver:latest

# Create a non-root user with UID:GID 1000:1000
RUN addgroup --gid 1000 appuser && \
    adduser --uid 1000 --gid 1000 --home /home/appuser --shell /bin/bash --disabled-password --gecos "" appuser

# Set ownership of the webroot directory
RUN mkdir /webroot && chown appuser:appuser /webroot

USER appuser
```

Build the custom image:

```bash
docker build -t simple-fileserver-nonroot:latest .
```

Run the container:

```bash
podman run -d \
  --name simple-fileserver \
  -p 8080:8080 \
  -v ~/served-files/public:/webroot:Z \
  simple-fileserver-nonroot:latest \
  -webroot /webroot \
  -port 8080 \
  -log
```

Ensure the host directory `~/served-files/public` has appropriate permissions:

```bash
sudo chown -R 1000:1000 ~/served-files/public
```

### 9.2 Firewall Configuration

**Using UFW (Ubuntu/Debian)**:

```bash
sudo ufw allow 8080/tcp
sudo ufw enable
```

**Using Firewalld (CentOS/RHEL/Fedora)**:

```bash
sudo firewall-cmd --permanent --add-port=8080/tcp
sudo firewall-cmd --reload
```

**Using iptables**:

```bash
sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
# To make the rule persistent, install iptables-persistent or save the rules manually.
```

### 9.3 Access Control

- **File Permissions**:

  ```bash
  chmod -R 755 ~/served-files/public
  chmod -R 700 ~/served-files/restricted
  ```

- **Regular Audits**:

  - Periodically scan for unauthorized files.
  - Review access logs for suspicious activity.

- **Update and Patch Regularly**:

  - Keep the host system and container images up-to-date with security patches.

---

## 10. Maintenance Procedures

### 10.1 Stopping and Restarting the Container

- **List Running Containers**:

  ```bash
  podman ps
  ```

- **Stop the Container**:

  ```bash
  podman stop simple-fileserver
  ```

- **Start the Container**:

  ```bash
  podman start simple-fileserver
  ```

- **Restart the Container**:

  ```bash
  podman restart simple-fileserver
  ```

### 10.2 Regular Tasks

- **Monitor Disk Usage**:

  ```bash
  podman exec simple-fileserver du -sh /webroot/*
  ```

- **Identify Large Files**:

  ```bash
  podman exec simple-fileserver find /webroot -type f -printf "%s\t%p\n" | sort -nr | head -n 20 | awk '{printf "%.2f MB\t%s\n", $1/1024/1024, $2}'
  ```

- **Check Logs**:

  ```bash
  podman logs simple-fileserver
  ```

### 10.3 Backup Strategy

Create regular backups of your content.

```bash
#!/bin/bash
backup_date=$(date +%Y%m%d)
tar czf ~/backups/served-files-$backup_date.tar.gz -C ~/served-files .
```

Automate this script using a cron job:

```bash
crontab -e
```

Add the following line to schedule the backup daily at 2 AM:

```cron
0 2 * * * /path/to/backup_script.sh
```

---

## 11. Troubleshooting Guide

**Common Issues:**

1. **Server Won't Start**

   - **Symptoms**: Container exits immediately or fails to start.
   - **Solutions**:

     - Check for port conflicts with `sudo netstat -tulpn | grep :8080`.
     - Verify file paths and permissions.
     - Ensure SSL certificates are correctly mounted and paths are accurate.
     - Check container logs with `podman logs simple-fileserver` for error messages.

2. **Slow File Access**

   - **Symptoms**: Users experience delays when accessing files.
   - **Solutions**:

     - Optimize large files (compress images, split archives).
     - Check network bandwidth and latency.
     - Review system resource usage (CPU, memory, disk I/O).
     - Ensure sufficient system resources are available.

3. **File Not Found Errors**

   - **Symptoms**: 404 errors when accessing known files.
   - **Solutions**:

     - Verify that files exist in `/webroot`.
     - Check for case sensitivity in filenames and URLs.
     - Ensure correct permissions are set.
     - Verify that `-no-index` is not set unintentionally.

4. **Permission Denied Errors**

   - **Symptoms**: Access denied errors in logs or terminal.
   - **Solutions**:

     - Ensure the container user has read permissions on the host directories.
     - Adjust SELinux policies or context if necessary (`:Z` in volume mounts).
     - Verify that the container is not running as root if it's intended to be non-root.

---

## 12. Alternative File Servers

If `simple-fileserver` doesn't meet your needs, consider these alternatives:

### **Caddy**

- **Advantages**:

  - Automatic HTTPS with Let's Encrypt.
  - Simple configuration using a `Caddyfile`.
  - High performance with built-in support for HTTP/2 and HTTP/3.

- **Disadvantages**:

  - Smaller community compared to Nginx or Apache.
  - Less extensive module ecosystem.

- **Link**: [https://caddyserver.com/](https://caddyserver.com/)

### **Nginx**

- **Advantages**:

  - High performance and low resource consumption.
  - Extensive documentation and community support.
  - Highly flexible with support for reverse proxying, load balancing, caching, and more.

- **Disadvantages**:

  - Configuration can be complex for beginners.
  - Requires additional modules or configuration for certain features.

- **Link**: [https://www.nginx.com/](https://www.nginx.com/)

### **Apache HTTP Server**

- **Advantages**:

  - Rich feature set with a vast array of modules.
  - Highly configurable and versatile.
  - Long-standing presence with a large community.

- **Disadvantages**:

  - Higher resource usage compared to Nginx or Caddy.
  - Configuration files can be complex and verbose.

- **Link**: [https://httpd.apache.org/](https://httpd.apache.org/)

---

## 13. Conclusion

Deploying `simple-fileserver` on the RK3588 ARM64 platform can be efficient and secure when following best practices. By containerizing the application, optimizing performance, and adhering to security guidelines, you can effectively serve static content.

Always consider the limitations of `simple-fileserver` and evaluate whether an alternative solution may better suit your requirements, especially for production environments with security concerns.

Ensure that you regularly update and maintain your system, monitor for security vulnerabilities, and perform regular backups to safeguard your data.

---

**Disclaimer**: Use `simple-fileserver` at your own risk. The authors and maintainers are not responsible for any security issues or data loss resulting from its use.