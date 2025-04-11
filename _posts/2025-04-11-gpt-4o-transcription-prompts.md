---
tags: [AI>prompt]
info: aberto.
date: 2025-04-11
type: post
layout: post
published: true
slug: gpt-4o-transcription-prompts
title: 'GPT-4o Transcription Prompts'
---
## Use Case 1: Transcribing Brazilian Portuguese Speech to Brazilian Portuguese Text
---
### Prompt Example
"O áudio a seguir está em português brasileiro (pt-BR). Transcreva-o sem traduzir, mantendo a pontuação correta e a fidelidade ao texto falado. Respeite expressões regionais, gírias e contextos culturais característicos do Brasil, utilizando a grafia e pontuação adequadas ao português brasileiro."
#### Explanation
- Specifies the source language (Brazilian Portuguese) and explicitly requests a transcription in the same language.  
- Emphasizes accuracy of punctuation, spelling, and regional expressions.  
- Keeps the default response format as text.
---
## Use Case 2: Pseudo-Translation from Brazilian Portuguese to American English
---
### Important Note
GPT-4o-mini-transcribe does not officially support the translations endpoint. However, you can coax an approximate translation-like output by carefully prompting the model in the standard transcriptions endpoint. Results will vary, and for professional translations, you may prefer using dedicated endpoints or specialized tools. Nonetheless, here is an illustrative prompt:
### Prompt Example
"The following audio is spoken in Brazilian Portuguese (pt-BR). Please transcribe and translate it faithfully into American English (en-US), providing natural, fluent, and contextually clear text. Include expressions or idioms as accurately as possible, reflecting their original meaning in English."
#### Explanation
- Instructs the model to interpret, then deliver transcribed text in American English.  
- Emphasizes natural, cultural, and idiomatic fidelity.  
- Reminds the user that GPT-4o models are primarily for transcription, and translation is a secondary, unsupported usage path (i.e., not the official translations endpoint).
---
## Implementation in Your iOS Shortcut
---
### 1) Endpoint and Headers
- POST to: https://api.openai.com/v1/audio/transcriptions  
- Headers:  
  - Content-Type: multipart/form-data  
  - Authorization: Bearer YOUR_API_KEY  
### 2) Basic Form Data
- model: gpt-4o-mini-transcribe  
- file: [Audio File]  
- response_format: text or json (text is typically sufficient for straightforward text transcripts)  
- prompt: [Use the relevant prompt example from above]