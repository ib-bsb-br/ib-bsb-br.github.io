---
title: Organize files by their extensions
date: 2024-05-30
tags: [scripts>python]
info: aberto.
type: post
layout: post
---

# File Organizer Documentation

A Python utility for organizing files from source directories into categorized target folders.

## Project Overview

### Purpose
This utility solves the problem of disorganized file directories by automatically sorting files based on their types or extensions. It addresses common issues like:

- Mixed file types in download or document folders
- Difficulty finding specific file types
- Managing large collections of files
- Batch organizing files while preserving their content and metadata

### Core Functionality
- Sort files by predefined categories (images, documents, etc.)
- Sort files by their extensions
- Copy or move files from source to destination
- Handle duplicate filenames
- Process hidden files and follow symbolic links if requested
- Track progress during file operations

### Design Principles
1. **Configurability:** Users can customize how files are categorized
2. **Reliability:** Careful handling of edge cases like duplicates and long paths
3. **Transparency:** Clear feedback on what's happening during operation
4. **Simplicity:** Straightforward command-line interface

## Installation

The utility requires only Python standard library modules and no external dependencies.

1. Download the script:
```bash
curl -O https://example.com/file_organizer.py
# or
wget https://example.com/file_organizer.py
```

2. Make the script executable (Linux/macOS):
```bash
chmod +x file_organizer.py
```

## Usage

### Basic Command Structure

```bash
python file_organizer.py --source <source_directory> --target <target_directory> [options]
```

### Command Line Options

| Option | Description |
|--------|-------------|
| --source, -s | Source directory to organize files from (required) |
| --target, -t | Target directory to organize files into (required) |
| --organize-by | Organization method: 'category' or 'extension' (default: 'category') |
| --no-timestamp | Disable adding timestamps to duplicate filenames |
| --move | Move files instead of copying them |
| --config, -c | Path to a JSON configuration file for custom categories |
| -i, --include_hidden | Include hidden files and directories |
| -l, --follow_links | Follow symbolic links during directory traversal |
| -sk, --skip_existing | Skip existing files instead of timestamping |

## Configuration

### Default Categories

The utility uses these default file categories:

| Category | File Extensions |
|----------|----------------|
| images | .jpg, .jpeg, .png, .gif, .bmp, .webp |
| documents | .pdf, .docx, .doc, .txt, .rtf, .odt, .xlsx, .xls, .csv, .pptx, .ppt |
| videos | .mp4, .avi, .mkv, .mov, .wmv, .flv |
| audio | .mp3, .wav, .flac, .aac, .ogg, .m4a |
| archives | .zip, .rar, .tar, .gz, .bz2, .7z |
| code | .py, .java, .c, .cpp, .h, .html, .css, .js, .xml, .json |
| apps | .exe, .msi, .apk, .dmg |
| other | Any file extension not listed above |

### Custom Categories

You can define your own categories using a JSON configuration file:

```json
{
  "category_name1": [".ext1", ".ext2"],
  "category_name2": [".ext3", ".ext4"],
  "other": []
}
```

Example custom config file:

```json
{
  "work": [".doc", ".docx", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"],
  "photos": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
  "code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".h"],
  "media": [".mp3", ".mp4", ".avi", ".mkv", ".mov", ".flac", ".wav"],
  "compressed": [".zip", ".rar", ".tar", ".gz", ".7z"],
  "other": []
}
```

## Examples

1. **Basic organization by category:**
   ```bash
   python file_organizer.py --source ~/Downloads --target ~/Organized
   ```

2. **Organize by file extension:**
   ```bash
   python file_organizer.py --source ~/Downloads --target ~/Organized --organize-by extension
   ```

3. **Move files instead of copying:**
   ```bash
   python file_organizer.py --source ~/Downloads --target ~/Organized --move
   ```

4. **Skip duplicate files instead of timestamping:**
   ```bash
   python file_organizer.py --source ~/Downloads --target ~/Organized --skip_existing
   ```

5. **Include hidden files and follow symbolic links:**
   ```bash
   python file_organizer.py --source ~/Downloads --target ~/Organized --include_hidden --follow_links
   ```

## Troubleshooting

