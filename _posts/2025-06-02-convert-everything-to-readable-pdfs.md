---
tags: [scratchpad]
info: aberto.
date: 2025-06-02
type: post
layout: post
published: true
slug: convert-everything-to-readable-pdfs
title: 'Convert everything to readable PDFs'
---
{% codeblock bash %}
#!/bin/bash
# enhanced_batch_convert_to_pdf.sh
# Converts diverse files to PDFs with readable text, metadata, or hex dumps.

# --- Configuration ---
# Optional: Set a common path prefix to strip from input file paths when creating output subdirectories.
# If your files are in /mnt/data/project1/docs and you set this to /mnt/data/project1,
# output for /mnt/data/project1/docs/file.txt will be in converted_pdfs/docs/file.pdf.
# If empty or not set, full paths (minus leading /) will be used for subdirectory structure.
COMMON_PREFIX_TO_STRIP="/mnt/mSATA/linaro/Desktop/00-TEMP/TCC/unique"

# How to handle binary/unconvertible files:
# "metadata": Create a PDF with file info (name, type, size).
# "hex": Create a PDF with a hex dump of the file.
# "strings": Create a PDF with printable strings from the file.
DEFAULT_BINARY_HANDLING="strings"

# Force OCR on all existing PDFs, even if they seem to have a text layer.
# If false, OCRs only if no text layer is detected or if it's an image-to-PDF conversion.
FORCE_OCR_ALL_EXISTING_PDFS=false

# For images converted to PDF, should OCR be attempted?
OCR_IMAGES_TO_PDF=true

OUTPUT_DIR_BASE="converted_pdfs" # All output will go into subdirectories here
LOG_FILE="conversion_log_enhanced.txt"

# --- Helper Functions ---

# Function to log messages
log_msg() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Check for required commands
check_commands() {
    local missing_cmds=0
    local cmds_to_check=(
        "file" "libreoffice" "pandoc" "pdflatex" "convert" "jq" "enscript"
        "ps2pdf" "pdffonts" "ocrmypdf" "xxd" "man" "realpath" "mktemp" "dirname" "basename"
    )
    log_msg "INFO: Checking for required commands..."
    for cmd in "${cmds_to_check[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            log_msg "ERROR: Required command '$cmd' not found. Please install it."
            echo "ERROR: Required command '$cmd' not found. Please install it." >&2
            missing_cmds=$((missing_cmds + 1))
        fi
    done
    if [[ $missing_cmds -gt 0 ]]; then
        log_msg "FATAL: $missing_cmds required command(s) are missing. Exiting."
        echo "FATAL: $missing_cmds required command(s) are missing. Exiting." >&2
        exit 1
    fi
    log_msg "INFO: All required commands found."
}

# Check for embedded text in PDF
has_text_layer() {
    # Returns 0 if text layer exists, 1 if not or error
    if ! pdffonts "$1" &>/dev/null; then return 1; fi # pdffonts error
    if [[ $(pdffonts "$1" | awk 'NR>2 {if ($NF != "no") c++} END{print c+0}') -gt 0 ]]; then
        return 0 # Has text
    else
        return 1 # No text
    fi
}

# Normalize extension to lowercase
normalize_ext() {
    local filename=$(basename "$1")
    local ext="${filename##*.}"
    if [[ "$ext" == "$filename" ]]; then # No extension
        echo ""
    else
        echo "${ext}" | tr '[:upper:]' '[:lower:]'
    fi
}

# Create placeholder PDF with metadata
create_metadata_pdf() {
    local infile="$1"
    local outfile="$2"
    local detected_mimetype="$3"
    local file_description="$4"
    local reason="$5"
    local filesize=$(du -b "$infile" | cut -f1) # Size in bytes

    log_msg "INFO: Creating metadata PDF for '$infile'. Reason: $reason"
    (
        echo "File Information"
        echo "----------------"
        echo "Original Filename: $(basename "$infile")"
        echo "Full Path: $infile"
        echo "Detected MIME Type: $detected_mimetype"
        echo "File Command Description: $file_description"
        echo "Size: $filesize bytes ($(du -h "$infile" | cut -f1))"
        echo "Modification Date: $(date -r "$infile")"
        echo ""
        echo "Reason for this Metadata PDF:"
        echo "$reason"
        echo "The content of the original file could not be meaningfully rendered as a standard document."
    ) | enscript -B --font=Courier10 --word-wrap --margins=50:50:50:50 -p - -o - | ps2pdf - "$outfile" >> "$LOG_FILE" 2>&1
    if [[ $? -eq 0 && -s "$outfile" ]]; then
        log_msg "OK: Metadata PDF created for '$infile' at '$outfile'."
    else
        log_msg "ERROR: Metadata PDF creation FAILED for '$infile'."
    fi
}

