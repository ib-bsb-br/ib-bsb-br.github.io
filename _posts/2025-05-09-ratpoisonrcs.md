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

# Maldus512
`https://github.com/Maldus512/dotfiles/tree/main/ratpoison`

```
<root>
<## data-filename="xml_code-block xml" data-code="">
    /mnt/mSATA/linaro/dotfiles-main/ratpoison/brightnessrc</source>
    
        exec [ -z "${rp_brightness_step}" ] && ratpoison -c 'setenv rp_brightness_step 5%' || true
        definekey top XF86MonBrightnessUp     exec brightnessctl s "${rp_brightness_step}"+; ratpoison -c "echo `brightnessctl | sed -nr 's/^.*\(([0-9]+%)\).*$/\1/p'`"
        definekey top XF86MonBrightnessDown     exec brightnessctl s "${rp_brightness_step}"-; ratpoison -c "echo `brightnessctl | sed -nr 's/^.*\(([0-9]+%)\).*$/\1/p'`"
    
</section>
<## data-filename="xml_code-block xml" data-code="">
    /mnt/mSATA/linaro/dotfiles-main/ratpoison/ratpoison_rofi.py</source>
    
        #!/usr/bin/env python
        
        import re
        import sys
        import subprocess
        import argparse
        import ratpoison_workspaces
        
        
        def rprun(*args):
            strargs = "".join([f"{x} " for x in args]).rstrip(" ")
            return subprocess.run(["ratpoison", "-c", strargs], stdout=subprocess.PIPE).stdout.decode("utf-8")
        
        
        def get_current_group():
            groups = [x.strip("\"") for x in rprun("groups").split("\n") if x]
            for group in groups:
                if found := re.compile(r"^([0-9]+)\*").search(group):
                    selected = int(found.group(1))
                    return selected
            return 0
        
        
        def get_groups():
            current_group = get_current_group()
            rawgroups = rprun("groups")
            groups = []
            for group in rawgroups.split("\n"):
                group = group.strip("\"")
                if found := re.compile("^([0-9]+)").search(group):
                    selected = int(found.group(1))
                    rprun("gselect", selected)
                    windows = [x.strip("\"") for x in rprun("windows").split("\n") if x]
                    wnames = []
                    for window in windows:
                        if found := re.compile(r"^[0-9]+#([\*|\+|-])#(.+)").search(window):
                            status = found.group(1)
                            if status == "*":
                                priority = 1
                            elif status == "+":
                                priority = 2
                            else:
                                priority = 3
        
                            wnames.append((priority, found.group(2)))
        
                    groups.append(f"{selected} - " + ", ".join([x[1] for x in sorted(wnames, key=lambda y: y[0])]))
        
                else:
                    groups.append(group)
        
            rprun("gselect", current_group)
            return groups
        
        
        def get_window_name(window):
            if name := re.compile(r"^[0-9]+#[\*\+\-]#(.+)$").search(window):
                return name.group(1)
            else:
                return window
        
        
        def main():
            parser = argparse.ArgumentParser(description="Navigate through workspaces and windows")
            parser.add_argument("-w", "--windows", action="store_true", help="switch through windows")
            parser.add_argument("-d", "--desktops", action="store_true", help="switch through workspaces")
            parser.add_argument("-s", "--send-to-desktop", dest="send_to_desktop", action="store_true", help="send current window to selected workspace")
            parser.add_argument("choice", nargs="?", help="Chosen option", default=None)
            args = parser.parse_args()
        
            if args.choice == None:
                if args.windows:
                    windows = rprun("windows")
                    for window in [x.strip("\"") for x in windows.split("\n") if len(x)]:
                        print(get_window_name(window))
                elif args.desktops or args.send_to_desktop:
                    for group in get_groups():
                        print(group)
        
            else:
                if args.windows:
                    windows = rprun("windows")
                    for window in [x.strip("\"") for x in windows.split("\n") if len(x)]:
                        if get_window_name(window) == args.choice:
                            if found := re.compile("^[0-9]+").search(window):
                                selected = int(found.group(0))
                                rprun("select", selected)
                elif args.send_to_desktop:
                    if found := re.compile("^[0-9]+").search(args.choice):
                        selected = int(found.group(0))
                        ratpoison_workspaces.move_to_workspace(selected)
                elif args.desktops:
                    if found := re.compile("^[0-9]+").search(args.choice):
                        selected = int(found.group(0))
                        ratpoison_workspaces.select_workspace(selected)
        
        
        
        if __name__ == "__main__":
            main()
    
</section>
<## data-filename="xml_code-block xml" data-code="">
    /mnt/mSATA/linaro/dotfiles-main/ratpoison/ratpoison_toggle_conky.py</source>
    
        #!/usr/bin/env python
        
        import re
        import sys
        import subprocess
        import argparse
        import ratpoison_workspaces
        
        
        def rprun(*args):
            strargs = "".join([f"{x} " for x in args]).rstrip(" ")
            return subprocess.run(["ratpoison", "-c", strargs], stdout=subprocess.PIPE).stdout.decode("utf-8")
        
        
        def setenv(variable, value):
            rprun("setenv", variable, value)
        
        
        def getenv(variable):
            return rprun("getenv", variable)
        
        
        def main():
            active = getenv("conky_visible").strip("\n")
            padding = [int(x) for x in rprun("set", "padding").split(" ") if x]
        
            if not active or active == "false":
                setenv("conky_visible", "true")
                padding[2] = 256 + 16
            else:
                setenv("conky_visible", "false")
                padding[2] = padding[0]
            
            rprun("set", "padding", padding[0], padding[1], padding[2], padding[3])
        
        
        
        if __name__ == "__main__":
            main()
    
</section>
<## data-filename="xml_code-block xml" data-code="">
    /mnt/mSATA/linaro/dotfiles-main/ratpoison/ratpoison_windows_list.py</source>
    
        #!/usr/bin/env python -u
        
        import re
        import sys
        import subprocess
        import argparse
        import signal
        import threading
        import os
        
        
        event = threading.Event()
        
        
        def rprun(*args):
            strargs = "".join([f"{x} " for x in args]).rstrip(" ")
            return subprocess.run(["ratpoison", "-c", strargs], stdout=subprocess.PIPE).stdout.decode("utf-8")
        
        
        def setenv(variable, value):
            rprun("setenv", variable, value)
        
        
        def getenv(variable):
            return rprun("getenv", variable)
        
        
        def received_usr1(signal, frame):
            event.set()
        
        
        def main():
            signal.signal(signal.SIGUSR1, received_usr1)
            setenv("windows_list_pid", os.getpid())
            event.set()
            counter = 0
        
            while True:
                counter += 1
                if event.wait(timeout=4):
                    event.clear()
        
                output = rprun("windows")
        
                if output.replace("\n", "") == "No managed windows":
                    print(" ")
                    continue
                
                windows = [x.strip("\"").replace("\n", "") for x in output.split("\n") if x]
                cleanwindows = []
        
                for window in windows:
                    if found := re.compile(r"^[0-9]+#([\*|\-|\+])#(.*)").search(window):
                        if found.group(1) == "*":
                            selected = True
                        else:
                            selected = False
                        if len(found.group(2)) > 0:
                            cleanwindows.append((selected, found.group(2)))
                        else:
                            cleanwindows.append((selected, " "))
                    else:
                        cleanwindows.append((False, window))
        
                print("%{-u} | ", end="")
                for (active, name) in cleanwindows:
                    if len(name) > 16:
                        name = name[:16]
                    if active:
                        print(f"%{{+u}}{name}%{{-u}}", end=" | ")
                    else:
                        print(f"{name}", end=" | ")
                print(counter, end="")
                print()
        
            print("ERROR")
        
        if __name__ == "__main__":
            main()
    
</section>
<## data-filename="xml_code-block xml" data-code="">
    /mnt/mSATA/linaro/dotfiles-main/ratpoison/ratpoison_workspaces.py</source>
    
        #!/usr/bin/env python
        
        import subprocess
        import argparse
        
        
        def rprun(*args):
            strargs = "".join([f"{x} " for x in args]).rstrip(" ")
            return subprocess.run(["ratpoison", "-c", strargs], stdout=subprocess.PIPE).stdout.decode("utf-8")
        
        
        def message(msg):
            rprun("echo", msg)
        
        
        def setenv(variable, value):
            rprun("setenv", variable, value)
        
        
        def unsetenv(variable):
            rprun("unsetenv", variable)
        
        
        def getenv(variable):
            return rprun("getenv", variable)
        
        def workspace_name(num):
            if int(num) == 0:
                return "default"
            else:
                return f"workspace_{num}"
        
        def workspace_dump_name(num):
            return f"{workspace_name(num)}_dump"
        
        def workspace_data():
            try:
                workspaces = int(getenv("workspaces"))
                current_workspace = int(getenv("current_workspace"))
            except ValueError:
                workspaces = 1
                current_workspace = 0
        
            return (current_workspace, workspaces)
        
        def dump_variables():
            print("workspaces", getenv("workspaces"))
            print("current_workspace", getenv("current_workspace"))
        
        def new_workspace():
            current_workspace, workspaces = workspace_data()
        
            frame_dump = rprun("fdump") 
            setenv(workspace_dump_name(current_workspace), frame_dump)
        
            rprun("select", "-")
            rprun("only")
        
            rprun("gnew", workspace_name(workspaces)) 
            frame_dump = rprun("fdump") 
        
            current_workspace = workspaces
            workspaces += 1
        
            setenv("current_workspace", str(current_workspace))
            setenv("workspaces", str(workspaces))
            setenv(workspace_dump_name(current_workspace), frame_dump)
        
            message(f"Created new workspace: {current_workspace}")
        
        def prepare_switch():
            current_workspace, workspaces = workspace_data()
            frame_dump = rprun("fdump") 
            setenv(workspace_dump_name(current_workspace), frame_dump)
            return (current_workspace, workspaces)
        
        
        def close_switch(current_workspace):
            setenv("current_workspace", current_workspace)
            rprun("gselect", current_workspace)
            frame_dump = getenv(workspace_dump_name(current_workspace))
            rprun("frestore", frame_dump)
        
            message(f"Switched to workspace {current_workspace}")
        
        
        def delete_workspace(workspace):
            (current_workspace, workspaces) = prepare_switch()
        
            if workspaces < 2:
                message("Not enough workspaces!")
                return
        
            windows = rprun("windows")
            if windows != "No managed windows\n":
                message("Workspace is not empty!")
                return
            
        
            if not workspace or workspace == "current":
                workspace = current_workspace
                next_workspace()
        
            name = workspace_dump_name(workspace)
            if not getenv(name):
                print(f"No workspace with name {name} found!")
                return
        
            unsetenv(name)
        
            rprun("gdelete", workspace)
            setenv("workspaces", str(workspaces-1))
        
        
        def next_workspace():
            (current_workspace, workspaces) = prepare_switch()
            if workspaces == 1:
                return
        
            current_workspace = (current_workspace + 1) % workspaces
            close_switch(current_workspace)
        
        
        def prev_workspace():
            (current_workspace, workspaces) = prepare_switch()
            if workspaces == 1:
                return
        
            if current_workspace == 0:
                current_workspace = workspaces-1
            else:
                current_workspace -= 1
            close_switch(current_workspace)
        
        
        def select_workspace(workspace):
            current_workspace, workspaces = prepare_switch()
            close_switch(workspace)
        
        
        def move_to_workspace(workspace):
            rprun("gmove", workspace) 
            rprun("select", "-")
            select_workspace(workspace)
        
        
        def main():
            parser = argparse.ArgumentParser()
            parser.add_argument("-c", "--create-workspace", action="store_true", help="Create a new workspace")
            parser.add_argument("-n", "--next", action="store_true", help="Move to next workspace")
            parser.add_argument("-p", "--prev", action="store_true", help="Move to previous workspace")
            parser.add_argument("-s", "--select", help="Select workspace")
            parser.add_argument("-d", "--delete", nargs="?", const="current", help="Delete workspace")
            args = parser.parse_args()
        
            if args.create_workspace:
                new_workspace()
        
            if args.next:
                next_workspace()
        
            if args.prev:
                prev_workspace()
        
            if args.select:
                select_workspace(args.select)
        
            print(args.delete)
            if args.delete:
                delete_workspace(args.delete)
        
        
        if __name__ == "__main__":
            main()
    
</section>
<## data-filename="xml_code-block xml" data-code="">
    /mnt/mSATA/linaro/dotfiles-main/ratpoison/ratpoisonrc</source>
    
        addhook switchwin exec kill -s USR1 `ratpoison -c "getenv windows_list_pid"`
        addhook switchframe exec kill -s USR1 `ratpoison -c "getenv windows_list_pid"`
        addhook switchgroup exec kill -s USR1 `ratpoison -c "getenv windows_list_pid"`
        addhook switchscreen exec kill -s USR1 `ratpoison -c "getenv windows_list_pid"`
        addhook deletewindow exec kill -s USR1 `ratpoison -c "getenv windows_list_pid"`
        addhook newwindow exec kill -s USR1 `ratpoison -c "getenv windows_list_pid"`
        addhook titlechanged exec kill -s USR1 `ratpoison -c "getenv windows_list_pid"`
        
        set fgcolor white
        set bgcolor black
        set font Mono-12
        set barpadding 8 8
        set barborder 4
        
        set padding 4 32 4 4
        set border 1
        set onlyborder 0
        set fwcolor purple
        set bwcolor gray
        set winfmt "%n#%s#%c"
        
        escape Super_L
        unbind k
        startup_message off
        bind i exec ratpoison_toggle_conky.py
        bind Return exec rofi -show run -theme purple
        bind M-Return exec rofi -show drun -theme purple
        bind S-Return exec rofi -show file-browser -theme purple
        bind t exec ${rp_terminal_emulator}
        bind q delete
        bind Q kill
        bind M-Tab exec rofi -modi dswitch:"ratpoison_rofi.py --desktops" -show dswitch -theme purple
        bind Tab exec rofi -modi wswitch:"ratpoison_rofi.py --windows" -show wswitch -theme purple
        bind S exec rofi -modi wswitch:"ratpoison_rofi.py --send-to-desktop" -show wswitch -theme purple
        bind minus vsplit
        bind backslash hsplit
        
        bind C exec ratpoison_workspaces.py -c
        bind N exec ratpoison_workspaces.py -n
        bind P exec ratpoison_workspaces.py -p
        bind M-BackSpace exec ratpoison_workspaces.py -l
        bind D exec ratpoison_workspaces.py -d
        
        bind BackSpace other
        bind n next
        bind p prev
        
        bind h focusleft
        bind j focusdown
        bind k focusup
        bind l focusright
        
        bind H exchangeleft
        bind J exchangedown
        bind K exchangeup
        bind L exchangeright
        
        bind o only
        
        definekey resize h resizeleft
        definekey resize j resizedown
        definekey resize k resizeup
        definekey resize l resizeright
        
        
        newkmap mouse
        bind m set topkmap mouse
        definekey mouse h ratrelwarp -5 0
        definekey mouse k ratrelwarp 0 -5
        definekey mouse j ratrelwarp 0 5
        definekey mouse l ratrelwarp 5 0
        definekey mouse H ratrelwarp -25 0
        definekey mouse K ratrelwarp 0 -25
        definekey mouse J ratrelwarp 0 25
        definekey mouse L ratrelwarp 25 0
        definekey mouse c ratclick 1
        definekey mouse v ratclick 2
        definekey mouse Escape set topkmap top
        
    
</section>
<## data-filename="xml_code-block xml" data-code="">
    /mnt/mSATA/linaro/dotfiles-main/ratpoison/volumerc</source>
    
        alias volume-unmute exec ${rp_volume_unmute}; ratpoison -c "echo `${rp_volume_mute_status}`"
        alias volume-toggle exec ${rp_volume_mute_toggle}; ratpoison -c "echo `${rp_volume_mute_status}`"
        alias volume-up     exec ${rp_volume_up}; ratpoison -c "echo `${rp_volume_status}`"
        alias volume-down   exec ${rp_volume_down}; ratpoison -c "echo `${rp_volume_status}`"
        
        definekey top XF86AudioMute volume-toggle
        definekey top XF86AudioLowerVolume volume-down
        definekey top XF86AudioRaiseVolume volume-up
        definekey top XF86AudioNext exec dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next
        definekey top XF86AudioPrev exec dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous
        definekey top XF86AudioStop exec dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Pause
        definekey top XF86AudioPlay exec dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Play
    
</section>
</root>
```

