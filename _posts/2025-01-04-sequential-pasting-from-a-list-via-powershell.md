---

tags: [scripts>powershell]
info: aberto.
date: 2025-01-04
type: post
layout: post
published: true
slug: sequential-pasting-from-a-list-via-powershell
title: 'Sequential pasting from a list via PowerShell'
---
This tool is particularly useful for tasks that require repetitive data entry, such as inputting serial numbers, codes, or form data, without the need to manually copy and paste each item individually.

### **Overview**

-   **Sequential Pasting:** Enables users to paste items from a list one after another by pressing a designated hotkey.
-   **Global Hotkeys:** Implements system-wide hotkeys to control the script's actions, such as pasting the next item, pausing/resuming the process, and quitting the script.
-   **User Interface:** Runs silently in the background with minimal user interface interaction, displaying messages when necessary to inform the user of important events or errors.

### **Key Components**

1.  **Loading Required Assemblies**
    
    ```powershell
    Add-Type -AssemblyName System.Windows.Forms
    ```
    
    -   Loads the necessary .NET assembly to access Windows Forms classes and methods, enabling features like message boxes and clipboard operations within the script.
2.  **Configuration Settings**
    
    ```powershell
    $Config = @{
        ListFilePath = "$HOME\Documents\list.txt"
        Hotkeys = @{
            Paste = 'Control+F11'
            # Pause = 'Control+Shift+F11'    # Updated hotkey to avoid conflicts
            Quit  = 'Control+F12'
        }
        AutoTab = $false
    }
    ```
    
    -   **ListFilePath:** Specifies the path to the text file containing the items to be pasted. Users can modify this path to point to their desired file location.
    -   **Hotkeys:** Defines the global hotkeys for controlling the script:
        -   **Paste:** Pressing `Control+F11` triggers the script to paste the next item in the list.
        -   **Pause:** (Commented out by default) Can be enabled to toggle pausing and resuming the pasting process.
        -   **Quit:** Pressing `Control+F12` exits the script.
    -   **AutoTab:** If set to `$true`, the script sends a `Tab` key after pasting each item, which is useful for moving to the next input field automatically.
3.  **Function `Show-Message`**
    
    -   A utility function that displays message boxes with customizable messages, titles, and icons. It uses Windows Forms to present information to the user, such as notifications or error messages.
4.  **Function `Load-ListItems`**
    
    -   Validates and loads the items from the specified list file. The function checks if the file exists and is not empty. It reads the contents into an array, ignoring any empty lines.
    -   If the file is not found or is empty, the function displays an error message and exits the script gracefully.
5.  **Function `Parse-Hotkeys`**
    
    -   Parses the hotkey strings defined in the configuration and converts them into modifier keys and virtual key codes that the Windows API can interpret.
    -   Associates each hotkey with a unique identifier (ID) required for registering the hotkeys with the system.
6.  **Hotkey Message Filter**
    
    -   Implements a custom message filter using the `IMessageFilter` interface to intercept Windows messages, specifically `WM_HOTKEY`.
    -   This allows the script to detect when the registered global hotkeys are pressed, even if the script's window is not in focus.
7.  **Function `Start-Paster`**
    
    -   The main function that encapsulates the script's core logic:
        -   **Initialization:** Loads the list items and initializes variables such as the current index and pause state.
        -   **Hotkey Registration:** Registers the global hotkeys using Windows API functions `RegisterHotKey` and `UnregisterHotKey`.
        -   **Hidden Form Creation:** Creates an invisible Windows Form to handle message processing and to keep the script running.
        -   **Hotkey Actions:**
            -   **Paste:** When the paste hotkey is pressed, the script checks if it is not paused and pastes the next item:
                -   Copies the current item to the clipboard.
                -   Simulates a `Ctrl+V` key press to paste the item into the active application.
                -   Optionally sends a `Tab` key if `AutoTab` is enabled.
                -   Increments the index to move to the next item.
                -   If all items have been pasted, the script notifies the user and exits.
            -   **Pause:** (If enabled) Toggles the paused state and informs the user.
            -   **Quit:** Exits the script gracefully.
        -   **Cleanup:** Unregisters hotkeys and removes message filters when the script is closed.
8.  **Starting the Script**
    
    ```powershell
    Start-Paster
    ```
    
    -   Invokes the main function to commence the sequential pasting process.

### **Usage Instructions**

**Prerequisites:**

-   **PowerShell Version:** Ensure you are running PowerShell 5.0 or higher.
-   **Execution Policy:** By default, PowerShell restricts script execution. You may need to adjust the execution policy to run this script:
    -   Open PowerShell as an administrator.
    -   Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.
    -   This allows you to run scripts you have written or downloaded from trusted sources.

**Setup:**

1.  **Prepare the List File:**
    
    -   Create a text file at the path specified by `ListFilePath` (e.g., `C:\Users\YourName\Documents\list.txt`).
    -   Add the items you wish to paste, placing each item on a new line.
2.  **Configure the Script:**
    
    -   Modify the `$Config` hashtable in the script if you wish to change file paths, hotkeys, or enable features like `AutoTab` or `Pause`.