### Permission Errors
- Ensure you have read permissions for the source directory
- Ensure you have write permissions for the target directory
- On Unix systems, run with sudo for system directories (use with caution)

### Long Paths on Windows
The utility automatically handles long paths (>255 characters) on Windows by prefixing with `\\?\`. If you still encounter issues:
- Use shorter directory names
- Move files to a less deeply nested location before organizing

### Performance with Large Directories
- For very large directories (thousands of files), the initial scan may take time
- Consider organizing subdirectories separately if performance is an issue

### Duplicate Files
When a file with the same name exists in the target directory:

1. Default behavior: Add timestamp to filename
2. With `--skip_existing`: Skip the file
3. With `--no-timestamp`: Overwrite existing file (use with caution)

## Development Notes

### Design Decisions

1. **File Operations (Copy vs. Move)**
   - Copy is the default to prevent accidental data loss
   - Move functionality provided for efficiency when source files aren't needed

2. **Categorization System**
   - Default categories cover common file types
   - Custom categories supported via JSON for flexibility
   - Extension-based organization added for users who prefer that system

3. **Handling Duplicates**
   - Timestamp approach preserves both old and new files
   - Skip option added for incremental organization tasks

4. **Error Handling**
   - Individual file errors don't halt the entire process
   - Errors are reported but the utility continues processing other files

### Error Handling Strategy

The utility employs an "attempt and continue" error handling strategy:
- Each file operation is wrapped in a try/except block
- Errors with individual files are reported but don't stop the overall process
- This ensures maximum files are processed even if some cause issues

### Security Considerations

1. **File Operations**
   - The utility doesn't attempt to open or read file contents (only metadata)
   - No execution of files occurs during organization
   
2. **When Using Move Operations**
   - Be aware that move operations permanently change your file system
   - Always verify the target directory before using --move

## Testing

Refer to [TESTING.md](TESTING.md) for detailed testing procedures and scenarios.

# Testing the File Organizer

This document outlines procedures for testing the File Organizer utility to ensure it functions correctly.

## Test Environment Setup

Create a test directory structure with various file types:

```bash
# Create test directories
mkdir -p test_environment/source
mkdir -p test_environment/target

# Create test files
touch test_environment/source/document1.pdf
touch test_environment/source/document2.docx
touch test_environment/source/image1.jpg
touch test_environment/source/image2.png
touch test_environment/source/video1.mp4
touch test_environment/source/script.py
touch test_environment/source/archive.zip
touch test_environment/source/noextension
touch test_environment/source/.hidden_file

