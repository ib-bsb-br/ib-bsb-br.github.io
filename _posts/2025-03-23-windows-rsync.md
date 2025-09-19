---
tags:
- scratchpad
info: aberto.
date: 2025-03-23
type: post
layout: post
published: true
slug: windows-rsync
title: Backing up Windows machines using rsync and ssh
comment: https://articles.manugarg.com/backup_rsync.html
---

## Executive summary (Windows 10 local user)

1. Generate a **new** SSH key (`ssh-keygen -t ed25519`) and append the **public** key to `~/.ssh/authorized_keys` on `dc2.myusadc.com` for user `ibbsbbry`.
2. Test `ssh -i ~/.ssh/id_ed25519 ibbsbbry@dc2.myusadc.com`.
3. Prefer **rsync over SSH** (no daemon). If you need rsync modules, use **daemon+tunnel** with a user-owned `rsyncd.conf`.
4. Use the PowerShell script below to automate: it can add your key, sync files listed in `filelist.txt` (Cygwin paths), and optionally create a minimal `rsyncd.conf`.

---

## Section 0: Immediate Steps to Secure Your Server Access After Key Compromise (Windows 10)

**0.1 Generate a NEW SSH key (PowerShell):**

```powershell
# Recommended
ssh-keygen -t ed25519 -C "your_email@example.com"
# OR
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

Default path: `C:\Users\<you>\.ssh\id_ed25519`. Use a strong passphrase.

**0.2 Add your NEW public key to the server (Windows lacks ssh-copy-id):**

```powershell
$pub = "$env:USERPROFILE\.ssh\id_ed25519.pub"
scp $pub ibbsbbry@dc2.myusadc.com:~/.ssh/tmp_newkey.pub
ssh ibbsbbry@dc2.myusadc.com "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat ~/.ssh/tmp_newkey.pub >> ~/.ssh/authorized_keys && rm ~/.ssh/tmp_newkey.pub && chmod 600 ~/.ssh/authorized_keys"
```

**0.3 Test login with the NEW key:**

```powershell
ssh -i "$env:USERPROFILE\.ssh\id_ed25519" ibbsbbry@dc2.myusadc.com
# If using a custom port, add: -p 2222
```

**0.4 Remove the compromised key from `authorized_keys` on the server.**

**0.5 Delete the compromised private key wherever it existed.**

**Optional `ssh-agent` (enter passphrase once per session):**

```powershell
Start-Service ssh-agent -ErrorAction SilentlyContinue
ssh-add "$env:USERPROFILE\.ssh\id_ed25519"
```

---

## Section 1: Understanding Your Server Information (Recap)

* **Username:** `ibbsbbry`
* **Hostname:** `dc2.myusadc.com`
* **Public IP:** `15.204.42.250`
* **SSH Port:** default `22` unless you use a custom port.

---

## Section 2: Connecting Remotely with SSH

**2.1 OpenSSH (PowerShell):**

```powershell
ssh ibbsbbry@dc2.myusadc.com
ssh -i "$env:USERPROFILE\.ssh\id_ed25519" ibbsbbry@dc2.myusadc.com
ssh -i "$env:USERPROFILE\.ssh\id_ed25519" -p 2222 ibbsbbry@dc2.myusadc.com
```

*First connection adds the host key. If your OpenSSH is older and doesn’t support `StrictHostKeyChecking=accept-new`, use the script’s `-InsecureHostKey` fallback only if needed.*

**2.2 PuTTY/Plink (optional):**

* Convert OpenSSH key to `.ppk` via **PuTTYgen**.
* PuTTY: Host `dc2.myusadc.com`, Port `22`, Auth → select `.ppk`. Save session and connect.
* Plink: `plink -i C:\path\to\id_ed25519.ppk ibbsbbry@dc2.myusadc.com`

---

## Section 3: Transferring Files Securely

**3.1 SFTP (interactive):**

```powershell
sftp ibbsbbry@dc2.myusadc.com
# or with key/port:
sftp -i "$env:USERPROFILE\.ssh\id_ed25519" -oPort=2222 ibbsbbry@dc2.myusadc.com
```

Common commands: `put`, `get`, `ls`, `cd`, `lcd`, `mkdir`, `rm`, `exit`.

**GUI options (quick):**

* **WinSCP:** Protocol `SFTP` → Host `dc2.myusadc.com` → Port `22` → User `ibbsbbry` → Advanced → SSH → Authentication → point to `.ppk` → Login.
* **FileZilla:** Host `sftp://dc2.myusadc.com` → User `ibbsbbry` → Port `22` → Settings → Connection → SFTP → add key.

