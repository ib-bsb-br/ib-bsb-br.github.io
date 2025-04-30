---
tags: [scratchpad]
info: aberto.
date: 2025-04-30
type: post
layout: post
published: true
slug: winntsetup-universal-windows-installer
title: 'WinNTSetup - universal Windows Installer'
---
**Features:**

*   Install (unattend) Windows 2k/XP/20??/Vista/7/8.x/10/11 x86/x64/arm64
*   Practically runs even on the most minimalistic WinPE
*   selectable drive letter for the new Windows installation
*   Fully automated with save/load setting in ini file and various command line options
*   Install Windows also if nlite/vlite has remove winnt32.exe/setup.exe
*   Integrate Drivers: normal PNP and Textmode Drivers
*   Patch uxtheme to allow unsigned Themes
*   Some common registry tweaks and \*.reg file import
*   DISM APPX  removal, feature enable/disable
*   Simple VHD creation and Installation
*   Support "Windows to Go" for Windows 7 and later installs
*   Supports WimBoot and CompactOS option for Windows 7 and later
*   Supports all current WIM files: WIM/SWM/ESD and ISO files
*   WinCapture - capture a Windows installation to WIM or ESD file
*   MinWin - simple trimming WIM in memory before apply
*   WinCopy - copy an existing Windows installation to another partition
*   Offline Hotfix uninstall
*   Offline password reset

**Not Supported:**

*   \- No Windows embedded version (this includes WinFLP)
*   \- No upgrades of existing installations

**About driver installation:**

Every driver added in NT6.x windows will be added to the driver store.  
So it's not recommended to add countless driver, but rather more really required ones.

NT5.x massstorage driver integration is possible thanks to **Mr dUSHA** powerful **MSSTMake.exe** tool

  
**To the Unattend option:**It's possible to use an **unattend.xml** to run the Setup unattended.  
But as the actual WinPE Setup Phase isn't effective in that way of install, all Winpe related settings inside the unattend.xml  
won't be applied.

  
**Ini config file**It's possible to save all GUI-settings to a ini file:

push **Ctrl + S** to **save** all settings to an ini.  
push **Ctrl + L** to **load** all settings from an ini.

A **WinNTSetup.ini** file in the same dir as the app itself will be loaded automatically at startup.

It also can be selected via command line:

WinNTSetup.exe /cfg:"C:\\mysettings.ini"

If you want to modify ini settings yourself, click-click has made a nice [PDF](https://www.mediafire.com/file/znuf574scdac94d/WinNTGUI2Ini.pdf/file) for it.

For advanced users there are also hidden settings described in the included WinNTSetup.ini.txt

**Command line:**

\- Press F1 to get list of all options

**To install Windows in a VHD file:**\- requires Windows 7 as OS and **Windows 7 Ultimate, Enterprise or Server 2008 R2** as Source  
\- create a partitioned VHD and assign a drive letter (push Ctrl + Shift + V to use build in diskpart wrapper for this)  
\- select the VHD drive as installation drive (make sure you boot drive ist a active primary partition on a physical disk)

If you get an Antivirus warning from your AV software, please report it to them as a false positive and let them check it.

**Current Version: 5.4.1**

Download: [Mega](https://mega.nz/folder/ObATya7C#oR2t79bT-4MGjKxOAYwkbQ) \- [MediaFire](https://www.mediafire.com/folder/53um6k2nmhvd5/)

**Edited December 29, 2024 by JFX**

21

  

[![Image 4: jaclaz](https://msfn.org/board/uploads/monthly_2017_08/Jgray.thumb.jpg.8353b51d429039be7eaa0a7da3fbd3fe.jpg)](https://msfn.org/board/profile/25215-jaclaz/ "Go to jaclaz's profile")

It looks like a nice tool. [![Image 5: :thumbup](https://msfn.org/board/applications/core/interface/js/spacer.png)](https://msfn.org/board/uploads/emoticons/default_thumbup.gif "Enlarge image")

And it shouldn't be dedicated to "USB only", if I am not mistaken. [![Image 6: :unsure:](https://msfn.org/board/applications/core/interface/js/spacer.png)](https://msfn.org/board/uploads/emoticons/default_unsure.png "Enlarge image")

Let's hope that whoever tests it will be so kind as to (please read as "anyone testing it please do") provide - for the benefit of the less expereinced users - some details on the various available options, and their usage.

Usual bothering request to the developer [![Image 7: :blushing:](https://msfn.org/board/applications/core/interface/js/spacer.png)](https://msfn.org/board/uploads/emoticons/default_blushing.gif "Enlarge image") :

*   Any chance that it will ever support command line? (or provide a pre-set in the form of a .ini file?) [![Image 8: :whistle:](https://msfn.org/board/applications/core/interface/js/spacer.png)](https://msfn.org/board/uploads/emoticons/default_whistling.gif "Enlarge image")  
    

jaclaz

[![Image 9: JFX](https://msfn.org/board/uploads/monthly_2025_01/avatar_small.thumb.png.54db03064974c08ad6356a340b1173b3.png)](https://msfn.org/board/profile/314753-jfx/ "Go to JFX's profile")

*   **Author**

> And it shouldn't be dedicated to "USB only", if I am not mistaken. [![Image 10: :unsure:](https://msfn.org/board/applications/core/interface/js/spacer.png)](https://msfn.org/board/uploads/emoticons/default_unsure.png "Enlarge image")

Well, you right, not the most correct forum section

> Let's hope that whoever tests it will be so kind as to (please read as "anyone testing it please do") provide - for the benefit of the less expereinced users - some details on the various available options, and their usage.

hmm, yeah i could add tool tip/balloons for every check box

Thanks for reminding about the ini file [![Image 11: :)](https://msfn.org/board/applications/core/interface/js/spacer.png)](https://msfn.org/board/uploads/emoticons/default_smile.png "Enlarge image") Added to first Post

More command line options could be added, if requested.

*   2 weeks later...

[![Image 12: lama](blob:http://localhost/3421ba85060e6030e813683c8ff84905)](https://msfn.org/board/profile/125656-lama/ "Go to lama's profile")

Thanks for the link @ reboot.pro wonko, but, how come this v 2.0 was not even mentioned by original creator? Excuse me but,...Did i missed the part where JFX became "was\_JFX" there? [![Image 13: :huh:](https://msfn.org/board/applications/core/interface/js/spacer.png)](https://msfn.org/board/uploads/emoticons/default_huh.png "Enlarge image")

[![Image 14: jaclaz](https://msfn.org/board/uploads/monthly_2017_08/Jgray.thumb.jpg.8353b51d429039be7eaa0a7da3fbd3fe.jpg)](https://msfn.org/board/profile/25215-jaclaz/ "Go to jaclaz's profile")

> Thanks for the link @ reboot.pro wonko, but, how come this v 2.0 was not even mentioned by original creator? Excuse me but,...Did i missed the part where JFX became "was\_JFX" there? [![Image 15: :huh:](https://msfn.org/board/applications/core/interface/js/spacer.png)](https://msfn.org/board/uploads/emoticons/default_huh.png "Enlarge image")

Evidently yes.

And however I don' t think it is part of your business.

jaclaz

[![Image 16: wimb](https://msfn.org/board/uploads/av-132150.jpg)](https://msfn.org/board/profile/132150-wimb/ "Go to wimb's profile")