# Create hex dump PDF
create_hexdump_pdf() {
    local infile="$1"
    local outfile="$2"
    local detected_mimetype="$3"
    local file_description="$4"
    local filesize=$(du -b "$infile" | cut -f1)

    log_msg "INFO: Creating hex dump PDF for '$infile'."
    (
        echo "File Information & Hex Dump"
        echo "---------------------------"
        echo "Original Filename: $(basename "$infile")"
        echo "Full Path: $infile"
        echo "Detected MIME Type: $detected_mimetype"
        echo "File Command Description: $file_description"
        echo "Size: $filesize bytes ($(du -h "$infile" | cut -f1))"
        echo "Modification Date: $(date -r "$infile")"
        echo ""
        echo "Hex Dump (first 1MB or full file if smaller):"
        xxd -l 1048576 "$infile" # Limit to 1MB to avoid huge PDFs
    ) | enscript -B --font=Courier8 --word-wrap --margins=50:50:50:50 -r -p - -o - | ps2pdf - "$outfile" >> "$LOG_FILE" 2>&1 # -r for landscape
     if [[ $? -eq 0 && -s "$outfile" ]]; then
        log_msg "OK: Hex dump PDF created for '$infile' at '$outfile'."
    else
        log_msg "ERROR: Hex dump PDF creation FAILED for '$infile'."
    fi
}

# Create strings PDF
create_strings_pdf() {
    local infile="$1"
    local outfile="$2"
    local detected_mimetype="$3"
    local file_description="$4"
    local filesize=$(du -b "$infile" | cut -f1)

    log_msg "INFO: Creating extracted strings PDF for '$infile'."
     (
        echo "File Information & Extracted Strings"
        echo "------------------------------------"
        echo "Original Filename: $(basename "$infile")"
        echo "Full Path: $infile"
        echo "Detected MIME Type: $detected_mimetype"
        echo "File Command Description: $file_description"
        echo "Size: $filesize bytes ($(du -h "$infile" | cut -f1))"
        echo "Modification Date: $(date -r "$infile")"
        echo ""
        echo "Extracted Printable Strings (UTF-8, min length 4):"
        strings -n 4 -a -t d --encoding=S "$infile" # Show offset, include all file
    ) | enscript -B --font=Courier10 --word-wrap --margins=50:50:50:50 -p - -o - | ps2pdf - "$outfile" >> "$LOG_FILE" 2>&1
    if [[ $? -eq 0 && -s "$outfile" ]]; then
        log_msg "OK: Strings PDF created for '$infile' at '$outfile'."
    else
        log_msg "ERROR: Strings PDF creation FAILED for '$infile'."
    fi
}


