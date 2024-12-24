---
tags: scripts>powershell, scripts>python, tasks
info: aberto.
date: 2024-12-24
type: post
layout: post
published: true
slug: list-senders
title: "List sender's email addresses from Gmail unread messages"
---
1. **Access Gmail's Search Functionality**:
   - In the search bar at the top of your Gmail interface, enter the search operator `is:unread` to filter all unread emails. 

2. **Select All Unread Emails**:
   - After executing the search, click the checkbox at the top left corner of the email list to select all displayed unread emails.
   - If you have multiple pages of unread emails, a prompt will appear allowing you to select all conversations matching the search criteria. Click on this option to ensure all unread emails are selected.

3. **Apply a Label to Selected Emails**:
   - With all unread emails selected, click on the "Labels" icon (it resembles a tag) and choose "Create new" to assign a new label, such as "Unread_Senders." This action helps in organizing and retrieving these emails easily.

4. **Export Emails Using Google Takeout**:
   - Navigate to [Google Takeout](https://takeout.google.com/), Google's data export tool.
   - Deselect all data types, then scroll down to select "Mail."
   - Click on "All Mail data included," deselect all labels, and select only the "Unread_Senders" label you created.
   - Proceed to create the export. Once the export is ready, download the file, which will be in MBOX format.

5. **Extract Sender Email Addresses**:

### python

```python
from typing import Set, Optional, Generator
import mailbox
import email.utils
import re
from email.header import decode_header
import logging
from pathlib import Path
import chardet
from email.errors import HeaderParseError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def decode_text(text: bytes, suggested_encoding: Optional[str] = None) -> str:
    """
    Decode bytes to string, attempting multiple encodings.
    
    Args:
        text: Bytes to decode
        suggested_encoding: Optional encoding to try first
        
    Returns:
        Decoded string
    """
    encodings = [suggested_encoding] if suggested_encoding else []
    encodings.extend(['utf-8', 'iso-8859-1', 'ascii'])
    
    for encoding in encodings:
        try:
            if encoding:
                return text.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            continue
            
    # Last resort: detect encoding
    detected = chardet.detect(text)
    try:
        return text.decode(detected['encoding'] or 'ascii', errors='replace')
    except (UnicodeDecodeError, LookupError):
        return text.decode('ascii', errors='replace')

def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def extract_email_streaming(mbox_path: Path) -> Generator[str, None, None]:
    """
    Memory-efficient streaming extraction of sender emails.
    
    Args:
        mbox_path: Path to MBOX file
        
    Yields:
        Extracted email addresses
    """
    try:
        mbox = mailbox.mbox(str(mbox_path))
        for message in mbox:
            try:
                from_header = message.get('From')
                if not from_header:
                    continue
                    
                # Decode header
                decoded_parts = decode_header(from_header)
                sender_str = ''
                for part, encoding in decoded_parts:
                    if isinstance(part, bytes):
                        sender_str += decode_text(part, encoding)
                    else:
                        sender_str += str(part)
                
                # Extract email
                match = re.search(r'<([^>]+)>', sender_str)
                email = match.group(1) if match else re.search(r'[\w\.-]+@[\w\.-]+', sender_str).group(0)
                
                if email and validate_email(email):
                    yield email.lower()
                    
            except (HeaderParseError, AttributeError) as e:
                logger.warning(f"Error processing message: {e}")
                continue
                
    except Exception as e:
        logger.error(f"Error processing MBOX file: {e}")
        raise

def extract_sender_emails_batch(
    mbox_path: Path,
    batch_size: int = 1000
) -> Generator[Set[str], None, None]:
    """
    Extract sender emails in batches to manage memory usage.
    
    Args:
        mbox_path: Path to MBOX file
        batch_size: Number of messages to process per batch
        
    Yields:
        Sets of unique email addresses
    """
    current_batch: Set[str] = set()
    processed = 0
    
    for email in extract_email_streaming(mbox_path):
        current_batch.add(email)
        processed += 1
        
        if processed % batch_size == 0:
            yield current_batch
            current_batch = set()
            
    if current_batch:
        yield current_batch

# Usage example with error handling and progress tracking
def process_mbox_file(mbox_path: str, output_path: str) -> None:
    """
    Process MBOX file and save unique sender emails.
    
    Args:
        mbox_path: Path to input MBOX file
        output_path: Path to output file
    """
    mbox_path = Path(mbox_path)
    output_path = Path(output_path)
    
    if not mbox_path.exists():
        raise FileNotFoundError(f"MBOX file not found: {mbox_path}")
        
    try:
        unique_emails: Set[str] = set()
        total_processed = 0
        
        logger.info("Starting MBOX processing...")
        
        for batch in extract_sender_emails_batch(mbox_path):
            unique_emails.update(batch)
            total_processed += len(batch)
            logger.info(f"Processed {total_processed} messages...")
            
        logger.info(f"Writing {len(unique_emails)} unique emails to {output_path}")
        
        with output_path.open('w', encoding='utf-8') as f:
            for email in sorted(unique_emails):
                f.write(f"{email}\n")
                
        logger.info("Processing completed successfully")
        
    except Exception as e:
        logger.error(f"Error processing MBOX file: {e}")
        raise

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract sender emails from MBOX file")
    parser.add_argument("mbox_path", help="Path to MBOX file")
    parser.add_argument("output_path", help="Path to output file")
    args = parser.parse_args()
    
    process_mbox_file(args.mbox_path, args.output_path)
```

a. **Create the Script File:**
   - Open a text editor (e.g., Notepad, VS Code) and paste the above script.
   - Save the file with a `.py` extension, such as `extract_senders.py`.

b. **Customize the Script:**
   - Replace `'C:\path\to\your\emails.mbox'` with the actual path to your MBOX file.
   - Ensure the path uses raw string notation (`r'path'`) or double backslashes to avoid escape character issues.

c. **Execute the Script:**
   - Open **Command Prompt**:
     - Press `Win + R`, type `cmd`, and press `Enter`.
   - Navigate to the script's directory:
     ```bash
     cd C:\path\to\your\script
     ```
   - Run the script:
     ```bash
     python extract_senders.py
     ```
   - **Output:** A file named `senders.txt` containing all unique sender email addresses.

### powershell

```ps1
$mboxPath = 'C:\path\to\your\mboxfile.mbox'
$outputPath = 'C:\path\to\your\senders_powershell.txt'

try {
    # Read the MBOX file
    $mbox = Get-Content $mboxPath
    
    # Initialize an array to hold sender emails
    $senderEmails = @()
    
    foreach ($line in $mbox) {
        if ($line -like "From: *") {
            # Extract email using regex
            if ($line -match '<([\w\.-]+@[\w\.-]+)>') {
                $senderEmails += $matches[1]
            }
            elseif ($line -match '([\w\.-]+@[\w\.-]+)') {
                $senderEmails += $matches[1]
            }
        }
    }
    
    # Remove duplicates and sort
    $uniqueSenders = $senderEmails | Sort-Object -Unique
    
    # Output to file
    $uniqueSenders | Out-File -FilePath $outputPath -Encoding utf8
    
    Write-Host "Sender email addresses have been saved to $outputPath"
}
catch {
    Write-Host "An error occurred: $_"
}
```

**Steps to Run the Script:**

a. **Create the Script File:**
   - Open Notepad or another text editor and paste the above script.
   - Save the file with a `.ps1` extension, e.g., `extract_senders.ps1`.

b. **Customize the Script:**
   - Replace `'C:\path\to\your\mboxfile.mbox'` with the path to your MBOX file.
   - Ensure the output path is correctly specified.

c. **Execute the Script:**
   - Open PowerShell with administrative privileges.
   - Navigate to the script's directory:
     ```powershell
     cd C:\path\to\your\script
     ```
   - Run the script:
     ```powershell
     .\extract_senders.ps1
     ```
