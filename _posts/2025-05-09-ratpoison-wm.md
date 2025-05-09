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
   Ensure the configuration specifies linaro and sets autologin-session to ratpoison. The autologin-session value should match the filename of the .desktop file created in Step 2 (without the .desktop extension).  
   `[Seat:*]`  
   `autologin-user=linaro`  
   `autologin-user-timeout=0`  
   `autologin-session=ratpoison`  
   If you are editing an existing file that previously specified autologin-session=xfce (or similar), change it to ratpoison. Adding this line explicitly makes the autologin deterministic.  
2. **Note on Session Selection:** While LightDM can sometimes remember the last session selected at the greeter, for an autologin setup, explicitly defining autologin-session is the most reliable method.

### **Step 4: Configure Ratpoison (~/.ratpoisonrc)**

Create and configure the ~/.ratpoisonrc file in the home directory of the autologin user (i.e., /home/linaro/.ratpoisonrc). This file controls Ratpoison’s behavior, keybindings, and startup applications.  
`# Ensure you are the user ‘linaro’ or adjust path accordingly`  
`nano /home/linaro/.ratpoisonrc`

Here’s a comprehensive example configuration:  
`# ~/.ratpoisonrc for linaro`
{% codeblock %}
set fgcolor black
set bgcolor silver
set framesels 123456789
set font "Intel One Mono:size=13"
set border 0
set barborder 0
set barpadding 0 0
set winname title
set winfmt %n %s %c
set winliststyle column
set wingravity n 
set gravity center 
set transgravity center
set bargravity ne
set waitcursor 1
set padding 0 0 0 24
# leave space for bars, 24 for desktop 39 for laptop

startup_message off
escape Super_L
banish
unmanage rpbar

exec xrdb -merge /home/linaro/.Xresources
exec brightnessctl s 7
exec unclutter
exec rpws init 9 -k
exec rpbar
exec nm-applet &

addhook switchwin exec rpbarsend
addhook switchframe exec rpbarsend
addhook switchgroup exec rpbarsend
addhook deletewindow exec rpbarsend
addhook titlechanged exec rpbarsend
addhook newwindow exec rpbarsend

definekey top M-Tab next
definekey top M-ISO_Left_Tab prev
definekey top S-Shift-1 exec rpws move1
definekey top S-Shift-2 exec rpws move2
definekey top S-Shift-3 exec rpws move3
definekey top S-Shift-4 exec rpws move4
definekey top S-Shift-5 exec rpws move5
definekey top S-Shift-6 exec rpws move6

# bind apostrophe exec zutty -saveLines 50000 -border 0 -font 10x20
# bind s-apostrophe exec zutty -saveLines 50000 -border 0 -font 12x24
# bind i exec zutty -saveLines 50000 -border 0 -font 10x20 -e wifish
# bind b exec zutty -saveLines 50000 -border 0 -font 10x20 -e bpytop
bind apostrophe exec x-terminal-emulator
bind s-apostrophe eval
bind i exec x-terminal-emulator -e wifish
bind b exec x-terminal-emulator -e bpytop
bind F1 only
bind F2 hsplit
bind F3 vsplit
bind F4 resize
bind e exec xnedit
bind s-e exec xnc
bind f exec thorium-browser
bind h exec menu
bind g exec gsimplecal
bind c exec write_clipboard_to_file.sh
bind s-c exec galculator
bind p exec xfce4-screenshooter
bind s-p exec scrot -s -e 'xclip -selection clipboard -t image/png -i $f && rm $f'
bind Prior exec thermal.sh
bind Next exec reverse-thermal.sh
bind r remove
bind t exec pcmanfm-qt --daemon-mode
bind v exec paste_clipboard_from_file.sh
bind s-v exec viewnior
bind w exec ratpoison -c "select `ratpoison -c "windows" | dmenu | awk '{print $1}'`"
bind z nextscreen
bind s-b exec vorta
bind s-k kill
bind s-x fselect
bind BackSpace undo
bind s-BackSpace redo
bind s-Down exchangedown
bind s-Up exchangeup
bind s-Left exchangeleft
bind s-Right exchangeright
bind s-Return prev
bind s-Tab focuslast
bind Tab focus
bind Escape abort
bind space exec dmenu_run
bind F9 exec amixer set Master 0
bind F10 exec amixer set Master 25%-
bind F11 exec amixer set Master 25%+
bind KP_0 exec xdotool key apostrophe key apostrophe key apostrophe
bind KP_Separator exec xdotool key quotedbl key quotedbl key quotedbl
bind KP_1 exec rpws 1
bind KP_2 exec rpws 2
bind KP_3 exec rpws 3
bind KP_4 exec rpws 4
bind KP_5 exec rpws 5
bind KP_6 exec rpws 6
bind KP_7 exec rpws 7
bind KP_8 exec rpws 8
bind KP_9 exec rpws 9
bind Home exec flatpak run com.github.tenderowl.frog
bind s-1 exec flatpak run org.telegram.desktop
bind s-2 exec flatpak run com.strlen.TreeSheets
bind s-3 exec flatpak run io.github.zaps166.QMPlay2
bind s-4 exec flatpak run com.github.ryonakano.reco
{% endcodeblock %}

#### .Xresources

