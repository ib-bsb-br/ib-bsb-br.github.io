---
categories: []
comment: 
date: '2026-03-17'
info: 
layout: post
published: true
sha: 
slug: extractor
tags:
  - scratchpad
title: 'extract handler'
type: post
---
Use this version of `/usr/local/bin/extract`:

```bash
#!/usr/bin/env bash
# extract common archive formats

set +e

extract() {
    local SAVEIFS=$IFS
    IFS=$' \t\n'

    if [ "$#" -eq 0 ]; then
        echo "Usage: extract <archive> [archive2 ...]"
        return 1
    fi

    while [ "$#" -gt 0 ]; do
        local n="$1"
        shift

        # stdin mode: extract - zip
        if [[ "$n" == "-" ]]; then
            if [ -z "$1" ]; then
                echo "Error: must provide extension after '-'"
                IFS=$SAVEIFS
                return 1
            fi

            local ext="$1"
            shift

            local tmpfile
            tmpfile=$(mktemp "/tmp/extract.stdin.XXXXXX.${ext}") || {
                echo "Error: mktemp failed"
                IFS=$SAVEIFS
                return 1
            }

            cat > "$tmpfile"
            echo "Saved stdin to temp file: $tmpfile"
            extract "$tmpfile"
            rm -f "$tmpfile"
            continue
        fi

        if [ ! -f "$n" ]; then
            echo "'$n' - file doesn't exist"
            continue
        fi

        case "$n" in
            *.cbt|*.tar.bz2|*.tar.gz|*.tar.xz|*.tbz2|*.tgz|*.txz|*.tar)
                tar --auto-compress -xvf "$n"
                ;;

            *.lzma)
                unlzma "$n"
                ;;

            *.lz4)
                lz4 -d "$n"
                ;;

            *.appimage)
                "$n" --appimage-extract
                ;;

            *.tar.lz4)
                tar --use-compress-program=lz4 -xvf "$n"
                ;;

            *.tar.br)
                tar --use-compress-program=brotli -xvf "$n"
                ;;

            *.bz2)
                bunzip2 "$n"
                ;;

            *.cbr|*.rar)
                unrar x -ad "$n"
                ;;

            *.gz)
                gunzip "$n"
                ;;

            *.cbz|*.epub|*.zip)
                unzip "$n"
                ;;

            *.z)
                uncompress "$n"
                ;;

            *.7z|*.apk|*.arj|*.cab|*.cb7|*.chm|*.deb|*.iso|*.lzh|*.msi|*.pkg|*.rpm|*.udf|*.wim|*.xar|*.vhd)
                7z x "$n"
                ;;

            *.xz)
                unxz "$n"
                ;;

            *.exe)
                cabextract "$n"
                ;;

            *.cpio)
                cpio -id < "$n"
                ;;

            *.cba|*.ace)
                unace x "$n"
                ;;

            *.zpaq)
                zpaq x "$n"
                ;;

            *.arc)
                arc e "$n"
                ;;

            *.cso)
                ciso 0 "$n" "$n.iso" && extract "$n.iso" && rm -f "$n"
                ;;

            *.zlib)
                zlib-flate -uncompress < "$n" > "${n%.*zlib}" && rm -f "$n"
                ;;

            *.dmg)
                echo "extract: '$n' - DMG handling in this script uses macOS tools and will not work on Debian"
                ;;

            *.tar.zst)
                tar -I zstd -xvf "$n"
                ;;

            *.zst)
                zstd -d "$n"
                ;;

            *)
                echo "extract: '$n' - unknown archive method"
                ;;
        esac
    done

    IFS=$SAVEIFS
}

extract "$@"
```

Then make it executable:

```bash
sudo chmod 755 /usr/local/bin/extract
```

Then test it:

```bash
extract somefile.zip
```