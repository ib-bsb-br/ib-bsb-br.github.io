---
tags: [scratchpad, iphone>shortcuts, linux]
info: aberto.
date: 2024-10-26
type: post
layout: post
published: true
slug: a-shell_thermal
title: 'iOS Shortcut for Linux Thermal Printing'
---

## Introduction

This solution leverages a-Shell, SSH, and embedded `dash` scripts to automate tasks on a remote Debian server. It focuses on efficiency, security, and user feedback through notifications.

## Prerequisites

- An iPhone with a-Shell installed.
- A Debian server with SSH access enabled.
- Basic familiarity with SSH key management.
- A thermal printer configured on the Debian server.

## Debian Server Setup

### Ensure `thermal.sh` Functionality

Since we'll be embedding the `thermal.sh` scripts within the a-Shell script, you don't need to have `thermal.sh` files on the server. However, ensure that your server has:

- The `lp` command available (usually part of the CUPS system).
- The thermal printer correctly configured and accessible via the `lp` command.
- Necessary utilities like `iconv` installed.

You can install `iconv` if it's not present:

```sh
sudo apt-get update
sudo apt-get install libc-bin
```

## SSH Configuration

Set up SSH key-based authentication to enable passwordless SSH connections from your iPhone to the Debian server.

### Generating SSH Keys on a-Shell

1. Open a-Shell on your iPhone.
2. Generate an SSH key pair:

   ```sh
   ssh-keygen -t rsa -b 2048
   ```

3. Accept the default file location and enter a passphrase if desired (leave empty for no passphrase).

### Copying Your Public Key to the Debian Server

1. Copy your public key to the server:

   ```sh
   ssh-copy-id yourusername@your_server_ip
   ```

   Replace `yourusername` with your actual username on the Debian server and `your_server_ip` with the server's IP address or hostname.

2. Test the SSH connection:

   ```sh
   ssh yourusername@your_server_ip
   ```

   You should be able to connect without entering a password.

## Create the a-Shell Script

Create the `remote_control.sh` script on your iPhone to pass the text directly to the embedded `thermal.sh` scripts on the server.

### Steps to Create `remote_control.sh`

1. Open a-Shell on your iPhone.
2. Run the following command to create the script:

   ```sh
   cat > ~/.shortcuts/remote_control.sh << 'EOL'
   #!/bin/dash

   # Configuration (Update with your actual credentials)
   SSH_USER="yourusername"
   SSH_HOST="your_server_ip"

   # Function to display notification in a-Shell
   show_notification() {
       message="$1"
       echo "$message" >&2  # Print to stderr for visibility in a-Shell and Shortcuts
   }

   # Function to run command with error handling
   run_command() {
       command="$1"
       error_message="$2"
       if ! eval "$command"; then
           show_notification "Error: $error_message"
           exit 1
       fi
   }

   # Main execution
   TEXT_CONTENT="$1"

   # Check if text content is provided
   if [ -z "$TEXT_CONTENT" ]; then
       show_notification "Error: No text content provided."
       exit 1
   fi

   # SSH command with error handling and passing the text directly to thermal.sh
   SSH_COMMAND="ssh -o BatchMode=yes -o ConnectTimeout=5 $SSH_USER@$SSH_HOST"

   # Embedded Normal Thermal Script
   NORMAL_THERMAL_SCRIPT='#!/bin/dash

   # Check for input
   if [ -z "$1" ]; then
     echo "Error: No text input provided."
     exit 1
   fi

   # Escape % to prevent printf interpretation
   escaped_content=$(echo "$1" | sed "s/%/%%/g")

   # Convert the encoding while suppressing specific iconv errors
   converted_text=$(echo "$escaped_content" | iconv -f UTF-8 -t CP850//TRANSLIT//IGNORE 2>/dev/null)

   # Print the formatted text to the thermal printer
   if ! printf "\033@%s\n\n\n\033i" "$converted_text" | lp -d thermal -o raw; then
     echo "Failed to print. Please check the printer and its configuration."
     exit 1
   fi

   echo "Success: Text printed successfully."
   '

   # Create and execute the normal thermal script on the server
   run_command "echo \"$NORMAL_THERMAL_SCRIPT\" | $SSH_COMMAND 'cat > /tmp/normal_thermal.sh && chmod +x /tmp/normal_thermal.sh'" "Failed to transfer normal thermal script."
   run_command "echo \"$TEXT_CONTENT\" | $SSH_COMMAND '/tmp/normal_thermal.sh \"\$(cat -)\"'" "Failed to execute normal thermal script."

   # Optionally, you can comment out the reverse thermal script execution if not needed
   # Embedded Reverse White Thermal Script
   REVERSE_THERMAL_SCRIPT='#!/bin/dash

   # Check for input
   if [ -z "$1" ]; then
     echo "Error: No text input provided."
     exit 1
   fi

   # Escape % to prevent printf interpretation
   escaped_content=$(echo "$1" | sed "s/%/%%/g")

   # Convert the encoding while suppressing specific iconv errors
   converted_text=$(echo "$escaped_content" | iconv -f UTF-8 -t CP850//TRANSLIT//IGNORE 2>/dev/null)

   # Print the formatted text to the thermal printer with reverse white printing
   if ! printf "\032[\001\000\000\000\000@\002\260\004\000\032T\001\000\000\000\000\030\000\004\000%s\000\032]\000\032O\000\033i" "$converted_text" | lp -d thermal -o raw; then
     echo "Failed to print. Please check the printer and its configuration."
     exit 1
   fi

   echo "Success: Reverse white text printed successfully."
   '

   # Uncomment the following lines to execute the reverse thermal script
   # run_command "echo \"$REVERSE_THERMAL_SCRIPT\" | $SSH_COMMAND 'cat > /tmp/reverse_thermal.sh && chmod +x /tmp/reverse_thermal.sh'" "Failed to transfer reverse thermal script."
   # run_command "echo \"$TEXT_CONTENT\" | $SSH_COMMAND '/tmp/reverse_thermal.sh \"\$(cat -)\"'" "Failed to execute reverse thermal script."

   show_notification "Success: Text printed successfully."
   EOL
   ```

