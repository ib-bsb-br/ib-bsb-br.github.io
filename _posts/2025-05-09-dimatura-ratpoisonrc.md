---
tags: [scratchpad,linux>dotfile]
info: aberto.
date: 2025-05-09
type: post
layout: post
published: true
slug: ratpoisonrc
title: "ratpoisonrc dot files"
---
{% raw %}
# kkantadas
`https://raw.githubusercontent.com/kkantadas/dotfiles/refs/heads/main/.ratpoisonrc`

```
exec /usr/bin/rpws init 2 -k

if egrep -iq 'touchpad' /proc/bus/input/devices; then
exec   synclient VertEdgeScroll=1 &
exec   synclient TapButton1=1 &
exec xsetroot -cursor_name left_ptr > /dev/null &
#exec redshift &
#exec xset r rate 250 25 &
#exec ./bin/conky.sh & ratpoison -c "set padding 0 15 0 0" & sleep 10s && killall conky ; ratpoison -c "set padding 0 0 0 0" > /dev/null &
#addhook switchwin exec rpthumb
#addhook quit exec rpexpose --clean
#bind v exec rpselect

#addhook switchwin banish
#exec unclutter -idle 1 -jitter 3 -root
#warp on

#RP commands
#aliasarestart "exec ratpoison -c 'restart ~/.config/ratpoison/.ratpoisonrc'"
#set chdir ~/.config/ratpoison/

set bgcolor grey1
set fgcolor grey
#set fwcolor black
set fwcolor #2f2f2f
set bwcolor #1f1f1f
#set bwcolor black

set barborder 0
set border 2

set bargravity n
#set padding 0 0 0 0
#set font fixed-6
#set resizeunit 1
set historysize 100
set historycompaction 1
startup_message off
set wingravity n#ne
#set winliststyle row
#set winfmt %t
#set inputwidth 800

##KeyBindings
newkmap   super-x
#definekey super-x d     exec 'exec' # exec dmenu_run > /dev/null &
#definekey super-x d     exec rofi -show drun -theme dmenu
#definekey super-x d     exec rofi -theme flat-orange -font "hack 11" -show drun
definekey super-x l      exec ./bin/lapower.sh
definekey super-x j      exec urxvt -e alsamixer 
definekey super-x space  exec ./bin/split.sh
definekey super-x R      exec ratpoison -c restart
definekey super-x D      exec dmenumount
#definekey super-x p     exec ./bin/mptest.sh
definekey super-x c      exec dratmenu
definekey top s-x        readkey super-x
definekey super-x Q      exec ratpoison -c quit
definekey super-x e      exec emacs
definekey super-x E      exec emacs -q -l ~/Emacs-project/init.el
#definekey super-x m     exec  urxvt -e mutt > /dev/null &


definekey super-x 1    exec  ratpoison -c "frestore `tail -n 1 .config/ratframe/ratframe1`" ;  ratpoison -c next
definekey super-x 2    exec  ratpoison -c "frestore `tail -n 1 .config/ratframe/ratframe2`" ;  ratpoison -c next
definekey super-x 3    exec  ratpoison -c "frestore `tail -n 1 .config/ratframe/ratframe3`" ;  ratpoison -c next
definekey super-x 4    exec  ./bin/rat-frame4.sh
definekey super-x 5    exec  ./bin/rat-frame5.sh
definekey super-x 6    exec  ./bin/rat-frame6.sh
definekey super-x 7    exec   transset-df 0.7
definekey super-x 8    exec   transset-df 0.8
definekey super-x 9    exec   transset-df 0.9
definekey super-x 0    exec   transset-df 1.0
definekey super-x "apostrophe"  exec ./bin/wifi.sh
definekey super-x F1   exec ratpoison -c "hsplit 21/29" -c focusleft -c "hsplit " -c focusleft -c "resize -190 0" -c  exchangeright
definekey super-x x   exec rat-ranger &
definekey super-x X   exec urxvt -e ranger &
#definekey super-x w exec chromium --process-per-site
definekey super-x w exec rat-or-raise firefox &
definekey super-x m exec scrot -e 'convert $f label:"%x %X" -append $f'
# exec sh ~/.fehbg &

#definekey super-x v  exec ./bin/conky.sh & sleep 9s && killall conky
#definekey super-x v   exec ./bin/conky.sh & ratpoison -c "set padding 0 15 0 0" & sleep 25s && killall conky ; ratpoison -c "set padding 0 0 0 0" &
#definekey super-x t   exec ratpoison -c "setenv fs1 `ratpoison -c 'fdump'`"

#restore the frame layout in slot #1
definekey super-x p exec ratpoison -c "frestore `tail -n 1 .config/ratframe/fsPing`" & urxvt -e ping -c4 google.com && ratpoison -c undo
#definekey super-x p exec ratpoison -c "vsplit 12/13" -c focusdown &  urxvt -e ping -c4 google.com  && ratpoison -c undo
#definekey super-x p exec ratpoison -c "echo `ping -c2 google.com | grep data`"
#definekey super-x C exec ratpoison -c "echo Connecting Ethernet `con` "
definekey super-x r exec ratpoison -c "frestore `ratpoison -c 'getenv fs1'`"
definekey super-x s exec ratpoison -c "vsplit 5/6" -c focusdown
definekey super-x S exec ratpoison -c "vsplit 5/6" -c focusdown & urxvt  
definekey super-x f exec xterm -e w3m -B

definekey super-x l exec ratpoison -c fdump > dump

definekey super-x f exec xterm -e w3m -B
definekey super-x h exec urxvt -e htop &

definekey super-x Down exec xrandr -o normal &
definekey super-x Left exec xrandr -o right &
definekey super-x Right exec xrandr -o left &

#definekey super-x a exec ratpoison -d :0.0 -c "echo Batt `acpi -b|cut -c-11-25` `acpi -t` `date`"
definekey super-x a exec ratpoison -d :0.0 -c "echo `~/bin/ping-check.sh` Net: `cat /sys/class/net/enp2s0f1/operstate` @  Wifi: `cat /sys/class/net/wlan0/operstate /sys/class/net/wlp3s0/operstate` `iw wlan0 info |grep ssid|cut -c6-50` @ Bat:`acpi -b |cut -c11-27` @  Mem: `free -h | grep Mem | cut -c27-30` @ Themp:`acpi -t|cut -c15-19`°C @ `date -R|cut -c18-22` `date|cut -c1-10`"
#: `connmanctl state|grep State|cut -c11-19`
definekey super-x G exec urxvt -e vim Vedatxt/Bhagavat-Gita/Bhagavad-Gita.txt &
definekey super-x K exec urxvt -e less Vedatxt/A.C.Bhaktivadanta\ Swami\ Prabhupada/Krsna_Book.txt &
definekey super-x B exec urxvt -e ranger Vedatxt/Srimad\ Bhagavatam/ &
definekey super-x V exec urxvt -e ranger Vedatxt &

bind k exec ratpoison -c focusup
bind j exec ratpoison -c focusdown 
bind h exec ratpoison -c focusleft
bind l exec ratpoison -c focusright
bind C-k exec ratpoison -c exchangeup
bind C-j exec ratpoison -c exchangedown
bind C-h exec ratpoison -c exchangeleft
bind C-l exec ratpoison -c exchangeright

bind C exec urxvt -bg grey -fg black & sleep 0.3 && transset-df -a 0.7
bind s exec ratpoison -c  vsplit -c focusdown
bind parenright exec ratpoison -c "frestore `tail -n 1 .config/ratframe/dump`" & sleep 0.6s && sudo systemctl suspend  

bind S exec ratpoison -c  hsplit -c focusright
bind O exec ratpoison -c kill 
bind o exec ratpoison -c delete
exec /usr/bin/rpws init 2 -k

if egrep -iq 'touchpad' /proc/bus/input/devices; then
exec   synclient VertEdgeScroll=1 &
exec   synclient TapButton1=1 &
exec xsetroot -cursor_name left_ptr > /dev/null &
#exec redshift &
#exec xset r rate 250 25 &
#exec ./bin/conky.sh & ratpoison -c "set padding 0 15 0 0" & sleep 10s && killall conky ; ratpoison -c "set padding 0 0 0 0" > /dev/null &
#addhook switchwin exec rpthumb
#addhook quit exec rpexpose --clean
#bind v exec rpselect

#addhook switchwin banish
#exec unclutter -idle 1 -jitter 3 -root
#warp on

#RP commands
#aliasarestart "exec ratpoison -c 'restart ~/.config/ratpoison/.ratpoisonrc'"
#set chdir ~/.config/ratpoison/

set bgcolor grey1
set fgcolor grey
#set fwcolor black
set fwcolor #2f2f2f
set bwcolor #1f1f1f
#set bwcolor black

set barborder 0
set border 2

set bargravity n
#set padding 0 0 0 0
#set font fixed-6
#set resizeunit 1
set historysize 100
set historycompaction 1
startup_message off
set wingravity n#ne
#set winliststyle row
#set winfmt %t
#set inputwidth 800

##KeyBindings
newkmap   super-x
#definekey super-x d     exec 'exec' # exec dmenu_run > /dev/null &
#definekey super-x d     exec rofi -show drun -theme dmenu
#definekey super-x d     exec rofi -theme flat-orange -font "hack 11" -show drun
definekey super-x l      exec ./bin/lapower.sh
definekey super-x j      exec urxvt -e alsamixer 
definekey super-x space  exec ./bin/split.sh
definekey super-x R      exec ratpoison -c restart
definekey super-x D      exec dmenumount
#definekey super-x p     exec ./bin/mptest.sh
#definekey super-x c      exec xterm  -e 'rm -rfv ~/{.cache/{/google-chrome/Default/,common-lisp/,gstreamer-1.0/,vimb/WebKitCache},  .cache/yay/,.local/share/webkitgtk,.pki/} ;read'
#definekey super-x c      exec xterm -e 'rm -rfv .cache/mozilla/firefox/3s57yr41.default-release/{thumbnails/,cache2/,weave/logs/,storage/default} .cache/yay/ .local/share/webkitgtk .pki/ .mozilla/firefox/3s57yr41.default-release/{thumbnails/,cache2/,weave/logs/,storage/default/} ;read'
definekey super-x c      exec xterm -e 'rm -rfv .cache/mozilla/firefox/3s57yr41.default-release/{thumbnails/,cache2/,weave/logs/,storage/default} .cache/yay/ .local/share/webkitgtk .pki/ . ;read'
definekey top s-x        readkey super-x
definekey super-x Q      exec ratpoison -c quit
definekey super-x e      exec emacs
#definekey super-x m     exec  urxvt -e mutt > /dev/null &


definekey super-x 1    exec  ratpoison -c "frestore `tail -n 1 .config/ratframe/ratframe1`" ;  ratpoison -c next
definekey super-x 2    exec  ratpoison -c "frestore `tail -n 1 .config/ratframe/ratframe2`" ;  ratpoison -c next
definekey super-x 3    exec  ratpoison -c "frestore `tail -n 1 .config/ratframe/ratframe3`" ;  ratpoison -c next
definekey super-x 4    exec  ./bin/frame4.sh
definekey super-x 5    exec  ./bin/frame5.sh
definekey super-x 6    exec  ./bin/frame6.sh
definekey super-x 7    exec   transset-df 0.7
definekey super-x 8    exec   transset-df 0.8
definekey super-x 9    exec   transset-df 0.9
definekey super-x 0    exec   transset-df 1.0
definekey super-x "apostrophe"  exec ./bin/wifi.sh
definekey super-x F1   exec ratpoison -c "hsplit 21/29" -c focusleft -c "hsplit " -c focusleft -c "resize -190 0" -c  exchangeright
definekey super-x x    exec urxvt -e ranger &
definekey super-x m    exec scrot -e 'convert $f label:"%x %X" -append $f'
# exec sh ~/.fehbg &

#definekey super-x v  exec ./bin/conky.sh & sleep 9s && killall conky
#definekey super-x v   exec ./bin/conky.sh & ratpoison -c "set padding 0 15 0 0" & sleep 25s && killall conky ; ratpoison -c "set padding 0 0 0 0" &

#definekey super-x t   exec ratpoison -c "setenv fs1 `ratpoison -c 'fdump'`"

#restore the frame layout in slot #1
definekey super-x p exec ratpoison -c "frestore `tail -n 1 .config/ratframe/fsPing`" & urxvt -fn "xft:monaco:pixelsize=10" -e ping -c4 google.com && ratpoison -c undo
#definekey super-x p exec ratpoison -c "frestore `tail -n 1 .config/ratframe/fsPing`" & urxvt -e ping -c4 google.com && ratpoison -c undo

#definekey super-x p exec ratpoison -c "vsplit 12/13" -c focusdown &  urxvt -e ping -c4 google.com  && ratpoison -c undo
#definekey super-x p exec ratpoison -c "echo `ping -c2 google.com | grep data`"
#definekey super-x C exec ratpoison -c "echo Connecting Ethernet `con` "
definekey super-x r exec ratpoison -c "frestore `ratpoison -c 'getenv fs1'`"
definekey super-x s exec ratpoison -c "vsplit 5/6" -c focusdown
definekey super-x f exec xterm -e w3m -B

definekey super-x l exec ratpoison -c fdump > dump

definekey super-x f exec xterm -e w3m -B
definekey super-x h exec urxvt -e htop &

definekey super-x Down exec xrandr -o normal &
definekey super-x Left exec xrandr -o right &
definekey super-x Right exec xrandr -o left &

#definekey super-x a exec ratpoison -d :0.0 -c "echo Batt `acpi -b|cut -c-11-25` `acpi -t` `date`"
definekey super-x a exec ratpoison -d :0.0 -c "echo `~/bin/ping-check.sh` Net: `cat /sys/class/net/enp2s0f1/operstate` @  Wifi: `cat /sys/class/net/wlan0/operstate /sys/class/net/wlp3s0/operstate` `iw wlan0 info |grep ssid|cut -c6-50` @ Bat:`acpi -b |cut -c11-27` @  Mem: `free -h | grep Mem | cut -c27-30` @ Themp:`acpi -t|cut -c15-19`°C @ `date -R|cut -c18-22` `date|cut -c1-10`"
#: `connmanctl state|grep State|cut -c11-19`

definekey super-x G exec urxvt -e vim Vedatxt/Bhagavat-Gita/Bhagavad-Gita.txt &
definekey super-x K exec urxvt -e less Vedatxt/A.C.Bhaktivadanta\ Swami\ Prabhupada/Krsna_Book.txt &
definekey super-x B exec urxvt -e ranger Vedatxt/Srimad\ Bhagavatam/ &
definekey super-x V exec urxvt -e ranger Vedatxt &

#bind j exec amixer -q set Master 10+
#bind h exec amixer -q set Master 10-
#bind C exec urxvt -bg grey -fg black & sleep 0.3 && transset-df -a 0.7
bind s exec ratpoison -c  vsplit -c focusdown
#bind parenright exec ratpoison -c "frestore `tail -n 1 .config/ratframe/dump`" & sleep 0.5s && sudo systemctl suspend  

bind S exec ratpoison -c  hsplit -c focusright
bind C exec  urxvt -bg '#F8C888' -fg '#392613' -fn "xft:comic shanns:pixelsize=16"
#bind h exec amixer -q set Speaker unmute # 100%
#bind l exec amixer -q set Speaker mute   # 0%
bind t exec ratpoison -d :0.0 -c "echo `ratpoison -c windows`"
bind m exec ratpoison -c undo "title mutt" ; urxvt -e mutt > /dev/null &
bind c exec urxvt
bind d exec xterm & sleep .3s && transset-df -a 0.7
#set font ScaBenguit 
#set font terminus
set font ter-13n
#set font Liberation Serif
#set font "-*-fixed-bold-r-normal-*-5-*-*-*-c-*-*-*"
set inputwidth 250

GPG_TTY=$(tty)
export GPG_TTY
exec xset b 0
```

# dimatura
`https://raw.githubusercontent.com/dimatura/dot_ratpoison/refs/heads/master/.ratpoisonrc`

```
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
```
{% endraw %}
