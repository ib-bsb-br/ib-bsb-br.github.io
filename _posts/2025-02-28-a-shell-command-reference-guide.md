---
tags: [scratchpad]
info: aberto.
date: 2025-02-28
type: post
layout: post
published: true
slug: a-shell-command-reference-guide
title: 'a-Shell Command Reference Guide'
---
# a-Shell Command Reference Guide

This guide aims to be a comprehensive listing of commands available within the a-Shell app for iOS.  It combines information from multiple sources and attempts to resolve any discrepancies.

## Table of Contents

- [File Management](#file-management)
- [Text Processing](#text-processing)
- [Shell Built-ins](#shell-built-ins)
- [Python Tools](#python-tools)
- [TeX and Document Processing](#tex-tools)
- [Networking Tools](#networking-tools)
- [Development Tools](#development-tools)
- [Compression and Archiving](#compression-archiving)
- [System Information](#system-information)
- [Web Browsers](#web-browsers)
- [a-Shell Specific Commands](#a-shell-commands)
- [Multimedia & Audio/Video](#multimedia)
- [Image Processing & Manipulation](#image-processing)
- [Version Control](#version-control)
- [Other Commands/Utilities](#other)
- [JavaScript  & JSON Processing](#javascript-json)
- [Machine Learning](#machine-learning)
- [GeoSpatial](#geospatial)
- [Font Management](#font-management)
- [Security](#security)
- [Clipboard](#clipboard)
- [Benchmarking](#benchmarking)
- [Documentation](#documentation)
- [MATLAB/Octave](#matlab-octave)
- [Build Systems](#build-systems)
- [WebAssembly](#webassembly)
- [Perl](#perl)
- [Lua](#lua)
- [Ruby](#ruby)
- [PHP](#php)
- [R](#r)
- [Text Editors](#text-editors)


### <a name="file-management"></a>File Management Commands

| Command | Description |
|---|---|
| `basename` | Extracts the filename from a given path.  Example: `basename /path/to/file.txt` returns `file.txt`. |
| `cat` | Concatenates and displays file contents. Example: `cat file.txt` |
| `cd` | Changes the current directory. Example: `cd /path/to/directory` |
| `chflags` | Changes file flags (macOS/Unix). Example: `chflags hidden file.txt` |
| `chmod` | Changes file permissions. Example: `chmod +x script.sh` |
| `cp` | Copies files and directories. Example: `cp file.txt new_file.txt` |
| `dirname` | Extracts the directory portion of a filepath. Example: `dirname /path/to/file.txt` returns `/path/to` |
| `du` | Estimates file space usage. Example: `du -h /path/to/directory` (for human-readable sizes) |
| `find` | Searches for files in a directory hierarchy. Example: `find . -name "*.txt"` |
| `head` | Displays the first few lines of a file. Example: `head file.txt` |
| `less` | Displays file contents with paging. Example: `less file.txt` |
| `ls` | Lists directory contents. Example: `ls -l` (for detailed listing) |
| `mkdir` | Creates directories. Example: `mkdir new_directory` |
| `more` | Displays file contents with paging. Example: `more file.txt` |
| `mv` | Moves or renames files and directories. Example: `mv file.txt new_location/` |
| `pwd` | Prints the current working directory. |
| `readlink` | Displays the target of a symbolic link. Example: `readlink link_to_file` |
| `rm` | Removes files or directories. Example: `rm file.txt` or `rm -r directory/` |
| `rmdir` | Removes empty directories. Example: `rmdir empty_directory/` |
| `send2trash` | Moves files to the trash/recycle bin (if supported). Example: `send2trash file.txt` |
| `stat` | Displays file or file system status. Example: `stat file.txt` |
| `tail` | Displays the last few lines of a file. Example: `tail file.txt` |
| `touch` | Creates empty files or updates timestamps. Example: `touch new_file.txt` |
| `unlink` | Removes files (similar to `rm`). Example: `unlink file.txt` |


[Back to Top](#table-of-contents)

<details>
  <summary>Click to expand the rest of the command list</summary>

### <a name="text-processing"></a>Text Processing Commands

| Command | Description |
|---|---|
| `awk` | Pattern-scanning and text-processing language. Example: `awk '{print $1}' file.txt` (prints the first field of each line) |
| `egrep` | Searches for lines matching a regular expression (extended grep). Example: `egrep "pattern" file.txt` |
| `fgrep` | Searches for lines matching a fixed string (fast grep). Example: `fgrep "string" file.txt` |
| `grep` | Searches for lines matching a pattern. Example: `grep "pattern" file.txt` |
| `multimarkdown` | Converts MultiMarkdown to HTML. Example: `multimarkdown file.md > file.html` |
| `piconv` | Converts text encodings. Example: `piconv -f utf-8 -t latin1 file.txt` |
| `sed` | Stream editor for filtering and transforming text. Example: `sed 's/old/new/g' file.txt` (replaces "old" with "new") |
| `sort` | Sorts lines of text files. Example: `sort file.txt` |
| `tr` | Translates or deletes characters. Example: `tr 'a-z' 'A-Z' < file.txt` (converts to uppercase) |
| `uniq` | Removes duplicate lines from sorted input. Example: `sort file.txt | uniq` |
| `wc` | Counts words, lines, and characters in files. Example: `wc file.txt` |
| `wordcloud_cli` | Generates word clouds. Example: `wordcloud_cli --text file.txt --imagefile wordcloud.png` |
| `xargs` | Builds and executes command lines from standard input. Example: `find . -name "*.txt" | xargs grep "pattern"` |


[Back to Top](#table-of-contents)


### <a name="shell-built-ins"></a>Shell Built-ins

| Command | Description |
|---|---|
| `alias` | Creates or displays aliases for commands. Example: `alias la="ls -la"` |
| `apropos` | Searches for commands by keyword in man pages. Example: `apropos search` |
| `bg` | Resumes a suspended job in the background. |
| `call` | Calls a shell function. Example: `call my_function` |
| `clear` | Clears the terminal screen. |
| `command` | Executes a command, bypassing aliases and functions. |
| `echo` | Displays a line of text. Example: `echo "Hello, world!"` |
| `env` | Displays or sets environment variables. Example: `env` or `env MY_VAR=value` |
| `eval` | Evaluates arguments as a shell command. |
| `exec` | Replaces the current shell with a command. |
| `exit` | Exits the current shell. |
| `export` | Sets environment variables. Example: `export MY_VAR=value` |
| `expr` | Evaluates expressions. Example: `expr 5 + 2` |
| `fg` | Brings a background job to the foreground. |
| `getopts` | Parses command-line options. |
| `hash` | Remembers the full path of commands. |
| `help` | Displays help information about commands. Example: `help cd` |
| `history` | Displays command history. |
| `jobs` | Lists active jobs. |
| `kill` | Sends a signal to a process. |
| `printenv` | Prints environment variables. |
| `read` | Reads a line from standard input. |
| `rehash` | Recreates the hash table of commands. |
| `return` | Exits a function. |
| `set` | Sets shell options. |
| `setenv` | Sets environment variables (csh style). |
| `shift` | Shifts positional parameters. |
| `sh` | Bourne shell interpreter. |
| `sleep` | Pauses execution for a specified time. Example: `sleep 5` (pauses for 5 seconds) |
| `source` | Executes a script in the current shell environment. Example: `source my_script.sh` |
| `stty` | Sets terminal characteristics. Example: `stty -echo` (disables echoing input) |
| `tee` | Reads from standard input, writes to standard output and files. Example: `command | tee output.txt` |
| `test` | Evaluates an expression (similar to `[ ]`). |
| `times` | Displays process times. |
| `trap` | Catches signals. |
| `true` | Returns true (exit status 0). |
| `type` | Displays the type of a command. Example: `type ls` |
| `ulimit` | Sets resource limits. |
| `umask` | Sets the default file creation mask. |
| `unalias` | Removes aliases. Example: `unalias la` |
| `unset` | Unsets variables and functions. |
| `unsetenv` | Unsets environment variables. Example: `unsetenv MY_VAR` |
| `wait` | Waits for a process to complete. |
| `whatis` | Displays one-line descriptions of commands. Example: `whatis ls` |


[Back to Top](#table-of-contents)


### <a name="python-tools"></a>Python Tools

| Command | Description |
|---|---|
| `2to3` | Converts Python 2 code to Python 3. Example: `2to3 -w my_script.py` |
| `2to3-3.11` | Converts Python 2 code to Python 3 (targeting Python 3.11). Example: `2to3-3.11 -w my_script.py` |
| `bokeh` | Python interactive visualization library.  Used to create interactive plots and visualizations. |
| `corelist` | Lists core Python packages. |
| `cython` | Optimizing static compiler for Python and the extended Cython programming language.  Used to create C extensions for Python. |
| `cythonize` | Compiles Cython code. Example: `cythonize my_module.pyx` |
| `deactivate` | Deactivates a Python virtual environment. |
| `docutils` | Python Documentation Utilities. Used to process reStructuredText and other documentation formats. |
| `f2py` | Fortran to Python interface generator.  Used to create Python interfaces for Fortran code. |
| `f2py3` | Fortran to Python 3 interface generator. |
| `f2py3.11` | Fortran to Python 3.11 interface generator. |
| `idle3` | Starts the IDLE Python IDE. |
| `idle3.11` | Starts the IDLE Python 3.11 IDE. |
| `import` | Imports a Python module (within scripts). Example: `import math` |
| `ipython` | Starts the IPython interactive shell. |
| `ipython3` | Starts the IPython 3 interactive shell. |
| `isympy` | Starts the SymPy console (symbolic mathematics in Python). |
| `nltk` | Natural Language Toolkit for Python. Used for natural language processing tasks. |
| `pip` | Python package installer. Example: `pip install requests` |
| `pip3` | Python 3 package installer. Example: `pip3 install numpy` |
| `pip3.10` | Python 3.10 package installer. |
| `pip3.11` | Python 3.11 package installer. |
| `pybabel` | Python internationalization library. Used for translating applications. |
| `pybind11-config` | Configuration tool for pybind11 (C++ bindings for Python). |
| `pydoc3` | Python 3 documentation tool. Example: `pydoc3 math` |
| `pydoc3.11` | Python 3.11 documentation tool. |
| `pyftmerge` | Merges font files (Python).  Part of the `fonttools` library. |
| `pyftsubset` | Creates subsets of font files (Python). Part of the `fonttools` library. |
| `pygmentize` | Python syntax highlighter. Used to add syntax highlighting to code snippets. |
| `pyjson5` | Python library for JSON5 (a superset of JSON). |
| `pyproj` | Python library for cartographic projections and coordinate transformations. |
| `python` | Python interpreter. Example: `python my_script.py` |
| `python3` | Python 3 interpreter. Example: `python3 my_script.py` |
| `python3-config` | Python 3 configuration tool.  Used to determine compiler and linker flags for building Python extensions. |
| `python3.11` | Python 3.11 interpreter. |
| `python3.11-config` | Python 3.11 configuration tool. |
| `python3.9` | Python 3.9 interpreter. |
| `qtpy` | Abstraction layer for PyQt and PySide (Qt bindings for Python).  Provides a consistent API for working with different Qt bindings. |
| `tqdm` | Progress bar library for Python.  Used to display progress bars for long-running operations. |
| `versioneer` | Tool for managing versions in Python projects.  Automates versioning tasks. |
| `wheel` | Python wheel builder. Used to create wheel packages for distribution. |


[Back to Top](#table-of-contents)


### <a name="tex-tools"></a>TeX and Document Processing

| Command | Description |
|---|---|
| `amstex` | Compiles LaTeX documents using the AMS-TeX package (provides additional mathematical symbols and formatting). |
| `bibtex` | Formats bibliographies for LaTeX documents. Example: `bibtex my_document.aux` |
| `cslatex` | Compiles LaTeX documents with Czech/Slovak support. |
| `csplain` | Processes TeX documents with Czech/Slovak support. |
| `dvilualatex` | Compiles LaTeX documents using LuaLaTeX and outputs a DVI file. |
| `dviluatex` | Compiles LaTeX documents using LuaTeX and outputs a DVI file. |
| `dvipdfmx` | Converts DVI files to PDF. Example: `dvipdfmx my_document.dvi` |
| `eplain` | Processes TeX documents using the eplain format. |
| `etex` | An extended version of TeX. |
| `euptex` | Processes TeX documents with Japanese support (euptex). |
| `fmtutil` | Generates TeX format files.  Used to create new formats for TeX. |
| `fmtutil-sys` | Generates TeX format files (system-wide). |
| `jadetex` | Processes LaTeX documents using JadeTeX. |
| `kpsewhich` | Locates TeX files. Example: `kpsewhich my_style.sty` |
| `latex` | Compiles LaTeX documents. Example: `latex my_document.tex` |
| `luahbtex` | Processes LaTeX documents using LuaHBTeX. |
| `lualatex` | Processes LaTeX documents using LuaLaTeX. Example: `lualatex my_document.tex` |
| `luatex` | Processes LaTeX documents using LuaTeX. |
| `makeindex` | Generates indexes for LaTeX documents. Example: `makeindex my_document.idx` |
| `mktexfmt` | Creates TeX format files. |
| `mktexlsr` | Creates TeX font map files. |
| `mllatex` | Processes LaTeX documents using MLTeX. |
| `mltex` | Processes TeX documents using MLTeX. |
| `pdfcslatex` | Processes LaTeX documents using pdfcslatex (with Czech/Slovak support) and outputs a PDF file. |
| `pdfcsplain` | Processes TeX documents using pdfcsplain (with Czech/Slovak support) and outputs a PDF file. |
| `pdfetex` | Processes LaTeX documents using pdfeTeX and outputs a PDF file. |
| `pdfjadetex` | Processes LaTeX documents using pdfJadeTeX and outputs a PDF file. |
| `pdflatex` | Processes LaTeX documents using pdfLaTeX and outputs a PDF file. Example: `pdflatex my_document.tex` |
| `pdfmex` | Processes LaTeX documents using pdfmex and outputs a PDF file. |
| `pdftex` | Processes TeX documents using pdfTeX and outputs a PDF file. |
| `pdfxmltex` | Processes LaTeX documents using pdfxmltex and outputs a PDF file. |
| `splain` | Processes TeX documents using splain. |
| `tex` | Processes TeX documents. Example: `tex my_document.tex` |
| `texlua` | Lua interpreter for TeX. |
| `texluac` | Lua compiler for TeX. |
| `texsis` | TeXsis formatting engine. |
| `tlmgr` | TeX Live Manager. Used to manage TeX Live installations. |
| `updmap` | Updates TeX font maps. |
| `updmap-sys` | Updates TeX font maps (system-wide). |
| `uplatex` | Processes LaTeX documents using upLaTeX (with Japanese support). |
| `uptex` | Processes TeX documents using upTeX (with Japanese support). |
| `xdvipdfmx` | Converts DVI files to PDF. |
| `xelatex` | Processes LaTeX documents using XeLaTeX. Example: `xelatex my_document.tex` |
| `xetex` | Processes TeX documents using XeTeX. |
| `xmltex` | Processes TeX documents using xmltex. |


[Back to Top](#table-of-contents)


### <a name="networking-tools"></a>Networking Tools

| Command | Description |
|---|---|
| `curl` | Transfers data with URLs. Supports various protocols (HTTP, FTP, SFTP, etc.). Example: `curl https://www.example.com` |
| `dig` | DNS lookup utility. Example: `dig example.com` |
| `host` | Performs DNS lookups. Example: `host example.com` |
| `httpx` | Modern HTTP client for Python.  Used for making HTTP requests. |
| `ifconfig` | Displays and configures network interfaces. Example: `ifconfig` |
| `nc` | Netcat - network utility for reading/writing data across network connections. Example: `nc -l 8080` (listens on port 8080) |
| `nslookup` | Queries DNS servers. Example: `nslookup example.com` |
| `ping` | Tests network connectivity using ICMP echo requests. Example: `ping example.com` |
| `ping6` | Tests IPv6 network connectivity. Example: `ping6 google.com` |
| `rlogin` | Remote login. Example: `rlogin user@host` |
| `scp` | Securely copies files between hosts. Example: `scp file.txt user@host:/path/to/destination` |
| `sftp` | Secure File Transfer Protocol client. Example: `sftp user@host` |
| `ssh` | Secure Shell client. Example: `ssh user@host` |
| `ssh-add` | Adds SSH keys to the SSH agent. Example: `ssh-add ~/.ssh/id_rsa` |
| `ssh-agent` | SSH agent. Manages SSH keys. |
| `ssh-copy-id` | Copies SSH keys to a remote server. Example: `ssh-copy-id user@host` |
| `ssh-keygen` | Generates SSH keys. Example: `ssh-keygen -t rsa` |
| `telnet` | Telnet client. Example: `telnet host` |
| `whois` | Retrieves domain registration information. Example: `whois example.com` |
| `wol` | Wake-on-LAN tool. Used to wake up computers remotely. |
| `wsdump` | Dumps WebSocket traffic.  Used for debugging WebSocket connections. |


[Back to Top](#table-of-contents)


### <a name="development-tools"></a>Development Tools


| Command | Description |
|---|---|
| `ctags.wasm3` | Generates an index (tags file) of language objects found in source files (compiled to WebAssembly). |
| `clang` | C language compiler. Example: `clang my_program.c -o my_program` |
| `clang++` | C++ compiler. Example: `clang++ my_program.cpp -o my_program` |
| `cygdb` | Debugger for Cython code. |
| `file.wasm3` | Determines file type (compiled to WebAssembly). |
| `ld` | The GNU linker. Example: `ld -o my_program my_object_file.o` |
| `ld.lld` | The LLVM linker. |
| `ld64.lld` | The LLVM linker (64-bit). |
| `lex` | Lexical analyzer generator. Used to create lexers for compilers and interpreters. |
| `link` | Creates hard links between files. Example: `link original_file linked_file` |
| `llc` | LLVM static compiler. |
| `lld` | LLVM linker. |
| `lld-link` | LLVM linker (alternative command). |
| `lli` | LLVM interpreter. |
| `llvm-dis` | LLVM disassembler. |
| `llvm-link` | LLVM linker. |
| `make` | Automates software build processes. Example: `make` |
| `mktemp.wasm3` | Creates temporary files (compiled to WebAssembly). |
| `meson` | Meson build system.  A modern build system for C/C++ and other languages. |
| `opt` | Compiler optimization options (LLVM). |
| `ranlib` | Generates or updates index for static libraries. Example: `ranlib my_library.a` |
| `readtags.wasm3` | Reads ctags output (compiled to WebAssembly). |
| `tree.wasm3` | Displays a tree view of directories (compiled to WebAssembly). |
| `wamr` | WebAssembly runtime. |
| `wasm` | WebAssembly tool. |
| `wasm-ld` | WebAssembly linker. |
| `wasm3` | WebAssembly interpreter. |
| `wasmer` | WebAssembly runtime. |
| `xz.wasm3` | XZ compressor (compiled to WebAssembly). |
| `xzdec.wasm3` | XZ decompressor (compiled to WebAssembly). |

[Back to Top](#table-of-contents)


### <a name="compression-archiving"></a>Compression and Archiving

| Command | Description |
|---|---|
| `ar` | Creates, modifies, and extracts from archives (static libraries). Example: `ar rcs my_library.a object_file1.o object_file2.o` |
| `compress` | Compresses files using Lempel-Ziv coding. Example: `compress file.txt` (creates file.txt.Z) |
| `gunzip` | Decompresses gzip files. Example: `gunzip file.txt.gz` |
| `gzip` | Compresses files using gzip. Example: `gzip file.txt` (creates file.txt.gz) |
| `ptar` | Parallel tar (may offer improved performance for large archives).  Example: `ptar -cvf archive.tar files/` |
| `ptardiff` | Compares tar archives. |
| `ptargrep` | Searches within tar archives. |
| `tar` | Creates and manipulates archive files. Example: `tar -cvf archive.tar file1 file2 directory/` |
| `uncompress` | Decompresses files compressed with `compress`. Example: `uncompress file.txt.Z` |
| `unrar` | Extracts RAR archives. Example: `unrar x archive.rar` |
| `xz` | XZ compression utility. Example: `xz file.txt` (creates file.txt.xz) |
| `z` | Compresses files (same as `compress`). |
| `zip` | Creates zip archives. Example: `zip archive.zip file1 file2 directory/` |
| `zipdetails` | Shows details of zip archives.  Example: `zipdetails archive.zip` |


[Back to Top](#table-of-contents)


### <a name="system-information"></a>System Information

| Command | Description |
|—|—|
| `date` | Displays current date and time. Example: `date` |
| `distro` | Displays Linux distribution information (may not be fully functional on iOS). |
| `id` | Displays user and group IDs. Example: `id` |
| `sw_vers` | Displays macOS software version information (may not be applicable on all iOS versions). |
| `uname` | Displays system information. Example: `uname -a` |
| `uptime` | Displays system uptime. Example: `uptime` |
| `whoami` | Displays current username. Example: `whoami` |


[Back to Top](#table-of-contents)


### <a name=“web-browsers”></a>Web Browsers

| Command | Description |
|—|—|
| `brave` | Opens the Brave web browser (if installed). |
| `firefox` | Opens the Firefox web browser (if installed). |
| `googlechrome` | Opens the Google Chrome web browser (if installed). |
| `opera` | Opens the Opera web browser (if installed). |
| `safari` | Opens the Safari web browser (if installed). |
| `yandexbrowser` | Opens the Yandex browser (if installed). |


[Back to Top](#table-of-contents)


### <a name=“a-shell-commands”></a>a-Shell Specific Commands

| Command | Description |
|—|—|
| `bookmark` | Bookmarks the current directory. Example: `bookmark my_project` |
| `config` | Configures a-Shell settings.  Opens the a-Shell settings interface. |
| `deletemark` | Deletes a bookmark. Example: `deletemark my_project` |
| `downloadFile` | Downloads a file using `curl`. Example: `downloadFile https://www.example.com/file.txt` |
| `downloadFolder` | Downloads a folder/directory. Example: `downloadFolder https://www.example.com/my_folder/` |
| `hideKeyboard` | Hides the on-screen keyboard. |
| `hideToolbar` | Hides the a-Shell toolbar. |
| `internalbrowser` | Opens the internal web browser.  Opens a web browser within the a-Shell app. |
| `isForeground` | Checks if a-Shell is currently in the foreground.  Returns true or false. |
| `jump` | Jumps to a bookmarked directory. Example: `jump my_project` |
| `keepDirectoryAfterShortcut` | Keeps the current directory after running a shortcut.  Prevents the directory from changing after a shortcut execution. |
| `newWindow` | Opens a new a-Shell window. |
| `open` | Opens files or URLs. Example: `open file.txt` or `open https://www.example.com` |
| `openurl` | Opens a URL. Example: `openurl https://www.example.com` |
| `pickFolder` | Opens a file picker to select a folder.  Allows the user to interactively choose a folder. |
| `pkg` | Installs a-Shell packages. Example: `pkg install git` |
| `renamemark` | Renames a bookmark. Example: `renamemark old_name new_name` |
| `showmarks` | Shows saved bookmarks.  Lists all currently saved bookmarks. |
| `showToolbar` | Shows the a-Shell toolbar. |
| `stream` | Streams data to a command.  Pipes data to a command’s standard input. |
| `streamzip` | Streams a zip archive.  Streams the contents of a zip archive to another command. |
| `updateCommands` | Updates a-Shell commands.  Checks for and installs updates to the available commands. |
| `view` | Views files (may open in a default viewer). Example: `view image.jpg` |


[Back to Top](#table-of-contents)


### <a name=“multimedia”></a>Multimedia & Audio/Video

| Command | Description |
|—|—|
| `ffmpeg` | Command-line tool for manipulating video and audio. Example: `ffmpeg -i input.mp4 output.webm` |
| `ffprobe` | Command-line tool to analyze multimedia streams. Example: `ffprobe input.mp4` |
| `play` | Plays media files. Example: `play music.mp3` |


[Back to Top](#table-of-contents)


### <a name=“image-processing”></a>Image Processing & Manipulation

| Command | Description |
|—|—|
| `compare` | Compares two images (ImageMagick). Example: `compare image1.jpg image2.jpg difference.png` |
| `composite` | Combines images (ImageMagick). Example: `composite image1.png image2.png -gravity center output.png` |
| `convert` | Converts images between formats (ImageMagick). Example: `convert image.jpg image.png` |
| `fits2bitmap` | Converts FITS (Flexible Image Transport System) astronomical image files to bitmaps. |
| `fitscheck` | Checks the integrity of FITS files. |
| `fitsdiff` | Compares FITS files. |
| `fitsheader` | Displays the header of a FITS file. |
| `fitsinfo` | Displays information about a FITS file. |
| `identify` | Identifies image properties (ImageMagick). Example: `identify image.jpg` |
| `magick-script` | ImageMagick scripting interface. |
| `mogrify` | Modifies images in-place (ImageMagick). Example: `mogrify -resize 50% image.jpg` |
| `montage` | Creates composite images from multiple images (ImageMagick). Example: `montage image1.jpg image2.jpg image3.jpg output.png` |


[Back to Top](#table-of-contents)


### <a name=“version-control”></a>Version Control

| Command | Description |
|—|—|
| `lg2` | Git-like version control system optimized for size.  Provides basic version control functionality. |


[Back to Top](#table-of-contents)


### <a name=“other”></a>Other Commands/Utilities

| Command | Description |
|—|—|
| `blink` | Makes text blink (may not be supported in all terminals). |
| `cowsay` | Makes a cow say things (ASCII art). Example: `cowsay “Hello”` |
| `dash` | Documentation browser.  Provides access to documentation for various commands and libraries. |
| `ebong` | Purpose unclear (non-standard command). |
| `fonttools` | Python library for manipulating font files.  Used for font processing tasks. |
| `l4p-tmpl` | Purpose unclear (non-standard command). |
| `libnetcfg` | Network configuration library (macOS/Unix). |
| `mandoc` | Formats and displays manual pages. Example: `mandoc manpage.1` |
| `mandocdb` | Creates and manages a manual page database. |
| `mercantile` | Command-line interface for working with map tiles.  Used for geospatial data processing. |
| `samp_hub` | Purpose unclear (non-standard command). |
| `say` | Speaks text aloud (text-to-speech). Example: `say “Hello”` |
| `showtable` | Purpose unclear (non-standard command). |
| `task` | Task management (a-Shell specific?).  May provide task management features within a-Shell. |
| `ttx` | Tool for working with TrueType fonts.  Used for font conversion and manipulation. |
| `volint` | Purpose unclear (non-standard command). |
| `wcslint` | Purpose unclear (non-standard command). |
| `xcode-select` | Manages Xcode installations (macOS).  Used to switch between different Xcode versions. |
| `xxd` | Creates a hex dump of a file. Example: `xxd file.txt` |

[Back to Top](#table-of-contents)

### <a name=“javascript-json”></a>JavaScript & JSON Processing

| Command | Description |
|—|—|
| `jq` | Command-line JSON processor. Example: `jq ‘.name’` data.json (extracts the value of the “name” field) |
| `jsc` | JavaScript interpreter (JavaScriptCore). Example: `jsc my_script.js` |
| `jsc_core` | JavaScriptCore interpreter. |
| `jsi` | JavaScript interpreter. |
| `json_pp` | Pretty-prints JSON data. Example: `echo ‘{“name”:”John”, “age”:30}’ | json_pp` |
| `jsonpointer` | JSON Pointer query tool.  Used to extract specific values from JSON data using JSON Pointers. |
| `jsonschema` | JSON Schema validation tool.  Used to validate JSON data against a JSON Schema. |

[Back to Top](#table-of-contents)


### <a name=“machine-learning”></a>Machine Learning

| Command | Description |
|—|—|
| `jlpm` | Julia package manager (may have limited functionality within a-Shell).  Used to manage Julia packages. |

[Back to Top](#table-of-contents)


### <a name=“geospatial”></a>GeoSpatial

| Command | Description |
|—|—|
| `rio` | Command-line interface for rasterio (geospatial data processing).  Used to process geospatial raster data. |

[Back to Top](#table-of-contents)


### <a name=“font-management”></a>Font Management

| Command | Description |
|—|—|
| `pyftmerge` | Merges font files (Python). Part of the `fonttools` library. |
| `pyftsubset` | Creates subsets of font files (Python). Part of the `fonttools` library. |

[Back to Top](#table-of-contents)


### <a name=“security”></a>Security

| Command | Description |
|—|—|
| `ssh-add` | Adds SSH keys to the SSH agent. |
| `ssh-agent` | SSH agent. |
| `ssh-copy-id` | Copies SSH keys to a remote server. |
| `ssh-keygen` | Generates SSH keys. |

[Back to Top](#table-of-contents)


### <a name=“clipboard”></a>Clipboard

| Command | Description |
|—|—|
| `pbcopy` | Copies data to the system clipboard. Example: `echo “text to copy” | pbcopy` |
| `pbpaste` | Pastes data from the system clipboard. Example: `pbpaste` |

[Back to Top](#table-of-contents)


### <a name=“benchmarking”></a>Benchmarking

| Command | Description |
|—|—|
| `fio` | Flexible I/O tester. Used to benchmark storage performance. |

[Back to Top](#table-of-contents)


### <a name=“documentation”></a>Documentation

| Command | Description |
|---|---|
| `man` | Displays manual pages for commands. Example: `man ls` |
| `perldoc` | Displays Perl documentation. |
| `pydoc3` | Python 3 documentation tool. |
| `pydoc3.11` | Python 3.11 documentation tool. |

[Back to Top](#table-of-contents)


### <a name="matlab-octave"></a>MATLAB/Octave

| Command | Description |
|---|---|
| `mex` | MATLAB executable. |
| `utf8mex` | MATLAB utility for UTF-8 encoding. |

[Back to Top](#table-of-contents)


### <a name="build-systems"></a>Build Systems

| Command | Description |
|---|---|
| `make` | Automates software build processes. |
| `meson` | Meson build system. |

[Back to Top](#table-of-contents)


### <a name="webassembly"></a>WebAssembly

| Command | Description |
|---|---|
| `wamr` | WebAssembly runtime. |
| `wasm` | WebAssembly tool. |
| `wasm-ld` | WebAssembly linker. |
| `wasm3` | WebAssembly interpreter. |
| `wasmer` | WebAssembly runtime. |

[Back to Top](#table-of-contents)


### <a name="perl"></a>Perl

| Command | Description |
|---|---|
| `cpan` | Comprehensive Perl Archive Network (CPAN) module installer. |
| `enc2xs` | Converts encoded Perl scripts to XS. |
| `encguess` | Guesses file encoding (often used with Perl). |
| `h2ph` | Converts C header files to Perl header files. |
| `h2xs` | Converts C header files to Perl extensions. |
| `instmodsh` | Installs Perl modules. |
| `perl` | Perl interpreter. |
| `perl5` | Perl 5 interpreter. |
| `perlbug` | Reports Perl bugs. |
| `perldoc` | Displays Perl documentation. |
| `perlivp` | Perl interactive version pragma. |
| `pl2pm` | Converts Perl libraries to modules. |
| `pod2html` | Converts POD (Plain Old Documentation) to HTML. |
| `prove` | Runs Perl tests. |
| `xsubpp` | Converts XS code to C. |

[Back to Top](#table-of-contents)


### <a name="lua"></a>Lua

| Command | Description |
|---|---|
| `lua` | Lua interpreter. Example: `lua my_script.lua` |
| `luac` | Lua compiler. |

[Back to Top](#table-of-contents)


### <a name="ruby"></a>Ruby (If installed)

| Command | Description |
|---|---|
| `irb` | Interactive Ruby Shell. |
| `rake` | Ruby build tool (similar to Make). |
| `gem` | RubyGems package manager. |
| `ruby` | Ruby interpreter. |

[Back to Top](#table-of-contents)

### <a name="php"></a>PHP (If installed)

| Command | Description |
|---|---|
| `php` | PHP interpreter. |
| `composer` | PHP dependency manager. |

[Back to Top](#table-of-contents)

### <a name="r"></a>R (If installed)

| Command | Description |
|---|---|
| `R` | R interpreter. |

[Back to Top](#table-of-contents)

### <a name="text-editors"></a>Text Editors

| Command | Description |
|---|---|
| `ed` | Line-oriented text editor. |
| `nano` | Text editor (if installed). |
| `pico` | Simple text editor. |
| `vim` | Vim text editor. |

[Back to Top](#table-of-contents)


### <a name="jupyter"></a>Jupyter

| Command | Description |
|---|---|
| `jupyter` | Jupyter command-line interface.  Provides a command-line interface for managing Jupyter notebooks and other Jupyter components. |
| `jupyter-bundlerextension` | Manages Jupyter bundler extensions.  Used to install and manage extensions for Jupyter bundlers. |
| `jupyter-console` | Jupyter console.  Provides a terminal-based console for interacting with Jupyter kernels. |
| `jupyter-contrib` | Jupyter contrib tools.  A collection of community-contributed tools and extensions for Jupyter. |
| `jupyter-dejavu` | Jupyter DejaVu extension.  Provides tools for exploring and visualizing code execution history. |
| `jupyter-events` | Jupyter events tools.  Used to manage and process Jupyter events. |
| `jupyter-execute` | Jupyter execute tools.  Used to execute code in Jupyter notebooks and other Jupyter environments. |
| `jupyter-kernel` | Manages Jupyter kernels.  Used to install, list, and manage Jupyter kernels for different programming languages. |
| `jupyter-kernelspec` | Manages Jupyter kernel specifications.  Used to manage the specifications that define Jupyter kernels. |
| `jupyter-lab` | JupyterLab interface.  Provides a web-based user interface for working with Jupyter notebooks, code, and data. |
| `jupyter-labextension` | Manages JupyterLab extensions.  Used to install and manage extensions for JupyterLab. |
| `jupyter-labhub` | JupyterLab hub tools.  Used to manage and configure JupyterLab hubs. |
| `jupyter-migrate` | Migrates Jupyter notebooks.  Used to migrate notebooks to newer versions of Jupyter. |
| `jupyter-nbclassic` | Jupyter Notebook classic interface.  Provides the classic web-based interface for Jupyter notebooks. |
| `jupyter-nbclassic-bundlerextension` | Manages Jupyter Notebook classic bundler extensions. |
| `jupyter-nbclassic-extension` | Manages Jupyter Notebook classic extensions. |
| `jupyter-nbclassic-serverextension` | Manages Jupyter Notebook classic server extensions. |
| `jupyter-nbconvert` | Converts Jupyter notebooks to other formats (e.g., HTML, PDF, Markdown). Example: `jupyter nbconvert --to html my_notebook.ipynb` |
| `jupyter-nbextension` | Manages Jupyter Notebook extensions.  Used to install and manage extensions for Jupyter Notebook. |
| `jupyter-nbextensions_configurator` | Configures Jupyter Notebook extensions.  Provides a graphical interface for configuring Jupyter Notebook extensions. |
| `jupyter-notebook` | Jupyter Notebook interface.  Starts the Jupyter Notebook server. |
| `jupyter-qtconsole` | Jupyter Qt console.  Provides a Qt-based console for interacting with Jupyter kernels. |
| `jupyter-run` | Runs Jupyter notebooks.  Executes the code in a Jupyter notebook. |
| `jupyter-server` | Jupyter server tools.  Used to manage and configure Jupyter servers. |
| `jupyter-serverextension` | Manages Jupyter server extensions.  Used to install and manage extensions for Jupyter servers. |
| `jupyter-troubleshoot` | Jupyter troubleshooting tools.  Provides tools for troubleshooting Jupyter installations and issues. |
| `jupyter-trust` | Manages trusted Jupyter notebooks.  Used to mark notebooks as trusted to allow execution of potentially unsafe code. |


[Back to Top](#table-of-contents)