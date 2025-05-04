---
tags:
- scratchpad
info: aberto.
date: 2025-05-04
type: post
layout: post
published: true
slug: live-raizo-commands
title: Live Raizo - Commands
comment: https://sourceforge.net/p/live-raizo/wiki/Commands/
---


Network
-------

fast-ip
-------

*   Configuration of IP address and eventually the gateway.
*   fast-ip, fast-dhcp and fast-dns used together enable to setup a dynamic DNS.
*   When it sets an interface to vlan, the mother of the interface (if it was down) is set to "manual" mode
*   To use it, you must be root or in the group "sudo"

### _Synopsis_

*   fast-ip \[INTERFACE-NAME\]\[INTERFACE-NUMBER\]\[:SUB-INTERFACE\]\[.VLAN-NUMBER\] IP-ADDRESS/NET-MASK \[IP-GATEWAY\]
*   fast-ip \[INTERFACE-NAME\]\[INTERFACE-NUMBER\]\[:SUB-INTERFACE\]\[.VLAN-NUMBER\] dhcp
*   fast-ip \[INTERFACE-NAME\]\[INTERFACE-NUMBER\]\[:SUB-INTERFACE\]\[.VLAN-NUMBER\] manual

### _Examples_

*   fast-ip 172.16.40.17/24
    *   enp1s0 : 172.16.40.17/24
*   fast-ip 1 172.16.40.17/24
    *   enp1s1 : 172.16.40.17/24
*   fast-ip 2 172.16.40.17/24 172.16.40.254
    *   enp1s2 : 172.16.40.17/24 and gateway : 172.16.40.254
*   fast-ip 3 dhcp
    *   enp1s3 requests an IP to a DHCP server
*   fast-ip 0.10 172.16.40.17/24 172.16.40.254
    *   vlan 10 on enp1s0 : 172.16.40.17/24 and gateway : 172.16.40.254
*   fast-ip virbr0 172.16.40.17/24 172.16.40.254
    *   virbr0 : 172.16.40.17/24 and gateway : 172.16.40.254
*   fast-ip enp1s0.10 172.16.40.17/24 172.16.40.254
    *   vlan 10 on enp1s0 : 172.16.40.17/24 and gateway : 172.16.40.254
    *   if enp1s0 was down, enp1s0 is set to manual mode
*   fast-ip 0:1 172.16.40.17/24 172.16.40.254
    *   sub interface 1 of enp1s0 : 172.16.40.17/24 and gateway : 172.16.40.254

* * *

fast-dhcp
---------

