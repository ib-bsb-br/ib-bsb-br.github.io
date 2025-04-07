---
title: Organize files by type
date: 2024-05-30
tags: [scripts>rust]
info: aberto.
type: post
layout: post
---

# Building and Running the File Organizer on Windows

## Prerequisites

Before you begin, you need to install Rust:

1. Visit [https://rustup.rs/](https://rustup.rs/) to download the Rust installer
2. Run the installer to set up:
   - `rustc` (the compiler)
   - `cargo` (the build tool and package manager)

## Creating the Project

Open a command prompt and run:

```bash
# Create a new Rust project
cargo new file_organizer_rs
cd file_organizer_rs

# Replace default files with project files
# Replace the contents of Cargo.toml with the provided configuration
# Replace the contents of src/main.rs with the provided source code
```

## Building the Project

### Debug Build (For Development)

```bash
cargo build
```

The executable will be created in the `target/debug/` directory.

### Release Build (For Distribution)

For a smaller, optimized executable:

```bash
cargo build --release
```

The executable will be created in the `target/release/` directory.

## Running the Tool

### Getting Help

View all available options:

```bash
.\target\release\file_organizer_rs.exe --help
```

### Usage Examples

#### Basic File Organization

Copy files by category from Downloads to an organized folder:

```bash
.\target\debug\file_organizer_rs.exe --source C:\Users\YourUser\Downloads --target C:\OrganizedFiles
```

#### Moving Files with Duplicate Handling

Move files from Downloads, adding timestamps to duplicates:

```bash
.\target\debug\file_organizer_rs.exe --source C:\Users\YourUser\Downloads --target C:\OrganizedFiles --move --timestamp-duplicates
```

#### Organizing by File Extension

Organize files by extension, including hidden files:

```bash
.\target\release\file_organizer_rs.exe -s "C:\Path\To\Source" -t "C:\Path\To\Target" --organize-by extension --include-hidden
```

#### Advanced Configuration

Use a custom configuration file and log all activity:

```bash
.\target\release\file_organizer_rs.exe -s .\input -t .\output -c .\my_config.json --log-file activity.log --overwrite
```

## Common Options Reference

| Option | Short | Description |
|--------|-------|-------------|
| `--source` | `-s` | Source directory to organize files from |
| `--target` | `-t` | Target directory to place organized files |
| `--move` | | Move files instead of copying them |
| `--organize-by` | | Organization method (extension or category) |
| `--timestamp-duplicates` | | Add timestamp to duplicate files |
| `--include-hidden` | `-i` | Include hidden files and directories |
| `--overwrite` | | Overwrite existing files in target |
| `--config` | `-c` | Path to custom configuration file |
| `--log-file` | | Write logs to specified file |

## Testing Your Installation

After building, verify your installation works by running a simple test:

```bash
# Create test directories
mkdir test_source test_target

# Copy some test files to test_source
# Then run the organizer
.\target\debug\file_organizer_rs.exe -s .\test_source -t .\test_target
```

```toml
# Cargo.toml (Fixed fern feature)
[package]
name = "rust_file_organizer"
version = "0.1.0"
edition = "2021"
description = "A Rust utility for organizing files by category or extension."
authors = ["AI Assistant"] # Replace with actual author
license = "MIT OR Apache-2.0" # Choose appropriate license

[dependencies]
# Command-line argument parsing
clap = { version = "4.5", features = ["derive", "cargo", "env"] } # cargo/env features allow reading from Cargo.toml/env vars

# Directory traversal
walkdir = "2.5"

# JSON parsing for configuration files
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"

# Logging framework
log = "0.4"
# Using fern for flexible file/console logging setup
# **Fix:** Enable the 'colored' feature for fern
fern = { version = "0.6", features = ["colored"] }

# Date and time handling for timestamps
chrono = "0.4"

# Flexible error handling and context reporting
anyhow = "1.0"

# Optional: More robust file operations (especially cross-device move)
# fs_extra = "1.3" # Keep commented unless needed; std lib fallback implemented

# Windows-specific dependencies are NOT needed here as std lib is used for hidden check
# [target.'cfg(windows)'.dependencies]
# windows = { version = "0.56", features = [...] }

# Release profile optimizations (optional but recommended for smaller/faster executables)
[profile.release]
# 'z' optimizes aggressively for size, potentially sacrificing some speed compared to 's' or '3'.
opt-level = 'z'
# Enable Link-Time Optimization across crates for potential performance gains and size reduction.
lto = true
# Maximize optimization opportunities by using a single codegen unit (can significantly increase compile times).
codegen-units = 1
# Remove symbols from the binary for smaller size.
# Alternatively, use `cargo strip` (requires `cargo install cargo-strip`) or set `debuginfo = 0` (removes debug symbols only).
strip = true
# Abort on panic instead of unwinding the stack. Reduces binary size but prevents catching panics.
panic = 'abort'
```

{% codeblock rust %}

// src/main.rs: Rust implementation of the file organizer utility.
// This version fixes compilation errors and ensures completeness.

use anyhow::{bail, Context, Result}; // Use anyhow for convenient error handling
use clap::Parser; // For command-line argument parsing
use chrono::Local; // For generating timestamps
use fern::colors::{Color, ColoredLevelConfig}; // For colored logging output
use log::{debug, error, info, warn, LevelFilter}; // Logging facade
use serde::Deserialize; // For deserializing JSON config
use std::{
    collections::{HashMap, HashSet},
    env, // For CARGO_PKG_VERSION
    // Removed unused 'File' import
    fs::{self}, // Standard file system operations
    io::{self, ErrorKind},
    path::{Path, PathBuf},
    time::Instant, // For accurate duration measurement
};
use walkdir::{DirEntry, WalkDir}; // For efficient directory traversal

// --- Configuration Structures ---

/// Represents the structure of the JSON configuration file for categories.
#[derive(Deserialize, Debug, Clone)]
struct CategoriesConfig(HashMap<String, Vec<String>>);

/// Provides the default file categorization configuration.
fn default_categories() -> CategoriesConfig {
    let mut map = HashMap::new();
    macro_rules! add_category {
        ($map:expr, $name:expr, [$($ext:expr),* $(,)?]) => {
            $map.insert($name.to_string(), vec![$($ext.to_string()),*]);
        };
    }
    add_category!(map, "images", [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".svg", ".ico"]);
    add_category!(map, "documents", [".pdf", ".docx", ".doc", ".txt", ".rtf", ".odt", ".xlsx", ".xls", ".csv", ".pptx", ".ppt", ".md", ".tex", ".chm", ".epub"]);
    add_category!(map, "videos", [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"]);
    add_category!(map, "audio", [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"]);
    add_category!(map, "archives", [".zip", ".rar", ".tar", ".gz", ".bz2", ".7z", ".iso"]);
    add_category!(map, "code", [".py", ".java", ".c", ".cpp", ".h", ".cs", ".html", ".css", ".js", ".ts", ".jsx", ".tsx", ".xml", ".json", ".yaml", ".yml", ".sh", ".bat", ".ps1", ".rb", ".php", ".go", ".rs", ".swift", ".kt", ".ipynb", ".sql", ".toml"]);
    add_category!(map, "apps", [".exe", ".msi", ".apk", ".dmg", ".deb", ".rpm", ".app"]);
    add_category!(map, "fonts", [".ttf", ".otf", ".woff", ".woff2"]);
    add_category!(map, "shortcuts", [".lnk", ".url"]);
    map.insert("other".to_string(), vec![]);
    CategoriesConfig(map)
}

/// Loads category configuration from a specified JSON file path.
fn load_config_file(config_path: Option<&PathBuf>) -> Result<CategoriesConfig> {
    match config_path {
        Some(path) if path.is_file() => {
            info!("Loading category configuration from: {}", path.display());
            let file_content = fs::read_to_string(path)
                .with_context(|| format!("Failed to read config file: {}", path.display()))?;
            let mut config: HashMap<String, Vec<String>> = serde_json::from_str(&file_content)
                .with_context(|| format!("Failed to parse JSON config file: {}", path.display()))?;
            config.entry("other".to_string()).or_insert_with(Vec::new);
            info!("Successfully loaded and validated custom configuration.");
            Ok(CategoriesConfig(config))
        }
        Some(path) => {
            warn!(
                "Config path '{}' provided but is not a valid file. Using default categories.",
                path.display()
            );
            Ok(default_categories())
        }
        None => {
            info!("No config file specified. Using default category configuration.");
            Ok(default_categories())
        }
    }
}

/// Determines the category name (String) for a given file based on its extension.
fn categorize_file(filename: &Path, categories_config: &CategoriesConfig) -> String {
    let extension = filename
        .extension()
        .and_then(|s| s.to_str())
        .map(|s| format!(".{}", s.to_lowercase()))
        .unwrap_or_else(|| "no_extension".to_string());
    if extension == "no_extension" { return extension; }
    for (category, extensions) in &categories_config.0 {
        if extensions.contains(&extension) { return category.clone(); }
    }
    "other".to_string()
}

// --- Platform Specific ---

/// Checks if a file or directory is hidden on Windows using standard library features.
#[cfg(windows)]
fn is_hidden(path: &Path) -> Result<bool> {
    use std::os::windows::fs::MetadataExt;
    let metadata = fs::metadata(path)
        .with_context(|| format!("Failed to get metadata for {}", path.display()))?;
    let attributes = metadata.file_attributes();
    // Use the raw value 0x2 for FILE_ATTRIBUTE_HIDDEN when using std::os::windows::fs
    const FILE_ATTRIBUTE_HIDDEN_VALUE: u32 = 0x2;
    Ok((attributes & FILE_ATTRIBUTE_HIDDEN_VALUE) != 0)
}

/// Checks if a file or directory is hidden on Unix-like systems (conventionally, starts with '.').
#[cfg(not(windows))]
fn is_hidden(path: &Path) -> Result<bool> {
    Ok(path
        .file_name()
        .and_then(|s| s.to_str())
        .map(|s| s.starts_with('.'))
        .unwrap_or(false))
}

/// Helper for walkdir filter_entry to check hidden status.
fn should_keep_entry(entry: &DirEntry, include_hidden: bool) -> bool {
    if include_hidden { return true; }
    match is_hidden(entry.path()) {
        Ok(hidden) => !hidden,
        Err(err) => {
            warn!(
                "Could not determine hidden status for {}: {}. Excluding entry.",
                entry.path().display(), err
            );
            false // Exclude if check fails (safer default)
        }
    }
}

// --- Command Line Arguments ---

#[derive(clap::ValueEnum, Clone, Debug, PartialEq, Eq)]
enum OrganizeMethod { Category, Extension, }

#[derive(Parser, Debug)]
#[command(author, version, about = "Organize files by category or extension (Rust version).",
    long_about = "A Rust utility for organizing files from source directories into categorized target folders based on file types or extensions.",
    help_template = "{before-help}{name} {version}\n{author-with-newline}{about-with-newline}\n{usage-heading} {usage}\n\n{all-args}{after-help}"
)]
struct CliArgs {
    #[arg(short, long, value_name = "DIR")] source: PathBuf,
    #[arg(short, long, value_name = "DIR")] target: PathBuf,
    #[arg(short, long, value_name = "FILE")] config: Option<PathBuf>,
    #[arg(long, value_enum, default_value_t = OrganizeMethod::Category)] organize_by: OrganizeMethod,
    #[arg(long)] move_files: bool,
    #[arg(long, conflicts_with_all = ["skip_existing", "overwrite"])] timestamp_duplicates: bool,
    #[arg(long, short = 'k', conflicts_with_all = ["timestamp_duplicates", "overwrite"])] skip_existing: bool,
    #[arg(long, conflicts_with_all = ["timestamp_duplicates", "skip_existing"])] overwrite: bool,
    #[arg(long, short = 'i')] include_hidden: bool,
    #[arg(long, short = 'l')] follow_links: bool,
    #[arg(long, requires = "move_files")] remove_empty_source_dirs: bool,
    #[arg(long, value_name = "FILE")] log_file: Option<PathBuf>,
    #[arg(long, value_parser = clap::value_parser!(LevelFilter), default_value = "info")] log_level: LevelFilter,
}

// --- Core Logic ---

/// Holds statistics about the file processing operation.
#[derive(Debug, Default)]
struct ProcessStats {
    /// Count of directory entries successfully yielded by the filtered WalkDir iterator.
    total_scanned: u64,
    processed: u64,
    skipped: u64,
    errors: u64,
    failed_files: Vec<(PathBuf, String)>, // Stores paths and error context
}

/// Scans the source directory for unique file extensions.
fn get_all_extensions(
    source_directory: &Path,
    include_hidden: bool,
    follow_links: bool,
) -> Result<HashSet<String>> {
    let mut extensions = HashSet::new();
    info!("Scanning source directory for all unique file extensions...");
    let walker = WalkDir::new(source_directory)
        .follow_links(follow_links)
        .into_iter();
    let mut count = 0;
    for entry_result in walker.filter_entry(|e| should_keep_entry(e, include_hidden)) {
        match entry_result {
            Ok(entry) => {
                let path = entry.path();
                if path.is_file() {
                    count += 1;
                    if let Some(ext) = path.extension().and_then(|e| e.to_str()) {
                        extensions.insert(ext.to_lowercase());
                    }
                    if count % 1000 == 0 { debug!("Scanned {} files for extensions...", count); }
                }
            }
            Err(e) => warn!("Error accessing entry during extension scan: {}", e),
        }
    }
    info!("Found {} unique extensions.", extensions.len());
    Ok(extensions)
}

/// Creates necessary target subfolders.
fn create_target_folders(
    base_dir: &Path,
    organize_by: &OrganizeMethod,
    categories_config: Option<&CategoriesConfig>,
    all_extensions: Option<&HashSet<String>>,
) -> Result<()> {
    info!("Ensuring target base directory exists: {}", base_dir.display());
    fs::create_dir_all(base_dir)
        .with_context(|| format!("Failed to create base target directory: {}", base_dir.display()))?;
    let folders_to_create: HashSet<String> = match organize_by {
        OrganizeMethod::Category => {
            let mut folders = categories_config
                .map(|cfg| cfg.0.keys().cloned().collect::<HashSet<String>>())
                .unwrap_or_default();
            folders.insert("other".to_string());
            folders.insert("no_extension".to_string());
            folders
        }
        OrganizeMethod::Extension => {
            let mut folders = all_extensions.cloned().unwrap_or_default();
            folders.insert("no_extension".to_string());
            folders
        }
    };
    info!(
        "Creating target subfolders (mode: {:?}). Total potential folders: {}",
        organize_by,
        folders_to_create.len()
    );
    let mut created_count = 0;
    for folder_name in &folders_to_create {
        if folder_name.is_empty() { warn!("Skipping creation of folder with empty name."); continue; }
        let folder_path = base_dir.join(folder_name);
        if !folder_path.exists() {
            fs::create_dir_all(&folder_path).with_context(|| {
                format!("Failed to create target folder '{}'", folder_path.display())
            })?;
            debug!("Created target folder: {}", folder_path.display());
            created_count += 1;
        }
    }
    info!("Created {} new target subfolders.", created_count);
    Ok(())
}

/// Attempts to move a file, falling back to copy-then-delete on cross-device errors.
fn move_file_with_fallback(source: &Path, target: &Path) -> io::Result<()> {
    match fs::rename(source, target) {
        Ok(_) => Ok(()),
        Err(rename_error) => {
            // Note: Relies on platform-specific OS error codes (Windows: 17, Unix: 18/libc::EXDEV). Might be brittle.
            let is_cross_device = || -> bool {
                #[cfg(windows)] { rename_error.raw_os_error() == Some(17) }
                #[cfg(unix)] { rename_error.raw_os_error() == Some(18) }
                #[cfg(not(any(windows, unix)))] { false }
            };
            if is_cross_device() {
                warn!("Rename failed (cross-device error detected), attempting copy+delete fallback for move: {} -> {}", source.display(), target.display());
                // Note: std::fs::copy preserves permissions but not other metadata like modification time (unlike Python's shutil.copy2).
                fs::copy(source, target)?;
                fs::remove_file(source)?;
                Ok(())
            } else { Err(rename_error) }
        }
    }
}


/// Main function to perform the file organization.
fn organize_files(args: &CliArgs, categories_config: &CategoriesConfig) -> Result<ProcessStats> {
    if !args.source.is_dir() { bail!("Source directory '{}' is invalid or not found.", args.source.display()); }
    if !args.target.exists() {
        info!("Creating target directory: {}", args.target.display());
        fs::create_dir_all(&args.target).with_context(|| format!("Could not create target directory '{}'", args.target.display()))?;
    } else if !args.target.is_dir() { bail!("Target path '{}' exists but is not a directory.", args.target.display()); }

    info!("Preparing target folders...");
    let extensions_for_folders = if args.organize_by == OrganizeMethod::Extension {
        Some(get_all_extensions(&args.source, args.include_hidden, args.follow_links)?)
    } else { None };
    create_target_folders(&args.target, &args.organize_by, Some(categories_config), extensions_for_folders.as_ref())?;

    info!("Starting file processing...");
    let mut stats = ProcessStats::default();
    let mut file_counter = 0u64;
    let walker = WalkDir::new(&args.source).follow_links(args.follow_links).into_iter();

    for entry_result in walker.filter_entry(|e| should_keep_entry(e, args.include_hidden)) {
        stats.total_scanned += 1; // Count filtered entries
        let entry = match entry_result {
            Ok(e) => e,
            Err(e) => {
                let path_display = e.path().unwrap_or_else(|| Path::new("?")).display();
                error!("Error scanning path {}: {}", path_display, e);
                stats.errors += 1;
                // Provide default PathBuf if e.path() is None
                stats.failed_files.push((
                    e.path().map_or_else(|| PathBuf::from("?"), |p| p.to_path_buf()),
                    format!("Scan error: {:?}", e),
                ));
                continue;
            }
        };

        if !entry.file_type().is_file() { stats.skipped += 1; continue; }

        file_counter += 1;
        let source_path = entry.path();
        let progress_prefix = format!("[{}]", file_counter);

        let file_result: Result<()> = (|| {
            let file_name = source_path.file_name().with_context(|| format!("Could not get filename for path: {}", source_path.display()))?;
            let target_subfolder_name = match args.organize_by {
                OrganizeMethod::Category => categorize_file(source_path, categories_config),
                OrganizeMethod::Extension => source_path.extension().and_then(|s| s.to_str()).map(|s| s.to_lowercase()).unwrap_or_else(|| "no_extension".to_string()),
            };
            let target_folder_path = args.target.join(&target_subfolder_name);
            let mut target_file_path = target_folder_path.join(file_name);

            if target_file_path.exists() {
                if args.skip_existing {
                    info!("{} Skipping (target exists): {}", progress_prefix, target_file_path.display());
                    stats.skipped += 1; return Ok(());
                } else if args.timestamp_duplicates {
                    let original_target_path_display = target_file_path.display().to_string();
                    let mut counter = 1;
                    // Use file_name directly, it's already &OsStr
                    let stem = source_path.file_stem().unwrap_or(file_name);
                    let ext = source_path.extension().unwrap_or_default();
                    const MAX_TIMESTAMP_ATTEMPTS: u32 = 1000;
                    loop {
                        let timestamp = Local::now().format("%Y%m%d_%H%M%S");
                        let mut new_name_os = std::ffi::OsString::new();
                        new_name_os.push(stem);
                        new_name_os.push(format!("_{}_{}", timestamp, counter));
                        if !ext.is_empty() { new_name_os.push("."); new_name_os.push(ext); }
                        target_file_path = target_folder_path.join(&new_name_os);
                        if !target_file_path.exists() { break; }
                        counter += 1;
                        if counter > MAX_TIMESTAMP_ATTEMPTS { bail!("Could not find unique timestamped name for {} after {} attempts. Skipping.", original_target_path_display, MAX_TIMESTAMP_ATTEMPTS); }
                    }
                    info!("{} Target exists '{}'. Renaming duplicate to: {}", progress_prefix, original_target_path_display, target_file_path.display());
                } else if args.overwrite { warn!("{} Overwriting existing target file: {}", progress_prefix, target_file_path.display()); }
                else { warn!("{} Overwriting existing target file (default): {}", progress_prefix, target_file_path.display()); }
            }

            fs::create_dir_all(&target_folder_path).with_context(|| format!("Failed to ensure target directory '{}' exists", target_folder_path.display()))?;
            let operation_desc = if args.move_files { "move" } else { "copy" };
            debug!("{} Attempting to {} '{}' to '{}'", progress_prefix, operation_desc, source_path.display(), target_file_path.display());

            if args.move_files {
                move_file_with_fallback(source_path, &target_file_path).with_context(|| format!("Failed to move '{}' to '{}'", source_path.display(), target_file_path.display()))?;
            } else {
                // Note: std::fs::copy preserves permissions but not other metadata like modification time (unlike Python's shutil.copy2).
                // For full metadata preservation, consider crates like `fs_extra` or platform-specific APIs.
                fs::copy(source_path, &target_file_path).map(|_| ()).with_context(|| format!("Failed to copy '{}' to '{}'", source_path.display(), target_file_path.display()))?;
            }
            stats.processed += 1;
            Ok(())
        })(); // End inner closure

        if let Err(e) = file_result {
            error!("{} Failed to process '{}': {:?}", progress_prefix, source_path.display(), e);
            stats.errors += 1;
            stats.failed_files.push((source_path.to_path_buf(), format!("{:?}", e)));
        }
    } // End main loop

    Ok(stats)
}

/// Recursively removes empty folders starting from the bottom up.
fn remove_empty_folders(directory: &Path) -> Result<u32> {
    let mut removed_count = 0u32;
    info!("Attempting to remove empty directories within: {}", directory.display());
    let mut dirs_to_check = Vec::new();
    for entry_result in WalkDir::new(directory).min_depth(1) {
        match entry_result {
            Ok(entry) if entry.file_type().is_dir() => { dirs_to_check.push(entry.into_path()); }
            Ok(_) => {}
            Err(e) => warn!("Error accessing entry during empty dir scan: {}", e),
        }
    }
    dirs_to_check.sort_by(|a, b| b.components().count().cmp(&a.components().count()));
    for dir_path in dirs_to_check {
        if !dir_path.is_dir() { continue; }
        match fs::read_dir(&dir_path) {
            Ok(mut read_dir) => {
                if read_dir.next().is_none() { // Directory is empty
                    match fs::remove_dir(&dir_path) {
                        Ok(_) => { info!("Removed empty directory: {}", dir_path.display()); removed_count += 1; }
                        Err(e) => { if e.kind() != ErrorKind::NotFound { warn!("Could not remove presumably empty directory '{}': {}", dir_path.display(), e); } }
                    }
                }
            }
            Err(e) => { if e.kind() != ErrorKind::NotFound { warn!("Could not read directory '{}' to check emptiness: {}", dir_path.display(), e); } }
        }
    }
    info!("Finished removing empty directories. Removed: {}", removed_count);
    Ok(removed_count)
}

// --- Logging Setup ---
/// Sets up logging using the fern crate.
fn setup_logging(log_level: LevelFilter, log_file: Option<&PathBuf>) -> Result<()> {
    let colors = ColoredLevelConfig::new().error(Color::Red).warn(Color::Yellow).info(Color::Green).debug(Color::Blue).trace(Color::BrightBlack);
    let base_config = fern::Dispatch::new()
        .format(move |out, message, record| {
            out.finish(format_args!(
                "[{} {} {}] {}",
                chrono::Local::now().format("%Y-%m-%d %H:%M:%S%.3f"), colors.color(record.level()), record.target(), message
            ))
        })
        .level(log_level)
        .level_for("hyper", LevelFilter::Warn).level_for("mio", LevelFilter::Warn).level_for("want", LevelFilter::Warn).level_for("reqwest", LevelFilter::Warn).level_for("rustls", LevelFilter::Warn);
    let stderr_logger = fern::Dispatch::new().filter(move |metadata| { log_level <= LevelFilter::Debug || metadata.target().starts_with(env!("CARGO_PKG_NAME")) }).chain(std::io::stderr());
    let mut final_dispatch = base_config.chain(stderr_logger);
    let mut file_logger_ok = false;
    if let Some(log_path) = log_file {
        match fern::log_file(log_path) {
            Ok(file_output) => { final_dispatch = final_dispatch.chain(file_output); file_logger_ok = true; }
            Err(e) => { eprintln!("Error: Failed to create log file '{}': {}. Logging to console only.", log_path.display(), e); }
        }
    }
    final_dispatch.apply().context("Failed to set up logging")?;
    if file_logger_ok { if let Some(path) = log_file { info!("File logging enabled to: {}", path.display()); } }
    Ok(())
}

// --- Main Application Entry Point ---
fn main() -> Result<()> {
    let overall_start_time = Instant::now(); // Start timing
    let args = CliArgs::parse();
    setup_logging(args.log_level, args.log_file.as_ref())?;

    info!("Rust File Organizer (v{}) starting...", env!("CARGO_PKG_VERSION"));
    debug!("Arguments received: {:?}", args);
    info!("Source directory: {}", args.source.display());
    info!("Target directory: {}", args.target.display());
    info!("Organization mode: {:?}", args.organize_by);
    info!("Operation: {}", if args.move_files { "Move" } else { "Copy" });
    info!("Include hidden: {}", args.include_hidden);
    info!("Follow links: {}", args.follow_links);
    if args.skip_existing { info!("Duplicate handling: Skip existing"); }
    else if args.timestamp_duplicates { info!("Duplicate handling: Timestamp duplicates"); }
    else if args.overwrite { info!("Duplicate handling: Overwrite existing (explicitly)"); }
    else { info!("Duplicate handling: Overwrite existing (default)"); }

    let categories = load_config_file(args.config.as_ref())?;
    let result = organize_files(&args, &categories);

    match result {
        Ok(stats) => {
            if args.move_files && args.remove_empty_source_dirs && stats.processed > 0 {
                if let Err(e) = remove_empty_folders(&args.source) { error!("Error during empty source directory removal: {:?}", e); }
            }
            let overall_duration = overall_start_time.elapsed();
            let summary = format!(
                "Operation completed in {:.2?}. Scanned Entries: {}, Processed Files: {}, Skipped: {}, Errors: {}",
                overall_duration, stats.total_scanned, stats.processed, stats.skipped, stats.errors
            );
            info!("{}", summary);
            println!("\n{}", summary);
            if stats.errors > 0 {
                eprintln!("\n--- Errors occurred during processing: ---");
                for (path, error_msg) in &stats.failed_files {
                    eprintln!(" - File: {}", path.display());
                    eprintln!("   Error: {}", error_msg);
                }
                eprintln!("-----------------------------------------");
                eprintln!("Warning: {} errors occurred. Please check logs (stderr/file) for full details.", stats.errors);
                // Potentially exit with non-zero status
                // std::process::exit(1);
            }
        }
        Err(e) => {
            error!("Critical error during file organization: {:?}", e);
            eprintln!("\nError: File organization failed critically. Check logs (stderr/file) for details.");
            std::process::exit(1);
        }
    }
    info!("Rust File Organizer finished.");
    Ok(())
}

// --- Testing Notes ---
// Consider using crates like `assert_fs`, `predicates`, `assert_cmd` for testing.
// Test scenarios: basic copy/move (category/extension), duplicate handling (skip/timestamp/overwrite),
// hidden files, symlinks, empty dirs, custom config, empty dir removal, errors (permissions), long paths.

{% endcodeblock %}
