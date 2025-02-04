---
comment: 'https://csh.rit.edu/~rg/alphasmart-3000/20221106195356/'
tags: [tasks, estudos>hardware]
info: aberto.
date: 2024-12-09
type: post
layout: post
published: true
slug: alphasmart
title: 'AlphaSmart Troubleshooting and Updating'
---
AlphaSmart devices were portable, battery-powered word processors popular in educational settings for their simplicity and durability. They allowed students to type and save their work, which could then be transferred to a computer. This guide provides comprehensive troubleshooting steps for common issues encountered with AlphaSmart devices, including general error messages, factory resets, and recovery from update interruptions. *Note that beginning March 5, 2010, AlphaSmart Manager replaced AlphaSmart Manager 2.*

## **Troubleshooting Your AlphaSmart Device**

This section outlines various troubleshooting steps to resolve common issues with your AlphaSmart device.

### **1. Addressing Common Error Messages**

**Issue:**

Your AlphaSmart device is displaying an error message.

**Reason:**

Common error messages for AlphaSmart 1 and AlphaSmart 2 include (but are not limited to):

*   _Bus Error_
*   _Address Error_
*   _Memory Size Overflow_
*   _Bad Data Pointer_
*   _Bad File Pointer_

**Resolution:**

Many error messages can be resolved by turning the device off and then back on. If this doesn't work, or if the error persists, follow these steps to retrieve AlphaWord files and reinstall the AlphaSmart system:

1. **Download and Install AlphaSmart Manager:** Download and install the latest version of AlphaSmart Manager from [http://www.renaissance.com/Customer-Center/alphasmart-downloads](http://www.renaissance.com/Customer-Center/alphasmart-downloads). Launch the application and leave it open on your computer.
2. **Connect Your AlphaSmart Device:**
    *   Turn off your AlphaSmart device.
    *   Hold down the <left-shift\> and <tab\> keys, then press the <on/off\> key.
    *   Release the keys when the screen displays "Select a SmartApplet and press enter."
    *   Connect the AlphaSmart device to your computer via a USB cable.
    *   If a Found New Hardware wizard appears and prompts about drivers not passing Windows Logo Testing, click "Continue Anyway."

    **NOTE:** This step won't work if Two-Button On is enabled. If it is, hold down the <left-shift\> and <tab\> keys while connecting the USB cable.
3. **Verify Connection:** Wait for the AlphaSmart screen to show "Connected to AlphaSmart Manager" and for the AlphaSmart Manager application to show one connected device (Direct USB). You can retrieve data from the 8 active file spaces or sync KeyWords data with Renaissance Place at this point.
4. **Configure Preferences:**
    *   In AlphaSmart Manager, click the Edit menu and select Preferences.
    *   Check the box for "Replace SmartApplets on device with SmartApplets from computer."
    *   Click OK.
5. **Reset Your AlphaSmart Device:**

    **WARNING:** This step will delete all AlphaWord files, all KeyWords students and data, and any quizzes loaded into AlphaQuiz. It also removes any non-default SmartApplets (e.g., Co:Writer).
    *   Click the Setup menu and select "Reset All AlphaSmart Devices..."
    *   Confirm by clicking Yes. AlphaSmart Manager will reinstall default SmartApplets and update your ROM and AlphaWord version, if applicable.
6. **Restore Files (Optional):** After the reset, you can restore AlphaWord files using the AlphaWord Files to Send tab.
7. **Disconnect and Resume:** Disconnect your AlphaSmart device and resume normal usage.

If you continue to receive error messages, refer to the section "Recovering from Update Interruptions" below.

### **2. Performing a Factory Reset**

A factory reset can be necessary if your device is experiencing persistent issues not resolved by simpler troubleshooting steps, or if you need to clear all data and settings.

**Issue:**

You need to reset your AlphaSmart device to its original factory settings.

**Reason:**

A factory reset will:

*   Delete all AlphaWord Plus files.
*   Delete all AlphaQuiz files.
*   Return all System and SmartApplet settings to their defaults.
*   Reset the master password (password protection will be turned off).

**Resolution:**

To reset your AlphaSmart device to factory defaults:

1. **Power Off:** Start with the device turned off.

    **Note:** The AlphaSmart device cannot be reset while plugged in via an AC adapter.
2. **Initiate Reset:**
    *   Press and hold the <right-shift\> and <backspace\> keys.
    *   While holding these keys, press the <on/off\> key to turn the device on.
3. **Confirm Reset:** When the screen displays "Are you sure you want to reset the AlphaSmart to factory defaults?", press Y (for yes).
4. **Enter Password:** Enter the reset password: **tommy**

    **Note:** Ensure only one asterisk appears per letter typed.
5. **Complete Reset:** Press <Enter\>.

**Note:** If successful, you'll see "Initializing AlphaSmart System." If not, you'll return to the last file, and you'll need to try again.

>Master password: think
>Default file password: write
>Factory default reset password: tommy

### **3. Recovering from Update Interruptions**

**Issue:**

Your AlphaSmart device is unresponsive after an update process was interrupted and does not respond to a reset.

**Resolution:**

If your AlphaSmart device becomes unresponsive due to an interrupted update, you can use the Small ROM mode for recovery. The Small ROM contains essential communication drivers that allow you to restore the device after a critical failure.

**Entering Small ROM Mode:**

1. **Initiate Small ROM Mode:**
    *   Press and hold <comma\>, <period\>, <forward slash\>, and <right-shift\>.
    *   While holding these keys, press <on/off\>.

    **NOTE:** If the device doesn't respond, connect a live USB cable while holding the four keys.
2. **Enter Password:** When prompted with "Enter Small ROM Password," enter the password: **ernie**
3. **Connect to AlphaSmart Manager:** Connect your AlphaSmart device to AlphaSmart Manager via a USB cable or an AlphaHub.
4. **Configure Preferences:**
    *   In AlphaSmart Manager, click the menu, then select Preferences.
    *   Check the box next to "Replace SmartApplets on device with SmartApplets from computer."
    *   Close the Preferences menu.
5. **Reset the Device:**
    *   Click the Setup menu, then select "Reset All AlphaSmart Devices."
    *   Click \[Yes] to proceed.

**Resolving Corrupted SmartApplets:**

If errors persist, you may have corrupted SmartApplets. This is often the case if Co:Writer was not installed successfully. Follow these steps:

1. **Disconnect:** Disconnect the AlphaSmart device from AlphaSmart Manager.
2. **Enter Updater Mode:** Press and hold the <left-shift\> and <tab\> keys while powering on the device.

    **NOTE:** If the device turns on briefly but then powers off, perform a factory default reset (see Section 2), then try again.
3. **Updater Mode or Applets Menu:** The device should display either "Attempting to enter the Updater Mode" or the Applets menu. If it displays the Applets menu, proceed to step 4. If it displays "Attempting to enter the Updater Mode", the device may take up to 3 minutes to switch to the Applets menu.
4. **Add a SmartApplet:** In AlphaSmart Manager, add a SmartApplet that is not utilized by Co:Writer, such as the Calculator or Beamer SmartApplets, to the install list.
5. **Delete Other SmartApplets:** Check the box that says "Delete SmartApplets that are not in the Install List from AlphaSmart Devices."
6. **Send the List:** Go to the Send List tab and click \[Send]. You may encounter errors on the device; press the space bar to clear them and continue the update. The device may take up to 3 minutes to reboot after the update is sent.

Completing these steps will remove any SmartApplets not included in the Send List. You should now be able to install additional SmartApplets. If errors continue, repeat these steps, choosing a different SmartApplet in step 4.

***

## Updating the Software

System 3 comes with [all kinds of updates](https://support.renaissance.com/techkb/download/AS3000_System_3_Addendum.pdf), including but not limited to viewing word counts (Ctrl+W), saving and opening files (Ctrl+N and Ctrl+F), and password protection.

I’ve been able to update all my Alphasmarts (both those running v1.3 as well as those running v1.6) to System 3.01 by following these steps:

*   Install [VirtualBox](https://www.virtualbox.org/) on Windows 10
*   Launch a virtual machine using a Windows XP ISO file (you can find them online)
    *   It will ask for a serial number, but you can just leave it blank each time it asks
*   Install [Alphasmart Manager](https://csh.rit.edu/~rg/alphasmart-3000/attachments/ASM3000Manager2.3Full.zip) (ASM 2.3)
*   Launch ASM 2.3 and connect your device via USB
    *   You will need to enable USB access in the virtual machine’s settings

![Image 5](https://csh.rit.edu/~rg/alphasmart-3000/attachments/2022-11-09-17-35-58.png)

*   Once the device is selected, go to the `SmartApplets` tab and select the applets you want
    *   AlphaWord Plus is a must
    *   Control Panel is a must
    *   SpellCheck Small is recommended
    *   Thesaurus Small is recommended

![Image 6](https://csh.rit.edu/~rg/alphasmart-3000/attachments/2022-11-09-17-27-03.png)

*   Next, head to the `Settings` tab and select System 3 in the left nav, make sure the Startup SmartApplet is set to AlphaWord Plus
    *   Change any other settings you wish to change
*   Go to the `Send List` tab and if everything looks good, click `Send`.
*   Wait for your device to update, DO NOT DISCONNECT IT until the update is complete.
