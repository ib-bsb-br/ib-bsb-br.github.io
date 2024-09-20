---
title: Rename files using llm.datasette.io
date: 2024-06-02 00:00:00 -03:00
categories:
- Code
tags:
- linux
- scripts
comment: https://github.com/heversonbr/scientific-paper-pdf-rename
info: aberto.
type: post
layout: post
---

Fork of https://github.com/heversonbr/scientific-paper-pdf-rename

```python
#!/usr/bin/env python3
import fitz
import os
import sys
import platform
import pkg_resources
import signal
import string
import hashlib
import shutil
import re
import logging
import llm
from src.helper import *

# Define logger / logger config
log_level = logging.INFO
logging.basicConfig(format='[%(asctime)s] - [%(levelname)s]- %(message)s', level=log_level)
logger = logging.getLogger()
set_helper_logger(log_level)

# Set your OpenAI API key
model = llm.get_model("gpt-3.5-turbo")
model.key = "<!-- INSERT OPENAI KEY -->"

def keyboardInterruptHandler(signal, frame):
    logger.info('You pressed Ctrl+C! Leaving...'.format(signal))
    sys.exit(0)

def validate_arguments(arguments):
    if len(arguments) > 2:
        logger.error('Wrong number of arguments!')
        print_usage()
        sys.exit()
    if len(sys.argv) == 1:
        logger.error("Missing arguments!")
        print_usage()
        sys.exit()
    if len(arguments) == 2:
        target = os.path.abspath(arguments[1])
        base_dir = ''
        filename = ''
        if os.path.exists(target):
            if os.path.isdir(target):
                base_dir = os.path.abspath(target)
            else:
                if target.endswith('.pdf'):
                    base_dir = os.path.dirname(target)
                    filename = os.path.basename(target)
                else:
                    logger.error('Argument is not a pdf file')
                    sys.exit()
        else:
            logger.error("Directory or file ["+ arguments[1] + "] path does not exist!")
            sys.exit()
        return base_dir, filename

def hash_file(target_file):
    blocksize = 65536
    hasher = hashlib.new('sha256')
    target_file = os.path.abspath(target_file)
    if os.path.isfile(target_file):
        with open(target_file, 'rb') as f:
            while True:
                data = f.read(blocksize)
                if not data:
                    break
                hasher.update(data)
        return hasher.hexdigest()
    else:
        logger.error(target_file + ' is not a file')
        sys.exit()

def parse_title(title, max_length=None):
    if max_length == None:
        max_length = 125
    if len(title) > max_length:
        title = title[:max_length]
    title = re.sub(r'[^a-zA-Z0-9]+', ' ', title)
    title = title.strip()
    title = re.sub(r'\s', '_', title)
    title = string.capwords(title) + '.pdf'
    return title

def get_page_text(current_page):
    python_version = platform.python_version()
    library_name = "PyMuPDF"
    library_version = pkg_resources.get_distribution(library_name).version

    acceptable_python_versions = ["3.11", "3.7", "3.8"]
    acceptable_pymupdf_versions = ["1.22", "1.18"]

    if any(python_version.startswith(ver) for ver in acceptable_python_versions) and \
       any(library_version.startswith(ver) for ver in acceptable_pymupdf_versions):
        blocks = current_page.get_text('dict')['blocks']
        logger.debug('Python version is: ' + python_version)
        logger.debug('PyMuPDF version is: ' + library_version)
    else:
        logger.warning('Python version is: ' + python_version)
        logger.warning('PyMuPDF version is: ' + library_version)
        logger.error('Your Python version or PyMuPDF is not at the required level!')
        logger.error('Please ensure that both meet the specified version requirements for this script to function properly.')
        sys.exit()

    return blocks

def get_best_title_from_llm(text_content):
    response = model.prompt(
        text_content,
        system='Given the extracted text from a PDF document, craft the most fitting title. The title should be accurate, clear, concise, and relevant to researchers, adhering, if possible, to the standard of ABNT NBR 6023 (e.g., "MARX, Karl; ENGELS, Friedrich. The communist manifesto. In: Ideals and ideologies. Routledge, 2019. p. 243-255."). However, ensure the title adheres to filename restrictions: avoid characters like `/ \ ? * : < > |` and control characters (ASCII 0-31). Prioritize alphanumeric characters, hyphens, underscores, and periods. Your response MUST contain ONLY the crafted title, NO MORE, NO LESS.')
    title = response.text().strip()
    return title

def scan_title(full_file_name, page_num=None):
    if page_num is None:
        page_num = 0
    doc = fitz.open(full_file_name)
    meta_title = doc.metadata['title'].strip()
    if len(meta_title) > 5:
        meta_title = parse_title(meta_title)
    page = doc.load_page(page_num)
    size_text_tup_list = []
    title = ''
    blocks = get_page_text(page)
    text_content = ""
    for blk in blocks:
        if blk['type'] == 0:
            for line in blk['lines']:
                if line['dir'] == (1.0, 0.0) and line['wmode'] == 0:
                    for span in line['spans']:
                        size_text_tup = (span['size'], span['text'], span['origin'])
                        size_text_tup_list.append(size_text_tup)
                        text_content += span['text'] + " "
    sorted_size_text_list = sorted(size_text_tup_list, key=lambda text_size: text_size[0], reverse=True)
    larger_font = 0
    title_max_lines = 5
    for item in sorted_size_text_list:
        t_font_size = item[0]
        t_text = item[1]
        t_text_len = len(t_text)
        if t_text_len > 2:
            if t_font_size > larger_font:
                larger_font = t_font_size
                title = t_text.strip() + ' '
                title_max_lines -= 1
            elif t_font_size == larger_font:
                title = title + t_text.strip() + ' '
                title_max_lines -= 1
            if title_max_lines < 1:
                break
    doc.close()
    parsed_found_title = parse_title(title)
    best_title = get_best_title_from_llm(text_content)
    return meta_title, parsed_found_title, best_title

def do_rename(fullpath_current_filename, fullpath_new_filename):
    if fullpath_current_filename == fullpath_new_filename:
        logger.warning('Current filename and found title are already the same. Skipping...')
        return False
    try:
        os.rename(fullpath_current_filename, fullpath_new_filename)
    except:
        logger.error("An exception occurred. File not renamed!")
        return False
    return True

def confirm_to_continue():
    valid_choices = ['c', 's', 'a']
    choice = input('Choose [c] to continue, [s] to skip, or [a] to abort : \n')
    while(choice not in valid_choices):
        choice = input('Choose [c] to continue or [a] to abort : \n')
    if choice == 'c':
        return True
    if choice == 's':
        return False
    if choice == 'a':
        logger.info("aborting...")
        sys.exit()

def select_loop_type():
    logger.info('Choose [1] : for renaming all pdf files in the directory')
    logger.info('Choose [2] : for one-by-one pdf file confirmation')
    valid_choices = ['1', '2', 'q']
    choice = input('Choose [1], [2] or q [quit] : \n')
    while(choice not in valid_choices):
        choice = input('Choose [1], [2] or q [quit] : \n')
    if choice == '1':
        return '1'
    if choice == '2':
        return '2'
    if choice == 'q':
        logger.info("aborting...")
        sys.exit()

def move_file(fullpath_src_file, destination_dir, dest_file):
    if(not os.path.isdir(destination_dir)):
        os.mkdir(os.path.join(destination_dir))
    try:
        shutil.move(fullpath_src_file, os.path.join(destination_dir, dest_file))
    except OSError as e:
        logger.exception(e.strerror)
        logger.warning('File ' + fullpath_src_file + ' was not moved to ' + destination_dir + '/auto_renamed_pdf' )

def search_candidate_title(src_dir, current_file):
    meta_title, font_based_title, best_title = scan_title(src_dir + '/' + current_file)
    if len(best_title) > 0:
        return best_title
    elif len(font_based_title) > 0:
        return font_based_title
    elif len(meta_title) > 0:
        return meta_title
    else:
        logger.info('No potential Title was found for : ' + current_file)
        return None

def rename_files_in_dir(base_dir):
    renamed_counter = 0
    total_counter = 0
    file_fingerprints = []
    full_path_base_dir = os.path.abspath(base_dir)
    if os.path.isdir(full_path_base_dir):
        list_of_files = [file for file in os.listdir(full_path_base_dir) if file.endswith('.pdf')]
        if len(list_of_files) < 1:
            logger.info('no pdf files found in the target directory')
            return renamed_counter, total_counter
        else:
            logger.info(str(len(list_of_files)) + ' files found in the target directory!')
        loop_type = select_loop_type()
        for current_file in list_of_files:
            total_counter += 1
            fingerprint = hash_file(full_path_base_dir + '/' + current_file)
            logger.info('*' * 80)
            logger.info('[Current file name] : ' + current_file)
            logger.debug('[Current file hash] : ' + fingerprint)
            logger.debug('[loop_type] : ' + loop_type)
            if loop_type == '2':
                answer = confirm_to_continue()
                if answer is False:
                    continue
            if fingerprint not in file_fingerprints:
                file_fingerprints.append(fingerprint)
                found_title = search_candidate_title(full_path_base_dir, current_file)
                if found_title is not None:
                    renamed = do_rename(full_path_base_dir + '/' + current_file, full_path_base_dir + '/' + found_title)
                    if renamed:
                        move_file(full_path_base_dir + '/' + found_title, full_path_base_dir + '/auto_renamed_pdf', found_title)
                        renamed_counter += 1
            else:
                logger.warning('Another file with the same content (hash) was found in the source directory!')
                logger.info('Skipping file: ' + current_file + ' adding prefix `duplicated_`to it')
                os.rename(full_path_base_dir + '/' + current_file, full_path_base_dir + '/duplicated_' + current_file)
    else:
        logger.error('Directory does not exist!')
    return renamed_counter, total_counter

def rename_target_file(src_dir, filename):
    fullpath_filename = src_dir + '/' + filename
    if os.path.isfile(fullpath_filename):
        if os.path.abspath(fullpath_filename).endswith('.pdf'):
            found_title = search_candidate_title(src_dir, filename)
            if found_title is not None:
                renamed = do_rename(fullpath_filename, src_dir + '/' + found_title)
                if renamed:
                    move_file(src_dir + '/' + found_title, src_dir + '/auto_renamed_pdf', found_title)
                return True
        else:
            logger.debug("File is not a pdf!")
            return False
    else:
        logger.error("File does not exist!")
        return False

def main():
    print_header()
    base_dir, filename = validate_arguments(sys.argv)
    signal.signal(signal.SIGINT, keyboardInterruptHandler)
    target_path = base_dir + '/' + filename
    logger.info('[Target Path]: ' + target_path)
    rename_counter = 0
    if os.path.isdir(target_path):
        rename_counter, total_counter = rename_files_in_dir(base_dir)
        logger.info('*' * 80)
        logger.info('Finished => Total files: ' + str(total_counter) + ' Renamed files: ' + str(rename_counter))
    else:
        renamed = rename_target_file(base_dir, filename)
        if renamed:
            rename_counter += 1
        logger.info('*' * 80)
        logger.info('Finished => Renamed files : ' + str(rename_counter))

if __name__ == "__main__":
    main()
```
