---
tags: software>windows
info: aberto.
date: 2024-12-19
type: post
layout: post
published: true
slug: browser-srware-iron
title: 'SRWare Iron Browser launcher in C++'
---
## Introduction

This document outlines the process of creating a browser launcher, a wrapper executable designed to launch a web browser with predefined settings, including permanently integrated command-line flags. This approach offers several benefits, such as centralized configuration management, persistent flag integration without modifying the original browser executable, and the ability to manage multiple browser configurations from a single point. The launcher is particularly useful for users who frequently use specific browser flags or need to manage different browser profiles for various tasks.

## Configuration

The browser launcher utilizes a configuration file named `browser_config.ini` to manage browser settings and launch parameters. This file is divided into sections:

*   **`[Browser]` Section:**
    *   `Executable`: Specifies the path to the browser executable (e.g., `G:\05-portable\IronPortable64\Iron\chrome.exe`).
    *   `VersionUrl`: Provides a URL for checking updates. For example, for Thorium, you might use `https://api.github.com/repos/Alex313031/Thorium-Win/releases/latest`. The launcher fetches the latest version information from this URL and compares it with the current browser version.
    *   `Flags`: Contains custom command-line flags to be passed to the browser (e.g., `--user-data-dir="G:\05-portable\IronPortable64\Iron\User Data" --no-default-browser-check --disable-logging --disable-breakpad --disable-features=PrintCompositorLPAC --enable-quic`).
*   **`[General]` Section:**
    *   `UpdateCheck`: A boolean value (`true` or `false`) that determines whether the launcher should check for updates.

Multiple `[Browser]` sections (e.g., `[Browser2]`, `[Browser3]`) can be added to define settings for different browsers. The launcher can handle multiple `[Browser]` sections, and the user can select a specific browser using the `--browser=` command-line argument followed by the number of the browser section (e.g., `--browser=2` to use `[Browser2]`).

**Example `browser_config.ini`:**

```ini
[Browser]
Executable=G:\05-portable\IronPortable64\Iron\chrome.exe
VersionUrl=
Flags=--user-data-dir="G:\05-portable\IronPortable64\Iron\User Data" --no-default-browser-check --disable-logging --disable-breakpad --disable-features=PrintCompositorLPAC --enable-quic

[Browser2]
Executable=C:\Browsers\Thorium\thorium.exe
VersionUrl=https://api.github.com/repos/Alex313031/Thorium-Win/releases/latest
Flags=--user-data-dir="C:\Browsers\Thorium\User Data" --no-default-browser-check --disable-logging --disable-breakpad --disable-features=PrintCompositorLPAC

[General]
UpdateCheck=true
```

An alternative configuration method using `browser.conf` and `browser_flags.conf` is also available, where `browser.conf` specifies the browser executable and user data directory, and `browser_flags.conf` contains additional flags. However, the `browser_config.ini` approach is recommended for its flexibility and ability to manage multiple browsers.

## C++ Implementation

The core functionality of the browser launcher is implemented in C++. The following code provides a comprehensive example:

```cpp
#include <windows.h>
#include <shlwapi.h>
#include <fstream>
#include <sstream>
#include <iostream>
#include <vector>
#include <algorithm>
#include <winhttp.h>

#pragma comment(lib, "shlwapi.lib")
#pragma comment(lib, "Version.lib")
#pragma comment(lib, "winhttp.lib")

#define MAX_CMD_LENGTH 32768
#define LOG_FILE "browser_wrapper.log"
#define CONFIG_FILE "browser_config.ini"

// Function to log messages to a file
void log_message(const std::string& message, DWORD error_code = 0) {
    std::ofstream log_file(LOG_FILE, std::ios::app);
    if (log_file.is_open()) {
        SYSTEMTIME st;
        GetLocalTime(&st);
        char timestamp[20];
        sprintf_s(timestamp, sizeof(timestamp), "[%02d:%02d:%02d]", st.wHour, st.wMinute, st.wSecond);
        log_file << timestamp << " " << message;
        if (error_code != 0) {
            log_file << " (Error: " << error_code << ")";
        }
        log_file << std::endl;
        log_file.close();
    } else {
        // Handle error: Cannot open log file
        std::cerr << "Error: Could not open log file " << LOG_FILE << std::endl;
    }
}

// Function to sanitize command-line arguments
void sanitize_command(char* cmdLine) {
    const char* dangerous_chars = "&|;`$<>^()[]{}";
    char* dst = cmdLine;
    for (char* src = cmdLine; *src != '\0'; ++src) {
        if (!strchr(dangerous_chars, *src)) {
            *dst++ = *src;
        }
    }
    *dst = '\0';
}