```
! +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
! title      Nord XResources                                    +
! project    nord-xresources                                    +
! version    0.1.0                                              +
! repository https://github.com/arcticicestudio/nord-xresources +
! author     Arctic Ice Studio                                  +
! email      development@arcticicestudio.com                    +
! copyright  Copyright (C) 2016                                 +
! +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#define nord0 #2E3440
#define nord1 #3B4252
#define nord2 #434C5E
#define nord3 #4C566A
#define nord4 #D8DEE9
#define nord5 #E5E9F0
#define nord6 #ECEFF4
#define nord7 #8FBCBB
#define nord8 #88C0D0
#define nord9 #81A1C1
#define nord10 #5E81AC
#define nord11 #BF616A
#define nord12 #D08770
#define nord13 #EBCB8B
#define nord14 #A3BE8C
#define nord15 #B48EAD

*.foreground:   nord4
*.background:   nord0
*.cursorColor:  nord4
*fading: 0
*fadeColor: nord3

*.color0: nord1
*.color1: nord11
*.color2: nord14
*.color3: nord13
*.color4: nord9
*.color5: nord15
*.color6: nord8
*.color7: nord5
*.color8: nord3
*.color9: nord11
*.color10: nord14
*.color11: nord13
*.color12: nord9
*.color13: nord15
*.color14: nord7
*.color15: nord6
```

### **Step 5: Configure User-Specific X Settings (~/.xsessionrc)**

The ~/.xsessionrc file (in /home/linaro/) is executed when your X session starts via LightDM. It’s useful for setting environment variables or running commands like xrandr before Ratpoison loads. This file must be executable.  
`nano /home/linaro/.xsessionrc`

Add your configurations, for example:  
{% codeblock %}
#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
# set -e

# Optional: Uncomment to log script execution for debugging
LOG_FILE=~/xsessionrc_debug.log
echo "$(date): .xsessionrc started" >> "$LOG_FILE"

# Define custom mode for DP-1 (1152x864 @ 60Hz)
# Ensure standard spaces are used in the modeline string.
# Modeline: "1152x864_60.00" 81.75 1152 1216 1336 1520 864 867 871 897 -hsync +vsync
xrandr --newmode "1152x864_60.00" 81.75 1152 1216 1336 1520 864 867 871 897 -hsync +vsync # 2>&1 | tee -a "$LOG_FILE"

# Define custom mode for HDMI-1 (2560x1080 @ 60Hz)
# Modeline: "2560x1080_60.00" 230.00 2560 2720 2992 3424 1080 1083 1093 1120 -hsync +vsync
xrandr --newmode "2560x1080_60.00" 230.00 2560 2720 2992 3424 1080 1083 1093 1120 -hsync +vsync # 2>&1 | tee -a "$LOG_FILE"

# Add the new modes to the respective outputs
xrandr --addmode DP-1 "1152x864_60.00" # 2>&1 | tee -a "$LOG_FILE"
xrandr --addmode HDMI-1 "2560x1080_60.00" # 2>&1 | tee -a "$LOG_FILE"

# Apply the modes and set the layout.
# NOTE: The command below sets DP-1 as primary.
# Your comment "# makes HDMI-1 primary" conflicts with this.
# Adjust --primary flag if HDMI-1 should be the primary display.
xrandr \
    --output DP-1 --primary --mode "1152x864_60.00" --below HDMI-1 \
    --output HDMI-1 --mode "2560x1080_60.00" # 2>&1 | tee -a "$LOG_FILE"

# Example: Start a key remapper or other background utility
# xmodmap /home/ linaro/.Xmodmap

# Example: Set an environment variable
# export QT_QPA_PLATFORMTHEME=qt5ct

echo "$(date): .xsessionrc finished successfully" >> "$LOG_FILE"
{% endcodeblock %}

Make it executable:  
`chmod +x /home/linaro/.xsessionrc`

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

Your system should automatically log in linaro directly into a Ratpoison session.  
**Troubleshooting:**

* LightDM logs: /var/log/lightdm/lightdm.log and seat-specific logs (e.g., /var/log/lightdm/seat0-greeter.log).  
* Xorg logs: ~/.local/share/xorg/Xorg.0.log (for user sessions) or /var/log/Xorg.0.log.  
* Session errors: Check ~/.xsession-errors (in /home/linaro/) for issues from ~/.xsessionrc or session startup.

### **Alternative: Manual Start with startx (If Not Using LightDM)**

If you choose not to use LightDM or wish to start Ratpoison manually from a TTY (console login):

1. Ensure xinit is installed: sudo apt install xinit.  
2. Create or edit ~/.xinitrc (in /home/linaro/.xinitrc):  
   `nano /home/linaro/.xinitrc`  
   Add:  

```
#!/bin/sh
# ~/.xinitrc for linaro

# Source user-specific X settings if desired (contents similar to .xsessionrc)
# if [ -f /home/linaro/.xprofile_custom ]; then
#  . /home/linaro/.xprofile_custom
# fi
# For xrandr, etc., you might call them directly here or source .xsessionrc
if [ -f /home/linaro/.xsessionrc ]; then
  . /home/linaro/.xsessionrc
fi

exec ratpoison
```

4. Make it executable: `chmod +x /home/linaro/.xinitrc`
5. Log in to a TTY as linaro and run startx.

This approach bypasses LightDM. The primary focus of this guide is the LightDM autologin method.
