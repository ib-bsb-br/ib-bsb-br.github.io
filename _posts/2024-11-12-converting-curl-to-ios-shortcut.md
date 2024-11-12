---
tags: scratchpad>gemini
info: aberto.
date: 2024-11-12
type: post
layout: post
published: true
slug: converting-curl-to-ios-shortcut
title: 'Converting cURL to iOS Shortcut'
---
## Converting cURL to iOS Shortcut

This guide provides a step-by-step approach to converting your `cURL` command into an iOS Shortcut, focusing on clarity and security.

### Step 1: Open Shortcuts and Create a New Shortcut

Launch the Shortcuts app and tap the **”+”** button to create a new shortcut.  Tap **”Add Action”**.

### Step 2: Add “Get Contents of URL”

Search for and add the **”Get Contents of URL”** action.

### Step 3: Configure URL and Method

1. **URL:**  Enter the following URL:
   ```
   https://app.khoj.dev/api/chat/history?client=web&conversation_id=b24b3a6b-0915-41a9-b540-643ed42b60ef
   ```
2. **Method:** Select **”GET”**.

### Step 4: Add Headers

Tap on **”Headers”** and add the following key-value pairs.  See the image below for a visual guide on adding headers:

![Adding Headers in Shortcuts](https://i.imgur.com/7F1t5bD.png)

| Key             | Value                                                                                                                                                                                                                         |
|——————|————————————————————————————————————————————————————————————————————————————|
| Host            | `app.khoj.dev`                                                                                                                                                                                                              |
| Sec-Fetch-Dest  | `empty`                                                                                                                                                                                                               |
| User-Agent      | `Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Mobile/15E148 Safari/604.1`                                                                              |
| Accept          | `*/*`                                                                                                                                                                                                                  |
| Referer         | `https://app.khoj.dev/chat?conversationId=b24b3a6b-0915-41a9-b540-643ed42b60ef`                                                                                                                                      |
| Sec-Fetch-Site   | `same-origin`                                                                                                                                                                                                             |
| Sec-Fetch-Mode  | `cors`                                                                                                                                                                                                                  |
| Accept-Language | `en-GB,en-US;q=0.9,en;q=0.8`                                                                                                                                                                                                |
| Priority        | `u=3, i`                                                                                                                                                                                                                 |
| Accept-Encoding | `gzip, deflate, br`                                                                                                                                                                                                         |
| Connection      | `keep-alive`                                                                                                                                                                                                             |
| Cookie          |  *(See Security Considerations below)*  Instead of directly embedding the cookie here, use a “Get Variable” action to retrieve it from a secure location (e.g., another shortcut dedicated to storing and refreshing it). |


### Step 5: Handling the Response (JSON)

1. Add a **”Get Dictionary Value”** action.
2. Connect it to the “Get Contents of URL” action.
3. In the “Key” field of “Get Dictionary Value”, enter the key you want to extract from the JSON response.  For example, if the JSON response is `{“message”: “Hello”}`, enter “message” to extract the value “Hello”.

**Example JSON Output and Parsing:**

Let’s say the API returns:

```json
{“status”: “success”, “data”: [{“id”: 1, “name”: “John”}, {“id”: 2, “name”: “Jane”}]}
```

To get the name of the first user, you would set the “Key” in “Get Dictionary Value” to “data”, then use another “Get Item from List” action to get the first item, and finally another “Get Dictionary Value” action with the key “name”.

### Step 6: Displaying the Result

Add a **”Show Result”** action and connect it to the output of the “Get Dictionary Value” action (or any other action processing the response).

### Step 7: Security Considerations

**Important:** Directly embedding the `session` cookie in your shortcut is not recommended due to security risks and session expiration.  Instead, store the cookie securely and retrieve it dynamically.  Consider using a dedicated secrets management shortcut or iCloud Keychain.  This allows you to refresh the cookie periodically without modifying the main shortcut.

### Step 8: Save and Run

Save your shortcut with a descriptive name (e.g., “Get Chat History”).  Run the shortcut to test its functionality.