# trapd00r
`https://raw.githubusercontent.com/trapd00r/configs/refs/heads/master/ratpoisonrc`
```
### vim:ft=ratpoison:fde:fdm=marker:fmr=#<,#>:fdc=3:fdl=0:
#< ${HOME}/etc/ratpoisonrc
#   ‗‗‗‗‗‗‗‗‗‗‗‗ ‗‗‗‗‗‗ ‗‗‗‗‗‗‗‗ ‗‗‗‗‗‗‗‗‗‗‗
#         owner  Magnus Woldrich <m@japh.se>
#       crafted  2009-04-24
#         mtime  2021-04-12 13:47:57
#           git  git://github.com/trapd00r/configs.git
#           url  http://github.com/trapd00r/configs
#           irc  japh@freenode #zsh #vim #perl
#   ‗‗‗‗‗‗‗‗‗‗‗‗ ‗‗‗‗‗‗‗‗‗‗‗‗‗ ‗‗‗‗ ‗‗‗‗ ‗‗‗‗
###>
startup_message off
         escape C-f
  defresizeunit 80
        addhook switchgroup next

## banish the mouse with each screenchange
#addhook switchwin banish

#setenv ratpoison_version `exec ratpoison -c "echo $(pgrep -l catpoison || 'ratpoison')"`
#< aliases
alias reload         exec catpoison -c "source $XDG_CONFIG_HOME/ratpoisonrc"

alias toggle-borders exec if [ "$(catpoison -c 'set border')" -ge 1 ]; then catpoison -c 'set border 0'; else catpoison -c 'set border 1'; fi
 bind BackSpace  toggle-borders

# move commands (moves window to other frame w/o exchanging)
# TODO: works badly when moving causes an empty frame ('other' fails)
alias moveleft  exec ratpoison -c 'exchangeleft'  -c 'focuslast' -c 'other' -c 'focuslast'
alias movedown  exec ratpoison -c 'exchangedown'  -c 'focuslast' -c 'other' -c 'focuslast'
alias moveup    exec ratpoison -c 'exchangeup'    -c 'focuslast' -c 'other' -c 'focuslast'
alias moveright exec ratpoison -c 'exchangeright' -c 'focuslast' -c 'other' -c 'focuslast'

alias showroot   exec catpoison -c fdump > ~/tmp/rp-frames; catpoison -c 'select -' -c only
alias unshowroot exec catpoison -c "frestore `cat ~/tmp/rp-frames`"
bind odiaeresis   showroot
bind C-odiaeresis unshowroot


#>
#< catpoison only!
set virtuals 4
vinit
definekey top   C-1  vselect 1
definekey top   C-2  vselect 2
definekey top   C-3  vselect 3
definekey top   C-4  vselect 4

set barsticky off

# https://www.japh.se/2021/03/21/ratpoison-urxvt-and-borders.html
set gap 1
#>

#< options
set           gravity c
set        bargravity c
set        wingravity c
set           winname title
set    maxsizegravity c
set        inputwidth 0
set  historyexpansion 1
set historycompaction 1
set       historysize 1000
set      winliststyle column
set        barpadding 8 8
set            winfmt %n%s%t
set          framefmt %t
set           infofmt (%H, %W) %n(%c - %a) -- PID: %p, XWID: %i
## for dzen2
#set           padding 0 13 0 0
set           padding 0 0 0 0
set            border 0
set           bgcolor #080808
set           bwcolor #0c0c0c
set           fgcolor #d75f00
set           fwcolor #303030
set              font 'xft:Terminus:style=Regular:pixelsize=24'
set          maxundos 20
#>
#< window management
unmanage mullvad-gui
unmanage mullvad-vpn
unmanage mullvad
unmanage tint2
unmanage dzen2
unmanage xmobar
unmanage sdlmame
unmanage mame
unmanage neverball
#unmanage gcolor2
unmanage steam
unmanage tallowmere
unmanage deluge
#>
#< binds: applications
#bind c exec urxvt -name uxterm +sb -fg white -bg black
bind c exec urxvt -name sid -fg white -bg black
bind C exec kitty
bind v exec urxvt -name sid -bg '#121212' -fg '#bbaaaa'
bind x exec urxvt -name sid -fn 'xft:Terminus:pixelsize=14'
bind X exec xterm -name XTerm
bind e exec rp-runorraise firefox


bind Tab focuslast

unbind n
bind n exec ratpoison -c "echo `mpc prev | head -1`"
bind p exec ratpoison -c "echo `mpc next | head -1`"
bind o exec mpc toggle

#bind o exec np
bind 0 exec ratpoison -c "echo ´~/bin/knnp´"
bind 9 exec sconsify -command play_pause

#< top level XF86 binds
definekey top XF86AudioRaiseVolume  exec amixer -c 0 set Master 2dB+
definekey top XF86AudioLowerVolume  exec amixer -c 0 set Master 2dB-
definekey top XF86AudioMute         exec amixer -c 0 set Master mute
definekey top XF86Calculator        exec amixer -c 0 set Master unmute
definekey top XF86Mail              exec nestopia -dpu ~/emu/nes/castlevania.nes
definekey top XF86HomePage          exec nestopia -dpu ~/emu/nes/castlevania3.nes
#definekey top Menu
#>

unbind space
bind   space exec ratpoison -c "echo `mpc | head -1`"

unbind w
unbind g
bind w exec sh ~/dev/ratpoison_scripts/window-menu/window-menu
bind g exec ~/dev/utils/rp-groups-menu
#>
#< binds: window management
bind H exchangeleft
bind J exchangedown
bind K exchangeup
bind L exchangeright

bind h focusleft
bind j focusdown
bind k focusup
bind l focusright

bind C-K kill

bind C-s split 2/3
bind C-S hsplit 2/3

bind u undo
bind G vmove

bind Tab focuslast
bind ISO_Left_Tab focus

bind Delete exec catpoison -c 'gmove crap' -c 'next'

#bind s-n gnext
#bind s-p gprev
#bind s-c gnew
#bind s-g gnew
#>
#< binds: workspaces
#exec rpws init 5 -k
#gnewbg one
#gnewbg two
#gnewbg three
#gnewbg four
#
#definekey top F1 exec rpws 1
#definekey top F2 exec rpws 2
#definekey top F3 exec rpws 3
#definekey top F4 exec rpws 4
#definekey top F5 exec rpws 5



#>
#< binds: top level
definekey top Pause       exec ~/dev/utils/monitor-toggle && echo 'screensaver disabled'
definekey top Scroll_Lock exec xscreensaver-command -lock
definekey top M-Return    nextscreen
definekey top s-Return    prevscreen
#>

# act normal, but prevent firefox from raising itself
# when links are opened from other applications
rudeness 12

#< init
## start spotify unless it's already started
#exec pgrep -l spotify || spotify
#exec pgrep -l cantata || cantata
exec pgrep -l nicotine || nicotine
#prevscreen
#exec urxvt -name sid -fg white -bg black
#>

gnewbg crap

#echo ratpoisonrc loaded.
```

