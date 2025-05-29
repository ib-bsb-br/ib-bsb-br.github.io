---
tags: [scratchpad]
info: aberto.
date: 2025-05-29
type: post
layout: post
published: true
slug: eml-mail-converter
title: '`.eml` mail converter'
---
{% codeblock python %}
import os
import email
from email.parser import BytesParser
from email.policy import default as default_email_policy # Modern email policy
from email.header import decode_header, make_header
import mimetypes # For guessing file extensions
import re
import traceback # For detailed error logging

def sanitize_filename(filename_str):
    """
    Sanitizes a string to be used as a filename.
    Removes or replaces characters that are not allowed or problematic in filenames
    across common operating systems. Handles email header objects.
    """
    if filename_str is None:
        return "_unnamed_file_"

    # If it's an email.header.Header object, decode it first
    if hasattr(filename_str, 'encode') and not isinstance(filename_str, str):
        try:
            decoded_parts = decode_header(str(filename_str))
            temp_filename_parts = []
            for part, charset in decoded_parts:
                if isinstance(part, bytes):
                    try:
                        temp_filename_parts.append(part.decode(charset or 'utf-8', 'replace'))
                    except LookupError: # Fallback for unknown charset
                        temp_filename_parts.append(part.decode('utf-8', 'replace'))
                else:
                    temp_filename_parts.append(part)
            filename_str = "".join(temp_filename_parts)
        except Exception as e:
            # If decoding complex header fails, fall back to simple string conversion
            print(f"    Warning: Could not fully decode filename header, using str(): {e}")
            filename_str = str(filename_str)
    elif not isinstance(filename_str, str):
        filename_str = str(filename_str) # Ensure it's a string

    # Remove or replace forbidden characters: < > : " / \ | ? * and control characters (0-31)
    filename_str = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', filename_str)

    # Replace multiple consecutive underscores or dots that might have resulted
    filename_str = re.sub(r'_+', '_', filename_str)
    filename_str = re.sub(r'\.+', '.', filename_str) # Allow single dots for extensions

    # Remove leading/trailing problematic characters (dots, underscores, spaces)
    filename_str = filename_str.strip('._ ')

    # Handle cases where the filename might become empty or just dots after sanitization
    if not filename_str or all(c == '.' for c in filename_str):
        return "_renamed_file_"

    # Prevent names that could be problematic (e.g., ".." relative paths)
    # The regex above should handle slashes, but this is an extra safety check.
    if ".." in filename_str:
        filename_str = filename_str.replace("..", "_") # Replace ".." with a single underscore

    # Limit length (e.g., 200 characters, leaving room for extensions/counters)
    max_len = 200
    if len(filename_str) > max_len:
        name_part, ext_part = os.path.splitext(filename_str)
        
        # Ensure ext_part is not excessively long itself
        if len(ext_part) > max_len / 2 : # Heuristic for very long extensions
            ext_part = ext_part[:10] # Truncate very long extension
        
        available_len_for_name = max_len - len(ext_part)
        if ext_part: # if there is an extension, account for the dot
            available_len_for_name -=1
            if available_len_for_name < 1: # Name part would be empty
                 name_part = "_trunc_" # Provide a minimal name part
                 available_len_for_name = len(name_part) # Recalculate for safety
            else:
                 name_part = name_part[:available_len_for_name]

        else: # No extension
            name_part = name_part[:max_len]
            
        filename_str = name_part + ('.' + ext_part.lstrip('.') if ext_part else "")

    return filename_str if filename_str else "_renamed_file_" # Final check for empty string