# --- Main Conversion Function ---
convert_file() {
    local infile="$1"
    local binary_handling_method="$2"
    local conversion_done=false

    # Determine output path
    local relative_path_to_input="$infile"
    if [[ -n "$COMMON_PREFIX_TO_STRIP" ]]; then
        # Ensure prefix ends with / if it's not empty and doesn't have one, for clean stripping
        local temp_prefix="$COMMON_PREFIX_TO_STRIP"
        [[ "${temp_prefix: -1}" != "/" && -n "$temp_prefix" ]] && temp_prefix="$temp_prefix/"
        
        # Strip prefix if infile starts with it
        if [[ "$infile" == "$temp_prefix"* ]]; then
             relative_path_to_input="${infile#"$temp_prefix"}"
        else # Prefix not found, use infile as is (minus leading / for safety with mkdir -p)
            relative_path_to_input="${infile#/}"
        fi
    else # No prefix to strip, use infile as is (minus leading /)
        relative_path_to_input="${infile#/}"
    fi
    
    local out_subdir="$OUTPUT_DIR_BASE/$relative_path_to_input"
    out_subdir=$(dirname "$out_subdir") # Get directory part for output
    mkdir -p "$out_subdir"

    local in_filename=$(basename "$infile")
    local in_base="${in_filename%.*}"
    # If filename has no extension, in_base becomes in_filename
    if [[ "$in_filename" == "$in_base" ]]; then
        in_base="$in_filename"
    fi
    local outfile="$out_subdir/$in_base.pdf"
    
    # Handle cases where infile itself is already $outfile (e.g. input is a.pdf, output is a.pdf)
    # or if infile is foo and outfile becomes foo.pdf, this is fine.
    # If infile is foo.txt and outfile is foo.pdf, this is fine.
    # If infile is foo.pdf and outfile is foo.pdf, this is fine.
    # The main concern is overwriting source if $infile == $outfile AND it's not a PDF already.
    # This is unlikely given $outfile always gets .pdf extension.
    # However, if $infile is /path/foo and $outfile is /path/foo.pdf, this is the desired outcome.

    local ext=$(normalize_ext "$in_filename")
    local mimetype=$(file -b --mime-type "$infile" | cut -d';' -f1) # Remove charset
    local filedesc=$(file -b "$infile")

    log_msg "-----------------------------------------------------"
    log_msg "START Processing: '$infile'"
    log_msg "INFO: MIME='$mimetype', Ext='$ext', Desc='$filedesc', OutFile='$outfile'"

    if [[ -f "$outfile" && "$outfile" -nt "$infile" ]]; then
        log_msg "SKIP: Output '$outfile' exists and is newer than '$infile'."
        return 0 # Indicate skipped
    fi

    case "$mimetype" in
        application/pdf)
            if $FORCE_OCR_ALL_EXISTING_PDFS; then
                log_msg "INFO: PDF '$infile' - OCR FORCED."
                ocrmypdf --force-ocr "$infile" "$outfile" >> "$LOG_FILE" 2>&1
            elif ! has_text_layer "$infile"; then
                log_msg "INFO: PDF '$infile' needs OCR (no text layer detected)."
                ocrmypdf "$infile" "$outfile" >> "$LOG_FILE" 2>&1 # Default: adds layer if missing
            else
                log_msg "INFO: PDF '$infile' has text layer. Copying."
                cp "$infile" "$outfile" >> "$LOG_FILE" 2>&1
                if [[ $? -eq 0 ]]; then conversion_done=true; else log_msg "ERROR: Failed to copy PDF '$infile'."; fi
            fi
            if [[ -f "$outfile" && $? -eq 0 ]]; then # Check if ocrmypdf or cp succeeded
                log_msg "OK: PDF '$infile' processed to '$outfile'."
                conversion_done=true
            elif [[ ! -f "$outfile" ]]; then # If ocrmypdf failed and didn't create outfile
                log_msg "ERROR: Processing PDF '$infile' failed. Output file not created."
            fi
            ;;

        application/msword|application/vnd.ms-word*|\
        application/vnd.openxmlformats-officedocument.wordprocessingml.document|\
        application/vnd.oasis.opendocument.text*|application/rtf|\
        application/vnd.ms-excel*|application/vnd.openxmlformats-officedocument.spreadsheetml.sheet|\
        application/vnd.oasis.opendocument.spreadsheet*)
            log_msg "INFO: Office document '$infile'. Converting with LibreOffice."
            # LibreOffice --convert-to pdf uses the input filename with .pdf extension in the --outdir
            local lo_expected_out_name="$out_subdir/$in_base.pdf" # This should match $outfile
            libreoffice --headless --convert-to pdf "$infile" --outdir "$out_subdir" >> "$LOG_FILE" 2>&1
            if [[ -f "$lo_expected_out_name" ]]; then
                 # If $lo_expected_out_name is different from $outfile (e.g. due to sanitization or complex base name)
                 # This should not happen if $outfile is correctly constructed as $out_subdir/$in_base.pdf
                if [[ "$lo_expected_out_name" != "$outfile" ]]; then
                    log_msg "WARN: LibreOffice output '$lo_expected_out_name' differs from expected '$outfile'. Moving."
                    mv "$lo_expected_out_name" "$outfile" >> "$LOG_FILE" 2>&1
                fi
                log_msg "OK: '$infile' converted via LibreOffice to '$outfile'."
                conversion_done=true
            else
                log_msg "ERROR: LibreOffice conversion FAILED for '$infile'. Output '$lo_expected_out_name' not found."
            fi
            ;;

        text/csv|text/tab-separated-values)
            log_msg "INFO: CSV/TSV '$infile'. Converting with Pandoc."
            pandoc "$infile" -o "$outfile" --from=csv --toc --standalone >> "$LOG_FILE" 2>&1 \
                && { log_msg "OK: '$infile' converted via Pandoc."; conversion_done=true; } \
                || log_msg "ERROR: Pandoc (CSV) FAILED for '$infile'."
            ;;

        text/markdown)
            log_msg "INFO: Markdown '$infile'. Converting with Pandoc."
            pandoc "$infile" -o "$outfile" --standalone >> "$LOG_FILE" 2>&1 \
                && { log_msg "OK: '$infile' converted via Pandoc."; conversion_done=true; } \
                || log_msg "ERROR: Pandoc (Markdown) FAILED for '$infile'."
            ;;
        
        application/json)
            log_msg "INFO: JSON '$infile'. Attempting pretty-print with jq then Pandoc."
            local tmp_json_pretty=$(mktemp "$out_subdir/json_pretty_XXXXXX.json")
            if jq . "$infile" > "$tmp_json_pretty" 2>/dev/null; then
                pandoc "$tmp_json_pretty" -o "$outfile" --standalone >> "$LOG_FILE" 2>&1 \
                    && { log_msg "OK: '$infile' (pretty JSON) converted via Pandoc."; conversion_done=true; } \
                    || { log_msg "ERROR: Pandoc (pretty JSON) FAILED for '$infile'. Trying enscript.";
                         enscript "$infile" --font=Courier10 -p - -o - | ps2pdf - "$outfile" >> "$LOG_FILE" 2>&1 \
                            && { log_msg "OK: '$infile' (JSON) converted via enscript fallback."; conversion_done=true; } \
                            || log_msg "ERROR: enscript fallback for JSON '$infile' FAILED."; }
            else
                log_msg "WARN: jq failed for '$infile'. Trying Pandoc on raw, then enscript."
                pandoc "$infile" -o "$outfile" --standalone >> "$LOG_FILE" 2>&1 \
                    && { log_msg "OK: '$infile' (raw JSON) converted via Pandoc."; conversion_done=true; } \
                    || { log_msg "ERROR: Pandoc (raw JSON) FAILED for '$infile'. Trying enscript.";
                         enscript "$infile" --font=Courier10 -p - -o - | ps2pdf - "$outfile" >> "$LOG_FILE" 2>&1 \
                            && { log_msg "OK: '$infile' (JSON) converted via enscript fallback."; conversion_done=true; } \
                            || log_msg "ERROR: enscript fallback for JSON '$infile' FAILED."; }
            fi
            rm -f "$tmp_json_pretty"
            ;;

        image/png|image/jpeg|image/gif|image/bmp|image/tiff|image/webp)
            log_msg "INFO: Image '$infile'."
            if $OCR_IMAGES_TO_PDF && command -v ocrmypdf &> /dev/null; then
                log_msg "Attempting OCR with ocrmypdf for image '$infile'."
                ocrmypdf "$infile" "$outfile" >> "$LOG_FILE" 2>&1 \
                    && { log_msg "OK: Image '$infile' OCR'd via ocrmypdf to '$outfile'."; conversion_done=true; } \
                    || { log_msg "ERROR: ocrmypdf FAILED for image '$infile'. Falling back to ImageMagick's convert.";
                         convert "$infile" "$outfile" >> "$LOG_FILE" 2>&1 \
                            && { log_msg "OK: Image '$infile' converted via ImageMagick (no OCR)."; conversion_done=true; } \
                            || log_msg "ERROR: ImageMagick's convert also FAILED for '$infile'."; }
            else
                log_msg "Converting image '$infile' with ImageMagick's convert (no OCR)."
                convert "$infile" "$outfile" >> "$LOG_FILE" 2>&1 \
                    && { log_msg "OK: Image '$infile' converted via ImageMagick."; conversion_done=true; } \
                    || log_msg "ERROR: ImageMagick's convert FAILED for '$infile'."
            fi
            ;;

        application/x-tex|text/x-tex|application/x-latex)
            if [[ "$ext" == "cls" || "$ext" == "sty" ]]; then # LaTeX class/style files
                log_msg "INFO: LaTeX Class/Style file '$infile'. Converting as syntax-highlighted text."
                pandoc "$infile" --standalone --highlight-style=kate -o "$outfile" >> "$LOG_FILE" 2>&1 \
                    && { log_msg "OK: '$infile' converted via Pandoc (as LaTeX source)."; conversion_done=true; } \
                    || { log_msg "ERROR: Pandoc (LaTeX source) FAILED for '$infile'. Trying enscript.";
                         enscript "$infile" --font=Courier10 --highlight=latex -p - -o - | ps2pdf - "$outfile" >> "$LOG_FILE" 2>&1 \
                            && { log_msg "OK: '$infile' converted via enscript (highlighted LaTeX)."; conversion_done=true; } \
                            || log_msg "ERROR: enscript (highlighted LaTeX) FAILED for '$infile'."; }
            else # Regular .tex files
                log_msg "INFO: LaTeX document '$infile'. Compiling with pdflatex."
                local temp_tex_dir=$(mktemp -d "$out_subdir/tex_compile_XXXXXX")
                cp "$infile" "$temp_tex_dir/" # Copy tex file to temp dir
                # If there are associated .bib files or images, they'd need to be copied too or paths adjusted.
                # This simplified version assumes self-contained .tex or resolvable paths from temp_tex_dir.
                
                local tex_filename_only=$(basename "$infile")
                (cd "$temp_tex_dir" && \
                 pdflatex -interaction=nonstopmode "$tex_filename_only" && \
                 pdflatex -interaction=nonstopmode "$tex_filename_only") >> "$LOG_FILE" 2>&1
                
                local compiled_pdf_base="${tex_filename_only%.*}"
                local compiled_pdf_path="$temp_tex_dir/$compiled_pdf_base.pdf"

                if [[ -f "$compiled_pdf_path" ]]; then
                    mv "$compiled_pdf_path" "$outfile" >> "$LOG_FILE" 2>&1 \
                        && { log_msg "OK: '$infile' compiled via pdflatex to '$outfile'."; conversion_done=true; } \
                        || log_msg "ERROR: pdflatex compiled '$infile', but FAILED to move to '$outfile'."
                else
                    log_msg "ERROR: pdflatex compilation FAILED for '$infile'. Output PDF not found in '$temp_tex_dir'."
                fi
                rm -rf "$temp_tex_dir"
            fi
            ;;
        
        application/x-bibtex|text/x-bibtex)
            log_msg "INFO: BibTeX file '$infile'. Converting with Pandoc."
            pandoc "$infile" --standalone -o "$outfile" >> "$LOG_FILE" 2>&1 \
                && { log_msg "OK: '$infile' converted via Pandoc."; conversion_done=true; } \
                || { log_msg "ERROR: Pandoc (BibTeX) FAILED for '$infile'. Trying enscript.";
                     enscript "$infile" --font=Courier10 -p - -o - | ps2pdf - "$outfile" >> "$LOG_FILE" 2>&1 \
                        && { log_msg "OK: '$infile' (BibTeX) converted as plain text via enscript."; conversion_done=true; } \
                        || log_msg "ERROR: enscript fallback for BibTeX '$infile' FAILED."; }
            ;;

        application/x-troff-man|text/troff) # Man pages
            log_msg "INFO: Man page '$infile'. Converting with 'man'."
            man -Tpdf "$infile" > "$outfile" 2>> "$LOG_FILE" # man outputs errors to stderr
            if [[ $? -eq 0 && -s "$outfile" ]]; then
                log_msg "OK: '$infile' converted via 'man -Tpdf'."
                conversion_done=true
            else
                log_msg "WARN: 'man -Tpdf' FAILED for '$infile'. Trying Pandoc."
                pandoc "$infile" --standalone -f man -t pdf -o "$outfile" >> "$LOG_FILE" 2>&1 \
                    && { log_msg "OK: '$infile' converted via Pandoc (man)."; conversion_done=true; } \
                    || { log_msg "ERROR: Pandoc (man) FAILED for '$infile'. Trying enscript.";
                         enscript "$infile" --font=Courier10 -p - -o - | ps2pdf - "$outfile" >> "$LOG_FILE" 2>&1 \
                            && { log_msg "OK: '$infile' (man page) converted as text via enscript."; conversion_done=true; } \
                            || log_msg "ERROR: enscript fallback for man page '$infile' FAILED."; }
            fi
            ;;

        text/x-python|text/x-shellscript|application/x-perl|application/x-ruby|\
        text/x-csrc|text/x-chdr|text/x-c++src|text/x-java|text/html|text/css|application/javascript|application/xml|text/xml) # Code, XML, HTML
            log_msg "INFO: Code/Markup file '$infile' ($mimetype). Converting with Pandoc (syntax highlighting)."
            # Determine Pandoc format based on extension if possible for better highlighting
            local pandoc_format_opt=""
            case "$ext" in
                py) pandoc_format_opt="python" ;;
                sh|bash) pandoc_format_opt="bash" ;;
                pl) pandoc_format_opt="perl" ;;
                rb) pandoc_format_opt="ruby" ;;
                c|h) pandoc_format_opt="c" ;;
                cpp|hpp|cxx) pandoc_format_opt="cpp" ;;
                java) pandoc_format_opt="java" ;;
                html|htm) pandoc_format_opt="html" ;;
                css) pandoc_format_opt="css" ;;
                js) pandoc_format_opt="javascript" ;;
                xml|bcf|run.xml) pandoc_format_opt="xml" ;; # .bcf (Biber control file), .run.xml
            esac
            
            if [[ -n "$pandoc_format_opt" ]]; then
                pandoc "$infile" --from="$pandoc_format_opt" --standalone --highlight-style=kate -o "$outfile" >> "$LOG_FILE" 2>&1
            else # Default to Pandoc auto-detection or plain text
                pandoc "$infile" --standalone --highlight-style=kate -o "$outfile" >> "$LOG_FILE" 2>&1
            fi

            if [[ $? -eq 0 && -s "$outfile" ]]; then
                log_msg "OK: '$infile' converted via Pandoc with highlighting."
                conversion_done=true
            else
                log_msg "WARN: Pandoc with highlighting FAILED for '$infile'. Trying enscript."
                local enscript_hl_opt=""
                [[ -n "$ext" ]] && enscript_hl_opt="--highlight=$ext"
                enscript "$infile" --font=Courier10 $enscript_hl_opt -p - -o - | ps2pdf - "$outfile" >> "$LOG_FILE" 2>&1 \
                    && { log_msg "OK: '$infile' converted via enscript."; conversion_done=true; } \
                    || log_msg "ERROR: enscript fallback for '$infile' FAILED."
            fi
            ;;
        
        text/*) # Generic text files (.log, .txt, .bak, .aux, .synctex, .blg, .info, .lst, .conf etc.)
            log_msg "INFO: Generic text file '$infile' ($mimetype, ext: .$ext). Converting with enscript."
            enscript "$infile" --font=Courier10 --word-wrap -p - -o - | ps2pdf - "$outfile" >> "$LOG_FILE" 2>&1 \
                && { log_msg "OK: '$infile' converted via enscript."; conversion_done=true; } \
                || log_msg "ERROR: enscript FAILED for '$infile'."
            ;;

        application/octet-stream|application/x-dosexec|application/x-sharedlib|\
        application/x-object|application/x-executable|application/x-sqlite3|inode/x-empty|\
        application/x-archive|application/zip|application/gzip|application/x-bzip2|application/x-xz)
            log_msg "INFO: Binary/Archive/Empty/Unknown file '$infile' (MIME: $mimetype, Desc: $filedesc)."
            if [[ "$mimetype" == "inode/x-empty" ]]; then
                create_metadata_pdf "$infile" "$outfile" "$mimetype" "$filedesc" "File is empty."
                conversion_done=true
            # Heuristic: if 'filedesc' suggests text despite octet-stream, try enscript
            elif [[ "$filedesc" == *"text"* || "$filedesc" == *"script"* || "$filedesc" == *"ASCII text"* || "$filedesc" == *"UTF-8 Unicode text"* ]]; then
                log_msg "INFO: MIME is '$mimetype', but filedesc suggests text ('$filedesc'). Trying enscript."
                enscript "$infile" --font=Courier10 --word-wrap -p - -o - | ps2pdf - "$outfile" >> "$LOG_FILE" 2>&1 \
                    && { log_msg "OK: '$infile' converted via enscript (heuristic)."; conversion_done=true; } \
                    || { log_msg "ERROR: enscript (heuristic) FAILED for '$infile'. Using binary handling.";
                         if [[ "$binary_handling_method" == "hex" ]]; then create_hexdump_pdf "$infile" "$outfile" "$mimetype" "$filedesc";
                         elif [[ "$binary_handling_method" == "strings" ]]; then create_strings_pdf "$infile" "$outfile" "$mimetype" "$filedesc";
                         else create_metadata_pdf "$infile" "$outfile" "$mimetype" "$filedesc" "Binary or undetermined content type ($mimetype)."; fi
                         conversion_done=true; # Placeholder PDF is a form of "done"
                       }
            else # Standard binary handling
                if [[ "$binary_handling_method" == "hex" ]]; then create_hexdump_pdf "$infile" "$outfile" "$mimetype" "$filedesc";
                elif [[ "$binary_handling_method" == "strings" ]]; then create_strings_pdf "$infile" "$outfile" "$mimetype" "$filedesc";
                else create_metadata_pdf "$infile" "$outfile" "$mimetype" "$filedesc" "Binary, archive, or undetermined content type ($mimetype)."; fi
                conversion_done=true; # Placeholder PDF is a form of "done"
            fi
            ;;
        
        *) # Fallback for truly unrecognized/unhandled MIME types
            log_msg "WARN: Unhandled MIME type '$mimetype' for '$infile'. File description: '$filedesc'."
            if [[ "$filedesc" == *"text"* || "$filedesc" == *"script"* || "$filedesc" == *"ASCII text"* || "$filedesc" == *"UTF-8 Unicode text"* ]]; then
                log_msg "INFO: Unhandled MIME, but filedesc suggests text ('$filedesc'). Trying enscript."
                enscript "$infile" --font=Courier10 --word-wrap -p - -o - | ps2pdf - "$outfile" >> "$LOG_FILE" 2>&1 \
                    && { log_msg "OK: '$infile' converted via enscript (heuristic for unhandled MIME)."; conversion_done=true; } \
                    || { log_msg "ERROR: enscript (heuristic for unhandled MIME) FAILED for '$infile'. Using binary handling.";
                         if [[ "$binary_handling_method" == "hex" ]]; then create_hexdump_pdf "$infile" "$outfile" "$mimetype" "$filedesc";
                         elif [[ "$binary_handling_method" == "strings" ]]; then create_strings_pdf "$infile" "$outfile" "$mimetype" "$filedesc";
                         else create_metadata_pdf "$infile" "$outfile" "$mimetype" "$filedesc" "Unhandled MIME type ($mimetype) and not clearly text."; fi
                         conversion_done=true;
                       }
            else
                log_msg "INFO: Unhandled MIME type '$mimetype' for '$infile'. Using configured binary handling."
                if [[ "$binary_handling_method" == "hex" ]]; then create_hexdump_pdf "$infile" "$outfile" "$mimetype" "$filedesc";
                elif [[ "$binary_handling_method" == "strings" ]]; then create_strings_pdf "$infile" "$outfile" "$mimetype" "$filedesc";
                else create_metadata_pdf "$infile" "$outfile" "$mimetype" "$filedesc" "Unhandled MIME type ($mimetype)."; fi
                conversion_done=true;
            fi
            ;;
    esac

    if ! $conversion_done && [[ ! -f "$outfile" ]]; then
        log_msg "FALLBACK: No conversion method succeeded and no output file created for '$infile'. Creating placeholder."
        create_metadata_pdf "$infile" "$outfile" "$mimetype" "$filedesc" "No applicable conversion rule or all attempts failed."
    elif ! $conversion_done && [[ -f "$outfile" ]]; then
        log_msg "WARN: Conversion logic did not explicitly set 'done' flag, but output file '$outfile' exists. Assuming prior step handled it."
    fi
    log_msg "END Processing: '$infile'"
    [[ -f "$outfile" ]] && return 0 || return 1 # Return 0 if output exists, 1 otherwise
}

# --- Script Main Logic ---

# Argument Parsing
if [[ "$#" -lt 1 || "$#" -gt 4 ]]; then
    echo "Usage: $0 <listfile.txt> [common_prefix_to_strip] [binary_handling: metadata|hex|strings] [force_ocr_all_pdfs: true|false]"
    echo "Example: $0 myfiles.txt \"/mnt/mydata\" hex true"
    exit 1
fi

INPUT_LIST_FILE="$1"
[[ -n "$2" ]] && COMMON_PREFIX_TO_STRIP="$2"
[[ -n "$3" ]] && BINARY_HANDLING_USER_CHOICE="$3" || BINARY_HANDLING_USER_CHOICE="$DEFAULT_BINARY_HANDLING"
[[ -n "$4" ]] && FORCE_OCR_ALL_PDFS_USER_CHOICE="$4"

# Validate binary handling choice
case "$BINARY_HANDLING_USER_CHOICE" in
    metadata|hex|strings) BINARY_HANDLING="$BINARY_HANDLING_USER_CHOICE" ;;
    *) log_msg "WARN: Invalid binary_handling option '$BINARY_HANDLING_USER_CHOICE'. Defaulting to '$DEFAULT_BINARY_HANDLING'."; BINARY_HANDLING="$DEFAULT_BINARY_HANDLING" ;;
esac

# Validate force OCR choice
if [[ -n "$FORCE_OCR_ALL_PDFS_USER_CHOICE" ]]; then
    if [[ "$FORCE_OCR_ALL_PDFS_USER_CHOICE" == "true" ]]; then
        FORCE_OCR_ALL_EXISTING_PDFS=true
    elif [[ "$FORCE_OCR_ALL_PDFS_USER_CHOICE" == "false" ]]; then
        FORCE_OCR_ALL_EXISTING_PDFS=false
    else
        log_msg "WARN: Invalid force_ocr_all_pdfs option '$FORCE_OCR_ALL_PDFS_USER_CHOICE'. Using default ($FORCE_OCR_ALL_EXISTING_PDFS)."
    fi
fi

# Initialize Log File
echo "Conversion process started at $(date)" > "$LOG_FILE"
log_msg "INFO: Input List File: '$INPUT_LIST_FILE'"
log_msg "INFO: Common Prefix to Strip: '$COMMON_PREFIX_TO_STRIP'"
log_msg "INFO: Binary File Handling: '$BINARY_HANDLING'"
log_msg "INFO: Force OCR All Existing PDFs: $FORCE_OCR_ALL_EXISTING_PDFS"
log_msg "INFO: OCR Images to PDF: $OCR_IMAGES_TO_PDF"
log_msg "INFO: Output Base Directory: '$OUTPUT_DIR_BASE'"

check_commands # Check for essential tools

# Prepare clean file list (robust URL decoding)
CLEANED_LIST_FOR_PROCESSING_INTERNAL="cleaned_input_list_internal.tmp"
log_msg "INFO: Preparing clean file list from '$INPUT_LIST_FILE'..."
if python3 -c 'import sys, urllib.parse; [print(urllib.parse.unquote(line.strip())) for line in sys.stdin if line.strip()]' < "$INPUT_LIST_FILE" > "$CLEANED_LIST_FOR_PROCESSING_INTERNAL"; then
    log_msg "INFO: Clean file list created successfully using Python."
else
    log_msg "WARN: Python URL decoding failed (Python 3 not found or error). Using original list (may have issues with URL-encoded names)."
    cp "$INPUT_LIST_FILE" "$CLEANED_LIST_FOR_PROCESSING_INTERNAL" # Fallback
fi

# Create output base directory
mkdir -p "$OUTPUT_DIR_BASE"
log_msg "INFO: Ensured output base directory '$OUTPUT_DIR_BASE' exists."

# Process the list
total_files=0
successful_conversions=0
failed_conversions=0
skipped_up_to_date=0

while IFS= read -r file_to_process || [[ -n "$file_to_process" ]]; do
    # Skip empty or comment lines from the (cleaned) list
    [[ -z "$file_to_process" || "$file_to_process" =~ ^# ]] && continue

    total_files=$((total_files + 1))
    if [[ ! -e "$file_to_process" ]]; then # Use -e to check if path exists (file or dir)
        log_msg "ERROR: File or directory '$file_to_process' from list NOT FOUND. Skipping."
        failed_conversions=$((failed_conversions + 1))
        continue
    fi
    if [[ -d "$file_to_process" ]]; then
        log_msg "SKIP: Path '$file_to_process' is a DIRECTORY. Skipping."
        # Consider if directories should be counted as skipped or failed. For now, just log.
        continue
    fi
     if [[ ! -f "$file_to_process" ]]; then
        log_msg "SKIP: Path '$file_to_process' is NOT A REGULAR FILE. Skipping."
        continue
    fi
    if [[ ! -r "$file_to_process" ]]; then
        log_msg "ERROR: File '$file_to_process' is NOT READABLE. Skipping."
        failed_conversions=$((failed_conversions + 1))
        continue
    fi

    # The up-to-date check is now inside convert_file, which returns 0 for success/skipped-up-to-date
    convert_file "$file_to_process" "$BINARY_HANDLING"
    status=$?
    
    # Crude status check based on return value (0 for success/skipped, 1 for failure)
    # A more refined check would involve parsing the log for "SKIP" vs "OK"
    if [[ $status -eq 0 ]]; then
        # This counts files where an output PDF was created OR skipped because it was up-to-date.
        # To differentiate, we'd need more complex return codes or log parsing.
        # For now, if convert_file returns 0, it means no critical error in its own execution.
        # The actual "success" of conversion is in the log.
        : # Not incrementing success here, summary is tricky.
    else
        failed_conversions=$((failed_conversions + 1))
    fi
done < "$CLEANED_LIST_FOR_PROCESSING_INTERNAL"

rm -f "$CLEANED_LIST_FOR_PROCESSING_INTERNAL" # Clean up temp list

# Final Summary (approximated from log counts for more detail)
successful_ops=$(grep -cE "^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} - OK:" "$LOG_FILE")
error_ops=$(grep -cE "^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} - ERROR:" "$LOG_FILE")
skipped_ops=$(grep -cE "^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} - SKIP:" "$LOG_FILE") # Includes up-to-date and non-file skips

log_msg "-----------------------------------------------------"
log_msg "Conversion process completed at $(date)"
log_msg "SUMMARY: Total items from list processed: $total_files"
log_msg "SUMMARY: Successful operations (OK): $successful_ops"
log_msg "SUMMARY: Errored operations (ERROR): $error_ops"
log_msg "SUMMARY: Skipped operations (SKIP/NOT FOUND/DIR): $skipped_ops (includes up-to-date, not found, directories)"
log_msg "INFO: Detailed log written to '$LOG_FILE'"
log_msg "INFO: Output PDFs are in subdirectories under '$OUTPUT_DIR_BASE'"

echo "Conversion complete. Log: $LOG_FILE. Output in $OUTPUT_DIR_BASE."
{% endcodeblock %}