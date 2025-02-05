---
tags: [scratchpad, scripts>python]
info: aberto.
date: 2025-02-05
type: post
layout: post
published: true
slug: files-to-prompt-ftppy
title: 'files-to-prompt ftp.py'
---
<?xml version="1.0" encoding="utf-8"?>
<opml version="2.0">
<head><title>Untitledftp</title></head>
<body><outline text=""><outline text="#!/usr/bin/env python
import os
import sys
import click
import shutil
import zipfile
import tarfile
import logging
import tempfile
from fnmatch import fnmatch

# Attempt rarfile and py7zr imports
try:
    import rarfile
except ImportError:
    rarfile = None

try:
    import py7zr
except ImportError:
    py7zr = None

# Attempt pathspec import
try:
    import pathspec
    pathspec_available = True
except ImportError:
    pathspec_available = False

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

ARCHIVE_HANDLERS = {
    &quot;.zip&quot;: &quot;handle_zip&quot;,
    &quot;.rar&quot;: &quot;handle_rar&quot;,
    &quot;.7z&quot;: &quot;handle_7z&quot;,
    &quot;.tar&quot;: &quot;handle_tar&quot;,
    &quot;.gz&quot;: &quot;handle_tar&quot;,
    &quot;.bz2&quot;: &quot;handle_tar&quot;,
}

OFFICE_EXTENSIONS = [
    &quot;.docx&quot;,
    &quot;.xlsx&quot;,
    &quot;.pptx&quot;,
    &quot;.odt&quot;,
    &quot;.ods&quot;,
    &quot;.odp&quot;,
]

