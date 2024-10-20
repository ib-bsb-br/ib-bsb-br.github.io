---
tags: scripts>AI
info: aberto.
date: 2024-10-20
type: post
layout: post
published: true
slug: ankiapp-interactively-ai-chat-python
title: 'AnkiApp interactively AI chat (python)'
---
{% codeblock python %}
import requests
import json
import os

# Authentication details (INSECURE - DO NOT USE IN PRODUCTION). Environment variables are preferred
# Extracting these to env vars should be done before moving the python code
# for interactivelly prompting into the phone

#for setting this on a-shell (ios):
#client_id=$(echo "<clientId from the hardcoded python vars extraction below gathered on script generation phase>" | base64)
#client_token=$(echo "<clientToken>" | base64) #client token does not need adjustments before putting it on base64 for security.
#client_version="<clientVersion from hardcoded vars as simple string>”

client_ids = ["12e5d390c33649d7b1e6c66b5d98bb80"]  # From your .har file
client_tokens = ["LdGInADDy99mbqWmkfh5YmfzHP9SMhmWwXs7ymfEEJc="] # From your .har file
client_versions = ["9.6.1"] # From your .har file

def anki_ai_chat(client_id, client_token, client_version):
    url = "https://api.ankiapp.com/decks/ai"
    headers = {
        "accept": "*/*",
        "accept-language": "en",
        "ankiapp-client-id": client_id,
        "ankiapp-client-token": client_token,
        "ankiapp-client-version": client_version,
        "content-type": "application/json"
    }

    session_id = None
    deck = {"layouts": [], "config": {}}

    while True:
        prompt = input("Enter your prompt (or type 'quit' to exit): ")
        if prompt.lower() == "quit":
            break

        data = {
            "prompt": prompt,
            "deck": deck,
            "pending": []  # Essential for newer API versions
        }
        if session_id:
            data["session_id"] = session_id

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            response_json = response.json()
            
            if "session_id" in response_json and not session_id: #Handles only from the very first time since a single user can and should only generate one of it. Multiple users is to be seen...
                session_id = response_json["session_id"]

            if 'data' in response_json:
                print("Response:")
                for item in response_json["data"]:
                    print(f"{item[0]}: {item[1]}")
            elif 'pending' in response_json:
                print("Response:")
                for item in response_json["pending"]:
                    print(f"{item['Front']}: {item['Back']}")
            else:
                print(f"Unexpected response structure:\n{json.dumps(response_json, indent=4)}")


        except requests.exceptions.RequestException as e:
            print(f"AnkiApp API Error: {e}")
            if response.content:  # Check for content before attempting decode
              try:
                  error_json = response.json()
                  print(f"Error details: {json.dumps(error_json, indent=4)}")
              except json.JSONDecodeError: #Handles empty or corrupted data as a raw text format (utf-8 or others...).
                print(f"Raw error response: {response.content}")
                  

        except json.JSONDecodeError as e: #If nothing worked, also try converting response's data to raw utf-8 string or even raw data, before continuing the conversation, which will probably halt in errors if done and some new error is introduced, so maybe remove it or adjust...
          print(f"Couldn't parse JSON response: {e}. Printing raw content instead...\nResponse content:{response.content}")

# Example usage (single credential). Extract multiple credentials and pass by user
anki_ai_chat(client_ids[0], client_tokens[0], client_versions[0])
{% endcodeblock %}