# Create subdirectory with more files
mkdir -p test_environment/source/subdir
touch test_environment/source/subdir/nested_doc.pdf
touch test_environment/source/subdir/nested_image.jpg
```

## Test Cases

### Test Case 1: Basic Category Organization

**Purpose:** Verify that files are correctly organized into category folders

**Command:**
```bash
python file_organizer.py --source test_environment/source --target test_environment/target
```

**Expected Results:**
- Target directory should contain category folders: documents, images, videos, code, archives, other
- Files should be placed in their correct category folders:
  - documents: document1.pdf, document2.docx
  - images: image1.jpg, image2.png
  - videos: video1.mp4
  - code: script.py
  - archives: archive.zip
  - other: noextension
- Hidden files should be skipped (.hidden_file)
- All files should be copied, not moved (source files should still exist)

**Verification:**
```bash
ls -la test_environment/target/*/
ls -la test_environment/source/
```

### Test Case 2: Extension-based Organization

**Purpose:** Verify that files are correctly organized by their extensions

**Command:**
```bash
python file_organizer.py --source test_environment/source --target test_environment/target --organize-by extension
```

**Expected Results:**
- Target directory should contain extension folders: pdf, docx, jpg, png, mp4, py, zip, no_extension
- Files should be placed in their respective extension folders
- Files without extension should be in the no_extension folder
- All files should be copied, not moved

**Verification:**
```bash
ls -la test_environment/target/*/
```

### Test Case 3: Move Operation

**Purpose:** Verify that files are moved instead of copied when using the --move flag

**Command:**
```bash
python file_organizer.py --source test_environment/source --target test_environment/target --move
```

**Expected Results:**
- Files should be moved to their category folders in the target directory
- Source directory should no longer contain the moved files
- Subdirectories in source should remain (unless empty on your OS)

**Verification:**
```bash
ls -la test_environment/source/
ls -la test_environment/target/*/
```

### Test Case 4: Duplicate File Handling with Timestamps

**Purpose:** Verify that duplicate files are handled correctly with timestamps

**Preparation:**
```bash
# Create duplicate file in target
mkdir -p test_environment/target/documents
cp test_environment/source/document1.pdf test_environment/target/documents/
```

**Command:**
```bash
python file_organizer.py --source test_environment/source --target test_environment/target
```

**Expected Results:**
- document1.pdf should be copied with a timestamp in the name (e.g., 2023-01-01T12-30-45-document1.pdf)
- Original document1.pdf should remain unchanged in target directory
- Console output should indicate that a timestamp was added

**Verification:**
```bash
ls -la test_environment/target/documents/
```

### Test Case 5: Skip Existing Files

**Purpose:** Verify that existing files are skipped with the --skip_existing flag

**Command:**
```bash
python file_organizer.py --source test_environment/source --target test_environment/target --skip_existing
```

**Expected Results:**
- document1.pdf should be skipped (not copied again)
- Console output should indicate that document1.pdf was skipped
- Other files should be processed normally

**Verification:**
```bash
# Only one document1.pdf should exist in the target
ls -la test_environment/target/documents/
```

### Test Case 6: Include Hidden Files

**Purpose:** Verify that hidden files are processed when using the --include_hidden flag

**Command:**
```bash
python file_organizer.py --source test_environment/source --target test_environment/target --include_hidden
```

**Expected Results:**
- .hidden_file should be processed and copied to the "other" category
- Console output should indicate that .hidden_file was processed

**Verification:**
```bash
ls -la test_environment/target/other/
```

### Test Case 7: Custom Categories

**Purpose:** Verify that custom category configurations work correctly

**Preparation:**
```bash
# Create a custom config file
cat > test_environment/custom_config.json << EOF
{
  "text_files": [".pdf", ".docx", ".txt"],
  "media": [".jpg", ".png", ".mp4"],
  "code_files": [".py", ".js", ".html"],
  "other": []
}
EOF
```

**Command:**
```bash
python file_organizer.py --source test_environment/source --target test_environment/target --config test_environment/custom_config.json
```

**Expected Results:**
- Files should be organized according to the custom categories:
  - text_files: document1.pdf, document2.docx
  - media: image1.jpg, image2.png, video1.mp4
  - code_files: script.py
  - other: archive.zip, noextension
- Console output should indicate custom categories are being used

**Verification:**
```bash
ls -la test_environment/target/*/
```

## Test Result Interpretation

Each test case should result in files being organized according to the expected results. If any test fails:

1. Check console output for error messages
2. Verify file permissions in source and target directories
3. Ensure test environment was set up correctly
4. Check if target directories were created as expected
5. Verify file contents to ensure they weren't corrupted during copy/move

## Cleanup

After testing, remove the test environment:

```bash
rm -rf test_environment
```

## Example config

```json
{
  "work": [".doc", ".docx", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"],
  "photos": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
  "code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".h"],
  "media": [".mp3", ".mp4", ".avi", ".mkv", ".mov", ".flac", ".wav"],
  "compressed": [".zip", ".rar", ".tar", ".gz", ".7z"],
  "other": []
}
```

# Maintenance Guide for File Organizer

This document provides guidelines for maintaining and extending the File Organizer utility. It is designed for developers who may be unfamiliar with the original implementation but need to maintain or enhance the codebase.

## Project Structure

The File Organizer consists of:

- `file_organizer.py`: Main script containing all functionality
- Configuration files: JSON files that define custom category mappings

## Code Architecture

The utility follows a simple procedural design with these core components:

1. **Argument Parsing**: Uses `argparse` to process command-line options
2. **Configuration Management**: Loads and validates category definitions
3. **File Processing**: Traverses directories and processes files
4. **File Operations**: Handles copying, moving, and naming of files

## Key Functions

| Function | Purpose | Implementation Notes |
|----------|---------|---------------------|
| `categorize_file_by_category()` | Maps files to categories | Performs simple extension lookup |
| `create_folders()` | Prepares target directory structure | Creates folders only when needed for 'category' mode |
| `handle_long_path()` | Handles Windows path limitations | Windows-specific fix for paths >255 chars |
| `sort_files()` | Main file processing logic | Contains the core logic and most complex function |
| `load_config_file()` | Loads custom category definitions | Includes fallback to defaults on error |
| `main()` | Entry point and argument processing | Sets up and initiates the process |

## Causality Chain

Understanding why certain implementation choices were made:

1. **Why copy files by default?**
   - To prevent accidental data loss
   - Move operation is available but requires explicit flag

2. **Why use timestamps for duplicates?**
   - Preserves both original and new files
   - Maintains file history
   - Prevents unintentional overwrites

3. **Why separate extension handling?**
   - Some users prefer organization by extension
   - Provides flexibility for different workflows

4. **Why include Windows long path handling?**
   - Windows has a 255 character path limitation
   - Without this, deeply nested files would fail to process

## Common Maintenance Tasks

### Adding New File Categories

To add new categories to the default configuration:

1. Modify the `DEFAULT_CATEGORIES_CONFIG` dictionary:
```python
DEFAULT_CATEGORIES_CONFIG = {
    # Existing categories...
    "new_category": [".ext1", ".ext2", ".ext3"],
    "other": []  # Always keep this as the fallback
}
```

### Adding New Command Line Options

To add a new command line option:

1. Add the option to the argument parser in `main()`:
```python
parser.add_argument('--new-option', action='store_true', 
                  help='Description of the new option')
```

2. Extract the option value:
```python
new_option = args.new_option
```

3. Pass the option to functions that need it:
```python
sort_files(..., new_option, ...)
```

4. Update the function signatures and implementations to use the new option

### Error Handling

The current error handling strategy is:
- Individual file errors are caught and reported
- The process continues with the next file
- Overall process doesn't terminate on individual file errors

When adding new functionality, maintain this pattern:

```python
try:
    # Your operation here
except Exception as e:
    print(f"Error: {e}")
    # Continue with next item rather than raising
```

## Testing

When making changes, ensure you test:

1. Basic functionality with default options
2. Any specific options you've modified
3. Edge cases like:
   - Empty directories
   - Files with unusual names or extremely long paths
   - Very large directories
   - Permission-restricted files

Follow the testing guide in TESTING.md to verify your changes.

## Performance Considerations

The utility was designed for moderate-sized directories. For very large directories (thousands of files), consider:

1. Adding progress indicators for lengthy operations
2. Implementing batch processing
3. Adding resume capabilities for interrupted operations

## Security Considerations

When modifying the code, maintain these security principles:

1. Never execute file contents
2. Validate all user inputs, especially paths and configuration files
3. Be careful with move operations that permanently alter file systems
4. Maintain appropriate error handling to prevent information leakage

## Documentation Updates

When changing functionality, update these documentation components:

1. Function docstrings in the code
2. README.md for user-facing changes
3. MAINTENANCE.md for developer-facing changes
4. TESTING.md for new test cases
```

# Decision Record and Implementation Notes

## Key Design Decisions

### 1. File Organization Approach
**Decision:** Implement two organization methods (category and extension)  
**Context:** Different users have different preferences for file organization  
**Consequences:** More flexible tool but more complex implementation and testing required

### 2. Default Copy vs. Move
**Decision:** Make copy the default operation and move optional  
**Context:** Moving files is destructive and could lead to data loss if not used carefully  
**Consequences:** Safer operation but may require more disk space temporarily

### 3. Duplicate File Handling
**Decision:** Implemented three strategies: timestamp, skip, or overwrite  
**Context:** Users need different approaches based on their specific use cases  
**Consequences:** More complexity but greater flexibility for different scenarios

### 4. Error Handling Strategy
**Decision:** Catch and report individual file errors but continue processing  
**Context:** A single problematic file shouldn't prevent organizing all other files  
**Consequences:** More robust operation but may mask underlying issues

### 5. Custom Configuration System
**Decision:** Use JSON for category definitions  
**Context:** Provides flexibility while using a standard format  
**Consequences:** Requires error handling for invalid JSON but enables easy customization

## Implementation Notes

### Platform Compatibility
- Windows long path handling was added specifically to address the 255-character path limit
- The utility uses path handling that works across Windows, macOS, and Linux
- File metadata preservation is implemented using `shutil.copy2()` instead of regular copy

### Progress Reporting
- Real-time progress updates were implemented to provide feedback during long operations
- The counter system shows both files processed and total files for context

### Security Considerations
- The tool only examines file metadata, not contents
- No execution of files occurs during the organization process
- User input validation is performed for all paths and configuration options

### Performance Optimization
- Directory walking is optimized by filtering directories early when hidden files are excluded
- Folders are created only as needed in extension mode to minimize filesystem operations

### Maintenance Approach
- Code is documented thoroughly for third-party maintenance
- Functions have clear purposes and interfaces
- Error handling is consistent across the codebase
- Testing procedures cover both common and edge cases

## Third-Party Maintenance Guidelines

For developers maintaining this code:

1. **Understanding the Core Logic**: 
   - The main functionality is in the `sort_files()` function
   - File categorization happens in `categorize_file_by_category()`
   - Configuration loading is handled by `load_config_file()`

2. **Adding New Features**:
   - Maintain the existing error handling pattern
   - Document all changes thoroughly
   - Update tests to cover new functionality
   - Consider backward compatibility

3. **Fixing Issues**:
   - Check for edge cases with unusual filenames or paths
   - Verify platform-specific behavior (especially Windows long paths)
   - Test with large directories and various file types

4. **Refactoring Guidelines**:
   - Maintain clear function purposes
   - Preserve the current error handling strategy
   - Ensure backward compatibility
   - Update documentation to reflect changes

# Python script code

{% codeblock python %}
#!/usr/bin/env python3
import os
import shutil
import argparse
import json
import platform
import traceback
import logging
from datetime import datetime

# --- Default Configuration ---
DEFAULT_CATEGORIES_CONFIG = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".svg", ".ico"],
    "documents": [".pdf", ".docx", ".doc", ".txt", ".rtf", ".odt", ".xlsx", ".xls", ".csv", ".pptx", ".ppt", ".md", ".tex", ".chm", ".epub"],
    "videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
    "audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "archives": [".zip", ".rar", ".tar", ".gz", ".bz2", ".7z", ".iso"],
    "code": [".py", ".java", ".c", ".cpp", ".h", ".cs", ".html", ".css", ".js", ".ts", ".jsx", ".tsx", ".xml", ".json", ".yaml", ".yml", ".sh", ".bat", ".ps1", ".rb", ".php", ".go", ".rs", ".swift", ".kt", ".ipynb", ".sql", ".toml"],
    "apps": [".exe", ".msi", ".apk", ".dmg", ".deb", ".rpm", ".app"],
    "fonts": [".ttf", ".otf", ".woff", ".woff2"],
    "shortcuts": [".lnk", ".url"],
    "other": []
}

