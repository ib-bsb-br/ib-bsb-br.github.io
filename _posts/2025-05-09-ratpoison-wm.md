---
tags: [aid>software>linux>dotfile]
info: aberto.
date: 2025-05-09
type: post
layout: post
published: true
slug: ratpoison-wm
title: 'Ratpoison WM'
comment: 'https://ozi-blog.ru/nastroyka-pereklyucheniya-rabochih-stolov-v-ratpoison/'
---
## documentation at
`https://ib.bsb.br/ratpoison-documentation/`

### **Step 1: Install Ratpoison and Essential Tools**

First, update your package lists and install Ratpoison. The rpws (Ratpoison Workspace System) script is included with the ratpoison package in Debian Bullseye. Consider installing dmenu for application launching and a basic terminal like xterm or rxvt-unicode.  
`sudo apt update`  
`sudo apt upgrade`  
`sudo apt install ratpoison dmenu xterm # Or rxvt-unicode, etc.`  
`# Install other optional utilities you might find useful:`  
`# sudo apt install alsamixergui bpytop brightnessctl catfish dialog gmrun gsimplecal neofetch `  
`# python3-psutil unclutter viewnior xdotool scrot `  
`# fonts-dejavu fonts-terminus nitrogen picom # (nitrogen for wallpaper, picom for compositing)`

### **Step 2: Create a Ratpoison Session File for LightDM**

LightDM uses .desktop files located in /usr/share/xsessions/ to identify available sessions. Create one for Ratpoison:  
`sudo nano /usr/share/xsessions/ratpoison.desktop`

Add the following content:  
`[Desktop Entry]`  
`Version=1.0`  
`Encoding=UTF-8`  
`Name=Ratpoison`  
`Comment=Minimalist Tiling Window Manager`  
`Exec=ratpoison`  
`TryExec=ratpoison`  
`Icon=`  
`Type=XSession`

Save and close the file (e.g., Ctrl+X, then Y, then Enter in nano).

### **Step 3: Configure LightDM for Ratpoison Autologin**

To ensure LightDM launches Ratpoison for the autologin user, you need to update its configuration. Debian best practices suggest using configuration snippets in /etc/lightdm/lightdm.conf.d/. If you already have an autologin configuration file there (e.g., 50-autologin.conf), modify it. Otherwise, you can edit /etc/lightdm/lightdm.conf directly or create a new snippet.

1. **Edit or Create LightDM Configuration:** For example, to create/edit a dedicated snippet:  
   `sudo nano /etc/lightdm/lightdm.conf.d/60-autologin-ratpoison.conf`  
   Ensure the configuration specifies linaro and sets autologin-session to ratpoison. The autologin-session value should match the filename of the .desktop file created in Step 2 (without the .desktop extension).  
   `[Seat:*]`  
   `autologin-user=linaro`  
   `autologin-user-timeout=0`  
   `autologin-session=ratpoison`  
   If you are editing an existing file that previously specified autologin-session=xfce (or similar), change it to ratpoison. Adding this line explicitly makes the autologin deterministic.  
2. **Note on Session Selection:** While LightDM can sometimes remember the last session selected at the greeter, for an autologin setup, explicitly defining autologin-session is the most reliable method.

### **Step 4: Configure Ratpoison (~/.ratpoisonrc)**

Create and configure the ~/.ratpoisonrc file in the home directory of the autologin user (i.e., /home/linaro/.ratpoisonrc). This file controls Ratpoison’s behavior, keybindings, and startup applications.  
`# Ensure you are the user ‘linaro’ or adjust path accordingly`  
`nano /home/linaro/.ratpoisonrc`

Here’s a comprehensive example configuration:  
`# ~/.ratpoisonrc for linaro`
{% codeblock %}
set winname title
set winliststyle column
set wingravity c
set winfmt %n%s%t
set framefmt %t
set infofmt (%H, %W) %n(%c - %a)
set waitcursor 1
set transgravity center
set padding 0 0 0 24
set maxsizegravity c
set inputwidth 0
set historysize 1000
set historyexpansion 1
set historycompaction 1
set gravity c
set fwcolor #303030
set framesels 1234567890
set fgcolor #d75f00
set bwcolor #0c0c0c
set border 0
set bgcolor #080808
set barpadding 8 8
set bargravity c
set barborder 0
set maxundos 20

#< hack - we need to set font once per head
nextscreen
set font "Intel One Mono:size=12"
nextscreen
set font "Intel One Mono:size=12"
#>

defresizeunit 80
definekey top Print exec xfce4-screenshooter
definekey top M-VoidSymbol exec x-terminal-emulator -e /home/linaro/.local/bin/clipse
definekey top C-VoidSymbol ratclick 3
definekey top ISO_Left_VoidSymbol ratclick 1
definekey top VoidSymbol ratclick 2

exec alttab
exec xsetroot -name "$wspl"
exec hsetroot -fill /home/linaro/Desktop/02-media/pics/wallpaper1.png
exec xrdb -merge /home/linaro/.Xresources
exec xfce4-power-manager
exec unclutter --timeout 2 --jitter 5
exec rpws init 9
exec nm-applet
exec env HOME=$HOME/.config rpbar
exec env HOME=$HOME rpbar
exec brightnessctl s 7
exec /usr/bin/numlockx

startup_message on
warp 1
banish
unmanage rpbar
escape Super_L
rudeness 12

bind c redisplay
bind M-1 exec xdotool key --repeat 6 dead_grave
bind M-2 exec xdotool key --repeat 6 dead_tilde
bind M-3 exec xdotool key --repeat 3 quotedbl
bind M-4 exec xdotool key --repeat 3 apostrophe
bind KP_0 rathold up ratclick 1
bind s-KP_0 rathold down ratclick 1
bind KP_Separator rathold up ratclick 3
bind s-KP_Separator rathold down ratclick 3
bind k gother
bind z undo
bind x swap
bind w exec thorium-browser
bind VoidSymbol nextscreen
bind v meta S-Insert
bind Up focusup
bind u exec /usr/bin/rpws dump /home/linaro/Desktop/01-document/dotfiles/rpws_layouts.dmp
bind Tab focus
bind t exec pcmanfm-qt --daemon-mode
bind space exec xboomx
bind s-z redo
bind s-x fselect
bind s-w select
bind s-VoidSymbol other
bind s-Up exchangeup
bind s-u exec /usr/bin/rpws restore /home/linaro/Desktop/01-document/dotfiles/rpws_layouts.dmp
bind s-Tab focuslast
bind s-t exec sudo pcmanfm-qt
bind s-space exec python3 /home/linaro/.local/bin/dratmenu.py
bind s-Right exchangeright
bind s-Return exec sudo x-terminal-emulator
bind s-r remove
bind s-Home exec /home/linaro/.local/bin/llm_scrot.sh
bind s-Page_Up exec rpws movenext
bind s-Page_Down exec rpws moveprev
bind s-o iother
bind s-minus exec /home/linaro/.local/bin/split1.sh
bind s-M-Tab inext
bind s-Left exchangeleft
bind s-KP_9 exec rpws move9
bind s-KP_8 exec rpws move8
bind s-KP_7 exec rpws move7
bind s-KP_6 exec rpws move6
bind s-KP_5 exec rpws move5
bind s-KP_4 exec rpws move4
bind s-KP_3 exec rpws move3
bind s-KP_2 exec rpws move2
bind s-KP_1 exec rpws move1
bind s-ISO_Left_Tab exec rpws movenext
bind s-i exec nm-connection-editor
bind s-g exec galculator
bind s-F11 exec amixer set Master 5%+
bind s-F10 exec amixer set Master 5%-
bind s-F9 exec amixer set Master toggle
bind s-F1 exec thermal.sh
bind s-Escape kill
bind s-equal exec /home/linaro/.local/bin/split2.sh
bind s-e exec xnc
bind s-Down exchangedown
bind s-BackSpace prev
bind s-apostrophe colon exec x-terminal-emulator -e sudo 
bind apostrophe colon exec x-terminal-emulator -e 
bind semicolon exec
bind s-semicolon colon
bind s-a title
bind s-9 swap 9
bind s-8 swap 8
bind s-7 swap 7
bind s-6 swap 6
bind s-5 swap 5
bind s-4 swap 4
bind s-3 swap 3
bind s-2 swap 2
bind s-1 swap 1
bind s-0 swap 0
bind Right focusright
bind Return exec x-terminal-emulator
bind r resize
bind q delete
bind Home exec scrot -s -e 'xclip -selection clipboard -t image/png -i $f && rm $f'
bind Page_Up exec rpws next
bind Page_Down exec rpws prev
bind p dedicate
bind o cother
bind minus vsplit
bind M-Tab cnext
bind M-F7 exec x-terminal-emulator -e /home/linaro/.local/bin/llm_sF12_extract_last.sh
bind M-F6 exec x-terminal-emulator -e /home/linaro/.local/bin/llm_sF9_attachment.sh
bind M-F5 exec x-terminal-emulator -e /home/linaro/.local/bin/llm_analyze_file.sh
bind M-F4 exec x-terminal-emulator -e /home/linaro/.local/bin/llm_sF8_fragment.sh
bind M-F3 exec x-terminal-emulator -e /home/linaro/.local/bin/llm_pipe_selected_sys.sh
bind M-F2 exec x-terminal-emulator -e /home/linaro/.local/bin/llm_sF6_system_prompt.sh
bind M-F1 exec x-terminal-emulator -e /home/linaro/.local/bin/llm_sF4_prompt.sh
bind Left focusleft
bind KP_9 exec rpws 9
bind KP_8 exec rpws 8
bind KP_7 exec rpws 7
bind KP_6 exec rpws 6
bind KP_5 exec rpws 5
bind KP_4 exec rpws 4
bind KP_3 exec rpws 3
bind KP_2 exec rpws 2
bind KP_1 exec rpws 1
bind ISO_Left_Tab exec rpws next
bind i exec viewnior
bind h exec x-terminal-emulator -e bpytop
bind g exec gsimplecal
bind F8 exec flatpak run io.github.zaps166.QMPlay2
bind F7 exec flatpak run com.github.ryonakano.reco
bind F6 exec flatpak run com.strlen.TreeSheets
bind F5 exec flatpak run com.github.tenderowl.frog
bind F4 exec flatpak run org.filezillaproject.Filezilla
bind F1 exec xnc /home/linaro/RAM.txt
bind f only
bind Escape abort
bind equal hsplit
bind e exec xnedit
bind Down focusdown
bind C-Tab exec rpws prev
bind C-s-Tab exec rpws moveprev
bind C-s-9 exec rpws move9
bind C-s-8 exec rpws move8
bind C-s-7 exec rpws move7
bind C-s-6 exec rpws move6
bind C-s-5 exec rpws move5
bind C-s-4 exec rpws move4
bind C-s-3 exec rpws move3
bind C-s-2 exec rpws move2
bind C-s-1 exec rpws move1
bind C-9 exec rpws 9
bind C-8 exec rpws 8
bind C-7 exec rpws 7
bind C-6 exec rpws 6
bind C-5 exec rpws 5
bind C-4 exec rpws 4
bind C-3 exec rpws 3
bind C-2 exec rpws 2
bind C-1 exec rpws 1
bind BackSpace next
bind b exec vorta

