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
# ==============================================================================
# Ratpoison Configuration File - Reorganized for Intuitive Use
# User: linaro (Paths and specific apps based on original config)
# ==============================================================================

# ------------------------------------------------------------------------------
# Core Settings
# ------------------------------------------------------------------------------
escape Super_L          # Use Super (Windows/Command key) as the prefix
startup_message off
banish                  # Hide mouse cursor on startup to a corner
set waitcursor 1        # Show wait cursor for slow-starting apps

# Appearance
set fgcolor black
set bgcolor silver
set font "Intel One Mono:size=13" # User preference
set border 0                      # No window borders
set barborder 0                   # No border for ratpoison's internal message/input bar
set barpadding 4 4                # Padding for ratpoison's internal bar
set padding 0 0 0 24           # Screen padding (leaves space for external bars like rpbar)

# Window & Frame Behavior
set framesels 123456789           # For selecting frames with prefix + number (e.g., Super+1 to focus frame 1)
set winname title                 # Display window title in frame name
set winfmt "%n: %t (%c)"          # Window format for display: "number: title (class)"
                                  # This is more informative than the original "%n %s %c".
set winliststyle column           # Display window list in a column
set wingravity n                  # New windows gravitate North (top)
set gravity center                # Default frame placement for new windows
set transgravity center           # Transient window (dialogs) placement
set bargravity c                  # Ratpoison's internal message bar gravity (center)
set inputwidth 600                # Width of ratpoison's input box
set historysize 1000              # Command history size for ratpoison's input box

# If your rpbar is an external window that manages its own position (common),
# unmanaging it prevents ratpoison from trying to tile it.
unmanage rpbar

# ------------------------------------------------------------------------------
# Startup Applications & Services
# ------------------------------------------------------------------------------
# Initialize Ratpoison Windowing System (rpws) for 9 workspaces.
# The -k flag (which creates default rpws keybindings) is omitted because
# we are defining all workspace-related keybindings manually for a cohesive setup.
exec rpws init 9

# Restore previous rpws window layouts if a dump file exists.
exec /usr/bin/rpws restore /home/linaro/Desktop/01-document/dotfiles/rpws_layouts.dmp

# Set root window properties (wallpaper and background color)
exec xsetroot -bitmap /home/linaro/Desktop/02-media/pics/wallpaper1.xbm -bg "#073642" -fg "#345345"

# Merge Xresources (for application theming, fonts, etc.)
exec xrdb -merge /home/linaro/.Xresources

# Set initial screen brightness (user-specific command)
exec brightnessctl s 7

# Hide mouse cursor after a period of inactivity
exec unclutter --timeout 2 --jitter 5 # Adjust timeout and jitter as needed

# NetworkManager applet for managing network connections
exec nm-applet

# Start your status bar (rpbar)
exec rpbar

# ------------------------------------------------------------------------------
# Hooks for rpbar / Status Bar Updates
# ------------------------------------------------------------------------------
# Your original configuration had multiple ways of notifying rpbar.
# It's very likely that ONLY ONE of the `exec` commands per hook event below
# is necessary for your specific rpbar setup.
#
# METHOD:
# 1. For each hook event (newwindow, deletewindow, etc.), there are three common methods listed.
# 2. UNCOMMENT ONLY ONE `addhook ... exec ...` line for each event.
# 3. Start with one method (e.g., `rpbarsend` for all events if you have that script).
# 4. Restart ratpoison (or log out/in) and test if rpbar updates correctly.
# 5. If not, comment out your first choice and try another one for that event.
#
# Common methods:
#   - `exec rpbarsend`: Calls a dedicated script you might have.
#   - `exec echo r > /tmp/rpbarfifo`: Sends a simple 'refresh' signal to a named pipe (FIFO).
#   - `exec ratpoison -c "windows <format>" > /tmp/rpbarfifo`: Sends detailed window info to a FIFO.
#     (Original format was "%n %t%s". If using this, adjust format as needed.)

# --- newwindow ---
# Choose ONE for newwindow event:
addhook newwindow exec rpbarsend                                    # Option 1
# addhook newwindow exec echo r > /tmp/rpbarfifo                      # Option 2
# addhook newwindow exec ratpoison -c "windows %n %t%s" > /tmp/rpbarfifo # Option 3 (original format)

# --- deletewindow ---
# Choose ONE for deletewindow event:
addhook deletewindow exec rpbarsend                                 # Option 1
# addhook deletewindow exec echo r > /tmp/rpbarfifo                   # Option 2
# addhook deletewindow exec ratpoison -c "windows %n %t%s" > /tmp/rpbarfifo # Option 3

# --- switchwin (window focus change) ---
# Choose ONE for switchwin event:
addhook switchwin exec rpbarsend                                    # Option 1
# addhook switchwin exec echo r > /tmp/rpbarfifo                      # Option 2
# addhook switchwin exec ratpoison -c "windows %n %t%s" > /tmp/rpbarfifo # Option 3

