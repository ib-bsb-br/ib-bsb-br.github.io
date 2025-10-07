---
tags: [scratchpad]
info: aberto.
date: 2025-10-07
type: post
layout: post
published: true
slug: auto-xrandr-for-two-monitors-bash-script
title: 'auto xrandr for two monitors bash script'
---
{% codeblock bash %}
#!/usr/bin/env bash
#
# monitor-setup-refactored-fixed.sh
#
# Purpose: Robust interactive multi-monitor configuration with visual verification overlay
#          Designed for Debian 11 (ARM64), Alacritty terminal, ratpoison WM, X11 session.
#
# Key reliability fixes to prevent post-overlay "freeze":
#   - Tkinter overlay closes from GUI thread using root.after(); no threading.Timer.
#   - Hard timeout guard around overlay (coreutils `timeout`) so we always proceed.
#   - Prompts and input read/write via /dev/tty to bypass pipe buffering and focus quirks.
#   - No layout churn during testing: only target output's mode changes until final apply.
#   - Line-buffered logging to file via tee; prompts go directly to TTY for immediate display.
#
# Requirements: bash, xrandr, python3, python3-tk, coreutils (timeout), awk, grep, sed.
# Usage: Run in an X11 terminal. Answer y/n/q per prompt after each 5s overlay.
# Autostart: Optional (~/.config/autostart). Set TARGET_USER and INSTALL_AUTOSTART as needed.

set -Eeuo pipefail

LOGF=${LOGF:-/tmp/monitor-setup.log}
# Log to file; prompts will go to /dev/tty, not to this pipe
exec > >(tee -a "$LOGF") 2>&1

# ---------------- Utilities ----------------
log() { printf '[%(%F %T)T] %s\n' -1 "$*"; }
fail() { log "ERROR: $*"; exit 1; }
need() { command -v "$1" >/dev/null 2>&1 || fail "$1 not found"; }

# ---------------- Requirements ----------------
need xrandr
need python3
python3 - <<'PY' 2>/dev/null || fail "python3-tk not available. Install python3-tk."
import tkinter  # noqa
PY
need timeout

# ---------------- Config ----------------
TARGET_USER=${TARGET_USER:-linaro}
INSTALL_AUTOSTART=${INSTALL_AUTOSTART:-1}
DISPLAY=${DISPLAY:-:0}
export DISPLAY

# XAUTHORITY so we can talk to the right X server (works under sudo as well)
if [[ $(id -u) -eq 0 ]]; then
  TARGET_HOME=$(getent passwd "$TARGET_USER" | cut -d: -f6 || true)
  [[ -z "${TARGET_HOME:-}" ]] && TARGET_HOME="/home/$TARGET_USER"
  if [[ -f "$TARGET_HOME/.Xauthority" ]]; then
    export XAUTHORITY="$TARGET_HOME/.Xauthority"
  elif [[ -f "/root/.Xauthority" ]]; then
    export XAUTHORITY="/root/.Xauthority"
  fi
else
  export XAUTHORITY="${XAUTHORITY:-$HOME/.Xauthority}"
fi

# Ensure we can read prompts from a controlling terminal
if [[ ! -t 0 ]] && [[ -r /dev/tty ]]; then
  exec </dev/tty
fi

# ---------------- Wait for X ----------------
for _ in {1..15}; do xrandr >/dev/null 2>&1 && break || sleep 1; done
xrandr >/dev/null 2>&1 || fail "X server not ready on $DISPLAY"

# ---------------- Globals ----------------
SAFEMODES=(
  1920x1080 1680x1050 1600x900 1440x900 1366x768 1280x1024 1280x960
  1280x800 1280x720 1024x768 800x600
)

declare -A FINAL_MODE WIDTH HEIGHT

# ---------------- Helpers ----------------
get_outputs() { xrandr --query | awk '/ connected/{print $1}'; }

