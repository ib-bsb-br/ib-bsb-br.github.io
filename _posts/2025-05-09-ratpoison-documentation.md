---
tags:
- linux>software>dotfile
info: aberto.
date: 2025-05-09
type: post
layout: post
published: true
slug: ratpoison-documentation
title: ratpoison documentation
comment: https://raw.githubusercontent.com/dimatura/ratpoison/refs/heads/master/doc/ratpoison.texi
---
**NAME**
**ratpoison** — window manager without mouse dependency
**SYNOPSIS**
**ratpoison** [**−hv**] **ratpoison** [**−d**_dpy_] [**−s**_num_] [**−f**_file_] **ratpoison** [**−d**_dpy_] [**−s**_num_] [**−i**] **−c**_command_ [**−c**_command ..._]
**DESCRIPTION**
**ratpoison** is a Window Manager without fat library dependencies, fancy graphics or rat dependence.
The screen can be split into non-overlapping frames. All windows are kept maximized inside their frames.
All interaction with the window manager is done through keystrokes. **ratpoison** has a prefix map to minimize key clobbering.
The options are as follows:
**−c**, **−−command**
Send ratpoison a command. There must be a ratpoison instance running as window manager for the given display/screen for this to work. Do not forget to quote the command if it contains spaces. For example:
**ratpoison −c** "_echo hello world_"
**−d**, **−−display**_display_
Set the X display to use or send commands to.
**−f**, **−−file**_filename_
Specify an alternate configuration file. If this is not given, **ratpoison** will try _$HOME/.ratpoisonrc_ and if that does not exist _/etc/ratpoisonrc_ and execute each command when starting up.
**−h**, **−−help**
Show summary of options.
**−i**, **−−interactive**
Execute commands given with **−c** or **−−command** in interactive mode. That means it will behave exactly as if called with **C−t :** like prompting for missing arguments and things like that.
**−s**, **−−screen**_number_
Only use the specified screen.
**−v**, **−−version**
Show version of program.
**KEY BINDINGS**
To avoid conflicts with other programs, all default ratpoison key bindings start with an escape key, per default **C−t** (read Control−t). Some important default key bindings:
**C−t ?**
Show key bindings
**C−t c**
Start an X terminal
**C−t n**
Switch to next window
**C−t p**
Switch to previous window
**C−t 1** | **2** | **3** | **4** | **5** | **6** | **7** | **8** | **9**
Switch to window number 1 | 2 | ...
**C−t k**
Close the current window
**C−t K**
XKill the current application
**C−t s** | **S**
Split the current frame into two vertical | horizontal ones
**C−t Tab** | **Left** | **Up** | **Right** | **Down**
Switch to the next | left | top | right | bottom frame.
**C−t Q**
Make the current frame the only one
**C−t :**
Execute a ratpoison command
Further default key bindings can be found in parentheses after the commands in the next section.
**COMMANDS AND DEFAULT ALIASES
 abort**
