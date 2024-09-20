---
tags: iphone, scripts>mobile
info: aberto.
date: 2024-07-20
type: post
layout: post
published: true
slug: iphone-files2zip-zip2clipboard
title: 'iPhone: files2zip & zip2clipboard'
---

iPhone:
1) Make a zip file with the desired contents;

2) Run the shortcut and select that zip file;

3) The desired contents now are in the clipboard.

***


### Script 1: `ftz.py`

This script is designed to handle and process files in a specific directory. Here's a step-by-step explanation:

1. **Logging Setup**: The script sets up logging to record events and errors in a log file located at `/private/var/mobile/Containers/Data/Application/5A3A90C0-A077-4A2C-80A6-0DF006769AC6/Documents/script.log`.

2. **Extracting Archives**: The `extract_archive` function can extract files from different types of compressed archives like `.zip`, `.tar`, `.gz`, and `.bz2`. If the archive format is not supported, it logs a warning.

3. **Processing Files**: The `process_files` function goes through all files in a given directory:
   - If it finds a `.rar` file, it moves it to a special folder called `CAT-RAR`.
   - For other files, it tries to extract them if they are in a supported archive format.

4. **Moving Files to CAT Folder**: The `move_to_cat_folder` function moves all files and folders (except `CAT` and `CAT-RAR`) into a new folder called `CAT`.

5. **Main Execution**: When you run the script, it expects a directory path as an argument. It processes the files in that directory and organizes them into the `CAT` and `CAT-RAR` folders.

### Script 2: `ftp.py`

This script is a simple command-line tool that uses the `click` library to handle command-line arguments. Here's what it does:

1. **Command-Line Interface**: The script defines a command-line interface using `click`. It expects a single argument, `file_path`.

2. **Subprocess Call**: When you run the script with a file path, it uses the `subprocess` module to call an external command `files-to-prompt` with the provided file path. It captures the output and prints it.

3. **Error Handling**: If the external command fails, it catches the error and prints an error message.

### How to Use These Scripts

1. **Running `ftz.py`**:
   - Open a terminal.
   - Run the script with a directory path: `python ftz.py /path/to/directory`.
   - The script will process the files in the directory, extract archives, move `.rar` files to `CAT-RAR`, and move everything else to `CAT`.

2. **Running `ftp.py`**:
   - Open a terminal.
   - Run the script with a file path: `python ftp.py /path/to/file`.
   - The script will call the `files-to-prompt` command with the provided file path and print the result.
  
***

/private/var/mobile/Containers/Data/Application/5A3A90C0-A077-4A2C-80A6-0DF006769AC6/Documents/backup/CAT/ftz.py
---
``` 
import os
import shutil
import zipfile
import tarfile
import gzip
import bz2
import sys
import logging
from pathlib import Path
# Set up logging
log_file_path = '/private/var/mobile/Containers/Data/Application/5A3A90C0-A077-4A2C-80A6-0DF006769AC6/Documents/script.log'
logging.basicConfig(filename=log_file_path, level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
def extract_archive(archive_path, extract_dir):
    """Extracts files from various archive formats."""
    logging.info(f'Starting extraction for: {archive_path}')
    try:
        if zipfile.is_zipfile(archive_path):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
        elif tarfile.is_tarfile(archive_path):
            with tarfile.open(archive_path, 'r') as tar_ref:
                tar_ref.extractall(extract_dir)
        elif archive_path.endswith('.gz') and not tarfile.is_tarfile(archive_path):
            with gzip.open(archive_path, 'rb') as gz_file:
                with open(archive_path[:-3], 'wb') as output_file:  # Remove .gz extension
                    shutil.copyfileobj(gz_file, output_file)
        elif archive_path.endswith('.bz2') and not tarfile.is_tarfile(archive_path):
            with bz2.open(archive_path, 'rb') as bz2_file:
                with open(archive_path[:-4], 'wb') as output_file:  # Remove .bz2 extension
                    shutil.copyfileobj(bz2_file, output_file)
        else:
            logging.warning(f'Unsupported archive format: {archive_path}')
            print(f"Unsupported archive format: {archive_path}")
    except Exception as e:
        logging.error(f'Failed to extract {archive_path}: {e}', exc_info=True)
        print(f"Failed to extract {archive_path}: {e}")
def process_files(root_path, rar_folder):
    """Recursively processes files and folders, extracting archives and moving RAR files."""
    logging.info(f'Starting to process files in: {root_path}')
    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path):
                if file_path.endswith('.rar'):
                    destination_path = os.path.join(rar_folder, filename)
                    try:
                        shutil.move(file_path, destination_path)
                        logging.info(f'Moved RAR file {file_path} to {destination_path}')
                    except Exception as e:
                        logging.error(f'Failed to move {file_path} to {destination_path}: {e}', exc_info=True)
                        print(f"Failed to move {file_path}: {e}")
                else:
                    extract_archive(file_path, dirpath)
def move_to_cat_folder(root_path):
    """Moves all files and folders to a new 'CAT' folder at the same level as the root path."""
    logging.info(f'Starting to move files to CAT folder from: {root_path}')
    root_path = Path(root_path).resolve()
    cat_folder_path = root_path / 'CAT'  # Create 'CAT' folder at the same level
    cat_folder_path.mkdir(exist_ok=True)
    
    for item in root_path.iterdir():
        if item.name in ['CAT', 'CAT-RAR']:
            continue
        destination_path = cat_folder_path / item.name
        try:
            shutil.move(str(item), destination_path)
            logging.info(f'Moved {item} to {destination_path}')
        except Exception as e:
            logging.error(f'Failed to move {item} to {destination_path}: {e}', exc_info=True)
            print(f"Failed to move {item}: {e}")
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path>")
        logging.error('Incorrect usage. Path not provided.')
        sys.exit(1)
    
    target_path = sys.argv[1]
    
    if os.path.exists(target_path):
        logging.info(f'Processing started for path: {target_path}')
        rar_folder_path = os.path.join(target_path, 'CAT-RAR')
        os.makedirs(rar_folder_path, exist_ok=True)
        
        process_files(target_path, rar_folder_path)
        move_to_cat_folder(target_path)
        print("Processing and moving completed!")
        logging.info('Processing completed successfully.')
    else:
        print(f"The path {target_path} does not exist.")
        logging.error(f'The path {target_path} does not exist.')
``` 
---
/private/var/mobile/Containers/Data/Application/5A3A90C0-A077-4A2C-80A6-0DF006769AC6/Documents/backup/CAT/ftp.py
---
``` 
import subprocess
import click
@click.command()
@click.argument('file_path')
def main(file_path):
    # Use subprocess to call the files-to-prompt command
    try:
        result = subprocess.run(['files-to-prompt', file_path], capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e.stderr}")
if __name__ == '__main__':
    main()
``` 
---
