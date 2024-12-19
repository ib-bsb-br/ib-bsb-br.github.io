---
tags: software>linux
info: aberto.
date: 2024-03-02
type: post
layout: post
published: true
slug: browser-thorium
title: 'Thorium Browser Flags'
---

# enclose flags within Thorium Binary

file:///opt/chromium.org/thorium/thorium-browser

{% codeblock bash %}
# Allow users to override command-line options with a file.
if [[ -f $XDG_CONFIG_HOME/thorium-flags.conf ]]; then
   CHROME_USER_FLAGS="$(cat $XDG_CONFIG_HOME/thorium-flags.conf)"
fi

# Append flags to CHROME_USER_FLAGS
CHROME_USER_FLAGS="$CHROME_USER_FLAGS"

# Sanitize std{in,out,err} because they'll be shared with untrusted child
# processes (http://crbug.com/376567).
exec < /dev/null
exec > >(exec cat)
exec 2> >(exec cat >&2)

if [ $want_temp_profile -eq 1 ] ; then
  TEMP_PROFILE=`mktemp -d`
  echo "Using temporary profile: $TEMP_PROFILE"
  CHROME_USER_FLAGS="$CHROME_USER_FLAGS --user-data-dir=$TEMP_PROFILE"
fi

# Launch Thorium
# Note: exec -a below is a bashism.
exec -a "$0" "$HERE/thorium" --no-sandbox --disable-nacl --use-gl=angle --use-angle=gl-egl --enable-unsafe-webgpu --disable-plugins --enable-gpu-rasterization --ignore-gpu-blacklist --enable-chrome-browser-cloud-management --disable-smooth-scrolling --disable-popup-blocking --enable-fast-unload --disable-overscroll-edge-effect --disable-threaded-scrolling --disable-composited-antialiasing --flag-switches-begin --allow-insecure-downloads --allow-insecure-localhost --close-window-with-last-tab=never --hide-sidepanel-button --unsafely-treat-insecure-origin-as-secure --enable-features=VaapiVideoDecodeLinuxGL --disable-features=BlockInsecurePrivateNetworkRequests,InsecureDownloadWarnings,SideSearch --flag-switches-end "$CHROME_USER_FLAGS" "$@"
{% endcodeblock %}
