---
tags: [scratchpad]
info: aberto.
date: 2025-05-17
type: post
layout: post
published: true
slug: czkawka-dedup-workflow
title: 'czkawka dedup workflow'
---
1.  **\!\!\! BACKUP YOUR ENTIRE TARGET DIRECTORY \!\!\!**

2.  Carefully identify your `TARGET_DIR` (and any `-r` reference directories).

3.  **Duplicate File Management (Czkawka CLI):**
      * **Dry Run:** `czkawka dup -d /your/target/dir [-r /your/reference/dir] -s HASH -D AEO --dry-run` (adjust `-m`, `-t`, `-D <method>` as needed).
      * Review output carefully.
      * **Actual Deletion:**
```
czkawka dup -d /mnt/my_data_drive/repository_to_clean -s HASH -t BLAKE3 -m 8192 -D AEO
```

4.  **Empty File Deletion (Czkawka CLI):**
      * Find: `czkawka empty-files -d /your/target/dir`
      * Review.
      * Delete: `czkawka empty-files -d /mnt/my_data_drive/repository_to_clean -D`

5.  **Empty Folder Deletion (Czkawka CLI):**
      * Find: `czkawka empty-folders -d /your/target/dir`
      * Review.
      * Delete: `czkawka empty-folders -d /mnt/my_data_drive/repository_to_clean -D`