# --- Utility Functions ---

def setup_logging(log_file_path=None):
    """Configures logging to console and optionally to a file."""
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('file_organizer')
    logger.setLevel(logging.INFO) # Set base level

    # Console Handler (prints INFO and above)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    # File Handler (prints INFO and above if path provided)
    if log_file_path:
        try:
            file_handler = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
            file_handler.setFormatter(log_formatter)
            logger.addHandler(file_handler)
            logger.info(f"Logging initialized. Log file: {log_file_path}")
        except Exception as e:
            logger.error(f"Failed to initialize log file handler at {log_file_path}: {e}")

    return logger

def handle_long_path(path):
    """Prepends the long path prefix for Windows if necessary."""
    path = os.path.abspath(path)
    if platform.system() == "Windows" and len(path) > 259 and not path.startswith("\\\\?\\"):
        path = "\\\\?\\" + path
    return path

def load_config_file(config_path, logger):
    """Loads category configuration from a JSON file."""
    if config_path and os.path.isfile(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                logger.info(f"Loading category configuration from: {config_path}")
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"Could not load or parse config file '{config_path}': {e}. Using default categories.")
    else:
        logger.info("Using default category configuration.")
    return DEFAULT_CATEGORIES_CONFIG

def categorize_file(filename, categories_config):
    """Determines the category of a file based on its extension."""
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    if not ext:
        return "no_extension"
    for category, extensions in categories_config.items():
        if ext in extensions:
            return category
    return "other"