// Function to read the configuration file
std::vector<std::pair<std::string, std::string>> read_config_file(const std::string& config_file, const std::string& section) {
    std::vector<std::pair<std::string, std::string>> settings;
    std::ifstream file(config_file);
    std::string line;
    bool in_section = false;

    if (!file.is_open()) {
        log_message("Failed to open config file: " + config_file, GetLastError());
        return settings;
    }

    while (std::getline(file, line)) {
        // Remove leading/trailing whitespace
        line.erase(0, line.find_first_not_of(" \t"));
        line.erase(line.find_last_not_of(" \t") + 1);

        // Skip comments and empty lines
        if (line.empty() || line[0] == '#') {
            continue;
        }

        if (line[0] == '[') {
            // Check if we are entering the desired section
            in_section = (line == "[" + section + "]");
        } else if (in_section) {
            // Parse key-value pairs
            size_t delimiter_pos = line.find('=');
            if (delimiter_pos != std::string::npos) {
                std::string key = line.substr(0, delimiter_pos);
                std::string value = line.substr(delimiter_pos + 1);
                // Remove leading/trailing whitespace from key and value
                key.erase(0, key.find_first_not_of(" \t"));
                key.erase(key.find_last_not_of(" \t") + 1);
                value.erase(0, value.find_first_not_of(" \t"));
                value.erase(value.find_last_not_of(" \t") + 1);
                settings.push_back(std::make_pair(key, value));
            }
        }
    }
    if (settings.empty() && in_section) {
        log_message("Configuration section " + section + " in file " + config_file + " is empty or invalid.");
    }
    return settings;
}

// Function to get the browser version
std::string get_browser_version(const std::string& browser_path) {
    DWORD verHandle = 0;
    UINT size = 0;
    LPBYTE lpBuffer = NULL;
    std::string version = "Unknown";

    DWORD verSize = GetFileVersionInfoSizeA(browser_path.c_str(), &verHandle);
    if (verSize == 0) {
        log_message("Failed to get version info size for: " + browser_path, GetLastError());
        return version;
    }

    std::vector<char> verData(verSize);
    if (!GetFileVersionInfoA(browser_path.c_str(), verHandle, verSize, verData.data())) {
        log_message("Failed to get version info for: " + browser_path, GetLastError());
        return version;
    }

    if (!VerQueryValueA(verData.data(), "\\", (VOID FAR * FAR*)&lpBuffer, &size) || size == 0) {
        log_message("Failed to query version value for: " + browser_path, GetLastError());
        return version;
    }

    VS_FIXEDFILEINFO* verInfo = (VS_FIXEDFILEINFO*)lpBuffer;
    if (verInfo->dwSignature != 0xfeef04bd) {
        log_message("Invalid version info signature for: " + browser_path);
        return version;
    }

    version = std::to_string((verInfo->dwFileVersionMS >> 16) & 0xffff) + "." +
              std::to_string((verInfo->dwFileVersionMS >> 0) & 0xffff) + "." +
              std::to_string((verInfo->dwFileVersionLS >> 16) & 0xffff) + "." +
              std::to_string((verInfo->dwFileVersionLS >> 0) & 0xffff);
    return version;
}

