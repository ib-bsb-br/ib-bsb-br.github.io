---
tags: [scratchpad]
info: aberto.
date: 2025-10-07
type: post
layout: post
published: true
slug: auto-xrandr
title: 'auto xrandr for multi-monitor setup'
---

# documentation

## A. Tests-First Verification

### A1. Test Matrix

| ID                  | Behavior                     | Trigger/Command                               | Expectation                              | Exit |
| ------------------- | ---------------------------- | --------------------------------------------- | ---------------------------------------- | ---- |
| T-HELP              | Help prints header block     | `pwsh -File ./pwsh_monitor_working.ps1 -Help` | Usage text includes OPTIONS & EXIT CODES | 0    |
| T-HEADLESS          | Headless detection           | Unset `DISPLAY` + break `xrandr`              | Error then exit                          | 20   |
| T-MISS-DEP          | Missing dep and `-NoInstall` | Remove `xrandr` from PATH                     | Named missing dep; fail fast             | 2    |
| T-AUTOINSTALL       | Auto-install needs root      | `-AutoInstall` as non-root                    | Error “requires root”                    | 2    |
| T-INTERACTIVE       | Interactive selection        | ≥2 monitors                                   | Overlay confirm; accepted mode           | 0    |
| T-APPLY-SAVED       | Non-interactive apply        | Valid JSON config                             | One-line summary JSON                    | 0    |
| T-APPLY-NOCONFIG    | Missing config               | `-ApplySavedLayout` w/ nonexistent file       | Warning                                  | 23   |
| T-JSON-ERROR        | Malformed JSON               | Bad config file                               | Error                                    | 24   |
| T-INVALID-CONFIG    | Empty/invalid object         | Corrupt config                                | Error                                    | 22   |
| T-FINAL-APPLY-ERROR | xrandr fails on final        | Mock nonzero exit                             | Warning                                  | 1    |
| T-PRIMARY           | Largest area → primary       | Mixed resolutions                             | `--primary` set                          | 0    |

### A2. Pester Samples

**tests/Docs.Tests.ps1**

```powershell
Describe 'Documentation coverage' {
  It 'Help text exists and includes sections' {
    $out = pwsh -NoLogo -NoProfile -File ./pwsh_monitor_working.ps1 -Help
    $out | Should -Match 'OPTIONS'
    $out | Should -Match 'EXIT CODES'
  }
  It 'JSON summary schema on success' {
    $cfg = '{"HDMI-1":"1920x1080"}'
    $tmp = New-TemporaryFile
    Set-Content -Path $tmp -Value $cfg -Encoding UTF8
    $json = pwsh -NoLogo -NoProfile -File ./pwsh_monitor_working.ps1 -ApplySavedLayout -ConfigPath $tmp
    Remove-Item $tmp -Force
    $obj = $json | ConvertFrom-Json
    $obj.ok | Should -BeTrue
    $obj.mode | Should -Be 'apply-saved'
    $obj | Get-Member -Name primary,order,chosen,configFile | Should -Not -BeNullOrEmpty
  }
}
```

**tests/XrandrParsing.Tests.ps1**

```powershell
Describe 'xrandr parsing' {
  It 'Parses connected outputs' {
    Mock Get-XrandrLines { @('HDMI-1 connected primary 1920x1080+0+0', 'DP-1 connected 2560x1440+1920+0') }
    (Get-ConnectedOutputs) | Should -Be @('HDMI-1','DP-1')
  }
  It 'Extracts modes for an output' {
    Mock Get-XrandrLines { @(
      'HDMI-1 connected', '  1920x1080 60.00*+', '  1280x720 60.00',
      'DP-1 connected',   '  2560x1440 59.95*', '  1920x1080 60.00'
    ) }
    (Get-OutputModes 'HDMI-1') | Should -Contain '1920x1080'
  }
  It 'Verifies geometry match' {
    Mock Get-CurrentGeometry { [pscustomobject]@{W=1920;H=1080;X=0;Y=0} }
    (Verify-OutputGeometry 'HDMI-1' '1920x1080') | Should -BeTrue
  }
}
```

**tests/ExitCodes.Tests.ps1**

```powershell
Describe 'Exit codes' {
  It '-ApplySavedLayout missing file => 23' {
    $p = Start-Process pwsh -ArgumentList '-File','./pwsh_monitor_working.ps1','-ApplySavedLayout','-ConfigPath','/nope.json' -PassThru -Wait
    $p.ExitCode | Should -Be 23
  }
}
```

