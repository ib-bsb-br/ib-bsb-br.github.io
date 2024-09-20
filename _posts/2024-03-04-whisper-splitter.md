---
title: Split `.wav` for Whisper
date: 2024-03-04 00:00:00 -03:00
categories:
- Code
tags:
- scripts
comment: 
info: aberto.
type: post
layout: post
---

```
import subprocess
import math

def get_bit_rate(input_file):
    result = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=bit_rate", "-of", "default=noprint_wrappers=1:nokey=1", input_file], capture_output=True, text=True)
    return int(result.stdout.strip())

def split_audio(input_file, file_size_mb):
    bit_rate = get_bit_rate(input_file)
    bit_rate_kbps = bit_rate / 1000
    segment_duration = (file_size_mb * 1024 * 8) / bit_rate_kbps
    segment_duration = math.ceil(segment_duration)  # Round up to avoid too small last segment

    subprocess.run(["ffmpeg", "-i", input_file, "-f", "segment", "-segment_time", str(segment_duration), "-c", "copy", "output%03d.wav"])

# Usage
input_file = "gelma.wav"
file_size_mb = 25
split_audio(input_file, file_size_mb)

```
