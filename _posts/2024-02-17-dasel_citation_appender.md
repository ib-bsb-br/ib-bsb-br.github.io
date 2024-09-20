---
title: dasel references filtering + citation appender [script]
date: 2024-02-17 01:00:00 -02:00
categories:
- Code
tags:
- scripts
comment: https://daseldocs.tomwright.me/
info: aberto.
type: post
layout: post
---

```
import os
import subprocess

COMMAND_TEMPLATE = "dasel_linux_arm64 -w - -f /root/Downloads/gelmaTCC/CAP.2/api-responses/api-response-$$$.json '.records.all().segment.document.name.filter(equal(this(),<!-- insert txt filename -->)).parent().parent().content' > $$$+<!-- insert txt filename -->"
FILENAMES_PATH = "/root/Downloads/gelmaTCC/CAP.2/filenames.txt"
OUTPUT_DIRECTORY = "/root/Downloads/gelmaTCC"

def load_filenames():
    """Loads filenames from a text file."""
    with open(FILENAMES_PATH, 'r') as file:
        filenames = [line.strip() for line in file]
    return filenames

def generate_command(filename, number):
    """Generates the customized command."""
    number_str = str(number).zfill(2)
    command = COMMAND_TEMPLATE.replace("<!-- insert txt filename -->", filename).replace("$$$", number_str)
    output_filename = f"{number_str}+{filename}"
    return command, output_filename

def execute_command(command):
    """Executes the given command in the shell."""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

def process_output_file(output_filename, input_filename):
    """Appends citation to the beginning and end of the output file."""
    filepath = os.path.join(OUTPUT_DIRECTORY, output_filename)
    citation = f"\\cite{{ input_filename }}"
    try:
        with open(filepath, 'r+') as file:
            content = file.read()
            file.seek(0, 0)
            file.write(citation + '\n' + content + '\n' + citation)
    except IOError as e:
        print(f"Error processing file: {e}")

def main():
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    filenames = load_filenames()
    for filename in filenames:
        for number in range(44):
            command, output_filename = generate_command(filename, number)
            execute_command(command)
            process_output_file(output_filename, filename)

if __name__ == "__main__":
    main()

```
