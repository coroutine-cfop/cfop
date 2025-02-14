# CFOP: Coroutine Frame-Oriented Programming -- SerenityOS/Ladybird PoC
This README details how to run our Coroutine Frame-Oriented Programming (CFOP) exploit on SerenityOS' browser, Ladybird.
This exploit demonstrates how to leverage the Infinite Coroutine Chaining (ICC) technique, executing three arbitrary calls with an arbitrary argument. The exploit does not modify return addresses and the control flow always reaches the beginning of functions, thus respecting the restrictions imposed by Intel CET.

## PoC Summary
The exploit consists of a malicious HTML website with embedded JavaScript - that triggers the vulnerability and runs the exploit. The exploit uses frame injection to inject malicious coroutine frames - that triggers an ICC chain, executing a theoretically infinite amount of arbitrary calls. For simplicity, without losing generality, we execute *execve("whoami")* three times. 

We use a modern version of ScyllaDB, and reincorporate the old CVE-2021-4327 vulnerability by making the appropiate source code changes. 
This vulnerability resides in the internal LibJS library, which Ladybird uses for website JavaScript parsing. Meanwhile, the browser and many other OS components rely on LibCore, a core SerenityOS library providing foundational functionality, in which developers are actively integrating coroutines. 
Although Ladybird itself does not currently utilize these coroutines, the LibCore library is linked to every binary, including *WebContent*, the process in charge of parsing websites. 
Thus, we exploit the CVE-2021-4327 vulnerability to inject malicious coroutine frames into memory, and overwrite a vtable pointer to redirect the execution flow to the LibCore coroutine code responsible of parsing them.
Here, an ICC chain of three elements is executed, leveraging the *destroyer* and *await_suspend* CFPs. 
We exploit 6 CFPs in total (2 for each element in the chain, where one CFP is used to build the chain and the other to issue the arbitrary calls).


# Setup
We release the modified source code responsible of building SerenityOS with the CVE-2021-4327 vulnerability.
With the goal of simplifying testing, we build and run the Ladybird inside a Ubuntu 24.04 docker - for which we provide the corresponding Dockerfile.

Since Ladybird is a program with a GUI, we recommend to install X-Server or a similar system in the host system. Our Docker container takes care of the rest of dependencies.

Ladybird is built with CET support, and the exploit can be tested under active CET enforcement. 
However, a correct setup and system are needed (the exploit can be tested without this runtime enforcement):
1) A modern Intel processor (Tiger Lake or newer).
2) Kernel support for userspace Shadow Stack enforcement (since 6.6 kernels).
3) The program needs to be compiled with CET support (Ladybird has it).
4) Every linked shared library must have CET support.

In practice, this last point might be found to be the most problematic. We found three libraries that might pose a problem in your setup:
1) libc: you can opt-in Shadow Stack support using ```export GLIBC_TUNABLES=glibc.cpu.hwcaps=SHSTK``` before running the program.
2) The libraries libgmp and libmpg123 were not compiled with CET support. While you could recompile them with it (using the ```-fcf-protection``` option, we preferred to bypass this and enforce CET via our script ```shstkenforcer.py```). We detail next how to use it to run Ladybird while actively enforcing CET.


# Building and running Ladybird
1. Our Dockerfile spawns an Ubuntu 24.04 Docker with every dependency already installed.
```sudo docker build -t vulnerable-serenityos .```

2. After this, you may run the Docker container and attach to it:
```
sudo docker run --rm --privileged --security-opt seccomp=unconfined -it -v $(pwd):/cfop -v /tmp/.X11-unix/:/tmp/.X11-unix -v ~/.Xauthority:/root/.Xauthority:rw -v ~/.Xauthority:/home/ubuntu/.Xauthority:rw -e DISPLAY=$DISPLAY -e XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR -v $XDG_RUNTIME_DIR:$XDG_RUNTIME_DIR --net=host vulnerable-serenityos

docker exec -it <id> /bin/bash
```

3. Once in the container, you can build and run Ladybird
```
./Meta/serenity.sh run lagom ladybird
```

Alternatively, it is possible to debug ladybird too:
```
./Meta/serenity.sh gdb lagom ladybird
```

In addition, once Ladybird has been built at least once, CET's Shadow Stack can be runtime enforced using our script:
```
python3 Meta/shstkenforcer.py
```

# Running the CFOP exploit
Once Ladybird is running, the GUI will be shown in screen. 
At this moment, we can navigate to the URL ```file:///cfop/Base/home/anon/exploit.html```.

Upon visiting this website, the command line will leak some address. 
This address is needed to be entered in the browser input as to run the exploit.
As a result of running the exploit, the name of the current user will be printed on screen three times (executing *execve("whoami")*). 


# Notes on running the SerenityOS exploit
Ladybird runs with ASLR disabled, and inside our supplied Docker container, so every user of this exploit will find the internal addresses to be valid - and thus the exploit to be working. 

In case the exploit would not work (e.g., to port this exploit to a different ScyllaDB exploit or a different system), the address corresponding to execve() would need to be updated (see ```exploit.html```).