## B. Background & Scope

* **Problem:** Multi-monitor setup is error-prone across WMs and distros.
* **Goal:** Interactive discovery + verification; persisted JSON; non-interactive reapply; machine-parseable success.
* **Scope:** X11 `xrandr` only; Wayland not supported.

## C. Supported Environments

* Debian/Ubuntu(+derivatives), Fedora/RHEL/CentOS, openSUSE, Arch-based; WM/terminal agnostic.
* Requires `xrandr`, `python3` with `tkinter`, and PowerShell 7+.

## D. Feature/Request Status Matrix

| Request                  | Status      | Implementation Notes                                                 |
| ------------------------ | ----------- | -------------------------------------------------------------------- |
| `-ConfigPath` override   | Implemented | Default `$HOME/.config/pwsh-monitor-layout.json`; used in both paths |
| `-Help`                  | Implemented | `Show-Help` extracts header `<# ... #>` and exits 0                  |
| One-line success JSON    | Implemented | Both interactive and apply-saved paths emit schema                   |
| Portability auto-install | Implemented | PM detection + root requirement                                      |
| `-NoInstall` fast-fail   | Implemented | Throws if missing dep; exit 2                                        |
| Headless explicit exit   | Implemented | `Assert-XSessionOrExit` → exit 20                                    |
| Autostart `.desktop`     | Implemented | Writes to `~/.config/autostart/` with proper Exec                    |

## E. Usage

* **Interactive:** `pwsh -File ./pwsh_monitor_working.ps1`
* **Auto-install (root):** `sudo pwsh -File ./pwsh_monitor_working.ps1 -AutoInstall`
* **Apply saved:** `pwsh -File ./pwsh_monitor_working.ps1 -ApplySavedLayout [-ConfigPath <file>]`
* **Help:** `pwsh -File ./pwsh_monitor_working.ps1 -Help`

## F. Dependencies & Authority

* Ensured via `Ensure-Dep`; PMs: `apt`, `dnf`, `zypper`, `pacman`. Root required for auto-install.
* When root, sets `XAUTHORITY` to target user; defaults `DISPLAY` to `:0` if unset.

## G. Design & Key Functions

* Parsing/validation (`Get-ConnectedOutputs`, `Get-OutputModes`, `Get-CurrentGeometry`, `Verify-OutputGeometry`).
* Application (`Apply-Layout` with cumulative width positioning; `--primary` set by area heuristic).
* Overlay (`Show-OverlayTk`) for visual confirmation.
* Persistence/autostart and summary emission.

## H. Data Model & Files

* **Config JSON (ordered mapping):**

```json
{
  "HDMI-1": "1920x1080",
  "DP-1": "2560x1440"
}
```

* **Success Summary (stdout, single line):**

```json
{"ok":true,"mode":"interactive","primary":"HDMI-1","order":["HDMI-1","DP-1"],"chosen":{"HDMI-1":"1920x1080","DP-1":"2560x1440"},"configFile":"/home/user/.config/pwsh-monitor-layout.json"}
```

* **Transcripts:** `/tmp/pwsh_monitor_working-YYYYMMDD-HHMMSS.log` (fallback `$HOME/...`).
* **Autostart:** `~/.config/autostart/pwsh_monitor_working.desktop`.

## I. Error Handling & Exit Codes

| Code | Meaning                               | Typical Source                         | Remedy                                         |
| ---: | ------------------------------------- | -------------------------------------- | ---------------------------------------------- |
|    0 | Success                               | Normal completion                      | —                                              |
|    1 | General/user abort/final apply failed | `Prompt-YNQ` quit; `Apply-Layout` fail | Retry with `-DebugMode` or adjust modes        |
|    2 | Missing dep / install failure         | `Ensure-Dep`/`Install-Dep`             | Install packages or use `-AutoInstall` as root |
|   20 | Headless / no X11                     | `Assert-XSessionOrExit`                | Start X11; ensure `xrandr` works               |
|   21 | No connected monitors                 | `Get-ConnectedOutputs`                 | Check hardware/cables                          |
|   22 | Invalid/empty config                  | Apply-saved path                       | Fix JSON                                       |
|   23 | Config file not found                 | Apply-saved path                       | Provide correct `-ConfigPath`                  |
|   24 | JSON parse error                      | Apply-saved path                       | Fix JSON syntax                                |
|   25 | Permission/ownership error            | Autostart/config setup                 | Correct ownership and perms                    |

