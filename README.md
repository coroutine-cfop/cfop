# CFOP: Coroutine Frame-Oriented Programming -- Artifacts Collection
This document briefly describes the artifacts submitted.
In total, there are six different artifacts, composed of four PoC exploits and two exploits in real-world programs (ScyllaDB and SerenityOS):
* PoCs:
    1) **gcc**: a PoC exploit showcasing how to call arbitrary functions with arbitrary arguments using a *Silver Gadget*. The program was compiled with GCC and Intel CET.
    2) **clang**: a PoC exploit showcasing how to call arbitrary functions with arbitrary arguments using a *Silver Gadget*. The program was compiled with Clang/LLVM and Intel CET.
    3) **msvc**: a PoC exploit showcasing how to call arbitrary functions with arbitrary arguments in Windows. The program was compiled with MSVC, and with Intel CET and Control Flow Guard (CFG) enabled.
    4) **doa**: a PoC exploit showcasing how to leverage a Data Only Attack for altering the program execution without hijacking any frame pointers, reading from an arbitrary file. Compiled with GCC and CET enabled.
5) **vulnerable-serenityos**: a modified version of SerenityOS with the CVE-2021-4327 vulnerability. Incorporates an exploit to leverage it. Showcases Infinite Coroutine Chaining (ICC).
6) **vulnerable-scylladb**: scripts and files to modify ScyllaDB, with an incorporated vulnerability and a modification in the database client to exploit it. Showcases the use of *Golden Gadgets* between others.

**Every file comes with its own README**