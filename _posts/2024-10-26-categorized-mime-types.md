---
tags: software
info: aberto.
date: 2024-10-26
type: post
layout: post
published: true
slug: categorized-mime-types
title: 'categorized MIME types'
---
| Category             | MIME Type                                                              | File Extension(s) | Example                                     |
|----------------------|----------------------------------------------------------------------|-------------------|----------------------------------------------|
| **Text & Documents** | `text/plain`                                                          | .txt, .log       | Code, logs, configuration files              |
|                      | `text/csv`                                                           | .csv             | Spreadsheets, data exchange                 |
|                      | `application/msword`                                                 | .doc, .docx      | Microsoft Word documents                     |
|                      | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | .docx            | Modern Word documents                        |
|                      | `application/vnd.oasis.opendocument.text`                            | .odt             | OpenDocument Text                           |
|                      | `application/pdf`                                                    | .pdf             | Documents, reports                          |
|                      | `text/html`                                                          | .html, .htm      | Web pages, email content                    |
|                      | `text/markdown`                                                       | .md              | Documentation, writing                       |
|                      | `application/rtf`                                                   | .rtf             | Rich Text Format                            |
| **Spreadsheets**    | `application/vnd.ms-excel`                                            | .xls             | Microsoft Excel (older)                     |
|                      | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` | .xlsx            | Microsoft Excel (modern)                    |
| **Images**          | `image/jpeg`                                                         | .jpg, .jpeg      | Photos, web graphics                        |
|                      | `image/png`                                                          | .png             | Graphics with transparency                   |
|                      | `image/gif`                                                          | .gif             | Animated images                             |
|                      | `image/webp`                                                         | .webp            | Web images                                  |
|                      | `image/heic`                                                         | .heic            | Images from Apple devices                   |
| **Audio**           | `audio/mpeg`                                                         | .mp3             | Music, audio files                          |
|                      | `audio/wav`                                                           | .wav             | Uncompressed audio                          |
|                      | `audio/ogg`                                                          | .ogg             | Ogg Vorbis audio                            |
|                      | `audio/aac`                                                          | .aac             | Advanced Audio Coding                       |
|                      | `audio/flac`                                                         | .flac            | Lossless audio                             |
| **Video**           | `video/mp4`                                                         | .mp4             | Video files                                |
|                      | `video/webm`                                                         | .webm            | Web video                                  |
|                      | `video/x-matroska`                                                    | .mkv             | Matroska video container                    |
| **Archives**         | `application/zip`                                                    | .zip             | Compressed archives                         |
|                      | `application/x-gzip`                                                  | .gz              | Gzip compressed files                       |
|                      | `application/x-tar`                                                   | .tar             | Tar archives                               |
| **Web Content**      | `text/css`                                                            | .css             | Cascading Style Sheets                      |
|                      | `application/javascript`                                              | .js              | JavaScript code                             |
| **Application Data** | `application/json`                                                    | .json            | Data exchange                               |
|                      | `application/xml`                                                     | .xml             | Configuration, data interchange             |
|                      | `application/octet-stream`                                             | (various)        | Generic binary data                         |
| **Sensor/IoT Data**  | `application/json`                                                    | .json            | Sensor readings                             |
|                      | `application/vnd.geo+json`                                           | .geojson         | Geospatial data                            |
|                      | `message/mqtt`                                                        | N/A              | MQTT messages                              |
|                      |  Often custom types                                                   | Varies           | Dependent on specific sensor and application |