(**C−t C−g**) Do nothing and that successfully. (
Useful if you pressed **C−t** in error ).
**addhook**_event command_
Add a hook: run _command_ whenever _event_ is called. Possible events are:
**deletewindow**
Run after a window is withdrawn.
**newwindow**
Run after a new window is mapped.
**key**
Run whenever a top level key is pressed (by default **C−t**).
**quit**
Run before exiting **ratpoison**.
**restart**
Run before restarting **ratpoison**.
**switchframe**
Run after a frame actually switched, but before the window in it is focused.
**switchgroup**
Run after selecting a new group.
**switchscreen**
Run when the user switches to a different screen.
**switchwin**
Run after a new window is selected. (With dedication, it may already be inactive again, if it was put into another frame)
**alias**_alias command_
Add _alias_ as new way to call _command_.
**bind**_key command_
alias for "**definekey root**_key command_"
**banish**
(**C−t b**) Banish the rat cursor to the lower right corner of the screen.
**banishrel**
Banish the rat cursor to the lower right corner of the current window. If there isn’t a window in the current frame, it banishes the rat cursor to the lower right corner of the frame.
**chdir** [_directory_]
If the optional argument is given, change the current directory of **ratpoison** to _directory_. If nothing is given, change it to the value of the environment variable "HOME".
**clrunmanaged**
Clears the unmanaged window list.
**cnext**
Like **next** but switch to the next window with another resource class than the current one. (That means the next window belonging to another type of application than the current one.)
**cprev**
Like **prev** but switch to the previous window with another resource class than the current one. (That means the previous window belonging to another type of application than the current one.)
**colon**_ratpoison−command_ (**C−t :**)
Execute _ratpoison−command_ interactively. (i.e. ask for possible missing arguments.)
**cother**
Like **other** but switch to the window of the current group that was last accessed and has another resource class but is not currently visible.
**curframe** (**C−t F**)
Show a bar marking the current frame.
**definekey**_keymap key command_
Add a new key binding in _keymap_ for _key_ to execute _command_. Default keymaps are top normally only containing **C−t**, which reads a key from root, containing all the normal commands.
Note that you have to describe ":" by "colon", "!" by "exclam" and so on. If you cannot guess a name of a key, try either **C−t**_key_ and look at the error message, or try **:describekey** root and pressing the key.
**dedicate** [**0** | **1**]
Consider the current frame dedicated/chaste (**1**) or promiscuous (**0**).
A dedicated frame will not accept new windows. When new windows are to be focused, they will be opened in a non-dedicated frame instead.
If no argument is given, toggle the current dedicateness. By default no windows are dedicated.
**delete** (**C−t k**)
Close the current window.
**delkmap**_keymap_
Deletes the keymap named _keymap_, that was generated with **newkmap**. The keymaps top (or whatever was specified by **set**_topkmap_) and root cannot be deleted.
**describekey**_keymap_
Grab the next key. Similar to **readkey**, **describekey** shows only the command in _keymap_, that would be executed by **readkey**.
**echo**_text_
Show _text_ as **ratpoison** message.
**escape**_key_
Update the default escape key to _key_.
Strictly speaking it updates the **readkey root** command in the keymap **top** to _key_, the **other** binding in root to _key_, and **meta** binding in root to _key_ without modifiers or **C−**_key_ if _key_ has no modifiers. (If **set topkmap** was called with an argument other than **top** that will be used instead of **top**.)
**exchangedown** (**C−t C−Down**)
Exchange the window in the current frame with the window in the frame below the current frame.
**exchangeleft** (**C−t C−Left**)
Exchange the window in the current frame with the window in the frame left of the current frame.
**exchangeright** (**C−t C−Right**)
Exchange the window in the current frame with the window in the frame right of the current frame.
**exchangeup** (**C−t C−Up**)
Exchange the window in the current frame with the window in the frame above the current frame.
**exec**_shell−command_ (**C−t !**)
Spawn a shell executing _shell−command_.
**execa**_shell−command_
Spawn a shell executing _shell−command_, without remembering the current frame, so that _NET_WM_PID declaring programs will be placed into the frame active when they open a window instead of the frame active when **ratpoison** gets this command.
**execf**_frame shell−command_
Spawn a shell executing _shell−command_, showing _NET_WM_PID supporting programs in the given frame instead of the frame selected when this program is run.
**fdump** [_screenno_]
Output the defining data for all frames of the current screen, or for screen number _screenno_ if this is specified.
**focus** (**C−t Tab**)
Focus the next frame.
**focuslast**
Switch to the last selected focus.
**focusleft** (**C−t Left**)
Switch to the frame to the left of the current one.
**focusdown** (**C−t Down**)
Switch to the frame beneath the current one.
**focusright** (**C−t Right**)
Switch to the frame to the right of the current one.
**focusprev**
Focus the previous frame.
**focusup** (**C−t Up**)
Switch to the frame above the current one.
**frestore**_frames_
Replace the current frames with the ones specified in _frames_ in the format as generated by **fdump**.
**fselect** [ _frameno_] (**C−t f**)
If an argument is supplied, switch to a frame given by number _frameno_.
If no argument is given, show a frame selector in each frame and wait for a key to be pressed. If the key matches an existing frame selector, this frame gets focused.
Frame selectors are by default the numbers starting with zero, but they can be changed by **set**ting _framesels_.
**gdelete** [_group_]
If the optional argument _group_ is supplied, delete _group_. Otherwise delete the current group. If the last group is deleted, a new group with name default is created. The group has to be empty, otherwise it cannot be deleted.
**getenv**_variable_
Output the value of the environment variable _variable_.
**getsel**
Paste the current X Selection into the current window.
**gmerge**_group_
Move all windows from group _group_ into the current group.
**gmove**_group_
Move the current window into group _group_.
**gnew**_group_
Create a new group with name _group_ and select it. Most window commands only see (and thus select, consider next, previous or last) windows within the group active when they are issued.
**gnewbg**_group_
Create a new group named _group_, but do not select it.
**gnext**
Select the next group. Most window commands only see windows in the effective group.
**gnumber** [_old new_]
Give the number _new_ to the group with the number _old_ or the current group.
**gother**
Select the last accessed group. Most window commands only see windows in the effective group.
**gprev**
Select the prior group. Most window commands only see windows in the effective group.
**gravity** [**nw** | **w** | **sw** | **n** | **c** | **s** | **ne** | **e** | **se**]
Change how in its frame the current window is aligned.
**grename**
Rename current group.
**groups**
Output a list of all groups with their number.
**gselect**_group_
Select the group named _group_.
**help** [_keymap_]
If the optional parameter _keymap_ is given, list all keybindings in this keymap, otherwise list all key bindings in keymap root.
**hsplit** [ _l_**/**_p_ | [ **−**]_pixels_] (**C−t S**)
Split the current frame into left frame and a right frame. If no parameter is given, split in halves. If two numbers separated by a slash (‘/’) are given, the left one is _l_ times the _p_ th part and the right one (_p_ − _l_) times the _p_ th part of the prior width. Otherwise the right half is _pixels_ wide or the left one is _pixels_ wide, depending whether there is ‘−’ in front of the number or not.
**inext**
Like **next** but switch to the next window with the same resource class as the current one. (That means the next window belonging to the same application as the current one.)
**info** (**C−t i**)
Output the current the width, height, window number and window name of the current window. (
What name means is chosen by ‘‘**set**_winname_’’. )
**iprev**
Like **prev** but switch to the previous window with the same resource class as the current one. (That means the previous window belonging to the same application as the current one.)
**iother**
Like **other** but switch to the window of the current group that was last accessed and has the same resource class but is not currently visible.
**kill** (**C−t K**)
Close the X-connection of the X-client responsible for the current window.
**lastmsg** (**C−t m**)
Reshow the last message.
**license** (**C−t V**)
Show **ratpoison**’s license.
**link**_key_ [_keymap_]
Do what _key_ is bound to in the keymap _keymap_ if supplied. Otherwise what _key_ is bound to in keymap root.
**listhook**_event_
List all commands specified with **addhook** to be executed when even _event_ occurs.
**meta** [ _key_] (**C−t t**)
Send the escape key (that which normally is **C−t**) to the current window. If a _key_ is specified, this is sent instead. Note that some applications by default ignore the synthetic key that is sent using this command as it is considered a security hole. xterm is one such application.
**msgwait** [_seconds_]
Set the duration the message window is shown. If _seconds_ is zero, wait infinitely. This command is deprecated, please set the _msgwait_ variable instead.
**newkmap**_keymap_
Generate a new keymap named _keymap_. This keymap can be used to add new key-command mappings to it with **definekey** and can be called with **readkey**.
**newwm**_new-window-manager_
Quit **ratpoison** and execute _new-window-manager_ instead.
**next** (**C−t Return** | **C−t n** | **C−t space**)
Switch to the next window in the current group.
**nextscreen** (**C−t N**)
Switch to the next screen. (If you have multiple physical ones.)
**number**_new_ [_old_]
Give the number _new_ to the window with the number _old_ or the current window.
**only** (**C−t Q**)
Remove all frames on the current screen except the current frame and maximize this one to the size of the whole screen.
**other** (**C−t C−t**)
Switch to the window of the current group that was last accessed but is not currently visible.
**prev** (**C−t p**)
Switch to the previous window in the current group.
**prevscreen** (**C−t P**)
Switch to the previous screen. (If you have multiple physical ones.)
**prompt** [_prompt_]
**ratpoison** will ask the user for input, showing _prompt_ (or a single colon, if no argument is given) and output the input the user has made. Note that this command probably does not make much sense in interactive mode.
**putsel**_x−selection_
Replace the X selection with the text _x−selection_. It can be inserted into the current window with **getsel**.
Quit **ratpoison**.
**ratinfo**
Display the x y coordinates of the rat cursor relative to the screen.
**ratrelinfo**
Display the x y coordinates of the rat cursor relative to the current window or current frame if no window is focused
**ratwarp**_x y_
Move the rat cursor to the position (_x_, _y_).
**ratrelwarp**_deltax deltay_
Move the rat cursor to (_deltax_, _deltay_), relative to the current position.
**ratclick** [_button_]
Simulate a rat click with _button_ (button 1=left button if none given).
**rathold** { **up** | **down**} [_button_]
Simulate pressing|releasing rat button _button_ (1=left button if none given).
**readkey**_keymap_
Grab the next key pressed, and execute the command associated to this key in _keymap_. To show it is waiting for a key, **ratpoison** will change the rat cursor to a square if _waitcursor_ is set. This command is perhaps best described with its usage in the default configuration: by pressing **C−t**, which is the only key in the keymap top , the command "**readkey root**" is executed. The next key then executes the command in keymap root belonging to this command.
**redisplay** (**C−t l**)
Extend the current window to the whole size of its current frame and redisplay it. (Useful to redisplay normal windows or bring transient windows to the full size of the frame as only normal windows are maximized by **ratpoison**)
**redo** (**C−t U**)
Revert the last **undo** of frame changes.
**remhook**_event command_
Remove command _command_ from the list of commands to be called when event _event_ is hit. (The command has to specified, as an event can have multiple commands attached to it.) Use "**listhook**_hook_" to get a list of all attached commands.
**remove** (**C−t R**)
Remove the current frame and extend some frames around to fill the remaining gap.
**removedown** (**C−t M−Down**)
Kill frames directly below the current frame, extending the current frame as much as possible.
**removeleft** (**C−t M−Left**)
Kill frames directly left of the current frame, extending the current frame as much as possible.
**removeup** (**C−t M−Up**)
Kill frames directly above the current frame, extending the current frame as much as possible.
**removeright** (**C−t M−Right**)
Kill frames directly right of the current frame, extending the current frame as much as possible.
**resize** [ _deltax deltay_] (**C−t r**)
If _deltax_ and _deltay_ are supplied, resize the current frame by that (i.e. move the bottom right corner by the given offsets and then move this frame and resize adjacent frames to make the frames fill the whole screen again.)
If in interactive mode no arguments are supplied, resize the current frame interactively:
**Return**
finish resizing
**C−g**, **Escape**
abort resizing
**C−n**, **Down**, **j**
grow vertically
**C−p**, **Up**, **k**
shrink vertically
**C−f**, **Right**, **l**
grow horizontally
**C−b**, **Up**, **h**
shrink horizontally
**s**
shrink to size of current window
While resizing interactively, changes are in multiples of the amount of pixels given by **set resizeunit** (by default 10).
Restart **ratpoison**.
**rudeness** [_rudeness_]
This command is deprecated, please use the _rudeness_ variable instead.
**sdump**
Output the list of all screens. The screens are separated by commas. Each screen is shown as 6 values: its number, its x-coordinate, its y-coordinate, its width, its height and if it is currently selected (1=true, 0=false).
**select** { **−** | _name_ | _number_} (**C−t ’**)
If a number is given, switch to the window with number _number_. If a name is given, switch to the window in the current group with name _name_. Blank the current frame, if **−** is given.
**set** [_variable_ [_value_]]
If no argument is given, output all **ratpoison** variables and their values.
If one argument is given, output the value of **ratpoison** variable _variable_. Otherwise set _variable_ to _value_. What values are valid depends on the variable. See the section _VARIABLES_ later in this document for details.
**setenv**_variable value_
Set the environment variable _variable_ to _value_. (
Environment variables will be passed to all programs started from **ratpoison**. )
**sfdump**
Output all frames similar to **fdump**, but not limited to one screen, but all screens at once and with the screen number after each frame.
**sfrestore**_frames_
Replace the current frames with the ones specified in _frames_ in the format as generated by **sfdump**.
**shrink**
Shrink the current frame to the size of the current window with in.
**split** [ _split_] (**C−t s**)
alias for **vsplit**
**source**_file_
Read _file_ and execute each line as **ratpoison** command.
**sselect**_screennumber_
Switch to the screen _screennumber_. (If you have multiple physical ones.)
**startup_message** {**on** | **off**}
Select whether **ratpoison** will show a startup message or not. This command is deprecated, please use the _startupmessage_ variable instead.
**swap**_dest-frame_ [ _src-frame_] (**C−t x**)
Exchange the window in _src−frame_ (or the current frame if there is no second argument) with the window _dest−frame_ (or ask interactively which frame to swap with if there is no argument).
**time** (**C−t a**)
Output current data and time.
**title**_newname_ (**C−t A**)
Overwrite the title of the current window with _newname_. All following **ratpoison** commands will only know the window under the new name.
**tmpwm**_tmpwm_
Temporarily give control over to the other window manager _tmpwm_, reclaiming control when that WM terminates.
**unalias**_alias_
Remove the alias _alias_.
**unbind**_key_
alias for
**undefinekey**_root key_
**undefinekey**_keymap key_
Remove the binding for _key_ from _keymap_.
**undo** (**C−t _**, **C−t u**)
Un−do the last change to the frameset. (Like splitting, resizing, deleting, ...)
The amount of steps that can be undone is specified by the variable _maxundos_.
**unmanage** [_name_]
Add _name_ to the list of unmanaged windows. Thus, windows of this name will not be managed but allowed to choose their position themselves.
In non−interactive mode calling it without arguments will print the list.
The list can be cleared again by calling **clrunmanaged**.
**unsetenv**_variable_
Remove variable _variable_ from the list of environment variables.
**verbexec**_cmdline_
Spawn a shell executing _cmdline_ after showing a message with the command.
**version** (**C−t v**)
Output version and compile time information.
**vsplit** [ _l_**/**_p_ | _pixels-from-top_ | **−**_pixels-from-bottom_] (**C−t s**)
Split the current frame into upper frame and a lower frame. If no parameter is given, split in halves. If two numbers separated by a slash (‘‘/’’) are given, the upper one is _l_ times the _p_ th part and the lower one (_p_ − _l_) times the _p_ th part of the prior height. Otherwise the lower one is _pixels from bottom_ wide or the upper one _pixels from top_ high, depending whether there is a ‘‘−’’ in front of the number or not.
**warp** {**on** | **off**}
Select if focusing a window moves the rat cursor to the place it had been last time this window was focused, or not. This command is deprecated, please set the _warp_ variable instead.
**windows** [ _format_] (**C−t w**)
In interactive mode, show the list of all windows in the current group for the duration specified by the variable _msgwait_. If _msgwait_ was zero, toggle between indefinitely showing and not showing.
The messages are shown in columns or rows depending on the value of _winliststyle_ in the format set by **set**_winfmt_. The following substitutions happen in format:
%a
application name (resource name)
%c
resource class
%f
frame number
%g
gravity of the window
%h
height of the window
%H
unit to resize the window vertically (height_inc)
%i
X Window ID
%p
process ID
%l
last access number
%M
string Maxsize, if it specifies a maximum size
%n
window number
%s
window status (
‘*’ is active window, ‘+’ would be chosen by **other**, ‘−’ otherwise )
 %S
