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
"""
File Organizer
A Python utility that organizes files from a source directory into categorized 
folders in a target directory.
"""
import os
import shutil
import argparse
import json
from datetime import datetime
import platform

# Default categories configuration
DEFAULT_CATEGORIES_CONFIG = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "documents": [".pdf", ".docx", ".doc", ".txt", ".rtf", ".odt", ".xlsx", ".xls", ".csv", ".pptx", ".ppt"],
    "videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
    "audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "archives": [".zip", ".rar", ".tar", ".gz", ".bz2", ".7z"],
    "code": [".py", ".java", ".c", ".cpp", ".h", ".html", ".css", ".js", ".xml", ".json"],
    "apps": [".exe", ".msi", ".apk", ".dmg"],
    "other": []  # Default category for unknown extensions
}

def categorize_file_by_category(filename, categories_config):
    """
    Categorizes a file based on its extension and provided categories configuration.
    """
    _, extension = os.path.splitext(filename)
    extension = extension.lower()
    for category, extensions in categories_config.items():
        if extension in extensions:
            return category
    return "other"

def create_folders(directory, organize_by, categories_config=None):
    """
    Creates category or extension-based folders in the target directory.
    Useful if you wish to pre-generate folders prior to sorting.
    """
    if organize_by == 'category':
        for category in categories_config.keys():
            os.makedirs(os.path.join(directory, category), exist_ok=True)
    elif organize_by == 'extension':
        # Folders will be created dynamically in sort_files() as extensions are encountered
        pass
    else:
        raise ValueError("Invalid organize_by option. Choose 'category' or 'extension'.")

def handle_long_path(path):
    """
    Handles long paths on Windows by adding the \\?\ prefix if length exceeds 255 characters.
    """
    if platform.system() == "Windows" and len(path) > 255:
        return "\\\\?\\" + path
    return path

def sort_files(source_directory, target_directory, organize_by, use_timestamp, move_files, 
               categories_config, include_hidden, follow_links, skip_existing):
    """
    Sorts files from source to target directory based on the chosen organization method.
    """
    # Transform paths for Windows if necessary
    source_directory = handle_long_path(os.path.abspath(source_directory))
    target_directory = handle_long_path(os.path.abspath(target_directory))

    # Validate directories
    if not os.path.isdir(source_directory):
        print(f"Error: Source directory '{source_directory}' is not valid.")
        return
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
        print(f"Target directory '{target_directory}' created.")
    elif not os.path.isdir(target_directory):
        print(f"Error: Target directory '{target_directory}' is not valid.")
        return

    total_files = 0
    processed_files = 0

    # Traverse the source directory
    for root, dirs, files in os.walk(source_directory, followlinks=follow_links):
        # Skip hidden directories if include_hidden is false
        if not include_hidden:
            dirs[:] = [d for d in dirs if not d.startswith('.')]

        total_files += len(files)

        for filename in files:
            # Skip hidden files if include_hidden is false
            if not include_hidden and filename.startswith('.'):
                continue

            filepath = os.path.join(root, filename)

            # Determine the target folder based on organization method
            if organize_by == 'category':
                file_category = categorize_file_by_category(filename, categories_config)
                target_folder = os.path.join(target_directory, file_category)
            elif organize_by == 'extension':
                _, extension = os.path.splitext(filename)
                if not extension:
                    # Handle files without extension
                    target_folder = os.path.join(target_directory, "no_extension")
                else:
                    target_folder = os.path.join(target_directory, extension[1:].lower())
                os.makedirs(target_folder, exist_ok=True)
            else:
                raise ValueError("Invalid organize_by option.")

            # Build the final target path
            target_path = os.path.join(target_folder, filename)

            try:
                if os.path.exists(target_path):
                    if skip_existing:
                        # Skip if file already exists and skip_existing is true
                        print(f"Skipping '{filepath}' (already exists).")
                        processed_files += 1
                        continue
                    elif use_timestamp:
                        # If file exists and skip_existing is false, timestamp the new file
                        file_date = datetime.fromtimestamp(os.path.getmtime(filepath))
                        sanitized_date = file_date.isoformat().replace(":", "-")
                        _, ext = os.path.splitext(filename)
                        name_without_ext = filename[:-len(ext)] if ext else filename
                        new_filename = f"{sanitized_date}-{name_without_ext}{ext}"
                        target_path = os.path.join(target_folder, new_filename)

                # Move or copy the file
                if move_files:
                    shutil.move(filepath, target_path)
                    print(f"Moved '{filename}' to '{target_folder}'")
                else:
                    shutil.copy2(filepath, target_path)
                    print(f"Copied '{filename}' to '{target_folder}'")
            except Exception as e:
                print(f"Error processing '{filename}': {e}")
            finally:
                processed_files += 1
                print(f"Progress: {processed_files}/{total_files} files processed", end='\r')

    print("\nFile organization completed!")

def load_config_file(config_path):
    """
    Loads categories configuration from a JSON file.
    """
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Warning: Config file not found at '{config_path}'. Using default categories.")
        return DEFAULT_CATEGORIES_CONFIG
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{config_path}'. Using default categories.")
        return DEFAULT_CATEGORIES_CONFIG

def main():
    """
    Main function to parse command line arguments and begin file organization.
    """
    parser = argparse.ArgumentParser(
        description="Organize files by category or extension with optional timestamping and move features."
    )

    parser.add_argument("--source", "-s", required=True, 
                        help="Source directory containing files to organize.")
    parser.add_argument("--target", "-t", required=True, 
                        help="Target directory where files will be organized.")
    parser.add_argument("--organize-by", choices=["category", "extension"], default="category", 
                        help="Method to organize files (category or extension). Default is 'category'.")
    parser.add_argument("--no-timestamp", action="store_true", 
                        help="Disable timestamps for duplicate file naming.")
    parser.add_argument("--move", action="store_true", 
                        help="Move files instead of copying them.")
    parser.add_argument("--config", "-c", 
                        help="Path to a JSON configuration file defining categories.")
    parser.add_argument("-i", "--include_hidden", action="store_true", 
                        help="Include hidden files and directories.")
    parser.add_argument("-l", "--follow_links", action="store_true", 
                        help="Follow symbolic links in the source directory.")
    parser.add_argument("-sk", "--skip_existing", action="store_true", 
                        help="Skip existing files in the target directory instead of timestamping.")

    args = parser.parse_args()

    source_directory = args.source
    target_directory = args.target
    organize_by = args.organize_by
    use_timestamp = not args.no_timestamp
    move_files = args.move
    config_path = args.config
    include_hidden = args.include_hidden
    follow_links = args.follow_links
    skip_existing = args.skip_existing

    categories_config = DEFAULT_CATEGORIES_CONFIG
    if config_path:
        categories_config = load_config_file(config_path)
        print(f"Using custom categories from '{config_path}'")
    else:
        print("Using default categories.")

    # Optionally call create_folders() if needed:
    # create_folders(target_directory, organize_by, categories_config)

    sort_files(source_directory, target_directory, organize_by, use_timestamp, move_files, 
               categories_config, include_hidden, follow_links, skip_existing)

if __name__ == "__main__":
    main()
{% endcodeblock %}
