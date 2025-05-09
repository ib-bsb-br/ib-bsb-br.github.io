---
tags: [scratchpad]
info: aberto.
date: 2025-05-09
type: post
layout: post
published: true
slug: ratpoison-wm
title: 'Ratpoison WM'
---
### **Step 1: Install Ratpoison and Essential Tools**

First, update your package lists and install Ratpoison. The rpws (Ratpoison Workspace System) script is included with the ratpoison package in Debian Bullseye. Consider installing dmenu for application launching and a basic terminal like xterm or rxvt-unicode.  
`sudo apt update`  
`sudo apt upgrade`  
`sudo apt install ratpoison dmenu xterm # Or rxvt-unicode, etc.`  
`# Install other optional utilities you might find useful:`  
`# sudo apt install alsamixergui bpytop brightnessctl catfish dialog gmrun gsimplecal neofetch `  
`# python3-psutil unclutter viewnior xdotool scrot `  
`# fonts-dejavu fonts-terminus nitrogen picom # (nitrogen for wallpaper, picom for compositing)`

### **Step 2: Create a Ratpoison Session File for LightDM**

LightDM uses .desktop files located in /usr/share/xsessions/ to identify available sessions. Create one for Ratpoison:  
`sudo nano /usr/share/xsessions/ratpoison.desktop`

Add the following content:  
`[Desktop Entry]`  
`Version=1.0`  
`Encoding=UTF-8`  
`Name=Ratpoison`  
`Comment=Minimalist Tiling Window Manager`  
`Exec=ratpoison`  
`TryExec=ratpoison`  
`Icon=`  
`Type=XSession`

Save and close the file (e.g., Ctrl+X, then Y, then Enter in nano).

### **Step 3: Configure LightDM for Ratpoison Autologin**

To ensure LightDM launches Ratpoison for the autologin user, you need to update its configuration. Debian best practices suggest using configuration snippets in /etc/lightdm/lightdm.conf.d/. If you already have an autologin configuration file there (e.g., 50-autologin.conf), modify it. Otherwise, you can edit /etc/lightdm/lightdm.conf directly or create a new snippet.

1. **Edit or Create LightDM Configuration:** For example, to create/edit a dedicated snippet:  
   `sudo nano /etc/lightdm/lightdm.conf.d/60-autologin-ratpoison.conf`  
   Ensure the configuration specifies  linaro and sets autologin-session to ratpoison. The autologin-session value should match the filename of the .desktop file created in Step 2 (without the .desktop extension).  
   `[Seat:*]`  
   `autologin-user= linaro`  
   `autologin-user-timeout=0`  
   `autologin-session=ratpoison`  
   If you are editing an existing file that previously specified autologin-session=xfce (or similar), change it to ratpoison. Adding this line explicitly makes the autologin deterministic.  
2. **Note on Session Selection:** While LightDM can sometimes remember the last session selected at the greeter, for an autologin setup, explicitly defining autologin-session is the most reliable method.

### **Step 4: Configure Ratpoison (~/.ratpoisonrc)**

Create and configure the ~/.ratpoisonrc file in the home directory of the autologin user (i.e., /home/ linaro/.ratpoisonrc). This file controls Ratpoison’s behavior, keybindings, and startup applications.  
`# Ensure you are the user ‘ linaro’ or adjust path accordingly`  
`nano /home/ linaro/.ratpoisonrc`

Here’s a comprehensive example configuration:  
`# ~/.ratpoisonrc for  linaro`

`# — Appearance and Behavior —`  
`set fgcolor black`  
`set bgcolor silver`  
`set font -xos4-terminus-medium-r-normal-*-*-140-*-*-c-*-iso8859-1 # Adjust font as needed`  
`set border 0`  
`set barborder 0`  
`set barpadding 0 0`  
`set winname class`  
`set winfmt %n %s %c # Window list format: number, status, class`  
`set bargravity ne # Bar in the northeast corner`  
`set padding 0 0 0 0`

`startup_message off`  
`escape Super_L # Use Left Windows key as the escape/prefix key`  
`banish # Hide mouse cursor to a corner`

`# — Desktop Switching with rpws —`  
`# Initialize 6 virtual desktops. The ‘-k’ flag adds default keybindings (e.g., Alt+Fx).`  
`exec rpws init 6 -k`

`# Custom keybindings for rpws (these might override -k defaults or add to them)`  
`# Keybinding Legend: S=Super/Windows, C=Control, M=Alt, Shift=Shift`  
`# Example: Switch desktops with Super+number`  
`definekey top S-1 exec rpws 1`  
`definekey top S-2 exec rpws 2`  
`definekey top S-3 exec rpws 3`  
`definekey top S-4 exec rpws 4`  
`definekey top S-5 exec rpws 5`  
`definekey top S-6 exec rpws 6`

`# Example: Move current window to desktop N with Super+Shift+number`  
`definekey top S-Shift-1 exec rpws move1`  
`definekey top S-Shift-2 exec rpws move2`  
`definekey top S-Shift-3 exec rpws move3`  
`definekey top S-Shift-4 exec rpws move4`  
`definekey top S-Shift-5 exec rpws move5`  
`definekey top S-Shift-6 exec rpws move6`