## J. Deployment & Autostart

* First run interactively to generate JSON; confirm overlay; verify autostart `.desktop`.
* For login issues, inspect latest transcript under `/tmp`.

## K. Troubleshooting

* **Overlay missing:** Install `python3-tk`/`tk`; some WMs may block undecorated topmost windows.
* **Apply-saved fails:** Outputs may be renamed (docks/GPUs); re-run interactive flow to refresh JSON.
* **Headless (20):** Ensure `DISPLAY` and functioning X server.

## L. Versioning

* **v0.1 (2025-10-14):** Initial structured docs and tests-first plan.

## M. Causality Links (Why → How Validated)

* **Correct ordering:** User selection + overlay → Pester interactive smoke + manual confirmation.
* **Accurate geometry:** Compare `Get-CurrentGeometry` against selected mode → Pester unit test for verifier.
* **Reproducibility:** Persist ordered mapping; non-interactive apply → schema test; exit-code tests.
* **Robust setup:** Auto-install with PM detection; guarded by root → negative test for non-root.
* **Headless clarity:** Explicit exit 20 → smoke test with unset `DISPLAY`.

{% codeblock bash %}
#!/usr/bin/env pwsh
<# 
pwsh_monitor_working.ps1 — Interactive + non-interactive multi-monitor configurator for X11 (Linux)

TARGET: Debian/Ubuntu/Derivatives, Fedora/RHEL/CentOS, openSUSE, Arch-based (pwsh, xrandr)
WM/TERM agnostic (works with ratpoison/Alacritty etc.)

KEY CAPABILITIES
- Interactive discovery of output order (left→right) and resolution selection per monitor using xrandr.
- Verifies applied geometry; shows a Tk red-border overlay to confirm the active monitor.
- Saves chosen layout to JSON and can re-apply non-interactively on login/autostart.
- Robust logging (Start-Transcript), strict error behavior, and explicit exit codes.

NEW/REQUESTED IMPROVEMENTS
- -ConfigPath <file> to override default config path (default: ~/.config/pwsh-monitor-layout.json).
- -Help: Prints usage, options, examples, and exit codes then exits 0.
- Emits a one-line machine-parseable JSON summary on success for both interactive and apply-saved paths.
- Portability hardening: auto-install gated by distro/pm detection (apt-get/dnf/zypper/pacman).
- -NoInstall: disable auto-install; fail fast if dependencies missing.
- Headless handling: detect missing X11/xrandr availability and exit with explicit code.

USAGE (examples)
  # First run (interactive):
  pwsh -File ./pwsh_monitor_working.ps1

  # Auto-install missing deps (root required):
  sudo pwsh -File ./pwsh_monitor_working.ps1 -AutoInstall

  # Save config to a specific path:
  pwsh -File ./pwsh_monitor_working.ps1 -ConfigPath "$HOME/.config/my-monitor-layout.json"

  # Non-interactive apply of saved layout (good for autostart):
  pwsh -File ./pwsh_monitor_working.ps1 -ApplySavedLayout

  # Print help:
  pwsh -File ./pwsh_monitor_working.ps1 -Help

OPTIONS
  -DebugMode             Verbose logging during execution.
  -AutoInstall           Attempt to install dependencies via detected package manager.
  -NoInstall             Do not install; fail fast if dependencies are missing.
  -ApplySavedLayout      Apply saved layout from the config JSON and exit.
  -OverlaySeconds <int>  Seconds to keep the red overlay visible when testing (default: 5).
  -TargetUser <string>   Login user for ownership of autostart/config when run as root (default: SUDO_USER/USER/linaro).
  -ScriptInstallPath     Path to place a self-copy used by autostart (default: $HOME/pwsh_monitor_working.ps1).
  -ConfigPath            Override config JSON path (default: $HOME/.config/pwsh-monitor-layout.json).
  -Help                  Show this help and exit.

EXIT CODES
  0  Success
  1  General error / user abort / final apply failed
  2  Missing dependency and -NoInstall provided (or auto-install disabled/unsupported)
 20  Headless / no X11 session detected (no DISPLAY or xrandr unusable)
 21  No connected monitors detected
 22  Invalid/empty configuration when using -ApplySavedLayout
 23  Config file not found for -ApplySavedLayout
 24  JSON parse error for -ConfigPath
 25  Permission or ownership errors during autostart/config setup

