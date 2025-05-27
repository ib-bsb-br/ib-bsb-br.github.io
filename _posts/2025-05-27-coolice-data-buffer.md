---
tags: [aid>cloud>server>dotfile]
info: aberto.
date: 2025-05-27
type: post
layout: post
published: true
slug: coolice-data-buffer
title: 'coolice data buffer'
---
`scp /path/to/your/local/file.jpg ibbsbbry@dc2.myusadc.com:/home/ibbsbbry/domains/arcreformas.com.br/public_html/files/`

`sftp ibbsbbry@dc2.myusadc.com`
`cd /home/ibbsbbry/domains/arcreformas.com.br/public_html/files/`
`put /path/to/local/file.txt`
`ls`
`exit`

`curl -F "fileToUpload=@/path/to/your/local/file.zip" https://arcreformas.com.br/upload.php`

`cat /path/to/local/file.txt | curl -F "fileToUpload=@-;filename=file.txt" https://arcreformas.com.br/upload.php`