3. Replace `yourusername` and `your_server_ip` with your actual SSH username and server IP address or hostname.
4. Make the script executable:

   ```sh
   chmod +x ~/.shortcuts/remote_control.sh
   ```

### Script Explanation

- **SSH Configuration**: The script uses `ssh` with options `-o BatchMode=yes` and `-o ConnectTimeout=5` for non-interactive and timeout settings.
- **Notifications**: The `show_notification` function sends messages back to the Shortcuts app.
- **Error Handling**: The `run_command` function checks if each command executes successfully.
- **Embedded Scripts**: Both the normal and reverse thermal scripts are embedded as strings within the `remote_control.sh` script.
- **Execution Flow**:
  - The embedded script is sent to the server and saved as a temporary file in `/tmp/`.
  - The script is made executable.
  - The text content is passed to the script for printing.
  - Cleanup of temporary scripts can be added if desired.

## iOS Shortcut Setup

1. Open the **Shortcuts** app on your iPhone.
2. Create a new shortcut and give it a descriptive name (e.g., "Print to Thermal Printer").
3. **Add a Text action**:
   - Leave it blank to prompt for input when the shortcut runs.
   - Or, enter the text you wish to print.
4. **Add a Run Script Over SSH action** (note that this action is available in the Shortcuts app):
   - **Host**: Enter `localhost` (since we're running the script locally on a-Shell).
   - **User**: Leave blank.
   - **Password**: Leave blank.
   - **Script**: Enter the following command:

     ```sh
     shortcuts://run-shortcut?name=Run%20a-Shell%20Script&input={Text}
     ```

     *(Note: Since a-Shell does not support running scripts over SSH directly from Shortcuts, we use the URL scheme to run the script via a-Shell.)*

5. **Add a URL action**:
   - Set the URL to:

     ```sh
     a-shell://shortcut?text={Text}&command=~/.shortcuts/remote_control.sh%20"{Text}"
     ```

     - Replace `{Text}` with the magic variable from the previous Text action.

6. **Add an Open URLs action**:
   - Use the URL from the previous step.
   - This will open a-Shell and run the `remote_control.sh` script with the provided text.

7. **Add a Show Notification action** (optional):
   - This will display the output from the script after it completes.

### Shortcut Steps Summary

1. **Text**: Input or specify the text to print.
2. **URL**: Build the URL to run the a-Shell script:

   ```sh
   a-shell://shortcut?text={Text}&command=~/.shortcuts/remote_control.sh%20"{Text}"
   ```

3. **Open URLs**: Opens a-Shell and runs the script.
4. **Wait**: (Optional) Pause to allow the script to execute.
5. **Show Notification**: Display success or error messages.

## Testing and Verification

1. Run the shortcut from the Shortcuts app or add it to your Home Screen for quick access.
2. When prompted, enter the text you wish to print or use predefined text.
3. The shortcut will open a-Shell, execute the script, and then return to Shortcuts.
4. Observe any notifications for success or error messages.
5. Verify that the text has been printed correctly by the thermal printer connected to your Debian server.
