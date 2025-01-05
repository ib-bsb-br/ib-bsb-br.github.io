---
tags: windows
info: aberto.
date: 2025-01-05
type: post
layout: post
published: true
slug: windows-run-env-vars-custom-shortcuts
title: 'Windows Run + env vars = custom shortcuts'
---
### **How It Works**

1. **Creating a Quick-Access Folder:**
   - Begin by creating a new folder (e.g., `C:\QuickAccess`) where you'll store your custom shortcuts.

2. **Adding the Folder to the Environment Variables:**
   - **Environment Variables**, like `PATH`, tell the operating system where to look for executable files.
   - By adding your quick-access folder to the `PATH` variable, you instruct Windows to include it when searching for commands entered in the Run dialog.
   - **Note:** Windows searches for executable files (`.exe`, `.bat`, `.com`, `.cmd`), not shortcut files (`.lnk`), in the `PATH`.
   - **Steps to Add to PATH (User Variables):**
     - Press **Win + X** and select **System** (or right-click **This PC** and select **Properties**).
     - Click on **Advanced system settings**.
     - In the **System Properties** window, click **Environment Variables**.
     - Under **User variables for [Your Username]**, select **Path** and click **Edit**.
     - Click **New** and add the path to your quick-access folder (e.g., `C:\QuickAccess`).
     - Click **OK** to save changes.
     - *Using user variables avoids needing administrative rights and only affects your account.*

3. **Creating Executable Shortcuts:**
   - Since the Run dialog executes files it finds in the `PATH`, you'll need to create executable files, such as batch files (`.bat`), instead of shortcuts (`.lnk`).
   - **Creating Batch Files to Open Drives or Folders:**
     - Open **Notepad**.
     - To create a shortcut for the D drive:
       - Type: `explorer D:\`
       - Save the file as `d.bat` in your quick-access folder.
   - **Creating Batch Files to Launch Applications:**
     - For applications, type: `start "" "C:\Path\To\Application.exe"`
     - Save the file with a simple name, like `chrome.bat`, in your quick-access folder.

4. **Using the Run Dialog:**
   - Press **Win + R** to open the Run dialog.
   - Type the name of your batch file without the `.bat` extension (e.g., `d`) and press **Enter**.
   - Windows will execute the batch file, opening the target drive, folder, or application.

---

### **Why It Works**

- **Run Dialog Mechanism:**
  - When you enter a command in the Run dialog, Windows searches the directories listed in the `PATH` environment variable and specific system directories for executable files.
  - By adding your quick-access folder to the `PATH`, Windows can find and execute your custom batch files when their names are entered in the Run dialog.

- **Executable Recognition:**
  - Windows recognizes batch files (`.bat`) as executable scripts.
  - Executing a batch file runs the commands it contains, opening applications or folders as specified.

---

### **In What Ways It Can Be Utilized**

**1. Quick Access to Drives and Folders:**

- **Access Drives Directly:**
  - Create batch files (e.g., `c.bat`, `d.bat`) that open specific drives.
  - Example content for `d.bat`: `explorer D:\`

- **Open Frequently Used Folders:**
  - Create batch files to open folders like Documents, Downloads, or project directories.
  - Example content for `docs.bat`: `explorer "C:\Users\[Your Username]\Documents"`

**2. Launch Applications Quickly:**

- **Custom Application Launchers:**
  - Create batch files to start applications that don't have simple Run commands.
  - Example content for `word.bat`: `start "" "C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"`

**3. Run Scripts or Automated Tasks:**

- **Execute Scripts:**
  - Use batch files to run scripts or a series of commands.
  - Example content for `backup.bat`:
    ```batch
    @echo off
    xcopy "C:\ImportantFiles" "E:\Backup\ImportantFiles" /E /H /C /I
    echo Backup completed.
    ```

**4. Personalized Commands:**

- **Tailored Shortcuts:**
  - Name batch files with easy-to-remember commands that suit your workflow.
  - For instance, `meet.bat` to open a video conferencing app.

---

### **Alternative Methods**

**Method 1: Placing Batch Files in the Windows Directory**

- Copy your batch files to `C:\Windows`, which is already included in the `PATH`.
- This method eliminates the need to modify environment variables.
- **Caution:** Modifying the Windows directory requires administrative privileges and should be done carefully to avoid system issues.

**Method 2: Using the "App Paths" Registry Key**

- **Overview:**
  - Create custom command aliases by adding entries to the Windows registry under `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\App Paths`.
- **Steps:**
  - Press **Win + R**, type `regedit`, and press **Enter** to open the Registry Editor.
  - Navigate to the key: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\App Paths`
  - Right-click **App Paths**, select **New > Key**, and name it `d.exe` (or any command followed by `.exe`).
  - Select the new key, then double-click the **(Default)** value on the right pane.
  - Enter the full path to the executable, batch file, or folder you wish to open (e.g., `D:\`).
  - **Note:** Modifying the registry can impact system stability; proceed with caution and consider backing up the registry first.

---

### **Considerations and Limitations**

- **Permissions:**
  - Modifying user environment variables typically doesn't require administrative rights.
  - Editing the registry or system environment variables may require elevated permissions.

- **Security Risks:**
  - Ensure batch files contain safe commands to prevent unintentional system changes.
  - Avoid sharing sensitive scripts in shared environments.

- **Maintenance:**
  - Keep your quick-access folder organized.
  - Update batch files if application paths or folder locations change.

- **Name Conflicts:**
  - Choose unique names for your batch files to avoid conflicting with existing system commands.