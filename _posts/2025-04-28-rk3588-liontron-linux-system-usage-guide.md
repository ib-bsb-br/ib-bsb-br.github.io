---
tags: [scratchpad]
info: aberto.
date: 2025-04-28
type: post
layout: post
published: true
slug: rk3588-liontron-linux-system-usage-guide
title: 'RK3588 liontron Linux System Usage Guide'
---
**Prerequisites**

Before proceeding, ensure you have the following:

* **Hardware:**  
  * The development board itself  
  * Necessary power supply  
  * Display (if applicable)  
  * Keyboard/mouse (if applicable)  
  * Ethernet cable  
  * WiFi access (if needed)  
  * USB OTG cable  
  * CAN loopback cable (2-pin H/L)  
  * Microphone, camera (if testing these features)  
* **Host Computer:**  
  * A separate computer (Windows, macOS, or Linux) for tasks like flashing, SSH access, and ADB communication.  
* **Host Software:**  
  * ADB (Android Debug Bridge) installed and functional.  
  * A text editor (like Notepad++, VS Code, vim, nano) for potential script editing.  
  * An SSH client (like PuTTY, Windows Terminal, or built-in terminal on Linux/macOS).  
  * The cansend/candump utilities (if performing CAN tests, placed in a known location like D:\\can-utils).  
  * Board-specific flashing tools and system image files (if flashing is required).  
* **Skills:** Basic familiarity with the Linux command line environment (navigating directories, executing commands) is assumed. Knowledge specific to the development board's hardware may also be beneficial.

**Note on Permissions and Usernames:** Commands often require appropriate privileges, which can be gained by using sudo before commands or switching to the root user via sudo su. The username teamhd appears in examples and should typically be replaced with your actual username where applicable during operations like SSH login.

**1\. Network Configuration and System Information**

Establishing network connectivity is often the first step after initial system setup. This section details how to configure both wired (Ethernet) and wireless (WiFi) connections, using either automatic (DHCP) or manual (static IP) methods, and how to verify network parameters.

* 1.1.3 Check MAC address, IP address  
  Verifying the MAC (Media Access Control) address, a unique hardware identifier, and the assigned IP (Internet Protocol) address is crucial for network identification and troubleshooting. To view these details for your active connection (WiFi or Ethernet):  
  Navigate to the WiFi Icon or Network Manager Icon (often located in the system tray or panel) \> Select Connection Information. This will display details about the current connection, including the IPv4 address, subnet mask, gateway, DNS servers, and the hardware MAC address.  