def process_eml_file(eml_file_path, base_output_dir):
    """
    Processes a single .eml file to extract its headers, body, and attachments.

    Args:
        eml_file_path (str): The path to the .eml file.
        base_output_dir (str): The directory where extracted content will be saved.
                               A subdirectory will be created here for each EML file.
    """
    print(f"\nProcessing EML file: {eml_file_path}")
    try:
        with open(eml_file_path, 'rb') as fp: # Read in binary mode
            msg = BytesParser(policy=default_email_policy).parse(fp)

        # --- Create a unique output directory for this email ---
        eml_filename_stem = os.path.splitext(os.path.basename(eml_file_path))[0]
        sanitized_eml_stem = sanitize_filename(eml_filename_stem)

        if not sanitized_eml_stem or sanitized_eml_stem == "_renamed_file_":
            unique_id = str(abs(hash(os.path.abspath(eml_file_path))) % 1000000) # Larger range for hash
            sanitized_eml_stem = f"email_extract_{unique_id}"
            print(f"    Warning: Original EML filename sanitized to an unusable name. Using fallback: {sanitized_eml_stem}")

        email_specific_output_dir = os.path.join(base_output_dir, sanitized_eml_stem)

        dir_counter = 1
        temp_output_dir = email_specific_output_dir
        while os.path.exists(temp_output_dir):
            temp_output_dir = f"{email_specific_output_dir}_{dir_counter}"
            dir_counter += 1
        email_specific_output_dir = temp_output_dir
        
        try:
            os.makedirs(email_specific_output_dir, exist_ok=True)
        except OSError as e:
            print(f"    Error creating output directory {email_specific_output_dir}: {e}")
            return # Cannot proceed without output directory
        print(f"  Outputting to: {email_specific_output_dir}")

        # --- Extract and save headers ---
        headers_to_extract = ["Subject", "From", "To", "Date", "Message-ID", 
                              "Cc", "Bcc", "Return-Path", "Reply-To"]
        header_info = []
        extracted_subject_for_log = "No_Subject" # Fallback

        for header_name in headers_to_extract:
            header_value = msg.get(header_name)
            if header_value:
                try:
                    # make_header handles folding and converting to a string.
                    # decode_header handles the actual charset decoding.
                    decoded_header_val = str(make_header(decode_header(str(header_value))))
                    header_info.append(f"{header_name}: {decoded_header_val}")
                    if header_name.lower() == "subject":
                        extracted_subject_for_log = decoded_header_val
                except Exception as e:
                    header_info.append(f"{header_name}: Error decoding header - {e}")
                    print(f"    Warning: Error decoding header '{header_name}': {e}")
        
        if header_info:
            try:
                with open(os.path.join(email_specific_output_dir, "_headers.txt"), "w", encoding="utf-8") as hf:
                    hf.write("\n".join(header_info))
                print("    Saved _headers.txt")
            except IOError as e:
                print(f"    Error saving _headers.txt: {e}")
        else:
            print("    No standard headers found or extracted.")


        # --- Extract Body and Attachments ---
        body_text_parts = []
        body_html_parts = []
        attachment_idx = 0 

        for part_num, part in enumerate(msg.walk()):
            content_disposition = part.get("Content-Disposition")
            content_type = part.get_content_type()
            
            is_attachment = False
            # Rule 1: Explicit "attachment" in Content-Disposition
            if content_disposition and "attachment" in content_disposition.lower():
                is_attachment = True
            # Rule 2: Has a filename (even if disposition is "inline" or missing)
            # This helps catch inline images that are also distinct files.
            elif part.get_filename(): 
                 is_attachment = True
            # Rule 3: Non-text, non-multipart part without a disposition (e.g., a directly embedded image)
            # This is a heuristic and might sometimes misclassify, but often useful.
            elif not part.is_multipart() and \
                 not content_type.startswith("text/") and \
                 not content_type.startswith("multipart/") and \
                 not content_disposition:
                 is_attachment = True

            if is_attachment:
                attachment_idx += 1
                original_filename = part.get_filename() # This method handles decoding of filenames

                if original_filename:
                    filename = sanitize_filename(original_filename)
                else:
                    ext = mimetypes.guess_extension(content_type, strict=False) or '.dat'
                    filename = sanitize_filename(f"attachment_{attachment_idx}{ext}")
                
                if not filename or filename == "_renamed_file_": # Final fallback if sanitization fails badly
                    filename = f"attachment_{attachment_idx}_fallback.dat"

                filepath = os.path.join(email_specific_output_dir, filename)
                
                file_counter = 1
                base_name, ext_name = os.path.splitext(filepath)
                # Ensure base_name is not empty if original filename was just an extension (e.g. ".pdf")
                if not base_name and ext_name: # e.g. if original was ".txt"
                    base_name = f"attachment_{attachment_idx}_base"

                while os.path.exists(filepath):
                    filepath = f"{base_name}_{file_counter}{ext_name}"
                    file_counter += 1
                    
                try:
                    payload = part.get_payload(decode=True) 
                    if payload is not None: 
                        with open(filepath, 'wb') as f_attach:
                            f_attach.write(payload)
                        print(f"    Saved attachment: {os.path.basename(filepath)}")
                    else:
                        print(f"    Skipped attachment {os.path.basename(filepath)} (empty payload after decoding).")
                except IOError as e:
                    print(f"    IOError saving attachment {os.path.basename(filepath)}: {e}")
                except Exception as e:
                    print(f"    Error saving attachment {os.path.basename(filepath)}: {e}")
            
            # Body parts (not explicitly attachments based on above rules)
            elif content_type == "text/plain" and (not content_disposition or "inline" in content_disposition.lower()):
                try:
                    payload = part.get_payload(decode=True)
                    if payload is not None:
                        charset = part.get_content_charset() or 'utf-8' 
                        body_text_parts.append(payload.decode(charset, errors='replace'))
                except Exception as e:
                    print(f"    Error decoding text/plain part: {e}")
            
            elif content_type == "text/html" and (not content_disposition or "inline" in content_disposition.lower()):
                try:
                    payload = part.get_payload(decode=True)
                    if payload is not None:
                        charset = part.get_content_charset() or 'utf-8'
                        body_html_parts.append(payload.decode(charset, errors='replace'))
                except Exception as e:
                    print(f"    Error decoding text/html part: {e}")

        # Save body parts
        if body_text_parts:
            body_text_content = "\n\n--- (Next Text Part) ---\n\n".join(body_text_parts)
            body_text_filepath = os.path.join(email_specific_output_dir, "body.txt")
            try:
                with open(body_text_filepath, 'w', encoding='utf-8') as f_body_txt:
                    f_body_txt.write(body_text_content)
                print(f"    Saved text body to body.txt")
            except IOError as e:
                print(f"    Error saving body.txt: {e}")
        
        if body_html_parts:
            body_html_content = "\n\n<hr><p>--- (Next HTML Part) ---</p><hr>\n\n".join(body_html_parts)
            body_html_filepath = os.path.join(email_specific_output_dir, "body.html")
            try:
                with open(body_html_filepath, 'w', encoding='utf-8') as f_body_html:
                    f_body_html.write(body_html_content)
                print(f"    Saved HTML body to body.html")
            except IOError as e:
                print(f"    Error saving body.html: {e}")
                
        # Fallback for non-multipart messages that are purely text and weren't caught as body
        if not msg.is_multipart() and not body_text_parts and not body_html_parts and msg.get_content_type().startswith("text/"):
            try:
                payload = msg.get_payload(decode=True)
                if payload is not None:
                    charset = msg.get_content_charset() or 'utf-8'
                    body_content = payload.decode(charset, errors='replace')
                    subtype = sanitize_filename(msg.get_content_subtype() or "txt")
                    if not subtype or subtype == "_renamed_file_": subtype = "txt" # Ensure valid extension
                    body_filepath = os.path.join(email_specific_output_dir, f"body_main.{subtype}")
                    with open(body_filepath, 'w', encoding='utf-8') as f_body_main:
                        f_body_main.write(body_content)
                    print(f"    Saved main text payload to {os.path.basename(body_filepath)}")
            except Exception as e:
                print(f"    Could not decode/save main text payload for non-multipart email: {e}")

        if not body_text_parts and not body_html_parts and attachment_idx == 0 and \
           (msg.is_multipart() or not msg.get_content_type().startswith("text/")):
            print(f"    Note: No distinct text/html body or attachments were extracted for '{os.path.basename(eml_file_path)}'. The content might be in an unusual format or the EML might be empty/corrupt.")

        print(f"  Finished processing {os.path.basename(eml_file_path)}")

    except FileNotFoundError:
        print(f"Error: EML file not found at {eml_file_path}")
    except Exception as e:
        print(f"An critical error occurred while processing {eml_file_path}: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    # --- HOW TO USE THIS SCRIPT ---
    # 1. Save this script as a Python file (e.g., eml_parser_revised.py).
    #
    # 2. CHOOSE ONE of the options below by UNCOMMENTING the relevant block.
    #    To uncomment a block, remove the triple quote characters (''' or """)
    #    from the beginning and end of that block.
    #
    # 3. MODIFY THE PATHS within your chosen uncommented block to point to your
    #    actual EML files and desired output location. Use ABSOLUTE paths if unsure.
    #    e.g., on Linux: '/home/youruser/my_emails/email.eml'
    #    e.g., on Windows: 'C:\\Users\\YourUser\\Documents\\MyEMLs' (note the double backslashes)
    #
    # 4. Run the script from your terminal:
    #    python3 eml_parser_revised.py
    #    (Or `python eml_parser_revised.py` if python3 is your default python)
    #
    # The script will create a main output directory, and inside it,
    # a subdirectory for each processed EML file. These subdirectories will
    # contain the extracted headers (_headers.txt), body (body.txt/body.html),
    # and any attachments.

    user_has_configured_an_option = True # This flag will be set if an option is chosen by uncommenting

    # --- OPTION 1: Process a SINGLE .eml file ---
    """
    eml_file_to_process = "YOUR_SINGLE_EML_FILE_PATH_HERE.eml"  # <-- *** SET THIS ABSOLUTE OR RELATIVE PATH ***
    main_output_folder = "eml_extracted_single_output"          # <-- SET YOUR DESIRED OUTPUT FOLDER NAME (will be created if not exists)

    # --- Do not edit below this line for Option 1 ---
    if eml_file_to_process == "YOUR_SINGLE_EML_FILE_PATH_HERE.eml":
        print("OPTION 1 IS UNCOMMENTED, BUT THE PATH IS STILL THE DEFAULT PLACEHOLDER.")
        print("Please edit 'eml_file_to_process' to your EML file's actual path.")
    elif os.path.isfile(eml_file_to_process):
        try:
            os.makedirs(main_output_folder, exist_ok=True)
            process_eml_file(eml_file_to_process, main_output_folder)
            print(f"\nSingle file processing complete. Output in: {os.path.abspath(main_output_folder)}")
        except Exception as e_main:
            print(f"Error during Option 1 execution: {e_main}")
        user_has_configured_an_option = True
    else:
        print(f"OPTION 1 ERROR: EML file not found at '{eml_file_to_process}'")
    """

    # --- OPTION 2: Process ALL .eml files in a DIRECTORY ---
    # """
    source_directory_with_emls = "/mnt/mSATA/linaro/Desktop/00-TEMP/EML mails/"  # <-- *** SET THIS ABSOLUTE OR RELATIVE PATH ***
    main_output_folder = "/mnt/mSATA/linaro/Desktop/00-TEMP/EMLout/"                        # <-- SET YOUR DESIRED OUTPUT FOLDER NAME (will be created if not exists)

    # --- Do not edit below this line for Option 2 ---
    if source_directory_with_emls == "YOUR_DIRECTORY_CONTAINING_EML_FILES_HERE":
        print("OPTION 2 IS UNCOMMENTED, BUT THE PATH IS STILL THE DEFAULT PLACEHOLDER.")
        print("Please edit 'source_directory_with_emls' to your EML directory's actual path.")
    elif os.path.isdir(source_directory_with_emls):
        try:
            os.makedirs(main_output_folder, exist_ok=True)
            eml_found_in_dir = False
            for item in os.listdir(source_directory_with_emls):
                if item.lower().endswith(".eml"):
                    eml_found_in_dir = True
                    full_eml_path = os.path.join(source_directory_with_emls, item)
                    process_eml_file(full_eml_path, main_output_folder)
            if not eml_found_in_dir:
                print(f"OPTION 2: No .eml files found in '{source_directory_with_emls}'")
            else:
                print(f"\nBatch processing complete. Output in: {os.path.abspath(main_output_folder)}")
        except Exception as e_main:
            print(f"Error during Option 2 execution: {e_main}")
        user_has_configured_an_option = True
    else:
        print(f"OPTION 2 ERROR: Directory not found at '{source_directory_with_emls}'")
    # """


    # --- OPTION 3: Test with the EML content provided in your prompt ---
    # To use this:
    # 1. Create a file named "my_test_email.eml" in the SAME directory as this script.
    # 2. Paste the FULL EML content (from your original prompt) into that "my_test_email.eml" file and save it.
    # 3. Then, uncomment this block and run the script.
    """
    test_eml_filename = "my_test_email.eml" 
    main_output_folder = "eml_extracted_test_sample_output"

    # --- Do not edit below this line for Option 3 ---
    if os.path.isfile(test_eml_filename):
        try:
            os.makedirs(main_output_folder, exist_ok=True)
            process_eml_file(test_eml_filename, main_output_folder)
            print(f"\nTest file processing complete. Output in: {os.path.abspath(main_output_folder)}")
        except Exception as e_main:
            print(f"Error during Option 3 execution: {e_main}")
        user_has_configured_an_option = True
    else:
        print(f"OPTION 3: Test file '{test_eml_filename}' not found in the script's directory.")
        print("          Please create it and paste your EML content into it to use this option.")
    """

    # --- If no option was uncommented and configured by the user, print detailed help ---
    if not user_has_configured_an_option:
        print("\n--- EML EXTRACTION SCRIPT HELP ---")
        print("This script extracts content and attachments from .eml (email) files.")
        print("\nTO USE THIS SCRIPT:")
        print("1. Open this Python script file (the .py file you saved) in a text editor.")
        print("2. Scroll down to the end of the file, to the section that starts with:")
        print("   'if __name__ == \"__main__\":'")
        print("3. You will see three 'OPTION' blocks (OPTION 1, OPTION 2, OPTION 3).")
        print("   These blocks are currently 'commented out' with triple quote characters")
        print("   (''') at their beginning and end.")
        print("\n4. CHOOSE ONLY ONE OPTION that fits your needs:")
        print("   - OPTION 1: If you want to process a single .eml file.")
        print("   - OPTION 2: If you want to process all .eml files within a specific folder.")
        print("   - OPTION 3: If you want to test the script with a sample 'my_test_email.eml' file")
        print("               (which you need to create first, as described in the comments for Option 3).")
        print("\n5. UNCOMMENT your chosen option's block. To do this, delete the three quote")
        print("   characters (''') from the very beginning of that block, AND delete the")
        print("   three quote characters (''') from the very end of that SAME block.")
        print("   Make sure only ONE option block is uncommented.")
        print("\n6. IMPORTANT: Inside the option block you just uncommented, you MUST update")
        print("   the placeholder paths. For example, change:")
        print("     'YOUR_SINGLE_EML_FILE_PATH_HERE.eml'")
        print("   to the actual, full path of your EML file, like:")
        print("     '/home/yourusername/emails/important_email.eml' (for Linux/macOS)")
        print("     'C:\\Users\\YourUserName\\Documents\\Emails\\archive.eml' (for Windows - note double backslashes)")
        print("   Similarly, update 'YOUR_DIRECTORY_CONTAINING_EML_FILES_HERE' if using Option 2,")
        print("   and you can customize 'main_output_folder' if desired.")
        print("\n7. Save the changes you made to this script file.")
        print("\n8. Open a terminal or command prompt.")
        print("9. Navigate to the directory where you saved this script file using the 'cd' command.")
        print("   (e.g., 'cd /path/to/where/you/saved/the_script')")
        print("10. Run the script by typing the following command and pressing Enter:")
        print("    python3 name_of_this_script.py")
        print("    (Replace 'name_of_this_script.py' with the actual filename you used, e.g., 'eml_parser_revised.py')")
        print("    If 'python3' doesn't work, try 'python name_of_this_script.py'.")
        print("\n   The script will then run, process your EML files, and save the extracted")
        print("   content (headers, body text/html, attachments) into subdirectories within")
        print("   the 'main_output_folder' you specified (or the default one for that option).")
        print("-----------------------------------\n")
{% endcodeblock %}