**3.2 SCP:**

```powershell
# Upload
scp -i "$env:USERPROFILE\.ssh\id_ed25519" .\local\file.txt ibbsbbry@dc2.myusadc.com:/remote/path/
# Download
scp -i "$env:USERPROFILE\.ssh\id_ed25519" ibbsbbry@dc2.myusadc.com:/remote/path/file.txt .\
# Custom port: add -P 2222
```

**3.3 rsync (efficient sync; requires Cygwin/MSYS2 rsync installed under your user)**

* Windows paths → Cygwin/MSYS2 paths (`C:\` ⇒ `/cygdrive/c`).
* **SSH mode (simpler; recommended):**

```powershell
rsync -avz --progress -e "ssh -i $env:USERPROFILE/.ssh/id_ed25519" /cygdrive/d/mydata/ ibbsbbry@dc2.myusadc.com:/backup/ibbsbbry/
```

* **Daemon+tunnel mode (module-based):**

  1. Create `~/rsyncd.conf` (user-owned):

     ```
     use chroot = no
     pid file = /home/ibbsbbry/rsyncd.pid
     [backup]
         path = /backup
         read only = no
         comment = backup area
         hosts allow = 127.0.0.1
         hosts deny  = *
     ```
  2. Start daemon & forward local 873 → remote 1873:

     ```powershell
     ssh ibbsbbry@dc2.myusadc.com 'rsync --daemon --port=1873 --config=$HOME/rsyncd.conf'
     ssh -N -L 873:localhost:1873 ibbsbbry@dc2.myusadc.com   # separate window
     ```
  3. Sync via module:

     ```powershell
     rsync -avz --progress /cygdrive/d/mydata 127.0.0.1::backup/ibbsbbry
     ```
  4. Stop daemon:

     ```powershell
     ssh ibbsbbry@dc2.myusadc.com 'kill $(cat ~/rsyncd.pid)'
     ```

---

## Section 4: Important General Considerations (server-side)

* **Firewall:** Ensure inbound SSH (e.g., 22 or your custom port) is allowed (`ufw`, `firewalld`, security groups).
* **`/etc/ssh/sshd_config` (admin-controlled):**

  * `Port 22` (or your custom)
  * `PubkeyAuthentication yes`
  * `PasswordAuthentication no` (once keys work)
  * `PermitRootLogin no`
  * Restart SSH after changes: `sudo systemctl restart sshd`
* **Client private key security:** Keep your private key private; use a strong passphrase and `ssh-agent`.

---

## Section 5: Troubleshooting

* **`Permission denied (publickey…)`**: Check that your **new** public key is in `~/.ssh/authorized_keys`, server perms `~/.ssh`=700, `authorized_keys`=600, and client private key perms are restrictive.
* **`Connection refused`**: Verify host/port, SSH service running, firewall rules, and reachability (`ping`, `tracert`).
* **Rsync path errors**: Use Cygwin paths on Windows; ensure the remote target directory exists and is writable.

---

## PowerShell automation (Windows 10 local user)

> Save as `coolice-ssh-rsync.ps1`.
> Requires: `ssh`, `scp` (OpenSSH), and `rsync` (Cygwin/MSYS2 in **user** PATH).
> Supports: custom SSH port, host-key fallback, optional creation of `rsyncd.conf`, SSH mode or Daemon+tunnel mode, `--progress` and `-z` toggles, and safe file list normalization.

```powershell
<# 
.SYNOPSIS
  Secure SSH setup + rsync backups for Windows 10 local users.

.PARAMETER ServerHost
  SSH host (e.g., dc2.myusadc.com)

.PARAMETER ServerUser
  SSH username (e.g., ibbsbbry)

.PARAMETER SshPort
  SSH port (default 22)

.PARAMETER PrivateKey / PublicKey
  Paths to your keypair (default: ~/.ssh/id_ed25519)

.PARAMETER FileList
  File with one Cygwin/MSYS2 path per line; lines starting with # are ignored.
  Quotes around paths are allowed; the script strips surrounding quotes.

.PARAMETER Mode
  SSH  : rsync over SSH (simpler)
  Daemon: rsync-daemon + SSH tunnel to localhost

.PARAMETER EnsureKey
  Append PublicKey to server's authorized_keys (creates ~/.ssh if needed)

.PARAMETER OldKeyPrefix
  If provided, removes lines containing this substring from authorized_keys (backup kept)

.PARAMETER EnsureRsyncdConf
  In Daemon mode, create a minimal ~/rsyncd.conf if missing (user-owned, loopback-only)

.PARAMETER Compress
  Add -z to rsync

.PARAMETER Progress
  Add --progress to rsync

.PARAMETER InsecureHostKey
  Fallback host-key policy if accept-new isn’t supported (less secure)
#>

[CmdletBinding(SupportsShouldProcess=$true)]
param(
  [string]$ServerHost = "dc2.myusadc.com",
  [string]$ServerUser = "ibbsbbry",
  [int]$SshPort = 22,

  [string]$PrivateKey = "$env:USERPROFILE\.ssh\id_ed25519",
  [string]$PublicKey  = "$env:USERPROFILE\.ssh\id_ed25519.pub",

  [string]$FileList   = ".\filelist.txt",

  [ValidateSet("SSH","Daemon")]
  [string]$Mode = "SSH",

  [string]$RemoteDir = "/backup/ibbsbbry/",  # SSH mode destination

  [int]$LocalForwardPort = 873,              # Daemon mode
  [int]$RemoteRsyncdPort = 1873,
  [string]$RsyncModule   = "backup",
  [string]$ModuleSubdir  = "ibbsbbry",

  [switch]$EnsureKey,
  [string]$OldKeyPrefix,
  [switch]$EnsureRsyncdConf,
  [switch]$Compress,
  [switch]$Progress,
  [switch]$InsecureHostKey
)

function Assert-Exe($name) {
  if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
    throw "Required command '$name' not found in PATH. Install/enable it for your user."
  }
}

