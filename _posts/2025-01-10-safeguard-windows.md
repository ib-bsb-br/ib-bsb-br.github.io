---
tags: [aid>software>windows]
info: aberto.
date: 2025-01-10
type: post
layout: post
published: true
slug: safeguard-windows
title: 'Safeguard Windows 11 customization'
---
### **1. Creating a Complete System Backup**

Windows 11 includes the "Backup and Restore (Windows 7)" feature, which allows you to create a system image.

**Steps:**

1. **Access the Backup Tool:**

   - Open the **Control Panel**.
   - Navigate to **"System and Security"** - **"Backup and Restore (Windows 7)"**.

2. **Create a System Image:**

   - Click on **"Create a system image"** in the left pane.
   - Choose a destination to save the backup (external hard drive, DVDs, or network location).
   - Select the drives you want to include (ensure your system drive is selected).
   - Proceed with the backup process.

3. **Create a System Repair Disc (Optional):**

   - In the same window, select **"Create a system repair disc."**
   - Follow the prompts to create a bootable repair disc.

**Considerations:**

- This method creates a full image of your system, allowing for complete restoration.
- It's suitable for personal use and doesn't require additional software.

---

### **2. Replicating Your Custom Settings to Other Machines**

**a) Using Windows Configuration Designer**

Create a provisioning package to apply your settings to other devices.

**Steps:**

1. **Install Windows Configuration Designer:**

   - Available from the Microsoft Store or as part of the Windows Assessment and Deployment Kit (ADK).

2. **Create a Provisioning Package:**

   - Launch the app and select **"Provision desktop devices."**
   - Configure the settings, policies, and applications you wish to deploy.

3. **Export the Package:**

   - Build and export the provisioning package (.ppkg file).

4. **Apply the Package to Target Machines:**

   - Transfer the .ppkg file to the target machine.
   - Run the package by double-clicking it, or apply it during the initial setup process.

**Considerations:**

- Ideal for users who prefer a graphical interface.
- Suitable for small to medium deployments.
- May not capture all personal customizations or third-party application settings.

---

**b) Using PowerShell Scripts**

Automate the configuration process with scripts.

**Steps:**

1. **Identify Configurable Settings:**

   - Determine which settings can be applied via PowerShell commands or registry edits.

2. **Write the PowerShell Script:**

   - Script the desired changes.
   - Example to disable the lock screen:

     ```powershell
     New-Item -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\Personalization" -Force
     New-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\Personalization" -Name "NoLockScreen" -Value 1 -PropertyType DWORD -Force
     ```

3. **Test the Script:**

   - Run the script on a test machine to ensure it works as intended.

4. **Deploy the Script:**

   - Execute the script on target machines with administrative privileges.

**Considerations:**

- Requires some scripting knowledge.
- Highly customizable and repeatable.
- Good for version control with tools like Git.

---

**c) Using User State Migration Tool (USMT)**

Migrate user accounts, data, and settings.

**Steps:**

1. **Install Windows ADK:**

   - Includes USMT for deployment purposes.

2. **Capture User State on Source Machine:**

   - Use `ScanState` to collect user profiles and settings.

3. **Apply User State on Target Machine:**

   - Use `LoadState` to deploy the collected data.

**Considerations:**

- Geared towards IT professionals.
- Does not migrate applications.
- Best suited for enterprise environments.

---

**d) Creating a Custom Image with Sysprep and Deployment Tools**

For deploying a standardized environment across multiple machines.

Steps: `https://ib.bsb.br/sysprep`
