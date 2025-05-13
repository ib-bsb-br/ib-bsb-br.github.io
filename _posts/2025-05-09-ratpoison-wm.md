---
tags: [aid>linux>software>dotfile]
info: aberto.
date: 2025-05-09
type: post
layout: post
published: true
slug: ratpoison-wm
title: 'Ratpoison WM'
comment: 'https://ozi-blog.ru/nastroyka-pereklyucheniya-rabochih-stolov-v-ratpoison/'
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
set winname title
set winliststyle column
set wingravity n
set winfmt "%n: %t (%c)"
set waitcursor 1
set transgravity center
set padding 0 0 0 24
set inputwidth 600
set historysize 1000
set gravity center
set font "Intel One Mono:size=13"
set border 0
set bgcolor silver
set barpadding 4 4
set bargravity c
set barborder 0

definekey top M-Tab next
definekey top M-ISO_Left_Tab prev

exec rpws init 9
exec rpbar
exec xsetroot -bitmap /home/linaro/Desktop/02-media/pics/wallpaper1.xbm -bg "#073642" -fg "#345345"
exec xrdb -merge /home/linaro/.Xresources
exec xfce4-power-manager
exec unclutter --timeout 2 --jitter 5
exec nm-applet
exec brightnessctl s 7
exec /usr/bin/rpws restore /home/linaro/Desktop/01-document/dotfiles/rpws_layouts.dmp

startup_message on
escape Super_L
banish
unmanage rpbar

addhook titlechanged exec rpbarsend
addhook switchwin exec rpbarsend
addhook switchgroup exec rpbarsend
addhook switchframe exec rpbarsend
addhook newwindow exec rpbarsend
addhook deletewindow exec rpbarsend

bind w exec thorium-browser
bind v exec paste_clipboard_from_file.sh
bind Up focusup
bind u undo
bind Tab focus 
bind t exec pcmanfm-qt --daemon-mode
bind space exec dmenu_run
bind Right focusright
bind Return exec x-terminal-emulator
bind r resize
bind q delete
bind k kill
bind Print exec xfce4-screenshooter
bind Page_Up exec rpws prev
bind Page_Down exec rpws next
bind minus vsplit
bind Left focusleft
bind KP_Separator exec xdotool key quotedbl key quotedbl key quotedbl
bind KP_9 exec rpws 9
bind KP_8 exec rpws 8
bind KP_7 exec rpws 7
bind KP_6 exec rpws 6
bind KP_5 exec rpws 5
bind KP_4 exec rpws 4
bind KP_3 exec rpws 3
bind KP_2 exec rpws 2
bind KP_1 exec rpws 1
bind KP_0 exec xdotool key apostrophe key apostrophe key apostrophe
bind i exec viewnior
bind g exec gsimplecal
bind F8 exec flatpak run io.github.zaps166.QMPlay2
bind F7 exec flatpak run com.github.ryonakano.reco
bind F6 exec flatpak run com.strlen.TreeSheets
bind F5 exec flatpak run com.github.tenderowl.frog
bind F4 exec flatpak run org.telegram.desktop
bind F1 exec thermal.sh
bind f only
bind Escape exec /usr/bin/rpws dump /home/linaro/Desktop/01-document/dotfiles/rpws_layouts.dmp
bind equal hsplit
bind e exec xnedit
bind Down focusdown
bind c exec write_clipboard_to_file.sh
bind BackSpace next
bind h exec x-terminal-emulator -e bpytop
bind apostrophe colon exec x-terminal-emulator -e 
bind 9 exec rpws 9
bind 8 exec rpws 8
bind 7 exec rpws 7
bind 6 exec rpws 6
bind 5 exec rpws 5
bind 4 exec rpws 4
bind 3 exec rpws 3
bind 2 exec rpws 2
bind 1 exec rpws 1
bind 0 remove
bind s-w exec x-terminal-emulator -e nm-connection-editor
bind s-Up exchangeup
bind s-u redo
bind s-Tab nextscreen
bind s-t exec sudo pcmanfm-qt
bind s-space exec ratpoison -c "select `ratpoison -c "windows %n: %c" | dmenu | awk '{print $1}'`"
bind s-Right exchangeright
bind s-Return exec sudo x-terminal-emulator
bind s-q abort
bind s-Print exec scrot -s -e 'xclip -selection clipboard -t image/png -i $f && rm $f'
bind s-Page_Up exec rpws movenext
bind s-Page_Down exec rpws moveprev
bind s-minus exec amixer set Master 5%-
bind s-Left exchangeleft
bind s-KP_9 exec rpws move9
bind s-KP_8 exec rpws move8
bind s-KP_7 exec rpws move7
bind s-KP_6 exec rpws move6
bind s-KP_5 exec rpws move5
bind s-KP_4 exec rpws move4
bind s-KP_3 exec rpws move3
bind s-KP_2 exec rpws move2
bind s-KP_1 exec rpws move1
bind s-g exec galculator
bind s-F1 exec reverse-thermal.sh
bind s-Escape exec /usr/bin/rpws restore /home/linaro/Desktop/01-document/dotfiles/rpws_layouts.dmp
bind s-equal exec amixer set Master 5%+
bind s-e exec xnc
bind s-Down exchangedown
bind s-BackSpace prev
bind s-b exec vorta
bind b exec sudo timeshift --create --comments "Before making changes"
bind s-apostrophe colon exec x-terminal-emulator -e sudo 
bind s-a title
bind s-9 exec rpws move9
bind s-8 exec rpws move8
bind s-7 exec rpws move7
bind s-6 exec rpws move6
bind s-5 exec rpws move5
bind s-4 exec rpws move4
bind s-3 exec rpws move3
bind s-2 exec rpws move2
bind s-1 exec rpws move1
bind s-0 exec amixer set Master toggle
{% endcodeblock %}