def is_hidden_windows(filepath):
    """Checks if a file or directory is hidden on Windows."""
    if platform.system() != "Windows":
        return False
    try:
        attrs = os.stat(filepath).st_file_attributes
        return attrs & 2 # FILE_ATTRIBUTE_HIDDEN = 2
    except OSError:
        return False # Assume not hidden if stat fails

def create_target_folders(base_dir, organize_by, categories_config, all_extensions, logger):
    """Creates necessary target folders before processing files."""
    base_dir = handle_long_path(base_dir)
    logger.info(f"Ensuring target base directory exists: {base_dir}")
    os.makedirs(base_dir, exist_ok=True) # Ensure base exists first

    folders_to_create = set()
    if organize_by == "category":
        folders_to_create = set(categories_config.keys()) | {"other", "no_extension"}
    elif organize_by == "extension":
        folders_to_create = all_extensions | {"no_extension"}
    else:
        logger.error(f"Invalid organize_by option: {organize_by}")
        raise ValueError("Invalid organize_by option.")

    logger.info(f"Creating target subfolders ({organize_by})...")
    created_count = 0
    for folder_name in folders_to_create:
        folder_path = os.path.join(base_dir, folder_name)
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path, exist_ok=True)
                created_count += 1
            except OSError as e:
                 logger.error(f"Failed to create target folder '{folder_path}': {e}")
    logger.info(f"Created {created_count} new target subfolders.")


