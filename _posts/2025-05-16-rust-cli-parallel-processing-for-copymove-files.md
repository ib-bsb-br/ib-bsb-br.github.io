---
tags: [software>rust]
info: aberto.
date: 2025-05-16
type: post
layout: post
published: true
slug: rust-cli-parallel-processing-for-copymove-files
title: 'Rust CLI parallel processing for copy/move files'
---
This tool provides basic file and directory `copy`, `move` (cut-and-paste), and `delete` operations, with an option for parallel processing on multi-core systems.

This guide is tailored for an `arm64 Debian Bullseye` environment, such as those found on RK3588-based single-board computers or servers.

## Prerequisites

Before you begin, ensure your `arm64 Debian Bullseye` system is set up with the following:

1.  **Rust Language Toolchain:**
    *   If you don't have Rust installed, visit [https://rustup.rs/](https://rustup.rs/) and follow the instructions. This will install `rustc` (the compiler) and `cargo` (the build tool and package manager).
        ```bash
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
        source $HOME/.cargo/env 
        # You might need to open a new terminal or re-login for changes to take effect
        ```
2.  **Essential Build Tools:**
    *   Install common build utilities often required by Rust crates that might link against C libraries or need system configuration.
        ```bash
        sudo apt update
        sudo apt install build-essential pkg-config libssl-dev
        ```
    *(Note: `libssl-dev` is a common dependency for many Rust crates, though not strictly required by this specific MVP's direct dependencies, it's good practice to have it for broader Rust development).*

## 1. Creating the Project and Adding Code

First, create a new Rust project using Cargo and navigate into its directory:

```bash
cargo new rapidcopy_rust_cli_mvp
cd rapidcopy_rust_cli_mvp
```

Next, you'll replace the default `src/main.rs` and `Cargo.toml` files with the code for our RapidCopy-rs MVP.

**Replace the contents of `Cargo.toml` with the following:**

```toml
[package]
name = "rapidcopy_rust_cli_mvp"
version = "0.1.0"
edition = "2021"

[dependencies]
clap = { version = "4.5.38", features = ["derive"] }
indicatif = "0.17.11"
rayon = "1.10.0"
thiserror = "1.0.69"
walkdir = "2.5.0"
libc = "0.2.172"
path-absolutize = "3.1.1"
```

**Replace the contents of `src/main.rs` with the following Rust code:**

{% codeblock rust %}
// src/main.rs

use clap::{Parser, Subcommand};
use indicatif::{HumanBytes, MultiProgress, ProgressBar, ProgressStyle};
use path_absolutize::*; // For Path::absolutize()
use rayon::prelude::*;
use std::{
    ffi::OsString,
    fs,
    io::{self, ErrorKind, Read, Write},
    path::{Path, PathBuf},
    sync::{
        atomic::{AtomicU64, Ordering as AtomicOrdering},
        Arc, Mutex,
    },
    thread,
    time::Duration,
};
use thiserror::Error;
use walkdir::{DirEntry, WalkDir};

// --- Argument Parsing ---
#[derive(Parser, Debug)]
#[clap(author, version, about = "RapidCopy-rs (MVP): Fast file operations CLI", long_about = None)]
struct Cli {
    #[clap(subcommand)]
    command: Commands,

    #[clap(short, long, global = true, help = "Enable verbose output")]
    verbose: bool,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// Copies a file or directory recursively
    Copy {
        /// Source path
        source: PathBuf,
        /// Destination path
        destination: PathBuf,
        #[clap(short, long, help = "Overwrite existing files at the destination")]
        overwrite: bool,
        #[clap(long, help = "Enable parallel processing for directory contents")]
        parallel: bool,
    },
    /// Moves a file or directory recursively (cut and paste)
    Move {
        /// Source path
        source: PathBuf,
        /// Destination path
        destination: PathBuf,
        #[clap(short, long, help = "Overwrite existing files at the destination if copying")]
        overwrite: bool,
        #[clap(short = 'f', long, help = "Force deletion of source without interactive confirmation (used in move)")]
        force_delete_source: bool,
        #[clap(long, help = "Enable parallel processing for directory contents during copy phase")]
        parallel: bool,
    },
    /// Deletes a file or directory recursively
    Delete {
        /// Path to delete
        path: PathBuf,
        #[clap(short, long, help = "Force deletion without interactive confirmation")]
        force: bool,
    },
}

