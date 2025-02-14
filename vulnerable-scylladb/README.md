# CFOP: Coroutine Frame-Oriented Programming -- ScyllaDB PoC
This README details how to run our Coroutine Frame-Oriented Programming (CFOP) exploit on ScyllaDB.
This exploit demonstrates how to leverage a golden gadget under CFOP, executing an arbitrary call with multiple arbitrary arguments. The exploit does not modify return addresses and the control flow always reaches the beginning of functions, thus respecting the restrictions imposed by Intel CET.

## PoC Summary
The exploit uses frame manipulation to hijack the coroutine frames in the scheduler (circular) queue. 
This queue is periodically used to dispatch groups of operations, including coroutines.
After we hijack one scheduler object, the scheduler resumes our counterfeit frame, resulting in a call to our golden gadget *rte_hash_hash*, which has the following form:

```
endbr64                      ; CET enforced
mov rax,rsi
mov rcx,QWORD PTR [rdi+0x90] ; ctrl rcx (line 7!)
mov esi,DWORD PTR [rdi+0x80] ; ctrl rsi
mov edx,DWORD PTR [rdi+0x98] ; ctrl rdx
mov rdi,rax                  ; ctrl rdi (line 2!)
jmp rcx                      ; arbitrary call
```

The golden gadget loads the attacker-supplied values, then calls *execve("bin/sh", "-c /usr/bin/whoami")* - but can be virtually any other program.

We introduce in ScyllaDB a vulnerability - in ```cql3/util.cc```, where the input received from the *cqlsh.py* command line, that users commonly use to communicate with a ScyllaDB instance, triggers a memory corruption. We accordingly introduce in the client program (```tools/cqlsh/bin/cqlsh.py```), the corresponding shellcode for the exploit.

In order to run the exploit, the user may run the *cqlsh.py* script like any other user - then introduce the "EXPLOITPAYLOAD;" keyword, which triggers the exploit. After the exploit is completed, we see how ScyllaDB stops its normal execution; "root" or the corresponding user name is printed on screen.

# Setup
ScyllaDB is made of numerous submodules - hosted in multiple repositories. In addition, its internal build system depends on such submodules for querying additional files at runtime, so it is not possible to offload all the code of ScyllaDB to one single repository. For this reason, our build system consists of:
1) A ```cfop_setup.sh``` script, that clones a certain version of ScyllaDB from its official GitHub repository, patches the code with our vulnerability and exploit, and then builds ScyllaDB. The official way of building ScyllaDB is inside a Docker that comes with every dependency - so no particular dependencies must be installed.
2) A folder ```cfop_mods``` that incorporates the files that patch scylla, most importantly:
    * ```configure.py```: modifications so that ScyllaDB generates Intel CET code.
    * ```util.cc```: code responsible of parsing the messages from the cqlsh client. We inject a Write-What-Where vulnerability.
    * ```reactor.cc```: the program responsible of the scheduler. Modified just for some memory leakes.
    * ```cqlsh.py```: the client program, introduce "EXPLOITPAYLOAD;" to run the exploit.

A particular OS version is not needed to run ScyllaDB, as every dependency is included inside its internal docker setup.
However, we recommend to use Ubuntu 24.04, as this is where we tested our code.

# CET Remarks
Although ScyllaDB is compiled with CET support, and our exploit respects the IBT and Shadow Stack restrictions of CET (the exploit does not modify return addresses and the control flow always reaches the beginning of functions), ScyllaDB cannot be tested under a runtime CET enforcement. The reason is that it uses some custom ```longjmp``` and ```setjmp``` functionality for its internal thread system - which collides with the Shadow Stack enforcement (which does not support this at the time).

# Building ScyllaDB
We provide a script that is in charge of building ScyllaDB and patching it with the code responsible of the vulnerability and the exploit. The steps are as follows:
1. Run the build script ```cfop_setup.sh```. As a result, you will have a new repository ```vulnerable_scylladb```:
```./cfop_setup```

Alternatively, here we detail the needed steps for the process, in case the script is not an option:
1. Clone ScyllaDB and revert to the version on 01-2025
```
git clone https://github.com/scylladb/scylla vulnerable_scylla
cd vulnerable_scylla
git checkout f4b1ad43d4e701538e60c5640032117c353577e2
git submodule update --init --force --recursive
```

2. Patch ScyllaDB
```
cp ../cfop_mods/configure.py configure.py
cp ../cfop_mods/cqlsh.py tools/cqlsh/bin/cqlsh.py
cp ../cfop_mods/cooking_recipe.cmake seastar/cooking_recipe.cmake
cp ../cfop_mods/circular_buffer_fixed_capacity.hh seastar/include/seastar/core/circular_buffer_fixed_capacity.hh
cp ../cfop_mods/reactor.cc seastar/src/core/reactor.cc
cp ../cfop_mods/util.cc cql3/util.cc
```

3. Build ScyllaDB (this uses its dockerized *frozen toolchain*):
```
./tools/toolchain/dbuild ./configure.py --mode=release
./tools/toolchain/dbuild ninja
```

# Running Scylla and the CFOP exploit
The build system compiles ScyllaDB, that is supposed to be run from the same Docker used by ScyllaDB during compilation. For running the ScyllaDB program:
```
podman run -d --rm --tty --security-opt seccomp=unconfined --security-opt label=disable --network host --cap-add SYS_PTRACE --privileged --ulimit nofile=1024:1048576 -v $(pwd):$(pwd) -v $HOME/.m2:$HOME/.m2 -v /etc/localtime:/etc/localtime:ro --env CARGO_HOME -v $HOME/.cargo:$HOME/.cargo -w $HOME/ -e HOME=$HOME docker.io/scylladb/scylla-toolchain:fedora-40-20241219 /bin/bash 
``` 

Next, you can attach to the docker container:
```
podman container attach <id>
```

Finally, you can run Scylla from here (or debug it with gdb)
```
./build/release/scylla --workdir tmp --smp 8 --memory 4G --developer-mode=1
```

Once the ScyllaDB instance is running, we can launch the client program and trigger the exploit:
```
python3 tools/cqlsh/bin/cqlsh.py
EXPLOITPAYLOAD;
```

Upon sending the previous input, the ScyllaDB instance will stop and show the current user's name on screen (as it runs *execve("bin/sh", "-c /usr/bin/whoami")*).

# Notes on running the ScyllaDB exploit
ScyllaDB runs with ASLR disabled, and inside ScyllaDB's frozen toolchain Docker, so every user of this exploit will find the internal addresses to be valid - and thus the exploit to be working. 

In case the exploit would not work (e.g., to port this exploit to a different ScyllaDB exploit, 4 memory addresses need to be updated in the exploit. Further detail is written in the exploit code, at ```cqlsh.py```).