screen number
%t
window name (
see **set**_winname_ ),
 %T
the string ‘‘Transient’’, if it is a transient window
%w
width of the window
%W
unit to resize the window horizontally (width_inc)
%x
xine screen number
%%
litteral ‘%’
Additionally there can be a positive decimal integer number between the percent sign and the format string to specify the length this value should be truncated to if longer. (
For example: %20t )
In non−interactive mode, output the list of windows in the current group line by line. The format string can be overwritten by the optional parameter _format_.
**VARIABLES**
**ratpoison** variables can be shown and set with **set**. The following variables are supported:
**resizeunit**_pixels_
Set the amount of pixels interactive **resize** will add/subtract in each step.
Default is 5.
**maxundos**_number_
The maximal amount of step **ratpoison** can undo with the **undo** command.
Default is 20.
**wingravity** {**nw** | **w** | **sw** | **n** | **c** | **s** | **ne** | **e** | **se**}
Set the default gravity new normal windows will get. Possible values are the same as in the **gravity** command, which changes the gravity of an existing window: cardinal points or numbers 1 to 9.
Default is nw.
**maxsizegravity** {**nw** | **w** | **sw** | **n** | **c** | **s** | **ne** | **e** | **se**}
Set the default gravity new self-maximized windows will get. Possible values are the same as in the **gravity** command, which changes the gravity of an existing window: cardinal points or numbers 1 to 9.
Default is c.
**transgravity** {**nw** | **w** | **sw** | **n** | **c** | **s** | **ne** | **e** | **se**}
Set the default gravity new transient windows will get. Possible values are the same as in the **gravity** command, which changes the gravity of an existing window: cardinal points or numbers 1 to 9.
**bargravity** {**nw** | **w** | **sw** | **n** | **c** | **s** | **ne** | **e** | **se**}
Select the location where message and prompt bars appear.
Default is ne.
**font**_font_
Make **ratpoison** use font _font_.
**padding**_left top right bottom_
Set how much space at the borders of the screen will not be used.
Default is 0 0 0 0.
**border**_pixels_
Selects how thick the frame around windows is.
Default is 1.
**barborder**_pixels_
Selects how thick the frame around **ratpoison**’s prompt or message windows is.
**inputwidth**_pixels_
Determine the width of the input window.
Default is 200.
**barinpadding** {**0** | **1**}
If there is padding, determines whether the bar appears at the edge of the screen (1) or at the edge of the window area (0).
Default is 0.
**topkmap**_kmap_
Make _kmap_ the top keymap **ratpoison** grabs directly.
The default value is top.
**waitcursor** {**0** | **1**}
Determine whether to change the rat cursor when waiting for a key (1) or not (0) See **readkey** and **describekey**.
**winfmt**_format_
Choose the default format for the the **windows** command.
Default is %n%s%t.
**winname** {**title** | **name** | **class**}
Choose what is considered the "name" of the window by **ratpoison**:
title
The title of the window.
name
The resource name of the window.
class
The resource class i.e. the name of the application.
Default is title.
**fgcolor**_color_
The foreground color of the windows **ratpoison** creates.
Default is black.
**bgcolor**_color_
The background color of the windows **ratpoison** creates.
Default is white.
**fwcolor**_color_
The border color of the focused window.
**bwcolor**_color_
The border color of unfocused windows.
**barpadding**_x y_
Set horizontal padding of **ratpoison** windows to _x_ and vertical padding to _y_.
Default is 4 0.
**winliststyle** {**row** | **column**}
Determines whether windows are shown in rows or in columns.
Default is column.
**framesels**_selectors_
Override the frame selectors **fselect** uses. The first character is the selector for the first frame, the second character is the selector for the second frame and so on.
Using this variable, one can directly access more than 10 frames.
Default is an empty string, which is equivalent to "0123456789".
**historysize**_number_
Specify maximum number of values kept in input history.
**historycompaction** {**0** | **1**}
Decide if new input lines added to history delete older equal lines from history.
Default is 1 (on).
**historyexpansion** {**0** | **1**}
Decide if history expansion using ! is available. (Can only be activated when compiled with readline’s libhistory.)
**msgwait**_seconds_
The duration the message window is shown. If _seconds_ is zero, wait infinitely.
**framemsgwait**_seconds_
The duration the ‘Current frame’ indicator is shown. If _seconds_ is zero, wait until the next interactive command. If _seconds_ is -1, don’t show any message.
**startupmessage** 0 | 1
Decide whether to show a greeting message at startup.
**warp** 0 | 1
Decide if focusing a window moves the rat cursor to the place it had been last time this window was focused, or not.
Default is 0 (off).
**rudeness**_number_
Show or set what kind of windows are allowed to jostle into the foreground.
_number_ is a bitwise OR of the following values:
1
Transient windows may raise.
2
Normal windows may raise.
4
New transient windows end up in the foreground.
8
New normal windows end up in the foreground.
Default is all allowed i.e. 15.
**FILES**
 ~/.ratpoisonrc
Configuration file read at startup time, if present.
/etc/ratpoisonrc
Fallback configuration file, if _~/.ratpoisonrc_ is not found.
**EXIT STATUS**
The **ratpoison** utility exits 0 on success, and>0 if an error occurs.
**AUTHORS**
Upstream author is Shawn Betts 〈 _sabetts AT gmail DOT com_〉 .
See the _/usr/share/doc/ratpoison/AUTHORS_ file for other contributors.
This manual page was written by Bernhard R. Link 〈 _brlink AT debian DOT org_〉 . The conversion to the [mdoc(7)](http://man.m.sourcentral.org/ubuntu2504/7+mdoc) language (**http://mdocml.bsd.lv**) was done by Jeremie Courreges-Anglas 〈 _jca AT wxcvbn DOT org_〉 .
**BUGS**
Please report any bug you find to the ratpoison mailing-list, 〈 _ratpoison-devel AT nongnu DOT org_〉 .
BSD September 29, 2019 BSD
{% raw %}
{% codeblock %}
\input texinfo   @c -*-texinfo-*-
@c %**start of header
@setfilename ratpoison.info
@include version.texi
@settitle Ratpoison @value{VERSION} manual
@c %**end of header
@dircategory X11
@direntry
* ratpoison: (ratpoison).       Say good-bye to the rodent
@end direntry
@copying
Copyright @copyright{} 2000, 2001, 2002, 2003, 2004, 2005, 2006 Shawn Betts
@quotation
The ratpoison user manual is free documentation; permission is granted to
copy, distribute and/or modify this document under the terms of either:
a) the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option)
any later version, or
b) the GNU Free Documentation License, version 1.2 or any later
version published by the Free Software Foundation; with no
Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
The ratpoison manual is distributed in the hope that it will be 
useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License or GNU Free Documentation License for more
details.
A copy of the FDL is included in the section entitled
@ref{GNU Free Documentation License}.
You should have received a copy of the GNU General Public License
along with this software; see the file COPYING. If not, write to
the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston,
MA 02110-1301, USA.
If you choose to allow use of your version of this content only under the
terms of one of the licenses, indicate your decision by deleting the notice
of the other license. If you do not delete any of those, a recipient may use
your version of this file unter the terms of either the GNU FDL or the GNU GPL.
@end quotation
@end copying
@titlepage
@title The ratpoison user manual
@author Shawn Betts
@page
@vskip 0pt plus 1filll
@insertcopying
@end titlepage
@ifnottex
@node Top
@top Ratpoison
This document explains how to use ratpoison @value{VERSION}.
@end ifnottex
@contents
@menu
* About::                       What Is Ratpoison?
* Contacting::                  How Do I Contact The Ratpoison Developers?
* Concepts::                    Window Manipulation Concepts
* General Use::                 How Does This Thing Work??
* Windows::                     Navigating The Windows
* Groups::                      Grouping Windows Together
* Frames::                      Dividing The Screen
* Multiple Screens::            What To Do With All Your Computer Junk
* Keystrokes::                  Key Commands And Functionality
* Hooks::                       Attaching Scripts To Ratpoison Events
* The Status Bar::              Ratpoison's Input/Output Area
* Using Other Window Managers:: Return To Evil
* Other Commands::              Miscellaneous Commands
* Input::                       Typing Text Into Ratpoison
* Command Line Arguments::      ratpoison Command-Line Actions
* Startup file::                They Threatened Me...With Violence!
* GNU Free Documentation License::
* Command Index::               Index
@detailmenu
 --- The Detailed Node Listing ---
