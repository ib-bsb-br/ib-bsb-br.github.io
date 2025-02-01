---

tags: [software>linux]
info: aberto.
date: 2024-10-27
type: post
layout: post
published: true
slug: zutty-cheatsheet
title: 'Zutty Cheatsheet'
---
## Overview

Zutty is a fast, lightweight terminal emulator for X Window System, optimized for low-end systems. It uses OpenGL ES 3.1 for rendering, offering high throughput and low latency.

**Key Features:**

* GPU-accelerated rendering using Compute Shaders
* Accurate VT emulation (VT52, VT100, VT102, VT220, VT320, VT420, VT520, xterm)
* Supports bitmap and TrueType fonts, including CJK characters
* True color support (24-bit)
* X clipboard/primary selection/copy-paste, including rectangular selection

## Installation (Debian/Ubuntu)

1. **Dependencies:**
   ```bash
   sudo apt-get install build-essential pkg-config python3 libegl-dev libfreetype-dev libgles-dev libxmu-dev
   ```
2. **Source:**
   ```bash
   git clone https://git.hq.sig7.se/zutty.git
   cd zutty
   ```
3. **Configure:**
   ```bash
   ./waf configure
   ```
4. **Compile:**
   ```bash
   ./waf
   ```
5. **Install:**
   ```bash
   sudo ./waf install
   ```

## Usage

### Launching

```bash
zutty [options] [shell]
zutty -e [command]
```

### Options

| Option        | Description                                      | Default        |
|---------------|--------------------------------------------------|----------------|
| `-altScroll`  | Alternate scroll mode (arrow keys on alt screen) | false          |
| `-autoCopy`   | Sync primary selection to clipboard             | false          |
| `-bg <color>` | Background color                               | #000           |
| `-boldColors` | Use bright colors for bold text                 | true           |
| `-border <n>` | Border width (pixels)                           | 2              |
| `-cr <color>` | Cursor color                                   | foreground color |
| `-display`    | X display                                       | `$DISPLAY`     |
| `-dwfont`     | Double-width font                              | 18x18ja        |
| `-fg <color>` | Foreground color                               | #fff           |
| `-font`       | Font name                                      | 9x18           |
| `-fontsize`   | Font size (scaled fonts)                        | 16             |
| `-fontpath`   | Font search path                               | /usr/share/fonts |
| `-geometry`   | Terminal size (chars)                           | 80x24          |
| `-glinfo`     | Print OpenGL info                               | false          |
| `-help`       | Print usage                                      |                |
| `-listres`    | Print resource listing                           |                |
| `-login`      | Start shell as login shell                      | false          |
| `-name`       | Instance name for Xrdb and WM_CLASS             | Zutty          |
| `-rv`         | Reverse video                                   | false          |
| `-saveLines`  | Scrollback history (lines)                      | 500            |
| `-shell`      | Shell to run                                    | bash           |
| `-showWraps`  | Show wrap marks                                 | false          |
| `-title`/`-T` | Window title                                   | Zutty          |
| `-quiet`      | Silence logging                                 | false          |
| `-verbose`    | Verbose logging                                 | false          |
| `-e`          | Command to execute                             |                |


### User Actions

| Action                    | Trigger                                   |
|---------------------------|-------------------------------------------|
| Scroll half page          | Shift+PageUp/Down                         |
| Scroll 5 lines / 1 line   | Scroll wheel / (alt screen with `-altScroll`) |
| Start/Adjust selection    | Left/Right mouse button press & hold       |
| Cycle selection snapping  | Double-click left/right mouse button      |
| Toggle rectangular select | Space (while selecting)                   |
| Paste primary selection   | Middle mouse button, Shift+Insert          |
| Copy selection to clipboard | Ctrl+Shift+C                             |
| Paste clipboard           | Ctrl+Shift+V                             |


## Configuration

Zutty can be configured via command-line options, X resources, and environment variables. Command-line options override X resources, which override defaults.

### X Resources

Edit `~/.Xresources` and add entries like:

```
Zutty.title: My Terminal
Zutty.geometry: 100x30
Zutty.font: LiberationMono
Zutty.fontsize: 14
Zutty.fg: #eee
Zutty.bg: #222
```

Merge changes: `xrdb -merge ~/.Xresources`

### Environment Variables

Zutty sets/uses:

* `DISPLAY`: X display
* `SHELL`: Shell path
* `TERM`: xterm-256color
* `COLORTERM`: truecolor
* `WINDOWID`: X window ID
* `ZUTTY_VERSION`: Zutty version
* `RESOURCE_NAME`:  Instance name for Xrdb (if `-name` option not used)


## Development

### Debug Build

```bash
./waf configure --debug
./waf
```

Run: `build/src/zutty.dbg -v`

### Step Debugger

Activate with PrintScreen key (in debug build). Cycles through step counts (1, 10, 100, off). Resume with `kill -CONT <pid>` or `fg`.

### Testing

See the `test/` directory for automated tests. Run individual tests (e.g., `test/vttest.sh`) or all tests with `test/run_ci.sh`.


## Resources

* **Homepage:** [https://tomscii.sig7.se/zutty](https://tomscii.sig7.se/zutty)
* **Source:** [https://git.hq.sig7.se/zutty.git](https://git.hq.sig7.se/zutty.git)
* **User Guide:** [https://tomscii.sig7.se/zutty/doc/USAGE.html](https://tomscii.sig7.se/zutty/doc/USAGE.html)
* **Developer Guide:** [https://tomscii.sig7.se/zutty/doc/HACKING.html](https://tomscii.sig7.se/zutty/doc/HACKING.html)
* **Key Mapping Sequences:** [https://tomscii.sig7.se/zutty/doc/KEYS.html](https://tomscii.sig7.se/zutty/doc/KEYS.html)
* **Vttest Results:** [https://tomscii.sig7.se/zutty/doc/VTTEST.html](https://tomscii.sig7.se/zutty/doc/VTTEST.html)
* **FAQ:** [https://tomscii.sig7.se/zutty/wiki/FAQ.html](https://tomscii.sig7.se/zutty/wiki/FAQ.html)