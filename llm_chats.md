# Information from chatting with LLMs

These are my own summaries of information I got from LLM chats that I just wanted to make note of. The information may be incorrect or incomplete; I don't necessarily fact check these at all and usually the answers aren't that important beyond my own curiosity. In some cases I've also added my own thoughts that came about from thinking on the responses.

### Q: For saving on video storage space, should I prefer lowering resolution or lowering encoding quality?

Prefer reducing resolution while maintaining quality. Low quality at higher resolutions will reduce file size as well, but will introduce more obvious artifacts (blockiness, banding, and smearing).

### Q: How does CRF (as used with H.264) relate to or scale with resolution?

CRF of 23 at 4K will look will look better than CRF 23 at 720p. When cutting resolution in half, you can usually increase CRF (reduce quality) without hurting perceptual quality because there is less detail to preserve. If CRF 23 looks fine for 1080p, then CRF 26-28 may be fine for 720p.

### Q: What even is CRF? What do the numbers represent?

It's a quality target, Constant Rate Factor. It can be better than a bitrate target because fixed bitrates waste data on simple scenes. Mathematically, it is a quantization parameter. Lower numbers are higher quality because the quantization steps are smaller.

- 0 = lossless
- 18 = effectively visually / perceptually lossless
- 20-24 = "sweet spot" for typical viewing
- 25-30 = noticable degredation, but not a bad tradeoff for storage savings
- 30+ = very compressed with obvious artifacts

### Q: How does H.265 achieve such small file sizes compared to H.264?

- It introduced recursively split CTUs (Coding Tree Units), which split the image into variable sized chunks as opposed to the fixed 16x16 blocks used in H.264
- More directional modes (33 vs. 9) for intra-frame prediction
- Other adaptive partitions and block sizes
- Improved CABAC

### Q: Compare Cinepak (as used in 1990s FMV) with the more modern MPEG-4?

Cinepak uses a combination of vector quantization and run-length encoding. It focuses on inter-frame compression, meaning it looks for similarities between consecutive frames.

MPEG-4 utilizes motion compensation, DCT, and variable bitrate encoding. It can take advantage of spatial and temporal redundancies.


### Q: As someone who never dives lower level than C, what makes architectures like x86, Z80, 68k, and ARM different from each other?

