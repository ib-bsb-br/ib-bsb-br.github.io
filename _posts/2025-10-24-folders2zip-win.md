---
tags:
  - 'scripts>powershell'
date: '2025-10-24'
type: post
layout: post
published: true
slug: folders2zip-win
title: 'folders2zip as non-admin Windows user'

---
{% codeblock powershell %}
#requires -Version 5.1
<#!
.SYNOPSIS
  Single-file archive as a non-admin Windows 10 user — create/overwrite/update a .zip of a folder; optional restore.

.DESCRIPTION
  Creates a single .zip archive of SourceDir with robust handling for invalid file timestamps by clamping
  to the ZIP spec range (1980-01-01 to 2107-12-31). No admin required. ASCII-only script for PS 5.1.
  This refactored version:
    - Sets ZipArchiveEntry.LastWriteTime BEFORE opening the entry stream (required for Create mode)
    - Prevents temp-file self-inclusion by blocking Create/Overwrite when ArchivePath is under SourceDir
    - Skips both ArchivePath and its temp path during Create/Overwrite enumeration

.PARAMETER SourceDir
  Absolute path to the folder to archive recursively.

.PARAMETER ArchivePath
  Target .zip file path. Default: $env:LOCALAPPDATA\SingleArchive\Out\<Leaf(SourceDir)>.zip

.PARAMETER RestoreDir
  Destination folder for optional restore/extract. Default: $env:LOCALAPPDATA\SingleArchive\Restored\<Leaf(SourceDir)>

.PARAMETER Mode
  Create    - Create new .zip; if it exists, prompt (or -Force) to use a timestamped name.
  Overwrite - Replace existing .zip atomically.
  Update    - Open or create .zip and add/replace entries that changed (does not delete removed files).

.PARAMETER VerifyOnly
  Compute and display stats (source, archive) without writing.

.PARAMETER DoRestore
  After archive step, extract the .zip to RestoreDir.

.PARAMETER Force
  Skip confirmations for overwrites and existing destination handling.

.PARAMETER DryRun
  Simulate actions; do not write.

.EXAMPLE
  .\SingleFile-Archive.ps1 -SourceDir "C:\Data\Docs" -Mode Create -Verbose

.EXAMPLE
  .\SingleFile-Archive.ps1 -SourceDir "C:\Data\Docs" -Mode Update -DoRestore -Force -Verbose

.NOTES
  Compress-Archive may fail on out-of-range timestamps. This script uses a .NET ZipArchive pipeline that clamps
  timestamps and avoids that failure for Create/Overwrite/Update. It also guards against self-inclusion when the
  archive destination resides under the source tree.
#>

[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)]
  [ValidateScript({ Test-Path $_ -PathType Container })]
  [string]$SourceDir,

  [string]$ArchivePath,

  [string]$RestoreDir,

  [ValidateSet('Create','Overwrite','Update')]
  [string]$Mode = 'Create',

  [switch]$VerifyOnly,
  [switch]$DoRestore,
  [switch]$Force,
  [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# ---------------------------- Helpers -----------------------------------------

function Write-Step { param([string]$Message) Write-Host ("[+] {0}" -f $Message) }
function Write-Sub  { param([string]$Message) Write-Host ("    - {0}" -f $Message) }

function Confirm-Action {
  param([Parameter(Mandatory=$true)][string]$Prompt,[switch]$DefaultNo)
  if ($Force) { return $true }
  $def = if ($DefaultNo) {'N'} else {'Y'}
  $choices = if ($DefaultNo) {'[y/N]'} else {'[Y/n]'}
  while ($true) {
    $resp = Read-Host "$Prompt $choices"
    if ([string]::IsNullOrWhiteSpace($resp)) { $resp = $def }
    switch ($resp.ToUpperInvariant()) {
      'Y' { return $true }
      'N' { return $false }
      default { Write-Host 'Please answer Y or N.' }
    }
  }
}

function New-Timestamp { (Get-Date).ToString('yyyyMMdd_HHmmss') }

function Ensure-Dir {
  param([Parameter(Mandatory=$true)][string]$Path)
  if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
    Write-Verbose "Ensure-Dir: $Path"
    New-Item -ItemType Directory -Path $Path -Force | Out-Null
  }
}

