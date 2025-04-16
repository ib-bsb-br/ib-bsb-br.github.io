---
tags: aid>software>windows
info: aberto.
date: 2025-04-16
type: post
layout: post
published: true
slug: requirements-for-sysprepbat-on-windows-server-2003
title: 'Requirements for sysprep.bat on Windows Server 2003'
---
## sysprep.bat

```sysprep.bat
@ECHO OFF
CLS
ECHO System Preparation Tool
ECHO.
ECHO Before continuing please:
ECHO 1. Be sure that the pre-sysprep steps were followed.
ECHO 2. Image the computer previous to this, as the sysprep
ECHO process may fail and this would corrupt the installation
ECHO you have prepared.
ECHO 3. Restart the computer before attempting this so that
ECHO system buffers are cleared.
ECHO 4. Close all open windows before continuing.
ECHO.
pause

ECHO.
ECHO Flushing data to disks (preliminary):
sync -r -e /accepteula

ECHO.
ECHO Cleaning up old driver caches:
del /s /q c:\sysprep\drivers\infcache.1

ECHO.
ECHO Creating driver path (SysPrep Driver Scanner):
spdrvscn /p c:\sysprep\drivers /e inf /d C:\windows\inf /m "Image: ~month/~day/~year" /o "Image created at ~hour:~minute:~second on ~month/~day/~year (~weekday)." /a /s /q

ECHO.
ECHO Closing open SMB connections:
net use * /delete /yes

ECHO.
ECHO Terminating unneeded processes:
kill /f vptray
kill /f ccapp
kill /f explorer
kill /f alg
kill /f ati2evxx
kill /f ccevtmgr
kill /f ccsetmgr
kill /f defwatch
kill /f lucoms~1
kill /f mdm

ECHO.
ECHO Stopping unnessary services:
net stop alerter /yes
net stop wuauserv /yes
net stop browser /yes
net stop cryptsvc /yes
net stop dhcp /yes
net stop mdm /yes
net stop trkwks /yes
net stop protectedstorage /yes
net stop remoteregistry /yes
net stop seclogon /yes
net stop samss /yes
net stop wscsvc /yes
net stop lanmanagerserver /yes
net stop "symantec antivirus" /yes
net stop defwatch /yes
net stop ccevtmgr /yes
net stop sndsrvc /yes
net stop ccpwdsvc /yes
net stop ccsetmgr /yes
net stop sens /yes
net stop srservice /yes
net stop schedule /yes
net stop lmhosts /yes
net stop ups /yes
net stop uphclean /yes
net stop webclient /yes
net stop audiosrv /yes
net stop sharedaccess /yes
net stop msiserver /yes
net stop w32time /yes
net stop wzcsvc /yes
net stop lanmanworkstation /yes
net stop spooler /yes

ECHO.
ECHO Flushing data to disks (finalization):
sync -r -e

ECHO.
ECHO Executing system preparation tool (reseal / minisetup)...
start sysprep -reseal -mini -quiet
```

To successfully execute the provided sysprep.bat script during a System Preparation (Sysprep) process on Windows Server 2003 Standard R2 x64, specific external software, utilities, and directory structures must be correctly configured and accessible. This document provides a detailed outline of these essential requirements. Sysprep itself is used to generalize a Windows installation, removing unique identifiers like the Security Identifier (SID) and configuring the OS to run an initial setup wizard (Mini-Setup) on the next boot, making the image suitable for deployment onto multiple machines. The process often involves external tools, like those in this script, to ensure data integrity by flushing disk caches, manage device drivers effectively for hardware independence across different target machines, and terminate potentially problematic background processes before sealing the final image. Failing to meet these prerequisites by having missing components or incorrect configurations will likely cause script execution errors, prevent the Sysprep process from completing successfully, or lead to deployment failures and unstable systems on target computers.

**Important Note on Privileges:** Executing this script requires Administrator privileges. Many actions performed, such as stopping system services, deleting files in protected locations (implicitly, via infcache.1), potentially placing tools in C:\\Windows\\System32, and running sysprep.exe itself, necessitate elevated rights. Ensure you are running the script from an administrative command prompt.

Standard Windows commands (ECHO, CLS, pause, del, net, start), which are integral parts of the Windows command-line environment, are assumed to be present in their default system locations (typically C:\\Windows\\System32) and are therefore not detailed as separate requirements below.

### **1\. Sysinternals Sync (sync.exe)**