def get_all_extensions(source_directory, include_hidden, follow_links, logger):
    """Scans the source directory to find all unique file extensions."""
    extensions = set()
    source_directory = handle_long_path(source_directory)
    logger.info("Scanning for all unique file extensions...")
    count = 0
    for root, dirs, files in os.walk(source_directory, followlinks=follow_links):
        root_path = handle_long_path(root)
        if not include_hidden:
            dirs[:] = [d for d in dirs if not d.startswith('.') and not is_hidden_windows(os.path.join(root_path, d))]
            files = [f for f in files if not f.startswith('.') and not is_hidden_windows(os.path.join(root_path, f))]

        for file in files:
            count +=1
            _, ext = os.path.splitext(file)
            if ext:
                extensions.add(ext[1:].lower())
            if count % 1000 == 0: # Log progress for large scans
                 logger.info(f"Scanned {count} files for extensions...")

    logger.info(f"Found {len(extensions)} unique extensions.")
    return extensions


# --- Core Logic ---

def sort_files(
    source_directory,
    target_directory,
    organize_by,
    timestamp_duplicates,
    move_files,
    categories_config,
    include_hidden,
    follow_links,
    skip_existing,
    logger
):
    """Sorts files from source to target directory based on specified options."""
    source_directory = handle_long_path(source_directory)
    target_directory = handle_long_path(target_directory)

    if not os.path.isdir(source_directory):
        logger.error(f"Source directory '{source_directory}' is invalid or not found.")
        return 0, 0

    if not os.path.exists(target_directory):
        try:
            os.makedirs(target_directory)
            logger.info(f"Created target directory: {target_directory}")
        except OSError as e:
            logger.error(f"Could not create target directory '{target_directory}': {e}")
            return 0, 0
    elif not os.path.isdir(target_directory):
        logger.error(f"Target path '{target_directory}' exists but is not a directory.")
        return 0, 0

    # --- Pre-scan and Folder Creation ---
    total_files = 0
    files_to_process = []
    logger.info("Scanning source directory to count files...")
    for root, dirs, files in os.walk(source_directory, topdown=True, followlinks=follow_links):
        root_path = handle_long_path(root)
        original_dirs = list(dirs) # Keep original list for iteration if needed
        if not include_hidden:
            dirs[:] = [d for d in dirs if not d.startswith('.') and not is_hidden_windows(os.path.join(root_path, d))]
            files = [f for f in files if not f.startswith('.') and not is_hidden_windows(os.path.join(root_path, f))]

        for file in files:
            filepath = os.path.join(root_path, file)
            # Basic check if it's actually a file before adding
            try:
                 if os.path.isfile(filepath):
                      files_to_process.append(filepath)
                      total_files += 1
                 else:
                      logger.warning(f"Item listed as file is not a file (skipping count): {filepath}")
            except OSError as e:
                 logger.warning(f"Could not access item during scan (skipping count): {filepath} - Error: {e}")


    logger.info(f"Found {total_files} files to process.")
    if total_files == 0:
        logger.info("No files found to process.")
        return 0, 0

    if organize_by == "category":
        create_target_folders(target_directory, "category", categories_config, None, logger)
    elif organize_by == "extension":
        all_exts = get_all_extensions(source_directory, include_hidden, follow_links, logger)
        create_target_folders(target_directory, "extension", None, all_exts, logger)

    # --- Process Files ---
    processed_files = 0
    skipped_files = 0
    error_files = 0
    logger.info("Starting file processing...")

    for i, filepath in enumerate(files_to_process):
        filepath = handle_long_path(filepath)
        file = os.path.basename(filepath)
        progress_prefix = f"[{i+1}/{total_files}]"

        try:
            if not os.path.exists(filepath): # Re-check existence before processing
                logger.warning(f"{progress_prefix} Skipping non-existent source file: {filepath}")
                skipped_files += 1
                continue
            if not os.path.isfile(filepath): # Ensure it's still a file
                logger.warning(f"{progress_prefix} Skipping item that is not a file: {filepath}")
                skipped_files += 1
                continue

            # Determine target folder
            if organize_by == "category":
                category = categorize_file(file, categories_config)
                target_folder = os.path.join(target_directory, category)
            elif organize_by == "extension":
                _, ext = os.path.splitext(file)
                ext_folder = ext[1:].lower() if ext else "no_extension"
                target_folder = os.path.join(target_directory, ext_folder)
            else: # Should not happen
                 logger.error(f"{progress_prefix} Invalid organization option for file {file}. Skipping.")
                 error_files += 1
                 continue

            target_fullpath = os.path.join(target_folder, file)
            target_fullpath = handle_long_path(target_fullpath)

            # Handle existing target files
            if os.path.exists(target_fullpath):
                if skip_existing:
                    logger.info(f"{progress_prefix} Skipping existing target: {target_fullpath}")
                    skipped_files += 1
                    continue
                elif timestamp_duplicates:
                    counter = 1
                    base, ext = os.path.splitext(file)
                    original_target_fullpath = target_fullpath # Store for logging
                    while os.path.exists(target_fullpath):
                        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        new_name = f"{base}_{stamp}_{counter}{ext}"
                        target_fullpath = os.path.join(target_folder, new_name)
                        target_fullpath = handle_long_path(target_fullpath)
                        counter += 1
                    logger.info(f"{progress_prefix} Target exists '{original_target_fullpath}'. Renaming duplicate to: {target_fullpath}")
                else:
                    logger.warning(f"{progress_prefix} Overwriting existing target file: {target_fullpath}")
                    # Overwrite happens implicitly

            # Perform file operation
            try:
                if move_files:
                    shutil.move(filepath, target_fullpath)
                    # logger.info(f"{progress_prefix} Moved: {file} -> {target_folder}") # Verbose
                else:
                    shutil.copy2(filepath, target_fullpath) # copy2 preserves metadata
                    # logger.info(f"{progress_prefix} Copied: {file} -> {target_folder}") # Verbose
                processed_files += 1
            except (OSError, shutil.Error) as e: # Catch specific shutil errors too
                logger.error(f"{progress_prefix} Failed to {'move' if move_files else 'copy'} '{filepath}' to '{target_fullpath}': {e}")
                error_files += 1
            except Exception as e: # Catch any other unexpected error during file op
                 logger.error(f"{progress_prefix} Unexpected error processing '{filepath}' -> '{target_fullpath}': {e}", exc_info=True) # Log traceback
                 error_files += 1

        except Exception as e: # Catch errors during path manipulation, categorization etc.
            logger.error(f"{progress_prefix} Unexpected error processing path '{filepath}': {e}", exc_info=True)
            error_files += 1

        # Optional: Print live progress to console (can be noisy)
        # print(f"Progress: {i+1}/{total_files} (P: {processed_files}, S: {skipped_files}, E: {error_files})", end="\r")


    # Final Summary
    summary = f"File organization completed. Processed: {processed_files}, Skipped: {skipped_files}, Errors: {error_files}"
    logger.info(summary)
    print(f"\n{summary}") # Also print final summary to console
    return processed_files, skipped_files + error_files

