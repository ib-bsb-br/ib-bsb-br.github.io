---
tags: software>windows, cloud
comment: 'https://github.com/FilenCloudDienste/filen-cli'
info: fechado.
date: '2024-10-13'
type: post
layout: post
published: true
sha: 
slug: filen-windows
title: 'Filen CLI sync: Setup Guide for Windows'

---
# Setting up Filen CLI as a Windows Service on Windows 11

This guide outlines the process of installing and configuring the Filen CLI to run as a Windows service for continuous syncing on a Windows 11 system.

## 1. Install Filen CLI

1. Download the Windows version of Filen CLI from the official website or GitHub repository.
2. Extract the zip file to a permanent location, e.g., `C:\Program Files\Filen CLI\`.
3. Rename the executable to `filen.exe` for simplicity.
4. Add the Filen CLI directory to your system PATH:
   - Right-click on 'This PC' or 'My Computer' and select 'Properties'.
   - Click on 'Advanced system settings'.
   - Click on 'Environment Variables'.
   - Under 'System variables', find and select 'Path', then click 'Edit'.
   - Click 'New' and add the path to the Filen CLI directory (e.g., `C:\Program Files\Filen CLI\`).
   - Click 'OK' to close all dialogs.

5. Verify installation by opening a new Command Prompt and running:
   ```
   filen --version
   ```

## 2. Set up Authentication

Create a file named `.filen-cli-credentials` in your user profile directory:

1. Open Notepad.
2. Add your Filen credentials to this file:
   ```
   your_email@example.com
   your_password
   your_2fa_code  # If 2FA is enabled
   ```
3. Save the file as `C:\Users\YourUsername\.filen-cli-credentials` (replace `YourUsername` with your actual Windows username).

Secure the credentials file:
- Right-click on the file, select 'Properties'.
- Go to the 'Security' tab, click 'Edit', and ensure only your user account has access.

## 3. Create a Windows Service

We'll use the Non-Sucking Service Manager (NSSM) to create a Windows service:

1. Download NSSM from [nssm.cc](https://nssm.cc/).
2. Extract the zip file and copy `nssm.exe` to `C:\Windows\System32\`.
3. Open Command Prompt as Administrator.
4. Run the following command to create the service:

```
nssm install FilenSync "C:\Program Files\Filen CLI\filen.exe" "sync C:\Users\YourUsername\FilenSync:twoWay:/999_SHARED --continuous"
```

Replace `YourUsername` with your actual Windows username and adjust the paths as necessary.

5. Set the service to run under your user account:
```
nssm set FilenSync ObjectName .\YourUsername YourPassword
```
Replace `YourUsername` and `YourPassword` with your actual Windows credentials.

## 4. Start the Service

1. Open the Services application (services.msc).
2. Find the "FilenSync" service.
3. Right-click and select "Start".

To make the service start automatically on boot:
1. Right-click the service and select "Properties".
2. Set "Startup type" to "Automatic".
3. Click "Apply" and "OK".

## 5. Verify Service Status

1. Open the Services application (services.msc).
2. Find the "FilenSync" service.
3. Check that its status is "Running".

## 6. Monitor Logs

To view the service logs:

1. Open Event Viewer (eventvwr.msc).
2. Expand "Windows Logs" and select "Application".
3. Look for events with "FilenSync" as the source.

## Troubleshooting

If you encounter issues:

1. Check the service status in the Services application.
2. Review the logs in Event Viewer.
3. Ensure the sync directories exist and have the correct permissions.
4. Verify the credentials in `C:\Users\YourUsername\.filen-cli-credentials` are correct.
5. Try running the sync command manually to see if there are any errors:
   ```
   "C:\Program Files\Filen CLI\filen.exe" sync C:\Users\YourUsername\FilenSync:twoWay:/999_SHARED
   ```
6. If problems persist, check for updates to the Filen CLI or consult the official Filen documentation.

## Maintenance

- Periodically check for updates to the Filen CLI.
- To update, download the new version, replace the executable in `C:\Program Files\Filen CLI\`, and restart the service.
- Regularly review and adjust your sync settings as needed.

Remember to keep your `.filen-cli-credentials` file secure and update it if you change your Filen account password.