* **Purpose in Script:** The script utilizes sync.exe (sync \-r \-e /accepteula and sync \-r \-e) to force the operating system to flush all modified file system data held in memory (cached data) to the physical disk drives. This is a critical step before finalizing system changes or shutting down, especially before the Sysprep reseal operation, as it ensures data consistency and minimizes the risk of data loss or corruption if the system were to shut down unexpectedly. The /accepteula flag is used once to automatically accept the Sysinternals End User License Agreement, preventing the script from pausing for user input. The \-r flag ensures it flushes files in subdirectories, and \-e attempts to flush and eject removable media.  
* **Required Software:** The specific executable sync.exe from the widely recognized Microsoft Sysinternals Suite. Using other utilities named 'sync' may not provide the same functionality or accept the same command-line arguments.  
  * *Acquisition:* This tool is typically downloaded directly from the official Microsoft Sysinternals documentation pages or website. For older operating systems like Windows Server 2003, ensure you obtain a version of the tool known to be compatible; archives of older Sysinternals suites may be necessary.  
* **Required Location:** For the script to run sync.exe, the executable must be located where the command processor can find it. This means placing sync.exe either in a directory listed in the system's PATH environment variable (like C:\\Windows\\System32) or directly in the same directory where the sysprep.bat script is being executed.  
* **Common Placement:** Placing sync.exe in C:\\Windows\\System32 is a frequent practice as it makes the tool available system-wide for various administrative scripts and tasks.

### **2\. Driver Scanner (spdrvscn.exe)**

* **Purpose in Script:** The command spdrvscn /p c:\\sysprep\\drivers ... strongly suggests this executable performs a specialized role related to device driver management during the Sysprep process. Its function is likely crucial for ensuring the prepared image can boot and correctly install devices when deployed onto potentially diverse hardware configurations. This might involve tasks such as scanning the system for installed drivers, comparing them against a repository, injecting necessary Plug-and-Play (PnP) drivers into the image from the specified path (c:\\sysprep\\drivers), or perhaps pre-indexing drivers to accelerate PnP detection during Mini-Setup. Effective driver management is fundamental to Sysprep's goal of hardware independence.  
* **Required Software:** An executable file specifically named spdrvscn.exe (or whatever tool this command actually invokes).  
  * *Note:* It is vital to understand that this is **not** a standard component of Windows Server 2003, nor is it part of common toolsets like Sysinternals or the Resource Kit Tools. It most likely represents a third-party utility or, quite possibly, a custom in-house tool developed specifically for the organization's unique imaging workflow. Crucially, you must identify this *exact* spdrvscn.exe tool from your organization's original imaging process and obtain it. Its specific function is unknown based solely on the script; attempting to substitute it with any other tool is impossible without knowing precisely what it does and will likely result in incorrect driver handling, deployment failures, or system instability (e.g., BSODs) on target machines.  
* **Required Location:** Similar to other external tools, spdrvscn.exe must be placed where the script can execute it: either in a directory included within the system's PATH environment variable or in the same directory from which the sysprep.bat script is being run.  
* **Common Placement:** Given its specialized nature and connection to Sysprep, it might logically reside within the C:\\Sysprep folder structure itself (e.g., in a subfolder like C:\\Sysprep\\Tools). Alternatively, it could be placed in C:\\Windows\\System32 or a centrally managed custom tools directory that's part of the system PATH. The script's reference to c:\\sysprep\\drivers might hint that related tools are also kept under C:\\Sysprep.

### **3\. Kill Process Utility (kill.exe)**

* **Purpose in Script:** The script uses kill.exe (with the /f flag for forceful termination) to stop specific background processes (vptray, ccapp, explorer, etc.) before proceeding with Sysprep. This is important to ensure a clean system state, prevent applications from interfering with the Sysprep operations (which modify many system files and registry settings), remove user-specific application states or running agents, and avoid potential conflicts during the resealing phase. The processes listed appear to include components of Symantec Antivirus (vptray, ccapp, ccevtmgr, ccsetmgr), the Windows shell (explorer), and various system or utility services.  
* **Required Software:** An executable named kill.exe. While Windows Server 2003 includes the native taskkill.exe command for terminating processes, this script explicitly relies on kill.exe. This specific utility often provided a simpler syntax or slightly different behavior compared to taskkill.  
  * *Acquisition:* kill.exe was a standard utility included in the freely downloadable Microsoft Windows Server 2003 Resource Kit Tools package. This package contained numerous helpful administrative utilities not included with the base OS.  
* **Required Location:** The kill.exe executable must be found by the command interpreter. Place the file either in a directory that is part of the system's PATH environment variable or directly in the same directory where the sysprep.bat script resides and is executed.  
* **Common Placement:** If the full Windows Server 2003 Resource Kit Tools package is installed, its installation directory is typically added to the system PATH automatically, making kill.exe accessible. A common alternative for deploying specific tools is to copy kill.exe directly into the C:\\Windows\\System32 folder.