function Get-FolderStats {
  [CmdletBinding()]
  param([Parameter(Mandatory=$true)][string]$Path)
  Write-Verbose "Get-FolderStats: $Path"
  $files = Get-ChildItem -LiteralPath $Path -Recurse -File -Force -ErrorAction Stop
  [pscustomobject]@{
    Path  = $Path
    Files = $files.Count
    Bytes = ($files | Measure-Object -Property Length -Sum).Sum
  }
}

function Get-ZipStats {
  [CmdletBinding()]
  param([Parameter(Mandatory=$true)][string]$ZipPath)
  if (-not (Test-Path -LiteralPath $ZipPath -PathType Leaf)) {
    return [pscustomobject]@{ Path=$ZipPath; Exists=$false; Entries=0; UncompressedBytes=0; CompressedBytes=0; SizeOnDisk=0 }
  }
  Add-Type -AssemblyName System.IO.Compression.FileSystem -ErrorAction Stop
  $fileInfo = Get-Item -LiteralPath $ZipPath -ErrorAction Stop
  $zip = [System.IO.Compression.ZipFile]::OpenRead($ZipPath)
  try {
    $entries = $zip.Entries
    $uc = 0L; $cc = 0L
    foreach ($e in $entries) {
      $uc += [int64]$e.Length
      if ($e.CompressedLength -is [long]) { $cc += [int64]$e.CompressedLength }
    }
    return [pscustomobject]@{
      Path              = $ZipPath
      Exists            = $true
      Entries           = $entries.Count
      UncompressedBytes = $uc
      CompressedBytes   = $cc
      SizeOnDisk        = $fileInfo.Length
    }
  } finally { $zip.Dispose() }
}

