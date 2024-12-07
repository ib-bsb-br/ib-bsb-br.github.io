---
tags: software>windows
info: aberto.
date: 2024-12-07
type: post
layout: post
published: true
slug: windows-xp-vm-for-hyper-v
title: 'Windows XP VM for Hyper-V'
---
#### Introduction
This guide provides a step-by-step process for setting up an official Windows XP virtual machine (VM) using Hyper-V. The purpose is to enable users to run legacy applications or perform tasks that require Windows XP in a controlled environment.

#### Prerequisites
- Ensure Hyper-V is installed on your host machine.
- Verify that you have the necessary permissions to install software and create virtual machines.

#### Background
Windows XP is an older operating system no longer supported by Microsoft, which means it doesn't receive security updates. Therefore, it's crucial to use this VM in a secure and controlled environment to minimize risks.

#### Obtaining the Virtual Machine Image
1. **Windows XP Mode**: Download the Windows XP Mode executable from the [archive.org link](https://archive.org/details/windows-xp-mode_20200907). This executable contains the virtual hard disk (VHD) image needed for the VM.

2. **Note**: The original Microsoft download link may not be active, hence the archive.org link is provided.

#### Extracting the VHD File
1. **Using 7-Zip**:
   - Open 7-Zip and drag the downloaded Windows XP Mode executable (e.g., `WindowsXPMode_en-us.exe`) into the 7-Zip window.
   - Navigate to the `Sources` folder within the executable.
   - Extract the `xpm` file to a local directory.

2. **Extracting the VHD**:
   - Open the extracted `xpm` file with 7-Zip.
   - Locate and extract the `VirtualXPVHD` file to a desired location.

3. **Renaming the VHD**:
   - Rename the extracted `VirtualXPVHD` file to `VirtualXP.VHD` by using the F2 key.

#### Setting Up the Virtual Machine in Hyper-V
1. **Creating a New VM**:
   - Open Hyper-V Manager.
   - Create a new virtual machine with the following settings:
     - Name: Windows XP
     - Memory: Allocate appropriate RAM (e.g., 1024 MB).
     - Networking: Attach to the default switch or a specific virtual switch.
     - Storage: Choose the existing virtual hard disk and browse to the `VirtualXP.VHD` file.

2. **Configuring VM Settings**:
   - Ensure that the VM is set to use the correct version of Hyper-V.
   - Adjust processor allocation as needed.

#### Post-Setup Configuration
1. **Initial Boot**:
   - Start the VM and complete the initial setup if required.
   - Activate Windows XP using a valid license key if necessary.

2. **Network Adapter**:
   - If using VirtualBox, ensure to select the "PCnet FAST III" network adapter for compatibility.

3. **Web Browser**:
   - For browsing the web, it's recommended to use Firefox 52 ESR, as Internet Explorer 6 does not support modern TLS protocols.

#### Testing the Virtual Machine
1. **Boot Verification**:
   - Ensure the VM boots correctly and reaches the desktop.
   - Check that basic applications and system functions work as expected.

2. **Network Connectivity**:
   - Verify that the VM can connect to the network and access the internet.
   - Test browsing using the recommended browser.

#### Maintenance and Updates
1. **Checkpoints**:
   - Regularly create checkpoints in Hyper-V to allow for rollback in case of issues.

2. **Security Considerations**:
   - Since Windows XP is no longer supported, ensure the VM is isolated and not exposed to untrusted networks.
   - Consider running the VM with enhanced security measures, such as firewalls and antivirus software compatible with Windows XP.

#### Troubleshooting
- **VM Fails to Boot**:
  - Ensure the VHD file is correctly extracted and renamed.
  - Verify that Hyper-V is properly installed and configured on the host machine.

- **Network Issues**:
  - Check the network adapter settings in the VM.
  - Ensure the virtual switch is correctly configured in Hyper-V Manager.

#### References and Resources
- [Windows XP Mode on Wikipedia](https://en.wikipedia.org/wiki/Windows_Virtual_PC#Windows_XP_Mode)
- [Hyper-V Manager Documentation](https://docs.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/managing-virtual-machines-with-hyper-v-manager)