addhook titlechanged exec rpbarsend
addhook switchwin exec rpbarsend
addhook switchgroup exec rpbarsend
addhook switchgroup next
addhook switchframe exec rpbarsend
addhook newwindow exec rpbarsend
addhook deletewindow exec rpbarsend
{% endcodeblock %}

#### ~/.local/bin/*.sh shell scripts

##### `shell/llm_analyze_file.sh`
```bash
#!/bin/bash
# Script to analyze a file with /home/linaro/.local/bin/llm (o3-mini) using a specific prompt.
# Refactored by Gemini to use `script` and `xsel` for capturing all terminal output to clipboard.

GEMINI_CAPTURE_MODE="${GEMINI_CAPTURE_MODE:-outer}" # Default to outer mode

if [ "$GEMINI_CAPTURE_MODE" = "inner" ]; then
    # INNER EXECUTION: This is the original script logic.
    # All terminal I/O here is captured by the `script` command.
    echo "/home/linaro/.local/bin/llm File Analysis (o3-mini)"
    echo "Enter the full path to the file you want to analyze (Ctrl+D or empty to cancel):"
    read -p "File Path: " FILE_PATH

    if [ -z "$FILE_PATH" ]; then
        echo "No file path entered. Exiting."
    elif [ -f "$FILE_PATH" ]; then
        SYSTEM_PROMPT_TEXT="Use your full analytic capacity to provide a thorough explanation: In what fundamental and causal ways does the file ('$FILE_PATH') consist? Please discuss: (1) Key events or conditions leading to its current state; (2) Its essential or structural nature; (3) Its broader purpose and significance."
        
        echo ""
        echo "Analyzing file: $FILE_PATH"
        echo "Using model: o3-mini"
        echo "Waiting for /home/linaro/.local/bin/llm response..."
        echo ""

        cat "$FILE_PATH" | /home/linaro/.local/bin/llm -m o3-mini -s "$SYSTEM_PROMPT_TEXT"
    else
        echo "File not found: $FILE_PATH" >&2
    fi
    
    printf '\n/home/linaro/.local/bin/llm command finished. Press any key to close this terminal...'
    read -n 1 -s -r
    exit 0 # Exit the inner script

else
    # OUTER EXECUTION: Set up `script`, run inner logic, then handle clipboard.
    _GEMINI_LOG_FILE_BASENAME="$(basename "$0" .sh)_session"
    _GEMINI_LOG_FILE=$(mktemp "/tmp/${_GEMINI_LOG_FILE_BASENAME}_XXXXXXXXXX.log")
    
    if [ -z "$_GEMINI_LOG_FILE" ] || [ ! -f "$_GEMINI_LOG_FILE" ]; then
        echo "Error: Failed to create temporary log file." >&2
        printf '\nPress any key to close this terminal...' && read -n 1 -s -r
        exit 1
    fi
    
    trap 'rm -f "$_GEMINI_LOG_FILE"' EXIT HUP INT TERM
    
    if ! command -v script &>/dev/null; then
        echo "Error: 'script' command not found. Please install it (e.g., sudo apt install bsdutils)." >&2
        printf '\nPress any key to close this terminal...' && read -n 1 -s -r
        exit 1
    fi

    script -q -e -c "GEMINI_CAPTURE_MODE=inner bash \"$0\" \"$@\"" "$_GEMINI_LOG_FILE"
    script_exit_status=$?
    
    if [ -f "$_GEMINI_LOG_FILE" ]; then
        if [ -s "$_GEMINI_LOG_FILE" ]; then
            if command -v xsel &>/dev/null; then
                CLEANED_CONTENT=""
                if command -v col &>/dev/null; then
                    CLEANED_CONTENT=$(col -b < "$_GEMINI_LOG_FILE")
                else
                    CLEANED_CONTENT=$(cat "$_GEMINI_LOG_FILE")
                    echo "Warning: 'col' command not found. Log content might contain unprocessed backspace characters." >&2
                fi

                if command -v sed &>/dev/null; then
                    FINAL_CONTENT=$(echo "$CLEANED_CONTENT" | sed -E 's/\x1B\[[0-9;?]*[a-zA-Z]//g; s/\r$//g; s/\r([^\n])/\1/g')
                    if echo "$FINAL_CONTENT" | xsel --clipboard --input; then
                        echo "Terminal session (cleaned) copied to clipboard using xsel."
                    else
                        echo "Error: xsel command failed to copy to clipboard (exit code $?)." >&2
                    fi
                else
                    echo "Warning: 'sed' command not found. ANSI escape codes and some carriage returns may not be removed." >&2
                    if echo "$CLEANED_CONTENT" | xsel --clipboard --input; then
                        echo "Terminal session (partially cleaned) copied to clipboard using xsel."
                    else
                        echo "Error: xsel command failed to copy to clipboard (exit code $?)." >&2
                    fi
                fi
            else
                echo "Error: 'xsel' command not found. Please install it (e.g., sudo apt install xsel). Skipping clipboard copy." >&2
            fi
        else
            echo "Terminal session log is empty; clipboard not updated."
        fi
    else
        echo "Error: Terminal session log file not found at '$_GEMINI_LOG_FILE'." >&2
    fi

    printf '\nClipboard operation finished. Press any key to close this wrapper terminal...'
    read -n 1 -s -r
    exit $script_exit_status
fi
```

##### `shell/llm_pipe_selected_sys.sh`
```bash
#!/bin/bash
# Takes selected text (clipboard/primary) and pipes to /home/linaro/.local/bin/llm with a user-provided system prompt.
# Refactored by Gemini to use `script` and `xsel` for capturing all terminal output to clipboard.

GEMINI_CAPTURE_MODE="${GEMINI_CAPTURE_MODE:-outer}"

if [ "$GEMINI_CAPTURE_MODE" = "inner" ]; then
    SELECTED_TEXT=$(xsel --clipboard --output 2>/dev/null) # Use xsel to get clipboard
    if [ -z "$SELECTED_TEXT" ]; then
        SELECTED_TEXT=$(xsel --primary --output 2>/dev/null) # Try primary selection
    fi

    if [ -z "$SELECTED_TEXT" ]; then
        echo "Action cancelled: No text found in clipboard or primary selection (used xsel). Copy text first."
        printf '\nPress any key to close...'
        read -n 1 -s -r
        exit 1
    fi

    echo "Selected text obtained."
    echo "Please enter the System Prompt for the selected text (Ctrl+D or empty to cancel):"
    read -p "System Prompt: " SYSTEM_PROMPT

    if [ -z "$SYSTEM_PROMPT" ]; then
        echo "Action cancelled: No system prompt provided."
    else
        echo ""
        echo "Processing selected text with system prompt: $SYSTEM_PROMPT"
        echo "--- Selected Text Start (first 200 chars) ---"
        echo "$SELECTED_TEXT" | head -c 200
        echo "--- Selected Text End (truncated if long) ---"
        echo "Waiting for /home/linaro/.local/bin/llm response..."
        echo ""
        echo "$SELECTED_TEXT" | /home/linaro/.local/bin/llm --system "$SYSTEM_PROMPT"
    fi

    printf '\n/home/linaro/.local/bin/llm command finished. Press any key to close this terminal...'
    read -n 1 -s -r
    exit 0

else
    # OUTER EXECUTION
    _GEMINI_LOG_FILE_BASENAME="$(basename "$0" .sh)_session"
    _GEMINI_LOG_FILE=$(mktemp "/tmp/${_GEMINI_LOG_FILE_BASENAME}_XXXXXXXXXX.log")
    
    if [ -z "$_GEMINI_LOG_FILE" ] || [ ! -f "$_GEMINI_LOG_FILE" ]; then
        echo "Error: Failed to create temporary log file." >&2
        printf '\nPress any key to close this terminal...' && read -n 1 -s -r
        exit 1
    fi
    
    trap 'rm -f "$_GEMINI_LOG_FILE"' EXIT HUP INT TERM
    
    if ! command -v script &>/dev/null; then
        echo "Error: 'script' command not found. Please install it (e.g., sudo apt install bsdutils)." >&2
        printf '\nPress any key to close this terminal...' && read -n 1 -s -r
        exit 1
    fi

    script -q -e -c "GEMINI_CAPTURE_MODE=inner bash \"$0\" \"$@\"" "$_GEMINI_LOG_FILE"
    script_exit_status=$?
    
    if [ -f "$_GEMINI_LOG_FILE" ]; then
        if [ -s "$_GEMINI_LOG_FILE" ]; then
            if command -v xsel &>/dev/null; then
                CLEANED_CONTENT=""
                if command -v col &>/dev/null; then
                    CLEANED_CONTENT=$(col -b < "$_GEMINI_LOG_FILE")
                else
                    CLEANED_CONTENT=$(cat "$_GEMINI_LOG_FILE")
                    echo "Warning: 'col' command not found. Log content might contain unprocessed backspace characters." >&2
                fi

                if command -v sed &>/dev/null; then
                    FINAL_CONTENT=$(echo "$CLEANED_CONTENT" | sed -E 's/\x1B\[[0-9;?]*[a-zA-Z]//g; s/\r$//g; s/\r([^\n])/\1/g')
                    if echo "$FINAL_CONTENT" | xsel --clipboard --input; then
                        echo "Terminal session (cleaned) copied to clipboard using xsel."
                    else
                        echo "Error: xsel command failed to copy to clipboard (exit code $?)." >&2
                    fi
                else
                    echo "Warning: 'sed' command not found. ANSI escape codes and some carriage returns may not be removed." >&2
                    if echo "$CLEANED_CONTENT" | xsel --clipboard --input; then
                        echo "Terminal session (partially cleaned) copied to clipboard using xsel."
                    else
                        echo "Error: xsel command failed to copy to clipboard (exit code $?)." >&2
                    fi
                fi
            else
                echo "Error: 'xsel' command not found. Please install it (e.g., sudo apt install xsel). Skipping clipboard copy." >&2
            fi
        else
            echo "Terminal session log is empty; clipboard not updated."
        fi
    else
        echo "Error: Terminal session log file not found at '$_GEMINI_LOG_FILE'." >&2
    fi

    printf '\nClipboard operation finished. Press any key to close this wrapper terminal...'
    read -n 1 -s -r
    exit $script_exit_status
fi
```

