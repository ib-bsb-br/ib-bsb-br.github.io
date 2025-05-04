---
tags:
- scratchpad
info: aberto.
date: 2025-05-04
type: post
layout: post
published: true
slug: live-raizo-api_add-to-gns3sh
title: Live Raizo - API_Add-to-GNS3.sh
comment: https://sourceforge.net/p/live-raizo/wiki/API_Add-to-GNS3.sh/
---


Explanations
------------

*   **Add-to-GNS3.sh** : API who uses a disk files from QEmu/Docker/Dynamips/VirtualBox to create VM and to add them to GNS3

* * *

Load the API
------------

```
source/opt/raizo/api/Add-to-GNS3.sh
```

* * *

Generic Functions
-----------------

VM
--

### Modify-ConfigVM

To modify the created config of VM

*   Modify-ConfigVM 1 2 3
    *   1 : Name of file returned by [Create-VMQEmu](https://sourceforge.net/p/live-raizo/wiki/API_Add-to-GNS3.sh/#create-vmqemu) or [Create-VMDocker](https://sourceforge.net/p/live-raizo/wiki/API_Add-to-GNS3.sh/#create-vmdocker)
    *   2 : Name of the parameter to change
    *   3 : New value of the parameter to change

### Add-ConfigVM-to-GNS3

To add config of VM to GNS3

*   Add-ConfigVM-to-GNS3 1
    *   1 : Name of file returned by [Create-VMQEmu](https://sourceforge.net/p/live-raizo/wiki/API_Add-to-GNS3.sh/#create-vmqemu)

You must create the md5sum file of the hard disk before to call Add-ConfigVM-to-GNS3

Network
-------

### Create-NetworkConfig

To create a specific network configuration

*   Create-NetworkConfig 1 2 3
    *   1 : Number of network card
    *   2 : Template (example : enp0s)
    *   3 : Type (example : e1000)
*   Type : the value must be in $TYPES\_NETWORK\_CARD[\[@\]](https://sourceforge.net/p/live-raizo/wiki/%40) : "e1000", "i82550", "i82551", "i82557a", "i82557b", "i82557c", "i82558a", "i82558b", "i82559a", "i82559b", "i82559c", "i82559er", "i82562", "i82801", "ne2k\_pci", "pcnet", "rtl8139", "virtio-net-pci"

### Modify-NetworkConfig

To modify a specific network configuration created with [Create-NetworkConfig](https://sourceforge.net/p/live-raizo/wiki/API_Add-to-GNS3.sh/#create-networkconfig)

*   Modify-NetworkConfig 1 2 3 4
    *   1 : File with config of Network Interfaces (returned by [Create-NetworkConfig](https://sourceforge.net/p/live-raizo/wiki/API_Add-to-GNS3.sh/#create-networkconfig))
    *   2 : The network card number : 0 1 ...
    *   3 : Field to modify : examples : port\_name / adapter\_type
    *   4 : New value of the field

### Add-NetworkConfig-to-VM

To add a specific network configuration created with [Create-NetworkConfig](https://sourceforge.net/p/live-raizo/wiki/API_Add-to-GNS3.sh/#create-networkconfig) to a VM config created with [Create-VMQEmu](https://sourceforge.net/p/live-raizo/wiki/API_Add-to-GNS3.sh/#create-vmqemu) or [Create-VMDocker](https://sourceforge.net/p/live-raizo/wiki/API_Add-to-GNS3.sh/#create-vmdocker)

*   Add-NetworkConfig-to-VM 1 2
    *   1 : File with config of New VM
    *   2 : File with config of Network Interfaces (returned by [Create-NetworkConfig](https://sourceforge.net/p/live-raizo/wiki/API_Add-to-GNS3.sh/#create-networkconfig))

* * *

QEmu
----

Global Variables
----------------

### To change parameter of commands

*   TYPE\_HARD\_DISK : To change the type of the hard disk of VM
    *   Possibles values in $TYPES\_HARD\_DISK[\[@\]](https://sourceforge.net/p/live-raizo/wiki/%40) : "ide", "sata", "scsi", "sd", "mtd", "floppy", "pflash", "virtio", "none"
    *   Default value in variable : DEFAULT\_TYPE\_HARD\_DISK
    *   ( Default value : sata )
*   TYPE\_NETWORK\_CARD : To change the type of the network interfaces of VM
    *   Possibles values in $TYPES\_NETWORK\_CARD[\[@\]](https://sourceforge.net/p/live-raizo/wiki/%40) : "e1000", "i82550", "i82551", "i82557a", "i82557b", "i82557c", "i82558a", "i82558b", "i82559a", "i82559b", "i82559c", "i82559er", "i82562", "i82801", "ne2k\_pci", "pcnet", "rtl8139", "virtio-net-pci"
    *   Default value in variable : DEFAULT\_TYPE\_NETWORK\_CARD
    *   ( Default value : e1000 )
*   SYMBOL\_QEMU : To change the default symbol of the QEmu device in GNS3
    *   Default value in variable : DEFAULT\_SYMBOL\_QEMU
    *   ( Default value : /symbols/qemu\_guest.svg )
*   OPTION\_QEMU : Option to use with [Create-VMQEmu](https://sourceforge.net/p/live-raizo/wiki/API_Add-to-GNS3.sh/#create-vmqemu) : To add options to the QEmu VM
    
    *   Default value in variable : DEFAULT\_OPTION\_QEMU
    *   ( default value : "" )
    *   Use also the read-only variables :
        *   OPTION\_QEMU\_9P\_HOSTHOME : configure the share of /home/user with the 9P protocol.
        *   OPTION\_QEMU\_VWIFI : configure the VHOST protocol used by vwifi-client of [vwifi](https://github.com/Raizo62/vwifi)
*   if a variable is unset, the functions initialise it to this default value.
    

### To test the success of the commands

*   When the commands failed because the parameters used are incorrects
    *   FAST\_ERROR\_RAIZO is set to a value different of zero
    *   FAST\_ERROR\_RAIZO\_LOG contains the message error

Functions
---------

### Create-VMQEmu

To create the configuration of a Qemu VM

*   Create-VMQEmu 1 2 3 4 5 \[6\] \[7\] \[8\] \[9\]
    *   1 : Name Of VM in GNS3
    *   2 : Number of network card
    *   3 : Size of Memory in MB
    *   4 : Type of Access : telnet / spice / spice+agent / vnc / none
    *   5 : Shutdown by ACPI : true / false
    *   6 : If exist, path of the disk file 1
    *   7 : If exist, path of the disk file 2
    *   8 : If exist, path of the disk file 3
    *   9 : If exist, path of the disk file 4

This function returns the name of the temporary file to use with [Add-ConfigVM-to-GNS3](https://sourceforge.net/p/live-raizo/wiki/API_Add-to-GNS3.sh/#add-configvm-to-gns3)

_Examples_
----------

### Windows Server 2019

```
#!/usr/bin/bash

source/opt/raizo/api/Add-to-GNS3.sh
if(($?))
then
return
fi

DIR_VDI="/media/usb0/vdi"

# Windows Server 2019

SYMBOL_QEMU="/symbols/raizo/microsoft_server.svg"

# On Processor AMD Ryzen, you should perhaps add :
# OPTION_QEMU="-cpu pentium2"

ConfigVM=$(Create-VMQEmuWin201912048spicefalse"${DIR_VDI}/windows-2019-server.vhd")
if[-n"${ConfigVM}"]
then
Add-ConfigVM-to-GNS3"${ConfigVM}"
fi
```

### Windows 10

```
#!/usr/bin/bash

source/opt/raizo/api/Add-to-GNS3.sh
if(($?))
then
return
fi

DIR_VDI="/media/usb0/vdi"

SYMBOL_QEMU="/symbols/raizo/microsoft_guest.svg"

# On Processor AMD Ryzen, you should perhaps add :
# OPTION_QEMU="-cpu pentium2"

ConfigVM=$(Create-VMQEmuWin1011024spicefalse"${DIR_VDI}/windows-10.vdi")
if[-n"${ConfigVM}"]
then
NetworkConfig=$(Create-NetworkConfig1"loc-area-con-"e1000)
Modify-NetworkConfig"${NetworkConfig}"0port_name"loc-area-con-2"
Add-NetworkConfig-to-VM"${ConfigVM}""${NetworkConfig}"

Add-ConfigVM-to-GNS3"${ConfigVM}"
fi
```

### Kali Linux

```
#!/usr/bin/bash

source/opt/raizo/api/Add-to-GNS3.sh
if(($?))
then
return
fi

DIR_VDI="/media/usb0/vdi"

SYMBOL_QEMU="/symbols/raizo/hacker.svg"

TYPE_HARD_DISK="IDE"

# OPTION_QEMU_9P_HOSTHOME : Use 9P to share /home/user via hosthome : mount -t 9p hosthome /mnt
# OPTION_QEMU_VWIFI : To use the virtual wifi after installing and running vwifi-client from https://github.com/Raizo62/vwifi
OPTION_QEMU="${OPTION_QEMU_9P_HOSTHOME}${OPTION_QEMU_VWIFI}"

ConfigVM=$(Create-VMQEmuKaliLinux21024spicefalse"${DIR_VDI}/linux-kali-2022.3-amd64.vmdk")
if[-n"${ConfigVM}"]
then
Add-ConfigVM-to-GNS3"${ConfigVM}"
fi

unsetTYPE_HARD_DISKOPTION_QEMUSYMBOL_QEMU
```

### ASA

```
#!/usr/bin/bash

source/opt/raizo/api/Add-to-GNS3.sh
if(($?))
then
return
fi

DIR_VDI="/media/usb0/vdi"

TYPE_HARD_DISK='ide'
SYMBOL_QEMU='/symbols/asa.svg'
OPTION_QEMU='-no-kvm -icount auto'

ConfigVM=$(Create-VMQEmuASA61024telnetfalse"${DIR_VDI}/ASA/FLASH")
if[-n"${ConfigVM}"]
then
Modify-ConfigVM"${ConfigVM}"initrd"${DIR_VDI}/ASA/asa842-initrd.gz"
Modify-ConfigVM"${ConfigVM}"kernel_command_line'ide_generic.probe_mask=0x01 ide_core.chs=0.0:980,16,32 auto nousb console=ttyS0,9600 bigphysarea=65536 ide1=noprobe no-hlt -net nic'
Modify-ConfigVM"${ConfigVM}"kernel_image"${DIR_VDI}/ASA/asa842-vmlinuz"
Modify-ConfigVM"${ConfigVM}"port_name_format'GigaEthernet{0}'

Modify-ConfigVM"${ConfigVM}"category'firewall'

Add-ConfigVM-to-GNS3"${ConfigVM}"
fi

unsetTYPE_HARD_DISKOPTION_QEMUSYMBOL_QEMU
```

* * *

Docker
------

Global Variables
----------------

### To change parameter of commands

*   SYMBOL\_DOCKER : To change the default symbol of the Docker device in GNS3
    
    *   Default value in variable : DEFAULT\_SYMBOL\_DOCKER
    *   ( Default value : /symbols/docker\_guest.svg )
*   if you unset a variable, the functions initialise it to this default value.
    

### To test the success of the commands

*   When the commands failed because the parameters used are incorrects
    *   FAST\_ERROR\_RAIZO is set to a value different of zero
    *   FAST\_ERROR\_RAIZO\_LOG contains the message error

Functions
---------

### Add-PersistentFolder-to-VMDocker

To add a folder to the list of persistent folders of the Docker VM

*   Add-PersistentFolder-to-VMDocker 1 2
    *   1 : File with config of New VM
    *   2 : Name of folder to set persistent

### Create-VMDocker

To create the configuration of a Docker VM

*   Create-VMDocker 1 2 3 4
    *   1 : Name Of VM in GNS3
    *   2 : Name of the Docker Image
    *   3 : Number of network card
    *   4 : Type of Access : telnet / http / https / vnc / none

This function returns the name of the temporary file to use with [Add-ConfigVM-to-GNS3](https://sourceforge.net/p/live-raizo/wiki/API_Add-to-GNS3.sh/#add-configvm-to-gns3)

_Examples_
----------

### Alpine

```
#!/usr/bin/bash

source/opt/raizo/api/Add-to-GNS3.sh
if(($?))
then
return
fi

# alpine :

dockerpullalpine

SYMBOL_DOCKER="/symbols/computer.svg"

ConfigVM=$(Create-VMDockeralpine"alpine:latest"1telnet)
if[-n"${ConfigVM}"]
then
Add-PersistentFolder-to-VMDocker"${ConfigVM}""/etc/ssl"
Add-ConfigVM-to-GNS3"${ConfigVM}"
fi
```

* * *

Dynamips
--------

_Examples_
----------

### Cisco C7200

```
#!/usr/bin/bash

source/opt/raizo/api/Add-to-GNS3.sh
if(($?))
then
return
fi

cat>"c7200.gns3"<<EOF
        {
            "name": "c7200",
            "default_name_format": "R{0}",
            "usage": "ConsoleType=Cisco",
            "image": "c7200-advipservicesk9-mz.152-4.S5.bin",
            "symbol": ":/symbols/router.svg",
            "category": "router",
            "startup_config": "/opt/raizo/user/Config/GNS3/configs/Raizo_ios_base_startup-config.txt",
            "private_config": "",
            "console_type": "telnet",
            "console_auto_start": false,
            "platform": "c7200",
            "idlepc": "0x62cf0330",
            "idlemax": 500,
            "idlesleep": 30,
            "exec_area": 64,
            "mmap": true,
            "sparsemem": true,
            "ram": 512,
            "nvram": 512,
            "mac_addr": "",
            "disk0": 0,
            "disk1": 0,
            "auto_delete_disks": true,
            "system_id": "FTX0945W0MY",
            "compute_id": "local",
            "slot0": "C7200-IO-FE",
            "slot1": "PA-2FE-TX",
            "slot2": "",
            "slot3": "",
            "slot4": "",
            "slot5": "",
            "slot6": "",
            "midplane": "vxr",
            "npe": "npe-400",
            "template_id": "8b3b55a3-3644-4fc9-a494-b525165a2603",
            "template_type": "dynamips",
            "builtin": false
        }
EOF
cp"c7200.gns3"/tmp/c7200.gns3

Add-ConfigVM-to-GNS3/tmp/c7200.gns3
```