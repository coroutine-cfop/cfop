# CFOP: Coroutine Frame-Oriented Programming -- Clang PoC
This README details how to run our Coroutine Frame-Oriented Programming (CFOP) PoC.
This PoC demonstrates one of the main techniques under CFOP: how to achieve arbitrary code execution exploiting coroutines (calling arbitrary functions with arbitrary arguments).

Note: this is a minimal reproducible example with a single arbitrary call, but it is possible to create exploits with an infinite number of arbitrary calls too.

## PoC Explanation
The program ```clangpoc``` is a very simple program using nested coroutines.
This program features one buffer that can be overflown via a buffer overflow vulnerability. This overflow overwrites critical coroutine data (the coroutine frame), which we exploit for our attack. 

We make use of multiple hijacked ```resume``` and ```destroy``` pointers, together with other coroutine frame objects, to achieve code reuse. During this process, using a _silver gadget_, the exploit sets the needed register values according to the call convention and calls the destination function ```execve()```.

Our script ```clangpocexploit.py``` can be used to start an instance of ```clangpoc``` and launch our exploit. A successful exploitation will result in the program printing _"ARBITRARY CODE EXECUTION!"_ on screen, even if this code is not present in the original program.

Note: the exploited program is just an example. The coroutine program does not necessarily need to feature three nested coroutines for an exploit to exist, and does not necessarily need to be using symmetric transfer (asymmetric is also vulnerable). All versions of Clang which support coroutines are vulnerable, here we target the latest. We recommend reading Section 3 of our paper for complete detail of every possible attack.

## Building and Running in Docker
We provide a pre-built Ubuntu 24.04 docker image for testing the PoC in a prepared container.
This container comes with a clang-19 toolchain along with some other python tools (e.g., pwntools) for running our automated exploit script. We also disabled ASLR in the system.

In order to run the PoC in the docker image, you should follow the next steps:
1. Build the docker image (pulls our pre-built image from dockerhub and loads PoC files under ```/opt/pocs```)
```docker build -t cfop_clang_poc .```
2. Run the docker container
```docker run --privileged --security-opt seccomp=unconfined -it cfop_clang_poc```
3. Once inside the container, navigate to where the PoC files are saved
```cd opt/pocs/```
4. Compile the coroutine program
```make```
5. Run the exploit script
```python3 clangpocexploit.py```


