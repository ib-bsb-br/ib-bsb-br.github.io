---
title: Linux typewriter setup
date: 2022-11-22 01:00:00 -02:00
categories:
- Tutorial
tags:
- linux
comment: https://tedz.eu/Linux%20typewriter%20notes.html
info: aberto.
type: post
layout: post
sha: 
---

# Core features
- Boots straight into text editor - no login, no GUI, no X.Org.
- Provide syncing (wirelessly to cloud, via QR code a la Pomera, USB key / SD card, email, or whatever)

# Setup
In Debian Live:

```
mkdir live
cd live/
#lb config
#lb config --architectures i386
lb config -a i386 -k 686-pae
echo "jed console-setup" >> config/package-lists/my.list.chroot

mkdir -p config/includes.chroot/etc/skel
cat << EOF >> config/includes.chroot/etc/skel/.bash_login
#!/bin/sh
# Ted Burke - Typewriter Linux - 9-Oct-2022
# Boot straight into text editor in terminal
jed
nano
EOF

mkdir -p config/hooks/live
cat << EOF > config/hooks/live/typewriter.hook.chroot
#!/bin/sh
# Ted Burke - Typewriter Linux - 9-Oct-2022
# Configure console font size
echo 'FONTSIZE="16x32"' >> /etc/default/console-setup
EOF
chmod 755 config/hooks/live/typewriter.hook.chroot

sudo lb build

sudo cp live-image-i386.hybrid.iso /dev/sdb
sudo sync
```

# To-do list
- Configure GRUB: bypass boot menu, splashscreen?
- Automatically connect to wifi?
- QR code transfer of typed text to phone. (Use e.g. fim / fbi to display QR code in terminal?)
- Boot settings: keyboard layout, timezone, user-default-groups for USB drive access?
- Modify .bash_login to launch text editor with filename specified?