* 1.2 Set up Ethernet  
  Ethernet provides a stable, wired network connection.  
  * 1.2.1 Connect to Ethernet (DHCP)  
    DHCP (Dynamic Host Configuration Protocol) allows the system to automatically obtain an IP address and other network settings from a router or DHCP server on the network. This is the most common and straightforward method for typical networks.  
    1. Physically connect the device to your network using an Ethernet cable.  
    2. Go to the **Network Manager icon** (often depicted with up/down arrows, interconnected computers, or similar) \> Select **Connection Information**.  
    3. If an IP address (e.g., 192.168.1.100), Subnet Mask (e.g., 255.255.255.0), and Gateway (e.g., 192.168.1.1) are displayed under the IPv4 section, the DHCP configuration was successful, and the connection is active. To further verify connectivity, you can try pinging the gateway (e.g., ping 192.168.1.1) or an external address (e.g., ping 8.8.8.8) from the terminal.  
  * 1.2.2 Set up Ethernet static IP address  
    Assigning a static IP address ensures the device always uses the same IP address on the network, which can be necessary for servers or devices that need to be reliably accessed by others. This requires manual configuration.  
    1. Go to the Network Manager icon \> Select Edit Connections... \> In the dialog window, select the relevant wired connection (often named "Wired connection 1" or similar, corresponding to eth0 or equivalent interface) \> Click the Gear icon (Settings).  
       (Alternative Access: If the icon is unavailable, you might access these settings via the main System Settings menu, typically under 'Network' \-\> 'Wired' \-\> 'Options/Settings'. Alternatively, advanced users can use command-line tools like nmcli con edit 'Wired connection 1'.)  
    2. In the connection settings window, navigate to the **IPv4 Settings** tab.  
    3. Change the "Method" dropdown menu from "Automatic (DHCP)" to **"Manual"**.  
    4. Click the **"Add"** button next to the Addresses list.  
    5. Enter the desired static **IP Address** (e.g., 192.168.1.50), the correct **Netmask** for your network (e.g., 255.255.255.0), and the **Gateway** address (usually the IP address of your router, e.g., 192.168.1.1).  
    6. Optionally, enter the IP addresses of **DNS servers** (e.g., 8.8.8.8 for Google DNS, or your router's IP). Multiple servers can be added, separated by commas.  
    7. Click **"Save"** to apply the static configuration. After saving, verify the new settings using Connection Information (1.1.3) and test connectivity (e.g., ping \<gateway\_ip\>). Additionally, confirm the IP address assignment directly from the command line using ip addr show eth0 (replace eth0 with your actual Ethernet interface name if different). If connectivity fails, double-check that the entered IP address, netmask, gateway, and DNS settings are correct and compatible with your network's configuration. Ensure the chosen static IP address is not already in use by another device on the network (IP conflict) and is within the valid range for your subnet.  
  * 1.2.3 Check MAC address, IP address  
    The method to verify the configured static IP address is the same as described in 1.1.3 (using the Network Manager icon \> Connection Information). Ensure the displayed IP address matches the static address you configured.  
* 1.3 Set up Manual (Static) WiFi Configuration  
  Similar to Ethernet, WiFi connections can also be configured with a static IP address if required.  
  1. Navigate to your WiFi connection settings. This is typically done via the **Network Manager icon** \> **Edit Connections...** \> Select the desired WiFi network name (SSID) from the list \> Click the **Gear icon** (Settings).  
  2. In the connection settings window, navigate to the **IPv4 Settings** tab.  
  3. Change the "Method" dropdown menu from "Automatic (DHCP)" to **"Manual"**.  
  4. Click the **"Add"** button and enter the desired static **IP Address**, **Netmask**, and **Gateway**, similar to the Ethernet setup described in 1.2.2.  
  5. Add **DNS servers** if needed.  
  6. Click **"Save"**. After saving and reconnecting, verify the settings using Connection Information (1.1.3) and test connectivity (e.g., ping \<gateway\_ip\>). If issues arise, confirm the IP, netmask, gateway, DNS, and WiFi password are correct.

**2\. Important Configuration**

Basic system maintenance is crucial for stability and access to software.

* 2.1 Update software list (Necessary update)  
  Before installing new software, it's essential to update the system's list of available packages from the configured software repositories. This ensures you can install the latest available versions and dependencies.  
  1. Ensure the device has an active internet connection (configured via WiFi or Ethernet as described in Section 1).  
  2. Open the **Terminal** or **Command Prompt** application. (The source image identified this as the third icon from the left at the top).  
  3. Execute the command to update the package lists:  
     sudo apt-get update

     This command downloads the latest package information from the repositories. It does not upgrade installed packages.  
     Tip: The method for opening the command window (Terminal) will not be repeated in subsequent sections.

CRITICAL WARNING:Please do not execute the command sudo apt-get upgrade or sudo apt full-upgrade. The original guide explicitly states that the system, in its current configuration, does not support this command. Running it may lead to system instability or cause other commands to become unusable, potentially requiring a complete system re-flash to resolve. Only update the package list (sudo apt-get update) and install specific packages as needed (sudo apt-get install \<package\_name\>).

**3\. System Debugging**

This section covers procedures for testing and debugging various hardware interfaces commonly found on development boards.

* 3.1 GPIO Debugging  
  GPIOs (General Purpose Input/Outputs) are digital pins that can be programmatically controlled to interact with external hardware like LEDs, buttons, sensors, and other peripherals.  
  The specific mapping of GPIO numbers to physical pins varies between boards and processors; consult your board's specification sheet or documentation for accurate pin numbering. The following example uses GPIO 218 (referenced as K1 in the source).  
  Execute the following commands sequentially in the terminal to control the GPIO:  
  \# Gain root privileges  
  sudo su  
  \# While \`sudo su\` provides root access, it's recommended to use \`sudo \<command\>\` for individual commands where possible and exit the root shell (\`exit\`) promptly after completing necessary tasks to minimize security risks.  
  \# Define the GPIO number to control  
  pio=218

  \# Export the GPIO to make it accessible via the sysfs interface  
  echo $pio \> /sys/class/gpio/export  
  \# Allow time for the system to create the GPIO directory in sysfs  
  sleep 1

  \# Set the GPIO direction to output  
  echo out \> /sys/class/gpio/gpio$pio/direction

  \# Set the GPIO value to 1 (High voltage level, e.g., 3.3V)  
  echo 1 \> /sys/class/gpio/gpio$pio/value  
  \# Check the physical pin with a multimeter or observe connected hardware (e.g., LED on)  
  sleep 1 \# Optional pause for observation

  \# Set the GPIO value to 0 (Low voltage level, e.g., 0V)  
  echo 0 \> /sys/class/gpio/gpio$pio/value  
  \# Check the physical pin or observe connected hardware (e.g., LED off)

  \# Optional: Release control of the GPIO when testing is complete  
  \# echo $pio \> /sys/class/gpio/unexport

  **Tip:** 218 represents the specific GPIO number for K1 in this example. echo 1 sets the output voltage high, while echo 0 sets it low. Always verify the expected voltage levels for your board and connected hardware to avoid damage. (The source image indicated this test was successful).  
* 3.2 Serial Port Debugging  
  Serial ports (like UARTs) provide a common method for low-level system console access, debugging output, and communication with external serial devices (GPS modules, microcontrollers, etc.).  
  First, install cutecom, a graphical serial terminal application:  
  sudo apt-get install cutecom

  When prompted Do you want to continue? \[Y/n\], type y and press Enter.  
  Once installed, launch the application:  
  sudo cutecom

  The CuteCom window will appear. Configure the connection:  
  1. Click **"Setting"**.  
  2. Select the correct **"Device"** (serial port node). Common names include /dev/ttyS0, /dev/ttyS1 for built-in UARTs, or /dev/ttyUSB0, /dev/ttyACM0 for USB-to-serial adapters. Consult your board documentation. If you are unsure of the device name, you can check available serial devices by listing the contents of the /dev directory (e.g., ls /dev/tty\*). If CuteCom fails to open the port, ensure you have the correct device name and necessary permissions. You might need to add your user to the dialout group (e.g., sudo usermod \-aG dialout $USER) and log out/in for the change to take effect.  
  3. Set the **"Baudrate"** (e.g., 115200, 9600), **"Data bits"** (usually 8), **"Parity"** (usually None), and **"Stop bits"** (usually 1\) to match the requirements of the device you are communicating with or the system console settings.  
  4. Click **"Open"** to establish the serial connection.  
  5. You can now type commands or text into the **"Input"** box at the bottom and press Enter to send data over the serial port. Received data will appear in the main window.  
* 3.3 CAN Port Debugging  
  CAN (Controller Area Network) bus is a robust protocol commonly used in automotive systems, industrial automation, and robotics for communication between microcontrollers and devices. This test involves setting up two CAN interfaces on the board and testing communication between them (likely a loopback test).  
  Preparation:  
  * Connect the board to a computer using an Android data cable via the board's **OTG (On-The-Go) port** to enable adb (Android Debug Bridge) communication. Ensure adb is installed and working on the host computer.  
  * Physically connect the board's two CAN ports (e.g., CAN0 and CAN1) using a **2-pin cable**, ensuring the **CAN High (H)** pin of one port is connected to the **H** pin of the other, and **CAN Low (L)** is connected to **L**. Check silkscreen labels on the board.  
  * Download the cansend and candump utility programs (if not already on the system) and place them in a known location on your computer, for example, D:\\can-utils. Adjust the paths in the commands below if you place them elsewhere.

  **Execution Steps:**

  1. Transfer Tools & Get Shell (Run on Host Computer):  
     Open a command prompt or shell window on your host computer and run:  
     \# Push the utilities to the device's /usr/bin directory  
     adb push D:\\can-utils\\cansend /usr/bin  
     adb push D:\\can-utils\\candump /usr/bin

     \# Start an adb shell session on the device  
     adb shell

  2. Set Permissions (Run inside adb shell on Device):  
     Execute these commands within the adb shell you just opened:  
     \# Set execute permissions for the utilities  
     chmod 755 /usr/bin/cansend  
     chmod 755 /usr/bin/candump

     (Source image indicated success)  
  3. Configure CAN Interfaces (Run inside adb shell on Device):  
     Continue within the same adb shell to configure can0 and can1:  
     \# Bring can0 down for configuration  
     ip link set can0 down  
     \# Set can0 type to CAN, specify bitrate (1Mbps), data bitrate (3Mbps), and enable CAN FD  
     \# bitrate: Standard CAN speed (before arbitration) \- 1,000,000 bits/sec  
     \# dbitrate: Data phase speed (after arbitration, only for CAN FD) \- 3,000,000 bits/sec  
     \# fd on: Enable CAN Flexible Data-Rate mode  
     ip link set can0 type can bitrate 1000000 dbitrate 3000000 fd on  
     \# These specific values (1Mbps arbitration phase, 3Mbps data phase) are examples; consult your device/network requirements for appropriate settings. CAN FD allows for faster data transmission after the initial arbitration phase compared to classic CAN.  
     \# Display detailed configuration for can0  
     ip \-details link show can0

     \# Bring can1 down for configuration  
     ip link set can1 down  
     \# Set can1 type to CAN with matching parameters  
     ip link set can1 type can bitrate 1000000 dbitrate 3000000 fd on  
     \# Display detailed configuration for can1  
     ip \-details link show can1

     \# Bring both interfaces up (ready for communication)  
     ip link set can0 up  
     ip link set can1 up

     (Source image indicated success)  
  4. Send Test Messages (Run inside adb shell on Device):  
     In the same adb shell, start sending test messages from can0 in a loop (this command will run continuously until interrupted with Ctrl+C):  
     \# Start sending test messages from can0 in a loop  
     while true; do  
     \# Send message: ID=0x123 (hex), Data=0xDEADBEAF (hex)  
     /usr/bin/cansend can0 123\#\#1DEADBEAF  
     \# Send message: ID=0x213 (hex), Data=0x11223344 (hex)  
     /usr/bin/cansend can0 213\#\#311223344  
     sleep 1 \# Wait 1 second between sends  
     done

  5. Monitor Reception (Run on Host Computer in a New Shell):  
     Open another command prompt or shell window on your host computer (while the sending loop runs in the first adb shell) and run:  
     \# Start a new adb shell session  
     adb shell

     \# Monitor incoming CAN messages on can1 within this \*new\* shell  
     /usr/bin/candump can1

     If you see messages appearing with IDs 123 and 213 and the corresponding data (DE AD BE AF, 11 22 33 44), continuously scrolling, the CAN interface loopback test is successful. (Source image showed continuous data, indicating success). Press Ctrl+C in both shells to stop the sending loop and monitoring when finished.  
* 3.4 Microphone Debugging  
  This procedure verifies the functionality of the onboard microphone or an externally connected one.  
  1. Navigate to the system's sound settings: Click the **Audio/Volume control icon** (usually in the system tray) \> Select **Sound Settings**.  
  2. Go to the **"Input Devices"** tab.  
  3. Locate the microphone device, often named something like **"rockchip, rk809-codec Stereo"** or "Internal Microphone". Ensure it is selected as the default input device.  
  4. Speak clearly into the microphone. Observe the input level meter (often shown as horizontal bars or stripes) next to the microphone name.  
  5. If the level meter actively moves or shows fluctuating bars corresponding to your voice, the microphone is detected and capturing audio correctly. If not, check physical connections, ensure the microphone is not muted (check settings in alsamixer or the sound settings GUI), verify drivers are loaded (dmesg), and confirm the correct device is selected.  
* 3.5 Camera Test  
  This tests the functionality of a connected USB camera or an onboard camera module.  
  1. Ensure the device is connected to the internet. Install the cheese webcam application using the terminal:  
     sudo apt-get install cheese

     When prompted Do you want to continue? \[Y/n\], type y and press Enter.  
  2. Launch the application:  
     \# Running with sudo might be needed if camera permissions are restrictive  
     cheese

     *(Try without sudo first. If it fails due to permissions, try sudo cheese)*.  
  3. The Cheese application window should open. If a connected camera is detected and working correctly, you should see the live video feed from the camera displayed within the window. If no image appears or an error occurs, check the camera's physical connection (USB port or ribbon cable seating), ensure necessary kernel drivers (like V4L2 \- Video4Linux2) are loaded (check dmesg output for camera-related messages), and verify camera detection using lsusb (for USB cameras) or board-specific commands. (Source image showed a successful camera feed).

**4\. Advanced Settings**

This section covers system customizations and remote access.

* 4.1 Rotate Screen  
  You can change the orientation of the display output, useful for portrait monitors or specific kiosk setups, using the xrandr utility via configuration files. This method makes the change persistent across reboots by modifying a session startup script. Prerequisite: A command-line text editor like vim or nano should be available.  
  1. Open a terminal and navigate to the Xsession configuration directory:  
     cd /etc/X11/Xsession.d/

  2. Edit the relevant session startup script using a text editor with root privileges (e.g., vim or nano):  
     sudo vim 55gnome-session\_gnomerc  
     \# OR, if you prefer nano:  
     \# sudo nano 55gnome-session\_gnomerc

     *(Note: The specific script name, like 55gnome-session\_gnomerc, might vary depending on the desktop environment and distribution. Check the contents of /etc/X11/Xsession.d/ if this file doesn't exist to find the appropriate script, often related to session setup).*  
  3. Inside the editor:  
     * Find an appropriate place to add the command, usually near the beginning of the script but after any initial setup.  
     * Add a line containing the desired xrandr command. Choose one:  
       * xrandr \-o left (Rotates the display 90 degrees counter-clockwise)  
       * xrandr \-o right (Rotates the display 90 degrees clockwise)  
       * xrandr \-o normal (Sets the display to the standard landscape orientation)  
       * xrandr \-o inverted (Rotates the display 180 degrees upside-down)  
     * Save the changes and exit the editor:  
       * For vim: Press Esc, type :wq, press Enter.  
       * For nano: Press Ctrl+O, press Enter to confirm filename, press Ctrl+X to exit.  
  4. Reboot the system. The display should now be rotated according to the command added upon login.  
     Tip: You can test xrandr commands directly in the terminal first (e.g., xrandr \-o left) to see the immediate effect before editing configuration files. The effect will reset on reboot unless added to a startup script.  
* 4.2 SSH Remote Login  
  SSH (Secure Shell) allows you to securely connect to the device's command line from another computer on the same network, enabling remote administration and file transfer.  
  1. Ensure the SSH server software is installed and running on the device. Check its status: sudo systemctl status ssh. If not installed, run: sudo apt-get update && sudo apt-get install openssh-server. If installed but not running, start and enable it: sudo systemctl enable ssh \--now.  
  2. Obtain the IP address of the device (using methods from Section 1).  
  3. From another computer on the same network, open a terminal (Linux/macOS) or an SSH client (like PuTTY or Windows Terminal with SSH on Windows).  
  4. Execute the SSH login command, replacing \<Device\_IP\> with the actual IP address found in step 2, and teamhd with the correct username on the device:  
     ssh teamhd@\<Device\_IP\>

  5. The first time you connect from a specific client machine, you will likely see a message about the authenticity of the host and its key fingerprint (e.g., ECDSA). Verify this fingerprint if you have a secure way to do so (though often impractical). Type yes and press Enter to trust the key and add it to your client's known\_hosts file.  
  6. Enter the password for the teamhd user when prompted and press Enter.  
  7. If authentication is successful, you will be logged into the device's command line remotely, indicated by the device's command prompt (e.g., teamhd@hostname:\~$).  
* 4.3 Wallpaper Change  
  You can customize the desktop appearance by changing the background wallpaper.  
  1. **Right-click** on an empty area of the desktop background.  
  2. From the context menu that appears, select **"Desktop Preferences"** or a similar option like "Change Desktop Background" or "Personalize".  
  3. In the preferences window, navigate to the **"Appearance"** or "Background" tab.  
  4. Locate the **"Wallpaper"** setting. Click the associated button, image preview box, or "Browse..." option to open a file selection dialog.  
  5. Navigate to the directory containing your desired image file (e.g., .jpg, .png). Select the image file and click **"Open"** or "Set".  
  6. The desktop background should update to display the selected image. You might also find options for how the image is positioned (e.g., "Stretch", "Tile", "Center", "Fill") which you can adjust to your preference.

**5\. Frequently Asked Questions**

This section addresses common issues and queries encountered during device operation.

* Q: Why does the system flashing display failure?  
  A: Flashing failures can occur if the device isn't in the correct bootloader mode required by the flashing tool. When using the tool, if it recognizes the device via ADB (indicating a normal boot), but flashing fails, you likely need to force it into a lower-level mode. Look for an "Advanced Settings" section in the flashing tool. Within that, find and activate an option to enter "Maskrom" mode (or a similar recovery/bootloader mode specific to the hardware). This usually involves specific button presses on the board while connecting power or USB. Once the tool indicates the device has reconnected successfully in Maskrom mode, navigate back to the "Download Image" or "Flash" tab and click "Execute" or "Start" to begin the flashing procedure again. Consult the flashing tool's documentation and board specifics for entering this mode.  
* Q: How to set screen brightness?  
  A: Screen brightness can often be controlled via the /sys filesystem interface provided by the kernel. First, identify the correct brightness control file:  
  \# List available backlight control directories  
  ls /sys/class/backlight/  
  \# (Assume the output is 'backlight\_device')

  Then, you can check the maximum and current brightness:  
  \# Check maximum brightness value  
  cat /sys/class/backlight/backlight\_device/max\_brightness  
  \# Check current brightness value  
  cat /sys/class/backlight/backlight\_device/actual\_brightness

  To set the brightness, replace backlight\_device with the actual directory name found above, and xx with a value between 0 and the maximum brightness:  
  \# Set the new brightness level (requires root privileges)  
  echo xx | sudo tee /sys/class/backlight/backlight\_device/brightness

  **Note:** Granting world-writable permissions (e.g., sudo chmod a+w .../brightness) is highly discouraged due to security risks. The sudo tee method shown above is safer as it doesn't permanently change permissions. Alternatively, check if your user belongs to a group (like video or plugdev) with write access (ls \-l /sys/class/backlight/backlight\_device/brightness), or use dedicated brightness control utilities (brightnessctl, xbacklight, or desktop environment settings) if available.  
* Q: How to get system logs?  
  A: The dmesg command displays kernel ring buffer messages (hardware detection, driver loading, errors since boot). Execute:  
  dmesg

  Pipe through less for easier viewing:  
  dmesg | less

  (Use arrow keys/PageUp/PageDown to scroll; type /search\_term to search; type q to quit less).  
  For persistent system logs (including application logs) on systems using systemd, use journalctl:  
  journalctl \# Show all logs (newest last)  
  journalctl \-b \# Show logs only from the current boot  
  journalctl \-f \# Follow new log messages in real-time  
  journalctl \-p err \-b \# Show only error messages (priority 3\) from the current boot

* Q: What is the method to check the 4G network status?  
  A: Ensure an active SIM card with a data plan is correctly inserted. After booting, look for a 4G/LTE or 5G network icon and signal strength bars in the system status area. This indicates successful registration on the cellular network. To confirm data connectivity, open a web browser and attempt to navigate to a known website (e.g., google.com). If issues occur, check signal, SIM status, and potentially APN settings via the Network Manager. For detailed command-line status, if ModemManager is installed, use mmcli:  
  mmcli \-L \# List available modems (shows modem index, e.g., 0\)  
  \# Replace 0 with the actual modem index if different  
  mmcli \-m 0 \# Show detailed status for modem 0

* Q: How to take a screenshot of the current screen?  
  A: Install the gnome-screenshot utility:  
  sudo apt install gnome-screenshot

  After installation, launch it via the application menu: **"Menu" \> "Accessories" \> "Screenshot"**. The tool offers options like capturing the whole screen, a specific window, or a selected area, often with an optional delay. Click **"Take Screenshot"** to capture, review the preview, and then click **"Save"** to choose a filename and location. Alternatively, many desktop environments have built-in screenshot capabilities, often mapped to the PrtScn key (full screen), Alt+PrtScn (active window), or Shift+PrtScn (select area).  
* Q: How to set up scheduled system shutdown?  
  A: Use the shutdown command with a time specification. To schedule a shutdown xxx minutes from the current time, execute:  
  sudo shutdown \+xxx

  Example: sudo shutdown \+120 schedules shutdown in 2 hours. A warning message is typically broadcast to logged-in users before shutdown. To schedule shutdown at a specific time (e.g., 11:00 PM), use HH:MM format: sudo shutdown 23:00. To shut down immediately, use sudo shutdown now or sudo shutdown \-h now (halt). To cancel a pending scheduled shutdown, execute sudo shutdown \-c.  
* Q: How to check the system version number?  
  A: To get detailed information about the installed Linux distribution, use:  
  lsb\_release \-a

  This typically shows Distributor ID, Description, Release, and Codename. To check the Linux kernel version specifically, use:  
  uname \-a

* Q: How to switch between HDMI audio and speaker audio?  
  A: Audio output selection is usually managed through the system's sound settings panel. Go to the Audio/Volume control icon \> Sound Settings \> Select the "Output Devices" tab. A list of detected audio outputs will be shown (e.g., "hdmi Stereo", "rk809-codec Stereo"). Click on the desired device name to select it as the active output. The currently active device is often indicated with a checkmark, highlighting, or by moving to the top of the list. Test audio playback after switching to confirm.  
  Tip: "rk809-codec Stereo" generally refers to the analog audio output provided by the onboard audio chip, typically connected to speakers or the headphone jack.  
* Q: What is the system restart command?  
  A: To properly reboot the system, closing applications and unmounting filesystems gracefully, execute:  
  sudo reboot

* Common Command-Line Errors Explained:  
  Understanding common errors helps in troubleshooting:  
  * **No such file or directory**: Indicates a typo in a filename or path, or the file/directory truly doesn't exist at that location. Use ls and pwd to verify names and current directory. Check for case sensitivity.  
  * **Permission denied**: The current user lacks the necessary read, write, or execute permissions for the file/directory or operation. Use sudo if the action requires root privileges. Check permissions with ls \-l. You might need to change ownership (chown) or permissions (chmod), or add your user to a specific group (usermod \-aG \<groupname\> $USER).  
  * **command not found**: The system cannot locate the executable file for the command entered. Double-check the command spelling (case-sensitive). Ensure the software package providing the command is installed (apt search \<command\>, dpkg \-S /path/to/command). Verify the command's directory is in the system's execution PATH (echo $PATH). Ensure correct spacing between the command and its arguments.

CRITICAL SYSTEM UPDATE REMINDER:  
As emphasized previously, avoid running sudo apt-get upgrade or sudo apt full-upgrade on this specific system configuration. The original documentation states this may cause system instability requiring a re-flash. Only use sudo apt-get update to refresh package lists and sudo apt-get install \<package\_name\> to install specific, required packages.  
**Troubleshooting Summary & Next Steps**

This guide provides a foundation for basic device operation and debugging. When encountering issues:

* **Verify Connections:** Double-check all physical connections (power, network cables, USB, peripherals).  
* **Check Commands:** Ensure commands are typed exactly as shown, paying attention to spelling, case, spacing, and paths.  
* **Consult Logs:** Use dmesg and journalctl (as described in the FAQ) to look for specific error messages related to the problem.  
* **Review Permissions:** Use ls \-l and consider if sudo is needed or if group membership (groups $USER) is required.  
* **Seek Further Information:** If the issue persists, consult the board's full technical manual, search online forums specific to the board or operating system, or check the manufacturer's support resources.

For more advanced features, specific hardware details, or application development, refer to the board's full technical manual, component datasheets, and relevant Linux/distribution documentation. Mastering these resources will help you fully leverage the capabilities of your device.