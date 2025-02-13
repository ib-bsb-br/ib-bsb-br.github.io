---
tags: [aid>cloud>windows]
info: aberto.
date: 2025-02-13
type: post
layout: post
published: true
slug: borgbase-ssh-key-windows-setup
title: 'BorgBase SSH Key Windows Setup'
---
## Quick Start Guide
{% codeblock powershell %}
# 1. Create SSH directory
mkdir G:\01-documents\.ssh

# 2. Set permissions
icacls G:\01-documents\.ssh /inheritance:r
icacls G:\01-documents\.ssh /grant:r "$($env:USERNAME):(OI)(CI)F"

# 3. Generate key
ssh-keygen -t ed25519 -C "borgbase-backup"

# 4. Set key permissions
icacls G:\01-documents\.ssh\id_ed25519 /inheritance:r
icacls G:\01-documents\.ssh\id_ed25519 /grant:r "$($env:USERNAME):R"
{% endcodeblock %}

## Prerequisites
- Windows 11
- powershell %} 7.5.0+
- Administrator access
- BorgBase account

## Directory Structure
{% codeblock plaintext %}
G:\01-documents\.ssh\
├── id_ed25519       # Private key (600 permissions)
├── id_ed25519.pub   # Public key (644 permissions)
└── config           # SSH configuration file
{% endcodeblock %}

## Detailed Setup Instructions

### 1. SSH Directory Creation
{% codeblock powershell %}
# Create directory
mkdir G:\01-documents\.ssh -ErrorAction SilentlyContinue

# Verify creation
if (Test-Path G:\01-documents\.ssh) {
    Write-Host "SSH directory created successfully"
} else {
    Write-Error "Failed to create SSH directory"
    exit 1
}
{% endcodeblock %}

### 2. Security Configuration
{% codeblock powershell %}
# Remove inheritance
icacls G:\01-documents\.ssh /inheritance:r
# Set user permissions
icacls G:\01-documents\.ssh /grant:r "$($env:USERNAME):(OI)(CI)F"

# Verify permissions
$acl = Get-Acl G:\01-documents\.ssh
if ($acl.Access.Count -eq 1) {
    Write-Host "Permissions set correctly"
} else {
    Write-Warning "Unexpected permission count"
}
{% endcodeblock %}

### 3. Key Generation
{% codeblock powershell %}
ssh-keygen -t ed25519 -C "borgbase-backup"
# When prompted:
# - Path: G:\01-documents\.ssh\id_ed25519
# - Passphrase: Strongly recommended
{% endcodeblock %}

### 4. Key Permission Setup
{% codeblock powershell %}
# Private key
icacls G:\01-documents\.ssh\id_ed25519 /inheritance:r
icacls G:\01-documents\.ssh\id_ed25519 /grant:r "$($env:USERNAME):R"

# Public key
icacls G:\01-documents\.ssh\id_ed25519.pub /inheritance:r
icacls G:\01-documents\.ssh\id_ed25519.pub /grant:r "$($env:USERNAME):R"
{% endcodeblock %}

### 5. SSH Configuration
{% codeblock powershell %}
$config = @"
Host borgbase
    HostName fdw7g8ds.repo.borgbase.com
    User fdw7g8ds
    IdentityFile G:\01-documents\.ssh\id_ed25519
    IdentitiesOnly yes
"@
$config | Out-File -Encoding utf8 G:\01-documents\.ssh\config
{% endcodeblock %}

### 6. BorgBase Key Upload
1. Copy public key:
{% codeblock powershell %}
Get-Content G:\01-documents\.ssh\id_ed25519.pub | clip
{% endcodeblock %}

2. Web Interface Steps:
   - Navigate to BorgBase SSH Keys section
   - Click "Add SSH Key"
   - Paste the copied key
   - Label: "windows-backup-[DATE]"
   - Save changes

### 7. Backup Procedures
1. Export Configuration:
{% codeblock powershell %}
# Create backup directory
$backupDir = "G:\01-documents\.ssh\backup-$(Get-Date -Format 'yyyyMMdd')"
mkdir $backupDir

# Backup files
Copy-Item G:\01-documents\.ssh\config $backupDir
Copy-Item G:\01-documents\.ssh\id_ed25519.pub $backupDir
{% endcodeblock %}

2. Secure Private Key:
- Use Windows BitLocker
- Or password manager's secure notes
- Consider hardware security key

## Error Resolution Guide

### Common Errors

1. Path Not Found (Exit Code 2)
{% codeblock powershell %}
# Error:
~\.ssh: The system cannot find the path specified.
# Solution:
Use absolute paths: G:\01-documents\.ssh
{% endcodeblock %}

2. Hostname Resolution (Exit Code 255)
{% codeblock powershell %}
# Error:
ssh: Could not resolve hostname borgbase
# Solutions:
- Use full hostname: ssh fdw7g8ds@fdw7g8ds.repo.borgbase.com
- Check DNS: nslookup fdw7g8ds.repo.borgbase.com
{% endcodeblock %}

3. Permission Denied
{% codeblock powershell %}
# Verify key permissions
icacls G:\01-documents\.ssh\id_ed25519
# Expected output should show only user read access
{% endcodeblock %}

## FileZilla Integration

### Configuration Steps
1. Site Manager (Ctrl+S)
2. New Site Settings:
{% codeblock plaintext %}
Protocol: SFTP
Host: fdw7g8ds.repo.borgbase.com
Port: 22
Logon Type: Key file
User: fdw7g8ds
Key file: G:\01-documents\.ssh\id_ed25519
{% endcodeblock %}

## Maintenance Procedures

### Monthly Checks
1. Permission Verification
{% codeblock powershell %}
# Run security audit
Get-Acl G:\01-documents\.ssh\id_ed25519 | Select-Object -ExpandProperty Access
{% endcodeblock %}

2. Connection Test
{% codeblock powershell %}
# Test SSH connection
ssh -T borgbase
{% endcodeblock %}

3. Backup Verification
{% codeblock powershell %}
# Verify backup integrity
Test-Path G:\01-documents\.ssh\backup-*
{% endcodeblock %}

## Command Reference
| Command | Purpose | Expected Output |
|---------|----------|----------------|
| `icacls` | Set permissions | "Successfully processed" |
| `ssh-keygen` | Generate keys | Fingerprint display |
| `ssh -T` | Test connection | Connection verification |
