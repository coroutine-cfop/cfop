# CFOP: Coroutine Frame-Oriented Programming -- PoCs repository
This repository contains a collection of PoCs that demonstrate the different techniques of Coroutine Frame-Oriented Programming (CFOP). This includes: (1) a mix of C++ coroutine programs, that resemble simple, yet exploitable programs when using CFOP; and (2) a series of python scripts for running different exploits on this programs, using PwnTools. 

To enhance reproducibility, some of the PoCs in this repository are dockerized - it is possible to run them on a Docker container, as to guarantee the same setup as they were first built. In the near future, and before the artifact submission, it is our intention to dockerize every single PoC here. In addition, more PoCs may be submitted to the final artifact evaluation - this is just a collection of the most relevant ones.

## Building and Running in Docker
For the PoCs under ```clang``` and ```gcc``` folders, we provide a pre-built Ubuntu 24.04 docker image for testing the PoC in a prepared container. These container comes with a default (unmodified) compiler toolchain along with some other python tools (e.g., pwntools) for running our automated exploit scripts. Specific instructions for running each PoC are detailed under each of them.

In general, the steps for running one of the dockerized exploit scripts is:
1. Build the docker image (pulls our pre-built image from dockerhub and loads PoC files under ```/opt/pocs```)

```docker build -t <docker-name> .```

2. Run the docker container

```docker run --privileged --security-opt seccomp=unconfined -it <docker-name>```

3. Once inside the container, navigate to where the PoC files are saved

```cd opt/pocs/```

4. Compile the coroutine program(-s)

```make```

5. Run the exploit script

```python3 <exploit>.py```

## Running standalone scripts
For those PoCs that are not dockerized just yet, we are still providing the code for transparency and reference - but their reproducibility is more limited due to the discrepances between the system they were built and tested and your own system. Even so, the exploit payload consists of a collection of named variables, so it is readable and not just a single string of hexadecimal symbols.

In general, the steps for running one of the undockerized exploit scripts is:
1. Compile the program

```gcc -g -O3 -std=c++20 -fcf-protection=full <code> -o <program>```

```clang -g -O3 -std=c++20 -fcf-protection=full <code> -o <program>```

2. Run the exploit scripts

```python3 <exploit>.py```

## PoCs Explanation
A more detailed explanation of each PoC is enclosed with each of the dockerized PoCs. 
The following is a summary of the purpose of each PoC:

### ```clangexecve.py```
It shows how to use a silver gadget to set 4 arbitrary argument registers and then call an arbitrary function - in this case ```execve```.

### ```gccexecve.py```
It shows how to use a silver gadget to set 4 arbitrary argument registers and then call an arbitrary function - in this case ```execve```.

### ```callexec.py```
It shows the most basic execution hijacking, redirecting the execution to an arbitrary function already existing in the program - in this case ```system```.

### ```contjumping.py```
It shows how to perform Infinite Coroutine Chaining (ICC), jumping multiple times between serveral coroutines.

### ```fileopening.py```
It shows an example of Data-Only Attack (DOA), modifying the variables with which the program works with, resulting in unintended consequences (reading from privileged files).


---
Note: the exploited programs are always just an example and not representative of the minimum requirements for the attack to take place. The coroutine program does not necessarily need to be using symmetric transfer or asymmetric transfer. All versions of GCC and Clang which support coroutines are vulnerable, here we target the latest. We recommend reading Section 3 of our paper for complete detail of every possible attack.