---
tags: [scratchpad]
info: aberto.
date: 2025-05-03
type: post
layout: post
published: true
slug: liveraizo-sbnb
title: 'Live Raizo OS as a hypervisor to run the `sbnb.vhd` VM'
---
This comprehensive guide details how to set up and run the sbnb.vhd virtual machine (VM) on the Live Raizo Linux distribution. Live Raizo is a specialized Debian-based environment optimized for network simulation and system administration training, making it an excellent platform for experimenting with VMs in complex virtual network topologies.  
**Why Live Raizo?** Live Raizo pre-installs GNS3, QEMU/KVM, and various networking tools, simplifying the setup process compared to a standard Linux distribution. Its integration with GNS3 allows you to easily incorporate the SBNB VM into simulated networks alongside virtual routers, switches, and other devices.  
**Recommendation:** Using **GNS3 (Method 1\)** is the strongly recommended approach on Live Raizo. It aligns with the distribution's purpose, offers graphical management, and facilitates network integration. Direct QEMU/KVM provides the lowest overhead but requires command-line proficiency, while Virt-Manager offers a more traditional VM management GUI but is less integrated with Live Raizo's specific networking tools.  
**Methods Overview:**

1. **GNS3 Integration (Recommended):** Manages the VM within the GNS3 network simulation environment.  
   * **Option A: GNS3 GUI (Manual Setup):** User-friendly, step-by-step configuration via the graphical interface. Best for most users.  
   * **Option B: Add-to-GNS3.sh API (Advanced/Scripting):** Automates template creation using Live Raizo's specific command-line tools. Suitable for users comfortable with scripting and wanting repeatable setups, but requires careful verification.  
2. **Direct QEMU/KVM (Minimalist Alternative):** Launches the VM directly using qemu-system-x86\_64 commands. Offers fine-grained control but lacks the integration benefits of GNS3.  
3. **Virt-Manager (Alternative GUI):** Uses the standard Linux graphical tool for managing libvirt VMs. Familiar to users of other distributions but requires separate installation and management from GNS3.

**Prerequisites (Apply to All Methods)**

1. **Live Raizo Host:** A functional Live Raizo system, booted from a Live USB/ISO or installed onto a hard drive. You will operate primarily as the default user, using sudo to execute commands requiring administrative privileges.  
2. **Hardware Virtualization (VT-x/AMD-V):** Modern virtualization relies on CPU extensions (Intel VT-x or AMD-V) for performance. This must be enabled in your computer's BIOS or UEFI settings. To check if Linux recognizes it, open a terminal:  
   lscpu | grep \-Ei \--color=auto "svm|vmx"

   You should see vmx (for Intel) or svm (for AMD) highlighted in the output. If not, reboot your computer, enter the BIOS/UEFI setup (often by pressing keys like Del, F2, F10, or Esc during boot), find settings related to "Virtualization Technology," "VT-x," "AMD-V," or similar, and ensure they are Enabled. Save changes and exit.  
3. **Install Essential Tools (If Needed):**  
   * Live Raizo typically includes GNS3 and QEMU/KVM.  
   * Install necessary supporting packages: genisoimage for creating the Tailscale key ISO, and ovmf which provides the UEFI firmware files required by QEMU for modern VM booting.  
     \# First, update the package list cache  
     sudo apt update  
     \# Install both packages; apt will handle dependencies  
     \# ovmf provides the UEFI firmware needed by QEMU for modern VMs  
     sudo apt install \-y genisoimage ovmf

   * *(Self-Check): You can verify the installation afterwards:*  
     dpkg \-s genisoimage ovmf &\> /dev/null && echo "Packages 'genisoimage' and 'ovmf' are installed." || echo "Error: One or both packages are MISSING."

     *This command checks the status; run the apt install command above if they are missing.*  
4. **Enable Libvirt Daemon (Only if using Method 3 \- Virt-Manager):** Virt-Manager relies on the libvirt service to manage VMs.  
   \# Ensure virt-manager and the libvirt service components are installed  
   sudo apt install virt-manager libvirt-daemon-system  
   \# Enable the service to start automatically on boot and start it now  
   sudo systemctl enable \--now libvirtd  
   \# Check its status to confirm it's running correctly  
   systemctl status libvirtd

   *(Look for "active (running)" in the status output).*  
5. **Obtain sbnb.vhd:** Download the SBNB virtual hard disk file (sbnb.vhd). Place it in a convenient and memorable location on your Live Raizo system, for example, create a dedicated directory: /home/user/SBNB\_VM/sbnb.vhd. Make sure you know the full, correct path to this file.  
6. **Obtain Tailscale Key:** Access your Tailscale account's admin console (usually via login.tailscale.com). Navigate to Settings \-\> Keys. Generate an authentication key. Consider using a reusable key if you plan to recreate this VM often, or an ephemeral key if the VM is temporary (ephemeral keys automatically remove the node from your Tailnet after a period of inactivity). Copy the generated key (it will look like tskey-auth-k...).