##### `shell/llm_sF11_list_fragments.sh`
```bash
#!/bin/bash
# Lists /home/linaro/.local/bin/llm fragments.
# Refactored by Gemini to use `script` and `xsel` for capturing all terminal output to clipboard.

GEMINI_CAPTURE_MODE="${GEMINI_CAPTURE_MODE:-outer}"

if [ "$GEMINI_CAPTURE_MODE" = "inner" ]; then
    echo "/home/linaro/.local/bin/llm Fragments List"
    echo "Fetching list..."
    echo ""
    /home/linaro/.local/bin/llm fragments list
    
    printf '\n/home/linaro/.local/bin/llm command finished. Press any key to close this terminal...'
    read -n 1 -s -r
    exit 0

else
    # OUTER EXECUTION
    _GEMINI_LOG_FILE_BASENAME="$(basename "$0" .sh)_session"
    _GEMINI_LOG_FILE=$(mktemp "/tmp/${_GEMINI_LOG_FILE_BASENAME}_XXXXXXXXXX.log")
    
    if [ -z "$_GEMINI_LOG_FILE" ] || [ ! -f "$_GEMINI_LOG_FILE" ]; then
        echo "Error: Failed to create temporary log file." >&2
        printf '\nPress any key to close this terminal...' && read -n 1 -s -r
        exit 1
    fi
    
    trap 'rm -f "$_GEMINI_LOG_FILE"' EXIT HUP INT TERM
    
    if ! command -v script &>/dev/null; then
        echo "Error: 'script' command not found. Please install it (e.g., sudo apt install bsdutils)." >&2
        printf '\nPress any key to close this terminal...' && read -n 1 -s -r
        exit 1
    fi

    script -q -e -c "GEMINI_CAPTURE_MODE=inner bash \"$0\" \"$@\"" "$_GEMINI_LOG_FILE"
    script_exit_status=$?
    
    if [ -f "$_GEMINI_LOG_FILE" ]; then
        if [ -s "$_GEMINI_LOG_FILE" ]; then
            if command -v xsel &>/dev/null; then
                CLEANED_CONTENT=""
                if command -v col &>/dev/null; then
                    CLEANED_CONTENT=$(col -b < "$_GEMINI_LOG_FILE")
                else
                    CLEANED_CONTENT=$(cat "$_GEMINI_LOG_FILE")
                    echo "Warning: 'col' command not found. Log content might contain unprocessed backspace characters." >&2
                fi

                if command -v sed &>/dev/null; then
                    FINAL_CONTENT=$(echo "$CLEANED_CONTENT" | sed -E 's/\x1B\[[0-9;?]*[a-zA-Z]//g; s/\r$//g; s/\r([^\n])/\1/g')
                    if echo "$FINAL_CONTENT" | xsel --clipboard --input; then
                        echo "Terminal session (cleaned) copied to clipboard using xsel."
                    else
                        echo "Error: xsel command failed to copy to clipboard (exit code $?)." >&2
                    fi
                else
                    echo "Warning: 'sed' command not found. ANSI escape codes and some carriage returns may not be removed." >&2
                    if echo "$CLEANED_CONTENT" | xsel --clipboard --input; then
                        echo "Terminal session (partially cleaned) copied to clipboard using xsel."
                    else
                        echo "Error: xsel command failed to copy to clipboard (exit code $?)." >&2
                    fi
                fi
            else
                echo "Error: 'xsel' command not found. Please install it (e.g., sudo apt install xsel). Skipping clipboard copy." >&2
            fi
        else
            echo "Terminal session log is empty; clipboard not updated."
        fi
    else
        echo "Error: Terminal session log file not found at '$_GEMINI_LOG_FILE'." >&2
    fi

    printf '\nClipboard operation finished. Press any key to close this wrapper terminal...'
    read -n 1 -s -r
    exit $script_exit_status
fi
```

##### `shell/llm_sF12_extract_last.sh`
```bash
#!/bin/bash
# Prompts for a message and sends it to /home/linaro/.local/bin/llm with o3-mini, extracting the last code block.
# Refactored by Gemini to use `script` and `xsel` for capturing all terminal output to clipboard.

GEMINI_CAPTURE_MODE="${GEMINI_CAPTURE_MODE:-outer}"

if [ "$GEMINI_CAPTURE_MODE" = "inner" ]; then
    echo "/home/linaro/.local/bin/llm Extract Last Code Block (o3-mini)"
    read -p "Enter your prompt: " prompt_text
    
    if [ -z "$prompt_text" ]; then
        echo "No prompt entered. Exiting."
    else
        /home/linaro/.local/bin/llm -m o3-mini --xl "$prompt_text"
    fi
    
    printf '\n/home/linaro/.local/bin/llm command finished. Press any key to close this terminal...'
    read -n 1 -s -r
    exit 0

else
    # OUTER EXECUTION
    _GEMINI_LOG_FILE_BASENAME="$(basename "$0" .sh)_session"
    _GEMINI_LOG_FILE=$(mktemp "/tmp/${_GEMINI_LOG_FILE_BASENAME}_XXXXXXXXXX.log")
    
    if [ -z "$_GEMINI_LOG_FILE" ] || [ ! -f "$_GEMINI_LOG_FILE" ]; then
        echo "Error: Failed to create temporary log file." >&2
        printf '\nPress any key to close this terminal...' && read -n 1 -s -r
        exit 1
    fi
    
    trap 'rm -f "$_GEMINI_LOG_FILE"' EXIT HUP INT TERM
    
    if ! command -v script &>/dev/null; then
        echo "Error: 'script' command not found. Please install it (e.g., sudo apt install bsdutils)." >&2
        printf '\nPress any key to close this terminal...' && read -n 1 -s -r
        exit 1
    fi

    script -q -e -c "GEMINI_CAPTURE_MODE=inner bash \"$0\" \"$@\"" "$_GEMINI_LOG_FILE"
    script_exit_status=$?
    
    if [ -f "$_GEMINI_LOG_FILE" ]; then
        if [ -s "$_GEMINI_LOG_FILE" ]; then
            if command -v xsel &>/dev/null; then
                CLEANED_CONTENT=""
                if command -v col &>/dev/null; then
                    CLEANED_CONTENT=$(col -b < "$_GEMINI_LOG_FILE")
                else
                    CLEANED_CONTENT=$(cat "$_GEMINI_LOG_FILE")
                    echo "Warning: 'col' command not found. Log content might contain unprocessed backspace characters." >&2
                fi

                if command -v sed &>/dev/null; then
                    FINAL_CONTENT=$(echo "$CLEANED_CONTENT" | sed -E 's/\x1B\[[0-9;?]*[a-zA-Z]//g; s/\r$//g; s/\r([^\n])/\1/g')
                    if echo "$FINAL_CONTENT" | xsel --clipboard --input; then
                        echo "Terminal session (cleaned) copied to clipboard using xsel."
                    else
                        echo "Error: xsel command failed to copy to clipboard (exit code $?)." >&2
                    fi
                else
                    echo "Warning: 'sed' command not found. ANSI escape codes and some carriage returns may not be removed." >&2
                    if echo "$CLEANED_CONTENT" | xsel --clipboard --input; then
                        echo "Terminal session (partially cleaned) copied to clipboard using xsel."
                    else
                        echo "Error: xsel command failed to copy to clipboard (exit code $?)." >&2
                    fi
                fi
            else
                echo "Error: 'xsel' command not found. Please install it (e.g., sudo apt install xsel). Skipping clipboard copy." >&2
            fi
        else
            echo "Terminal session log is empty; clipboard not updated."
        fi
    else
        echo "Error: Terminal session log file not found at '$_GEMINI_LOG_FILE'." >&2
    fi

    printf '\nClipboard operation finished. Press any key to close this wrapper terminal...'
    read -n 1 -s -r
    exit $script_exit_status
fi
```

##### `shell/llm_sF4_prompt.sh`
```bash
#!/bin/bash
# Prompts for a message and sends it to /home/linaro/.local/bin/llm with gpt-4.1.
# Refactored by Gemini to use `script` and `xsel` for capturing all terminal output to clipboard.

GEMINI_CAPTURE_MODE="${GEMINI_CAPTURE_MODE:-outer}"

if [ "$GEMINI_CAPTURE_MODE" = "inner" ]; then
    echo "/home/linaro/.local/bin/llm with gpt-4.1"
    read -p "Enter your prompt: " prompt_text
    
    if [ -z "$prompt_text" ]; then
        echo "No prompt entered. Exiting."
    else
        /home/linaro/.local/bin/llm -m gpt-4.1 "$prompt_text"
    fi
    
    printf '\n/home/linaro/.local/bin/llm command finished. Press any key to close this terminal...'
    read -n 1 -s -r
    exit 0

else
    # OUTER EXECUTION
    _GEMINI_LOG_FILE_BASENAME="$(basename "$0" .sh)_session"
    _GEMINI_LOG_FILE=$(mktemp "/tmp/${_GEMINI_LOG_FILE_BASENAME}_XXXXXXXXXX.log")
    
    if [ -z "$_GEMINI_LOG_FILE" ] || [ ! -f "$_GEMINI_LOG_FILE" ]; then
        echo "Error: Failed to create temporary log file." >&2
        printf '\nPress any key to close this terminal...' && read -n 1 -s -r
        exit 1
    fi
    
    trap 'rm -f "$_GEMINI_LOG_FILE"' EXIT HUP INT TERM
    
    if ! command -v script &>/dev/null; then
        echo "Error: 'script' command not found. Please install it (e.g., sudo apt install bsdutils)." >&2
        printf '\nPress any key to close this terminal...' && read -n 1 -s -r
        exit 1
    fi

    script -q -e -c "GEMINI_CAPTURE_MODE=inner bash \"$0\" \"$@\"" "$_GEMINI_LOG_FILE"
    script_exit_status=$?
    
    if [ -f "$_GEMINI_LOG_FILE" ]; then
        if [ -s "$_GEMINI_LOG_FILE" ]; then
            if command -v xsel &>/dev/null; then
                CLEANED_CONTENT=""
                if command -v col &>/dev/null; then
                    CLEANED_CONTENT=$(col -b < "$_GEMINI_LOG_FILE")
                else
                    CLEANED_CONTENT=$(cat "$_GEMINI_LOG_FILE")
                    echo "Warning: 'col' command not found. Log content might contain unprocessed backspace characters." >&2
                fi

                if command -v sed &>/dev/null; then
                    FINAL_CONTENT=$(echo "$CLEANED_CONTENT" | sed -E 's/\x1B\[[0-9;?]*[a-zA-Z]//g; s/\r$//g; s/\r([^\n])/\1/g')
                    if echo "$FINAL_CONTENT" | xsel --clipboard --input; then
                        echo "Terminal session (cleaned) copied to clipboard using xsel."
                    else
                        echo "Error: xsel command failed to copy to clipboard (exit code $?)." >&2
                    fi
                else
                    echo "Warning: 'sed' command not found. ANSI escape codes and some carriage returns may not be removed." >&2
                    if echo "$CLEANED_CONTENT" | xsel --clipboard --input; then
                        echo "Terminal session (partially cleaned) copied to clipboard using xsel."
                    else
                        echo "Error: xsel command failed to copy to clipboard (exit code $?)." >&2
                    fi
                fi
            else
                echo "Error: 'xsel' command not found. Please install it (e.g., sudo apt install xsel). Skipping clipboard copy." >&2
            fi
        else
            echo "Terminal session log is empty; clipboard not updated."
        fi
    else
        echo "Error: Terminal session log file not found at '$_GEMINI_LOG_FILE'." >&2
    fi

    printf '\nClipboard operation finished. Press any key to close this wrapper terminal...'
    read -n 1 -s -r
    exit $script_exit_status
fi
```

