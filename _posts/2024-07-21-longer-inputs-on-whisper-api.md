---
tags: scripts>AI
info: aberto.
date: 2024-07-21
type: post
layout: post
published: true
slug: longer-inputs-on-whisper-api
title: 'Longer inputs on WHISPER API'
---

### [Audio file limitations](https://console.groq.com/docs/speech-text#audio-file-limitations)

*   File uploads are limited to 25 MB
*   The following input file types are supported: `mp3`, `mp4`, `mpeg`, `mpga`, `m4a`, `wav`, and `webm`
*   If a file contains multiple audio tracks, for example a video with dubs, only the first track will be transcribed

  
Whisper will downsample audio to 16,000 Hz mono before transcribing. This preprocessing can be performed client-side to reduce file size and allow longer files to be uploaded to groq. The following ffmpeg command can be used to reduce file size:

```
ffmpeg \
  -i <your file> \
  -ar 16000 \
  -ac 1 \
  -map 0:a: \
  <output file name>
```

By default, the Whisper API only supports files that are less than 25 MB. If you have an audio file that is longer than that, you will need to break it up into chunks of 25 MB's or less or used a compressed audio format. To get the best performance, we suggest that you avoid breaking the audio up mid-sentence as this may cause some context to be lost.

One way to handle this is to use the PyDub open source Python package to split the audio:

``` 
from pydub import AudioSegment

song = AudioSegment.from_mp3("good_morning.mp3")

# PyDub handles time in milliseconds
ten_minutes = 10 * 60 * 1000

first_10_minutes = song[:ten_minutes]

first_10_minutes.export("good_morning_10.mp3", format="mp3")
``` 

To preserve the context of a file that was split into segments, you can prompt the model with the transcript of the preceding segment. This will make the transcript more accurate, as the model will use the relevant information from the previous audio. The model will only consider the final 224 tokens of the prompt and ignore anything earlier.