**Handling the SBNB Tailscale Key (sbnb-tskey.txt)**  
SBNB requires the Tailscale authentication key during its initial boot phase to securely join your Tailnet. Providing this key via a small, simple ISO image attached as a virtual CD-ROM is a reliable method. It ensures the key is accessible early in the boot process, independent of complex disk configurations or network states within the nascent VM.

1. **Create Key File:** Open a terminal. Use a text editor or echo to create the file containing *only* your Tailscale key. Replace YOUR\_TAILSCALE\_KEY with the actual key you copied.  
   \# Create the directory if it doesn't exist  
   mkdir \-p /home/user/SBNB\_VM \# Use the same directory as your VHD for organization  
   \# Create the key file  
   echo "YOUR\_TAILSCALE\_KEY" \> /home/user/SBNB\_VM/sbnb-tskey.txt \# Ensure the filename is exactly 'sbnb-tskey.txt'

2. **Create ISO Image:** Use the genisoimage command (installed previously) to package the text file into an ISO.  
   \# Command syntax: genisoimage \-o \<output\_iso\_path\> \<input\_file\_path\>  
   genisoimage \-o /home/user/SBNB\_VM/sbnb-key.iso /home/user/SBNB\_VM/sbnb-tskey.txt

   This creates sbnb-key.iso in the /home/user/SBNB\_VM directory.  
3. **Note the Path:** Remember the full path to sbnb-key.iso, as you will need it when configuring the VM in the following steps.

**Method 1: GNS3 Integration (Recommended)**  
This method leverages GNS3, Live Raizo's core tool, providing a graphical interface for managing the VM and integrating it into network simulations.

* **Option A: Using the GNS3 GUI (Manual Setup)**  
  * This is the most user-friendly and generally recommended way within GNS3.  
  1. **Start GNS3:** If you're in the Live Raizo console, type startx to enter the graphical environment. Launch GNS3 from the application menu or by typing gns3 in a terminal.  
  2. **Preferences:** Navigate the menu: "Edit" \-\> "Preferences".  
  3. **QEMU VMs Section:** In the Preferences window, find "QEMU" in the left pane and click on "QEMU VMs".  
  4. **Create New Template:** Click the "New" button at the bottom of the window.  
  5. **Wizard Steps:**  
     * Server Type: Choose "Run this QEMU VM on the local computer". Click "Next".  
     * Name: Enter a descriptive name for the template, e.g., SBNB-GUI. Click "Next".  
     * RAM: Allocate RAM in MiB (e.g., 1024 for 1GB, 2048 for 2GB). Adjust based on SBNB's requirements and your host system's resources. Click "Next".  
     * Console Type: Select VNC (provides a graphical console view) or Spice (another graphical protocol, sometimes offering better integration like copy/paste if guest tools are installed in the VM). VNC is generally a safe default. Click "Next".  
     * Disk Image: Click "Browse...", navigate to where you saved sbnb.vhd (e.g., /home/user/SBNB\_VM/sbnb.vhd), select it, and click "Open". Click "Finish".  
  6. **Edit Template Settings:** The wizard created a basic template. Now, fine-tune it. Select the newly created SBNB-GUI template in the list and click "Edit".  
  7. **Configure Tabs:** Review and adjust settings across the different tabs. Click "Apply" within the Edit window after making changes in each relevant tab.  
     * **General settings:** Set the desired number of **vCPUs** (e.g., 2).  
     * **HDD:** Ensure the **Disk interface** is set to virtio. This uses paravirtualized drivers for significantly better disk performance compared to emulated IDE or SATA controllers.  
     * **CD/DVD:** For the **Image**, click "Browse...", navigate to and select your sbnb-key.iso (e.g., /home/user/SBNB\_VM/sbnb-key.iso).  
     * **Advanced:** This tab is crucial for boot settings. \*\*CRITICAL:\*\* Check the box labeled **"Use UEFI boot"**. This tells QEMU to use the OVMF firmware instead of legacy BIOS, which is likely required by SBNB.  
  8. **Save Changes:** Once all tabs are configured, click "OK" in the Edit window, and then "OK" again in the Preferences window.  
  9. **Use in Project:** Create a new GNS3 project or open an existing one. Find SBNB-GUI in the "End devices" panel (usually looks like a computer monitor icon). Drag it onto the main workspace. Optionally, connect its network interface (e.g., Ethernet0) to other GNS3 nodes like a Switch, Router, NAT cloud (for internet access), or the "LiveRaizo" node (for host communication via virbr0). Right-click the SBNB node on the workspace and select "Start". Once started, right-click again and select "Console" to view its output (this will open a VNC or Spice viewer).  
