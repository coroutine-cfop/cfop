# CFOP: Coroutine Frame-Oriented Programming -- ICC PoC
This README details how to run our Coroutine Frame-Oriented Programming (CFOP) PoC.
This PoC demonstrates one of the main techniques under CFOP: Infinite Coroutine Chaining (building a chain to call multiple arbitrary functions).

## Building and Running in Docker
We provide a Ubuntu 24.04 docker image for testing the PoC in a prepared container.
This container comes with a gcc-14 toolchain along with some other python tools (e.g., pwntools) for running our automated exploit script. We also disabled ASLR in the system (for simplicity).

In order to run the PoC in the docker image, you should follow the next steps:
1. Build the docker image (pulls our pre-built image from dockerhub and loads PoC files under ```/opt/pocs```)
```docker build -t cfop_icc_poc .```
2. Run the docker container
```docker run --privileged --security-opt seccomp=unconfined -it -v $(pwd)/src:/cfop cfop_icc_poc```
3. Once inside the container, navigate to where the PoC files are saved
```cd /cfop```
4. Start tmux
```tmux```
6. Compile the coroutine program
```make```
7. Run the exploit script
```python3 icc.py```


As a result of the successful exploitation, six different calls to a function that prints "called arbitrary function!" should be visible on screen.

Note: For simplicity we didn't set any arguments in this case, but it would be as simple as finding a golden/silver gadget or pivoting only rdi.