class GitignoreHandler:
    &quot;&quot;&quot;Handles .gitignore rules in two ways:
       1) uses pathspec if installed,
       2) falls back to basic fnmatch approach otherwise.&quot;&quot;&quot;
    def __init__(self):
        self.spec = None
        self.rules = []

    def load(self, directory):
        gitignore_path = os.path.join(directory, &quot;.gitignore&quot;)
        if os.path.isfile(gitignore_path):
            with open(gitignore_path, &quot;r&quot;, encoding=&quot;utf-8&quot;) as f:
                lines = [
                    line.strip() for line in f
                    if line.strip() and not line.startswith(&quot;#&quot;)
                ]
            if pathspec_available:
                self.spec = pathspec.PathSpec.from_lines(&quot;gitwildmatch&quot;, lines)
            else:
                self.rules.extend(lines)

    def should_ignore(self, path):
        if self.spec:
            # pathspec matches relative paths by default
            return self.spec.match_file(path)
        else:
            base = os.path.basename(path)
            if os.path.isdir(path):
                base += &quot;/&quot;
            for rule in self.rules:
                if fnmatch(base, rule):
                    return True
            return False


def handle_zip(file_path, extract_dir):
    try:
        with zipfile.ZipFile(file_path, &quot;r&quot;) as zf:
            zf.extractall(extract_dir)
        return True
    except zipfile.BadZipFile as e:
        logger.warning(f&quot;Failed to extract ZIP: {file_path} ({e})&quot;)
        return False


def handle_rar(file_path, extract_dir):
    if rarfile is None:
        logger.warning(&quot;RAR support not installed. &apos;rarfile&apos; required.&quot;)
        return False
    try:
        with rarfile.RarFile(file_path, &quot;r&quot;) as rf:
            rf.extractall(extract_dir)
        return True
    except rarfile.Error as e:
        logger.warning(f&quot;Failed to extract RAR: {file_path} ({e})&quot;)
        return False


def handle_7z(file_path, extract_dir):
    if py7zr is None:
        logger.warning(&quot;7z support not installed. &apos;py7zr&apos; required.&quot;)
        return False
    try:
        with py7zr.SevenZipFile(file_path, mode=&quot;r&quot;) as sz:
            sz.extractall(path=extract_dir)
        return True
    except py7zr.exceptions.Bad7zFile as e:
        logger.warning(f&quot;Failed to extract 7Z: {file_path} ({e})&quot;)
        return False


def handle_tar(file_path, extract_dir):
    try:
        with tarfile.open(file_path, &quot;r:*&quot;) as tf:
            tf.extractall(extract_dir)
        return True
    except tarfile.TarError as e:
        logger.warning(f&quot;Failed to extract TAR: {file_path} ({e})&quot;)
        return False


def decompress_file(file_path, extension):
    &quot;&quot;&quot;Extract the archive or document into a temporary directory and return that directory path.&quot;&quot;&quot;
    tmpdir = tempfile.mkdtemp()
    handler_name = ARCHIVE_HANDLERS.get(extension.lower())
    if extension.lower() in OFFICE_EXTENSIONS:
        handler_name = &quot;handle_zip&quot;

    if handler_name is None:
        logger.warning(f&quot;No handler for extension {extension} in file {file_path}&quot;)
        shutil.rmtree(tmpdir)
        return None

    handler_func = globals()[handler_name]
    success = handler_func(file_path, tmpdir)
    if success:
        return tmpdir
    else:
        shutil.rmtree(tmpdir)
        return None


class FileProcessor:
    &quot;&quot;&quot;Handles recursive file/directory processing with optional .gitignore usage, archiving, etc.&quot;&quot;&quot;
    def __init__(self, extensions, include_hidden, ignore_gitignore, ignore_patterns, output_xml, writer, max_depth):
        self.extensions = [ext.lower() for ext in extensions]
        self.include_hidden = include_hidden
        self.ignore_gitignore = ignore_gitignore
        self.ignore_patterns = ignore_patterns
        self.output_xml = output_xml
        self.writer = writer
        self.max_depth = max_depth
        self.xml_index = 1

    def process_path(self, path, depth=0, gitignore_handler=None):
        if depth > self.max_depth:
            logger.warning(f&quot;Maximum recursion depth ({self.max_depth}) reached for {path}&quot;)
            return

        if os.path.isfile(path):
            self._handle_file(path, depth)
        elif os.path.isdir(path):
            if not gitignore_handler and not self.ignore_gitignore:
                gitignore_handler = GitignoreHandler()
                gitignore_handler.load(path)
            self._handle_directory(path, depth, gitignore_handler)

    def _handle_file(self, path, depth):
        _, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext in ARCHIVE_HANDLERS or ext in OFFICE_EXTENSIONS:
            extracted = decompress_file(path, ext)
            if extracted:
                try:
                    self.process_path(extracted, depth=depth+1)
                finally:
                    shutil.rmtree(extracted)
        else:
            self._print_file_content(path)

    def _handle_directory(self, dir_path, depth, gitignore_handler):
        for root, dirs, files in os.walk(dir_path):
            if not self.include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith(&quot;.&quot;)]
                files = [f for f in files if not f.startswith(&quot;.&quot;)]

            if gitignore_handler:
                for d in list(dirs):
                    full_d = os.path.join(root, d)
                    gitignore_handler.load(root)
                    if gitignore_handler.should_ignore(full_d):
                        dirs.remove(d)
                new_files = []
                for f in files:
                    full_f = os.path.join(root, f)
                    if not gitignore_handler.should_ignore(full_f):
                        new_files.append(f)
                files = new_files

            if self.ignore_patterns:
                files = [
                    f for f in files
                    if not any(fnmatch(f, pattern) for pattern in self.ignore_patterns)
                ]

            if self.extensions:
                files = [
                    f for f in files
                    if any(f.lower().endswith(ext) for ext in self.extensions)
                ]

            for filename in sorted(files):
                fpath = os.path.join(root, filename)
                self.process_path(fpath, depth + 1, gitignore_handler)

    def _print_file_content(self, path):
        try:
            with open(path, &quot;r&quot;, encoding=&quot;utf-8&quot;) as f:
                content = f.read()
            self._print_content(path, content)
        except UnicodeDecodeError:
            try:
                with open(path, &quot;r&quot;, encoding=&quot;latin-1&quot;) as f:
                    content = f.read()
                self._print_content(path, content)
            except Exception as e:
                logger.warning(f&quot;Could not read file {path} with fallback encoding: {e}&quot;)
        except Exception as e:
            logger.warning(f&quot;Could not read file {path}: {e}&quot;)

    def _print_content(self, path, content):
        if self.output_xml:
            self.writer(f&quot;&lt;document index=\&quot;{self.xml_index}\&quot;>&quot;)
            self.writer(f&quot;    &lt;source>{path}&lt;/source>&quot;)
            self.writer(&quot;    &lt;document_content>&quot;)
            self.writer(f&quot;        {content}&quot;)
            self.writer(&quot;    &lt;/document_content>&quot;)
            self.writer(&quot;&lt;/document>&quot;)
            self.xml_index += 1
        else:
            self.writer(path)
            self.writer(&quot;---&quot;)
            self.writer(content)
            self.writer(&quot;&quot;)
            self.writer(&quot;---&quot;)