*   Configuration of a DHCP server based on the IP address of the server.
*   fast-dhcp configures the dnsmasq server
*   [fast-ip](https://sourceforge.net/p/live-raizo/wiki/Commands/#fast-ip), fast-dhcp and [fast-dns](https://sourceforge.net/p/live-raizo/wiki/Commands/#fast-dns) used together enable to setup a dynamic DNS.
*   You can change the default domain (domain.lan.) used by fast-dhcp and [fast-dns](https://sourceforge.net/p/live-raizo/wiki/Commands/#fast-dns) by
    *   modifying the variable FAST\_DOMAIN in /opt/raizo/etc/fast.conf
    *   exporting the variable FAST\_DOMAIN :

```
exportFAST_DOMAIN="yournewdomain.org"
```

*   To use fast-dhcp, you must be root or in the group "sudo"

### _Synopsis_

*   fast-dhcp \[-g\] \[-d\] \[INTERFACE-NAME\]INTERFACE-NUMBER\[:SUB-INTERFACE\]\[.VLAN-NUMBER\] \[IP-DNS\]
    *   \-g : the dhcp server doesn't propagate the gateway
    *   \-d : the dhcp server doesn't propagate the DNS

By default :

*   IP-DNS is IP address of nameserver found in /etc/resolv.conf. If it doesn't find it, it uses the IP address of INTERFACE-NUMBER
*   The default gateway of dhcp clients is the default gateway of the network of chosen interface, or IP address of INTERFACE-NUMBER

### _Examples_

*   fast-dhcp 2 172.16.4.3
    *   if IP address of enp1s2 is 192.168.33.17
        *   create pool of IP addresses : 192.168.33.\[10,100\]/24
        *   gateway of dhcp clients can be 192.168.33.17
        *   DNS of dhcp clients will be 172.16.4.3
*   fast-dhcp enp1s2
    *   if IP address of enp1s2 is 192.168.33.17
        *   create pool of IP addresses : 192.168.33.\[10,100\]/24
        *   gateway of dhcp clients can be 192.168.33.254
        *   DNS of dhcp clients will be 192.168.33.17

* * *

fast-dns
--------

*   Configuration of a DNS server.
*   fast-dns configures the dnsmasq server
*   if name is not ended by a dot, fast-dns adds to name the default domain (domain.lan.)
*   [fast-ip](https://sourceforge.net/p/live-raizo/wiki/Commands/#fast-ip), [fast-dhcp](https://sourceforge.net/p/live-raizo/wiki/Commands/#fast-dhcp) and fast-dns used together enable to setup a dynamic DNS.
*   You can change the default domain (domain.lan.) used by [fast-dhcp](https://sourceforge.net/p/live-raizo/wiki/Commands/#fast-dhcp) and fast-dns by
    *   modifying the variable FAST\_DOMAIN in /opt/raizo/etc/fast.conf
    *   exporting the variable FAST\_DOMAIN :

```
exportFAST_DOMAIN="yournewdomain.org"
```

*   To use fast-dns, you must be root or in the group "sudo"

### _Synopsis_

*   fast-dns NAME IP \[NAME2 IP2 \[NAME3 IP3 \[NAME4 IP4...\]\]\]
    *   Creates a DNS server (if necessary), and adds the record for theirs IPs and theirs NAMEs
*   fast-dns dns
    *   Clears the previous records of the DNS server and creates a new one.

### _Examples_

*   fast-dns PC1 10.0.0.1
    *   For the server DNS, PC1.domain.lan. has the IP 10.0.0.1
*   fast-dns PC2.other.local**.** 10.0.0.2
    *   For the server DNS, PC1.domain.lan. has the IP 10.0.0.1 and PC2.other.local. has the IP 10.0.0.2
*   fast-dns PC3 10.0.0.3 PC4.other.local**.** 10.0.0.4
    *   For the server DNS, PC1.domain.lan. has the IP 10.0.0.1, PC2.other.local. has the IP 10.0.0.2, PC3.domain.lan. has the IP 10.0.0.3 and PC4.other.local. has the IP 10.0.0.4
*   fast-dns PC2.other.local**.** 10.0.0.4
    *   For the server DNS, PC1.domain.lan. has the IP 10.0.0.1, PC2.other.local. has the IP 10.0.0.4, PC3.domain.lan. has the IP 10.0.0.3 and PC4.other.local. has the IP 10.0.0.4
*   fast-dns dns
    *   Reset records of the DNS server

* * *

fast-rip
--------

*   RIPv2 router configuration for IPv4 and IPv6
*   fast-rip configures the [FRRouting](https://frrouting.org/) server
*   To use it, you must be root or in the group "sudo"

* * *

fast-proxy-on
-------------

*   Configure shell variables, sudo config and Docker to use the proxy
*   Use configuration of /etc/resolv.conf to exclude networks from proxy
*   By default, use the proxy "proxy:8080"
*   if user is not root or in sudo group, fast-proxy-on does only the commands that doesn't need to have root power

### _Synopsis_

*   fast-proxy-on \[IP:PORT\]
    *   \[IP:PORT\] : use IP:PORT as proxy

* * *

fast-proxy-off
--------------

*   Remove configuration of [fast-proxy-on](https://sourceforge.net/p/live-raizo/wiki/Commands/#fast-proxy-on)
*   if user is not root or in sudo group, fast-proxy-off does only the commands that doesn't need to have root power

* * *

fast-http
---------

*   Start a web server on the port 80 and share a directory (by default : "/home/user")
*   CTRL+C to stop it

### _Synopsis_

*   fast-http \[SharedFolder\]
    *   \[SharedFolder\] : the folder to share. By default : "/home/user"

* * *

fast-vwifi
----------

### On LiveRaizo

*   [Enable the virtual wifi 802.11](https://sourceforge.net/p/live-raizo/wiki/Virtual%20WIFI%20802.11/)
*   Use and configure the program [vwifi](https://github.com/Raizo62/vwifi)
*   The command must be start on LiveRaizo
*   You can change MAC address prefixes by modifying the variable VWIFI\_PREFIX\_MAC\_ADDRESS

```
exportVWIFI_PREFIX_MAC_ADDRESS="94:95:96"
```

*   fast-vwifi can't be use in the same time as [fast-wifi-docker](https://sourceforge.net/p/live-raizo/wiki/Commands/#fast-wifi-docker)

#### _Synopsis_

*   fast-vwifi \[NUMBER\_WIFI\_INTERFACE\]
    *   \[NUMBER\_WIFI\_INTERFACE\] : Number of wifi interfaces wlan must be created

### On Debian VM

*   [Enable the virtual wifi 802.11](https://sourceforge.net/p/live-raizo/wiki/Virtual%20WIFI%20802.11/)
*   Use and configure the program [vwifi](https://github.com/Raizo62/vwifi)
*   The command must be start on each VM Debian
*   You can change MAC address prefixes by modifying the variable VWIFI\_PREFIX\_MAC\_ADDRESS
*   with the optional parameter "-s", you set the IP of vwifi-server, and use the TCP protocol.

```
exportVWIFI_PREFIX_MAC_ADDRESS="94:95:96"
```

#### _Synopsis_

*   fast-vwifi \[NUMBER\_WIFI\_INTERFACE\] -s \[IP\_SERVER\]
    *   \[NUMBER\_WIFI\_INTERFACE\] : Number of wifi interfaces wlan must be created ( <\= 10)
    *   \-s \[NUMBER\_WIFI\_INTERFACE\] : Set the IP address of server and use the TCP protocol.

* * *

fast-wifi-docker
----------------

*   Add a wlan interfaces to Docker VM
*   The command must be start on LiveRaizo
*   You can change MAC address prefixes by modifying the variable VWIFI\_PREFIX\_MAC\_ADDRESS

```
exportVWIFI_PREFIX_MAC_ADDRESS="94:95:96"
```

*   fast-wifi-docker can't be use in the same time as [fast-vwifi](https://sourceforge.net/p/live-raizo/wiki/Commands/#fast-vwifi)

### _Synopsis_

*   fast-wifi-docker \[-y\] \[-a\] \[-r\] \[-m\] \[-n Number\] \[-c NumberWlanToCreate\] \[NameOfVM1\] \[NameOfVM2\] \[NameOfVM3\] \[NameOfVM...\]
    *   \-y|Y|o|O : don't ask for confirmation from user to add wlan
    *   \-a|A : select all the VMs
    *   \-r|R : set a random MAC address to wlan interfaces
    *   \-m|M : enable the monitor mode for wlan0 of LiveRaizo
    *   \-n|N Number : number of wlan interfaces by VM
    *   \-c|C NumberWlanToCreate : number of wlan interfaces to create, if it is not enough

### _Examples_

*   fast-wifi-docker
    *   Display the VM Devices availables and ask the number of the VM. fast-wifi-docker ask for confirmation before to add a wlan interface to the Virtual Machines selected.
*   fast-wifi-docker -Y
    *   Display the VM Devices availables and ask the number of the VM. fast-wifi-docker do not ask for confirmation to add a wlan interface to the Virtual Machines selected.
*   fast-wifi-docker AP1
    *   Ask for confirmation before to add a wlan interface to the Virtual Machine "AP1".
*   fast-wifi-docker -Y Client1
    *   Add a wlan interface to the Virtual Machine "Client1".
*   fast-wifi-docker -Y PC1 PC2 Server5
    *   Add a wlan interface to the Virtual Machines "PC1", "PC2" and "Server5"

* * *

* * *

System
------

fast-rescan-interfaces
----------------------

*   Scan to detect new plugged network interfaces, and update the files /etc/network/interfaces, history of Zsh/Bash

* * *

fast-syslog
-----------

*   Displays in color the last 40 lines of the file /var/log/syslog

* * *

fast-mount-usb
--------------

*   Mount the USB key in the directory /media/usb0. If /mnt/usb0 is already used, fast-mount-usb will use /mnt/usb1, etc

### _Synopsis_

*   fast-mount-usb \[-q\]
    *   \-q|Q : quiet mode : show only the mounted point and the label
    *   \-h|H|? : show this help

* * *

fast-battery
------------

*   Display the percentage of energy remaining in the battery.
    *   Try to bring the console windows to the front if percentage of energy remaining is less of 10%, and if the battery is detected and not charging

### _Synopsis_

*   fast-battery \[-i\] \[-t\] \[-p\] \[-u\]
    *   \-i|I : checks this percentage every 60 seconds and displays the changes
    *   \-t|T : show this percentage in the title bar of xterm
    *   \-p|P : do a pause before to stop the program
    *   \-u|U : test of utility. exit 0 only if usefull : battery detected
    *   \-h|H|? : show this help

* * *

fast-console-resize
-------------------

*   Recalculate the console size
*   Useful with DDebian in Web-UI

* * *

* * *

Laboratory
----------

fast-save-project
-----------------

*   Asks questions to save a GNS3 project

### _Synopsis_

*   fast-save-project \[-h\] \[options\]
    *   \-h : show usefull parameters of [fast-backup-lab](https://sourceforge.net/p/live-raizo/wiki/Commands/#fast-backup-lab)
    *   \[options\] is totally used with [fast-backup-lab](https://sourceforge.net/p/live-raizo/wiki/Commands/#fast-backup-lab)

### _Steps_

1.  Show detected projects of GNS3 in /home/user/projects and ask which you want to save. For each project, it shows his current size.
2.  Launch [fast-mount-usb](https://sourceforge.net/p/live-raizo/wiki/Commands/#fast-mount-usb) to detect new usb keys connected
3.  Show destinations where to copy the backup of project
    *   For each usb key, it shows the free space on the total space.
4.  Do the backup with [fast-backup-lab](https://sourceforge.net/p/live-raizo/wiki/Commands/#fast-backup-lab)
5.  Run associated command with destination
6.  If destination is usb, ask to umount the usb key

### _Your own commands_

*   You can add your own destination and associated commands in /opt/raizo/etc/cmd-fast-save-project.conf
*   Line is commented if it begins with #
*   Each line must be : _title_ \[_command_ _options_\]
    
    *   title : title shown by fast-save-project in the step where you must choose the destination
    *   _command options_ : if it is not empty, the command "_command options_" is launched after the backup
    *   In _command options_, use "%f" for name of archive
*   You can use more functionality if title begins with "local:", "net:" or "usb:",
    
    *   local:_directory_ : Before to run [fast-backup-lab](https://sourceforge.net/p/live-raizo/wiki/Commands/#fast-backup-lab), it verifies that _directory_ exists
    *   net:_title_ : Before to run [fast-backup-lab](https://sourceforge.net/p/live-raizo/wiki/Commands/#fast-backup-lab), it verifies that it has an IPv4 address
    *   usb:_mountPoint_ :
        *   Before to run [fast-backup-lab](https://sourceforge.net/p/live-raizo/wiki/Commands/#fast-backup-lab), it verifies that _mountPoint_ is already mounted
        *   After the backup in _mountPoint_, fast-save-project asks if it musts unmount _mountPoint_
*   Example of /opt/raizo/etc/cmd-fast-save-project.conf
    

```
# Copy into /mnt/archive and ask to unmount /mnt/archive
usb:/mnt/archive
# Copy into /tmp and show details on archive
local:/tmpls-l%f
# Copy on the FTPs server : srvftp.domain.local
net:ftpsecho-n"Login : "&&readLOGIN&&lftp-u$LOGIN-e"set ftp:ssl-protect-data true ; put '%f'; exit"srvftp.domain.local
# Copy on the ssh server srvssh.domain.local
net:sshecho-n"Login : "&&readLOGIN&&scp%f${LOGIN}@srvssh.domain.local:
```

* * *

fast-backup-lab
---------------

*   Backup of the GNS3 project with configuration of GNS3, Qemu,....

### _Synopsis_

*   fast-backup-lab \[-g\] \[-p\] \[-s\] \[-w\] \[-d\] \[-c\] \[-f\] \[-l\] \[-n\] \[-a\] \[-t\] \[-y\] \[DIRECTORY-PROJECT-GNS3\] \[DIRECTORY-DESTINATION\]
    *   Creates an archive of the directory "DIRECTORY-PROJECT-GNS3". This archive is created in the directory "DIRECTORY-DESTINATION"
    *   \-g|G : exclude the configurations files of GNS3 from archive
    *   \-p|P : exclude the GNS3 project from archive
    *   \-s|S : exclude the Startups files from archive
    *   w|W : exclude the backup of the vwifi's state
    *   \-d|D : ADD the Default config of devices
    *   \-c|C : ADD the Capture files from archive
    *   \-f|F : ADD the Firewall rules
    *   \-l|L : ADD the sysctl config
    *   \-n|N : ADD the network configuration
    *   \-a|A : ADD the same as : -f -l -n
    *   \-t|T : test only the config. Don't create the archive
    *   \-y|Y|o|O : Don't ask for confirmation from user
    *   \-h|H|? : show this help

### _Examples_

*   fast-backup-lab TP
    *   Create an archive TP\_backup\_20130723\_12\_20\_10.tar.xz
*   fast-backup-lab TP /media/usb0
    *   Create an archive /media/usb0/TP\_backup\_20130723\_12\_23\_05.tar.xz
*   fast-backup-lab -P  
    \+ Create an archive config\_backup\_20130723\_12\_29\_43.tar.xz with only the configurations files

* * *

fast-restore-lab
----------------

*   Restore a GNS3 project, which has been saved with [fast-backup-lab](https://sourceforge.net/p/live-raizo/wiki/Commands/#fast-backup-lab) or [fast-save-project](https://sourceforge.net/p/live-raizo/wiki/Commands/#fast-save-project)
*   By default, the GNS3 project is restored in the directory /home/user/projects
*   fast-restore-lab refuses to restore a saved config of GNS3 if it is incompatible with the installed GNS3. This restriction can be bypassed with the "-g" option
*   The existence of the "/opt/raizo/etc/disable\_output\_log.lock" file automatically activates the "-e" option

### _Synopsis_

*   fast-restore-lab \[-g\] \[-p\] \[-s\] \[-w\] \[-d\] \[-c\] \[-f\] \[-l\] \[-n\] \[-v\] BACKUP-PROJECT-GNS3
    *   \-g|G : don't extract the configurations files of GNS3 from archive
    *   \-p|P : don't extract the GNS3 project from archive
    *   \-s|S : don't extract the Startups files from archive
    *   w|W : exclude the startup of vwifi
    *   \-d|D : exclude the Default config of devices
    *   \-c|C : exclude the Captured packets
    *   \-f|F : exclude the Firewall rules of Live from archive
    *   \-l|L : exclude the sysctl config of Live from archive
    *   \-n|N : don't extract the network files of Live from archive
    *   \-u|U : use the current directory to receive the GNS3 project
    *   \-e|E : output only the error messages
    *   \-v|V : only verify if the current version of VMRaizo is compatible
    *   \-h|H|? : show this help

### _Example_

*   fast-restore-lab TP\_backup\_20130723\_12\_20\_10.tar.xz
    *   Restores files from the archive TP\_backup\_20130723\_12\_20\_10.tar.xz
*   fast-restore-lab -s TP\_backup\_20130723\_12\_20\_10.tar.xz
    *   Restores files from the archive TP\_backup\_20130723\_12\_20\_10.tar.xz, without restoring Startups files

* * *

fast-reset-vm
-------------

*   Reset the QEmu devices :
    *   The Hard Disks of the QEmu device return to their initials states
*   fast-reset-vm must be used when a project of GNS3 is open
*   It loads the credential of GNS3 from /opt/raizo/etc/gns3.conf

### _Synopsis_

*   fast-reset-vm \[-a\] \[-y|-o\] \[NAME-VM1\] \[NAME-VM2\] \[NAME-VM3\] \[NAME-VM...\]
    
    *   \-a|-A : Select all the VMs
    *   \-y|-Y|-o|-O : Don't ask for confirmation from user
    *   NAME-VM : reset only the VM "NAME-VM1", "NAME-VM2", "NAME-VM3"...
    *   \-h|H|? : show this help
*   fast-reset-vm is case insensitive on the name "NAME-VM" if there are no doubt on the choose.
    

### _Examples_

*   fast-reset-vm
    *   Display the VM Devices availables and ask the number of the VM. fast-reset-vm ask for confirmation before to reset the Virtual Machines selected.
*   fast-reset-vm -Y
    *   Display the VM Devices availables and ask the number of the VM. fast-reset-vm do not ask for confirmation to reset the Virtual Machines selected.
*   fast-reset-vm Router1
    *   Ask for confirmation before to reset the Virtual Machine "Router1".
*   fast-reset-vm -Y Server1
    *   Reset the Virtual Machine "Server1".
*   fast-reset-vm -Y PC1 PC2 Server5
    *   Reset the Virtual Machines "PC1", "PC2" and "Server5"

* * *

fast-clean-crash-gns3
---------------------

*   Kill all the processes used by GNS3 (in case of a crash for instance).

### _Synopsis_

*   fast-clean-crash-gns3 \[-y|-o\] \[-h\]
    *   \-y|-Y|-o|-O : Don't ask for confirmation from user
    *   \-h|H|? : show this help

### _Examples_

*   fast-clean-crash-gns3
    *   Ask for confirmation before to kill all the processes used by GNS3.
*   fast-clean-crash-gns3 -Y
    *   Kill all the processes used by GNS3.

* * *

fast-nat
--------

*   enable IP forwarding, configure an DHCP Server and an DNS Server and use NAT with packets coming out of the virbr0 interface

### _Synopsis_

*   fast-nat \[-d\] \[-n\] \[-i\] \[-s\] \[IP-ADDRESS\]
    *   \-d : disable the DHCP service
    *   \-n : disable the DNS service
    *   \-i : don't run iptables rules
    *   \-s : don't start the sysctl config
    *   if virbr0 has an IP, and IP-ADDRESS is not defined, then fast-nat uses the IP of virbr0
    *   if virbr0 has no IP, and IP-ADDRESS is not defined, then fast-nat uses the IP 10.145.147.1
    *   if IP-ADDRESS is defined, then fast-nat uses this IP and modifies with it the IP of virbr0

### _Example_

```
>fast-nat
*fast-ipvirbr010.145.147.1/24
+[/etc/network/interfaces:Addthenewconfigurationforvirbr0]
*sudoifupvirbr0
*fast-dnsdns
+[/etc/Raizo.dnsmasq.hosts:Createthefile]
+[/etc/dnsmasq.d/Raizo.DNS.conf:Configurationoftheserver]
*sudosystemctlstartdnsmasq
*sudosystemctlenablednsmasq
Synchronizingstateofdnsmasq.servicewithSysVservicescriptwith/lib/systemd/systemd-sysv-install.
Executing:/lib/systemd/systemd-sysv-installenablednsmasq
*fast-dhcpvirbr010.145.147.1
# Pool          : 10.145.147.[10,100]/24
# Gateway       : 10.145.147.1
# DNS           : 10.145.147.1
-----------------------------
*sudosystemctlstopdnsmasq
+[/etc/dnsmasq.d/Raizo.DHCP.conf:Addpool10.145.147.[10,100]/24]
*sudosystemctlstartdnsmasq
*sudosysctlnet.ipv4.ip_forward=1
net.ipv4.ip_forward=1
*sudoiptables-tmangle-IPREROUTING-ivirbr0-jMARK--set-mark0xd001
*sudoiptables-tnat-IPOSTROUTING-mmark--mark0xd001-jMASQUERADE
```

* * *

fast-vwifi-update-gns3
----------------------

*   Update the server "vwifi" with the geographical coordinates of each VM from GNS3
    
*   vwifi-server ([fast-vwifi](https://sourceforge.net/p/live-raizo/wiki/Commands/#fast-vwifi)) must be started before
    
*   fast-vwifi-update-gns3 must be used when a project of GNS3 is open
*   fast-vwifi-update-gns3 update only the coordinate of the VMs which use the VHOST protocol
*   It loads the credential of GNS3 from /opt/raizo/etc/gns3.conf

* * *

fast-gns3-server
----------------

*   Start the gns3server.
*   Without parameter, gnsserver is started in foreground. CTRL+C to stop it.
*   It loads the credential of GNS3 from /opt/raizo/etc/gns3.conf
*   If gns3server is already started by gns3-gui, then gns3server becomes accessible from external IPs.

### _Synopsis_

*   fast-gns3-server \[-r\] \[-s\] \[-d\]
    *   r|R : run the service gns3-server (sudo systemctl start gns3-server.service)
    *   s|S : stop the service gns3-server (sudo systemctl stop gns3-server.service)
    *   \-d|D : display if gns3server is running

* * *

[Add-to-GNS3.sh](https://sourceforge.net/p/live-raizo/wiki/API_Add-to-GNS3.sh/)
-------------------------------------------------------------------------------

* * *

* * *

Update
------

fast-startup
------------

*   Mount automatically the USB key in /media/usb0 (or usb1, usb2..) and processes the script /media/usb0/raizo.sh.

### _Synopsis_

*   fast-startup \[NAME-SCRIPT\]
    
    *   By default, NAME-SCRIPT is raizo.sh. NAME-SCRIPT will always be lowercase before downloading.
    *   You can modify default values in the file /opt/raizo/etc/fast-startup.conf
    *   Your script raizo.sh (or NAME-SCRIPT) can affect a value different of zero at the variable FAST\_ERROR\_RAIZO to indicate an error at fast-startup. You can use the variable FAST\_ERROR\_RAIZO\_LOG to indicate also a message
    *   You can use the variable MOUNT\_KEY to know where the usb key is mounted

### _Examples_

*   fast-startup
    *   Mount automatically the USB key in /media/usb0 and processes the script /media/usb0/raizo.sh.
*   fast-startup US
    *   Mount automatically the USB key in /media/usb0 and processes the script /media/usb0/us.

* * *

fast-update
-----------

*   Download the file on a web server and processes it.

### _Synopsis_

*   fast-update \[-s WEB-SERVER\] \[NAME-SCRIPT\]
    
    *   By default, NAME-SCRIPT is raizo.sh. NAME-SCRIPT will always be lowercase before downloading.
    *   By default, WEB-SERVER is UpdateRaizo.
    *   You can modify the default values in the file /opt/raizo/etc/fast-startup.conf
    *   Your script raizo.sh (or NAME-SCRIPT) can affect a value different of zero at the variable FAST\_ERROR\_RAIZO to indicate an error at fast-update. You can use the variable FAST\_ERROR\_RAIZO\_LOG to indicate also a message.

### _Examples_

*   fast-update
    *   Download the file [http://UpdateRaizo/raizo.sh](http://updateraizo/raizo.sh) and processes it.
*   fast-update WIN
    *   Download the file [http://UpdateRaizo/win](http://updateraizo/win) and processes it.
*   fast-update -s 88.89.90.91 WIN
    *   Download the file [http://88.89.90.91/win](http://88.89.90.91/win) and processes it.

* * *

* * *

Helps
-----

fast-memo
---------

*   Display a reminder

### _Synopsis_

*   fast-memo \[-t\] \[NAME-MEMO\]
    *   \-t|T : Show the name of memo in the title bare of xterm
    *   \-h|H|? : show this help
    *   NAME-MEMO : Show the reminder "NAME-MEMO". If none NAME-MEMO is indicated then fast-memo shows all reminders available. You must indicate the number of memo that you want display

### _Keys to interact_

*   "q" to quit (as less command)
*   "/" to search a word. It ignores case, except if any uppercase letters appear in the search pattern
    *   "n" to find the next word
    *   "shift+n" the find the previous word

### _Examples_

```
>fast-memo
Availablechoices:
1)*QUIT*24)diff47)mkdir70)sockstat
2)7z25)dig48)mount71)sort
3)ab26)distcc49)mysql72)split
4)apparmor27)emacs50)mysqldump73)ssh
5)apt-cache28)find51)ndiswrapper74)ssh-copy-id
6)apt-get29)gcc52)netcat75)ssh-keygen
7)aptitude30)gdb53)netstat76)stdout
8)asterisk31)git54)nmap77)strace
9)at32)GNS355)notify-send78)systemctl
10)awk33)gpg56)od79)tail
11)bash34)grep57)openssl80)Tap
12)Bridge35)gs58)pdftk81)tar
13)chmod36)head59)php82)tcpdump
14)chown37)history60)ping83)tmux
15)Cisco38)ifconfig61)ps84)top
16)convert39)ip62)python85)truncate
17)crontab40)iptables63)rm86)uname
18)curl41)iwconfig64)Routage87)vim
19)cut42)less65)sam2p88)Vlan
20)date43)ln66)scp89)wget
21)dd44)ls67)screen90)WiFi
22)df45)lsof68)sed
23)dhclient46)MAC69)shred
#?
```

```
>fast-memopi
(Fromcheat/https://github.com/chrisallenlane/cheat)

# ping a host with a total count of 15 packets overall.
ping-c15www.example.com

# ping a host with a total count of 15 packets overall, one every .5 seconds (faster ping).
ping-c15-i.5www.example.com

# test if a packet size of 1500 bytes is supported (to check the MTU for example)
ping-s1500-c10-Mdowww.example.com
```