##### `shell/llm_sF6_system_prompt.sh`
```bash
#!/bin/bash
# Prompts for a system prompt and a main prompt for llm.
# Refactored by Gemini to use `script` and `xsel` for capturing all terminal output to clipboard.

GEMINI_CAPTURE_MODE="${GEMINI_CAPTURE_MODE:-outer}"

if [ "$GEMINI_CAPTURE_MODE" = "inner" ]; then
    echo "/home/linaro/.local/bin/llm with System Prompt"
    read -p "Enter SYSTEM prompt: " system_prompt
    if [ -z "$system_prompt" ]; then
        echo "No system prompt entered. Exiting."
        printf '\nPress any key to close...'
        read -n 1 -s -r
        exit 1
    fi
    
    read -p "Enter MAIN prompt: " main_prompt
    if [ -z "$main_prompt" ]; then
        echo "No main prompt entered. Exiting."
    else
        /home/linaro/.local/bin/llm --system "$system_prompt" "$main_prompt"
    fi
    
    printf '\n/home/linaro/.local/bin/llm command finished. Press any key to close this terminal...'
    read -n 1 -s -r
    exit 0

else
    # OUTER EXECUTION
    _GEMINI_LOG_FILE_BASENAME="$(basename "$0" .sh)_session"
    _GEMINI_LOG_FILE=$(mktemp "/tmp/${_GEMINI_LOG_FILE_BASENAME}_XXXXXXXXXX.log")
    
    if [ -z "$_GEMINI_LOG_FILE" ] || [ ! -f "$_GEMINI_LOG_FILE" ]; then
        echo "Error: Failed to create temporary log file." >&2
        printf '\nPress any key to close this terminal...' && read -n 1 -s -r
        exit 1
    fi
    
    trap 'rm -f "$_GEMINI_LOG_FILE"' EXIT HUP INT TERM
    
    if ! command -v script &>/dev/null; then
        echo "Error: 'script' command not found. Please install it (e.g., sudo apt install bsdutils)." >&2
        printf '\nPress any key to close this terminal...' && read -n 1 -s -r
        exit 1
    fi

    script -q -e -c "GEMINI_CAPTURE_MODE=inner bash \"$0\" \"$@\"" "$_GEMINI_LOG_FILE"
    script_exit_status=$?
    
    if [ -f "$_GEMINI_LOG_FILE" ]; then
        if [ -s "$_GEMINI_LOG_FILE" ]; then
            if command -v xsel &>/dev/null; then
                CLEANED_CONTENT=""
                if command -v col &>/dev/null; then
                    CLEANED_CONTENT=$(col -b < "$_GEMINI_LOG_FILE")
                else
                    CLEANED_CONTENT=$(cat "$_GEMINI_LOG_FILE")
                    echo "Warning: 'col' command not found. Log content might contain unprocessed backspace characters." >&2
                fi

                if command -v sed &>/dev/null; then
                    FINAL_CONTENT=$(echo "$CLEANED_CONTENT" | sed -E 's/\x1B\[[0-9;?]*[a-zA-Z]//g; s/\r$//g; s/\r([^\n])/\1/g')
                    if echo "$FINAL_CONTENT" | xsel --clipboard --input; then
                        echo "Terminal session (cleaned) copied to clipboard using xsel."
                    else
                        echo "Error: xsel command failed to copy to clipboard (exit code $?)." >&2
                    fi
                else
                    echo "Warning: 'sed' command not found. ANSI escape codes and some carriage returns may not be removed." >&2
                    if echo "$CLEANED_CONTENT" | xsel --clipboard --input; then
                        echo "Terminal session (partially cleaned) copied to clipboard using xsel."
                    else
                        echo "Error: xsel command failed to copy to clipboard (exit code $?)." >&2
                    fi
                fi
            else
                echo "Error: 'xsel' command not found. Please install it (e.g., sudo apt install xsel). Skipping clipboard copy." >&2
            fi
        else
            echo "Terminal session log is empty; clipboard not updated."
        fi
    else
        echo "Error: Terminal session log file not found at '$_GEMINI_LOG_FILE'." >&2
    fi

    printf '\nClipboard operation finished. Press any key to close this wrapper terminal...'
    read -n 1 -s -r
    exit $script_exit_status
fi
```

##### `shell/llm_sF8_fragment.sh`
```bash
#!/bin/bash
# Prompts for a fragment source and a main prompt for llm.
# Refactored by Gemini to use `script` and `xsel` for capturing all terminal output to clipboard.

GEMINI_CAPTURE_MODE="${GEMINI_CAPTURE_MODE:-outer}"

if [ "$GEMINI_CAPTURE_MODE" = "inner" ]; then
    echo "/home/linaro/.local/bin/llm with Fragment"
    read -p "Enter fragment source (URL or file path): " fragment_source
    if [ -z "$fragment_source" ]; then
        echo "No fragment source entered. Exiting."
        printf '\nPress any key to close...'
        read -n 1 -s -r
        exit 1
    fi
    
    read -p "Enter MAIN prompt: " main_prompt
    if [ -z "$main_prompt" ]; then
        echo "No main prompt entered. Exiting."
    else
        /home/linaro/.local/bin/llm -f "$fragment_source" "$main_prompt"
    fi
    
    printf '\n/home/linaro/.local/bin/llm command finished. Press any key to close this terminal...'
    read -n 1 -s -r
    exit 0

else
    # OUTER EXECUTION
    _GEMINI_LOG_FILE_BASENAME="$(basename "$0" .sh)_session"
    _GEMINI_LOG_FILE=$(mktemp "/tmp/${_GEMINI_LOG_FILE_BASENAME}_XXXXXXXXXX.log")
    
    if [ -z "$_GEMINI_LOG_FILE" ] || [ ! -f "$_GEMINI_LOG_FILE" ]; then
        echo "Error: Failed to create temporary log file." >&2
        printf '\nPress any key to close this terminal...' && read -n 1 -s -r
        exit 1
    fi
    
    trap 'rm -f "$_GEMINI_LOG_FILE"' EXIT HUP INT TERM
    
    if ! command -v script &>/dev/null; then
        echo "Error: 'script' command not found. Please install it (e.g., sudo apt install bsdutils)." >&2
        printf '\nPress any key to close this terminal...' && read -n 1 -s -r
        exit 1
    fi

    script -q -e -c "GEMINI_CAPTURE_MODE=inner bash \"$0\" \"$@\"" "$_GEMINI_LOG_FILE"
    script_exit_status=$?
    
    if [ -f "$_GEMINI_LOG_FILE" ]; then
        if [ -s "$_GEMINI_LOG_FILE" ]; then
            if command -v xsel &>/dev/null; then
                CLEANED_CONTENT=""
                if command -v col &>/dev/null; then
                    CLEANED_CONTENT=$(col -b < "$_GEMINI_LOG_FILE")
                else
                    CLEANED_CONTENT=$(cat "$_GEMINI_LOG_FILE")
                    echo "Warning: 'col' command not found. Log content might contain unprocessed backspace characters." >&2
                fi

                if command -v sed &>/dev/null; then
                    FINAL_CONTENT=$(echo "$CLEANED_CONTENT" | sed -E 's/\x1B\[[0-9;?]*[a-zA-Z]//g; s/\r$//g; s/\r([^\n])/\1/g')
                    if echo "$FINAL_CONTENT" | xsel --clipboard --input; then
                        echo "Terminal session (cleaned) copied to clipboard using xsel."
                    else
                        echo "Error: xsel command failed to copy to clipboard (exit code $?)." >&2
                    fi
                else
                    echo "Warning: 'sed' command not found. ANSI escape codes and some carriage returns may not be removed." >&2
                    if echo "$CLEANED_CONTENT" | xsel --clipboard --input; then
                        echo "Terminal session (partially cleaned) copied to clipboard using xsel."
                    else
                        echo "Error: xsel command failed to copy to clipboard (exit code $?)." >&2
                    fi
                fi
            else
                echo "Error: 'xsel' command not found. Please install it (e.g., sudo apt install xsel). Skipping clipboard copy." >&2
            fi
        else
            echo "Terminal session log is empty; clipboard not updated."
        fi
    else
        echo "Error: Terminal session log file not found at '$_GEMINI_LOG_FILE'." >&2
    fi

    printf '\nClipboard operation finished. Press any key to close this wrapper terminal...'
    read -n 1 -s -r
    exit $script_exit_status
fi
```

