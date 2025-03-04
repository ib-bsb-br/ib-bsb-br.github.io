---

tags: [software>linux]
info: aberto.
date: 2024-10-27
type: post
layout: post
published: true
slug: zutty-linux-terminal
title: Zutty Linux terminal
comment: 'https://git.hq.sig7.se/zutty.git'
---

>Homepage: `https://tomscii.sig7.se/zutty/`

Zutty - Zero-cost Unicode Teletype
==================================

**A high-end terminal for low-end systems**


Zutty is a terminal emulator for the X Window System, functionally similar to several other X terminal emulators such as `xterm`, `rxvt` and countless others. It is also similar to other, much more modern, GPU-accelerated terminal emulators such as Alacritty and Kitty. What really sets Zutty apart is its radically simple, yet extremely efficient rendering implementation, coupled with a sufficiently complete feature set to make it useful for a wide range of users. Zutty offers high throughput with low latency, and strives to conform to relevant (published or de-facto) standards.

Zutty is written in straightforward C++ and only relies on OpenGL ES 3.1 for rendering, making it trivially portable to windowing systems other than X and operating systems other than Linux. Zutty provides a clean implementation written from scratch, resulting in a minimal, maintainable, modern codebase unencumbered by historical baggage.

Zutty is released under the GNU General Public License (GPL) v3 or (at your option) any later version. Please refer to the file LICENSE for the full text of the license.

Documentation
-------------

Core documentation (bundled with the Zutty sources):