// --- Error Handling ---
#[derive(Error, Debug)]
pub enum AppError {
    #[error("I/O error accessing '{path:?}': {source}")]
    Io {
        source: io::Error,
        path: PathBuf,
    },
    #[error("WalkDir error for path '{path:?}': {source}")]
    WalkDir {
        source: walkdir::Error,
        path: PathBuf,
    },
    #[error("Source path does not exist: {0}")]
    SourceDoesNotExist(PathBuf),
    #[error("Destination path '{0}' already exists and overwrite is false")]
    DestinationExists(PathBuf),
    #[error("Cannot copy/move directory '{source_dir}' to existing file '{dest_file}'")]
    DirToExistingFile {
        source_dir: PathBuf,
        dest_file: PathBuf,
    },
    #[error("Cannot copy/move file '{source_file}' to existing directory '{dest_dir}' (ambiguous destination name or destination is a file and overwrite is false)")]
    FileToExistingDirAmbiguous {
        source_file: PathBuf,
        dest_dir: PathBuf,
    },
    #[error("User did not confirm deletion of '{0}'")]
    DeletionNotConfirmed(PathBuf),
    #[error("Failed to get metadata for path: {0}")]
    MetadataError(PathBuf),
    #[error("Source path '{0}' has no filename component")]
    NoFileName(PathBuf),
    #[error("Failed to strip prefix for path processing: '{path}' relative to '{base}'")]
    StripPrefixError { path: PathBuf, base: PathBuf },
    #[error("Operation failed with multiple errors during parallel processing:\n{0:#?}")]
    ParallelOperationFailed(Vec<String>),
    #[error("Cannot move/copy '{0}' to a subdirectory of itself '{1}'")]
    RecursiveMoveOrCopy(PathBuf, PathBuf),
    #[error("Indicatif style template error: {0}")]
    TemplateError(String),
}

impl From<walkdir::Error> for AppError {
    fn from(err: walkdir::Error) -> Self {
        let path = err
            .path()
            .unwrap_or_else(|| Path::new("<unknown path from walkdir error>"))
            .to_path_buf();
        AppError::WalkDir { source: err, path }
    }
}

fn io_err_with_path(err: io::Error, path: &Path) -> AppError {
    AppError::Io {
        source: err,
        path: path.to_path_buf(),
    }
}

impl From<indicatif::style::TemplateError> for AppError {
    fn from(err: indicatif::style::TemplateError) -> Self {
        AppError::TemplateError(err.to_string())
    }
}

// --- Core Logic Module ---
mod core_logic {
    use super::*;

    const BUFFER_SIZE: usize = 128 * 1024;

    #[derive(Debug)]
    struct ProgressInfo {
        items_processed: AtomicU64,
        bytes_processed: AtomicU64,
        total_items_to_process: u64,
        total_bytes_to_process: u64,
    }

    impl ProgressInfo {
        fn new(total_items: u64, total_bytes: u64) -> Self {
            Self {
                items_processed: AtomicU64::new(0),
                bytes_processed: AtomicU64::new(0),
                total_items_to_process: total_items,
                total_bytes_to_process: total_bytes,
            }
        }
    }

    fn pre_scan_directory(dir: &Path, verbose: bool) -> Result<(u64, u64), AppError> {
        if verbose {
            println!("Pre-scanning directory '{}'...", dir.display());
        }
        let mut total_items = 0u64;
        let mut total_bytes = 0u64;
        total_items += 1; // Count the root directory itself
        for entry_result in WalkDir::new(dir).min_depth(1).follow_links(false) {
            let entry = entry_result?; 
            total_items += 1;
            if entry.file_type().is_file() {
                total_bytes += entry.metadata()?.len(); 
            }
        }
        if verbose {
            println!(
                "Pre-scan complete: {} items, {}",
                total_items,
                HumanBytes(total_bytes)
            );
        }
        Ok((total_items, total_bytes))
    }