@click.command()
@click.argument(&quot;paths&quot;, nargs=-1, type=click.Path(exists=True))
@click.option(&quot;-e&quot;, &quot;--extension&quot;, &quot;extensions&quot;, multiple=True, help=&quot;File extensions (e.g., .txt)&quot;)
@click.option(&quot;--include-hidden&quot;, is_flag=True, help=&quot;Include hidden files/folders.&quot;)
@click.option(&quot;--ignore-gitignore&quot;, is_flag=True, help=&quot;Ignore .gitignore rules.&quot;)
@click.option(&quot;--ignore&quot;, &quot;ignore_patterns&quot;, multiple=True, default=[], help=&quot;Glob patterns to ignore.&quot;)
@click.option(&quot;-o&quot;, &quot;--output&quot;, &quot;output_file&quot;, type=click.Path(writable=True), help=&quot;Output to a file.&quot;)
@click.option(&quot;-c&quot;, &quot;--cxml&quot;, &quot;output_xml&quot;, is_flag=True, help=&quot;Output in XML format.&quot;)
@click.option(&quot;-d&quot;, &quot;--max-depth&quot;, &quot;max_depth&quot;, type=int, default=5, help=&quot;Max recursion depth.&quot;)
@click.version_option()
def cli(paths, extensions, include_hidden, ignore_gitignore, ignore_patterns, output_file, output_xml, max_depth):
    &quot;&quot;&quot;
    Process files/directories, including archives &amp; Office/LibreOffice docs.
    &quot;&quot;&quot;
    writer = click.echo
    fp = None
    if output_file:
        try:
            fp = open(output_file, &quot;w&quot;, encoding=&quot;utf-8&quot;)
            writer = lambda s: print(s, file=fp)
        except Exception as e:
            logger.error(f&quot;Could not open output file {output_file}: {e}&quot;)
            sys.exit(1)

    processor = FileProcessor(
        extensions=extensions,
        include_hidden=include_hidden,
        ignore_gitignore=ignore_gitignore,
        ignore_patterns=ignore_patterns,
        output_xml=output_xml,
        writer=writer,
        max_depth=max_depth,
    )

    if output_xml:
        writer(&quot;{% codeblock xml %}&quot;)
        writer(&quot;&lt;documents>&quot;)

    for path in paths:
        if not os.path.exists(path):
            logger.error(f&quot;Path does not exist: {path}&quot;)
            continue
        processor.process_path(path, depth=0)

    if output_xml:
        writer(&quot;&lt;/documents>&quot;)
        writer(&quot;{% endcodeblock %}&quot;)

    if fp:
        fp.close()

if __name__ == &quot;__main__&quot;:
    cli()"></outline>

<outline text="import os
import sys
import tempfile
import shutil
import zipfile
import tarfile
import click
import logging
from fnmatch import fnmatch
from typing import Callable, List, Optional, Tuple

# Optional libraries
try:
    import rarfile
except ImportError:
    rarfile = None

try:
    import py7zr
except ImportError:
    py7zr = None

try:
    import pathspec
except ImportError:
    pathspec = None

# Configure logging
logging.basicConfig(level=logging.INFO, format=&quot;%(levelname)s: %(message)s&quot;)
logger = logging.getLogger(__name__)

# Archive handler functions using direct references
def handle_zip(file_path: str, extract_dir: str) -> bool:
    try:
        with zipfile.ZipFile(file_path, &apos;r&apos;) as zf:
            zf.extractall(extract_dir)
        return True
    except zipfile.BadZipFile as e:
        logger.warning(f&quot;Bad ZIP file {file_path}: {e}&quot;)
        return False

def handle_rar(file_path: str, extract_dir: str) -> bool:
    if rarfile is None:
        logger.warning(f&quot;RAR support not available. Install &apos;rarfile&apos; to handle {file_path}&quot;)
        return False
    try:
        with rarfile.RarFile(file_path, &apos;r&apos;) as rf:
            rf.extractall(extract_dir)
        return True
    except rarfile.Error as e:
        logger.warning(f&quot;Failed to extract RAR file {file_path}: {e}&quot;)
        return False

def handle_7z(file_path: str, extract_dir: str) -> bool:
    if py7zr is None:
        logger.warning(f&quot;7z support not available. Install &apos;py7zr&apos; to handle {file_path}&quot;)
        return False
    try:
        with py7zr.SevenZipFile(file_path, mode=&apos;r&apos;) as sz:
            sz.extractall(path=extract_dir)
        return True
    except py7zr.exceptions.Bad7zFile as e:
        logger.warning(f&quot;Bad 7z file {file_path}: {e}&quot;)
        return False

def handle_tar(file_path: str, extract_dir: str) -> bool:
    try:
        with tarfile.open(file_path, &apos;r:*&apos;) as tf:
            tf.extractall(extract_dir)
        return True
    except tarfile.TarError as e:
        logger.warning(f&quot;Bad TAR file {file_path}: {e}&quot;)
        return False

# Mapping file extensions to handler functions directly
ARCHIVE_HANDLERS = {
    &quot;.zip&quot;: handle_zip,
    &quot;.rar&quot;: handle_rar,
    &quot;.7z&quot;: handle_7z,
    &quot;.tar&quot;: handle_tar,
    &quot;.gz&quot;: handle_tar,
    &quot;.bz2&quot;: handle_tar,
}

# Office document extensions handled as archives via ZIP
OFFICE_EXTENSIONS = [&quot;.docx&quot;, &quot;.xlsx&quot;, &quot;.pptx&quot;, &quot;.odt&quot;, &quot;.ods&quot;, &quot;.odp&quot;]

