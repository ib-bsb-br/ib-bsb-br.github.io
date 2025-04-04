---
tags: [scratchpad]
info: aberto.
date: 2025-04-03
type: post
layout: post
published: true
slug: autorandr
title: 'autorandr'
---
### **Why Use autorandr?**

autorandr is a highly effective, Python-based utility specifically designed to automate and simplify the management of multiple display configurations on Linux systems. Its core strength lies in its ability to automatically detect which displays (like projectors, external monitors, or ultrawide screens) are currently connected to your system and then apply a pre-saved configuration ("profile") that matches that specific hardware setup. This eliminates the need to manually execute commands with xrandr (a command-line tool for configuring display settings) every time you connect or disconnect a display.

This automation is particularly beneficial in your scenario as a professor using a Raspberry Pi 4B with openSUSE Tumbleweed. Imagine moving between different lecture halls, each potentially having a projector with a unique native resolution (1024x768, 1280x800, etc.), then returning to your office to connect to an ultrawide monitor (e.g., 3440x1440), and perhaps later connecting to a standard monitor in a departmental meeting room. Without autorandr, each transition would require manual reconfiguration. With autorandr, once you've saved a profile for each setup, the system adapts automatically upon connection. Furthermore, on a modern system like openSUSE Tumbleweed, autorandr integrates seamlessly with the systemd init system. This means it can leverage udev events (the system's way of detecting hardware changes like plugging in a monitor) to trigger the profile switching automatically in the background, offering a truly hands-off experience after the initial setup.

**Key Benefits Elaborated:**

* **Automatic Detection & Application:** autorandr intelligently identifies connected displays, often using their unique EDID information, and compares this against its library of saved profiles to find the best match, applying it instantly.  
* **Ease of Use:** The "save once, use anywhere" philosophy drastically reduces complexity. Instead of remembering complex xrandr commands or navigating display settings repeatedly, you perform the setup once per unique display combination and save it with a memorable name.  
* **Flexibility:** It excels at managing numerous distinct profiles. You can have profiles for single displays, dual displays in different arrangements (extended desktop, mirrored), displays with specific resolutions or refresh rates, covering virtually any common scenario you encounter.  
* **Robustness:** It gracefully handles situations where display EDID information might be missing, corrupt, or ambiguous – common issues with older projectors or certain adapters. Instead of failing outright or requiring manual intervention like raw xrandr might, autorandr can use other detected properties or fall back to a predefined default profile, ensuring you usually get a usable display state.

### **Prerequisites (Raspberry Pi 4B Specific)**

Before diving into autorandr installation, optimizing your Raspberry Pi 4B environment is crucial for smooth display operation, especially given its shared memory architecture:

* **GPU Memory (gpu\_mem):** The Raspberry Pi dynamically allocates system RAM between the CPU and the VideoCore GPU. Insufficient memory allocated to the GPU can lead to various graphical issues, such as visual glitches, screen tearing, an inability to drive displays at their native (especially high) resolutions (like 4K), or even completely blank screens. While the default allocation might be sufficient for basic desktop use, connecting multiple monitors or high-resolution displays often requires more. Check your current allocation and consider increasing it if you face issues. You can adjust this by editing the /boot/efi/extraconfig.txt file (the path might vary slightly depending on the exact Tumbleweed Pi image setup) and adding or modifying a line like gpu\_mem=256 or gpu\_mem=512 (allocating 256MB or 512MB respectively). A reboot is required for this change to be applied by the system.  
* **Firmware & System Updates:** The Raspberry Pi's firmware and the Linux kernel's graphics drivers (like V3D DRM) are continually updated to improve hardware compatibility, fix bugs, and enhance performance. These updates often include improved handling of display detection protocols like EDID. Keeping your openSUSE Tumbleweed system fully updated is the best way to ensure you have the latest fixes and broadest compatibility. Use the standard Tumbleweed update command, sudo zypper dup (which performs a full system upgrade). Regularly running this ensures you benefit from the latest improvements relevant to display handling.

### **Installation on openSUSE Tumbleweed**

You have several avenues to install autorandr on your system:

1. **Check Standard Repositories (Try First):** OpenSUSE Tumbleweed might already include autorandr in its main repositories. You can check its availability and install it if found:  
   \# Check if the package exists  
   zypper info autorandr  
   \# If available, install it  
   sudo zypper refresh  
   sudo zypper install autorandr

2. **Recommended Method (openSUSE Build Service \- OBS):** The autorandr author often maintains a more up-to-date version in a dedicated OBS repository. This is generally the preferred method if the package isn't in the main repos or if you need the latest features/fixes:  
   \# Add the repository  
   sudo zypper addrepo https://download.opensuse.org/repositories/home:phillipberndt/openSUSE\_Tumbleweed/home:phillipberndt.repo  
   \# Refresh repository metadata  
   sudo zypper refresh  
   \# Install autorandr from the new repo  
   sudo zypper install autorandr

