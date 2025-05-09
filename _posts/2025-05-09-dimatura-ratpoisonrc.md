---
tags: [linux>dotfile]
info: aberto.
date: 2025-05-09
type: post
layout: post
published: true
slug: dimatura-ratpoisonrc
title: 'dimatura .ratpoisonrc'
---
bibref https://raw.githubusercontent.com/dimatura/dot_ratpoison/refs/heads/master/.ratpoisonrc

{% codeblock %}
# vim: commentstring=#%s

# replacement for this hack: set PATH in .profile
# setenv PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/home/dmaturan/bin

# start up progs ***********************************************#{{{

## misc daemons
#exec gnome-power-manager
#exec gnome-settings-daemon
#exec cinnamon-settings-daemon
#exec nm-applet
#exec urxvtd -q -o -f

## widgets
# set bg
exec xsetroot -solid gray8 -cursor_name left_ptr
# conky status monitor
#exec conky
# also: alpha 128, monitor
#exec trayer --align left --edge top --distance 0 --expand true --transparent true --SetDockType true --SetPartialStrut true --height 14 --width 50 --widthtype percent
# MIT coords
#exec redshift -l 40.44:-80.0
#exec redshift -l 42.35391379569696:-71.09029769897461

## ui
#exec easystroke
# set up keyboard layout switching (press both shifts)
#exec setxkbmap -option grp:switch,grp:shifts_toggle,grp_led:scroll us,es
# also run xmodmap
#exec xmodmap ~/.Xmodmaprc
# thinkpad button
#exec tpb -d

#unmanage rpbar
#exec rpbar
unmanage panel

#exec ssh-add .ssh/id_rsa
#exec daemon mpdas
#}}}

# appearance/ui ***************************************************#{{{

set startupmessage 0
set border 2
# left top right bottom, leave px for bars
#set padding 0 14 0 13
set padding 0 14 0 0
#set padding 0 28 0 0

# bar at south and middle, fits well with 15 padding at bottom
set bargravity c
set barpadding 4 4
# some colors:
# DarkTurquoise, lightskyblue, Gold, Goldenrod, Lavender,
# LightSlateGray, LightSteelBlue, PowderBlue, SkyBlue, palegreen
# DarkSeaGreen, Navy, MidnightBlue, DarkSlateGray, gray12
set bgcolor #6a9fb5
set fgcolor #151515
# from vim mustang colorthem
# set fwcolor #b1d631
set fwcolor #d28445

#set font -*-snap-*-*-*-*-*-*-*-*-*-*-*-*
#set font -*-terminus-*-*-*-*-20-*-*-*-*-*-*-*
#set font -*-terminus-medium-r-normal-*-14-*-*-*-*-*-*-*
set font -*-helvetica-*-r-*-*-*-*-*-*-*-*-*-*
set inputwidth 600
set historysize 1000

set msgwait 1
# don't move mouse cursor around
set warp 0

#}}}

# hooks ********************************************************#{{{

# get rid of mouse cursor
# addhook key banish

# for rpbar
#addhook switchwin exec rpbarsend
#addhook switchframe exec rpbarsend
#addhook switchgroup exec rpbarsend
#addhook deletewindow exec rpbarsend
#addhook titlechanged exec rpbarsend
#addhook newwindow exec rpbarsend

#addhook switchwin exec ratpoison -c "windows %n %t%s" > /tmp/rpbarfifo
#addhook switchframe exec ratpoison -c "windows %n %t%s" > /tmp/rpbarfifo
#addhook switchgroup exec ratpoison -c "windows %n %t%s" > /tmp/rpbarfifo
#addhook deletewindow exec ratpoison -c "windows %n %t%s" > /tmp/rpbarfifo
# TODO use this
# echo -e "`ratpoison -c "windows %n %t%s"`\00"

#addhook switchwin exec echo r > /tmp/rpbarfifo
#addhook switchframe exec echo r > /tmp/rpbarfifo
#addhook switchgroup exec echo r > /tmp/rpbarfifo
#addhook deletewindow exec echo r > /tmp/rpbarfifo

# kill programs there should be only one of
addhook restart exec killall conky
#addhook restart exec killall rpbar
#addhook restart exec killall redshift
addhook quit exec killall conky
#addhook quit exec killall rpbar
#addhook quit exec killall redshift

# verbose group switching
addhook switchgroup groups
#addhook switchwin windows %n %c %t

#}}}

# aliases ******************************************************#{{{
#alias ipython exec urxvt -e ipython
alias ipythonq exec ipython-qtconsole
alias bpython exec urxvt -e bpython
alias firefox exec firefox
#alias chromium exec chromium-browser
alias chrome exec google-chrome
alias mc exec urxvt -e mc
alias mocp exec urxvt -e mocp
alias ncmpc exec urxvt -e ncmpc -c
alias alsamixer exec urxvt -e alsamixer
#alias wicd exec wicd-client -n
alias vimwiki exec gvim ~/repos/notes/vimwiki/index.wiki
alias bash exec urxvt -e bash
alias fmlove exec fmlove.sh
alias shell exec urxvt -e

