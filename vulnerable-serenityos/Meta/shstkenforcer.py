from pwn import *

# This script enforces SHSTK use on Ladybird, using some tricks, without shared library modification.
binary = '../Build/lagom/bin/Ladybird'

gdbscript = f'''
set follow-fork-mode parent
b main
commands
    b launch_generic_server_process
    commands
        del
        b launch_generic_server_process
        commands
            set follow-fork-mode child
            b *0x7ffff7fdcca9
            commands
                set *0x7ffff7ffe068 = 0x2
                del
            end
        end
    end
end
c
'''

# Attach GDB with the script
p = gdb.debug(binary, gdbscript=gdbscript)

# Interact with the process
p.interactive()