* **Option B: Using the Add-to-GNS3.sh API (Advanced/Scripting Alternative)**  
  * *\*Note: This advanced method uses Live Raizo's specific command-line API for automation. It requires careful path configuration in the script and understanding of the API's limitations. **Manual verification of the generated template in the GNS3 GUI afterwards is essential**, as the API might not configure all options (like vCPUs) perfectly.*  
  1. **Prepare Files:** Ensure sbnb.vhd, sbnb-key.iso, and the necessary firmware/tools are ready.  
     * Place sbnb.vhd in a stable location (e.g., /home/user/SBNB\_VM/sbnb.vhd).  
     * Place sbnb-key.iso in the same location (e.g., /home/user/SBNB\_VM/sbnb-key.iso).  
     * **Create MD5 sum file for the VHD (Required by API):** The API uses this checksum to identify the disk image.  
       cd /home/user/SBNB\_VM/ \# Navigate to VHD directory  
       \# Use 'cut' to store only the 32-character hash, excluding the filename  
       md5sum sbnb.vhd | cut \-d' ' \-f1 \> sbnb.vhd.md5sum

  2. **Create an Import Script (e.g., add\_sbnb.sh):** Create a new file named add\_sbnb.sh using a text editor (like nano add\_sbnb.sh) and paste the following content. **Carefully review and adjust the paths in the Configuration section.**  
     \#\!/usr/bin/bash

     \# Source the Live Raizo API definitions  
     source /opt/raizo/api/Add-to-GNS3.sh  
     if (($?)); then  
         echo "Error: Failed to source the Live Raizo API script '/opt/raizo/api/Add-to-GNS3.sh'."  
         exit 1  
     fi

     \# \--- User Configuration \---  
     \# Adjust these variables to match your setup  
     VM\_NAME="SBNB-API" \# Name that will appear in GNS3  
     RAM\_MB=1024        \# Memory in Megabytes (e.g., 1024, 2048\)  
     NUM\_NICS=1         \# Number of network interfaces (SBNB likely needs 1 for Tailscale)  
     CONSOLE\_TYPE="vnc" \# Console access method ('vnc' or 'spice')  
     VHD\_PATH="/home/user/SBNB\_VM/sbnb.vhd"       \# FULL path to the VHD file  
     KEY\_ISO\_PATH="/home/user/SBNB\_VM/sbnb-key.iso" \# FULL path to the key ISO file  
     \# Standard path for OVMF firmware on Debian/Live Raizo. Verify this path exists.  
     OVMF\_PATH="/usr/share/OVMF/OVMF\_CODE.fd"

     \# \--- Script Logic \---  
     echo "--- Starting SBNB VM Import Script \---"

     \# \--- Pre-flight Checks \---  
     echo "Performing pre-checks..."  
     if \[\[ \! \-f "$OVMF\_PATH" \]\]; then  
         echo "Error: OVMF firmware not found at '$OVMF\_PATH'. Please ensure 'ovmf' package is installed ('sudo apt install ovmf')."  
         exit 1  
     fi  
     if \[\[ \! \-f "$VHD\_PATH" \]\]; then  
         echo "Error: VHD disk image not found at '$VHD\_PATH'."  
         exit 1  
     fi  
     if \[\[ \! \-f "${VHD\_PATH}.md5sum" \]\]; then  
         echo "Error: MD5 sum file not found at '${VHD\_PATH}.md5sum'."  
         echo "Please create it in the same directory as the VHD using: md5sum '${VHD\_PATH\#\#\*/}' | cut \-d' ' \-f1 \> '${VHD\_PATH\#\#\*/}.md5sum'"  
         exit 1  
     fi  
     if \[\[ \! \-f "$KEY\_ISO\_PATH" \]\]; then  
         echo "Error: Key ISO file not found at '$KEY\_ISO\_PATH'."  
         exit 1  
     fi  
     echo "Pre-checks passed."

     \# \--- Set Live Raizo API Global Variables \---  
     \# These variables influence the Create-VMQEmu function.  
     \# Using VirtIO generally offers the best performance for disk and network.  
     export TYPE\_HARD\_DISK="virtio"       \# Disk interface type for the VHD  
     export TYPE\_NETWORK\_CARD="virtio-net-pci" \# Network card type

     \# Pass essential QEMU options (UEFI firmware and CD-ROM) via the OPTION\_QEMU variable.  
     \# Based on API docs, this is the intended mechanism for custom QEMU flags.  
     export OPTION\_QEMU="-bios ${OVMF\_PATH} \-cdrom ${KEY\_ISO\_PATH}"  
     echo "Set API options: TYPE\_HARD\_DISK=$TYPE\_HARD\_DISK, TYPE\_NETWORK\_CARD=$TYPE\_NETWORK\_CARD"  
     echo "Set API options: OPTION\_QEMU=$OPTION\_QEMU"

     \# Optional: Define a custom icon for GNS3 (uncomment and set path if desired)  
     \# export SYMBOL\_QEMU="/path/to/your/custom\_icon.svg"

     \# \--- Create VM Configuration Template \---  
     echo "Creating VM configuration template file..."  
     \# Function Signature from docs: Create-VMQEmu Name NICs RAM Access ACPI Disk1 \[Disk2...\]  
     \# We provide Name, NIC count, RAM, Console Type, ACPI (false), and primary Disk (VHD).  
     \# vCPUs are not directly supported by this API call and must be set manually later.  
     \# The ISO is attached via OPTION\_QEMU, not as a positional disk argument.  
     ConfigVM=$(Create-VMQEmu "$VM\_NAME" "$NUM\_NICS" "$RAM\_MB" "$CONSOLE\_TYPE" false "$VHD\_PATH")

     \# \--- Check for Errors from Create-VMQEmu \---  
     \# The API uses FAST\_ERROR\_RAIZO (non-zero indicates error) and FAST\_ERROR\_RAIZO\_LOG for messages.  
     if \[\[ \-z "$ConfigVM" || $FAST\_ERROR\_RAIZO \-ne 0 \]\]; then  
         echo "Error: Failed to create VM configuration template."  
         echo "API Error Code: $FAST\_ERROR\_RAIZO"  
         echo "API Error Log: $FAST\_ERROR\_RAIZO\_LOG"  
         \# Clean up the temporary config file if it was partially created  
         \[\[ \-n "$ConfigVM" && \-f "$ConfigVM" \]\] && rm \-f "$ConfigVM"  
         exit 1  
     fi  
     echo "VM Config file successfully created: ${ConfigVM}"

     \# \--- Add VM Configuration to GNS3 \---  
     \# This function processes the template file created above and adds it to GNS3's config.  
     \# It relies on the .md5sum file existing alongside the VHD\_PATH.  
     echo "Adding VM configuration to GNS3..."  
     Add-ConfigVM-to-GNS3 "${ConfigVM}"

     \# \--- Check for Errors from Add-ConfigVM-to-GNS3 \---  
     if (($FAST\_ERROR\_RAIZO \!= 0)); then \# Check if FAST\_ERROR\_RAIZO is not zero  
         echo "Error: Failed to add VM configuration to GNS3."  
         echo "API Error Code: $FAST\_ERROR\_RAIZO"  
         echo "API Error Log: $FAST\_ERROR\_RAIZO\_LOG"  
         \# Clean up the temporary config file  
         rm \-f "${ConfigVM}"  
         exit 1  
     fi

     \# \--- Success Message & Verification Steps \---  
     echo "--------------------------------------------------------------------"  
     echo "SUCCESS: VM template '$VM\_NAME' added to GNS3."  
     echo ""  
     echo "=====\> IMPORTANT: VERIFICATION STEPS REQUIRED in GNS3 GUI \<====="  
     echo "The API should have configured UEFI and CD-ROM, but please verify these settings"  
     echo "and manually configure options not supported by the script (like vCPUs):"  
     echo "  1\. Start GNS3 (run 'startx' first if not in GUI)."  
     echo "  2\. Go to Edit \-\> Preferences \-\> QEMU VMs."  
     echo "  3\. Select '$VM\_NAME' and click 'Edit'."  
     echo "  4\. General Settings Tab: Manually set desired vCPUs (e.g., 2)."  
     echo "  5\. HDD Tab: Confirm Disk image is '${VHD\_PATH}' and Interface is 'virtio'."  
     echo "  6\. CD/DVD Tab: Verify Image points to '${KEY\_ISO\_PATH}'."  
     echo "  7\. Advanced Settings Tab: \*\*Confirm 'Use UEFI boot' is YES (checked).\*\*"  
     echo "     Also verify 'Additional settings \-\> Options' contains '${OPTION\_QEMU}'."  
     echo "  8\. Network Tab: Confirm Adapters=${NUM\_NICS}, Type='virtio-net-pci'."  
     echo "  9\. Console Tab: Confirm Type is '${CONSOLE\_TYPE}'."  
     echo " 10\. Click OK and Apply to save changes (especially vCPUs)."  
     echo "The VM template is now ready to be used on the GNS3 canvas."  
     echo "--------------------------------------------------------------------"

     \# Optional: Clean up the temporary configuration file generated by Create-VMQEmu  
     \# echo "Cleaning up temporary file: ${ConfigVM}"  
     \# rm \-f "${ConfigVM}"

     \# Unset API variables used by the script to avoid polluting the interactive shell environment  
     unset TYPE\_HARD\_DISK TYPE\_NETWORK\_CARD OPTION\_QEMU SYMBOL\_QEMU ConfigVM FAST\_ERROR\_RAIZO FAST\_ERROR\_RAIZO\_LOG VM\_NAME RAM\_MB NUM\_NICS CONSOLE\_TYPE VHD\_PATH KEY\_ISO\_PATH OVMF\_PATH

     exit 0

  3. **Make Executable and Run:** Save the script (e.g., as add\_sbnb.sh), make it executable, and run it.  
     chmod \+x add\_sbnb.sh  
     ./add\_sbnb.sh

  4. **Verify in GNS3 GUI:** \*\*Carefully follow the verification steps printed by the script upon successful execution.\*\* Pay close attention to setting the vCPU count and confirming the UEFI boot option is enabled in the GNS3 template editor.  
  5. **Use in GNS3:** Once verified, find SBNB-API in the End Devices panel, drag it onto the GNS3 workspace, and start it.