# rwstauner
`https://github.com/rwstauner/run_control/blob/master/archive/.ratpoisonrc`
```

# Set the prefix key to that of screen's default
#escape C-a
# but then how would i use screen? that'd be like using screen inside of screen (which is mighty annoying, let me tell you)

# some options
set bgcolor #555555
set fgcolor #e6e6e6
set border 1
set barborder 2
#set bargravity ne
set barpadding 6 4
set inputwidth 250
set winname class
#set winname name

# i removed all this b/c unmanaged really means UNmanaged...
# tiny windows--not fit for full screen
#unmanage gimp
#unmanage Gimp
#unmanage The GIMP
#unmanage xmms

# ratpoison.tld : keybind, xmenu
# hack C-t
#addhook switchwin set rp_lastwin1 $rp_lastwin0
#addhook switchwin set rp_lastwin0 

# some key bindings
bind Escape abort
bind g groups
bind C-g groups
bind d dedicate 1
bind C-d dedicate 1
bind D dedicate 0
bind C-D dedicate 0
# this is dangerous
bind k abort
bind C-k abort
bind K delete
bind C-F4 delete
#bind C-K kill
# and I don't like these
bind C-V version
bind C-v getsel

# getsel has a shortcut, putsel needs one too.
bind C-c putsel

# am I the only one who uses the keypad?
bind KP_Decimal select 0
bind C-KP_0 select 0
bind KP_0 select 0
bind KP_1 select 1
bind KP_2 select 2
bind KP_3 select 3
bind KP_4 select 4
bind KP_5 select 5
bind KP_6 select 6
bind KP_7 select 7
bind KP_8 select 8
bind KP_9 select 9

# lock screen
bind Delete exec xscreensaver-command -lock

# launch my vnc shortcut and ask for who
bind v colon exec vnc 

## help!
bind slash exec ratpoison -c "echo $(<~/.ratpoisonhelp)"

## colorpicker!
bind numbersign exec woundedrc screencolor = "`grabc`"; ratpoison -c "echo `woundedrc screencolor`"

# launch my xmms hotkeys app and ask for action
#bind x colon exec xmmskeys - 
#alias xmmstitle exec ratpoison -c "set bargravity n"; ratpoison -c "echo  ..:|[  `xmmskeys -t`  ]|:.. "; sleep 1s; ratpoison -c "set bargravity ne"
alias xmmstitle exec ratpoison -c "echo  ..:|[  `xmmskeys -t`  ]|:.. ";
bind x readkey xmmskeys
bind C-x readkey xmmskeys
newkmap xmmskeys
definekey xmmskeys 1 exec xmmskeys -1 ; ratpoison -c xmmstitle
definekey xmmskeys p exec xmmskeys -p ; ratpoison -c xmmstitle
definekey xmmskeys f exec xmmskeys -f ; ratpoison -c xmmstitle
definekey xmmskeys r exec xmmskeys -r ; ratpoison -c xmmstitle
definekey xmmskeys s exec xmmskeys -s ; ratpoison -c xmmstitle
definekey xmmskeys m exec xmmskeys -m ; ratpoison -c xmmstitle
definekey xmmskeys c exec xmmskeys -c ; ratpoison -c xmmstitle
definekey xmmskeys t xmmstitle
definekey xmmskeys Escape abort

# handy woundedrc manipulation
#bind w readkey woundedrc
bind W readkey woundedrc
newkmap woundedrc
definekey woundedrc m exec check_email.pl -z ; ratpoison -c "echo checked email"
definekey woundedrc Escape abort

# some keys for mouse manipulation
bind m readkey mouse
newkmap mouse
definekey mouse 1 ratclick 1
definekey mouse l ratclick 1
definekey mouse 2 ratclick 2
definekey mouse c ratclick 2
definekey mouse m ratclick 2
definekey mouse 3 ratclick 3
definekey mouse r ratclick 3
definekey mouse d exec ratpoison -c "ratclick 1" -c "ratclick 1"
#definekey mouse ! rathold 1
#definekey mouse L rathold 1
#definekey mouse @ rathold 2
#definekey mouse C rathold 2
#definekey mouse M rathold 2
#definekey mouse # rathold 3
#definekey mouse R rathold 3
definekey mouse Left ratwarp 640 512
definekey mouse Right ratwarp 1980 525
definekey mouse Escape abort

# ah, just like screen
bind quotedbl windows
bind S vsplit
bind C-S vsplit
bind s hsplit
bind C-s hsplit

# Gets rid of that ugly crosshairs default cursor
exec xsetroot -cursor_name left_ptr

# not if it's already running...
alias execonce exec execonce

# I do still like to have this going
exec nice xscreensaver -no-splash
	## some essentials
execonce aterm
	#exec sleep 1s; ratpoison -c "gravity c" -c "dedicate 1"
exec sleep 2s; ratpoison -c "select xterm" -c "number 0" -c "gravity c" -c "dedicate 1" -c "sselect 1" -c "fselect 1"
	#	#ratpoison -c "sselect 1"; ratpoison -c "fselect 1";
	#		# and aterm only, please
	#		#dedicate 1
	#		# i like these on the left side
	#		#sselect 1 
	#		#fselect 1
execonce xmms
	#	exec sleep 2s; ratpoison -c "select xmms" -c "number 1"
execonce firefox
execonce thunderbird
execonce acroread
	#	select acroread
	#	number 4
	#	#exec sleep 4s; ratpoison -c "select firefox" -c "number 2"
	#	#execonce thunderbird
	#	#exec sleep 2s; ratpoison -c "select thunderbird" -c "number 3"
	#	#exec firefox
	#	#exec thunderbird
	#	#exec sleep5s; xmms
	#		# and go back to aterm
	#		sselect 0
	#		fselect 0
	#		select 0
	#		gravity c
	#	#setenv RATPOISON_STARTED 1

## the above never seems to work out right, so i'll just call this when ready
alias fixwindows exec ratpoison -c "fselect 1" -c "select xmms" -c "fselect 0" -c "dedicate 0" -c "select xterm" -c "dedicate 1" -c "select acroread" -c "select acroread" -c "number 4" -c "select xterm" -c "number 0" -c "gravity c" -c "select xmms" -c "select xmms" -c "number 1" -c "select firefox" -c "number 2" -c "select thunderbird" -c "number 3" -c "select 2" -c "select 2" -c "fselect 0"

# bind M-! to store the current frame layout in slot #1
bind M-exclam exec ratpoison -c "setenv fs1 `ratpoison -c 'fdump'`"

#bind M-1 to restore the frame layout in slot #1
bind M-1 exec ratpoison -c "frestore `ratpoison -c 'getenv fs1'`"

# Do the same for slot #2 and bind it to M-@ and M-2, respectively.
bind M-at exec ratpoison -c "setenv fs2 `ratpoison -c 'fdump'`"
bind M-2 exec ratpoison -c "frestore `ratpoison -c 'getenv fs2'`"

# Give ourselves another slot on M-# and M-3, respectively.
bind M-numbersign exec ratpoison -c "setenv fs3 `ratpoison -c 'fdump'`"
bind M-3 exec ratpoison -c "frestore `ratpoison -c 'getenv fs3'`"

# Here's a hack from John Meacham:

bind plus exec ratpoison -c "echo `date +'%n %I:%M:%S%p - %A %n   %D - %B'`  `cal | tail -n +2 | sed -e 's/^Su/\n\n Su/' -e 's/.*/ & /' -e \"s/\ $(date +%e)\ /\<$(date +%e)\>/\"`"

# it produces output like the following in the message window, very handy:
#         +-----------------------+
#         |05:05:24 PM - Tuesday  |
#         |   09/09/03 - September|
#         |                       |
#         |Su Mo Tu We Th Fr Sa   |
#         |    1  2  3  4  5  6   |
#         | 7  8< 9>10 11 12 13   |
#         |14 15 16 17 18 19 20   |
#         |21 22 23 24 25 26 27   |
#         |28 29 30               |
#         +-----------------------+

```

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