3. **Alternative Method (pip):** You can install autorandr using Python's package installer, pip. However, be aware that this method might install it only for the current user, might not integrate as seamlessly with system-wide services like systemd/udev, and might require manual handling of non-Python dependencies. It can also lead to conflicts if system packages also provide parts of the dependencies.  
   \# Ensure pip is installed, then install autorandr  
   sudo zypper install python3-pip  
   sudo pip install autorandr

4. **Alternative Method (From Source):** For developers or those needing the absolute latest code, you can clone the autorandr Git repository and install it manually. This typically requires development tools like gcc and make, and you'll need to manage dependencies yourself. Consult the README file in the repository for specific instructions.  
   \# Example (dependencies might vary)  
   sudo zypper install git make python3-devel  
   git clone https://github.com/phillipberndt/autorandr.git  
   cd autorandr  
   sudo make install

### **Basic Configuration: Creating and Managing Profiles**

The fundamental workflow for using autorandr revolves around capturing the state of your display setup for each unique configuration you use:

1. **Connect:** Physically connect your Raspberry Pi to the specific combination of displays (e.g., a single classroom projector, your dual monitors at the office).  
2. **Configure Manually (Once):** Use your preferred method to arrange the displays exactly how you want them *for this specific setup*. This could be:  
   * **Desktop Environment Tools:** Use the graphical display settings panel provided by your desktop environment (e.g., xfce4-display-settings in Xfce, the 'Displays' panel in GNOME Settings). Here you can typically enable/disable monitors, set resolutions, refresh rates, orientation, and define primary displays and relative positions in an extended desktop.  
   * **Manual xrandr Commands:** For more fine-grained control or scripting, use xrandr directly in the terminal. For example: xrandr \--output HDMI-1 \--mode 1920x1080 \--primary \--output DisplayPort-1 \--mode 2560x1440 \--rotate left \--right-of HDMI-1.  
3. **Save Profile:** Once the displays are configured correctly, save this entire state as an autorandr profile using a descriptive name. Choosing a consistent naming convention can be helpful, e.g., location-displaytype-resolution or setup\_description.  
   \# Example for a specific lecture hall projector  
   autorandr \--save lecturehallB-projector-1280x800

   \# Example for your office ultrawide setup  
   autorandr \--save office-ultrawide-3440x1440

   \# Example for a standard 1080p monitor used for testing  
   autorandr \--save lab-monitor-1080p

   It's a good idea to back up this directory periodically, especially if you have complex or finely-tuned profiles.  
4. **List Profiles:** To review the profiles you have saved:  
   autorandr \--list

### **Applying Configurations**

* **Manual Application:** You can manually trigger autorandr to detect the currently connected displays and apply the best-matching profile from your saved library. This is useful for testing or if automation isn't set up.  
  autorandr \--change

  Behind the scenes, autorandr \--change performs several steps: it detects all connected displays and their properties (like EDID, which is data that allows a display to communicate its capabilities to the graphics card), compares this information against the data stored in each of your saved profiles, calculates a "match score" for each profile based on how well it fits the current hardware, and then automatically executes the xrandr commands stored within the highest-scoring profile (if the score exceeds a certain threshold). If no profile matches well enough, it might load the designated default profile or leave the configuration unchanged, depending on your setup.

### **Automation (Recommended)**

For the most convenient experience, configure autorandr to react automatically whenever you connect or disconnect a display:

* **Using systemd Service:** This is generally the most robust and manageable method on modern Linux systems like openSUSE Tumbleweed. The autorandr.service unit, when enabled, typically integrates with udev to monitor for display-related hardware events (specifically from the Direct Rendering Manager or DRM subsystem). Upon detecting such an event (e.g., an HDMI cable being plugged in), systemd activates the service, which in turn usually runs autorandr \--change to apply the appropriate profile.  
  \# Enable the service to start on boot and start it immediately  
  sudo systemctl enable \--now autorandr.service  
  \# You can check its status later with: systemctl status autorandr.service

* **Using udev Rules:** autorandr packages often include udev rules (e.g., in /lib/udev/rules.d/) that directly trigger autorandr \--change when specific kernel events related to display hardware occur. While this works, managing services through systemd often provides better control, logging, and dependency management. If you installed manually or suspect the rules aren't active, you might need to reload them:  
  sudo udevadm control \--reload-rules && sudo udevadm trigger

  With either automation method properly configured, plugging in a known projector or monitor should automatically result in your saved configuration being applied, although there might be a brief delay (a few seconds) while autorandr detects the display and applies the profile.

### **Setting a Default Fallback Profile**