# --- switchframe (frame focus change) ---
# Choose ONE for switchframe event:
addhook switchframe exec rpbarsend                                  # Option 1
# addhook switchframe exec echo r > /tmp/rpbarfifo                    # Option 2
# addhook switchframe exec ratpoison -c "windows %n %t%s" > /tmp/rpbarfifo # Option 3

# --- switchgroup (workspace change, if rpbar uses this) ---
# Choose ONE for switchgroup event:
addhook switchgroup exec rpbarsend                                  # Option 1
# addhook switchgroup exec echo r > /tmp/rpbarfifo                    # Option 2
# addhook switchgroup exec ratpoison -c "windows %n %t%s" > /tmp/rpbarfifo # Option 3

# --- titlechanged ---
# Choose ONE for titlechanged event:
addhook titlechanged exec rpbarsend                                 # Option 1
# addhook titlechanged exec echo r > /tmp/rpbarfifo                   # Option 2
# addhook titlechanged exec ratpoison -c "windows %n %t%s" > /tmp/rpbarfifo # Option 3

# This hook updates ratpoison's *internal* window list string,
# often used by commands like `fselect` or if ratpoison itself displays status.
# The format should match `set winfmt` if used for similar display purposes.
# addhook switchwin windows "%n: %t (%c)"


# ==============================================================================
# Keybindings (All 'bind' commands are prefixed by 'Super_L' unless 'definekey top')
# ==============================================================================

# ------------------------------------------------------------------------------
# I. Essential Applications & Actions
# ------------------------------------------------------------------------------
# bind Return exec zutty -saveLines 50000 -border 0 -font 10x20orINTEL
# bind i exec zutty -saveLines 50000 -border 0 -font 10x20 -e wifish
# bind b exec zutty -saveLines 50000 -border 0 -font 10x20 -e bpytop
bind Return exec x-terminal-emulator      # Super + Enter: Launch terminal (common standard)
bind s-Return exec colon exec x-terminal-emulator -e 
bind space exec dmenu_run                 # Original: bind space exec dmenu_run (Super+Space is also common)
bind s-space exec ratpoison -c "select \"$(ratpoison -c 'windows %n: %t (%c)' | dmenu -p 'Window:')\""
bind w exec thorium-browser               # Super + W: Launch Web browser
bind e exec pcmanfm-qt --daemon-mode      # Super + E: Launch File Manager (E for Explorer-like)

# ------------------------------------------------------------------------------
# II. Frame & Window Management (within current workspace)
# ------------------------------------------------------------------------------
# Killing windows / Removing frames
bind q kill                               # Super + Q: Kill current window (Q for Quit/Kill)
bind s-q abort                            # Abort current ratpoison command sequence

# Focusing Windows (within current frame) & Frames
bind Tab next                             # Super + Tab: Focus next window in current frame
bind s-Tab prev                       # Focus previous window in current frame

# Focusing Frames (Arrow keys)
bind Left focusleft                       # Super + Left Arrow: Focus frame to the left
bind Right focusright                     # Super + Right Arrow: Focus frame to the right
bind Up focusup                           # Super + Up Arrow: Focus frame above
bind Down focusdown                       # Super + Down Arrow: Focus frame below
# Vim-like alternatives for frame focus (uncomment these and comment out arrows if preferred):
# bind h focusleft
# bind l focusright
# bind k focusup
# bind j focusdown

bind apostrophe fselect                        # Select frame to focus via window list (easier than original s-x)
bind s-apostrophe colon                        # Open ratpoison command prompt

# Splitting Frames
bind 0 exec remove                        # Remove current frame (unsplit)
bind minus hsplit                         # for horizontal
bind equal vsplit                         # for vertical

# Resizing Frames
bind r resize                             # Super + R: Enter resize mode (then use HJKL or Arrows, Enter to confirm)

# Maximizing Frame / Fullscreen Toggle
bind f only                               # Super + F: Toggle current frame to use full screen space (F for Fullscreen/Focus)

# Arrow key alternatives for exchanging (if not using Vim-keys):
bind s-Left exchangeleft
bind s-Down exchangedown
bind s-Up exchangeup
bind s-Right exchangeright

# ------------------------------------------------------------------------------
# III. Workspace Management (using rpws)
# ------------------------------------------------------------------------------
# Switch to workspace N (Super + Number)
bind 1 exec rpws 1
bind 2 exec rpws 2
bind 3 exec rpws 3
bind 4 exec rpws 4
bind 5 exec rpws 5
bind 6 exec rpws 6
bind 7 exec rpws 7
bind 8 exec rpws 8
bind 9 exec rpws 9