#}}}

# key bindings *************************************************#{{{

# escape key
escape C-a

bind Return nextscreen
#abort key sequence
bind Escape abort
# TODO interactive group selection with dwm or something like it
bind g groups
bind semicolon colon

# example of creating keymap
#newkmap ctrl-x
#definekey ctrl-x n next

# running apps#{{{

# TODO consider execa, execf
# TODO see archlinux wiki for various dwm-based launchers
bind space exec dmenu_run
bind e colon exec gvim
bind c exec urxvt -e fish
unbind b
bind b exec urxvt -e bash
#bind b exec urxvt -e st
# execute in terminal; "!" used to be for execute,
# but dmenu is better for that
unbind exclam
bind exclam colon exec urxvt -e
# i is 'info' but I don't use it
unbind i
bind i exec urxvt -e ipython
#bind c exec urxvt -is +sb -fg '#51a366' -bg '#111111' -fn 'xft:DejaVu Sans Mono:pixelsize=11:antialias=false:autohinting=true'
#}}}

# window management#{{{

bind W exec dratmenu.py
# a window selector using rpselect
#bind w exec rpselect
# a window selector using ratmen
#bind w exec ratmenwin
bind w exec dratmenu.py
bind C-w exec dratmenu.py

# some vi-like bindings
bind v hsplit
bind s split
bind q remove
bind o only

bind j focusdown
bind h focusleft
bind l focusright
bind k focusup
#bind j exec ratpy focus down
#bind h exec ratpy focus left
#bind l exec ratpy focus right
#bind k exec ratpy focus up

bind J exchangedown
bind K exchangeup
bind H exchangeleft
bind L exchangeright

bind r resize
bind R resize
#bind Q kill
bind Q delete

# workspaces
#definekey top s-F1 rpws1
#definekey top s-F2 rpws2
#definekey top s-F3 rpws3
#definekey top s-F4 rpws4
#definekey top s-F5 rpws5

# just go with raw groups for now
# TODO start with 1?
definekey top s-F1 gselect 0
definekey top s-F2 gselect 1
definekey top s-F3 gselect 2
definekey top s-F4 gselect 3
definekey top s-F5 gselect 4
definekey top s-F6 gselect 5

#definekey top s-F1 sselect 0
#definekey top s-F2 sselect 1
#definekey top s-F3 sselect 2

#definekey top s-Left prevscreen
#definekey top s-Right nextscreen
definekey top s-Return nextscreen

#}}}

# music and audio#{{{

# 'm' is bound to last message by default but I don't use that
unbind m
bind m exec st -e ncmpcpp
#bind greater exec mpc next
#bind less exec mpc prev
#bind slash exec mpc toggle
bind greater exec pytify -n
bind less exec pytify -p
bind slash exec pytify -pp

#volume bindings
# chose these F-keys because they correspond to fn-keys in eee.
#bind F10 exec amixer sset PCM toggle
#bind F11 exec bin/ratpy_audio.py amixer_volume -
#bind F12 exec bin/ratpy_audio.py amixer_volume +
bind F11 exec bin/ratpy_audio.py pamixer_volume -
bind F12 exec bin/ratpy_audio.py pamixer_volume +

#}}}

# links to window key#{{{
# use describekey to find these !!
definekey top s-n link n
definekey top s-p link p
definekey top s-b link b
definekey top s-j link j
definekey top s-k link k
definekey top s-l link l
definekey top s-h link h
definekey top s-o link o
definekey top s-q link q
definekey top s-w link w
definekey top s-x link x
definekey top s-r link r
definekey top s-r link R
definekey top s-s link s
definekey top s-v link v
#definekey top s-u link u
definekey top s-0 link 0
definekey top s-1 link 1
definekey top s-2 link 2
definekey top s-3 link 3
definekey top s-4 link 4
definekey top s-5 link 5
definekey top s-6 link 6
definekey top s-7 link 7
definekey top s-8 link 8
definekey top s-9 link 9
definekey top s-S link S
definekey top s-N link N
definekey top s-P link P
# audio controls
definekey top s-F10 link F10
definekey top s-F11 link F11
definekey top s-F12 link F12
# a couple of important keys
definekey top s-space link space
definekey top s-Return link Return
#}}}

# rat emulation#{{{

definekey top s-Up ratrelwarp 0 -15
definekey top s-Down ratrelwarp 0 15
definekey top s-Left ratrelwarp -15 0
definekey top s-Right ratrelwarp 15 0
definekey top s-Menu ratclick 1

#definekey top Home ratrelwarp 0 -15
#definekey top End ratrelwarp 0 15
#definekey top Delete ratrelwarp -15 0
#definekey top Next ratrelwarp 15 0
# weird menu key. Also possible: Insert, Backslash. KP_Insert, asterisk
#definekey top s-Menu ratclick 1

#}}}

#}}}
{% endcodeblock %}