### **4\. System Preparation Tool (sysprep.exe)**

* **Purpose in Script:** This is the core Microsoft utility essential for the entire image preparation process. The command start sysprep \-reseal \-mini \-quiet initiates the final phase. Specifically, \-reseal configures the system to run the Mini-Setup wizard (also known as Windows Welcome or OOBE \- Out-Of-Box Experience) upon the next boot, clearing system-specific information like the SID. The \-mini option specifies that the Mini-Setup wizard should run, allowing for customization during deployment (like setting computer name, joining a domain, etc.). The \-quiet flag suppresses any graphical user interface or prompts from Sysprep itself, making it suitable for automated scripting.  
* **Required Software:** The main sysprep.exe executable and all its necessary supporting files (such as setupcl.exe, factory.exe, and various .inf or .dll files). These components work together; simply having sysprep.exe alone is insufficient. These files are specific to the operating system version, architecture (x64 in this case), and potentially the service pack level. Using mismatched versions can lead to unpredictable failures.  
  * *Acquisition:* The correct Sysprep files for Windows Server 2003 are typically located within the Deploy.cab compressed archive file found in the \\Support\\Tools\\ directory on the official Windows Server 2003 installation media (CD or ISO). You must extract the *entire contents* of Deploy.cab to the designated Sysprep location using a tool capable of handling CAB archives (like expand.exe or built-in Windows functionality).  
* **Required Location:** Sysprep files must be placed precisely where the operating system and the start sysprep command expect to find them. While Sysprep *might* be found if placed in the system PATH, this is not the standard or recommended practice for Windows Server 2003\.  
* **Standard Location:** For Windows Server 2003, the universally accepted and expected location is the C:\\Sysprep folder at the root of the system drive. You should manually create this folder if it doesn't exist and then extract all files from the Deploy.cab archive directly into C:\\Sysprep.

### **5\. Directory Structure (C:\\Sysprep\\drivers)**

* **Purpose in Script:** The script explicitly interacts with this directory in two ways: first, by deleting c:\\sysprep\\drivers\\infcache.1, and second, by passing the path c:\\sysprep\\drivers as a parameter to spdrvscn.exe. The deletion of infcache.1 (a file Windows uses to cache information about discovered INF files) is likely intended to force a complete rebuild of the driver cache during Mini-Setup, ensuring that only explicitly provided or newly detected drivers are considered, rather than relying on potentially outdated cached information. The spdrvscn.exe tool, as discussed, likely uses this directory either as a source repository from which to inject necessary drivers into the image or as a target location to store information about the drivers it has processed for use during deployment.  
* **Required:** The directory path C:\\Sysprep\\drivers must physically exist on the file system *before* the sysprep.bat script is executed. If the directory is missing, the del command might simply report an error, but the spdrvscn.exe tool would likely fail catastrophically if it expects to read from or write to this specific location. The contents required within this directory depend entirely on the function of the custom spdrvscn.exe tool.

Note on Services:  
The script includes a lengthy section dedicated to stopping numerous Windows services using net stop. Examples include security software (symantec antivirus, defwatch), Windows Update (wuauserv), networking services (dhcp, lanmanserver, lanmanworkstation), and various others. While the script attempts to stop these, their actual presence on the system isn't strictly required for the net stop command itself to run (it will simply report an error like "The service name is invalid" or "The service has not been started" if the service doesn't exist or isn't running). However, the explicit inclusion of these commands strongly implies that the script was carefully crafted for a specific baseline system configuration where these services were typically installed and running. Stopping them is considered best practice before Sysprep to prevent interference with the generalization process (e.g., AV scanning/blocking file changes, Windows Update trying to install updates, DHCP client renewing leases during cloning, remote registry service allowing unwanted access). Failure to stop necessary services, especially those performing background file modifications or network communications, could compromise the integrity and stability of the sealed image.  
**Verification Note:** The information provided regarding sync.exe and kill.exe assumes the use of standard, compatible distributions from Microsoft Sysinternals and the Windows Server 2003 Resource Kit Tools, respectively. Given the significant age of the Windows Server 2003 operating system, it is absolutely crucial to verify that you are using tool versions explicitly stated as compatible with this OS and architecture (R2 x64). Using incompatible or newer versions not designed for WS2003 could lead to subtle errors or outright failures. Furthermore, the identity, specific function, and correct method for obtaining and implementing the non-standard spdrvscn.exe utility must be determined entirely from the documentation or institutional knowledge surrounding your organization's specific, established imaging process. This document can only highlight its likely role based on the script's commands.

Ensuring these prerequisites are met is essential for the successful execution of the sysprep.bat script and the creation of a reliable Windows Server 2003 image.