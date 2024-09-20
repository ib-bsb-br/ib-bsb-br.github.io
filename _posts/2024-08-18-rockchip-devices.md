---
tags:
  - hardware
info: aberto.
date: 2024-08-18
type: post
layout: post
published: true
slug: rockchip-devices
title: 'RockChip devices'
---

URL Source: https://sites.google.com/site/tweakradje/android/rockchip-device

Many Android devices use the RockChip soc these days. I have some using the ARM7 rk3066 dual core. I love it. It is fast but it must come with mali400 gpu. On this page I will try to explain how to customize these devices. Also some tools to do just that are added as downloads to the bottom of this page. I don't use ClockWorkMod recovery much. All can be done with adb and some unix commands.

I use adb on this page. But adb sometimes doesn't recognize newer devices. You can help it by creating a **.android** folder in your windows profile folder. Put **adb\_usb.ini** in there with the USB VID of your device. RockChip has Vendor ID **0x2207**. See adb download below.

You device needs to be rooted (but most are from the factory).

**Backup Backup Backup**

The first thing you do before anything is create a proper backup of your new device. Just common sense.

Creating a backup of your device is very simple. You need an sdcard (or use internal /sdcard partition). From the Short Overview page we now know that Android roms are stored in mtd NAND partitions. So we need to get them to the PC.

After turning on your device manage to get an ADB connection working to your PC and follow these instructions:

*   *   adb shell
        
    *   su (if not pre-rooted)
        
    *   stop
        
    *   cat /proc/mtd
        
    *   copy and paste the content of the output to a text file on your pc
        

mtd0: 00400000 00004000 "misc"

mtd1: 00800000 00004000 "kernel"

mtd2: 01000000 00004000 "boot"

mtd3: 01000000 00004000 "recovery"

mtd4: 18000000 00004000 "backup"

mtd5: 08000000 00004000 "cache"

mtd6: 20000000 00004000 "userdata"

mtd7: 00400000 00004000 "kpanic"

mtd8: 20000000 00004000 "system"

mtd9: 16bc00000 00004000 "user"

*   cat /dev/mtd/mtd0 > /sdcard/mtd0\_misc.img
    
    *   cat /dev/mtd/mtd1 > /sdcard/mtd1\_kernel.img
        
    *   ... do that for all mtd's
        
    *   exit
        

_**Note:**_ "user" is your internal /sdcard partition which size could be up to 12 Gb !!! Do not backup that one, this is the user installed packages and settings :)

Now back on your PC you need to copy them img's to the PC with adb. Create a folder on your pc and use:

*   adb pull /sdcard/mtd0\_misc.img
    
*   adb pull /sdcard/mtd1\_kernel.img
    
*   ... do that for all mtd's
    

For tablet you can also use ClockWorkMod Recovery to do it. I use CWMRecovery\_RK3060\_5.5.0.4 and flash it using flashtool (only flash recovery!)

