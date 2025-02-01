---

tags: [software>windows, scripts>powershell]
info: aberto.
date: 2025-01-18
type: post
layout: post
published: true
slug: windows-11-switch-workspaces-via-virtualdesktop-module-with-custom-shortcuts
title: 'Windows 11: Switch Workspaces via VirtualDesktop Module with custom shortcuts'
---
# Creating Batch Files to Switch to Specific Virtual Desktops Using PowerShell and the VirtualDesktop Tool

## **Overview**

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