Zilog Z80 is an 8-bit CISC  from the late 1970's and 80's. It was capable for the time, but has very limited registers, complex and inconsistent instruction timings, and is not orthogonal (every register can't be used with every instruction). The lack of registers and stack support makes it difficult to compile C for Z80.

Motorola 68k is a 16/32-bit CISC from the 1980's. It has a clean, almost RISC-like instruction set that is orthogonal (many operations allowed on any register). It is very friendly for compiling C.

Intel x86 is a 16/32/64-bit CISC from the 1970's and evolving onward. It has a segment-based memory model in 16-bit modes. It has a backward-compatible but massive, ugly instruction set that is variable length and irregular. Early x86 was difficult for C compilers, but x86-64 is fine. Registers were too few and function call overhead was high.

ARM is a 32/64-bit RISC from the 1980's and onward. It has a simple, orthogonal instruction set. It is compiler friendly and power-efficient. However, it requires more instructions to accomplish some complex tasks when compared to CISC. It is excellent as a target for C compilers.

### Q: What is the relationship between voltage and clock speed? Why does overclocking sometimes depend on increasing voltage?

It comes down to how quickly transistors can switch between on/off states. Running at a higher clock requires that transistors switch between on/off states faster, and higher voltages allow electrons to move more quickly and thus change transistor state faster.

### Q: What is the difference between GnuWin32, MSYS, MinGW, and Cygwin?

GnuWin32 aims to provide native Windows GNU utilities without an emulation layer. There is no POSIX emulation. It is generally outdated and no longer maintained.

MSYS aims to provide a lightweight POSIX-like shell and environment, primarily for building MinGW programs. It is derived from Cygwin but stripped down. The POSIX layer lives in a DLL. It has its own package manager.

MinGW aims to provide a native Windows toolchain based on GCC without POSIX emulation. It compiles Windows-native executables. MinGW is the outdated original while MinGW-w64 is modern and supports 64-bit Windows.

Cygwin aims to provide a full POSIX-compliant environment on Windows, including a Unix-like filesystem and API. A DLL provides the POSIX layer. It has its own package manager.

### Q: Has a basic "Hello World" Win32 application changed at all between Windows 95 and Windows 11?

Not really, the same code should compile for Windows 95 and Windows 11, albeit perhaps with different compilation parameters. Unicode APIs are preferred as of Windows NT, but ANSI will still work. Any other features like visual styles, manifest requirements, or dark mode / theming are all optional.

### Q: How does WinMain relate to the more standard C main?

Windows has different "subsystems" for console and GUI applications. For console applications, Windows expects the standard "main" or "wmain" for Unicode. The console subsystem provides stdin, stdout, and stderr. The root entry point is typically mainCRTStartup which initializes the C runtime before calling main.

In a GUI application, Windows expects WinMain and provides Windows-specific parameters like the application instance handle.


### Q: What even is the C "runtime" if it compiles to native code?

It is a library (e.g. msvcrt.dll on Windows or glibc on Linux) that provides initialization code, standard library implementations, memory management, file I/O, possibly threading and exception handling support, and exit-time cleanup. It sets up the environment. It is linked to produce the final executable as opposed to being a distinct and isolated "supervisor" like Java or .NET runtimes.

The OS doesn't call main directly; it calls a runtime startup function (e.g. mainCRTStartup or _start) which sets up the stack and heap, handles global/static initialization, and passes argc/argv to main.

Basic functions are implemented in a platform-specific manner:

- malloc/free via VirtualAlloc on Windows or sbrk on Linux, INT 21h on DOS
- printf via WriteFile on Windows or write on Linux, interrupts on DOS

Cleanup runs any atexit() handlers and deallocates CRT memory itself.

On embedded systems, there may not be a standard C runtime or it may be lacking features. There may not be a malloc/free if no heap memory exists, and there may be no file I/O functions if the system has no file system. Something like putchar may be implemented to write characters to a UART register address.


### Q: On Android, do apps begin execution via a C runtime?

No, even native NDK apps start with Java bytecode executed by the Android Runtime or Dalvik VM. Native code is only loaded as dynamic libraries. There is no native C 'main' in the traditional sense.

However, some native daemon or command-line utilities like toybox or adb do run on Android via a traditional C runtime (bionic) and a traditional native entry point (_start). Native ELF binaries can be run within an app sandbox, even without root access. Root access allows ELF binaries to be placed and executed like a typical Linux system.

### Q: Do iOS apps begin execution via traditional C runtime?

Almost -- the system loads the executable and performs dynamic linking before executing a _start function which calls main. However, main is not implemented by the app code but is instead a very thin wrapper that calls UIApplicationMain.

### Q: How did application startup work on classic macOS?

It did not begin with a function call like _start or main in the Unix sense. A special function usually named Start or Main was loaded from the application's "resource fork". There was no cooperative multitasking; applications had to cooperate by yielding CPU time. POSIX APIs like malloc were not used, Mac Toolbox APIs like GetNewHandle and ExitToShell were.

### Q: Do Windows and Linux support other mechanisms for launching executables?

Linux ELF binaries can define any entry point in the assembly; they don't need _start or main.

Similarly, the PE format on Windows allows custom entry points and does not require a standardized main or WinMain. Services define a ServiceMain instead. Windows UWP apps don't launch like traditional PE executables; WindowsRT reads an entry point from an XML manifest and the AppContainer sandbox launches it.

### Q: What was a blitter chip and why did the IBM PC apparently never have one?

Short for Bit Block Transfer (BitBlt), they were responsible for moving rectangular regions of data from one area of memory to another, sometimes with transformations like mirroring or rotation. They may support image masks and filling areas with patterns or colors. Noteworthy systems with blitter chips include Amiga / Commodore, Atari ST, and arcade or home console systems of the time. The chip offloads these operations from the main CPU.

The IBM PC did not have a blitter chip and graphics operations were very much CPU-bound. Later graphics adapters introduced some hardware accelerated operations, but true GPUs with 3D acceleration took over shortly after.

Blitter chips accelerated rectangular memory moves by operating in parallel, bypassing the CPU for memory access, and lacking the overhead associated with general purpose instruction processing as seen in a CPU.

Image data is not efficiently handled by the CPU because the image data is fragmented. Copying an entire image may be accomplished with a simple copy operation of a continuous region of memory, but copying a sub-rectangle requires calculating offsets and copying different fragmented regions of memory per row.

Software blit operations on a PC, such as when using SDL without GPU acceleration, leverage various low-level optimizations. SIMD instruction sets like SSE2 and AVX play a key part in performing operations on batches of pixel data efficiently, but the same fundamental issues associated with using the CPU like memory bandwidth and cache misses remain.

### Q: What's the deal with Snap, AppImage, and Flatpak?

Snap is a containerized packaging system developed by Canonical. It uses AppArmor for security isolation and bundles dependencies with the app, isolating it from the host system's libraries. The containerization involves some performance penalty at startup. It is the default on Ubuntu but not universally loved.

AppImage is a lightweight format where the application and its dependencies are bundled into a single executable. There is no sandboxing by default, no built-in update mechanism, and still relies on certain core libraries like glibc from the host system. It has minimal overhead as it is not truly containerized in the same way as Snap.

Flatpak focuses on using Linux namespaces for sandboxed app distribution. While decentralized, Flathub is the most popular repository. Startup performance may be influenced due to sandboxing and runtime loading. Encourages sharing "runtimes", but apps can bundle dependencies as well.

### Q: I hear about UTF-8 all the time, but what's the deal with UTF-16 and UTF-32?

UTF-8 is ubiquitous on the web and in open-source systems (Linux). This is largely due to its backward-compatibility with ASCII and space efficiency for ASCII-heavy text.

UTF-16 is the native encoding for text in modern Windows, Java, and .NET. It can be more space efficient for Asian languages which often use characters that would require 3 bytes in UTF-8 but only 2 bytes in UTF-16. Systems designed in the late 1990s or early 2000s often adopted UTF-16 before UTF-8 became dominant. UTF-16 is not backward-compatible with ASCII.

UTF-32 is used for specific applications where constant-time indexing of code points is valuable. Every character is stored as 4 bytes, even ASCII characters. Therefore, it is not backward-compatible with ASCII either.

Until relatively recently (an update to Windows 10), Notepad would save files as ANSI or UTF-16 LE with BOM by default. Today, though, the default is UTF-8.

### Q: What is an In-Circuit Emulator?

An ICE is a physical device that serves as a substitute for a target microcontroller during development. It emulates the target microcontroller behavior while allowing for debugging and observation.

Traditional ICEs have largely been replaced by on-chip debugging technologies like JTAG or SWD.

### Q: Why did we used to use screensavers to prevent burn-in instead of just turning the monitor off?

Early CRT monitors didn't have the power management features we have now (e.g. VES DPMS); monitors didn't have a "sleep" or "standby" state, so changing what was displayed was the only thing that a system could do automatically.

Early CRTs also often needed some "warm-up" time after being turned on, which was another factor in not wanting to turn them off. Cultural momentum and legacy systems led screensavers to be used even after alternatives existed.

### Q: Why are dedicated audio processors no longer "a thing" while GPUs are?

In the earlier days of the IBM PC, CPUs struggled with audio tasks enough for dedicated hardware to have value. Aside from niche products, modern CPUs handle audio processing sufficiently. Graphics tasks are inherently highly parallel and benefit substantially from hardware that operates differently than a CPU. Audio tasks, on the other hand, have more limited parallelism potential.

### Q: Has there been or is there a port of Linux that runs on 68k Macs? And PowerPC?

Yes, with Debian m68k being one of the most prominent. Booting Linux on 68k Macs is not trivial and typically requires using MacOS as a staging platform to initialize the Linux kernel.

Unlike PCs with a standardized BIOS or UEFI, 68k Macs didn't have a firmware designed for booting other OSes. The Macintosh ROM contained core system software, hardware initialization, device drivers, and parts of the OS. To work around this, a bootloader was run from MacOS to load the Linux kernel.

Starting with iMac G3, Apple moved to Open Firmware, which is more similar to BIOS or UEFI and allows booting arbitrary OSes. Disk partitioning schemes still differed, however, needing to use Apple Partition Map layouts rather than MBR or GPT.

### Q: What is a "federated" system?

A federated system is a decentralized one composed of multiple independent "nodes" that cooperate. A common example is email. There is no central email system or provider; email is really a set of protocols that different systems agree on for sending messages to each other. Although Gmail dominates personal email accounts today, a person can create an email account using any available service or even set up their own email server.

Users authenticate with their chosen node, or "instance", with their credentials. This may use something like OAuth 2.0.

Instances communicate with others through a protocol like ActivityPub, or SMTP/IMAP in the case of email. Cryptographic signatures (public key cryptography) are used to verify the authenticity of interactions. For example, each instance may have its own pair of public and private keys. The public keys allow other instances to verify that incoming messages were truly sent by a given instance.

As commonly seen with email, "identity" is tied to a specific instance (e.g. "@gmail.com").

### Q: How does Single Sign-On work?

SSO delegates authentication to a trusted third party. The target system sends you to the authentication system. Upon authentication, you are directed back to the target system along with an authorization code. The target system uses the authorization code to request an access token (and optionally a refresh token) from the identity provider. This access token can then be used to make authorized requests to the identity provide for more information. The target system may also set its own session cookie or token to manage your session independently from the identity provider.

Standardized protocols and formats may be used, such as OAuth 2.0, OpenID Connect, and JWT.

A state parameter is used to prevent CSRF attacks. The target system generates a unique value for each authentication request which the identity provider must return unchanged.


### Q: Do ARM devices have a semi-standard boot process like x86 PCs do (BIOS or UEFI)?

Some ARM-based devices use UEFI (especially in servers), but many ARM devices like smartphones use custom bootloaders specific to the manufacturerer. Typically, ROM code baked into a chip runs first, does minimal hardware initialization, then hands off to a first-stage bootloader, then a second, and finally the OS kernel.

Because ARM is used in various kinds of systems, the boot process may be even more customized. It may not have a staged boot process but simply boot by running the OS at a fixed location.

The bootloader stages would be most analogous to a BIOS, or a combination of BIOS and a bootloader like GRUB.

### Q: How did the standardized BIOS come about?

The BIOS originated as a component of CP/M, which gained popularity in the late 1970s and early 1980s across various microcomputers. The BIOS enabled CP/M to run on these different systems by isolating the specifics of I/O, storage, system interrupts, and other low-level functions.

PC-DOS and MS-DOS were designed for compatibility with CP/M applications. The PC's BIOS took care of hardware initialization and provided a standardized interface while MS-DOS handled other functions that had historically been part of the CP/M BIOS. Still, the IBM PC BIOS was conceptually derived from the CP/M BIOS component.

### Q: What systems inspired the design of CP/M?

It was inspired by two main systems. The hierarchical file structure and disk-based storage were influenced by the IBM System/360. Aspects of the command-line interface and file management drew inspiration from DEC OS/8, used with the PDP-8 minicomputer.

### Q: What is the legacy of the IBM System/360?

The IBM System/360, introduced in the 1960s, introduced the concept of "family architecture" where multiple models in a family shared a common architecture and instruction set, allowing for backward compability and smooth transitions.

It introduced virtual memory, swapping storage between RAM and the more plentiful disk-based storage.

Instruction set concepts like registers, addressing modes, and instruction formats have roots in System/360.

The operating system, OS/360 and its successors, introduced concepts like time-sharing, multitasking, and spooling.

### Q: What are mainframe computers still used for in the modern day?

They are used for certain critical and resource-intensive tasks due to their robustness and reliability. They excel at processing vast amounts of data quickly and efficiently and are used in industries like finance, healthcare, and telecommunications.

They are used in the airline industry for flight reservation systems, seat inventory management, and scheduling.

They are still used in large retail organizations for inventory management, supply chain optimization, and point-of-sale systems.

They are employed by utility and energy companies to manage power distribution and billing.

Many large organizations still rely on them to run legacy applications that have been developed and maintained over decades where migration would be costly and risky.

Mainframes can handle large-scale data processing with extremely low latency, making them more suitable for tasks that require real-time or near-real-time processing when compared to distributed cloud solutions. They are known for high levels of reliability and availability, being designed with redundant components and failure mechanisms which is vital for sectors like finance, healthcare, and government. They are preferred for handling sensitive data that require top-level security. Their use may be tied to stringent regulatory requirements in industries like finance and healthcare.

Mainframes utilize dedicated hardware I/O channels which offload I/O operations from the CPU, allowing the CPU to focus solely on fast memory operations. On a typical x86 PC, I/O still involves the CPU significantly. They tend to have hardware support for atomic transactions and journaling, for example to commit or rollback multiple memory writes. In general, mainframes move a lot of work into hardware that must be done in software on x86.

### Q: Is the "openness" of the PC platform some kind of fluke?

A combination of factors aligned to allow the IBM PC to become an open platform without it necessarily being "by design". IBM used off-the-shelf parts rather than proprietary hardware which made the system easier to clone, and IBM didn't foresee the long-term consequences of this decision.

The critical factor in the IBM PC's "openness" was the rise of clones, particularly Compaq. They reverse-engineered the IBM PC BIOS, one of the few proprietary components, legally through clean-room techniques and created PCs that could run the same software. This spurred competition and pushed the market toward standardized hardware.

MS-DOS targeted varied hardware using the x86 architecture, and so compatibility with MS-DOS and x86 became more important than compatibility with IBM hardware specifically.

Unlike Apple with its vertical integration of hardware and software, IBM lost control of the PC platform. They attempted to introduce proprietary architectures with IBM PS/2 and MCA, but the industry favored open standards like ISA and later PCI.

In the 80s and 90s, the PC market was fueled by business computing, customization, and hobbyist culture. These market forces favored compatibility, expansion, and innovation from multiple vendors. Modern devices are often more "locked down" because the market prioritizes security, intellectual property control, and user experience. Devices are sold more like appliances than general-purpose machines. There is more business emphasis on locking users into specific app stores, services, and operating systems.

Before the IBM PC, the computing market was fragmented among various incompatible systems. There were mainframes, minicomputers, and early personal computers such as the Apple II, Commodore PET, Tandy TRS-80, and the Atari 400/800. CP/M was an early OS that several machines used, but the systems still varied in hardware design and had limited compatibility.

No single machine prior to the IBM PC had gained enough market share to dominate the market.

### Q: Why does it feel like technology is moving "backward" toward closed systems?

In the 90s and 2000s, there was massive competition between hardware vendors and almost all hardware adhered to standards like ISA, PCI, or x86, allowing users and OEMS to mix and match components. This was partly a byproduct of the IBM PC standard becoming an industry de facto. Openness facilitated rapid hardware development and software compatibility. Tech companies were focused on horizontal integration; selling hardware and software platforms that worked across various devices.

Since the late 2000s, the rise of mobile devices shifted the focus away from general purpose computing to more "appliance-like" products. Large companies like Google and Apple pushed closed ecosystems because they offered better control and security. Google and Apple began controlling hardware and software tightly, moving toward vertical integration. Because this model has proven profitable, other companies increasingly adopt it. It's a fundamental shift from the more open, component-based PC world.

The openness seen in the 90s and 2000s was somewhat unusual. Historically, platforms were more closed (mainframes, early Macs, game consoles), and the IBM PC era offered an unusual market that adopted openness and modularity.

One factor is that today's mobile market is dominated by only two players. In the early days of computing, many companies were experimenting with different, incompatible systems which made open standardization appealing.

### Q: How do Linux and BSD differ, given their shared Unix roots?

For one, Linux itself is strictly a kernel. Even shells and other utilities one would expect to find are provided from other projects like GNU. BSDs are considered complete operating systems with the kernel and user-space programs developed together as part of the same project.

Linux is licensed under the GPL which requires modifications to be released under the same license. BSD has a more permissive license which is why it is the foundation for commercial systems like macOS and the operating system used in the PS4.

Several alternative package managers and init systems are used with Linux, and a variety of filesystems are supported, with ext4 being the most commonly used. BSD supports UFS, with FreeBSD supporting ZFS as well. BSDs have an associated package management system and the init system is generally simpler and more traditional.

Linux can use various security modules such as SELinux or AppArmor to provide mandatory access control and other security policies. BSD variants have their own approach to security. OpenBSD is notable for its "secure by default" philosophy. FreeBSD has a jail mechanism for lightweight virtualization.

Linux kernel development is more rapid and community-driven, while each BSD variant has a more centralized development model with a core team of maintainers. This can result in more stability but potentially slower adoption of new features.

Linux networking is highly customizable with a variety of subsystems and drivers. Networking performance is often fine-tuned per distribution for a specific use case. BSD networking is well-regarded for its reliability and simplicity. It has been a reference implementation for TCP/IP and is still considered one of the most stable and performant stacks.

### Q: When did Unix first make the jump to x86 / PC hardware?

Xenix was an early Unix-like operating system that ran on x86 (1981), based on UNIX Version 7.

System V/386 was a port of UNIX System V to the Intel 80386 in 1987.

BSD Unix systems were originally developed on DEC hardware, but the release of 386BSD in 1992 was the first BSD variant to target the Intel 386. It was based on BSD 4.3, and laid the foundation for the FreeBSD and NetBSD projects.

Linux is not truly "a Unix", but for comparison it's worth noting that it first arrived in 1991.

### Q: How does UFS compare with ext4?

UFS originated as the Berkeley FFS in the early 1980s and evolved into UFS. It has options like journaling (UFS+J), but the design remains simpler and more conservative compared to newer file systems.

ext4 is more feature-rich; things like online defragmentation, delayed allocation, file preallocation, journal checksums, multiple journaling modes, and various optimizations. In general, ext4 can offer better scalability and performance.

### Q: What was the overall timeline of file system development?

The 1970s saw the earliest file systems on mainframes such as that seen on IBM's OS/360.

The 1980s saw UFS which improved on earlier Unix file systems with features like block allocation and inodes. MS-DOS FAT12 was a simple solution introduced with MS-DOS 1.0 in 1982.

The 1990s saw ext (1992) developed for Linux. NTFS (1993) provided a better alternative to FAT that supported journaling, file permissions, and large volume and file support. Later in 1998, ext2 brought support for larger file systems, better performance, and more robust data structures to Linux.

The 2000s saw ext3 (2003), which added journaling and became the default for many Linux distributions. ZFS (2005) was developed for Solaris and featured advanced data management capabilities, snapshots, and built-in RAID. ext4 (2008) added extents and delayed allocation.

The 2010s saw Btrfs added to Linux, adding snapshots and checksumming. It is still under active development. APFS (2014) was introduced to macOS and designed for SSD storage with built-in features like encryption, space sharing, and snapshots, replacing HFS+ as the default file system.

Overall, key innovations over time were the introduction of journaling for reliability and recovery, extents which reduced fragmentation by allocating large contiguous blocks, snapshots for creating point-in-time copies, checksumming for integrity verification, and volume management features.

### Q: Why does it seem like defragmenting was so necessary on Windows historically but not on Mac or Linux?

The primary reason is probably the use of FAT historically. It was a simple system where files were stored in clusters without much of a mechanism for allocating space efficiently. NTFS improved on this but still suffers from fragmentation over time, especially with large files.

The ext3 and ext4 file systems on Linux, while not immune, try harder to avoid fragmentation. ext3 tries to allocate files contiguously when possible and uses algorithms to reduce fragmentation. ext4 takes this a step further with the introduction of extents.

HFS+ used on Macs could experience fragmentation, but was designed to handle it more gracefully than FAT and allocates space more efficiently.

### Q: How and why did the POSIX specification come about?

POSIX was developed to address a need for standardization in Unix-like operating systems. Unix was developed at Bell Labs in the late 1960s. Its source code was shared with various universities and organizations which led to multiple variants that became incompatible. In 1980, the IEEE recognized the need for a standardized interface, and the first edition was published in 1988.

### Q: What was the real-world context in which Unix commands like "write" and "wall" were used?

Such commands were designed in the context of multi-user mainframes and minicomputers such as the PDP-11 and VAX. In a university setting, for example, terminals would be set up in different rooms or offices all connected to the same system. Those commands were quick and easy ways to communicate with other active users to ask questions, coordinate, or announce administrative events or warnings.

In the modern world, it's less common for users to share a single system in that way. Most work is done on some kind of personal system, whether that be physically personal or a virtualized environment, and communication is done via network communication between systems rather than within a single one.

### Q: What's the deal with MINIX?

MINIX was developed in 1987 as a simple, Unix-like, POSIX compliant OS for educational purposes. It has a microkernel design where the kernel is minimal and handles only functions like CPU scheduling, inter-process communication, and basic memory management. Although MINIX was an inspiration for Linux, Linux uses a monolithic kernel design where services like the file system, device drivers, and network stack run in kernel space as well.

As of MINIX 3.0 in 2005, the system evolved into an OS for embedded systems in addition to serving as an educational tool. Despite this, it has not seen substantial adoption even in that space.

### Q: What is the timeline and history of common shells?

The Thompson Shell (tsh) in 1971 was relatively simple but served as the basis for later shells.

The Bourne Shell (sh) replaced the earlier Thompson Shell in 1977 and introduced control structures and improved scripting capabilities.

The C Shell (csh) was developed in 1978 as a more user-friendly shell that would support features similar to the C programming language. It introduced features like history and job control for interactive use.

The Korn Shell (ksh) in 1983 aimed to improve on the Bourne Shell with features like associative arrays, arithmetic operations, and better scripting capabilities.

The TENEX C Shell (tcsh) in 1987 extended the C Shell with additional features like command-line editing, completion, and improved history.

The Bourne Again Shell (bash) in 1989 is a free software replacement for the Bourne Shell, and was designed to incorporate features from the Korn Shell and C Shell.

The Almquist Shell (ash) was created in 1989 as a lightweight, fast, and small shell to be used when resources are limited.

The Z Shell (zsh) in 1990 was created to extend the Bourne Shell with more features including advanced completion, globbing, and customization.

### Q: How do copy and move operations interact with "created at" and "modified at" dates on different systems?

On Windows and macOS, move operations typically preserve both the "created at" and "modified at" dates while copy operations replace the "created at" date. On Linux, both operations typically preserve both dates.

### Q: How does the concept of a Byzantine fault relate to the design of distributed systems?

Byzantine faults are about the inability of nodes in a system to know whether other nodes are providing correct or information or may even be behaving maliciously. Fault-tolerant designs may involve redundant copies of data with replication, consensus algorithms like PBFT, HoneyBadgerBFT, Paxos or Raft, and of course secure communciation via encryption, authentication, and authorization.

One failure mode is that nodes may simply stop functioning or be unreachable due to network partition. Timeouts and heartbeats can be used as a basic signal that a node is "dead" or unreachable and to exclude it until it comes back online. Another failure mode is that a given node may be operating on old or incorrect information, or be otherwise faulty in some way while still responding to messages. This is where consensus algorithms come in so that the system can agree on a ground truth.

### Q: What is the relevance of "3n + 1" with regard to Byzantine faults?

A 1980 paper showed that "3n + 1" nodes are necessary and sufficient in a distributed system to handle "n" nodes acting maliciously. In other words, the system can still agree on the correct "truth" as long as under 1/3 of the nodes are acting maliciously.

### Q: How do PBFT and HoneyBadgerBFT work?

Practical Byzantine Fault Tolerance aims to provide a solution to the Byzantine Generals Problem. It relies on replicating the relevant state across a set of nodes that participate in the consensus process. A "primary node" proposes a value, other nodes acknowledge the proposed value, and then nodes vote on a value. A certain number of nodes (quorum) need to agree on a value for it be accepted. The optimistic path is that most nodes are functioning correctly and will agree, otherwise a slower path is required. Cryptographic signatures are used to ensure the authenticity of messages.

HoneyBadgerBFT operates in an asynchronous network that doesn't rely on assumptions about message delivery times. This makes it more tolerant to unpredictable network conditions. It uses broadcast encryption to transmit messages to a subset of nodes without revealing the content to others which adds an extra layer of privacy and security. It (somehow) maintains its functionality even when the number of faulty nodes exceeds the expected threshold. It is particularly suitable for use in blockchain or decentralized ledger technologies.

### Q: What is the recommended way to partition a disk for Linux?

In general, using a single partition is fine. More complex schemes are often related to outdated advice or specific use cases or concerns.

Partitioning is about failure isolation and policy control. For example, it can prevent log output from filling the entire disk or apply different mounting options. It can also make backups or system reinstalls easier.

The "modern" default is often a single root partition, optionally with "home" on a separate partition, which can be useful for separating user data from system files.

More rigid compartmentation was more relevant in the past because storage was more constrained in general and older filesystems didn't handle large trees as well.

For servers or other systems where you expect heavy logging, growing database storage, or Docker containers, it can make sense to put "var" on a separate partition to isolate uncontrolled growth.

The "tmp" and "var/tmp" directories historically were separated for safety, but today they are usually fine on the root partition and are often handled with a RAM-based tmpfs instead of residing on the disk anyway.

A "swap" partition was also common practice, but a swap file is fine unless you need hibernation support. It's more flexible and easier to resize.

### Q: It occurred to me that we kind of take hierarchical filesystems for granted but presumably they were not the singular correct approach. How did they come to be so fundamental to computer systems?

A filesystem maps well to human understanding and also provides naming, isolation, and interoperability. In general, applications can expect that an error involving one file will remain isolated to that file, and this provides coarse-grained fault isolation "for free". The filesystem is a kind of "common ground" for communication or data exchange between software. The concept of a "file" is simple and can transcend differences in programming language, runtimes, machines, decades, etc.

Historically, filesystems as we know them won because they were a low common denominator abstraction that balanced simplicity, safety, and generality.

### Q: What value do critics provide? Seems like they just provide subjective opinions for the most part. I often like things that critics rated poorly.

I may like critically unpopular media because I don't consume that much of it and a given example is therefore still novel and entertaining enough to me. A critic likely consumes a lot more content and is comparing to many more examples. Fair enough.

### Q: How does something like a centralized crypto exchange scale given the non-negotiable requirements for sequential order execution?

At its core, an exchange does rely on strongly ordered, single-writer components, and this doesn't scale the way a more stateless web backend does, nor does it pretend to. Instead of scaling everything horizontally, exchanges are almost always sharded by market. The exchange overall may have massive traffic, but traffic is substantially less for any given market pair.

Of course, certain markets are more active than others, and for this some amount of vertical scaling is required: faster CPUs, more memory on a single system, optimizations, etc.

Persistence on the critical path is usually handled by append-only logs rather than a traditional "source of truth" database. The order matching engine writes an event stream which is used to build database state downstream. If the engine crashes, the log still serves as a source of truth for reconstructing the expected state, and so distributed transactions and eventual consistency are avoided in the critical path.

Outside of that, there is much more room for horizontal scaling. Things like authentication, API gateways, order intake, and balance checks don't require precise timing and can be eventually consistent. There is more room for being optimistic until the boundary of the critical order matching path.

Account balances are somewhat split-brained. There is typically a fast and strongly consistent balance colocated with the matching engine, or logically owned by it, that tracks available funds. Separately, there are slower, replicated ledger systems that track deposits, withdrawals, funding, and reconciliation.

Similarly, market data feeds and user dashboards can tolerate a fair amount of lag without major consequences, and so these may be a fan-out from the event log the matching engine writes to.

For a given market, only one engine instance is active, but there may be hot standbys replaying the event log, ready to take leadership if the primary engine instance fails.

### Q: Why does it seem that flight searches are extremely slow? Product searches are usually extremely fast. It feels like a comparable case of "live" availability being searched, no?

A web store search is fundamentally a read from a precomputed, cache-friendly data set. A flight search is more like a distributed transaction and pricing problem. A product search typically involves tightly integrated systems while pricing and availability change infrequently. A flight search often requires querying multiple lives systems including the airline's reservation system, partner airlines, and fare construction engines.

Airline fare are not looked up so much as constructed. They are governed by a large rule system. For a round trip, the system may need to evaluate many outbound and return combinations. It's more of an optimization problem than a lookup. Raw seat inventory may be cached, but the valid price for a particular trip often isn't.

Flight availability is managed in terms of fare class availability. Availability is not purely about whether a given seat is free, but whether there is at least one unit left in a particular fare bucket on a particular flight. Those buckets are controlled by revenue management and can be opened, closed, or resized dynamically. Caching is less useful when results change so dynamically.

Flight searches must consider combinations of flights with hops to a destination while factoring in connection times.

Flight availability is intentionally fuzzy. Airlines overbook and rely on probabilistic no-show models, so the inventory is not a hard count but rather based on a controlled risk model.

There's a lot of legacy infrastructure. Core airline reservation systems are famously old. Many are mainframe-era systems that expose functionality via protocols that are not optimized for low-latency. Many airlines run on Passenger Service Systems (Amadeus, Sabre, Travelport) that date back to the 1970s-1990s.

### Q: Why does it seem that people commonly report themselves as "tired". If everyone is "tired", then that's just the baseline state, no?

A few possibilities. People tend to compare to an idealized norm, not their own baseline. If their potential best is an idealized well-rested, alert, focused, then anything less than than is "tired".

It may also be used as a safer communication shortcut that avoids over-sharing. It can mean anxious, unmotivated, or empty without getting into specifics.

However there are potentially true modern lifestyle deficits including getting less than 7-8 hours of sleep regulary or getting poor sleep due to artifical light, caffeine, alcohol, or sedentary work.

### Q: What are some games for handheld systems that break the mold of handheld games being "lesser"?

On the GB / GBC:
- Link's Awakening
- Pokemon Gold and Silver
- Metal Gear: Ghost Babel
- Shantae
- Tetris

On the GBA:
- Metroid Fusion / Zero Mission
- Advance Wars and Advance Wars 2
- Fire Emblem and Fire Emblem: The Sacred Stones
- Final Fantasy Tactics Advance
- Mario Kart: Super Circuit
- Castlevania: Aria of Sorrow

On the DS:
- The World Ends With You
- Castlevania: Dawn of Sorrow / Portrait of Ruin / Order of Ecclesia
- Advance Wars: Dual Strike
- Mario & Luigi: Bowser's Inside Story
- Pokemon Black & White / Black 2 & White 2

On the PSP:
- Monster Hunter Portable 3rd
- Monster Hunter Freedom Unite
- Persona 3 Portable
- Crisis Core: Final Fantasy VII
- God of War: Chains of Olympus / Ghost of Sparta
- Metal Gear Solid: Peace Walker
- Daxter
- Jeanne d'Arc

### Q: I recall various x86 instruction set "expansions" over the years. Are they all still in use? Do They get used together or replace each other?

They are not all in use in modern software and in general are not mixed; compilation targets a particular set. In some cases, a binary may ship with multiple versions of hot functions that are selected at runtime after querying the CPUID information, but function versions don't arbitrarily mix instruction sets.

To begin with, MMX (1997) is obsolete and SSE2 supersedes it completely. 3DNow! (1998) is also dead as it was AMD-only and is not available in modern CPUs. x87 FPU (1987) is legacy and still supported for scalar FP, but compilers prefer SSE/AVX over it.

The original SSE (1999) is legacy and mostly irrelevant. SSE2 (2001) is essentially the baseline; it's mandatory for x86-64 and compilers assume it, with FP often mapped to SSE2. However, SSE1-4.2 (2008) are effectively universal unless compatibility with old hardware is needed.

In the modern day, though, SSE is a compatibility fallback. In practice, AVX (2011) and AVX2 (2013) are common enough and AVX2 in particular can be considered the mainstream vector ISA today.

FMA3 (fused multiply-add) (2013) is common and often paired with AVX2.

BMI1 and BMI 2 (2013) are also common bit manipulation instructions useful for certain algorithms.

AVX-512 is a fragmented family of instruction sets introduced in 2016, and was server centric until "recently". AVX10 is an emerging attempt by Intel to unify AVX-512. AMX (Advanced Matrix Extensions) is another emerging instruction set. This leaves AVX2 as the most recent reliable ISA.

To summarize, the modern compatibility baseline is SSE2 through SSE4. The modern, but essentially ubiquitous, performance target is AVX2, FMA, and BMI1/2.

### Q: Why would the NSA release Ghidra publicly?

Ghidra may have been released in 2019 for several reasons. It may serve strategic signaling and soft power; it demonstrates technical prowess, builds goodwill among security researchers, and helps position the NSA as a "good actor" in global cybersecurity.

The NSA competes with the private sector for cybersecurity talent. Releasing Ghidra showcases the agency's capabilities and gives prospective recruits the chance to learn tooling they would use.

NSA contractors and partner agencies have a use for such tools, and releasing it publicly makes it easier to standardize across agencies.

Releasing Ghidra puts pressure on the long standing dominance of IDA Pro and Hex-Rays as closed-source, expensive reverse engineering tools.

Ghidra had been used internally for nearly two decades. It was mature and well-documented. Most of the advantages associated with keeping it secret were no longer relevant. It also doesn't include exploits or anything; it is a passive analysis tool.

### Q: Having grown up in the U.S., why was I completely unaware of the Sega Master System?

It was crushed by the NES in North America and Japan by a factor of roughly 20 to 1. Sega's marketing was half-hearted in the U.S. and they frequently changed distribution partners. The box art was infamously minimalist and unattractive.

The Master System had solid games, but no particular mascot or breakout hit at the time. The Genesis / Mega Drive along with Sonic as its mascot was effectively Sega's debut for many Americans.

The Master System was a massive hit in other markets, particularly Brazil, the UK, and Portugal.

### Q: Why do so many European folk and fairy tails involve the woods? Which real-world woods are these tales likely influenced by?

The woods symbolically and historically represented the boundary between the known and the unknown. In pre-modern Europe, forests were vast, untamed, and dangerous. The rules of society didn't apply, mystery and magic felt plausible, and old pre-Christian beliefs lingered.

Most classic fairy tales stem from Central and Northern European traditions involving Germany's Black Forest, The Ardennes, and Scandinavian boreal forests.

### Q: It's hard to even comprehend how many people are alive today. Can you compare global populations through history to modern day regions?

- 10,000 BCE (start of agriculture): around 4 million, similar to the modern Los Angeles metro area
- 1,000 BCE: around 50 million, or modern South Korea
- 1 CE (height of Roman Empire): around 170-300 million, up to roughly the modern United States
- 1000 CE: around 250-310 million, still roughly up to the modern United States
- 1300 CE: around 400 million, modern European Union
- 1350 CE (post-Black Death): around 350 million, roughly modern United States
- 1500 CE: around 450-500 million, modern European Union + Japan
- 1700 CE: around 600 million, modern Central America plus South America
- 1800 CE: around 1 billion, modern Africa
- 1900 CE: around 1.6 billion, modern China plus United States
- 1950 CE: around 2.5 billion, modern India plus Africa
- 2000 CE: around 6.1 billion, roughly modern Asia
- 2026 CE: around 8.1 billion, present day global population

### Q: In 1 CE, how much of the global population was within the Roman Empire?

The Roman Empire likely had a population of around 45 to 60 million people depending on how borders are defined and what estimates are used. That would put it between 15% and 35% of the world's population.

Han China around the same time had roughly 60 million as well, and the combination of the two could've held nearly half the global population.

### Q: If land area were equally divided for every living human, how much land would each person get?

Every human could get around 7 acres of land, ignoring the fact that not all land is equally useful or productive, and that in practice wild zones are needed for maintaining ecosystems.

For comparison, modern industrial agriculture requires around 0.5 to 2 acres per person to feed a meat-heavy Western diet, although plant-based diets can be grown on 0.2-0.5 acres.

Urban housing and roads only use maybe 0.05-0.1 acres per person, while suburban housing may use over 1 acre.

Some estimates say that an average American uses over 20 acres for their full footprint, including infrastructure for energy, waste management, roads, factories, etc.

### Q: I understand that dogs benefited from eating leftover food from humans, but how did early humans benefit from having dogs around?

Dogs are much better at detecting intruders via smell and hearing. They sleep lightly and serve as a warning system for sleeping humans.

The "cleanup" of bones and food scraps may have reduced disease vectors around a human camp.

Dogs can track prey by scent and chase wounded animals into the open which aids humans in hunting. Some early dogs could retrieve hunted animals that may have died somewhere out of sight.

Of course, emotional bonds and companionship at some point started to reinforce the relationship.

### Q: When were the first photos of Earth from space taken?

The first photo was taken in 1946 by a V-2 rocket launched from New Mexico. It reached an altitude of about 65 miles, just above the boundary of space.

The TIROS-1 weather satellite launched by NASA in 1960 took more comprehensive images of Earth from an altitude of around 450 miles.

The first full-disk image of the Earth (what most would consider "from space") was taken by the ATS-3 satellite in 1967 at an altitude of 22,300 miles.

### Q: How did palm trees end up in California?

They are not native to the region. Spanish missionaries planted date palms at their missions, which were brought from Spain. Spain had imported them even earlier from North Africa. During the late 1800s, exotic plants such as palms were brought to California as the state promoted its image as a paradise. In the 1930s, thousands were planted as part of public works programs.

### Q: What's the deal with Santa Claus, St. Nicholas, and Kris Kringle all being names for the same person? And how does Krampus fit in?

St. Nicholas was a real 4th-century Bishop, known for his piety, generosity, and gift-giving. The name "Santa Claus" is derived from the Dutch Sinterklaas, which itself is a hsortening of Sint Nikolaas. Dutch settlers brought the tradition to America.

Kris Kringle is an Americanization of the German Christkind (Christ Child), a gift-bringer figure introduced by Martin Luther as an alternative to St. Nicholas meant to emphasize the Christ-centericity of the holiday.

Krampus is a figure from Alpine folklore, likely part of winter solstice festivals. Over time he was adapted to act as a kind of "punishing" counter-part to St. Nicholas.

### Q: What is the origin of the American diner and its aesthetic?

The diner originated in the late 19th century as a mobile eatery to serve workers during odd hours. By the 1910s, the concept evolved into stationary but prefabricated structures. Early diners were inspired by railway dining cars. During the 1930s and 1940s, the Art Deco movement added stainless steel, bold lines, and neon accents. The post-World War II boom popularized bright color schemes, vinyl booths, and checkerboard tiles.

### Q: Presumably grid power supply never perfectly matches demand, so where does any "extra" energy go?

Although modern grids may incorporate some energy storage in the form of flywheels, pumped hydroelectric storage, and batteries, in general the system aims to quickly adjust to match demand. A mismatch may manifest as additional heat or divergence from the target frequency (e.g. 60 Hz in the U.S.), but that is not catastrophic.

### Q: Why is "Sino" sometimes used in reference to China?

The term "sino" derives from the Latin word Sinae, which was the Roman name for China. This likely originates from an earlier Greek term, Sinai, which was derived from Sanskrit Cina. The term referred to the Qin dynasty. The Chinese refer to their country as Zhong Guo, which means "middle kingdom".

### Q: What is the relationship between things like Taoism, Buddhism, Confucianism, and Yin-Yang?

Taoism (Daoism) is a Chinese philosophy and religious tradition that emphasizes living with the Dao (the Way), which is "the fundamental principle that underlies the universe". It values spontaneity, naturalness, non-resistance, and balance.

Buddhism originated in India before spreading and being adapted to local beliefs in China. Chinese Buddhism incorporates elements of Taoism, leading to sects like Chan Buddhism which later became "Zen" in Japan. It focuses on enlightenment, impermanence, and the cessation of suffering through detachment from desire.

Confuscianism is a socio-political philosophy founded by Confuscius that emphasizes ethics, hierarchy, duty, and proper behavior. It is less spiritual than the others.

Yin-Yang is a concept from ancient Chinese cosmology that represents dualism: the interplay of opposite but complementary forces. It is not exclusive to Taoism, but it plays a significant role in its worldview. Confucianism and Buddhism also reference yin-yang to explain balance in ethics and the universe.

Taoism and confucianism emerged around 500-200 BCE in response to the social chaos of the Warring States period. Taoism sought to escape from rigid structures while Confucianism sought order within them. Buddhism entered China around the 1st century CE and blended with both. Yin-yang is more of a cosmological principle that all three use to explain aspects of their philosophies.

### Q: Why do I associate "city life" in the 1990s with jazz music?

Jazz had a cultural presence in the 1990s despite not being mainstream. It was used in media as a kind of shorthand for "sophistication and urban cool". You would see it in Hey Arnold, Cowboy Bebop, and Seinfeld to some extent. It was used in coffee culture advertising. Games like SimCity 3000 had jazz-heavy soundtracks, reinforcing the connection between jazz and the cityscape.

### Q: I remember WolframAlpha handling natural language questions long before modern NLP; how did it do this?

It used a highly structured, rule-based approach relying on thousands of handcrafted parsing rules and templates. These rules were designed to capture common ways people might phrase questions in specific domains. It drew on curated databases and knowledge models and used Mathematica as a computational engine to produce results based on that data.

### Q: What does it mean for an animation to be "on 1s" or "on 2s"?

Animation "on 1s" means there is a new drawing every frame while "on 2s" means every other frame repeats. Most often the purpose of this is simply to save time drawing frames on less important parts of an animation and prioritizing detailed frame work on the focal point of an animation.

### Q: What was a "paladin" historically?

In historical contexts, a paladin was a term used to refer to a high-ranking knight, typically of noble birth, renowned for their martial prowess, chivalry, and loyalty to their lord or sovereign. The concept of paladins originated in the medieval period, particularly during the Carolingian era in Europe, and gained popularity through literature, such as the epic poems of Charlemagne and his knights.

Paladins were often depicted as champions of justice and defenders of the realm, embarking on quests to protect the innocent, uphold the law, and fight against evil forces, including monsters, invaders, and rival knights. They adhered to a strict code of conduct, emphasizing virtues like courage, honesty, humility, and honor.


### Q: What is data normalization and denormalization?

Data normalization is the reorganization of data to eliminate data redundancy. It involves breaking a database down into smaller, related tables with each piece of data stored canonically in one place. Denormalization is the opposite -- intentionally introducing redundancy into a database. This may be done to improve the performance of certain types of queries (eliminating costly joins), but must be done thoughtfully or it can lead to data integrity issues.

### Q: What is Redis and how does it differ from Memcached?

Redis (Remote Dictionary Server) and Memcached are both in-memory data storage systems used for caching. Redis supports additional features over Memcached, including a wider range of data structures that can be stored natively, options for persisting data for durability, support for atomic operations, a pub/sub messaging system, and replication/clustering.

### Q: Why is it called "dynamic programming"? A bit vague isn't it?

Dynamic programming refers to the technique of breaking a problem down into simpler problems of the same kind while storing subproblem solutions to avoid redundant calculations. It is primarily approached either top-down with memoization or bottom-up with tabulation.

The term "dynamic programming" was chosen by Richard Bellman apparently for some combination of attempting to sound good to the people who held funding control and to sound impressive more generally.


### Q: What is CORS and how has it influenced browser behavior over time?

Cross-Origin Resource Sharing is a browser security feature that prevents web pages from making requests to a different domain. This prevents a malicious website from quietly making requests to another without the user's awareness or permission.

Browsers initially enforced a strict same-origin policy, but this was quite restrictive. CORS introduces HTTP headers like `Access-Control-Allow-Origin` which allows a server to specify which origins are permitted to access their resources. Browsers enforce this by considering these headers before allowing a request through.

### Q: What are all the things the POSIX standard covers?

- System calls for file I/O, process management, inter-process communciation, and more.
- Standard libraries extending the C standard library for file and directory operations, regular expressions, and memory management.
- Command-line utilities such as ls, cat, grep, and many others.
- Certain shell syntax, functionality, and command-line argument conventions.
- File system hierarchy, including standard directories like /bin, /usr, /etc, and /home.
- A set of standard environment variables including PATH, HOME, and USER.
- An interface (pthread) for multi-threading.
- Specifies how signals are handled by processes, e.g. SIGINT and SIGTERM.
- A standard syntax for regular expressions.
- Specifications for socket-based network programming.
- Functions and data types for time and date.
- User and group account management and permissions (UID, GID).
- Specifications for terminal I/O.

### Q: What are some of the most commonly used non-standard C libraries to add essential functionality?

- GLib provides a wide array of data structures and utility functions
- uthash is a lightweight hash table library
- klib is a small library containing a variety of data structures
- khash is a set of macros and functions for generating hash tables
- C Hash Map is a lightweight hash map library with open addressing and chaining
- Cello is a library that offers object-oriented features in C and includes common data structures
- Judy Arrays are a versatile and efficient data structure library
- PBL is a collection of C libraries that includes common data structures
- CDI is a library that provides data structure and algorithms for various tasks
- C99-Data Structures is a collection of common generic data structures

### Q: Is the placebo effect definitely real and what kinds of effects have been seen?

It is recognized as a genuine biological phenomenon, although the exact mechanisms are not fully understood. Some notable effects observed have been pain relief, influence on psychiatric conditions, immune system response, and motor performance.

### Q: Why did FreeBSD remove block devices while Linux _only_ creates block devices?

Block devices operate on fixed size blocks of data with the OS managing a buffer. Character, or raw, devices are accessed directly by applications with no OS-managed cache. FreeBSD removed block devices in favor of moving caching logic into the filesystem layer (UFS/ZFS). This simplified aspects of the kernel.

Linux instead treats the block device as the primary interface for a disk. This helps enable the OS to optimize I/O in a centralized way via scheduling and read-ahead prediction. If an application like a database wants more direct access, it can use the block device with the O_DIRECT flag which disables caching while still using the same block device interface.

### Q: What are the differences between all the "editions" of Dungeons & Dragons?

- Original (OD&D): Released in the 1970s, it was a relatively simple system that encouraged creativity with rules that were up to interpretation.
- Advanced (AD&D): Released in the late 1970s, it introduced more complexity and detailed rules, classes, and races.
- 3rd Edition (D&D 3E): Released in 2000, it revamped the system with a unified mechanic (the d20 system).
- 3.5 Edition (D&D 3.5E): A revision that addressed balance issues and refind some rules.
- 4th Edition (D&D 4E): Released in 2008, it brought significant changes, emphasizing tactical combat through roles for each class (defender, striker, leader, controller), with powers being a key feature.
- 5th Edition (D&D 5E): Released in 2014, it aimed to streamline gameplay, making it accessible to newcomers while retaining depth. It simplified rules, emphasized storytelling, and introduced advantage/disadavantage mechanics.

### Q: Why do we say something is "byazantine" when it's excessively complicated?

It reflects a historical perception of the Byzantine political, bureaucratic, and administrative systems as complex and intricate. The Byzantine Empire was known for its elaborate court rituals, intricate political maneuvering, and complex administrative procedures.

### Q: How does a UEFI system boot?

- UEFI firmware initializes hardware components, similar to how a BIOS does.
- UEFI provides a more modular and standardized architecture for hardware manufacturers to develop boot-time drivers.
- UEFI systems have a boot manager integrated into the firmware which is more flexible than the legacy BIOS boot sequence.
- The UEFI boot loader is a small program expected to be found in an EFI System Partition (ESP), a special partition on a storage device intended to be bootable. The ESP is identified by a unique GUID and is usually formatted with FAT32.
- UEFI variables are configuration parameters saved in NVRAM, such as the boot device priority order.
- UEFI often supports a Secure Boot feature whereby only signed and authenticated boot loaders and OS kernels are approved to be loaded during the boot process.

### Q: How does SSH establish a connection without leaking information to the public Internet?

SSH uses a secure key exchange, typically Diffie-Hellman or its elliptic curve variant (ECDH).

1. The client sends a "hello" message including information about supported encryption algorithms and exchange methods.
2. The server responds with a "hello" message acknowledging the request and providing its own set of supported encryption and exchange methods.
3. The client and server agree on an exchange method and generate key material to establish a shared secret without transmitting the secret over the network. Diffie-Hellman involves both parties contributing to a generated shared secret without explicitly exchanging it in public.
4. A handshake is done to verify that both parties have generated the same key material.
5. The client and server can then exxchange data securely using keys derived from the shared secret.

The server typically presents its public key to the client during the exchange process, allowing the client to verify the server's identity.

### Q: In the context of cryptography, what is a "nonce"?

The term "nonce" refers to a "number used once" (may also relate to more general uses of the term meaning "something used for now"). It describes a random or pseudo-random number that is generated for a specific purpose and is intended and expected to be used only once within a given context or session. 

Generally, the server generates a nonce and sends it to the client as part of a communication protocol. The client uses it as instructed within the protocol, for example as part of signing a request. The server checks to ensure that the nonce has not been used previously in the same context or session and can reject the request if it has. To achieve this, the server typcially maintains a record of nonces that have been used within the current session.

### Q: What is the origin of the phrase "winner winner chicken dinner"?

Unclear, but it may have originated in Las Vegas casinos in the mid-to-late 20th century when a typical payout at some tables matched the cost of a casino meal, which was often a chicken dinner.

### Q: What is the difference between Marxism and Communism?

Marxism is a socio-economic and political theory emphasizing the role of class struggle and the eventual establishment of a classless society. Communism is a political and economic ideology that advocates for a society in which the means of production are commonly owned and the distribution of wealth is based on the principle of balancing ability and need. In other words, Marxism is a broader theoretical framework while communism is a specific socio-economic system that is considered the ultimate "stage" in Marxist theory.

### Q: Why did primates evolve to have flatter faces than other animals?

It is an adaptation to an arboreal (tree-dwelling) lifestyle. Flatter faces provide a broader field of binocular vision which helps in accurately judging distances while navigating through branches; better depth perception.

### Q: Why did Hollywood become the place that movies are made?

1. The sunny and consistent weather allowed for year-round outdoor filming, especially important for early cameras that required bright light.
2. Proximity to diverse scenery such as deserts, mountains, and beaches.
3. Distance from Thomas Edison's Motion Picture Patents Company on the East Coast, offering some protection from patent restrictions.

### Q: When a photon hits a transparent window, is the photon that emerges on the other side the "same" photon?

Identity is not necessarily straightforward in the subatomic world. In a simplified physical model where photons are particles, a photon is emitted on the other side after a chain of interactions, absorptions, and energy transfers, and so in that sense it is not really the same photon.

However, from the perspective of Quantum Field Theory, there is one universal "photon field" with localized ripples rather than "little billiard balls", and in that sense photons are fundamentally indistinguishable. If you have two photons A and B, there is no physical experiment that can tell you which is which after an interaction and so the concept of identity has little meaning.

### Q: Why do private vehicles not use diesel if it is a more efficient fuel?

Diesel vehicles are typically more expensive due to their robust engines that handle higher compression. In some countries, diesel fuel is also taxed more heavily than gasoline.

Diesel engines are most efficient during long, steady drives. Private vehicles often make short trips with frequent stops which reduces the efficiency benefits of diesel. Diesel engines take longer to warm up, again making them less appropriate for short commutes.

While diesel engines produce less CO2, they emit more nitrogen oxides and particulate matter which reduces air quality. Emission regulations have made gasoline more attractive for private buyers.

Gasoline engines generally provide smoother acceleration and quieter operation which appeals to many private buyers. Public perception of diesel as being something dirty for commercial or utility vehicles further influences private buyer choices.

### Q: What do the "dot product" and "cross product" of two vectors represent?

The dot product is a scalar value measuring how much one vector extends in the direction of the other. If two vectors are perpendicular, then their dot product is zero and if they are parallel then their dot product is maximized. In other words, it is a measure of "how parallel" or "how perpendicular" two vectors are.

The cross product produces a third vector that is perpendicular to both of the other vectors. It is useful for finding the normal vector of surfaces, computing torque, and determining rotational direction.

### Q: What is the distinction between absurdism and nihilism?

Both confront an apparent meaninglessness of existence, but interpret and respond to it differently. Nihilism says there is no inherent meaning, value, or purpose in the universe and does not take the idea further than that. Absurdism incorporates the idea that there is a human desire for meaning despite the lack of a universal meaning, and emphasizes the absurdity of that conflict. Where nihilism surrenders to the meaningless in a way, absurdism is more like an acknowledgement, observation, and possibly defiance.

### Q: What was the "environment of evolutionary adaptation" for humans?

The details are still a subject of debate, but it is generally believed to span from about 200,000 years ago to roughly 10,000 years ago. During the EEA, humans were primarily hunter-gatherers, relying on foraging for food rather than agriculture and settled societies. The period was characterized by a nomadic lifestyle and various environments, including savannahs, forests, and costal regions.

1. Hunter-gatherer lifestyle required mobility and skills such as tracking, tool-making, and knowledge of the local environment.
2. Small groups consisting of extended family or bands of related individuals. Cooperation and bonding were crucial for survival.
3. Bipedal locomotion enabled efficient travel over long distances and a larger brain enabled complex problem-solving and social interaction.
4. A diverse and adaptable diet involving meat, fish, fruits, vegetables, nuts, and roots.


### Q: How does a generative image model work?

A massive dataset teaches the model relationships between image data and text descriptions.

When prompting, the text is transformed into a point in a "latent space". This is a high-dimensional, mathematical "space" that captures relationships between various image features that have been learned.

Most commonly, models use a diffusion process to generate an image based on the prompt. This involves starting with random noise and iteratively refining the image toward one that aligns with the prompt's associated region of the latent space.

### Q: To what extent are language models and image models similar?

Both types of models often use the same kinds of neural network models with a transformer architecture. They both rely heavily on pre-training with massive amounts of data to establish reasonable baseline performance.

Both models learn to map input data into a high-dimensional latent space where related concepts or features are located near each other.

Language models must track dependencies over long sequences, but they are ultimately working with a linear structure. Images are far more complex due to the spacial nature and the higher dimensionality of the output (height x width x color channels).

In language models, the "attention" mechanism of a transformer architecture helps the model focus on the most relevant parts of the input sequence as it generates output tokens. In image models, the attention mechanism is more spatially oriented, tracking relationships between different parts of the image.


### Q: What are "unified shaders"?

The unified shader model refers to the shader model found in modern GPUs. Prior to their introduction, GPUs used a largely fixed rendering pipeline where each stage was handled by different specialized units. With unified shaders, shader cores on the GPU are flexible and not dedicated to a particular function; they are "unified". This means the cores can be better allocated and utilized for the specific needs of a given application.

### Q: What is meant by "deferred rendering"?

Deferred rendering is a technique that attemps to reduce the raw compute needed to render a scene with complex lighting. More traditional rendering techniques such as forward rendering require performing lighting calculations for each individual object or light source which scales poorly for complex scenes. In deferred rendering, computations are done per-pixel, and so the amount of computations is pinned more to a fixed, unchanging resolution regardless of scene complexity.

The process has two stages. First, the geometry stage renders the geometry in the scene to several buffers that capture different attributes, for example diffuse color, normals, and material properties (often in the form of a numeric identifier). This set of buffers is collectively called the G-buffer. Then, in the shading stage, the lighting and shading calculations are performed based on the G-buffer.

One drawback of deferred rendering is the increased memory requirements of the G-buffer as output resolution grows. Another is that traditional MSAA blurs the image instead of only softening edges because of the way that the G-buffer interacts with that process.

### Q: What is "tile-based deferred rendering"?

Traditional deferred shading can be computationally expensive due to the large number of pixels processed in the lighting pass. Tile-based deferred shading divides the screen into smaller tiles and the lighting pass is done per-tile rather than per-pixel. A per-tile light list contains the necessary data for lighting calculations in that tile. This reduces the raw amount of lighting calculations needed by a factor of how large the tiles are, and it enables efficient memory access patterns where related light information lives together per tile.

### Q: What is "global illumination"?

In traditional rendering, direct illumination is typically calculated by considering only the light sources and their direct paths to the objects in the scene. However, this ignores the indirect lighting effects caused by light bouncing of surfaces. Global illumination techniques aim to model these indirect lighting effects.

Ray tracing is a widely used technique for global illumination where light rays are simulated by tracing them from the camera throughout the scene. It can be physically accurate but computationally expensive.

Radiosity is a method that divides the scene into small patches and calculates energy transfer between them. It can accurately simulate diffuse inter-reflections, but it may not handle other effects like glossy surfaces or caustics.

Photon mapping is a two-pass technique where photons are traced from light sources and then used to estimate the lighting at different points in the scene. It can handle effects like caustics.

Path tracing traces light rays through the scene while using random samples to estimate the light contribution at each point. Like ray tracing, it can be computationally demanding but can produce physically accurate results.


### Q: What are spherical harmonic probes?

SH probes are a technique for capturing and representing lighting information in a scene. They are a compact representation of functions defind on a sphere, such as lighting environments or light intensities.

Lighting information for a particular environment or scene is "captured" and encoded into a compact form using spherical harmonic coefficients. These represent the distribution of lighting across the spherical harmonics.

Spherical harmonics are analogous to the harmonics in one-dimensional waves, but extended to a sphere. By using these harmonics, it becomes possible to capture and represent lighting information using a low-dimensional set of coefficients.

### Q: What is SSAO?

Screen-Space Ambient Occlusion is a technique to approximate the ambient occlusion effect in graphics. This is a phenomenon where surfaces close to each other (like the corner of a room) receive less ambient light due to the blocking effect of nearby objects.

SSAO estimates the occlusion of each pixel in the image based on its surrounding geometry in screen space. Instead of calculating occlusion in the full 3D scene, SSAO operates on the final rendered image.

SSAO often operates on the G-buffer used in deferred rendering. For each pixel, the depth values from the G-buffer are used to reconstruct the 3D position at that point. By comparing with the depth of surrounding samples, an occlusion amount can be estimated. The occlusion value is often used to darken the original color of the pixel.

### Q: How did the legacy fixed-function pipeline in OpenGL operate?

In versions of OpenGL prior to 2.0, vertices went through a series of fixed stages:

1. Vertex data was provided as position ,color, texture coordinates, and normals.
2. The vertices were transformed by the modelview and projection matrices to bring the vertices into view space and then screen space. Lighting calculations like diffuse and specular lighting were applied to the transformed vertices using fixed light positions and material properties.
3. The primitives were clipped against the view frustum to discard portions of geometry outside the visible region.
4. Assembled primitives were rasterized into fragments based on screen coordinates. This determined which pixels were covered by a given primitive and generated fragment position, color, texture, coordinates, and depth.
5. If textures were enabled, the rasterizer would apply texture mapping to the fragments. This involved interpolating texture coordinates across the primitive and sampling textures to determine the texture color.
6. Fragments underwent depth testing, stencil testing, and blending.
7. The resulting fragments were written to the final framebuffer.


### Q: How do games deal with transparent objects?

One approach is to sort and render objects such that those farther from the camera are rendered first. This ensures that closer transparent objects correctly blend with those rendered behind them. This sorting can be done per-object, per-triangle, or per-pixel. This opposes the "typical" rendering order where objects are rendered front-to-back such that occluded objects are ignored.

Depth peeling is a technique for scenes with complex overlapping transparent objects. It involves multiple rendering passes to peel away layers of transparent geometry and resolve the order of blending correctly. Each pass renders a subset of transparent objects with depth values of previous objects stored and used to determine the correct rendering order.

Order-independent transparency techniques aim to overcome a need for explicit sorting by using different data structures or algorithms to maintain transparency information for correct rendering.


### Q: What is a "skin mesh"?

A skin mesh, skinned mesh, or skeletal mesh, is a mesh often used to represent character models. It consists of a combined base mesh and skeletal rig. The base mesh contains the static geometry of the character. The skeletal rig is a hierarchical structure of interconnected bones or joints that define the character's underlying skeletal structure, with each bone or join associated with a specific region of the character mesh.


### Q: What are the advantages of forward rendering?

Forward rendering is generally more efficient and better leverages graphics hardware for scenes with a moderate number of lights or scenes where the number of lights affecting each pixels is relatively low. It has a lower memory footprint than deferred rendering as it does not need to store per-pixel information in intermediate buffers.

Forward rendering benefits from early depth testing. By depth testing as early as possible, occluded objects don't need to be processed.

Forward rendering handles transparency more naturally than deferred rendering.

Forward rendering has a more straightforward pipeline that allows for greater control and customization of the rendering process by providing direct access to per-pixel lighting calculations and shading models.

Forward rendering can be enhanced with so-called Forward+ rendering techniques whereby screenspace is divided into tiles or clusters and performing light culling and shading calculations only on relevant tiles, allowing forward rendering to handle more complex lighting scenarios.

### Q: What are the various techniques for rendering shadows?

Shadow mapping renders a depth map, known as a shadow map, from the perspective of the light source. During final rendering, each fragment is compared with its corresponding position in the shadow map to determine if shadowing should be applied. It can support both hard and soft shadows using techniques such as Percentage Closer Filtering (PCF) or variance shadow mapping.

Shadow volumes use the stencil buffer to determine whether a fragment is inside or outside a shadow volume. The volumes are generated by extruding the silhouette edges of occluder geometry in the direction of the light source. The stencil buffer is then used to count the number of times a fragment's depth is incremented or decremented, indicating whether it's inside or outside the shadow volume. They can handle hard and soft shadows, self-shadowing, and dynamic objects, but can be computationally expensive.

Stencil shadows are an alternative to shadow volumes where geometry is not extruded. Instead, depth values of the occluder geometry are used to create a silhouette in the stencil buffer. Fragments are compared against the stencil value to determine if they are inside or outside the shadow. They are generally faster than shadow volumes and can support hard and soft shadows, but may not support self-shadowing.

### Q: Why are "self-shadows" a distinct problem from shadowing in general?

In shadow mapping, which is the most common real-time shadowing method, the scene is rendered from a given light's point of view and depth is recorded. This is fine for capturing unambiguous cases of an object being further "behind" another object that casts a shadow. However, when considering whether a given object casts a shadow on itself, floating-point precision limits become a problem. They can lead to various artifacts like streaks, speckles, flickering, etc.


### Q: What developments allowed for real-time raytracing in recent years?

NVIDIA introduced RT Cores in 2018, specialized units designed to accelerate Bounding Volume Hierarchy (BVH) traversal and triangle intersection tests. BHV is used to eficiently find which objects a ray intersects. BHV is a tree structure that groups objects into bounding boxes.

Even so, it isn't that full scenes are being raytraced. The scene still uses traditional rasterization but adds more accurate reflections, shadows, global illumination, and ambient occlusion using raytracing operations.

Raytracing produces noisy images when limited samples per pixel are used. AI-based denoising enabled more accurate, smoother final images with limited samples.

Similarly, AI-based upscaling via DLSS or FSR allowed games to render to a lower "native" resolution, offloading more raw compute power for raytracing operations.


### Q: How does raytracing fit into the existing rasterization pipeline?

Raytracing introduces new shader types, including:

- Ray generation: launches rays and defines what to compute when they hit or miss.
- Intersection: defines how rays interact with complex geometry like curves.
- Any-hit: runs whenever a ray hits geometry and can decide whether to continue or terminate the ray (e.g. for transparency).
- Closest-hit: runs at the closest ray intersection and determines final color, material, lighting, etc.
- Miss: handles rays that don't hit anything (used for skyboxes, backgrounds, etc.).

### Q: How are "decals" (e.g., bullet holes) typically implemented?

Often times, both historically and in modern engines, it is simply a piece of textured geometry offset very slightly from a surface.

In games that use deferred rendering, they may be volumetric geometry that influences the G-buffer (modifying normals or other attributes).

In some cases, such as for persistent effects on terrain, texture "splatting" maybe used where by textures are truly modified at runtime and "painted" over.

### Q: What is the point of "premultiplying alpha"?

Premultiplied alpha makes compositing mathematically simpler, more stable, and more efficient. Many compositing operations (additive effects, particles, glow, etc.) behave much more naturally with premultiplied alpha.

A useful way to think about premultiplied alpha is that the RGB already represents the amount of light the pixel contributes; it stores "emitted light" instead of "color + opacity".

The representation is more physically meaningful. Without premultiplied alpha, RGB can be any value while alpha is zero, which doesn't "mean" anything since a fully transparent pixel's color is irrelevant. With premultiplied alpha, RGB must be zero when alpha is zero. After premultiplication, the 4 channels behave more uniformly: scaling brightness multplies all four channels, fading multiplies all four channels, and interpolation works correctly. Before premultiplication, the alpha channel is somewhat independent of the others.

Premultiplying alpha does not mean the alpha channel becomes unnecessary, though. It still controls how much of the destination/target image should be visible when blending.

### Q: How do "living world" games like Skyrim or S.T.A.L.K.E.R. simulate AI for NPCs that are distant?

They don't truly simulate distant NPCs the same way they simulate the ones nearby that can be seen. They only need to make sure what the player sees appears consistent at the time that they see it.

For NPCs in other parts of the world, the real-time AI is replaced with various other approaches:

- Behavior state machines with time-based transitions.
- Random event resolution: instead of simulating full combat, the results may be decided by "dice rolls" and high-level statistics about the groups involved.
- Coarse position updates: NPCs may "teleport" between key points based on elapsed time.

These systems often don't update every frame. They run on a schedule of seconds or minutes, or they may perform a batch of updates when the player moves to a new location.


### Q: When RTS games moved from 2D to 3D, they often appear to have dropped the concept of a fixed grid at the same time. How does that work?

The world is primarily modeled on continuous world coordinates while grids and spatial partitioning structures serve as coarse ways of looking up what exists in particular areas; structures like uniform grids, quadtrees, or BVH and KD-trees in games that truly operate in three dimensions.

Buildings typically have bounding volumes; when attempting to place one, the terrain is evaluated to determine if it's flat enough, and collision tests are done against nearby existing structures.

Pathfinding moves beyond grid-based A-star and onto navigation meshes (navmeshes). A navgmesh is a representation of walkable areas as polygons. Obstacles carve holes in that mesh. A-star can still be used for finding a path, but it operates on a variable-cost navmesh rather than a fixed-cost grid. Geometric "cutting" operations can be used to cut a building footprint out of such a navmesh.

Triangles are trivial to split against a convex shape. In practice, though, buildings may be treated as "dynamic obstacles" rather than navmesh edits. The navmesh may reflect only the static terrain while the existence of buildings and units only operate on a runtime obstacle "mask" of nodes in that navmesh.

The high-level approach for convex clipping is the Sutherland-Hodgman algorithm. This can, however, leave non-convex leftovers that need to be accounted for.

### Q: How did HTML change up through HTML5?

HTML 1.0 was standardized in 1991. It had headings, paragraphs, lists, and links, but no support for images or tables and styling was limited (no CSS).

HTML 2.0 in 1995 introduced tables, images, and forms. It also introduced the script tag.

HTML 3.2 in 1997 introduced styling elements like font and center. Support for frames was added. The concept of CSS was introduced, but support was limited and inconsistent.

HTML 4.01 in 1999 refined CSS support and introduced div and span for controlling document structure. It also added more form input types like checkboxes, radio buttons, and text areas.

XHTML 1.0 in 2000 was a reformulation of HTML 4.01 as a strict XML specification. However, the strict XML syntax requirements would not carry forward in HTML5 as backward-compatibility with existing web content was prioritized.

HTML5 in 2014 introduced major changes and features. It added semantic structural elements like header, nav, article, and footer. Multimedia support was added via the video and audio elements, reducing the need for multimedia plugins. Canvas and SVG elements allowed for dynamic and interactive graphics and animations. Input types were added to forms along with form validation. Local storage and offline cache APIs were added. APIs for geolocation, drag-and-drop, and web workers were added.

### Q: What is a Red-Black tree and how does it work?

A Red-Black tree is a type of self-balancing binary search tree, continually keeping the height of the tree from growing more than necessary. Each node has an associated color attribute. The root is always black. Red nodes cannot have red children (and thus a red node also cannot have a red parent). Every path from a node to its descendant leaves must have the same number of black nodes. This ensures the longest path from the root to a leaf is no more than twice the length of the shortest path.

### Q: What is a heap and what are its interesting properties?

A heap is a specialized tree data structure. Commonly, a heap is either a min-heap or a max-heap, where the value of a given node is less than or greater than the values of its children respectively. Extracting the minimum or maximum value of these structures is guaranteed to be a constant-time operation since it will always be the root element. Heaps are commonly used to implement a priority queue where elements can be added and then retrieved according to some ordered property. However, unlike a binary search tree a heap is not a sorted data structure. The root is guaranteed to hold the minimum or maximum value, but the structure is not entirely sorted beyond that (no ordering between sibling nodes).

Inserting an element into a heap involves appending the element and then running a "heapify" operation.

Extracting the root element (minimum or maximum) is similarly done in constant-time, followed by a "heapify" operation.

The heapify operation typically involves swapping elements and recursively adjusting the tree structure from the root to the leaves or vice versa until the heap order property is restored.

### Q: What are radix sort and bucket sort?

Radix sort is a non-comparative sorting algorithm specifically for integers. It processes the digits of an integer in order, distributing integers into buckets based on their digits. It has a time complexity of O(kn) where k is the maximum number of digits allowed. If k is relatively small, then radix sort can be very efficient. It is suitable for sorting integers with a known, limited range of values.

Bucket sort is a more general sorting algorithm that also involves the use of "buckets". Input values within a known range are distributed across ordered buckets. Typically, the buckets are then sorted using some other sorting algorithm. The sorted buckets are then concatenated to produce the final sorted result. It is suitable for sorting data with a uniform distribution across a known range, such as floating-point values within a known range. The performance depends on the specific data and implementation, but on average a bucket sort can aim to achieve linear time complexity.

### Q: What information is a Git commit ID derived from?

A Git commit ID is a hash of the commit object, typically SHA-256. A commit object contains:

- The tree object (snapshot of the directory at that commit)
- zero or more parent commit IDs
- author name, email, and timestamp
- committer name, email, and timestamp
- optional extra headers
- the commit message

Thus, if any of these things are changed (e.g. via amending the commit), the commit ID hash will change.

### Q: My mental model of a "git commit" is that it's defined by a diff. How should I think about it?

Because a commit most often has a single parent associated with it, it is not uncommon to think of a commit as capturing a diff. However, a commit is not a diff. It is a pointer to a tree that captures a snapshot of the entire repository. When you "commit", git writes a tree object representing every file and directory, and the commit stores a reference to that tree along with parent commit IDs and other metadata.

A diff only exists when you pick two of these snapshots to compare; there is no diff that represents a single commit by itself. If a commit has one parent, then naturally a diff against that parent is a useful representation of the commit.

A commit can have more than one parent when histories are joined, such as when a branch is merged. A merge commit can have multiple parents (one in each branch involved in the merge, usually two). In that case, the diff associated with the merge commit is more ambiguous, especially if the merge involved conflict resolution. If the merge includes changes for conflict resolution, a diff against either parent branch will be non-empty, but it won't be the same diff.

### Q: What exactly is a "pull request" in the context of Git?

It's not a feature of Git but rather a collaboration feature of platforms like GitHub. It bundles review, discussion, and possible merge into a formal process. The term comes from the idea that "I have work in my branch and I want you to pull it into yours".

The request is usually defined by a source branch, a target branch, the commits reachable from the source but not the target, along with associated comments, approvals, automated checks, etc.

### Q: What are the different "signals" that can be sent to a process on Unix-like systems?

- SIGTERM (15): It asks the process to terminate gracefully, giving it an opportunity to cleanup and finalize.
- SIGKILL (9): This forces the process to terminate immediately.
- SIGHUP (1): Typically used to instruct a process to reload its configuration files.
- SIGINT (2): Sent via Ctrl+C in the terminal. It's meant to interrupt the process, which may be treated similarly to SIGTERM but not ncessarily.
- SIGQUIT (3): Similar to SIGINT, it's often used to generate a core dump for debugging.
- SIGSTOP (19) and SIGCONT (18): SIGSTOP pauses a process while SIGCONT resumes a paused process.
- SIGABRT (6): Often used by the process itself when it detects a critical error. It can be handled, but the default action is to terminate and generate a core dump.
- SIGALRM (14): Generated when a timer set by the `alarm()` function expires. IT is used to handle timeouts or delays in a program.


### Q: What should be considered when choosing between serverless computing and traditional fleets?

Severless is great when the workload is unpredictable or very dynamic. The pay-as-you-go pricing model can be very effective when applications have sporadic usage. Serverless platforms enable faster development and deployment since infrastructure setup, configuration, and maintenance are minimal. On the other hand, serverless platforms come with a degree of vendor lock-in and less configuration flexibility.

Traditional server fleets offer more control of the underlying hardware and software stack. Because they can be left in a running and available state at all times, they can fulfill more stringent latency requirements and offer more predictable performance. They are capable of maintaining state between requests. Even for a generally stateless service, local cache layers that persist between requests may be beneficial.

### Q: What's the deal with fullscreen behavior on Windows?

Windows has two fullscreen modes. True "exclusive fullscreen" involves the game bypassing the Windows compositor (DWM). This often means better performance and, perhaps more notably, lower latency. The downside is that switching back to the Windows desktop can be slow and disruptive, particularly with older games using Direct3D 9 through 11.

Alternatively, a borderless window can be used to display the game fullscreen. In that case, the compositor is not bypassed. This means switching to other windows is just as smooth as any other application, but it can introduce input lag and slightly worse performance that some users don't tolerate.

Windows 10 and 11 introduced Fullscreen Optimizations (FSO) which attempts to combine the best of both worlds for games running in exclusive fullscreen, but some users still complain about latency or other quirks.

### Q: Does Linux have an "exclusive fullscreen" mode?

Technically, but not in the exact same way as Windows. Neither X11 nor Wayland allow an application to take full control of the display. Some compositors support bypass of compositing for fullscreen windows which can offer better performance similar to exclusive fullscreen.

It is possible to run in a GPU-level exclusive model via DRM/KMS, but it requires that the application run outside the context of a windowing system.

### Q: Are microservices still "in vogue" (2025)?

They are widely used, but the hype has cooled and alternatives are common.

Microservices are used more pragmatically. People have felt the pain of latency, complexity, cross-service coordination, and versioning issues.

"Modular monoliths" are making a comeback -- monolithic services with clear internal boundaries and responsibilities. This provides the simplicity and performance benefits of a monolithic service while still allowing for logical separation or transition to multiple services later.

Serverless / Function-as-a-Service (FaaS) emerged as an alternative -- breaking logic into event-driven functions while avoiding infrastructure management.

Event-Driven architectures -- instead of REST-only APIs, services communicate via events (e.g. Kafka). It can lead to looser coupling and more resilient systems at the cost of harder debugging, eventual consistency, or a more complex mental model.

### Q: Very generally, how do search systems like Lucene work?

Systems like Lucene use an inverted index to efficiently find which documents contain given keywords.

During the indexing phase, Lucene scans each document, tokenizing text into individual terms, optionally applying stemming, lowercasing, stopword removal, etc. For each term, it records the list of documents that contain that term, called a "posting list". Optionally, Lucene can store positions and frequencies of words that appear.

During the query phrase, the given search keyword is looked up in the inverted index. The list of associated documents is often sorted or scored using something like TF-IDF or BM25.

Once candidate documents are found, they are scored based on term frequency, how rare the terms are in general (inverse document frequency), field boosts, document length normalization, etc.

### Q: I understand what a lambda is in Python or C++, but what exactly is "the lambda calculus" and why does it matter?

The lambda calculus is a system that shows how computation can be done using only functions and function application. In other words, it is a language consisting of only variables, function abstractions, and function applications.

It's significant because it's Turing complete and shows that computation in general can be done via functions and function application -- no loops, stateful variables, control structures, etc.


### Q: What's the deal with libstdc++ and libc++, particularly on macOS?

Historically, libstdc++ was the default standard library implementation used with GCC. Conversely, libc++ is the implementation associated with LLVM and Clang. After Apple transitioned to using Clang as the default compiler, libc++ became the default.

### Q: What is the history and purpose of the /opt directory?

Short for "optional", the directory was intorduced to provide a location for packages that are not part of the default OS installation. Software installed in opt is often self-contained with its own directory structures, libraries, and resources.


### Q: What are all the different terminal color "modes" or standards?

ANSI escape codes allow setting text foreground, background, "bright" foreground and "bright" background colors according to indices associated with 8 possible pre-configured colors each.

8-color mode supports 4 text and 4 background colors, limited to a set of common colors.

256-color mode using ANSI escape codes to set text foreground and background colors to a palette of 256 pre-configured colors.

TrueColor mode allows fully specifying 24-bit RGB values via ANSI escape codes.


### Q: What are the simplest solutions to the problem of packing rectangles?

First-Fit Decreasing Height (FFDH) whereby the rectangles are sorted by height in descending order and placed on the first "shelf" where it fits. A new "shelf" is started if the next rectangle can't fit on the current shelf.

Best-Fit Decreasing Height (BFDH) whereby rectangles are sorted by height in descending order and placed in the shelf where it leaves the least amount of unused space.

Bottom-Left (BL) whereby rectangles are sorted in some way (e.g. height or area) and then placed in the bottom-most, left-most position where it can fit. Choose the left-most option when multiple positions are possible.

Guillotine Cut algorithms whereby remaining free space is recursively split after placing each rectangle:
- Choose a rectangle and place it in a corner, e.g. bottom left.
- Split the remaining space into two parts horizontally and vertically.
- Recursively apply the same operation to the remaining space.


### Q: Why is C sort of the "lingua franca" of programming languages?

Partly historical precedence. It is old an influential, with many modern languages having been designed or influenced by compatibility with C which further reinforces that entrenched compatibility expectation.

C has a relatively simple and well-defined ABI, making it easier for languages to interface with compiled C code.

C provides low-level memory manipulation capabilities that are missing in higher-level languages. In other words, few popular languages could fill the role of being a foundation the way C is.

### Q: Why have web technologies evolved to be a kind of "universal platform" rather than something purpose-built for that goal (e.g. JVM)?

The web had three structural advantages over efforts like the JVM: instant distribution, universal runtime availability, and decentralized evolution.

To run a Java Applet, the user had to navigate somewhere in their browser, possibly install or update a secondary Java plugin, download the application content, and then run it. Even that relatively low amount of friction couldn't compete with the use of features built into the browser and delivered with the web page content seamlessly. Distribution friction turned out to be very important in practice.

Browser development involved a tension between introduction of features and maintaining compatibility. This resulted in experimentation followed by open standardization, allowing further evolution along standardized interfaces. This won out over something like the JVM which had been owned and developed by one centralized party.

This follows a common pattern where the most widely deployed runtime becomes the "universal platform". If someone visited your web application, it was guaranteed they had a browser, so targeting the browser itself made sense when possible. They may or may not have had other software, like a JVM plugin or Flash installed.

### Q: What are some guidelines for the point when highly composed or compact code hurts readability instead of helping it?

Compact code can aid readability when each function has a clear and understandable responsibility, e.g. `users.filter(isActive).map(toDisplayName).sort(byLastName)`, follows a standard, well-known pattern, and there are minimal branches or side effects embedded within.

Compact code can hurt readability when the functions being composed are too abstract, anonymous, or nested, e.g. `doSomething(f(g(h(x))))`, side-effects or context changes are embedded within, or when intermediate values are useful for understanding and debugging key steps.

The line is wherever mental unpacking outweighs perceived elegance. Some rules of thumb might be 3-5 functions in an intuitive pipeline and no more than 2-3 levels of nesting.

### Q: What are the roces behind the fact that JavaScript became popular well beyond its original frontend scripting domain?

1. The ubiquity of the browser runtime (and therefore JavaScript) as a platform.
2. Developer consolidation and hiring economics. Companies prefer to hire generalists, and if the frontend is unavoidably JavaScript, it makes sense to write back-end systems in JavaScript as well.
3. NPM grew to be a giant package repository and tooling like Electron, React Native, and WebAssembly allowed JavaScript to run across various non-browser environments.
4. Modern JS runtimes allowed JavaScript performance to be "good enough" for most use cases.
5. Writing software as a webapp is of the path of least resistance due to browser ubiquity and frictionless distribution.

### Q: What's the dela with "range queries", query types 1 and 2, and "difference arrays"?

This refers to a particular category of algorithm involving modifying and querying values in an array efficiently.

Query Type 1 (Point Update or Range Update) modifies or adds values in a specified range of indices. For example, add "x" between indices "l" and "r".

Query Type 2 (Range Query) typically involves computing some function, like a sum or max, over a range of indices.

A difference arrays is a secondary array that can be leveraged to handle these updates and reads efficiently. A difference array is created that captures the difference between consecutive elements of the primary array. To, for example, increment all values, one would most naturally need to walk through and increment every relevant value in the primary array. When using a difference array, one would instead just modify the "difference" value at the left and right boundary of the range (two modifications). The appropriate value for the original array can then be recovered by taking the prefix sum of the difference array. This makes sense to do when there are many update operations relative to reads (imagine a task involving incrementing various large ranges of an array). It reduces a linear update operation to a constant-time one.

### Q: What's the deal with COM and OLE in Windows programming, and are there equivalents on macOS or Linux?

COM and OLE are Microsoft's way, especially historically, of enabling interprocess communication, code reuse, and language interoperability. COM provides a binary interface standard that can enable cross-language integration, and allow processes to communicate, even over a network via DCOM. OLE started as a way to embed objects (e.g. inserting an Excel sheet into a Word document), which further generalized to COM and evolved into more modern architectures like .NET.

Objective-C's runtime provides dynamic object messaging between Objective-C and Swift which supports some of what COM aims to achieve but with less language agnosticism. Similarly, CoreFoundation and CoreServices handle modular component interaction.

D-Bus on Linux is used for interprocess communication, but is more focused on system services. GObject is similar but primarily for use with C and GTK.

### Q: I get the sense that COM, at the time, was meant to be a bigger thing than it became. What happened?

It was designed as a kind of grand unifying framework for software components, but didn't catch on outside of Microsoft's own products and system-level APIs. It was notoriously difficult to work with directly -- the manual reference counting, interface querying, and need for IDL files made it cumbersome.

While COM was meant to be language-agnostic, its design was very C++-centric. Outside of Microsoft, most developers didn't see a strong reason to adopt COM when they could just use DLLs, shared libraries, and other cross-platform solutions. COM was also not designed with cross-platform compatibility in mind because, at the time, Windows was so dominant in the desktop software space.

### Q: What and when was the first C compiler?

The original C compiler was developed in the early 1970s, initially for the PDP-11. Over the years, it was updated to support more architectures and was named the Portable C Compiler, PCC. In the mid-1980s, the GCC C compiler was created and widely adopted.

### Q: What are the GNU extensions to the C standard?

- Statement expressions allow you to execute blocks of code within an expression, e.g. `int x = ({ int y = 3; y + 2; });`.
- Nested functions allow the definition and use of a function within the scope of another (similar to Python).
- The address of a label can be used as a value and jumped to dynamically.
- Variable-length arrays inside structures.
- Designated initializers, although this was standardized in C99.
- GCC allows inline assembly within C.
- GCC provides attributes to control certain things about functions, variables, or types, e.g. `__attribute((packed))__` to disable padding bytes.
- `typeof` can be used to get the type of an expression.
- Numeric ranges in a case statement.
- Zero-length arrays in structures.
- Extended integer types like `__int128`.


### Q: Are there any features in modern C that are missing from modern C++?

- Variable-Length arrays (VLAs). C++ does not support VLAs; instead, a vector or other standard library container would be used.
- C99 has the `restrict` keyword which indicates that a pointer is the sole reference to an object and tells the compiler to assume no pointer aliasing. Some C++ compilers may support `__restrict__` as an extension.
- C99 supports designated initializers where struct fields can be initialized using their names. C++20 introduced a form of designated initialization, but the rules differ slightly.
- C retains implicit `int` type for function declarations which is invalid in C++.
- C99 supports flexible array members where the last member of a struct can have an unspecified size.
- C99 supports compound literals. C++ can achieve similar functionality through the initializer list type.
- C99 supports macros with variables arguments via `__VA_ARGS__`.


### Q: Why has aspect-oriented programming apparently had very limited adoption?

AOP hides behavior and clashes with standard debugging tools. It often relies on weaving to inject behavior such that the runtime code does not exactly reflect the source.

AOP often requires integration into the build pipeline, adding complexity and breaking the "standard" build steps one would expect.

While AOP is useful for certain cross-cutting concerns like metrics in an effort to keep the business logic clear, the use cases are somewhat limited and may not justify the complexity of adding AOP to a project.

Functional programming idioms like second order functions and monadic constructs can be used to address cross-cutting concerns with less "magic".

Mainstream languages emphasize explicitness and simplicity. A language could integrate AOP as a first-class feature, but it would need to embrace the idea that implicit behaviors are acceptable. There are patterns such as decorators and functional techniques that reduce the relative value of introducing AOP.

In other words, AOP sounds nice but in practice the complexity it introduces has not been found to be worth it for the limited use cases.


### Q: I was always taught singletons are bad, so why do we seem to accept singleton logging interfaces?

Logging is a cross-cutting concern, so it does make some sense for it to be accessible anywhere without requiring passing references around. It is also something that generally benefits from centralized configuration and consistent logging behavior across an application.

It does have downsides, though. Unit tests may fall back to default logging behavior unless they are appropriately configured. It can be more difficult or awkward to customize logging behavior for a specific section of the application.

The biggest factor, though, is probably that logging is one-way. There is not really problematic global state, which is the issue that singletons may introduce. A logging interface is simply an output sink; writing to the log should never impact any other part of the system.

### Q: Another thing I often see that feels counter to best practices is context objects. Do they not violate design guidelines?

Context objects typically serve to reduce the number of related objects or values passed around and to keep function signatures from growing. They are not inherently bad but should be used with clear intent. When multiple pieces of information are highly related and multiple layers of the system need access, context objects make sense and serve to reduce the size of function signatures and number of changes required to change or add to that set of related information. They are particularly useful for passing read-only configuration information, scoped state such as request or transaction information, or encapsulating cross-cutting concerns like logging, authentication, or metrics.

Where context objects become a problem is when they become bloated and start to contain unrelated information simply for the convenience of not having to change function signatures. They can be used, but one should consider whether it makes logical sense to group the information or interfaces that are added to them. When the context objects serve read-only information, the potential impact down the line from bad decisions is more limited.

### Q: Python and Ruby are similar but yet so different. What is the difference in their design philosophies?

Python emphasizes readability, where explicit is better than implicit and there is "only one way to do it". It supports object-oriented programming but is more multi-paradigm and precedural styles feel natural as well. It supports some level of metaprogramming via decorators, dynamic class creation, and metaclasses, but it prefers clarity and understandability.

Ruby emphasizes flexibility with multiple ways of writing the same code and multiple ways of accomplishing the same thing. It is a purely object-oriented language where absolutely every construct is an object. Ruby's metaprogramming is more flexible and integrated into the language which is powerful but more "magical" and harder to follow.


### Q: What are some best practices or rigid ideas that are taught in programming but have more nuance in practice?

Global state is not always bad when controlled. Some global state is often a practical necessity, with things like configuration, environment variables, and dependency injection containers often being a form of global state. The key is controlled usage, and often acceptable global state is state that is largely read-only.

The Don't Repeat Yourself (DRY) principle is sometimes taken too literally. Prematurely abstracting any and all shared code can lead to unnecessary complexity. Sometimes, two pieces of code look similar but have different reasons to exist or _should_ otherwise be allowed to evolve separately. Write Everything Twice (WET) may be a better principle; that is, don't worry about consolidating repetition until it has been repeated three times or more and it makes logical sense to share.

Preferring composition is a good practice, but that doesn't mean inheritance is never useful. It can be useful for defining shared behavior when there truly is a clear "is-a" relationship between two things.

Overusing dependency injection can make code more complex than needed. Sometimes, creating an object directly inline is fine if it's lightweight, simple, and/or unlikely to change or need to be substituted in tests.

OOP has been the standard paradigm in development and education for some time, but it is often applied poorly and only overcomplicates the design of a system. More recently, functional, data-oriented, and event-driven approaches have become popular.

100% unit test coverage is a bit excessive sometimes; simple getters/setters and glue code don't necessarily benefit from test coverage.

While breaking down functions into smaller units is useful to an extent, excessively small functions can make code harder to read when the function definitions start to become a larger percentage of the code one is looking at.

While ORMs abstract away database interaction, that also means they can make debugging and understanding what exactly is happening with regard to the database more difficult. Perhaps more direct SQL generation has advantages.

Self-documenting code is a good goal, but in practice some business logic, decisions, or historical context are much better explained with comments than names.

Excessive decoupling can lead to unnecessary complexity. Sometimes, direct dependencies make code simpler and easier to maintain.

The latest programming trends do not always last or represent progress. Trending languages and frameworks have come and gone while other staples, like C, SQL, and POSIX, have stayed relevant for many decades.

More lines of code does not mean more complexity or less readability. Sometimes, overly concise or condensed code (ternary operators, list comprehensions, bitwise tricks) is less readable and maintainable.

Encapsulation is valuable for managing invariants or abstracting implementation details that could change, but it can be taken to an extreme (e.g. getters and setters for fields that logically have no invariants).


### Q: What even is a monad, really?

A monad is a functional design pattern that represents computations as a series of steps. At it score, a monad is a type with two operations that satisfy the "monad laws":

- A unit or return function that takes a plain value and wraps it in a monadic context, e.g. `Some(value)`
- A bind function (sometimes called flatMap) that takes a value from within a monad and a function that returns another monad, flattening the result into a single monad. This allows chaining monadic operations together.

The monadic laws are:
- Left identity: wrapping a value with the unit function and then applying bind should be the same as applying the function to the value directly.
- Right identity: applying the bind function with the unit function should not change the monad.
- Associativity: chaining multiple operations with the bind function should not depend on how the operations are grouped.

Looking at a "Maybe" or "Optional" type, you have a way of putting a value into that context (e.g. `Some(value)`) or of putting an "empty" value into it (e.g. `None`). That is the entire space of possible things that can exist in that monadic context. Then, you have a bind or flatMap function which takes one of those possible things and provides a new one which may be the same or different. That is the "chaining" operation that allows representing computation as a series of steps.

Other common monads are `Either`, which allows a "successful" `Right` result or an error `Left` result, analogous to `Some` or `None`, and the `List` monad which allows chaining operations over lists, handling multiple values, and combining results.

### Q: What is "backpressure" in reactive programming?

Backpressure refers to a mechanism for handling situations where a data producer (e.g. a stream or observable) generates data faster than a consumer (e.g. subscriber) can process it. It can be implemented in several ways, including:

- Buffering excess messages. This helps to tolerate occasional bursts of data but isn't a solution if the producer continuously outpaces the consumer.
- Dropping messages. This can be acceptable when only the latest data is relevant and a backlog has little value anyway.
- Throttling, whereby the producer reacts to the consumer's inability to keep up or proactively throttles itself.
- Blocking, whereby the producer must wait until the consumer is ready accept new data.
- Windowing and batching, whereby the system processes data in fixed-size chunks or batches, reducing the overhead of processing data items individually.


### Q: What is the "non-member, non-friend principle"?

The principle states that, with regard to C++, if a function can be implemented using only a class's public interface, then it should be implemented as a free function (a non-member, non-friend function).

The reasoning is that it clearly signals that the function does not rely on internals of the class, and that any changes to the internals of the related class should not require changes to the function.

However, some may argue that it impacts discoverability (i.e. no "dot completion" in an IDE) and can create a sense of fragmentation or disorganization when not all of a class's associated functionality is strictly part of the class.


### Q: How can one determine whether the "right" abstraction has been achieved?

The abstraction should have a minimal but sufficient interface. Client code should not need to reach "under the hood" for details or do what they need without workarounds.

It should have predictable, intuitive behavior. Clients shouldn't need to guess how something works or be surprised by the effects of small changes in usage.

It should hide what varies and expose what's stable.

It should minimize dependencies on other parts of the system and keep related responsibilities together (low coupling, high cohesion). If changes outside the abstraction often force changes inside it, that's a bad sign.

It should be reusable in multiple contexts without bending too much or requiring adapters, glue, workarounds, etc.

If it survives multiple iterations or feature additions without becoming cumbersome, that's a positive sign.

It should fit the mental model that you and other developers have about the problem; it should be easy to "get".

### Q: What is the distinction between a unit, integration, and acceptance test?

A unit test targets a small unit of behavior in isolation; often a single function, method, or class. Everything outside of that scope should be controlled or replaced with mock implementations.

An integration test checks that multiple real components work together correctly. It tests boundaries: database to service, service to service, configuration, etc.

An acceptance test validates the system from the perspective of a user or stakeholder. It tests whether the system satisfies the requirements it was built for, often exercising the whole stack from UI through backend. They are often the most brittle and least precise diagnostically, but they provide confidence that the system actually does what was intended.


### Q: What is the guidance on the use of "auto" in modern C++?

The guidance is to use auto fairly liberally when the type is obvious or irrelevant to understanding, but to avoid it when it hides important type information. Practical guidance many teams follow is:

Use auto when:
- The type is obvious from the initializer
- The type is verbose or template-heavy (and hard to follow anyway)
- It would be repetitive not to
- You want the compiler to adjust to type changes without intervention

And to avoid auto when:
- The exact type is important to understanding the code
- The initializer doesn't clearly reveal th type
- It could hide conversions or narrowing


### Q: What is the timeline of programming language design and popularity?

Assembly languages (1940s-1950s) mapped mnemonic codes directly to hardware operations. Essential, but impractical for increasingly complex applications.

Early high-level languages (1950s-1960s) like Fortran for scientific computing and Cobol for business applications.

Structured programming languages (1960s-1980s) introduced the concepts of block structure and scope. Algol (1960) was influential in acacemia but less so in industry. Pascal (1970) was popular in educational settings and C (1972) became very popular for system programming and is still highly relevant today.

Object-Oriented programming languages (1980s-1990s) emerged starting with Smalltalk (1980). C++ (1985) extended C with object-oriented features while maintaining backward compatibility. Java (1995) emphasized platform independence and security.

Scripting and functional languages (1990s-2000s) emerged with Perl (1987) focusing on text processing, Haskell (1990) demonstrating a purely functional language, Python (1991) emphasizing readability and simplicity long before recent explosive growth in the data science world, and JavaScript (1995) for web browser scripting.

Modern trends (2000s-2025) bring us Rust (2010), aiming to combine memory safety with the efficiency of C++, Go (2009) emphasizing simplicity and efficiency for concurrent programming, and Kotlin (2011) aiming to be a more modern and pragmatic language for the Java VM.


### Q: What about Ruby, Objective-C, and Delphi?

Ruby was introduced in 1995 before gaining popularity later due to the Ruby on Rails framework for web development. It is highly influenced by the object-oriented purity of Smalltalk.

Objective-C is similarly influenced by Smalltalk, but maintains compatibility with C. It was introduced in the early 1980s and became dominant in the Apple ecosystem because of its association with NeXTSTEP. Swift is meant as a modern, safer alternative that reduces the syntax complexity and verbosity of Objective-C.

Delphi was introduced in 1995 as part of a rapid application development by Borland. It was heavily influenced by Object Pascal with an emphasis on quick GUI development for Windows. However, it faced challenges from Java, .NET, and later web applications.

### Q: What exactly is the difference between structured, imperative, and procedural programming?

They are technically different paradigms, but most popular modern languages involve all three.

Imperative programming is the idea that programs are composed as a series of commands that manipulate state

Structured programming introduces concepts like loops, conditionals, and associated blocks of code.

Procedural programming is the idea of abstracting parts of a program into named blocks to aid abstraction and reuse.

### Q: What's the relationship between algabraic data types, traits, higher-kinded types, and implicits as seen in Scala?

Traits are somewhat similar to interfaces in other languages. They define contracts but can also hold state and implement methods. They are used for a kind of multiple inheritance to share both interfaces and data among classes in a way that is more like composition than inheritance.

Higher-Kinded Types are types that take type constructors as parameters, enabling the definition of more generic structures that operate on a wide variety of types. In other words, they're types that take other types as parameters.

Implicits are mechanisms that allow the compiler to automatically supply parameters to functions or to convert types.

Algabraic Data Types are types formed by combining other types, typically using sum types (variants) and product types (tuples). They allos the definition of complex structures that can encapsulate a fixed set of possible values for type-safe data handling.

Traits can be used to define ADTs by writing a set of classes that implement a sealed trait.

Higher-Kinded Types are often used in conjunction with implicits to define generic operations over data structures like functors, monads, etc. Implicits provide instances of these type classes, allowing for automatic derivation of functionality based on context.

Implicits can be used to provide default behavior or type class instances for ADTs, enabling more flexible and reusable code.

Traits can be parameterized with higher-kinded types to define abstract data structures or operations that work with any type constructor.

### Q: What was the earliest game console where games were typically programming in C or C++ rather than assembly?

The majority of SNES games were still written in assembly for performance. The PlayStation and Saturn were the earliest to provide robust development kits for C, and this of course continued with the N64, Dreamcast, and so on.

### Q: How can one replicate the "context and dependency capture" role of objects in OOP in other paradigms?

In C, this might be accomplished with context structs holding relevant context for use with multiple functions.

In languages that have closures, you can create lambdas or function objects with relevant context bound. Similarly, partial function application achieves binding of context separately from use.


### Q: Why are houses in the US typically built with wood while in the UK they're typically built with brick or stone?

By the time large-scale building was needed in the UK, much of Britain's original forest cover had already been depleted due to centuries of shipbuilding, charcoal production, and land clearing for agriculture. Timber shortages were already an issue by the 17th and 18th centuries.

The UK has abundant natural stone deposits (limestone, sandstone, granite, etc.). Stone is durable, fire-resistant, and sutiable for the damp British climate.

Wood construction works well in the US because it offers better insulation against the more extreme temperature fluctuations.

### Q: What is the distinction between England, Britain, and the UK now and historically?

Britain is the geographical island that includes three countries (although, not countries in the usual international sense of the word): England, Scotland, and Wales.

The United Kingdom is a sovereign state or political entity that comprises England, Scotland, Wales, and Northern Ireland (i.e. Great Britain and Northern Ireland). From an international perspective it is often referred to as a country despite also having entities within it called "countries".

Prior to the 10th century, England, Scotland, and Wales contained various kingdoms. In 927, England was unified under one monarch. In 1284, Wales was effectively annexed by England (but not formalized until 1535-1542). The Acts of Union in 1707 united England and Scotland under the Kingdom of Great Britain, at which point Britain became a political term rather than a purely geographical one. Ireland was added in 1801, with part of it leaving in 1922.


### Q: How and when did the monarchy in the UK lose its "real" power and why am I not aware of any kind of revolution?

It was a long, gradual decline in authority rather than a sudden revolution. As early as 1215, English kings had their power legally limited by nobles with the Magna Carta.

Charles I fought Parliament across money, religion, and authority, but was put on trial and executed in 1649, reinforcing that the monarch could be judged by his own people.

A major turning point was the introduction of the English Bill of Rights in 1689. King James II was forced out by Parliament while William III and Mary II were invited to rule under the new conditions. The bill made it unlawful for the monarch to suspend laws or tax without Parliament's consent. This made Parliament the supreme lawmaking body.

The 18th century saw a shift in power from the monarch to the Prime Minister and Cabinet. Elected ministers were more involved in day-to-day governance by the 1800s.

A single violent revolution didn't occur because the monarch gradually lost practical power even if technically he still had formal authority. Parliament held control of funding. The military was not loyal to the king to the extent that they would act without pay and support from Parliament, so Parliament effectively had the power.


### Q: How and when did the US and UK become allies, or at least friendly, post-revolution?

The two were still unfriendly and the situation remained tense through the early 1800s. However, the War of 1812 ended with a treaty and trade between the two countries grew. It became practical and profitable to cooperate.

Tensions briefly rose during the American Civil War with Britain's economic ties to cotton, but Britain ultimately stayed neutral.

Around the turn of the 20th century, Britain had bigger concerns with Germany's rise in Europe. With the U.S. becoming a major industrial and naval power, along with strong cultural ties, the relationship became increasingly friendly and centered on strategic trust. The two World Wars further cemented the two as allies.

Overall, it was a gradual shift where hostility clearly stopped making economic sense and friendly trade offered benefits for both. Later, emerging threats incentivized strategic cooperation.


### Q: What is the population of the UK in terms of US regions or states?

At roughly 69 million people, the UK overall is similar to the combination of California and Texas.

England is a bit more than Florida and New York combined.

Scotland is roughly the same as Minnesota or Colorado.

Wales is roughly Iowa or Arkansas.

Northern Ireland is roughly New Mexico or West Virginia.


### Q: What is the UK's economic output in terms of US regions or states?

For reference, the US's approximate nominal GDP is 29.2 trillion USD.

The UK's GDP is approximately 3.3-3.9 trillion USD.

The UK falls between California and Texas in terms of GDP, with California having 4.1 trillion USD and Texas having 2.7 trillion USD.


### Q: How can I deal with the "awkwardness" of handling both orientation and velocity with a vector?

A velocity vector is awkward for orientation because it can have zero magnitude which has no orientation. These are really two independent pieces of state that are only correlated in many cases.

You can store a normalized direction vector separately from a speed vector. Even if the velocity/magnitude is zero, orientation can be retained.

You can store angle and magnitude instead, but without an associated "zero degrees" axis, the angle is underspecified. For most operations, a direction vector is more immediately useful anyway.


### Q: What is the difference between brush-based and model-based environments?

Brush-based geometry, also known as constructive solid geometry (CSG), involves constructing an environment from primitive shapes called brushes. Brushes can be combined, subtracted, or intersected to create more complex shapes and structures.

Model-based geometry emphasizes the construction of an environment by composing geometry that was crafted in dedicated 3D modeling software.

Brush-based environments have become less common since the mid-2000s as the industry leveraged increased processing power and more advanced 3D modeling tools to build environments directly from more complex models.


### Q: How is gamma different from brightness or contrast?

Brightness adjusts the overall luminance of an image, with all regions and tones affected uniformly.

Contrast controls the difference between the darkest areas and the lighest areas in an image.

Gamma refers to a nonlinear relationship between the numerical values of pixel intensities and their perceived brightness on a display. It is used to compensate for the nonlinearity of human visual perception and to ensure that images appear correctly on different devices. Adjusting the gamma value affects the overall brightness distribution and mid-tones of an image.

### Q: What is frame pacing?

Frame pacing refers to the consistency of the time it takes to render each frame in a game. While frame rate indicates an average, it does not say anything about how consistent the time between each frame is. Frame pacing issues can result from a variety of factors, including rendering techniques, CPU or GPU bottlenecks, or synchronization issues.

### Q: What are all the various anti-aliasing techniques?

Multisample Anti-Aliasing (MSAA) is a common traditional technique. Instead of resolving a pixel to one virtual point in the scene, it samples a few clustered points in the scene to get an average.

Supersample Anti-Aliasing (SSAA) involves rendering the scene at a higher resolution and then downsampling to the target display resolution.

Fast Approximate Anti-Aliasing (FXAA) operates on the final rendered image. It analyzes and smooths the image, but may blur details as a result.

Temporal Anti-Aliasing (TAA) is a more advanced technique that combines information from multiple frames to reduce aliasing as well as flickering or shimmering. It leverages motion vectors from the game data and the previous frame to create a smoother result.

Conservative Morphological Anti-Aliasing (CMAA) is a technique that works by examining the scene's depth buffer to determine edges, allowing for more selective anti-aliasing.

### Q: What are some methods of procedurally generating game worlds or maps?

The real goal and difficulty comes from creating local variety while maintaining global constraints or intentions.

A common approach in roguelikes is a graph-first, abstract layout that is "realized" into a more physical space. The graph defines rooms or areas as nodes with edges between them representing connections via doors or corridors, and encodes any constraints like special areas that must exist somewhere (e.g. boss or starting area). The graph is then used to build a more detailed tile-based world. The details of a given room or connection can be decided on-the-fly, but by following the graph when building it ensures that the high-level constraints are maintained.

Cellular automata can be good for creating organic, cave-like spaces with natural chokepoints and emergent shapes, but connectivity is probabalistic without post-processing and you have less control. It works best when the environment is the focus rather than layout control. You start with random noise and apply local rules iteratively such as "if a cell has more than N solid neighbors, it becomes solid". Then, you flood-fill to keep only the largest connected region.

Binary space partitioning can be used to carve less organic spaces. It involves splitting the map rectangle recursively and placing a room in each leaf and potentially connecting sibling partitions. It is essential building a graph from space rather than building spaces from a graph. It works well for clean, readable layouts and reliable connectivity.

Random walk tunneling involves metaphorically digging tunnels by walking agents through a solid space including variants like the drunkard's walk or biasing toward unexplored regions. This is not especially interesting on its own but can be used to make more interesting corridors or connections between rooms that have been placed in another way.

Constraint satisfcation or "wave function collapse" style methods involves building a map from local adjacency rules. You iteratively pin tiles in the world from among the options that are valid for a given tile considering what has been pinned already. It's good for enforcing local adjacency rules and making a coherent map, but on its own does little to satisfy global constraints unless those constraints bias the choices that are made when pinning.

Rule-based generation like shape grammars or L-systems require a bit more upfront design work, but can allow a map to feel authored.

For outdoor spaces or terrain, it can make sense to start with a noise-based heightfield. Use flood-fill to find large connected components and either discard small isolated areas or carve passes between them. The heightmap can be used to determine walkability, where water flows, where vegetation can grow, etc.

### Q: What are typical final loudness targets in modern music?

For streaming platforms, the common reference metric is integrated LUFS over the full track.

- Pop / dance: around -9 to -7 integrated LUFS
- Rock: more often -10 to -8 integrated LUFS
- More dynamic or less "commercial" material: -12 to -10 integrated LUFS

Anything louder than about -7 LUFS is usually a conscious aesthetic choice toward aggression or "hard" club material.

However, musically, short-term and momentary loudness matter more:

- Short-term LUFS in choruses is often around -6 to -4 LUFS in modern pop/dance
- Verses might live closer to -10 to -8 LUFS

Dynamic range (LRA) is also important to consider:

- Modern pop/dance typically lands around 3-6 LU LRA
- Rock may stretch to 5-8 LU LRA
- Below around 3 LU, things often start sounding flat and fatiguing unless the genre demands it

Commonly, a gentle bus compression (1-2 dB GR, slow attack, auto or medium release) is used to glue the track and final loudness is achieved primarily through limiting, often in stages. Try to make the mix feel finished and punchy at around -14 to -12 LUFS integrated and then see how far it can be pushed in a limiter without noticeable changes. That often puts the track somewhere between -10 and -7 LUFS.


### Q: What exactly is an LU or an LUFS?

LU is a relative "loudness unit" while LUFS is the same measure in absolute terms ("loudness units relative to full scale"). 0 LUFS is the theoretical maximum within a digital audio system. LUFS only has meaning when paired with a time window: "integrated" means the entire track, short-term often means around 3 seconds, and momentary means around 400 milliseconds.

An LU itself is simply a difference of 1 dB in loudness relative to some reference loudness. For example, a common broadcast standard like EBU R128 might use a reference of -23 LUFS. From that perspective, material at -21 LUFS is said to be +2 LU. Therefore, a value like "16 LU" on its own has little meaning without context.


### Q: How should I think about using the various kinds of dynamics tools?

A very high-level guideline might be that early tools should make decisions and late stage tools should manage consequences.

Default to single-band compressors for general envelope shaping, groove consistency, or glue. They are appropriate on individual tracks, subgroups, and the mix bus only for very light glue (1-2 db GR).

Single-band limiters can be used to cap peaks in material, increase density without reshaping envelopes, and achieving final mix loudness. They can occasionally be used on unruly individual tracks, but should almost exclusively live at the end of the mix chain.

Saturation is for when things feel thin, sterile, or disconnected. They may be chosen over compression when something feels overly dynamic but also lifeless. They can make sense on individual tracks, subgroups, or very lightly on the mix bus.

More specialized tools like maximizers or transient shapers are often just multiple tools behind a unified interface, maybe with special psychoacoustic processing. Maximizers, for example, are often a combination of limiter, soft clipping, and psychoacoustics. The danger is that they make decisions for you. It's fine in the mastering stage if it sounds the way you want, but it's risky to use earlier in the mix somewhere. Transient shapers can be used when compression is changing the tone too much and you want more or less attack without sustain side effects.

Multiband compressors should be used judiciously to avoid inappropriately compensating for imbalances. They should only be used when a known frequency range is dynamically unstable and this can't be fixed in another way. Using one on the mix bus is often a sign that you're compensating for too much low-end energy, overcrowded mids, or over-bright top end.

Multiband limiters may be used to push loudness on the final mix, perhaps in part by controlling the low-end separately from the rest of the mix.

In general, a practical hierarchy:

1. Arrangement and sound choice
2. Track-level EQ and compression
3. Subgroup processing
4. Gentle mix-bus glue compression
5. Final limiting


### Q: How do I reconcile the idea of "track-level" with the fact that many synthesized sounds can be quite layered and dense to begin with?

Really, the a better mental model is perceptual or functional "voices". A three-oscillator synth through one filter and envelope may function as a single voice. A layered bass may be one "thing" rhythmically or melodically, but consist of a sub sine, mid growl, and distorted top, each of which may be treated separately before being bussed. Multiple unrelated elements shouldn't share a (non-glue) compressor or EQ.

### Q: What's the distinction between a compressor and a transient shaper?

Both can be used to control transients, but compressors operate on input levels while transient shapers operate on _changes_ in amplitude rather than the absolute level. Transient shapers aim to identify the fast attack component and shape it separately from the rest of the sound.

Transient shapers are less dependent on input level; they aim to treat the input envelope similarly regardless of peak level.

### Q: What's the deal with oversampling, true peak, dithering, and noise shaping?

These only come into play for rendering a final output file.

Oversampling is relevant to non-linear processes like clipping that create harmonics. They can fold back into the signal as aliasing, but oversampling runs the process at a higher internal sample rate to avoid this.

True peak again uses oversampling to catch peaks that fall in-between the digital samples. For final delivery, you may want to enable true peak processing with a ceiling of -1.0 dBTP to -0.8 dBTP.

Dithering only matters if you are reducing bit depth. It replaces correlated quantization distortion with uncorrelated noise, making quiet fades and tails behave correctly. It is really not relevant for 24-bit or 32-bit float exports, only 16-bit files. Noise shaping just impacts where the dither noise goes. A flat dither spreads the noise evenly while noise shaping puts the noise into less audible frequencies.


### Q: Are there any guidelines for how to chain non-linear distortion effects and EQ?

The key principle is that non-linaer processors create new frequency content. EQ before them changes what gets created while EQ after them changes what survives.

Use EQ before distortion to prevent ugly artifacts or bias where harmonics are generated. Common cases include high-pass to avoid muddy, pumping results, cutting harsh bands, especially 3-6 kHz, or feeding target band-pass or shelf into saturation.

EQ after distortion is for removing added "junk" and fitting the sound back into the mix. Common moves include a low-pass to remove fizz, high-pass to clean up low frequency junk, or broad shaping for tone balance.

Some common chains:

- HPF + mild saturation + LPF on busses for subtle thickening
- Mid boost + saturation + undo with EQ to add presence without changing tone
- Band-pass + heavy distortion + quiet blend to add parallel excitement

### Q: What is an amp/cab model if you break it down?

1. Input conditioning: high pass or tilt filtering
2. Non-linear gain: preamp distortion, saturation, or dynamic effects
3. Tone stack: EQ controls that interact with the distortion behavior
4. Power amp: more saturation, compression, low-frequency resonance and damping
5. Cabinet + mic: very strong filtering, resonances, high-frequency roll-off

In other words: EQ + distortion + EQ + compression + extreme EQ


### Q: What makes a sound "boxy"?

1. Strong midrange resonances, often around 200-400 Hz or 600-900 Hz
2. Aggressive high-frequency roll-off above 6-8 kHz
3. Comb filtering due to micro-reflections


### Q: Should I aggressively filter anything under 20 Hz?

It's reasonable, but don't do it by putting a steep filter on the mix bus. Use gentle and purposeful high-pass filters on tracks or busses, especially on tracks that are not at all meant to contribute to the low-end. Don't automatically high-pass the bass and kick unless there is a problem. If you do filter, use a gentle 6-12 dB/oct slope around 20-25 Hz.


### Q: How might I name MIDI clips or patterns in a useful way?

Consider a template of (Role) - (Behavior) - (Section).

Role captures functions like bass, lead, pad, chords, arp, pluck, drone, or stab.

Behavior captures sustain, groove, offbeat, swell, or syncopated.

Section captures compositional purpose like main, alt, answer, fill, breakdown, dropout, verse, chorus, or bridge.

### Q: What is the role of a "pad" in comparison to other sustained sounds?

Pads fill a role of continuous harmonic support in genres or styles that call for it. They fill space between rhythmic events and add a sense of space. Genres that prioritize articulation, rhythm, or attack may not make use what one would call a "pad" because silence and temporal spacing are features.

Not all sustained sounds are pads; a Hammond organ is harmonic, but usually rhythmic and articulated. A horn section may hold sustained notes, but it sits in the foreground and is declarative. Pads are intentionally non-assertive and subordinate.

### Q: Aside from strong use as an effect, how is reverb typically used?

It has three main roles:
- Glueing tracks or voices so they "feel" like they're in the same room.
- Pushing elements back in the mix so they feel farther away
- Adding emotion, realism, or "vibe"

There is often at least one shared reverb fed by multiple tracks simulating a common environment, like a hall or a plate.

It's also common to use different reverbs for specific purposes, such as a vocal plate for vocals, room reverb for drums, and long hall for pads. However, big differences in reverb between instruments can sound unnatural if not intentional.

It is common to use small amounts on almost everything, as dry instruments/voices can sound disconnected.

Pre-delay and EQ are essential, as pre-delay separates the reverb tail from the dry signal and high or low-pass filtering avoids muddiness.

### Q: What is the subjective difference between a plate, room, and hall reverb?

Plate reverb mimics a mechanical device from the 50s-60s where a metal plate vibrates to create reverb. It is bright, dense, and smooth, but lacks natural early reflections and sounds less realistic. However, it tends to muddy the mix less than other kinds of reverb. It is often used on vocals, snare drums, or general glue when the artificial sound is okay.

Room reverb has a short decay, strong early reflections, and doesn't wash out the dry signal. It is often used on drums to simulate a real recording room, guitars and pianos for realism, and general cohesion for a shared space effect.

Hall reverb has a long decay with obvious tails for a sense of depth and grandeur, often with rolled-off highs. It is often used with orchestral instruments, pads or ambient layers, and vocals if you want an epic or cinematic feel.

### Q: How are delay effects most often used?

It is often used on vocals with short delays for thickness, tempo-sync for rhythmic interest, or automated to hit at the end of phrases.

Tempo-synced delays dominate modern production, but unsynced delays are used for effects or organic feel in ambient/experimental music.

Delay is usually per-instrument. They are often EQ'd to avoid frequency clutter and modulated for richness.

### Q: Why did producers go crazy with reverb and delay in the 1980s?

The late 1970s and early 1980s saw the appearance of new digital processors like the AMS RMX16 Digital Reverb and the Lexicon 224 Digital Reverb. For the first time, producers had clean, controllable reverb with precise gating and automation. The gated reverb drum sound in particular was an accidental discovery that became a trend due to its ability to make drums sound "big" while keeping the mix controlled.

1970s production tended toward natural room sound and warmth. The 1980s reacted against that by emphasizing synthetic textures, electronic drums, processing, and brightness. This fits a general pattern in production trends where new technology or trend appears, it gets overused, and then there is a reaction against it.

Considering the later decades, they might be associated with:

- 1980s: gated reverb
- 1990s: raw minimalism
- 2000s: extreme loudness
- 2010s: sidechain pumping
- 2020s: analog nostalgia


### Q: Why does 80s music sound decently "modern" to me while earlier music does not?

The 80s production crossed a threshold such that it is not fundamentally different from the modern day. Digital tools, MIDI, and increasingly clean multitrack recording all arrived around the same time. The aesthetic target changed from capturing a performance in a room toward aiming for clarity, separation, and control.

A lot of pre-80s music is still rhythmically "human" with loose timing, swing by default, and tempo drift. Tools in the 80s allowed for and encouraged the use of quantized, grid-locked patterns. This rhythmic rigidity has become standard.

The frequency balance moved toward what modern playback systems are designed for. Earlier music often emphasizes mids with rolled-off lows and highs, partly due to the constraints of vinyl and live-band instrumentation. The 80s brings extended low-end and bright highs with cleaner transients, and modern speakers or headphones are capable of producing the full range.

Certain synthetic sounds introduced in the 80s are sonically simple and remain functional. Unlike performance instruments which have strong ties to certain places or times, many synthetic sounds are abstract and timeless in a way.

### Q: Was there pushback against the shift from "capturing a performance" to the modern multitrack studio sound?

Yes, many felt it was sterile, fake, or dishonest. Some listeners described it as cold, plastic, or soulless. Genres like punk and grunge were in some way push-back against the new artificial sound.

### Q: What were the audio capabilities of the Sega Genesis / Mega Drive?

It had two audio chips: a Yamaha YM2612 FM Synthesizer and a Texas Instruments SN75489, the latter mainly for backward compatibility with the Master System.

The FM synthesizer provided:
- 6 simultaneous voice channels which can all be allocated to FM synthesis, but channel 6 can instead be used as a PCM channel for 8-bit audio samples.
- Each channel has 4 operators arranged in 8 possible modulation relationships
- Each operator is a sine wave with configurable ADSR envelope, detuning, and scaling
- Stereo output with each channel assignable to left, right, or both
- Roughly 9-bit dynamic range due to internal DAC limitations
- LFO support for vibrato / tremolo
- Sample playback is roughly 8-bit and 32 kHz at best

The 8 FM algorithms were:
- 4-op chain, good for metallic or complex evolving tones
- 3-op chain + 1 op, balance between complex voice and simple voice
- 2x2 op chains, good for layered or stereo voices
- 4 parallel, maximum polyphony, least complexity, good for percussion and layered pads
- Op1 mod Op2/Op3, Op4 separate, used for richer stereo-like detuned tones or chorused effects
- Op1 mod Op2/Op3 mod Op4, allows for tight control and complexity
- Parallel Op2 mod Op1, Op3 mod Op4, complex dual-instrument sounds

The SN76489 provided:
- 4 channels: 3 square wave tone generators with a fixed duty cyle, 1 noise channel with white or periodic noise
- 16 volume levels (4-bit volume control)
- Tone range roughly from 110 Hz to 111 kHz
- Mono only

No built-in effects or subtractive filters.

FM operator configurations and envelope parameters could be changed at any time during playback, but with important caveats due to CPU time, timing precision, and voice allocation, however such changes are not common due to artifacts like clicks and pops.


### Q: What does an "exciter" do exactly?

An exciter emphasizes harmonic content, adding presence and increasing perceived brightness or clarity. Primarily, an exciter generates additional harmonics in the original signal and then mixes them back in.

Exciters are commonly used to add "air" to vocals, giving a "breathy" quality. More generally, they are used to add presence and definition to certain instruments or voices, making them stand out.

### Q: Without any compressors or limiters, how was dynamic range handled on hardware like the Sega Genesis / Mega Drive?

Everything was handled manually or left to quirks of the chip. Dynamics were handled via volume envelopes, channel balancing, and deliberate saturation/clipping via DAC limitations. The DAC is nonlinaer and slightly distorted eve nat normal volumes, but if the sum of the FM outputs is too loud then it clips.

Sometimes, percussive sounds or bass were deliberately driven into the red to stand out.

### Q: How can you have a "second order linear regression"? It's quadratic, not a line.

In the context of statistics and machine learning, "linear regression" means the coefficients appear linearly, not that the regression itself is linear.

- `y = a + bx` is a 1st-order linear regression
- `y = a + bx + cx^2` is a 2nd-order linear regression
- `y = a + b^x` is _not_ a linear regression

### Q: If LLMs predict tokens sequentially, what stops one bad prediction from derailing the rest of the response?

Nothing fundamentally stops it and it can happen, but there are some factors that prevent it from happening constantly.

Language has a strong statistical structure and is extremely redundant. Even if one token is slightly wrong, the rest of the context still constrains the continuation heavily. A long with this, modern models have very large context windows that contribute to the probability and stability of the next token.

During training, models learn from imperfect text. It implicitly learns to recover from inconsistencies in a coherent way even if part of the response is slightly odd or incorrect.


### Q: How were "reasoning" models trained?

Early versions relied heavily on human-written reasoning traces, but modern reasoning models are not primarily trained that way. After a point, they were trained from self-generated reasoning plus verification and reinforcement learning. You have a model generate reasoning paths for a problem and train a new model on the reasoning trajectories that reached the correct answer. This is somewhat analogous to selection pressure in evolution. Even the correct answer can be decided automatically by assuming that the answer which appears most often in many traces is correct. In some domains like math, code, or logic, correctness for known problems can be checked automatically.


### Q: Why do reasoning traces often seem to ramble and repeat awkwardly?

The training rewarded correctness, not elegance. Only the final result was rewarded. Thinking longer often improves accuracy, so models learned to think longer even if they end up repeating or going in circles sometimes.

Self-generated reasoning amplifies weird patterns. Models may generate strange patterns that happen to succeed, and training reinforces this. This is somewhat analogous to the way that arbitrary mutations or features that are hard to explain in nature are carried along with obvious beneficial genetic changes.

Some repetitive phrasing serves to represent a kind of state or state change that happens to be represented as natural language.

### Q: How do LLMs decide when to stop a response? If it's just another token, isn't it unlikely to choose that token over all others?

Conceptually they predict a end-of-sequence token as the next token. It works relibably because the model has learned very strong signals about when text typically ends. It has seen billions or more samples of how text ends with a concluding sentence, finished list, closing braces, etc. Furthermore, every training input ends with an EOS token so the model has a high amount of exposure to it.

Models are also trained on length. As the length of a response approaches a typical response length, the probability of predicting EOS dramatically increases. This is also why a model might produce a similarly lengthy response to both a simple and complex question.


### Q: In the context of machine learning, what is MLP?

A Multilayer Perceptron, a type of feedforward artificial neural network. An input layer receives initial data corresponding to the number of "features". A set of one or more "hidden layers" sits between the input and output layers, with each node in a given layer connected to every node in the next layer (fully connected network). The hidden layers use non-linear activation functions like ReLU or sigmoid which is crucial for the model's ability to learn complex, non-linear relationships. At each neuron input, a weighted sum of inputs from the previous layer is calculated and a bias is added. The output layer has a number of neurons dependent on the task; it may have one for a single decision or multiple for a classification problem.

The network learns by adjusting weights and biases to minimize the difference between predictions and expected values using a process called backpropagation. Backpropagation uses the chain rule from calculus to efficiently calculate how much each weight and bias contributes to the overall error. These adjustments are made through an optimization algorithm like gradient descent.

MLPs are considered universal function approximators; they can, in theory, approximate any continuous function given enough hidden neurons and layers.


### Q: What are some known universal function approximators?

Universal function approximators are systems that have been proven to be capable of approximating any continous function using the Universal Approximation Theorem.

- Multilayer Perceptrons (MLPs): a common type of feedforward artificial neural network.
- Radial Basis Function (RBF) networks: a type of neural network that uses radial basis functions (like a Gaussian curve) as activation functions in the hidden layer. Instead of a weighted sum of inputs like MLPs, RBF networks use the distance from a central point to determine the output of a neuron.
- Support Vector Machines (SVMs): these are often used for classification problems, but SVMs with certain kernels like the Gaussian kernel can act as universal function approximators. The kernel essentially maps data into a higher-dimensional space where it can be separated or approximated linearly.
- Polynomials and Fourier Series: the Stone-Weirstrass theorem shows that polynomials can approximate any continuous function on a closed interval. Similarly, the Fourier series can.
- Turing Machines: although more abstract and conceptual, a Turing machine can simulate any computer algorithm and thus, in a sense, process any computable function. It is a broader class than continuous functions.

### Q: What is the highest "ping" latency for an idealized network connection between two points on Earth?

The speed of light in fiber is around 200,000 km/s. A realistic best-case cable path would be something like 30,000 - 40,000 km one way. This gives up to 200 ms one-way or 400 ms round-trip.

### Q: What's the difference between "realm" and "domain"?

Realm is related to the Latin regimen, meaning "rule, government", and historically is the territory of a monarch; a kingdom or empire. Domain comes from Latin dominus, meaning "lord, master", and historically is the land controlled by a lord or noble. A domain is a smaller area than a realm.

### Q: Where does the trope of dwarves being master craftsmen and elves being archers come from?

Norse mythology includes the concept of dwarves as subterranean smiths who forged legendary items like Thor's hammer and Odin's spear. Germanic folklore also involves dwarves as miners and metalworkers living and working underground.

Elves in Celtic mythology were otherwordly beings associated with nature, beauty, and sometimes skill with weapons, but they were not strongly associated with bows until Tolkien's portrayal of Legolas. He linked elves with forests and the bow as a weapon.

### Q: Where does the depiction of elves as tiny creatures originate?

The "tiny elf" stereotype comes from later European folklore. Early Germanic and Norse sources depicted elves as human-sized or larger. Over time, especially in British folklore, elves became conflated with fairies and household spirits which were depicted as small, mischievous beings.

In the 19th century Victorian era, literature and art portrayed elves as miniature, whimsical creatures living in flowers or mushrooms. Around the same time, the 19th century evolution of Santa Claus introduced Santa's elves as tiny, industrious helpers.

### Q: Are futhorc runes derived from the Latin alphabet?

Elder Futhark was developed around 150-300 CE among Germanic tribes. It was not derived from Latin, but was almost certainly influenced by Italic scripts like Old Italic or Greek, as Germanic peoples traded and fought near the Roman frontier.

Anglo-Saxon Futhorc descended from Elder Futhark and was used from around the 5th to the 11th centuries, expanding the script from 24 to 28-33 runes to accommodate Old English phonemes.