function Get-FreeSpaceForPath {
  param([Parameter(Mandatory=$true)][string]$TargetPath)
  $parent = Split-Path -Path $TargetPath -Parent
  if (-not $parent) { $parent = $env:TEMP }
  Ensure-Dir $parent
  $driveRoot = (Split-Path -Path (Resolve-Path -LiteralPath $parent) -Qualifier)
  $di = New-Object System.IO.DriveInfo ($driveRoot.TrimEnd('\'))
  return $di.AvailableFreeSpace
}

function Ensure-ZipAssemblies {
  Add-Type -AssemblyName System.IO.Compression -ErrorAction Stop
  Add-Type -AssemblyName System.IO.Compression.FileSystem -ErrorAction Stop
}

function Get-RelativePath {
  param([Parameter(Mandatory=$true)][string]$BaseDir,[Parameter(Mandatory=$true)][string]$FullName)
  $base = (Resolve-Path -LiteralPath $BaseDir).Path.TrimEnd('\\')
  $rel = $FullName.Substring($base.Length).TrimStart('\\')
  return ($rel -replace '\\','/')
}

function Clamp-ZipTimestamp {
  param([Parameter(Mandatory=$true)][datetime]$DateUtc)
  # ZIP spec range: 1980-01-01 .. 2107-12-31
  $min = [datetime]::Parse('1980-01-01T00:00:00Z')
  $max = [datetime]::Parse('2107-12-31T23:59:59Z')
  $utc = $DateUtc.ToUniversalTime()
  if ($utc -lt $min) { $utc = $min }
  if ($utc -gt $max) { $utc = $max }
  return [datetimeoffset]$utc
}

function Get-AbsolutePath {
  param([Parameter(Mandatory=$true)][string]$Path)
  if ([System.IO.Path]::IsPathRooted($Path)) { return [System.IO.Path]::GetFullPath($Path) }
  $base = (Get-Location).Path
  return [System.IO.Path]::GetFullPath((Join-Path $base $Path))
}

function Test-IsSubPath {
  param([Parameter(Mandatory=$true)][string]$Child,[Parameter(Mandatory=$true)][string]$Parent)
  $p = $Parent.TrimEnd('\\') + '\\'
  $c = $Child.TrimEnd('\\')
  return $c.StartsWith($p, [System.StringComparison]::OrdinalIgnoreCase)
}

function Add-EntryFromFile {
  param(
    [Parameter(Mandatory=$true)][System.IO.Compression.ZipArchive]$Zip,
    [Parameter(Mandatory=$true)][string]$EntryName,
    [Parameter(Mandatory=$true)][string]$FilePath
  )
  # Create the entry object first
  $entry = $Zip.CreateEntry($EntryName, [System.IO.Compression.CompressionLevel]::Optimal)

  # FIX: Set timestamp BEFORE opening the entry stream (required for Create mode)
  $fi = Get-Item -LiteralPath $FilePath -ErrorAction SilentlyContinue
  if ($fi) {
    $entry.LastWriteTime = Clamp-ZipTimestamp -DateUtc $fi.LastWriteTimeUtc
  } else {
    $entry.LastWriteTime = Clamp-ZipTimestamp -DateUtc ([datetime]::UtcNow)
  }

  # Now open streams and copy data
  $inStream  = $null
  $outStream = $null
  try {
    $inStream  = [System.IO.File]::Open($FilePath, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::Read)
    $outStream = $entry.Open()
    $inStream.CopyTo($outStream)
  } finally {
    if ($outStream) { $outStream.Dispose() }
    if ($inStream)  { $inStream.Dispose() }
  }
}

function New-ZipFromDirectory {
  param(
    [Parameter(Mandatory=$true)][string]$SourceDir,
    [Parameter(Mandatory=$true)][string]$ArchivePath,
    [string[]]$SkipPaths,
    [switch]$DryRun
  )
  if ($DryRun) {
    Write-Sub ("DryRun: would create zip from {0} -> {1}" -f $SourceDir, $ArchivePath)
    return
  }
  Ensure-ZipAssemblies
  $tmp = "$ArchivePath.tmp.$(New-Timestamp)"
  if (Test-Path -LiteralPath $tmp -PathType Leaf) { Remove-Item -LiteralPath $tmp -Force }

  # Build skip set (ArchivePath and its temp)
  $skipSet = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)
  if ($SkipPaths) { foreach ($sp in $SkipPaths) { if ($sp) { [void]$skipSet.Add($sp) } } }
  [void]$skipSet.Add($ArchivePath)
  [void]$skipSet.Add($tmp)

  $fs = $null
  $zip = $null
  try {
    $fs  = [System.IO.File]::Open($tmp, [System.IO.FileMode]::Create, [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None)
    $zip = New-Object System.IO.Compression.ZipArchive($fs, [System.IO.Compression.ZipArchiveMode]::Create, $false)
    $files = Get-ChildItem -LiteralPath $SourceDir -Recurse -File -Force
    foreach ($f in $files) {
      if ($skipSet.Contains($f.FullName)) { continue }
      $entryName = Get-RelativePath -BaseDir $SourceDir -FullName $f.FullName
      Add-EntryFromFile -Zip $zip -EntryName $entryName -FilePath $f.FullName
    }
  } finally {
    if ($zip) { $zip.Dispose() }
    if ($fs)  { $fs.Dispose() }
  }
  if (Test-Path -LiteralPath $ArchivePath -PathType Leaf) {
    Remove-Item -LiteralPath $ArchivePath -Force -ErrorAction Stop
  }
  Move-Item -LiteralPath $tmp -Destination $ArchivePath -Force
}

function Update-ZipFromDirectory {
  param(
    [Parameter(Mandatory=$true)][string]$SourceDir,
    [Parameter(Mandatory=$true)][string]$ArchivePath,
    [switch]$DryRun
  )
  if (-not (Test-Path -LiteralPath $ArchivePath -PathType Leaf)) {
    Write-Sub "Archive does not exist; creating new."
    New-ZipFromDirectory -SourceDir $SourceDir -ArchivePath $ArchivePath -DryRun:$DryRun
    return
  }
  if ($DryRun) {
    Write-Sub ("DryRun: would open zip for update: {0}" -f $ArchivePath)
    return
  }
  Ensure-ZipAssemblies
  $fs  = [System.IO.File]::Open($ArchivePath, [System.IO.FileMode]::Open, [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None)
  $zip = New-Object System.IO.Compression.ZipArchive($fs, [System.IO.Compression.ZipArchiveMode]::Update, $false)
  try {
    # Build a lookup of existing entries (case-insensitive)
    $map = @{}
    foreach ($e in $zip.Entries) { $map[$e.FullName.ToLowerInvariant()] = $e }
    $added = 0; $replaced = 0; $skipped = 0
    $files = Get-ChildItem -LiteralPath $SourceDir -Recurse -File -Force
    foreach ($f in $files) {
      if ($f.FullName -ieq $ArchivePath) { continue }
      $rel = Get-RelativePath -BaseDir $SourceDir -FullName $f.FullName
      $key = $rel.ToLowerInvariant()
      if ($map.ContainsKey($key)) {
        $existing = $map[$key]
        # Compare length and timestamp (ZIP timestamp granularity ~2 seconds)
        $needsReplace = $true
        try {
          $zipTime = $existing.LastWriteTime.UtcDateTime
          $fileTime = $f.LastWriteTimeUtc
          $lenDiff = ($existing.Length -ne $f.Length)
          $timeDiff = [math]::Abs((New-TimeSpan -Start $zipTime -End $fileTime).TotalSeconds) -gt 2
          $needsReplace = ($lenDiff -or $timeDiff)
        } catch { $needsReplace = $true }
        if ($needsReplace) {
          $existing.Delete()
          Add-EntryFromFile -Zip $zip -EntryName $rel -FilePath $f.FullName
          $replaced++
        } else {
          $skipped++
        }
      } else {
        Add-EntryFromFile -Zip $zip -EntryName $rel -FilePath $f.FullName
        $added++
      }
    }
    Write-Sub ("Update summary: added={0}, replaced={1}, skipped={2}" -f $added, $replaced, $skipped)
  } finally {
    if ($zip) { $zip.Dispose() }
    if ($fs)  { $fs.Dispose() }
  }
}

function Invoke-Expand {
  param(
    [Parameter(Mandatory=$true)][string]$ArchivePath,
    [Parameter(Mandatory=$true)][string]$RestoreDir
  )
  Ensure-ZipAssemblies
  [System.IO.Compression.ZipFile]::ExtractToDirectory($ArchivePath, $RestoreDir)
}

# ---------------------------- Defaults ----------------------------------------

$resolvedSource = (Resolve-Path -LiteralPath $SourceDir).Path
$sourceLeaf = Split-Path -Path $resolvedSource -Leaf

if (-not $ArchivePath) {
  $defaultOut = Join-Path $env:LOCALAPPDATA 'SingleArchive\Out'
  Ensure-Dir $defaultOut
  $ArchivePath = Join-Path $defaultOut ($sourceLeaf + '.zip')
} else {
  Ensure-Dir (Split-Path -Path $ArchivePath -Parent)
}

if (-not $RestoreDir) {
  $RestoreDir = Join-Path (Join-Path $env:LOCALAPPDATA 'SingleArchive\Restored') $sourceLeaf
} else {
  Ensure-Dir (Split-Path -Path $RestoreDir -Parent)
}

$resolvedArchive = Get-AbsolutePath -Path $ArchivePath

# ---------------------------- Preflight ---------------------------------------

Write-Step "Environment"
Write-Sub  ("UserMode: {0}" -f [Environment]::UserName)
Write-Sub  ("SourceDir:  {0}" -f $resolvedSource)
Write-Sub  ("ArchivePath: {0}" -f $resolvedArchive)
Write-Sub  ("RestoreDir:  {0}" -f $RestoreDir)
Write-Sub  ("Mode:        {0}" -f $Mode)
Write-Sub  ("VerifyOnly:  {0}" -f ($(if($VerifyOnly){'Yes'}else{'No'})))
Write-Sub  ("DryRun:      {0}" -f ($(if($DryRun){'Yes'}else{'No'})))

$srcStats = Get-FolderStats -Path $resolvedSource
("{0} files; {1:N0} bytes - Source" -f $srcStats.Files, $srcStats.Bytes) | Write-Host

$existingZip = Get-ZipStats -ZipPath $resolvedArchive
if ($existingZip.Exists) {
  ("{0} entries; {1:N0} bytes on disk - Existing Archive" -f $existingZip.Entries, $existingZip.SizeOnDisk) | Write-Host
}

if ($VerifyOnly) {
  Write-Step "Verify-only mode - no writes will occur"
  return
}

# Guard: prevent Create/Overwrite when archive path is under source (self-inclusion risk via temp file)
if (($Mode -eq 'Create' -or $Mode -eq 'Overwrite') -and (Test-IsSubPath -Child $resolvedArchive -Parent $resolvedSource)) {
  throw "Unsafe configuration: ArchivePath resides under SourceDir for mode '$Mode'. Place the archive outside the source tree."
}

# Free space heuristic
try {
  $free = Get-FreeSpaceForPath -TargetPath $resolvedArchive
  Write-Sub ("Free space on target volume: {0:N0} bytes" -f $free)
  $needed = if ($Mode -eq 'Update' -and $existingZip.Exists) {
    [int64]([Math]::Max($srcStats.Bytes * 0.2, $existingZip.SizeOnDisk * 0.1))
  } else {
    [int64]$srcStats.Bytes
  }
  if ($free -lt $needed) {
    throw ("Insufficient free space. Needed approx {0:N0} bytes, Available {1:N0} bytes" -f $needed, $free)
  }
} catch { throw "Free space check failed. $_" }

# ---------------------------- Mode-specific confirms --------------------------

switch ($Mode) {
  'Create' {
    if (Test-Path -LiteralPath $resolvedArchive -PathType Leaf) {
      $ts = New-Timestamp
      $altPath = Join-Path (Split-Path -Path $resolvedArchive -Parent) ("{0}_{1}.zip" -f [IO.Path]::GetFileNameWithoutExtension($resolvedArchive), $ts)
      if (-not (Confirm-Action -Prompt "Archive exists. Create a new timestamped archive instead?`n  $altPath")) {
        throw "User declined to proceed in Create mode with existing archive."
      }
      $resolvedArchive = $altPath
      $ArchivePath = $altPath
    }
  }
  'Overwrite' {
    if ((Test-Path -LiteralPath $resolvedArchive -PathType Leaf) -and -not (Confirm-Action -Prompt "Overwrite will DELETE existing archive. Proceed?")) {
      throw "User declined overwrite."
    }
  }
  'Update' {
    $null = $null
  }
}

# ---------------------------- Archive -----------------------------------------

Write-Step "Archiving"
Write-Sub  ("Operation: {0}" -f $Mode)
Write-Sub  ("Target:    {0}" -f $resolvedArchive)

try {
  switch ($Mode) {
    'Create'   {
      New-ZipFromDirectory -SourceDir $resolvedSource -ArchivePath $resolvedArchive -SkipPaths @($resolvedArchive) -DryRun:$DryRun
    }
    'Overwrite'{
      New-ZipFromDirectory -SourceDir $resolvedSource -ArchivePath $resolvedArchive -SkipPaths @($resolvedArchive) -DryRun:$DryRun
    }
    'Update'   {
      Update-ZipFromDirectory -SourceDir $resolvedSource -ArchivePath $resolvedArchive -DryRun:$DryRun
    }
  }
} catch { throw "Archive step failed. $_" }

# ---------------------------- Post-archive verification -----------------------

Write-Step "Verifying archive"
try {
  if (-not $DryRun) {
    $zipStats = Get-ZipStats -ZipPath $resolvedArchive
    if (-not $zipStats.Exists) { throw "Archive not found after operation." }
    ("{0} entries; {1:N0} bytes on disk - Archive" -f $zipStats.Entries, $zipStats.SizeOnDisk) | Write-Host
  } else {
    Write-Sub "DryRun: verification skipped (no archive written)"
  }
} catch { throw "Verification failed. $_" }

# ---------------------------- Optional restore --------------------------------

if ($DoRestore -and -not $DryRun) {
  Write-Step "Restore (extract)"
  $existsAndHasContent = (Test-Path -LiteralPath $RestoreDir -PathType Container) -and ((Get-ChildItem -LiteralPath $RestoreDir -Force | Measure-Object).Count -gt 0)
  if ($existsAndHasContent) {
    if (-not (Confirm-Action -Prompt "RestoreDir has existing content. Move aside as a timestamped backup?" -DefaultNo)) {
      throw "User declined to touch existing RestoreDir."
    }
    $backup = "$RestoreDir.__backup__$(New-Timestamp)"
    Write-Sub ("Renaming existing RestoreDir to '{0}'" -f $backup)
    Rename-Item -LiteralPath $RestoreDir -NewName (Split-Path -Path $backup -Leaf) -ErrorAction Stop
  }
  Ensure-Dir $RestoreDir
  try {
    Invoke-Expand -ArchivePath $resolvedArchive -RestoreDir $RestoreDir
    $restStats = Get-FolderStats -Path $RestoreDir
    ("{0} files; {1:N0} bytes - Restored" -f $restStats.Files, $restStats.Bytes) | Write-Host
  } catch { throw "Restore failed. $_" }
} elseif ($DoRestore -and $DryRun) {
  Write-Step "DryRun: would extract archive to '$RestoreDir'"
}

# ---------------------------- Done --------------------------------------------

Write-Step "Done"
Write-Sub  ("Archive at: {0}" -f $resolvedArchive)
if ($DoRestore -and -not $DryRun) { Write-Sub ("Restored to: {0}" -f $RestoreDir) }
Write-Sub  "Re-run with -Mode Update for incremental refresh; use Overwrite to fully regenerate."
{% endcodeblock %}