def remove_empty_folders(directory, logger):
    """Recursively removes empty folders starting from the bottom up."""
    directory = handle_long_path(directory)
    removed_count = 0
    logger.info(f"Attempting to remove empty directories from: {directory}")
    # Walk from bottom up
    for root, dirs, files in os.walk(directory, topdown=False):
        root_path = handle_long_path(root)
        # Consider hidden status if needed, but generally just check emptiness
        if not files and not dirs: # Directory is empty
            try:
                os.rmdir(root_path)
                logger.info(f"Removed empty directory: {root_path}")
                removed_count += 1
            except OSError as e:
                # Common errors: permission denied, directory not empty (race condition?)
                logger.warning(f"Could not remove directory '{root_path}': {e}")
            except Exception as e:
                 logger.error(f"Unexpected error removing directory '{root_path}': {e}", exc_info=True)

    logger.info(f"Finished removing empty directories. Removed: {removed_count}")


# --- Main Execution ---

def main():
    parser = argparse.ArgumentParser(
        description="Organize files by category or extension.",
        formatter_class=argparse.RawTextHelpFormatter
        )
    parser.add_argument("--source", "-s", required=True, help="Source directory containing files to organize.")
    parser.add_argument("--target", "-t", required=True, help="Target directory where organized files will be placed.")
    parser.add_argument("--config", "-c", help="Path to JSON config file for custom file categories and extensions.")
    parser.add_argument(
        "--organize-by", choices=["category", "extension"], default="category",
        help="Method for organizing files:\n"
             "  category: Group into folders based on categories (default).\n"
             "  extension: Group into folders named after file extensions."
        )
    parser.add_argument("--move", action="store_true", help="Move files instead of copying them.")
    parser.add_argument("--timestamp-duplicates", action="store_true", help="Append timestamp+counter to duplicate filenames instead of overwriting/skipping.")
    parser.add_argument("--skip-existing", action="store_true", help="Skip processing if a file with the same name exists in the target.")
    parser.add_argument("--include-hidden", action="store_true", help="Include hidden files/folders (e.g., starting with '.') in processing.")
    parser.add_argument("--follow-links", action="store_true", help="Follow symbolic links (process target, not link). Use with caution (potential loops).")
    parser.add_argument("--remove-empty-source-dirs", action="store_true", help="After moving (--move must be enabled), attempt to remove empty source directories.")
    parser.add_argument("--log-file", help="Optional path to a file for logging progress and errors.")

    args = parser.parse_args()

    # --- Argument Validation ---
    if args.timestamp_duplicates and args.skip_existing:
        parser.error("--timestamp-duplicates and --skip-existing cannot be used together.")
    if args.remove_empty_source_dirs and not args.move:
        parser.error("--remove-empty-source-dirs requires --move to be enabled.")

    # --- Setup ---
    logger = setup_logging(args.log_file)
    logger.info("Script starting...")
    logger.info(f"Arguments: {vars(args)}") # Log arguments used

    categories = load_config_file(args.config, logger)

    # --- Execute Sorting ---
    processed, failed_or_skipped = sort_files(
        source_directory=args.source,
        target_directory=args.target,
        organize_by=args.organize_by,
        timestamp_duplicates=args.timestamp_duplicates,
        move_files=args.move,
        categories_config=categories,
        include_hidden=args.include_hidden,
        follow_links=args.follow_links,
        skip_existing=args.skip_existing,
        logger=logger
    )

    # --- Optional Cleanup ---
    if args.move and args.remove_empty_source_dirs and processed > 0:
        remove_empty_folders(args.source, logger)

    logger.info("Script finished.")
    print("\nScript finished. Check console and log file (if specified) for details.")

if __name__ == "__main__":
    main()
{% endcodeblock %}
