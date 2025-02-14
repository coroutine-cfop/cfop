FROM ubuntu:24.04

#WORKDIR /app

RUN apt-get update && \
    apt-get install -y gdb && \
    apt-get install -y nano sudo curl gcc make cmake git g++ python3 build-essential qt6-base-dev libgl1-mesa-dev ninja-build qt6-base-dev qt6-tools-dev-tools qt6-multimedia-dev ccache libxkbcommon-dev libxkbfile-dev x11-apps pip libmagic-dev file python3-dev libssl-dev libffi-dev build-essential xterm gdbserver

RUN echo "ubuntu:ubuntu" | chpasswd && \
    usermod -aG sudo ubuntu 

RUN pip3 install file --break-system-packages

RUN pip3 install pwntools --break-system-packages

ENTRYPOINT ["sh", "-c", "echo 0 | tee /proc/sys/kernel/randomize_va_space && exec \"$@\"", "--"]
CMD ["/bin/bash"]
