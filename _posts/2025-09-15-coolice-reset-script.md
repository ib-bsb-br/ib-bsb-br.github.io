---
tags: [scratchpad]
info: aberto.
date: 2025-09-15
type: post
layout: post
published: true
slug: coolice-reset-script
title: 'coolice reset script'
---
```bash
#!/usr/bin/env bash
#
# Revised: stable logging and safe optional tracing.
# - Key changes vs. previous iteration:
#   * Use a stable log file in BASEDIR (not inside ephemeral WORKDIR) for all persistent logs.
#   * Open a single persistent FD (3) for programmatic logging and (optionally) BASH_XTRACEFD.
#   * Do NOT use DEBUG traps (they are fragile with process substitution); rely on BASH_XTRACEFD when available.
#   * Avoid tee pipelines for log writes; use single FD writes to avoid FD lifecycle races.
#
set -Eeuo pipefail
shopt -s inherit_errexit 2>/dev/null || true
IFS=$'\n\t'

# -----------------------
# Small helpers early (used by arg parsing/sanity checks)
# -----------------------
timestamp() { date +'%Y-%m-%d %H:%M:%S'; }

abs() {
  local p="$1"
  if command -v realpath >/dev/null 2>&1; then
    realpath -m "$p" 2>/dev/null || printf '%s\n' "$p"
  elif command -v readlink >/dev/null 2>&1; then
    readlink -f "$p" 2>/dev/null || printf '%s\n' "$p"
  else
    (cd "$(dirname "$p")" 2>/dev/null && printf '%s/%s\n' "$(pwd -P)" "$(basename "$p")") || printf '%s\n' "$p"
  fi
}

is_special() { [ -S "$1" ] || [ -p "$1" ] || [ -b "$1" ] || [ -c "$1" ]; }

# -----------------------
# Configuration defaults
# -----------------------
DEFAULT_BASEDIR="${HOME:-/home/ibbsbbry}"
BASEDIR="$DEFAULT_BASEDIR"
APPLY=0
USE_ZIP=0
DEBUG=0
TRACE=0
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
MIN_FREE_KB=102400

# -----------------------
# Tool detection (FIX for latent bug)
# -----------------------
TAR_GNU=0
if tar --version 2>/dev/null | grep -q 'GNU tar'; then
  TAR_GNU=1
fi
HAS_ZIP=0
if command -v zip >/dev/null 2>&1; then
  HAS_ZIP=1
fi

# -----------------------
# Lightweight logging helpers (they write to FD 3 when available)
# -----------------------
_log_to_fd3() {
  # write a single line to FD3 if it's open; fall back to stdout/stderr
  local ln="$1"
  if { true >&3; } 2>/dev/null; then
    printf '%s\n' "$ln" >&3 2>/dev/null || true
  else
    printf '%s\n' "$ln" 2>/dev/null || true
  fi
}

log() {
  local msg="$1"
  local line
  line=$(printf '[%s] INFO: %s' "$(timestamp)" "$msg")
  _log_to_fd3 "$line"
  printf '%s\n' "$line"
}
warn() {
  local msg="$1"
  local line
  line=$(printf '[%s] WARN: %s' "$(timestamp)" "$msg")
  _log_to_fd3 "$line"
  printf '%s\n' "$line" >&2
}
err() {
  local msg="$1"
  local line
  line=$(printf '[%s] ERROR: %s' "$(timestamp)" "$msg")
  _log_to_fd3 "$line"
  printf '%s\n' "$line" >&2
}
dbg() {
  [ "${DEBUG:-0}" -ne 0 ] || return 0
  local msg="$1"
  local line
  line=$(printf '[%s] DEBUG: %s' "$(timestamp)" "$msg")
  _log_to_fd3 "$line"
  printf '%s\n' "$line"
}
trace_log() {
  [ "${TRACE:-0}" -ne 0 ] || return 0
  local msg="$1"
  local line
  line=$(printf '[%s] TRACE: %s' "$(timestamp)" "$msg")
  _log_to_fd3 "$line"
  printf '%s\n' "$line"
}

# Capture minimal last/current command for error context
CURRENT_COMMAND=""
LAST_COMMAND=""

# -----------------------
# Argument parsing
# -----------------------
usage() {
  cat <<USAGE
Usage: trim_and_fixperms.sh [options]
Default: DRY-RUN (no destructive actions).

Options:
  -y, --apply        Execute archive + remove + permissions (destructive)
      --zip          Prefer ZIP archive (requires 'zip')
      --base DIR     Base directory (default: \$HOME)
      --debug        Enable verbose debug logging (paths & outcomes)
      --trace        Enable command tracing (command-level trace; requires bash >= 4.1)
  -h, --help         Show this help
USAGE
}

while [ $# -gt 0 ]; do
  case "$1" in
    -y|--apply) APPLY=1; shift ;;
    --zip) USE_ZIP=1; shift ;;
    --base)
      shift
      BASEDIR="${1:-$BASEDIR}"
      shift
      ;;
    --debug) DEBUG=1; shift ;;
    --trace) TRACE=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 1 ;;
  esac
done

# -----------------------
# Resolve BASEDIR and do early safety checks (we create persistent log in BASEDIR)
# -----------------------
BASEDIR="$(abs "$BASEDIR")"
case "$BASEDIR" in
  "/"|"/root"|"/home") echo "Refusing to operate on $BASEDIR" >&2; exit 1 ;;
esac
[ -d "$BASEDIR" ] || { echo "Base dir not found: $BASEDIR" >&2; exit 1; }

FREE_KB=$(df -k "$BASEDIR" 2>/dev/null | awk 'NR==2{print $4}' || echo 0)
if [ -z "$FREE_KB" ] || [ "$FREE_KB" -lt "$MIN_FREE_KB" ]; then
  echo "Low free space on filesystem containing $BASEDIR ($FREE_KB KB < $MIN_FREE_KB KB)" >&2
  exit 1
fi

# -----------------------
# Prepare stable log (outside WORKDIR) and open FD3
# -----------------------
LOG_STABLE="$BASEDIR/trim_and_fixperms_${TIMESTAMP}.log"
: >"$LOG_STABLE" 2>/dev/null || true
# Open FD3 for persistent programmatic logging; leave it open until on_exit
exec 3>>"$LOG_STABLE" 2>/dev/null || true

# If TRACE requested, enable Bash xtrace to FD3 (requires bash >= 4.1)
if [ "${TRACE:-0}" -eq 1 ]; then
  if ((BASH_VERSINFO[0] > 4 || (BASH_VERSINFO[0] == 4 && BASH_VERSINFO[1] >= 1))); then
    export BASH_XTRACEFD=3
    PS4='+[$(date "+%Y-%m-%d %H:%M:%S")] '
    set -x
    trace_log "Enabled per-command xtrace to $LOG_STABLE"
  else
    TRACE=0
    dbg "TRACE disabled: bash too old to safely redirect xtrace (requires bash >= 4.1)"
  fi
fi

log "Script started: $0 (TIMESTAMP=$TIMESTAMP) LOG=$LOG_STABLE"

# -----------------------
# Prepare WORKDIR (ephemeral)
# -----------------------
WORKDIR="$(mktemp -d "${TMPDIR:-/tmp}/trimwork.${TIMESTAMP}.XXXXXX" 2>/dev/null || true)"
if [ -z "${WORKDIR:-}" ] || [ ! -d "$WORKDIR" ] || [ ! -w "$WORKDIR" ]; then
  WORKDIR="$BASEDIR/.trimwork_${TIMESTAMP}"
  mkdir -p "$WORKDIR" 2>/dev/null || { err "Cannot create workdir: $WORKDIR"; exit 1; }
  chmod 700 "$WORKDIR" 2>/dev/null || true
fi

# local copies of path variables inside workdir if needed
DOMAINS_FILE="$WORKDIR/domains_${TIMESTAMP}.lst"
CAND_ABS="$WORKDIR/candidates_abs_${TIMESTAMP}.nul"
CAND_REL="$WORKDIR/candidates_rel_${TIMESTAMP}.nul"

: >"$DOMAINS_FILE"
: >"$CAND_ABS"
: >"$CAND_REL"

dbg "WORKDIR=$WORKDIR"

# -----------------------
# Error handler uses stable log (LOG_STABLE). Keep WORKDIR until on_exit.
# -----------------------
on_error() {
  local rc=${1:-$?}
  LAST_COMMAND=${LAST_COMMAND:-'<none>'}
  CURRENT_COMMAND=${CURRENT_COMMAND:-"$BASH_COMMAND"}
  err "Script failed (exit code ${rc})."
  err "Last command: ${LAST_COMMAND}"
  err "Current command: ${CURRENT_COMMAND}"
  err "Location: PWD=$(pwd 2>/dev/null || echo '<pwd?>') USER=${USER:-}"
  err "Preserved WORKDIR for inspection: ${WORKDIR:-<none>}"
  KEEP_WORKDIR_ON_EXIT=1
  # Ensure stable log has been copied/available; it's already in BASEDIR so no-op most times.
  cp -f "$LOG_STABLE" "$BASEDIR/trim_and_fixperms_${TIMESTAMP}.log.FAILED" 2>/dev/null || true
  err "Copied runtime log (best-effort) to $BASEDIR/trim_and_fixperms_${TIMESTAMP}.log.FAILED"
  # Close FD3 only at the end via on_exit; exit now
  exit "$rc"
}
trap 'on_error $?' ERR

on_exit() {
  local rc=${1:-$?}
  # flush/close FD3 last (best-effort)
  if [ -n "${WORKDIR:-}" ] && [ -f "$LOG_STABLE" ] && [ "$rc" -eq 0 ]; then
    cp -f "$LOG_STABLE" "$BASEDIR/trim_and_fixperms_${TIMESTAMP}.log" 2>/dev/null || true
    dbg "Final log left at $LOG_STABLE"
  fi
  if [ "${KEEP_WORKDIR_ON_EXIT:-0}" -eq 1 ]; then
    dbg "Preserving WORKDIR for inspection: ${WORKDIR:-<none>}"
  else
    if [ -n "${WORKDIR:-}" ]; then
      rm -rf -- "$WORKDIR" 2>/dev/null || true
      dbg "Removed WORKDIR: $WORKDIR"
    fi
  fi
  # close FD3
  exec 3>&- 2>/dev/null || true
}
trap 'on_exit $?' EXIT

# -----------------------
# Portable functions used below
# -----------------------
path_size() {
  local p="$1"
  [ -n "$p" ] || { printf '0\n'; return; }
  if command -v stat >/dev/null 2>&1; then
    if stat --version >/dev/null 2>&1; then
      stat -c%s -- "$p" 2>/dev/null || du -sb -- "$p" 2>/dev/null | awk '{print $1}' || echo 0
    else
      stat -f%z -- "$p" 2>/dev/null || du -sk -- "$p" 2>/dev/null | awk '{print $1*1024}' || echo 0
    fi
  else
    du -sb -- "$p" 2>/dev/null | awk '{print $1}' || du -sk -- "$p" 2>/dev/null | awk '{print $1*1024}' || echo 0
  fi
}

human() {
  local n="${1:-0}"
  if command -v numfmt >/dev/null 2>&1; then
    numfmt --to=iec --suffix=B "$n" 2>/dev/null || printf '%sB' "$n"
  else
    awk -v b="$n" 'BEGIN{function hr(x){s="B K M G";i=1;while(x>=1024&&i<4){x/=1024;i++}printf 
"%.1f%s",x,substr(s,i*2-1,1)};hr(b)}'
  fi
}

safe_move() {
  local src="$1" dst="$2"
  dbg "safe_move: '$src' -> '$dst'"
  if [ "${APPLY:-0}" -eq 1 ]; then
    if mv -- "$src" "$dst" 2>>"$LOG_STABLE"; then
      dbg "mv succeeded: $src -> $dst"
      return 0
    fi
    dbg "mv failed, attempting cp -a + rm -rf for $src"
    if cp -a -- "$src" "$dst" 2>>"$LOG_STABLE"; then
      rm -rf -- "$src" 2>>"$LOG_STABLE" || { err "rm after cp failed for $src"; return 1; }
      dbg "cp+rm succeeded for $src"
      return 0
    fi
    err "safe_move failed for $src -> $dst"
    return 1
  else
    dbg "DRY-RUN safe_move: $src -> $dst"
    return 0
  fi
}

# -----------------------
# Discover domain roots
# -----------------------
log "Discovering domain roots..."
[ -d "$BASEDIR/public_html" ] && printf '%s\n' "$BASEDIR" >>"$DOMAINS_FILE"
if [ -d "$BASEDIR/domains" ]; then
  for d in "$BASEDIR/domains"/*; do
    [ -d "$d/public_html" ] && printf '%s\n' "$d" >>"$DOMAINS_FILE"
  done
fi
for d in "$BASEDIR"/*; do
  [ -d "$d/public_html" ] && printf '%s\n' "$d" >>"$DOMAINS_FILE"
done
if [ -s "$DOMAINS_FILE" ]; then
  LC_ALL=C sort -u "$DOMAINS_FILE" -o "$DOMAINS_FILE"
fi
DOM_COUNT=$(wc -l < "$DOMAINS_FILE" 2>/dev/null || echo 0)
log "Detected $DOM_COUNT domain roots"
if [ "$DOM_COUNT" -gt 0 ]; then
  sed 's/^/  /' "$DOMAINS_FILE" >>"$LOG_STABLE" 2>/dev/null || true
fi

# -----------------------
# Candidate collection helpers
# -----------------------
SCRIPT_PATH="$(abs "$0")"
SCRIPT_IN_BASE=0
case "$SCRIPT_PATH" in "$BASEDIR"|"$BASEDIR"/*) SCRIPT_IN_BASE=1 ;; esac

append_abs() {
  local p="${1:-}"
  [ -n "$p" ] || return 0
  if [ "${SCRIPT_IN_BASE:-0}" -eq 1 ] && [ "$p" = "$SCRIPT_PATH" ]; then
    dbg "Skipping script itself: $p"
    return 0
  fi
  case "$p" in "$WORKDIR"/*) dbg "Skipping workdir path: $p"; return 0 ;; esac
  if is_special "$p"; then
    dbg "Skipping special file: $p"
    return 0
  fi
  printf '%s\0' "$p" >>"$CAND_ABS"
  dbg "Appended candidate: $p"
}

# -----------------------
# Collect candidates
# -----------------------
log "Collecting candidate files..."
if [ "$DOM_COUNT" -gt 0 ]; then
  while IFS= read -r D; do
    D="$(abs "$D")"
    dbg "Processing domain root: $D"
    mkdir -p "$D/public_html" "$D/cgi-bin" "$D/logs" "$D/stats" "$D/awstats/.data" "$D/public_ftp/incoming" 
2>>"$LOG_STABLE" || true

    # Find all items (files, links, directories) at the top level of the domain root.
    find "$D" -mindepth 1 -maxdepth 1 -print0 2>>"$LOG_STABLE" | while IFS= read -r -d '' item; do
      base_item="$(basename "$item")"
      # Exclude standard directories that are handled by later, specific loops.
      case "$base_item" in
        public_html|cgi-bin|logs|stats|awstats|public_ftp|.htpasswd)
          dbg "Skipping standard path in main loop: $item"
          continue
          ;;
      esac

      # If the item is a file or symlink at the domain root, add it as a candidate.
      if [ -f "$item" ] || [ -L "$item" ]; then
        append_abs "$item"
      # If the item is a directory not in our exclusion list (e.g., 'data'),
      # recursively find and add all files within it.
      elif [ -d "$item" ]; then
        dbg "Scanning non-standard directory for files: $item"
        find "$item" -type f -print0 2>>"$LOG_STABLE" | while IFS= read -r -d '' f; do
          append_abs "$f"
        done
      fi
    done

    # Now, process the standard directories with their specific rules.
    PH="$D/public_html"
    if [ -d "$PH" ]; then
      find "$PH" -type f -print0 2>>"$LOG_STABLE" | while IFS= read -r -d '' f; do
        base="$(basename "$f")"
        case "$base" in index.html|index.htm|index.php) continue ;; esac
        case "$f" in "$PH/.well-known"|"${PH}/.well-known/"*) continue ;; esac
        append_abs "$f"
      done
    fi

    if [ -d "$D/logs" ]; then
      find "$D/logs" -type f -print0 2>>"$LOG_STABLE" | while IFS= read -r -d '' f; do append_abs "$f"; done
    fi
    if [ -d "$D/stats" ]; then
      find "$D/stats" -type f -print0 2>>"$LOG_STABLE" | while IFS= read -r -d '' f; do append_abs "$f"; done
    fi

    if [ -d "$D/awstats" ]; then
      find "$D/awstats" -mindepth 1 -maxdepth 1 -type f -print0 2>>"$LOG_STABLE" | while IFS= read -r -d '' f; do
        bn="$(basename "$f")"
        case "$bn" in .data|awstats.pl) continue ;; esac
        case "$bn" in awstats*.conf) continue ;; esac
        append_abs "$f"
      done
    fi

    if [ -d "$D/public_ftp" ]; then
      find "$D/public_ftp" -type f -print0 2>>"$LOG_STABLE" | while IFS= read -r -d '' f; do
        case "$f" in "$D/public_ftp/incoming"|"${D}/public_ftp/incoming/"*) continue ;; esac
        append_abs "$f"
      done
    fi
  done < "$DOMAINS_FILE"
fi

# Top-level under BASEDIR
find "$BASEDIR" -mindepth 1 -maxdepth 1 -print0 2>>"$LOG_STABLE" | while IFS= read -r -d '' top; do
  [ -e "$top" ] || continue
  case "$top" in "$BASEDIR/.ssh"|"$BASEDIR/public_html"|"$BASEDIR/domains") continue ;; esac
  skip=0
  if [ "$DOM_COUNT" -gt 0 ]; then
    while IFS= read -r D; do [ "$top" = "$D" ] && { skip=1; break; }; done < "$DOMAINS_FILE"
  fi
  [ "$skip" -eq 1 ] && continue
  if [ -f "$top" ] || [ -L "$top" ]; then append_abs "$top"
  elif [ -d "$top" ]; then
    find "$top" -type f -print0 2>>"$LOG_STABLE" | while IFS= read -r -d '' f; do append_abs "$f"; done
  fi
done

# If no candidates, exit gracefully
if [ ! -s "$CAND_ABS" ]; then
  log "No candidates found; nothing to do."
  exit 0
fi

# -----------------------
# Build relative list and compute totals
# -----------------------
: >"$CAND_REL"
while IFS= read -r -d '' abs; do
  case "$abs" in
    "$BASEDIR") rel='.' ;;
    "$BASEDIR"/*) rel="${abs#$BASEDIR/}" ;;
    *) rel="$abs" ;;
  esac
  printf '%s\0' "$rel" >>"$CAND_REL"
done <"$CAND_ABS"

CAND_COUNT=$(tr -cd '\0' <"$CAND_REL" | wc -c || echo 0)
TOTAL_BYTES=0
while IFS= read -r -d '' p; do
  if [ -e "$p" ]; then
    bytes=$(path_size "$p" 2>/dev/null || echo 0)
    case "$bytes" in ''|*[!0-9]*) bytes=0 ;; esac
    TOTAL_BYTES=$((TOTAL_BYTES + bytes))
  fi
done <"$CAND_ABS"
log "Candidates: $CAND_COUNT (~$(human "$TOTAL_BYTES"))"
log "Sample (first 20):"
i=0
while IFS= read -r -d '' p && [ $i -lt 20 ]; do
  printf '  %s\n' "$p" >>"$LOG_STABLE" 2>/dev/null || true
  i=$((i+1))
done <"$CAND_ABS"

# Dry-run: report and exit
if [ "$APPLY" -eq 0 ]; then
  log "DRY-RUN: no changes made. Re-run with --apply to execute."
  exit 0
fi

# Confirm destructive action
printf 'Type EXACTLY CONFIRM to proceed: '
read -r CONFIRM
[ "$CONFIRM" = "CONFIRM" ] || { err "Aborted by user"; exit 1; }

# -----------------------
# Archiving (same behavior)
# -----------------------
ARCHIVE_TGZ="$BASEDIR/min_trim_${TIMESTAMP}.tar.gz"
ARCHIVE_ZIP="$BASEDIR/min_trim_${TIMESTAMP}.zip"
log "Archiving to: $ARCHIVE_TGZ (tar) or $ARCHIVE_ZIP (zip)"

if [ "$TAR_GNU" -eq 1 ]; then
  log "Using GNU tar with --remove-files"
  set +e
  (cd "$BASEDIR" && tar --null --ignore-failed-read -czf "$ARCHIVE_TGZ" --remove-files -T "$CAND_REL") 
2>>"$LOG_STABLE"
  TAR_RC=$?
  set -e
  if [ $TAR_RC -ne 0 ]; then
    warn "tar returned $TAR_RC; some files may not have been archived/removed."
  fi
  if [ -f "$ARCHIVE_TGZ" ]; then
    tar -tzf "$ARCHIVE_TGZ" >/dev/null 2>&1 || warn "Archive verification failed: $ARCHIVE_TGZ"
  else
    err "Archive was not created: $ARCHIVE_TGZ"
  fi
else
  STAGE="$WORKDIR/stage"
  mkdir -p "$STAGE"
  log "Staging files to $STAGE"
  while IFS= read -r -d '' rel; do
    src="$BASEDIR/$rel"
    dst="$STAGE/$rel"
    mkdir -p "$(dirname "$dst")" 2>>"$LOG_STABLE" || true
    if [ -e "$src" ]; then
      if ! safe_move "$src" "$dst"; then
        err "Failed to stage $src"
      fi
    fi
  done <"$CAND_REL"

  if [ "$USE_ZIP" -eq 1 ] && [ "$HAS_ZIP" -eq 1 ]; then
    (cd "$STAGE" && zip -r -q "$ARCHIVE_ZIP" .) 2>>"$LOG_STABLE" || warn "zip failed"
    [ -f "$ARCHIVE_ZIP" ] && unzip -t "$ARCHIVE_ZIP" >/dev/null 2>&1 || warn "ZIP verification failed"
  else
    (cd "$STAGE" && tar -czf "$ARCHIVE_TGZ" .) 2>>"$LOG_STABLE" || warn "tar failed"
    [ -f "$ARCHIVE_TGZ" ] && tar -tzf "$ARCHIVE_TGZ" >/dev/null 2>&1 || warn "tar.gz verification failed"
  fi
  rm -rf -- "$STAGE"
fi

# Residual cleanup
log "Residual cleanup..."
while IFS= read -r -d '' p; do
  if [ -e "$p" ]; then
    dbg "Removing residual: $p"
    rm -rf -- "$p" 2>>"$LOG_STABLE" || warn "Failed to remove residual: $p"
  fi
done <"$CAND_ABS"

find "$BASEDIR" -depth -type d -empty -delete 2>>"$LOG_STABLE" || true

# -----------------------
# Recreate skeletons
# -----------------------
log "Recreating skeletons..."
if [ -s "$DOMAINS_FILE" ]; then
  while IFS= read -r D; do
    D="$(abs "$D")"
    dbg "Recreating for domain: $D"
    mkdir -p "$D/public_html" "$D/cgi-bin" "$D/logs" "$D/stats" "$D/awstats/.data" "$D/public_ftp/incoming" 
2>>"$LOG_STABLE" || true
    PH="$D/public_html"
    if [ ! -f "$PH/index.html" ] && [ ! -f "$PH/index.php" ]; then
      cat > "$PH/index.html" <<'HTML'
<!doctype html><html><head><meta charset="utf-8"><title>Placeholder</title></head>
<body><h1>Placeholder</h1><p>Minimal skeleton active. Upload your site to public_html.</p></body></html>
HTML
      chmod 644 "$PH/index.html" 2>>"$LOG_STABLE" || true
    fi

    if [ -d "$D/logs" ]; then
      find "$D/logs" -mindepth 1 -print0 | xargs -0 -r rm -rf -- 2>>"$LOG_STABLE" || true
    fi
    if [ -d "$D/stats" ]; then
      find "$D/stats" -mindepth 1 -print0 | xargs -0 -r rm -rf -- 2>>"$LOG_STABLE" || true
    fi
    if [ -d "$D/awstats" ]; then
      find "$D/awstats" -mindepth 1 -maxdepth 1 -print0 2>>"$LOG_STABLE" | while IFS= read -r -d '' f; do
        bn="$(basename "$f")"
        case "$bn" in .data|awstats.pl|awstats*.conf) continue ;; esac
        rm -rf -- "$f" 2>>"$LOG_STABLE" || true
      done
    fi
  done <"$DOMAINS_FILE"
fi

# -----------------------
# Apply permissions
# -----------------------
log "Applying permissions..."
find "$BASEDIR" -type d -print0 | xargs -0 -r chmod 0755 -- 2>>"$LOG_STABLE" || true
find "$BASEDIR" -type f -print0 | xargs -0 -r chmod 0644 -- 2>>"$LOG_STABLE" || true
find "$BASEDIR" -type d -name "cgi-bin" -print0 2>>"$LOG_STABLE" | while IFS= read -r -d '' d; do
  find "$d" -type f -print0 | xargs -0 -r chmod 0755 -- 2>>"$LOG_STABLE" || true
done
find "$BASEDIR" -type f -name "awstats.pl" -print0 | xargs -0 -r chmod 0755 -- 2>>"$LOG_STABLE" || true
find "$BASEDIR" -type d -path "*/public_ftp" -print0 | xargs -0 -r chmod 0711 -- 2>>"$LOG_STABLE" || true
find "$BASEDIR" -type d -path "*/public_ftp/incoming" -print0 | xargs -0 -r chmod 0733 -- 2>>"$LOG_STABLE" || 
true
if [ -d "$BASEDIR/.ssh" ]; then
  chmod 700 "$BASEDIR/.ssh" 2>>"$LOG_STABLE" || true
  find "$BASEDIR/.ssh" -type f -print0 | xargs -0 -r chmod 0600 -- 2>>"$LOG_STABLE" || true
fi
find "$BASEDIR" -type f \( -name ".htaccess" -o -name ".htpasswd" \) -print0 | xargs -0 -r chmod 0644 -- 
2>>"$LOG_STABLE" || true
find "$BASEDIR" -type f \( -iname "wp-config.php" -o -iname "config.php" -o -iname ".env" \) -print0 | xargs -0 
-r chmod 0640 -- 2>>"$LOG_STABLE" || true
find "$BASEDIR" -type f \( -iname "*token*" -o -iname "*secret*" -o -name "id_*" \) -print0 | xargs -0 -r chmod 
0600 -- 2>>"$LOG_STABLE" || true

# -----------------------
# Finalization
# -----------------------
log "Completed successfully."
exit 0
```