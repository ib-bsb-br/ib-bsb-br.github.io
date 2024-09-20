---
title: "/.ratpoisonrc"
date: 2024-04-14 00:00:00 -03:00
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
set fgcolor black
set bgcolor silver
set framesels 123456789
set font -xos4-terminus-medium-r-normal-*-*-140-*-*-c-*-iso8859-1
set border 0
set barborder 0
set barpadding 0 0
set winname class
set winfmt %n %s %c
set winliststyle column
set wingravity n 
set gravity center 
set transgravity center
set bargravity ne
set waitcursor 1
set padding 0 0 0 0

startup_message off
escape Super_L
banish

unmanage rpbar

exec brightnessctl s 7
exec unclutter
exec rpws init 9 -k
exec systemctl start performance_governors.service
exec ferdium --no-sandbox

definekey top M-Tab next
definekey top M-ISO_Left_Tab prev

bind F1 only
bind F2 hsplit
bind F3 vsplit
bind F4 resize
bind y exec freetube --no-sandbox 
bind apostrophe exec zutty -saveLines 50000 -border 0 -font 10x20
bind s-apostrophe exec zutty -saveLines 50000 -border 0 -font 12x24
bind e exec xnc
bind f exec thorium-browser
bind s-f exec ferdium --no-sandbox
bind g exec gsimplecal
bind c exec write_clipboard_to_file.sh
bind s-c exec galculator
bind i exec zutty -saveLines 50000 -border 0 -font 10x20 -e wifish
bind p exec xfce4-screenshooter
bind Prior exec thermal.sh
bind Next exec reverse-thermal.sh
bind r remove
bind t exec pcmanfm-qt --daemon-mode
bind v exec paste_clipboard_from_file.sh
bind s-v exec viewnior
bind w exec ratpoison -c "select `ratpoison -c "windows" | dmenu | awk '{print $1}'`"
bind b exec zutty -saveLines 50000 -border 0 -font 10x20 -e bpytop
bind z nextscreen
bind s-b exec vorta
bind s-k kill
bind s-x fselect
bind BackSpace undo
bind s-BackSpace redo
bind s-Down exchangedown
bind s-Up exchangeup
bind s-Left exchangeleft
bind s-Right exchangeright
bind s-Return prev
bind s-Tab focuslast
bind Tab focus
bind Escape abort
bind space exec dmenu_run
bind F9 exec amixer set Master 0
bind F10 exec amixer set Master 25%-
bind F11 exec amixer set Master 25%+
bind KP_0 exec xdotool key apostrophe key apostrophe key apostrophe
bind KP_Separator exec xdotool key quotedbl key quotedbl key quotedbl
bind Home exec xdotool key shift+1 key m key u key l key t key i
bind End exec xdotool key shift+1 key e key n key d
bind KP_1 exec rpws 1
bind KP_2 exec rpws 2
bind KP_3 exec rpws 3
bind KP_4 exec rpws 4
bind KP_5 exec rpws 5
bind KP_6 exec rpws 6
bind KP_7 exec rpws 7
bind KP_8 exec rpws 8
bind KP_9 exec rpws 9
bind s-0 exec flatpak run com.github.tenderowl.frog
bind s-1 exec flatpak run com.rtosta.zapzap
bind s-2 exec flatpak run com.strlen.TreeSheets
bind s-3 exec flatpak run io.github.zaps166.QMPlay2
bind s-4 exec flatpak run com.github.ryonakano.reco
```