class GitignoreHandler:
    &quot;&quot;&quot;
    Handles .gitignore rules using pathspec if available.
    &quot;&quot;&quot;
    def __init__(self, directory: str):
        self.spec = None
        gitignore_path = os.path.join(directory, &quot;.gitignore&quot;)
        if os.path.isfile(gitignore_path):
            try:
                with open(gitignore_path, &quot;r&quot;, encoding=&quot;utf-8&quot;) as f:
                    lines = f.read().splitlines()
                if pathspec:
                    self.spec = pathspec.PathSpec.from_lines(&quot;gitwildmatch&quot;, lines)
                else:
                    # Fallback: use basic list of rules
                    self.spec = lines
            except Exception as e:
                logger.warning(f&quot;Error reading .gitignore from {gitignore_path}: {e}&quot;)

    def should_ignore(self, file_path: str) -> bool:
        if self.spec is None:
            return False
        if pathspec and isinstance(self.spec, pathspec.PathSpec):
            return self.spec.match_file(file_path)
        else:
            basename = os.path.basename(file_path)
            for rule in self.spec:
                if fnmatch(basename, rule):
                    return True
                if os.path.isdir(file_path) and fnmatch(basename + &quot;/&quot;, rule):
                    return True
            return False

def print_default(writer: Callable[[str], None], path: str, content: str) -> None:
    writer(path)
    writer(&quot;---&quot;)
    writer(content)
    writer(&quot;&quot;)
    writer(&quot;---&quot;)

def print_as_xml(writer: Callable[[str], None], path: str, content: str, index: int) -> None:
    writer(f&quot;&lt;document index=\&quot;{index}\&quot;>&quot;)
    writer(f&quot;    &lt;source>{path}&lt;/source>&quot;)
    writer(&quot;    &lt;document_content>&quot;)
    for line in content.splitlines():
        writer(f&quot;        {line}&quot;)
    writer(&quot;    &lt;/document_content>&quot;)
    writer(&quot;&lt;/document>&quot;)

class FileProcessor:
    def __init__(
        self,
        extensions: Tuple[str, ...],
        include_hidden: bool,
        ignore_gitignore: bool,
        ignore_patterns: Tuple[str, ...],
        writer: Callable[[str], None],
        output_xml: bool,
        max_depth: int,
    ):
        self.extensions = tuple(ext.lower() for ext in extensions)
        self.include_hidden = include_hidden
        self.ignore_gitignore = ignore_gitignore
        self.ignore_patterns = ignore_patterns
        self.writer = writer
        self.output_xml = output_xml
        self.max_depth = max_depth
        self.xml_index = 1

    def process_path(self, path: str, depth: int = 0) -> None:
        if depth > self.max_depth:
            logger.warning(f&quot;Maximum recursion depth reached for {path}&quot;)
            return
        if os.path.isfile(path):
            self._handle_file(path, depth)
        elif os.path.isdir(path):
            self._handle_directory(path, depth)

    def _handle_file(self, path: str, depth: int) -> None:
        _, ext = os.path.splitext(path)
        ext = ext.lower()
        # Process archive or Office document
        if ext in ARCHIVE_HANDLERS or ext in OFFICE_EXTENSIONS:
            self._handle_archive_or_office(path, ext, depth)
        else:
            self._print_file(path)

    def _handle_archive_or_office(self, path: str, ext: str, depth: int) -> None:
        with tempfile.TemporaryDirectory() as extract_dir:
            handler = ARCHIVE_HANDLERS.get(ext)
            if ext in OFFICE_EXTENSIONS:
                handler = ARCHIVE_HANDLERS[&quot;.zip&quot;]
            if handler is None:
                logger.warning(f&quot;No handler for archive type {ext} in {path}&quot;)
                return
            # Check for required libraries
            if (ext == &quot;.rar&quot; and rarfile is None) or (ext == &quot;.7z&quot; and py7zr is None):
                return
            success = handler(path, extract_dir)
            if success:
                self.process_path(extract_dir, depth + 1)
            else:
                logger.warning(f&quot;Failed to extract archive: {path}&quot;)

    def _print_file(self, path: str) -> None:
        try:
            with open(path, &quot;r&quot;, encoding=&quot;utf-8&quot;) as f:
                content = f.read()
                self._print_content(path, content)
        except UnicodeDecodeError:
            try:
                with open(path, &quot;r&quot;, encoding=&quot;latin-1&quot;) as f:
                    content = f.read()
                    self._print_content(path, content)
            except Exception as e:
                logger.warning(f&quot;Skipping file {path} due to encoding error: {e}&quot;)
        except Exception as e:
            logger.warning(f&quot;Skipping file {path} due to error: {e}&quot;)

    def _print_content(self, path: str, content: str) -> None:
        if self.output_xml:
            print_as_xml(self.writer, path, content, self.xml_index)
            self.xml_index += 1
        else:
            print_default(self.writer, path, content)

    def _handle_directory(self, path: str, depth: int) -> None:
        gitignore = None if self.ignore_gitignore else GitignoreHandler(path)
        for root, dirs, files in os.walk(path):
            if not self.include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith(&quot;.&quot;)]
                files = [f for f in files if not f.startswith(&quot;.&quot;)]
            if gitignore:
                dirs[:] = [d for d in dirs if not gitignore.should_ignore(os.path.join(root, d))]
                files = [f for f in files if not gitignore.should_ignore(os.path.join(root, f))]
            if self.ignore_patterns:
                files = [f for f in files if not any(fnmatch(f, pattern) for pattern in self.ignore_patterns)]
            if self.extensions:
                files = [f for f in files if any(f.lower().endswith(ext) for ext in self.extensions)]
            for file in sorted(files):
                file_path = os.path.join(root, file)
                self.process_path(file_path, depth + 1)