**Method 2: Direct QEMU/KVM (Minimalist Alternative)**  
This method bypasses GNS3 entirely, launching the VM directly from the command line using QEMU commands. It offers maximum control but requires more manual configuration for networking beyond basic user-mode NAT.

1. **Verify OVMF Path:** Ensure the UEFI firmware file exists, typically at /usr/share/OVMF/OVMF\_CODE.fd.  
2. **Launch Command:** Open a terminal. Adjust memory (-m), CPU cores (-smp), and file paths as needed.  
   qemu-system-x86\_64 \\  
       \-enable-kvm \\  
       \-m 1G \\  
       \-smp 2 \\  
       \-cpu host \\  
       \-bios /usr/share/OVMF/OVMF\_CODE.fd \\  
       \-drive file=/home/user/SBNB\_VM/sbnb.vhd,format=vpc,if=virtio \\  
       \-cdrom /home/user/SBNB\_VM/sbnb-key.iso \\  
       \-netdev user,id=net0 \\  
       \-device virtio-net-pci,netdev=net0 \\  
       \-vga virtio \\  
       \# Remove the next line to get a graphical console window instead of running headless  
       \-nographic

   * \-enable-kvm: Use Linux Kernel Virtual Machine for hardware acceleration (essential for performance).  
   * \-m 1G: Allocate 1 Gigabyte of RAM to the VM.  
   * \-smp 2: Assign 2 virtual CPU cores to the VM.  
   * \-cpu host: Pass through the host CPU's features to the guest for potentially better compatibility and performance. If this causes issues, try a specific model like \-cpu qemu64.  
   * \-bios /path/to/OVMF\_CODE.fd: **CRITICAL.** Specifies the UEFI firmware file, enabling UEFI boot.  
   * \-drive file=path,format=vpc,if=virtio: Defines the virtual hard disk. file= points to your VHD, format=vpc specifies the VHD format, if=virtio uses high-performance VirtIO drivers.  
   * \-cdrom /path/to/iso: Attaches the specified ISO file as a virtual CD/DVD drive.  
   * \-netdev user,id=net0: Creates a basic user-mode network backend (provides simple NAT). id=net0 names this backend.  
   * \-device virtio-net-pci,netdev=net0: Creates a virtual network card in the VM using VirtIO drivers and connects it to the net0 backend.  
   * \-vga virtio: Use the VirtIO GPU for better graphics performance if running with a graphical console.  
   * \-nographic: Run the VM without a graphical display window (headless). Remove this if you need to interact with a GUI or see boot messages directly.

