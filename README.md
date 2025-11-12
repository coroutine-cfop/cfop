# CFOP: Coroutine Frame-Oriented Programming
The paper for Coroutine Frame-Oriented Programming appeared in USENIX Security 2025 and is available [here](https://publications.cispa.de/articles/conference_contribution/Await_a_Second_Evading_Control_Flow_Integrity_by_Hijacking_C_Coroutines/28718642?file=53381996).

It will appear in [Black Hat USA 2025](https://www.blackhat.com/us-25/briefings/schedule/index.html#coroutine-frame-oriented-programming-breaking-control-flow-integrity-by-abusing-modern-c-45928), we will share the video of the presentation when available.

# Authors
This work has been developed by [Marcos Bajo](https://github.com/h3xduck) (*h3xduck*) and [Christian Rossow](https://github.com/crossow), researchers from the System Security group of the CISPA Helmholtz Center for Information Security in Germany.

# Artifacts Collection
Here we briefly describe the artifacts in this repository.
In total, there are seven different artifacts, composed of five PoC exploits and two exploits in real-world programs (ScyllaDB and SerenityOS):
* PoCs:
    1) **gcc**: a PoC exploit showcasing how to call arbitrary functions with arbitrary arguments using a *Silver Gadget*. The program was compiled with GCC and Intel CET.
    2) **clang**: a PoC exploit showcasing how to call arbitrary functions with arbitrary arguments using a *Silver Gadget*. The program was compiled with Clang/LLVM and Intel CET.
    3) **msvc**: a PoC exploit showcasing how to call arbitrary functions with arbitrary arguments in Windows. The program was compiled with MSVC, and with Intel CET and Control Flow Guard (CFG) enabled.
    4) **doa**: a PoC exploit showcasing how to leverage a Data Only Attack for altering the program execution without hijacking any frame pointers, reading from an arbitrary file. Compiled with GCC and CET enabled.
    4) **icc**: a PoC exploit showcasing Infinite Coroutine Chaining (ICC). Compiled with GCC and CET enabled.
5) **vulnerable-serenityos**: a modified version of SerenityOS with the CVE-2021-4327 vulnerability. Incorporates an exploit to leverage it. Showcases Infinite Coroutine Chaining (ICC).
6) **vulnerable-scylladb**: scripts and files to modify ScyllaDB, with an incorporated vulnerability and a modification in the database client to exploit it. Showcases the use of *Golden Gadgets* between others.

**Every file comes with its own README**

# Requirements
In general, Docker and Podman are the only software requirements needed. 
We tested our artifacts in a Ubuntu 24.04 machine with a 20-core i9-12900H CPU and 32GB of RAM, and a Microsoft Windows 11 Pro machine with 4-core i7-1165G7 CPU and 32GB of RAM (only for *msvc*). 

# Cite the paper
```
@inproceedings{cfop,
author = {Bajo, Marcos and Rossow, Christian},
title = {Await() a second: evading control flow integrity by hijacking C++ coroutines},
year = {2025},
isbn = {978-1-939133-52-6},
publisher = {USENIX Association},
address = {USA},
booktitle = {Proceedings of the 34th USENIX Conference on Security Symposium},
articleno = {380},
numpages = {20},
location = {Seattle, WA, USA},
series = {SEC '25}
}
```
