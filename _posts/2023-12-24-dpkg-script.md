---
title: Packages list script
date: 2023-12-24 01:00:00 -02:00
categories:
- Dotfiles
tags:
- linux
- scripts
comment: 
info: fechado.
type: post
layout: post
---

```
#!/bin/bash

# Setup output file
backup_dir="$HOME/backup_software_lists"
mkdir -p "$backup_dir"
outfile="$backup_dir/complete-installed-software-list.txt"

# Clear the outfile before writing
> "$outfile"

# Python Packages
if which pip >/dev/null; then
  echo "Python Packages:" >> "$outfile"
  pip freeze >> "$outfile"
else
  echo "Python pip is not installed or not found in PATH." >> "$outfile"
fi
echo >> "$outfile"

# Node.js Global Packages
if which npm >/dev/null; then
  echo "Node.js Global Packages:" >> "$outfile"
  npm list -g --depth=0 >> "$outfile"
else
  echo "Node.js npm is not installed or not found in PATH." >> "$outfile"
fi
echo >> "$outfile"

# Snap Packages
if which snap >/dev/null; then
  echo "Snap Packages:" >> "$outfile"
  snap list >> "$outfile"
else
  echo "Snap is not installed." >> "$outfile"
fi
echo >> "$outfile"

# Applications in /opt
if [ -d "/opt" ]; then
  echo "Applications in /opt:" >> "$outfile"
  ls /opt >> "$outfile"
else
  echo "/opt directory does not exist." >> "$outfile"
fi
echo >> "$outfile"

# Local Applications in /usr/local
echo "Local Applications in /usr/local:" >> "$outfile"
ls /usr/local >> "$outfile"
echo >> "$outfile"

# User Installed Applications 
user_applications_dir="$HOME/applications"
if [ -d "$user_applications_dir" ]; then
  echo "User Applications Folder:" >> "$outfile"
  ls "$user_applications_dir" >> "$outfile"
else
  echo "User applications directory does not exist or not found: $user_applications_dir" >> "$outfile"
fi
echo >> "$outfile"

# Installed Debian Packages Details
echo "Installed Debian Packages Details:" >> "$outfile"
dpkg-query -l | awk 'BEGIN {print "| Name | Description |\n|---|---|"}
                       NR>5 {
                         desc=$5; 
                         for (i=6; i<=NF; i++) 
                             desc=desc " " $i; 
                         print "| " $2 " | " desc " |"
                       }' >> "$outfile"
echo "Installed packages list written to $outfile"
echo >> "$outfile"

# Backup of repositories
sources_list="$backup_dir/sources.list.backup"
sources_list_d="$backup_dir/sources.list.d.backup.tar.gz"
echo "Backup of repositories:" >> "$outfile"
echo "Sources list: $sources_list" >> "$outfile"
echo "Sources list.d: $sources_list_d" >> "$outfile"
cp /etc/apt/sources.list "$sources_list"
tar czvf "$sources_list_d" -C /etc/apt sources.list.d/
echo >> "$outfile"

echo "Backup of software lists has been created at: $outfile."
```