Windows
* Manipulating Windows::        
* Window Classes::              
* Unmanaged Windows::           
* Rudeness::                    
Frames
* Splitting Frames::            
* Resizing Frames::             
* Frame Navigation Commands::   
* Saving and Restoring Frame Sets::  
* Frame Numbering::             
* Dedicated Frames::            
Keystrokes
* Key Maps::                    
* Default Key Bindings::        
@end detailmenu
@end menu
@node About, Contacting, Top, Top
@chapter About
ratpoison is a simple Window Manager with no fat library dependencies,
no fancy graphics, no window decorations, and no rodent dependence. It
is largely modeled after GNU Screen which has done wonders in the
virtual terminal market.
All interaction with the window manager is done through
keystrokes. ratpoison has a prefix map to minimize the key clobbering
that cripples Emacs and other quality pieces of software.
ratpoison was written by Shawn Betts (@email{sabetts@@gmail.com}).
@node Contacting
@chapter Contacting
ratpoison is hosted on @url{http://savannah.nongnu.org}. To see the latest
developments in ratpoison go to
@url{http://savannah.nongnu.org/projects/ratpoison} or visit the
ratpoison webpage at @url{http://www.nongnu.org/ratpoison}.
There is also a ratpoison mailing list:
@email{ratpoison-devel@@nongnu.org}. For details on subscribing
and for the list archives go to the ratpoison Savannah project.
There is a @url{irc://irc.freenode.net/#ratpoison, #ratpoison} IRC
channel on the @url{http://freenode/, Freenode} network.
@node Concepts
@chapter Concepts
ratpoison uses the concept of @dfn{panes} to place and size
windows. Instead of allowing windows to have arbitary shapes at
arbitary locations on the screen, the display is divided into panes,
the same way a physical window might contain several pieces of glass
seperated by wood. In ratpoison, the panes are called @dfn{frames},
and windows are placed in them, maximised. ratpoison starts with one
frame, which can be split into an arbitary number of smaller
ones. Each frame can be split in half either horizontally or
vertically. You can move among them, making different ones the
current. For more information, see @ref{Splitting Frames}.
Each frame has at most one window associated with it, which is visible
in that frame. If you select a window that is associated with a frame,
the focus will move to its associated frame, rather than moving the
window to the current frame. If you select a window that is not
associated with a frame, that window will be opened in the current
frame and resized to fit that frame.
If the window associated with a frame does not fill the frame
completely, the various gravity commands control how it is placed.
If no window was open in that frame before the current window was
opened, the X root will be visible behind it.
Transient windows (dialog boxes, splash screens, and the like) are
handled specially. In order to understand the contents of a transient
window, the previously focused window is often required. Take a search
window, it is useful to be able to see the document you are searching
as well as the search window. For this reason transient windows appear
overtop (according to their gravity) of the previously focused window.
Every window belongs in a group. A group is simply that: a group of
windows. By default there is only one group (the @dfn{default group})
that all windows exist in. You can create new groups. When a program
creates a window it will be added to the current group. Groups are
generally used to organize windows into different classes such as work
and wasting-time-at-work.
@node General Use
@chapter General Use
When ratpoison starts you should see an empty X server. To open an x
terminal hit @kbd{C-t c}. You can now run shell commands as you would on
any terminal. Notice the terminal maximized full screen. @kbd{C-t !}
will run a single shell command and saves you the effort of opening a
terminal.
Once you have a couple X programs running, you'll want to navigate
between windows. To see what windows are being managed hit @kbd{C-t
w}. Each window has a number. You can jump to a window by hitting
@kbd{C-t} followed by the window's number. This assumes the window's
number is one digit. You can also switch to a window by typing in part
of its name. To do this hit @kbd{C-t '}.
ratpoison allows you to cycle through the windows with @kbd{C-t n}
and @kbd{C-t p}.
And that concludes a brief introduction on how to use ratpoison. Notice
how we didn't have to drag a single window, or click a single maximize
button? Beautiful wasn't it? Felt fast? Cool? It's modern computing at
its best.
@node Windows
@chapter Windows
Windows are what ratpoison manages.
@node Manipulating Windows
@section Manipulating Windows
The following are commands used to manipulate windows.
@deffn Command select @var{n}
This jumps you to window @var{n} where @var{n} is the window number as
shown in the Program Bar. You can do the same trick with
@kbd{C-@var{n}} too. To select no window, blanking the current
frame, type @samp{select -}.
@end deffn
@deffn Command select @var{window-name}
Go to a window by name. A shortcut is @kbd{C-t '}.
@deffn Command windows @var{fmt}
This displays the Program Bar which displays the windows you currently
have running. The number before each window name is used to jump to
that window. You can do this by typing @kbd{C-t @var{n}} where @var{n}
is the number of the window. Note that only windows with numbers from
0 to 9 can be referenced using this keystroke.  To reach windows with
numbers greater than 9, use @kbd{C-t '} and type the number at the
prompt.
After 5 seconds the Program Bar disappears.
This command is bound to @kbd{C-t w} by default.
When invoked from the command-line like this,
@example
$ ratpoison -c windows
@end example
Instead of a message bar, you will get a list of the windows printed
to stdout. This allows you to write more advanced scripts than simple
keyboard macros. This is where @var{fmt} comes into play. If
@command{windows} is given an argument it treats it as the format string as
described in @command{set winfmt}.
@deffn Command title @var{title}
Rename the currently active window. This name will remain for the
duration of the window's life, unless you change it again. By default,
the @kbd{C-t A} keystroke is bound to this command.
@deffn Command other
This toggles between the current window and the last window. By
default, this is bound to @kbd{C-t C-t}.
@deffn Command prev
This jumps you to the previous window in the window list. By default,
this is bound to @kbd{C-t p}.
@deffn Command next
This jumps you to the next window in the window list. This one is
bound to three keystrokes, namely @kbd{C-t n}, @kbd{C-t space},
and @kbd{C-t enter}.
@deffn Command kill
This destroys the current window. Normally you should only need to
use @command{delete}, but just in case you need to rip the heart out of a
misbehaving window this command should do the trick. Also available as
@kbd{C-t K}.
@deffn Command info @var{fmt}
Display information about the current window. At optional @var{fmt}
argument can be passed to override the default format. @command{info}
accepts the same format options as @command{windows}.
@deffn Command gravity @var{g}
Change the gravity of the current window. A normal window will default
to the top-left corner of the screen, but it can also be placed at the
bottom-right corner of the screen. Valid values for @var{g} are the 8
directions @samp{northwest}, @samp{north}, @samp{northeast},
@samp{east}, @samp{southeast}, @samp{south}, @samp{southwest} and
@samp{west}, clockwise from the top left corner. @samp{center} will
center the window in the frame. @var{g} and can be abbreviated to the
standard compass 1 and 2 letter abbreviations (i.e. @samp{nw},
@samp{s}, etc).
When called with no arguments, the current setting is
returned.
@deffn Command delete
This deletes the current window. You can access it with the @kbd{C-t k}
keystroke.
@deffn Command {set infofmt} @var{fmt}
Set the default window format for the @command{info} command. See
@command{set winfmt} for accepted format characters.
@deffn Command {set warp} @var{n}
Set rat warping. By default this variable is set (@code{1}) and
ratpoison saves the position of the rat when leaving a window and when
the user returns to the window the rat's position is restored. If you
find this counter-intuitive, set this variable to @code{0}.
When called with no arguments, the current setting is returned.
@deffn Command {set winname} @var{name}
There are three resources ratpoison can get a window's name from: the
WMNAME hint, the res_name from the WMCLASS hint, or the res_class from
the WMCLASS hint. @var{name} can be @samp{title} which is what most
window managers put in the title bar, @samp{name} which is the
res_name, or @samp{class} which is the res_class.
@deffn Command {set wingravity} @var{g}
Set the default gravity for normal windows. See the
@command{gravity} command.
@deffn Command {set winliststyle} @var{setting}
The window list can be displayed in a row or a column. @var{setting}
can be @samp{row} or @samp{column}.
@deffn Command {set winfmt} @var{fmt}
Set the default window format for the @command{windows} command. By
default it is @samp{%n%s%t}. The following is a list of valid format
characters:
@table @samp
@item %a
Application Name
@item %c
Resource Class
@item %f
The frame number the window is displayed in or a space if it is not in
a frame.
@item %g
The window's gravity setting
@item %h
The window's height
@item %H
The window's height increment hint.
@item %i
X11 Window ID
@item %l
A unique number based on when the window was last accessed. The higher
the number, the more recently it was accessed.
@item %n
The window number
@item %p
Process ID ('?' if _NET_WM_PID isn't set)
@item %s
Window status (current window, last window, etc)
@item %S
The window's screen
@item %t
Window Name
@item %T
Whether the window is a transient or not.
@item %M
Whether the window is a maxsize window or not.
@item %w
The window's width
@item %W
The window's width increment hint
@item %x
the window's xrandr screen
@end table
Additionally there can be a number between the percent sign and the format
character, denoting a maximum length this value is to truncate to, e.g. @samp{%n%s%20t}.
@deffn Command number @var{n} @var{target}
Set a window's number to @var{n}. If another window occupies the
requested number already, then the windows' numbers are swapped.
The second argument, @var{target}, is optional. It should be the
number of the window whose number will be changed. If @var{target} is
omitted ratpoison defaults to the current window.
@deffn Command {set transgravity} @var{g}
Set the default alignment for transient windows. See the
@deffn Command {set maxsizegravity} @var{g}
Set the default alignment for windows with maxsize hints. See the
@deffn Command {set border} @var{n}
Set the border width for all windows.
@deffn Command {set onlyborder} @var{n}
Allows hiding of borders when only one frame is on the current
screen. The argument @var{n} can be @code{1} (default) which shows
borders or @code{0} which hides them for single frames.
@node Window Classes
@section Window Classes
Window classes are a way of grouping windows together. Windows that
are part of the same program generally have the same class. Ratpoison
takes advantage of this to help you navigate between windows of the
same class. This is useful if you only want to cycle through Emacs
frames or XTerms.
@deffn Command inext
Go to the next window in the window list that is in the same class as
the current window.
@deffn Command iprev
Go to the previous window in the window list that is in the same class
as the current window.
@deffn Command iother
Go to the last accessed window that is in the same class as the
current window.
@deffn Command cnext
Go to the next window in the window list that is in a different class
from the current window.
@deffn Command cprev
Go to the previous window in the window list that is in a different
class from the current window.
@deffn Command cother
Go to the last accessed window that is in a different class from the
@node Unmanaged Windows
@section Unmanaged Windows
ratpoison can intentionally not manage windows. ratpoison keeps a list
of strings and if any new window's name matches a string in the list,
then it will not be picked up and managed by ratpoison.
The following are commands to manipulate this list
@deffn Command clrunmanaged
Clear the unmanaged window list.
@deffn Command unmanage @var{text}
Add @var{text} to the unmanaged window list. Any window whose name
matches any of the strings in the unmanaged window list will not be
handled in any way by ratpoison. This only applies to new windows (not
windows already managed by ratpoison).
When called with no arguments, the list is returned.
@node Rudeness
@section Rudeness
Some programs will attempt to steal the focus without the users
permission. Not only is this a sign of a lame programmers attempt to fix
a window manager problem in the wrong place, it's just plain rude. By
default ratpoison will honour these rudeness requests, but it doesn't
have to. Use the rudeness variable to deal with such programs.
@deffn Command {set rudeness} @var{n}
The rudeness variable lets you decide what windows pop-up
automatically and when. This is often useful for those deep hack
sessions when you absolutely can't be disturbed.
There are two kinds of windows: normal windows (like an xterm) and
transient windows (generally pop-up dialog boxes). When a client
program wants to display a new window it makes a requests to
ratpoison. ratpoison then decides whether to grant the request and
display the window or ignore it. A client program can also request
that one of its windows be raised. You can customize ratpoison to
either honour these requests (the default operation) or ignore them.
@var{n} is a number from 0 to 15. Each of the four bits determine
which requests ratpoison grants.
@table @asis
@item Bit 0
Tells ratpoison to grant raise requests on transient windows
@item Bit 1
Tells ratpoison to grant raise requests on normal windows
@item Bit 2
Tells ratpoison to grant display requests on new transient windows
@item Bit 3
Tells ratpoison to grant display requests on new normal windows
For example, if you wanted only wanted to grant transient windows
raise requests and display requests you would type @samp{set rudeness
5}.
If a request is not granted ratpoison will tell you about the
request with a message like @samp{Raise request from window 1
(emacs)}.
@node Groups
@chapter Groups
ratpoison provides functionality to group windows together. This
coupled with saving and restoring frames configurations is what most
people would call @dfn{virtual desktops} or @dfn{workspaces}.
While ratpoison doesn't explicitly provide support for such things, it
does allow you to write scripts to this end. Such a script exists in
@file{contrib/} called @file{rpws}. Consult that file for details on
setting up workspaces inside ratpoison.
Groups are more general purpose than workspaces. windows from one
group can be visible along with windows from another group. If you
switch to a different group nothing changes except the list of windows
you can cycle through. ratpoison allows the user to move a window from
one group to another, merge two groups, create new groups, and delete
existing ones.
The following is a list of of commands used for manipulating groups.
@deffn Command gnew @var{name}
Create a new group with the name @var{name}. @var{name} is
optional. The new group becomes the current group.
@deffn Command gnewbg @var{name}
This is the same as @command{gnew} except that the current group does
not change.
@deffn Command groups
Display a list of groups with a similar format to @command{windows}.
@deffn Command gmove @var{group}
Move the current window to @var{group}.
@deffn Command gnext
Go to the next group in the list.
@deffn Command gother
Go to the last accessed group.
@deffn Command gprev
Go to the previous group in the list.
@deffn Command grename
@deffn Command gnumber @var{GROUP} @var{target}
Set a group's number to @var{GROUP}. If another group occupies the
requested number already, then the groups' numbers are swapped.
number of the group whose number will be changed. If @var{target} is
omitted ratpoison defaults to the current group.
@deffn Command gselect @var{group}
Select a particular group by name or number. If @var{group} is not
provided, ratpoison will interactively prompt for the group.
@deffn Command gmerge @var{group}
Merge @var{group} with the current group. All windows in @var{group}
will be moved to the current group. @var{group} is not deleted.
@deffn Command gdelete @var{group}
Delete a group. @var{group} is optional. If it is not specified
ratpoison will attempt to delete the current group. Only empty groups
can be deleted. To empty a group see @command{gmerge}.
@node Frames
@chapter Frames
Sometimes you may want to see two or more windows at the same
time. ratpoison allows you to split the display into frames (see
@ref{Concepts}). Each frame can then contain 1 window.
@node Splitting Frames
@section Splitting Frames
To split the
current frame horizontally use @kbd{C-t s}. To split the current frame
vertically use @kbd{C-t S}. If you have enough windows, you'll notice
that the new frame will find a window for itself. You can now use the
normal navigation commands to switch windows in the frame. Note,
however, that if you switch by name or number to a window that is
already in another frame, you'll switch to that frame.
Before too long, you'll probably want to switch to another frame. Use
@kbd{C-t tab} to cycle through the frames. If you want to remove a
frame use @kbd{C-t R}. ratpoison automatically adjusts the size of the
other frames to take up the free space. Unfortunately ratpoison may
not always fill it in the way you might like it to.
Finally, when you've had enough of the splitting and you just want
good ol' full screen ratpoison press @kbd{C-t Q} to remove all splits
and leave you with the current window full screen.
@deffn Command remove
Kill the current frame. This is a no-op if there is only one frame.
@deffn Command only
Kill all frames but the current one.
@deffn Command split @var{n}
@deffnx Command vsplit @var{n}
Split the current frame vertically in two. The last accessed window
not occupying a frame will be the second window.
@var{n} is either a fraction of the form @code{x/y} or a number. If it
is a fraction then the current frame is resized to that fraction of
its original size and the new frame takes up the remaining space. For
instance, @code{split 1/4} will split the current frame to a quarter
of its original size and the new frame will then be 3/4 of the size of
the original frame.
If it is a pixel, the original frame is resized to that many
pixels. If @var{n} has a minus sign before it, then the new frame will
shrink by that many pixels.
@deffn Command hsplit @var{n}
Split the current frame horizontally in two. The last accessed window
@node Resizing Frames
@section Resizing Frames
ratpoison provides a command, @command{resize}, that resizes the
current frame. It is bound to the key @kbd{C-t r} by
default. @command{resize} can be used non-interactively by providing
two arguments: the number of pixels to grow horizontally and the
number to grow vertically. For example, if you wanted to grow the
current window by 10 pixels horizontally and shrink it vertically by
50 you could enter the command:
resize 10 -50
When resizing interactively, the following keys are used:
@table @kbd
@item C-p
Grow the frame vertically.
@item C-n
Shrink the frame vertically.
@item C-f
Grow the frame horizontally.
@item C-b
Shrink the frame horizontally.
@item return
Accept the new frame size.
@item C-g
Abort and restore the frame to its original size.
The increment size used to resize the frame interactively is
customized with the command @command{set resizeunit}.
@deffn Command {set resizeunit} @var{pixels}
Set the number of pixels a frame will grow or shrink by when being
dynamically resized.
@deffn Command resize @var{horizontal} @var{vertical}
Resize the current frame by @var{horizontal} pixels horizontally, and
@var{vertical} pixels vertically. If no arguments are given and the
command is called interactively, ratpoison will let the user
dynamically resize the frame using @kbd{C-p} to shrink vertically,
@kbd{C-n} to grow vertically, @kbd{C-b} to shrink horizontally,
@kbd{C-f} to grow horizontally, and @kbd{s} to shrink the frame to the
size of the window (See the @command{shrink} command). When you have
resized the frame to your liking, press @kbd{Return} to finish.
@deffn Command shrink
If a window has resize increment hints, such as xterms, the window may
not be able to take up the whole frame. In this case, use this command
to suck the frame up to the to window, reclaiming any wasted space.
@node Frame Navigation Commands
@section Frame Navigation Commands
Here are the commands for Navigating frames.
@deffn Command fselect @var{n}
Select a frame by number. If an argument is passed to it then attempt
to select the frame whose number is @var{n}. If not, ratpoison will
print a number at the top left corner of each frame and wait for the
user to type the number they wish to select. Currently there is no way
to select a frame whose number is greater than 9 unless the number is
passed as an argument.
@deffn Command curframe
Indicate which frame is the current frame.
@deffn Command focus
cycle through ratpoison's frames.
@deffn Command focusprev
cycle through ratpoison's frames backwards.
@deffn Command focusdown
Move to the frame below the current frame.
@deffn Command focuslast
Switch to the last focused frame.
@deffn Command focusleft
Move to the frame left of the current frame.
@deffn Command focusright
Move to the frame right of the current frame.
@deffn Command focusup
Move to the frame above the current frame.
@node Saving and Restoring Frame Sets
@section Saving and Restoring Frame Sets
ratpoison provides two commands, @command{fdump} and
@command{frestore}, that allow the user to save and restore frame
configurations. Let's say, for example, you have split your desktop
into several frames with some windows in these frames and now you want
to quickly bring Emacs forward and browse some code (full-screen of
course) then return to your funky frame configuration. You could use
@command{fdump} to dump the frames, hit @kbd{C-t Q} to remove all
frames, and then select your emacs window. When you've finished with
emacs you could use @command{frestore} to restore the windows and
frames.
If a frame contained a window when you dumped the frame layout but
that window is not present when you restore the layout, the frame
holding that window will be blank.
Calling @command{fdump} and @command{frestore} and copying and pasting
the layout by hand each time is a bit cumbersome. There are some
simple bindings in @file{doc/sample.ratpoisonrc} that allow you to
save and restore frame layouts with the press of a key.
@deffn Command fdump @var{screen-num}
Dump the current frame layout as text.
Without an argument the current screen's frames are dumped. With an
argument the @var{screen-num}th screen is dumped. @xref{Multiple Screens}.
@deffn Command frestore @var{frames}
Restore the frame layout based on the list of frames
@var{frames}. @var{frames} should be the text that was printed after
calling @code{fdump}.
@deffn Command undo
Undo the last change of frame layout. This is especially helpful
after a @command{only} command. One can step at most @dfn{maxundos}
steps back in frame layout history.
@deffn Command redo
redo the last change that was undone.
@node Frame Numbering
@section Frame Numbering
Frames are normally numbered starting from 0. But this can be changed
with @command{set framesels} to, for instance, include letters as well.
set framesels abcdefghijklmnopqrstuvwxyz
The above code will bind letters to frames instead of numbers.
@deffn Command set framesels @var{order}
Tell ratpoison what alphanumeric character to give each frame and in
what order.
@node Dedicated Frames
@section Dedicated Frames
A dedicated frame is a frame that will not allow new windows to appear
in it. Only the user may switch windows in this frame.
@deffn Command dedicate @var{arg}
Set the current frame as dedicated (@var{arg} = 1) or not (@var{arg} = 0).
If @var{arg} is not supplied, toggle the dedicated state of the
current frame.
@node Multiple Screens
@chapter Multiple Screens
When you've finally accumulated enough computer junk, you'll find
yourself attaching a second screen to your computer. ratpoison has
functionality to help you get around your new and improved desktop
space.
To switch to another screen use the commands @command{nextscreen} and
@command{prevscreen}. Or, @command{sselect} to jump to a specified
screen. ratpoison will tell you which frame has focus by drawing the
current frame indicator in it.
Many commands operate only on the current screen. This becomes
apparent when you have 2 screens each with 1 frame. In each frame you
have an xterm. If you try to switch to the other xterm with the
command @command{other}, for instance, you'll get a message ``No other
window.'' ratpoison means there's no other window to switch to in the
current screen. If you want to switch to the other xterm you can
switch to it by name (use @command{select} or @kbd{C-t '}), by number,
or you can use @command{nextscreen}, @command{prevscreen}, and
@command{sselect}.  The commands @command{focusright},
@command{focusleft}, @command{focusup}, and @command{focusdown} also
allow you to navigate across screens.
@deffn Command nextscreen
This jumps you to the next X11 screen. @command{nextscreen} is
used for dual-head displays and multiple screen setups.
@deffn Command prevscreen
This jumps you to the previous X11 screen. @command{prevscreen} is
@deffn Command sselect @var{n}
This jumps you to the @var{n}th X11 screen. Screen numbers start at 0.
@deffn Command sdump
Like fdump, but dump information about each screen instead of each frame.
@deffn Command sfdump
Dump all the screen number and the frames on all screens.
@deffn Command sfrestore
restore a frame configuration created using @command{sfdump}.
@node Keystrokes
@chapter Keystrokes
Interactive control of ratpoison is done entirely through
keystrokes. This chapter explains how keystrokes are stored and
manipulated.
ratpoison uses the Emacs style key notation. A combination of
modifiers and one non-modifier key combine to invoke an action. The
syntax is one or more modifiers seperated with dashes followed by a
dash and the non-modifier key name. For instance, holding down
control, shift, and super then pressing the spacebar would be
described as:
S-C-s-space
The following is a list of modifiers ratpoison accepts:
@item S
Shift modifier
@item C
Control modifier
@item M
Meta modifier
@item A
Alt modifier
@item H
Hyper modifier
@item s
Super modifier
ratpoison uses the X11 keysym names for keys. Alphanumeric key names
are exactly what you see on your keyboard. Punctuation and other keys
have longer names which vary from X server to X server. To find the
name of a key, see the @command{describekey} command. Or to find the
name of a key not yet bound to an action, type @kbd{C-t} and then the
key. ratpoison will tell you it isn't bound and give you the name of
the key.
@node Key Maps
@section Key Maps
All keystrokes exist inside a keymap. When you press the prefix key you
are accessing the @samp{root} keymap. By default all commands reside in
the @samp{root} key map and are accessed by pressing @kbd{C-t}.
There is also a top level key map, @samp{top}. Any keystroke in this key
map can be accessed simply by pressing the key. This is where the prefix
key resides.
The following example adds a @kbd{C-x b} key binding to switch windows,
much like @kbd{C-x b} in Emacs. See the functions below for full
descriptions.
# Create the key map
newkmap ctrl-x
# Bind b to 'select' on our new key map
definekey ctrl-x b select
# Attach our keymap to the top level key map via C-x.
definekey top C-x readkey ctrl-x
The following functions control creating, editing, and deleting key maps.
@deffn Command newkmap @var{kmap}
Create a new keymap named @var{kmap}.
@deffn Command delkmap @var{kmap}
Delete the keymap, @var{kmap}.
@deffn Command bind @var{Key} @var{command}
Bind a key to a ratpoison command on the @samp{root} keymap. This
command takes two arguments: the key to bind and the command to
run. For example, to bind @kbd{C-t R} to restart ratpoison:
bind R restart
@deffn Command unbind @var{key}
Unbind a keystroke on the @samp{root} keymap.
@deffn Command definekey @var{kmap} @var{key} @var{command}
@command{definekey} works exactly like @command{bind} except that it
can bind keys on any key map (not just @samp{root}).
@deffn Command undefinekey @var{kmap} @var{key}
Like @command{unbind} except that you pass it a key map in @var{kmap}.
@deffn Command readkey @var{kmap}
Read a key from the keyboard and execute the command associated with
it in the keymap, @var{kmap}.
@deffn Command link @var{key}
Call the command that @var{key} is bound to. For instance
@command{link C-t} would call the command @command{other} and switch
to the last window.
@deffn Command describekey @var{keymap}
An interactive way to find the command bound to a given key on the
specified keymap. This command will wait for the user to type a
key. When the user does, the command will display the command bound to
this key.
@deffn Command {set topkmap} @var{kmap}
Set the top level keymap to @var{kmap}. You might use this to swap
between several common keymappings or to implement modes.
@node Default Key Bindings
@section Default Key Bindings
The default keystrokes are listed in this chapter. Not all commands
are accessible by default by keys.
@item C-t C-t
Switch to the last window.
@item C-t t
Sometimes you need to send a C-t to the current window. This keystroke
does just that.
@item C-t 0-9
Switch to the numbered window.
@item C-t -
Select no window, essentially hiding all windows in the current frame.
@item C-t A
@item C-t C-A
Rename the current window. The window's new name will prevail for the
rest of its lifetime.
@item C-t K
@item C-t C-K
Send a DestroyClient event to the current window. This will terminate
the application without question.
@item C-t n
@item C-t C-n
@item C-t Return
@item C-t C-Return
@item C-t Space
@item C-t C-Space
Go to next window.
@item C-t p
@item C-t C-p
Go to previous window.
@item C-t '
@item C-t C-'
Go to a window by name.  You will usually only need to type the first
few characters of the window name.
@item C-t a
@item C-t C-a
Display the current time of day.
@item C-t c
@item C-t C-c
Open a new X terminal.
@item C-t :
This allows you to execute a single ratpoison command.
@item C-t !
Run a shell command.
@item C-t C-!
Run a shell command through an X terminal.
@item C-t i
@item C-t C-i
Display information about the current window.
@item C-t k
@item C-t C-k
@item C-t l
@item C-t C-l
Redisplay the current window. Sometimes windows don't respond correctly
to the initial maximize event and need some coaxing. This is a fancy way
of saying there are still bugs in ratpoison. @kbd{C-t l} will force the
current window to maximize.
@item C-t m
@item C-t C-m
Display the last message.
@item C-t v
@item C-t C-v
Display the version of ratpoison.
@item C-t V
@item C-t C-V
Display ratpoison's license.
@item C-t w
@item C-t C-w
Display the list of managed windows. The current window is highlighted.
@item C-t s
@item C-t C-s
Split the current window horizontally in two. The last accessed window
@item C-t S
@item C-t C-S
Split the current window vertically in two. The last accessed window not
occupying a frame will be the second window.
@item C-t tab
Cycle through ratpoison's frames.
@item C-t M-tab
@item C-t Q
@item C-t R
@item C-t r
@item C-t C-r
Resize the current frame.
@item C-t b
@item C-t C-b
Banish the mouse to the lower right corner of the screen.
@item C-t ?
Display a help screen.
@item C-t f
@item C-t C-f
select a frame by number.
@item C-t F
@item C-t Down
@item C-t Left
@item C-t Right
@item C-t Up
@item C-t C-Down
Exchange the window in the current frame with the window in the frame below it.
@item C-t C-Left
Exchange the window in the current frame with the window in the frame to the left of it.
@item C-t C-Right
Exchange the window in the current frame with the window in the frame to the rigth of it.
@item C-t C-Up
Exchange the window in the current frame with the window in the frame above it.
@item C-t x
@item C-t C-x
Choose a frame and exchange the window in the current frame with the
window in the chosen frame.
@node Hooks
@chapter Hooks
One of the goals of ratpoison is to allow users to create exciting
customization to fit their specific needs. Hooks allow a user to latch
scripts onto certain events.
Each hook contains a list of commands to be executed when the
appropriate event occurs in ratpoison. For example, if you want to warp
the rat to corner of the screen every time you press a top level bound
key, you could add this to you .ratpoisonrc file:
addhook key banish
That should keep the rat out of your way.
@deffn Command addhook @var{hook} @var{command}
Add a @var{command} to @var{hook}. When the hook is run, @var{command}
will be executed.
The following hooks are available:
@item key
Run when a top level key is pressed (by default the only top level key
is the prefix key).
@item switchwin
Run when the user switches to a different window in the current frame.
@item switchframe
Run when the user switches to another frame. This is also run when the
user switches to a different screen, since a frame switch also occurs.
@item switchgroup
Run when the user switches to a different group.
@item switchscreen
@item deletewindow
Run when a window is deleted.
@item newwindow
@item titlechanged
Run when the current window's title changes.
@item quit
Run when ratpoison exits.
@item restart
Run when ratpoison restarts.
@deffn Command remhook @var{hook} @var{command}
Remove @var{command} from the hook. See @command{addhook} for a list
of available hooks.
@deffn Command listhook @var{hook}
List the commands that will be run when @var{hook} is fired.
@node The Status Bar
@chapter The Status Bar
ratpoison presents status and output through the status bar. By default
it is located in the top right corner of the screen.
This chapter presents commands for manipulating the status bar.
Since it is the only visible evidence that ratpoison is running (as
opposed to the invisible evidence including the lack of title bars and
your favorite desktop background) there are also copious visual
customizations available for those rainy days.
@deffn Command lastmsg
@deffn Command echo @var{text}
Display @var{text} as a message.
@deffn Command {set msgwait} @var{n}
Set the bar's timeout in seconds.
@deffn Command {set inputwidth} @var{n}
Set the width of the input window.
@deffn Command {set font} @var{font}
Set the font. @var{font} is a font string like @samp{9x15bold}.
@deffn Command {set framefmt} @var{fmt}
Set the text that appears when the @command{curframe} command is
called. @var{fmt} is a format string that accepts the same format
characters as @command{set winfmt}.
@deffn Command {set fgcolor} @var{color}
Set the foreground color for all text ratpoison displays. @var{color}
is any valid X11 color.
@deffn Command {set bgcolor} @var{color}
Set the background color for all text ratpoison displays. @var{color}
@deffn Command {set fwcolor} @var{color}
Set the border color for the focused window.
@deffn Command {set bwcolor} @var{color}
Set the border color for unfocused windows.
@deffn Command {set framemsgwait} @var{n}
Set the duration the @samp{Current frame} indicator is shown.  If seconds
is zero, wait until the next interactive command.  If seconds is -1,
don't show any message.
@deffn Command {set barpadding} @var{x} @var{y}
Set the horizontal and vertical padding inside the bar.
@deffn Command {set bargravity} @var{g}
Set the default alignment for the message bar. See the @command{gravity} command.
@deffn Command {set barborder} @var{n}
Set the border width for the bar window.
@deffn Command {set barinpadding} @var{n}
Set whether the bar window appears at the edge of the screen when there is
padding -- that is, within the "padding" area -- or whether it appears at the
edge of the window area.  "1" represents the former, "0" the latter.  See the
@command{set padding} and @command{set bargravity} commands.
@node Using Other Window Managers
@chapter Using Other Window Managers
There are times when a program has been so badly written that it is
virtually impossible to use under ratpoison. Some authors have tailored
their programs to certain window management paradigms so aggressively
that very little can be done. Ratpoison has two commands to help you
through these difficult times: @command{tmpwm} and @command{newwm}.
These commands should be used sparingly. They were created to allow
users to understand how a poorly designed program is intended to
function so they can build a replacement or patch an existing
alternative's missing functionality.
According to independant studies, @command{tmpwm} has been used almost
exclusively to verify its correct operation -- like a vintage sports
car: always kept in prime condition and never used.
@command{tmpwm} and @command{newwm} are provided for boasting and
completeness.
@deffn Command tmpwm @var{WM}
Gives control over to another window manager and regains control once
it has terminated. @var{WM} is the path to the new window
manager. This command is useful when you want to temporarily take a
look at another window manager, or program under a different window
manager, but you want to come back to ratpoison when you've finished
your investigation.
@deffn Command newwm @var{window-manager}
This is a bad-bad command. It kills ratpoison and revives that
ugly rodent! Yuck! Avoid!
@node Other Commands
@chapter Other Commands
The following is a list of commands that don't fit in any existing
chapters.
@deffn Command abort
This is a pretty useless command. By default, it is bound to @kbd{C-t
g} and its purpose is to abort the current chain of keystrokes (just
like @kbd{C-g} in @samp{Emacs}).
@deffn Command alias @var{name} @var{command}
Allows you to name a ratpoison command something else. For
instance, if you frequently open emacs you may want to make an alias
called @samp{emacs} that loads emacs. You would do it like this:
alias emacs exec emacs
An alias is treated exactly like a colon command in that you can call
it from the colon prompt, bind it to a key, and call it
non-interactively with @command{ratpoison -c}.
@deffn Command banish
@deffn Command banishrel
Banish the rat cursor to the lower right corner of the curren window.
If there isn't a window in the current frame, it banishes the rat cursor
to the lower right corner of the frame.
@deffn Command chdir
Change the current directory for ratpoison.
@deffn Command colon @var{command}
Run a ratpoison command.
@deffn Command {set padding} @var{left} @var{top} @var{right} @var{bottom}
Set the padding around the edge of the screen.
@deffn Command {set waitcursor} @var{n}
Set whether the rat cursor should change into a square when waiting
for a key. A non-zero number means change the cursor. Zero means don't
change the cursor.
@deffn Command {set historysize} @var{n}
Set how many lines of history should be recorded.
@deffn Command {set historcompaction} @var{bool}
Set whether to remove multiple equal lines from history,
even if not adjacent.
@deffn Command {set historexpansion} @var{bool}
Set whether to expand ! using readline's libhistory in input.
@deffn Command escape @var{key}
Set the prefix to @var{key}. For example @samp{escape C-b} sets the
prefix key to @key{C-b}.
@deffn Command exchangedown
Exchange the current frame with the one below it.
@deffn Command exchangeleft
Exchange the current frame with the one to the left of it.
@deffn Command exchangeright
Exchange the current frame with the one to the right of it.
@deffn Command exchangeup
Exchange the current frame with the one above it.
@deffn Command exec @var{command}
Execute a shell command. By default, @kbd{C-t !} does this.
@deffn Command execa @var{command}
Execute a shell command but don't record which frame it was executed
from. The client's windows will pop up in whatever frame is current.
@deffn Command execf @var{frame} @var{command}
Execute a shell command and choose which frame the client's first
window will open in. The client must be netwm compliant for this to
work.
@deffn Command getenv @var{env}
Display the value of the environment variable @var{env}.
@deffn Command getsel
Return the contents of the X11 selection.
@deffn Command help
Display a help screen that lists all bound keystrokes.
@deffn Command license
Display ratpoison's license. By default, this is bound to @kbd{C-t V}.
@deffn Command meta @var{key}
@var{key} is an optional argument. When @var{key} is omitted, send a
@kbd{C-t} to the current window. Otherwise, send the key described by
@var{key} to the current window. Note that some applications by
default ignore the synthetic key that is sent using this command as it
is considered a security hole. xterm is one such application.
For example, if your @samp{Emacs} window is focused,
meta M-x
Would cause emacs to prompt for an extended command.
@deffn Command prompt @var{prompt}
This command is only useful when called
non-interactively. @command{prompt} prompts the user for input using
@var{prompt} and returns the input.
@deffn Command putsel @var{text}
Make text the X11 selection.
@deffn Command quit
Quit ratpoison.
@deffn Command ratinfo
@deffn Command ratrelinfo
Display the x y coordinates of the rat cursor relative to the current window or current frame if no window is focused.
@deffn Command ratrelwarp @var{x} @var{y}
Warp the rat to the specified location relative to the current rat
position.
@deffn Command ratwarp @var{x} @var{y}
Warp the rat to the specified absolute location.
@deffn Command ratclick @var{button}
click the rat. @var{button} is either 1, 2, or 3. @var{button}
defaults to button 1.
@deffn Command rathold @var{state} @var{button}
click the rat button down if @var{state} is @samp{down} or release the button if @var{state} is @samp{up}.
@deffn Command redisplay
Extend the current window to the whole size of its current frame and
redisplay it. This can be used to:
@itemize @bullet
@item redisplay normal windows or bring transient windows to the full size of the frame as only normal windows are maximized by ratpoison.
@item fix xterms that didn't catch ratpoison's initial maximize event.
@end itemize
@deffn Command restart
Restart ratpoison.
@deffn Command set @var{var} @var{value}
Set the value of a ratpoison variable.
Here is a list of variables that can be set:
@item framesels
@item winliststyle
@item barpadding
@item bgcolor
@item fgcolor
@item winname
@item winfmt
@item waitcursor
@item inputwidth
@item barborder
@item border
@item padding
@item font
@item bargravity
@item maxsizegravity
@item transgravity
@item wingravity
@item maxundos
@item resizeunit
@item historysize
@item historycompaction
@item historyexpansion
@item msgwait
@item framemsgwait
@item startupmessage
@item warp
@deffn Command setenv @var{env} @var{value}
Set the environment variable @var{env} to @var{value}
@deffn Command source @var{file}
Read a text file containing ratpoison commands.
@deffn Command swap @var{destination-frame} @var{source-frame}
When called interactively prompt for a frame and swap its window with
the window in the current frame. An optional second argument allows
swapping of windows between arbitrary frames.
@deffn Command time
Show current time in the status bar.
@deffn Command unalias @var{name}
Remove @var{name} from the list of defined aliases.
@deffn Command unsetenv @var{env}
Clear the value of the environment variable, @var{env}.
@deffn Command verbexec @var{command}
Verbosely exec the shell command @var{command}. Raptoison displays a
message saying command was executed.
@deffn Command version
Print ratpoison version.  By default, this is bound to @kbd{C-t v}.
@node Input
@chapter Input
At various times ratpoison will prompt you for input. Ratpoison sports
a fully featured line editor. The following table lists the keystrokes
and actions:
@table @key
@itemx escape
abort the command requesting input.
@itemx right arrow
move forward a character.
@itemx left arrow
move backward a character.
@item M-f
move forward a word.
@item M-b
move backward a word.
@item C-a
@itemx home
move to the beginning of the line.
@item C-e
@itemx end
move to the end of the line.
@item C-d
@itemx delete
delete the character at point.
@item M-d
delete the word at point.
@item backspace
delete the character before the point.
@item M-backspace
delete the word before the point.
@item C-k
delete from the point to the end of the line.
@item C-u
delete from the point to the beginning of the line.
@item C-y
Yank the text from the X11 cut buffer.
@itemx up arrow
Cycle backwards through the history (This command does nothing if
ratpoison was configured with the @code{--disable-history} configure
option).
@itemx down arrow
Cycle forwards through the history (This command does nothing if
submit the line of text.
@item tab
complete the text up to the point or if there are several possible
completions, cycle through them. This only works in certain
contexts. Tab completion will complete a shell command, a window name,
a group name, and colon commands in their appropriate context
(i.e. when being asked for a window name).
@item S-iso-lefttab
This is shift + tab by the way. This does the same as tab, but cycles
backwards through the completions.
All input is stored in the same history list. By default ratpoison has
a history length of 100 entries. This history is saved to the file
@file{~/.ratpoison_history} and is loaded when you start
ratpoison. This means your history sticks between sessions. This
assumes history has not been disabled on compilation.
@node Command Line Arguments
@chapter Command Line Arguments
ratpoison supports command line arguments to request various actions
when invoking ratpoison.
@table @code
@item -h, --help
Display this help screen
@item -v, --version
Display the version
@item -d, --display
Specify the X display to connect to.
@item -s, --screen
Specify the screen to use. By default ratpoison runs on all
screens. You can tell it to use just one with this option.
@item -c, --command
Send ratpoison a colon-command. This allows you to control ratpoison
from the command-line. with the @option{-c} option you can script
ratpoison using any programming language that can spawn a
process. Some commands behave differently when invoked this
way. Currently the only commands that behaves differently are the
@code{windows} and @code{set} commands. For @code{windows}, instead of
displaying the window list in a message window, it is printed to
stdout. The output can then be captured and used in the ratpoison
script. For instance, this could be used to check whether a program is
running and if it is switch to its window otherwise launch it.
It should also be noted that multiple @option{-c} options can be used.
to facilitate writing scripts, the @env{RATPOISON} environment
variable is set to the full path of the ratpoison binary.
$ ratpoison -c split -c split
Here ratpoison would split the current frame twice.
@item -i, --interactive
Force ratpoison to execute commands in interactive mode. This is used
in conjunction with the @option{-c} option.
@item -f, --file
Specify an alternate configuration file. @xref{Startup file}.
@node Startup file
@chapter Startup file
Now you've probably read the web page, and you've no doubt dug up some
old file I forgot about. You're probably wondering, ``say, didn't he say
there was no configuration file to customize?''. Okay, ya got me. But let's
be honest here: ratpoison is so pure and fast-acting, customization is
barely worth the extra effort. In the off chance that you need to make
ratpoison your own, we now support it.
On startup ratpoison looks for @file{~/.ratpoisonrc} and runs it through
the command parser. If @file{~/.ratpoisonrc} does not exist, ratpoison
tries @file{/etc/ratpoisonrc}. This means any command you can bind a key
to or run at the command prompt (@kbd{C-t :}) you can execute in this rc
file.
You can also use the @option{-f} option to specify another startup
file, allowing you to switch between different configurations
(@pxref{Command Line Arguments}).
@deffn Command {set startupmessage} @var{n}
Turn on or off the startup_message. This is most useful in your
.ratpoisonrc file. @var{n} can be @code{1} (default) or @code{0}.
@node GNU Free Documentation License
@chapter GNU Free Documentation License
@include fdl.texi
@node Command Index
@unnumbered Command Index
@printindex fn
@bye
{% endcodeblock %}
{% endraw %}
