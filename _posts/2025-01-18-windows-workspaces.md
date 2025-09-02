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


# non-admin setup

# **Windows 10 Workspace Hotkeys for Non-Admins**

This guide details how to create Win \+ Numpad \[Number\] hotkeys to switch directly to specific virtual desktops on Windows 10 without requiring administrator privileges. This is achieved by using the VirtualDesktop.exe tool, batch files, and an AutoHotkey script.

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
2. Copy and paste the entire PowerShell script below into the editor. This script has been updated to use the correct folder paths.  
   \# Define paths relative to the user's profile.  
   $basePath \= "$env:USERPROFILE\\Documents\\WindowsHotkeys"  
   $virtualDesktopPath \= Join-Path \-Path $basePath \-ChildPath "Tools\\VirtualDesktop\\VirtualDesktop.exe"  
   $outputFolder \= Join-Path \-Path $basePath \-ChildPath "QuickAccess"

   \# Check if the VirtualDesktop executable exists.  
   if (-not (Test-Path \-Path $virtualDesktopPath)) {  
       Write-Error "VirtualDesktop.exe not found at '$virtualDesktopPath'. Please check the path."  
       return  
   }

   \# Generate batch files 1.bat through 9.bat.  
   for ($i \= 1; $i \-le 9; $i++) {  
       \# Desktop numbers are 0-indexed, so we subtract 1\.  
       $desktopNumber \= $i \- 1  
       $batchFilePath \= Join-Path \-Path $outputFolder \-ChildPath "$i.bat"

       \# Content of the batch file.  
       $batchContent \= "@echo off\`n\`"$virtualDesktopPath\`" /Switch:$desktopNumber"

       try {  
           Set-Content \-Path $batchFilePath \-Value $batchContent \-Encoding Ascii  
           Write-Host "Successfully created $batchFilePath"  
       }  
       catch {  
           Write-Error "Failed to create $batchFilePath. Error: $\_"  
       }  
   }

   Write-Host "Batch file generation complete."

3. Save the file as GenerateBatchFiles.ps1 inside the Documents\\WindowsHotkeys\\Scripts folder.  
4. Open PowerShell by pressing Win \+ X and selecting **Windows PowerShell**.  
5. Run the following command. This command navigates to your script folder and runs the script, bypassing the default security policy that normally blocks local scripts.  
   Set-Location "$env:USERPROFILE\\Documents\\WindowsHotkeys\\Scripts"; powershell \-ExecutionPolicy Bypass \-File .\\GenerateBatchFiles.ps1

6. Press Enter. Verify that the script output says it successfully created 1.bat through 9.bat.

### **Part 2: Create Hotkeys with AutoHotkey**

#### **Step 2.1: Install AutoHotkey**

1. Go to the official AutoHotkey website: [https://www.autohotkey.com](https://www.autohotkey.com)  
2. Download and run the installer, choosing the **Express Installation** option.

#### **Step 2.2: Create the AutoHotkey Hotkey Script**

1. Go to your Desktop, right-click an empty space, and select **New** \> **AutoHotkey Script**.  
2. Name the file WorkspaceHotkeys.ahk.  
3. Right-click the new file and select **Edit Script**.  
4. Delete all default text and paste the following code, which points to the batch files in your Documents folder. This script uses modern AutoHotkey v2 syntax.
```
   ; \=== HOTKEYS TO TRIGGER WORKSPACE BATCH FILES (AutoHotkey v2 Syntax) \===  
   \#Numpad1::Run(A\_MyDocuments . "\\WindowsHotkeys\\QuickAccess\\1.bat")  
   \#Numpad2::Run(A\_MyDocuments . "\\WindowsHotkeys\\QuickAccess\\2.bat")  
   \#Numpad3::Run(A\_MyDocuments . "\\WindowsHotkeys\\QuickAccess\\3.bat")  
   \#Numpad4::Run(A\_MyDocuments . "\\WindowsHotkeys\\QuickAccess\\4.bat")  
   \#Numpad5::Run(A\_MyDocuments . "\\WindowsHotkeys\\QuickAccess\\5.bat")  
   \#Numpad6::Run(A\_MyDocuments . "\\WindowsHotkeys\\QuickAccess\\6.bat")  
   \#Numpad7::Run(A\_MyDocuments . "\\WindowsHotkeys\\QuickAccess\\7.bat")  
   \#Numpad8::Run(A\_MyDocuments . "\\WindowsHotkeys\\QuickAccess\\8.bat")  
   \#Numpad9::Run(A\_MyDocuments . "\\WindowsHotkeys\\QuickAccess\\9.bat")  
```
