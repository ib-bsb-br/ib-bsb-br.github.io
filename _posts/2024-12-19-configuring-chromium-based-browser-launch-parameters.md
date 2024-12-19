---
tags: software>windows
info: aberto.
date: 2024-12-19
type: post
layout: post
published: true
slug: configuring-chromium-based-browser-launch-parameters
title: 'Configuring chromium-based browser launch parameters'
---
1. **Create Local Configuration File**
   ```batch
   # Create directory for configuration
   mkdir "%~dp0config"
   
   # Create browser configuration file
   echo {
     "browser": {
       "custom_flags": [
         "--user-data-dir=\"%~dp0Profile\"",
         "--enable-gpu-rasterization",
         "--gpu-preferences=UAAAAAAAAADgAAAAAAAAAAAAAAABgAAAAAAAAAA",
         "--no-pre-read-main-dll",
         "--breakpad=no",
         "--no-periodic-tasks",
         "--allow-insecure-localhost",
         "--enable-experimental-web-platform-features",
         "--enable-quic",
         "--extensions-on-chrome-urls",
         "--video-capture-use-gpu-memory-buffer"
       ]
     }
   } > "%~dp0config\browser_config.json"
   ```

2. **Create Launcher Script**
   ```batch
   @echo off
   setlocal enabledelayedexpansion
   
   set "SCRIPT_DIR=%~dp0"
   set "BROWSER_EXE=%SCRIPT_DIR%\IronPortable64\Iron\chrome.exe"
   set "CONFIG_FILE=%SCRIPT_DIR%\config\browser_config.json"
   
   rem Read configuration and build command line
   for /f "tokens=* delims=" %%a in ('type "%CONFIG_FILE%" ^| findstr /c:"custom_flags"') do (
       set "FLAGS=%%a"
   )
   
   start "" "%BROWSER_EXE%" %FLAGS%
   ```
   Save as `launch_browser.bat` in the root directory