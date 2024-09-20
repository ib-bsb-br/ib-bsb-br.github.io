---
title: Installation of ratpoison in debian/ubuntu
date: 2023-11-10 01:00:00 -02:00
categories:
- Tutorial
tags:
- linux
comment: 
info: aberto.
type: post
layout: post
sha: 
---

How to make Ratpoison your only window manager:

a) Go through the distro installation process as you typically would. Once you reach the desktop, open up a Terminal.

b) Update your system:

```bash
sudo apt-get update && sudo apt-get upgrade
```

c) Install Ratpoison, misc softwares and create the `.ratpoisonrc` file:

```bash
sudo aptitude install ratpoison alsamixergui bpytop brightnessctl catfish dialog gir1.2-xfconf-0 gmrun gsimplecal libfltk1.1 libjs-jquery libjs-sphinxdoc libjs-underscore libxnvctrl0 neofetch python3-dbus python3-dialog python3-pexpect python3-psutil python3-ptyprocess rxvt rxvt-unicode unclutter viewnior brightness-udev chafa fonts-dejavu fonts-ipaexfont-gothic fonts-ipafont-gothic fonts-ipafont-nonfree-jisx0208 fonts-liberation fonts-mona fonts-takao-gothic fonts-umeplus-cl fonts-vlgothic javascript-common libu2f-udev locate mlocate plocate system-config-printer unclutter-startup 9menu cups-pk-helper fonts-ipafont-mincho ghostscript gir1.2-secret-1 gsfonts menu packagekit python3-smbc system-config-printer-udev dmenu fonts-droid-fallback libpaper-utils packagekit-tools fonts-noto-mono gdebi lintian bcc build-essential clang-11 clang-13 clang-9 fakeroot gcc gcc-10 gcc-9 libalgorithm-merge-perl libfile-fcntllock-perl libpackage-stash-xs-perl libref-util-perl libtype-tiny-xs-perl libxml-sax-expat-perl pseudo tcc elks-libc libalgorithm-diff-xs-perl libomp-11-dev libreadonly-perl libref-util-xs-perl llvm-11-dev llvm-13-dev llvm-9-dev
```

[touch ~/.ratpoisonrc](https://ib.bsb.br/ratpoisonrc)

d) Now, you want Ratpoison to be your default session. You can configure this in the `.xinitrc` file in your home directory:

```bash
nano ~/.xinitrc
```

e) If there is no `.xinitrc` file, creating one with the following command:

```bash
touch ~/.xinitrc
```

f) Insert the following line and save the file:

```bash
exec ratpoison
```

g) Give the `.xinitrc` file the necessary permissions:

```bash
chmod +x ~/.xinitrc
```

h) To ensure Ratpoison starts on boot, you need to install `xinit` and `lightdm`, which is a handy and lightweight display manager:

```bash
sudo apt-get install xinit
```

For autologin, edit `lightdm` as follows:

```
1. Open a terminal window.

2. To allow automatic login, you need to edit the 'lightdm.conf' file. If it doesn't exist, you need to create it. Use the following command: `sudo nano /etc/lightdm/lightdm.conf`

3. Add the following lines to the file:

```
[Seat:*]
autologin-user=yourusername
autologin-user-timeout=0
```

Replace 'yourusername' with your actual username.

4. Save the file and exit the editor (in nano, you can do this by pressing `Ctrl+X`, then `Y` to confirm saving changes, then `Enter` to confirm the file name).

5. Restart your system for the changes to take effect.
```


i) If you want to get rid of the existing window managers or desktop environments, starting with GNOME, execute:

```bash
sudo apt-get purge ubuntu-desktop gnome-shell
```

j) Following that, to remove all the related packages and dependencies, use:

```bash
sudo apt-get autoremove
```

k) To check if other desktop environments or window manager are installed, make sure Aptitude is installed:

```bash
sudo apt install aptitude
```

l) Then run a command like this for each potential desktop package:

```bash
aptitude search '?installed(?name(gnome-shell))'
```

Change "gnome-shell" to the package name of the desktop you are searching for. If it returns nothing, the package isn't installed.

m) If you find another installed desktop environment or window manager, substitute "gnome-shell" in the purge command above with the corresponding packages.

n) Now, you need to edit the `/etc/inittab` file to enable automatic login. However, Debian 11 uses `systemd` by default, which doesn't use `/etc/inittab`. Instead, you can create a service to autologin and start `xinit`. First, create a new service file:

```bash
sudo mousepad /etc/systemd/system/autologin@.service
```

Add the following content to this file:

```ini
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin yourusername --noclear %I $TERM
Type=idle

[Install]
WantedBy=multi-user.target
```

Replace 'yourusername' with your actual username.

Save and exit the file.

Now, you should be able to enable the service:

```bash
sudo systemctl enable autologin@.service
```

Finally, reboot your system. It should now automatically log you in and start a ratpoison session.

***

# Create ratpoison.desktop file in /usr/share/xsessions/

```
[Desktop Entry]
Version=1.0
Encoding=UTF-8
Name=ratpoison
Name[en_US]=ratpoison
Comment=Simple and fast window manger
Exec=ratpoison
TryExec=ratpoison
Type=Xsession
[Window Manager]
SessionManaged=true
```

# Make a symbolic link of /usr/bin/ratpoison file in /etc/alternatives/
`sudo ln -s /usr/bin/ratpoison /etc/alternatives/x-window-manager`

`sudo ln -s /usr/bin/ratpoison /etc/alternatives/x-session-manager`
