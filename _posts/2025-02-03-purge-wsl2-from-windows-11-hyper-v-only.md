---
tags: [scratchpad]
info: aberto.
date: 2025-02-03
type: post
layout: post
published: true
slug: purge-wsl2-from-windows-11-hyper-v-only
title: 'Purge WSL2 from Windows 11 (Hyper-V only)'
---
Removing WSL and WSL2 from Windows 11 to work exclusively with Hyper-V involves a set of deliberate steps designed to eliminate the Linux compatibility layer and its associated virtual environment, without disabling Hyper-V itself. Below is a detailed guide that covers how to perform these actions, the technical rationale behind them, and the impacts on your system.

#### 1. Step-by-Step Removal Process

**Step 1: Uninstall Linux Distributions**  
- **Action:** Unregister and remove any installed Linux distributions.  
- **Command Example:**
  ```powershell
  wsl --list --quiet  # Lists all installed distributions
  wsl --unregister <DistributionName>  # Replace <DistributionName> (e.g., Ubuntu) for each distribution
  ```
- **Rationale:** This step ensures that no residual Linux distributions are left which might continue to consume system resources.

**Step 2: Disable WSL and Associated Features**  
- **Action:** Open the "Turn Windows features on or off" dialog.
  - Uncheck **Windows Subsystem for Linux**.
  - Uncheck **Virtual Machine Platform**.
- **Note:** Although the Virtual Machine Platform is used by WSL2, some features like Windows Sandbox also depend on it. Consider whether you need these features before disabling.
- **Action:** Reboot the system to finalize these changes.

**Step 3: Remove Residual Files and Configuration Data**  
- **Action:** Clean up any leftover files that may reside in the user profile.
- **Command Example:**
  ```powershell
  Remove-Item -Recurse -Force "$env:USERPROFILE\AppData\Local\Packages\*CanonicalGroup.Ubuntu*"
  ```
- **Rationale:** This recovers disk space and removes configuration data that is no longer needed.

**Step 4: Verify Hyper-V Remains Active**  
- **Action:** Check that Hyper-V is still enabled, since it is independent of WSL/WSL2.
- **Command Example:**
  ```powershell
  Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V
  ```
- **If needed, re-enable Hyper-V:**
  ```powershell
  Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All
  ```
- **Rationale:** This confirms that the removal of WSL components did not inadvertently disable Hyper-V’s core functionalities.

#### 2. Why This Process Works (Technical Rationale)

- **WSL/WSL2 Architecture:**  
  - WSL provides a compatibility layer for running Linux binaries on Windows. WSL2, in particular, utilizes a lightweight VM managed by the Virtual Machine Platform. Removing these components stops the Linux interface and associated VM without affecting Hyper-V.
  
- **Hyper-V Independence:**  
  - Hyper-V is a Type 1 hypervisor that operates directly on the hardware abstraction layer. It remains fully operational independent of the WSL components. Therefore, disabling WSL/WSL2 frees up resources while leaving your primary virtualization platform intact.
  
- **Clean Removal:**  
  - By unregistering distributions and disabling the specific Windows features, you ensure that no parts of the WSL layer or its supporting services remain active. This prevents resource conflicts and can potentially simplify system configuration, especially if you rely exclusively on Hyper-V for virtual machine management.

#### 3. Impacts on System Functionality

**Consequences**  
- **Loss of Native Linux Integration:**  
  - You will no longer have immediate access to Linux command-line tools or distributions on Windows.
  - Tools and extensions (e.g., for Visual Studio Code) that depend on WSL may no longer work.
  
- **Tool Compatibility Changes:**  
  - Docker Desktop users who rely on the WSL2 backend must reconfigure Docker to use the Hyper-V backend or Windows Containers.

**Benefits**  
- **Resource Optimization:**  
  - Reclaim system resources (memory, CPU, storage allocated for WSL2’s virtual machine) for use by Hyper-V, potentially improving performance.
  
- **Simplified Virtualization Environment:**  
  - Reduced complexity in virtualization settings by eliminating duplicate virtualization layers.
  - Less potential for conflicts between different virtualization and containerization environments.

**Limitations**  
- **Reduced Flexibility:**  
  - Removing WSL/WSL2 means you lose the ability to run Linux applications natively within Windows, which is beneficial for development and testing.
  
- **Dependency Impact:**  
  - Certain applications or environments that integrate with WSL2 will require reconfiguration or alternative solutions.

#### Final Verification

After completing the steps:
- **Confirm no Linux distributions remain active:**
  ```powershell
  wsl --list  # Expected output: "No installed distributions."
  ```
- **Test Hyper-V:**  
  - Use Hyper-V Manager to create and run a virtual machine to verify that Hyper-V operates as expected.

This comprehensive process ensures that you remove WSL/WSL2 completely while continuing to leverage Hyper-V exclusively, along with an understanding of the technical and practical impacts of this change.
