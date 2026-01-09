---
categories: []
tags:
  - scratchpad
comment: 
info: 
date: '2026-01-09'
type: post
layout: post
published: true
sha: 
slug: treesheets-build
title: 'TreeSheets Debian 11 arm64 build'

---
{% codeblock bash %}
#!/usr/bin/env bash
#
# TreeSheets local build for Debian 11 (bullseye) on arm64/aarch64.
#
# Key constraints (from your environment):
#   - glibc stays Debian-11-compatible (2.31)
#   - Prefer hardware OpenGL ES via EGL/GLES (Mali-G610) when GLX/OpenGL is llvmpipe
#   - Debian 11 default GCC 10 libstdc++ typically lacks std::from_chars(float/double)
#     which breaks Lobster; we patch Lobster to use strto*() fallback when needed.
#
# What this script does:
#   1) Installs Debian-11-safe deps (idempotent)
#   2) Clones/updates TreeSheets
#   3) Selects a C/C++ toolchain robustly (never captures apt output into CC/CXX)
#        - Uses system gcc/g++ by default
#        - Optionally tries gcc-11/12 if already installed or installable
#        - Never fails just because gcc-11/12 are unavailable
#   4) Configures CMake + prefers EGL/GLES (wxUSE_GLCANVAS_EGL)
#   5) Patches Lobster if float-from_chars is missing
#   6) Builds the CPack 'package' target to produce a .deb
#
# Usage:
#   chmod +x ./build-treesheets-debian11-arm64.sh
#   ./build-treesheets-debian11-arm64.sh --clean
#
# Options:
#   --workdir DIR
#   --clean
#   --no-update
#   --no-deps
#   --prefer-gles | --prefer-gl
#   --jobs N
#   --install
#   --no-lobster-patch
#   --try-newer-gcc    (attempt to apt-install gcc-11/12 if available; non-fatal)
#
set -euo pipefail
IFS=$'\n\t'

log(){ printf '\n[treesheets] %s\n' "$*" >&2; }
warn(){ printf '\n[treesheets][WARN] %s\n' "$*" >&2; }
die(){ printf '\n[treesheets][ERROR] %s\n' "$*" >&2; exit 1; }

have(){ command -v "$1" >/dev/null 2>&1; }

sudo_cmd(){
  if [[ "${EUID:-$(id -u)}" -eq 0 ]]; then "$@"; else sudo "$@"; fi
}

# Defaults
REPO_URL="https://github.com/aardappel/treesheets.git"
BRANCH="master"
WORKDIR=""
CLEAN=0
NO_UPDATE=0
NO_DEPS=0
PREFER_GFX="auto"   # auto|gles|gl
ALLOW_LOBSTER_PATCH=1
JOBS="$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 4)"
DO_INSTALL=0
TRY_NEWER_GCC=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --workdir) WORKDIR="$2"; shift 2;;
    --clean) CLEAN=1; shift;;
    --no-update) NO_UPDATE=1; shift;;
    --no-deps) NO_DEPS=1; shift;;
    --prefer-gles) PREFER_GFX="gles"; shift;;
    --prefer-gl) PREFER_GFX="gl"; shift;;
    --no-lobster-patch) ALLOW_LOBSTER_PATCH=0; shift;;
    --jobs) JOBS="$2"; shift 2;;
    --install) DO_INSTALL=1; shift;;
    --try-newer-gcc) TRY_NEWER_GCC=1; shift;;
    -h|--help)
      sed -n '1,220p' "$0" | sed 's/^# \{0,1\}//'; exit 0;;
    *) die "Unknown arg: $1";;
  esac
done

if [[ -z "$WORKDIR" ]]; then
  if [[ -d /mnt/mSATA ]]; then WORKDIR=/mnt/mSATA/treesheets-local; else WORKDIR="$HOME/treesheets-local"; fi
fi