@click.command()
@click.argument(&quot;paths&quot;, nargs=-1, type=click.Path(exists=True))
@click.option(&quot;-e&quot;, &quot;--extension&quot;, &quot;extensions&quot;, multiple=True, help=&quot;File extensions to include (e.g., .txt, .md)&quot;)
@click.option(&quot;--include-hidden&quot;, is_flag=True, help=&quot;Include hidden files and folders.&quot;)
@click.option(&quot;--ignore-gitignore&quot;, is_flag=True, help=&quot;Ignore .gitignore rules.&quot;)
@click.option(&quot;--ignore&quot;, &quot;ignore_patterns&quot;, multiple=True, default=[], help=&quot;Glob patterns to ignore (e.g., *.log).&quot;)
@click.option(&quot;-o&quot;, &quot;--output&quot;, &quot;output_file&quot;, type=click.Path(writable=True), help=&quot;Output to a file instead of stdout.&quot;)
@click.option(&quot;-c&quot;, &quot;--cxml&quot;, &quot;output_xml&quot;, is_flag=True, help=&quot;Output in XML format enclosed in codeblock tags.&quot;)
@click.option(&quot;-d&quot;, &quot;--max-depth&quot;, &quot;max_depth&quot;, type=int, default=5, help=&quot;Maximum recursion depth (default: 5).&quot;)
@click.version_option()
def cli(paths: Tuple[str, ...], extensions: Tuple[str, ...], include_hidden: bool, ignore_gitignore: bool,
        ignore_patterns: Tuple[str, ...], output_file: Optional[str], output_xml: bool, max_depth: int) -> None:
    writer: Callable[[str], None] = click.echo
    fp = None
    if output_file:
        try:
            fp = open(output_file, &quot;w&quot;, encoding=&quot;utf-8&quot;)
            writer = lambda s: print(s, file=fp)
        except Exception as e:
            logger.error(f&quot;Cannot open output file {output_file}: {e}&quot;)
            sys.exit(1)
    if output_xml:
        writer(&quot;{% codeblock xml %}&quot;)
        writer(&quot;&lt;documents>&quot;)
    processor = FileProcessor(extensions, include_hidden, ignore_gitignore, ignore_patterns, writer, output_xml, max_depth)
    for path in paths:
        processor.process_path(path)
    if output_xml:
        writer(&quot;&lt;/documents>&quot;)
        writer(&quot;{% endcodeblock %}&quot;)
    if fp:
        fp.close()

if __name__ == &quot;__main__&quot;:
    cli()"></outline>

<outline text="import os
import sys
import tempfile
import shutil
import logging
from fnmatch import fnmatch
import zipfile
import tarfile
import click
from typing import List, Callable, Optional, Tuple

try:
    import rarfile
except ImportError:
    rarfile = None

try:
    import py7zr
except ImportError:
    py7zr = None

try:
    import pathspec
except ImportError:
    pathspec = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=&quot;%(asctime)s - %(levelname)s - %(message)s&quot;,
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

# Supported archive extensions and their handlers
ARCHIVE_HANDLERS = {
    &quot;.zip&quot;: lambda f, d: handle_zip(f, d),
    &quot;.rar&quot;: lambda f, d: handle_rar(f, d),
    &quot;.7z&quot;: lambda f, d: handle_7z(f, d),
    &quot;.tar&quot;: lambda f, d: handle_tar(f, d),
    &quot;.gz&quot;: lambda f, d: handle_tar(f, d),
    &quot;.bz2&quot;: lambda f, d: handle_tar(f, d),
}

# Microsoft Office and LibreOffice document extensions
OFFICE_EXTENSIONS = [&quot;.docx&quot;, &quot;.xlsx&quot;, &quot;.pptx&quot;, &quot;.odt&quot;, &quot;.ods&quot;, &quot;.odp&quot;]

