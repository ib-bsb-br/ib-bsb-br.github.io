---
title: "/root/.xsessionrc"
date: 2024-03-10 00:00:00 -03:00
categories:
- Dotfiles
tags:
- linux
comment: 
info: aberto.
type: post
layout: post
sha: 
---

```

#!/bin/sh

# /etc/X11/xinit/xinitrc
#
# global xinitrc file, used by all X sessions started by xinit (startx)

# invoke global X session script
xrandr --output HDMI-1 --auto --above DP-1

xrandr --newmode "1152x864_60.00"   81.75  1152 1216 1336 1520  864 867 871 897 -hsync +vsync
xrandr --newmode "2560x1080_60.00"  230.00  2560 2720 2992 3424  1080 1083 1093 1120 -hsync +vsync

xrandr --addmode DP-1 "1152x864_60.00"
xrandr --addmode HDMI-1 "2560x1080_60.00"

xrandr --output HDMI-1 --mode "2560x1080_60.00"
xrandr --output DP-1 --mode "1152x864_60.00"


```