# Move current window to workspace N
bind s-1 exec rpws move1
bind s-2 exec rpws move2
bind s-3 exec rpws move3
bind s-4 exec rpws move4
bind s-5 exec rpws move5
bind s-6 exec rpws move6
bind s-7 exec rpws move7
bind s-8 exec rpws move8
bind s-9 exec rpws move9

# Switch to next/previous workspace
bind Page_Down exec rpws prev
bind Page_Up exec rpws next

# Move current window to next/previous workspace
bind s-Page_Down exec rpws moveprev
bind s-Page_Up exec rpws movenext

# ------------------------------------------------------------------------------
# IV. System Control & Ratpoison Commands
# ------------------------------------------------------------------------------
# Volume Control
bind s-0 exec amixer set Master toggle       # Toggle Mute
bind s-minus exec amixer set Master 5%-      # Volume Down 5% (adjust percentage as needed)
bind s-equal exec amixer set Master 5%+      # Volume Up 5%

# Screenshot (using standard PrintScreen keys)
bind Print exec xfce4-screenshooter       # Super + PrintScreen: Launch screenshot tool (interactive)
bind s-Print exec scrot -s -e 'xclip -selection clipboard -t image/png -i $f && rm $f' # Select area, copy to clipboard, remove file

# Ratpoison Command Prompt & Actions
bind u undo                               # Super + U: Undo last ratpoison layout action
bind s-u redo                             # Super + Shift + U: Redo ratpoison layout action

# ------------------------------------------------------------------------------
# V. Other Applications & Utilities
# ------------------------------------------------------------------------------
# Layout Management (rpws)
bind Escape exec /usr/bin/rpws dump /home/linaro/Desktop/01-document/dotfiles/rpws_layouts.dmp # (Save layout)
bind s-Escape exec /usr/bin/rpws restore /home/linaro/Desktop/01-document/dotfiles/rpws_layouts.dmp # (Restore layout)

# Custom User Scripts
bind F1 exec thermal.sh
bind s-F1 exec reverse-thermal.sh

# Terminals with specific commands
bind s-w exec x-terminal-emulator -e nmtui        # (wifi utility)
bind b exec x-terminal-emulator -e bpytop         # (bpytop system monitor)

# Editor & Other Tools
bind x exec xnedit                                # Editor: xnedit
bind s-x exec xnc                                 # xnedit server
bind g exec gsimplecal                            # Super + G (Calendar: gsimplecal)
bind s-g exec galculator                          # (Calculator: galculator)
bind i exec viewnior                              # (Image Viewer: viewnior)
bind s-b exec vorta                               # (Backup: vorta)

# Clipboard interaction scripts (using standard Super+C/V)
bind c exec write_clipboard_to_file.sh            # Super + C (Copy to file - user script)
bind v exec paste_clipboard_from_file.sh          # Super + V (Paste from file - user script)

# User Specific Applications (Flatpaks, etc.)
bind F4 exec flatpak run org.telegram.desktop
bind F5 exec flatpak run com.github.tenderowl.frog
bind F6 exec flatpak run com.strlen.TreeSheets
bind F7 exec flatpak run com.github.ryonakano.reco
bind F8 exec flatpak run io.github.zaps166.QMPlay2

# ------------------------------------------------------------------------------
# VI. Numpad Specific Bindings (Kept if Numpad is actively used for these)
# ------------------------------------------------------------------------------
# Switch to workspace N using Numpad
bind KP_1 exec rpws 1
bind KP_2 exec rpws 2
bind KP_3 exec rpws 3
bind KP_4 exec rpws 4
bind KP_5 exec rpws 5
bind KP_6 exec rpws 6
bind KP_7 exec rpws 7
bind KP_8 exec rpws 8
bind KP_9 exec rpws 9

# Move current window to workspace N
bind s-KP_1 exec rpws move1
bind s-KP_2 exec rpws move2
bind s-KP_3 exec rpws move3
bind s-KP_4 exec rpws move4
bind s-KP_5 exec rpws move5
bind s-KP_6 exec rpws move6
bind s-KP_7 exec rpws move7
bind s-KP_8 exec rpws move8
bind s-KP_9 exec rpws move9

# Original xdotool bindings for typing quotes (very specific, uncomment if needed)
bind KP_0 exec xdotool key apostrophe key apostrophe key apostrophe
bind KP_Separator exec xdotool key quotedbl key quotedbl key quotedbl

# ------------------------------------------------------------------------------
# VII. Prefix-less Keybindings (`definekey top`)
# These bindings work WITHOUT the Super_L prefix.
# ------------------------------------------------------------------------------
# Standard Alt+Tab like behavior for switching between windows (ratpoison's 'next' and 'prev')
definekey top M-Tab next
definekey top M-ISO_Left_Tab prev


# ==============================================================================
# End of Configuration
# ==============================================================================
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