def is_within_directory(directory: str, target: str) -> bool:
    &quot;&quot;&quot;
    Check if the target path is within the specified directory to prevent path traversal.
    &quot;&quot;&quot;
    abs_directory = os.path.abspath(directory)
    abs_target = os.path.abspath(target)
    return os.path.commonprefix([abs_directory, abs_target]) == abs_directory

def safe_extract(tar: tarfile.TarFile, path: str = &quot;.&quot;, members=None, numeric_owner: bool = False) -> None:
    &quot;&quot;&quot;
    Safely extract a tar archive, preventing path traversal attacks.
    &quot;&quot;&quot;
    for member in (members or tar.getmembers()):
        member_path = os.path.join(path, member.name)
        if not is_within_directory(path, member_path):
            raise Exception(&quot;Attempted Path Traversal in Tar file&quot;)
    tar.extractall(path=path, members=members, numeric_owner=numeric_owner)

class GitignoreHandler:
    &quot;&quot;&quot;Handles .gitignore rules.&quot;&quot;&quot;

    def __init__(self, path: str):
        if pathspec:
            self.matches = self.read_gitignore(path)
        else:
            self.rules = self.read_gitignore_basic(path)

    def read_gitignore(self, path: str) -> Callable[[str], bool]:
        &quot;&quot;&quot;Read and parse .gitignore file using pathspec.&quot;&quot;&quot;
        gitignore_path = os.path.join(path, &quot;.gitignore&quot;)
        if os.path.isfile(gitignore_path):
            try:
                with open(gitignore_path, &quot;r&quot;, encoding=&quot;utf-8&quot;) as f:
                    spec = pathspec.PathSpec.from_lines(&quot;gitwildmatch&quot;, f)
                return spec.match_file
            except Exception as e:
                logger.warning(f&quot;Error parsing .gitignore: {e}&quot;)
        return lambda x: False

    def read_gitignore_basic(self, path: str) -> List[str]:
        &quot;&quot;&quot;Read and parse .gitignore file (basic implementation).&quot;&quot;&quot;
        gitignore_path = os.path.join(path, &quot;.gitignore&quot;)
        if os.path.isfile(gitignore_path):
            with open(gitignore_path, &quot;r&quot;, encoding=&quot;utf-8&quot;) as f:
                return [
                    line.strip()
                    for line in f
                    if line.strip() and not line.startswith(&quot;#&quot;)
                ]
        return []

    def should_ignore(self, path: str) -> bool:
        &quot;&quot;&quot;Determine if a path should be ignored based on .gitignore rules.&quot;&quot;&quot;
        if pathspec and self.matches:
            return self.matches(path)
        else:
            for rule in self.rules:
                if fnmatch(os.path.basename(path), rule):
                    return True
                if os.path.isdir(path) and fnmatch(os.path.basename(path) + &quot;/&quot;, rule):
                    return True
        return False

class XMLPrinter:
    &quot;&quot;&quot;Prints content in an XML-like format.&quot;&quot;&quot;

    def __init__(self, writer: Callable[[str], None]):
        self.writer = writer
        self.index = 1

    def print_header(self):
        &quot;&quot;&quot;Print the XML header.&quot;&quot;&quot;
        self.writer(&quot;{% codeblock xml %}&quot;)
        self.writer(&quot;&lt;documents>&quot;)

    def print_footer(self):
        &quot;&quot;&quot;Print the XML footer.&quot;&quot;&quot;
        self.writer(&quot;&lt;/documents>&quot;)
        self.writer(&quot;{% endcodeblock %}&quot;)

    def print(self, path: str, content: str):
        &quot;&quot;&quot;Print content in XML format.&quot;&quot;&quot;
        self.writer(f&quot;&lt;document index=\&quot;{self.index}\&quot;>&quot;)
        self.writer(f&quot;    &lt;source>{path}&lt;/source>&quot;)
        self.writer(&quot;    &lt;document_content>&quot;)
        self.writer(f&quot;        {content}&quot;)
        self.writer(&quot;    &lt;/document_content>&quot;)
        self.writer(&quot;&lt;/document>&quot;)
        self.index += 1

class DefaultPrinter:
    &quot;&quot;&quot;Prints content in the default text format.&quot;&quot;&quot;

    def __init__(self, writer: Callable[[str], None]):
        self.writer = writer

    def print(self, path: str, content: str):
        &quot;&quot;&quot;Print content in default format.&quot;&quot;&quot;
        self.writer(path)
        self.writer(&quot;---&quot;)
        self.writer(content)
        self.writer(&quot;&quot;)
        self.writer(&quot;---&quot;)

class FileProcessor:
    &quot;&quot;&quot;Processes files and directories.&quot;&quot;&quot;

    def __init__(
        self,
        extensions: List[str],
        include_hidden: bool,
        ignore_gitignore: bool,
        ignore_patterns: List[str],
        printer: Callable[[str, str], None],
        max_depth: int = 5,
    ):
        self.extensions = extensions
        self.include_hidden = include_hidden
        self.ignore_gitignore = ignore_gitignore
        self.ignore_patterns = ignore_patterns
        self.printer = printer
        self.max_depth = max_depth

    def process_path(
        self,
        path: str,
        gitignore_handler: Optional[GitignoreHandler] = None,
        depth: int = 0,
    ):
        &quot;&quot;&quot;Recursively process a given path, handling files and directories.&quot;&quot;&quot;
        if depth > self.max_depth:
            logger.warning(f&quot;Maximum recursion depth reached for {path}&quot;)
            return

        if os.path.isfile(path):
            self.process_file(path)
        elif os.path.isdir(path):
            self.process_directory(path, gitignore_handler, depth)

    def process_file(self, path: str):
        &quot;&quot;&quot;Process a single file.&quot;&quot;&quot;
        _, ext = os.path.splitext(path)
        ext = ext.lower()

        if ext in ARCHIVE_HANDLERS or ext in OFFICE_EXTENSIONS:
            self.process_archive(path, ext)
        else:
            self.print_file_content(path)

    def process_archive(self, path: str, ext: str):
        &quot;&quot;&quot;Process an archive file.&quot;&quot;&quot;
        with tempfile.TemporaryDirectory() as extract_dir:
            if ext.lower() in OFFICE_EXTENSIONS:
                handler_func = handle_zip  # Use ZIP handler for Office documents
            else:
                handler_func = ARCHIVE_HANDLERS.get(ext)

            if handler_func:
                if ext == &quot;.rar&quot; and rarfile is None:
                    logger.warning(
                        f&quot;RAR support not available. Install &apos;rarfile&apos; to handle {path}&quot;
                    )
                    return
                if ext == &quot;.7z&quot; and py7zr is None:
                    logger.warning(
                        f&quot;7z support not available. Install &apos;py7zr&apos; to handle {path}&quot;
                    )
                    return

                success = handler_func(path, extract_dir)
                if success:
                    self.process_path(extract_dir, depth=1)
                else:
                    logger.warning(f&quot;Failed to extract archive: {path}&quot;)
            else:
                logger.warning(f&quot;No handler for archive type {ext} in {path}&quot;)

    def print_file_content(self, path: str):
        &quot;&quot;&quot;Print the content of a file.&quot;&quot;&quot;
        try:
            with open(path, &quot;r&quot;, encoding=&quot;utf-8&quot;) as f:
                content = f.read()
                self.printer.print(path, content)
        except UnicodeDecodeError:
            try:
                with open(path, &quot;r&quot;, encoding=&quot;latin-1&quot;) as f:
                    content = f.read()
                    self.printer.print(path, content)
            except Exception as e:
                logger.warning(f&quot;Skipping file {path} due to error: {e}&quot;)
        except Exception as e:
            logger.warning(f&quot;Skipping file {path} due to error: {e}&quot;)

    def process_directory(
        self,
        path: str,
        gitignore_handler: Optional[GitignoreHandler] = None,
        depth: int,
    ):
        &quot;&quot;&quot;Process a directory.&quot;&quot;&quot;
        if not self.ignore_gitignore and gitignore_handler is None:
            gitignore_handler = GitignoreHandler(path)

        for root, dirs, files in os.walk(path):
            if not self.include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith(&quot;.&quot;)]
                files = [f for f in files if not f.startswith(&quot;.&quot;)]

            if gitignore_handler:
                dirs[:] = [
                    d
                    for d in dirs
                    if not gitignore_handler.should_ignore(os.path.join(root, d))
                ]
                files = [
                    f
                    for f in files
                    if not gitignore_handler.should_ignore(os.path.join(root, f))
                ]

            if self.ignore_patterns:
                files = [
                    f
                    for f in files
                    if not any(fnmatch(f, pattern) for pattern in self.ignore_patterns)
                ]

            if self.extensions:
                files = [
                    f
                    for f in files
                    if any(f.lower().endswith(ext.lower()) for ext in self.extensions)
                ]

            for file in sorted(files):
                file_path = os.path.join(root, file)
                self.process_path(file_path, gitignore_handler, depth + 1)

