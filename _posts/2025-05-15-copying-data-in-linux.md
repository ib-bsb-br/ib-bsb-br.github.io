---
tags: [scratchpad]
info: aberto.
date: 2025-05-15
type: post
layout: post
published: true
slug: copying-data-in-linux
title: 'Copying data in Linux'
---
Copying a large volume of data like 500GiB, especially when it consists of thousands of individual files, from an SD card to an external hard disk in Linux requires strategies that minimize overhead and maximize throughput. The key is to leverage parallel processing to utilize multiple CPU cores and choose tools that handle file operations efficiently.

**Understanding the Bottlenecks**

Before diving into tools, it's helpful to understand potential bottlenecks:
1.  **Per-File Overhead (CPU Bound):** When dealing with thousands of small files, the operating system incurs overhead for each file operation (opening, reading metadata, writing metadata, closing). This can make the CPU a bottleneck even if the drives aren't saturated. Parallel processing helps here.
2.  **I/O Throughput (Drive Bound):** The read speed of your SD card and the write speed of your external HDD (especially if it's a mechanical drive vs. an SSD) will ultimately limit transfer rates for large files or when per-file overhead is minimized.
3.  **Single-Threaded Operations:** Standard `cp` or `mv` commands are typically single-threaded, processing one file at a time, making them inefficient for this scale.

Here are several effective Linux tools and techniques to accomplish this task, focusing on speed and resource utilization:

**1. `rsync` with GNU `parallel` (Recommended for Robustness & Parallelism)**

`rsync` is a powerful and versatile tool for copying and synchronizing files. While `rsync` itself processes files sequentially within a single instance, you can use it with GNU `parallel` to run multiple `rsync` jobs concurrently, significantly speeding up the transfer of many files.

*   **How it Works:** `find` lists all files and directories. GNU `parallel` takes this list and launches multiple `rsync` processes, each handling a subset of the files/directories simultaneously. This leverages multiple CPU cores to manage the per-file operations and can better saturate your drive's I/O capabilities.
*   **Key Advantages:** Robust error handling, ability to resume interrupted transfers (with `rsync`), preserves permissions and metadata, detailed progress.
*   **Installation:** If `parallel` isn't installed: `sudo apt update && sudo apt install parallel` (Debian/Ubuntu) or `sudo dnf install parallel` (Fedora/RHEL).

**Example Command (Copying contents of source into destination):**

```bash
# Ensure destination directory exists: mkdir -p /media/user/externalhdd/backup_destination
find /media/user/sdcard/source_folder/ -mindepth 1 -print0 | \
  parallel -0 -j$(nproc) --eta --joblog /tmp/rsync_parallel.log \
  rsync -aP {} /media/user/externalhdd/backup_destination/
```

*   `/media/user/sdcard/source_folder/`: Your source directory on the SD card. The trailing slash means "contents of."
*   `-mindepth 1`: Excludes the top-level source directory itself from the list, processing its contents.
*   `-print0`: Handles filenames with spaces or special characters safely.
*   `parallel -0 -j$(nproc) --eta --joblog /tmp/rsync_parallel.log`:
    *   `-0`: Expects null-terminated input from `find`.
    *   `-j$(nproc)`: Runs a number of jobs equal to your CPU cores. You can set a specific number, e.g., `-j4`.
    *   `--eta`: Shows estimated time of arrival.
    *   `--joblog /tmp/rsync_parallel.log`: Logs the progress and success/failure of each parallel job.
*   `rsync -aP {} /media/user/externalhdd/backup_destination/`:
    *   `-a`: Archive mode (preserves permissions, timestamps, symbolic links, etc.).
    *   `-P`: Combines `--progress` and `--partial` (for resumability).
    *   `{}`: Placeholder for the file/directory passed by `parallel`.
    *   `/media/user/externalhdd/backup_destination/`: The destination. The trailing slash is important for `rsync` to copy items *into* this directory.

**Dry Run (Highly Recommended):** Before running the actual copy, perform a dry run:
Add `rsync -anP` (note the `n` for dry-run) in the command above, or add `--dry-run` to the `parallel` command.

**2. `tar` Pipelined (Efficient for Many Small Files)**

This classic method archives the source files into a single stream (`stdout`) and pipes this stream directly to another `tar` process that extracts it at the destination (`stdin`). This significantly reduces the overhead of individual file system operations, especially beneficial for mechanical drives and vast numbers of tiny files.

*   **How it Works:** `tar` reads all source files sequentially and writes them as a continuous data stream. The receiving `tar` process reads this stream and recreates the files and directory structure.
*   **Key Advantages:** Can be very fast for scenarios with extreme numbers of small files by minimizing disk head seeking.
*   **Considerations:** Less easily resumable if interrupted compared to `rsync`. Progress indication is often through tools like `pv` (Pipe Viewer).

**Example Command:**

```bash
# Ensure destination directory exists: mkdir -p /media/user/externalhdd/backup_destination
(cd /media/user/sdcard/source_folder/ && tar -cf - .) | pv | (cd /media/user/externalhdd/backup_destination/ && tar -xf -)
```

*   `(cd /media/user/sdcard/source_folder/ && tar -cf - .)`:
    *   `cd ...`: Changes to the source directory. The subshell `(...)` ensures this `cd` doesn't affect your main shell's working directory.
    *   `tar -cf - .`: Creates (`c`) an archive of the current directory (`.`) and writes it to standard output (`f -`).
*   `pv`: (Optional, install with `sudo apt install pv`) Pipe Viewer shows progress of data through the pipe.
*   `(cd /media/user/externalhdd/backup_destination/ && tar -xf -)`:
    *   `cd ...`: Changes to the destination directory in a subshell.
    *   `tar -xf -`: Extracts (`x`) the archive from standard input (`f -`).

**3. `find` with `xargs` and `cp --parents` (Parallel Basic Copy)**

This method uses `find` to locate files, and `xargs` to execute `cp` commands in parallel. The crucial `--parents` option for `cp` ensures the source directory structure is replicated at the destination.

*   **How it Works:** `find` generates a list of files. `xargs` takes this list and runs multiple `cp` commands simultaneously. `cp --parents` recreates the necessary parent directories at the destination.
*   **Key Advantages:** Uses standard `cp`, can be effective if `rsync`'s overhead is a concern for a simple copy.
*   **Considerations:** `cp` doesn't have `rsync`'s advanced resumability or delta-transfer capabilities (though not relevant for an initial full copy).

**Example Command:**

```bash
# Ensure base destination directory exists: mkdir -p /media/user/externalhdd/backup_destination
cd /media/user/sdcard/source_folder/ && \
  find . -type f -print0 | \
  xargs -0 -P$(nproc) -I {} cp --parents -a {} /media/user/externalhdd/backup_destination/
```

*   `cd /media/user/sdcard/source_folder/`: Change to the source directory to make relative paths work with `cp --parents`.
*   `find . -type f -print0`: Finds only files (`-type f`) in the current directory (`.`) and its subdirectories.
*   `xargs -0 -P$(nproc) -I {}`:
    *   `-0`: Null-terminated input.
    *   `-P$(nproc)`: Parallel processes up to the number of CPU cores.
    *   `-I {}`: Replaces `{}` with each input item. This makes `cp --parents` work correctly with paths containing spaces.
*   `cp --parents -a {} /media/user/externalhdd/backup_destination/`:
    *   `--parents`: Recreates the source directory structure under the destination.
    *   `-a`: Archive mode (like `rsync -a`, equivalent to `-dR --preserve=all`).
    *   `{}`: The file to copy.
    *   `/media/user/externalhdd/backup_destination/`: The target directory where the structure from `source_folder` will be created.

**4. `fpsync` (Specialized Parallel `rsync` Wrapper)**

`fpsync` is a tool designed to parallelize `rsync`. It uses `fpart` to partition the file list and then runs multiple `rsync` workers.

*   **How it Works:** Automates the process of splitting the workload and managing parallel `rsync` instances.
*   **Key Advantages:** Tailored for this exact scenario; can be very efficient.
*   **Installation:** May need to be installed via your package manager (e.g., `sudo apt install fpart`, as `fpsync` is often bundled with it).

**Example Command:**

```bash
# Ensure destination directory exists: mkdir -p /media/user/externalhdd/backup_destination
fpsync -n $(nproc) -v \
  /media/user/sdcard/source_folder/ /media/user/externalhdd/backup_destination/
```

*   `-n $(nproc)`: Number of parallel `rsync` workers (e.g., number of CPU cores).
*   `-v`: Verbose mode.
*   `/media/user/sdcard/source_folder/`: Source directory.
*   `/media/user/externalhdd/backup_destination/`: Destination directory.
*   **Note on batching:** `fpsync` uses `fpart` underneath. If you need to control batching by number of files per job (rather than just total workers), you might pass `fpart` options using `fpsync -o "-f <num_files>"`. Check `man fpart` for details.

**5. `mc` (Midnight Commander - TUI Alternative)**

For users who prefer a Text-based User Interface, Midnight Commander is a powerful console file manager. Its built-in copy operations (`F5`) are generally well-optimized and can handle large numbers of files more gracefully than a simple desktop file manager.

*   **How it Works:** Provides an interactive way to select source files/directories and copy them. While it might not offer the same granular parallel control as CLI combinations, it's often faster than basic `cp` for large jobs.
*   **Installation:** `sudo apt install mc` or `sudo dnf install mc`.
*   **Usage:** Run `mc`, navigate panels to source and destination, select files (e.g., `Insert` key or `*`), press `F5` to copy.

**Additional Considerations for Maximizing Speed:**

*   **Hardware:** Ensure both SD card reader and external HDD are connected to the fastest available USB ports (USB 3.0+). An SSD external drive will be significantly faster than a mechanical HDD.
*   **Filesystem Mount Options:** Mounting filesystems with `noatime` or `relatime` can reduce some disk I/O by not updating file access times on every read.
    `sudo mount -o remount,noatime /media/user/sdcard` (if applicable and safe for your use case).
*   **I/O Scheduler:** For mechanical drives, the I/O scheduler can matter. Modern kernels often default to `bfq` or `mq-deadline`, which are generally good.
*   **System Load:** Minimize other disk-intensive or CPU-intensive processes during the copy.
*   **Resource Monitoring:** Use tools like `iotop` (to see disk I/O per process), `htop` (CPU/memory), `vmstat`, or `dstat` to identify bottlenecks during the transfer.
*   **GUI `rsync` Front-ends:** If you prefer a GUI but want `rsync`'s power, tools like `grsync` provide a graphical interface to `rsync`.

**Which Method to Choose?**

*   **For general robustness, features, and good parallel performance:** `rsync` with GNU `parallel` (Method 1) or `fpsync` (Method 4) are excellent choices.
*   **For potentially the highest speed with extreme numbers of very small files (especially to/from mechanical drives):** The `tar` pipe (Method 2) can be very effective.
*   **For a simpler parallel `cp` approach:** `find` with `xargs` and `cp --parents` (Method 3) is a solid option.
*   **For an interactive TUI approach:** `mc` (Method 5) is user-friendly.

Always test with a smaller subset of your data and use dry-run options where available before committing to the full 500GiB transfer. This allows you to verify commands and estimate performance. Remember to replace placeholder paths with your actual SD card and external HDD mount points.