**Method 3: Virt-Manager (Alternative GUI)**  
This uses the standard virt-manager graphical tool, which interacts with the libvirt daemon. It's a common way to manage VMs on Linux but operates separately from GNS3.

1. **Launch Virt-Manager:** Ensure the libvirtd service is running (see Prerequisites). Launch virt-manager from the menu or terminal.  
2. **Create New VM:** Click the "Create a new virtual machine" button (often top-left icon) or go to "File" \-\> "New Virtual Machine".  
3. **Import Disk:** Choose the option "Import existing disk image". Click "Forward".  
4. **Provide Disk Path:** Click "Browse...", then "Browse Local". Navigate to your sbnb.vhd file (e.g., /home/user/SBNB\_VM/sbnb.vhd) and click "Open". Select the volume and click "Choose Vol".  
5. **OS Type:** In the "Choose Operating System" step, type "Generic" in the search box and select "Generic OS" or "Generic Linux". Click "Forward".  
6. **Memory and CPU:** Allocate RAM (e.g., 1024 MiB) and CPUs (e.g., 2). Click "Forward".  
7. **Final Configuration:** Give the VM a name (e.g., SBNB-VirtMgr). **Crucially, check the box "Customize configuration before install"**. Click "Finish".  
8. **Customize Configuration Window:** Adjust the VM hardware settings before the first boot:  
   * **Overview:** Under "Hypervisor Details", find **Firmware**. \*\*CRITICAL:\*\* Select the option containing **UEFI x86\_64: /usr/share/OVMF/OVMF\_CODE.fd**. Click "Apply".  
   * **Disk 1 (or VirtIO Disk 1):** Expand "Advanced options". Set "Disk bus" to **VirtIO**. Click "Apply".  
   * **Add Hardware:** Click the "Add Hardware" button (usually bottom-left).  
     * Select "Storage".  
     * Choose "Select or create custom storage".  
     * Device type: "CDROM device".  
     * Click "Manage...". Click "Browse Local". Navigate to your sbnb-key.iso file, select it, click "Open", then "Choose Vol".  
     * Click "Finish" to add the CD-ROM drive.  
   * **NIC (Network Interface):** Select the network card. Ensure "Device model" is set to **virtio**. Click "Apply".  