**Running the Script:**

-   Open PowerShell and navigate to the directory containing the script.
-   Execute the script by typing `.\SequentialPaster.ps1` (replace with the script's actual filename).
-   A message box will appear, confirming that the Sequential Paster is running.

**Using the Hotkeys:**

-   **Paste Next Item:** Press `Control+F11` to paste the next item in your list.
-   **Pause/Resume:** If enabled, press the configured hotkey (e.g., `Control+Shift+F11`) to pause or resume the pasting process.
-   **Quit:** Press `Control+F12` to stop the script.

**Notes:**

-   If you reach the end of your list, the script will notify you that all items have been pasted and will exit automatically.
-   If you attempt to paste while the script is paused, it will inform you that pasting is currently paused.

### **Understanding How the Script Works**

-   **Sequential Processing:**
    
    -   The script keeps track of the current item using an index. Each time you press the paste hotkey, it processes the next item in the array.
-   **Global Hotkeys:**
    
    -   Global hotkeys are registered with the Windows operating system, allowing the script to respond to key presses regardless of which application is currently active.
-   **Clipboard Management:**
    
    -   The script uses the Windows clipboard to transfer text. It copies the next item to the clipboard and then simulates a `Ctrl+V` key press to paste it.
-   **Error Handling:**
    
    -   The script includes error handling to manage issues such as missing or empty list files, hotkey registration failures, and attempting to paste beyond the end of the list.

### **Common Issues and Troubleshooting**

-   **Hotkey Conflicts:**
    
    -   If hotkey registration fails, the script will display an error message with an error code.
        -   **Error Code 1409:** Indicates that the hotkey is already in use by another application.
        -   **Resolution:** Modify the hotkeys in the `$Config.Hotkeys` hashtable to use a different combination.
-   **Script Execution Policy Errors:**
    
    -   If you receive an error about script execution being disabled, adjust your execution policy as outlined in the prerequisites.
-   **Permissions:**
    
    -   Running the script typically does not require administrative privileges. However, ensure that your user account has the necessary permissions to execute scripts and access the specified files.

### **Customizing the Script**

-   **Changing Hotkeys:**
    
    -   Update the hotkey combinations in the `$Config.Hotkeys` hashtable to suit your preferences.
    -   Use key names recognized by `[System.Windows.Forms.Keys]` for compatibility.
-   **Enabling AutoTab:**
    
    -   Set `$Config.AutoTab` to `$true` if you want the script to automatically send a `Tab` key after pasting each item.
-   **Enabling Pause Functionality:**
    
    -   Uncomment and configure the `Pause` hotkey in the configuration to enable pausing and resuming the pasting process.

### **code**

{% codeblock powershell %}
# Sequential Paster.ps1 - Corrected Version with Proper Variable Scoping

# Load necessary assemblies

Add-Type -AssemblyName System.Windows.Forms

# Configuration

$Config = @{ ListFilePath = "$HOME\\Documents\\list.txt" Hotkeys = @{ Paste = 'Control+F11'

# Pause = 'Control+Shift+F11' # Updated hotkey to avoid conflicts

```
    Quit  = 'Control+F12'
}
AutoTab = $false
```

}

# Function to display messages

function Show-Message { param( \[string\]$Message, \[string\]$Title = "Sequential Paster", \[string\]$IconType = "Information" ) $icon = switch ($IconType.ToLower()) { "information" { \[System.Windows.Forms.MessageBoxIcon\]::Information } "error" { \[System.Windows.Forms.MessageBoxIcon\]::Error } "warning" { \[System.Windows.Forms.MessageBoxIcon\]::Warning } default { \[System.Windows.Forms.MessageBoxIcon\]::Information } } \[System.Windows.Forms.MessageBox\]::Show($Message, $Title, \[System.Windows.Forms.MessageBoxButtons\]::OK, $icon) | Out-Null }

# Validate and load items from the list file

function Load-ListItems { try { if (-not (Test-Path -Path $Config.ListFilePath)) { Show-Message "List file not found at:`n$($Config.ListFilePath)`nPlease create it and add items." "Error" "Error" exit } $ListItems = Get-Content -Path $Config.ListFilePath -Encoding UTF8 | Where-Object { $*.Trim() } if ($ListItems.Count -eq 0) { Show-Message "The list file is empty." "Error" "Error" exit } return $ListItems } catch { Show-Message "Error reading list file: $*" "Error" "Error" exit } }

# Parse hotkey strings into modifier keys and virtual key codes

function Parse-Hotkeys { param(\[hashtable\]$HotkeyConfig) $hotkeyMappings = @{} foreach ($key in $HotkeyConfig.Keys) { try { $hotkeyString = $HotkeyConfig\[$key\] $modifiers = 0 $keyCode = 0 $parts = $hotkeyString -split '+' foreach ($part in $parts) { switch ($part.ToLower()) { 'control' { $modifiers += 2 } 'shift' { $modifiers += 4 } 'alt' { $modifiers += 1 } default { $keyCode = \[int\]\[System.Windows.Forms.Keys\]::$part } } } $hotkeyMappings\[$key\] = @{ Modifiers = $modifiers KeyCode = $keyCode ID = \[System.Guid\]::NewGuid().GetHashCode() } } catch { Show-Message "Invalid hotkey configuration for '$key': $hotkeyString" "Error" "Error" exit } } return $hotkeyMappings }

# Implement the IMessageFilter interface for handling messages

Add-Type -ReferencedAssemblies "System.Windows.Forms" -TypeDefinition @" using System; using System.Windows.Forms;

public class HotkeyMessageFilter : IMessageFilter { public delegate void HotkeyPressedHandler(int hotkeyId); public event HotkeyPressedHandler HotkeyPressed;

```
public bool PreFilterMessage(ref Message m)
{
    const int WM_HOTKEY = 0x0312;
    if (m.Msg == WM_HOTKEY)
    {
        int hotkeyId = m.WParam.ToInt32();
        if (HotkeyPressed != null)
        {
            HotkeyPressed.Invoke(hotkeyId);
        }
        return true;
    }
    return false;
}
```

} "@

# Main logic encapsulated in a function

function Start-Paster { $script:ListItems = Load-ListItems $script:CurrentIndex = 0 $script:IsPaused = $false

```
$Hotkeys = Parse-Hotkeys -HotkeyConfig $Config.Hotkeys

Add-Type -MemberDefinition @"
    [DllImport("user32.dll", SetLastError = true)]
    public static extern bool RegisterHotKey(IntPtr hWnd, int id, int fsModifiers, int vk);

    [DllImport("user32.dll", SetLastError = true)]
    public static extern bool UnregisterHotKey(IntPtr hWnd, int id);
```

"@ -Name "NativeMethods" -Namespace "WinAPI"

```
$form = New-Object System.Windows.Forms.Form
$form.WindowState = 'Minimized'
$form.ShowInTaskbar = $false

# Register hotkeys
foreach ($hotkeyName in $Hotkeys.Keys) {
    $hotkey = $Hotkeys[$hotkeyName]
    $registered = [WinAPI.NativeMethods]::RegisterHotKey($form.Handle, $hotkey.ID, $hotkey.Modifiers, $hotkey.KeyCode)
    if (-not $registered) {
        $errorCode = [Runtime.InteropServices.Marshal]::GetLastWin32Error()
        Show-Message "Failed to register hotkey '$hotkeyName'. Error code: $errorCode" "Error" "Error"
        exit
    }
}

# Create an instance of the message filter
$filter = New-Object HotkeyMessageFilter

# Add the message filter to the application
[System.Windows.Forms.Application]::AddMessageFilter($filter)

# Define the action when a hotkey is pressed
$filter.add_HotkeyPressed({
    param($hotkeyId)

    foreach ($hotkeyName in $Hotkeys.Keys) {
        if ($Hotkeys[$hotkeyName].ID -eq $hotkeyId) {
            switch ($hotkeyName) {
                'Paste' {
                    if (-not $script:IsPaused) {
                        if ($script:CurrentIndex -lt $script:ListItems.Count) {
                            $item = $script:ListItems[$script:CurrentIndex]
                            try {
                                [System.Windows.Forms.Clipboard]::SetText($item)
                                [System.Windows.Forms.SendKeys]::SendWait('^v')
                                if ($Config.AutoTab) {
                                    Start-Sleep -Milliseconds 50
                                    [System.Windows.Forms.SendKeys]::SendWait('{TAB}')
                                }
                                $script:CurrentIndex++
                            } catch {
                                Show-Message "Error during paste: $_" "Error" "Error"
                            }
                            if ($script:CurrentIndex -ge $script:ListItems.Count) {
                                Show-Message "All items pasted." "Info" "Information"
                                $form.Close()
                            }
                        }
                    } else {
                        Show-Message "Pasting is paused." "Info" "Information"
                    }
                }
                'Pause' {
                    $script:IsPaused = -not $script:IsPaused
                    $status = if ($script:IsPaused) { 'Paused' } else { 'Resumed' }
                    Show-Message "Pasting $status." "Info" "Information"
                }
                'Quit' {
                    Show-Message "Quitting." "Info" "Information"
                    $form.Close()
                }
            }
            break
        }
    }
})

# Form Closed event handler
$form.add_FormClosed({
    # Unregister hotkeys
    foreach ($hotkey in $Hotkeys.Values) {
        [WinAPI.NativeMethods]::UnregisterHotKey($form.Handle, $hotkey.ID) | Out-Null
    }
    # Remove the message filter
    [System.Windows.Forms.Application]::RemoveMessageFilter($filter)
    [System.Windows.Forms.Application]::Exit()
})

# Show startup message
Show-Message "Sequential Paster is running.`nUse the configured hotkeys to control it." "Info" "Information"

# Start the application loop
[System.Windows.Forms.Application]::Run($form)
```

}

# Start the paster

Start-Paster
{% endcodeblock %}