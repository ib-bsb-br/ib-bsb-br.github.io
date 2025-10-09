---
title: "/etc/apt/sources.list + deb pkgs"
date: 2024-04-14
tags: [linux>dotfile]
info: aberto.
type: post
layout: post
---

{% codeblock %}
deb https://mirrors.ustc.edu.cn/debian bullseye main contrib non-free
deb https://mirrors.ustc.edu.cn/debian bullseye-updates main contrib non-free non-free-firmware
deb https://mirrors.ustc.edu.cn/debian bullseye-proposed-updates main contrib non-free non-free-firmware
deb https://mirrors.ustc.edu.cn/debian-security bullseye-security main contrib non-free non-free-firmware
{% endcodeblock %}

***

Applications in /opt:

- FreeTube

- Min

- NightPDF

***

| Name | Description |
|---|---|
| 7zip | 7-Zip file archiver with a high compression ratio |
| 9menu | Creates X menus from the shell |
| abook | text-based ncurses address book application |
| acpi-support-base | scripts for handling base ACPI events such as the power button |
| acpid | Advanced Configuration and Power Interface event daemon |
| adduser | add and remove users and groups |
| adwaita-icon-theme | default icon theme of GNOME |
| alsa-utils | Utilities for configuring and using ALSA |
| alsamixergui | graphical soundcard mixer for ALSA soundcard driver |
| alsaplayer-alsa | alsaplayer output module for ALSA |
| alsaplayer-common | audio player (common files) |
| alsaplayer-gtk | alsaplayer gtk interface |
| alsaplayer-jack | alsaplayer output module for JACK |
| alsaplayer-text | alsaplayer text interface |
| anacron | cron-like program that doesn't go by time |
| appmenu-gtk-module-common | Common files for GtkMenuShell D-Bus exporter |
| appmenu-gtk3-module:arm64 | GtkMenuShell D-Bus exporter (GTK+3.0) |
| appstream | Software component metadata management |
| apt | commandline package manager |
| apt-transport-https | transitional package for https support |
| apt-utils | package management related utility programs |
| atmel-firmware | Firmware for Atmel at76c50x wireless networking chips. |
| autoconf | automatic configure script builder |
| automake | Tool for generating GNU Standards-compliant Makefiles |
| autotools-dev | Update infrastructure for config.{guess,sub} files |
| bamfdaemon | Window matching library - daemon |
| base-files | Debian base system miscellaneous files |
| base-passwd | Debian base system master password and group files |
| bash | GNU Bourne Again SHell |
| bash-completion | programmable completion for the bash shell |
| bcc | 16-bit x86 C compiler |
| bin86 | 16-bit x86 assembler and loader |
| binfmt-support | Support for extra binary formats |
| binutils | GNU assembler, linker and binary utilities |
| binutils-aarch64-linux-gnu | GNU binary utilities, for aarch64-linux-gnu target |
| binutils-common:arm64 | Common files for the GNU assembler, linker and binary utilities |
| bison | YACC-compatible parser generator |
| blueman | Graphical bluetooth manager |
| bluez | Bluetooth tools and daemons |
| bluez-firmware | Firmware for Bluetooth devices |
| bluez-obexd | bluez obex daemon |
| borgbackup | deduplicating and compressing backup program |
| borgbackup-doc | deduplicating and compressing backup program (documentation) |
| bpytop | Resource monitor that shows usage and stats |
| brightness-udev | Control backlight brightness - udev rules |
| brightnessctl | Control backlight brightness |
| bsdextrautils | extra utilities from 4.4BSD-Lite |
| bsdmainutils | Transitional package for more utilities from FreeBSD |
| bsdutils | basic utilities from 4.4BSD-Lite |
| bubblewrap | utility for unprivileged chroot and namespace manipulation |
| build-essential | Informational list of build-essential packages |
| busybox | Tiny utilities for small and embedded systems |
| bzip2 | high-quality block-sorting file compressor - utilities |
| ca-certificates | Common CA certificates |
| camera-engine-rkaiq | 3A libraries match Rockchip rkisp v30(rk3588). |
| can-utils | SocketCAN userspace utilities and tools |
| catfish | File searching tool which is configurable via the command line |
| cdtool | text-based audio CD player and CD-ROM control commands |
| chafa | Image-to-text converter supporting a wide range of symbols, etc. |
| cheese | tool to take pictures and videos from your webcam |
| cheese-common | Common files for the Cheese tool to take pictures and videos |
| clang-11 | C, C++ and Objective-C compiler |
| clang-11-doc | C, C++ and Objective-C compiler - Documentation |
| clang-13 | C, C++ and Objective-C compiler |
| clang-13-doc | C, C++ and Objective-C compiler - Documentation |
| clang-9 | C, C++ and Objective-C compiler |
| clang-9-doc | C, C++ and Objective-C compiler - Documentation |
| cmake | cross-platform, open-source make system |
| cmake-data | CMake data files (modules, templates and documentation) |
| coinor-libcbc3:arm64 | Coin-or branch-and-cut mixed integer programming solver (shared libraries) |
| coinor-libcgl1 | COIN-OR Cut Generation Library |
| coinor-libclp1 | Coin-or linear programming solver (shared libraries) |
| coinor-libcoinmp1v5:arm64 | Simple C API for COIN-OR Solvers Clp and Cbc -- library |
| coinor-libcoinutils3v5 | Coin-or collection of utility classes (binaries and libraries) |
| coinor-libosi1v5:arm64 | COIN-OR Open Solver Interface |
| conky | highly configurable system monitor (transitional package) |
| conky-std | highly configurable system monitor (default version) |
| console-setup | console font and keymap setup program |
| console-setup-linux | Linux specific part of console-setup |
| containerd | open and reliable container runtime |
| coreutils | GNU core utilities |
| cpio | GNU cpio -- a program to manage archives of files |
| cpp | GNU C preprocessor (cpp) |
| cpp-10 | GNU C preprocessor |
| cpp-9 | GNU C preprocessor |
| cpufrequtils | utilities to deal with the cpufreq Linux kernel feature |
| crda | wireless Central Regulatory Domain Agent |
| cron | process scheduling daemon |
| cups-pk-helper | PolicyKit helper to configure cups with fine-grained privileges |
| curl | command line tool for transferring data with URL syntax |
| dahdi-firmware-nonfree | DAHDI non-free firmware |
| dash | POSIX-compliant shell |
| dbus | simple interprocess messaging system (daemon and utilities) |
| dbus-x11 | simple interprocess messaging system (X11 deps) |
| dconf-gsettings-backend:arm64 | simple configuration storage system - GSettings back-end |
| dconf-service | simple configuration storage system - D-Bus service |
| debconf | Debian configuration management system |
| debian-archive-keyring | GnuPG archive keys of the Debian archive |
| debian-keyring | GnuPG keys of Debian Developers and Maintainers |
| debianutils | Miscellaneous utilities specific to Debian |
| desktop-base | common files for the Debian Desktop |
| desktop-file-utils | Utilities for .desktop files |
| dialog | Displays user-friendly dialog boxes from shell scripts |
| diffstat | produces graph of changes introduced by a diff file |
| diffutils | File comparison utilities |
| dirmngr | GNU privacy guard - network certificate management service |
| distro-info-data | information about the distributions' releases (data files) |
| dmsetup | Linux Kernel Device Mapper userspace library |
| dnsmasq-base | Small caching DNS proxy and DHCP/TFTP server |
| docx2txt | Convert Microsoft OOXML files to plain text |
| dosfstools | utilities for making and checking MS-DOS FAT filesystems |
| dpkg | Debian package management system |
| dpkg-dev | Debian package development tools |
| dvb-tools | Collection of command line DVB utilities |
| dvb-tools-dbgsym | debug symbols for dvb-tools |
| e2fsprogs | ext2/ext3/ext4 file system utilities |
| eapoltest | EAPoL testing utility |
| eapoltest-dbgsym | debug symbols for eapoltest |
| eject | ejects CDs and operates CD-Changers under Linux |
| elks-libc | 16-bit x86 C library and include files |
| evtest | utility to monitor Linux input device events |
| exo-utils | Utility files for libexo |
| fakeroot | tool for simulating superuser privileges |
| fdisk | collection of partitioning utilities |
| ffmpegthumbnailer | fast and lightweight video thumbnailer |
| file | Recognize the type of data in a file using "magic" numbers |
| findutils | utilities for finding files--find, xargs |
| firmware-amd-graphics | Binary firmware for AMD/ATI graphics chips |
| firmware-ath9k-htc | firmware for AR7010 and AR9271 USB wireless adapters |
| firmware-atheros | Binary firmware for Qualcomm Atheros wireless cards |
| firmware-bnx2 | Binary firmware for Broadcom NetXtremeII |
| firmware-bnx2x | Binary firmware for Broadcom NetXtreme II 10Gb |
| firmware-brcm80211 | Binary firmware for Broadcom/Cypress 802.11 wireless cards |
| firmware-cavium | Binary firmware for Cavium Ethernet adapters |
| firmware-intel-sound | Binary firmware for Intel sound DSPs |
| firmware-intelwimax | Binary firmware for Intel WiMAX Connection |
| firmware-ipw2x00 | Binary firmware for Intel Pro Wireless 2100, 2200 and 2915 |
| firmware-ivtv | Binary firmware for iTVC15-family MPEG codecs (ivtv and pvrusb2 drivers) |
| firmware-iwlwifi | Binary firmware for Intel Wireless cards |
| firmware-libertas | Binary firmware for Marvell wireless cards |
| firmware-linux | Binary firmware for various drivers in the Linux kernel (metapackage) |
| firmware-linux-free | Binary firmware for various drivers in the Linux kernel |
| firmware-linux-nonfree | Binary firmware for various drivers in the Linux kernel (metapackage) |
| firmware-misc-nonfree | Binary firmware for various drivers in the Linux kernel |
| firmware-myricom | Binary firmware for Myri-10G Ethernet adapters |
| firmware-netronome | Binary firmware for Netronome network adapters |
| firmware-netxen | Binary firmware for QLogic Intelligent Ethernet (3000 and 3100 Series) |
| firmware-qcom-soc | Binary firmware for Qualcomm SoCs |
| firmware-qlogic | Binary firmware for QLogic HBAs |
| firmware-realtek | Binary firmware for Realtek wired/wifi/BT adapters |
| firmware-samsung | Binary firmware for Samsung MFC video codecs |
| firmware-siano | Binary firmware for Siano MDTV receivers |
| firmware-sof-signed | Intel SOF firmware - signed |
| firmware-ti-connectivity | Binary firmware for TI Connectivity wifi and BT/FM/GPS adapters |
| firmware-zd1211 | binary firmware for the zd1211rw wireless driver |
| flex | fast lexical analyzer generator |
| fontconfig | generic font configuration library - support binaries |
| fontconfig-config | generic font configuration library - configuration |
| fonts-aenigma | 465 free TrueType fonts by Brian Kent |
| fonts-arphic-ukai | "AR PL UKai" Chinese Unicode TrueType font collection Kaiti style |
| fonts-arphic-uming | "AR PL UMing" Chinese Unicode TrueType font collection Mingti style |
| fonts-dejavu | metapackage to pull in fonts-dejavu-core and fonts-dejavu-extra |
| fonts-dejavu-core | Vera font family derivate with additional characters |
| fonts-dejavu-extra | Vera font family derivate with additional characters (extra variants) |
| fonts-droid-fallback | handheld device font with extensive style and language support (fallback) |
| fonts-font-awesome | iconic font designed for use with Twitter Bootstrap |
| fonts-freefont-otf | Freefont Serif, Sans and Mono OpenType fonts |
| fonts-freefont-ttf | Freefont Serif, Sans and Mono Truetype fonts |
| fonts-glyphicons-halflings | icons made for smaller graphic |
| fonts-ipaexfont-gothic | Japanese OpenType font, IPAex Gothic Font |
| fonts-ipaexfont-mincho | Japanese OpenType font, IPAex Mincho Font |
| fonts-ipafont | Japanese OpenType font set, all IPA Fonts |
| fonts-ipafont-gothic | Japanese OpenType font set, IPA Gothic and IPA P Gothic Fonts |
| fonts-ipafont-mincho | Japanese OpenType font set, IPA Mincho and IPA P Mincho Fonts |
| fonts-ipafont-nonfree-jisx0208 | Japanese TrueType font, IPAfont (JISX0208) |
| fonts-lato | sans-serif typeface family font |
| fonts-liberation | Fonts with the same metrics as Times, Arial and Courier |
| fonts-mathjax | JavaScript display engine for LaTeX and MathML (fonts) |
| fonts-mona | Japanese TrueType font for 2ch ASCII art |
| fonts-nanum | Nanum Korean fonts |
| fonts-noto | metapackage to pull in all Noto fonts |
| fonts-noto-cjk | "No Tofu" font families with large Unicode coverage (CJK regular and bold) |
| fonts-noto-cjk-extra | "No Tofu" font families with large Unicode coverage (CJK all weight) |
| fonts-noto-color-emoji | color emoji font from Google |
| fonts-noto-core | "No Tofu" font families with large Unicode coverage (core) |
| fonts-noto-extra | "No Tofu" font families with large Unicode coverage (extra) |
| fonts-noto-mono | "No Tofu" monospaced font family with large Unicode coverage |
| fonts-noto-ui-core | "No Tofu" font families with large Unicode coverage (UI core) |
| fonts-noto-ui-extra | "No Tofu" font families with large Unicode coverage (UI extra) |
| fonts-noto-unhinted | "No Tofu" font families with large Unicode coverage (unhinted) |
| fonts-opensymbol | OpenSymbol TrueType font |
| fonts-quicksand | sans-serif font with round attributes |
| fonts-takao-gothic | Japanese TrueType font set, Takao Gothic Fonts |
| fonts-texgyre | OpenType fonts based on URW Fonts |
| fonts-umeplus-cl | Japanese TrueType font, based on Ume Gothic Classic and M+ fonts |
| fonts-urw-base35 | font set metric-compatible with the 35 PostScript Level 2 Base Fonts |
| fonts-vlgothic | Japanese TrueType font from Vine Linux |
| fonts-wqy-zenhei | "WenQuanYi Zen Hei" A Hei-Ti Style (sans-serif) Chinese font |
| freetube |  |
| fuse | Filesystem in Userspace |
| g++ | GNU C++ compiler |
| g++-10 | GNU C++ compiler |
| gcc | GNU C compiler |
| gcc-10 | GNU C compiler |
| gcc-10-base:arm64 | GCC, the GNU Compiler Collection (base package) |
| gcc-10-doc | documentation for the GNU compilers (gcc, gobjc, g++) |
| gcc-10-locales | GCC, the GNU compiler collection (native language support files) |
| gcc-9 | GNU C compiler |
| gcc-9-base:arm64 | GCC, the GNU Compiler Collection (base package) |
| gcc-9-doc | documentation for the GNU compilers (gcc, gobjc, g++) |
| gcc-9-locales | GCC, the GNU compiler collection (native language support files) |
| gcc-doc | documentation for the GNU compilers (gcc, gobjc, g++) |
| gcc-doc-base | several GNU manual pages |
| gdal-data | Geospatial Data Abstraction Library - Data files |
| gdb | GNU Debugger |
| gdebi | simple tool to view and install deb files - GNOME GUI |
| gdebi-core | simple tool to install deb files |
| gdisk | GPT fdisk text-mode partitioning tool |
| gettext | GNU Internationalization utilities |
| gettext-base | GNU Internationalization utilities for the base system |
| ghostscript | interpreter for the PostScript language and for PDF |
| ghostscript-x | interpreter for the PostScript language and for PDF - X11 support |
| gir1.2-atk-1.0:arm64 | ATK accessibility toolkit (GObject introspection) |
| gir1.2-atspi-2.0:arm64 | Assistive Technology Service Provider (GObject introspection) |
| gir1.2-ayatanaappindicator3-0.1 | Typelib files for libayatana-appindicator3-1 (GTK-3+ version) |
| gir1.2-freedesktop:arm64 | Introspection data for some FreeDesktop components |
| gir1.2-gdkpixbuf-2.0:arm64 | GDK Pixbuf library - GObject-Introspection |
| gir1.2-glib-2.0:arm64 | Introspection data for GLib, GObject, Gio and GModule |
| gir1.2-gst-plugins-bad-1.0:arm64 | GObject introspection data for the GStreamer libraries from the "bad" set |
| gir1.2-gst-plugins-base-1.0:arm64 | GObject introspection data for the GStreamer Plugins Base library |
| gir1.2-gstreamer-1.0:arm64 | GObject introspection data for the GStreamer library |
| gir1.2-gtk-2.0:arm64 | GTK graphical user interface library -- gir bindings |
| gir1.2-gtk-3.0:arm64 | GTK graphical user interface library -- gir bindings |
| gir1.2-harfbuzz-0.0:arm64 | OpenType text shaping engine (GObject introspection data) |
| gir1.2-libxfce4util-1.0:arm64 | Typelib file for libxfce4util |
| gir1.2-nm-1.0:arm64 | GObject introspection data for the libnm library |
| gir1.2-notify-0.7:arm64 | sends desktop notifications to a notification daemon (Introspection files) |
| gir1.2-packagekitglib-1.0 | GObject introspection data for the PackageKit GLib library |
| gir1.2-pango-1.0:arm64 | Layout and rendering of internationalized text - gir bindings |
| gir1.2-polkit-1.0 | GObject introspection data for PolicyKit |
| gir1.2-secret-1:arm64 | Secret store (GObject-Introspection) |
| gir1.2-vte-2.91:arm64 | GObject introspection data for the VTE library |
| gir1.2-xfconf-0 | utilities for managing settings in Xfce - introspection support |
| gir1.2-zeitgeist-2.0:arm64 | library to access Zeitgeist - GObject introspection data |
| git | fast, scalable, distributed revision control system |
| git-man | fast, scalable, distributed revision control system (manual pages) |
| glib-networking:arm64 | network-related giomodules for GLib |
| glib-networking-common | network-related giomodules for GLib - data files |
| glib-networking-services | network-related giomodules for GLib - D-Bus services |
| glmark2-data | OpenGL (ES) 2.0 benchmark suite -- data files |
| glmark2-drm | OpenGL 2.0 benchmark suite |
| glmark2-drm-dbgsym | debug symbols for glmark2-drm |
| glmark2-es2-drm | OpenGL 2.0 benchmark suite |
| glmark2-es2-drm-dbgsym | debug symbols for glmark2-es2-drm |
| glmark2-es2-wayland | OpenGL 2.0 benchmark suite |
| glmark2-es2-wayland-dbgsym | debug symbols for glmark2-es2-wayland |
| glmark2-es2-x11 | OpenGL 2.0 benchmark suite |
| glmark2-es2-x11-dbgsym | debug symbols for glmark2-es2-x11 |
| glmark2-wayland | OpenGL 2.0 benchmark suite |
| glmark2-wayland-dbgsym | debug symbols for glmark2-wayland |
| glmark2-x11 | OpenGL 2.0 benchmark suite |
| glmark2-x11-dbgsym | debug symbols for glmark2-x11 |
| gmrun | Featureful CLI-like GTK+ application launcher |
| gnome-desktop3-data | Common files for GNOME desktop apps |
| gnome-icon-theme | GNOME Desktop icon theme |
| gnome-system-tools | Cross-platform configuration utilities |
| gnome-video-effects | Collection of GStreamer effects |
| gnupg | GNU privacy guard - a free PGP replacement |
| gnupg-l10n | GNU privacy guard - localization files |
| gnupg-utils | GNU privacy guard - utility programs |
| gpg | GNU Privacy Guard -- minimalist public key operations |
| gpg-agent | GNU privacy guard - cryptographic agent |
| gpg-wks-client | GNU privacy guard - Web Key Service client |
| gpg-wks-server | GNU privacy guard - Web Key Service server |
| gpgconf | GNU privacy guard - core configuration utilities |
| gpgsm | GNU privacy guard - S/MIME version |
| gpgv | GNU privacy guard - signature verification tool |
| grep | GNU grep, egrep and fgrep |
| groff-base | GNU troff text-formatting system (base system components) |
| gsasl-common | GNU SASL platform independent files |
| gsettings-desktop-schemas | GSettings desktop-wide schemas |
| gsfonts | Fonts for the Ghostscript interpreter(s) |
| gsimplecal | lightweight GUI calendar application |
| gstreamer1.0-alsa:arm64 | GStreamer plugin for ALSA |
| gstreamer1.0-alsa-dbgsym:arm64 | debug symbols for gstreamer1.0-alsa |
| gstreamer1.0-clutter-3.0:arm64 | Clutter PLugin for GStreamer 1.0 |
| gstreamer1.0-gl:arm64 | GStreamer plugins for GL |
| gstreamer1.0-gl-dbgsym:arm64 | debug symbols for gstreamer1.0-gl |
| gstreamer1.0-gtk3:arm64 | GStreamer plugin for GTK+3 |
| gstreamer1.0-gtk3-dbgsym:arm64 | debug symbols for gstreamer1.0-gtk3 |
| gstreamer1.0-libav:arm64 | ffmpeg plugin for GStreamer |
| gstreamer1.0-libav-dbgsym:arm64 | debug symbols for gstreamer1.0-libav |
| gstreamer1.0-opencv:arm64 | GStreamer OpenCV plugins |
| gstreamer1.0-opencv-dbgsym:arm64 | debug symbols for gstreamer1.0-opencv |
| gstreamer1.0-plugins-bad:arm64 | GStreamer plugins from the "bad" set |
| gstreamer1.0-plugins-bad-apps | GStreamer helper programs from the "bad" set |
| gstreamer1.0-plugins-bad-apps-dbgsym | debug symbols for gstreamer1.0-plugins-bad-apps |
| gstreamer1.0-plugins-bad-dbgsym:arm64 | debug symbols for gstreamer1.0-plugins-bad |
| gstreamer1.0-plugins-base:arm64 | GStreamer plugins from the "base" set |
| gstreamer1.0-plugins-base-apps | GStreamer helper programs from the "base" set |
| gstreamer1.0-plugins-base-apps-dbgsym | debug symbols for gstreamer1.0-plugins-base-apps |
| gstreamer1.0-plugins-base-dbgsym:arm64 | debug symbols for gstreamer1.0-plugins-base |
| gstreamer1.0-plugins-good:arm64 | GStreamer plugins from the "good" set |
| gstreamer1.0-plugins-good-dbgsym:arm64 | debug symbols for gstreamer1.0-plugins-good |
| gstreamer1.0-plugins-ugly:arm64 | GStreamer plugins from the "ugly" set |
| gstreamer1.0-pulseaudio:arm64 | GStreamer plugin for PulseAudio (transitional package) |
| gstreamer1.0-qt5:arm64 | GStreamer plugin for Qt5 |
| gstreamer1.0-qt5-dbgsym:arm64 | debug symbols for gstreamer1.0-qt5 |
| gstreamer1.0-rockchip1 | The Gstreamer plugins for Rockchip platforms. |
| gstreamer1.0-rockchip1-dbgsym | debug symbols for gstreamer1.0-rockchip1 |
| gstreamer1.0-tools | Tools for use with GStreamer |
| gstreamer1.0-tools-dbgsym | debug symbols for gstreamer1.0-tools |
| gstreamer1.0-wpe:arm64 | GStreamer WPEWebKit plugin |
| gstreamer1.0-wpe-dbgsym:arm64 | debug symbols for gstreamer1.0-wpe |
| gstreamer1.0-x:arm64 | GStreamer plugins for X11 and Pango |
| gstreamer1.0-x-dbgsym:arm64 | debug symbols for gstreamer1.0-x |
| gtk-update-icon-cache | icon theme caching utility |
| guile-2.2-libs:arm64 | Core Guile libraries |
| gvfs:arm64 | userspace virtual filesystem - GIO module |
| gvfs-backends | userspace virtual filesystem - backends |
| gvfs-common | userspace virtual filesystem - common data files |
| gvfs-daemons | userspace virtual filesystem - servers |
| gvfs-libs:arm64 | userspace virtual filesystem - private libraries |
| gzip | GNU compression utilities |
| hardinfo | Displays system information |
| hdmi2usb-fx2-firmware | FX2 firmware for hdmi2usb board development |
| hicolor-icon-theme | default fallback theme for FreeDesktop.org icon themes |
| hostapd | access point and authentication server for Wi-Fi and Ethernet |
| hostapd-dbgsym | debug symbols for hostapd |
| hostname | utility to set/show the host name or domain name |
| i2c-tools | heterogeneous set of I2C tools for Linux |
| icu-devtools | Development utilities for International Components for Unicode |
| ifupdown | high level tools to configure network interfaces |
| imagemagick-6-common | image manipulation programs -- infrastructure |
| init-system-helpers | helper tools for all init systems |
| initramfs-tools | generic modular initramfs generator (automation) |
| initramfs-tools-core | generic modular initramfs generator (core tools) |
| initscripts | scripts for initializing and shutting down the system |
| input-utils | utilities for the input layer of the Linux kernel |
| insserv | boot sequence organizer using LSB init.d script dependency information |
| intltool-debian | Help i18n of RFC822 compliant config files |
| iotop | simple top-like I/O monitor |
| iperf | Internet Protocol bandwidth measuring tool |
| iproute2 | networking and traffic control tools |
| iptables | administration tools for packet filtering and NAT |
| iputils-ping | Tools to test the reachability of network hosts |
| ir-keytable | Alter keymaps of Remote Controller devices |
| ir-keytable-dbgsym | debug symbols for ir-keytable |
| isc-dhcp-client | DHCP client for automatically obtaining an IP address |
| iso-codes | ISO language, territory, currency, script codes and their translations |
| isync | IMAP and MailDir mailbox synchronizer |
| iw | tool for configuring Linux wireless devices |
| ixo-usb-jtag | Altera Bus Blaster emulation using Cypress FX2 chip |
| javascript-common | Base support for JavaScript library packages |
| kbd | Linux console font and keytable utilities |
| kded5 | Extensible daemon for providing session services |
| keyboard-configuration | system-wide keyboard preferences |
| kio | resource and network access abstraction |
| klibc-utils | small utilities built with klibc for early boot |
| kmod | tools for managing Linux kernel modules |
| kwayland-data | Qt library wrapper for Wayland libraries - data files |
| kwayland-integration:arm64 | kwayland runtime integration plugins |
| less | pager program similar to more |
| liba52-0.7.4:arm64 | library for decoding ATSC A/52 streams |
| libaa1:arm64 | ASCII art library |
| libabw-0.1-1:arm64 | library for reading and writing AbiWord(tm) documents |
| libacl1:arm64 | access control list - shared library |
| libaec0:arm64 | Adaptive Entropy Coding library |
| libalgorithm-diff-perl | module to find differences between files |
| libalgorithm-diff-xs-perl | module to find differences between files (XS accelerated) |
| libalgorithm-merge-perl | Perl module for three-way merge of textual data |
| libaliased-perl | Perl module to provide aliases of class names |
| libalsaplayer-dev | alsaplayer plugin library (development files) |
| libalsaplayer0:arm64 | alsaplayer plugin library |
| libao-common | Cross Platform Audio Output Library (Common files) |
| libao4:arm64 | Cross Platform Audio Output Library |
| libaom0:arm64 | AV1 Video Codec Library |
| libapparmor1:arm64 | changehat AppArmor library |
| libappmenu-gtk3-parser0:arm64 | GtkMenuShell to GMenuModel parser (GTK+3.0) |
| libappstream4:arm64 | Library to access AppStream services |
| libapt-pkg-perl | Perl interface to libapt-pkg |
| libapt-pkg6.0:arm64 | package management runtime library |
| libarchive-dev:arm64 | Multi-format archive and compression library (development files) |
| libarchive-tools | FreeBSD implementations of 'tar' and 'cpio' and other archive tools |
| libarchive-zip-perl | Perl module for manipulation of ZIP archives |
| libarchive13:arm64 | Multi-format archive and compression library (shared library) |
| libargon2-1:arm64 | memory-hard hashing function - runtime library |
| libaribb24-0:arm64 | library for ARIB STD-B24 decoding (runtime files) |
| libarmadillo10 | streamlined C++ linear algebra library |
| libarpack2:arm64 | Fortran77 subroutines to solve large scale eigenvalue problems |
| libasan5:arm64 | AddressSanitizer -- a fast memory error detector |
| libasan6:arm64 | AddressSanitizer -- a fast memory error detector |
| libasound2:arm64 | shared library for ALSA applications |
| libasound2-data | Configuration files and profiles for ALSA drivers |
| libasound2-plugins:arm64 | ALSA library additional plugins |
| libass9:arm64 | library for SSA/ASS subtitles rendering |
| libassuan0:arm64 | IPC library for the GnuPG components |
| libasyncns0:arm64 | Asynchronous name service query library |
| libatasmart4:arm64 | ATA S.M.A.R.T. reading and parsing library |
| libatk-bridge2.0-0:arm64 | AT-SPI 2 toolkit bridge - shared library |
| libatk-bridge2.0-dev:arm64 | Development files for the AT-SPI 2 toolkit bridge |
| libatk1.0-0:arm64 | ATK accessibility toolkit |
| libatk1.0-data | Common files for the ATK accessibility toolkit |
| libatk1.0-dev:arm64 | Development files for the ATK accessibility toolkit |
| libatkmm-1.6-1v5:arm64 | C++ wrappers for ATK accessibility toolkit (shared libraries) |
| libatomic1:arm64 | support library providing __atomic built-in functions |
| libatopology2:arm64 | shared library for handling ALSA topology definitions |
| libatspi2.0-0:arm64 | Assistive Technology Service Provider Interface - shared library |
| libatspi2.0-dev:arm64 | Development files for the assistive technology service provider |
| libattr1:arm64 | extended attribute handling - shared library |
| libaudit-common | Dynamic library for security auditing - common files |
| libaudit1:arm64 | Dynamic library for security auditing |
| libavahi-client3:arm64 | Avahi client library |
| libavahi-common-data:arm64 | Avahi common data files |
| libavahi-common3:arm64 | Avahi common library |
| libavahi-glib1:arm64 | Avahi GLib integration library |
| libavc1394-0:arm64 | control IEEE 1394 audio/video devices |
| libavcodec-dev:arm64 | FFmpeg library with de/encoders for audio/video codecs - development files |
| libavcodec58:arm64 | FFmpeg library with de/encoders for audio/video codecs - runtime files |
| libavfilter7:arm64 | FFmpeg library containing media filters - runtime files |
| libavformat-dev:arm64 | FFmpeg library with (de)muxers for multimedia containers - development files |
| libavformat58:arm64 | FFmpeg library with (de)muxers for multimedia containers - runtime files |
| libavresample4:arm64 | FFmpeg compatibility library for resampling - runtime files |
| libavutil-dev:arm64 | FFmpeg library with functions for simplifying programming - development files |
| libavutil56:arm64 | FFmpeg library with functions for simplifying programming - runtime files |
| libayatana-appindicator3-1 | Ayatana Application Indicators (GTK-3+ version) |
| libayatana-ido3-0.4-0:arm64 | Widgets and other objects used for Ayatana Indicators |
| libayatana-indicator3-7:arm64 | panel indicator applet - shared library (GTK-3+ variant) |
| libb-hooks-endofscope-perl | module for executing code after a scope finished compilation |
| libb-hooks-op-check-perl | Perl wrapper for OP check callbacks |
| libb2-1:arm64 | BLAKE2 family of hash functions |
| libbabeltrace1:arm64 | Babeltrace conversion libraries |
| libbamf3-2:arm64 | Window matching library - shared library |
| libbinutils:arm64 | GNU binary utilities (private shared library) |
| libblas3:arm64 | Basic Linear Algebra Reference implementations, shared library |
| libblkid-dev:arm64 | block device ID library - headers |
| libblkid1:arm64 | block device ID library |
| libblockdev-fs2:arm64 | file system plugin for libblockdev |
| libblockdev-loop2:arm64 | Loop device plugin for libblockdev |
| libblockdev-part-err2:arm64 | Partition error utility functions for libblockdev |
| libblockdev-part2:arm64 | Partitioning plugin for libblockdev |
| libblockdev-swap2:arm64 | Swap plugin for libblockdev |
| libblockdev-utils2:arm64 | Utility functions for libblockdev |
| libblockdev2:arm64 | Library for manipulating block devices |
| libbluetooth3:arm64 | Library to use the BlueZ Linux Bluetooth stack |
| libbluray2:arm64 | Blu-ray disc playback support library (shared library) |
| libboost-filesystem1.74.0:arm64 | filesystem operations (portable paths, iteration over directories, etc) in C++ |
| libboost-iostreams1.74.0:arm64 | Boost.Iostreams Library |
| libboost-locale1.74.0:arm64 | C++ facilities for localization |
| libboost-regex1.74.0:arm64 | regular expression library for C++ |
| libboost-thread1.74.0:arm64 | portable C++ multi-threading |
| libbpf0:arm64 | eBPF helper library (shared library) |
| libbrotli-dev:arm64 | library implementing brotli encoder and decoder (development files) |
| libbrotli1:arm64 | library implementing brotli encoder and decoder (shared libraries) |
| libbs2b0:arm64 | Bauer stereophonic-to-binaural DSP library |
| libbsd0:arm64 | utility functions from BSD systems - shared library |
| libbz2-1.0:arm64 | high-quality block-sorting file compressor library - runtime |
| libc++1:arm64 | LLVM C++ Standard library |
| libc++1-11:arm64 | LLVM C++ Standard library |
| libc++abi1-11:arm64 | LLVM low level support for a standard C++ library |
| libc-bin | GNU C Library: Binaries |
| libc-dev-bin | GNU C Library: Development binaries |
| libc-l10n | GNU C Library: localization files |
| libc6:arm64 | GNU C Library: Shared libraries |
| libc6-dev:arm64 | GNU C Library: Development Libraries and Header Files |
| libcaca0:arm64 | colour ASCII art library |
| libcairo-gobject2:arm64 | Cairo 2D vector graphics library (GObject library) |
| libcairo-script-interpreter2:arm64 | Cairo 2D vector graphics library (script interpreter) |
| libcairo2:arm64 | Cairo 2D vector graphics library |
| libcairo2-dev:arm64 | Development files for the Cairo 2D graphics library |
| libcairomm-1.0-1v5:arm64 | C++ wrappers for Cairo (shared libraries) |
| libcanberra-gtk3-0:arm64 | GTK+ 3.0 helper for playing widget event sounds with libcanberra |
| libcanberra0:arm64 | simple abstract interface for playing event sounds |
| libcap-ng0:arm64 | An alternate POSIX capabilities library |
| libcap2:arm64 | POSIX 1003.1e capabilities (library) |
| libcap2-bin | POSIX 1003.1e capabilities (utilities) |
| libcapture-tiny-perl | module to capture STDOUT and STDERR |
| libcbor0:arm64 | library for parsing and generating CBOR (RFC 7049) |
| libcc1-0:arm64 | GCC cc1 plugin for GDB |
| libcddb2 | library to access CDDB data - runtime files |
| libcdio-cdda2:arm64 | library to read and control digital audio CDs |
| libcdio-paranoia2:arm64 | library to read digital audio CDs with error correction |
| libcdio19:arm64 | library to read and control CD-ROM |
| libcdparanoia0:arm64 | audio extraction tool for sampling CDs (library) |
| libcdr-0.1-1:arm64 | library for reading and converting Corel DRAW files |
| libcfitsio9:arm64 | shared library for I/O with FITS format data files |
| libchafa0:arm64 | library for image-to-text converter chafa |
| libcharls2:arm64 | Implementation of the JPEG-LS standard |
| libcheese-gtk25:arm64 | tool to take pictures and videos from your webcam - widgets |
| libcheese8:arm64 | tool to take pictures and videos from your webcam - base library |
| libchromaprint1:arm64 | audio fingerprint library |
| libclang-common-11-dev | Clang library - Common development package |
| libclang-common-13-dev | Clang library - Common development package |
| libclang-common-9-dev | Clang library - Common development package |
| libclang-cpp11 | C++ interface to the Clang library |
| libclang-cpp13 | C++ interface to the Clang library |
| libclang-cpp9 | C++ interface to the Clang library |
| libclang1-11 | C interface to the Clang library |
| libclang1-13 | C interface to the Clang library |
| libclass-data-inheritable-perl | Perl module to create accessors to class data |
| libclass-method-modifiers-perl | Perl module providing method modifiers |
| libclass-xsaccessor-perl | Perl module providing fast XS accessors |
| libclone-perl | module for recursively copying Perl datatypes |
| libclucene-contribs1v5:arm64 | language specific text analyzers (runtime) |
| libclucene-core1v5:arm64 | core library for full-featured text search engine (runtime) |
| libclutter-1.0-0:arm64 | Open GL based interactive canvas library |
| libclutter-gst-3.0-0:arm64 | Open GL based interactive canvas library GStreamer elements |
| libclutter-gtk-1.0-0:arm64 | Open GL based interactive canvas library GTK+ widget |
| libcmis-0.5-5v5 | CMIS protocol client library |
| libcodec2-0.9:arm64 | Codec2 runtime library |
| libcogl-pango20:arm64 | Object oriented GL/GLES Abstraction/Utility Layer |
| libcogl-path20:arm64 | Object oriented GL/GLES Abstraction/Utility Layer |
| libcogl20:arm64 | Object oriented GL/GLES Abstraction/Utility Layer |
| libcolamd2:arm64 | column approximate minimum degree ordering library for sparse matrices |
| libcolord2:arm64 | system service to manage device colour profiles -- runtime |
| libcom-err2:arm64 | common error description library |
| libconfig-tiny-perl | Read/Write .ini style files with as little code as possible |
| libcpanel-json-xs-perl | module for fast and correct serialising to JSON |
| libcpufreq0 | shared library to deal with the cpufreq Linux kernel feature |
| libcrypt-dev:arm64 | libcrypt development files |
| libcrypt1:arm64 | libcrypt shared library |
| libcryptsetup12:arm64 | disk encryption support - shared library |
| libctf-nobfd0:arm64 | Compact C Type Format library (runtime, no BFD dependency) |
| libctf0:arm64 | Compact C Type Format library (runtime, BFD dependency) |
| libcue2:arm64 | CUE Sheet Parser Library |
| libcups2:arm64 | Common UNIX Printing System(tm) - Core library |
| libcurl3-gnutls:arm64 | easy-to-use client-side URL transfer library (GnuTLS flavour) |
| libcurl4:arm64 | easy-to-use client-side URL transfer library (OpenSSL flavour) |
| libdap27:arm64 | Open-source Project for a Network Data Access Protocol library |
| libdapclient6v5:arm64 | Client library for the Network Data Access Protocol |
| libdata-dpath-perl | DPath is like XPath but for Perl data structures |
| libdata-messagepack-perl | MessagePack serializing/deserializing |
| libdata-optlist-perl | module to parse and validate simple name/value option pairs |
| libdata-validate-domain-perl | perl domain name validation functions |
| libdatrie-dev:arm64 | Development files for double-array trie library |
| libdatrie1:arm64 | Double-array trie library |
| libdav1d4:arm64 | fast and small AV1 video stream decoder (shared library) |
| libdb5.3:arm64 | Berkeley v5.3 Database Libraries [runtime] |
| libdbus-1-3:arm64 | simple interprocess messaging system (library) |
| libdbus-1-dev:arm64 | simple interprocess messaging system (development headers) |
| libdbus-glib-1-2:arm64 | deprecated library for D-Bus IPC |
| libdbusmenu-glib4:arm64 | library for passing menus over DBus |
| libdbusmenu-gtk3-4:arm64 | library for passing menus over DBus - GTK-3+ version |
| libdbusmenu-qt5-2:arm64 | Qt implementation of the DBusMenu protocol |
| libdc1394-25:arm64 | high level programming interface for IEEE 1394 digital cameras |
| libdc1394-dev:arm64 | high level programming interface for IEEE 1394 digital cameras - development |
| libdca0:arm64 | decoding library for DTS Coherent Acoustics streams |
| libdconf1:arm64 | simple configuration storage system - runtime library |
| libde265-0:arm64 | Open H.265 video codec implementation |
| libdebconfclient0:arm64 | Debian Configuration Management System (C-implementation library) |
| libdebuginfod1:arm64 | library to interact with debuginfod (development files) |
| libdeflate-dev:arm64 | headers for whole-buffer compression and decompression library |
| libdeflate0:arm64 | fast, whole-buffer DEFLATE-based compression and decompression |
| libdevel-callchecker-perl | custom op checking attached to subroutines |
| libdevel-size-perl | Perl extension for finding the memory usage of Perl variables |
| libdevel-stacktrace-perl | Perl module containing stack trace and related objects |
| libdevmapper1.02.1:arm64 | Linux Kernel Device Mapper userspace library |
| libdjvulibre-text | Linguistic support files for libdjvulibre |
| libdjvulibre21:arm64 | Runtime support for the DjVu image format |
| libdns-export1110 | Exported DNS Shared Library |
| libdouble-conversion3:arm64 | routines to convert IEEE floats to and from strings |
| libdpkg-perl | Dpkg perl modules |
| libdrm-amdgpu1:arm64 | Userspace interface to amdgpu-specific kernel DRM services -- runtime |
| libdrm-common | Userspace interface to kernel DRM services -- common files |
| libdrm-cursor | A hook of drm cursor APIs to fake cursor plane. |
| libdrm-cursor-dbgsym | debug symbols for libdrm-cursor |
| libdrm-cursor-dev | A hook of drm cursor APIs to fake cursor plane. |
| libdrm-dev:arm64 | Userspace interface to kernel DRM services -- development files |
| libdrm-etnaviv1:arm64 | Userspace interface to etnaviv-specific kernel DRM services -- runtime |
| libdrm-freedreno1:arm64 | Userspace interface to msm/kgsl kernel DRM services -- runtime |
| libdrm-nouveau2:arm64 | Userspace interface to nouveau-specific kernel DRM services -- runtime |
| libdrm-radeon1:arm64 | Userspace interface to radeon-specific kernel DRM services -- runtime |
| libdrm-tegra0:arm64 | Userspace interface to tegra-specific kernel DRM services -- runtime |
| libdrm2:arm64 | Userspace interface to kernel DRM services -- runtime |
| libdv4:arm64 | software library for DV format digital video (runtime lib) |
| libdvbpsi10:arm64 | library for MPEG TS and DVB PSI tables decoding and generating |
| libdvbv5-0:arm64 | Libraries to control, scan and zap on Digital TV channels |
| libdvbv5-0-dbgsym:arm64 | debug symbols for libdvbv5-0 |
| libdvbv5-dev:arm64 | Development files for libdvbv5 |
| libdvbv5-doc | Doxygen generated documentation for libdvbv5 |
| libdvdnav4:arm64 | DVD navigation library |
| libdvdread8:arm64 | library for reading DVDs |
| libdw-dev:arm64 | libdw1 development libraries and header files |
| libdw1:arm64 | library that provides access to the DWARF debug information |
| libdynaloader-functions-perl | deconstructed dynamic C library loading |
| libe-book-0.1-1:arm64 | library for reading and converting various e-book formats |
| libebml5:arm64 | access library for the EBML format (shared library) |
| libedit2:arm64 | BSD editline and history libraries |
| libegl-dev:arm64 | Vendor neutral GL dispatch library -- EGL development files |
| libegl-mesa0:arm64 | free implementation of the EGL API -- Mesa vendor library |
| libegl1:arm64 | Vendor neutral GL dispatch library -- EGL support |
| libegl1-mesa-dev:arm64 | free implementation of the EGL API -- development files |
| libelf-dev:arm64 | libelf1 development libraries and header files |
| libelf1:arm64 | library to read and write ELF files |
| libemail-address-xs-perl | Perl library for RFC 5322 address/group parsing and formatting |
| libencode-locale-perl | utility to determine the locale encoding |
| libeot0:arm64 | Library for parsing/converting Embedded OpenType files |
| libepoxy-dev:arm64 | OpenGL function pointer management library- development |
| libepoxy0:arm64 | OpenGL function pointer management library |
| libepsilon1:arm64 | Library for wavelet image compression |
| libept1.6.0:arm64 | High-level library for managing Debian package information |
| libepubgen-0.1-1:arm64 | EPUB generator library |
| liberror-perl | Perl module for error/exception handling in an OO-ish way |
| libestr0:arm64 | Helper functions for handling strings (lib) |
| libetonyek-0.1-1:arm64 | library for reading and converting Apple Keynote presentations |
| libevdev2:arm64 | wrapper library for evdev devices |
| libevent-2.1-7:arm64 | Asynchronous event notification library |
| libexception-class-perl | module that allows you to declare real exception classes in Perl |
| libexempi8:arm64 | library to parse XMP metadata (Library) |
| libexif-dev:arm64 | library to parse EXIF files (development files) |
| libexif12:arm64 | library to parse EXIF files |
| libexiv2-27:arm64 | EXIF/IPTC/XMP metadata manipulation library |
| libexo-2-0:arm64 | Library with extensions for Xfce (GTK-3 version) |
| libexo-common | libexo common files |
| libexpat1:arm64 | XML parsing C library - runtime library |
| libexpat1-dev:arm64 | XML parsing C library - development kit |
| libexporter-tiny-perl | tiny exporter similar to Sub::Exporter |
| libext2fs2:arm64 | ext2/ext3/ext4 file system libraries |
| libexttextcat-2.0-0:arm64 | Language detection library |
| libexttextcat-data | Language detection library - data files |
| libfaad2:arm64 | freeware Advanced Audio Decoder - runtime files |
| libfakeroot:arm64 | tool for simulating superuser privileges - shared libraries |
| libfam0:arm64 | Client library to control the FAM daemon |
| libfastjson4:arm64 | fast json library for C |
| libfdisk1:arm64 | fdisk partitioning library |
| libffi-dev:arm64 | Foreign Function Interface library (development files) |
| libffi7:arm64 | Foreign Function Interface library runtime |
| libffmpegthumbnailer4v5 | shared library for ffmpegthumbnailer |
| libfftw3-double3:arm64 | Library for computing Fast Fourier Transforms - Double precision |
| libfftw3-single3:arm64 | Library for computing Fast Fourier Transforms - Single precision |
| libfido2-1:arm64 | library for generating and verifying FIDO 2.0 objects |
| libfile-basedir-perl | Perl module to use the freedesktop basedir specification |
| libfile-desktopentry-perl | Perl module to handle freedesktop .desktop files |
| libfile-fcntllock-perl | Perl module for file locking with fcntl(2) |
| libfile-find-rule-perl | module to search for files based on rules |
| libfile-listing-perl | module to parse directory listings |
| libfile-mimeinfo-perl | Perl module to determine file types |
| libfl-dev:arm64 | static library for flex (a fast lexical analyzer generator) |
| libfl2:arm64 | SHARED library for flex (a fast lexical analyzer generator) |
| libflac8:arm64 | Free Lossless Audio Codec - runtime C library |
| libflite1:arm64 | Small run-time speech synthesis engine - shared libraries |
| libfltk1.1:arm64 | Fast Light Toolkit - shared libraries |
| libfluidsynth2:arm64 | Real-time MIDI software synthesizer (runtime library) |
| libfm-extra4:arm64 | file management support (extra library) |
| libfm-qt-l10n | Language package for libfm-qt |
| libfm-qt8:arm64 | file management support for pcmanfm-qt |
| libfont-ttf-perl | Perl module for TrueType font hacking |
| libfontconfig-dev:arm64 | generic font configuration library - development |
| libfontconfig1:arm64 | generic font configuration library - runtime |
| libfontconfig1-dev:arm64 | generic font configuration library - dummy package |
| libfontenc-dev:arm64 | X11 font encoding library (development headers) |
| libfontenc1:arm64 | X11 font encoding library |
| libfreehand-0.1-1 | Library for parsing the FreeHand file format structure |
| libfreetype-dev:arm64 | FreeType 2 font engine, development files |
| libfreetype6:arm64 | FreeType 2 font engine, shared library files |
| libfreetype6-dev:arm64 | FreeType 2 font engine, development files (transitional package) |
| libfreexl1:arm64 | library for direct reading of Microsoft Excel spreadsheets |
| libfribidi-dev:arm64 | Development files for FreeBidi library |
| libfribidi0:arm64 | Free Implementation of the Unicode BiDi algorithm |
| libfuse2:arm64 | Filesystem in Userspace (library) |
| libfyba0:arm64 | FYBA library to read and write Norwegian geodata standard format SOSI |
| libgarcon-1-0:arm64 | freedesktop.org compliant menu implementation for Xfce |
| libgarcon-common | common files for libgarcon menu implementation |
| libgarcon-gtk3-1-0:arm64 | menu library for Xfce (GTK3 library) |
| libgbm1:arm64 | generic buffer management API -- runtime |
| libgc1:arm64 | conservative garbage collector for C and C++ |
| libgcc-10-dev:arm64 | GCC support library (development files) |
| libgcc-9-dev:arm64 | GCC support library (development files) |
| libgcc-s1:arm64 | GCC support library |
| libgck-1-0:arm64 | Glib wrapper library for PKCS#11 - runtime |
| libgcr-base-3-1:arm64 | Library for Crypto related tasks |
| libgcrypt20:arm64 | LGPL Crypto library - runtime library |
| libgd3:arm64 | GD Graphics Library |
| libgdal28 | Geospatial Data Abstraction Library |
| libgdata-common | Library for accessing GData webservices - common data files |
| libgdata22:arm64 | Library for accessing GData webservices - shared libraries |
| libgdbm-compat4:arm64 | GNU dbm database routines (legacy support runtime version) |
| libgdbm6:arm64 | GNU dbm database routines (runtime version) |
| libgdcm-dev | Grassroots DICOM development libraries and headers |
| libgdcm3.0:arm64 | Grassroots DICOM runtime libraries |
| libgdk-pixbuf-2.0-0:arm64 | GDK Pixbuf library |
| libgdk-pixbuf-2.0-dev:arm64 | GDK Pixbuf library (development files) |
| libgdk-pixbuf-xlib-2.0-0:arm64 | GDK Pixbuf library (deprecated Xlib integration) |
| libgdk-pixbuf2.0-0:arm64 | GDK Pixbuf library (transitional package) |
| libgdk-pixbuf2.0-bin | GDK Pixbuf library (thumbnailer) |
| libgdk-pixbuf2.0-common | GDK Pixbuf library - data files |
| libgee-0.8-2:arm64 | GObject based collection and utility library |
| libgeoip1:arm64 | non-DNS IP-to-country resolver library |
| libgeos-3.9.0:arm64 | Geometry engine for Geographic Information Systems - C++ Library |
| libgeos-c1v5:arm64 | Geometry engine for Geographic Information Systems - C Library |
| libgeotiff5:arm64 | GeoTIFF (geografic enabled TIFF) library -- run-time files |
| libgexiv2-2:arm64 | GObject-based wrapper around the Exiv2 library |
| libgfortran5:arm64 | Runtime library for GNU Fortran applications |
| libgif7:arm64 | library for GIF images (library) |
| libgirara-gtk3-3:arm64 | library for minimalistic user interfaces (shared libraries) |
| libgirepository-1.0-1:arm64 | Library for handling GObject introspection data (runtime library) |
| libgl-dev:arm64 | Vendor neutral GL dispatch library -- GL development files |
| libgl1:arm64 | Vendor neutral GL dispatch library -- legacy GL support |
| libgl1-mesa-dri:arm64 | free implementation of the OpenGL API -- DRI modules |
| libgl2ps1.4 | Lib providing high quality vector output for OpenGL application |
| libglapi-mesa:arm64 | free implementation of the GL API -- shared library |
| libgles-dev:arm64 | Vendor neutral GL dispatch library -- GLES development files |
| libgles1:arm64 | Vendor neutral GL dispatch library -- GLESv1 support |
| libgles2:arm64 | Vendor neutral GL dispatch library -- GLESv2 support |
| libgles2-mesa-dev:arm64 | transitional dummy package |
| libglew2.1:arm64 | OpenGL Extension Wrangler - runtime environment |
| libglib2.0-0:arm64 | GLib library of C routines |
| libglib2.0-bin | Programs for the GLib library |
| libglib2.0-data | Common files for GLib library |
| libglib2.0-dev:arm64 | Development files for the GLib library |
| libglib2.0-dev-bin | Development utilities for the GLib library |
| libglibmm-2.4-1v5:arm64 | C++ wrapper for the GLib toolkit (shared libraries) |
| libglu1-mesa:arm64 | Mesa OpenGL utility library (GLU) |
| libglu1-mesa-dev:arm64 | Mesa OpenGL utility library -- development files |
| libglvnd-dev:arm64 | Vendor neutral GL dispatch library -- development files |
| libglvnd0:arm64 | Vendor neutral GL dispatch library |
| libglx-dev:arm64 | Vendor neutral GL dispatch library -- GLX development files |
| libglx-mesa0:arm64 | free implementation of the OpenGL API -- GLX vendor library |
| libglx0:arm64 | Vendor neutral GL dispatch library -- GLX support |
| libgme0:arm64 | Playback library for video game music files - shared library |
| libgmime-3.0-0:arm64 | MIME message parser and creator library |
| libgmp10:arm64 | Multiprecision arithmetic library |
| libgnome-autoar-0-0:arm64 | Archives integration support for GNOME |
| libgnome-desktop-3-19:arm64 | Utility library for loading .desktop files - runtime files |
| libgnome-menu-3-0:arm64 | GNOME implementation of the freedesktop menu specification |
| libgnutls30:arm64 | GNU TLS library - main runtime library |
| libgoa-1.0-0b:arm64 | library for GNOME Online Accounts |
| libgoa-1.0-common | library for GNOME Online Accounts - common files |
| libgomp1:arm64 | GCC OpenMP (GOMP) support library |
| libgpg-error0:arm64 | GnuPG development runtime library |
| libgpgme11:arm64 | GPGME - GnuPG Made Easy (library) |
| libgpgmepp6:arm64 | C++ wrapper library for GPGME |
| libgphoto2-6:arm64 | gphoto2 digital camera library |
| libgphoto2-dev:arm64 | gphoto2 digital camera library (development files) |
| libgphoto2-port12:arm64 | gphoto2 digital camera port library |
| libgpm2:arm64 | General Purpose Mouse - shared library |
| libgraphene-1.0-0:arm64 | library of graphic data types |
| libgraphite2-3:arm64 | Font rendering engine for Complex Scripts -- library |
| libgraphite2-dev:arm64 | Development files for libgraphite2 |
| libgs9:arm64 | interpreter for the PostScript language and for PDF - Library |
| libgs9-common | interpreter for the PostScript language and for PDF - common files |
| libgsasl7:arm64 | GNU SASL library |
| libgsf-1-114:arm64 | Structured File Library - runtime version |
| libgsf-1-common | Structured File Library - common files |
| libgsm1:arm64 | Shared libraries for GSM speech compressor |
| libgssapi-krb5-2:arm64 | MIT Kerberos runtime libraries - krb5 GSS-API Mechanism |
| libgssdp-1.2-0:arm64 | GObject-based library for SSDP |
| libgstreamer-gl1.0-0:arm64 | GStreamer GL libraries |
| libgstreamer-gl1.0-0-dbgsym:arm64 | debug symbols for libgstreamer-gl1.0-0 |
| libgstreamer-opencv1.0-0:arm64 | GStreamer OpenCV libraries |
| libgstreamer-opencv1.0-0-dbgsym:arm64 | debug symbols for libgstreamer-opencv1.0-0 |
| libgstreamer-plugins-bad1.0-0:arm64 | GStreamer libraries from the "bad" set |
| libgstreamer-plugins-bad1.0-0-dbgsym:arm64 | debug symbols for libgstreamer-plugins-bad1.0-0 |
| libgstreamer-plugins-bad1.0-dev:arm64 | GStreamer development files for libraries from the "bad" set |
| libgstreamer-plugins-base1.0-0:arm64 | GStreamer libraries from the "base" set |
| libgstreamer-plugins-base1.0-0-dbgsym:arm64 | debug symbols for libgstreamer-plugins-base1.0-0 |
| libgstreamer-plugins-base1.0-dev:arm64 | GStreamer development files for libraries from the "base" set |
| libgstreamer1.0-0:arm64 | Core GStreamer libraries and elements |
| libgstreamer1.0-0-dbgsym:arm64 | debug symbols for libgstreamer1.0-0 |
| libgstreamer1.0-dev:arm64 | GStreamer core development files |
| libgstreamer1.0-dev-dbgsym:arm64 | debug symbols for libgstreamer1.0-dev |
| libgtk-3-0:arm64 | GTK graphical user interface library |
| libgtk-3-common | common files for the GTK graphical user interface library |
| libgtk-3-dev:arm64 | development files for the GTK library |
| libgtk2.0-0:arm64 | GTK graphical user interface library - old version |
| libgtk2.0-common | common files for the GTK graphical user interface library |
| libgtk2.0-dev:arm64 | development files for the GTK library |
| libgtkmm-3.0-1v5:arm64 | C++ wrappers for GTK+ (shared libraries) |
| libgtop-2.0-11:arm64 | gtop system monitoring library (shared) |
| libgtop2-common | gtop system monitoring library (common) |
| libgudev-1.0-0:arm64 | GObject-based wrapper library for libudev |
| libgupnp-1.2-0:arm64 | GObject-based library for UPnP |
| libgupnp-igd-1.0-4:arm64 | library to handle UPnP IGD port mapping |
| libgxps2:arm64 | handling and rendering XPS documents (library) |
| libharfbuzz-dev:arm64 | Development files for OpenType text shaping engine |
| libharfbuzz-gobject0:arm64 | OpenType text shaping engine ICU backend (GObject library) |
| libharfbuzz-icu0:arm64 | OpenType text shaping engine ICU backend |
| libharfbuzz0b:arm64 | OpenType text shaping engine (shared library) |
| libhdf4-0-alt | Hierarchical Data Format library (without NetCDF) |
| libhdf5-103-1:arm64 | HDF5 C runtime files - serial version |
| libhdf5-hl-100:arm64 | HDF5 High Level runtime files - serial version |
| libheif1:arm64 | ISO/IEC 23008-12:2017 HEIF file format decoder - shared library |
| libhogweed6:arm64 | low level cryptographic library (public-key cryptos) |
| libhtml-html5-entities-perl | module to encode and decode character entities defined in HTML5 |
| libhtml-parser-perl | collection of modules that parse HTML text documents |
| libhtml-tagset-perl | data tables pertaining to HTML |
| libhtml-tree-perl | Perl module to represent and create HTML syntax trees |
| libhttp-cookies-perl | HTTP cookie jars |
| libhttp-date-perl | module of date conversion routines |
| libhttp-message-perl | perl interface to HTTP style messages |
| libhttp-negotiate-perl | implementation of content negotiation |
| libhunspell-1.7-0:arm64 | spell checker and morphological analyzer (shared library) |
| libhyphen0:arm64 | ALTLinux hyphenation library - shared library |
| libi2c0:arm64 | userspace I2C programming library |
| libical3:arm64 | iCalendar library implementation in C (runtime) |
| libice-dev:arm64 | X11 Inter-Client Exchange library (development headers) |
| libice6:arm64 | X11 Inter-Client Exchange library |
| libiconv-hook-dev | header files of libiconv-hook |
| libiconv-hook1 | extension of iconv for libapache-mod-encoding |
| libicu-dev:arm64 | Development files for International Components for Unicode |
| libicu67:arm64 | International Components for Unicode |
| libid3tag0:arm64 | ID3 tag reading library from the MAD project |
| libidn11:arm64 | GNU Libidn library, implementation of IETF IDN specifications |
| libidn2-0:arm64 | Internationalized domain names (IDNA2008/TR46) library |
| libiec61883-0:arm64 | partial implementation of IEC 61883 (shared lib) |
| libijs-0.35:arm64 | IJS raster image transport protocol: shared library |
| libilmbase-dev:arm64 | development files for IlmBase |
| libilmbase25:arm64 | several utility libraries from ILM used by OpenEXR |
| libimlib2:arm64 | image loading, rendering, saving library |
| libimobiledevice6:arm64 | Library for communicating with iPhone and other Apple devices |
| libimport-into-perl | module for importing packages into other packages |
| libinput-bin | input device management and event handling library - udev quirks |
| libinput10:arm64 | input device management and event handling library - shared library |
| libinstpatch-1.0-2:arm64 | MIDI instrument editing library |
| libio-html-perl | open an HTML file with automatic charset detection |
| libio-socket-ssl-perl | Perl module implementing object oriented interface to SSL sockets |
| libio-string-perl | Emulate IO::File interface for in-core strings |
| libio-stringy-perl | modules for I/O on in-core objects (strings/arrays) |
| libip4tc2:arm64 | netfilter libip4tc library |
| libip6tc2:arm64 | netfilter libip6tc library |
| libipc-run3-perl | run a subprocess with input/output redirection |
| libipc-system-simple-perl | Perl module to run commands simply, with detailed diagnostics |
| libiptcdata0 | Library to parse IPTC metadata |
| libisc-export1105:arm64 | Exported ISC Shared Library |
| libisl23:arm64 | manipulating sets and relations of integer points bounded by linear constraints |
| libiterator-perl | Perl implementation of iterators |
| libiterator-util-perl | Useful functions for creating and manipulating iterator objects |
| libitm1:arm64 | GNU Transactional Memory Library |
| libiw30:arm64 | Wireless tools - library |
| libixml10:arm64 | Portable SDK for UPnP Devices, version 1.8 (ixml shared library) |
| libjack-jackd2-0:arm64 | JACK Audio Connection Kit (libraries) |
| libjansson4:arm64 | C library for encoding, decoding and manipulating JSON data |
| libjbig-dev:arm64 | JBIGkit development files |
| libjbig0:arm64 | JBIGkit libraries |
| libjbig2dec0:arm64 | JBIG2 decoder library - shared libraries |
| libjim0.79:arm64 | small-footprint implementation of Tcl - shared library |
| libjpeg-dev:arm64 | Development files for the JPEG library [dummy package] |
| libjpeg62-turbo:arm64 | libjpeg-turbo JPEG runtime library |
| libjpeg62-turbo-dev:arm64 | Development files for the libjpeg-turbo JPEG library |
| libjs-bootstrap | HTML, CSS and JS framework |
| libjs-jquery | JavaScript library for dynamic web applications |
| libjs-mathjax | JavaScript display engine for LaTeX and MathML |
| libjs-sphinxdoc | JavaScript support for Sphinx documentation |
| libjs-underscore | JavaScript's functional programming helper library |
| libjson-c5:arm64 | JSON manipulation library - shared library |
| libjson-glib-1.0-0:arm64 | GLib JSON manipulation library |
| libjson-glib-1.0-common | GLib JSON manipulation library (common files) |
| libjson-maybexs-perl | interface to the best available JSON module |
| libjsoncpp24:arm64 | library for reading and writing JSON for C++ |
| libjxr-tools | JPEG-XR lib - command line apps |
| libjxr0:arm64 | JPEG-XR lib - libraries |
| libk5crypto3:arm64 | MIT Kerberos runtime libraries - Crypto Library |
| libkate1:arm64 | Codec for karaoke and text encapsulation |
| libkeybinder-3.0-0:arm64 | registers global key bindings for applications - Gtk+3 |
| libkeyutils1:arm64 | Linux Key Management Utilities (library) |
| libkf5archive5:arm64 | Qt 5 addon providing access to numerous types of archives |
| libkf5attica-dev | development files for libkf5attica5 |
| libkf5attica5:arm64 | Qt library that implements the Open Collaboration Services API |
| libkf5auth-data | Abstraction to system policy and authentication features |
| libkf5auth-dev:arm64 | Abstraction to system policy and authentication features |
| libkf5auth-dev-bin | Abstraction to system policy and authentication features |
| libkf5auth5:arm64 | Abstraction to system policy and authentication features |
| libkf5authcore5:arm64 | Abstraction to system policy and authentication features |
| libkf5bookmarks-data | Qt library with support for bookmarks and the XBEL format. |
| libkf5bookmarks-dev | Qt library with support for bookmarks and the XBEL format. |
| libkf5bookmarks5:arm64 | Qt library with support for bookmarks and the XBEL format. |
| libkf5codecs-data | collection of methods to manipulate strings |
| libkf5codecs-dev | development files for kcodecs |
| libkf5codecs5:arm64 | collection of methods to manipulate strings |
| libkf5completion-data | Widgets with advanced auto-completion features. |
| libkf5completion-dev | development files for kcompletion |
| libkf5completion5:arm64 | Widgets with advanced auto-completion features. |
| libkf5config-bin | configuration settings framework for Qt |
| libkf5config-data | configuration settings framework for Qt |
| libkf5config-dev:arm64 | configuration settings framework for Qt |
| libkf5config-dev-bin | configuration settings framework for Qt -- binary package |
| libkf5configcore5:arm64 | configuration settings framework for Qt |
| libkf5configgui5:arm64 | configuration settings framework for Qt |
| libkf5configwidgets-data | Extra widgets for easier configuration support. |
| libkf5configwidgets-dev | development files for kconfigwidgets |
| libkf5configwidgets5:arm64 | Extra widgets for easier configuration support. |
| libkf5coreaddons-data | KDE Frameworks 5 addons to QtCore - data files |
| libkf5coreaddons-dev:arm64 | KDE Frameworks 5 addons to QtCore - development files |
| libkf5coreaddons-dev-bin | KDE Frameworks 5 addons to QtCore - development files |
| libkf5coreaddons5:arm64 | KDE Frameworks 5 addons to QtCore |
| libkf5crash5:arm64 | Support for application crash analysis and bug report from apps |
| libkf5dbusaddons-data | class library for qtdbus |
| libkf5dbusaddons-dev | development files for dbusaddons |
| libkf5dbusaddons5:arm64 | class library for qtdbus |
| libkf5doctools5:arm64 | Tools to generate documentation in various formats from DocBook |
| libkf5globalaccel-bin | Configurable global shortcut support. |
| libkf5globalaccel-data | Configurable global shortcut support. |
| libkf5globalaccel-dev:arm64 | development files for kglobalaccel |
| libkf5globalaccel5:arm64 | Configurable global shortcut support. |
| libkf5globalaccelprivate5:arm64 | Configurable global shortcut support - private runtime library |
| libkf5guiaddons-dev | development headers for the kguiaddons framework |
| libkf5guiaddons5:arm64 | additional addons for QtGui |
| libkf5i18n-data | Advanced internationalization framework. |
| libkf5i18n-dev:arm64 | Advanced internationalization framework. |
| libkf5i18n5:arm64 | Advanced internationalization framework. |
| libkf5iconthemes-data | Support for icon themes. |
| libkf5iconthemes-dev | development files for kiconthemes |
| libkf5iconthemes5:arm64 | Support for icon themes. |
| libkf5idletime5:arm64 | library to provide information about idle time |
| libkf5itemviews-data | Qt library with additional widgets for ItemModels |
| libkf5itemviews-dev | Qt library with additional widgets for ItemModels |
| libkf5itemviews5:arm64 | Qt library with additional widgets for ItemModels |
| libkf5jobwidgets-data | Widgets for tracking KJob instances |
| libkf5jobwidgets-dev | Widgets for tracking KJob instances |
| libkf5jobwidgets5:arm64 | Widgets for tracking KJob instances |
| libkf5kio-dev | resource and network access abstraction (development files) |
| libkf5kiocore5:arm64 | resource and network access abstraction (KIO core library) |
| libkf5kiofilewidgets5:arm64 | resource and network access abstraction (KIO file widgets library) |
| libkf5kiogui5:arm64 | resource and network access abstraction (KIO gui library) |
| libkf5kiontlm5:arm64 | resource and network access abstraction (KIO NTLM library) |
| libkf5kiowidgets5:arm64 | resource and network access abstraction (KIO widgets library) |
| libkf5mediaplayer-data | Plugin interface for media player features. |
| libkf5mediaplayer-dev | Plugin interface for media player features. |
| libkf5mediaplayer5:arm64 | Plugin interface for media player features. |
| libkf5notifications-data | Framework for desktop notifications |
| libkf5notifications5:arm64 | Framework for desktop notifications |
| libkf5parts-data | Document centric plugin system. |
| libkf5parts-dev | development files for kparts |
| libkf5parts5:arm64 | Document centric plugin system. |
| libkf5service-bin | Advanced plugin and service introspection |
| libkf5service-data | Advanced plugin and service introspection |
| libkf5service-dev:arm64 | development files for kservice |
| libkf5service5:arm64 | Advanced plugin and service introspection |
| libkf5solid-dev | Qt library to query and control hardware |
| libkf5solid5:arm64 | Qt library to query and control hardware |
| libkf5solid5-data | Qt library to query and control hardware |
| libkf5sonnet-dev:arm64 | spell checking library for Qt, devel files |
| libkf5sonnet-dev-bin | spell checking library for Qt, devel binaries |
| libkf5sonnet5-data | spell checking library for Qt, data files |
| libkf5sonnetcore5:arm64 | spell checking library for Qt, core lib |
| libkf5sonnetui5:arm64 | spell checking library for Qt, ui lib |
| libkf5textwidgets-data | Advanced text editing widgets. |
| libkf5textwidgets-dev | development files for ktextwidgets |
| libkf5textwidgets5:arm64 | Advanced text editing widgets. |
| libkf5wallet-bin | Secure and unified container for user passwords. |
| libkf5wallet-data | Secure and unified container for user passwords. |
| libkf5wallet5:arm64 | Secure and unified container for user passwords. |
| libkf5waylandclient5:arm64 | Qt library wrapper for Wayland libraries |
| libkf5widgetsaddons-data | add-on widgets and classes for applications that use the Qt Widgets module |
| libkf5widgetsaddons-dev | development files for kwidgetsaddons |
| libkf5widgetsaddons5:arm64 | add-on widgets and classes for applications that use the Qt Widgets module |
| libkf5windowsystem-data | Convenience access to certain properties and features of the window manager |
| libkf5windowsystem-dev | development files for kwindowsystem |
| libkf5windowsystem5:arm64 | Convenience access to certain properties and features of the window manager |
| libkf5xmlgui-data | User configurable main windows. |
| libkf5xmlgui-dev:arm64 | User configurable main windows. |
| libkf5xmlgui5:arm64 | User configurable main windows. |
| libklibc:arm64 | minimal libc subset for use with initramfs |
| libkmlbase1:arm64 | Library to manipulate KML 2.2 OGC standard files - libkmlbase |
| libkmldom1:arm64 | Library to manipulate KML 2.2 OGC standard files - libkmldom |
| libkmlengine1:arm64 | Library to manipulate KML 2.2 OGC standard files - libkmlengine |
| libkmod2:arm64 | libkmod shared library |
| libkms1:arm64 | Userspace interface to kernel DRM KMS services |
| libkms1-dbgsym:arm64 | debug symbols for libkms1 |
| libkrb5-3:arm64 | MIT Kerberos runtime libraries |
| libkrb5support0:arm64 | MIT Kerberos runtime libraries - Support library |
| libksba8:arm64 | X.509 and CMS support library |
| libkwalletbackend5-5:arm64 | Secure and unified container for user passwords. |
| liblangtag-common | library to access tags for identifying languages -- data |
| liblangtag1:arm64 | library to access tags for identifying languages |
| liblapack3:arm64 | Library of linear algebra routines 3 - shared version |
| liblcms2-2:arm64 | Little CMS 2 color management library |
| libldap-2.4-2:arm64 | OpenLDAP libraries |
| libldb2:arm64 | LDAP-like embedded database - shared library |
| liblept5:arm64 | image processing library |
| liblightdm-gobject-1-0:arm64 | simple display manager (GObject library) |
| liblilv-0-0:arm64 | library for simple use of LV2 plugins |
| liblirc-client0:arm64 | infra-red remote control support - client library |
| liblist-compare-perl | Perl module for comparing elements of two or more lists |
| liblist-moreutils-perl | Perl module with additional list functions not found in List::Util |
| liblist-moreutils-xs-perl | Perl module providing compiled List::MoreUtils functions |
| liblist-utilsby-perl | higher-order list utility functions |
| libllvm11:arm64 | Modular compiler and toolchain technologies, runtime library |
| libllvm13:arm64 | Modular compiler and toolchain technologies, runtime library |
| libllvm9:arm64 | Modular compiler and toolchain technologies, runtime library |
| liblmdb0:arm64 | Lightning Memory-Mapped Database shared library |
| liblocale-gettext-perl | module using libc functions for internationalization in Perl |
| liblognorm5:arm64 | log normalizing library |
| liblqr-1-0:arm64 | converts plain array images into multi-size representation |
| liblsan0:arm64 | LeakSanitizer -- a memory leak detector (runtime) |
| libltc11:arm64 | linear timecode library |
| libltdl-dev:arm64 | System independent dlopen wrapper for GNU libtool |
| libltdl7:arm64 | System independent dlopen wrapper for GNU libtool |
| liblua5.1-0:arm64 | Shared library for the Lua interpreter version 5.1 |
| liblua5.2-0:arm64 | Shared library for the Lua interpreter version 5.2 |
| liblua5.3-0:arm64 | Shared library for the Lua interpreter version 5.3 |
| liblua5.4-0:arm64 | Shared library for the Lua interpreter version 5.4 |
| liblwp-mediatypes-perl | module to guess media type for a file or a URL |
| liblwp-protocol-https-perl | HTTPS driver for LWP::UserAgent |
| liblxqt-l10n | Language package for liblxqt |
| liblxqt0 | Shared libraries for LXQt desktop environment (libs) |
| liblz4-1:arm64 | Fast LZ compression algorithm library - runtime |
| liblzma-dev:arm64 | XZ-format compression library - development files |
| liblzma5:arm64 | XZ-format compression library |
| liblzo2-2:arm64 | data compression library |
| libmad0:arm64 | MPEG audio decoder library |
| libmagic-mgc | File type determination library using "magic" numbers (compiled magic file) |
| libmagic1:arm64 | Recognize the type of data in a file using "magic" numbers - library |
| libmagickcore-6.q16-6:arm64 | low-level image manipulation library -- quantum depth Q16 |
| libmagickcore-6.q16-6-extra:arm64 | low-level image manipulation library - extra codecs (Q16) |
| libmagickwand-6.q16-6:arm64 | image manipulation library -- quantum depth Q16 |
| libmali-valhall-g610-g13p0-x11-gbm | Mali GPU User-Space Binary Drivers |
| libmariadb3:arm64 | MariaDB database client library |
| libmarkdown2:arm64 | implementation of the Markdown markup language in C (library) |
| libmatroska7:arm64 | extensible open standard audio/video container format (shared library) |
| libmaxminddb0:arm64 | IP geolocation database library |
| libmd0:arm64 | message digest functions from BSD systems - shared library |
| libmd4c0:arm64 | Markdown for C |
| libmenu-cache-bin | LXDE implementation of the freedesktop Menu's cache (libexec) |
| libmenu-cache3:arm64 | LXDE implementation of the freedesktop Menu's cache |
| libmhash2:arm64 | Library for cryptographic hashing and message authentication |
| libmikmod3:arm64 | Portable sound library |
| libminizip1:arm64 | compression library - minizip library |
| libmjpegutils-2.1-0:arm64 | MJPEG capture/editing/replay and MPEG encoding toolset (library) |
| libmm-glib0:arm64 | D-Bus service for managing modems - shared libraries |
| libmms0:arm64 | MMS stream protocol library - shared library |
| libmnl0:arm64 | minimalistic Netlink communication library |
| libmodplug1:arm64 | shared libraries for mod music based on ModPlug |
| libmodule-implementation-perl | module for loading one of several alternate implementations of a module |
| libmodule-runtime-perl | Perl module for runtime module handling |
| libmoo-perl | Minimalist Object Orientation library (with Moose compatibility) |
| libmoox-aliases-perl | easy aliasing of methods and attributes in Moo |
| libmotif-common | Motif - common files |
| libmotif-dev:arm64 | Motif - development files |
| libmount-dev:arm64 | device mounting library - headers |
| libmount1:arm64 | device mounting library |
| libmouse-perl | lightweight object framework for Perl |
| libmp3lame0:arm64 | MP3 encoding library |
| libmpc3:arm64 | multiple precision complex floating-point library |
| libmpcdec6:arm64 | MusePack decoder - library |
| libmpdec3:arm64 | library for decimal floating point arithmetic (runtime library) |
| libmpeg2-4:arm64 | MPEG1 and MPEG2 video decoder library |
| libmpeg2encpp-2.1-0:arm64 | MJPEG capture/editing/replay and MPEG encoding toolset (library) |
| libmpfr6:arm64 | multiple precision floating-point computation |
| libmpg123-0:arm64 | MPEG layer 1/2/3 audio decoder (shared library) |
| libmplex2-2.1-0:arm64 | MJPEG capture/editing/replay and MPEG encoding toolset (library) |
| libmrm4:arm64 | Motif - MRM (Motif Resource Manager) shared library |
| libmspub-0.1-1:arm64 | library for parsing the mspub file structure |
| libmtdev1:arm64 | Multitouch Protocol Translation Library - shared library |
| libmtp-common | Media Transfer Protocol (MTP) common files |
| libmtp9:arm64 | Media Transfer Protocol (MTP) library |
| libmwaw-0.3-3:arm64 | import library for some old Mac text documents |
| libmysofa1:arm64 | library to read HRTFs stored in the AES69-2015 SOFA format |
| libmythes-1.2-0:arm64 | simple thesaurus library |
| libnamespace-clean-perl | module for keeping imports and functions out of the current namespace |
| libnautilus-extension1a:arm64 | libraries for nautilus components - runtime version |
| libncurses-dev:arm64 | developer's libraries for ncurses |
| libncurses6:arm64 | shared libraries for terminal handling |
| libncursesw6:arm64 | shared libraries for terminal handling (wide character support) |
| libndp0:arm64 | Library for Neighbor Discovery Protocol |
| libneon27-gnutls:arm64 | HTTP and WebDAV client library (GnuTLS enabled) |
| libnet-dbus-perl | Perl extension for the DBus bindings |
| libnet-domain-tld-perl | list of currently available Top-level Domains (TLDs) |
| libnet-http-perl | module providing low-level HTTP connection client |
| libnet-ssleay-perl | Perl module for Secure Sockets Layer (SSL) |
| libnetcdf18:arm64 | Interface for scientific data access to large binary data |
| libnetfilter-conntrack3:arm64 | Netfilter netlink-conntrack library |
| libnettle8:arm64 | low level cryptographic library (symmetric and one-way cryptos) |
| libnewt0.52:arm64 | Not Erik's Windowing Toolkit - text mode windowing with slang |
| libnfnetlink0:arm64 | Netfilter netlink library |
| libnfs13:arm64 | NFS client library (shared library) |
| libnftnl11:arm64 | Netfilter nftables userspace API library |
| libnghttp2-14:arm64 | library implementing HTTP/2 protocol (shared library) |
| libnginx-mod-http-auth-pam | PAM authentication module for Nginx |
| libnginx-mod-http-cache-purge | Purge content from Nginx caches |
| libnginx-mod-http-dav-ext | WebDAV missing commands support for Nginx |
| libnginx-mod-http-echo | Bring echo and more shell style goodies to Nginx |
| libnginx-mod-http-fancyindex | Fancy indexes module for the Nginx |
| libnginx-mod-http-geoip | GeoIP HTTP module for Nginx |
| libnginx-mod-http-geoip2 | GeoIP2 HTTP module for Nginx |
| libnginx-mod-http-headers-more-filter | Set and clear input and output headers for Nginx |
| libnginx-mod-http-image-filter | HTTP image filter module for Nginx |
| libnginx-mod-http-lua | Lua module for Nginx |
| libnginx-mod-http-ndk | Nginx Development Kit module |
| libnginx-mod-http-perl | Perl module for Nginx |
| libnginx-mod-http-subs-filter | Substitution filter module for Nginx |
| libnginx-mod-http-uploadprogress | Upload progress system for Nginx |
| libnginx-mod-http-upstream-fair | Nginx Upstream Fair Proxy Load Balancer |
| libnginx-mod-http-xslt-filter | XSLT Transformation module for Nginx |
| libnginx-mod-mail | Mail module for Nginx |
| libnginx-mod-nchan | Fast, flexible pub/sub server for Nginx |
| libnginx-mod-stream | Stream module for Nginx |
| libnginx-mod-stream-geoip | GeoIP Stream module for Nginx |
| libnginx-mod-stream-geoip2 | GeoIP2 Stream module for Nginx |
| libnice10:arm64 | ICE library (shared library) |
| libnl-3-200:arm64 | library for dealing with netlink sockets |
| libnl-genl-3-200:arm64 | library for dealing with netlink sockets - generic netlink |
| libnl-route-3-200:arm64 | library for dealing with netlink sockets - route interface |
| libnm-dev:arm64 | GObject-based client library for NetworkManager (development files) |
| libnm0:arm64 | GObject-based client library for NetworkManager |
| libnm0-dbgsym:arm64 | debug symbols for libnm0 |
| libnma-common | NetworkManager GUI library - translations |
| libnma0:arm64 | NetworkManager GUI library |
| libnorm1:arm64 | NACK-Oriented Reliable Multicast (NORM) library |
| libnotify4:arm64 | sends desktop notifications to a notification daemon |
| libnotmuch5 | thread-based email index, search and tagging (runtime) |
| libnpth0:arm64 | replacement for GNU Pth using system threads |
| libnsl-dev:arm64 | libnsl development files |
| libnsl2:arm64 | Public client interface for NIS(YP) and NIS+ |
| libnspr4:arm64 | NetScape Portable Runtime Library |
| libnss3:arm64 | Network Security Service libraries |
| libntfs-3g883 | read/write NTFS driver for FUSE (runtime library) |
| libntlm0:arm64 | NTLM authentication library |
| libnuma1:arm64 | Libraries for controlling NUMA policy |
| libnumber-compare-perl | module for performing numeric comparisons in Perl |
| libnumbertext-1.0-0:arm64 | Number to number name and money text conversion library |
| libnumbertext-data | Number to number name and money text conversion library -- data files |
| libobjc-10-dev:arm64 | Runtime library for GNU Objective-C applications (development files) |
| libobjc4:arm64 | Runtime library for GNU Objective-C applications |
| libobrender32v5 | rendering library for openbox themes |
| libobt2v5 | parsing library for openbox |
| libodbc1:arm64 | ODBC library for Unix |
| libodfgen-0.1-1:arm64 | library to generate ODF documents |
| libofa0:arm64 | library for acoustic fingerprinting |
| libogdi4.1 | Open Geographic Datastore Interface Library -- library |
| libogg0:arm64 | Ogg bitstream library |
| libomp-11-dev | LLVM OpenMP runtime - dev package |
| libomp-11-doc | LLVM OpenMP runtime - Documentation |
| libomp5-11:arm64 | LLVM OpenMP runtime |
| liboobs-1-5:arm64 | GObject based interface to system-tools-backends - shared library |
| libopenal-data | Software implementation of the OpenAL audio API (data files) |
| libopenal1:arm64 | Software implementation of the OpenAL audio API (shared library) |
| libopencore-amrnb0:arm64 | Adaptive Multi Rate speech codec - shared library |
| libopencore-amrwb0:arm64 | Adaptive Multi-Rate - Wideband speech codec - shared library |
| libopencv-calib3d-dev:arm64 | development files for libopencv-calib3d4.5 |
| libopencv-calib3d4.5:arm64 | computer vision Camera Calibration library |
| libopencv-contrib-dev:arm64 | development files for libopencv-contrib4.5 |
| libopencv-contrib4.5:arm64 | computer vision contrlib library |
| libopencv-core-dev:arm64 | development files for libopencv-core4.5 |
| libopencv-core4.5:arm64 | computer vision core library |
| libopencv-dev | development files for opencv |
| libopencv-dnn-dev:arm64 | development files for libopencv-dnn4.5 |
| libopencv-dnn4.5:arm64 | computer vision Deep neural network module |
| libopencv-features2d-dev:arm64 | development files for libopencv-features2d4.5 |
| libopencv-features2d4.5:arm64 | computer vision Feature Detection and Descriptor Extraction library |
| libopencv-flann-dev:arm64 | development files for libopencv-flann4.5 |
| libopencv-flann4.5:arm64 | computer vision Clustering and Search in Multi-Dimensional spaces library |
| libopencv-highgui-dev:arm64 | development files for libopencv-highgui4.5 |
| libopencv-highgui4.5:arm64 | computer vision High-level GUI and Media I/O library |
| libopencv-imgcodecs-dev:arm64 | development files for libopencv-imgcodecs4.5 |
| libopencv-imgcodecs4.5:arm64 | computer vision Image Codecs library |
| libopencv-imgproc-dev:arm64 | development files for libopencv-imgproc4.5 |
| libopencv-imgproc4.5:arm64 | computer vision Image Processing library |
| libopencv-ml-dev:arm64 | development files for libopencv-ml4.5 |
| libopencv-ml4.5:arm64 | computer vision Machine Learning library |
| libopencv-objdetect-dev:arm64 | development files for libopencv-objdetect4.5 |
| libopencv-objdetect4.5:arm64 | computer vision Object Detection library |
| libopencv-photo-dev:arm64 | development files for libopencv-photo4.5 |
| libopencv-photo4.5:arm64 | computer vision computational photography library |
| libopencv-shape-dev:arm64 | development files for libopencv-shape4.5 |
| libopencv-shape4.5:arm64 | computer vision shape descriptors and matchers library |
| libopencv-stitching-dev:arm64 | development files for libopencv-stitching4.5 |
| libopencv-stitching4.5:arm64 | computer vision image stitching library |
| libopencv-superres-dev:arm64 | development files for libopencv-superres4.5 |
| libopencv-superres4.5:arm64 | computer vision Super Resolution library |
| libopencv-video-dev:arm64 | development files for libopencv-video4.5 |
| libopencv-video4.5:arm64 | computer vision Video analysis library |
| libopencv-videoio-dev:arm64 | development files for libopencv-videoio4.5 |
| libopencv-videoio4.5:arm64 | computer vision Video I/O library |
| libopencv-videostab-dev:arm64 | development files for libopencv-videostab4.5 |
| libopencv-videostab4.5:arm64 | computer vision video stabilization library |
| libopencv-viz-dev:arm64 | development files for libopencv-viz4.5 |
| libopencv-viz4.5:arm64 | computer vision 3D data visualization library |
| libopenexr-dev | development files for the OpenEXR image library |
| libopenexr25:arm64 | runtime files for the OpenEXR image library |
| libopengl-dev:arm64 | Vendor neutral GL dispatch library -- OpenGL development files |
| libopengl0:arm64 | Vendor neutral GL dispatch library -- OpenGL support |
| libopenjp2-7:arm64 | JPEG 2000 image compression/decompression library |
| libopenmpt-modplug1:arm64 | module music library based on OpenMPT -- modplug compat library |
| libopenmpt0:arm64 | module music library based on OpenMPT -- shared library |
| libopenni2-0:arm64 | framework for sensor-based 'Natural Interaction' |
| libopts25:arm64 | automated option processing library based on autogen |
| libopus0:arm64 | Opus codec runtime library |
| liborc-0.4-0:arm64 | Library of Optimized Inner Loops Runtime Compiler |
| liborc-0.4-dev:arm64 | Library of Optimized Inner Loops Runtime Compiler (development headers) |
| liborc-0.4-dev-bin | Library of Optimized Inner Loops Runtime Compiler (development tools) |
| liborcus-0.16-0:arm64 | library for processing spreadsheet documents |
| liborcus-parser-0.16-0:arm64 | library for processing spreadsheet documents - parser library |
| libosinfo-1.0-0:arm64 | Library for managing information about operating systems and hypervisors |
| libp11-kit0:arm64 | library for loading and coordinating access to PKCS#11 modules - runtime |
| libpackage-stash-perl | module providing routines for manipulating stashes |
| libpackage-stash-xs-perl | Perl module providing routines for manipulating stashes (XS version) |
| libpackagekit-glib2-18:arm64 | Library for accessing PackageKit using GLib |
| libpagemaker-0.0-0:arm64 | Library for importing and converting PageMaker Documents |
| libpam-modules:arm64 | Pluggable Authentication Modules for PAM |
| libpam-modules-bin | Pluggable Authentication Modules for PAM - helper binaries |
| libpam-runtime | Runtime support for the PAM library |
| libpam-systemd:arm64 | system and service manager - PAM module |
| libpam0g:arm64 | Pluggable Authentication Modules library |
| libpango-1.0-0:arm64 | Layout and rendering of internationalized text |
| libpango1.0-dev:arm64 | Development files for the Pango |
| libpangocairo-1.0-0:arm64 | Layout and rendering of internationalized text |
| libpangoft2-1.0-0:arm64 | Layout and rendering of internationalized text |
| libpangomm-1.4-1v5:arm64 | C++ Wrapper for pango (shared libraries) |
| libpangoxft-1.0-0:arm64 | Layout and rendering of internationalized text |
| libpaper-utils | library for handling paper characteristics (utilities) |
| libpaper1:arm64 | library for handling paper characteristics |
| libparams-classify-perl | Perl module for argument type classification |
| libparams-util-perl | Perl extension for simple stand-alone param checking functions |
| libparted-fs-resize0:arm64 | disk partition manipulator - shared FS resizing library |
| libparted2:arm64 | disk partition manipulator - shared library |
| libpath-tiny-perl | file path utility |
| libpcap0.8:arm64 | system interface for user-level packet capture |
| libpci3:arm64 | PCI utilities (shared library) |
| libpciaccess-dev:arm64 | Generic PCI access library for X - development files |
| libpciaccess0:arm64 | Generic PCI access library for X |
| libpcre16-3:arm64 | Old Perl 5 Compatible Regular Expression Library - 16 bit runtime files |
| libpcre2-16-0:arm64 | New Perl Compatible Regular Expression Library - 16 bit runtime files |
| libpcre2-32-0:arm64 | New Perl Compatible Regular Expression Library - 32 bit runtime files |
| libpcre2-8-0:arm64 | New Perl Compatible Regular Expression Library- 8 bit runtime files |
| libpcre2-dev:arm64 | New Perl Compatible Regular Expression Library - development files |
| libpcre2-posix2:arm64 | New Perl Compatible Regular Expression Library - posix-compatible runtime files |
| libpcre3:arm64 | Old Perl 5 Compatible Regular Expression Library - runtime files |
| libpcre3-dev:arm64 | Old Perl 5 Compatible Regular Expression Library - development files |
| libpcre32-3:arm64 | Old Perl 5 Compatible Regular Expression Library - 32 bit runtime files |
| libpcrecpp0v5:arm64 | Old Perl 5 Compatible Regular Expression Library - C++ runtime files |
| libpcsclite1:arm64 | Middleware to access a smart card using PC/SC (library) |
| libpeas-1.0-0:arm64 | Application plugin library |
| libpeas-common | Application plugin library (common files) |
| libperl5.32:arm64 | shared Perl library |
| libperlio-gzip-perl | module providing a PerlIO layer to gzip/gunzip |
| libpfm4:arm64 | Library to program the performance monitoring events |
| libpgm-5.3-0:arm64 | OpenPGM shared library |
| libphonon4qt5-4:arm64 | multimedia framework from KDE using Qt 5 - core library |
| libphonon4qt5-data | multimedia framework from KDE using Qt 5 - core library data |
| libpipeline1:arm64 | Unix process pipeline manipulation library |
| libpixman-1-0:arm64 | pixel-manipulation library for X and cairo |
| libpixman-1-dev:arm64 | pixel-manipulation library for X and cairo (development files) |
| libpkcs11-helper1:arm64 | library that simplifies the interaction with PKCS#11 |
| libplacebo72:arm64 | GPU-accelerated video/image rendering primitives (shared library) |
| libplank-common | Library to build an elegant, simple, clean dock (shared files) |
| libplank1:arm64 | Library to build an elegant, simple, clean dock |
| libplist3:arm64 | Library for handling Apple binary and XML property lists |
| libpng-dev:arm64 | PNG library - development (version 1.6) |
| libpng16-16:arm64 | PNG library - runtime (version 1.6) |
| libpocketsphinx3:arm64 | Speech recognition tool - front-end library |
| libpolkit-agent-1-0:arm64 | PolicyKit Authentication Agent API |
| libpolkit-gobject-1-0:arm64 | PolicyKit Authorization API |
| libpolkit-qt5-1-1:arm64 | PolicyKit-qt5-1 library |
| libpoppler-glib8:arm64 | PDF rendering library (GLib-based shared library) |
| libpoppler102:arm64 | PDF rendering library |
| libpopt0:arm64 | lib for parsing cmdline parameters |
| libpostproc55:arm64 | FFmpeg library for post processing - runtime files |
| libpq-dev | header files for libpq5 (PostgreSQL library) |
| libpq5:arm64 | PostgreSQL C client library |
| libproc-processtable-perl | Perl library for accessing process table information |
| libprocps8:arm64 | library for accessing process information from /proc |
| libproj19:arm64 | Cartographic projection library |
| libprotobuf-lite23:arm64 | protocol buffers C++ library (lite version) |
| libprotobuf23:arm64 | protocol buffers C++ library |
| libproxy1v5:arm64 | automatic proxy configuration management library (shared) |
| libpseudo:arm64 | advanced tool for simulating superuser privileges |
| libpsl5:arm64 | Library for Public Suffix List (shared libraries) |
| libpthread-stubs0-dev:arm64 | pthread stubs not provided by native libc, development files |
| libpulse-mainloop-glib0:arm64 | PulseAudio client libraries (glib support) |
| libpulse0:arm64 | PulseAudio client libraries |
| libpulsedsp:arm64 | PulseAudio OSS pre-load library |
| libpython3-dbg:arm64 | debug build of the Python 3 Interpreter (version 3.9) |
| libpython3-stdlib:arm64 | interactive high-level object-oriented language (default python3 version) |
| libpython3.9:arm64 | Shared Python runtime library (version 3.9) |
| libpython3.9-dbg:arm64 | Debug Build of the Python Interpreter (version 3.9) |
| libpython3.9-minimal:arm64 | Minimal subset of the Python language (version 3.9) |
| libpython3.9-stdlib:arm64 | Interactive high-level object-oriented language (standard library, version 3.9) |
| libqhull8.0:arm64 | calculate convex hulls and related structures (shared library) |
| libqrcodegencpp1:arm64 | QR Code generator library in multiple languages - C++ version |
| libqscintilla2-qt5-15 | Qt5 port of the Scintilla source code editing widget |
| libqscintilla2-qt5-l10n | Scintilla source code editing widget for Qt5, translation files |
| libqt5concurrent5:arm64 | Qt 5 concurrent module |
| libqt5core5a:arm64 | Qt 5 core module |
| libqt5dbus5:arm64 | Qt 5 D-Bus module |
| libqt5designer5:arm64 | Qt 5 designer module |
| libqt5designercomponents5:arm64 | Qt 5 Designer components module |
| libqt5gui5:arm64 | Qt 5 GUI module |
| libqt5help5:arm64 | Qt 5 help module |
| libqt5multimedia5:arm64 | Qt 5 Multimedia module |
| libqt5multimedia5-plugins:arm64 | Qt 5 Multimedia module plugins |
| libqt5multimediagsttools5:arm64 | GStreamer tools for Qt 5 Multimedia module |
| libqt5multimediaquick5:arm64 | Qt 5 Multimedia Quick module |
| libqt5multimediawidgets5:arm64 | Qt 5 Multimedia Widgets module |
| libqt5network5:arm64 | Qt 5 network module |
| libqt5opengl5:arm64 | Qt 5 OpenGL module |
| libqt5opengl5-dev:arm64 | Qt 5 OpenGL library development files |
| libqt5positioning5:arm64 | Qt Positioning module |
| libqt5printsupport5:arm64 | Qt 5 print support module |
| libqt5qml5:arm64 | Qt 5 QML module |
| libqt5qmlmodels5:arm64 | Qt 5 QML Models library |
| libqt5qmlworkerscript5:arm64 | Qt 5 QML Worker Script library |
| libqt5quick5:arm64 | Qt 5 Quick library |
| libqt5quickwidgets5:arm64 | Qt 5 Quick Widgets library |
| libqt5script5:arm64 | Qt 5 script module |
| libqt5scripttools5:arm64 | Qt 5 script tools module |
| libqt5sensors5:arm64 | Qt Sensors module |
| libqt5sql5:arm64 | Qt 5 SQL module |
| libqt5sql5-sqlite:arm64 | Qt 5 SQLite 3 database driver |
| libqt5svg5:arm64 | Qt 5 SVG module |
| libqt5svg5-dev:arm64 | Qt 5 SVG module development files |
| libqt5test5:arm64 | Qt 5 test module |
| libqt5texttospeech5:arm64 | Speech library for Qt - libraries |
| libqt5waylandclient5:arm64 | QtWayland client library |
| libqt5waylandcompositor5:arm64 | QtWayland compositor library |
| libqt5webchannel5:arm64 | Web communication library for Qt |
| libqt5webkit5:arm64 | Web content engine library for Qt |
| libqt5widgets5:arm64 | Qt 5 widgets module |
| libqt5x11extras5:arm64 | Qt 5 X11 extras |
| libqt5xdg3:arm64 | Implementation of the XDG Specifications for Qt (shared lib) |
| libqt5xdgiconloader3:arm64 | Implementation of the XDG Iconloader for Qt (shared lib) |
| libqt5xml5:arm64 | Qt 5 XML module |
| libquvi-0.9-0.9.3:arm64 | library for parsing video download links (runtime libraries) |
| libquvi-scripts-0.9 | library for parsing video download links (Lua scripts) |
| libqxp-0.0-0 | library for reading and converting QuarkXPress files |
| librabbitmq4:arm64 | AMQP client library written in C |
| libraptor2-0:arm64 | Raptor 2 RDF syntax library |
| librasqal3:arm64 | Rasqal RDF query library |
| libraw1394-11:arm64 | library for direct access to IEEE 1394 bus (aka FireWire) |
| libraw1394-dev:arm64 | library for direct access to IEEE 1394 bus - development files |
| librdf0:arm64 | Redland Resource Description Framework (RDF) library |
| libre2-9:arm64 | efficient, principled regular expression library |
| libreadline8:arm64 | GNU readline and history libraries, run-time libraries |
| libreadonly-perl | facility for creating read-only scalars, arrays and hashes |
| libref-util-perl | set of utility functions for checking references |
| libref-util-xs-perl | XS implementation for Ref::Util |
| libresid-builder0c2a | SID chip emulation class based on resid |
| librest-0.7-0:arm64 | REST service access library |
| librevenge-0.0-0:arm64 | Base Library for writing document interface filters |
| librga-dev | Userspace interface to Rockchip RGA 2D accelerator |
| librga2 | Userspace interface to Rockchip RGA 2D accelerator |
| librga2-dbgsym | debug symbols for librga2 |
| librhash0:arm64 | shared library for hash functions computing |
| librhythmbox-core10:arm64 | support library for the rhythmbox music player |
| librockchip-mpp-dev | Media Process Platform |
| librockchip-mpp1 | Media Process Platform |
| librockchip-mpp1-dbgsym | debug symbols for librockchip-mpp1 |
| librockchip-vpu0 | Media Process Platform |
| librockchip-vpu0-dbgsym | debug symbols for librockchip-vpu0 |
| librole-tiny-perl | Perl module for minimalist role composition |
| librsvg2-2:arm64 | SAX-based renderer library for SVG files (runtime) |
| librsvg2-common:arm64 | SAX-based renderer library for SVG files (extra runtime) |
| librtmp1:arm64 | toolkit for RTMP streams (shared library) |
| librttopo1:arm64 | Tuscany Region topology library |
| librubberband2:arm64 | audio time-stretching and pitch-shifting library |
| libsamplerate0:arm64 | Audio sample rate conversion library |
| libsasl2-2:arm64 | Cyrus SASL - authentication abstraction library |
| libsasl2-modules-db:arm64 | Cyrus SASL - pluggable authentication modules (DB) |
| libsbc1:arm64 | Sub Band CODEC library - runtime |
| libsdl-image1.2:arm64 | Image loading library for Simple DirectMedia Layer 1.2, libraries |
| libsdl1.2debian:arm64 | Simple DirectMedia Layer |
| libsdl2-2.0-0:arm64 | Simple DirectMedia Layer |
| libseccomp2:arm64 | high level interface to Linux seccomp filter |
| libsecret-1-0:arm64 | Secret store |
| libsecret-common | Secret store (common files) |
| libselinux1:arm64 | SELinux runtime shared libraries |
| libselinux1-dev:arm64 | SELinux development headers |
| libsemanage-common | Common files for SELinux policy management libraries |
| libsemanage1:arm64 | SELinux policy management library |
| libsensors-config | lm-sensors configuration files |
| libsensors5:arm64 | library to read temperature/voltage/fan sensors |
| libsepol1:arm64 | SELinux library for manipulating binary security policies |
| libsepol1-dev:arm64 | SELinux binary policy manipulation library and development files |
| libserd-0-0:arm64 | lightweight RDF syntax library |
| libsereal-decoder-perl | fast, compact, powerful binary deserialization module |
| libsereal-encoder-perl | fast, compact, powerful binary serialization module |
| libshine3:arm64 | Fixed-point MP3 encoding library - runtime files |
| libshout3:arm64 | MP3/Ogg Vorbis broadcast streaming library |
| libsidplay1v5:arm64 | SID (MOS 6581) emulation library |
| libsidplay2 | SID (MOS 6581) emulation library |
| libsigc++-2.0-0v5:arm64 | type-safe Signal Framework for C++ - runtime |
| libsigsegv2:arm64 | Library for handling page faults in a portable way |
| libslang2:arm64 | S-Lang programming library - runtime version |
| libsm-dev:arm64 | X11 Session Management library (development headers) |
| libsm6:arm64 | X11 Session Management library |
| libsmartcols1:arm64 | smart column output alignment library |
| libsmbclient:arm64 | shared library for communication with SMB/CIFS servers |
| libsnappy1v5:arm64 | fast compression/decompression library |
| libsndfile1:arm64 | Library for reading/writing audio files |
| libsndio7.0:arm64 | Small audio and MIDI framework from OpenBSD, runtime libraries |
| libsocket++1:arm64 | lightweight convenience library to handle low level BSD sockets in C++ - libs |
| libsodium23:arm64 | Network communication, cryptography and signaturing library |
| libsord-0-0:arm64 | library for storing RDF data in memory |
| libsoundtouch1:arm64 | Sound stretching library |
| libsoup-gnome2.4-1:arm64 | HTTP library implementation in C -- GNOME support library |
| libsoup2.4-1:arm64 | HTTP library implementation in C -- Shared library |
| libsource-highlight-common | architecture-independent files for source highlighting library |
| libsource-highlight4v5 | source highlighting library |
| libsox-fmt-all:arm64 | All SoX format libraries |
| libsox-fmt-alsa:arm64 | SoX alsa format I/O library |
| libsox-fmt-ao:arm64 | SoX Libao format I/O library |
| libsox-fmt-base:arm64 | Minimal set of SoX format libraries |
| libsox-fmt-mp3:arm64 | SoX MP2 and MP3 format library |
| libsox-fmt-oss:arm64 | SoX OSS format I/O library |
| libsox-fmt-pulse:arm64 | SoX PulseAudio format I/O library |
| libsox3:arm64 | SoX library of audio effects and processing |
| libsoxr0:arm64 | High quality 1D sample-rate conversion library |
| libspandsp2:arm64 | Telephony signal processing library |
| libspatialaudio0:arm64 | library for ambisonic encoding and decoding (runtime files) |
| libspatialite7:arm64 | Geospatial extension for SQLite - libraries |
| libspeex1:arm64 | The Speex codec runtime library |
| libspeexdsp1:arm64 | The Speex extended runtime library |
| libsphinxbase3:arm64 | Speech recognition tool - shared library |
| libsqlite3-0:arm64 | SQLite 3 shared library |
| libsqlite3-dev:arm64 | SQLite 3 development files |
| libsratom-0-0:arm64 | library for serialising LV2 atoms to/from Turtle |
| libsrt1.4-gnutls:arm64 | Secure Reliable Transport UDP streaming library (GnuTLS flavour) |
| libsrtp2-1:arm64 | Secure RTP (SRTP) and UST Reference Implementations - shared library |
| libss2:arm64 | command-line interface parsing library |
| libssh-gcrypt-4:arm64 | tiny C SSH library (gcrypt flavor) |
| libssh2-1:arm64 | SSH2 client-side library |
| libssl1.1:arm64 | Secure Sockets Layer toolkit - shared libraries |
| libstaroffice-0.0-0:arm64 | Import filter library to import all StarOffice documents |
| libstartup-notification0:arm64 | library for program launch feedback (shared library) |
| libstdc++-10-dev:arm64 | GNU Standard C++ Library v3 (development files) |
| libstdc++-10-doc | GNU Standard C++ Library v3 (documentation files) |
| libstdc++6:arm64 | GNU Standard C++ Library v3 |
| libstemmer0d:arm64 | Snowball stemming algorithms for use in Information Retrieval |
| libstrictures-perl | Perl module to turn on strict and make all warnings fatal |
| libstrongswan | strongSwan utility and crypto library |
| libsub-exporter-perl | sophisticated exporter for custom-built routines |
| libsub-exporter-progressive-perl | module for using Sub::Exporter only if needed |
| libsub-identify-perl | module to retrieve names of code references |
| libsub-install-perl | module for installing subroutines into packages easily |
| libsub-name-perl | module for assigning a new name to referenced sub |
| libsub-quote-perl | helper modules for subroutines |
| libsuitesparseconfig5:arm64 | configuration routines for all SuiteSparse modules |
| libsuperlu5:arm64 | Direct solution of large, sparse systems of linear equations |
| libswresample-dev:arm64 | FFmpeg library for audio resampling, rematrixing etc. - development files |
| libswresample3:arm64 | FFmpeg library for audio resampling, rematrixing etc. - runtime files |
| libswscale-dev:arm64 | FFmpeg library for image scaling and various conversions - development files |
| libswscale5:arm64 | FFmpeg library for image scaling and various conversions - runtime files |
| libsynctex2:arm64 | TeX Live: SyncTeX parser library |
| libsystemd0:arm64 | systemd utility library |
| libsz2:arm64 | Adaptive Entropy Coding library - SZIP |
| libtag1v5:arm64 | audio meta-data library |
| libtag1v5-vanilla:arm64 | audio meta-data library - vanilla flavour |
| libtagc0:arm64 | audio meta-data library - C bindings |
| libtalloc2:arm64 | hierarchical pool based memory allocator |
| libtasn1-6:arm64 | Manage ASN.1 structures (runtime) |
| libtbb-dev:arm64 | parallelism library for C++ - development files |
| libtbb2:arm64 | parallelism library for C++ - runtime files |
| libtcl8.6:arm64 | Tcl (the Tool Command Language) v8.6 - run-time library files |
| libtdb1:arm64 | Trivial Database - shared library |
| libteamdctl0:arm64 | library for communication with `teamd` process |
| libtesseract4:arm64 | Tesseract OCR library |
| libtevent0:arm64 | talloc-based event loop library - shared library |
| libtext-glob-perl | Perl module for matching globbing patterns against text |
| libtext-levenshteinxs-perl | XS implementation of the Levenshtein edit distance |
| libtext-markdown-discount-perl:arm64 | Perl interface to Discount, an implementation of Markdown |
| libtext-xslate-perl | scalable template engine for Perl 5 (C/XS accelerated) |
| libthai-data | Data files for Thai language support library |
| libthai-dev:arm64 | Development files for Thai language support library |
| libthai0:arm64 | Thai language support library |
| libtheora0:arm64 | Theora Video Compression Codec |
| libtiff-dev:arm64 | Tag Image File Format library (TIFF), development files |
| libtiff5:arm64 | Tag Image File Format (TIFF) library |
| libtiffxx5:arm64 | Tag Image File Format (TIFF) library -- C++ interface |
| libtime-duration-perl | module for rounded or exact English expression of durations |
| libtime-moment-perl | Perl C/XS module representing date and time of day with UTC offset |
| libtimedate-perl | collection of modules to manipulate date/time information |
| libtinfo-dev:arm64 | transitional package for libncurses-dev |
| libtinfo6:arm64 | shared low-level terminfo library for terminal handling |
| libtirpc-common | transport-independent RPC library - common files |
| libtirpc-dev:arm64 | transport-independent RPC library - development files |
| libtirpc3:arm64 | transport-independent RPC library |
| libtk8.6:arm64 | Tk toolkit for Tcl and X11 v8.6 - run-time files |
| libtokyocabinet9:arm64 | Tokyo Cabinet Database Libraries [runtime] |
| libtool | Generic library support script |
| libtotem-plparser-common | Totem Playlist Parser library - common files |
| libtotem-plparser18:arm64 | Totem Playlist Parser library - runtime files |
| libtracker-control-2.0-0:arm64 | library to control/monitor tracker miners |
| libtracker-miner-2.0-0:arm64 | tracker data miner library |
| libtracker-sparql-2.0-0:arm64 | metadata database, indexer and search tool - library |
| libtry-tiny-perl | module providing minimalistic try/catch |
| libtsan0:arm64 | ThreadSanitizer -- a Valgrind-based detector of data races (runtime) |
| libtwolame0:arm64 | MPEG Audio Layer 2 encoding library |
| libtype-tiny-perl | tiny, yet Moo(se)-compatible type constraint |
| libtype-tiny-xs-perl | boost for some of Type::Tiny's built-in type constraints |
| libu2f-udev | Universal 2nd Factor (U2F) — transitional package |
| libubsan1:arm64 | UBSan -- undefined behaviour sanitizer (runtime) |
| libuchardet0:arm64 | universal charset detection library - shared library |
| libudev1:arm64 | libudev shared library |
| libudfread0:arm64 | UDF reader library |
| libudisks2-0:arm64 | GObject based library to access udisks2 |
| libuil4:arm64 | Motif - UIL (User Interface Language) shared library |
| libunarr-dev:arm64 | Decompression library for RAR, TAR, ZIP and 7z archives (devel) |
| libunarr1:arm64 | Decompression library for RAR, TAR, ZIP and 7z archives (runtime) |
| libunicode-utf8-perl | encoding and decoding of UTF-8 encoding form |
| libunistring2:arm64 | Unicode string library for C |
| libuno-cppu3 | LibreOffice UNO runtime environment -- CPPU public library |
| libuno-cppuhelpergcc3-3 | LibreOffice UNO runtime environment -- CPPU helper library |
| libuno-purpenvhelpergcc3-3 | LibreOffice UNO runtime environment -- "purpose environment" helper |
| libuno-sal3 | LibreOffice UNO runtime environment -- SAL public library |
| libuno-salhelpergcc3-3 | LibreOffice UNO runtime environment -- SAL helpers for C++ library |
| libunwind-dev:arm64 | library to determine the call-chain of a program - development |
| libunwind8:arm64 | library to determine the call-chain of a program - runtime |
| libupnp13:arm64 | Portable SDK for UPnP Devices, version 1.8 (shared library) |
| libupower-glib3:arm64 | abstraction for power management - shared library |
| liburi-perl | module to manipulate and access URI strings |
| liburiparser1:arm64 | URI parsing library compliant with RFC 3986 |
| libusb-1.0-0:arm64 | userspace USB programming library |
| libusbmuxd6:arm64 | USB multiplexor daemon for iPhone and iPod Touch devices - library |
| libutempter0:arm64 | privileged helper for utmp/wtmp updates (runtime) |
| libuuid1:arm64 | Universally Unique ID library |
| libuv1:arm64 | asynchronous event notification library - runtime library |
| libv4l-0:arm64 | Collection of video4linux support libraries |
| libv4l-0-dbgsym:arm64 | debug symbols for libv4l-0 |
| libv4l-dev:arm64 | Collection of video4linux support libraries (development files) |
| libv4l-rkmpp | A rockchip-mpp V4L2 wrapper plugin for chromium V4L2 VDA |
| libv4l-rkmpp-dbgsym | debug symbols for libv4l-rkmpp |
| libv4l2rds0:arm64 | Video4Linux Radio Data System (RDS) decoding library |
| libv4l2rds0-dbgsym:arm64 | debug symbols for libv4l2rds0 |
| libv4lconvert0:arm64 | Video4linux frame format conversion library |
| libv4lconvert0-dbgsym:arm64 | debug symbols for libv4lconvert0 |
| libva-drm2:arm64 | Video Acceleration (VA) API for Linux -- DRM runtime |
| libva-wayland2:arm64 | Video Acceleration (VA) API for Linux -- Wayland runtime |
| libva-x11-2:arm64 | Video Acceleration (VA) API for Linux -- X11 runtime |
| libva2:arm64 | Video Acceleration (VA) API for Linux -- runtime |
| libvariable-magic-perl | module to associate user-defined magic to variables from Perl |
| libvdpau1:arm64 | Video Decode and Presentation API for Unix (libraries) |
| libvidstab1.1:arm64 | video stabilization library (shared library) |
| libvisio-0.1-1:arm64 | library for parsing the visio file structure |
| libvisual-0.4-0:arm64 | audio visualization framework |
| libvlc5:arm64 | multimedia player and streamer library |
| libvlccore9:arm64 | base library for VLC and its modules |
| libvo-aacenc0:arm64 | VisualOn AAC encoder library |
| libvo-amrwbenc0:arm64 | VisualOn AMR-WB encoder library |
| libvorbis0a:arm64 | decoder library for Vorbis General Audio Compression Codec |
| libvorbisenc2:arm64 | encoder library for Vorbis General Audio Compression Codec |
| libvorbisfile3:arm64 | high-level API for Vorbis General Audio Compression Codec |
| libvpx6:arm64 | VP8 and VP9 video codec (shared library) |
| libvte-2.91-0:arm64 | Terminal emulator widget for GTK+ 3.0 - runtime files |
| libvte-2.91-common | Terminal emulator widget for GTK+ 3.0 - common files |
| libvtk9 | VTK libraries |
| libvulkan-dev:arm64 | Vulkan loader library -- development files |
| libvulkan1:arm64 | Vulkan loader library |
| libwacom-common | Wacom model feature query library (common files) |
| libwacom2:arm64 | Wacom model feature query library |
| libwavpack1:arm64 | audio codec (lossy and lossless) - library |
| libwayland-bin | wayland compositor infrastructure - binary utilities |
| libwayland-client0:arm64 | wayland compositor infrastructure - client library |
| libwayland-cursor0:arm64 | wayland compositor infrastructure - cursor library |
| libwayland-dev:arm64 | wayland compositor infrastructure - development files |
| libwayland-egl1:arm64 | wayland compositor infrastructure - EGL library |
| libwayland-server0:arm64 | wayland compositor infrastructure - server library |
| libwbclient0:arm64 | Samba winbind client library |
| libwebp6:arm64 | Lossy compression of digital photographic images. |
| libwebpdemux2:arm64 | Lossy compression of digital photographic images. |
| libwebpmux3:arm64 | Lossy compression of digital photographic images. |
| libwebrtc-audio-processing1:arm64 | AudioProcessing module from the WebRTC project. |
| libwildmidi2:arm64 | software MIDI player library |
| libwmf0.2-7:arm64 | Windows metafile conversion library |
| libwnck-3-0:arm64 | Window Navigator Construction Kit - runtime files |
| libwnck-3-common | Window Navigator Construction Kit - common files |
| libwoff1:arm64 | library for converting fonts to WOFF 2.0 |
| libwpa-client-dev:arm64 | development files for WPA/WPA2 client support (IEEE 802.11i) |
| libwpd-0.10-10:arm64 | Library for handling WordPerfect documents (shared library) |
| libwpe-1.0-1:arm64 | Base library for the WPE WebKit port |
| libwpebackend-fdo-1.0-1:arm64 | WPE backend for FreeDesktop.org |
| libwpewebkit-1.0-3:arm64 | Web content engine for embedded devices |
| libwpg-0.3-3:arm64 | WordPerfect graphics import/convert library (shared library) |
| libwps-0.4-4:arm64 | Works text file format import filter library (shared library) |
| libwrap0:arm64 | Wietse Venema's TCP wrappers library |
| libwww-perl | simple and consistent interface to the world-wide web |
| libwww-robotrules-perl | database of robots.txt-derived permissions |
| libx11-6:arm64 | X11 client-side library |
| libx11-data | X11 client-side library |
| libx11-dev:arm64 | X11 client-side library (development headers) |
| libx11-xcb-dev:arm64 | Xlib/XCB interface library (development headers) |
| libx11-xcb1:arm64 | Xlib/XCB interface library |
| libx264-160:arm64 | x264 video coding library |
| libx265-192:arm64 | H.265/HEVC video stream encoder (shared library) |
| libxapian30:arm64 | Search engine library |
| libxau-dev:arm64 | X11 authorisation library (development headers) |
| libxau6:arm64 | X11 authorisation library |
| libxaw7:arm64 | X11 Athena Widget library |
| libxcb-dri2-0:arm64 | X C Binding, dri2 extension |
| libxcb-dri3-0:arm64 | X C Binding, dri3 extension |
| libxcb-glx0:arm64 | X C Binding, glx extension |
| libxcb-icccm4:arm64 | utility libraries for X C Binding -- icccm |
| libxcb-image0:arm64 | utility libraries for X C Binding -- image |
| libxcb-keysyms1:arm64 | utility libraries for X C Binding -- keysyms |
| libxcb-present0:arm64 | X C Binding, present extension |
| libxcb-randr0:arm64 | X C Binding, randr extension |
| libxcb-render-util0:arm64 | utility libraries for X C Binding -- render-util |
| libxcb-render0:arm64 | X C Binding, render extension |
| libxcb-render0-dev:arm64 | X C Binding, render extension, development files |
| libxcb-res0:arm64 | X C Binding, res extension |
| libxcb-shape0:arm64 | X C Binding, shape extension |
| libxcb-shm0:arm64 | X C Binding, shm extension |
| libxcb-shm0-dev:arm64 | X C Binding, shm extension, development files |
| libxcb-sync1:arm64 | X C Binding, sync extension |
| libxcb-util1:arm64 | utility libraries for X C Binding -- atom, aux and event |
| libxcb-xfixes0:arm64 | X C Binding, xfixes extension |
| libxcb-xinerama0:arm64 | X C Binding, xinerama extension |
| libxcb-xinput0:arm64 | X C Binding, xinput extension |
| libxcb-xkb1:arm64 | X C Binding, XKEYBOARD extension |
| libxcb-xv0:arm64 | X C Binding, xv extension |
| libxcb1:arm64 | X C Binding |
| libxcb1-dev:arm64 | X C Binding, development files |
| libxcomposite-dev:arm64 | X11 Composite extension library (development headers) |
| libxcomposite1:arm64 | X11 Composite extension library |
| libxcursor-dev:arm64 | X cursor management library (development files) |
| libxcursor1:arm64 | X cursor management library |
| libxdamage-dev:arm64 | X11 damaged region extension library (development headers) |
| libxdamage1:arm64 | X11 damaged region extension library |
| libxdmcp-dev:arm64 | X11 authorisation library (development headers) |
| libxdmcp6:arm64 | X11 Display Manager Control Protocol library |
| libxdo3:arm64 | library for simulating (generating) X11 keyboard/mouse input events |
| libxerces-c3.2:arm64 | validating XML parser library for C++ |
| libxext-dev:arm64 | X11 miscellaneous extensions library (development headers) |
| libxext6:arm64 | X11 miscellaneous extension library |
| libxfce4panel-2.0-4 | Xfce4 panel library (GTK3 variant) |
| libxfce4ui-2-0:arm64 | widget library for Xfce - Gtk+3 variant |
| libxfce4ui-common | common files for libxfce4ui |
| libxfce4ui-utils | Utility files for libxfce4ui |
| libxfce4util-common | common files for libxfce4util |
| libxfce4util-dev:arm64 | Development files for libxfce4util7 |
| libxfce4util7:arm64 | Utility functions library for Xfce4 |
| libxfconf-0-3:arm64 | Client library for Xfce4 configure interface |
| libxfixes-dev:arm64 | X11 miscellaneous 'fixes' extension library (development headers) |
| libxfixes3:arm64 | X11 miscellaneous 'fixes' extension library |
| libxfont-dev | X11 font rasterisation library (development headers) |
| libxfont2:arm64 | X11 font rasterisation library |
| libxft-dev:arm64 | FreeType-based font drawing library for X (development files) |
| libxft2:arm64 | FreeType-based font drawing library for X |
| libxi-dev:arm64 | X11 Input extension library (development headers) |
| libxi6:arm64 | X11 Input extension library |
| libxinerama-dev:arm64 | X11 Xinerama extension library (development headers) |
| libxinerama1:arm64 | X11 Xinerama extension library |
| libxkbcommon-dev:arm64 | library interface to the XKB compiler - development files |
| libxkbcommon-x11-0:arm64 | library to create keymaps with the XKB X11 protocol |
| libxkbcommon0:arm64 | library interface to the XKB compiler - shared library |
| libxkbfile-dev:arm64 | X11 keyboard file manipulation library (development headers) |
| libxkbfile1:arm64 | X11 keyboard file manipulation library |
| libxkbregistry0:arm64 | library to query available RMLVO |
| libxklavier16:arm64 | X Keyboard Extension high-level API |
| libxm4:arm64 | Motif - X/Motif shared library |
| libxml-libxml-perl | Perl interface to the libxml2 library |
| libxml-namespacesupport-perl | Perl module for supporting simple generic namespaces |
| libxml-parser-perl:arm64 | Perl module for parsing XML files |
| libxml-sax-base-perl | base class for SAX drivers and filters |
| libxml-sax-expat-perl | Perl module for a SAX2 driver for Expat (XML::Parser) |
| libxml-sax-expatxs-perl | Perl SAX 2 XS extension to Expat parser |
| libxml-sax-perl | Perl module for using and building Perl SAX2 XML processors |
| libxml-twig-perl | Perl module for processing huge XML documents in tree mode |
| libxml2:arm64 | GNOME XML library |
| libxml2-dev:arm64 | Development files for the GNOME XML library |
| libxml2-utils | XML utilities |
| libxmlsec1:arm64 | XML security library |
| libxmlsec1-nss:arm64 | Nss engine for the XML security library |
| libxmu-dev:arm64 | X11 miscellaneous utility library (development headers) |
| libxmu-headers | X11 miscellaneous utility library headers |
| libxmu6:arm64 | X11 miscellaneous utility library |
| libxmuu1:arm64 | X11 miscellaneous micro-utility library |
| libxnvctrl0:arm64 | NV-CONTROL X extension (runtime library) |
| libxpm4:arm64 | X11 pixmap library |
| libxpresent1:arm64 | X11 Present extension library |
| libxrandr-dev:arm64 | X11 RandR extension library (development headers) |
| libxrandr2:arm64 | X11 RandR extension library |
| libxrender-dev:arm64 | X Rendering Extension client library (development files) |
| libxrender1:arm64 | X Rendering Extension client library |
| libxres1:arm64 | X11 Resource extension library |
| libxshmfence1:arm64 | X shared memory fences - shared library |
| libxslt1.1:arm64 | XSLT 1.0 processing library - runtime library |
| libxss1:arm64 | X11 Screen Saver extension library |
| libxt-dev:arm64 | X11 toolkit intrinsics library (development headers) |
| libxt6:arm64 | X11 toolkit intrinsics library |
| libxtables12:arm64 | netfilter xtables library |
| libxtst-dev:arm64 | X11 Record extension library (development headers) |
| libxtst6:arm64 | X11 Testing -- Record extension library |
| libxv1:arm64 | X11 Video extension library |
| libxvidcore4:arm64 | Open source MPEG-4 video codec (library) |
| libxxf86dga1:arm64 | X11 Direct Graphics Access extension library |
| libxxf86vm1:arm64 | X11 XFree86 video mode extension library |
| libxxhash0:arm64 | shared library for xxhash |
| libyajl2:arm64 | Yet Another JSON Library |
| libyaml-0-2:arm64 | Fast YAML 1.1 parser and emitter library |
| libyaml-libyaml-perl | Perl interface to libyaml, a YAML implementation |
| libz3-4:arm64 | theorem prover from Microsoft Research - runtime libraries |
| libz3-dev:arm64 | theorem prover from Microsoft Research - development files |
| libzbar0:arm64 | QR code / bar code scanner and decoder (library) |
| libzeitgeist-2.0-0:arm64 | library to access Zeitgeist - shared library |
| libzmf-0.0-0:arm64 | Zoner Draw/Zebra file reading/converting library |
| libzmq5:arm64 | lightweight messaging kernel (shared library) |
| libzstd1:arm64 | fast lossless compression algorithm |
| libzvbi-common | Vertical Blanking Interval decoder (VBI) - common files |
| libzvbi0:arm64 | Vertical Blanking Interval decoder (VBI) - runtime files |
| lightdm-gtk-greeter | simple display manager (GTK+ greeter) |
| lightdm-gtk-greeter-settings | settings editor for the LightDM GTK+ Greeter |
| lintian | Debian package checker |
| linux-base | Linux image base package |
| linux-libc-dev:arm64 | Linux support headers for userspace development |
| llvm-11 | Modular compiler and toolchain technologies |
| llvm-11-dev | Modular compiler and toolchain technologies, libraries and headers |
| llvm-11-doc | Modular compiler and toolchain technologies, documentation |
| llvm-11-runtime | Modular compiler and toolchain technologies, IR interpreter |
| llvm-11-tools | Modular compiler and toolchain technologies, tools |
| llvm-13 | Modular compiler and toolchain technologies |
| llvm-13-dev | Modular compiler and toolchain technologies, libraries and headers |
| llvm-13-doc | Modular compiler and toolchain technologies, documentation |
| llvm-13-linker-tools | Modular compiler and toolchain technologies - Plugins |
| llvm-13-runtime | Modular compiler and toolchain technologies, IR interpreter |
| llvm-13-tools | Modular compiler and toolchain technologies, tools |
| llvm-9 | Modular compiler and toolchain technologies |
| llvm-9-dev | Modular compiler and toolchain technologies, libraries and headers |
| llvm-9-doc | Modular compiler and toolchain technologies, documentation |
| llvm-9-runtime | Modular compiler and toolchain technologies, IR interpreter |
| llvm-9-tools | Modular compiler and toolchain technologies, tools |
| lm-sensors | utilities to read temperature/voltage/fan sensors |
| locales | GNU C Library: National Language (locale) data [support] |
| locate | maintain and query an index of a directory tree |
| login | system login tools |
| logrotate | Log rotation utility |
| logsave | save the output of a command in a log file |
| lp-solve | Solve (mixed integer) linear programming problems |
| lsb-base | Linux Standard Base init script functionality |
| lsb-release | Linux Standard Base version reporting utility |
| lsof | utility to list open files |
| lua-bitop:arm64 | fast bit manipulation library for the Lua language |
| lua-expat:arm64 | libexpat bindings for the Lua language |
| lua-json | JSON decoder/encoder for Lua |
| lua-lpeg:arm64 | LPeg library for the Lua language |
| lua-socket:arm64 | TCP/UDP socket library for the Lua language |
| lximage-qt | Image viewer for LXQt |
| lxqt-qtplugin:arm64 | LXQt system integration plugin for Qt |
| lxqt-sudo | Graphical QT frontend for plain sudo |
| lxqt-sudo-l10n | Language package for lxqt-sudo |
| lynx | classic non-graphical (text-mode) web browser |
| lynx-common | shared files for lynx package |
| lzip | lossless data compressor based on the LZMA algorithm |
| lzop | fast compression program |
| m4 | macro processing language |
| make | utility for directing compilation |
| makedev | creates device files in /dev |
| man-db | tools for reading manual pages |
| manpages | Manual pages about using a GNU/Linux system |
| manpages-dev | Manual pages about using GNU/Linux for development |
| mariadb-common | MariaDB common configuration files |
| mawk | Pattern scanning and text processing language |
| media-player-info | Media player identification files |
| media-types | List of standard media types and their usual file extension |
| menu | generates programs menu for all menu-aware applications |
| mesa-common-dev:arm64 | Developer documentation for Mesa |
| mesa-utils | Miscellaneous Mesa GL utilities |
| min | A web browser with smarter search, improved tab management, and built-in ad blocking. Includes full-text history search, instant answers from DuckDuckGo, the ability to split tabs into groups, and more. |
| mlocate | quickly find files on the filesystem based on their name |
| mount | tools for mounting and manipulating filesystems |
| mpop | POP3 mail retriever |
| msmtp | light SMTP client with support for server profiles |
| mysql-common | MySQL database common files, e.g. /etc/mysql/my.cnf |
| nano | small, friendly text editor inspired by Pico |
| ncal | display a calendar and the date of Easter |
| ncurses-base | basic terminal type definitions |
| ncurses-bin | terminal-related programs and man pages |
| ncurses-doc | developer's guide and documentation for ncurses |
| neofetch | Shows Linux System Information with Distribution Logo |
| neomutt | command line mail reader based on Mutt, with added features |
| net-tools | NET-3 networking toolkit |
| netbase | Basic TCP/IP networking system |
| network-manager | network management framework (daemon and userspace tools) |
| network-manager-config-connectivity-debian | NetworkManager configuration to enable connectivity checking |
| network-manager-dbgsym | debug symbols for network-manager |
| network-manager-dev | network management framework (development files) |
| network-manager-gnome | network management framework (GNOME frontend) |
| network-manager-l2tp | network management framework (L2TP plugin core) |
| network-manager-openvpn | network management framework (OpenVPN plugin core) |
| network-manager-pptp | network management framework (PPTP plugin core) |
| network-manager-strongswan | network management framework (strongSwan plugin) |
| network-manager-vpnc | network management framework (VPNC plugin core) |
| nginx-common | small, powerful, scalable web/proxy server - common files |
| nginx-extras | nginx web/proxy server (extended version) |
| nightpdf | Dark Mode PDF reader |
| nocache | bypass/minimize file system caching for a program |
| nodm | automatic display manager |
| notification-daemon | daemon for displaying passive pop-up notifications |
| notmuch | thread-based email index, search and tagging |
| ntfs-3g | read/write NTFS driver for FUSE |
| ntp | Network Time Protocol daemon and utility programs |
| ntpdate | client for setting system time from NTP servers (deprecated) |
| obconf | preferences manager for Openbox window manager |
| ocl-icd-libopencl1:arm64 | Generic OpenCL ICD Loader |
| odbcinst | Helper program for accessing odbc ini files |
| odbcinst1debian2:arm64 | Support library for accessing odbc ini files |
| onlyoffice-documentserver | Online editors for text documents, spreadsheets, and presentations |
| openssh-client | secure shell (SSH) client, for secure access to remote machines |
| openssh-server | secure shell (SSH) server, for secure access from remote machines |
| openssh-sftp-server | secure shell (SSH) sftp server module, for SFTP access from remote machines |
| openssl | Secure Sockets Layer toolkit - cryptographic utility |
| openvpn | virtual private network daemon |
| osinfo-db | Operating system database files |
| p7zip | 7zr file archiver with high compression ratio |
| p7zip-full | 7z and 7za file archivers with high compression ratio |
| packagekit | Provides a package management service |
| packagekit-tools | Provides PackageKit command-line tools |
| pango1.0-tools | Development utilities for Pango |
| papirus-icon-theme | Papirus open source icon theme for Linux |
| parole | media player based on GStreamer framework |
| parole-dev | development files for Parole media player |
| parted | disk partition manipulator |
| pass | lightweight directory-based password manager |
| passwd | change and administer password and group data |
| patch | Apply a diff file to an original |
| patchutils | Utilities to work with patches |
| pavucontrol | PulseAudio Volume Control |
| pci.ids | PCI ID Repository |
| pciutils | PCI utilities |
| pcmanfm-qt | extremely fast and lightweight file and desktop icon manager |
| pcmanfm-qt-l10n | Language package for pcmanfm-qt |
| perl | Larry Wall's Practical Extraction and Report Language |
| perl-base | minimal Perl system |
| perl-modules-5.32 | Core Perl modules |
| perl-openssl-defaults:arm64 | version compatibility baseline for Perl OpenSSL packages |
| phonon4qt5:arm64 | multimedia framework from KDE using Qt 5 - metapackage |
| phonon4qt5-backend-vlc:arm64 | Phonon4Qt5 VLC backend |
| pinentry-curses | curses-based PIN or pass-phrase entry dialog for GnuPG |
| pkg-config | manage compile and link flags for libraries |
| plank | Elegant, simple, clean dock |
| pm-utils | utilities and scripts for power management |
| policykit-1 | framework for managing administrative policies and privileges |
| policykit-1-gnome | authentication agent for PolicyKit |
| poppler-data | encoding data for the poppler PDF rendering library |
| poppler-utils | PDF utilities (based on Poppler) |
| powerdebug | tool to display regulator, sensor and clock information |
| powermgmt-base | common utils for power management |
| powertop | diagnose issues with power consumption and management |
| ppp | Point-to-Point Protocol (PPP) - daemon |
| pptp-linux | Point-to-Point Tunneling Protocol (PPTP) Client |
| procps | /proc file system utilities |
| proj-data | Cartographic projection filter and library (datum package) |
| pseudo | advanced tool for simulating superuser privileges |
| psmisc | utilities that use the proc file system |
| pulseaudio | PulseAudio sound server |
| pulseaudio-module-bluetooth | Bluetooth module for PulseAudio sound server |
| pulseaudio-utils | Command line tools for the PulseAudio sound server |
| python-apt-common | Python interface to libapt-pkg (locales) |
| python-dbus-doc | Documentation for the D-Bus Python interface |
| python-llfuse-doc | Python bindings for the low-level FUSE API (documentation) |
| python-pexpect-doc | Python module for automating interactive applications (documentation) |
| python-psutil-doc | module providing convenience functions for managing processes (doc) |
| python-pygments-doc | documentation for the Pygments |
| python3 | interactive high-level object-oriented language (default python3 version) |
| python3-appdirs | determining appropriate platform-specific directories (Python 3) |
| python3-apscheduler | In-process task scheduler with Cron-like capabilities |
| python3-apt | Python 3 interface to libapt-pkg |
| python3-bcrypt | password hashing library for Python 3 |
| python3-cairo:arm64 | Python3 bindings for the Cairo vector graphics library |
| python3-certifi | root certificates for validating SSL certs and verifying TLS hosts (python3) |
| python3-cffi-backend:arm64 | Foreign Function Interface for Python 3 calling C code - runtime |
| python3-chardet | universal character encoding detector for Python3 |
| python3-cryptography | Python library exposing cryptographic recipes and primitives (Python 3) |
| python3-cups:arm64 | Python3 bindings for CUPS |
| python3-cupshelpers | Python utility modules around the CUPS printing system |
| python3-dateutil | powerful extensions to the standard Python 3 datetime module |
| python3-dbg | debug build of the Python 3 Interpreter (version 3.9) |
| python3-dbus | simple interprocess messaging system (Python 3 interface) |
| python3-dbus-dbg | debug build of the D-Bus Python 3 interface |
| python3-debian | Python 3 modules to work with Debian-related data formats |
| python3-dialog | Python module for making simple terminal-based user interfaces |
| python3-distro | Linux OS platform information API |
| python3-distutils | distutils package for Python 3.x |
| python3-doc | documentation for the high-level object-oriented language Python 3 |
| python3-gi | Python 3 bindings for gobject-introspection libraries |
| python3-gi-cairo | Python 3 Cairo bindings for the GObject library |
| python3-idna | Python IDNA2008 (RFC 5891) handling (Python 3) |
| python3-jeepney | pure Python D-Bus interface |
| python3-ldb | Python 3 bindings for LDB |
| python3-lib2to3 | Interactive high-level object-oriented language (lib2to3) |
| python3-llfuse:arm64 | Python 3 bindings for the low-level FUSE API |
| python3-minimal | minimal subset of the Python language (default python3 version) |
| python3-nacl | Python bindings to libsodium (Python 3) |
| python3-paramiko | Make ssh v2 connections (Python 3) |
| python3-peewee | Simple ORM for PostgreSQL, MySQL and SQLite (Python 3) |
| python3-pexpect | Python 3 module for automating interactive applications |
| python3-pkg-resources | Package Discovery and Resource Access using pkg_resources |
| python3-psutil | module providing convenience functions for managing processes (Python3) |
| python3-ptyprocess | Run a subprocess in a pseudo terminal from Python 3 |
| python3-py7zr | pure Python 7-zip library |
| python3-pycryptodome | cryptographic Python library (Python 3) |
| python3-pygments | syntax highlighting package written in Python 3 |
| python3-pyqt5 | Python 3 bindings for Qt5 |
| python3-pyqt5.qsci | Python 3 bindings for QScintilla 2 with Qt 5 |
| python3-pyqt5.sip | runtime module for Python extensions using SIP |
| python3-requests | elegant and simple HTTP library for Python3, built for human beings |
| python3-secretstorage | Python module for storing secrets - Python 3.x version |
| python3-six | Python 2 and 3 compatibility library (Python 3 interface) |
| python3-smbc | Python 3 bindings for the Samba client library |
| python3-talloc:arm64 | hierarchical pool based memory allocator - Python3 bindings |
| python3-texttable | Module for creating simple ASCII tables — python3 |
| python3-tz | Python3 version of the Olson timezone database |
| python3-tzlocal | tzinfo object for the local timezone |
| python3-urllib3 | HTTP library with thread-safe connection pooling for Python3 |
| python3-yaml | YAML parser and emitter for Python3 |
| python3.9 | Interactive high-level object-oriented language (version 3.9) |
| python3.9-dbg | Debug Build of the Python Interpreter (version 3.9) |
| python3.9-doc | Documentation for the high-level object-oriented language Python (v3.9) |
| python3.9-minimal | Minimal subset of the Python language (version 3.9) |
| qdoc-qt5 | Qt 5 qdoc tool |
| qhelpgenerator-qt5 | Qt 5 qhelpgenerator tool |
| qml-module-qt-labs-folderlistmodel:arm64 | Qt 5 folderlistmodel QML module |
| qml-module-qtmultimedia:arm64 | Qt 5 Multimedia QML module |
| qml-module-qtquick2:arm64 | Qt 5 Qt Quick 2 QML module |
| qt3d5-doc | Qt 3D documentation |
| qt5-assistant | Qt 5 Assistant |
| qt5-doc | Qt 5 API Documentation |
| qt5-qmake:arm64 | Qt 5 qmake Makefile generator tool |
| qt5-qmake-bin | Qt 5 qmake Makefile generator tool — binary file |
| qtattributionsscanner-qt5 | Qt 5 qtattributionsscanner tool |
| qtbase5-dev:arm64 | Qt 5 base development files |
| qtbase5-dev-tools | Qt 5 base development programs |
| qtbase5-doc | Qt 5 base documentation |
| qtcharts5-doc | Qt charts QCH documentation |
| qtchooser | Wrapper to select between Qt development binary versions |
| qtconnectivity5-doc | Qt 5 Connectivity documentation |
| qtdatavisualization5-doc | Qt 5 Data Visualization documentation |
| qtdeclarative5-doc | Qt 5 declarative documentation |
| qtgraphicaleffects5-doc | Qt 5 graphical effects documentation |
| qtlocation5-doc | Qt 5 Location and Positioning QCH documentation |
| qtmultimedia5-doc | Qt 5 multimedia documentation |
| qtmultimedia5-examples:arm64 | Examples for Qt 5 Multimedia module |
| qtnetworkauth5-doc | online account access for Qt apps - documentation |
| qtquickcontrols2-5-doc | Qt 5 Quick Controls 2 documentation |
| qtquickcontrols5-doc | Qt 5 Quick Controls documentation |
| qtscript5-dev:arm64 | Qt 5 script development files |
| qtscript5-doc | Qt 5 script documentation |
| qtscxml5-doc | Qt SCXML QCH documentation |
| qtsensors5-doc | Qt 5 Sensors documentation |
| qtserialbus5-doc | Qt serialbus serial bus access QCH documentation |
| qtserialport5-doc | Qt 5 serial port documentation |
| qtsvg5-doc | Qt 5 SVG documentation |
| qttools5-dev-tools | Qt 5 development tools |
| qttools5-doc | Qt 5 tools documentation |
| qttranslations5-l10n | translations for Qt 5 |
| qtvirtualkeyboard5-doc | Qt 5 Virtual Keyboard documentation |
| qtwayland5:arm64 | QtWayland platform plugin |
| qtwayland5-doc | Qt 5 Wayland Compositor documentation |
| qtwebchannel5-doc | Web communication library for Qt - Documentation |
| qtwebengine5-doc | Qt 5 webengine documentation |
| qtwebsockets5-doc | Qt 5 Web Sockets documentation |
| qtwebview5-doc | display web content in a QML application - Documentation |
| qtx11extras5-doc | Qt 5 X11 extras documentation |
| qtxmlpatterns5-doc | Qt 5 XML patterns documentation |
| qv4l2 | Test bench application for video4linux devices |
| qv4l2-dbgsym | debug symbols for qv4l2 |
| raspi-firmware | Raspberry Pi family GPU firmware and bootloaders |
| ratmenu | Creates X menus from the shell |
| ratpoison | keyboard-only window manager |
| rcconf | Debian Runlevel configuration tool |
| read-edid | hardware information-gathering tool for VESA PnP monitors |
| readline-common | GNU readline and history libraries, common files |
| resolvconf | name server information handler |
| rfkill | tool for enabling and disabling wireless devices |
| rhythmbox | music player and organizer for GNOME |
| rhythmbox-data | data files for rhythmbox |
| rktoolkit:arm64 | some small tool used in Rockchip SDK |
| rktoolkit-dbgsym:arm64 | debug symbols for rktoolkit |
| rkwifibt-broadcom-firmware | include the rkwifibt broadcom firmware for rockchip linux |
| rkwifibt-dev-tools | include the rkwifibt broadcom tools for rockchip linux |
| rkwifibt-dev-tools-dbgsym | debug symbols for rkwifibt-dev-tools |
| rkwifibt-realtek-firmware | include the rkwifibt realtek firmware for rockchip linux |
| rockchip-mpp-demos | Media Process Platform Demos |
| rockchip-mpp-demos-dbgsym | debug symbols for rockchip-mpp-demos |
| rsyslog | reliable system and kernel logging daemon |
| runc | Open Container Project - runtime |
| runit-helper | dh-runit implementation detail |
| samba-libs:arm64 | Samba core libraries |
| sed | GNU stream editor for filtering/transforming text |
| sensible-utils | Utilities for sensible alternative selection |
| shared-mime-info | FreeDesktop.org shared MIME database and spec |
| sound-theme-freedesktop | freedesktop.org sound theme |
| sox | Swiss army knife of sound processing |
| sphinx-rtd-theme-common | sphinx theme from readthedocs.org (common files) |
| ssh-import-id | securely retrieve an SSH public key and install it locally |
| startpar | run processes in parallel and multiplex their output |
| strace | System call tracer |
| stress | tool to impose load on and stress test a computer system |
| strongswan | IPsec VPN solution metapackage |
| strongswan-charon | strongSwan Internet Key Exchange daemon |
| strongswan-libcharon | strongSwan charon library |
| strongswan-nm | strongSwan plugin to interact with NetworkManager |
| strongswan-starter | strongSwan daemon starter and configuration file parser |
| suckless-tools | simple commands for minimalistic window managers |
| sudo | Provide limited super user privileges to specific users |
| synaptic | Graphical package manager |
| system-config-printer | graphical interface to configure the printing system |
| system-config-printer-common | backend and the translation files for system-config-printer |
| system-config-printer-udev | Utilities to detect and configure printers automatically |
| system-tools-backends | System Tools to manage computer configuration -- scripts |
| systemd | system and service manager |
| systemd-sysv | system and service manager - SysV links |
| sysv-rc | System-V-like runlevel change mechanism |
| sysvinit-utils | System-V-like utilities |
| t1utils | Collection of simple Type 1 font manipulation programs |
| tar | GNU version of the tar archiving utility |
| task-desktop | Debian desktop environment |
| tasksel | tool for selecting tasks for installation on Debian systems |
| tasksel-data | official tasks used for installation of Debian systems |
| tcc | small ANSI C compiler |
| thorium-browser | The web browser from Alex313031 |
| timgm6mb-soundfont | TimGM6mb SoundFont from MuseScore 1.3 |
| tini | tiny but valid init for containers |
| trace-cmd | Utility for retrieving and analyzing function tracing in the kernel |
| tracker | metadata database, indexer and search tool |
| tracker-extract | metadata database, indexer and search tool - metadata extractors |
| tracker-miner-fs | metadata database, indexer and search tool - filesystem indexer |
| tree | displays an indented directory tree, in color |
| triggerhappy | global hotkey daemon for Linux |
| ttf-bitstream-vera | The Bitstream Vera family of free TrueType fonts |
| tzdata | time zone and daylight-saving time data |
| ucf | Update Configuration File(s): preserve user changes to config files |
| udev | /dev/ and hotplug management daemon |
| udisks2 | D-Bus service to access and manipulate storage devices |
| uil | Motif - UIL (User Interface Language) compiler |
| unclutter | hides the mouse cursor in X after a period of inactivity |
| unclutter-startup | autostart infrastructure for unclutter and unclutter-xfixes |
| uno-libs-private | LibreOffice UNO runtime environment -- private libraries used by public ones |
| unrar | Unarchiver for .rar files (non-free version) |
| unzip | De-archiver for .zip files |
| upower | abstraction for power management |
| ure | LibreOffice UNO runtime environment |
| urlview | Extracts URLs from text |
| usb-modeswitch | mode switching tool for controlling "flip flop" USB devices |
| usb-modeswitch-data | mode switching data for usb-modeswitch |
| usb.ids | USB ID Repository |
| usbutils | Linux USB utilities |
| user-setup | Set up initial user and password |
| util-linux | miscellaneous system utilities |
| uuid-dev:arm64 | Universally Unique ID library - headers and static libraries |
| v4l-utils | Collection of command line video4linux utilities |
| v4l-utils-dbgsym | debug symbols for v4l-utils |
| viewnior | simple, fast and elegant image viewer |
| vim-common | Vi IMproved - Common files |
| vim-runtime | Vi IMproved - Runtime files |
| vlc-data | common data for VLC |
| vlc-plugin-base:arm64 | multimedia player and streamer (base plugins) |
| vlc-plugin-video-output:arm64 | multimedia player and streamer (video output plugins) |
| vorta | Desktop Client for Borg Backup |
| vpnc | Cisco-compatible VPN client |
| vpnc-scripts | Network configuration scripts for VPNC and OpenConnect |
| wayland-protocols | wayland compositor protocols |
| wget | retrieves files from the web |
| whiptail | Displays user-friendly dialog boxes from shell scripts |
| wireless-regdb | wireless regulatory database for Linux |
| wireless-tools | Tools for manipulating Linux Wireless Extensions |
| wpagui | graphical user interface for wpa_supplicant |
| wpagui-dbgsym | debug symbols for wpagui |
| wpasupplicant | client support for WPA and WPA2 (IEEE 802.11i) |
| wpasupplicant-dbgsym | debug symbols for wpasupplicant |
| x11-apps | X applications |
| x11-common | X Window System (X.Org) infrastructure |
| x11-session-utils | X session utilities |
| x11-utils | X11 utilities |
| x11-xkb-utils | X11 XKB utilities |
| x11-xserver-utils | X server utilities |
| x11proto-dev | X11 extension protocols and auxiliary headers |
| x11proto-input-dev | transitional dummy package |
| x11proto-randr-dev | transitional dummy package |
| x11proto-record-dev | transitional dummy package |
| x11proto-xext-dev | transitional dummy package |
| x11proto-xinerama-dev | transitional dummy package |
| xauth | X authentication utility |
| xbindkeys | Associate a combination of keys or mouse buttons with a shell command |
| xbitmaps | Base X bitmaps |
| xclip | command line interface to X selections |
| xdg-dbus-proxy | filtering D-Bus proxy |
| xdg-utils | desktop integration utilities from freedesktop.org |
| xdotool | simulate (generate) X11 keyboard/mouse input events |
| xfce4-battery-plugin | battery monitor plugin for the Xfce4 panel |
| xfce4-power-manager | power manager for Xfce desktop |
| xfce4-power-manager-data | power manager for Xfce desktop, arch-indep files |
| xfce4-pulseaudio-plugin:arm64 | Xfce4 panel plugin to control pulseaudio |
| xfce4-screenshooter | screenshots utility for Xfce |
| xfce4-whiskermenu-plugin:arm64 | Alternate menu plugin for the Xfce desktop environment |
| xfconf | utilities for managing settings in Xfce |
| xfdesktop4-data | Xfce desktop background, icons and root menu (common files) |
| xfonts-100dpi | 100 dpi fonts for X |
| xfonts-75dpi | 75 dpi fonts for X |
| xfonts-base | standard fonts for X |
| xfonts-encodings | Encodings for X.Org fonts |
| xfonts-intl-chinese | international fonts for X - Chinese |
| xfonts-scalable | scalable fonts for X |
| xfonts-utils | X Window System font utility programs |
| xinit | X server initialisation tool |
| xinput | Runtime configuration and test of XInput devices |
| xkb-data | X Keyboard Extension (XKB) configuration data |
| xl2tpd | layer 2 tunneling protocol implementation |
| xorg | X.Org X Window System |
| xorg-docs-core | Core documentation for the X.org X Window System |
| xorg-sgml-doctools | Common tools for building X.Org SGML documentation |
| xserver-common | common files used by various X servers |
| xserver-xorg | X.Org X server |
| xserver-xorg-core | Xorg X server - core server |
| xserver-xorg-dev | Xorg X server - development files |
| xserver-xorg-input-all | X.Org X server -- input driver metapackage |
| xserver-xorg-input-evdev | X.Org X server -- evdev input driver |
| xserver-xorg-input-libinput | X.Org X server -- libinput input driver |
| xserver-xorg-legacy | setuid root Xorg server wrapper |
| xserver-xorg-video-all | X.Org X server -- output driver metapackage |
| xserver-xorg-video-amdgpu | X.Org X server -- AMDGPU display driver |
| xserver-xorg-video-ati | X.Org X server -- AMD/ATI display driver wrapper |
| xserver-xorg-video-fbdev | X.Org X server -- fbdev display driver |
| xserver-xorg-video-nouveau | X.Org X server -- Nouveau display driver |
| xserver-xorg-video-radeon | X.Org X server -- AMD/ATI Radeon display driver |
| xserver-xorg-video-vesa | X.Org X server -- VESA display driver |
| xterm | X terminal emulator |
| xtrans-dev | X transport library (development files) |
| xxd | tool to make (or reverse) a hex dump |
| xz-utils | XZ-format compression utilities |
| zip | Archiver for .zip files |
| zlib1g:arm64 | compression library - runtime |
| zlib1g-dev:arm64 | compression library - development |
