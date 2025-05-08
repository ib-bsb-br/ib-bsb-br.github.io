---
tags: [linux>dotfile]
info: aberto.
date: 2024-03-10
type: post
layout: post
published: true
slug: xsessionrc
title: '/root/.xsessionrc'
---

Configuring Xorg Display Settings with .xsessionrc on Debian Bullseye

This guide explains how to use the ~/.xsessionrc file to run custom X-related commands, such as xrandr for display configuration, when a user logs into their graphical session on Debian Bullseye.
1. Understanding .xsessionrc

    Purpose: The ~/.xsessionrc file is a user-specific script. If it exists in your home directory and is executable, it's sourced (executed in the current shell's context) at the beginning of your X Window System session. This allows you to set environment variables or run commands before your window manager or desktop environment starts.

    Execution Time: It runs when you log in via a display manager (like GDM, LightDM, SDDM, etc.) and your graphical session starts. It does not run during the system boot process itself (before login).

    Use Cases: Common uses include setting xrandr configurations, starting background applications, or modifying X server settings on a per-user basis.

2. How to Make Your .xsessionrc File Execute

To ensure your ~/.xsessionrc file is executed:

    Step 1: Correct Location
    The file must be named exactly .xsessionrc (note the leading dot) and placed directly in your home directory. For a user named youruser, the full path would be /home/youruser/.xsessionrc.

    Step 2: Correct Permissions
    The file must be executable. You can set this permission using the terminal:

    chmod +x ~/.xsessionrc

    Also, ensure you own the file:

    sudo chown $(whoami):$(whoami) ~/.xsessionrc

    Step 3: Shebang
    The first line of your script should be a shebang indicating the interpreter. For shell scripts, #!/bin/sh or #!/bin/bash is appropriate. Your use of #!/bin/sh is correct.

    Step 4: File Content (Your Script)

```
#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Optional: Uncomment to log script execution for debugging
# LOG_FILE=~/xsessionrc_debug.log
# echo "$(date): .xsessionrc started" >> "$LOG_FILE"

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
# This sets DP-1 to its mode, HDMI-1 to its mode, makes HDMI-1 primary,
# and positions HDMI-1 above DP-1.
# Adjust --primary and relative positioning (--above, --below, --left-of, --right-of) as needed.
xrandr \
    --output DP-1 --mode "1152x864_60.00" \
    --output HDMI-1 --primary --mode "2560x1080_60.00" --above DP-1 # 2>&1 | tee -a "$LOG_FILE"

# Optional: Uncomment to log script completion
# echo "$(date): .xsessionrc finished successfully" >> "$LOG_FILE"
```

    Copy the "Recommended Script Version" into your ~/.xsessionrc file.

3. Verifying Execution

To check if your .xsessionrc script is running:

    Add a simple command to it, like echo "xsessionrc ran at $(date)" > ~/xsessionrc_test.txt.

    Save the ~/.xsessionrc file.

    Log out of your graphical session and log back in.

    Check if the ~/xsessionrc_test.txt file was created and contains the correct message. If your xrandr commands are not working, you can add exec >> ~/xsessionrc_debug.log 2>&1 at the top of your script (after set -e) to log all output and errors from the script to ~/xsessionrc_debug.log.

4. Important Considerations

    Not for System Boot: As mentioned, .xsessionrc is for user session startup, not for system-wide boot-time configuration before any user logs in.

    X Server Dependency: xrandr commands require a running X server and appropriate DISPLAY and XAUTHORITY environment variables, which are typically set up by the time .xsessionrc is executed.

    Display Manager: Most display managers on Debian (like GDM for GNOME, LightDM for XFCE/LXDE/MATE, SDDM for KDE) respect and execute ~/.xsessionrc.

    Command Order & Idempotency: The xrandr commands for defining modes (--newmode) and adding them (--addmode) are generally safe to run multiple times (though xrandr will complain if a mode name already exists for --newmode). Setting the final output configuration in a single xrandr command (as shown in the recommended script) is often more reliable than multiple separate commands for modes and positions.

5. Alternative for System-Wide Configuration (Advanced)

If you need display configurations to be applied system-wide (e.g., at the login screen, before any user logs in, or as a default for all users), you would typically configure the Xorg server directly. This involves creating configuration files (e.g., /etc/X11/xorg.conf.d/10-monitor.conf) with Monitor, Screen, and ServerLayout sections, including Modeline definitions. This method is more complex and uses a different syntax than xrandr commands.

By following these steps, your .xsessionrc file should correctly execute your xrandr commands each time you log into your Debian Bullseye system, setting up your displays as intended.
