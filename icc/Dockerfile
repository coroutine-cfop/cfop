FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y wget software-properties-common && \
    apt-get install -y make && \
    apt-get install -y gdb && \
    apt-get install -y tmux && \
    apt-get install -y curl && \
    apt-get install -y file && \
    apt-get install -y gdbserver && \
    apt-get install -y nano && \
    apt-get install -y python3 python3-pip python3-dev git libssl-dev libffi-dev build-essential &&\
    add-apt-repository ppa:ubuntu-toolchain-r/test -y && \
    apt-get update && \
    apt-get install -y gcc-14 g++-14

RUN python3 -m pip install --upgrade pwntools --break-system-packages

RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-14 100 && \
    update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-14 100

ENTRYPOINT ["sh", "-c", "echo 0 | tee /proc/sys/kernel/randomize_va_space && exec \"$@\"", "--"]
CMD ["/bin/bash"]