// Function to perform a basic update check
bool check_for_updates(const std::string& current_version, const std::string& version_url) {
    if (version_url.empty()) {
        return false;
    }

    HINTERNET hSession = WinHttpOpen(L"BrowserUpdateChecker/1.0", WINHTTP_ACCESS_TYPE_DEFAULT_PROXY, WINHTTP_NO_PROXY_NAME, WINHTTP_NO_PROXY_BYPASS, 0);
    if (!hSession) {
        log_message("Failed to open HTTP session", GetLastError());
        return false;
    }

    URL_COMPONENTS urlComponents;
    ZeroMemory(&urlComponents, sizeof(urlComponents));
    urlComponents.dwStructSize = sizeof(urlComponents);
    urlComponents.dwHostNameLength = -1;
    urlComponents.dwUrlPathLength = -1;

    if (!WinHttpCrackUrl(std::wstring(version_url.begin(), version_url.end()).c_str(), version_url.length(), 0, &urlComponents)) {
        log_message("Failed to parse URL: " + version_url, GetLastError());
        WinHttpCloseHandle(hSession);
        return false;
    }

    std::wstring hostName(urlComponents.lpszHostName, urlComponents.dwHostNameLength);
    std::wstring urlPath(urlComponents.lpszUrlPath, urlComponents.dwUrlPathLength);

    HINTERNET hConnect = WinHttpConnect(hSession, hostName.c_str(), INTERNET_DEFAULT_HTTPS_PORT, 0);
    if (!hConnect) {
        log_message("Failed to connect to host: " + std::string(hostName.begin(), hostName.end()), GetLastError());
        WinHttpCloseHandle(hSession);
        return false;
    }

    HINTERNET hRequest = WinHttpOpenRequest(hConnect, L"GET", urlPath.c_str(), NULL, WINHTTP_NO_REFERER, WINHTTP_DEFAULT_ACCEPT_TYPES, WINHTTP_FLAG_SECURE);
    if (!hRequest) {
        log_message("Failed to open HTTP request", GetLastError());
        WinHttpCloseHandle(hConnect);
        WinHttpCloseHandle(hSession);
        return false;
    }

    if (!WinHttpSendRequest(hRequest, WINHTTP_NO_ADDITIONAL_HEADERS, 0, WINHTTP_NO_REQUEST_DATA, 0, 0, 0)) {
        log_message("Failed to send HTTP request", GetLastError());
        WinHttpCloseHandle(hRequest);
        WinHttpCloseHandle(hConnect);
        WinHttpCloseHandle(hSession);
        return false;
    }

    if (!WinHttpReceiveResponse(hRequest, NULL)) {
        log_message("Failed to receive HTTP response", GetLastError());
        WinHttpCloseHandle(hRequest);
        WinHttpCloseHandle(hConnect);
        WinHttpCloseHandle(hSession);
        return false;
    }

    std::string responseData;
    DWORD bytesRead = 0;
    char buffer[4096];
    do {
        if (!WinHttpReadData(hRequest, buffer, sizeof(buffer), &bytesRead)) {
            log_message("Failed to read HTTP data", GetLastError());
            WinHttpCloseHandle(hRequest);
            WinHttpCloseHandle(hConnect);
            WinHttpCloseHandle(hSession);
            return false;
        }
        responseData.append(buffer, bytesRead);
    } while (bytesRead > 0);

    WinHttpCloseHandle(hRequest);
    WinHttpCloseHandle(hConnect);
    WinHttpCloseHandle(hSession);

    // Basic JSON parsing for latest version
    size_t tag_name_pos = responseData.find("\"tag_name\"");
    if (tag_name_pos == std::string::npos) {
        log_message("Failed to find tag_name in response");
        return false;
    }
    size_t version_start_pos = responseData.find("\"", tag_name_pos + 10) + 1;
    size_t version_end_pos = responseData.find("\"", version_start_pos);
    if (version_start_pos == std::string::npos || version_end_pos == std::string::npos) {
        log_message("Failed to parse version from response");
        return false;
    }
    std::string latest_version = responseData.substr(version_start_pos, version_end_pos - version_start_pos);

    // Compare versions
    log_message("Current version: " + current_version + ", Latest version: " + latest_version);
    if (latest_version.length() > current_version.length() || (latest_version.length() == current_version.length() && latest_version > current_version))
    {
        std::cout << "A new version is available: " << latest_version << std::endl;
        return true;
    }

    return false;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    try {
        SetErrorMode(SEM_FAILCRITICALERRORS | SEM_NOOPENFILEERRORBOX);

        char cwd[MAX_PATH] = { 0 };
        if (!GetCurrentDirectoryA(sizeof(cwd), cwd)) {
            log_message("Failed to get current directory", GetLastError());
            return 1;
        }

        // Determine which browser section to use based on command-line arguments or default to "Browser"
        std::string browser_section = "Browser";
        if (lpCmdLine && *lpCmdLine) {
            std::string cmdLineStr(lpCmdLine);
            size_t browser_arg_pos = cmdLineStr.find("--browser=");
            if (browser_arg_pos != std::string::npos) {
                size_t browser_name_start = browser_arg_pos + 10;
                size_t browser_name_end = cmdLineStr.find(" ", browser_name_start);
                if (browser_name_end == std::string::npos) {
                    browser_name_end = cmdLineStr.length();
                }
                browser_section = "Browser" + cmdLineStr.substr(browser_name_start, browser_name_end - browser_name_start);
            }
        }

        // Read configuration
        auto browser_settings = read_config_file(CONFIG_FILE, browser_section);
        auto general_settings = read_config_file(CONFIG_FILE, "General");

        std::string browser_path;
        std::string browser_flags;
        std::string version_url;
        bool update_check = false;

        for (const auto& setting : browser_settings) {
            if (setting.first == "Executable") {
                browser_path = setting.second;
            } else if (setting.first == "Flags") {
                browser_flags = setting.second;
            } else if (setting.first == "VersionUrl") {
                version_url = setting.second;
            }
        }

        for (const auto& setting : general_settings) {
            if (setting.first == "UpdateCheck") {
                update_check = (setting.second == "true");
            }
        }

        // Validate browser path
        if (browser_path.empty() || !PathFileExistsA(browser_path.c_str())) {
            log_message("Browser executable not found or not specified in config file: " + browser_path);
            std::cerr << "Error: Browser executable not found or not specified in config file: " << browser_path << std::endl;
            return 1;
        }

        // Get and display browser version
        std::string browser_version = get_browser_version(browser_path);
        std::cout << "Launching " << browser_section << " Version: " << browser_version << std::endl;

        // Perform update check if enabled
        if (update_check) {
            check_for_updates(browser_version, version_url);
        }

        // Construct command line
        std::string final_cmd = "\"" + browser_path + "\" " + browser_flags;

        // Append user-provided arguments
        if (lpCmdLine && *lpCmdLine) {
            char sanitized_args[MAX_CMD_LENGTH] = { 0 };
            strncpy_s(sanitized_args, lpCmdLine, MAX_CMD_LENGTH - 1);
            sanitize_command(sanitized_args);
            final_cmd += " ";
            final_cmd += sanitized_args;
        }

        // Check for command-line length
        if (final_cmd.length() > MAX_CMD_LENGTH) {
          log_message("Command-line arguments are too long");
          std::cerr << "Error: Command-line arguments are too long" << std::endl;
          return 1;
        }

        // Create process
        STARTUPINFOA si = { 0 };
        PROCESS_INFORMATION pi = { 0 };
        si.cb = sizeof(si);

        if (!CreateProcessA(NULL, const_cast<char*>(final_cmd.c_str()), NULL, NULL, FALSE,
            CREATE_NEW_PROCESS_GROUP, NULL, cwd, &si, &pi)) {
            log_message("Failed to create process: " + final_cmd, GetLastError());
            std::cerr << "Error: Failed to create process: " << final_cmd << std::endl;
            return 1;
        }

        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);

        return 0;
    } catch (const std::exception& e) {
        log_message("An exception occurred: " + std::string(e.what()));
        std::cerr << "Error: An exception occurred: " << e.what() << std::endl;
        return 1;
    }
}
```

**Key Features:**

*   **`read_config_file`:** Reads the `browser_config.ini` file and parses the specified section, returning a vector of key-value pairs. It handles missing or invalid configuration files by logging an error and returning an empty vector. It also checks if the configuration section is empty or invalid after parsing.
*   **`get_browser_version`:** Retrieves the version of the specified browser executable using the Windows Version API. It handles cases where the version information cannot be retrieved or is invalid.
*   **`check_for_updates`:** Performs an update check by fetching the latest version from the specified `VersionUrl` (if provided) and comparing it with the current version. It uses WinHTTP for making HTTP requests and includes error handling for various stages of the process, such as network issues, URL parsing, and JSON parsing.
*   **`sanitize_command`:** Sanitizes command-line arguments by removing potentially dangerous characters that could be used for command injection, such as `&`, `|`, `;`, `` ` ``, `$`, `<`, `>`, `^`, `(`, `)`, `[`, `]`, `{`, `}`.
*   **`WinMain`:** The main entry point of the application. It performs the following actions:
    *   Sets the error mode to prevent error dialogs from appearing.
    *   Gets the current working directory.
    *   Determines the browser section to use based on command-line arguments (if provided) using the `--browser=` argument.
    *   Reads the configuration from `browser_config.ini`.
    *   Validates the browser path, logging an error and exiting if the path is invalid or the executable is not found.
    *   Retrieves and displays the browser version.
    *   Performs an update check if enabled.
    *   Constructs the final command line by combining the browser path, flags, and user-provided arguments.
    *   Appends sanitized user-provided arguments to the command line.
    *   Checks for command-line length, logging an error and exiting if the command line is too long.
    *   Creates a new process to launch the browser using `CreateProcessA`, logging an error and exiting if the process creation fails.
    *   Closes the process and thread handles.
    *   Includes exception handling to catch and log any exceptions that occur during the process.