*   [README](https://tomscii.sig7.se/zutty/README.html): general overview (this document)
*   [User guide](https://tomscii.sig7.se/zutty/doc/USAGE.html): guide and reference for all users
*   [Developer guide](https://tomscii.sig7.se/zutty/doc/HACKING.html): internals, debugging, testing, contributing
*   [Key mapping sequences](https://tomscii.sig7.se/zutty/doc/KEYS.html): reference on keyboard-induced sequences
*   [Vttest results](https://tomscii.sig7.se/zutty/doc/VTTEST.html): documents the level of conformance against Vttest

More about Zutty:

*   [Screenshots](https://tomscii.sig7.se/zutty/wiki/Screenshots.html): Zutty in action
*   [Frequently Asked Questions](https://tomscii.sig7.se/zutty/wiki/FAQ.html): What you never thought you'd need to know about Zutty
*   [How Zutty works](https://tomscii.sig7.se/2020/11/How-Zutty-works): Rendering a terminal with an OpenGL Compute Shader
*   [A totally biased comparison of Zutty](https://tomscii.sig7.se/2020/12/A-totally-biased-comparison-of-Zutty) (to some better-known X terminal emulators)
*   [Measured: Typing latency of Zutty](https://tomscii.sig7.se/2021/01/Typing-latency-of-Zutty) (compared to others)

Current status
--------------

Zutty started out as a concept to prove the feasibility of using a GLES Compute Shader to render a fixed-width text grid entirely in graphics hardware. From its modest beginnings as a technological proof of concept, Zutty has evolved considerably and is now perfectly capable of serving as the main terminal emulator for heavy users of the command line. In particular, this author employs Zutty to run a workload of `tmux`, `emacs` (`-nw`), `tig`, `mutt`, `htop`, and a bunch of other applications making extensive use of the terminal (including its mouse support), with some Zutty instances running for months at a time, on a very resource-constrained SBC (ab)used as a desktop. The correctness, performance, and stability of Zutty is excellent, as one would rightly expect from something as fundamental as a terminal emulator.

There is, however, a list of ancillary features that Zutty does not presently implement. Completing the ones in scope is more or less a matter of straightforward implementation work within the already existing architecture of Zutty, and time will be spent on these in proportion to popular user demand.

Notable features
----------------

### Radically simple, uniquely performant rendering technology

The main idea behind Zutty is the implementation of "raw" character video memory via OpenGL ES 3.1. This video memory is just an array of cells backing all character grid locations, with each cell containing Unicode character codes plus color and other visual attributes. This memory area, allocated on the GPU, is mapped to make it directly writable by the application. This results in a conceptually similar interface as to how one could write to the screen by directly poking at physical video memory starting at 0xB8000 on the IBM PC. Zutty employs an OpenGL Compute Shader running on the GPU to read this video memory and render output pixels. The full name of Zutty (dubbed the _Zero-cost Unicode Teletype_) stands for the remarkable fact that its image rendering is zero-cost from the host CPU perspective.

Zutty requires OpenGL ES 3.1 because this is precisely the lowest version with support for the Compute Shader, the enabling technology behind Zutty. We have chosen OpenGL ES over OpenGL to widen the range of supported hardware platforms, primarily towards small, low-cost Single Board Computers. These boards are commonly built around an ARM SoC with a graphics core supporting OpenGL ES, but not "desktop" OpenGL. Zutty is the first GPU-accelerated terminal for such low-cost platforms.

### Correct (and fairly complete) VT emulation

Zutty substantially emulates the "commonly used" subsets of the protocols of VT52, VT100, VT102, VT220, VT320, VT420 and VT520 terminals (originally manufactured by DEC) as well as some more modern additions defined by the de-facto standard `xterm` implementation.

We take great care to ensure that Zutty passes the subset of VTTEST screens that we care about (this amounts to the overwhelming majority of tests concerned with actual screen rendering, and is subject to further extension). We have an automated regression testing setup to run VTTEST in Zutty and verify that the output is a pixel-perfect match of the pre-approved video output. You can thus expect the terminal output to be _correct_ – be it driven by tmux, emacs (with org-mode, helm, magit, etc.) or whatever else. Zutty handles corner cases (escape sequences) which, sadly enough, several popular terminal emulators do not correctly support.

Zutty implements xterm's de-facto standard method (`modifyOtherKeys`) to expose non-trivial modifier key combinations to programs such as Emacs and Vim. Zutty also boasts mouse support (again, modeled after xterm's capabilities) to make the user experience of many terminal applications more interactive.

In a perfect world, these would not be highlighted as such prominent features, but unfortunately, our focus on correctness is rather the exception than the norm among widely used terminal emulators (including more modern ones).

### Font handling

Zutty supports both fixed size (bitmap) and scaled (TTF, OTF) fonts. Up to four variants of a font are supported (Regular, Bold, Italic / Oblique, plus BoldItalic) with automatic, sensible fallbacks in case any of them (apart from Regular) is missing. Zutty tries to locate the font files itself under a configured font search path, and loads them on its own, without any support from the windowing system.

Zutty is able to display CJK symbols (ideographs) in double-width cells. This requires a suitable double-width font. This font can be fixed or scaled independent from the main font (for example, you may use a scaled font for CJK along with a fixed main font).

### True color support

Each grid cell in the virtual video memory emulated via OpenGL has three bytes reserved for the foreground color as well as the background color. As such, Zutty naturally supports true color (24 bits / 16 million colors) on each cell's foreground and background, completely independent of each other and all other cells.

### Traditional X-clipboard / primary selection / copy-paste support

Zutty supports the traditional method of "copy-paste" based on the X Selection API, and is accessible via the same GUI mechanisms that long-time `xterm` users are familiar with.

Zutty faithfully replicates what `xterm` has provided for a very long time: starting selections with the left button, adjusting them with the right button, and cycling between snap-to-char/word/line with double clicks. This naturally yields the ability to select whole words with a double-click, and complete lines with a triple-click. Compared with `xterm`, one notable difference is a built-in, simpler rule for word boundaries (as opposed to user-adjustable definitions of character classes).

It is possible to adjust the selection while navigating scrollback. Thus, the complete content of the screen buffer (page history plus on-screen lines), or any part of it, can be copied as a single selection. No need to switch back and forth between source and destination programs when copying large amounts of terminal output!

Selecting a region with the mouse will set the primary selection, and pressing Control+Shift+C will copy that to the clipboard. This mechanism is useful because it allows holding two separate pieces of selection data at once. Zutty can also be configured to automatically copy the primary to the clipboard each time a selection is done.

Paste the primary selection into the terminal via middle click or Shift+Insert, like in `xterm`. Paste the clipboard via Control+Shift+V.

Just as with `xterm`, terminal programs might enable one of the supported "mouse protocols" to provide mouse interaction on their user interfaces; in such cases, press and hold the Shift key while performing the clicks and drags of the selection that you want to perform (both while copying and pasting). Holding Shift will cut through to the Zutty mouse handler instead of sending those mouse events to the terminal program via the mouse protocol. So, regardless of the program running in the terminal, you can always access the built-in copy-paste support in Zutty; but you can also use whatever mouse support your program has.

In addition, Zutty adds a unique feature for real power users of the terminal: rectangular selection. This is extremely useful if working with a vertically split terminal (think `emacs` or `tmux`). Simply toggle between "regular" and "rectangular" selection mode with the Space key while a selection adjustment is in progress (left or right mouse button is held down). For your convenience, this setting persists over individual selections made, throughout the lifetime of a running Zutty terminal.

### Small, clean codebase

The radical simplicity of our rendering technology allows for a straightforward virtual terminal implementation that happens to be extremely performant despite the lack of any fancy optimizations on the source code level. This also allows the codebase of Zutty to be fairly small and understandable. Therefore, Zutty lends itself towards educational use and as a vehicle for hacking on terminals. If you've always wanted to learn how a terminal emulator works from the inside out, consider studying the Zutty codebase (and associated developer documentation)!

Omissions and limitations
-------------------------

There are things that Zutty does not implement compared to other, more established X terminal emulators (`xterm` being the gold standard of completeness here). The below list gives an overview of what might be considered missing. Some of them are clearly out of scope for Zutty, but some will possibly be implemented in the future.

*   Zutty is opinionated about the primacy of UTF-8, which means that non-UTF-8 interaction is generally not supported, not even via bridges such as `luit`. DEC builtin character sets (such as the DEC Special Graphics, DEC Technical Characters, etc.) and the escape sequences to enable them are well implemented though, so users of any modern Linux environment should never run into trouble.
*   Zutty is Unicode-based, but it is a terminal emulator, not an all-purpose Unicode program. Therefore it does not aim to implement the whole breadth and depth of glyph and language support that Unicode defines. Currently not supported:
    *   Characters with a code point above `U+FFFF` (that is, outside the Basic Multilingual Plane);
    *   Bidirectional (right-to-left) text;
    *   Composing characters (things that can only be represented as a base glyph plus one or more composing glyphs superimposed, even in Unicode NFC representation). Do not confuse this with using the _compose key_ to input accented or special characters missing from your keyboard; that works fine!
    *   Possibly more esoteric features.
*   DEC VT100 double-height / double-width (DECDHL, DECDWL) lines are not supported. Do not confuse this with double-width cells for wide characters (e.g. CJK ideographs), which are supported.
*   Rectangular area operations (introduced by the DEC VT400 series) are not supported. However, this set of features is optional and the terminal's self-identification response clearly states the absence of this support, so conforming client applications should not run into any trouble. No fundamental technical reasons here other than the lack of pressing need.
*   The mouse protocol implementation aims to be complete with the exception of highlight tracking mode that is not implemented. Mouse highlight tracking is a mode that requires cooperation from the client application; it is not clear if any software actively used in 2020 needs this feature.
*   Blinking in general (blinking text driven by the SGR attribute 5, and blinking cursor mode turned on/off by DEC-private set/reset escape sequences) are not (yet) supported. Certain more esoteric text attributes, such as the "concealed" bit, are also not implemented. This is purely due to lack of bandwidth, and will most likely be added in the future.