##### `shell/llm_sF9_attachment.sh`
```bash
#!/bin/bash
# Prompts for a main prompt and an attachment for /home/linaro/.local/bin/llm with gpt-4.1-mini.
# Refactored by Gemini to use `script` and `xsel` for capturing all terminal output to clipboard.

GEMINI_CAPTURE_MODE="${GEMINI_CAPTURE_MODE:-outer}"

if [ "$GEMINI_CAPTURE_MODE" = "inner" ]; then
    echo "/home/linaro/.local/bin/llm with Attachment (gpt-4.1-mini)"
    read -p "Enter MAIN prompt: " main_prompt
    if [ -z "$main_prompt" ]; then
        echo "No main prompt entered. Exiting."
        printf '\nPress any key to close...'
        read -n 1 -s -r
        exit 1
    fi
    
    read -p "Enter attachment (URL or file path): " attachment_source
    if [ -z "$attachment_source" ]; then
        echo "No attachment source entered. Exiting."
    else
        /home/linaro/.local/bin/llm -m gpt-4.1-mini "$main_prompt" -a "$attachment_source"
    fi
    
    printf '\n/home/linaro/.local/bin/llm command finished. Press any key to close this terminal...'
    read -n 1 -s -r
    exit 0

else
    # OUTER EXECUTION
    _GEMINI_LOG_FILE_BASENAME="$(basename "$0" .sh)_session"
    _GEMINI_LOG_FILE=$(mktemp "/tmp/${_GEMINI_LOG_FILE_BASENAME}_XXXXXXXXXX.log")
    
    if [ -z "$_GEMINI_LOG_FILE" ] || [ ! -f "$_GEMINI_LOG_FILE" ]; then
        echo "Error: Failed to create temporary log file." >&2
        printf '\nPress any key to close this terminal...' && read -n 1 -s -r
        exit 1
    fi
    
    trap 'rm -f "$_GEMINI_LOG_FILE"' EXIT HUP INT TERM
    
    if ! command -v script &>/dev/null; then
        echo "Error: 'script' command not found. Please install it (e.g., sudo apt install bsdutils)." >&2
        printf '\nPress any key to close this terminal...' && read -n 1 -s -r
        exit 1
    fi

    script -q -e -c "GEMINI_CAPTURE_MODE=inner bash \"$0\" \"$@\"" "$_GEMINI_LOG_FILE"
    script_exit_status=$?
    
    if [ -f "$_GEMINI_LOG_FILE" ]; then
        if [ -s "$_GEMINI_LOG_FILE" ]; then
            if command -v xsel &>/dev/null; then
                CLEANED_CONTENT=""
                if command -v col &>/dev/null; then
                    CLEANED_CONTENT=$(col -b < "$_GEMINI_LOG_FILE")
                else
                    CLEANED_CONTENT=$(cat "$_GEMINI_LOG_FILE")
                    echo "Warning: 'col' command not found. Log content might contain unprocessed backspace characters." >&2
                fi

                if command -v sed &>/dev/null; then
                    FINAL_CONTENT=$(echo "$CLEANED_CONTENT" | sed -E 's/\x1B\[[0-9;?]*[a-zA-Z]//g; s/\r$//g; s/\r([^\n])/\1/g')
                    if echo "$FINAL_CONTENT" | xsel --clipboard --input; then
                        echo "Terminal session (cleaned) copied to clipboard using xsel."
                    else
                        echo "Error: xsel command failed to copy to clipboard (exit code $?)." >&2
                    fi
                else
                    echo "Warning: 'sed' command not found. ANSI escape codes and some carriage returns may not be removed." >&2
                    if echo "$CLEANED_CONTENT" | xsel --clipboard --input; then
                        echo "Terminal session (partially cleaned) copied to clipboard using xsel."
                    else
                        echo "Error: xsel command failed to copy to clipboard (exit code $?)." >&2
                    fi
                fi
            else
                echo "Error: 'xsel' command not found. Please install it (e.g., sudo apt install xsel). Skipping clipboard copy." >&2
            fi
        else
            echo "Terminal session log is empty; clipboard not updated."
        fi
    else
        echo "Error: Terminal session log file not found at '$_GEMINI_LOG_FILE'." >&2
    fi

    printf '\nClipboard operation finished. Press any key to close this wrapper terminal...'
    read -n 1 -s -r
    exit $script_exit_status
fi
```

#### ~/.rpbar.ini

```
[program]
# Window name for rpbar
win_name = rpbar

# Path for the communication socket with rpbarsend
# /tmp/ is generally standard and should work on Debian.
socket_path = /tmp/rpbarsocket

# Separator for program title (likely for ratpoison integration)
sep = $)@=

# Buffer size for communication with ratpoison
bufsize = 2048

# Timeout in seconds for communication
timeout_s = 5

[display]
# Whether rpbar is on the top (1) or bottom (0) of the screen
top = 0

# The Xorg screen (monitor) to display the bar on.
# '0' is typically the primary monitor. Adjust if you have multiple monitors
# and want it on a different one (e.g., 1 for secondary).
# Use `xrandr` to list screens if unsure.
screen = 0 ; Defaulting to primary screen, adjust if needed.

# Padding around the top/bottom of the text within the bar
padding = 4

# Left/right padding for elements like buttons
button_margin = 10

# Padding specifically for the status bar text area
status_padding = 30

# Font string for the bar (e.g., "Font Family Name:size=POINT_SIZE").
# CRITICAL: Ensure "Intel One Mono" is installed on your Debian Bullseye system.
# If not, replace with an available font (e.g., "DejaVu Sans Mono:size=10", "Liberation Mono:size=10", "Monospace:size=10").
# Check availability with `fc-list | grep "Your Font Name"`
font_str = Intel One Mono:size=13 ; ### VERIFY THIS FONT IS INSTALLED OR CHANGE IT ###

[color]
bordercolor = #d7d7d7
bgcolor = #353535
fgcolor = #d7d7d7
mainbgcolor = #d4ccb9
mainfgcolor = #45363b
statusbgcolor = #d7d7d7
statusfgcolor = #353535
```

#### **Configure dratmenu.py (/home/linaro/.local/bin/dratmenu.py)**

{% codeblock python %}
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
dratmenu.py: A dmenu-based window switcher for the Ratpoison Window Manager.