## Build Instructions

To build the browser launcher, you'll need a C++ compiler that supports Windows development, such as MinGW or Visual Studio.

*   **Using Visual Studio:**
    1. Open the Visual Studio Developer Command Prompt.
    2. Navigate to the directory where you saved the C++ code (e.g., `browser_launcher.cpp`).
    3. Compile using the following command:

        ```bash
        cl /EHsc /W4 /Ox /std:c++17 browser_launcher.cpp /link shlwapi.lib Version.lib winhttp.lib
        ```


*   **Using MinGW:**
    1. Open the MinGW command prompt.
    2. Navigate to the directory where you saved the C++ code.
    3. Compile using the following command:

        ```bash
        g++ -o browser_launcher.exe browser_launcher.cpp -lshlwapi -lversion -lwinhttp -std=c++17
        ```

## Deployment and Updates

After building the launcher, you can deploy it by placing the executable (`browser_launcher.exe`) and the `browser_config.ini` file in the desired location. To update the browser, you can use the following script:

```batch
@echo off
set BROWSER_DIR=
cd /d %BROWSER_DIR%

if exist .exe.new (
    move /y .exe .exe.old
    move /y .exe.new .orig.exe
    copy /y wrapper.exe .exe
)
```

This script assumes that the new browser executable is named `.exe.new` and the wrapper executable is named `wrapper.exe`. It renames the existing browser executable, moves the new executable into place, and copies the wrapper executable over the original browser executable. You may need to modify this script based on your specific browser and directory structure. For example, for Iron Portable, the script would be:

```batch
@echo off
set BROWSER_DIR=\IronPortable64\Iron
cd /d %BROWSER_DIR%

if exist IronPortable.exe.new (
    move /y IronPortable.exe IronPortable.exe.old
    move /y IronPortable.exe.new IronPortable.orig.exe
    copy /y browser_launcher.exe IronPortable.exe
) else (
    if exist IronPortable.exe (
        move /y IronPortable.exe IronPortable.orig.exe
        copy /y browser_launcher.exe IronPortable.exe
    )
)
```

**Update Process:**

1. The launcher checks for updates if `UpdateCheck` is set to `true` in the `[General]` section of `browser_config.ini` and a `VersionUrl` is provided in the `[Browser]` section.
2. The `check_for_updates` function fetches the latest version information from the `VersionUrl` using WinHTTP.
3. It parses the JSON response (assuming the response is in JSON format) to extract the latest version number.
4. It compares the latest version with the current browser version.
5. If a newer version is available, it notifies the user.
6. The actual download and installation of the new version are not handled by the launcher and would typically be performed manually or through a separate update mechanism.

**Error Handling:**

The launcher includes error handling for various scenarios:

*   **Missing or Invalid Configuration File:** If `browser_config.ini` is missing or cannot be opened, the launcher logs an error and terminates. If a specific section is missing or invalid, it logs an error and uses default values or terminates, depending on the criticality of the missing information.
*   **Missing Browser Executable:** If the specified browser executable is not found, the launcher logs an error and terminates.
*   **Failed Update Check:** If the update check fails (e.g., due to network issues or invalid URL), the launcher logs an error and continues launching the browser with the existing version.
*   **Failed Version Retrieval:** If the launcher cannot retrieve the browser version, it logs an error and uses a default version or terminates, depending on whether the version information is critical.
*   **Command-line Arguments Too Long:** If the combined length of the command line exceeds the maximum allowed length, the launcher logs an error, truncates the arguments, or terminates.
*   **Failed Process Creation:** If the launcher fails to create a new process for the browser, it logs an error and terminates.
*   **Log File Error:** If the launcher cannot open the log file, it logs an error to the standard error stream.

## Usage

To use the launcher:

1. **Modify Configuration:** Edit `browser_config.ini` to specify the browser executable, flags, and update settings for each browser you want to manage.
2. **Run Launcher:** Execute `browser_launcher.exe` to start the browser with custom configurations.
3. **Additional Arguments:** Pass extra command-line arguments; they are sanitized and forwarded to the browser.
4. **Select Browser Configuration:** Use the `--browser=` argument to choose a specific browser configuration:

    ```bash
    browser_launcher.exe --browser=2
    ```

    This selects the `[Browser2]` section from the configuration file.
5. **Update Checks:** Ensure `UpdateCheck=true` in the `[General]` section to enable update checking. Provide a valid `VersionUrl` in the browser section for update verification.

## Simplified Version without Update Checking

If you don't need the update checking functionality, you can use a simplified version of the C++ code without the `check_for_updates` function and the related code in `WinMain`. This will reduce the complexity of the launcher and remove the dependency on the `WinHTTP` library. You can remove the `VersionUrl` parameter from the configuration file in this case.



Here's the simplified C++ code without the update checking functionality:

```cpp
#include <windows.h>
#include <shlwapi.h>
#include <fstream>
#include <sstream>
#include <iostream>
#include <vector>
#include <algorithm>

#pragma comment(lib, "shlwapi.lib")
#pragma comment(lib, "Version.lib")

#define MAX_CMD_LENGTH 32768
#define LOG_FILE "browser_wrapper.log"
#define CONFIG_FILE "browser_config.ini"

// Function to log messages to a file
void log_message(const std::string& message, DWORD error_code = 0) {
    std::ofstream log_file(LOG_FILE, std::ios::app);
    if (log_file.is_open()) {
        SYSTEMTIME st;
        GetLocalTime(&st);
        char timestamp[20];
        sprintf_s(timestamp, sizeof(timestamp), "[%02d:%02d:%02d]", st.wHour, st.wMinute, st.wSecond);
        log_file << timestamp << " " << message;
        if (error_code != 0) {
            log_file << " (Error: " << error_code << ")";
        }
        log_file << std::endl;
        log_file.close();
    }
}

// Function to sanitize command-line arguments
void sanitize_command(char* cmdLine) {
    const char* dangerous_chars = "&|;`$<>^()[]{}";
    char* dst = cmdLine;
    for (char* src = cmdLine; *src != '\0'; ++src) {
        if (!strchr(dangerous_chars, *src)) {
            *dst++ = *src;
        }
    }
    *dst = '\0';
}

// Function to read the configuration file
std::vector<std::pair<std::string, std::string>> read_config_file(const std::string& config_file, const std::string& section) {
    std::vector<std::pair<std::string, std::string>> settings;
    std::ifstream file(config_file);
    std::string line;
    bool in_section = false;

    if (!file.is_open()) {
        log_message("Failed to open config file: " + config_file, GetLastError());
        return settings;
    }

    while (std::getline(file, line)) {
        // Remove leading/trailing whitespace
        line.erase(0, line.find_first_not_of(" \t"));
        line.erase(line.find_last_not_of(" \t") + 1);

        // Skip comments and empty lines
        if (line.empty() || line[0] == '#') {
            continue;
        }

        if (line[0] == '[') {
            // Check if we are entering the desired section
            in_section = (line == "[" + section + "]");
        } else if (in_section) {
            // Parse key-value pairs
            size_t delimiter_pos = line.find('=');
            if (delimiter_pos != std::string::npos) {
                std::string key = line.substr(0, delimiter_pos);
                std::string value = line.substr(delimiter_pos + 1);
                // Remove leading/trailing whitespace from key and value
                key.erase(0, key.find_first_not_of(" \t"));
                key.erase(key.find_last_not_of(" \t") + 1);
                value.erase(0, value.find_first_not_of(" \t"));
                value.erase(value.find_last_not_of(" \t") + 1);
                settings.push_back(std::make_pair(key, value));
            }
        }
    }
    return settings;
}