    fn copy_single_file(
        source: &Path,
        destination: &Path,
        overwrite: bool,
        mp_opt: Option<&MultiProgress>,
        overall_progress_info_opt: Option<&Arc<ProgressInfo>>,
        verbose: bool,
    ) -> Result<u64, AppError> {
        if destination.exists() {
            let dest_meta =
                fs::metadata(destination).map_err(|e| io_err_with_path(e, destination))?;
            if dest_meta.is_dir() {
                return Err(AppError::FileToExistingDirAmbiguous {
                    source_file: source.to_path_buf(),
                    dest_dir: destination.to_path_buf(),
                });
            }
            if !overwrite {
                if verbose {
                    println!(
                        "Skipping '{}': destination file exists and overwrite is false.",
                        destination.display()
                    );
                }
                if let Some(stats) = overall_progress_info_opt {
                    stats.items_processed.fetch_add(1, AtomicOrdering::Relaxed);
                }
                return Ok(0);
            }
        }

        if let Some(parent) = destination.parent() {
            if !parent.exists() {
                fs::create_dir_all(parent).map_err(|e| io_err_with_path(e, parent))?;
            }
        }

        let file_size = fs::metadata(source)
            .map_err(|e| io_err_with_path(e, source))?
            .len();

        let pb = if let Some(mp) = mp_opt {
            let p = mp.add(ProgressBar::new(file_size));
            p.enable_steady_tick(Duration::from_millis(250));
            p
        } else {
            let p = ProgressBar::new(file_size);
            p.enable_steady_tick(Duration::from_millis(100));
            p
        };

        pb.set_style(
            ProgressStyle::default_bar()
                .template(
                    "{msg:<30.bold.dim} [{bar:40.cyan/blue}] {bytes}/{total_bytes} ({bytes_per_sec}, {eta})",
                )?
                .progress_chars("=> "),
        );
        let filename = source.file_name().unwrap_or_default().to_string_lossy();
        pb.set_message(filename.chars().take(30).collect::<String>());

        let mut source_file = fs::File::open(source).map_err(|e| io_err_with_path(e, source))?;
        let mut dest_file =
            fs::File::create(destination).map_err(|e| io_err_with_path(e, destination))?;

        let mut buffer = vec![0; BUFFER_SIZE];
        let mut copied_bytes_for_this_file = 0u64;

        loop {
            let bytes_read = source_file
                .read(&mut buffer)
                .map_err(|e| io_err_with_path(e, source))?;
            if bytes_read == 0 {
                break;
            }
            dest_file
                .write_all(&buffer[..bytes_read])
                .map_err(|e| io_err_with_path(e, destination))?;
            copied_bytes_for_this_file += bytes_read as u64;
            pb.set_position(copied_bytes_for_this_file);
            if let Some(stats) = overall_progress_info_opt {
                stats
                    .bytes_processed
                    .fetch_add(bytes_read as u64, AtomicOrdering::Relaxed);
            }
        }
        pb.finish_with_message(format!("Copied {} ({})", filename, HumanBytes(file_size)));
        if let Some(stats) = overall_progress_info_opt {
            stats.items_processed.fetch_add(1, AtomicOrdering::Relaxed);
        }
        Ok(file_size)
    }