def handle_zip(file_path: str, extract_dir: str) -> bool:
    &quot;&quot;&quot;Handle extraction of ZIP archives.&quot;&quot;&quot;
    try:
        with zipfile.ZipFile(file_path, &quot;r&quot;) as zip_ref:
            zip_ref.extractall(extract_dir)
        return True
    except zipfile.BadZipFile:
        logger.warning(f&quot;Bad ZIP file {file_path}&quot;)
        return False

def handle_rar(file_path: str, extract_dir: str) -> bool:
    &quot;&quot;&quot;Handle extraction of RAR archives.&quot;&quot;&quot;
    if rarfile is None:
        logger.warning(
            f&quot;RAR support not available. Install &apos;rarfile&apos; to handle {file_path}&quot;
        )
        return False
    try:
        with rarfile.RarFile(file_path, &quot;r&quot;) as rar_ref:
            rar_ref.extractall(extract_dir)
        return True
    except rarfile.Error as e:
        logger.warning(f&quot;Failed to extract RAR file {file_path}: {e}&quot;)
        return False

def handle_7z(file_path: str, extract_dir: str) -> bool:
    &quot;&quot;&quot;Handle extraction of 7Z archives.&quot;&quot;&quot;
    if py7zr is None:
        logger.warning(
            f&quot;7z support not available. Install &apos;py7zr&apos; to handle {file_path}&quot;
        )
        return False
    try:
        with py7zr.SevenZipFile(file_path, mode=&quot;r&quot;) as z:
            z.extractall(path=extract_dir)
        return True
    except py7zr.exceptions.Bad7zFile as e:
        logger.warning(f&quot;Bad 7Z file {file_path}: {e}&quot;)
        return False

