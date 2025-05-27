---
tags:
- scratchpad
info: aberto.
date: 2025-05-27
type: post
layout: post
published: true
slug: actually-portable-executable
title: Actually Portable Executable
comment: https://justine.lol/ape.html
---


Markdown Content:
24 aug 2020 @ [justine's web page](https://justine.lol/index.html)

αcτµαlly pδrταblε εxεcµταblε
----------------------------

One day, while studying old code, I found out that it's possible to encode Windows Portable Executable files as a UNIX Sixth Edition shell script, due to the fact that the Thompson Shell didn't use a shebang line. Once I realized it's possible to create a synthesis of the binary formats being used by Unix, Windows, and MacOS, I couldn't resist the temptation of making it a reality, since it means that high-performance native code can be almost as pain-free as web apps. Here's how it works:

MZqFpD='
BIOS BOOT SECTOR'
exec 7<> $(command -v $0)
printf '\177ELF...LINKER-ENCODED-FREEBSD-HEADER' >&7
exec "$0" "$@"
exec qemu-x86_64 "$0" "$@"
exit 1
REAL MODE...
ELF SEGMENTS...
OPENBSD NOTE...
NETBSD NOTE...
MACHO HEADERS...
CODE AND DATA...
ZIP DIRECTORY...

I started a project called [Cosmopolitan](https://github.com/jart/cosmopolitan) which implements the [αcτµαlly pδrταblε εxεcµταblε](https://raw.githubusercontent.com/jart/cosmopolitan/1.0/ape/ape.S) format. I chose the name because I like the idea of having the freedom to write software without restrictions that transcends traditional boundaries. My goal has been helping C become a build-once run-anywhere language, suitable for greenfield development, while avoiding any assumptions that would prevent software from being shared between tech communities. Here's how simple it is to get started:

gcc -g -O -static -fno-pie -no-pie -mno-red-zone -nostdlib -nostdinc -o hello.com hello.c \
  -Wl,--oformat=binary -Wl,--gc-sections -Wl,-z,max-page-size=0x1000 -fuse-ld=bfd -gdwarf-4 \
  -Wl,-T,[ape.lds](https://justine.lol/cosmopolitan/ape.lds) -include [cosmopolitan.h](https://justine.lol/cosmopolitan/cosmopolitan.h) [crt.o](https://justine.lol/cosmopolitan/crt.o) [ape.o](https://justine.lol/cosmopolitan/ape.o) [cosmopolitan.a](https://justine.lol/cosmopolitan/cosmopolitan.a)

In the above one-liner, we've basically reconfigured the stock compiler on Linux so it outputs binaries that'll run on MacOS, Windows, FreeBSD, OpenBSD, and NetBSD too. They also boot from the BIOS. Please note this is intended for people who don't care about desktop GUIs, and just want stdio and sockets without devops toil.

### Platform Agnostic C / C++ / FORTRAN Tooling

Who could have predicted that cross-platform native builds would be this easy? As it turns out, they're surprisingly cheap too. Even with all the magic numbers, win32 utf-8 polyfills, and bios bootloader code, exes still end up being roughly 100x smaller than Go Hello World:

[life.com](https://justine.lol/life.com) is 12kb ([symbols](https://worker.jart.workers.dev/life.com.dbg), [source](https://raw.githubusercontent.com/jart/cosmopolitan/1.0/examples/life.c)) 

[hello.com](https://justine.lol/hello.com) is 16kb ([symbols](https://worker.jart.workers.dev/hello.com.dbg), [source](https://raw.githubusercontent.com/jart/cosmopolitan/1.0/examples/hello.c))

Please note that zsh has a minor backwards compatibility glitch with Thompson Shell [update 2021-02-15: [zsh has now been patched](https://github.com/zsh-users/zsh/commit/326d9c203b3980c0f841bc62b06e37134c6e51ea)] so try `sh hello.com` rather than `./hello.com`. That one thing aside, if it's this easy, why has no one done this before? The best answer I can tell is it requires a minor ABI change, where C preprocessor macros relating to system interfaces need to be symbolic. This is barely an issue, except in cases like `switch(errno){case EINVAL:...}`. If we feel comfortable bending the rules, then the GNU Linker can easily be configured to generate at linktime all the PE/Darwin data structures we need, without any special toolchains.

### PKZIP Executables Make Pretty Good Containers

Single-file executables are nice to have. There are a few cases where static executables depending on system files makes sense, e.g. zoneinfo. However we can't make that assumption if we're building binaries intended to run on multiple distros with Windows support too.

As it turns out, PKZIP was designed to place its magic marker at the end of file, rather than the beginning, so we can synthesize ELF/PE/MachO binaries with ZIP too! I was able to implement this efficiently in the Cosmopolitan codebase using a few lines of linker script, along with a program for incrementally compressing sections.

It's possible to run `unzip -vl executable.com` to view its contents. It's also possible on Windows 10 to change the file extension to .zip and then open it in Microsoft's bundled ZIP GUI. Having that flexibility of being able to easily edit assets post-compilation means we can also do things like create an easily distributable JavaScript interpreter that reflectively loads interpreted sources via zip.

[hellojs.com](https://justine.lol/hellojs.com) is 300kb ([symbols](https://worker.jart.workers.dev/hellojs.com.dbg), [source](https://github.com/jart/cosmopolitan/blob/1.0/examples/hellojs.c))

Cosmopolitan also uses the ZIP format to automate compliance with the GPLv2 [update 2020-12-28: APE is now licensed ISC]. The non-commercial libre build is configured, by default, to embed any source file linked from within the hermetic make mono-repo. That makes binaries roughly 10x larger. For example:

[life2.com](https://justine.lol/life2.com) is 216kb ([symbols](https://worker.jart.workers.dev/life2.com.dbg), [source](https://github.com/jart/cosmopolitan/blob/1.0/examples/life.c)) 

[hello2.com](https://justine.lol/hello2.com) is 256kb ([symbols](https://worker.jart.workers.dev/hello2.com.dbg), [source](https://github.com/jart/cosmopolitan/blob/1.0/examples/hello.c))

Rock musicians have a love-hate relationship with dynamic range compression, since it removes a dimension of complexity from their music, but is necessary in order to sound professional. Bloat might work by the same principles, in which case, zip source file embedding could be a more socially conscious way of wasting resources in order to gain appeal with the non-classical software consumer.

### x86-64 Linux ABI Makes a Pretty Good Lingua Franca

It wasn't until very recently in computing history that a clear shakeout occurred with hardware architectures, which is best evidenced by the [TOP 500 list](https://en.wikipedia.org/w/index.php?title=TOP500&oldid=966847096#Architecture_and_operating_systems). Outside phones routers mainframes and cars, the consensus surrounding x86 is so strong, that I'd compare it to the Tower of Babel. Thanks to Linus Torvalds, we not only have a consensus on architecture, but we've come pretty close to having a consensus on the input output mechanism by which programs communicate with their host machines, via the SYSCALL instruction. He accomplished that by sitting at home in a bathrobe sending emails to huge corporations, getting them to agree to devote their resources to creating something beautifully opposite to tragedy of the commons.

So I think it's really the best of times to be optimistic about systems engineering. We agree more on sharing things in common than we ever have. There are still outliers like the plans coming out of Apple and Microsoft we hear about in the news, where they've sought to pivot PCs towards ARM. I'm not sure why we need a C-Class Macintosh, since the x86_64 patents should expire this year. Apple could have probably made their own x86 chip without paying royalties. The free/open architecture that we've always dreamed of, might turn out to be the one we're already using.

If a microprocessor architecture consensus finally exists, then I believe we should be focusing on building better tools that help software developers benefit from it. One of the ways I've been focusing on making a contribution in that area, is by building a friendlier way to visualize the impact that x86-64 execution has on memory. It should should hopefully clarify how αcτµαlly pδrταblε εxεcµταblε works.

You'll notice that execution starts off by treating the Windows PE header as though it were code. For example, the ASCII string `"MZqFpD"` decodes as `pop %r10 ; jno 0x4a ; jo 0x4a` and the string `"\177ELF"` decodes as `jg 0x47`. It then hops through a mov statement which tells us the program is being run from userspace rather than being booted, and then hops to the entrypoint.

Magic numbers are then [easily unpacked](https://github.com/jart/cosmopolitan/blob/1.0/libc/sysv/systemfive.S) for the host operating system using decentralized sections and the GNU Assembler `.sleb128` directive. Low entropy data like UNICODE bit lookup tables will generally be decoded using either a [103 byte LZ4 decompressor](https://github.com/jart/cosmopolitan/blob/1.0/libc/str/lz4cpy.c) or a [17 byte run-length decoder](https://github.com/jart/cosmopolitan/blob/1.0/libc/nexgen32e/rldecode.S), and runtime code morphing can easily be done using Intel's [3kb x86 decoder](https://github.com/jart/cosmopolitan/blob/1.0/third_party/xed/x86ild.greg.c).

Please note that this emulator isn't a requirement. αcτµαlly pδrταblε εxεcµταblεs work fine if you just run them on the shell, the NT command prompt, or boot them from the BIOS. This isn't a JVM. You only use the emulator if you need it. For example, it's helpful to be able to have cool visualizations of how program execution impacts memory.

It'll be nice to know that any normal PC program we write will "just work" on Raspberry Pi and Apple ARM. All we have to do embed an ARM build of the emulator above within our x86 executables, and have them morph and re-exec appropriately, similar to how Cosmopolitan is already doing doing with qemu-x86_64, except that this wouldn't need to be installed beforehand. The tradeoff is that, if we do this, binaries will only be 10x smaller than Go's Hello World, instead of 100x smaller. The other tradeoff is the GCC Runtime Exception forbids code morphing, but I already took care of that for you, by rewriting the GNU runtimes.

The most compelling use case for making x86-64-linux-gnu as tiny as possible, with the availability of full emulation, is that it enables normal simple native programs to run everywhere including web browsers by default. Many of the solutions built in this area tend to focus too much on the interfaces that haven't achieved consensus, like GUIs and threads, otherwise they'll just emulate the entire operating system, like Docker or Fabrice Bellard running Windows in browsers. I think we need compatibility glue that just runs programs, ignores the systems, and treats x86_64-linux-gnu as a canonical software encoding.

### Long Lifetime Without Maintenance

One of the reasons why I love working with a lot of these old technologies, is that I want any software work I'm involved in to stand the test of time with minimal toil. Similar to how the Super Mario Bros ROM has managed to survive all these years without needing a GitHub issue tracker.

I believe the best chance we have of doing that, is by gluing together the binary interfaces that've already achieved a decades-long consensus, and ignoring the APIs. For example, here are the [magic numbers](https://github.com/jart/cosmopolitan/blob/1.0/libc/sysv/consts.sh) used by Mac, Linux, BSD, and Windows distros. They're worth seeing at least once in your life, since these numbers underpin the internals of nearly all the computers, servers, and phones you've used.

If we focus on the subset of numbers all systems share in common, and compare it to their common ancestor, Bell System Five, we can see that few things about systems engineering have changed in the last 40 years at the binary level. Magnums are boring. Platforms can't break them without breaking themselves. Few people have proposed visions over the years on why UNIX numerology needs to change.

**download ![Image 1: [Linux]](https://worker.jart.workers.dev/redbean/linux.png)![Image 2: [Windows]](https://worker.jart.workers.dev/redbean/windows10.png)![Image 3: [DOS]](https://worker.jart.workers.dev/redbean/msdos60.png)![Image 4: [MacOS]](https://worker.jart.workers.dev/redbean/macos.png)![Image 5: [FreeBSD]](https://worker.jart.workers.dev/redbean/freebsd64.png)![Image 6: [OpenBSD]](https://worker.jart.workers.dev/redbean/openbsd.png)![Image 7: [NetBSD]](https://worker.jart.workers.dev/redbean/netbsd2.png)**

[emulator.com](https://justine.lol/emulator.com) (280k PE+ELF+MachO+ZIP+SH)

[tinyemu.com](https://justine.lol/tinyemu.com) (188k PE+ELF+MachO+ZIP+SH)

**source code**

[ape.S](https://raw.githubusercontent.com/jart/cosmopolitan/1.0/ape/ape.S)

[ape.lds](https://raw.githubusercontent.com/jart/cosmopolitan/1.0/ape/ape.lds)

[blinkenlights.c](https://github.com/jart/cosmopolitan/blob/1.0/tool/build/blinkenlights.c)

[x86ild.greg.c](https://github.com/jart/cosmopolitan/blob/1.0/third_party/xed/x86ild.greg.c)

[syscalls.sh](https://github.com/jart/cosmopolitan/blob/1.0/libc/sysv/syscalls.sh)

[consts.sh](https://github.com/jart/cosmopolitan/blob/1.0/libc/sysv/consts.sh)

**programs**

[life.com](https://justine.lol/life.com) (12kb ape [symbols](https://worker.jart.workers.dev/life.com.dbg)) 

[sha256.elf](https://justine.lol/sha256.elf) (3kb x86_64-linux-gnu) 

[hello.bin](https://justine.lol/hello.bin) (55b x86_64-linux-gnu)

**example**

bash hello.com              # runs it natively
./hello.com                 # runs it natively
./tinyemu.com hello.com     # just runs program
./emulator.com -t life.com  # show debugger gui
echo hello | ./emulator.com sha256.elf

**manual**

SYNOPSIS

  ./emulator.com [-?HhrRstv] [ROM] [ARGS...]

DESCRIPTION

  Emulates x86 Linux Programs w/ Dense Machine State Visualization
  Please keep still and only watchen astaunished das blinkenlights

FLAGS

  -h        help
  -z        zoom
  -v        verbosity
  -r        real mode
  -s        statistics
  -H        disable highlight
  -t        tui debugger mode
  -R        reactive tui mode
  -b ADDR   push a breakpoint
  -L PATH   log file location

ARGUMENTS

  ROM files can be ELF or a flat αcτµαlly pδrταblε εxεcµταblε.
  It should use x86_64 in accordance with the System Five ABI.
  The SYSCALL ABI is defined as it is written in Linux Kernel.

FEATURES

  8086, 8087, i386, x86_64, SSE3, SSSE3, POPCNT, MDA, CGA, TTY

WEBSITE

  https://justine.lol/blinkenlights/

**credits**

Jilles Tjoelker from the FreeBSD project played an instrumental role in helping me to get the POSIX rules changed to allow binary in shell scripts, which is what made this project possible. The monospace font used on this page is called [PragmataPro](https://fsd.it/shop/fonts/pragmatapro/) and it was was designed by [Fabrizio Schiavi](https://en.wikipedia.org/wiki/Fabrizio_Schiavi) in Italy.

**funding**

[![Image 8: [United States of Lemuria - two dollar bill - all debts public and primate]](https://worker.jart.workers.dev/sectorlisp2/lemuria.png)](https://justine.lol/lemuria.png)

Funding for this technology was crowdsourced from Justine Tunney's [GitHub sponsors](https://github.com/sponsors/jart) and [Patreon subscribers](https://www.patreon.com/jart). Your support is what makes projects like Actually Portable Executable possible. Thank you.

**see also**

[justine's web page](https://justine.lol/)

![Image 9](https://ipv4.games/claim?name=jart)