    fn copy_dir_recursive(
        source_dir: &Path,
        target_dest_dir: &Path, 
        overwrite: bool,
        parallel: bool,
        _overall_item_pb: &ProgressBar, 
        progress_info: &Arc<ProgressInfo>,
        verbose: bool, // verbose is available here
    ) -> Result<(), Vec<String>> {
        if verbose {
            println!(
                "Recursively copying contents of '{}' into '{}'",
                source_dir.display(),
                target_dest_dir.display()
            );
        }

        if !target_dest_dir.exists() {
            fs::create_dir_all(target_dest_dir)
                .map_err(|e| vec![io_err_with_path(e, target_dest_dir).to_string()])?;
            if verbose {
                println!("Created directory '{}'", target_dest_dir.display());
            }
        }
      
        let entries: Vec<DirEntry> = WalkDir::new(source_dir)
            .min_depth(1) 
            .follow_links(false)
            .into_iter()
            .collect::<Result<Vec<_>, _>>()
            .map_err(|e| {
                vec![AppError::WalkDir {
                    source: e,
                    path: source_dir.to_path_buf(),
                }
                .to_string()]
            })?;

        let multi_progress_manager_opt = if parallel && entries.iter().filter(|e| e.path().is_file()).count() > 1 {
            Some(MultiProgress::new())
        } else {
            None
        };

        let errors_arc = Arc::new(Mutex::new(Vec::<String>::new()));

        let process_entry_closure = |entry: DirEntry| {
            let entry_path = entry.path();
            let relative_path = match entry_path.strip_prefix(source_dir) {
                Ok(p) => p,
                Err(_) => {
                    errors_arc.lock().unwrap().push(
                        AppError::StripPrefixError {
                            path: entry_path.to_path_buf(),
                            base: source_dir.to_path_buf(),
                        }
                        .to_string(),
                    );
                    return;
                }
            };
            let dest_path = target_dest_dir.join(relative_path);

            if entry.file_type().is_dir() {
                if verbose {
                    println!("Creating directory '{}'", dest_path.display());
                }
                if let Err(e) = fs::create_dir_all(&dest_path) {
                    errors_arc
                        .lock()
                        .unwrap()
                        .push(io_err_with_path(e, &dest_path).to_string());
                    return;
                }
                progress_info
                    .items_processed
                    .fetch_add(1, AtomicOrdering::Relaxed);
            } else if entry.file_type().is_file() {
                match copy_single_file(
                    entry_path,
                    &dest_path,
                    overwrite,
                    multi_progress_manager_opt.as_ref(),
                    Some(progress_info), 
                    verbose,
                ) {
                    Ok(_) => {}
                    Err(e) => {
                        errors_arc.lock().unwrap().push(format!(
                            "Error copying file '{}': {}",
                            entry_path.display(),
                            e
                        ));
                    }
                }
            } else {
                progress_info
                    .items_processed
                    .fetch_add(1, AtomicOrdering::Relaxed);
                if verbose {
                    println!("Skipping non-file/non-directory entry: {}", entry_path.display());
                }
            }
        };

        if parallel && entries.len() > 1 {
            entries.into_par_iter().for_each(process_entry_closure);
        } else {
            for entry in entries {
                process_entry_closure(entry);
            }
        }

        if let Some(mp) = multi_progress_manager_opt {
            if let Err(e) = mp.clear() {
                if verbose {
                    // Error during UI cleanup is not critical to the copy operation itself.
                    eprintln!("Warning: Failed to clear multi-progress display: {}", e);
                }
            }
        }

        let final_errors = Arc::try_unwrap(errors_arc)
            .expect("Mutex still has multiple owners for errors_arc")
            .into_inner()
            .expect("Mutex was poisoned for errors_arc");

        if !final_errors.is_empty() {
            return Err(final_errors);
        }
        Ok(())
    }