def handle_tar(file_path: str, extract_dir: str) -> bool:
    &quot;&quot;&quot;Handle extraction of TAR archives.&quot;&quot;&quot;
    try:
        with tarfile.open(file_path, &quot;r:*&quot;) as tar_ref:
            safe_extract(tar_ref, extract_dir)
        return True
    except tarfile.TarError:
        logger.warning(f&quot;Bad TAR file {file_path}&quot;)
        return False

@click.command()
@click.argument(&quot;paths&quot;, nargs=-1, type=click.Path(exists=True))
@click.option(
    &quot;extensions&quot;,
    &quot;-e&quot;,
    &quot;--extension&quot;,
    multiple=True,
    help=&quot;File extensions to include (e.g., .txt, .md)&quot;,
)
@click.option(
    &quot;--include-hidden&quot;,
    is_flag=True,
    help=&quot;Include files and folders starting with a dot (.).&quot;,
)
@click.option(
    &quot;--ignore-gitignore&quot;,
    is_flag=True,
    help=&quot;Ignore .gitignore files and include all files.&quot;,
)
@click.option(
    &quot;ignore_patterns&quot;,
    &quot;--ignore&quot;,
    multiple=True,
    default=[],
    help=&quot;List of patterns to ignore (e.g., *.log, temp*).&quot;,
)
@click.option(
    &quot;output_file&quot;,
    &quot;-o&quot;,
    &quot;--output&quot;,
    type=click.Path(writable=True),
    help=&quot;Output to a file instead of stdout.&quot;,
)
@click.option(
    &quot;claude_xml&quot;,
    &quot;-c&quot;,
    &quot;--cxml&quot;,
    is_flag=True,
    help=&quot;Output in XML format enclosed within codeblock tags.&quot;,
)
@click.option(
    &quot;max_depth&quot;,
    &quot;-d&quot;,
    &quot;--max-depth&quot;,
    type=int,
    default=5,
    help=&quot;Maximum recursion depth for processing nested archives (default: 5).&quot;,
)
@click.version_option()
def cli(
    paths: Tuple[str, ...],
    extensions: Tuple[str, ...],
    include_hidden: bool,
    ignore_gitignore: bool,
    ignore_patterns: Tuple[str, ...],
    output_file: Optional[str],
    claude_xml: bool,
    max_depth: int,
):
    &quot;&quot;&quot;
    Process files and directories, including archives and Office/LibreOffice documents.

    This script takes one or more paths to files or directories and outputs every file
    recursively. It can handle various archive formats and Microsoft Office/LibreOffice documents,
    extracting their contents for processing. The output can be in plain text or XML format.

    Usage:
    python script.py [OPTIONS] PATHS...

    Example:
    python script.py path/to/directory -e .txt .md --cxml -o output.xml

    Prerequisites:
        - Install required libraries:
          ```
          pip install click rarfile py7zr pathspec
          ```
    &quot;&quot;&quot;
    if output_file:
        try:
            fp = open(output_file, &quot;w&quot;, encoding=&quot;utf-8&quot;)
            writer = lambda s: print(s, file=fp)
        except Exception as e:
            logger.error(f&quot;Cannot open output file {output_file}: {e}&quot;)
            sys.exit(1)
    else:
        fp = None
        writer = lambda s: print(s)

    if claude_xml:
        printer = XMLPrinter(writer)
        printer.print_header()
    else:
        printer = DefaultPrinter(writer)

    processor = FileProcessor(
        list(extensions),
        include_hidden,
        ignore_gitignore,
        list(ignore_patterns),
        printer,
        max_depth,
    )

    try:
        for path in paths:
            processor.process_path(path)

        if claude_xml:
            printer.print_footer()
    finally:
        if fp:
            fp.close()

if __name__ == &quot;__main__&quot;:
    cli()"></outline>
</outline>
</body></opml>