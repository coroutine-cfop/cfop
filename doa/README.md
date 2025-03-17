# CFOP: Coroutine Frame-Oriented Programming -- DoA PoC
This README details how to run our CFOP Data-Only Attack DPoC (DOA).
This PoC demonstrates how an attacker can open and read an arbitrary file without overwriting the coroutine frame *resume* or *destroy* pointers (it is a 0 CFP attack).

## PoC Explanation
The program ```fileopening``` is a very simple program reading from a file - whose name is hardcoded in the program.
This program features one buffer that can be overflown via a buffer overflow vulnerability. This overflow overwrites critical coroutine data (the coroutine frame), which we exploit for our attack. 

We overwrite the internal data of the coroutine frame - without tampering with the *resume* or *destroy* pointers - in order to hijack the name of the file being opened. As a result, an attacker may read the contents of an arbitrary file.

Our script ```fileopening.py``` can be used to start an instance of ```fileopening``` and launch our exploit. A successful exploitation will result in the program printing the contents of the file ```/etc/hosts``` on screen, even when this filename was not present in the original program.

## Requirements
We test this experiment in a machine with a 20-core i9-12900H CPU and 32GB of RAM. We used an Ubuntu 24.04 machine. Docker is the only software requirement.

## Building and Running in Docker
We provide a pre-built Ubuntu 24.04 docker image for testing the PoC in a prepared container.
This container comes with a gcc-14.2 toolchain along with some other python tools (e.g., pwntools) for running our automated exploit script. We also disabled ASLR in the system.

In order to run the PoC in the docker image, you should follow the next steps:
1. Build the docker image (pulls our pre-built image from dockerhub and loads PoC files under ```/opt/pocs```)
```docker build -t cfop_doa_poc .```
2. Run the docker container
```docker run --privileged --security-opt seccomp=unconfined -it cfop_doa_poc```
3. Once inside the container, navigate to where the PoC files are saved
```cd opt/pocs/```
4. Compile the coroutine program
```make```
5. Run the exploit script
```python3 fileopening.py```

## Notes on active CET enforcement
You can opt-in Shadow Stack support using ```export GLIBC_TUNABLES=glibc.cpu.hwcaps=SHSTK``` before running the program.