    pub fn handle_copy_operation_main(
        source: &Path,
        destination: &Path,
        overwrite: bool,
        parallel: bool,
        verbose: bool,
    ) -> Result<u64, AppError> {
        if verbose {
            println!(
                "Copy operation: '{}' -> '{}'",
                source.display(),
                destination.display()
            );
        }
        if !source.exists() {
            return Err(AppError::SourceDoesNotExist(source.to_path_buf()));
        }

        let source_meta = fs::metadata(source).map_err(|e| io_err_with_path(e, source))?;
        let source_abs = source.absolutize().map_err(|e| io_err_with_path(e, source))?.into_owned();


        let target_path_for_item: PathBuf; 
        let effective_dest_dir_for_contents: PathBuf; 

        if source_meta.is_dir() {
            let source_name = source
                .file_name()
                .ok_or_else(|| AppError::NoFileName(source.to_path_buf()))?;
            if destination.exists()
                && fs::metadata(destination)
                    .map_err(|e| io_err_with_path(e, destination))?
                    .is_dir()
            {
                target_path_for_item = destination.join(source_name);
            } else if destination.exists()
                && fs::metadata(destination)
                    .map_err(|e| io_err_with_path(e, destination))?
                    .is_file()
            {
                return Err(AppError::DirToExistingFile {
                    source_dir: source.to_path_buf(),
                    dest_file: destination.to_path_buf(),
                });
            } else {
                target_path_for_item = destination.to_path_buf();
            }
            effective_dest_dir_for_contents = target_path_for_item.clone(); 
            
            let target_abs_check = target_path_for_item.absolutize().map_err(|e| io_err_with_path(e, &target_path_for_item))?.into_owned();
            if target_abs_check.starts_with(&source_abs) {
                 return Err(AppError::RecursiveMoveOrCopy(source.to_path_buf(), target_path_for_item));
            }

        } else { // Source is a file
            if destination.exists()
                && fs::metadata(destination)
                    .map_err(|e| io_err_with_path(e, destination))?
                    .is_dir()
            {
                target_path_for_item = destination.join(
                    source
                        .file_name()
                        .ok_or_else(|| AppError::NoFileName(source.to_path_buf()))?,
                );
            } else if !destination.exists()
                && destination.to_string_lossy().ends_with(std::path::MAIN_SEPARATOR)
            {
                fs::create_dir_all(destination).map_err(|e| io_err_with_path(e, destination))?;
                target_path_for_item = destination.join(
                    source
                        .file_name()
                        .ok_or_else(|| AppError::NoFileName(source.to_path_buf()))?,
                );
            } else {
                target_path_for_item = destination.to_path_buf();
            }
            effective_dest_dir_for_contents = target_path_for_item
                .parent()
                .unwrap_or_else(|| Path::new("."))
                .to_path_buf();
        }

        let (total_items_scanned, total_bytes_scanned) = if source_meta.is_dir() {
            pre_scan_directory(source, verbose)?
        } else {
            (1, source_meta.len()) 
        };
        let progress_info = Arc::new(ProgressInfo::new(
            total_items_scanned,
            total_bytes_scanned,
        ));

        let overall_pb = ProgressBar::new(total_items_scanned.max(1)); 
        overall_pb.set_style(
            ProgressStyle::default_bar()
                .template("{msg} [{elapsed_precise}] {wide_bar:.cyan/blue} Overall Items: {pos}/{len} ({items_per_sec}, ETA {eta})")?
                .progress_chars("=> "),
        );
        let source_filename_owned: OsString =
            source.file_name().unwrap_or_default().to_os_string();

        overall_pb.set_message(format!(
            "Preparing to copy {}",
            source_filename_owned.to_string_lossy()
        ));
        overall_pb.enable_steady_tick(Duration::from_millis(200));

        let overall_pb_clone_for_updater = overall_pb.clone();
        let progress_info_clone_for_updater = progress_info.clone();
        let source_filename_clone_for_updater = source_filename_owned.clone();

        let bytes_updater_thread = thread::spawn(move || {
            while !overall_pb_clone_for_updater.is_finished() {
                let items_done = progress_info_clone_for_updater
                    .items_processed
                    .load(AtomicOrdering::Relaxed);
                let bytes_done = progress_info_clone_for_updater
                    .bytes_processed
                    .load(AtomicOrdering::Relaxed);

                overall_pb_clone_for_updater.set_position(items_done); 
                overall_pb_clone_for_updater.set_message(format!(
                    "Copying {} (Bytes: {} / {}) | Items: {}/{}",
                    source_filename_clone_for_updater.to_string_lossy(),
                    HumanBytes(bytes_done),
                    HumanBytes(progress_info_clone_for_updater.total_bytes_to_process),
                    items_done,
                    progress_info_clone_for_updater.total_items_to_process
                ));
                thread::sleep(Duration::from_millis(200));
            }
            let items_done = progress_info_clone_for_updater
                .items_processed
                .load(AtomicOrdering::Relaxed);
            let bytes_done = progress_info_clone_for_updater
                .bytes_processed
                .load(AtomicOrdering::Relaxed);
            overall_pb_clone_for_updater.set_position(items_done);
            overall_pb_clone_for_updater.set_message(format!(
                "Finished {} (Bytes: {} / {}) | Items: {}/{}",
                source_filename_clone_for_updater.to_string_lossy(),
                HumanBytes(bytes_done),
                HumanBytes(progress_info_clone_for_updater.total_bytes_to_process),
                items_done,
                progress_info_clone_for_updater.total_items_to_process
            ));
        });

        let result = if source_meta.is_dir() {
            if !target_path_for_item.exists() {
                 fs::create_dir_all(&target_path_for_item).map_err(|e| io_err_with_path(e, &target_path_for_item))?;
                 if verbose { println!("Created target base directory '{}'", target_path_for_item.display()); }
            }
            progress_info.items_processed.fetch_add(1, AtomicOrdering::Relaxed);

            copy_dir_recursive(
                source, 
                &effective_dest_dir_for_contents, 
                overwrite,
                parallel,
                &overall_pb,
                &progress_info,
                verbose,
            )
            .map_err(AppError::ParallelOperationFailed)?;
            Ok(progress_info.items_processed.load(AtomicOrdering::Relaxed))
        } else if source_meta.is_file() {
            copy_single_file(
                source,
                &target_path_for_item,
                overwrite,
                None, 
                Some(&progress_info),
                verbose,
            )?;
            Ok(1) 
        } else {
            if verbose {
                println!(
                    "Warning: Source '{}' is not a regular file or directory. Skipping.",
                    source.display()
                );
            }
            Ok(0)
        };

        overall_pb.set_position(progress_info.items_processed.load(AtomicOrdering::Relaxed)); 
        overall_pb.finish_with_message(format!("Copy of '{}' complete.", source.display()));
        bytes_updater_thread
            .join()
            .expect("Bytes updater thread panicked");
        result
    }

