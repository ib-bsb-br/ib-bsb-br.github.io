---
title: OpenAI GPT API in Google Sheets
date: 2023-12-21
tags: scripts>google-apps-script
comment: script para usar openai gpt api no google sheets
info: fechado.
type: post
layout: post
---

# =gpt(A1;B1;C1)

A1: "SYSTEM PROMPT"

B1: "CONTEXT"

C1: "USER PROMPT"

```
function gpt(system, context, input) {
  messages = [];
  messages.push({"role":"system","content": system});
  messages.push({"role":"user","content": "Context: " + context});
  messages.push({"role":"user","content": "Prompt: " + input});

  var payload = {
    model: "gpt-4-1106-preview",
    messages: messages,
    temperature: 0.3,
    max_tokens: 4000,
    top_p: 0.7    
  };

  var options = {
    method: 'post',
    contentType: 'application/json',
    headers: {
      Authorization: 'Bearer ' + "OpenAI_GPT_API_key"
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  var url = "https://api.openai.com/v1/chat/completions";
  try {
    var response = UrlFetchApp.fetch(url, options);
    var json = JSON.parse(response.getContentText());
    Logger.log(json);
    if (json.error) {
      throw new Error(json.error.message);
    }
    return json.choices[0].message.content;
  } catch (e) {
    Logger.log(e.message);
    return "Error: " + e.message;
  }
}

```