ARCH="$(uname -m)"
OS_ID="$(. /etc/os-release && echo "${ID:-unknown}")"
OS_VER="$(. /etc/os-release && echo "${VERSION_ID:-unknown}")"
GLIBC_STR="$(ldd --version 2>/dev/null | head -n1 || true)"

log "Host: $(hostname) | Arch: $ARCH | OS: $OS_ID $OS_VER"
log "glibc: ${GLIBC_STR:-unknown}"
log "Workdir: $WORKDIR"
log "Jobs: $JOBS"

SRCROOT="$WORKDIR/src"
REPODIR="$SRCROOT/treesheets"
BUILDDIR="$WORKDIR/_build"
DISTDIR="$WORKDIR/dist"

mkdir -p "$SRCROOT" "$DISTDIR"

has_bullseye_backports(){
  grep -Rqs "bullseye-backports" /etc/apt/sources.list /etc/apt/sources.list.d/*.list 2>/dev/null
}

apt_install(){
  sudo_cmd apt-get -o Acquire::Retries=3 install -y "$@"
}

apt_install_targeted(){
  local target="$1"; shift
  if has_bullseye_backports; then
    sudo_cmd apt-get -o Acquire::Retries=3 install -y -t "$target" "$@" || return 1
  else
    return 1
  fi
}

install_deps(){
  log "Installing dependencies via apt (Debian 11 compatible)"
  sudo_cmd apt-get -o Acquire::Retries=3 update

  apt_install \
    ca-certificates git curl file zip unzip \
    build-essential pkg-config ninja-build fakeroot dpkg-dev \
    cmake \
    libcurl4-openssl-dev

  apt_install libgtk-3-dev libxext-dev

  # EGL/GLES headers
  apt_install libegl-dev libgles-dev libegl1-mesa-dev mesa-common-dev

  # OpenGL dev package can help FindOpenGL on some setups (even if runtime uses GLES)
  sudo_cmd apt-get -o Acquire::Retries=3 install -y libgl1-mesa-dev || true

  # Optional debug helpers
  sudo_cmd apt-get -o Acquire::Retries=3 install -y mesa-utils mesa-utils-extra || true

  have cmake || die "cmake missing after install"
  have git  || die "git missing after install"
  have gcc  || die "gcc missing after install (build-essential should provide it)"
  have g++  || die "g++ missing after install (build-essential should provide it)"
}

clone_or_update(){
  if [[ ! -d "$REPODIR/.git" ]]; then
    log "Cloning: $REPO_URL ($BRANCH)"
    git clone --branch "$BRANCH" --depth 1 "$REPO_URL" "$REPODIR"
  else
    log "Repo exists: $REPODIR"
    if [[ "$NO_UPDATE" -eq 0 ]]; then
      log "Updating repo (fetch + reset to origin/$BRANCH)"
      (cd "$REPODIR" && git fetch --depth 1 origin "$BRANCH" && git reset --hard "origin/$BRANCH")
    else
      log "Skipping repo update (--no-update)"
    fi
  fi
}

# Does this libstdc++ provide std::from_chars for double?
compiler_has_float_from_chars(){
  local cxx="$1"
  local tmpd
  tmpd="$(mktemp -d)"
  cat >"$tmpd/t.cpp" <<'EOF'
#include <charconv>
int main(){
  double x = 0;
  auto r = std::from_chars("1.25", "1.25"+4, x);
  (void)r;
}
EOF
  "$cxx" -std=c++17 -c "$tmpd/t.cpp" -o "$tmpd/t.o" >/dev/null 2>&1
  local ok=$?
  rm -rf "$tmpd"
  return $ok
}

# Global outputs from toolchain selection
CC_PATH=""
CXX_PATH=""

try_pick_toolchain(){
  local cc="$1" cxx="$2"
  local ccpath cxxpath
  ccpath="$(command -v "$cc" 2>/dev/null || true)"
  cxxpath="$(command -v "$cxx" 2>/dev/null || true)"
  [[ -n "$ccpath" && -n "$cxxpath" ]] || return 1
  CC_PATH="$ccpath"
  CXX_PATH="$cxxpath"
  return 0
}

select_toolchain(){
  # Always set a working default first.
  try_pick_toolchain gcc g++ || die "Could not find gcc/g++ in PATH"

  local major
  major="$(g++ -dumpversion 2>/dev/null | cut -d. -f1 || echo unknown)"
  log "Default g++ major: ${major}"

  if compiler_has_float_from_chars "$CXX_PATH"; then
    log "Toolchain OK: system g++ provides float from_chars"
    return 0
  fi

  warn "Current C++ stdlib likely lacks std::from_chars(double). We'll patch Lobster unless a newer GCC is available."

  # If user didn't ask to try installing newer GCC, still prefer an already-installed newer one.
  for v in 12 11; do
    if have "g++-$v"; then
      if compiler_has_float_from_chars "g++-$v"; then
        log "Using already-installed toolchain: gcc-$v / g++-$v"
        try_pick_toolchain "gcc-$v" "g++-$v" || true
        return 0
      fi
    fi
  done

  [[ "$TRY_NEWER_GCC" -eq 1 ]] || return 0

  # Best-effort attempt to install newer GCC. Non-fatal if not available.
  for v in 11 12; do
    # Quick check: is there any candidate?
    if apt-cache policy "g++-$v" 2>/dev/null | grep -q "Candidate:"; then
      log "Attempting to install gcc-$v/g++-$v (best-effort)"

      if apt_install_targeted bullseye-backports "gcc-$v" "g++-$v"; then
        true
      else
        apt_install "gcc-$v" "g++-$v" || true
      fi

      if have "g++-$v" && compiler_has_float_from_chars "g++-$v"; then
        log "Using toolchain: gcc-$v / g++-$v"
        try_pick_toolchain "gcc-$v" "g++-$v" || true
        return 0
      fi
    fi
  done

  warn "Could not obtain a newer GCC via apt. Continuing with system gcc/g++ and Lobster patch."
  return 0
}

configure_cmake(){
  [[ -n "$CC_PATH" && -n "$CXX_PATH" ]] || die "Internal error: empty compiler paths"
  [[ -x "$CC_PATH" && -x "$CXX_PATH" ]] || die "Compiler not executable: cc='$CC_PATH' cxx='$CXX_PATH'"

  if [[ "$CLEAN" -eq 1 ]]; then
    log "Cleaning build directory: $BUILDDIR"
    rm -rf "$BUILDDIR"
  fi
  mkdir -p "$BUILDDIR"

  local gfx="$PREFER_GFX"
  if [[ "$gfx" == "auto" ]]; then
    if [[ -e /usr/include/EGL/egl.h && -e /usr/include/GLES2/gl2.h ]]; then gfx="gles"; else gfx="gl"; fi
  fi
  log "Graphics intent: $gfx"

  local extra_flags=()
  if [[ "$gfx" == "gles" ]]; then
    extra_flags+=("-DwxUSE_GLCANVAS_EGL=ON")
  fi

  log "Using CC=$CC_PATH, CXX=$CXX_PATH"
  log "Configuring CMake (Release)"
  (
    cd "$REPODIR"
    cmake -S . -B "$BUILDDIR" \
      -G Ninja \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_PREFIX=/usr \
      -DCPACK_PACKAGING_INSTALL_PREFIX=/usr \
      -DCMAKE_C_COMPILER="$CC_PATH" \
      -DCMAKE_CXX_COMPILER="$CXX_PATH" \
      -DwxBUILD_SHARED=OFF \
      -DwxBUILD_INSTALL=OFF \
      -DTREESHEETS_VERSION="$(date +%Y%m%d%H%M)" \
      "${extra_flags[@]}"
  )
}

patch_lobster_if_needed(){
  [[ "$ALLOW_LOBSTER_PATCH" -eq 1 ]] || return 0

  # If compiler supports float from_chars, no patch.
  if compiler_has_float_from_chars "$CXX_PATH"; then
    return 0
  fi

  local f="$BUILDDIR/_deps/lobster-src/dev/src/lobster/string_tools.h"
  if [[ ! -f "$f" ]]; then
    warn "Lobster header not found yet ($f). If the build fails with from_chars(double), re-run with --clean."
    return 0
  fi

  if grep -q "TREESHEETS_LOCAL_FLOAT_FROM_CHARS_FALLBACK" "$f"; then
    log "Lobster already patched for float from_chars fallback"
    return 0
  fi

  log "Patching Lobster: replace std::from_chars(float/double) with strto*() fallback"

  # Replace the single line in parse_float() that calls from_chars() with a guarded fallback.
  # This avoids relying on feature-test macros that don't reliably encode float-from_chars support.
  perl -0777 -i -pe 's/\Qauto res = from_chars(sv.data(), sv.data() + sv.size(), val);\E/
\/\/ TREESHEETS_LOCAL_FLOAT_FROM_CHARS_FALLBACK\n#if defined(__GNUC__) && (__GNUC__ >= 11)\n        auto res = from_chars(sv.data(), sv.data() + sv.size(), val);\n#else\n        \/\/ GCC\/libstdc++ < 11 often lacks std::from_chars for float\/double.\n        \/\/ Fallback: copy to NUL-terminated buffer and use strto*().\n        std::string _tmp(sv);\n        char* _end = nullptr;\n        if constexpr (std::is_same_v<T, float>) {\n            val = std::strtof(_tmp.c_str(), &_end);\n        } else if constexpr (std::is_same_v<T, double>) {\n            val = std::strtod(_tmp.c_str(), &_end);\n        } else {\n            val = (T)std::strtold(_tmp.c_str(), &_end);\n        }\n        std::from_chars_result res{sv.data(), std::errc{}};\n        if (!_end || _end == _tmp.c_str()) {\n            res.ec = std::errc::invalid_argument;\n            res.ptr = sv.data();\n        } else {\n            res.ptr = sv.data() + (size_t)(_end - _tmp.c_str());\n        }\n#endif\n/smg' "$f"

  # Ensure required headers are present (best-effort, non-fatal).
  if ! grep -q "<cstdlib>" "$f"; then
    perl -i -pe 'if($.==1){print "#include <cstdlib>\n"}' "$f" || true
  fi
}

build_and_package(){
  log "Building + packaging (cmake --build ... --target package), jobs=$JOBS"
  cmake --build "$BUILDDIR" --target package -j"$JOBS"
}

collect_artifacts(){
  log "Collecting artifacts to: $DISTDIR"
  shopt -s nullglob
  local debs=("$BUILDDIR"/treesheets_*.deb)
  [[ ${#debs[@]} -gt 0 ]] || die "No .deb artifacts found in $BUILDDIR (build likely failed)."
  rm -f "$DISTDIR"/*.deb "$DISTDIR"/SHA256SUMS 2>/dev/null || true
  for f in "${debs[@]}"; do cp -av -- "$f" "$DISTDIR/"; done
  (cd "$DISTDIR" && sha256sum ./*.deb | tee SHA256SUMS)
  ls -lh "$DISTDIR"/*.deb
}

install_artifact(){
  [[ "$DO_INSTALL" -eq 1 ]] || return 0
  shopt -s nullglob
  local newest
  newest="$(ls -t "$DISTDIR"/*.deb | head -n1)"
  log "Installing: $newest"
  sudo_cmd dpkg -i "$newest" || { warn "dpkg failed; attempting apt-get -f install"; sudo_cmd apt-get -y -f install; }
}

# Run
[[ "$NO_DEPS" -eq 1 ]] || install_deps
clone_or_update

select_toolchain
[[ -n "$CC_PATH" && -n "$CXX_PATH" ]] || die "Toolchain selection failed"

configure_cmake
patch_lobster_if_needed
build_and_package
collect_artifacts
install_artifact

log "Done."
{% endcodeblock %}