This script fetches the list of current windows from Ratpoison, presents them
in dmenu for selection, and then tells Ratpoison to switch to the chosen window.
It is updated for Python 3 and aims for robustness.
"""

import subprocess
import sys
import shlex # For safer command construction if needed, though not strictly required here

# --- Configuration ---

# Separator string used internally to parse Ratpoison output.
# IMPORTANT: This exact string MUST NOT appear in any window number, class, or title.
# Using a complex, unlikely sequence to minimize collision risk.
SEP = "~!@#DRATMENU_SEP#@!~"

# Separator used *within dmenu* to separate the hidden window number from the visible text.
# A tab character is often a good choice as it's unlikely to be the *first* character
# in the formatted display string and easy to split on.
DMENU_SEP = '\t'

# dmenu appearance settings (adjust as needed)
# Font examples:
# FONT = "-*-terminus-*-r-*-*-14-*-*-*-*-*-*-*"
# FONT = "-*-jetbrains mono-*-r-*-*-14-*-*-*-*-*-*-*"
FONT = 'Intel One Mono:size=13' # Default Terminus
NORMAL_BG = '#002b36'      # Solarized Dark base03
SELECTED_BG = '#859900'    # Solarized Dark green
NUM_LINES = '20'           # Number of lines dmenu shows vertically

# --- Helper Function ---

def run_subprocess(command_list, input_data=None):
    """
    Runs a subprocess, handling text encoding/decoding and errors.

    Args:
        command_list (list): The command and its arguments.
        input_data (str, optional): String data to pass to the command's stdin. Defaults to None.

    Returns:
        subprocess.CompletedProcess: The result object from subprocess.run.

    Raises:
        FileNotFoundError: If the command is not found.
        subprocess.CalledProcessError: If the command returns a non-zero exit code.
        Exception: For other unexpected errors during execution.
    """
    try:
        result = subprocess.run(
            command_list,
            input=input_data,
            capture_output=True, # Capture stdout and stderr
            text=True,           # Work with text (auto encodes input, decodes output)
            check=True,          # Raise CalledProcessError on non-zero exit codes
            encoding='utf-8'     # Explicitly use UTF-8
        )
        return result
    except FileNotFoundError:
        print(f"Error: Command '{command_list[0]}' not found. Is it installed and in your PATH?", file=sys.stderr)
        raise # Re-raise the exception to be caught by the main logic
    except subprocess.CalledProcessError as e:
        # check=True raises this, stderr is part of the exception object
        print(f"Error running command: {' '.join(e.cmd)}", file=sys.stderr)
        print(f"Return code: {e.returncode}", file=sys.stderr)
        if e.stderr:
            print(f"Stderr: {e.stderr.strip()}", file=sys.stderr)
        # Don't raise here if we want to handle specific return codes (like dmenu cancel) later
        # For now, let the main logic handle specific cases if needed, otherwise re-raise
        raise
    except Exception as e:
        print(f"An unexpected error occurred running {' '.join(command_list)}: {e}", file=sys.stderr)
        raise

# --- Main Logic ---

def main():
    # 1. Get window list from Ratpoison
    # Format: %n<SEP>%c<SEP>%t (number, class, title)
    rp_list_cmd = ['ratpoison', '-c', f"windows %n{SEP}%c{SEP}%t"]
    try:
        rp_result = run_subprocess(rp_list_cmd)
    except (FileNotFoundError, subprocess.CalledProcessError, Exception):
        sys.exit(1) # Error message already printed by run_subprocess

    # Process the output from Ratpoison
    stdout_str = rp_result.stdout.strip()
    if not stdout_str:
        print("No ratpoison windows found.", file=sys.stderr)
        sys.exit(0)

    lines = stdout_str.split('\n')
    windows_data = [] # Store tuples of (number, class, title)
    for i, ln in enumerate(lines):
        parts = ln.split(SEP)
        if len(parts) == 3:
            windows_data.append(parts)
        else:
            print(f"Warning: Skipping malformed line {i+1} from ratpoison (separator issue?): {ln}", file=sys.stderr)

    if not windows_data:
        print("No valid window data parsed from ratpoison.", file=sys.stderr)
        sys.exit(1)

    # 2. Format window list for dmenu
    # Format for dmenu input: "<number><DMENU_SEP><formatted_display_string>"
    # The <number> part is hidden by dmenu but used for selection later.
    dmenu_input_lines = []
    for num, current, title in windows_data:
        # Format the part visible in dmenu
        display_str = f"{num.rjust(3)} {current.ljust(10)[:10]} {title}"
        # Prepend the raw number and the dmenu separator
        dmenu_input_lines.append(f"{num}{DMENU_SEP}{display_str}")

    dmenu_input_text = '\n'.join(dmenu_input_lines)

    # 3. Pipe the list to dmenu and get the selection
    dmenu_cmd = ['dmenu', '-i',                # Case-insensitive
                 '-sb', SELECTED_BG,         # Selected background
                 '-nb', NORMAL_BG,           # Normal background
                 '-fn', FONT,                # Font
                 '-l', NUM_LINES]            # Lines to display

    try:
        # We expect dmenu might return 1 if the user cancels (e.g., Esc)
        # So, we temporarily disable check=True and handle return codes manually
        dmenu_result = subprocess.run(
            dmenu_cmd,
            input=dmenu_input_text,
            capture_output=True,
            text=True,
            encoding='utf-8'
            # check=False # Default, handle return code below
        )

        if dmenu_result.returncode == 1:
            # User cancelled dmenu (e.g., pressed Esc)
            print("dmenu cancelled by user.", file=sys.stderr)
            sys.exit(0)
        elif dmenu_result.returncode != 0:
            # Other dmenu error
            print(f"Error running dmenu.", file=sys.stderr)
            print(f"Return code: {dmenu_result.returncode}", file=sys.stderr)
            if dmenu_result.stderr:
                print(f"Stderr: {dmenu_result.stderr.strip()}", file=sys.stderr)
            sys.exit(1)

        selection = dmenu_result.stdout.strip()

    except FileNotFoundError:
        print(f"Error: Command 'dmenu' not found. Is it installed and in your PATH?", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred running dmenu: {e}", file=sys.stderr)
        sys.exit(1)

    # 4. Extract the *actual* window number from the selection
    if not selection:
        # Should not happen if return code was 0, but check anyway
        print("dmenu returned success but selection is empty.", file=sys.stderr)
        sys.exit(1)

    try:
        # Split the selected line ONLY at the first dmenu separator
        # The first part is the raw window number we embedded
        sel_number = selection.split(DMENU_SEP, 1)[0]

        # Basic validation that it looks like a number
        if not sel_number.isdigit():
             raise ValueError("Extracted selection number is not a digit.")

    except (IndexError, ValueError) as e:
        print(f"Error: Could not parse window number from dmenu selection.", file=sys.stderr)
        print(f"Selected line: '{selection}'", file=sys.stderr)
        print(f"Reason: {e}", file=sys.stderr)
        sys.exit(1)

    # 5. Tell Ratpoison to select the chosen window
    rp_select_cmd = ['ratpoison', '-c', f'select {sel_number}']
    try:
        run_subprocess(rp_select_cmd)
    except (FileNotFoundError, subprocess.CalledProcessError, Exception):
        # Error message already printed by run_subprocess
        sys.exit(1)

    # Success!
    sys.exit(0)

if __name__ == "__main__":
    main()
{% endcodeblock %}

#### **Configure ratpoison.py (/home/linaro/.local/bin/ratpoison.py)**

```python
import os
ratpoison = os.getenv('RATPOISON') or 'ratpoison'
def rp_command( *args ):
    p = os.popen( ratpoison + ' -c ' + '"' + (' '.join(  args  ) ) + '"', 'r' )
    r = p.readlines();
    p.close();
    return r


def rp_abort( *args ): return rp_command ( 'abort ' +  ' '.join( args ) )
def rp_addhook( *args ): return rp_command ( 'addhook ' +  ' '.join( args ) )
def rp_alias( *args ): return rp_command ( 'alias ' +  ' '.join( args ) )
def rp_banish( *args ): return rp_command ( 'banish ' +  ' '.join( args ) )
def rp_chdir( *args ): return rp_command ( 'chdir ' +  ' '.join( args ) )
def rp_clrunmanaged( *args ): return rp_command ( 'clrunmanaged ' +  ' '.join( args ) )
def rp_colon( *args ): return rp_command ( 'colon ' +  ' '.join( args ) )
def rp_curframe( *args ): return rp_command ( 'curframe ' +  ' '.join( args ) )
def rp_definekey( *args ): return rp_command ( 'definekey ' +  ' '.join( args ) )
def rp_undefinekey( *args ): return rp_command ( 'undefinekey ' +  ' '.join( args ) )
def rp_delete( *args ): return rp_command ( 'delete ' +  ' '.join( args ) )
def rp_delkmap( *args ): return rp_command ( 'delkmap ' +  ' '.join( args ) )
def rp_echo( *args ): return rp_command ( 'echo ' +  ' '.join( args ) )
def rp_escape( *args ): return rp_command ( 'escape ' +  ' '.join( args ) )
def rp_exec( *args ): return rp_command ( 'exec ' +  ' '.join( args ) )
def rp_execa( *args ): return rp_command ( 'execa ' +  ' '.join( args ) )
def rp_execf( *args ): return rp_command ( 'execf ' +  ' '.join( args ) )
def rp_fdump( *args ): return rp_command ( 'fdump ' +  ' '.join( args ) )
def rp_focus( *args ): return rp_command ( 'focus ' +  ' '.join( args ) )
def rp_focusprev( *args ): return rp_command ( 'focusprev ' +  ' '.join( args ) )
def rp_focusdown( *args ): return rp_command ( 'focusdown ' +  ' '.join( args ) )
def rp_exchangeup( *args ): return rp_command ( 'exchangeup ' +  ' '.join( args ) )
def rp_exchangedown( *args ): return rp_command ( 'exchangedown ' +  ' '.join( args ) )
def rp_exchangeleft( *args ): return rp_command ( 'exchangeleft ' +  ' '.join( args ) )
def rp_exchangeright( *args ): return rp_command ( 'exchangeright ' +  ' '.join( args ) )
def rp_swap( *args ): return rp_command ( 'swap ' +  ' '.join( args ) )
def rp_focuslast( *args ): return rp_command ( 'focuslast ' +  ' '.join( args ) )
def rp_focusleft( *args ): return rp_command ( 'focusleft ' +  ' '.join( args ) )
def rp_focusright( *args ): return rp_command ( 'focusright ' +  ' '.join( args ) )
def rp_focusup( *args ): return rp_command ( 'focusup ' +  ' '.join( args ) )
def rp_frestore( *args ): return rp_command ( 'frestore ' +  ' '.join( args ) )
def rp_fselect( *args ): return rp_command ( 'fselect ' +  ' '.join( args ) )
def rp_gdelete( *args ): return rp_command ( 'gdelete ' +  ' '.join( args ) )
def rp_getenv( *args ): return rp_command ( 'getenv ' +  ' '.join( args ) )
def rp_gmerge( *args ): return rp_command ( 'gmerge ' +  ' '.join( args ) )
def rp_gmove( *args ): return rp_command ( 'gmove ' +  ' '.join( args ) )
def rp_gnew( *args ): return rp_command ( 'gnew ' +  ' '.join( args ) )
def rp_gnewbg( *args ): return rp_command ( 'gnewbg ' +  ' '.join( args ) )
def rp_gnumber( *args ): return rp_command ( 'gnumber ' +  ' '.join( args ) )
def rp_grename( *args ): return rp_command ( 'grename ' +  ' '.join( args ) )
def rp_gnext( *args ): return rp_command ( 'gnext ' +  ' '.join( args ) )
def rp_gprev( *args ): return rp_command ( 'gprev ' +  ' '.join( args ) )
def rp_gother( *args ): return rp_command ( 'gother ' +  ' '.join( args ) )
def rp_gravity( *args ): return rp_command ( 'gravity ' +  ' '.join( args ) )
def rp_groups( *args ): return rp_command ( 'groups ' +  ' '.join( args ) )
def rp_gselect( *args ): return rp_command ( 'gselect ' +  ' '.join( args ) )
def rp_help( *args ): return rp_command ( 'help ' +  ' '.join( args ) )
def rp_hsplit( *args ): return rp_command ( 'hsplit ' +  ' '.join( args ) )
def rp_info( *args ): return rp_command ( 'info ' +  ' '.join( args ) )
def rp_kill( *args ): return rp_command ( 'kill ' +  ' '.join( args ) )
def rp_lastmsg( *args ): return rp_command ( 'lastmsg ' +  ' '.join( args ) )
def rp_license( *args ): return rp_command ( 'license ' +  ' '.join( args ) )
def rp_link( *args ): return rp_command ( 'link ' +  ' '.join( args ) )
def rp_listhook( *args ): return rp_command ( 'listhook ' +  ' '.join( args ) )
def rp_meta( *args ): return rp_command ( 'meta ' +  ' '.join( args ) )
def rp_msgwait( *args ): return rp_command ( 'msgwait ' +  ' '.join( args ) )
def rp_newkmap( *args ): return rp_command ( 'newkmap ' +  ' '.join( args ) )
def rp_newwm( *args ): return rp_command ( 'newwm ' +  ' '.join( args ) )
def rp_next( *args ): return rp_command ( 'next ' +  ' '.join( args ) )
def rp_nextscreen( *args ): return rp_command ( 'nextscreen ' +  ' '.join( args ) )
def rp_number( *args ): return rp_command ( 'number ' +  ' '.join( args ) )
def rp_only( *args ): return rp_command ( 'only ' +  ' '.join( args ) )
def rp_other( *args ): return rp_command ( 'other ' +  ' '.join( args ) )
def rp_prev( *args ): return rp_command ( 'prev ' +  ' '.join( args ) )
def rp_prevscreen( *args ): return rp_command ( 'prevscreen ' +  ' '.join( args ) )
def rp_quit( *args ): return rp_command ( 'quit ' +  ' '.join( args ) )
def rp_ratinfo( *args ): return rp_command ( 'ratinfo ' +  ' '.join( args ) )
def rp_ratrelinfo( *args ): return rp_command ( 'ratrelinfo ' +  ' '.join( args ) )
def rp_banishrel( *args ): return rp_command ( 'banishrel ' +  ' '.join( args ) )
def rp_ratwarp( *args ): return rp_command ( 'ratwarp ' +  ' '.join( args ) )
def rp_ratrelwarp( *args ): return rp_command ( 'ratrelwarp ' +  ' '.join( args ) )
def rp_ratclick( *args ): return rp_command ( 'ratclick ' +  ' '.join( args ) )
def rp_rathold( *args ): return rp_command ( 'rathold ' +  ' '.join( args ) )
def rp_readkey( *args ): return rp_command ( 'readkey ' +  ' '.join( args ) )
def rp_redisplay( *args ): return rp_command ( 'redisplay ' +  ' '.join( args ) )
def rp_remhook( *args ): return rp_command ( 'remhook ' +  ' '.join( args ) )
def rp_remove( *args ): return rp_command ( 'remove ' +  ' '.join( args ) )
def rp_removeup( *args ): return rp_command ( 'removeup ' +  ' '.join( args ) )
def rp_removedown( *args ): return rp_command ( 'removedown ' +  ' '.join( args ) )
def rp_removeleft( *args ): return rp_command ( 'removeleft ' +  ' '.join( args ) )
def rp_removeright( *args ): return rp_command ( 'removeright ' +  ' '.join( args ) )
def rp_resize( *args ): return rp_command ( 'resize ' +  ' '.join( args ) )
def rp_restart( *args ): return rp_command ( 'restart ' +  ' '.join( args ) )
def rp_rudeness( *args ): return rp_command ( 'rudeness ' +  ' '.join( args ) )
def rp_select( *args ): return rp_command ( 'select ' +  ' '.join( args ) )
def rp_set( *args ): return rp_command ( 'set ' +  ' '.join( args ) )
def rp_setenv( *args ): return rp_command ( 'setenv ' +  ' '.join( args ) )
def rp_shrink( *args ): return rp_command ( 'shrink ' +  ' '.join( args ) )
def rp_sfrestore( *args ): return rp_command ( 'sfrestore ' +  ' '.join( args ) )
def rp_source( *args ): return rp_command ( 'source ' +  ' '.join( args ) )
def rp_sselect( *args ): return rp_command ( 'sselect ' +  ' '.join( args ) )
def rp_startup_message( *args ): return rp_command ( 'startup_message ' +  ' '.join( args ) )
def rp_time( *args ): return rp_command ( 'time ' +  ' '.join( args ) )
def rp_title( *args ): return rp_command ( 'title ' +  ' '.join( args ) )
def rp_tmpwm( *args ): return rp_command ( 'tmpwm ' +  ' '.join( args ) )
def rp_unalias( *args ): return rp_command ( 'unalias ' +  ' '.join( args ) )
def rp_unmanage( *args ): return rp_command ( 'unmanage ' +  ' '.join( args ) )
def rp_unsetenv( *args ): return rp_command ( 'unsetenv ' +  ' '.join( args ) )
def rp_verbexec( *args ): return rp_command ( 'verbexec ' +  ' '.join( args ) )
def rp_version( *args ): return rp_command ( 'version ' +  ' '.join( args ) )
def rp_vsplit( *args ): return rp_command ( 'vsplit ' +  ' '.join( args ) )
def rp_warp( *args ): return rp_command ( 'warp ' +  ' '.join( args ) )
def rp_windows( *args ): return rp_command ( 'windows ' +  ' '.join( args ) )
def rp_cnext( *args ): return rp_command ( 'cnext ' +  ' '.join( args ) )
def rp_cother( *args ): return rp_command ( 'cother ' +  ' '.join( args ) )
def rp_cprev( *args ): return rp_command ( 'cprev ' +  ' '.join( args ) )
def rp_dedicate( *args ): return rp_command ( 'dedicate ' +  ' '.join( args ) )
def rp_describekey( *args ): return rp_command ( 'describekey ' +  ' '.join( args ) )
def rp_inext( *args ): return rp_command ( 'inext ' +  ' '.join( args ) )
def rp_iother( *args ): return rp_command ( 'iother ' +  ' '.join( args ) )
def rp_iprev( *args ): return rp_command ( 'iprev ' +  ' '.join( args ) )
def rp_prompt( *args ): return rp_command ( 'prompt ' +  ' '.join( args ) )
def rp_sdump( *args ): return rp_command ( 'sdump ' +  ' '.join( args ) )
def rp_sfdump( *args ): return rp_command ( 'sfdump ' +  ' '.join( args ) )
def rp_undo( *args ): return rp_command ( 'undo ' +  ' '.join( args ) )
def rp_redo( *args ): return rp_command ( 'redo ' +  ' '.join( args ) )
def rp_putsel( *args ): return rp_command ( 'putsel ' +  ' '.join( args ) )
def rp_getsel( *args ): return rp_command ( 'getsel ' +  ' '.join( args ) )
def rp_commands( *args ): return rp_command ( 'commands ' +  ' '.join( args ) )
```

#### .Xresources

```
! +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
! title      Nord XResources                                    +
! project    nord-xresources                                    +
! version    0.1.0                                              +
! repository https://github.com/arcticicestudio/nord-xresources +
! author     Arctic Ice Studio                                  +
! email      development@arcticicestudio.com                    +
! copyright  Copyright (C) 2016                                 +
! +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#define nord0 #2E3440
#define nord1 #3B4252
#define nord2 #434C5E
#define nord3 #4C566A
#define nord4 #D8DEE9
#define nord5 #E5E9F0
#define nord6 #ECEFF4
#define nord7 #8FBCBB
#define nord8 #88C0D0
#define nord9 #81A1C1
#define nord10 #5E81AC
#define nord11 #BF616A
#define nord12 #D08770
#define nord13 #EBCB8B
#define nord14 #A3BE8C
#define nord15 #B48EAD

*.foreground:   nord4
*.background:   nord0
*.cursorColor:  nord4
*fading: 0
*fadeColor: nord3

*.color0: nord1
*.color1: nord11
*.color2: nord14
*.color3: nord13
*.color4: nord9
*.color5: nord15
*.color6: nord8
*.color7: nord5
*.color8: nord3
*.color9: nord11
*.color10: nord14
*.color11: nord13
*.color12: nord9
*.color13: nord15
*.color14: nord7
*.color15: nord6
```
#### Setting Up `rpws` for Desktop Switching

To configure desktop switching with `rpws`, you will need to add the following line to your `~/.ratpoisonrc` file:

```sh
exec rpws init N -k
```

Where `N` is the number of desktops you wish to create (at least 2). The `-k` flag is optional and is only necessary if you want to use predefined keybindings for switching desktops and managing windows.

When `rpws` is initialized, it will create `N` desktops, and by default, it assigns the following keybindings:

- `Alt+F(N)` - Switch to desktop `N` (e.g., `Alt+F1` switches to the first desktop).
- `Ctrl+Alt+Right` - Go to the next desktop.
- `Ctrl+Alt+Left` - Go to the previous desktop.
- `Ctrl+Alt+Windows+F(N)` - Move the current window to desktop `N`.
- `Ctrl+Alt+>` - Move the window to the next desktop.
- `Ctrl+Alt+<` - Move the window to the previous desktop.

However, you may find these keybindings inconvenient or difficult to use. In that case, you can customize them to suit your preferences.

#### Customizing `rpws` Hotkeys

To customize the keybindings, add the following lines to your `~/.ratpoisonrc` file:

```sh
# Initialize 6 desktops
exec rpws init 6

# Switch desktops with the Windows+digit combination
definekey top s-1 exec rpws 1
definekey top s-2 exec rpws 2
definekey top s-3 exec rpws 3
definekey top s-4 exec rpws 4
definekey top s-5 exec rpws 5
definekey top s-6 exec rpws 6

# Move windows to desktops using Windows+F(N)
definekey top s-F1 exec rpws move1
definekey top s-F2 exec rpws move2
definekey top s-F3 exec rpws move3
definekey top s-F4 exec rpws move4
definekey top s-F5 exec rpws move5
definekey top s-F6 exec rpws move6

# Move between desktops with Windows+Right/Left
definekey top s-Right exec rpws next
definekey top s-Left exec rpws prev

# Move window to next/previous desktop using Windows+Up/Down
definekey top s-Up exec rpws movenext
definekey top s-Down exec rpws moveprev
```

##### Keybinding Legend:
- `C` stands for **Ctrl**
- `S` stands for the **Windows** key
- `M` stands for **Alt**

For example, `C-S-M-q` represents pressing `Ctrl + Windows + Alt + q` in sequence.

#### /usr/bin/rpws
```
#!/usr/bin/perl

#
# Copyright (c) 2009 Hatem Nassrat <hnassrat@gmail.com>
# All rights reserved. Modifications under same license as original script.
# ChangeLog:
#
#   Added C-M-Right and C-M-Left for next and prev workspace
#   Added move window to next prev workspace
#   Added dump/restore workspaces
#
# Copyright (c) 2005 Mike O'Connor
# All rights reserved.
# Author Mike O'Connor <stew@vireo.org>
#
# Modified by Shawn Betts.
#
# Code was adapted from rpws that comes from ratpoison containing the
# following copyright:
# Copyright (C) 2003 Shawn Betts
# Author: Shawn Betts
#

use strict;
use warnings;
use Fcntl qw (:flock);
use Getopt::Std;

my $ratpoison = $ENV{ "RATPOISON" } || "ratpoison";
my $tmp=$ENV{ "TMP" } || "/tmp";
my $lockfile = $ENV{ "RPWS_LOCKFILE" } || "$tmp/rpws.$<.lock";

# Check if sfdump/sfrestore commands are available
my $use_multiscreen = 0;
my $test_sfdump = `$ratpoison -c "help sfdump" 2>&1`;
if ($test_sfdump !~ /unknown command/i && $test_sfdump !~ /error/i) {
    $use_multiscreen = 1;
}

sub help
{
    system("pod2usage", $0);
    print( "for more detailed documentation run \"perldoc $0\"\n" );
}

sub rp_call
{
    my $result = `$ratpoison -c "@_"`;
    chomp( $result );
    chomp( $result );
    return $result;
}

sub ws_init_ws
{

    my $num = shift;

    rp_call( "gnew wspl$num" );
    my $fd = fdump();
    rp_call( "setenv fspl$num $fd" );
}

sub fdump
{
    if ($use_multiscreen) {
        return rp_call( "sfdump" );
    } else {
        return rp_call( "fdump" );
    }
}

sub frestore
{
    my $data = shift;
    if ($use_multiscreen) {
        return rp_call( "sfrestore $data" );
    } else {
        return rp_call( "frestore $data" );
    }
}

sub ws_init
{
    my $num = shift;

    $num >= 2 || die "You must create at least 2 workspaces.";

    # Backup the frames
    my $fd = fdump();

    rp_call( "select -" );
    rp_call( "only" );

    my $i;
    for my $i (2..$num)
    {
        ws_init_ws( $i );
    }

    # Workspace 1 uses the 'default' group.
    # Start in workspace 1.
    my $fd1 = fdump();
    rp_call( "gselect default" );
    rp_call( "setenv fspl1 $fd1" );
    rp_call( "setenv wspl 1" );

    # Keep track of workspace count
    rp_call( "setenv wspc $num" );

    # restore the frames
    frestore( $fd );

    if( -e "$lockfile" )
    {
        unlink ("$lockfile" );
    }
}

sub ws_save
{
    my $ws = rp_call( "getenv wspl" );
    my $fd = fdump();
    rp_call( "setenv fspl$ws $fd" );
}

sub ws_restore
{
    my $which = shift;
    my $which_name;
    my $move;

    # Step1: determine which workspace to move to

    if ( $which =~ /^move/ )
    {
        $move = 1;
        $which = substr($which, 4);
    }

    if ( $which =~ /^(?:next|prev)$/ )
    {
        my $ws = rp_call( "getenv wspl" );
        my $wspc = rp_call( "getenv wspc" );

        if ( $which eq 'next' )
        {
            $ws++;
        }
        else
        {
            $ws--;
        }
        $which = ( ( $ws - 1 ) % $wspc ) + 1;
    }

    if ( $which == 1 )
    {
        $which_name = "default";
    }
    else
    {
        $which_name = "wspl$which";
    }

    # Step 2a: Moving Window if necessary
    if ( $move )
    {
        rp_call( "gmove $which_name" );
        rp_call( "select -" );
        rp_call( "prev" );
    }

    # Step2: Process the workspace switch
    ws_save();
    rp_call( "gselect $which_name");
    my $last = rp_call( "getenv fspl$which" );
    frestore( $last );
    rp_call( "setenv wspl $which" );

    # Step 2x: Display the moved Window
    if ( $move )
    {
        rp_call( "next" );
    }

    rp_call( "echo Workspace $which" );

}

sub ws_dump
{
    my $ws_dumpf = shift;
    my $wspc = rp_call( "getenv wspc" );

    open WSDUMP, ">$ws_dumpf" or die $!;

    ws_save();

    for my $i (1..$wspc)
    {
        print WSDUMP rp_call( "getenv fspl$i" )."\n";
    }

    close WSDUMP;

    rp_call( "echo Workspaces dumped to $ws_dumpf" );
}

sub ws_dumprestore
{
    my $ws_dumpf = shift;
    my $ws = rp_call( "getenv wspl" );
    my $wspc = rp_call( "getenv wspc" );

    # Get dumped frame info
    open WSDUMP, "$ws_dumpf" or die $!;
    my @wsdata=<WSDUMP>;
    close WSDUMP;

    my $wspc_dump = scalar @wsdata;

    if ($wspc < $wspc_dump)
    {
        # Number of workspaces to restore more than available
        die "Cannot restore all workspaces (dump_count = " . $wspc_dump . ", rp_count = " . $wspc . ")";
    }

    # Restoring all workspaces
    for my $i (1..$wspc_dump)
    {
        # calculating previous workspace number
        my $j = ( $wspc + $i - 2 ) % $wspc + 1;
        # moving to workspace $i -1
        ws_restore( $j );
        # restoring workspace $i
        rp_call( "setenv fspl$i $wsdata[$i-1]" );
    }

     # goto the originally visible workspace
     ws_restore( $ws );

    rp_call( "echo Workspaces loaded from $ws_dumpf" );
}

sub add_aliases
{
    my $n = shift;
    foreach my $i (1..$n) {
        # Switch Workspace
        rp_call ( "alias rpws$i exec $0 $i" );
        # Move Window to wrokspace
        rp_call ( "alias rpwsm$i exec $0 move$i" );
    }
    rp_call ( "alias rpwsn exec $0 next" );
    rp_call ( "alias rpwsp exec $0 prev" );
    rp_call ( "alias rpwsmn exec $0 movenext" );
    rp_call ( "alias rpwsmp exec $0 moveprev" );


}

sub add_keys
{
    my $n = shift;
    foreach my $i (1..$n) {
        # Switch Workspace
        rp_call ( "definekey top M-F$i rpws$i" );
        # Move Window to wrokspace
        rp_call ( "definekey top C-M-S-F$i rpwsm$i" );
    }
    rp_call ( "definekey top C-M-Right rpwsn" );
    rp_call ( "definekey top C-M-Left rpwsp" );
    rp_call ( "definekey top C-M-greater rpwsmn" );
    rp_call ( "definekey top C-M-less rpwsmp" );
}

my $arg = shift @ARGV || 'help';

if( $arg eq "help" ) {
    help();
} elsif( $arg eq "init" ) {
    my $num = shift @ARGV;
    my %opts;
    getopts('ka', \%opts);
    ws_init( $num );
    add_aliases( $num ) if $opts{'a'} || $opts{'k'};
    add_keys ( $num ) if $opts{'k'};
} elsif( $arg eq "dump" ) {
    my $filename = shift @ARGV;
    ws_dump($filename);
} elsif( $arg eq "restore" ) {
    my $filename = shift @ARGV;
    ws_dumprestore($filename);
} elsif ( $arg eq "current" ) {
    my $cws = rp_call( "getenv wspl" );
    print "$cws";
} else {
   open LOCK, ">>$lockfile" or die "Cannot open lockfile: $lockfile";
   flock(LOCK, LOCK_EX);
   ws_restore( $arg );
}

__END__

=head1 NAME

rpws - Implements multiple workspaces in ratpoison

=head1 SYNOPSIS

 rpws init n [-k] [-a]  - setup rpws with n workspaces.
                            -a sets up command aliases;
                            -k sets up key bindings and aliases.
 rpws dump <fname>      - dumps the current layout to <fname>
 rpws restore <fname>   - restores rpws workspaces from <fname>
 rpws current           - print the current workspace
 rpws help              - this documentation
 rpws n                 - switch to this workspace


=head1 DESCRIPTION

 B<rpws> implements multiple workspaces in ratpoison by making calls
 to fdump, freestore.  It was adapted from rpws which comes with
 ratpoison in the contrib directory.

 This version automatically detects and uses sfdump/sfrestore commands
 if available for proper multi-monitor support. If these commands are
 not available, it falls back to using fdump/frestore.

=head1 USAGE

Add the following line in ~/.ratpoisonrc

     exec /path/to/rpws init 6 -k

This creates 6 aliases rpws1, rpws2, etc. It also binds the keys M-F1,
M-F2, etc to each rpwsN alias. Moreover, rpwsn (Next) and rpwsp (Prev) are
created, and C-M-{Right,Left} are bound to rpws{n,p}. Aliases rpwsm1, rpwsm2,
etc. and rpwsm{n,p} are used to move the focused window to another workspace.

Full list of keybindings created are:

    M-F$i           Goto workspace $i
    C-M-Right       Goto Next workspace
    C-M-Left        Goto Prev workspace
    C-M-S-F$i       Move window to workspace $i
    C-M-greater     Move current window to next workspace
    C-M-less        Move current window to prev workspace

=head1 FILES

 rpws requires use of a lockfile.  It defaults to using
/tmp/rpws.<UID>.lock but this can be changed by setting the
environment variable RPWS_LOCKFILE to your desired lockfile.

=head1 AUTHOR

 Mike O'Connor <stew@vireo.org>

=head1 COPYRIGHT

 Copyright (c) 2005 Mike O'Connor
 All rights reserved.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2
 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
```

### **Step 5: Configure User-Specific X Settings (~/.xsessionrc)**

The ~/.xsessionrc file (in /home/linaro/) is executed when your X session starts via LightDM. It’s useful for setting environment variables or running commands like xrandr before Ratpoison loads. This file must be executable.  
`nano /home/linaro/.xsessionrc`

Add your configurations, for example:  
{% codeblock %}
#!/bin/sh

# Optional: Uncomment to log script execution for debugging
LOG_FILE=~/xsessionrc_debug.log
echo "$(date): .xsessionrc started" >> "$LOG_FILE"

# --- Step 1: Disable Caps Lock's default toggle behavior ---
# This command uses the X Keyboard Extension (XKB) to make the Caps Lock key
# stop toggling character case. It essentially turns it into a "neutral" key.
echo "$(date): Applying setxkbmap -option caps:none" >> "$LOG_FILE"
setxkbmap -option caps:none >> "$LOG_FILE" 2>&1

# --- Step 2: Apply custom key mappings using xmodmap ---
# This command loads your .xmodmaprc file, which should contain the
# instructions to remap the (now neutral) Caps Lock key to F13.
# It's important this runs AFTER setxkbmap has modified the Caps Lock behavior.
# You can verify your Caps Lock keycode using the 'xev' command in a terminal.
# Run 'xev', press Caps Lock, and note the keycode. It's usually 66.
if [ -f /home/linaro/.xmodmaprc ]; then
  echo "$(date): Applying xmodmap /home/linaro/.xmodmaprc" >> "$LOG_FILE"
  xmodmap /home/linaro/.xmodmaprc >> "$LOG_FILE" 2>&1
else
  echo "$(date): WARNING - /home/linaro/.xmodmaprc not found." >> "$LOG_FILE"
fi

# --- XRandR display configuration (existing from your file) ---
# Define custom mode for DP-1 (1152x864 @ 60Hz)
xrandr --newmode "1152x864_60.00" 81.75 1152 1216 1336 1520 864 867 871 897 -hsync +vsync # >> "$LOG_FILE" 2>&1

# Define custom mode for HDMI-1 (2560x1080 @ 60Hz)
xrandr --newmode "2560x1080_60.00" 230.00 2560 2720 2992 3424 1080 1083 1093 1120 -hsync +vsync # >> "$LOG_FILE" 2>&1

# Add the new modes to the respective outputs
xrandr --addmode DP-1 "1152x864_60.00" # >> "$LOG_FILE" 2>&1
xrandr --addmode HDMI-1 "2560x1080_60.00" # >> "$LOG_FILE" 2>&1

# Apply the modes and set the layout.
xrandr \
--output DP-1 --primary --mode "1152x864_60.00" --below HDMI-1 \
--output HDMI-1 --mode "2560x1080_60.00" # >> "$LOG_FILE" 2>&1

echo "$(date): .xsessionrc finished successfully" >> "$LOG_FILE"
{% endcodeblock %}

Make it executable:  
`chmod +x /home/linaro/.xsessionrc`

### **Step 6: (Optional but Recommended) Remove XFCE4**

If you no longer need XFCE4 and want to free up disk space, you can remove its packages. **Be cautious** and review the packages to be removed before confirming.  
`# Identify XFCE4 meta-packages and components`  
`sudo apt purge xfce4 xfce4-goodies libxfce4ui-utils xfce4-panel xfce4-session xfce4-settings xfconf xfdesktop4 xfwm4 thunar mousepad parole ristretto`  
`# This list might need adjustment based on your specific XFCE4 installation.`  
`# Always review the list of packages apt proposes to remove.`  
`sudo apt autoremove`  
`sudo apt clean`

### **Step 7: Verify the Setup**

Reboot your system or restart LightDM to apply changes:  
`sudo systemctl restart lightdm`

Your system should automatically log in linaro directly into a Ratpoison session.  
**Troubleshooting:**

* LightDM logs: /var/log/lightdm/lightdm.log and seat-specific logs (e.g., /var/log/lightdm/seat0-greeter.log).  
* Xorg logs: ~/.local/share/xorg/Xorg.0.log (for user sessions) or /var/log/Xorg.0.log.  
* Session errors: Check ~/.xsession-errors (in /home/linaro/) for issues from ~/.xsessionrc or session startup.

### **Alternative: Manual Start with startx (If Not Using LightDM)**

If you choose not to use LightDM or wish to start Ratpoison manually from a TTY (console login):

1. Create ~/.xmodmaprc
```
remove Lock = Caps_Lock
clear Lock
keycode 66 = F13
```
3. Ensure xinit is installed: sudo apt install xinit.
4. Create or edit ~/.xinitrc (in /home/linaro/.xinitrc):  
   `nano /home/linaro/.xinitrc`  
   Add:  

```
#!/bin/sh

if [ -f /home/linaro/.xsessionrc ]; then
  . /home/linaro/.xsessionrc
fi

exec ratpoison
```

4. Make it executable: `chmod +x /home/linaro/.xinitrc`
5. Log in to a TTY as linaro and run startx.

This approach bypasses LightDM. The primary focus of this guide is the LightDM autologin method.
