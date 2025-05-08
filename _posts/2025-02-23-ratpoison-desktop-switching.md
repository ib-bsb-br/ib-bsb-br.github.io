---
tags: [linux]
info: aberto.
date: 2025-02-23
type: post
layout: post
published: true
slug: ratpoison-desktop-switching
title: Setting Up Desktop Switching in Ratpoison
comment: '`https://ozi-blog.ru/nastroyka-pereklyucheniya-rabochih-stolov-v-ratpoison/`'
---


Ratpoison is a minimalist window manager for X11. It is designed to be efficient and fast, providing a simple, keyboard-driven interface with no unnecessary decorations or features. It doesn't rely on external libraries and allows for efficient window management. Although the lack of a traditional desktop environment might feel unusual at first, users find that it increases productivity by minimizing the need for window resizing, opening, or hiding.

For an even more streamlined experience, Ratpoison includes the `rpws` script. This script enables multiple desktops, making it easier to organize and switch between tasks. Using multiple desktops in Ratpoison can be particularly useful when working with multiple documents or tasks simultaneously.

## Setting Up `rpws` for Desktop Switching

To configure desktop switching with `rpws`, you will need to add the following line to your `~/.ratpoisonrc` file:

```sh
exec rpws init N -k
```

Where `N` is the number of desktops you wish to create (at least 2). The `-k` flag is optional and is only necessary if you want to use predefined keybindings for switching desktops and managing windows.

When `rpws` is initialized, it will create `N` desktops, and by default, it assigns the following keybindings:

- `Alt+F(N)` - Switch to desktop `N` (e.g., `Alt+F1` switches to the first desktop).
- `Ctrl+Alt+Right` - Go to the next desktop.
- `Ctrl+Alt+Left` - Go to the previous desktop.
- `Ctrl+Alt+Windows+F(N)` - Move the current window to desktop `N`.
- `Ctrl+Alt+>` - Move the window to the next desktop.
- `Ctrl+Alt+<` - Move the window to the previous desktop.

However, you may find these keybindings inconvenient or difficult to use. In that case, you can customize them to suit your preferences.

## Customizing `rpws` Hotkeys

To customize the keybindings, add the following lines to your `~/.ratpoisonrc` file:

```sh
# Initialize 6 desktops
exec rpws init 6

# Switch desktops with the Windows+digit combination
definekey top s-1 exec rpws 1
definekey top s-2 exec rpws 2
definekey top s-3 exec rpws 3
definekey top s-4 exec rpws 4
definekey top s-5 exec rpws 5
definekey top s-6 exec rpws 6

# Move windows to desktops using Windows+F(N)
definekey top s-F1 exec rpws move1
definekey top s-F2 exec rpws move2
definekey top s-F3 exec rpws move3
definekey top s-F4 exec rpws move4
definekey top s-F5 exec rpws move5
definekey top s-F6 exec rpws move6

# Move between desktops with Windows+Right/Left
definekey top s-Right exec rpws next
definekey top s-Left exec rpws prev

# Move window to next/previous desktop using Windows+Up/Down
definekey top s-Up exec rpws movenext
definekey top s-Down exec rpws moveprev
```

### Keybinding Legend:
- `C` stands for **Ctrl**
- `S` stands for the **Windows** key
- `M` stands for **Alt**

For example, `C-S-M-q` represents pressing `Ctrl + Windows + Alt + q` in sequence.
