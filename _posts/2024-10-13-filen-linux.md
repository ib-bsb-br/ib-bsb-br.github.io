---

tags: [software>linux, cloud]
comment: 'https://github.com/FilenCloudDienste/filen-cli'
info: fechado.
date: '2024-10-13'
type: post
layout: post
published: true
sha: 
slug: filen-linux
title: 'Filen CLI sync: Setup Guide for Linux'

---
# Setting up Filen CLI as a Systemd Service on Debian Bullseye ARM64

This guide outlines the process of installing and configuring the Filen CLI to run as a systemd service for continuous syncing on a Debian Bullseye ARM64 system.

## 1. Install Filen CLI

```bash
# Download the ARM64 version of filen-cli
wget https://cdn.filen.io/desktop/release/filen-cli_linux_arm64.tar.gz

# Extract the archive
tar -xzvf filen-cli_linux_arm64.tar.gz

# Move the binary to a location in your PATH
sudo mv filen-cli-v0.0.12-linux-arm64 /usr/bin/

# Verify installation
/usr/bin/filen-cli-v0.0.12-linux-arm64 --version
```

## 2. Set up Authentication

Create a file named `.filen-cli-credentials` in the root user's home directory:

```bash
sudo nano /root/.filen-cli-credentials
```

Add your Filen credentials to this file:

```
your_email@example.com
your_password
your_2fa_code  # If 2FA is enabled
```

Secure the credentials file:

```bash
sudo chmod 600 /root/.filen-cli-credentials
```

## 3. Create Systemd Service File

Create a new systemd service file:

```bash
sudo nano /etc/systemd/system/filen-sync.service
```

Add the following content:

```ini
[Unit]
Description=Filen CLI Sync Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/filen-cli-v0.0.12-linux-arm64 sync /userdata/000_download/share/:twoWay:/999_SHARED --continuous
Restart=on-failure
RestartSec=5
User=root
WorkingDirectory=/root

[Install]
WantedBy=multi-user.target
```

Note: Adjust the paths in the `ExecStart` line to match your specific sync requirements.

## 4. Enable and Start the Service

```bash
# Reload systemd configuration
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable filen-sync.service

# Start the service
sudo systemctl start filen-sync.service
```

## 5. Verify Service Status

Check if the service is running correctly:

```bash
sudo systemctl status filen-sync.service
```

## 6. Monitor Logs

To view the service logs:

```bash
journalctl -u filen-sync.service -f
```

## Troubleshooting

If you encounter issues:

1. Check the service status and logs using the commands in steps 5 and 6.
2. Ensure the sync directories exist and have the correct permissions.
3. Verify the credentials in `/root/.filen-cli-credentials` are correct.
4. Try running the sync command manually to see if there are any errors:

   ```bash
   sudo /usr/bin/filen-cli-v0.0.12-linux-arm64 sync /userdata/000_download/share/:twoWay:/999_SHARED
   ```

5. If problems persist, check for updates to the Filen CLI or consult the official Filen documentation.

## Maintenance

- Periodically check for updates to the Filen CLI.
- To update, download the new version, replace the binary in `/usr/bin/`, and restart the service.
- Regularly review and adjust your sync settings as needed.

Remember to keep your `.filen-cli-credentials` file secure and update it if you change your Filen account password.