function Get-SSHOptions {
  if ($InsecureHostKey) {
    return @("-p",$SshPort,"-i",$PrivateKey,"-o","StrictHostKeyChecking=no","-o","UserKnownHostsFile=NUL")
  } else {
    return @("-p",$SshPort,"-i",$PrivateKey,"-o","StrictHostKeyChecking=accept-new")
  }
}

function Invoke-SSHInline([string]$cmd) {
  $opts = Get-SSHOptions
  & ssh @opts "$ServerUser@$ServerHost" $cmd
  if ($LASTEXITCODE -ne 0) { throw "SSH command failed: $cmd" }
}

function Start-SSHForward {
  $opts = Get-SSHOptions
  $args = $opts + @("-N","-L","$LocalForwardPort:localhost:$RemoteRsyncdPort","$ServerUser@$ServerHost","-o","ExitOnForwardFailure=yes","-o","ServerAliveInterval=30")
  $p = Start-Process -PassThru -WindowStyle Minimized -FilePath "ssh" -ArgumentList $args
  Write-Host "Started SSH port forward (PID=$($p.Id))..."
  $deadline = (Get-Date).AddSeconds(10)
  do {
    Start-Sleep -Milliseconds 300
    $ok = Test-NetConnection -ComputerName "127.0.0.1" -Port $LocalForwardPort -InformationLevel Quiet
  } until ($ok -or (Get-Date) -gt $deadline)
  if (-not $ok) { try { $p | Stop-Process -Force } catch {} ; throw "Local port $LocalForwardPort did not open." }
  return $p
}