It's highly recommended to define a "fallback" or "default" profile. This profile will be automatically applied by autorandr \--change (and thus by the automated services) if you connect a display configuration that doesn't closely match any of your specifically saved profiles. The primary purpose is to prevent being left with an unusable or awkward display state (like a very low resolution, incorrect mirroring, or only the laptop's internal display active when an external one is connected but unrecognized).

1. **Choose and Save a Safe Profile:** Configure your display(s) to a very common and widely supported resolution, like 1920x1080@60Hz or perhaps 1280x720@60Hz, which most monitors and projectors should handle without issue. Save this configuration:  
   \# Example: Configure for 1920x1080 manually first, then save  
   autorandr \--save fallback-1080p

2. **Set as Default:** Tell autorandr to use this profile as the default:  
   autorandr \--default fallback-1080p

   Now, when connecting an unknown display, autorandr will attempt to apply this safe configuration, maximizing the chances of getting a usable picture.

### **Advanced Usage**

autorandr offers features beyond basic profile switching:

* Wildcard EDID Matching: Sometimes you might have several projectors or monitors of the same model series. Their EDIDs might be very similar but differ slightly (e.g., in serial number fields). To create a single profile that matches all of them, you can edit the config file within the profile directory (e.g., \~/.config/autorandr/classroom-projectors/config). Find the line(s) specifying the EDID for the relevant output(s) and replace the differing parts (or less critical parts) with an asterisk (\*).  
  Example snippet from \~/.config/autorandr/some\_profile/config:\*  
  output HDMI-1  
    \# edid 00ffffffffffff001e6d\[...\] \# Original specific EDID  
    edid 00ffffffffffff001e6d\* \# Matches any EDID starting with this prefix

  *Caution:* Be careful not to make the wildcard too broad, or it might incorrectly match unintended displays.  
* **Hook Scripts:** You can automate actions that should occur whenever a specific profile is loaded or unloaded. Create executable scripts (e.g., using bash or python) named preswitch (runs before switching *to* this profile), postswitch (runs after switching *to* this profile), predetect (runs before detection), or postdetect (runs after detection) inside a profile's directory (\~/.config/autorandr/\<profile\_name\>/) or the global config directory (\~/.config/autorandr/). Common uses for postswitch include:  
  * Setting a specific desktop wallpaper: feh \--bg-scale /path/to/wallpaper.jpg  
  * Restarting desktop panels if they don't resize correctly: xfce4-panel \-r  
  * Changing the default audio output sink.  
    Remember to make the scripts executable: chmod \+x \~/.config/autorandr/\<profile\_name\>/postswitch.  
* **Forcing Matches (--match-edid):** In rare troubleshooting scenarios where display properties other than EDID might be causing incorrect profile matching, you can experiment with options like autorandr \--change \--match-edid to force matching based primarily or solely on the EDID information. Consult man autorandr for details.

### **Troubleshooting**

If autorandr doesn't behave as expected:

* **Check Detected Profiles & Scores:** See what autorandr currently detects and how well it matches known profiles. The output shows detected profiles and their calculated match scores.  
  autorandr \--detected

* **Use Debug Mode:** This provides highly detailed output about the detection process, including EDIDs read, profiles considered, matching scores, and the exact xrandr commands being generated and executed. This is invaluable for diagnosing why a specific profile isn't being selected.  
  autorandr \--change \--debug

* **Check System Logs:** Look for errors or warnings related to the graphics driver (DRM) or EDID processing in the system journal. This can reveal underlying hardware or driver issues.  
  \# View live logs (press Ctrl+C to stop)  
  journalctl \-f | grep \-i \-E "drm|edid|autorandr"  
  \# View logs from the current boot  
  journalctl \-b | grep \-i \-E "drm|edid|autorandr"

* **Ensure System Updates:** Reiterate the importance of sudo zypper dup to ensure you have the latest kernel, graphics drivers, and potentially autorandr fixes.  
* **Check Physical Connections:** Sometimes the simplest solution is overlooked. Ensure HDMI or DisplayPort cables are securely plugged in at both the Raspberry Pi and the display ends. Try a different cable if problems persist.

### **Alternative: Hardware HDMI EDID Emulator**

For displays that consistently cause problems due to missing, corrupt, or non-standard EDID information, a hardware **HDMI EDID Emulator** (also known as an EDID ghost or dummy plug) can be a viable workaround. This small device plugs into an HDMI port on the Pi and contains a chip pre-programmed with standard EDID data (e.g., for a 1080p monitor). The Raspberry Pi's operating system reads the EDID from the emulator instead of the actual connected display. This effectively forces the Pi to "see" a standard display, often resolving issues with problematic hardware like some older projectors or KVM switches. While it provides consistency, it lacks the dynamic flexibility of autorandr – it forces one specific configuration regardless of what display (if any) is actually connected downstream. It's a targeted solution for specific problematic hardware, not a replacement for general-purpose profile management.

### **Resources**

* **autorandr** GitHub Repository: The primary source for code, detailed documentation (README), and reporting issues. Check the Issues page here for existing bug reports or troubleshooting discussions. [https://github.com/phillipberndt/autorandr](https://github.com/phillipberndt/autorandr)  
* **openSUSE Build Service Package:** Link to the specific package page for the OBS repository, useful for checking versions and build status. [https://build.opensuse.org/package/show/home:phillipberndt/autorandr](https://build.opensuse.org/package/show/home:phillipberndt/autorandr)

By carefully configuring autorandr and leveraging its automation features, you can significantly streamline the process of using your Raspberry Pi 4B with diverse display setups, making your transitions between classroom, office, and other locations much smoother and less prone to technical interruptions.