#### ~/.rpbar.ini

```
[program]
# Window name for rpbar
win_name = rpbar

# Path for the communication socket with rpbarsend
# /tmp/ is generally standard and should work on Debian.
socket_path = /tmp/rpbarsocket

# Separator for program title (likely for ratpoison integration)
sep = $)@=

# Buffer size for communication with ratpoison
bufsize = 2048

# Timeout in seconds for communication
timeout_s = 5

[display]
# Whether rpbar is on the top (1) or bottom (0) of the screen
top = 0

# The Xorg screen (monitor) to display the bar on.
# '0' is typically the primary monitor. Adjust if you have multiple monitors
# and want it on a different one (e.g., 1 for secondary).
# Use `xrandr` to list screens if unsure.
screen = 0 ; Defaulting to primary screen, adjust if needed.

# Padding around the top/bottom of the text within the bar
padding = 4

# Left/right padding for elements like buttons
button_margin = 10

# Padding specifically for the status bar text area
status_padding = 30

# Font string for the bar (e.g., "Font Family Name:size=POINT_SIZE").
# CRITICAL: Ensure "Intel One Mono" is installed on your Debian Bullseye system.
# If not, replace with an available font (e.g., "DejaVu Sans Mono:size=10", "Liberation Mono:size=10", "Monospace:size=10").
# Check availability with `fc-list | grep "Your Font Name"`
font_str = Intel One Mono:size=13 ; ### VERIFY THIS FONT IS INSTALLED OR CHANGE IT ###

[color]
bordercolor = #d7d7d7
bgcolor = #353535
fgcolor = #d7d7d7
mainbgcolor = #d4ccb9
mainfgcolor = #45363b
statusbgcolor = #d7d7d7
statusfgcolor = #353535
```

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
#### Setting Up `rpws` for Desktop Switching

To configure desktop switching with `rpws`, you will need to add the following line to your `~/.ratpoisonrc` file:

```sh
exec rpws init N -k
```

Where `N` is the number of desktops you wish to create (at least 2). The `-k` flag is optional and is only necessary if you want to use predefined keybindings for switching desktops and managing windows.

When `rpws` is initialized, it will create `N` desktops, and by default, it assigns the following keybindings:

- `Alt+F(N)` - Switch to desktop `N` (e.g., `Alt+F1` switches to the first desktop).
- `Ctrl+Alt+Right` - Go to the next desktop.
- `Ctrl+Alt+Left` - Go to the previous desktop.
- `Ctrl+Alt+Windows+F(N)` - Move the current window to desktop `N`.
- `Ctrl+Alt+>` - Move the window to the next desktop.
- `Ctrl+Alt+<` - Move the window to the previous desktop.

However, you may find these keybindings inconvenient or difficult to use. In that case, you can customize them to suit your preferences.

#### Customizing `rpws` Hotkeys

To customize the keybindings, add the following lines to your `~/.ratpoisonrc` file:

```sh
# Initialize 6 desktops
exec rpws init 6

# Switch desktops with the Windows+digit combination
definekey top s-1 exec rpws 1
definekey top s-2 exec rpws 2
definekey top s-3 exec rpws 3
definekey top s-4 exec rpws 4
definekey top s-5 exec rpws 5
definekey top s-6 exec rpws 6

# Move windows to desktops using Windows+F(N)
definekey top s-F1 exec rpws move1
definekey top s-F2 exec rpws move2
definekey top s-F3 exec rpws move3
definekey top s-F4 exec rpws move4
definekey top s-F5 exec rpws move5
definekey top s-F6 exec rpws move6

# Move between desktops with Windows+Right/Left
definekey top s-Right exec rpws next
definekey top s-Left exec rpws prev

# Move window to next/previous desktop using Windows+Up/Down
definekey top s-Up exec rpws movenext
definekey top s-Down exec rpws moveprev
```

##### Keybinding Legend:
- `C` stands for **Ctrl**
- `S` stands for the **Windows** key
- `M` stands for **Alt**

For example, `C-S-M-q` represents pressing `Ctrl + Windows + Alt + q` in sequence.

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