    pub fn handle_delete_operation(
        path: &Path,
        force: bool,
        verbose: bool,
    ) -> Result<u64, AppError> {
        if verbose {
            println!(
                "Delete operation: '{}' (Force: {})",
                path.display(),
                force
            );
        }

        if !path.exists() {
            if force {
                if verbose {
                    println!(
                        "Path '{}' does not exist. Nothing to delete (forced).",
                        path.display()
                    );
                }
                return Ok(0);
            }
            return Err(AppError::SourceDoesNotExist(path.to_path_buf()));
        }

        if !force {
            print!(
                "Are you sure you want to delete '{}' and all its contents? (yes/no): ",
                path.display()
            );
            io::stdout().flush().map_err(|e| io_err_with_path(e, path))?;
            let mut confirmation = String::new();
            io::stdin()
                .read_line(&mut confirmation)
                .map_err(|e| io_err_with_path(e, path))?;
            if confirmation.trim().to_lowercase() != "yes" {
                return Err(AppError::DeletionNotConfirmed(path.to_path_buf()));
            }
        }

        let items_deleted_count: u64;

        if path.is_dir() {
            let (total_items, _) = pre_scan_directory(path, verbose)?; 

            let pb = ProgressBar::new(total_items.max(1));
            pb.set_style(
                ProgressStyle::default_bar()
                    .template(
                        "{msg:.red.bold} [{bar:40.red/yellow}] Items: {pos}/{len} ({elapsed_precise})",
                    )?
                    .progress_chars("=> "),
            );
            pb.set_message(format!(
                "Deleting dir {}",
                path.file_name().unwrap_or_default().to_string_lossy()
            ));
            pb.enable_steady_tick(Duration::from_millis(200));
            
            fs::remove_dir_all(path).map_err(|e| io_err_with_path(e, path))?;
            items_deleted_count = total_items; 
            pb.set_position(items_deleted_count);
            pb.finish_with_message(format!("Deleted directory '{}'", path.display()));
        } else {
            if verbose {
                println!("Deleting file '{}'...", path.display());
            }
            fs::remove_file(path).map_err(|e| io_err_with_path(e, path))?;
            items_deleted_count = 1;
        }

        if verbose {
            println!(
                "Deletion of '{}' complete. {} items affected.",
                path.display(),
                items_deleted_count
            );
        }
        Ok(items_deleted_count)
    }