sort_outputs() {
  local -a outs; mapfile -t outs < <(get_outputs)
  ((${#outs[@]})) || return 1
  local prefs=(HDMI DP DVI eDP VGA)
  for p in "${prefs[@]}"; do for o in "${outs[@]}"; do [[ $o == ${p}* ]] && echo "$o"; done; done
  for o in "${outs[@]}"; do
    local hit=0; for p in "${prefs[@]}"; do [[ $o == ${p}* ]] && { hit=1; break; }; done
    ((hit==0)) && echo "$o"
  done
}

get_modes_for_output() {
  local out="$1"
  xrandr --query | awk -v o="$out" '
    $1==o {in=1; next}
    /^[A-Z]/ {in=0}
    in && $1 ~ /^[0-9]+x[0-9]+/ {print $1}
  ' | awk '!seen[$0]++'
}

pick_testlist() {
  # stdin: available modes; stdout: up to 3 modes
  mapfile -t avail
  ((${#avail[@]})) || return 1
  local -a picked=()
  for safe in "${SAFEMODES[@]}"; do
    for m in "${avail[@]}"; do [[ $m == "$safe" ]] && { picked+=("$m"); break; }; done
    ((${#picked[@]}>=3)) && break
  done
  if ((${#picked[@]})); then printf '%s\n' "${picked[@]}"; return 0; fi
  # else: top-3 by area
  printf '%s\n' "${avail[@]}" | awk -Fx '{print $1*$2, $0}' | sort -nr | awk '{print $2}' | head -n3
}

current_geometry() {
  local out="$1"
  xrandr --query | awk -v o="$out" '
    $1==o { if (match($0, /[0-9]+x[0-9]+\+[0-9]+\+[0-9]+/)) { print substr($0, RSTART, RLENGTH) } }
  '
}

show_rectangle() {
  local W="$1" H="$2" X="$3" Y="$4"
  log "   displaying overlay ${W}x${H}+${X}+${Y} for 5s"
  timeout 7s python3 - "$W" "$H" "$X" "$Y" <<'PY'
import sys, tkinter as t
W,H,X,Y = map(int, sys.argv[1:])
root = t.Tk()
root.overrideredirect(True)
root.geometry(f"{W}x{H}+{X}+{Y}")
frame = t.Frame(root, width=W, height=H, highlightbackground='red', highlightthickness=8)
frame.pack()
root.attributes('-topmost', True)
root.after(5000, root.quit)
root.mainloop()
try:
    root.destroy()
except Exception:
    pass
PY
  local code=$?
  if (( code != 0 )); then log "   [WARN] overlay exited non-zero ($code); continuing"; fi
}

ask_ynq() {
  # Prompt to /dev/tty; read one char from /dev/tty; returns 0=y,1=n,2=q
  local prompt="$1" ch
  while true; do
    printf "%s" "$prompt" > /dev/tty
    IFS= read -r -n1 ch < /dev/tty || ch=""
    printf "\n" > /dev/tty
    case "$ch" in
      y|Y) return 0;;
      n|N) return 1;;
      q|Q) return 2;;
      *) prompt="Please type y (accept), n (next), or q (quit): ";;
    esac
  done
}

# ---------------- Main ----------------
log "Starting interactive monitor configuration..."

mapfile -t outputs < <(get_outputs)
((${#outputs[@]})) || fail "No connected monitors detected"

mapfile -t sorted < <(sort_outputs)

for out in "${sorted[@]}"; do
  log "======== Configuring $out ========"
  mapfile -t avail < <(get_modes_for_output "$out")
  if ((${#avail[@]}==0)); then log "No modes found for $out, skipping"; continue; fi

  mapfile -t testlist < <(printf '%s\n' "${avail[@]}" | pick_testlist)
  if ((${#testlist[@]}==0)); then log "No usable candidates for $out, skipping"; continue; fi

  sel=""; sel_w=0; sel_h=0

  for mode in "${testlist[@]}"; do
    [[ -z "$mode" ]] && continue
    log "---> Trying $mode for $out"
    if ! xrandr --output "$out" --mode "$mode"; then log "    Could not apply $mode"; continue; fi
    sleep 0.2

    geom=$(current_geometry "$out" || true)
    if [[ ! $geom =~ ^([0-9]+)x([0-9]+)\+([0-9]+)\+([0-9]+)$ ]]; then
      log "    Could not parse geometry; skipping"
      continue
    fi
    W=${BASH_REMATCH[1]}; H=${BASH_REMATCH[2]}; X=${BASH_REMATCH[3]}; Y=${BASH_REMATCH[4]}

    show_rectangle "$W" "$H" "$X" "$Y"

    ask_ynq "Was the red rectangle fully enclosed on $out at $mode? [y=accept / n=next / q=quit] "; rc=$?
    case "$rc" in
      0) sel="$mode"; sel_w=$W; sel_h=$H; break ;;
      1) ;;  # try next
      2) log "User aborted"; exit 1 ;;
    esac
  done

  if [[ -z "$sel" ]]; then
    log "!! No accepted mode for $out. Falling back to ${testlist[0]}"
    mode="${testlist[0]}"
    if xrandr --output "$out" --mode "$mode"; then
      sleep 0.2
      geom=$(current_geometry "$out" || true)
      if [[ $geom =~ ^([0-9]+)x([0-9]+)\+([0-9]+)\+([0-9]+)$ ]]; then
        sel_w=${BASH_REMATCH[1]}; sel_h=${BASH_REMATCH[2]}; sel="$mode"
      else
        log "!! Could not determine geometry for fallback; skipping monitor"
        continue
      fi
    else
      log "!! Fallback apply failed; skipping monitor"
      continue
    fi
  fi

  FINAL_MODE["$out"]="$sel"
  WIDTH["$out"]=$sel_w
  HEIGHT["$out"]=$sel_h

done

# ---------------- Final apply ----------------
log "Applying selected monitor configuration..."

pos=0
primary_out="${sorted[0]}"; maxarea=0

for out in "${sorted[@]}"; do
  mode="${FINAL_MODE[$out]:-}"
  if [[ -z "$mode" ]]; then log "Skipping $out (no selected mode)"; continue; fi
  xrandr --output "$out" --mode "$mode" --pos "${pos}x0"
  area=$(( WIDTH[$out] * HEIGHT[$out] ))
  if (( area > maxarea )); then maxarea=$area; primary_out="$out"; fi
  pos=$(( pos + WIDTH[$out] ))
  sleep 0.1
done

xrandr --output "$primary_out" --primary || true
log "[SUCCESS] Configuration complete. Primary: $primary_out"

# ---------------- Autostart (optional) ----------------
if (( INSTALL_AUTOSTART )); then
  TARGET_HOME=${TARGET_HOME:-$(getent passwd "$TARGET_USER" | cut -d: -f6 || echo "/home/$TARGET_USER")}
  AUTOSTART_DIR="$TARGET_HOME/.config/autostart"
  SCRIPT_PATH="$TARGET_HOME/monitor-setup-refactored-fixed.sh"
  AUTOSTART_FILE="$AUTOSTART_DIR/monitor-setup-refactored-fixed.desktop"

  mkdir -p "$AUTOSTART_DIR"
  cp -- "$0" "$SCRIPT_PATH" || true
  chmod +x "$SCRIPT_PATH"
  if [[ $(id -u) -eq 0 ]]; then chown -R "$TARGET_USER:$TARGET_USER" "$TARGET_HOME/.config" "$SCRIPT_PATH" || true; fi

  cat > "$AUTOSTART_FILE" <<EOF
[Desktop Entry]
Type=Application
Exec=bash "$SCRIPT_PATH"
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Auto Monitor Setup
Comment=Autoconfigure monitors layout interactively at login
EOF
  chmod 644 "$AUTOSTART_FILE"
  if [[ $(id -u) -eq 0 ]]; then chown "$TARGET_USER:$TARGET_USER" "$AUTOSTART_FILE" || true; fi
  log "[INFO] Autostart installed at $AUTOSTART_FILE for user $TARGET_USER"
fi

exit 0
{% endcodeblock %}