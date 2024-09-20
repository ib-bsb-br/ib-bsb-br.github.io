---
title: WhatsapPY data
date: 2024-04-28 00:00:00 -03:00
categories:
- Code
tags:
- scripts
comment: https://github.com/chris18369/Whatsappdata
info: aberto.
type: post
layout: post
---

```
import pandas as pd
import re

class WhatsAppDataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.chat_data = None
        self.data_frame = None

    def read_chat(self):
        """Reads the chat data from a file, ensuring proper handling of character encoding."""
        with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as file:
            self.chat_data = file.read()

    def parse_chat(self):
        """Parses the chat data into structured components using regular expressions."""
        if self.chat_data is None:
            raise ValueError("Chat data is not loaded. Please run read_chat() first.")

        # Adjusted regex pattern to capture date, time, sender, and message
        pattern = r'(\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}) - ([^:]+): (.*?)(?=\n\d{2}/\d{2}/\d{4} \d{2}:\d{2} - |\Z)'
        matches = re.findall(pattern, self.chat_data, flags=re.S)

        if not matches:
            raise ValueError("No messages could be parsed from the chat data. Check the format of the chat log.")

        # Creating DataFrame from the matches
        self.data_frame = pd.DataFrame(matches, columns=['Date', 'Time', 'Sender', 'Message'])

    def save_to_file(self, output_path='result.csv'):
        """Saves the parsed data to a CSV file in a readable format."""
        if self.data_frame is None:
            raise ValueError("Data frame is not created. Please run parse_chat() first.")

        self.data_frame.to_csv(output_path, index=False, sep='\t')

if __name__ == "__main__":
    processor = WhatsAppDataProcessor('chat.txt')
    processor.read_chat()
    processor.parse_chat()
    processor.save_to_file()
```