`# — Startup Applications —`  
`# Uncomment to load .Xresources (useful for terminal colors, etc.)`  
`# exec xrdb -merge /home/ linaro/.Xresources`  
`exec xsetroot -cursor_name left_ptr # Set default cursor`  
`exec unclutter —timeout 5 —jitter 10 —fork # Hide mouse when idle`  
`# exec nitrogen —restore & # Wallpaper (if using nitrogen)`  
`# exec picom —experimental-backends & # Compositor (if desired)`  
`# exec nm-applet & # Network manager applet (if needed and not handled otherwise)`  
`# exec volumeicon & # Volume control icon (if needed)`

`# — Custom Keybindings (Ratpoison prefix key (Super_L) + binding) —`  
`# Launch terminal`  
`bind c exec x-terminal-emulator # System default. # Or specify: ‘rxvt-unicode’, ‘xterm’`  
`# Launch application launcher (dmenu)`  
`bind space exec dmenu_run -fn ‘-xos4-terminus-medium-r-normal-*-*-140-*-*-c-*-iso8859-1’ -nb black -nf silver -sb silver -sf black`

`# Window management`  
`bind Tab next # Focus next window`  
`bind Shift-Tab prev # Focus previous window (Note: Shift-Tab might be M-ISO_Left_Tab depending on keysyms)`  
`# definekey top M-ISO_Left_Tab prev # More reliable for Shift+Tab`  
`bind k kill # Kill current window (SIGKILL)`  
`bind r remove # Close current window (nicer, sends SIGTERM)`  
`bind s hsplit # Horizontal split`  
`bind v vsplit # Vertical split`  
`bind colon eval # Execute Ratpoison command interactively`

`# Resize (after pressing prefix + R, then use h,j,k,l or arrows)`  
`bind R resize`

`# Example application launchers`  
`bind F exec firefox-esr # Or your preferred browser`  
`bind T exec thunar # Or another file manager if installed`

`# Quit Ratpoison (ends the session)`  
`definekey top C-M-Delete exec ratpoison -c “quit”`  
`# This will typically return you to the LightDM greeter or trigger system shutdown/reboot`  
`# depending on how the system handles ended sessions.`

### **Step 5: Configure User-Specific X Settings (~/.xsessionrc)**

The ~/.xsessionrc file (in /home/ linaro/) is executed when your X session starts via LightDM. It’s useful for setting environment variables or running commands like xrandr before Ratpoison loads. This file must be executable.  
`nano /home/ linaro/.xsessionrc`

Add your configurations, for example:  
`#!/bin/sh`  
`# ~/.xsessionrc for  linaro`

`# Exit immediately if a command exits with a non-zero status.`  
`set -e`

`# Example: Set screen resolution with xrandr`  
`# xrandr —output DP-1 —mode 1920x1080 —rate 60`  
`# xrandr —output HDMI-1 —primary —mode 2560x1080 —above DP-1`

`# Example: Start a key remapper or other background utility`  
`# xmodmap /home/ linaro/.Xmodmap`

`# Example: Set an environment variable`  
`# export QT_QPA_PLATFORMTHEME=qt5ct`

Make it executable:  
`chmod +x /home/ linaro/.xsessionrc`

### **Step 6: (Optional but Recommended) Remove XFCE4**

If you no longer need XFCE4 and want to free up disk space, you can remove its packages. **Be cautious** and review the packages to be removed before confirming.  
`# Identify XFCE4 meta-packages and components`  
`sudo apt purge xfce4 xfce4-goodies libxfce4ui-utils xfce4-panel xfce4-session xfce4-settings xfconf xfdesktop4 xfwm4 thunar mousepad parole ristretto`  
`# This list might need adjustment based on your specific XFCE4 installation.`  
`# Always review the list of packages apt proposes to remove.`  
`sudo apt autoremove`  
`sudo apt clean`

### **Step 7: Verify the Setup**

Reboot your system or restart LightDM to apply changes:  
`sudo systemctl restart lightdm`

Your system should automatically log in  linaro directly into a Ratpoison session.  
**Troubleshooting:**

* LightDM logs: /var/log/lightdm/lightdm.log and seat-specific logs (e.g., /var/log/lightdm/seat0-greeter.log).  
* Xorg logs: ~/.local/share/xorg/Xorg.0.log (for user sessions) or /var/log/Xorg.0.log.  
* Session errors: Check ~/.xsession-errors (in /home/ linaro/) for issues from ~/.xsessionrc or session startup.

### **Alternative: Manual Start with startx (If Not Using LightDM)**

If you choose not to use LightDM or wish to start Ratpoison manually from a TTY (console login):

1. Ensure xinit is installed: sudo apt install xinit.  
2. Create or edit ~/.xinitrc (in /home/ linaro/.xinitrc):  
   `nano /home/ linaro/.xinitrc`  
   Add:  
   `#!/bin/sh`  
   `# ~/.xinitrc for  linaro`

   `# Source user-specific X settings if desired (contents similar to .xsessionrc)`  
   `# if [ -f /home/ linaro/.xprofile_custom ]; then`  
   `#  . /home/ linaro/.xprofile_custom`  
   `# fi`  
   `# For xrandr, etc., you might call them directly here or source .xsessionrc`  
   `# if [ -f /home/ linaro/.xsessionrc ]; then`  
   `#   . /home/ linaro/.xsessionrc`  
   `# fi`

   `exec ratpoison`

3. Make it executable: chmod +x /home/ linaro/.xinitrc.  
4. Log in to a TTY as  linaro and run startx.

This approach bypasses LightDM. The primary focus of this guide is the LightDM autologin method.