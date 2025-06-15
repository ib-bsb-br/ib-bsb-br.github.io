---
tags: [scratchpad]
info: aberto.
date: 2025-06-15
type: post
layout: post
published: true
slug: singlefile-cli-hint
title: 'singlefile cli hint'
---
some website doesn't load the data on headless + cloudflare block

The solution i found is :

tell application "Microsoft Edge"
activate
open location Link
tell application "System Events"
keystroke "y" using {control down, shift down}

end tell
 

