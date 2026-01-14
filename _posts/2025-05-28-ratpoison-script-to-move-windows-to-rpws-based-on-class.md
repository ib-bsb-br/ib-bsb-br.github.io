---
tags: [scratchpad]
info: aberto.
date: 2025-05-28
type: post
layout: post
published: true
slug: ratpoison-script-to-move-windows-to-rpws-based-on-class
title: 'ratpoison script to move windows to rpws based on class'
---
```
present the `pseudocode` that illustrates the most effective ways of scripting an solution for the following ratpoison's wanted feature:
"feature: to be able to press an keyboard key that binds to the script that cycles between each and every 'rpws' instance, ratpoison workspaces, collecting data and information about each and every resource opened as windows within the entire 'ratpoison' instance and tagging/marking each one of those opened windows in order to be able to use an keyboard shortcut to move all windows that have the same resource name to a single `rpws` dedicated and organied by that mimetype type.
```

{% codeblock markdown %}
Okay, here's a dummy dmenu command that illustrates how it would be generated and executed by the move_windows_by_resource.py script, specifically for the part where the user selects the resource type to organize.
Let's assume the following state within the move_windows_by_resource.py script:
The SNAPSHOT_FILE_PATH (/tmp/ratpoison_window_snapshot.json) has been read, and after processing, the unique_resource_names list is:
unique_resource_names = ['Thunar', 'firefox', 'xterm', 'xnedit']
Use code with caution.
Python
(Note: The script sorts this list, so it would actually be ['Thunar', 'firefox', 'xnedit', 'xterm'] if sorted alphabetically as in the script, but the order for the example doesn't strictly matter as dmenu will handle display and filtering).
The DMENU_EXECUTABLE constant is 'dmenu'.
The DMENU_COMMAND list in the script is ['dmenu', '-i', '-l', '15', '-p'].
The prompt message passed to get_selection_from_dmenu is "Organize which resource type?:".
The Python code:
# ... inside get_selection_from_dmenu ...
dmenu_input = "\n".join(options_list).encode('utf-8') # options_list is unique_resource_names
dmenu_full_command = [DMENU_EXECUTABLE, '-i', '-l', '15', '-p', prompt_message]
process = subprocess.run(dmenu_full_command, input=dmenu_input, ...)
Use code with caution.
Python
would effectively result in a command similar to this if you were to type it in a shell:
echo -e "Thunar\nfirefox\nxterm\nxnedit" | dmenu -i -l 15 -p "Organize which resource type?:"
Use code with caution.
Bash
Explanation of the components:
echo -e "Thunar\nfirefox\nxterm\nxnedit":
This part simulates the input=dmenu_input argument in subprocess.run().
The unique_resource_names list is joined by newline characters (\n) to create a multi-line string.
echo -e is used to interpret the newline characters, so each resource name appears on a new line when piped to dmenu.
|:
The pipe symbol, which sends the standard output of the echo command to the standard input of the dmenu command.
dmenu -i -l 15 -p "Organize which resource type?:":
dmenu: The dmenu executable.
-i: Makes dmenu case-insensitive.
-l 15: Instructs dmenu to display 15 lines vertically.
-p "Organize which resource type?:": Sets the prompt text displayed by dmenu.
When this command is executed (either by the script or manually in a terminal), dmenu would appear, showing "Thunar", "firefox", "xterm", and "xnedit" as selectable options, with the prompt "Organize which resource type?:" at the top. The user's selection would then be returned by dmenu on its standard output, which the Python script captures.
18.6s
{% endcodeblock %}