    pub fn handle_move_operation(
        source: PathBuf,
        destination: PathBuf,
        overwrite: bool,
        force_delete_source: bool, 
        parallel: bool,
        verbose: bool,
    ) -> Result<u64, AppError> {
        if verbose {
            println!(
                "Move operation: '{}' -> '{}'",
                source.display(),
                destination.display()
            );
        }
        if !source.exists() {
            return Err(AppError::SourceDoesNotExist(source.clone()));
        }

        let source_meta = fs::metadata(&source).map_err(|io_e| io_err_with_path(io_e, &source))?;
        let source_abs = source.absolutize().map_err(|e| io_err_with_path(e, &source))?.into_owned();

        let final_dest_target = if destination.exists()
            && fs::metadata(&destination)
                .map_err(|e| io_err_with_path(e, &destination))?
                .is_dir()
        {
            destination.join(
                source
                    .file_name()
                    .ok_or_else(|| AppError::NoFileName(source.clone()))?,
            )
        } else {
            destination.clone()
        };

        if source_meta.is_dir() {
            let target_abs_check = final_dest_target.absolutize().map_err(|e| io_err_with_path(e, &final_dest_target))?.into_owned();
            if target_abs_check.starts_with(&source_abs) {
                 return Err(AppError::RecursiveMoveOrCopy(source, final_dest_target));
            }
        }

        if final_dest_target.exists() && !overwrite {
            if source_meta.is_file() {
                 let dest_meta = fs::metadata(&final_dest_target).map_err(|e| io_err_with_path(e, &final_dest_target))?;
                 if dest_meta.is_file() {
                    return Err(AppError::DestinationExists(final_dest_target));
                 }
            } else if source_meta.is_dir() {
                let dest_meta = fs::metadata(&final_dest_target).map_err(|e| io_err_with_path(e, &final_dest_target))?;
                if dest_meta.is_file() {
                    return Err(AppError::DirToExistingFile { source_dir: source.clone(), dest_file: final_dest_target });
                }
                 return Err(AppError::DestinationExists(final_dest_target));
            }
        }

        match fs::rename(&source, &final_dest_target) {
            Ok(_) => {
                if verbose {
                    println!(
                        "Successfully moved (renamed) '{}' to '{}'",
                        source.display(),
                        final_dest_target.display()
                    );
                }
                Ok(1) 
            }
            Err(e) => {
                let should_fallback_to_copy_delete = e.kind() == ErrorKind::CrossesDevices
                    || e.raw_os_error() == Some(libc::EXDEV)
                    || (source_meta.is_file()
                        && destination.exists() 
                        && fs::metadata(&destination)
                            .map_err(|io_e| io_err_with_path(io_e, &destination))?
                            .is_dir());

                if should_fallback_to_copy_delete {
                    if verbose {
                        println!(
                            "Rename failed (reason: {}, OS error: {:?}), attempting copy then delete...",
                            e.kind(),
                            e.raw_os_error()
                        );
                    }
                    
                    let items_copied = handle_copy_operation_main(
                        &source,
                        &destination, 
                        overwrite,
                        parallel,
                        verbose,
                    )?;
                    if verbose {
                        println!(
                            "Copy phase of move complete. Now deleting source '{}'.",
                            source.display()
                        );
                    }

                    match handle_delete_operation(&source, force_delete_source, verbose) { 
                        Ok(_) => {
                            if verbose {
                                println!(
                                    "Source '{}' deleted successfully after copy.",
                                    source.display()
                                );
                            }
                            Ok(items_copied)
                        }
                        Err(del_err) => {
                            eprintln!("CRITICAL: Error deleting source '{}' after copy: {}. Copied files remain at '{}'. Manual cleanup of source may be required.", source.display(), del_err, destination.display());
                            Err(AppError::Io {
                                source: io::Error::new(
                                    ErrorKind::Other,
                                    "Failed to delete source after successful copy during move operation",
                                ),
                                path: source,
                            })
                        }
                    }
                } else {
                    Err(io_err_with_path(e, &source))
                }
            }
        }
    }
}

// --- Main Application Logic ---
fn main() -> Result<(), ()> {
    let cli = Cli::parse();

    let result: Result<u64, AppError> = match cli.command {
        Commands::Copy {
            source,
            destination,
            overwrite,
            parallel,
        } => core_logic::handle_copy_operation_main(
            &source,
            &destination,
            overwrite,
            parallel,
            cli.verbose,
        ),
        Commands::Move {
            source,
            destination,
            overwrite,
            force_delete_source,
            parallel,
        } => core_logic::handle_move_operation(
            source,
            destination,
            overwrite,
            force_delete_source,
            parallel,
            cli.verbose,
        ),
        Commands::Delete { path, force } => {
            core_logic::handle_delete_operation(&path, force, cli.verbose)
        }
    };

    match result {
        Ok(items_affected) => {
            if items_affected > 0 || cli.verbose {
                println!(
                    "Operation completed successfully. {} items affected.",
                    items_affected
                );
            } else if !cli.verbose {
                println!(
                    "Operation completed (no items affected or action skipped). Use --verbose for details."
                );
            }
            Ok(())
        }
        Err(e) => {
            eprintln!("Error: {}", e);
            if let AppError::ParallelOperationFailed(errors) = e {
                for (i, err_msg) in errors.iter().enumerate() {
                    eprintln!("  Parallel error {}: {}", i + 1, err_msg);
                }
            }
            Err(())
        }
    }
}
{% endcodeblock %}

## To Build and Run

1.  Save `src/main.rs` and `Cargo.toml`.
2.  Ensure Rust and build essentials are installed on your `arm64 Debian Bullseye` machine.
3.  Build: `cargo build --release`