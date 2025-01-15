---
tags: scripts>powershell, windows
info: aberto.
date: 2024-12-31
type: post
layout: post
published: true
slug: windows-11-maintenancerepair-via-powershell
title: 'Windows 11 maintenance/repair via PowerShell'
---
### **Step 1: Create the PowerShell Script**

1. **Open a Text Editor:**

   - Use **Notepad** or any text editor of your choice.

2. **Save the File with a `.ps1` Extension:**

   - For example, save it as `Maintenance.ps1`.

---

### **Step 2: Write the PowerShell Script**

Below is the adapted script with explanations:

```powershell
# Maintenance.ps1

# Check for Administrator privileges
if (-not [Bool] (New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Warning "This script must be run as an Administrator."
    exit
}

Write-Host "Running System File Checker (SFC)..."
sfc /scannow

Write-Host "Running DISM ScanHealth..."
dism /Online /Cleanup-Image /ScanHealth

Write-Host "Running DISM RestoreHealth..."
dism /Online /Cleanup-Image /RestoreHealth

Write-Host "Running DISM StartComponentCleanup..."
dism /Online /Cleanup-Image /StartComponentCleanup

Write-Host "Running CHKDSK on C drive..."
$chkdskCommand = "chkdsk C: /r /f"
Write-Host "Scheduling CHKDSK on reboot..."
cmd.exe /c "echo Y | $chkdskCommand"

Write-Host "Maintenance completed."
Read-Host -Prompt "Press Enter to exit"
```

**Explanation:**

- **Administrator Check:**

  - The script checks if it's run as an administrator.
  - If not, it displays a warning and exits.

- **Running Commands:**

  - **SFC:** Scans and repairs protected system files.
  - **DISM ScanHealth:** Checks for component store corruption.
  - **DISM RestoreHealth:** Repairs the component store.
  - **DISM StartComponentCleanup:** Cleans up superseded components.

- **CHKDSK:**

  - Runs `chkdsk` on the C: drive.
  - `echo Y | chkdsk C: /r /f` automatically confirms scheduling if the drive is in use.
  - Does not use the `/x` parameter to avoid forcing a dismount, reducing the risk of data loss.

---

### **Step 3: Run the Script with Administrative Privileges**

**Option 1: Run PowerShell as Administrator**

1. **Open PowerShell as Administrator:**

   - Click on **Start**, type **PowerShell**.
   - Right-click **Windows PowerShell**, select **Run as administrator**.

2. **Navigate to the Script Location:**

   ```powershell
   cd "C:\Path\To\Your\Script"
   ```

3. **Run the Script:**

   ```powershell
   .\Maintenance.ps1
   ```

**Option 2: Run the Script Directly**

- Right-click on `Maintenance.ps1` and select **Run with PowerShell**.
- Ensure you confirm any prompts for administrative access.

---

### **Step 4: Adjust Execution Policy if Necessary**

If you encounter an error about the execution policy, set the policy for the current session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

- This command allows script execution for the current session without changing the system-wide policy.
- **Important:** Avoid using `-ExecutionPolicy Bypass`, as it can pose security risks.

---

### **Important Considerations**

- **Administrative Rights:**

  - The script requires administrative privileges to run system maintenance commands.
  - Always run PowerShell as an administrator when executing this script.

- **Understanding the Commands:**

  - **SFC (`sfc /scannow`):** Scans all protected system files and replaces corrupted files with a cached copy.
  - **DISM (`dism /Online /Cleanup-Image`):**

    - **/ScanHealth:** Checks for component store corruption.
    - **/RestoreHealth:** Repairs the component store.
    - **/StartComponentCleanup:** Cleans up superseded components and reduces the size of the component store.

  - **CHKDSK (`chkdsk C: /r /f`):**

    - **/r:** Locates bad sectors and recovers readable information.
    - **/f:** Fixes errors on the disk.
    - **Note:** If the drive is in use, `chkdsk` will prompt to schedule the check on the next reboot.

- **Handling CHKDSK Scheduling:**

  - The script automatically schedules `chkdsk` to run at the next reboot if required.
  - **Do not use** the `/x` parameter, as it forces a dismount and can cause data loss if programs are accessing the drive.

- **System Impact:**

  - Running these commands can be time-consuming.
  - `CHKDSK` may require a reboot and can take a significant amount of time to complete.
  - Ensure you save all work and close applications before running the script.

- **Execution Policy:**

  - The execution policy helps prevent unauthorized scripts from running.
  - Adjusting the policy for the current session is safer than changing it permanently.
  - **Do not** bypass the execution policy unless absolutely necessary.

---

### **Additional Tips**

- **Logging Output:**

  - To log the output of each command, you can redirect the output to files:

    ```powershell
    sfc /scannow | Out-File -FilePath "$env:UserProfile\Desktop\sfc_log.txt" -Encoding utf8 -Append
    ```

  - Repeat similar redirection for other commands as needed.
