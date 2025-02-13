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
```powershell
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
```

## Prerequisites
- Windows 11
- PowerShell 7.5.0+
- Administrator access
- BorgBase account

## Directory Structure
```plaintext
G:\01-documents\.ssh\
├── id_ed25519       # Private key (600 permissions)
├── id_ed25519.pub   # Public key (644 permissions)
└── config           # SSH configuration file
```

## Detailed Setup Instructions

### 1. SSH Directory Creation
```powershell
# Create directory
mkdir G:\01-documents\.ssh -ErrorAction SilentlyContinue

# Verify creation
if (Test-Path G:\01-documents\.ssh) {
    Write-Host "SSH directory created successfully"
} else {
    Write-Error "Failed to create SSH directory"
    exit 1
}
```

### 2. Security Configuration
```powershell
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
```

### 3. Key Generation
```powershell
ssh-keygen -t ed25519 -C "borgbase-backup"
# When prompted:
# - Path: G:\01-documents\.ssh\id_ed25519
# - Passphrase: Strongly recommended
```

### 4. Key Permission Setup
```powershell
# Private key
icacls G:\01-documents\.ssh\id_ed25519 /inheritance:r
icacls G:\01-documents\.ssh\id_ed25519 /grant:r "$($env:USERNAME):R"

# Public key
icacls G:\01-documents\.ssh\id_ed25519.pub /inheritance:r
icacls G:\01-documents\.ssh\id_ed25519.pub /grant:r "$($env:USERNAME):R"
```

### 5. SSH Configuration
```powershell
$config = @"
Host borgbase
    HostName fdw7g8ds.repo.borgbase.com
    User fdw7g8ds
    IdentityFile G:\01-documents\.ssh\id_ed25519
    IdentitiesOnly yes
"@
$config | Out-File -Encoding utf8 G:\01-documents\.ssh\config
```

### 6. BorgBase Key Upload
1. Copy public key:
```powershell
Get-Content G:\01-documents\.ssh\id_ed25519.pub | clip
```

2. Web Interface Steps:
   - Navigate to BorgBase SSH Keys section
   - Click "Add SSH Key"
   - Paste the copied key
   - Label: "windows-backup-[DATE]"
   - Save changes

### 7. Backup Procedures
1. Export Configuration:
```powershell
# Create backup directory
$backupDir = "G:\01-documents\.ssh\backup-$(Get-Date -Format 'yyyyMMdd')"
mkdir $backupDir

# Backup files
Copy-Item G:\01-documents\.ssh\config $backupDir
Copy-Item G:\01-documents\.ssh\id_ed25519.pub $backupDir
```

2. Secure Private Key:
- Use Windows BitLocker
- Or password manager's secure notes
- Consider hardware security key

## Error Resolution Guide

### Common Errors

1. Path Not Found (Exit Code 2)
```powershell
# Error:
~\.ssh: The system cannot find the path specified.
# Solution:
Use absolute paths: G:\01-documents\.ssh
```

2. Hostname Resolution (Exit Code 255)
```powershell
# Error:
ssh: Could not resolve hostname borgbase
# Solutions:
- Use full hostname: ssh fdw7g8ds@fdw7g8ds.repo.borgbase.com
- Check DNS: nslookup fdw7g8ds.repo.borgbase.com
```

3. Permission Denied
```powershell
# Verify key permissions
icacls G:\01-documents\.ssh\id_ed25519
# Expected output should show only user read access
```

## FileZilla Integration

### Configuration Steps
1. Site Manager (Ctrl+S)
2. New Site Settings:
```plaintext
Protocol: SFTP
Host: fdw7g8ds.repo.borgbase.com
Port: 22
Logon Type: Key file
User: fdw7g8ds
Key file: G:\01-documents\.ssh\id_ed25519
```

## Maintenance Procedures

### Monthly Checks
1. Permission Verification
```powershell
# Run security audit
Get-Acl G:\01-documents\.ssh\id_ed25519 | Select-Object -ExpandProperty Access
```

2. Connection Test
```powershell
# Test SSH connection
ssh -T borgbase
```

3. Backup Verification
```powershell
# Verify backup integrity
Test-Path G:\01-documents\.ssh\backup-*
```

## Version Control
- Document version: 1.0.0
- PowerShell version tested: 7.5.0
- Windows version: 11
- Last validated: 2025-02-13

## Command Reference
| Command | Purpose | Expected Output |
|---------|----------|----------------|
| `icacls` | Set permissions | "Successfully processed" |
| `ssh-keygen` | Generate keys | Fingerprint display |
| `ssh -T` | Test connection | Connection verification |