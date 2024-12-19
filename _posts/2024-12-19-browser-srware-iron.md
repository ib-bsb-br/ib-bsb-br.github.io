---
tags: software>windows
info: aberto.
date: 2024-12-19
type: post
layout: post
published: true
slug: browser-srware-iron
title: 'SRWare Iron Browser Flags'
---
# Modifying Browser Executable for Permanent Flag Integration

## Initial Setup
```batch
@echo off
if exist IronPortable.exe (
    if not exist IronPortable.orig.exe (
        move /y IronPortable.exe IronPortable.orig.exe
    )
)
```

## Wrapper Implementation
```c
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <shlwapi.h>

#pragma comment(lib, "shlwapi.lib")

#define MAX_CMD_LENGTH 32768
#define LOG_FILE "chrome_wrapper.log"

void log_error(const char* message, DWORD error_code) {
    FILE* log_file = fopen(LOG_FILE, "a");
    if (log_file) {
        SYSTEMTIME st;
        GetLocalTime(&st);
        fprintf(log_file, "[%02d:%02d:%02d] %s (Error: %lu)\n", 
                st.wHour, st.wMinute, st.wSecond, message, error_code);
        fclose(log_file);
    }
}

void sanitize_command(char* cmdLine) {
    const char* dangerous_chars = "&|;`$<>^()[]{}";
    char* temp = _strdup(cmdLine);
    if (!temp) return;

    size_t i, j;
    for (i = 0, j = 0; temp[i] != '\0'; i++) {
        if (!strchr(dangerous_chars, temp[i])) {
            cmdLine[j++] = temp[i];
        }
    }
    cmdLine[j] = '\0';
    free(temp);
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, 
                   LPSTR lpCmdLine, int nCmdShow) {
    SetErrorMode(SEM_FAILCRITICALERRORS | SEM_NOOPENFILEERRORBOX);
    
    char cwd[MAX_PATH] = {0};
    char cmd[MAX_CMD_LENGTH] = {0};
    STARTUPINFOA si = {0};
    PROCESS_INFORMATION pi = {0};
    
    if (!GetCurrentDirectoryA(sizeof(cwd), cwd)) {
        log_error("Failed to get current directory", GetLastError());
        return 1;
    }

    const char* chrome_orig = "IronPortable.orig.exe";
    if (!PathFileExistsA(PathCombineA(cmd, cwd, chrome_orig))) {
        log_error("Original chrome executable not found", GetLastError());
        return 1;
    }

    char* final_cmd = calloc(MAX_CMD_LENGTH, sizeof(char));
    if (!final_cmd) {
        log_error("Memory allocation failed", GetLastError());
        return 1;
    }

    _snprintf(final_cmd, MAX_CMD_LENGTH - 1,
        "\"%s\\%s\" --user-data-dir=\"%s\\Profile\" "
        "--enable-gpu-rasterization "
        "--gpu-preferences=UAAAAAAAAADgAAAAAAAAAAAAAAABgAAAAAAAAAA "
        "--no-pre-read-main-dll "
        "--breakpad=no "
        "--no-periodic-tasks "
        "--allow-insecure-localhost "
        "--enable-experimental-web-platform-features "
        "--enable-quic "
        "--extensions-on-chrome-urls "
        "--video-capture-use-gpu-memory-buffer",
        cwd, chrome_orig, cwd);

    if (lpCmdLine && *lpCmdLine) {
        char sanitized_args[MAX_CMD_LENGTH] = {0};
        strncpy(sanitized_args, lpCmdLine, MAX_CMD_LENGTH - 1);
        sanitize_command(sanitized_args);
        strncat(final_cmd, " ", MAX_CMD_LENGTH - strlen(final_cmd) - 1);
        strncat(final_cmd, sanitized_args, MAX_CMD_LENGTH - strlen(final_cmd) - 1);
    }

    si.cb = sizeof(si);
    
    if (!CreateProcessA(NULL, final_cmd, NULL, NULL, FALSE, 
                       CREATE_NEW_PROCESS_GROUP, NULL, cwd, &si, &pi)) {
        log_error("Failed to create process", GetLastError());
        free(final_cmd);
        return 1;
    }

    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    free(final_cmd);
    
    return 0;
}
```

## Build Instructions

### Visual Studio
```batch
cl /O2 /W4 /WX /DNDEBUG /FeIronPortable.exe chrome_wrapper.c /link user32.lib kernel32.lib shlwapi.lib
```

### MinGW
```batch
gcc -O2 -Wall -Wextra -Werror -o IronPortable.exe chrome_wrapper.c -mwindows -lshlwapi
```

## Deployment Script
```batch
@echo off
set BROWSER_DIR=\IronPortable64\Iron
cd /d %BROWSER_DIR%

if exist IronPortable.exe.new (
    move /y IronPortable.exe IronPortable.exe.old
    move /y IronPortable.exe.new IronPortable.orig.exe
    copy /y wrapper.exe IronPortable.exe
) else (
    if exist IronPortable.exe (
        move /y IronPortable.exe IronPortable.orig.exe
        copy /y wrapper.exe IronPortable.exe
    )
)
```

## Update Handler
```batch
@echo off
set BROWSER_DIR=\IronPortable64\Iron
cd /d %BROWSER_DIR%

if exist IronPortable.exe.new (
    move /y IronPortable.exe IronPortable.exe.old
    move /y IronPortable.exe.new IronPortable.orig.exe
    copy /y wrapper.exe IronPortable.exe
)
```