9. **Begin Installation:** Click the "Begin Installation" button in the top-left corner of the customization window. The VM will now boot using the specified settings.

**Optional: VHD to QCOW2 Conversion**

* **Why Convert?** While QEMU handles VHD (vpc) format, converting to QEMU's native QCOW2 (qcow2) format is often beneficial. QCOW2 supports features like:  
  * **Snapshots:** Capture the VM's state at a point in time, allowing you to easily revert changes – invaluable for testing.  
  * **Thin Provisioning:** The image file only grows as data is written, potentially saving disk space initially.  
  * **Compression (Optional):** Can further reduce disk space usage.  
  * Potentially Better Performance: Native format interaction might be slightly faster.  
    This conversion is not strictly required but recommended for flexibility and features.  
* **How to Convert:** Ensure the VM using the VHD is powered off. Use the qemu-img command:  
  \# Syntax: qemu-img convert \[options\] \-f \<source\_format\> \-O \<dest\_format\> \<source\_file\> \<dest\_file\>  
  \# \-p shows progress  
  qemu-img convert \-p \-f vpc \-O qcow2 /home/user/SBNB\_VM/sbnb.vhd /home/user/SBNB\_VM/sbnb.qcow2

* **Using the QCOW2 File:** After conversion, simply update the disk path in your chosen method to point to the new sbnb.qcow2 file.  
  * **GNS3 GUI/API:** Edit the template, change the disk image path, and ensure the format/interface is still correct (VirtIO). If using the API script (Method 1B), update VHD\_PATH in the script, delete the old .md5sum file, and regenerate it for the .qcow2 file (md5sum /home/user/SBNB\_VM/sbnb.qcow2 | cut \-d' ' \-f1 \> /home/user/SBNB\_VM/sbnb.qcow2.md5sum).  
  * **Direct QEMU:** Change \-drive file=... to point to the .qcow2 file and set format=qcow2.  
  * **Virt-Manager:** Edit the VM settings, remove the old VHD storage, and add the new QCOW2 file as storage, ensuring the bus is VirtIO.

**Verification**  
After successfully starting the SBNB VM using any of the methods:

1. **Monitor Tailscale:** Open your Tailscale Admin Console in a web browser. Within a short time after the VM boots and processes the key from the ISO, the new SBNB node (likely named sbnb-...) should appear in your list of machines.  
2. **Establish SSH Connection:** Once the node appears and shows as connected in Tailscale, find its assigned Tailscale IP address (usually in the 100.x.y.z range) or use its MagicDNS name (e.g., sbnb-hostname.your-tailnet.ts.net). Attempt to SSH into the VM from another machine on your Tailnet (or from the Live Raizo host if Tailscale is also installed and running there):  
   ssh \<username\>@\<SBNB\_Tailscale\_IP\_or\_MagicDNS\_Name\>

   *(Replace \<username\> with the appropriate login user for the SBNB environment, if known. If connection fails, check VM boot logs via console, Tailscale ACLs, and key validity. See Troubleshooting below).*  
3. **Execute SBNB Tasks:** Once logged in via SSH, proceed with any specific tasks required within the SBNB environment, such as running setup scripts like sbnb-dev-env.sh if applicable.

**Troubleshooting Common Issues**

* **VM Doesn't Boot / Stuck at UEFI Shell:**  
  * **Check UEFI Setting:** Double-check that UEFI boot is enabled in the VM settings (GNS3 Advanced Tab, QEMU \-bios option, Virt-Manager Overview tab).  
  * **OVMF Path:** Verify the path to OVMF\_CODE.fd is correct and the ovmf package is installed.  
  * **Disk Path/Format:** Ensure the path to the .vhd or .qcow2 file is correct and the format (vpc or qcow2) matches.  
  * **Console Output:** Check the VM console (VNC/Spice/Terminal) for specific error messages during boot.  
* **Tailscale Key Not Read / VM Doesn't Join Tailnet:**  
  * **ISO Path:** Verify the CD/DVD drive in the VM settings points to the correct sbnb-key.iso file.  
  * **ISO Content:** Mount the ISO temporarily on the host (sudo mount \-o loop /home/user/SBNB\_VM/sbnb-key.iso /mnt) and check if /mnt/sbnb-tskey.txt exists and contains the correct key. Unmount with sudo umount /mnt.  
  * **Filename:** Ensure the file *inside* the ISO is exactly sbnb-tskey.txt.  
  * **Key Validity:** Confirm the Tailscale key hasn't expired or been revoked. Try generating a new key.  
