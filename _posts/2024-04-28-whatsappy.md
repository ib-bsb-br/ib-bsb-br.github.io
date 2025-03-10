---

title: WhatsapPY data
date: 2024-04-28
tags: [scripts]
comment: https://github.com/chris18369/Whatsappdata
info: aberto.
type: post
layout: post
---

{% codeblock python%}
import pandas as pd
import re
from typing import List, Tuple, Optional, Dict, Any
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, time
import logging
from enum import Enum

class MessageType(Enum):
    TEXT = "text"
    MEDIA = "media"
    SYSTEM = "system"

@dataclass
class Message:
    date: datetime
    time: time
    sender: str
    content: str
    type: MessageType

class WhatsAppDataProcessor:
    def __init__(self, file_path: str, config: Optional[Dict[str, Any]] = None):
        """Initialize the WhatsApp chat processor with optional configuration.
        
        Args:
            file_path: Path to the WhatsApp chat export file
            config: Optional configuration dictionary with processing settings
        
        Raises:
            FileNotFoundError: If the specified file doesn't exist
        """
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"Chat file not found: {file_path}")
        
        # Default configuration
        self.config = {
            'max_line_length': 32767,  # Excel's maximum cell content length
            'preserve_emoji': True,
            'remove_system_messages': False,
            'date_format': '%d/%m/%y',
            'time_format': '%H:%M:%S',
            'output_encoding': 'utf-8',
            'normalize_whitespace': True
        }
        if config:
            self.config.update(config)
            
        self.chat_data: Optional[str] = None
        self.data_frame: Optional[pd.DataFrame] = None
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _is_system_message(self, sender: str, content: str) -> bool:
        """Detect if a message is a system message.
        
        Args:
            sender: Message sender
            content: Message content
            
        Returns:
            bool indicating if the message is a system message
        """
        system_patterns = [
            r"changed the subject to",
            r"added \d",
            r"left$",
            r"changed this group's icon",
            r"Messages and calls are end-to-end encrypted",
        ]
        return any(re.search(pattern, content) for pattern in system_patterns)

    def _normalize_message(self, message: str) -> str:
        """Normalize a message by converting newlines and handling special characters.
        
        Args:
            message: The raw message text
            
        Returns:
            Normalized message as a single line
        """
        if not self.config['normalize_whitespace']:
            return message
            
        # Preserve emojis if configured
        if self.config['preserve_emoji']:
            # Convert emojis to temporary placeholders
            emoji_pattern = r'[\U0001F000-\U0001F999]'
            emojis = re.finditer(emoji_pattern, message)
            emoji_map = {m.group(): f"__EMOJI_{i}__" for i, m in enumerate(emojis)}
            for emoji, placeholder in emoji_map.items():
                message = message.replace(emoji, placeholder)
        
        # Normalize whitespace and newlines
        message = re.sub(r'\r\n|\r|\n', ' ', message)
        message = re.sub(r'\s+', ' ', message)
        message = message.strip()
        
        # Restore emojis if they were preserved
        if self.config['preserve_emoji']:
            for emoji, placeholder in emoji_map.items():
                message = message.replace(placeholder, emoji)
        
        # Truncate if exceeds max length
        if len(message) > self.config['max_line_length']:
            message = message[:self.config['max_line_length']-3] + "..."
            
        return message

    def _detect_message_type(self, content: str) -> MessageType:
        """Detect the type of message based on its content.
        
        Args:
            content: Message content
            
        Returns:
            MessageType enum value
        """
        media_patterns = [
            r'<Media omitted>',
            r'image omitted',
            r'video omitted',
            r'audio omitted',
            r'document omitted',
            r'sticker omitted',
            r'GIF omitted'
        ]
        
        if any(re.search(pattern, content, re.IGNORECASE) for pattern in media_patterns):
            return MessageType.MEDIA
            
        return MessageType.TEXT

    def _process_message_chunk(self, chunk: List[Tuple[str, str, str, str]]) -> Optional[Message]:
        """Process a chunk of message lines into a single message entry.
        
        Args:
            chunk: List containing the message header and continuation lines
        
        Returns:
            Optional[Message] object containing the processed message data
        """
        if not chunk:
            return None
        
        date_str, time_str, sender, first_line = chunk[0]
        continuation_lines = [line[0] for line in chunk[1:]]
        
        # Combine message lines
        full_message = first_line
        if continuation_lines:
            full_message += ' ' + ' '.join(continuation_lines)
            
        # Normalize the message
        normalized_message = self._normalize_message(full_message)
        
        # Convert date and time strings to proper types
        try:
            date = datetime.strptime(date_str, self.config['date_format']).date()
            time_obj = datetime.strptime(time_str, self.config['time_format']).time()
        except ValueError as e:
            self.logger.warning(f"Date/time parsing error: {e}")
            return None
            
        # Detect message type
        msg_type = self._detect_message_type(normalized_message)
        
        # Check if it's a system message
        if self._is_system_message(sender, normalized_message):
            msg_type = MessageType.SYSTEM
            if self.config['remove_system_messages']:
                return None
                
        return Message(
            date=date,
            time=time_obj,
            sender=sender.strip(),
            content=normalized_message,
            type=msg_type
        )

    def parse_chat(self) -> None:
        """Parses the chat data into structured components.
        
        Raises:
            ValueError: If chat data isn't loaded or if no valid messages are found
            RuntimeError: If message parsing fails
        """
        if self.chat_data is None:
            raise ValueError("Chat data is not loaded. Please run read_chat() first.")

        # Enhanced regex pattern for better message header detection
        date_time_pattern = (
            r'^\[(?P<date>\d{2}/\d{2}/\d{2}), (?P<time>\d{2}:\d{2}:\d{2})\] '
            r'(?P<sender>[^:]+): (?P<content>.*?)$'
        )
        
        try:
            lines = [line.strip() for line in self.chat_data.split('\n') if line.strip()]
            messages: List[Message] = []
            current_chunk = []
            
            for line in lines:
                match = re.match(date_time_pattern, line)
                if match:
                    # Process previous chunk if it exists
                    if current_chunk:
                        processed_msg = self._process_message_chunk(current_chunk)
                        if processed_msg:
                            messages.append(processed_msg)
                        current_chunk = []
                    
                    # Start new message chunk
                    current_chunk.append(match.groups())
                elif current_chunk:
                    # Add continuation line
                    current_chunk.append([line])

            # Process the final chunk
            if current_chunk:
                processed_msg = self._process_message_chunk(current_chunk)
                if processed_msg:
                    messages.append(processed_msg)

            if not messages:
                raise ValueError("No valid messages found in the chat data")

            # Convert messages to DataFrame
            self.data_frame = pd.DataFrame([
                {
                    'Date': msg.date,
                    'Time': msg.time,
                    'Sender': msg.sender,
                    'Message': msg.content,
                    'Type': msg.type.value
                }
                for msg in messages
            ])

        except Exception as e:
            raise RuntimeError(f"Error parsing chat data: {e}")

    def save_to_file(self, output_path: str = 'result.csv') -> None:
        """Saves the parsed data to a CSV file with proper encoding and escaping.
        
        Args:
            output_path: Path where the CSV file will be saved
        
        Raises:
            ValueError: If data frame is not created
            IOError: If there are issues saving the file
        """
        if self.data_frame is None:
            raise ValueError("Data frame is not created. Please run parse_chat() first.")
            
        try:
            self.data_frame.to_csv(
                output_path,
                index=False,
                sep='\t',
                encoding=self.config['output_encoding'],
                quoting=1,  # Quote all non-numeric fields
                escapechar='\\',  # Use backslash as escape character
                date_format='%Y-%m-%d'  # ISO format for dates
            )
            self.logger.info(f"Successfully saved {len(self.data_frame)} messages to {output_path}")
        except IOError as e:
            raise IOError(f"Error saving to file: {e}")

    def read_chat(self) -> None:
        """Reads the chat data from the file with proper encoding handling.
        
        Raises:
            IOError: If there are issues reading the file
        """
        try:
            with open(self.file_path, 'r', encoding=self.config['output_encoding'], errors='ignore') as file:
                self.chat_data = file.read()
            if not self.chat_data.strip():
                raise ValueError("The chat file is empty")
            self.logger.info(f"Successfully read chat file: {self.file_path}")
        except IOError as e:
            raise IOError(f"Error reading chat file: {e}")

def main():
    try:
        # Example configuration
        config = {
            'preserve_emoji': True,
            'remove_system_messages': True,
            'normalize_whitespace': True
        }
        
        processor = WhatsAppDataProcessor('chat.txt', config)
        processor.read_chat()
        processor.parse_chat()
        processor.save_to_file()
        
    except Exception as e:
        logging.error(f"Error processing chat: {e}")

if __name__ == "__main__":
    main()
{% endcodeblock %}
