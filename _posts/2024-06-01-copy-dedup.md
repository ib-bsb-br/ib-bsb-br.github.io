---
title: '"Copy Spotter" and Deduplication'
date: 2024-06-01 00:00:00 -03:00
categories:
- Code
tags:
- linux
- scripts
comment: https://github.com/Wazzabeee/copy-spotter
info: aberto.
type: post
layout: post
---

# Duplicate-File-Remover

https://github.com/Kilemonn/Duplicate-File-Remover

A command-line tool that takes input directories and create an output directory containing only unique files from the provided input directories. The files are determined as being unique based on its content hash.

# Ordering (sort-SIMILAR-pairs.py):

```python
import base64
import email
from bs4 import BeautifulSoup
import pandas as pd

# Path to the .mhtml file
mhtml_file_path = "/<!-- INSERT PATH -->/_results.mhtml"
output_file_path = "/<!-- INSERT PATH -->/sorted_pairs.txt"

# Function to extract HTML content from .mhtml file
def extract_html_from_mhtml(file_path):
    with open(file_path, 'rb') as file:
        mhtml_content = file.read()

    # Parse the mhtml content
    msg = email.message_from_bytes(mhtml_content)

    # Find the HTML part
    for part in msg.walk():
        if part.get_content_type() == "text/html":
            html_content = part.get_payload(decode=True)
            return html_content.decode('utf-8')

    return None

# Function to parse HTML and extract table data
def parse_html_table(html_content):
    soup = BeautifulSoup(html_content, 'html5lib')
    table = soup.find('table')
    return pd.read_html(str(table))[0]

# Function to process and sort the table data
def process_and_sort_table(df):
    # Extract the document names from the first row and column
    document_names = df.iloc[0, 1:].tolist()
    df = df.iloc[1:, 1:]
    df.columns = document_names
    df.index = document_names

    # Melt the DataFrame to get pairs and their similarity scores
    melted_df = df.reset_index().melt(id_vars='index', var_name='Document Pair', value_name='Similarity Score')
    melted_df.columns = ['Document 1', 'Document 2', 'Similarity Score']

    # Drop NaN values and convert similarity scores to numeric
    melted_df = melted_df.dropna()
    melted_df['Similarity Score'] = pd.to_numeric(melted_df['Similarity Score'], errors='coerce')

    # Sort the DataFrame by similarity scores
    sorted_df = melted_df.sort_values(by='Similarity Score', ascending=False)
    return sorted_df

# Function to write the sorted pairs to a text file
def write_sorted_pairs_to_file(sorted_df, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for index, row in sorted_df.iterrows():
            file.write(f"Pair: <!__{row['Document 1']}__> - <!__{row['Document 2']}__>, Similarity Score: {row['Similarity Score']}\n")

# Main script execution
html_content = extract_html_from_mhtml(mhtml_file_path)
if html_content:
    df = parse_html_table(html_content)
    sorted_df = process_and_sort_table(df)
    write_sorted_pairs_to_file(sorted_df, output_file_path)
    print(f"Sorted pairs have been written to {output_file_path}")
else:
    print("No HTML content found in the .mhtml file.")
```

# Grouping (pdf2folders.py):

```python
import os
import shutil
import re

def clean_filename(filename):
    """Removes special characters and converts spaces to underscores."""
    return re.sub(r'[^\w\s-]', '', filename).replace(' ', '_')

def find_pdf(pdf_name, pdf_dir):
    """Searches for a PDF file in the directory that matches the given name."""
    for filename in os.listdir(pdf_dir):
        cleaned_filename = clean_filename(filename).lower()
        if cleaned_filename == clean_filename(pdf_name).lower():
            return os.path.join(pdf_dir, filename)
    return None

def create_and_move(pairs_file, pdf_dir):
    """
    Creates folders for each PDF pair and moves the PDFs into them.

    Args:
        pairs_file (str): Path to the file containing the PDF pairs.
        pdf_dir (str): Path to the directory containing the PDFs.
    """
    folder_count = 1

    with open(pairs_file, 'r') as f:
        for line in f:
            match = re.match(r"Pair: <!\s*(.*?)\s*> - <!\s*(.*?)\s*>, Similarity Score.*", line)
            if match:
                pdf1_name = match.group(1).strip()
                pdf2_name = match.group(2).strip()

                # Remove leading and trailing underscores
                pdf1_name = pdf1_name.strip('_') + ".pdf"
                pdf2_name = pdf2_name.strip('_') + ".pdf"

                # Find the actual PDF files
                pdf1_path = find_pdf(pdf1_name, pdf_dir)
                pdf2_path = find_pdf(pdf2_name, pdf_dir)

                if not pdf1_path:
                    print(f"Warning: Could not find PDF: {pdf1_name}")
                if not pdf2_path:
                    print(f"Warning: Could not find PDF: {pdf2_name}")

                if pdf1_path and pdf2_path:
                    # Create a folder name using numeric notation
                    folder_name = f"folder{folder_count:03d}"
                    folder_path = os.path.join(pdf_dir, folder_name)

                    # Create the folder if it doesn't exist
                    os.makedirs(folder_path, exist_ok=True)

                    # Move the PDFs into the folder
                    try:
                        shutil.move(pdf1_path, folder_path)
                        shutil.move(pdf2_path, folder_path)
                        print(f"Moved {pdf1_name} and {pdf2_name} to {folder_path}")
                        folder_count += 1
                    except Exception as e:
                        print(f"Error moving files: {e}")

if __name__ == "__main__":
    pairs_file = "/<!-- INSERT PATH -->/sorted_pairs.txt"  # Replace with the actual path to your pairs file
    pdf_dir = "/<!-- INSERT PATH -->/030.REFS"  # Replace with the actual path to your PDF directory
    create_and_move(pairs_file, pdf_dir)
```

# Removing one of the pair (rmSMALLpdf.py):

```python
import os

def delete_smaller_pdf(folder_path):
    """
    Deletes the smaller PDF in the given folder.

    Args:
        folder_path (str): Path to the folder containing the PDFs.
    """
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    
    if len(pdf_files) != 2:
        print(f"Skipping folder {folder_path} as it does not contain exactly two PDFs.")
        return

    pdf1_path = os.path.join(folder_path, pdf_files[0])
    pdf2_path = os.path.join(folder_path, pdf_files[1])

    pdf1_size = os.path.getsize(pdf1_path)
    pdf2_size = os.path.getsize(pdf2_path)

    if pdf1_size < pdf2_size:
        os.remove(pdf1_path)
        print(f"Deleted smaller PDF: {pdf1_path}")
    else:
        os.remove(pdf2_path)
        print(f"Deleted smaller PDF: {pdf2_path}")

def iterate_folders(base_dir):
    """
    Iterates through each folder in the base directory and deletes the smaller PDF.

    Args:
        base_dir (str): Path to the base directory containing the folders.
    """
    for root, dirs, files in os.walk(base_dir):
        for dir_name in dirs:
            folder_path = os.path.join(root, dir_name)
            delete_smaller_pdf(folder_path)

if __name__ == "__main__":
    base_dir = "/<!-- INSERT PATH -->/030.REFS"  # Replace with the actual path to your base directory
    iterate_folders(base_dir)
```