function Stop-ProcessSafe($p) { if ($p -and !$p.HasExited) { $p | Stop-Process -Force } }

try {
  Assert-Exe "ssh"
  Assert-Exe "scp"
  Assert-Exe "rsync"

  if ($EnsureKey) {
    if (-not (Test-Path $PublicKey)) { throw "Public key not found at $PublicKey. Generate one with ssh-keygen." }
    Write-Host "Appending public key to $ServerUser@$ServerHost ..."
    $opts = Get-SSHOptions
    & scp "-P" $SshPort $PublicKey "$ServerUser@$ServerHost:~/.ssh/tmp_newkey.pub"
    if ($LASTEXITCODE -ne 0) { throw "scp failed while uploading public key." }
    Invoke-SSHInline "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat ~/.ssh/tmp_newkey.pub >> ~/.ssh/authorized_keys && rm ~/.ssh/tmp_newkey.pub && chmod 600 ~/.ssh/authorized_keys"
    if ($OldKeyPrefix) {
      Write-Host "Removing lines containing '$OldKeyPrefix' from authorized_keys (backup kept as authorized_keys.bak)..."
      Invoke-SSHInline "cp -f ~/.ssh/authorized_keys ~/.ssh/authorized_keys.bak && grep -v '$OldKeyPrefix' ~/.ssh/authorized_keys.bak > ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
    }
  }

  if (-not (Test-Path $FileList)) { throw "File list not found: $FileList (Cygwin-style paths, one per line)." }
  $rawLines = Get-Content -LiteralPath $FileList
  $paths = foreach ($line in $rawLines) {
    $t = $line.Trim()
    if (-not $t) { continue }
    if ($t.StartsWith("#")) { continue }
    # Strip surrounding quotes if present
    if ($t.StartsWith('"') -and $t.EndsWith('"')) { $t = $t.Trim('"') }
    $t
  }
  if (-not $paths) { throw "No valid paths found in $FileList." }

  if ($Mode -eq "SSH") {
    Write-Host "Running rsync over SSH to $ServerHost:$RemoteDir ..."
    $sshCmd = "ssh " + (Get-SSHOptions -join ' ')
    $rsyncArgs = @("-av")
    if ($Compress) { $rsyncArgs += "-z" }
    if ($Progress) { $rsyncArgs += "--progress" }
    $rsyncArgs += @("-e", $sshCmd)

    foreach ($p in $paths) {
      & rsync @rsyncArgs "$p" "$ServerUser@$ServerHost:$RemoteDir"
      if ($LASTEXITCODE -ne 0) { throw "rsync failed for path: $p" }
    }
    Write-Host "All paths synced (SSH mode)."
  }
  else {
    Write-Host "Daemon mode selected."
    if ($EnsureRsyncdConf) {
      Write-Host "Ensuring ~/rsyncd.conf exists remotely ..."
      $conf = @"
use chroot = no
pid file = /home/$ServerUser/rsyncd.pid
[${RsyncModule}]
    path = /backup
    read only = no
    comment = backup area
    hosts allow = 127.0.0.1
    hosts deny  = *
"@
      $escaped = $conf -replace "`r","" -replace "`n","`n"
      Invoke-SSHInline "test -f ~/rsyncd.conf || printf '%s' '$escaped' > ~/rsyncd.conf"
    }

    Write-Host "Starting remote rsync daemon on port $RemoteRsyncdPort ..."
    Invoke-SSHInline "rsync --daemon --port=$RemoteRsyncdPort --config=\$HOME/rsyncd.conf"
    $forward = $null
    try {
      $forward = Start-SSHForward
      $rsyncArgs = @("-av")
      if ($Compress) { $rsyncArgs += "-z" }
      if ($Progress) { $rsyncArgs += "--progress" }
      foreach ($p in $paths) {
        & rsync @rsyncArgs "$p" "127.0.0.1::$RsyncModule/$ModuleSubdir"
        if ($LASTEXITCODE -ne 0) { throw "rsync failed for path: $p" }
      }
      Write-Host "All paths synced (Daemon mode)."
    }
    finally {
      Stop-ProcessSafe $forward
      Write-Host "Stopping remote rsync daemon..."
      # Graceful stop only if pid file exists; avoid brittle pkill
      Invoke-SSHInline "if test -f ~/rsyncd.pid; then kill \$(cat ~/rsyncd.pid); else echo 'No pid file; rsyncd stop skipped.'; fi"
    }
  }

  Write-Host "Done."
}
catch {
  Write-Error $_.Exception.Message
  exit 1
}
```

### Usage

**Prepare keys (once) and append to server:**

```powershell
ssh-keygen -t ed25519 -C "you@example.com"
.\coolice-ssh-rsync.ps1 -EnsureKey -ServerHost dc2.myusadc.com -ServerUser ibbsbbry -SshPort 22 -FileList .\filelist.txt
```

**`filelist.txt` examples (no quotes needed; one per line; Cygwin paths):**

```
/cygdrive/d/Documents and Settings/501106700/My Documents/project
/cygdrive/d/Documents and Settings/501106700/My Documents/Outlook
/cygdrive/c/Program Files/Lotus/Sametime Client/Chat Transcripts
```

**Run a sync (SSH mode, with compression & progress):**

```powershell
.\coolice-ssh-rsync.ps1 -ServerHost dc2.myusadc.com -ServerUser ibbsbbry -SshPort 22 -FileList .\filelist.txt -Mode SSH -Compress -Progress
```

**Daemon+tunnel mode (and create `rsyncd.conf` if missing):**

```powershell
.\coolice-ssh-rsync.ps1 -ServerHost dc2.myusadc.com -ServerUser ibbsbbry -SshPort 22 -FileList .\filelist.txt -Mode Daemon -EnsureRsyncdConf -Compress -Progress
```

**If host-key prompts block automation on older Win10 OpenSSH:**

```powershell
.\coolice-ssh-rsync.ps1 -ServerHost dc2.myusadc.com -ServerUser ibbsbbry -SshPort 22 -FileList .\filelist.txt -Mode SSH -InsecureHostKey
```

***

Economical backup solution: rsync and ssh
-----------------------------------------

As all other unix tricks this is also the result of laziness and the need. I wanted to backup data on my windows laptop to a central linux/unix server. I didn't want all the features of available expensive backup solutions. Just a simple updated copy of my data on a central machine which is backed up to the tape daily. rsync is known for fast incremental transfer and was an obvious choice for the purpose.

We have a unix machine at our workplace which has a directory structure /backup/username allocated for backing up user data. rsync has a client/server architecture, where rsync client talks to an rsync daemon at the server side (This statement may not be completely true. I am not sure and don't care also. You can refer to rsync manpage for complete discussion over rsync.). rsync client can connect to rsync server directly or through other remote transport programs like rsh, ssh etc. I decided to use ssh for transport for security and simplicity.

rsync daemon requires a configuration file rsyncd.conf. For my use, I have set it up like this:

\[manu@amusbocldmon01 ~\]$ cat rsyncd.conf
use chroot = no
\[backup\]
        path = /backup
        read only = no
        comment = backup area

This says,

\-do no chroot (required because I'll run it as a non-root user)  
\-\[backup\] specifies a module named backup.  
\-/backup is the path to backup module on filesystem

That's all we need at the server side. We don't need to keep rsync deamon running on the server. We'll start rsync daemon from the client using ssh before starting the backup.

At Windows side, we need rsync and some ssh client. rsync is available for windows through cygwin port. You can download cygwin from [http://www.cygwin.com/](http://www.cygwin.com/). While installing cygwin, remember to select rsync. For ssh client, you can either use ssh that comes with cygwin or plink command line tool that comes with putty. Since, I have already set up my putty for password-less authentication using public/private key pair and pageant, I'll demonstrate this solution using plink. However you can use any other ssh client too. You can download putty and plink from [http://www.chiark.greenend.org.uk/~sgtatham/putty/.](http://www.chiark.greenend.org.uk/~sgtatham/putty/) You can find much information about ssh password less authentication on the web. To keep commands short, add rsync and plink to Windows path. Let's start our backup now.

First, we need to start rsync daemon at the server. It can be started from the client using following command:

plink -v -t -l manu fileserver.local.com rsync --daemon --port=1873 --config=$HOME/rsyncd.conf

where, fileserver.local.com is the central server where we are going to store our data. This logs in user 'manu' on fileserver and starts a rsync daemon there at the port 1873. rsync goes to the background and plink returns immediately.

Next we need to setup an ssh transport tunnel using plink:

plink -v -N -L 873:localhost:1873 -l manu fileserver.local.com

This sets up the local port forwarding -- forwarding local port 873 to port 1873 on the remote server.

After running this, we have port 873 on our windows box connected to the port 1873 on the fileserver on which rsync daemon is listening. So, now we just need to run rsync on windows machine with localhost as the target server:

rsync -av src 127.0.0.1::backup/manu

This command copies file or dir '`src`' incrementally to directory '`manu`' inside 'backup' module. Since this rsync is the one that comes with cygwin, it understand only cygwin paths for the files. For that reason, 'src' needs to be specified in cygwin terms. For example, `D:\project `becomes `/cygdrive/d/project` in cygwin terms.

Putting it all in scripts:
--------------------------

This trick is not much handy, unless you put it in the scripts and make it easy to run. To automate the process, I created 2 small scripts:

plink\_rsync.bat: (To start plink for rsync)

REM Start rsync daemon the server
plink -v -t %\* rsync --daemon --port=1873 --config=$HOME/rsyncd.conf
REM Setup ssh transport tunnel.
plink -v -N -L 873:localhost:1873 %\*

runrsync.bat: (Main script - calls plink\_rsync.bat and starts rsync)

REM Start plink\_rsync.bat
START /MIN "PLINK\_FOR\_RSYNC" plink\_rsync.bat -l manu fileserver.local.com
REM Sleep for 15 seconds to give plink enough time to finish
sleep 15
REM Iterate through filenames in filelist.txt and rsync them
for /F "delims=" %%i in (filelist.txt) do rsync -av %%i 127.0.0.1::backup/manu
REM Kill plink\_rsync.bat window
TASKKILL /T /F /FI "WINDOWTITLE eq PLINK\_FOR\_RSYNC \*"
REM Kill remote rsync daemon
plink -l manu fileserver.local.com pkill rsync

The main script starts `plink_rsync.bat` in another window and sleeps for 15 seconds to make sure that connection is set up. Then it runs rsync over the files and directories list in` filelist.txt`. After rsyncing is done, it kills `plink_rsync.bat` window and kills rsync daemon on the remote server by running pkill though plink.

filelist.txt contains the list of files and directories that you want to take backup of. For example, my `filelist.txt` contains:

filelist.txt:

"/cygdrive/d/Documents and Settings/501106700/My Documents/project"
"/cygdrive/d/Documents and Settings/501106700/My Documents/Outlook"
"/cygdrive/c/Program Files/Lotus/Sametime Client/Chat Transcripts"

You can schedule runrsync.bat to run everyday or every week depending on your requirement.
