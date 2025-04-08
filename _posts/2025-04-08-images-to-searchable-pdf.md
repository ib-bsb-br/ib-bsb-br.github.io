---
tags: [scratchpad]
info: aberto.
date: 2025-04-08
type: post
layout: post
published: true
slug: images-to-searchable-pdf
title: 'Images to Searchable PDF'
---
This guide provides a comprehensive, in-depth walkthrough for transforming a directory full of images (such as scans of book pages, photographs of receipts, or digital documents saved in formats like JPG, PNG, or TIFF) into a single, unified, and text-searchable PDF file. Creating a searchable PDF unlocks numerous benefits: it allows for instant keyword searching, enables easy copying and pasting of text, improves accessibility for screen readers, facilitates data extraction, and allows seamless integration with document management systems.

We'll leverage powerful, mature, and widely-used open-source command-line tools available on most Linux-based systems, including the Windows Subsystem for Linux (WSL) on Windows and macOS via package managers like Homebrew.

**Scope and Alternatives:**

This guide focuses specifically on the img2pdf \+ ocrmypdf command-line workflow, which is highly efficient and scriptable, especially for large batches of images.

* **When this method shines:** Processing large numbers of images, automating document workflows, integrating into scripts, achieving lossless image combination before OCR.  
* ***When this method might not be ideal:***  
  * Users uncomfortable with the command line (GUI tools like [NAPS2](https://www.naps2.com/) (Windows/Linux) offer similar functionality).  
  * Processing existing digital PDFs that just need OCR (other tools might be simpler).  
  * Documents requiring the highest level of OCR accuracy or specific features only found in commercial OCR software (e.g., advanced table recognition, legal/compliance features).

## **Prerequisites: Tools and Concepts**

Before diving into the conversion process, it's crucial to install the necessary software and gain a solid understanding of the role each component plays. This foundation will help in troubleshooting potential issues and customizing the process to your specific needs.

1. **img2pdf**: This utility is specifically designed for combining multiple images into a single PDF document with remarkable efficiency. Its primary advantage lies in its commitment to **lossless conversion** whenever possible. Instead of re-compressing or re-encoding the image data (which can introduce quality degradation, known as generational loss, and increase processing time), img2pdf directly embeds the original image streams (JPG, PNG, TIFF, etc.) into the PDF structure. This preserves the exact pixel data, maintains any embedded metadata (like EXIF tags), and makes the initial PDF creation incredibly fast. While it supports common formats well, be aware that very obscure or specialized image types might require pre-conversion using other tools like ImageMagick.  
2. **ocrmypdf**: This is the powerhouse tool that adds the crucial searchability layer to your PDF. It takes an existing PDF (ideally, the one created losslessly by img2pdf) and orchestrates the complex process of Optical Character Recognition (OCR). Internally, it relies on the **Tesseract OCR engine**. For each page, ocrmypdf typically performs several preprocessing steps (like detecting orientation, deskewing tilted images, and potentially cleaning noise) before feeding the image to Tesseract. Tesseract then analyzes the shapes and patterns within the image, attempting to identify characters and words. The recognized text is then meticulously added back into the PDF as an **invisible text layer**, precisely positioned *behind* the original page image. This "sandwich PDF" approach (the default) preserves the original visual appearance while making the text selectable, searchable, and indexable.  
3. **Tesseract OCR Engine & Language Packs**: ocrmypdf is essentially a sophisticated wrapper around Tesseract. Tesseract itself is the engine performing the character recognition. Crucially, Tesseract cannot recognize text effectively without data files specific to the language(s) used in the document. These **language packs** contain information about character shapes, common letter combinations (ligatures), dictionaries, and grammatical structures for a specific language. Using the correct language pack(s) is paramount for accuracy. For example, recognizing French requires tesseract-ocr-fra to handle accents (é, à, ç) and specific letter pairings correctly, which tesseract-ocr-eng (English) would struggle with. You *must* install the packs corresponding to all significant languages present in your images. You can often find the required package names using your system's package manager search function (e.g., apt cache search tesseract-ocr-, dnf search tesseract-langpack-). Tesseract also includes a special pack, osd (Orientation and Script Detection), which helps ocrmypdf automatically determine page rotation and the script used (e.g., Latin, Cyrillic, Han).

**Installation:**

Choose the installation method most appropriate for your operating system. **Using the system package manager (apt, dnf, brew) is strongly recommended** as it handles dependencies, including the essential Tesseract engine and language packs, much more robustly.

* **Debian / Ubuntu / WSL:** System package managers like apt handle dependencies well.  
  \# Always update package list first for latest versions and dependencies  
  sudo apt update  
  \# Install the core tools and the English language pack  
  sudo apt install img2pdf ocrmypdf tesseract-ocr tesseract-ocr-eng  
  \# Example: Add Spanish and French language packs if needed  
  \# sudo apt install tesseract-ocr-spa tesseract-ocr-fra  
  \# Example: Install the Orientation and Script Detection pack (often useful)  
  \# sudo apt install tesseract-ocr-osd

* **Fedora / CentOS / RHEL:** dnf is the modern package manager for these distributions.  
  \# Check for updates first  
  sudo dnf check-update  
  \# Install the core tools and the English language pack  
  \# Note the slightly different naming convention for language packs  
  sudo dnf install img2pdf ocrmypdf tesseract tesseract-langpack-eng  
  \# Example: Add German language pack  
  \# sudo dnf install tesseract-langpack-deu

* **macOS (using Homebrew):** Homebrew is the de facto package manager for macOS command-line tools.  
  \# Update Homebrew itself and formula definitions  
  brew update  
  \# Install tools; Tesseract is usually installed as a dependency of ocrmypdf  
  brew install img2pdf ocrmypdf  
  \# Install desired language packs. Check Homebrew for exact naming.  
  \# Tesseract might need separate language pack installation via brew.  
  \# brew install tesseract-lang \# This might be a meta-package, check options  
  \# Or install all available languages (can be large, \>1GB)  
  \# brew install tesseract \--with-all-languages

* **pip (Python Package Installer \- Use with Extreme Caution):** While img2pdf and ocrmypdf are Python applications, installing them via pip requires **manual installation of dependencies** and is **not recommended for most users**.  
  \# Ensure pip is up-to-date  
  pip install \--upgrade pip  
  \# Install the Python tools  
  pip install img2pdf ocrmypdf  
  **\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\***  
  **CRITICAL WARNING: pip DOES NOT INSTALL TESSERACT OR LANGUAGE PACKS**  
  Installing ocrmypdf via pip **ONLY** installs the Python wrapper script.  
  It **DOES NOT** install the underlying Tesseract OCR engine or any Tesseract language packs, which are essential for OCR functionality.  
  You **MUST** *separately* install tesseract (the engine) and the required tesseract-data-\* or tesseract-langpack-\* packages using your operating system's native package manager (apt, dnf, brew) as shown in the sections above.  
  **Failure to install Tesseract and its language packs separately will cause ocrmypdf to fail when it attempts (and fails) to call the missing Tesseract engine.**  
  **\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\***  
  After any installation method, especially if using pip or encountering issues, ensure the tesseract executable is in your system's PATH. You can check this by simply typing tesseract \--version in your terminal; it should show version information, not a "command not found" error.

**Verify Installation & Languages (Optional but Recommended):**

Performing these checks confirms the tools are installed correctly and Tesseract has the necessary language support.

1. **Check Tool Versions:** Running the commands with \--version confirms they are installed and accessible. The version numbers can be useful for debugging (checking compatibility with documentation or known issues).  
   img2pdf \--version  
   ocrmypdf \--version  
   tesseract \--version \# This also shows versions of related libraries like Leptonica (image processing)

2. **List Installed Tesseract Languages:** This is crucial to ensure Tesseract can process your document's language(s).  
   tesseract \--list-langs

   The output will be a list of short codes (e.g., eng, fra, deu, spa, osd). Compare this list against the languages present in your source images. If a required language code is missing, you need to install the corresponding language pack using your system's package manager.

## **The Conversion Process: Step-by-Step**

Follow these steps meticulously. Accuracy in the early stages, particularly file naming and ordering, prevents significant headaches later.

### **1\. Navigate to Your Image Directory**

All subsequent commands assume you are running them from *within* the directory containing your image files. Use the terminal's cd (change directory) command.

\# Replace '/path/to/your/directory\_with\_images/' with the actual, full path  
cd /path/to/your/directory\_with\_images/

\# Tip: Use tab-completion\! Type the first few letters of a directory name  
\# and press Tab; the shell will try to auto-complete it, saving typing  
\# and preventing typos.  
pwd \# Optional: Print Working Directory to confirm you are in the right place.

Operating from the correct directory is essential as commands using wildcards (\*) will only find files in the current location.

### **2\. Verify and Ensure Correct Image Order**

The final PDF's page sequence is dictated by the order files are passed to img2pdf. When using shell wildcards (like \*.jpg), the shell expands this into a list of filenames. Crucially, this expansion typically uses **lexical sorting** based on your system's locale settings (like sorting in dictionary order). This means page\_10.jpg often comes *before* page\_2.jpg. Therefore, consistent, zero-padded file naming is essential for correct numerical ordering when using simple wildcards.

* **Ideal Naming:** Use leading zeros in sequential numbers to ensure lexical sort matches numerical sort.  
  * *Bad Example:* 1.jpg, 2.jpg, ..., 9.jpg, 10.jpg, 11.jpg (Lexical sort: 1.jpg, 10.jpg, 11.jpg, 2.jpg ...)  
  * *Good Example:* page\_001.jpg, page\_002.jpg, ..., page\_009.jpg, page\_010.jpg, page\_011.jpg, ..., page\_123.tif (Lexical sort matches numerical: ...009.jpg, 010.jpg, 011.jpg...)  
* **Check the Order:** Use ls \-v for a "version sort" or "natural sort". This command is generally smarter about numbers within filenames and usually previews the order img2pdf will receive files more accurately than a plain ls. (Note: ls \-v is common but not universally available on all systems; reliable zero-padding is the most robust method).  
  \# List JPG files using version sort (if available)  
  ls \-v \*.jpg  
  \# If using PNGs:  
  \# ls \-v \*.png  
  \# If mixed types, be careful how the shell expands this:  
  \# ls \-v page\_\*.jpg page\_\*.png \# May interleave types incorrectly depending on names

  **Visually inspect** the output carefully. Check the first few, last few, and transition points (like page 9 to 10, 99 to 100\) to confirm the sequence matches your intended document structure (e.g., cover, table of contents, chapters, index).  
* **Rename if Necessary:** If the order is incorrect, renaming is essential *before* proceeding.  
  * **Recommendation:** Use dedicated **bulk renaming tools**. These tools often provide previews, support complex patterns safely, and reduce the risk of accidental data loss compared to manual renaming or complex scripts.  
    * **Linux:** rename (Perl regex version, very powerful but complex syntax), renameutils (provides qmv for interactive editing in a text editor, imv for interactive single file renaming), graphical tools integrated with file managers (e.g., Thunar Bulk Rename, Krusader's Multi-Rename).  
    * **macOS:** Finder's built-in batch renaming (select files, right-click \> Rename), or powerful third-party apps like Name Mangler or A Better Finder Rename.  
    * **Windows/WSL:** Windows Explorer's basic renaming, dedicated GUI tools like Bulk Rename Utility (powerful, free), or use Linux tools via WSL.  
  * **Manual Renaming:** Only practical for a handful of files. Tedious and error-prone for many files.  
  * **Scripting (Advanced):** While custom scripts (e.g., bash loops) can rename files, they are risky. A small error in the script logic could potentially overwrite files or create an incorrect sequence. **Always test renaming scripts on copies of your files first.**

Investing time to get the file order correct now saves considerable effort compared to attempting to reorder pages within the PDF later.

### **3\. Combine Images into a Single PDF (Losslessly)**

Now, use img2pdf to assemble the correctly ordered images into a single, non-OCR'd PDF. Use wildcards carefully, ensuring they match your naming scheme.

* **Globbing Patterns:** \* matches zero or more characters, ? matches exactly one character. \*.jpg matches all files ending in .jpg. page\_???.jpg matches files starting with page\_ followed by exactly three characters and .jpg.

\# Ensure the wildcard matches your zero-padded, correctly ordered files  
\# Example for JPG files named like page\_001.jpg, page\_002.jpg ... page\_123.jpg  
img2pdf \*.jpg \--output combined\_raw.pdf

\# Example for PNG files named scan-001.png ... scan-999.png  
\# img2pdf scan-???.png \--output combined\_raw.pdf

\# Example for TIFF files:  
\# img2pdf \*.tif \--output combined\_raw.pdf

\# Combining multiple types requires careful ordering or explicit listing:  
\# If names ensure correct order across types (e.g., doc\_001.jpg, doc\_002.png):  
\# img2pdf doc\_\*.jpg doc\_\*.png \--output combined\_raw.pdf  
\# Be cautious with generic wildcards like \* if non-image files are present.

\# You can also set basic metadata here, though ocrmypdf often overwrites it:  
\# img2pdf \*.jpg \--output combined\_raw.pdf \--title "Initial Scan Combination"

* **Wildcard/File List:** The shell expands the pattern based on lexical sorting. Zero-padding ensures \*.jpg expands numerically. If filenames contain spaces or special characters, quote them: img2pdf "page 001.jpg" "page 002.jpg" ....  
* **\--output combined\_raw.pdf**: Specifies the output filename. Using a descriptive suffix like \_raw or \_no\_ocr clearly indicates this is the intermediate file *before* OCR processing.  
* **Potential img2pdf Errors:** Common issues include "file not found" (check path, wildcard, permissions) or errors related to unsupported/corrupted image formats (consider pre-conversion with ImageMagick).

Upon successful completion, a combined\_raw.pdf file will be created. **Open this PDF immediately** in a viewer. Quickly scroll through the pages to perform a final visual check of the order and ensure all images were included and appear correctly before proceeding to the time-consuming OCR step.

### **4\. Add OCR Text Layer and Optimize the PDF**

This is the core step where searchability is added. ocrmypdf orchestrates Tesseract and applies various enhancements. This step is computationally intensive and can take significant time.

\# Run ocrmypdf with a robust set of recommended options  
\# Adjust '-l' based on your document's language(s)  
ocrmypdf \\  
  \-l eng+fra \\  
  \--rotate-pages \\  
  \--deskew \\  
  \--optimize 3 \\  
  \--jobs 0 \\  
  \--title "Final Report \- Project X (2025)" \\  
  \--author "Operations Department" \\  
  \--output-type pdfa \\  
  combined\_raw.pdf \\  
  output\_document\_ocr.pdf

Let's dissect these and other useful options:

* **\-l LANGS**: Specifies language(s) for OCR (e.g., \-l eng, \-l eng+fra, \-l deu+jpn). Providing all relevant languages significantly boosts accuracy. Use codes from tesseract \--list-langs.  
* **\--rotate-pages**: Automatically detects page orientation based on recognized text and corrects it. Highly recommended.  
* **\--deskew**: Detects and corrects slightly tilted/skewed pages. Dramatically improves OCR accuracy.  
* **\--optimize N**: Controls file size optimization level.  
  * \--optimize 0: None. Fastest, largest file.  
  * \--optimize 1: Safe, lossless compression. Good balance.  
  * \--optimize 2: Enables mild lossy image optimization (e.g., slightly higher JPEG compression). Check quality.  
  * \--optimize 3 (Default if just \--optimize): Aggressive lossless *and* lossy optimization (may use JPEG/JPEG2000 for color/gray, JBIG2 for B\&W). Smallest size, potentially slower, requires quality check.  
* **\--jobs N**: Number of CPU cores for parallel processing.  
  * \--jobs 0: Use all available cores. Fastest, but highest RAM/disk usage.  
  * \--jobs N (e.g., \--jobs 4): Use N cores. Use if \--jobs 0 causes issues. Start with half your cores if unsure.  
* **\--title "..."** / **\--author "..."**: Sets PDF metadata.  
* **\--output-type pdfa**: Creates a PDF/A-2b file for long-term archival. Recommended.  
* **combined\_raw.pdf**: Input file from img2pdf.  
* **output\_document\_ocr.pdf**: Final searchable PDF.

**Other Potentially Useful ocrmypdf Options:**

* \--force-ocr: Re-runs OCR even if text is detected.  
* \--skip-text: Preserves existing text layers on pages that have them.  
* \--clean: Image cleaning *before* OCR (removes speckles). May improve accuracy but alters image.  
* \--clean-final: Image cleaning *after* OCR (cleans visual layer only).  
* \--jbig2-lossy: Aggressive lossy compression for B\&W images. Significant size reduction, check quality.  
* \--pdf-renderer {auto,hocr,sandwich}: How PDF is generated. sandwich (default) is most compatible (invisible text behind image). hocr embeds HTML-like data, potentially smaller but needs viewer support.  
* \--unpaper-args "...": Advanced image cleaning options. (Advanced).  
* \--skip-big N: Skip OCR on images \> N megapixels.

Once the command initiates, ocrmypdf provides a progress bar. Remember optimization occurs *after* OCR hits 100%. When finished, test the output PDF thoroughly (search, select text).

## **Important Considerations & Troubleshooting**

The conversion process, especially OCR, can be resource-intensive and prone to issues.

### **Resource Usage: Disk Space and Memory (RAM)**

**Critical Warning:** ocrmypdf is resource-hungry. Insufficient disk space or RAM are common causes of failure or extreme slowness.

* **Disk Space:**  
  * **Why?** Unpacks images, creates intermediate files (deskew, clean), stores OCR results. Temporary space needed can be **many times** the input PDF size (e.g., 500MB input might need 2-5GB+ temp space).  
  * **Location:** /tmp or $TMPDIR environment variable.  
  * **Problem:** Fails with "No space left on device" if the temp location is too small.  
  * **Monitoring:** df \-h /tmp (or $TMPDIR). Monitor during processing (du \-sh /tmp/ocrmypdf\*).  
  * **Solution:** Redirect temp files using TMPDIR to a larger partition:  
    export TMPDIR=/path/to/large/temp\_dir  
    mkdir \-p $TMPDIR \# Ensure it exists and is writable  
    ocrmypdf \[options...\] input.pdf output.pdf  
    \# Or per-command:  
    env TMPDIR=/path/to/large/temp\_dir ocrmypdf \[options...\] input.pdf output.pdf

  * **WSL Filesystem Caveats:** Using Windows paths (/mnt/c/...) for TMPDIR in WSL *can* work but may be slower or cause permission/feature issues. Using a directory *within* the WSL filesystem (\~/ocr\_temp) is often more reliable if space permits (df \-h within WSL).  
* **Memory (RAM):**  
  * **Usage:** OCR, especially parallel jobs (--jobs), uses significant RAM.  
  * **Problem:** Running out of RAM leads to slow "swapping" (using disk as RAM) or abrupt termination by the OOM Killer.  
  * **Monitoring:** htop, top, free \-h. Watch for high swap usage or disappearing processes.  
  * **Solution:** Reduce parallel jobs: use \--jobs N with a smaller N (e.g., \--jobs 2, \--jobs 1).

### **Processing Time: Patience is Key**

OCR takes time. Factors influencing speed:

* Number of pages, image resolution/complexity, chosen options (--optimize, \--clean), hardware (CPU, RAM, disk speed \- SSD \>\> HDD for temp files).  
* Expect seconds to minutes *per page*.  
* Optimization happens *after* OCR progress reaches 100%. Monitor system activity (htop) to ensure it's still working.

### **Input Image Quality: Garbage In, Garbage Out (GIGO)**

OCR accuracy depends heavily on image quality.

* **Resolution (DPI):** Aim for **300 DPI** for standard text. \<200 DPI hurts accuracy; \>600 DPI often gives diminishing returns.  
* **Clarity & Contrast:** Need sharp, clear text. Blurriness, low contrast, noise (speckles, bleed-through, shadows) degrade results.  
* **Scanning Best Practices:** Use a flatbed scanner, clean glass, lay pages flat/straight, use appropriate color mode (B\&W/Grayscale usually best for text), adjust scanner brightness/contrast *before* scanning.  
* **Pre-processing (Optional):** For poor quality images, *before* img2pdf, consider image editing tools:  
  * **ImageMagick:** convert in.jpg \-threshold 60% out.png (binarize), convert in.png \-level 10%,90% out.png (contrast), convert in.tif \-normalize out.tif (auto-contrast), convert in.jpg \-deskew 40% out.jpg.  
  * **GIMP:** Levels, Curves, Threshold, Despeckle filter.

### **Error Checking and Cleanup**

Verify success and handle failures gracefully.

**Common Errors Summary:**

| Error Message Snippet | Likely Cause(s) | Common Solution(s) |
| :---- | :---- | :---- |
| No space left on device | Temporary directory (/tmp or $TMPDIR) is full. | Set TMPDIR to a larger partition (see Disk Space section). |
| TesseractNotFoundError | Tesseract engine not installed or not in PATH. | Install tesseract-ocr via system package manager (esp. if used pip for ocrmypdf). |
| Language pack not found | Missing Tesseract language pack for specified \-l. | Install the required tesseract-ocr-\[lang\] pack via system package manager. |
| Permission denied | Cannot read input files or write output/temp files. | Check file/directory permissions (ls \-l, chmod, chown). |
| img2pdf: error: ... | Issue with input image (corrupt, unsupported format). | Try opening/resaving image; consider pre-conversion with ImageMagick. |
| ocrmypdf: error: ... | Various issues (see detailed logs/errors below). | Check command options, input file validity, resource usage. |

**Detailed Checks:**

* **Check Command Output:** Read all terminal warnings/errors carefully.  
* **Exit Codes:** Check status after command: echo $? (0 \= success, non-zero \= error).  
* **Failed Runs & Cleanup:** If ocrmypdf fails, manually delete temporary directories (rm \-rf /tmp/ocrmypdf\_\* or in $TMPDIR) to free space.  
* **Verification:** **Crucially, always open the final OCR'd PDF.** Test search, select/copy text, visually skim pages. Only delete originals/intermediates after verification.  
* **Common OCR Errors:** Expect imperfections (character confusion: l/1, O/0; merged/split words; issues with tables/fonts). Perfect accuracy is rare. Manual correction might be needed for critical documents.