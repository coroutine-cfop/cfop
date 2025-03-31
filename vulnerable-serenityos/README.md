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

## Requirements
We test this experiment in a machine with a 20-core i9-12900H CPU and 32GB of RAM. We used an Ubuntu 24.04 machine. Whilst the build happens inside Docker, the Ladybird browser has a GUI, so it is necessary that the host machine has a X11 server. In Linux, we recommend using *Xorg*, whilst we have also tested this in Windows using *vcxsrv*.

## Setup
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


## Building and running Ladybird
1. Our Dockerfile spawns an Ubuntu 24.04 Docker with every dependency already installed.
```sudo docker build -t vulnerable-serenityos .```

2. After this, you may run the Docker container and attach to it:
```
sudo docker run --rm --privileged --security-opt seccomp=unconfined -it -v $(pwd):/cfop -v /tmp/.X11-unix/:/tmp/.X11-unix -v ~/.Xauthority:/root/.Xauthority:rw -v ~/.Xauthority:/home/ubuntu/.Xauthority:rw -e DISPLAY=$DISPLAY -e XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR -v $XDG_RUNTIME_DIR:$XDG_RUNTIME_DIR --net=host vulnerable-serenityos
```

3. Once in the container, switch to user 'ubuntu'; then build and run Ladybird
```
usermod -u 1001 ubuntu

su ubuntu

cd cfop

export SERENITY_SOURCE_DIR=/cfop

./Meta/serenity.sh run lagom ladybird
```

## Running the CFOP exploit
Once Ladybird is running, the GUI will be shown in screen. 
At this moment, we can navigate to the URL ```file:///cfop/Base/home/anon/exploit.html```.

Upon visiting this website, the command line will leak some address. 
This address is needed to be entered in the browser input as to run the exploit.
As a result of running the exploit, the name of the current user will be printed on screen three times (executing *execve("whoami")*). 


## Notes on running the SerenityOS exploit
Ladybird runs with ASLR disabled, and inside our supplied Docker container, so every user of this exploit will find the internal addresses to be valid - and thus the exploit to be working. 

In case the exploit would not work (e.g., to port this exploit to a different ScyllaDB exploit or a different system), the address corresponding to execve() would need to be updated (see ```exploit.html```).

Alternatively, it is possible to debug ladybird too:
```
./Meta/serenity.sh gdb lagom Ladybird
```

In addition, once Ladybird has been built at least once, CET's Shadow Stack can be runtime enforced using our script:
```
python3 Meta/shstkenforcer.py
```

## Appendix: Running the SerenityOS exploit in a remote machine over SSH
The Ladybird application is a web browser with a GUI, meaning that the system needs to proxy X11 twice:
1) From inside the docker running Ladybird, to the remote machine host accessed via SSH
2) From the remote machine host, to your own machine you are ssh-ing from

The system is prepared to manage the first proxy (this is done with the arguments docker is run with), but the second X11 forwarding must be started by the evaluator:
1) If your own machine is Linux, then you must add the flag ```-Y``` to your ssh command:
```ssh -Y reviewer@10.17.130.180```
2) If your own machine is Windows, then we recommend using Putty and vcxsrv as your X11 server. 
    * Activate vcxsrv, and check on its logs the DISPLAY variable (usually, 127.0.0.1:0.0). Logs are found after right-clicking the toolbar icon (after launching vcxsrv, it appears under hidden icons), then selecting "Show logs".
    * You can then setup the X11 forwarding in Putty under Connection->SSH->X11. Click on "Enable X11 forwarding" and write the value of the DISPLAY variable in the field "X display location". Then, start the SSH connection.

We strongly recommend not using WSL for the evaluation, as we found some buggy behaviour when using it.

At any point during the evaluation (in your own machine, in the remote machine, and finally inside the Ladybird docker), it is possible to run the command ```xeyes``` to test if the X11 forwarding works correctly. 