Even easier is [](https://play.google.com/store/apps/details?id=com.h3r3t1c.onnandbup) [NanDroid Backup](https://play.google.com/store/apps/details?id=com.h3r3t1c.onnandbup). You can install it from the PlayStore and perform a MTD backup on a live device. Choose CWM format.

Now you are safe as you can be and you can start changing some things on your device.

**Restoring**

This shows how to restore your device or flash it with other mtd partitions. There are tools for official RockChip roms. I will attach them below. But on this page I do not use them.

I will show how to restore mtd partitions with unix binary called **flash\_image** on a running device. After that I will show how to do it on a dead device using the fastboot method. Fastboot is a low level Android device state which allows you to write mtd nand partitions too. The official RockChip flasher uses that Android device state too.

**With adb**

You need flash\_image from below. And you need your original mtd images created earlier or other mtd images you want to try. Put your device in adb mode first.

*   *   adb push flash\_image /sdcard
        
    *   adb push mtd0\_misc.img /sdcard/mtd0\_misc.img
        
    *   adb push mtd1\_kernel.img /sdcard/mtd1\_kernel.img
        
    *   ... do that for all mtd's
        
    *   adb shell
        
    *   su (if not pre-rooted)
        
    *   stop
        
    *   busybox cp /sdcard/flash\_image /dev
        
    *   cd /dev
        
    *   chmod 777 fl\*
        
    *   ./flash\_image misc /sdcard/mtd0\_misc.img
        
    *   ./flash\_image kernel /sdcard/mtd1\_kernel.img
        
    *   ... do that for all mtd's
        
    *   cd /data/dalvik-cache
        
    *   rm \*
        
    *   sync
        
    *   reboot
        

The first thing after the reboot is to do a factory reset to wipe the data partition. You will loose all user installed apps and data.

**With fastboot**

When your device is "bricked" you will not be able to get a proper adb connection. There is an escape: **fastboot**. How to enter fastboot on power up is different on every device. But you need to push and hold a button during boot or push and hold a paperclip in the hole. If in fastboot mode you will see a RK30SDK or similar device in your Windows hardware tree. It requires other USB drivers then regular adb. You can get it from the RockChipBatchTool below.

Fastboot is a **Windows utility**. All commands are done from the pc and are similar to that of the unix flash\_image tool described earlier.

example: fastboot flash system mtd8\_system.img

**Wendal.img: Unpack the firmare image (Rockchip\_TOOLS)**

The Rockchip firmware image is packed as one img file containing these partitions (example RK3229 firmware):

boot.img

kernel.img

misc.img

recovery.img

resource.img

system.img

trust.img

uboot.img

You can Pack/Unpack it with the RK3066\_IMG\_Mod\_Tool.zip you can download [](https://www.google.com/url?q=https%3A%2F%2Fgithub.com%2Fronniehd%2Fandroid.projects.ec%2Ftree%2Fmaster%2FMK808%2FRockchip_TOOLS&sa=D&sntz=1&usg=AOvVaw3M2BDJvvk30-gBHBPUPBg2) [here](https://www.google.com/url?q=https%3A%2F%2Fgithub.com%2Fronniehd%2Fandroid.projects.ec%2Ftree%2Fmaster%2FMK808%2FRockchip_TOOLS&sa=D&sntz=1&usg=AOvVaw3M2BDJvvk30-gBHBPUPBg2).

Put your image in the Mod Tool folder and rename it to **wendal.img**

Run the Runme.bat file to Unpack or Pack it. It will be unpacked in the **temp\\Image** folder.

**Unpack the system.img**

You can unpack system.img with [](http://www.google.com/url?q=http%3A%2F%2Fforum.xda-developers.com%2Fshowthread.php%3Ft%3D1921399&sa=D&sntz=1&usg=AOvVaw0pXTRtpPu148sy-dHJFvOH) [EXT4 Unpacker](http://www.google.com/url?q=http%3A%2F%2Fforum.xda-developers.com%2Fshowthread.php%3Ft%3D1921399&sa=D&sntz=1&usg=AOvVaw0pXTRtpPu148sy-dHJFvOH) (or 7-zip now).

**System Mods**

You might want to change some things on your device's system partition. Add some things to your build.prop ( better put them in your own /system/default.prop) or remove/add/update some apk's.

The /system partition is readonly by default. Goto adb shell and mount the partition read-write: **mount -o remount,rw /system**

Some interesting read from Finless [](http://www.google.com/url?q=http%3A%2F%2Fwww.freaktab.com%2Fshowthread.php%3F287-RockChip-ROM-Building-Tips-and-Tricks-by-Finless&sa=D&sntz=1&usg=AOvVaw1PXsFNV1IynPdVXFxKAg-u) [here](http://www.google.com/url?q=http%3A%2F%2Fwww.freaktab.com%2Fshowthread.php%3F287-RockChip-ROM-Building-Tips-and-Tricks-by-Finless&sa=D&sntz=1&usg=AOvVaw1PXsFNV1IynPdVXFxKAg-u).

**Deep Sleep**

On the RK3066 tablets it is common that Deep Sleep system state is not happening. This is because of the ril daemon and a process that provides 3G USB dongle support. If you don't use the 3G USB dongle you are better of with Deep Sleep. In standy your tablet battery last much longer.

The easiest way to kill this problem is to kill the rild process. This process starts as a service from the /init.rc file that belongs to the kernel.

service ril-daemon /system/bin/rild

class main

socket rild stream 660 root radio

socket rild-debug stream 660 radio system

user root

group radio cache inet misc audio sdcard\_r sdcard\_rw log

In a shell you can use this command to stop it each time after a reboot: **stop ril-daemon**

Take a close look at that /init.rc file. You will see that /system/etc/install-recovery.sh is called there like this:

service flash\_recovery /system/etc/install-recovery.sh

class main

oneshot

Now we can create a shell script **/system/etc/install-recovery.sh** that executes stop ril-daemon

#!/system/bin/sh

stop ril-daemon

Of course you can put into the install-recovery script what you want. Most setprop or sysctl commands or even use it for a semi init.d mechanism.

**Changing Wifi and BT drivers**

Leave alone all other mtd's and only concentrate on /system. There are kernels that are in the boot.img but there are also devices that have a small boot.img and the kernel.img is used. In the kernel there is the low level driver for the hardware such as bluetooth, wifi and infrared remote control.

But the Android drivers are loaded by modules or libraries in the /system partition.

Check with dmesg command which hardware you have before you change the system.img. For the wifi chip you can also

**cat /sys/class/rkwifi/chip** (like MT5931)

For changing the Wifi you need to replace or add with that from your original ROM

/system/lib/**libhardware\_legacy.so** (loads proper driver module)

/system/lib/modules/xxxxx.ko (use **lsmod** to find the proper one that is loaded, in case of MT5931 **wlan.ko** is loaded )

/system/etc/firmware/yyyyy (where yyyyy is the file needed for your specific hardware loaded by xxxxx.ko, wlan.ko loads **WIFI\_RAM\_CODE** )

/system/bin/**netd**

/system/bin/**wpa\_supplicant**

For changing Bluetooth you need to replace or add with that of your original ROM

/system/lib/**libbluedroid.so**

/system/lib/**libbluetooth\_mtk.so** (or other for specific hardware, this one it for MT6622 )

/system/etc/firmware/**yyyyy** (in this case /system/etc/firmware/**MTK\_MT6622\_E2\_Patch.nb0** )

/system/bin/**hciattach**

Of course you need to set the proper owner and permissions.

In /system/build.prop you sometimes find these lines to activate the options in the Android Settings app:

ro.version.radiocontrols=1

ro.version.bluetooth=1

ro.version.ethernet=1

You find them by extracting the classes.dex from the Settings.apk file and do a: strings classes.dex|find "ro." (strings is sysinternals windows util)

**Enable multitouch rotate and tilt (jazzhand) on tablet**

On some Rockchip tablets you can only use multitouch zoom, not rotate or tilt. There is an easy fix on your rooted tablet.

Edit the /etc/permissions/android.hardware.touchscreen.multitouch file to read like this and write it back to /etc/permissions folder.

<permissions>

<feature name="android.hardware.faketouch" />

<feature name="android.hardware.touchscreen" />

<feature name="android.hardware.touchscreen.multitouch" />

**<feature name="android.hardware.touchscreen.multitouch.distinct" />**

**<feature name="android.hardware.touchscreen.multitouch.jazzhand" />**

</permissions>

**CrewRKTablets Tablet Roms**

CrewRKTablets is a german group that creates nice tablet roms for RockChip devices. **You only need to flash the system.img and keep kernel** (must be 3.0.8 or higher). They have made CM and JB/AOSP 4.x roms and can be found [](http://www.google.com/url?q=http%3A%2F%2Fcrewrktablets.arctablet.com%2F&sa=D&sntz=1&usg=AOvVaw3U3PCyybtzxMl3XgqFwYaw) [here](http://www.google.com/url?q=http%3A%2F%2Fcrewrktablets.arctablet.com%2F&sa=D&sntz=1&usg=AOvVaw3U3PCyybtzxMl3XgqFwYaw). On [](http://www.google.com/url?q=http%3A%2F%2Fforum.xda-developers.com%2Fshowthread.php%3Ft%3D2108704&sa=D&sntz=1&usg=AOvVaw2PkQmfm_NriXyDLgfVYQ2X) [XDA](http://www.google.com/url?q=http%3A%2F%2Fforum.xda-developers.com%2Fshowthread.php%3Ft%3D2108704&sa=D&sntz=1&usg=AOvVaw2PkQmfm_NriXyDLgfVYQ2X) there are some threads too. Try [](http://www.google.com/url?q=http%3A%2F%2Fcrewrktablets.arctablet.com%2F%3Fp%3D2315&sa=D&sntz=1&usg=AOvVaw2eaoB8zz_7fVoY8LVMWUAg) [AOSP 4.2.2 v3.3](http://www.google.com/url?q=http%3A%2F%2Fcrewrktablets.arctablet.com%2F%3Fp%3D2315&sa=D&sntz=1&usg=AOvVaw2eaoB8zz_7fVoY8LVMWUAg) first (fastest).

But not always your Wifi/Bluetooth/Rotation sensor ([fix](http://www.google.com/url?q=http%3A%2F%2Fforum.xda-developers.com%2Fshowpost.php%3Fp%3D46532663%26postcount%3D619&sa=D&sntz=1&usg=AOvVaw0cBeoX-MhH8YPcEDYA0KXD)) is supported by default. But you can find fixes there or on the xda thread.

The rotation sensor is **/system/lib/hw/sensors/sensors.rk30board.so**

Sometimes you internal SD card is not recognized. That can be [](http://www.google.com/url?q=http%3A%2F%2Fforum.xda-developers.com%2Fshowpost.php%3Fp%3D48004974%26postcount%3D736&sa=D&sntz=1&usg=AOvVaw1dlU6Hyw_wCPJZps25-oCa) [fixed](http://www.google.com/url?q=http%3A%2F%2Fforum.xda-developers.com%2Fshowpost.php%3Fp%3D48004974%26postcount%3D736&sa=D&sntz=1&usg=AOvVaw1dlU6Hyw_wCPJZps25-oCa) with reformatting it FAT32 directly again after flashing.

If e.g. your internal sdcard (mtd called user) is mtd9:

0x0000eb400000-0x0003db800000 : "user" mtd9 /sdcard (FAT) internal

mkdosfs -F 32 /dev/block/mtdblock9

and reboot.