---
tags: [scratchpad]
info: aberto.
date: 2025-04-04
type: post
layout: post
published: true
slug: to-enable-video-acceleration-on-rpi4
title: 'to enable video acceleration on RPI4'
---
bibref https://www.dedoimedo.com/computers/rpi4-ubuntu-mate-hw-video-acceleration.html

Markdown Content:
RPI4 & Ubuntu MATE - How to enable video acceleration

Updated: June 27, 2020

Let's fix another problem. This is a big one, and technically speaking, the most important one. Because if you intend to use [Raspberry Pi 4 as a desktop system](https://www.dedoimedo.com/computers/raspberry-pi-4-viable-desktop.html), like I do, then hardware acceleration is a critical component of the overall experience. What this translates to, in layman's terms: smooth video playback with low system resource utilization and less heating.

By default, even the earlier Pi models could play 1080p movies without a problem. This means you ought to get solid results here, too. However, the default configuration is not (currently) optimized for a desktop experience, and we will need to make a few manual changes. Let me show you what you need to do on the system level first - and then how to allow Firefox, Chromium and VLC to use hardware acceleration. After me.

![Image 1: Teaser](https://www.dedoimedo.com/images/computers-years/2020-1/rpi4-ubuntu-mate-hd-video.jpg)

Update system & install libraries
---------------------------------

The first, basic step is to update the system:

sudo apt-get update  
sudo apt-get dist-upgrade

Then, you need to install a few wee libraries:

sudo apt-get install libgles2-mesa libgles2-mesa-dev xorg-dev

Configuration file tweaks
-------------------------

We talked about this in my guide on [how to fix the screen resolution in MATE](https://www.dedoimedo.com/computers/rpi4-ubuntu-mate-fix-screen-resolution.html), where you end up having either black bars top and bottom, or a black border around your desktop, and a weird resolution like 1824x984 instead of full HD 1920x1080. I will briefly repeat some of the stuff, for clarity.

There are two ways you can do this:

*   Using the guided tool called raspi-config. However, it may not be present in MATE or work correctly.
*   Manually change the boot configuration file that is used to setup the system.

I would recommend you go for the manual change, because it also allows you to better understand what you're doing. The boot configuration is stored in the following locations:

*   32-bit Raspberry Pis (up to Model 3) under /boot/config.txt.
*   64-bit Raspberry Pi (Model 4) under /boot/firmware/usercfg.txt.

On Raspberry Pi, /boot/firmware/config.txt also exists, but this file tells you not to write changes to it directly, and to use usercfg.txt. At the bottom of the config.txt file, there's an include statement, which will pull all your manual overrides from the usercfg.txt file. So this is where we want to make the change.

Open the file in a text editor as root or sudo:

sudo nano /boot/firmware/usercfg.txt

Then add the following lines in there:

dtoverlay=vc4-fkms-v3d  
max\_framebuffers=2  
gpu\_mem=128  
hdmi\_enable\_4kp60=1

What we're doing here, we're enabling the 3D video driver (so-called Fake KMS), and we set the memory to 128 MB - please note that Pi 4 does GPU memory management differently from previous models, and since there is a discrete processor for graphics, you don't need as much as you would use on earlier hardware.

Now, there are two other drivers you can try, provided you don't get the hardware acceleration working as you like. So instead of dtoverlay=vc4-fkms-v3d, you can use:

dtoverlay=vc4-kms-v3d

Or this one:

dtoverlay=vc4-kms-v3d-pi4

You can also change the memory allocation for the GPU, but [this is not a trivial topic](https://www.raspberrypi.org/documentation/configuration/config-txt/memory.md). So we won't go into that at this point. Just be aware that you have some flexibility in how much memory you want to allocate. The amount of RAM your Pi has will also play a role in getting the number right. 128 MB ought to be fine.

### Memory splitting and CMA allocation

One more trick you can do is memory splitting. Basically, you can tell how much memory is allocated to the GPU and how much goes to the CPU. Normally, the memory is allocated dynamically, but you can do your own split. What it actually means is that once this value is crossed (in MB), the GPU will either request more memory from the CPU, or relinquish some back - this can lead to potential performance bottlenecks during intense operations, hence the split allows you to pre-optimize for characteristic use cases. You can see this configuration if you run the raspi-config tool, for instance. It allows you to specify how much memory will be given to the CPU (ARM), and how much to the GPU (VideoCore).

![Image 2: Memory split](https://www.dedoimedo.com/images/computers-years/2020-1/rpi4-ubuntu-mate-hw-accel-memory-split.png)

The actual setting is then (either kms or fkms) something like:

dtoverlay=vc4-kms-v3d, cma-128

dtoverlay=vc4-fkms-v3d, cma-128

Reboot & check
--------------

Once your Pi boots again, you can check that 3D drivers are loaded and working:

cat /proc/device-tree/soc/firmwarekms@7e600000/status

cat /proc/device-tree/v3dbus/v3d@7ec04000/status

If these two commands return okay, you have hardware acceleration on. If the result is disabled, try with a different dtoverlay option, reboot, and check again. Please be aware that you may not be able to turn the hardware acceleration on for some reason - kernel version, missing graphics stack utilities, etc. If that happens, just wait until the next system update.

Enable hardware acceleration in Firefox
---------------------------------------

Having your system with hardware acceleration is not enough. You also need to tell individual programs to use it. For whatever reason, neither Firefox nor Chromium have the right flags set by default. In Firefox, you can check the status with about:support. Go to Graphics and check the line that reads Compositing. If the value is Basic, you do not have hardware acceleration enabled.

To override, go to about:config, and search for the following key:

layers.acceleration.force-enabled

![Image 3: Firefox, turn layers on](https://www.dedoimedo.com/images/computers-years/2020-1/rpi4-ubuntu-mate-hw-accel-firefox-turn-layers-on.png)

And toggle it to true. Restart Firefox. Open the about:support page. The Compositing field should have the value OpenGL. Now you can watch videos as intended.

![Image 4: Firefox, Compositing](https://www.dedoimedo.com/images/computers-years/2020-1/rpi4-ubuntu-mate-hw-accel-firefox-compositing.png)

Enable hardware acceleration in Chromium
----------------------------------------

Similarly, if you choose to use Chromium, it will initially report no HW acceleration under chrome://gpu. We can change that through chrome://flags. What you want is Override software rendering list, and change the setting to Enabled.

![Image 5: Chromium, experimental features](https://www.dedoimedo.com/images/computers-years/2020-1/rpi4-ubuntu-mate-hw-accel-chromium-experimental.png)

![Image 6: Chromium, GPU flags](https://www.dedoimedo.com/images/computers-years/2020-1/rpi4-ubuntu-mate-hw-accel-chromium-gpu-flags.png)

Please note that some options will still read Disabled or Software only. This is because some of these are hardware-dependent (if you have say Windows and Nvidia graphics, do the same check, for fun), and some of these depend on OpenGL 3.0. To the best of my knowledge, Raspberry Pi only supports OpenGL 2.1.

Enable hardware acceleration in VLC
-----------------------------------

This is the simplest of the three. Tools \> Preferences. Click on Video. Under Video Settings \> Output, select OpenGL video output. Please note that if you're trying this on a random distribution of choice, or if VLC has not been compiled with OpenGL, this won't work, regardless of what your platform supports.

![Image 7: VLC, OpenGL](https://www.dedoimedo.com/images/computers-years/2020-1/rpi4-ubuntu-mate-hw-accel-vlc-opengl-output.png)

Testing & results
-----------------

And now, you need to actually fire up some nice video content and see what gives.

![Image 8: HD video playback](https://www.dedoimedo.com/images/computers-years/2020-1/rpi4-ubuntu-mate-hd-video.jpg)

Conclusion
----------

I believe that over time, these issues will disappear, and you won't be needing this guide. Well, I hope so. Looking at Ubuntu MATE - but also Raspberry Pi OS, the defaults are not designed with too much focus for desktop use just yet. That's understandable, but for anyone who does seek to use the Pi as an ordinary mouse and keyboard system, this means a lot of extra work.

Hopefully, this tutorial has all the pieces you need to have an enjoyable multimedia experience. In the next article in this series, we will discuss, you guessed it, audio, a second and just as critical component. That would be all for now, stay tuned.

Cheers.