---
tags: scratchpad>o1-mini
info: aberto.
date: 2024-11-12
type: post
layout: post
published: true
slug: curl-command-into-an-ios-shortcuts
title: '`cURL` command into an **iOS Shortcuts**'
---
### **Step 1: Open the Shortcuts App**

1. **Launch the Shortcuts App** on your iOS device. If you don't have it installed, you can download it from the [App Store](https://apps.apple.com/app/shortcuts/id915249334).

### **Step 2: Create a New Shortcut**

1. Tap the **"+"** button in the top right corner to create a new shortcut.
2. Tap **"Add Action"** to begin building your shortcut.

### **Step 3: Add the "Get Contents of URL" Action**

1. In the search bar, type **"Get Contents of URL"** and select the action from the list.
   
   ![Add Get Contents of URL Action](https://i.imgur.com/1e3GkDK.png)

### **Step 4: Configure the URL and Method**

1. **Set the URL**:
   - Tap on the **"URL"** field.
   - Enter the URL from your `cURL` command:
     ```
     https://app.khoj.dev/api/chat/history?client=web&conversation_id=b24b3a6b-0915-41a9-b540-643ed42b60ef
     ```

2. **Set the Method to GET**:
   - Tap on **"Method"**.
   - Select **"GET"** from the dropdown menu.

   ![Configure URL and Method](https://i.imgur.com/6XaJHfQ.png)

### **Step 5: Add Headers**

1. **Tap on "Headers"** within the "Get Contents of URL" action to expand the section.

2. **Add Each Header** from your `cURL` command:
   
   - **Host**:
     - **Key**: `Host`
     - **Value**: `app.khoj.dev`
   
   - **Sec-Fetch-Dest**:
     - **Key**: `Sec-Fetch-Dest`
     - **Value**: `empty`
   
   - **User-Agent**:
     - **Key**: `User-Agent`
     - **Value**: 
       ```
       Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Mobile/15E148 Safari/604.1
       ```
   
   - **Accept**:
     - **Key**: `Accept`
     - **Value**: `*/*`
   
   - **Referer**:
     - **Key**: `Referer`
     - **Value**: `https://app.khoj.dev/chat?conversationId=b24b3a6b-0915-41a9-b540-643ed42b60ef`
   
   - **Sec-Fetch-Site**:
     - **Key**: `Sec-Fetch-Site`
     - **Value**: `same-origin`
   
   - **Sec-Fetch-Mode**:
     - **Key**: `Sec-Fetch-Mode`
     - **Value**: `cors`
   
   - **Accept-Language**:
     - **Key**: `Accept-Language`
     - **Value**: `en-GB,en-US;q=0.9,en;q=0.8`
   
   - **Priority**:
     - **Key**: `Priority`
     - **Value**: `u=3, i`
   
   - **Accept-Encoding**:
     - **Key**: `Accept-Encoding`
     - **Value**: `gzip, deflate, br`
   
   - **Cookie**:
     - **Key**: `Cookie`
     - **Value**: 
       ```
       session=eyJ1c2VyIjogeyJpc3MiOiAiaHR0cHM6Ly9hY2NvdW50cy5nb29nbGUuY29tIiwgImF6cCI6ICI1NzY4NjE0NTk3ODgtMWF0cmZpZjhwM3Mxa2h0bDhwZGs2azNrOXI2MzA5cWYuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCAiYXVkIjogIjU3Njg2MTQ1OTc4OC0xYXRyZmlmOHAzczFraHRsOHBkazZrM2s5cjYzMDlxZi5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsICJzdWIiOiAiMTA4ODUzMjkzMDY4NzI4MzUyODIwIiwgImVtYWlsIjogIm1hcmlvc2VpeGFzY2FyZG9zb25ldG9AZ21haWwuY29tIiwgImVtYWlsX3ZlcmlmaWVkIjogdHJ1ZSwgIm5iZiI6IDE3MzAzMzY3NzksICJuYW1lIjogIk1hcmlvIFNlaXhhcyBTYWxlcyIsICJwaWN0dXJlIjogImh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0lLV0lpdjdYbS03SjFLSTdsN2Z3NWs0bGZHNjRlUkY1WV9zbDI4d1hTQnRBcDRScFd3PXM5Ni1jIiwgImdpdmVuX25hbWUiOiAiTWFyaW8iLCAiZmFtaWx5X25hbWUiOiAiU2VpeGFzIFNhbGVzIiwgImlhdCI6IDE3MzAzMzcwNzksICJleHAiOiAxNzMwMzQwNjc5LCAianRpIjogIjUyODlmNjk1Y2RjMGU0YzY4ZjZlZjU1NjJjZmQ2MTk3N2QzYzIxMTEifX0=.ZzMjTg.080SZpM3-PyjgbVM1tWbCULmRp4; g_state={"i_l":0}"
       ```
   
   - **Connection**:
     - **Key**: `Connection`
     - **Value**: `keep-alive`

   ![Add Headers](https://i.imgur.com/7F1t5bD.png)

> **Reference:** [Setting up cURL Command in Shortcuts](https://talk.automators.fm/t/help-setting-up-curl-command-into-shortcuts-get-contents-of-url/2595) [1](https://talk.automators.fm/t/help-setting-up-curl-command-into-shortcuts-get-contents-of-url/2595)

### **Step 6: Handle the Response**

1. **Add a "Text" Action** (optional):
   - This can help you visualize or process the response from the API.
   
2. **Connect the "Get Contents of URL" Action to the "Text" Action**:
   - Drag from the output of "Get Contents of URL" to the input of "Text".

3. **Add a "Show Result" Action**:
   - This will display the API response.
   
4. **Connect the "Text" Action to "Show Result"**.

### **Step 7: Save and Test the Shortcut**

1. **Name Your Shortcut**:
   - Tap on the **settings icon** (three dots) at the top right.
   - Enter a name, e.g., **"Fetch Chat History"**.
   
2. **Run the Shortcut**:
   - Tap the **play button** (▶️) to execute the shortcut.
   - You should see the response from the API displayed.

### **Complete Shortcut Flow**

1. **Get Contents of URL**
   - **URL**: `https://app.khoj.dev/api/chat/history?client=web&conversation_id=b24b3a6b-0915-41a9-b540-643ed42b60ef`
   - **Method**: `GET`
   - **Headers**: *(As configured above)*
   
2. **Text** *(Optional)*
   - **Input**: Result from "Get Contents of URL"
   
3. **Show Result**
   - **Input**: Text from the previous step

---

### **Additional Tips**

- **Security Considerations**:
  - Be cautious when handling sensitive information like session cookies. Ensure that your shortcuts are stored securely.
  
- **Testing Headers**:
  - If the API doesn't respond as expected, double-check all header values for accuracy.
  
- **Using JSON**:
  - For more complex responses, consider adding actions to parse JSON and handle data accordingly. You can use the **"Get Dictionary Value"** action to extract specific information from the JSON response.

- **Automation**:
  - Integrate this shortcut with other automation triggers like **Time of Day**, **Location**, or **Siri Commands** for seamless workflows.