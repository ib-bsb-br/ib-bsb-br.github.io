---
tags: [software>windows, scripts>powershell]
info: aberto.
date: 2025-01-18
type: post
layout: post
published: true
slug: windows-workspaces
title: 'Windows 11: Switch Workspaces via VirtualDesktop Module with custom shortcuts'
---
## Creating Batch Files to Switch to Specific Virtual Desktops Using PowerShell and the VirtualDesktop Tool

This guide will help you create a PowerShell script that generates batch files (`1.bat` to `8.bat`) to switch directly to any of your eight virtual desktops (workspaces) on Windows 11. We will use the **VirtualDesktop** command-line tool by Markus Scholtes to manage virtual desktops via command-line commands.

---

## **Prerequisites**

1. **Download the VirtualDesktop Tool:**

   - Access the **VirtualDesktop** repository on GitHub:

     [https://github.com/MScholtes/VirtualDesktop](https://github.com/MScholtes/VirtualDesktop)

   - **Download Precompiled Binaries:**

     - Navigate to the **Releases** section:

       [https://github.com/MScholtes/VirtualDesktop/releases](https://github.com/MScholtes/VirtualDesktop/releases)

     - Download the latest release ZIP file (e.g., `VirtualDesktop_v1.19.zip`).

   - **Extract the Executable:**

     - Extract the contents of the ZIP file to a folder accessible to your user account, e.g., `C:\Tools\VirtualDesktop`.

     - Ensure you use the correct executable for your Windows version:

       - For **Windows 11**, use `VirtualDesktop11.exe`.

       - For **Windows 10**, use `VirtualDesktop.exe`.

---

## **Step 1: Ensure Eight Virtual Desktops Exist**

We need to make sure that you have exactly eight virtual desktops. We will use PowerShell to create additional desktops if necessary.

1. **Open PowerShell:**

   - Press **Win + X** and select **Windows PowerShell** or **Windows Terminal**.

2. **Navigate to the VirtualDesktop Directory:**

   ```powershell
   Set-Location "C:\Tools\VirtualDesktop"
   ```

3. **Check the Current Number of Virtual Desktops:**

   ```powershell
   $virtualDesktopExe = "C:\Tools\VirtualDesktop\VirtualDesktop11.exe"

   if (-Not (Test-Path -Path $virtualDesktopExe)) {
       Write-Error "VirtualDesktop executable not found at $virtualDesktopExe"
       exit 1
   }

   $countOutput = & $virtualDesktopExe /Count
   $currentDesktopCount = ($countOutput -match 'Desktops: (\d+)') ? [int]$Matches[1] : 0

   Write-Host "Current number of desktops: $currentDesktopCount"
   ```

4. **Create Additional Desktops if Necessary:**

   ```powershell
   for ($i = $currentDesktopCount + 1; $i -le 8; $i++) {
       & $virtualDesktopExe /New | Out-Null
       Write-Host "Created virtual desktop $i"
   }
   ```

5. **Optionally, Name Your Desktops:**

   ```powershell
   for ($i = 1; $i -le 8; $i++) {
       & $virtualDesktopExe /GetDesktop:$i /Name:"Workspace $i" | Out-Null
       Write-Host "Named desktop $i as 'Workspace $i'"
   }
   ```

---

## **Step 2: Create a PowerShell Script to Generate Batch Files**

We will create a PowerShell script that automatically generates the batch files needed to switch to each of the eight virtual desktops.

1. **Create the Output Directory for Batch Files:**

   - We'll use `C:\QuickAccess` as the folder to store the batch files.

   ```powershell
   $outputFolder = "C:\QuickAccess"
   if (-Not (Test-Path -Path $outputFolder)) {
       New-Item -ItemType Directory -Path $outputFolder -Force | Out-Null
       Write-Host "Created output directory: $outputFolder"
   }
   ```

2. **Create the PowerShell Script:**

   - Open Notepad or your preferred text editor.

3. **Script Content:**

   Paste the following PowerShell script:
{% codeblock powershell %}
# Path to the VirtualDesktop executable
$virtualDesktopPath = "G:\05-portable\VirtualDesktop11-24H2.exe"

# Output folder for the batch files
$outputFolder = "C:\QuickAccess"

# Ensure the VirtualDesktop executable exists
if (-Not (Test-Path -Path $virtualDesktopPath)) {
    Write-Error "VirtualDesktop executable not found at $virtualDesktopPath"
    exit 1
}

# Ensure the output folder exists
if (-Not (Test-Path -Path $outputFolder)) {
    New-Item -ItemType Directory -Path $outputFolder -Force | Out-Null
    Write-Host "Created output directory: $outputFolder"
}

# Generate batch files for desktops 1 to 8
for ($desktopNumber = 1; $desktopNumber -le 8; $desktopNumber++) {

    # Batch file content
    $batFileContent = "@echo off`n"
    $batFileContent += "`"$virtualDesktopPath`" /Switch:$desktopNumber"

    # Batch file path
    $batFilePath = Join-Path $outputFolder "$desktopNumber.bat"

    # Create the batch file
    try {
        Set-Content -Path $batFilePath -Value $batFileContent -Encoding ASCII
        Write-Host "Created batch file: $batFilePath"
    }
    catch {
        Write-Error "Error creating batch file ${batFilePath}: $_"
        # Or using the -f operator:
        # Write-Error ("Error creating batch file {0}: {1}" -f $batFilePath, $_)
    }
}

Write-Host "All batch files have been generated in $outputFolder."
{% endcodeblock %}

   **Notes:**

   - Replace `$virtualDesktopPath` with the actual path to your VirtualDesktop executable if it's different.

   - Ensure that the path to the output folder `$outputFolder` matches your desired location.

   - The script includes error handling to alert you if the VirtualDesktop executable is not found or if there are issues creating the batch files.

4. **Save the Script:**

   - Save the script as `GenerateBatchFiles.ps1` in a folder of your choice, e.g., `C:\Scripts`.

---

## **Step 3: Run the PowerShell Script**

1. **Run the Script:**

   - Open PowerShell and navigate to the script's directory:

     ```powershell
     Set-Location "C:\Scripts"
     ```

   - Execute the script:

     ```powershell
     .\GenerateBatchFiles.ps1
     ```

   - You should see output indicating that each batch file has been created.

2. **Verify the Batch Files:**

   - Navigate to `C:\QuickAccess` and confirm that `1.bat` to `8.bat` have been created.

   - Open one of the batch files (e.g., `1.bat`) to verify its content:

     ```batch
     @echo off
     "C:\Tools\VirtualDesktop\VirtualDesktop11.exe" /Switch:1
     ```

---

## **Step 4: Add `C:\QuickAccess` to Your PATH Environment Variable**

Adding the `C:\QuickAccess` folder to your PATH allows Windows to recognize the batch files when using the Run dialog or Command Prompt.

1. **Modify User PATH Variable:**

   - Press **Win + X** and select **System** (or **Settings** > **System** > **About** > **Advanced system settings**).

   - Click on **Advanced system settings**.

   - In the **System Properties** window, click **Environment Variables**.

   - Under **User variables**, select **Path** and click **Edit**.

   - Click **New** and add:

     ```plaintext
     C:\QuickAccess
     ```

   - Click **OK** to save changes.

2. **Restart Any Open Command Prompts or Applications:**

   - For the changes to take effect, restart any applications that might use the PATH variable.

---

## **Step 5: Use the Batch Files to Switch Workspaces**

You can now switch to any workspace by running the corresponding batch file.

- **From the Run Dialog:**

  - Press **Win + R** to open the Run dialog.

  - Type the number of the workspace you want to switch to (e.g., `1` for workspace 1) and press **Enter**.

- **From Command Prompt or PowerShell:**

  - Simply type the number (which corresponds to the batch file's name) and press **Enter**: `C:\Users\YourUsername> 3`

# CODE

.\00-QuickAccess\0.bat
```
start "" "C:\Program Files\PowerShell\7\pwsh.exe"
```
.\00-QuickAccess\1.bat
```
@echo off
"G:\05-portable\VirtualDesktop11-24H2.exe" /Switch:0
```
.\00-QuickAccess\2.bat
```
@echo off
"G:\05-portable\VirtualDesktop11-24H2.exe" /Switch:1

```
.\00-QuickAccess\3.bat
```
@echo off
"G:\05-portable\VirtualDesktop11-24H2.exe" /Switch:2

```
.\00-QuickAccess\4.bat
```
@echo off
"G:\05-portable\VirtualDesktop11-24H2.exe" /Switch:3

```
.\00-QuickAccess\5.bat
```
@echo off
"G:\05-portable\VirtualDesktop11-24H2.exe" /Switch:4

```
.\00-QuickAccess\6.bat
```
@echo off
"G:\05-portable\VirtualDesktop11-24H2.exe" /Switch:5

```
.\00-QuickAccess\7.bat
```
@echo off
"G:\05-portable\VirtualDesktop11-24H2.exe" /Switch:6

```
.\00-QuickAccess\8.bat
```
@echo off
"G:\05-portable\VirtualDesktop11-24H2.exe" /Switch:7

```
.\00-QuickAccess\9.bat
```
@echo off
"G:\05-portable\VirtualDesktop11-24H2.exe" /Switch:8

```
.\00-QuickAccess\b.bat
```
@echo off
pushd "G:\05-portable\ungoogled"
start "" "C:\Program Files\PowerShell\7\pwsh.exe" -NoProfile -ExecutionPolicy Bypass -File "un-script.ps1"
exit
```
.\00-QuickAccess\t.bat
```
start "" "G:\05-portable\ExplorerPlusPlus\Explorer++.exe"
```


## non-admin setup

### **Part 0: Prerequisites**

Before starting, complete these two essential setup steps.

#### **Step 0.1: Create Nine Virtual Desktops**

The script will create hotkeys for nine desktops. You must ensure these desktops exist first.

1. Press Win \+ Tab to open the Task View.  
2. At the top of the screen, click the **"New desktop"** button eight times until you have a total of nine desktops available (Desktop 1 through Desktop 9).

#### **Step 0.2: Create a Main Project Folder**

To avoid any permission issues, we will store all files in your personal Documents folder.

1. Open File Explorer and navigate to your **Documents** folder.  
2. Create a new folder and name it WindowsHotkeys. All subsequent files and folders will be created inside this one.

### **Part 1: Prepare the Workspace Switching Tools**

This section covers the download and setup of the necessary files and scripts inside your project folder.

#### **Step 1.1: Download and Place the VirtualDesktop Tool**

1. Navigate to the VirtualDesktop releases page on GitHub: [https://github.com/MScholtes/VirtualDesktop/releases](https://github.com/MScholtes/VirtualDesktop/releases)  
2. Download the latest .zip file (e.g., VirtualDesktop\_v1.19.zip).  
3. Inside your Documents\\WindowsHotkeys folder, create a new folder named Tools.  
4. Inside Tools, create another folder named VirtualDesktop.  
5. Extract the contents of the downloaded ZIP file. From the extracted files, copy VirtualDesktop.exe into the Documents\\WindowsHotkeys\\Tools\\VirtualDesktop folder.

#### **Step 1.2: Create Directories for Scripts and Batch Files**

1. Inside Documents\\WindowsHotkeys, create a folder named Scripts.  
2. Inside Documents\\WindowsHotkeys, create a folder named QuickAccess.

#### **Step 1.3: Create and Run the PowerShell Batch File Generator**

1. Open Notepad or another plain text editor.  
2. Copy and paste the entire PowerShell script below into the editor.

```ps1
#requires -Version 5.1
[CmdletBinding()]
param(
    [string]$BasePath = "$env:USERPROFILE\Documents\WindowsHotkeys",
    [string]$ExePath = "C:\Tools\VirtualDesktop\VirtualDesktop11.exe",
    [string]$OutputSubfolder = "QuickAccess",
    [int]$Count = 9
)

# Resolve executable path (prefer explicit ExePath, then fallback under BasePath)
$virtualDesktopPath = $ExePath
if (-not (Test-Path -LiteralPath $virtualDesktopPath -PathType Leaf)) {
    $virtualDesktopPath = Join-Path -Path $BasePath -ChildPath "Tools\VirtualDesktop\VirtualDesktop.exe"
}

# Ensure output directory exists
$outputFolder = Join-Path -Path $BasePath -ChildPath $OutputSubfolder
New-Item -ItemType Directory -Path $outputFolder -Force | Out-Null

# Validate executable exists
if (-not (Test-Path -LiteralPath $virtualDesktopPath -PathType Leaf)) {
    Write-Error "VirtualDesktop executable not found at '$ExePath' or '$BasePath\Tools\VirtualDesktop\VirtualDesktop.exe'."
    exit 1
}

# Generate batch files 1..$Count
for ($i = 1; $i -le $Count; $i++) {
    # Desktop numbers are 0-indexed
    $desktopNumber = $i - 1
    $batchFilePath = Join-Path -Path $outputFolder -ChildPath "$i.bat"

    # Use a double-quoted here-string to avoid escaping issues
    $batchContent = @"
@echo off
"$virtualDesktopPath" /Switch:$desktopNumber
"@

    $attempt = 0
    while ($true) {
        try {
            # CRLF is written by default on Windows; ASCII suits .bat files
            Set-Content -LiteralPath $batchFilePath -Value $batchContent -Encoding ASCII -Force
            Write-Host "Successfully created $batchFilePath"
            break
        }
        catch {
            $attempt++
            if ($attempt -ge 3) {
                Write-Error "Failed to create $batchFilePath. Error: $($_.Exception.Message)"
                break
            }
            Start-Sleep -Milliseconds 250
        }
    }
}

Write-Host "Batch file generation complete."
```

4. Save the file as GenerateBatchFiles.ps1 inside the Documents\\WindowsHotkeys\\Scripts folder.  
5. Open PowerShell by pressing Win \+ X and selecting **Windows PowerShell**.  
6. Run the following command. This command navigates to your script folder and runs the script, bypassing the default security policy that normally blocks local scripts.  
   Set-Location "$env:USERPROFILE\\Documents\\WindowsHotkeys\\Scripts"; powershell \-ExecutionPolicy Bypass \-File .\\GenerateBatchFiles.ps1

7. Press Enter. Verify that the script output says it successfully created 1.bat through 9.bat.

### **Part 2: Create Hotkeys with AutoHotkey**

#### **Step 2.1: Install AutoHotkey**

1. Go to the official AutoHotkey website: [https://www.autohotkey.com](https://www.autohotkey.com)  
2. Download and run the installer, choosing the **Express Installation** option for AutoHotkey v2.

#### **Step 2.2: Create the Combined AutoHotkey Hotkey Script**

This single script will enable both switching between workspaces and moving windows to them.

1. Go to your Desktop, right-click an empty space, and select **New** \> **AutoHotkey Script**.  
2. Name the file WorkspaceHotkeys.ahk.  
3. Right-click the new file and select **Edit Script**.  
4. Delete all default text and paste the complete code below.  

```
#Requires AutoHotkey v2.0
#SingleInstance Force
#Warn

; === Windows 10/11 Workspace Hotkeys (Non-Admin) ===
; Uses VirtualDesktop.exe to switch/move windows across virtual desktops.
; Fixes for reliable window moves:
;  - Capture active window handle before launching the CLI
;  - Use /MoveWindowHandle:<hwnd> (not /MoveActiveWindow)
;  - Run the CLI hidden and in quiet mode (/q) with RunWait to serialize calls
;  - Ensure target desktop exists (auto-create as needed)

; --- Configuration ---
VD_DIR := A_MyDocuments . "\WindowsHotkeys\Tools\VirtualDesktop"

; Try common executable names. First found will be used.
candidates := [
    VD_DIR . "\VirtualDesktop.exe",
    VD_DIR . "\VirtualDesktop11.exe",
    VD_DIR . "\VirtualDesktop11-24H2.exe",
    VD_DIR . "\VirtualDesktopServer2022.exe",
    VD_DIR . "\VirtualDesktopServer2016.exe"
]

global VD_EXE := ""
for _, path in candidates {
    if FileExist(path) {
        VD_EXE := path
        break
    }
}

if (VD_EXE = "") {
    msg := "VirtualDesktop executable not found in:`n" VD_DIR "`n`nExpected one of:`n"
    for _, p in candidates
        msg .= p "`n"
    MsgBox msg, "WorkspaceHotkeys.ahk - Error", 48
    ExitApp
}

; --- Internal Helpers ---
VD_Run(args) {
    ; Run the VirtualDesktop tool hidden; return exit code (last command's result)
    global VD_EXE, VD_DIR
    try {
        return RunWait('"' . VD_EXE . '" ' . args, VD_DIR, "Hide")
    } catch {
        return -1
    }
}

EnsureDesktopExists(desktopIndex) {
    ; Make sure a 0-based desktop index exists; create desktops if needed
    count := VD_Run("/q /Count")
    if (count < 0)
        return false
    while (count <= desktopIndex) {
        res := VD_Run("/q /New")
        if (res < 0)
            return false
        count++
    }
    return true
}

IsMovableWindow(hwnd) {
    if !hwnd
        return false
    cls := WinGetClass("ahk_id " hwnd)
    ; Avoid trying to move shell/taskbar/desktop windows
    if (cls = "Progman" || cls = "WorkerW" || cls = "Shell_TrayWnd" || cls = "TaskListThumbnailWnd")
        return false
    return true
}

; --- Public Functions ---
SwitchToDesktop(desktopIndex) {
    if !EnsureDesktopExists(desktopIndex)
        return
    VD_Run("/q /Switch:" . desktopIndex)
}

MoveWindowAndSwitch(desktopIndex) {
    ; Capture the active window handle before launching the CLI
    hwnd := WinExist("A")
    if !IsMovableWindow(hwnd)
        return
    if !EnsureDesktopExists(desktopIndex)
        return
    ; Chain: target desktop -> move specific window by handle -> switch
    VD_Run("/q /GetDesktop:" . desktopIndex . " /MoveWindowHandle:" . hwnd . " /Switch")
}

; --- Hotkeys ---
; Note: VirtualDesktop indices are 0-based (Desktop 1 = 0)
; Switching: Win + Numpad [1-9]
#Numpad1::SwitchToDesktop(0)
#Numpad2::SwitchToDesktop(1)
#Numpad3::SwitchToDesktop(2)
#Numpad4::SwitchToDesktop(3)
#Numpad5::SwitchToDesktop(4)
#Numpad6::SwitchToDesktop(5)
#Numpad7::SwitchToDesktop(6)
#Numpad8::SwitchToDesktop(7)
#Numpad9::SwitchToDesktop(8)

; Move & Switch: Ctrl + Numpad [1-9]
^Numpad1::MoveWindowAndSwitch(0)
^Numpad2::MoveWindowAndSwitch(1)
^Numpad3::MoveWindowAndSwitch(2)
^Numpad4::MoveWindowAndSwitch(3)
^Numpad5::MoveWindowAndSwitch(4)
^Numpad6::MoveWindowAndSwitch(5)
^Numpad7::MoveWindowAndSwitch(6)
^Numpad8::MoveWindowAndSwitch(7)
^Numpad9::MoveWindowAndSwitch(8)

; Sequential navigation: Win + NumpadSub / Win + NumpadAdd
#NumpadSub::VD_Run("/q /Left")
#NumpadAdd::VD_Run("/q /Right")

; Management: Win + Ctrl + NumpadAdd / NumpadSub
#^NumpadAdd::VD_Run("/q /New")
#^NumpadSub::VD_Run("/q /Remove:LAST")
```

Save and close the file.

Part 3: Activate the Hotkeys
Step 3.1: Run the AutoHotkey Script
Go to your Desktop and double-click the WorkspaceHotkeys.ahk file.

A green "H" icon will appear in your system tray (bottom-right of the screen). This indicates the hotkeys are active.

You can now use Win + Numpad [Number] to switch desktops, and Win + Alt + Numpad [Number] to move the active window to a new desktop. A small command window may flash on screen; this is normal.

Step 3.2: Make Hotkeys Run Automatically on Startup
Press Win + R to open the Run dialog.

Type shell:startup and press Enter.

Copy the WorkspaceHotkeys.ahk file from your Desktop and paste it into this Startup folder.

The setup is now complete. The hotkeys will activate automatically every time you log into Windows.