// Function to get the browser version
std::string get_browser_version(const std::string& browser_path) {
    DWORD verHandle = 0;
    UINT size = 0;
    LPBYTE lpBuffer = NULL;
    std::string version = "Unknown";

    DWORD verSize = GetFileVersionInfoSizeA(browser_path.c_str(), &verHandle);
    if (verSize == 0) {
        log_message("Failed to get version info size for: " + browser_path, GetLastError());
        return version;
    }

    std::vector<char> verData(verSize);
    if (!GetFileVersionInfoA(browser_path.c_str(), verHandle, verSize, verData.data())) {
        log_message("Failed to get version info for: " + browser_path, GetLastError());
        return version;
    }

    if (!VerQueryValueA(verData.data(), "\\", (VOID FAR * FAR*)&lpBuffer, &size) || size == 0) {
        log_message("Failed to query version value for: " + browser_path, GetLastError());
        return version;
    }

    VS_FIXEDFILEINFO* verInfo = (VS_FIXEDFILEINFO*)lpBuffer;
    if (verInfo->dwSignature != 0xfeef04bd) {
        log_message("Invalid version info signature for: " + browser_path);
        return version;
    }

    version = std::to_string((verInfo->dwFileVersionMS >> 16) & 0xffff) + "." +
              std::to_string((verInfo->dwFileVersionMS >> 0) & 0xffff) + "." +
              std::to_string((verInfo->dwFileVersionLS >> 16) & 0xffff) + "." +
              std::to_string((verInfo->dwFileVersionLS >> 0) & 0xffff);
    return version;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    try {
        SetErrorMode(SEM_FAILCRITICALERRORS | SEM_NOOPENFILEERRORBOX);

        char cwd[MAX_PATH] = { 0 };
        if (!GetCurrentDirectoryA(sizeof(cwd), cwd)) {
            log_message("Failed to get current directory", GetLastError());
            return 1;
        }

        // Determine which browser section to use based on command-line arguments or default to "Browser"
        std::string browser_section = "Browser";
        if (lpCmdLine && *lpCmdLine) {
            std::string cmdLineStr(lpCmdLine);
            size_t browser_arg_pos = cmdLineStr.find("--browser=");
            if (browser_arg_pos != std::string::npos) {
                size_t browser_name_start = browser_arg_pos + 10;
                size_t browser_name_end = cmdLineStr.find(" ", browser_name_start);
                if (browser_name_end == std::string::npos) {
                    browser_name_end = cmdLineStr.length();
                }
                browser_section = "Browser" + cmdLineStr.substr(browser_name_start, browser_name_end - browser_name_start);
            }
        }

        // Read configuration
        auto browser_settings = read_config_file(CONFIG_FILE, browser_section);

        std::string browser_path;
        std::string browser_flags;

        for (const auto& setting : browser_settings) {
            if (setting.first == "Executable") {
                browser_path = setting.second;
            } else if (setting.first == "Flags") {
                browser_flags = setting.second;
            }
        }

        // Validate browser path
        if (browser_path.empty() || !PathFileExistsA(browser_path.c_str())) {
            log_message("Browser executable not found or not specified in config file: " + browser_path);
            return 1;
        }

        // Get and display browser version
        std::string browser_version = get_browser_version(browser_path);
        std::cout << "Launching " << browser_section << " Version: " << browser_version << std::endl;

        // Construct command line
        std::string final_cmd = "\"" + browser_path + "\" " + browser_flags;

        // Append user-provided arguments
        if (lpCmdLine && *lpCmdLine) {
            char sanitized_args[MAX_CMD_LENGTH] = { 0 };
            strncpy_s(sanitized_args, lpCmdLine, MAX_CMD_LENGTH - 1);
            sanitize_command(sanitized_args);
            final_cmd += " ";
            final_cmd += sanitized_args;
        }

        // Create process
        STARTUPINFOA si = { 0 };
        PROCESS_INFORMATION pi = { 0 };
        si.cb = sizeof(si);

        if (!CreateProcessA(NULL, const_cast<char*>(final_cmd.c_str()), NULL, NULL, FALSE,
            CREATE_NEW_PROCESS_GROUP, NULL, cwd, &si, &pi)) {
            log_message("Failed to create process: " + final_cmd, GetLastError());
            return 1;
        }

        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);

        return 0;
    } catch (const std::exception& e) {
        log_message("An exception occurred: " + std::string(e.what()));
        return 1;
    }
}
```

**Building the Simplified Version:**

The build instructions for the simplified version are the same as for the full version, except that you don't need to link the `winhttp.lib` library.

**Using Visual Studio:**

```bash
cl /EHsc /W4 /Ox /std:c++17 browser_launcher_simple.cpp /link shlwapi.lib Version.lib
```

**Using MinGW:**

```bash
g++ -o browser_launcher_simple.exe browser_launcher_simple.cpp -lshlwapi -lversion -std=c++17
```