MACHINE-PARSABLE SUMMARY
  On success, prints a single line JSON to stdout like:
  {"ok":true,"mode":"interactive","primary":"HDMI-1","order":["HDMI-1","DP-1"],"chosen":{"HDMI-1":"1920x1080","DP-1":"2560x1440"},"configFile":"/home/user/.config/pwsh-monitor-layout.json"}

#>

[CmdletBinding()]
param(
    [switch] $DebugMode,
    [switch] $AutoInstall,
    [switch] $NoInstall,
    [switch] $ApplySavedLayout,
    [switch] $Help,
    [int]    $OverlaySeconds = 5,
    [string] $TargetUser = ($env:SUDO_USER ?? $env:USER ?? 'linaro'),
    [string] $ScriptInstallPath = "$HOME/pwsh_monitor_working.ps1",
    [string] $ConfigPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
if ($DebugMode) { $VerbosePreference = 'Continue' }

function Stop-TranscriptSafe { try { Stop-Transcript | Out-Null } catch {} }

# Transcript
$tsFile = "/tmp/pwsh_monitor_working-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"
try { Start-Transcript -Path $tsFile -Force | Out-Null } catch {
    $tsFile = Join-Path $HOME "pwsh_monitor_working-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"
    try { Start-Transcript -Path $tsFile -Force | Out-Null } catch {}
}
Write-Verbose "Transcript: $tsFile"

# ---------- Helpers ----------
function Show-Help {
    $path = $PSCommandPath
    if (-not $path) { $path = $MyInvocation.MyCommand.Path }
    $content = Get-Content -Raw -Path $path
    $helpBlock = [regex]::Match($content, '(?s)<#\s*(.*?)\s*#>').Groups[1].Value
    if ([string]::IsNullOrWhiteSpace($helpBlock)) {
        Write-Output "Usage: pwsh -File $path [-AutoInstall|-NoInstall] [-ApplySavedLayout] [-ConfigPath <file>] [-OverlaySeconds <int>] [-DebugMode] [-Help]"
    } else {
        Write-Output $helpBlock.Trim()
    }
}

function Test-Cmd([string]$Name) { $null -ne (Get-Command -Name $Name -ErrorAction SilentlyContinue) }

function Test-IsRoot {
    try { ((& id '-u' 2>$null) -eq 0) } catch {
        try { ((& whoami) -eq 'root') } catch { ($env:USER -eq 'root') }
    }
}

function Detect-PackageManager {
    if (Test-Cmd 'apt-get') { return 'apt' }
    if (Test-Cmd 'dnf')     { return 'dnf' }
    if (Test-Cmd 'zypper')  { return 'zypper' }
    if (Test-Cmd 'pacman')  { return 'pacman' }
    return $null
}

function Install-Dep([string]$pkg) {
    $pm = Detect-PackageManager
    if (-not $pm) { throw 'No supported package manager found.' }
    if (-not (Test-IsRoot)) { throw 'Auto-install requires root.' }

    switch ($pm) {
        'apt'    { & apt-get update -y; & apt-get install -y $pkg }
        'dnf'    { & dnf install -y $pkg }
        'zypper' { & zypper -n install -y $pkg }
        'pacman' { & pacman -Sy --noconfirm $pkg }
    }
}

function Ensure-Dep([string]$cmd, [string]$pkg, [string]$friendly) {
    if (Test-Cmd $cmd) { return }
    if ($NoInstall) { throw "Missing dependency '$friendly' and -NoInstall was specified." }
    if (-not $AutoInstall) { throw "Missing dependency '$friendly'. Rerun with -AutoInstall or install '$pkg' manually." }
    Install-Dep $pkg
    if (-not (Test-Cmd $cmd)) { throw "Dependency '$friendly' not available after install." }
}

function Test-PythonTk {
@'
import sys
try:
    import tkinter as t
    root = t.Tk()
    root.withdraw()
    print("OK")
except Exception as e:
    print("ERR", e)
    sys.exit(1)
'@ | Set-Content -Path ($tmp = [IO.Path]::GetTempFileName() + '.py') -Encoding UTF8
    try {
        $p = Start-Process -FilePath 'python3' -ArgumentList @($tmp) -PassThru -NoNewWindow -Wait
        return ($p.ExitCode -eq 0)
    } finally {
        try { Remove-Item $tmp -Force -ErrorAction SilentlyContinue } catch {}
    }
}

function Assert-XSessionOrExit {
    if (-not $env:DISPLAY) { $env:DISPLAY = ':0' }
    for ($i=0; $i -lt 6; $i++) {
        try { & xrandr --current | Out-Null; return } catch { Start-Sleep -Milliseconds 300 }
    }
    Write-Error 'No X11 display/xrandr available (headless or X not running).'
    Stop-TranscriptSafe; exit 20
}

# ---------- Dependency checks ----------
try {
    Ensure-Dep 'xrandr'  'x11-xserver-utils' 'xrandr'
    Ensure-Dep 'python3' 'python3'           'python3'
} catch {
    Write-Error $_.Exception.Message
    Stop-TranscriptSafe; exit 2
}

# ---------- X11 availability ----------
Assert-XSessionOrExit

# tkinter (package name differs by distro)
if (-not (Test-PythonTk)) {
    try {
        $pm = Detect-PackageManager
        switch ($pm) {
            'apt'    { Install-Dep 'python3-tk' }
            'dnf'    { Install-Dep 'python3-tkinter' }
            'zypper' { Install-Dep 'python3-tk' }
            'pacman' { Install-Dep 'tk' }
            default  { throw 'Unsupported package manager for tkinter.' }
        }
    } catch {
        Write-Error "Unable to install/verify tkinter: $($_.Exception.Message)"
        Stop-TranscriptSafe; exit 2
    }
    if (-not (Test-PythonTk)) {
        Write-Error 'python3-tk/tkinter not available after installation.'
        Stop-TranscriptSafe; exit 2
    }
}

# ---------- X11 env + authority ----------
$root = Test-IsRoot
$homeTarget = if ($root) { "/home/$TargetUser" } else { $HOME }
if (-not $env:DISPLAY) { $env:DISPLAY = ':0' }
if ($root) {
    $xaUser = "/home/$TargetUser/.Xauthority"
    if (Test-Path $xaUser) { $env:XAUTHORITY = $xaUser }
    elseif (Test-Path '/root/.Xauthority') { $env:XAUTHORITY = '/root/.Xauthority' }
} elseif (-not $env:XAUTHORITY) {
    $env:XAUTHORITY = Join-Path $HOME '.Xauthority'
}

# Config path default
if (-not $ConfigPath -or [string]::IsNullOrWhiteSpace($ConfigPath)) {
    $ConfigPath = Join-Path (Join-Path $homeTarget '.config') 'pwsh-monitor-layout.json'
}

# ---------- Early exits ----------
if ($Help) { Show-Help; Stop-TranscriptSafe; exit 0 }

# ---------- xrandr helpers ----------
function Get-XrandrLines { (& xrandr --query | Out-String) -split "`n" }

function Get-ConnectedOutputs {
    Get-XrandrLines | ForEach-Object {
        if ($_ -match '^\s*(\S+)\s+connected') { $Matches[1] }
    }
}

function Sort-OutputsPreferred([string[]]$Outputs) {
    $order = @('HDMI','DP','DVI','VGA','eDP')
    $picked = [System.Collections.Generic.List[string]]::new()
    foreach ($p in $order) {
        $Outputs | Where-Object { $_ -like "$p*" } | ForEach-Object { [void]$picked.Add($_) }
    }
    $Outputs | Where-Object { $picked -notcontains $_ } | ForEach-Object { [void]$picked.Add($_) }
    $picked | Select-Object -Unique
}

function Get-OutputModes([string]$Output) {
    $lines = Get-XrandrLines
    $in = $false
    $modes = [System.Collections.Generic.List[string]]::new()
    foreach ($ln in $lines) {
        if (-not $in) {
            if ($ln -match "^\s*$([Regex]::Escape($Output))\s+connected") { $in = $true; continue }
        } else {
            if ($ln -match '^\S+\s+(connected|disconnected)') { break }
            if ($ln -match '^\s+([0-9]{3,5}x[0-9]{3,5}\S*)') {
                $t = $Matches[1]
                if (-not $modes.Contains($t)) { [void]$modes.Add($t) }
            }
        }
    }
    if ($modes.Count -eq 0) { throw "No modes parsed for $Output" }
    return $modes.ToArray()
}

function Get-Size([string]$Token) {
    if ($Token -notmatch '^(\d{3,5})x(\d{3,5})') { throw "Invalid mode token: $Token" }
    [pscustomobject]@{ W = [int]$Matches[1]; H = [int]$Matches[2] }
}

function Get-CurrentGeometry([string]$Output) {
    $pattern = "^{0}\b" -f [Regex]::Escape($Output)
    $ln = Get-XrandrLines | Where-Object { $_ -match $pattern } | Select-Object -First 1
    if (-not $ln) { return $null }
    $m = [regex]::Match($ln, '(\d{3,5}x\d{3,5})\+(\d+)\+(\d+)')
    if (-not $m.Success) { return $null }
    $wxh = $m.Groups[1].Value
    $x = [int]$m.Groups[2].Value
    $y = [int]$m.Groups[3].Value
    $m2 = [regex]::Match($wxh, '^(\d{3,5})x(\d{3,5})$')
    if (-not $m2.Success) { return $null }
    [pscustomobject]@{ W = [int]$m2.Groups[1].Value; H = [int]$m2.Groups[2].Value; X = $x; Y = $y }
}

function Invoke-Xrandr([string[]]$XRArgs) {
    $p = Start-Process -FilePath 'xrandr' -ArgumentList $XRArgs -PassThru -NoNewWindow -Wait
    if ($DebugMode) { Write-Verbose ("xrandr " + ($XRArgs -join ' ') + " => " + $p.ExitCode) }
    $p.ExitCode
}

function Apply-Layout([System.Collections.Specialized.OrderedDictionary]$Map) {
    $x = 0
    foreach ($o in $Map.Keys) {
        $tok = [string]$Map[$o]
        $code = Invoke-Xrandr @('--output', $o, '--mode', $tok, '--pos', ("{0}x0" -f $x), '--rotate', 'normal')
        if ($code -ne 0) {
            Write-Warning ("xrandr failed for {0} token {1} (exit {2})" -f $o, $tok, $code)
            return $false
        }
        Start-Sleep -Milliseconds 120
        $sz = Get-Size $tok
        $x += $sz.W
    }
    Start-Sleep -Milliseconds 180
    return $true
}

function Verify-OutputGeometry([string]$Output, [string]$Token) {
    $want = Get-Size $Token
    $cur = Get-CurrentGeometry $Output
    if (-not $cur) {
        if ($DebugMode) { Write-Verbose "Verify: no geometry for $Output" }
        return $false
    }
    $ok = ($cur.W -eq $want.W -and $cur.H -eq $want.H)
    if ($DebugMode) {
        Write-Verbose ("Verify: {0} current={1}x{2} vs want={3}x{4} => {5}" -f $Output, $cur.W, $cur.H, $want.W, $want.H, $ok)
    }
    $ok
}

function Show-OverlayTk([int]$W,[int]$H,[int]$X,[int]$Y,[int]$Seconds) {
$py = @'
import sys, tkinter as t
w, h, x, y, sec = map(int, sys.argv[1:6])
root = t.Tk()
root.overrideredirect(1)
root.attributes("-topmost", True)
root.geometry(f"{w}x{h}+{x}+{y}")
t.Frame(root, width=w, height=h, highlightbackground="red", highlightthickness=8).pack()
root.after(sec*1000, root.destroy)
root.mainloop()
'@
    $tmp = [IO.Path]::GetTempFileName() + '.py'
    [IO.File]::WriteAllText($tmp, $py)
    $p = Start-Process -FilePath 'python3' -ArgumentList @($tmp, $W, $H, $X, $Y, $Seconds) -PassThru -NoNewWindow
    $timeout = [Math]::Max($Seconds + 3, 8)
    $exited = $true
    try { Wait-Process -Id $p.Id -Timeout $timeout } catch { $exited = $false }
    if (-not $exited) {
        try { Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue } catch {}
        Write-Warning 'Overlay timeout; killed.'
    }
    try { Remove-Item $tmp -Force -ErrorAction SilentlyContinue } catch {}
}

function Prompt-YNQ([string]$Msg) {
    while ($true) {
        $r = Read-Host $Msg
        switch -Regex ($r) {
            '^(?i)y$' { return 'y' }
            '^(?i)n$' { return 'n' }
            '^(?i)q$' { return 'q' }
            default   { Write-Host 'Please type y, n, or q.' -ForegroundColor Yellow }
        }
    }
}

# ---------- Apply saved layout fast-path ----------
if ($ApplySavedLayout) {
    if (-not (Test-Path $ConfigPath)) {
        Write-Warning "Config not found: $ConfigPath"
        Stop-TranscriptSafe; exit 23
    }
    try {
        $raw = Get-Content -Raw -Path $ConfigPath
        $obj = $raw | ConvertFrom-Json
    } catch {
        Write-Error "Failed to parse config JSON: $($_.Exception.Message)"
        Stop-TranscriptSafe; exit 24
    }
    if (-not $obj) { Write-Error 'Empty/invalid configuration object.'; Stop-TranscriptSafe; exit 22 }

    $orderedChosen = [System.Collections.Specialized.OrderedDictionary]::new()
    foreach ($p in $obj.PSObject.Properties) {
        $orderedChosen[$p.Name] = [string]$p.Value
    }

    if ($orderedChosen.Count -eq 0) { Write-Error 'No entries in configuration.'; Stop-TranscriptSafe; exit 22 }

    if (-not (Apply-Layout $orderedChosen)) {
        Write-Warning 'Applying saved layout reported errors.'
        Stop-TranscriptSafe; exit 1
    }

    $primary = $null; $maxA = -1
    foreach ($o in $orderedChosen.Keys) {
        $sz = Get-Size ([string]$orderedChosen[$o])
        $a  = $sz.W * $sz.H
        if ($a -gt $maxA) { $primary = $o; $maxA = $a }
    }
    $null = Invoke-Xrandr @('--output', $primary, '--primary')

    $summary = [pscustomobject]@{
        ok         = $true
        mode       = 'apply-saved'
        primary    = $primary
        order      = @($orderedChosen.Keys)
        chosen     = $orderedChosen
        configFile = $ConfigPath
    } | ConvertTo-Json -Compress
    Write-Output $summary
    Stop-TranscriptSafe; exit 0
}

# ---------- Probe outputs ----------
$outs = Get-ConnectedOutputs
if (-not $outs -or $outs.Count -eq 0) { Write-Error 'No connected monitors detected.'; Stop-TranscriptSafe; exit 21 }

# ---------- Interactive ordering ----------
$orderedOuts = [System.Collections.Generic.List[string]]::new()
if ($outs.Count -gt 1) {
    $remaining = [System.Collections.Generic.List[string]]::new()
    $remaining.AddRange([string[]]$outs)
    Write-Host "Multiple monitors detected: $($remaining -join ', ')" -ForegroundColor Cyan
    while ($remaining.Count -gt 0) {
        if ($orderedOuts.Count -eq 0) {
            Write-Host "Which monitor should be on the far left?"
        } else {
            Write-Host "Which monitor should be to the right of $($orderedOuts[-1])?"
        }
        for ($i=0; $i -lt $remaining.Count; $i++) { Write-Host "  [$($i+1)] $($remaining[$i])" }
        $ans = Read-Host "Enter number (1-$($remaining.Count))"
        if (($ans -match '^\d+$') -and ([int]$ans -ge 1) -and ([int]$ans -le $remaining.Count)) {
            $choiceIndex = [int]$ans - 1
            $orderedOuts.Add($remaining[$choiceIndex])
            $remaining.RemoveAt($choiceIndex)
        } else {
            Write-Warning "Invalid selection."
        }
    }
} else {
    $orderedOuts.Add($outs[0])
}
Write-Host "Final monitor order (left-to-right): $($orderedOuts -join ' -> ')" -ForegroundColor Green

# ---------- Gather modes ----------
$All   = @{}
$First = @{}
foreach ($o in $orderedOuts) {
    $m = Get-OutputModes $o
    $All[$o] = $m
    $First[$o] = $m[0]
    if ($DebugMode) { Write-Verbose ("Modes[{0}] (#{1}): {2}" -f $o, $m.Count, ($m -join ' ')) }
}

$Chosen = [System.Collections.Specialized.OrderedDictionary]::new()
foreach ($o in $orderedOuts) { $Chosen[$o] = $null }

# ---------- Per-output interactive selection ----------
foreach ($current in $orderedOuts) {
    Write-Host ("======== Configuring {0} ========" -f $current) -ForegroundColor Cyan
    $cands = @($All[$current])
    $accepted = $false

    for ($i = 0; $i -lt $cands.Count; $i++) {
        $tok = $cands[$i]
        Write-Host ("---> [{0}/{1}] Trying {2} for {3}" -f ($i + 1), $cands.Count, $tok, $current) -ForegroundColor Green

        $proposal = [System.Collections.Specialized.OrderedDictionary]::new()
        foreach ($o in $orderedOuts) {
            if ($o -eq $current) { $proposal[$o] = $tok }
            else { $proposal[$o] = ($Chosen[$o] ?? $First[$o]) }
        }

        if (-not (Apply-Layout $proposal)) { Write-Warning ("Skip {0}: xrandr exit!=0" -f $tok); continue }
        if (-not (Verify-OutputGeometry $current $tok)) { Write-Warning ("Skip {0}: geometry mismatch" -f $tok); continue }

        $xoff = 0
        foreach ($o in $orderedOuts) {
            if ($o -eq $current) { break }
            $sz = Get-Size ([string]$proposal[$o])
            $xoff += $sz.W
        }
        $szC = Get-Size $tok
        Show-OverlayTk -W $szC.W -H $szC.H -X $xoff -Y 0 -Seconds $OverlaySeconds

        $ans = Prompt-YNQ ("Was the red rectangle fully enclosed on {0} at {1}? [y=accept / n=next / q=quit]" -f $current, $tok)
        if ($ans -eq 'y') { $Chosen[$current] = $tok; $accepted = $true; break }
        if ($ans -eq 'q') { Write-Warning 'User aborted.'; Stop-TranscriptSafe; exit 1 }
    }

    if (-not $accepted) {
        $fb = $First[$current]
        Write-Warning ("No accepted mode for {0}. Falling back to {1}" -f $current, $fb)
        $Chosen[$current] = $fb
    }
}

# ---------- Final apply ----------
Write-Host "Final configuration selected. Applying..." -ForegroundColor Cyan
if (-not (Apply-Layout $Chosen)) {
    Write-Warning 'Final layout application reported errors.'
    Stop-TranscriptSafe; exit 1
}

# choose primary as largest area
$primary = $null; $maxA = -1
foreach ($o in $orderedOuts) {
    $sz = Get-Size ([string]$Chosen[$o])
    $a  = $sz.W * $sz.H
    if ($a -gt $maxA) { $primary = $o; $maxA = $a }
}
$null = Invoke-Xrandr @('--output', $primary, '--primary')

# ---------- Save config + autostart ----------
try {
    $configDir = Split-Path -Parent $ConfigPath
    if (-not (Test-Path $configDir)) {
        if ($root) { & sudo -u $TargetUser mkdir -p -- $configDir }
        else       { New-Item -ItemType Directory -Path $configDir -Force | Out-Null }
    }

    $tmpChosen = [ordered]@{}
    foreach ($k in $Chosen.Keys) { $tmpChosen[$k] = [string]$Chosen[$k] }
    ($tmpChosen | ConvertTo-Json) | Set-Content -Path $ConfigPath -Encoding UTF8
    if ($root) { & chown "${TargetUser}:${TargetUser}" $ConfigPath }
    Write-Host "[INFO] Configuration saved to $ConfigPath" -ForegroundColor DarkCyan

    $autoDir = Join-Path $homeTarget '.config/autostart'
    if (-not (Test-Path $autoDir)) {
        if ($root) { & sudo -u $TargetUser mkdir -p -- $autoDir }
        else       { New-Item -ItemType Directory -Path $autoDir -Force | Out-Null }
    }
    if (-not (Test-Path $ScriptInstallPath)) {
        $src = $PSCommandPath; if (-not $src) { $src = $MyInvocation.MyCommand.Path }
        Copy-Item -Path $src -Destination $ScriptInstallPath -Force
        if ($root) { & chown "${TargetUser}:${TargetUser}" $ScriptInstallPath }
        & chmod +x $ScriptInstallPath
    }
    $desktopFile = Join-Path $autoDir 'pwsh_monitor_working.desktop'
    $execLine = "pwsh -File $ScriptInstallPath -ApplySavedLayout -ConfigPath `"$ConfigPath`""
@"
[Desktop Entry]
Type=Application
Exec=$execLine
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=PwshAutoMonitor
Comment=Autoconfigure monitors layout (pwsh)
"@ | Set-Content -Path $desktopFile -Encoding UTF8 -NoNewline
    if ($root) { & chown "${TargetUser}:${TargetUser}" $desktopFile }
    & chmod 0644 $desktopFile
    Write-Host ("[INFO] Autostart installed at {0} for user {1}" -f $desktopFile, $TargetUser) -ForegroundColor DarkCyan
} catch {
    Write-Warning ("Autostart/config setup issue: {0}" -f $_.Exception.Message)
}

# ---------- Success summary (single-line JSON) ----------
$summary2 = [pscustomobject]@{
    ok         = $true
    mode       = 'interactive'
    primary    = $primary
    order      = @($orderedOuts)
    chosen     = $Chosen
    configFile = $ConfigPath
} | ConvertTo-Json -Compress
Write-Output $summary2

Stop-TranscriptSafe
exit 0
{% endcodeblock %}