* **No Network Connectivity (Even after joining Tailnet):**  
  * **Tailscale ACLs:** Check your Tailscale Access Control Lists in the admin console to ensure traffic is allowed to/from the SBNB node.  
  * **GNS3 Network:** If connected to other nodes in GNS3 (like NAT or Cloud), ensure those nodes are configured correctly and running. Check cabling in the GNS3 workspace.  
  * **VM Internal Firewall:** Check if the SBNB VM itself has an internal firewall blocking traffic (unlikely for initial connection but possible).  
* **GNS3 API Script (add\_sbnb.sh) Errors:**  
  * **Paths:** Double-check all file paths (VHD\_PATH, KEY\_ISO\_PATH, OVMF\_PATH) defined in the script.  
  * **MD5 File:** Ensure the .md5sum file exists, is named correctly (\<vhd\_filename\>.md5sum), and contains only the hash (cut command used).  
  * **API Errors:** Read the FAST\_ERROR\_RAIZO\_LOG message printed by the script for specific clues from the Live Raizo API.  
  * **Permissions:** Ensure the script has execute permissions (chmod \+x add\_sbnb.sh).

**Leveraging Live Raizo Features (Especially with GNS3)**  
Integrating SBNB into Live Raizo/GNS3 unlocks powerful testing capabilities:

* **Simulate Complex Networks:** Connect the SBNB VM within your GNS3 topology to virtual network devices like Cisco routers (requires providing IOS/IOU images), switches, firewalls (e.g., pfSense, FortiGate VMs), or the built-in Linux VMs (Debian, DDebian) provided by Live Raizo. This allows you to test SBNB's behavior in diverse and realistic network configurations. *(Connections between nodes are made by clicking and dragging cables between device interfaces in the GNS3 workspace.)*  
* **Save and Restore Labs:** Use Live Raizo's fast-save-project (interactive) or fast-backup-lab (command-line) tools to create archives of your entire GNS3 project. This typically saves the topology, device configurations, and potentially the running state of QEMU VMs (if supported and configured), allowing you to easily stop and resume complex lab setups. Use fast-restore-lab to load saved archives.  
* **Connect to External/Host Networks:**  
  * Use the GNS3 **"Cloud"** node, configured to bridge to one of Live Raizo's physical network interfaces (e.g., eth0), to connect your virtual lab, including SBNB, directly to your physical network.  
  * Use the GNS3 **"NAT"** node for simple internet access for VMs via the host's connection.  
  * Use the GNS3 **"LiveRaizo"** node, connected to the virbr0 interface on the host. This allows direct IP communication between your virtual devices and the Live Raizo host OS itself. For easy NAT setup through this bridge, run sudo fast-nat on the Live Raizo host terminal.  
* **Revert VM Disk Changes:** The fast-reset-vm \<VM\_NAME\_in\_GNS3\> command (run while the relevant GNS3 project is open) can discard changes made to the VM's disk image since it was started or last reset, effectively reverting it to its initial state within that project instance. **Warning:** This is a destructive action for the VM's internal state. Use it carefully, primarily when you want a clean slate for testing, and be aware it erases any work done inside the VM. It does not affect the base VHD/QCOW2 file outside the project.  
* **Improve Readability:** Take advantage of Live Raizo's pre-configured Zsh shell with colorized command output, which can make navigating directories, reading logs (fast-syslog), and interpreting network tool output (ip, ping, traceroute) easier during setup and troubleshooting.

***

# /mnt/sbnb-data partition

**Step 1: Create the Virtual Disk File on Live Raizo Host**

You need a file to act as the persistent storage. The QCOW2 format is recommended because it's space-efficient (grows as needed) and supports snapshots.

1.  **Choose Location:** Decide where to store the disk file. Good options include a dedicated VM storage directory (e.g., `/home/user/GNS3_VMs/SBNB/`) or within the specific GNS3 project directory if you prefer (e.g., `/home/user/projects/SBNB/images/`). Ensure the location has sufficient free space.
2.  **Open Terminal:** Launch a terminal on your Live Raizo host.
3.  **Create Disk Image:** Use the `qemu-img` command. Adjust the path and size (`10G` in the example) as required.

    ```bash
    # Example using a dedicated VM storage directory
    mkdir -p /home/user/GNS3_VMs/SBNB/
    qemu-img create -f qcow2 /home/user/GNS3_VMs/SBNB/persistent_storage.qcow2 10G

    # --- OR ---

    # Example using a GNS3 project directory (replace 'SBNB' if project name differs)
    # mkdir -p /home/user/projects/SBNB/images/
    # qemu-img create -f qcow2 /home/user/projects/SBNB/images/persistent_storage.qcow2 10G
    ```
    This creates an empty (but expandable up to 10GB) QCOW2 file. Remember the path you used.

**Step 2: Attach the Virtual Disk in GNS3 (Recommended Method)**

