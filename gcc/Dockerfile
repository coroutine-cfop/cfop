FROM cispacfop/cfop_gcc_poc:1.0.0

COPY src /opt/pocs

ENTRYPOINT ["sh", "-c", "echo 0 | tee /proc/sys/kernel/randomize_va_space && exec \"$@\"", "--"]
CMD ["/bin/bash"]