Modify the SBNB VM *template* in GNS3 so that all instances based on it will have this extra disk.

1.  **Stop the VM:** Ensure any running SBNB VM instances in your GNS3 project are stopped.
2.  **Edit GNS3 Template:**
    *   In GNS3, go to `Edit` -> `Preferences`.
    *   Navigate to `QEMU` -> `QEMU VMs`.
    *   Select your `SBNB` VM template from the list.
    *   Click `Edit`.
3.  **Go to HDD Tab:**
    *   You will see the primary disk (e.g., `sbnb.vhd` or `hda_disk.qcow2`) assigned to `hda`.
    *   Find the next available disk slot, typically `hdb` (Hard disk 2).
    *   **Disk image:** Click `Browse...` and navigate to the `persistent_storage.qcow2` file you created in Step 1. Select it.
    *   **Disk interface:** Choose **`virtio`** for the best performance.
4.  **Apply Changes:** Click `Apply` and then `OK` to close the preferences window.

**(Alternative Attachment Methods)**

*   **Direct QEMU:** Add another `-drive` argument to your `qemu-system-x86_64` command:
    `-drive file=/path/to/persistent_storage.qcow2,format=qcow2,if=virtio`
*   **Virt-Manager:** Use the "Add Hardware" -> "Storage" option in the VM's settings, selecting the `.qcow2` file and setting the bus to `VirtIO`.
*   **GNS3 API:** Adding *subsequent* disks via the `Add-to-GNS3.sh` API is not clearly documented or straightforward. If you initially created the SBNB template using the API, it's recommended to use the GNS3 GUI (as described above) to add the second disk to the existing template.

**Step 3: Initialize and Mount the Disk Inside SBNB VM**

Once the disk is attached via the configuration, start the VM and prepare the disk for use within the SBNB operating system.

1.  **Start the SBNB VM** in GNS3 (or via your chosen method).
2.  **Access the VM:** Connect via SSH or the console.
3.  **Identify the New Disk:** Use `lsblk` to list block devices. The new disk will likely appear as `/dev/vdb` (if using VirtIO and the primary is `/dev/vda`) or possibly `/dev/sdb` (if using SATA). Confirm the size matches what you created (e.g., 10G).
    ```bash
    lsblk
    sudo fdisk -l # Provides more detail
    ```
    *Note: Device names can vary. Always use `lsblk` or similar tools to confirm the correct device identifier.*
4.  **Partition the Disk (Recommended):** Create a partition table and at least one partition. Using `fdisk` for a single partition covering the whole disk:
    ```bash
    sudo fdisk /dev/vdb # Replace /dev/vdb with your identified disk
    ```
    Inside `fdisk`, typically press: `n` (new), `p` (primary), `1` (partition number), `Enter` (default first sector), `Enter` (default last sector), `w` (write and exit). This creates `/dev/vdb1`.
5.  **Format the Partition:** Create a filesystem. `ext4` is common for Linux.
    ```bash
    sudo mkfs.ext4 /dev/vdb1 # Use the partition device, e.g., /dev/vdb1
    ```
6.  **Create a Mount Point:** Make a directory where the storage will be accessible.
    ```bash
    sudo mkdir /mnt/persistent_data # Or choose another name like /data
    ```
7.  **Mount the Partition:**
    ```bash
    sudo mount /dev/vdb1 /mnt/persistent_data
    ```
8.  **(Optional) Set Permissions:** If needed, change ownership so your user can write files.
    ```bash
    # Find the correct user/group within SBNB
    sudo chown $(whoami):$(whoami) /mnt/persistent_data
    ```

The storage is now ready to use at `/mnt/persistent_data`. Files written here will be saved to the `persistent_storage.qcow2` file on your Live Raizo host.

**Step 4: Handling Mounts Across Reboots (Crucial for RAM-based SBNB)**

Since SBNB runs primarily from RAM, changes made to files like `/etc/fstab` *within the running VM* will likely be lost upon reboot. Therefore, simply adding an fstab entry is often unreliable for automounting.

*   **Recommended Initial Approach: Manual Mount:** After each boot of the SBNB VM, manually run the mount command:
    ```bash
    sudo mount /dev/vdb1 /mnt/persistent_data
    ```
*   **Investigate SBNB Startup Mechanisms:** Check the SBNB documentation or explore its filesystem (after mounting the persistent disk) for any specific mechanisms designed to run scripts or commands automatically at boot time (e.g., `/etc/rc.local`, systemd service loading from a specific path, profile scripts). If you find such a mechanism, add the `mount` command there.
*   **Avoid Relying Solely on `/etc/fstab`:** Do not assume an `/etc/fstab` entry inside the VM will work correctly after a reboot unless SBNB has a specific feature to persist or re-apply fstab changes.

You have now successfully added persistent storage to your RAM-based SBNB VM within the Live Raizo/GNS3 environment. Remember to handle the mounting process appropriately for the RAM-based nature of the OS.
